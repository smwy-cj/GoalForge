# -*- coding: utf-8 -*-
import json,hashlib,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
logp=OUT/'consumed-files.json'
log=json.loads(logp.read_text(encoding='utf-8'))
def read(p):
    b=(ROOT/p).read_bytes(); h=hashlib.sha256(b).hexdigest()
    log[p]={'sha256':h,'bytes':len(b)}
    return b.decode('utf-8-sig'),h
def obj(p):
    t,h=read(p); return json.loads(t),h
oldpath='revised/DOC029/v1/delivery/goal-model.json'
newpath='revised/DOC029/v2/delivery/goal-model.json'
old,oh=obj(oldpath); new,nh=obj(newpath)
assert oh=='b5afe842d44d583850dd477fc5067dfa42c49d86a100d8346d4e6e9853ae8899'
assert nh=='a65febe8cc0790dafeb09104e2bdb6630ba678fd3a6574cc21d8e6b2761f26c0'
source,sh=read('_inputs/DOC029/source.txt'); s,sih=obj('_inputs/DOC029/source-input.json')
by={x['source_id']:x for x in s['segments']}
def norm_target(g,m):
    result={k:v for k,v in g.items() if k!='evidence_ids'}
    eb={e['evidence_id']:e for e in m['evidence_index']}
    result['actual_evidence']=sorted([{k:v for k,v in eb[eid].items() if k!='evidence_id'} for eid in g['evidence_ids']],key=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True))
    return result
oldgoals={g['goal_id']:g for g in old['goals']}; newgoals={g['goal_id']:g for g in new['goals']}
assert set(oldgoals)==set(newgoals) and len(oldgoals)==16
others=[gid for gid in oldgoals if gid!='DOC029-G02']
unchanged=[]
for gid in others:
    assert norm_target(oldgoals[gid],old)==norm_target(newgoals[gid],new),gid
    unchanged.append(gid)
g1=oldgoals['DOC029-G02']; g2=newgoals['DOC029-G02']
assert {k:v for k,v in g1.items() if k!='evidence_ids'}=={k:v for k,v in g2.items() if k!='evidence_ids'}
ob={e['evidence_id']:e for e in old['evidence_index']}; nb={e['evidence_id']:e for e in new['evidence_index']}
old_e=[{k:v for k,v in ob[eid].items() if k!='evidence_id'} for eid in g1['evidence_ids']]
new_e=[{k:v for k,v in nb[eid].items() if k!='evidence_id'} for eid in g2['evidence_ids']]
added=[e for e in new_e if e not in old_e]
assert len(added)==1 and added[0]['source_id']=='DOC029:T043' and added[0]['evidence_role']=='context'
assert added[0]['quote']==by['DOC029:T043']['text']
assert all(e in new_e for e in old_e)
for e in new['evidence_index']:
    assert e['quote'] in by[e['source_id']]['text']
    assert source[e['start_char']:e['end_char']]==e['quote']
assert len(old['refinement_groups'])==len(new['refinement_groups'])==1
assert norm_target(old['refinement_groups'][0],old)==norm_target(new['refinement_groups'][0],new)
assert old['issues']==new['issues']
bindings=[]
for version,model,mhash in [('v1',old,oh),('v2',new,nh)]:
    base=f'revised/DOC029/{version}/delivery/'
    ex,eh=obj(base+'attachments/extraction.json')
    ju,jh=obj(base+'attachments/judgments.json')
    ka,kh=obj(base+'attachments/kaos-decisions.json')
    mf,mfh=obj(base+'manifest.json')
    ast,ash=read(base+'attachments/source.txt')
    assert sh==ash=='7a83fb5d6371761614b085555fe6a35dcfa69a14f322e614cf098d76da1b6ee3'
    assert ast==source and ex['segments']==s['segments']
    actual={'attachments/extraction.json':eh,'attachments/judgments.json':jh,'attachments/source.txt':ash,'attachments/kaos-decisions.json':kh}
    for p,h in actual.items():
        assert next(i['sha256'] for i in mf['files'] if i['path']==p)==h
        assert next(i['sha256'] for i in model['input_artifacts'] if i['path']==p)==h
    assert next(i['sha256'] for i in mf['files'] if i['path']=='goal-model.json')==mhash
    if version=='v1':exold=ex; juold=ju; kaold=ka
    else:
        assert ju['judgments']==juold['judgments']
        assert ka['groups']==kaold['groups'] and ka['questions']==kaold['questions']
        eo={c['candidate_id']:c for c in exold['candidates']}; en={c['candidate_id']:c for c in ex['candidates']}
        for gid in others:assert eo[gid]==en[gid]
    bindings.append({'version':version,'source_sha256':ash,'extraction_sha256':eh,'judgments_sha256':jh,'kaos_decisions_sha256':kh,'manifest_sha256':mfh,'binding_check':'passed'})
def ev(ts):return [{'source_id':f'DOC029:T{t:03d}','speaker':by[f'DOC029:T{t:03d}']['speaker'],'quote':by[f'DOC029:T{t:03d}']['text']} for t in ts]
result={
    'review_id':'remaining-20261025-batch2-followup-DOC029-v2','reviewer':{'agent':'/root/remaining_review2','model':'unknown','model_settings':'unknown'},
    'verdict':'repair_confirmed','finding_ids':['RR2-001'],'original_model_path':oldpath,'revised_model_path':newpath,
    'original_model_sha256':oh,'model_sha256':nh,'reviewed_goal_ids':['DOC029-G02'],'reviewed_group_ids':['F029-1'],
    'goal_review':{'goal_id':'DOC029-G02','statement':g2['statement'],'independent_support_label':'direct',
        'reason':'T013的个人需要/心情、T015的匹配价值与T043母亲节共同观看经历共同直接支持推荐贴合兴趣、当天心情和情境。新E0004绑定完整T043连续原文，确实补足情境证据的可见性；没有修改目标或把受访者对平台知道母亲节/私人关系的解释认证为事实。',
        'source_evidence':ev([12,13,14,15,42,43,44,45]),'added_evidence':added,
        'counts_as_confirmed_semantic_error':False,'local_blocking_scope':[]},
    'unchanged_goal_comparison':{'goal_ids':unchanged,'count':len(unchanged),'comparison':'full goal fields plus actual evidence normalized by source_id/quote/role/locations, ignoring evidence_id renumbering','all_unchanged':True,'scope_note':'其余15项目标为语义字段及真实引文不变性比较，不宣称新增15项目标的全量独立语义审查。'},
    'group_review':{'group_id':'F029-1','status':'proposed','completeness':'partial','normalized_group_and_actual_evidence_unchanged':True,
        'reason':'T033提出预览选片与直接跳节目，T037/T039仅预期减少外跳/提升留存。即使预览和直达均实现，内容不合口味等分析反例仍可能使用户离开，故不能把贡献当充分精化；该组继续proposed/partial及相关问题忠实，修订未改变组。',
        'source_evidence':ev([33,35,37,38,39]),'analysis_assumption':'预览后内容仍可能不适合或用户因其他原因离开是分析反例，未声称访谈实际发生。'},
    'source_unchanged':True,'source_sha256':sh,'source_input_sha256':sih,'bindings':bindings,
    'initial_review_preserved':{'path':'review.json','model_version':'DOC029/v1','finding_status':'open_at_initial_v1_review','not_rewritten_to_v2':True},
    'finding_resolution':{'finding_id':'RR2-001','status':'resolved_in_v2','resolution_type':'evidence_presentation_improvement','counts_as_confirmed_semantic_error':False},
    'limits':['此修订确认不是人工采纳或形式证明。','RR2-C01仅为DOC030候选覆盖风险，仍未确证遗漏，不受本次DOC029修订影响。','未改任何模型、源文、技能或核心inspection。']
}
(OUT/'followup.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'followup.md').write_text('\n'.join([
    '# DOC029 v2 独立局部复查','',
    '结论：repair_confirmed。RR2-001已在v2解决，性质为证据呈现改善，非语义错误。','',
    f'初审v1：{oh}',f'复查v2：{nh}','',
    result['goal_review']['reason'],'',
    '其余15个目标的完整语义字段和实际source_id/quote/role/位置归一化后均不变；只忽略证据ID重新编号。全部目标的真实引文均与标准源文精确匹配。','',
    result['group_review']['reason'],'',
    '原文、source-input映射、唯一组、组的问题均未变；extraction/judgments/kaos及manifest绑定实测通过。初审review.json和report.md仍保留v1及其当时的未解决状态，修复确认独立保存于本followup。','',
    '独立语义补查目标仅DOC029-G02，实际复查组F029-1。其余15目标仅进行不变性比较。人工采纳pending，形式证明not_run；DOC030 RR2-C01依然只是候选覆盖风险。',''
]),encoding='utf-8')
logp.write_text(json.dumps(log,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'verdict':result['verdict'],'model_sha256':nh,'goal_fields_and_bound_evidence_unchanged_other_goals':len(unchanged),'group_unchanged':True,'source_unchanged':True},ensure_ascii=False))
