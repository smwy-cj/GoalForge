"""Clarify a boundary and complete evidence after independent source review."""
import hashlib
import json
from pathlib import Path

OUT=Path(__file__).resolve().parents[1]
original=OUT/'revised/DOC033/v1/authoring.json'
author=json.loads(original.read_text(encoding='utf-8'))
source=json.loads((OUT/'_inputs/DOC033/source-input.json').read_text(encoding='utf-8'))
turns={s['source_id']:s['text'] for s in source['segments']}
goals={g['candidate_id']:g for g in author['goals']}
g=goals['DOC033-G12']
old_statement=g['statement']
assert '20分钟以上' in old_statement
g['statement']=old_statement.replace('20分钟以上','超过20分钟')
g['support']['supported_parts']=[g['statement']]
g17=goals['DOC033-G17']
t151=turns['DOC033:T151']
prefix='But sometimes it goes into advertisements that themselves are '
long_ad=t151[t151.index(prefix):]
g17['evidence'].append(dict(source_id='DOC033:T151',quote=long_ad,role='basis'))
g17['evidence'].append(dict(source_id='DOC033:T155',quote=turns['DOC033:T155'],role='context'))
review=author['author_review'].replace(old_statement,g['statement'])
author['author_review']=('# DOC033 外层 v2：表达与证据可核验性补充\n\n'
    '独立复核的两项低严重度建议：ER-B3-002将G12“20分钟以上”消歧为“超过20分钟”，与T129/T133/T135的greater than/over一致；ER-B3-003为G17补T151明确两小时长广告的连续原文及T155愿修复但非决定弃用因素的上下文。它们不自动计为两项确证错误目标。\n\n'
    '父代理实际回查T127–T135和T149–T159，G17目标含义/来源/支持结论未改。其余16目标的语义与证据不变，没有精化组。以下为沿用的原生成方全篇自检（更新G12措辞）；本轮不冒充父代理重新语义评审所有目标。完整包用冻结工具重新绑定、定位、组装、检查与交付。\n\n'+review)
target=OUT/'revised/_authoring/DOC033-v2.json'
with target.open('xb') as f:f.write((json.dumps(author,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
record=dict(document_id='DOC033',findings=['ER-B3-002','ER-B3-003'],kind='low_severity_wording_and_evidence_clarity',
            before_authoring=original.relative_to(OUT).as_posix(),before_authoring_sha256=hashlib.sha256(original.read_bytes()).hexdigest(),
            after_authoring=target.relative_to(OUT).as_posix(),affected_goal_ids=['DOC033-G12','DOC033-G17'],
            source_review_turn_ranges=['T127-T135','T149-T159'],source_unchanged=True,goals_added=[],goals_removed=[],
            groups_changed=[],human_feedback=False,human_acceptance='pending',independent_recheck='pending')
(OUT/'revised/_authoring/DOC033-v2-revision-record.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(target)
