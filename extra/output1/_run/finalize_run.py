"""Close the run after declared reviews and artifact checks are complete."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]


def load(relative):
    return json.loads((OUT / relative).read_bytes().decode('utf-8-sig'))


def sha(relative):
    return hashlib.sha256((OUT / relative).read_bytes()).hexdigest()


def save(relative, data):
    (OUT / relative).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    now = datetime.now(timezone.utc).isoformat()
    review = load('review/expanded-review.json')
    verification = load('_run/final-verification.json')
    navigation = load('_run/navigation-verification.json')
    index = load('_run/delivery-index.json')
    assert verification['status'] == navigation['status'] == 'passed'
    assert not verification['errors'] and not navigation['errors']
    assert review['totals']['revised_documents'] == 34
    assert review['totals']['revised_independently_reviewed_groups'] == 44
    assert review['totals']['open_confirmed_material_findings'] == 0
    inspected = {(d['arm'], d['document_id']): d for d in verification['deliveries']}
    deliveries = []
    for selected in index['documents']:
        digest = sha(selected['json'])
        check = inspected[(selected['arm'], selected['document_id'])]
        assert check['delivery'] == selected['json'] and check['model_sha256'] == digest
        deliveries.append(dict(arm=selected['arm'], document_id=selected['document_id'],
                               model_path=selected['json'], model_sha256=digest,
                               structure=check['structure'], readiness=check['readiness']))
    config = load('_run/run-config.json')
    previous = config['execution_status']
    config.update(
        execution_status='complete_with_one_local_unresolved_candidate',
        completed_at_utc=now, pending_independent_review_batches=[],
        completed_revised_documents=34, remaining_generation_documents=[],
        final_counts=review['totals'],
        final_summary='处理总结.md', final_review='review/expanded-review.md',
        final_verification='_run/final-verification.json',
        unresolved_candidate=review['remaining_blockers'],
        completion_scope='All requested source processing and declared model reviews complete; human adoption pending. DOC036-G17 requires genuine clarification, not more processing of the same transcript.',
    )
    if previous != config['execution_status']:
        config.setdefault('execution_history', []).append(dict(time_utc=now, previous_status=previous,
            new_status=config['execution_status'], note='Completed batch1 and final independent revision rechecks; local unknown retained'))
    save('_run/run-config.json', config)
    # Keep the exact plan bytes read by reviewers; final state is a separate record.
    assert sha('_run/expanded-review-plan.json') == '587d1b5e364e962c9d1f2c62948b54379622f582d4ff46a18bb18f78a719a1a4'
    save('_run/expanded-review-completion.json', dict(
        status='completed_for_declared_scope', completed_at_utc=now,
        initial_plan='_run/expanded-review-plan.json', initial_plan_sha256=sha('_run/expanded-review-plan.json'),
        actual_coverage=review['totals'], consolidated_review='review/expanded-review.json'))
    files = [
        'README.md', 'index.html', '处理总结.md', '_run/run-config.json',
        '_run/expanded-review-plan.json', '_run/expanded-review-completion.json', '_run/delivery-index.json',
        '_run/final-verification.json', '_run/navigation-verification.json', '_run/revision-ledger.json',
        'review/expanded-review.md', 'review/expanded-review.json',
        'review/pilot-comparison.md', 'review/pilot-review.json',
        'review/pilot-v2-followup.md', 'review/pilot-v2-followup.json',
        'review/expanded-batch1/report.md', 'review/expanded-batch1/review.json',
        'review/expanded-batch1/followup.md', 'review/expanded-batch1/followup.json',
        'review/expanded-batch2/report.md', 'review/expanded-batch2/review.json',
        'review/expanded-batch2/followup-by-batch3.md', 'review/expanded-batch2/followup-by-batch3.json',
        'review/expanded-batch3/report.md', 'review/expanded-batch3/review.json',
    ]
    closeout = dict(
        status=config['execution_status'], completed_at_utc=now, totals=review['totals'],
        selected_deliveries=deliveries, report_files=[dict(path=p, file_sha256=sha(p)) for p in files],
        engineering='passed_for_actual_selected_bytes', navigation='local_file_targets_passed',
        semantic='completed_for_explicit_sample_and_all_groups; no all-goal correctness claim',
        human='pending', formal_proof='not_run', remaining_blockers=review['remaining_blockers'],
    )
    save('_run/completion-record.json', closeout)
    print(json.dumps(dict(status=closeout['status'], deliveries=len(deliveries),
                          bound_report_files=len(files), totals=review['totals']), ensure_ascii=False))


if __name__ == '__main__':
    main()
