"""Complete the evidence packet without changing the goal's meaning."""
import hashlib
import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]
original = OUT / 'revised/DOC003/v1/authoring.json'
author = json.loads(original.read_text(encoding='utf-8'))
source = json.loads((OUT / '_inputs/DOC003/source-input.json').read_text(encoding='utf-8'))
turns = {s['source_id']: s['text'] for s in source['segments']}
goal = next(g for g in author['goals'] if g['candidate_id'] == 'DOC003-G14')
# Keep the question that gives "both" its meaning, then the stakeholder's answer.
goal['evidence'].extend([
    dict(source_id='DOC003:T146', quote=turns['DOC003:T146'], role='context'),
    dict(source_id='DOC003:T147', quote=turns['DOC003:T147'].split(' And as students,')[0], role='basis'),
])
author['author_review'] = (
    '# DOC003 外层 v2：补充心智负担的直接出处\n\n'
    '独立复核指出G14在完整原文中有支持，但绑定证据只列T149/T155，未包含明确说明心智负担的轮次。本轮补入T146提问上下文与T147受访者连续回答；不是目标语义错误，也不改目标陈述、主体、条件、来源、支持结论或精化组。\n\n'
    '父代理实际回读T139–T156及G14语义字段。以下沿用生成方原全篇自检，不冒充父代理重新核查所有目标。新增证据会重新分配后续E编号，修订比对使用真实引文与字段。完整包实际使用冻结工具重新绑定、组装、检查与交付。\n\n'
    + author['author_review']
)
target = OUT / 'revised/_authoring/DOC003-v2.json'
with target.open('xb') as f:
    f.write((json.dumps(author, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
record = dict(
    document_id='DOC003', kind='evidence_traceability_improvement',
    before_authoring=original.relative_to(OUT).as_posix(),
    before_authoring_sha256=hashlib.sha256(original.read_bytes()).hexdigest(),
    after_authoring=target.relative_to(OUT).as_posix(),
    affected_goal_ids=['DOC003-G14'], source_review_turn_ranges=['T139-T156'],
    source_unchanged=True, goal_meaning_unchanged=True, goals_added=[], goals_removed=[],
    groups_changed=[], human_feedback=False, human_acceptance='pending',
    independent_recheck='pending',
)
(OUT / 'revised/_authoring/DOC003-v2-revision-record.json').write_text(
    json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(target)
