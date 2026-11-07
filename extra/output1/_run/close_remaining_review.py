"""Record effective repair outcomes and close only the actual verified round."""
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]
ROUND = OUT / 'review/remaining-20261025'


def load(path):
    return json.loads(Path(path).read_bytes().decode('utf-8-sig'))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    now = datetime.now(timezone.utc).isoformat()
    plan = load(ROUND / 'plan.json')
    for saved in plan['prior_state']:
        assert sha(OUT / saved['frozen_path']) == saved['sha256'], saved['frozen_path']
    repairs = load(ROUND / 'repairs.json')
    for repair in repairs['repairs']:
        followup_path = OUT / repair['independent_followup']
        followup = load(followup_path)
        assert followup['verdict'] == 'repair_confirmed'
        assert followup['model_sha256'] == repair['after_model_sha256'] == sha(OUT / repair['after_model_path'])
        repair.setdefault('initial_independent_recheck', repair['independent_recheck'])
        repair.update(independent_recheck='repair_confirmed', independent_followup_sha256=sha(followup_path),
                      independent_recheck_recorded_at_utc=now)
        save((OUT / repair['after_model_path']).parent.parent / 'revision-record.json', repair)
    save(ROUND / 'repairs.json', repairs)
    # Regenerate narrative from actual completed outcomes, preserving native review files.
    subprocess.run([sys.executable, '-X', 'utf8', str(OUT / '_run/report_remaining_review.py')], check=True)
    coverage = load(ROUND / 'coverage.json')
    summary = load(ROUND / 'summary.json')
    assert coverage['status'] == 'passed' and not coverage['remaining_unreviewed_goal_ids']
    assert coverage['total_selected_goals'] == 559 and coverage['total_selected_groups'] == 44
    assert summary['open_confirmed_material_findings'] == 0
    for review in coverage['reviews']:
        assert sha(OUT / review['report']) == review['report_sha256'], review['report']
    selected = load(OUT / '_run/delivery-index.json')['documents']
    audit = load(OUT / '_run/final-verification.json')
    navigation = load(OUT / '_run/navigation-verification.json')
    assert audit['status'] == navigation['status'] == 'passed'
    assert not audit['errors'] and not navigation['errors']
    inspected = {(d['arm'], d['document_id']): d for d in audit['deliveries']}
    for item in selected:
        recorded = inspected[(item['arm'], item['document_id'])]
        assert item['json'] == recorded['delivery']
        assert sha(OUT / item['json']) == recorded['model_sha256']
    (ROUND / 'engineering-verification.json').write_bytes((OUT / '_run/final-verification.json').read_bytes())
    (ROUND / 'navigation-verification.json').write_bytes((OUT / '_run/navigation-verification.json').read_bytes())
    files = []
    for path in sorted(ROUND.rglob('*')):
        if path.is_file() and path != ROUND / 'completion.json':
            files.append(dict(path=path.relative_to(OUT).as_posix(), file_sha256=sha(path)))
    current_navigation = [dict(path=p, file_sha256=sha(OUT / p)) for p in ('README.md', 'index.html', '_run/delivery-index.json', '_run/revision-ledger.json')]
    record = dict(round_id=plan['round_id'], user_date='2026-10-25', completed_at_utc=now,
                  status='complete_with_one_local_unresolved_candidate',
                  newly_reviewed_goals=243, total_independently_covered_goals=559,
                  total_independently_covered_groups=44, revised_documents=34,
                  newly_confirmed_material_findings=summary['newly_confirmed_material_findings'],
                  open_confirmed_material_findings=summary['open_confirmed_material_findings'],
                  nonsemantic_repairs=['RR2-001'], unconfirmed_coverage_risks=['RR1-CR01','RR1-CR02','RR2-C01','RR3-001'],
                  remaining_local_candidate='DOC036-G17', human='pending', formal_proof='not_run',
                  selected_delivery_bindings=audit['deliveries'], report_files=files, current_navigation=current_navigation,
                  prior_run_preservation='Original reports and model versions retained. Navigation and mutable run summaries replaced only after byte-exact copies in prior-state; plan.json records the mapping.',
                  current_reports=['review/remaining-20261025/复核总结.md','review/remaining-20261025/统一问题清单.md'],
                  limits=summary['note'])
    save(ROUND / 'completion.json', record)
    print(json.dumps(dict(status=record['status'], goals=559, groups=44,
                          bound_report_files=len(files), navigation_targets=navigation['local_targets_checked']), ensure_ascii=False))


if __name__ == '__main__':
    main()
