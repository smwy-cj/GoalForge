"""Keep a proposed group rationale within its actual parent-goal scope."""
import hashlib
import json
from pathlib import Path

OUT=Path(__file__).resolve().parents[1]
p=OUT/'revised/DOC025/v1/authoring.json'
d=json.loads(p.read_text(encoding='utf-8'))
source=json.loads((OUT/'_inputs/DOC025/source-input.json').read_text(encoding='utf-8'))
turns={s['source_id']:s['text'] for s in source['segments']}
g=next(g for g in d['groups'] if g['group_id']=='DOC025-F1')
for e in g['evidence']:
    assert e['quote'] in turns[e['source_id']]
old=g['rationale']
assert '招聘回应' in old
g['rationale']='这些能力有助于检索和申请，但职位是否符合本人条件、需要补充的完整申请环节及筛选/提醒组合覆盖范围仍未确定，不能据此证明父目标的整体充分性。'
g['assumptions']=['不假定推荐均相关、岗位一定符合本人条件或列出的操作已穷尽申请所需步骤。']
assert g['status']=='proposed' and g['completeness']=='partial'
for q in d['model_questions']:
    if q['target_type']=='group' and q['target_id']=='DOC025-F1':
        q['message']='候选组尚未证明共同充分性：'+g['rationale']
d['author_review']=d['author_review'].replace('即便提交顺利也可能不获聘用，F1不能保证求职结果。',
    '候选组合是否能识别合适职位并完整提交申请仍需核验；聘用或招聘回应在父目标范围外，不用于判断F1充分性。')
d['author_review']=('# DOC025 外层 v2：精化理由范围澄清\n\n'
    'ER-B2-001为低严重度表达不足：F1原理由提及招聘回应，而父G01仅是探索并申请合适工作。本轮移除该不相关理由及雇主回应假设；保留职位匹配、完整申请和组合覆盖范围未定的真实不足，F1仍proposed/partial。全部9目标及其支持不改；不新增精化、不宣称得到聘用。\n\n'
    '父代理核对T003/T005/T013/T021及组端点与条件；以下沿用原生成方全篇自检，仅消除场景文字中的同一范围混淆。冻结脚本实际重新绑定、组装、检查与交付，不伪造人工反馈。\n\n'+d['author_review'])
target=OUT/'revised/_authoring/DOC025-v2.json'
with target.open('xb') as f:f.write((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
record=dict(finding_id='ER-B2-001',document_id='DOC025',before_authoring=p.relative_to(OUT).as_posix(),
            before_authoring_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),after_authoring=target.relative_to(OUT).as_posix(),
            changed_goal_ids=[],changed_group_ids=['DOC025-F1'],goals_added=[],goals_removed=[],
            source_unchanged=True,group_status_unchanged=True,human_feedback=False,human_acceptance='pending',independent_recheck='pending')
(OUT/'revised/_authoring/DOC025-v2-revision-record.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(target)
