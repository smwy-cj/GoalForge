"""Freeze the previous delivery selection and partition its uncovered goal IDs."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]
ROUND = OUT / 'review/remaining-20261025'


def load(path):
    return json.loads(path.read_bytes().decode('utf-8-sig'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    with path.open('xb') as f:
        f.write((json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))


def main():
    ROUND.mkdir(exist_ok=False)
    frozen = ROUND / 'prior-state'
    frozen.mkdir()
    files = ['README.md', 'index.html', '处理总结.md', '_run/delivery-index.json',
             '_run/run-config.json', '_run/completion-record.json', '_run/final-verification.json',
             '_run/navigation-verification.json', '_run/revision-ledger.json',
             'review/expanded-review.json', 'review/expanded-review.md']
    prior = []
    for name in files:
        source = OUT / name
        dest = frozen / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(source.read_bytes())
        prior.append(dict(original_path=name, frozen_path=dest.relative_to(OUT).as_posix(), sha256=sha(source)))
    reviewed = load(OUT / 'review/expanded-review.json')
    selected = load(OUT / '_run/delivery-index.json')
    latest = {r['document_id']: r for r in selected['documents'] if r['arm'] == 'revised'}
    docs = []
    for item in reviewed['documents']:
        if not item['unreviewed_goal_ids']:
            continue
        doc = item['document_id']
        path = OUT / latest[doc]['json']
        assert latest[doc]['json'] == item['selected_model_path'] and sha(path) == item['selected_model_sha256']
        model = load(path)
        assert set(item['reviewed_goal_ids']) | set(item['unreviewed_goal_ids']) == {g['goal_id'] for g in model['goals']}
        source_dir = OUT / '_inputs' / doc
        text = (source_dir / 'source.txt').read_bytes().decode('utf-8')
        source_input = load(source_dir / 'source-input.json')
        docs.append(dict(document_id=doc, model_path=path.relative_to(OUT).as_posix(), model_sha256=sha(path),
                         source_path=(source_dir / 'source.txt').relative_to(OUT).as_posix(),
                         source_input_path=(source_dir / 'source-input.json').relative_to(OUT).as_posix(),
                         source_sha256=sha(source_dir / 'source.txt'), source_characters=len(text),
                         source_turns=len(source_input['segments']), required_goal_ids=item['unreviewed_goal_ids'],
                         goals_total=len(model['goals']), groups_total=len(model['refinement_groups'])))
    assert len(docs) == 20 and sum(len(d['required_goal_ids']) for d in docs) == 243
    batches = [dict(batch=i, documents=[], source_characters=0, goals=0) for i in (1, 2, 3)]
    for doc in sorted(docs, key=lambda d: d['source_characters'] + 1500 * len(d['required_goal_ids']), reverse=True):
        batch = min(batches, key=lambda b: b['source_characters'] + 1500 * b['goals'])
        batch['documents'].append(doc)
        batch['source_characters'] += doc['source_characters']
        batch['goals'] += len(doc['required_goal_ids'])
    for batch in batches:
        batch['documents'].sort(key=lambda d: d['document_id'])
        (ROUND / f'batch{batch["batch"]}').mkdir()
        write(ROUND / f'batch{batch["batch"]}/assignment.json', batch)
    plan = dict(round_id='remaining-20261025', created_at_utc=datetime.now(timezone.utc).isoformat(),
                user_date='2026-10-25', scope='All 243 previously uncovered goal IDs in 20 documents; all previously reviewed groups remain covered, changed dependencies rechecked',
                status='in_progress', original_revised_goals=559, previously_independently_reviewed_goals=316,
                required_goal_count=243, documents=docs, allocation=[dict(batch=b['batch'], goals=b['goals'],
                documents=[d['document_id'] for d in b['documents']], source_characters=b['source_characters']) for b in batches],
                prior_state=prior,
                review_kind='Fresh independent model contexts; source-first; not human review or formal proof',
                exact_model='unknown', sampling_parameters='unknown', budget='unknown',
                restricted_materials='No author self-review, previous semantic verdicts, baseline, old output, research/development reference answers',
                repairs='Preserve original versions. Source-grounded repairs in new artifact versions, frozen tools, independent affected-object recheck. No fabricated human feedback.',
                stop_rule='Keep genuinely unknown cases unresolved with exact local scope; no artificial goal additions or repeated review without new evidence')
    write(ROUND / 'plan.json', plan)
    print(json.dumps(plan['allocation'], ensure_ascii=False))


if __name__ == '__main__':
    main()
