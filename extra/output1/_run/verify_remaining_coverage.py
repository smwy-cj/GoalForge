"""Bind actual independent-review ID sets to preserved and current model bytes."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]
ROUND = OUT / 'review/remaining-20261025'


def load(path):
    return json.loads(Path(path).read_bytes().decode('utf-8-sig'))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def normalized(model, kind):
    evidence = {e['evidence_id']: e for e in model['evidence_index']}
    id_field = 'goal_id' if kind == 'goals' else 'group_id'
    return {item[id_field]: dict(
        fields={k: v for k, v in item.items() if k != 'evidence_ids'},
        quotes=[{k: v for k, v in evidence[eid].items() if k != 'evidence_id'}
                for eid in item.get('evidence_ids', [])]) for item in model[kind]}


def main():
    plan = load(ROUND / 'plan.json')
    prior = load(ROUND / 'prior-state/review/expanded-review.json')
    prior_index = load(ROUND / 'prior-state/_run/delivery-index.json')
    prior_closed = load(ROUND / 'prior-state/_run/completion-record.json')
    original_hash = {(r['arm'], r['document_id']): r['model_sha256'] for r in prior_closed['selected_deliveries']}
    old = {r['document_id']: r for r in prior_index['documents'] if r['arm'] == 'revised'}
    now = {r['document_id']: r for r in load(OUT / '_run/delivery-index.json')['documents'] if r['arm'] == 'revised'}
    assert set(old) == set(now) and len(now) == 34
    pilot = load(OUT / 'review/pilot-review.json')
    previous_goals = {d['document_id']: set(d['reviewed_goal_ids']) for d in prior['documents']}
    previous_groups = {d['document_id']: set(d['reviewed_group_ids']) for d in prior['documents']}
    for doc in ('DOC010', 'DOC023', 'DOC031'):
        previous_goals[doc] = {g['goal_id'] for g in pilot['goal_reviews'] if g['document'] == doc and g['branch'] == 'revised'}
        previous_groups[doc] = {g['group_id'] for g in pilot['group_reviews'] if g['document'] == doc and g['branch'] == 'revised'}
    assert sum(map(len, previous_goals.values())) == 316
    assert sum(map(len, previous_groups.values())) == 44
    new_goals, reviews = {}, []
    bound_quotes_checked = 0
    for number in (1, 2, 3):
        directory = ROUND / f'batch{number}'
        assignment = load(directory / 'assignment.json')
        report = load(directory / 'review.json')
        entries = {d['document_id']: d for d in report['documents']}
        assert set(entries) == {d['document_id'] for d in assignment['documents']}
        for spec in assignment['documents']:
            doc = spec['document_id']
            item = entries[doc]
            assert item['model_path'].removeprefix('output1/') == spec['model_path'], doc
            assert item['model_sha256'] == spec['model_sha256'] == sha(OUT / spec['model_path']), doc
            assert item['source_sha256'] == spec['source_sha256'] == sha(OUT / spec['source_path']), doc
            assert item['source_complete_read'] is True, doc
            required = set(spec['required_goal_ids'])
            assert required == set(item['required_goal_ids']) == set(item['reviewed_goal_ids']), doc
            actual = [g['goal_id'] for g in item['goal_reviews']]
            assert len(actual) == len(set(actual)) and set(actual) == required, doc
            model = load(OUT / spec['model_path'])
            model_goals = {g['goal_id']: g for g in model['goals']}
            evidence = {e['evidence_id']: e for e in model['evidence_index']}
            segments = {s['source_id']: s['text'] for s in load(OUT / spec['source_input_path'])['segments']}
            evidence_key = lambda e: (e['evidence_id'], e['source_id'], e['quote'], e['evidence_role'])
            for assessment in item['goal_reviews']:
                target = model_goals[assessment['goal_id']]
                for field in ('statement', 'actor', 'conditions'):
                    assert assessment[field] == target[field], (doc, target['goal_id'], field)
                assert assessment['reason'].strip(), (doc, target['goal_id'], 'missing specific review reason')
                bound = assessment.get('bound_evidence', assessment.get('all_bound_evidence'))
                assert isinstance(bound, list)
                assert [evidence_key(e) for e in bound] == [evidence_key(evidence[eid]) for eid in target['evidence_ids']]
                for quote in bound:
                    assert quote['quote'] in segments[quote['source_id']], (doc, target['goal_id'], 'review quote mismatch')
                    bound_quotes_checked += 1
            assert not previous_goals[doc] & required, doc
            assert doc not in new_goals
            new_goals[doc] = required
        reviews.append(dict(batch=number, report=(directory / 'review.json').relative_to(OUT).as_posix(),
                            report_sha256=sha(directory / 'review.json'), goals=sum(len(d['reviewed_goal_ids']) for d in report['documents'])))
    assert sum(map(len, new_goals.values())) == plan['required_goal_count'] == 243
    repair_path = ROUND / 'repairs.json'
    repairs = load(repair_path)['repairs'] if repair_path.exists() else []
    repaired = {r['document_id']: r for r in repairs}
    assert len(repaired) == len(repairs)
    docs = []
    for doc in sorted(now):
        original = OUT / old[doc]['json']
        selected = OUT / now[doc]['json']
        assert sha(original) == original_hash[('revised', doc)], doc
        before, after = load(original), load(selected)
        a, z = normalized(before, 'goals'), normalized(after, 'goals')
        ga, gz = normalized(before, 'refinement_groups'), normalized(after, 'refinement_groups')
        covered = previous_goals[doc] | new_goals.get(doc, set())
        assert covered == set(a), (doc, 'incomplete original goal coverage')
        assert previous_groups[doc] == set(ga), (doc, 'incomplete previous group coverage')
        changed_goals = sorted(g for g in set(a) | set(z) if a.get(g) != z.get(g))
        changed_groups = sorted(g for g in set(ga) | set(gz) if ga.get(g) != gz.get(g))
        followup = None
        if sha(original) != sha(selected):
            r = repaired[doc]
            assert r['before_model_path'] == old[doc]['json'] and r['after_model_path'] == now[doc]['json']
            assert r['before_model_sha256'] == sha(original) and r['after_model_sha256'] == sha(selected)
            assert set(changed_goals) == set(r['changed_goal_ids'])
            assert set(changed_groups) == set(r['changed_group_ids'])
            followup = load(OUT / r['independent_followup'])
            assert followup['verdict'] == 'repair_confirmed'
            assert followup['model_sha256'] == sha(selected)
            assert set(followup['reviewed_goal_ids']) >= set(changed_goals)
            assert set(followup['reviewed_group_ids']) >= set(changed_groups)
            # Repaired/added objects must have explicit independent recheck, preserved ones equality.
            covered = (covered & set(z)) | set(followup['reviewed_goal_ids'])
        else:
            assert not changed_goals and not changed_groups
        assert covered >= set(z), (doc, 'selected goals not independently covered')
        assert sha(selected.parent / 'attachments/source.txt') == sha(original.parent / 'attachments/source.txt')
        docs.append(dict(document_id=doc, original_model_path=old[doc]['json'], original_model_sha256=sha(original),
                         selected_model_path=now[doc]['json'], selected_model_sha256=sha(selected),
                         previously_reviewed_goal_ids=sorted(previous_goals[doc]), newly_reviewed_goal_ids=sorted(new_goals.get(doc, set())),
                         independently_covered_goal_ids=sorted(set(z)), independently_covered_group_ids=sorted(set(gz)),
                         changed_goal_ids=changed_goals, changed_group_ids=changed_groups,
                         repair_followup=repaired[doc]['independent_followup'] if followup else None))
    output = dict(record_type='full_goal_coverage_after_remaining_review', verified_at_utc=datetime.now(timezone.utc).isoformat(),
                  status='passed', previously_reviewed_goals=316, newly_reviewed_goals=243,
                  total_selected_goals=sum(len(d['independently_covered_goal_ids']) for d in docs),
                  total_selected_groups=sum(len(d['independently_covered_group_ids']) for d in docs),
                  revised_documents=len(docs), original_required_ids_covered=True, remaining_unreviewed_goal_ids=[],
                  new_review_bound_quotes_checked=bound_quotes_checked,
                  reviews=reviews, documents=docs,
                  claim='Independent model-context semantic review coverage only. Not human adoption, external validation, accuracy estimate, exhaustive omission proof, or formal proof.')
    (ROUND / 'coverage.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: output[k] for k in ('status', 'previously_reviewed_goals', 'newly_reviewed_goals', 'total_selected_goals', 'total_selected_groups', 'revised_documents')}))


if __name__ == '__main__':
    main()
