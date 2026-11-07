"""Validate frozen anonymous reviews and report descriptive results, never P/R/F1."""
import json
from collections import Counter
from pathlib import Path

RUN=Path(__file__).resolve().parent


def load(path):return json.loads(path.read_bytes())
def require(condition,message):
    if not condition:raise ValueError(message)
def sha(raw):
    import hashlib
    return hashlib.sha256(raw).hexdigest()
def indexed(items,key):
    require(isinstance(items,list),'Review arrays required')
    result={item[key]:item for item in items}
    require(len(result)==len(items),'Duplicate review key: '+key)
    return result


def reachability(model):
    pairs={(g['parent_id'],c) for g in model['refinement_groups'] if g['status']=='supported' and g['completeness']=='complete' for c in g['child_ids']}
    closure=set(pairs)
    while True:
        extra={(a,d) for a,b in closure for c,d in closure if b==c and a!=d}-closure
        if not extra:break
        closure.update(extra)
    return len(pairs),len(closure)


def main():
    review_root=RUN/'evaluation/source-first-review';manifest_path=review_root/'freeze-manifest.json';freeze=load(manifest_path)
    inventories={}
    for item in freeze['inventories']:
        path=review_root/item['inventory_path'];raw=path.read_bytes()
        require(sha(raw)==item['inventory_sha256'],'Frozen inventory changed')
        inventories[item['document_id']]=indexed(json.loads(raw)['intents'],'intent_id')
    records=[];bindings=[]
    for round_name in ('first','repeat'):
        mapping=load(RUN/'evaluation'/('blinding-map-'+round_name+'.json'))
        require(mapping['inventory_manifest_sha256']==sha(manifest_path.read_bytes()),'Review freeze binding mismatch')
        for selected in mapping['records']:
            doc,label=selected['document_id'],selected['label'];packet_path=RUN/selected['anonymous'];packet_raw=packet_path.read_bytes()
            require(sha(packet_raw)==selected['anonymous_sha256'],'Anonymous packet changed')
            packet=json.loads(packet_raw);model_path=RUN/selected['source_model'];model_raw=model_path.read_bytes()
            require(sha(model_raw)==selected['source_sha256'],'Initial delivered model changed')
            model=json.loads(model_raw);review_path=review_root/doc/('review-'+round_name+'.json');review=load(review_path)
            require(review['document_id']==doc,'Review document mismatch')
            samples=indexed(review['samples'],'sample');sample=samples[round_name+':'+label]
            intents=indexed(sample['intent_matches'],'intent_id');goals=indexed(sample['goal_assessments'],'goal_id')
            relations=indexed(sample['relation_assessments'],'relation_id');groups=indexed(sample['group_assessments'],'group_id')
            packet_goals={g['id'] for g in packet['goals']}
            require(set(intents)==set(inventories[doc]),'Each source inventory intent needs a review: '+doc)
            require(set(goals)==packet_goals,'Each goal needs exactly one review: '+doc)
            require(set(relations)=={r['id'] for r in packet['relations']} and set(groups)=={g['id'] for g in packet['groups']},'Each relation/group needs review')
            for item in intents.values():
                require(item['status'] in {'complete','partial','absent','uncertain'} and item['rationale'].strip(),'Invalid source intent review')
                require(len(item['goal_ids'])==len(set(item['goal_ids'])) and set(item['goal_ids'])<=packet_goals,'Unknown/duplicate matched goals')
                require(item['status']!='complete' or bool(item['goal_ids']),'Complete match needs goals')
            for item in goals.values():
                require(item['judgment'] in {'supported','needs_revision','uncertain'} and item['rationale'].strip(),'Invalid goal judgment')
                require(set(item['intent_ids'])<=set(inventories[doc]),'Unknown source intent; keep errata separate')
                require(isinstance(item['issues'],list),'Goal issues must be an array')
                for issue in item['issues']:
                    require(issue['category'] in {'compound','over_split','condition_loss','strength','selected_means_loss','unsupported','background','other'} and issue['reason'].strip(),'Invalid issue')
            for item in list(relations.values())+list(groups.values()):
                require(item['judgment'] in {'consistent','needs_revision','uncertain'} and item['rationale'].strip(),'Invalid relation/group judgment')
            direct,closure=reachability(model)
            records.append(dict(document_id=doc,round=round_name,branch=selected['branch'],sample=round_name+':'+label,
                goals=len(model['goals']),relations=len(model.get('relations',[])),groups=len(model['refinement_groups']),
                active_groups=sum(g['status']=='supported' and g['completeness']=='complete' for g in model['refinement_groups']),
                source_inventory_units=len(intents),intent_matches=dict(Counter(i['status'] for i in intents.values())),
                goal_judgments=dict(Counter(i['judgment'] for i in goals.values())),
                goal_issue_categories=dict(Counter(issue['category'] for item in goals.values() for issue in item['issues'])),
                relation_judgments=dict(Counter(i['judgment'] for i in relations.values())),group_judgments=dict(Counter(i['judgment'] for i in groups.values())),
                refinement_direct_goal_pairs=direct,refinement_reachable_pairs=closure,
                original_model=selected['source_model'],review=str(review_path.relative_to(RUN))))
            bindings.append(dict(document_id=doc,branch=selected['branch'],model_sha256=sha(model_raw),anonymous_sha256=sha(packet_raw),review_sha256=sha(review_path.read_bytes())))
    arms={}
    for branch in ('baseline','candidate','baseline-repeat','candidate-repeat'):
        rows=[r for r in records if r['branch']==branch]
        require(len(rows)==8,'Eight documents required per run')
        aggregate={key:sum(r[key] for r in rows) for key in ('goals','relations','groups','active_groups','source_inventory_units')}
        for key in ('intent_matches','goal_judgments','goal_issue_categories','relation_judgments','group_judgments'):
            counter=Counter()
            for row in rows:counter.update(row[key])
            aggregate[key]=dict(counter)
        arms[branch]=aggregate
    result=dict(schema_version='goalforge-descriptive-forward-comparison-1',validation='passed',documents=records,arms=arms,bindings=bindings,
        inventory_manifest_sha256=sha(manifest_path.read_bytes()),source_inventory='isolated model review, not human Gold',
        limitations=['Two context-isolated runs per branch; model/temperature/token/cost controls unavailable.',
                    'End-to-end development comparison, not mechanism ablation or unseen holdout.',
                    'Source inventory and judgments are model assessments; no precision/recall/F1 or significance claim.',
                    'Goal count is grain/coverage information, not a quality score. Structural reachability is not new semantic evidence.',
                    'Generation and review outputs remain frozen; repairs are separate versions.'])
    output=RUN/'evaluation/metrics.json'
    with output.open('x',encoding='utf-8') as handle:json.dump(result,handle,ensure_ascii=False,indent=2)
    lines=['# 八篇访谈开发前向对比','','两次隔离上下文运行，保留全部首次结果；源文优先清单在匿名结果之前冻结。它是模型评审判断，不是人工Gold，也不计算标准P/R/F1。','',
           '| 分支 | 目标 | 联系 | 候选组 | 成立组 | 清单完整对应 | 部分 | 未对应 | 不确定 | 建议修改目标 | 不确定目标 |',
           '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for name,row in arms.items():
        m,j=row['intent_matches'],row['goal_judgments']
        lines.append('| '+name+' | '+' | '.join(str(v) for v in [row['goals'],row['relations'],row['groups'],row['active_groups'],m.get('complete',0),m.get('partial',0),m.get('absent',0),m.get('uncertain',0),j.get('needs_revision',0),j.get('uncertain',0)])+' |')
    lines+=['','每行的原文清单分母均为129个模型评审单元。允许多个目标共同承接一个单元；清单本身的遗漏单列errata，不根据模型改写冻结清单。问题类别条数可能多于问题目标数，不相加当错误率。','',
            '| 文档 | 基线目标（首次/重复） | 新版目标（首次/重复） | 首轮评审 | 重复评审 |','|---|---:|---:|---|---|']
    for doc in inventories:
        rows={r['branch']:r for r in records if r['document_id']==doc}
        lines.append('| '+doc+' | '+str(rows['baseline']['goals'])+'/'+str(rows['baseline-repeat']['goals'])+' | '+str(rows['candidate']['goals'])+'/'+str(rows['candidate-repeat']['goals'])+
                     ' | [逐项判断](source-first-review/'+doc+'/review-first.json) | [逐项判断](source-first-review/'+doc+'/review-repeat.json) |')
    lines+=['','目标数变化不能直接解释为质量提升。两次样本只描述本轮差异与波动；无法控制的模型、预算和成本如实unknown。联系和充分精化分别评价，精化可达关系不回填成直接依据。','',
            '完整计数与实际文件绑定见[metrics.json](metrics.json)，方法及补充重复登记见[protocol.md](protocol.md)。首次结果保留，修复版另存，机器检查报告不被改写成独立语义通过或人工采纳。','']
    with (RUN/'evaluation/对比结果.md').open('x',encoding='utf-8') as handle:handle.write('\n'.join(lines))
    print(json.dumps(dict(status='passed',samples=len(records),arms=arms),ensure_ascii=False))


if __name__=='__main__':main()
