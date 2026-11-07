# -*- coding: utf-8 -*-
import json, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'output1/review'
def load(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
p1=ROOT/'output1/revised/DOC010/v1'
p2=ROOT/'output1/revised/DOC010/v2'
m1=load(p1/'delivery/goal-model.json')
m2=load(p2/'delivery/goal-model.json')
e2=load(p2/'extraction.json')
j2=load(p2/'judgments.json')['judgments']
r=load(p2/'revision-record.json')
def differences(a,b,p=''):
    if type(a)!=type(b): return [p]
    if isinstance(a,dict):
        out=[]
        for k in set(a)|set(b):
            if k not in a or k not in b: out.append(p+'/'+k)
            else: out += differences(a[k],b[k],p+'/'+k)
        return out
    if isinstance(a,list):
        if len(a)!=len(b): return [p]
        return sum((differences(x,y,p+'/'+str(i)) for i,(x,y) in enumerate(zip(a,b))),[])
    return [] if a==b else [p]
goal_changes={a['goal_id']:differences(a,b) for a,b in zip(m1['goals'],m2['goals']) if a!=b}
source=ROOT/'output1/_inputs/DOC010/source.txt'
text=source.read_text(encoding='utf-8-sig')
segments={s['source_id']:s for s in load(ROOT/'output1/_inputs/DOC010/source-input.json')['segments']}
errors=[]
for e in m2['evidence_index']:
    if text[e['start_char']:e['end_char']]!=e['quote'] or e['quote'] not in segments[e['source_id']]['text']:
        errors.append('quote '+e['evidence_id'])
for c,g in zip(e2['candidates'],m2['goals']):
    for k in ('statement','actor','origin','inference'):
        if c.get(k)!=g.get(k): errors.append('projection '+g['goal_id']+' '+k)
    if c['context']!=g['conditions']: errors.append('context '+g['goal_id'])
    for k in ('label','rationale','supported_parts','unsupported_parts','assumptions','reasoning_steps'):
        if j2[g['goal_id']].get(k)!=g['support'].get(k): errors.append('judgment '+g['goal_id']+' '+k)
record={'record_type':'independent_context_revision_review','date_local':'2026-10-24',
 'scope':'revised DOC010 external v2: G08 full semantics/support/conditions and dependent F02; remaining 12 goals and F01/F03 checked for exact equality to fully reviewed v1',
 'reviewer':'/root/pilot_review','model_exact_id':'unknown','author_self_review_used_as_acceptance':False,
 'sources':['DOC010:T049','DOC010:T063','DOC010:T066','DOC010:T067','DOC010:T069','DOC010:T041','DOC010:T065'],
 'goal_changes':goal_changes,'groups_exactly_equal':m1['refinement_groups']==m2['refinement_groups'],
 'source_identical_to_frozen':sha(p2/'source.txt')==sha(source),
 'source_input_identical_to_frozen':sha(p2/'source-input.json')==sha(ROOT/'output1/_inputs/DOC010/source-input.json'),
 'assembled_delivery_identical':sha(p2/'assembled/model-input.json')==sha(p2/'delivery/goal-model.json'),
 'exact_model_quotes_checked':len(m2['evidence_index']),'errors':errors,
 'lineage_hashes_match':r['previous_model']['sha256']==sha(p1/'delivery/goal-model.json') and r['current_model']['sha256']==sha(p2/'delivery/goal-model.json'),
 'independent_inspection':load(OUT/'engineering/revised-DOC010-v2-inspection.json'),
 'semantic_conclusion':'G08的雨情变化表述保守承接是否降雨、开始/停止及变化，不再容易被误读为雨强指标；direct保留合理。频率仍未量化，降雨条件和常规通知例外不变。F02仍正确为proposed/partial：频繁不能保证实时，且降雨局部不覆盖全部天气。',
 'finding_disposition':{'finding_id':'PR-003','v1_status':'unresolved_in_v1_preserved','v2_status':'resolved_by_conservative_wording','severity_change':'none_needed; original was nonblocking ambiguity'},
 'version_limitation':{'external_artifact_version':'v2','internal_model_version':m2['version'],'internal_parent':m2['parent'],'assessment':'内部仍version=v1、parent=null，不能声称工具已递增原生模型版本。外层revision-record中的路径、双哈希和ID映射可辨别助手修订谱系；后续引用须同时绑定路径和哈希，不能仅用model_id/version识别。未来需支持非人工反馈的修订入口。该限制已透明记录，不影响当前实际文件的可核验性。'},
 'gate_after_revision':'pass','human_acceptance':'pending','formal_proof':'not_run','generated_files_modified_by_reviewer':False}
assert goal_changes=={'G08':['/statement','/support/supported_parts/0']} or set(goal_changes)=={'G08'} and set(goal_changes['G08'])=={'/statement','/support/supported_parts/0'}
assert record['groups_exactly_equal'] and record['source_identical_to_frozen'] and record['source_input_identical_to_frozen'] and record['assembled_delivery_identical'] and record['lineage_hashes_match'] and not errors
(OUT/'pilot-v2-followup.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
note='''# DOC010 外层 v2 独立修订补查

**结论：PR-003 已在外层 v2 通过保守措辞解决，可使用该版本。** 冻结 v1 原始对照与风险记录不覆盖；这不是人工采纳。

实际读取了 v2 的 G08 完整目标、条件、支持、引用，F02完整组，以及 revision-record.json / revision-notes.md。没有用作者自检作为接受依据。回查冻结来源 T049/T063 与 T041/T065、T066–T069的频率/实时更新语境，源文第一阶段已完整阅读。

- 唯一目标内容差异为G08陈述及对应supported_parts：“雨势变化”改为“雨情变化”；其余12目标和全部3组逐对象完全一致。G08仍保留降雨条件、相对常规更频繁以及无统一分钟阈值。
- T049说关心何时停止及降雨变化，T063说raining and not raining。新的雨情措辞不再暗示必须提供雨强信息，direct可保留；并未删除及时通知意图。
- F02仍proposed/partial，原因正确：频繁发出的通知可能仍用旧数据，而且只覆盖下雨情境。修订未使其变成成立精化，没有衍生层级退化。
- 重新实际执行inspect通过。全部50处模型引文（43处目标证据加7处组证据）与冻结全文/轮次精确匹配；候选/判断到目标投影一致，源文件不变，assembled与delivery一致，revision-record前后哈希实测匹配。

版本限制须保留：这是外层作者产物版本v2，内部模型仍version=v1、parent=null。不能称工具已递增模型版本，也不能伪造用户反馈绕过限制。外层修订记录已绑定双路径、双哈希及ID映射，当前仍可识别和验证；后续消费必须使用路径与哈希，不仅凭model_id/version。建议未来提供助手修订的原生版本入口。该局部工具限制不妨碍当前来源与修订谱系核验。

最终采用新版组合：DOC010外层v2，加DOC023/DOC031冻结v1，扩展门槛为pass。仍无外部人审、形式证明或全部扩展资料独立语义审核的含义。原inspection状态未修改，人工pending。

机器证据见pilot-v2-followup.json及engineering/revised-DOC010-v2-inspection.json。
'''
(OUT/'pilot-v2-followup.md').write_text(note,encoding='utf-8')
data=load(OUT/'pilot-review.json')
data['revision_followup']={'status':'completed','artifact':'pilot-v2-followup.json','finding_id':'PR-003','v1_status':'unresolved_in_v1_preserved','v2_status':'resolved_by_conservative_wording','final_selection':{'DOC010':'revised external v2','DOC023':'revised v1','DOC031':'revised v1'},'final_gate':'pass','version_limitation':record['version_limitation']}
(OUT/'pilot-review.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
for filename in ('pilot-comparison.md','pilot-gate.md'):
    with (OUT/filename).open('a',encoding='utf-8') as f:
        f.write('\n## 后续修订补查（不覆盖上述冻结 v1 判断）\n\nDOC010外层v2已独立补查，PR-003在该版本解决；G08仅“雨势”收窄为“雨情”，F02仍proposed/partial，其他目标/组无变。重跑inspect及50处引文核验通过。采用DOC010外层v2及DOC023/DOC031 v1的最终组合，门槛为 **pass**。详见 `pilot-v2-followup.md` / `.json`。内部version=v1、parent=null的工具限制已明确记录，外层谱系通过路径与前后哈希绑定，不能冒称人工反馈或原生版本递增。\n')
print(json.dumps({'goal_changes':goal_changes,'errors':errors,'PR-003_v2':'resolved','gate':'pass'},ensure_ascii=False))
