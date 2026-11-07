import hashlib
import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]
old = OUT / 'revised/DOC003/v1/delivery/goal-model.json'
new = OUT / 'revised/DOC003/v2/delivery/goal-model.json'
a = json.loads(old.read_text(encoding='utf-8'))
z = json.loads(new.read_text(encoding='utf-8'))


def normalized(model):
    evidence = {e['evidence_id']: e for e in model['evidence_index']}
    return {g['goal_id']: dict(
        fields={k: v for k, v in g.items() if k != 'evidence_ids'},
        quotes=[{k: v for k, v in evidence[eid].items() if k != 'evidence_id'}
                for eid in g['evidence_ids']],
    ) for g in model['goals']}


x, y = normalized(a), normalized(z)
changed = [gid for gid in x if x[gid] != y[gid]]
assert changed == ['DOC003-G14'], changed
assert all(x[gid]['fields'] == y[gid]['fields'] for gid in x)
assert a['refinement_groups'] == z['refinement_groups']
assert all(quote in y['DOC003-G14']['quotes'] for quote in x['DOC003-G14']['quotes'])
record = json.loads((OUT / 'revised/_authoring/DOC003-v2-revision-record.json').read_text(encoding='utf-8'))
record.update(
    before_model_path=old.relative_to(OUT).as_posix(),
    before_model_sha256=hashlib.sha256(old.read_bytes()).hexdigest(),
    after_model_path=new.relative_to(OUT).as_posix(),
    after_model_sha256=hashlib.sha256(new.read_bytes()).hexdigest(),
    all_19_goal_semantic_fields_equal=True, other_18_goal_quotes_equal=True,
    all_original_G14_quotes_retained=True, groups_exactly_equal=True,
    internal_model_version=z['version'], internal_parent=z['parent'],
    evidence_numbering='E IDs regenerated; compared actual quote/location fields independent of IDs',
)
(new.parent.parent / 'revision-record.json').write_text(
    json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
(new.parent.parent / 'revision-notes.md').write_text(
    '# DOC003 外层 v2 修订\n\nG14补充T146提问上下文及T147明确心智负担、反复搜索和时间关系的连续回答。19目标的语义字段全部不变；其他18目标真实引文不变，唯一精化组完全相同。原v1保留。\n\n'
    '冻结工具实际重跑并通过；独立补查记录另见review/expanded-batch1/followup.md。外层v2仍对应内部version=v1、parent=null；路径及SHA-256区分修订，人工审核pending，没有伪造人类反馈。\n',
    encoding='utf-8')
print('DOC003: only G14 evidence packet changed; all semantic fields and group equal.')
