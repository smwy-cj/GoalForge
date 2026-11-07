"""v2 relation lifecycle, v1 compatibility, dependency invalidation and exports."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from test_kaos_model import fixture as legacy_fixture, case as legacy_case, k


def fixture():
    data, source, judgments, decisions = legacy_fixture()
    decisions.update(schema_version='goalforge-kaos-decisions-2', relations=[], reassessments=[])
    for group in decisions['groups']:
        group['relation_ids'] = []
        group['checks'] = [dict(kind=kind, origin='analysis_assumption', scenario=scenario, outcome='supports',
                                rationale='仅针对合成资料定义的有效申请和允许渠道，未扩展到其他系统。')
                           for kind, scenario in [('normal', '指定有效申请按允许渠道处理。'), ('exception', '未送达或登记不全时，子目标也不满足，不构成子目标满足而父目标不满足的反例。')]]
    quote = copy.deepcopy(decisions['groups'][0]['evidence_quotes'][0])
    decisions['relations'] = [dict(relation_id='R1', source_id='G2', target_id='G1', type='contribution', status='supported',
                                    conditions=[], assumptions=[], rationale='登记有助于申请处理目标，单独登记不保证回执送达。', evidence_ids=[], evidence_quotes=[quote])]
    decisions['groups'][0]['relation_ids'] = ['R1']
    return data, source, judgments, decisions


def build_fixture():
    data, source, j, d = fixture()
    return k.build(k.encode(data), k.encode(j), source, k.encode(d))


def feedback(model, kind='relation', identifier='R1'):
    return dict(schema_version=k.FEEDBACK2, model=k.binding(model), status='submitted', entries=[
        dict(target_type=kind, target_id=identifier, decision='modify', comment='合成测试意见：请重新评估。')], form_drafts={}, note='')


class RelationTests(unittest.TestCase):
    def test_relations_stay_separate_from_refinement_and_keep_evidence(self):
        model = build_fixture()
        self.assertEqual(model['schema_version'], k.SCHEMA2)
        self.assertEqual(len(k.dag_layout(model)['edges']), 7)
        self.assertEqual(model['relations'][0]['status'], 'supported')
        self.assertTrue(model['relations'][0]['evidence_ids'][0].startswith('K'))
        self.assertIn('不表示充分精化', k.markdown(model))
        self.assertNotIn('data-relation', k.svg(model))
        self.assertIn('data-relation="R1"', k.relations_svg(model))

    def test_invalid_relations_and_no_silent_v1_fields(self):
        for variant in ('endpoint', 'self', 'type', 'status', 'duplicate', 'no_basis', 'unsupported', 'v1'):
            data, source, j, d = fixture()
            r = d['relations'][0]
            if variant == 'endpoint': r['target_id'] = 'missing'
            elif variant == 'self': r['target_id'] = r['source_id']
            elif variant == 'type': r['type'] = 'refinement'
            elif variant == 'status': r['status'] = 'confirmed'
            elif variant == 'duplicate': d['relations'].append(dict(copy.deepcopy(r), relation_id='R2'))
            elif variant == 'no_basis': r['evidence_quotes'][0]['role'] = 'context'
            elif variant == 'v1': d['schema_version'] = 'goalforge-kaos-decisions-1'
            else:
                j['judgments']['G2']['label'] = 'insufficient'
                d['input_binding']['judgments_sha256'] = k.digest(k.encode(j)); d['groups'] = []
            with self.subTest(variant=variant), self.assertRaises(ValueError):
                k.build(k.encode(data), k.encode(j), source, k.encode(d))

    def test_type_specific_cycles_allow_mutual_contribution_only(self):
        for kind in k.RELATION_TYPES:
            data, source, j, d = fixture()
            d['groups'] = []
            d['relations'][0]['type'] = kind
            r = dict(copy.deepcopy(d['relations'][0]), relation_id='R2', source_id='G1', target_id='G2')
            d['relations'].append(r)
            with self.subTest(kind=kind):
                if kind == 'contribution':
                    self.assertEqual(len(k.build(k.encode(data), k.encode(j), source, k.encode(d))['relations']), 2)
                else:
                    with self.assertRaisesRegex(ValueError, 'cycle'):
                        k.build(k.encode(data), k.encode(j), source, k.encode(d))

    def test_proposed_rejected_and_counterexamples_cannot_establish_refinement(self):
        for variant in ('proposed', 'rejected', 'counterexample', 'unknown', 'missing_check'):
            data, source, j, d = fixture()
            if variant in ('proposed', 'rejected'): d['relations'][0]['status'] = variant
            elif variant == 'missing_check': d['groups'][0]['checks'].pop()
            else: d['groups'][0]['checks'][1]['outcome'] = variant
            with self.subTest(variant=variant), self.assertRaises(ValueError):
                k.build(k.encode(data), k.encode(j), source, k.encode(d))
            d['groups'][0].update(status='proposed', completeness='partial')
            model = k.build(k.encode(data), k.encode(j), source, k.encode(d))
            self.assertFalse(k.active(model['refinement_groups'][0]))

    def test_feedback_propagates_from_goals_to_relations_and_groups(self):
        model = build_fixture()
        request = k.process_feedback(model, feedback(model, 'goal', 'G2'))
        self.assertEqual(request['affected_relation_ids'], ['R1'])
        self.assertEqual(request['affected_group_ids'], ['F1'])
        request = k.process_feedback(model, feedback(model))
        self.assertEqual(request['affected_goal_ids'], [])
        self.assertEqual(request['affected_group_ids'], ['F1'])
        old_packet = feedback(model); old_packet['schema_version'] = k.FEEDBACK
        with self.assertRaises(ValueError): k.validate_feedback(old_packet, model, True)

    def test_revision_requires_reassessment_and_keeps_unresolved_opinions(self):
        data, source, j, d = fixture(); model = build_fixture(); packet = feedback(model)
        with self.assertRaisesRegex(ValueError, 'reassessments'):
            k.build(k.encode(data), k.encode(j), source, k.encode(d), previous=model, feedback=packet)
        d['reassessments'] = [dict(assessment_id='A1', target_type='relation', target_id='R1', reason='重新核对贡献范围。'),
                              dict(assessment_id='A2', target_type='group', target_id='F1', reason='重查依赖联系的整组充分性。')]
        revised = k.build(k.encode(data), k.encode(j), source, k.encode(d), previous=model, feedback=packet)
        self.assertEqual(revised['review'], {'status': 'pending'})
        self.assertTrue(any(i['target_type'] == 'relation' and '前轮' in i['message'] for i in revised['issues']))
        self.assertEqual(revised['changes'][0]['before_relations'], model['relations'])

    def test_changed_conditions_even_without_goal_feedback_invalidate_relations(self):
        from trace_candidates import judgment_template
        data, source, j, d = fixture(); model = build_fixture(); packet = feedback(model, 'model', model['model_id'])
        data['candidates'][1]['context'] = ['仅在人工录入场景']
        current_j = judgment_template(data, k.encode(data)); current_j['judgments'] = j['judgments']
        d['input_binding'] = dict(extraction_sha256=k.digest(k.encode(data)), judgments_sha256=k.digest(k.encode(current_j)))
        with self.assertRaisesRegex(ValueError, 'reassessments'):
            k.build(k.encode(data), k.encode(current_j), source, k.encode(d), previous=model, feedback=packet)

    def test_changed_relation_quote_with_same_evidence_id_invalidates_dependents(self):
        data, source, j, d = fixture(); model = build_fixture(); packet = feedback(model, 'model', model['model_id'])
        d['relations'][0]['evidence_quotes'] = copy.deepcopy(d['groups'][1]['evidence_quotes'])
        with self.assertRaisesRegex(ValueError, 'reassessments'):
            k.build(k.encode(data), k.encode(j), source, k.encode(d), previous=model, feedback=packet)

    def test_source_change_outside_existing_quotes_invalidates_old_judgments(self):
        from trace_candidates import judgment_template
        data, source, j, d = fixture(); model = build_fixture(); packet = feedback(model, 'model', model['model_id'])
        source += '补充场景与例外，需重新核对。\n'.encode('utf-8')
        data['document_hash'] = k.digest(source)
        current_j = judgment_template(data, k.encode(data)); current_j['judgments'] = j['judgments']
        d['input_binding'] = dict(extraction_sha256=k.digest(k.encode(data)), judgments_sha256=k.digest(k.encode(current_j)))
        with self.assertRaisesRegex(ValueError, 'reassessments'):
            k.build(k.encode(data), k.encode(current_j), source, k.encode(d), previous=model, feedback=packet)

    def test_migration_requires_explicit_binding_and_keeps_v1_unchanged(self):
        data, source, j, old_d = legacy_fixture()
        old = k.build(k.encode(data), k.encode(j), source, k.encode(old_d)); saved = copy.deepcopy(old)
        d = k.decision_template(k.encode(data), k.encode(j), 2)
        d['migration_parent'] = k.binding(old)
        with self.assertRaises(ValueError): k.build(k.encode(data), k.encode(j), source, k.encode(d))
        new = k.build(k.encode(data), k.encode(j), source, k.encode(d), migration=old)
        self.assertEqual(new['goals'], old['goals'])
        self.assertEqual(new['relations'], [])
        self.assertEqual(new['refinement_groups'], [])
        self.assertEqual(new['changes'][0]['removed_group_ids'], ['F1', 'F2', 'F3'])
        self.assertTrue(any('尚未重新编制' in i['message'] for i in new['issues']))
        self.assertEqual(old, saved)

    def test_cli_delivery_feedback_exports_and_tamper_detection(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp); data, source, j, d = fixture()
            for name, raw in [('extraction.json', k.encode(data)), ('source.txt', source), ('judgments.json', k.encode(j)), ('decisions.json', k.encode(d))]:
                (base/name).write_bytes(raw)
            script = Path(k.__file__)
            def cli(*args):
                result = subprocess.run([sys.executable, '-X', 'utf8', str(script), *map(str,args)], capture_output=True, timeout=30)
                self.assertEqual(result.returncode, 0, result.stderr.decode('utf-8', errors='replace'))
            cli('template',base/'extraction.json',base/'judgments.json',base/'template.json')
            self.assertEqual(k.load(base/'template.json')['schema_version'], 'goalforge-kaos-decisions-2')
            cli('assemble',base/'extraction.json',base/'judgments.json',base/'source.txt',base/'decisions.json',base/'assembled')
            cli('inspect',base/'assembled/model-input.json',base/'report.json')
            cli('finalize',base/'assembled/model-input.json',base/'report.json',base/'delivery','--svg')
            model = k.load(base/'delivery/goal-model.json')
            self.assertEqual((base/'delivery/goal-relations.svg').read_text(encoding='utf-8'),k.relations_svg(model))
            (base/'feedback.json').write_bytes(k.encode(feedback(model)))
            cli('feedback',base/'delivery/goal-model.json',base/'feedback.json',base/'feedback-output')
            self.assertEqual(k.load(base/'feedback-output/revision-request.json')['affected_relation_ids'], ['R1'])
            from serve_model import save_export
            receipt = save_export(model,base/'delivery',dict(kind='relations-svg',content=k.relations_svg(model)))
            self.assertTrue(Path(receipt['path']).is_file())
            model['relations'][0]['conditions'] = ['篡改条件']
            with self.assertRaises(ValueError): k.inspect(model,base/'delivery')

    def test_upgrade_cli_does_not_infer_types_from_legacy_groups(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp); old, _ = legacy_case(base/'old')
            script = Path(k.__file__)
            command = [sys.executable, str(script), 'upgrade-template', str(base/'old/model-input.json'), str(base/'upgrade.json')]
            result = subprocess.run(command,capture_output=True,timeout=30)
            self.assertEqual(result.returncode,0,result.stderr)
            upgrade = k.load(base/'upgrade.json')
            self.assertEqual(upgrade['groups'],[]);self.assertEqual(upgrade['relations'],[])
            self.assertEqual(upgrade['migration_parent'], k.binding(old))
            inputs = base/'old/attachments'
            args = [sys.executable,str(script),'assemble',str(inputs/'extraction.json'),str(inputs/'judgments.json'),str(inputs/'source.txt'),str(base/'upgrade.json'),str(base/'upgraded'),'--migrate-from',str(base/'old/model-input.json')]
            result=subprocess.run(args,capture_output=True,timeout=30)
            self.assertEqual(result.returncode,0,result.stderr)
            migrated=k.load(base/'upgraded/model-input.json')
            report=k.inspect(migrated,base/'upgraded')
            self.assertEqual(report['structure'],'passed')
            k.package(migrated,base/'upgraded',base/'delivery',report,with_svg=True)
            self.assertEqual(k.load(base/'delivery/goal-model.json')['parent'],k.binding(old))

    def test_material_literal_template_tokens_do_not_corrupt_html_payload(self):
        import re
        from trace_candidates import judgment_template
        for version in (1, 2):
            with self.subTest(version=version), tempfile.TemporaryDirectory() as tmp:
                data, source, j, d = fixture() if version == 2 else legacy_fixture()
                literal='__CSS__ __PAYLOAD__ __CORE__ __UI__'
                data['limitations'].append(literal)
                current_j=judgment_template(data,k.encode(data));current_j['judgments']=j['judgments']
                d['input_binding']=dict(extraction_sha256=k.digest(k.encode(data)),judgments_sha256=k.digest(k.encode(current_j)))
                raws=[k.encode(data),k.encode(current_j),source,k.encode(d)]
                model=k.build(*raws);base=Path(tmp)/'assembled'
                for name,raw in zip(['extraction.json','judgments.json','source.txt','kaos-decisions.json'],raws):
                    path=base/'attachments'/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
                    model['input_artifacts'].append(dict(path='attachments/'+name,sha256=k.digest(raw)))
                k.package(model,base,Path(tmp)/'delivery')
                page=(Path(tmp)/'delivery/goal-model.html').read_text(encoding='utf-8')
                payload=json.loads(re.search(r'<script id="payload" type="application/json">(.*?)</script>',page,re.S).group(1))
                self.assertEqual(payload['model'],model)
                self.assertIn(literal,payload['model']['limitations'])


if __name__ == '__main__': unittest.main()
