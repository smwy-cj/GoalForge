"""Build inspectable comparisons from authored judgments and frozen artifacts."""
import csv
import hashlib
import json
import runpy
import statistics
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

RUN=Path(__file__).resolve().parent
ROOT=RUN.parents[1]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,x):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def lines(p,x):p.write_text(''.join(json.dumps(a,ensure_ascii=False)+'\n' for a in x),encoding='utf-8')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def clean(s):return str(s).replace('|','／').replace('\n',' ')
def canonical_turns(packet,e):
    return [f"T{int(t['turn']):03}" for t in packet['source'] if t['start_char']<=e['start_char']<=t['end_char']]

def benchmark_metrics():
    keys={x['case_id']:x for x in read(RUN/'relation-benchmark-key.json')}
    preds=read(RUN/'relation-calibration-predictions.json')+read(RUN/'relation-evaluation-predictions.json')
    scored=[{**keys[x['case_id']],**x,'correct':x['prediction']==keys[x['case_id']]['reference']} for x in preds]
    results={}
    for split in ['calibration','consensus_evaluation','single_rater_evaluation']:
        rows=[x for x in scored if x['split']==split]
        resolved=[x for x in rows if x['prediction']!='UNCERTAIN']
        class_stats={}
        for label in ['REFINES','REFINED_BY','NONE','EQUIV']:
            tp=sum(x['reference']==label and x['prediction']==label for x in resolved)
            fp=sum(x['reference']!=label and x['prediction']==label for x in resolved)
            fn=sum(x['reference']==label and x['prediction']!=label for x in resolved)
            if tp+fp+fn:
                class_stats[label]={'tp':tp,'fp':fp,'fn':fn,'precision':tp/(tp+fp) if tp+fp else None,
                                    'recall':tp/(tp+fn) if tp+fn else None,'f1':2*tp/(2*tp+fp+fn)}
        conf=Counter((x['reference'],x['prediction']) for x in rows)
        results[split]={'n':len(rows),'resolved':len(resolved),'abstained':len(rows)-len(resolved),
              'coverage':len(resolved)/len(rows),'correct':sum(x['correct'] for x in rows),
              'exact_agreement_all_including_abstentions_in_denominator':sum(x['correct'] for x in rows)/len(rows),
              'resolved_exact_agreement':sum(x['correct'] for x in resolved)/len(resolved) if resolved else None,
              'per_class_on_resolved':class_stats,
              'confusion':[{'reference':a,'prediction':b,'n':n} for (a,b),n in conf.items()]}
    swap=read(RUN/'order_swap_decisions.json')
    primary={x['case_id']:x['prediction'] for x in preds}
    flip={'REFINES':'REFINED_BY','REFINED_BY':'REFINES','NONE':'NONE','UNCERTAIN':'UNCERTAIN','EQUIV':'EQUIV'}
    results['same_context_order_swap']={'n':len(swap),'consistent':sum(flip[x['prediction']]==primary[x['case_id']] for x in swap),
                                      'independent_reviewer':False,'scope':'same Codex reviewer and context; consistency only'}
    write(RUN/'relation-benchmark-scored.json',scored)
    return results

def main():
    authored=runpy.run_path(str(RUN/'semantic_decisions.py'))
    amendments=runpy.run_path(str(RUN/'review_amendments.py'))['AMENDMENTS']
    decisions={k:list(v) for k,v in authored['DECISIONS'].items()}
    rechecks=[]
    for doc,gid,status,note in amendments:
        i=next(i for i,row in enumerate(decisions[doc]) if row[0]==gid)
        old=decisions[doc][i]
        decisions[doc][i]=(*old[:3],status,note)
        rechecks.append({'document_id':doc,'local_id':f'{doc}-G{gid:03}','old_support':old[3],
                        'new_support':status,'old_rationale':old[4],'new_rationale':note,
                        'review_type':'same-reviewer expanded-source-context; not independent'})
    manifest=read(RUN/'input-manifest.json')
    changed=[x['path'] for x in manifest['files'] if not (ROOT/x['path']).exists() or digest(ROOT/x['path'])!=x['sha256']]
    assert not changed,changed
    audit=read(RUN/'audit-results.json')
    audit_by={x['document_id']:x for x in audit['documents']}
    graph_audit=read(RUN/'paper-graph-audit.json')
    paper_graphs=read(RUN/'inputs/paper/study1/data1/graphs.json')
    ga={(x['document_id'],x['run_index']):x for x in graph_audit['runs']}
    alignments,paper_records,relations,documents=[],[],[],[]
    issue_candidates=[]
    for doc,rows in sorted(decisions.items()):
        packet=read(RUN/'packets'/f'{doc}.json')
        gs={int(g['goal_id'].split('-G')[-1]):g for g in packet['local_goals']}
        assert set(gs)=={x[0] for x in rows} and len(rows)==len(gs)
        paper={x['paper_id']:x['statement'] for x in packet['paper_goals']}
        reverse=defaultdict(list)
        local_records=[]
        mapping={}
        for gid,ref_ids,rel,support,note in rows:
            g=gs[gid];pids=[f'g{i}' for i in ref_ids]
            assert all(x in paper for x in pids)
            mapping[g['goal_id']]=pids
            for pid in pids:reverse[pid].append(g['goal_id'])
            ev=[{'evidence_id':e['evidence_id'],'quote':e['quote'],'source_turn_ids':canonical_turns(packet,e),
                 'start_char':e['start_char'],'end_char':e['end_char']} for e in g['quotes']]
            row={'document_id':doc,'local_id':g['goal_id'],'local_statement':g['statement'],
                 'local_origin':g['origin'],'local_trace_status':g['trace_status'],
                 'local_context':g.get('context',[]),'paper_ids':pids,'paper_statements':[paper[p] for p in pids],
                 'correspondence':rel,'split_merge':len(pids)>1,'source_support_judgment':support,'rationale':note,
                 'evidence':ev,'reviewer':'Codex automatic semantic review',
                 'review_scope':'full transcript' if doc in authored['PILOT_PAPER_ONLY'] else 'attached source excerpts; focused context for selected issues',
                 'not_a_gold_label':True}
            local_records.append(row);alignments.append(row)
            if support not in ['supported','supported_with_scope_note']:
                issue_candidates.append({'document_id':doc,'local_id':g['goal_id'],'kind':support,'rationale':note,'evidence':ev})
        unmatched=[]
        for pid,text in paper.items():
            n=int(pid[1:]);review=authored['PILOT_PAPER_ONLY'].get(doc,{}).get(n)
            item={'document_id':doc,'paper_id':pid,'statement':text,'local_ids':reverse[pid],
                  'correspondence_status':'has_correspondence' if reverse[pid] else 'paper_only',
                  'source_support_assessment':'via_correspondence_not_independent' if reverse[pid] else (review[0] if review else 'not_assessed'),
                  'source_turns':review[1] if review else None,'rationale':review[2] if review else None}
            paper_records.append(item)
            if not reverse[pid]:unmatched.append(item)
        key=str(int(doc[3:]));per_run=[]
        for ix,(nodes,edges,implied) in enumerate(paper_graphs[key]):
            check=ga[doc,ix]
            per_run.append({'run_index':ix,'nodes':nodes,'edges':set(map(tuple,edges)),
                            'closure':set(map(tuple,check['closure'])),'eligible':check['dag'] and not check['base_goal_mismatches']})
        model=read(ROOT/'output'/doc/'final/goal-model.json')
        local_ref={(x['parent_id'],x['child_id']) for x in model['edges'] if x['type']=='refinement'}
        for pair in model['pair_decisions']:
            a,b=pair['a'],pair['b']
            directions=[]
            for parent,child in [(a,b),(b,a)]:
                candidates=[(x,y) for x in mapping[parent] for y in mapping[child] if x!=y]
                eligible=[x for x in per_run if x['eligible']]
                strict=bool(len(mapping[parent])==len(mapping[child])==1 and
                    next(x for x in local_records if x['local_id']==parent)['correspondence']=='equivalent' and
                    next(x for x in local_records if x['local_id']==child)['correspondence']=='equivalent' and
                    len(reverse[mapping[parent][0]])==len(reverse[mapping[child][0]])==1)
                directions.append({'parent':parent,'child':child,'local_refinement':(parent,child) in local_ref,
                    'paper_endpoint_candidates':[list(t) for t in candidates],
                    'comparison_mode':'strict_equivalent_one_to_one' if strict else 'exploratory_partial_mapping',
                    'eligible_paper_runs':len(eligible),
                    'direct_edge_runs':sum(any(t in x['edges'] for t in candidates) for x in eligible) if candidates else None,
                    'closure_runs':sum(any(t in x['closure'] for t in candidates) for x in eligible) if candidates else None,
                    'interpretation':'structural correspondence only; presence is not ground-truth correctness'})
            relations.append({'document_id':doc,'decision_id':pair['pair_id'] if 'pair_id' in pair else pair.get('decision_id'),
                'local_pair':[a,b],'local_label':pair['label'],'directions':directions,
                'semantic_review_scope':'only explicitly listed source-based relation reviews; remaining pairs not independently rejudged'})
        doc_result={'document_id':doc,'review_status':'first_pass_complete','local_goals':local_records,
           'paper_only':unmatched,'source_review_limits':'Local-goal correspondence is complete; paper-only support outside pilot is not exhaustively judged.',
           'counts':{'local_goals':len(rows),'local_with_correspondence':sum(bool(x['paper_ids']) for x in local_records),
                     'paper_goals':len(paper),'paper_with_correspondence':len(reverse.keys() & {p for p in reverse if reverse[p]}),
                     'paper_only':len(unmatched),'local_only':sum(not x['paper_ids'] for x in local_records)},
           'local_refinement_count':len(local_ref),'eligible_paper_runs':sum(x['eligible'] for x in per_run),
           'relation_semantic_reviews':[x for x in authored['RELATION_REVIEWS'] if x['document_id']==doc],
           'rubric':{'why_how_hierarchy':'partial' if local_ref else 'insufficient_expression',
                      'kaos_refinement_groups':'not_expressed_in_old_schema',
                      'full_group_sufficiency':'not_assessed','alternatives_completeness':'not_assessed',
                      'source_locations':'supported_by_deterministic_checks','human_or_independent_review':'not_run'}}
        documents.append(doc_result)
        write(RUN/'per-document'/f'{doc}.json',doc_result)
        md=[f'# {doc} 目标与关系比对','',
            '评价类型：Codex 自动语义评审；局部源文支持判断不等于完整人工 Gold。',
            f"本地 {len(rows)} 个目标；论文建模前 {len(paper)} 个目标。全部10次论文图均留存，DAG且基础节点文本一致的可对照运行 {doc_result['eligible_paper_runs']} 次。",'',
            '| 本地目标 | 论文对应 | 对应类型 | 源文判断 | 判断依据 |','|---|---|---|---|---|']
        md.extend(f"| {x['local_id']} {clean(x['local_statement'])} | {', '.join(x['paper_ids']) or '无'} | {x['correspondence']} | {x['source_support_judgment']} | {clean(x['rationale'])} |" for x in local_records)
        md.extend(['','## 论文单方目标','', '下表为未找到同义或包含对应的参照目标，不能直接当作本地漏提。非试点文档的单方目标未逐项完成完整源文裁决。','',
                   '| 论文ID | 原文 | 源文判断 | 理由 |','|---|---|---|---|'])
        md.extend(f"| {x['paper_id']} | {clean(x['statement'])} | {x['source_support_assessment']} | {clean(x['rationale'] or '待完整源文复核；不据此计为本地错误')} |" for x in unmatched)
        md.extend(['','## 层级与限制','',f"本地精化边 {len(local_ref)} 条；旧版模型未表达AND精化组与完整OR方案，因此共同充分性不能从二元边自动判通过。",'',
                   '逐项英文表述、证据原句、字符位置与原文轮次见同名 JSON。配对统计见 relation-comparison.jsonl；多对多映射只用于候选差异分析。'])
        (RUN/'per-document'/f'{doc}.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
    lines(RUN/'goal-alignment.jsonl',alignments)
    lines(RUN/'paper-goal-correspondence.jsonl',paper_records)
    lines(RUN/'relation-comparison.jsonl',relations)
    lines(RUN/'review-disagreements.jsonl',rechecks)
    lines(RUN/'issue-candidates.jsonl',issue_candidates)
    write(RUN/'source-based-relation-reviews.json',authored['RELATION_REVIEWS'])
    benchmark=benchmark_metrics()
    labels=read(RUN/'relation-label-profile.json')
    counts={k:sum(x['counts'][k] for x in documents) for k in documents[0]['counts']}
    stats={'date':'2026-10-22','stage':'34-document first-pass local-goal correspondence, graph comparison, selected source rechecks, evaluator pilot',
        'counts':counts,'correspondence_labels':dict(Counter(x['correspondence'] for x in alignments)),
        'reasonable_inference_labeled_explicit_in_original':sum(x['source_support_judgment']=='reasonable_inference' and x['local_origin']=='explicit' for x in alignments),
        'source_support_judgments':dict(Counter(x['source_support_judgment'] for x in alignments)),
        'paper_only_source_assessed':sum(x['correspondence_status']=='paper_only' and x['source_support_assessment']!='not_assessed' for x in paper_records),
        'paper_only_source_not_assessed':sum(x['correspondence_status']=='paper_only' and x['source_support_assessment']=='not_assessed' for x in paper_records),
        'local_deterministic':audit['totals'],'paper_graphs':graph_audit['totals'],
        'paper_dag_and_base_consistent_runs':sum(x['dag'] and not x['base_goal_mismatches'] for x in graph_audit['runs']),
        'relation_pairs_structurally_compared':len(relations),'source_based_refinement_reviews':sum('G' in x['parent'] and x['document_id'] in ['DOC003','DOC010'] for x in authored['RELATION_REVIEWS']),
        'relation_benchmark':benchmark,'reference_label_quality':{k:labels[k] for k in ['rows','double_labeled_rows','missing_rater1_rows','normalized_agreement_among_double_labeled','distinct_ordered_pairs','duplicate_groups_with_conflicting_rater2']},
        'rechecked_goals':len(rechecks),'independent_context_review':'not_run','formal_verification':'not_run',
        'paper_reported_metrics_reproduction':'not_established; current public graph/input snapshot and RQ3 notebook artifacts do not by themselves establish exact final paper score population',
        'claims_not_supported':['extraction accuracy against independent gold','causal benefit of skills','cost superiority','overall superiority to the paper'],
        'pending_work':['Full source-based adjudication of unmatched reference goals outside three pilot documents',
                        'Exact reconciliation of final paper RQ3 scoring artifact names and 77-turn source count difference',
                        'Independent-context review if required for stronger research conclusions'],
        'validation':{'frozen_input_files_unchanged':not changed,'local_goal_ids_unique':len({x['local_id'] for x in alignments})==398,
                      'local_goal_rows':len(alignments),'paper_goal_rows':len(paper_records),'no_upstream_generated_code_executed':True}}
    stats['decision_files']=[{'path':p.name,'sha256':digest(p)} for p in [RUN/'semantic_decisions.py',RUN/'review_amendments.py',RUN/'order_swap_decisions.json',RUN/'build_results.py']]
    write(RUN/'metrics.json',stats)
    with (RUN/'document-summary.csv').open('w',newline='',encoding='utf-8-sig') as f:
        fields=['document_id',*counts.keys(),'local_refinement_count','eligible_paper_runs']
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for d in documents:w.writerow({'document_id':d['document_id'],**d['counts'],'local_refinement_count':d['local_refinement_count'],'eligible_paper_runs':d['eligible_paper_runs']})
    print(json.dumps({k:v for k,v in stats.items() if k not in ['decision_files','relation_benchmark','local_deterministic']},ensure_ascii=False,indent=2))
    print('BENCHMARK',json.dumps({k:{a:b for a,b in v.items() if a in ['n','resolved','correct','coverage','resolved_exact_agreement','consistent']} for k,v in benchmark.items()},ensure_ascii=False))

if __name__=='__main__':main()
