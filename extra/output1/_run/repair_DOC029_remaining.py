"""Add the exact situational recommendation example after independent review."""
import copy
import hashlib
import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]
ROUND = OUT / 'review/remaining-20261025'


def load(path):
    return json.loads(Path(path).read_bytes().decode('utf-8-sig'))


def main():
    previous = OUT / 'revised/DOC029/v1/authoring.json'
    author = load(previous)
    original = copy.deepcopy(author)
    source = load(OUT / '_inputs/DOC029/source-input.json')
    turn = next(s['text'] for s in source['segments'] if s['source_id'] == 'DOC029:T043')
    goal = next(g for g in author['goals'] if g['candidate_id'] == 'DOC029-G02')
    assert 'T043' in goal['support']['rationale']
    assert not any(e['source_id'] == 'DOC029:T043' for e in goal['evidence'])
    goal['evidence'].append(dict(source_id='DOC029:T043', quote=turn, role='context'))
    for old, new in zip(original['goals'], author['goals']):
        assert {k: v for k, v in old.items() if k != 'evidence'} == {k: v for k, v in new.items() if k != 'evidence'}
    author['author_review'] = (
        '# DOC029 外层 v2：情境推荐的直接出处补充\n\n'
        'RR2-001是证据呈现改善建议，不是确证目标含义错误。G02原理由已引用T043母亲节推荐例子，但绑定证据只有T013/T015兴趣与心情片段。本轮补入T043连续原文作为上下文，保留受访者正面体验与其关于个性化机制的主观解释；不把平台知道私人关系当核实事实。\n\n'
        '父代理实际回读T037–T047及G02语义/支持/全部引文。16目标的陈述、主体、条件、origin、inference、support完全不改；其他15目标引文及唯一精化组不改。新增E编号后按真实引文和字段归一化比较，原v1保留。冻结工具实际重跑，独立补查另存；人工仍pending，没有虚构反馈。\n\n'
        + author['author_review']
    )
    target = OUT / 'revised/_authoring/DOC029-v2.json'
    with target.open('xb') as f:
        f.write((json.dumps(author, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
    record = dict(finding_ids=['RR2-001'], document_id='DOC029', kind='evidence_presentation_improvement',
                  before_authoring=previous.relative_to(OUT).as_posix(),
                  before_authoring_sha256=hashlib.sha256(previous.read_bytes()).hexdigest(),
                  after_authoring=target.relative_to(OUT).as_posix(), changed_goal_ids=['DOC029-G02'],
                  changed_group_ids=[], goal_meaning_unchanged=True, source_unchanged=True,
                  source_review_turns=['DOC029:T%03d' % i for i in range(37, 48)],
                  human_feedback=False, human_acceptance='pending', independent_recheck='pending')
    (ROUND / 'DOC029-repair-preparation.json').write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(target)


if __name__ == '__main__':
    main()
