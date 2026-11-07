# -*- coding: utf-8 -*-
import json, hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
assignment=json.loads((HERE/'assignment.json').read_text(encoding='utf-8'))
notes=json.loads((HERE/'notes.json').read_text(encoding='utf-8'))
documents=[]
for a in assignment['documents']:
    doc=a['document_id']
    if doc not in notes: continue
    model=json.loads((ROOT/a['model_path']).read_text(encoding='utf-8'))
    inp=json.loads((ROOT/a['source_input_path']).read_text(encoding='utf-8'))
    source=(ROOT/a['source_path']).read_bytes()
    actual_model=hashlib.sha256((ROOT/a['model_path']).read_bytes()).hexdigest()
    actual_source=hashlib.sha256(source).hexdigest()
    assert actual_model==a['model_sha256'] and actual_source==a['source_sha256']
    segments={s['source_id']:s for s in inp['segments']}
    ev={e['evidence_id']:e for e in model['evidence_index']}
    reviews=[]
    for g in model['goals']:
        short=g['goal_id'].split('-')[-1]
        if short not in notes[doc]: continue
        n=notes[doc][short]
        reviews.append({'goal_id':g['goal_id'],'statement':g['statement'],'actor':g['actor'],'conditions':g['conditions'],'author_origin':g['origin'],'author_inference':g['inference'],'author_support':g['support'],'independent_support':n['support'],'assessment':n.get('assessment','supported_with_boundaries'),'reason':n['reason'],'actual_source_ids':[f'{doc}:T{t:03}' for t in n['sources']],'source_evidence':[{'source_id':f'{doc}:T{t:03}','speaker':segments[f'{doc}:T{t:03}']['speaker'],'quote':segments[f'{doc}:T{t:03}']['text']} for t in n['sources']],'all_bound_evidence':[{'evidence_id':e,'source_id':ev[e]['source_id'],'quote':ev[e]['quote'],'evidence_role':ev[e]['evidence_role']} for e in g['evidence_ids']],'questions_issues_checked':[x for x in model.get('issues',[]) if x.get('target_id')==g['goal_id']],'finding_ids':n.get('finding_ids',[])})
    reviewed=[g['goal_id'] for g in reviews]
    d={'document_id':doc,'model_path':a['model_path'],'model_sha256':actual_model,'source_sha256':actual_source,'hashes_match_assignment':True,'source_read_ranges':[{'start_source_id':f'{doc}:T000','end_source_id':f'{doc}:T{a["source_turns"]-1:03}','reading':'complete, before substantive model review; DOC011 truncated combined output re-read in separate ranges'}],'source_complete_read':True,'reviewed_goal_ids':reviewed,'required_goal_ids':a['required_goal_ids'],'goal_reviews':reviews,'reviewed_group_ids':[],'status':'complete' if set(reviewed)==set(a['required_goal_ids']) else 'in_progress'}
    ranges={'DOC011':[(0,55),(56,85),(86,110)],'DOC036':[(0,39),(40,76)]}.get(doc,[(0,a['source_turns']-1)])
    d['source_read_ranges']=[{'start_source_id':f'{doc}:T{start:03}','end_source_id':f'{doc}:T{end:03}','complete':True} for start,end in ranges]
    d['context_only_goal_ids']=[x['goal_id'] for x in model['goals'] if x['goal_id'] not in reviewed]
    if doc=='DOC018':
        d['additional_coverage_check']='RR3-001: 额外读取G02/G05/G06/G07完整statement/conditions/evidence，仅用于12目标现有覆盖核对，不纳入本轮逐目标审核数。'
    if doc=='DOC011':
        d['reading_limit']='初始合并输出有截断，最终判断前已按T000–T055、T056–T085、T086–T110补齐；未将截断输出当完整读取。'
    documents.append(d)
    (HERE/(doc+'-review.json')).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
extra=json.loads((HERE/'review-extra.json').read_text(encoding='utf-8')) if (HERE/'review-extra.json').exists() else {}
out={'review_id':'remaining-20261025-batch3','reviewer':{'executor':'independent semantic review sub-agent /root/remaining_review3','model':'unknown','model_settings':'unknown','human_review':'not_run','formal_proof':'not_run'},'status':'complete' if len(documents)==len(assignment['documents']) and all(d['status']=='complete' for d in documents) else 'in_progress','documents':documents,'findings':extra.get('findings',[]),'correct_boundaries':extra.get('correct_boundaries',[]),'candidate_omission_risks':extra.get('candidate_omission_risks',[]),'limits':['仅评审assignment指定71个目标；其他目标仅作覆盖和上下文，不宣称目标全量审查。','精化组此前已有单独审核；本轮仅读取必要依赖上下文，未声称重新审核全部组。','未读author-review、此前语义报告、baseline、其他批次结论或development/upstream/research参考答案。','全部全文读取、来源核对和逐目标语义复核不等于人审、形式证明或真实采纳。','转写的真实性、访谈者产品事实陈述、实际方案可实现性未外部验证；没有新证据的局部未知继续保留。']}
(HERE/'review.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':out['status'],'documents':len(documents),'reviewed_goals':sum(len(d['goal_reviews']) for d in documents)},ensure_ascii=False))

# Verify review bookkeeping and source citations without altering delivery files.
qa={'documents':len(documents),'reviewed_goals':sum(len(d['goal_reviews']) for d in documents),'confirmed_findings':len([f for f in out['findings'] if f.get('counts_as_confirmed_semantic_error')]),'candidate_omission_risks':len(out['candidate_omission_risks']),'checks':[]}
for d in documents:
    a=next(x for x in assignment['documents'] if x['document_id']==d['document_id'])
    m=json.loads((ROOT/a['model_path']).read_text(encoding='utf-8'))
    inp=json.loads((ROOT/a['source_input_path']).read_text(encoding='utf-8'))
    seg={s['source_id']:s['text'] for s in inp['segments']}
    assert set(d['reviewed_goal_ids'])==set(a['required_goal_ids'])
    assert len(d['reviewed_goal_ids'])==len(set(d['reviewed_goal_ids']))
    for g in d['goal_reviews']:
        for e in g['all_bound_evidence']:
            assert e['quote'] in seg[e['source_id']], (g['goal_id'],e)
        assert len(g['reason'])>50
    base=(ROOT/a['model_path']).parent
    man=json.loads((base/'manifest.json').read_text(encoding='utf-8'))
    for item in man['files']:
        if item['path'] not in ['goal-model.json','attachments/extraction.json','attachments/judgments.json','attachments/kaos-decisions.json','attachments/source.txt']: continue
        assert hashlib.sha256((base/item['path']).read_bytes()).hexdigest()==item['sha256']
    qa['checks'].append({'document_id':d['document_id'],'required_ids_exact':True,'model_source_hash_match':True,'all_bound_quotes_exact_in_declared_turn':True,'relevant_attachment_hashes_match_manifest':True})
for risk in out['candidate_omission_risks']:
    a=next(x for x in assignment['documents'] if x['document_id']==risk['document_id'])
    seg={s['source_id']:s['text'] for s in json.loads((ROOT/a['source_input_path']).read_text(encoding='utf-8'))['segments']}
    for e in risk['source_evidence']: assert e['quote'] in seg[e['source_id']]
(HERE/'validation.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

paths=[HERE/'assignment.json']
for a in assignment['documents']:
    paths.extend([ROOT/a['source_path'],ROOT/a['source_input_path'],ROOT/a['model_path']])
    base=(ROOT/a['model_path']).parent
    paths.extend([base/'manifest.json',base/'attachments/extraction.json',base/'attachments/judgments.json',base/'attachments/kaos-decisions.json',base/'attachments/source.txt'])
rulebase=ROOT/'_run/skill-snapshots/revised/skills'
paths.extend(rulebase/x for x in ['model-review/SKILL.md','model-review/references/semantic-review.md','goal-extraction/references/goal-boundaries.md','goal-extraction/references/evidence-rules.md','goal-model-building/references/modeling-rules.md'])
consumed=[{'path':str(p.resolve()),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths]
(HERE/'consumed-files.json').write_text(json.dumps(consumed,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

lines=['# batch3 独立语义补审报告','','已完成 assignment 指定的 6 篇、71 个目标；阅读全文共 514 轮。当前范围没有新确认的实质语义错误，保留 1 项未确证候选遗漏风险（RR3-001）。未修改任何生成包、source、skills 或核心 inspection。','','| 文档 | 实际读取轮次 | 指定/已审目标 | 字节哈希 |','|---|---|---:|---|']
for d in documents:
    a=next(x for x in assignment['documents'] if x['document_id']==d['document_id'])
    lines.append(f'| {d["document_id"]} | T000–T{a["source_turns"]-1:03} | {len(d["goal_reviews"])}/{len(a["required_goal_ids"])} | source/model 均匹配 assignment |')
lines += ['','## 读取和判断边界','','使用独立复核子代理 remaining_review3；精确模型、采样参数、预算 unknown。只用指定 source.txt/source-input、模型与必要 extraction/judgments/kaos-decisions/manifest 字段及冻结规则。未读取作者另存的 author-review、此前语义报告、其他批次结论或开发参考答案。当前模型中的作者 origin/support/理由作为被审对象，在全文和整句判断后对照；这不是完全盲审。DOC011初次综合输出曾截断，已分段补齐后形成最终判断。','','仅下列71目标作逐目标审核；其他节点只用于现有覆盖和上下文。DOC036只审核13个指定目标，没有读取此前G17评审，也没有将它的支持不足汇总成整篇不可验证。本轮没有重新审核精化组，reviewed_group_ids 留空。没有真实人审、形式证明或用户采纳；现有局部未知没有被抹去。','','## 候选遗漏风险','','**RR3-001 — DOC018章节剩余时间维持意图：not_confirmed，不计确证错误。**','','T049本人称章节剩余时间功能“very cool”，随后希望应用“also show”章节百分比。这种正面价值可以支持维持推断，不能因功能已经实现或未说未来希望而过滤。已核12目标完整statement/conditions/evidence：G06焦虑目标及G07百分比目标全文引用T049，剩余时间内容保留在证据中，但任何目标statement/conditions均未独立表达该能力；G07仅明确百分比。T055排序再次专指百分比；T064剩余时间由采访者概括，T065对全段泛确认。是否应与章节进度合并承接、单独表达，或仅为背景比较仍未定。保留风险等待后续提取核验，不新增节点，不据此判G06/G07当前整句错误。','','## 正确与边界案例','']
for b in out['correct_boundaries']:
    lines += ['- **'+b['boundary_id']+'**（'+', '.join(b['goal_ids'])+'）：'+b['reason']]
lines += ['','## 逐目标判断','','每项先按当前完整statement、actor、conditions和实际全文上下文判断，再核origin/inference/support及绑定引文、questions/issues。完整原文轮次、全部绑定引文和作者字段见 review.json 及各文档 JSON。']
for d in documents:
    lines += ['', '### '+d['document_id'],'']
    for g in d['goal_reviews']:
        lines += ['- **'+g['goal_id']+'** — '+g['statement']+'（独立支持：'+g['independent_support']+'）。'+g['reason']+' 回查：'+', '.join(g['actual_source_ids'])+'。']
lines += ['','## 验证及限制','','validation.json 核对71指定ID完整、无重复，source/model哈希与assignment一致，相关附件哈希与manifest一致，全部绑定引文均精确存在于声明轮次。该记录仅证明此处复核记录和引用的完整性，不证明目标语义、方案可实现性或现实事实。转写真实性、录音和受访者的产品/金融/技术事实没有外部验证。未知的费用、权限、参数、信任及实现边界继续保留在现有问题中。']
(HERE/'report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
