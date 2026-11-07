"""Provenance/coverage regressions, with synthetic intentions, not accuracy claims."""
import copy
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/goal-extraction/scripts'))
import check_coverage as coverage
from prepare_source import prepare, build_windows, encode, digest


def fixture():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / 'source.txt'
        path.write_text('希望比较方案😀，也希望一次提交所有条件得到推荐。\n更喜欢白天出发，但夜间也可以。\n页面现在有离线功能。\n采访者问：是否需要匿名浏览或发布？\n回答：是。\n', encoding='utf-8')
        source, prepared = prepare(path, 'SYN-COVERAGE')
    raws = dict(source=source.encode('utf-8'), source_input=encode(prepared))
    windows = build_windows(prepared, source, 4, 2, digest(raws['source_input']))
    raws['windows'] = encode(windows)

    def evidence(n):
        s = prepared['segments'][n]
        return dict(source_id=s['source_id'], quote=s['text'], role='basis',
                    start_char=s['original_locator']['start_char'], end_char=s['original_locator']['end_char'])

    statements = ['比较方案', '一次提交所有条件得到推荐', '更喜欢白天出发，但夜间也可以']
    final = copy.deepcopy(prepared)
    final.update(schema_version='goalforge-extraction-3', status='completed', review_questions=[], limitations=[],
                 candidates=[dict(candidate_id=f'G{i + 1}', statement=s, actor=None, origin='explicit', context=[],
                                  evidence_candidates=[evidence(0 if i < 2 else 1)], inference=None, review_status='pending')
                             for i, s in enumerate(statements)])
    raws['extraction'] = encode(final)
    capture = coverage.capture_template(raws)
    capture['candidates'] = [dict(candidate_id=f'C{i + 1}', statement=s, actor=None, modality='暂定，待全文核对',
        origin='unknown', context=[], pass_id='P1', window_ids=[windows['windows'][0]['window_id']],
        evidence_candidates=[evidence(n)]) for i, (s, n) in enumerate([
            ('比较与推荐', 0), ('白天出发偏好', 1), ('现有离线能力是否有维持意图', 2), ('匿名发布？', 3)])]
    raws['candidates'] = encode(capture)
    ledger = coverage.template(raws)
    ledger['run'].update(planned_passes=1, stop_reason='完成一次基础捕获和全篇校正；合成开发样例。')
    ledger['run']['passes'][0].update(kind='initial', context='shared', status='completed')
    for result in ledger['run']['passes'][0]['window_results']:
        result['status'] = 'processed'
    ledger['full_context_review'] = dict(status='completed', source_ids=[s['source_id'] for s in prepared['segments']],
                                       reason='核对后文让步、现状与复合问句，仍保留未决意图。')
    for entry, disposition, targets in zip(ledger['entries'], ['split', 'keep', 'exclude', 'uncertain'],
                                          [['G1', 'G2'], ['G3'], [], []]):
        entry.update(disposition=disposition, final_goal_ids=targets, reason='合成开发判断，非独立语义结论。')
    ledger['source_checks'] = [dict(check_id='S1', evidence_candidates=[evidence(0)], candidate_ids=['C1'],
                                    final_goal_ids=['G1', 'G2'], outcome='represented', reason='两种可独立实现的结果分开保留。')]
    return raws, ledger


class CoverageTests(unittest.TestCase):
    def test_complete_mapping_preserves_uncertainty_without_semantic_claim(self):
        raws, ledger = fixture()
        before = copy.deepcopy((raws, ledger))
        report = coverage.audit(raws, ledger)
        self.assertEqual(report['errors'], [])
        self.assertEqual(report['workflow'], 'recorded')
        self.assertEqual(report['uncertain_candidate_ids'], ['C4'])
        self.assertEqual(report['semantic_completeness'], 'not_assessed')
        self.assertEqual(report['counts']['dispositions'], dict(split=1, keep=1, exclude=1, uncertain=1))
        self.assertEqual((raws, ledger), before)

    def test_empty_template_never_certifies_reading_or_dispositions(self):
        raws, _ = fixture()
        ledger = coverage.template(raws)
        report = coverage.audit(raws, ledger)
        self.assertEqual(report['structure'], 'passed')
        self.assertEqual(report['workflow'], 'partial')
        self.assertEqual(report['counts']['actual_passes'], 0)
        self.assertIn('C1:disposition', report['pending'])
        self.assertIn('G1:no_candidate_provenance', report['pending'])

    def test_changed_final_conditions_or_candidates_invalidate_ledger(self):
        for name in ('extraction', 'candidates'):
            raws, ledger = fixture()
            changed = json.loads(raws[name])
            changed['candidates'][0]['context'] = ['新增条件']
            raws[name] = encode(changed)
            report = coverage.audit(raws, ledger)
            self.assertEqual(report['structure'], 'failed')
            self.assertTrue(any('version/hash' in e for e in report['errors']))

    def test_missing_duplicate_and_unknown_dispositions_rejected(self):
        for change in ('missing', 'duplicate', 'unknown_goal', 'single_split', 'excluded_with_goal', 'merge_without_peer'):
            raws, ledger = fixture()
            if change == 'missing': ledger['entries'].pop()
            elif change == 'duplicate': ledger['entries'].append(copy.deepcopy(ledger['entries'][0]))
            elif change == 'unknown_goal': ledger['entries'][0]['final_goal_ids'] = ['G404', 'G2']
            elif change == 'single_split': ledger['entries'][0]['final_goal_ids'] = ['G1']
            elif change == 'excluded_with_goal': ledger['entries'][2]['final_goal_ids'] = ['G1']
            else: ledger['entries'][1]['disposition'] = 'merge'
            with self.subTest(change=change):
                self.assertEqual(coverage.audit(raws, ledger)['structure'], 'failed')

    def test_synonym_merge_keeps_both_source_candidates(self):
        raws, ledger = fixture()
        capture = json.loads(raws['candidates'])
        capture['candidates'].append(dict(copy.deepcopy(capture['candidates'][1]), candidate_id='C5'))
        raws['candidates'] = encode(capture)
        ledger['input_binding'] = coverage.binding(raws)
        ledger['entries'].append(dict(candidate_id='C5', disposition='merge', final_goal_ids=['G3'], reason='主体范围条件相同。'))
        self.assertEqual(coverage.audit(raws, ledger)['workflow'], 'recorded')

    def test_tampered_source_window_and_quote_fail_even_after_rebinding_ledger(self):
        for change in ('source', 'window_text', 'window_missing', 'candidate_quote', 'candidate_offset', 'window_reference'):
            raws, ledger = fixture()
            if change == 'source': raws['source'] += b'changed'
            elif change.startswith('window_') and change != 'window_reference':
                bundle = json.loads(raws['windows'])
                if change == 'window_text': bundle['windows'][0]['text'] += '改写'
                else: bundle['windows'].pop()
                raws['windows'] = encode(bundle)
            else:
                capture = json.loads(raws['candidates'])
                if change == 'candidate_quote': capture['candidates'][0]['evidence_candidates'][0]['quote'] = '虚构引文'
                elif change == 'candidate_offset': capture['candidates'][0]['evidence_candidates'][0]['start_char'] += 1
                else: capture['candidates'][0]['window_ids'] = [json.loads(raws['windows'])['windows'][-1]['window_id']]
                raws['candidates'] = encode(capture)
            ledger['input_binding'] = coverage.binding(raws)
            with self.subTest(change=change):
                self.assertEqual(coverage.audit(raws, ledger)['structure'], 'failed')

    def test_processed_windows_do_not_replace_full_context_review(self):
        raws, ledger = fixture()
        ledger['full_context_review'] = dict(status='partial', source_ids=[], reason='仅局部核对')
        report = coverage.audit(raws, ledger)
        self.assertEqual(report['structure'], 'passed')
        self.assertIn('full_context_review', report['pending'])
        self.assertEqual(report['workflow'], 'partial')

    def test_targeted_pass_can_skip_windows_but_initial_pass_cannot_claim_full_coverage(self):
        raws, ledger = fixture()
        focused = copy.deepcopy(ledger['run']['passes'][0])
        focused.update(pass_id='P2', kind='focused')
        focused['window_results'][-1].update(status='skipped', reason='补查范围外')
        ledger['run']['passes'].append(focused)
        self.assertEqual(coverage.audit(raws, ledger)['workflow'], 'recorded')
        ledger['run']['passes'][0]['window_results'][-1].update(status='skipped', reason='尚未读取')
        report = coverage.audit(raws, ledger)
        self.assertEqual(report['workflow'], 'partial')
        self.assertIn('run:initial_full_source_pass', report['pending'])

    def test_misleading_completed_review_and_missing_window_status_rejected(self):
        for change in ('incomplete_review', 'missing_window', 'not_run_processed', 'completed_pending'):
            raws, ledger = fixture()
            if change == 'incomplete_review': ledger['full_context_review']['source_ids'].pop()
            elif change == 'missing_window': ledger['run']['passes'][0]['window_results'].pop()
            elif change == 'not_run_processed': ledger['run']['passes'][0]['status'] = 'not_run'
            else: ledger['run']['passes'][0]['window_results'][-1]['status'] = 'pending'
            with self.subTest(change=change):
                self.assertEqual(coverage.audit(raws, ledger)['structure'], 'failed')

    def test_final_goal_without_provenance_is_reported_not_silently_accepted(self):
        raws, ledger = fixture()
        ledger['entries'][0].update(disposition='keep', final_goal_ids=['G1'])
        ledger['source_checks'] = []
        report = coverage.audit(raws, ledger)
        self.assertEqual(report['structure'], 'passed')
        self.assertIn('G2:no_candidate_provenance', report['pending'])

    def test_source_checks_cannot_claim_mappings_different_from_dispositions(self):
        raws, ledger = fixture()
        ledger['source_checks'][0]['final_goal_ids'] = ['G3']
        self.assertEqual(coverage.audit(raws, ledger)['structure'], 'failed')

    def test_zero_goals_is_allowed_but_empty_process_is_not_completed(self):
        raws, _ = fixture()
        for name in ('candidates', 'extraction'):
            data = json.loads(raws[name]); data['candidates'] = []; raws[name] = encode(data)
        ledger = coverage.template(raws)
        report = coverage.audit(raws, ledger)
        self.assertEqual(report['structure'], 'passed')
        self.assertEqual(report['workflow'], 'partial')
        self.assertIn('run:no_passes', report['pending'])

    def test_cli_is_self_contained_readonly_and_reports_exit_codes(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            # Only the extraction skill is installed; no dependency on legacy tracing.
            shutil.copytree(ROOT / 'skills/goal-extraction', base / 'skill', ignore=shutil.ignore_patterns('__pycache__'))
            raws, ledger = fixture()
            paths = {key: base / (key + ('.txt' if key == 'source' else '.json')) for key in raws}
            for key, path in paths.items(): path.write_bytes(raws[key])
            ledger_path = base / 'ledger.json'; ledger_path.write_bytes(encode(ledger))
            script = base / 'skill/scripts/check_coverage.py'
            arguments = [a for key, path in paths.items() for a in ('--' + key.replace('_', '-'), str(path))]
            before = {p: p.read_bytes() for p in [*paths.values(), ledger_path]}
            def invoke(command, output, extra=()):
                return subprocess.run([sys.executable, str(script), command, *arguments, '--output', str(output), *extra],
                                      cwd=base, capture_output=True, timeout=30)
            result = invoke('check', base / 'report.json', ['--ledger', str(ledger_path)])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads((base / 'report.json').read_bytes())['ledger_sha256'], digest(before[ledger_path]))
            self.assertEqual(invoke('check', base / 'report.json', ['--ledger', str(ledger_path)]).returncode, 2)
            self.assertEqual(invoke('template', base / 'blank-ledger.json').returncode, 0)
            self.assertEqual(invoke('check', base / 'partial-report.json', ['--ledger', str(base / 'blank-ledger.json')]).returncode, 1)
            self.assertTrue(all(p.read_bytes() == raw for p, raw in before.items()))
            source_args = [a for key in ('source_input', 'source', 'windows') for a in ('--' + key.replace('_', '-'), str(paths[key]))]
            result = subprocess.run([sys.executable, str(script), 'capture-template', *source_args, '--output', str(base/'capture.json')],
                                    cwd=base, capture_output=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads((base/'capture.json').read_bytes())['candidates'], [])

    def test_new_final_extraction_passes_existing_trace_and_model_contracts(self):
        from trace_candidates import judgment_template, trace
        sys.path.insert(0, str(ROOT / 'skills/goal-model-building/scripts'))
        import kaos_model as k
        raws, _ = fixture()
        data = json.loads(raws['extraction'])
        judgments = judgment_template(data, raws['extraction'])
        for goal in data['candidates']:
            judgments['judgments'][goal['candidate_id']].update(label='direct', rationale='合成资料明确表述，开发者测试判断。', supported_parts=[goal['statement']])
        tracing = trace(data, judgments, raws['source'].decode('utf-8'), digest(raws['extraction']))
        self.assertTrue(all(t['support']['label'] == 'direct' for t in tracing['traces']))
        jraw = encode(judgments)
        decisions = k.decision_template(raws['extraction'], jraw)
        model = k.build(raws['extraction'], jraw, raws['source'], encode(decisions))
        self.assertEqual(model['schema_version'], 'goalforge-kaos-1')
        self.assertEqual(len(model['goals']), 3)
        self.assertEqual(model['refinement_groups'], [])


if __name__ == '__main__':
    unittest.main()
