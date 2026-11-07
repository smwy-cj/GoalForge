import hashlib
import json
from pathlib import Path
from verify_remaining_coverage import normalized

OUT = Path(__file__).resolve().parents[1]
ROUND = OUT / 'review/remaining-20261025'


def load(path):
    return json.loads(Path(path).read_bytes().decode('utf-8-sig'))


def main():
    old = OUT / 'revised/DOC029/v1/delivery/goal-model.json'
    new = OUT / 'revised/DOC029/v2/delivery/goal-model.json'
    a, z = load(old), load(new)
    before, after = normalized(a, 'goals'), normalized(z, 'goals')
    changed = [gid for gid in before if before[gid] != after[gid]]
    assert changed == ['DOC029-G02'], changed
    assert all(before[gid]['fields'] == after[gid]['fields'] for gid in before)
    assert a['refinement_groups'] == z['refinement_groups']
    assert all(e in after['DOC029-G02']['quotes'] for e in before['DOC029-G02']['quotes'])
    record = load(ROUND / 'DOC029-repair-preparation.json')
    record.update(before_model_path=old.relative_to(OUT).as_posix(),
                  after_model_path=new.relative_to(OUT).as_posix(),
                  before_model_sha256=hashlib.sha256(old.read_bytes()).hexdigest(),
                  after_model_sha256=hashlib.sha256(new.read_bytes()).hexdigest(),
                  changed_goal_ids=changed, changed_group_ids=[],
                  all_16_goal_semantic_fields_equal=True, other_15_goal_quotes_equal=True,
                  all_original_G02_quotes_retained=True, group_exactly_equal=True,
                  internal_version=z['version'], internal_parent=z['parent'],
                  independent_followup='review/remaining-20261025/batch2/followup.json')
    content = json.dumps(record, ensure_ascii=False, indent=2) + '\n'
    (new.parent.parent / 'revision-record.json').write_text(content, encoding='utf-8')
    (ROUND / 'repairs.json').write_text(
        json.dumps(dict(repairs=[record]), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (new.parent.parent / 'revision-notes.md').write_text(
        '# DOC029 外层 v2：证据呈现补充\n\n'
        'RR2-001：G02原支持理由引用母亲节推荐的T043情境实例，本轮把真实连续原文补入绑定上下文。不是确证语义错误；16目标的陈述、主体、条件、来源、推断和支持完全不变，其他15目标真实引文和唯一精化组不变。原v1保留，冻结工具实际重新执行并通过。\n\n'
        '独立补查另见output1/review/remaining-20261025/batch2/followup.md与JSON。内部仍version=v1、parent=null；外层路径及SHA-256识别修订。人工仍pending，没有虚构用户反馈。\n', encoding='utf-8')
    print('DOC029: all 16 semantic field sets equal; only G02 evidence packet extended.')


if __name__ == '__main__':
    main()
