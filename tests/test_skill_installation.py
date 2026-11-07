"""Installation/compatibility checks with synthetic authoring, not extraction accuracy."""
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from test_kaos_model import fixture, feedback, k
from trace_candidates import trace, judgment_template

ROOT = Path(__file__).resolve().parents[1]
FORMAL_SKILLS = ('goal-extraction', 'goal-model-building', 'model-review')


def install_three(destination):
    skills = Path(destination) / 'skills'
    for name in FORMAL_SKILLS:
        shutil.copytree(ROOT / 'skills' / name, skills / name,
                        ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    return skills


def cli(script, *args, cwd):
    result = subprocess.run([sys.executable, str(script), *(str(a) for a in args)],
                            cwd=str(cwd), capture_output=True, text=True,
                            encoding='utf-8', errors='replace', timeout=30,
                            env=dict(os.environ, PYTHONIOENCODING='utf-8'))
    if result.returncode:
        raise AssertionError(str(script) + '\n' + result.stdout + result.stderr)
    return result


def isolated_workflow(destination):
    """Exercise CLI delivery and feedback with only the three sibling packages."""
    destination = Path(destination)
    skills = install_three(destination)
    work = destination / 'work'
    work.mkdir()
    data, source, judgments, decisions = fixture()
    for name, raw in [('extraction.json', k.encode(data)), ('source.txt', source)]:
        (work / name).write_bytes(raw)
    tracer = skills / 'goal-extraction/scripts/trace_candidates.py'
    modeler = skills / 'goal-model-building/scripts/kaos_model.py'
    cli(tracer, work/'extraction.json', '--judgment-template', work/'judgments.json', cwd=work)
    authored = k.load(work/'judgments.json')
    authored['judgments'] = judgments['judgments']
    (work/'judgments.json').write_bytes(k.encode(authored))
    before = {p.name: p.read_bytes() for p in work.iterdir() if p.is_file()}
    cli(tracer, work/'extraction.json', work/'tracing', '--source', work/'source.txt',
        '--judgments', work/'judgments.json', '--review-md', cwd=work)
    assert all((work/name).read_bytes() == raw for name, raw in before.items())
    cli(modeler, 'template', work/'extraction.json', work/'judgments.json', work/'kaos-decisions.json', '--schema-version', '1', cwd=work)
    authored_decisions = k.load(work/'kaos-decisions.json')
    authored_decisions['groups'] = decisions['groups']
    (work/'kaos-decisions.json').write_bytes(k.encode(authored_decisions))
    cli(modeler, 'assemble', work/'extraction.json', work/'judgments.json', work/'source.txt',
        work/'kaos-decisions.json', work/'assembled', cwd=work)
    cli(modeler, 'inspect', work/'assembled/model-input.json', work/'inspection.json', cwd=work)
    cli(modeler, 'finalize', work/'assembled/model-input.json', work/'inspection.json', work/'delivery', cwd=work)
    report = k.load(work/'inspection.json')
    assert report['structure'] == 'passed' and report['independent_semantic'] == 'not_run'
    model = k.load(work/'delivery/goal-model.json')
    (work/'feedback.json').write_bytes(k.encode(feedback(model)))
    cli(modeler, 'feedback', work/'delivery/goal-model.json', work/'feedback.json', work/'feedback-output', cwd=work)
    request = k.load(work/'feedback-output/revision-request.json')
    assert request['affected_goal_ids'] == ['G3']
    assert request['affected_group_ids'] == ['F1', 'F2', 'F3']
    # Same synthetic targets are re-authored for the feedback-bound revision;
    # unresolved feedback must remain, even when there is no statement change.
    cli(modeler, 'assemble', work/'extraction.json', work/'judgments.json', work/'source.txt',
        work/'kaos-decisions.json', work/'revised', '--previous', work/'delivery/goal-model.json',
        '--feedback', work/'feedback-output/review-feedback.json', cwd=work)
    cli(modeler, 'inspect', work/'revised/model-input.json', work/'revised-inspection.json', cwd=work)
    cli(modeler, 'finalize', work/'revised/model-input.json', work/'revised-inspection.json', work/'revised-delivery', cwd=work)
    revised = k.load(work/'revised-delivery/goal-model.json')
    assert revised['review']['status'] == 'pending'
    assert any('前轮意见尚待处理' in i['message'] for i in revised['issues'])
    for skill, script in [('goal-model-building','reconcile_model.py'),
                          ('goal-model-building','revise_model.py'),
                          ('model-review','process_feedback.py')]:
        cli(skills / skill / 'scripts' / script, '--help', cwd=work)
    assert not (skills/'goal-tracing').exists()
    return dict(formal_skills=list(FORMAL_SKILLS), structure=report['structure'],
                independent_semantic=report['independent_semantic'], formal_proof=report['formal_proof'],
                input_unchanged=True, feedback_scope=request['affected_goal_ids'],
                unresolved_feedback_preserved=True, delivery=str(work/'delivery/goal-model.html'),
                revised_delivery=str(work/'revised-delivery/goal-model.html'))


class SkillInstallationTests(unittest.TestCase):
    def test_three_skill_installation_runs_delivery_and_feedback(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = isolated_workflow(tmp)
            self.assertEqual(result['structure'], 'passed')



    def test_partial_support_preserves_original_decision_and_cannot_establish_refinement(self):
        for label in ('direct', 'inferred'):
            with self.subTest(label=label):
                data, source, judgments, decisions = fixture()
                judgments['judgments']['G1'].update(label=label, unsupported_parts=['并收到有效回执'])
                original = copy.deepcopy(data)
                traced = trace(data, judgments, source.decode(), k.digest(k.encode(data)))
                self.assertEqual(traced['traces'][0]['submitted_semantic_judgment']['label'], label)
                self.assertEqual(traced['traces'][0]['support']['label'], 'insufficient')
                self.assertIn('partial_support', [i['code'] for i in traced['traces'][0]['issues']])
                self.assertEqual(traced['traces'][1]['support']['label'], 'direct')
                self.assertEqual(data, original)
                decisions['input_binding']['judgments_sha256'] = k.digest(k.encode(judgments))
                with self.assertRaisesRegex(ValueError, 'unsupported goals'):
                    k.build(k.encode(data), k.encode(judgments), source, k.encode(decisions))
                decisions['groups'] = []
                model = k.build(k.encode(data), k.encode(judgments), source, k.encode(decisions))
                self.assertTrue(any(i['target_id'] == 'G1' and i['blocking'] for i in model['issues']))
                self.assertFalse(any(i['target_id'] == 'G2' and i['blocking'] for i in model['issues']))

    def test_empty_goal_list_is_valid_completed_verification(self):
        data, source, _, _ = fixture()
        data['candidates'] = []
        traced = trace(data, judgment_template(data), source.decode())
        self.assertEqual(traced['traces'], [])
        self.assertEqual(traced['status'], 'completed')

    def test_changed_conditions_invalidate_support_even_with_same_statement(self):
        data, source, judgments, _ = fixture()
        data['candidates'][0]['context'] = ['仅在工作日']
        with self.assertRaisesRegex(ValueError, 'version/hash'):
            trace(data, judgments, source.decode())


if __name__ == '__main__':
    unittest.main()
