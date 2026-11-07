import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/goal-model-building/scripts'))
import kaos_model as k
from trace_candidates import judgment_template


def fixture():
    source = '这是一份合成的工程测试资料，不是真实访谈。\n用户希望有效申请得到登记，并收到有效回执。\n有效申请得到完整登记、有效回执送达，两项都满足即可实现上述目标。\n回执允许通过邮件或短信送达，任一种渠道送达都算完成。\n用户希望收到邮件回执，或收到短信回执。\n'
    statements = ['有效申请得到登记，并收到有效回执', '有效申请得到完整登记', '有效回执送达', '收到邮件回执', '收到短信回执']
    data = dict(schema_version='goalforge-extraction-3', document_id='SYN-KAOS', document_hash=k.digest(source.encode()), status='completed',
                materials=[dict(material_id='M1', file_name='合成预约说明.md', media_type='text/markdown', original_hash=k.digest(source.encode()), id_origin='generated', processing_status='processed')],
                conversion=dict(canonical_text_path='source.txt', method='native_text', issues=[]),
                segments=[dict(source_id='SYN-KAOS:S1', material_id='M1', text=source, speaker='合成角色', original_locator=dict(start_char=0, paragraph=1), recognition_status='native_text')],
                coverage=dict(scope='provided_material', source_ids=['SYN-KAOS:S1'], omissions=[]), candidates=[], review_questions=[], limitations=['本示例为合成资料与开发判断，用于审核新版表达方式，不代表真实资料准确率。'])
    for i, statement in enumerate(statements, 1):
        start = source.index(statement)
        data['candidates'].append(dict(candidate_id='G'+str(i), statement=statement, origin='explicit', actor='用户', context=[], inference=None, review_status='pending',
                                       evidence_candidates=[dict(source_id='SYN-KAOS:S1', quote=statement, role='basis', start_char=start, end_char=start+len(statement))]))
    raw = k.encode(data)
    judgments = judgment_template(data, raw)
    for g in data['candidates']:
        judgments['judgments'][g['candidate_id']].update(label='direct', rationale='合成资料直接陈述该结果，本判断由开发者编制。', supported_parts=[g['statement']])
    jraw = k.encode(judgments)
    decisions = k.decision_template(raw, jraw)
    for gid, parent, children, rationale in [('F1','G1',['G2','G3'],'原文明确说明登记和送达共同满足上层目标。'),('F2','G3',['G4'],'原文允许邮件作为一种完整送达方案。'),('F3','G3',['G5'],'原文允许短信作为另一种完整送达方案。')]:
        relation_quote = '有效申请得到完整登记、有效回执送达，两项都满足即可实现上述目标。' if gid=='F1' else '回执允许通过邮件或短信送达，任一种渠道送达都算完成。'
        offset=source.index(relation_quote)
        decisions['groups'].append(dict(group_id=gid, parent_id=parent, child_ids=children, kind='and', status='supported', completeness='complete',
                                       rationale=rationale, assumptions=[] if gid=='F1' else ['邮件和短信均为本场景允许的回执渠道。'], evidence_ids=['E0001','E0002','E0003','E0004','E0005'],
                                       evidence_quotes=[dict(source_id='SYN-KAOS:S1',quote=relation_quote,role='basis',start_char=offset,end_char=offset+len(relation_quote))]))
    return data, source.encode(), judgments, decisions


def case(base):
    data, source, judgments, decisions = fixture()
    raws = [k.encode(data), k.encode(judgments), source, k.encode(decisions)]
    model = k.build(*raws)
    names = ['extraction.json','judgments.json','source.txt','kaos-decisions.json']
    for name, raw in zip(names, raws):
        p = Path(base)/'attachments'/name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(raw)
        model['input_artifacts'].append(dict(path='attachments/'+name, sha256=k.digest(raw)))
    (Path(base)/'model-input.json').write_bytes(k.encode(model))
    return model, raws


def feedback(model):
    return dict(schema_version=k.FEEDBACK, model=k.binding(model), status='submitted', note='', form_drafts={},
                entries=[dict(target_type='goal', target_id='G3', decision='modify', comment='请核对有效的含义，说明是否确有明确标准。')])


class KaosTests(unittest.TestCase):
    def test_goal_only_contract_short_document_and_bound_trace(self):
        from simple_candidates import validate, render
        from trace_candidates import trace
        data, source, judgments, _ = fixture()
        validate(data)
        doc = render(data)
        self.assertNotIn('主类', doc)
        self.assertNotIn('classification', doc)
        self.assertEqual(len(trace(data, judgments, source.decode(), k.digest(k.encode(data)))['traces']), 5)
        data['candidates'][0]['subtype']='achievement'
        with self.assertRaises(ValueError): validate(data)

    def test_grouped_and_or_model_without_all_pairs_and_embedded_exports(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp)/'base'; model,_=case(base)
            report=k.inspect(model,base)
            self.assertEqual(report['readiness'],'reviewable')
            out=Path(tmp)/'delivery'; k.package(model,base,out,report)
            text=(out/'goal-model.html').read_text(encoding='utf-8')
            self.assertIn('simple-feedback-1',text)
            self.assertIn('完整内容',text)
            self.assertNotIn('__PAYLOAD__',text)
            self.assertIn('方案 2', (out/'goal-model.md').read_text(encoding='utf-8'))
            self.assertFalse((out/'goal-model.svg').exists())
            self.assertEqual(k.inspect(k.load(out/'goal-model.json'),out),report)
            manifest=k.load(out/'manifest.json')
            for item in manifest['files']: self.assertEqual(k.digest((out/item['path']).read_bytes()),item['sha256'])

    def test_stale_judgment_or_decision_rejected(self):
        data,source,judgments,decisions=fixture()
        data['candidates'][0]['statement']+='（变更）'
        with self.assertRaises(ValueError): k.build(k.encode(data),k.encode(judgments),source,k.encode(decisions))
        data,source,judgments,decisions=fixture();decisions['input_binding']['judgments_sha256']='old'
        with self.assertRaises(ValueError): k.build(k.encode(data),k.encode(judgments),source,k.encode(decisions))

    def test_invalid_group_cycles_duplicates_and_evidence(self):
        for bad in ('cycle','unknown','duplicate','unsupported_kind','evidence'):
            data,source,j,d=fixture()
            if bad=='cycle': d['groups'][1]['child_ids']=['G1']
            elif bad=='unknown': d['groups'][0]['child_ids']=['G9']
            elif bad=='duplicate': d['groups'].append(dict(d['groups'][0],group_id='FX'))
            elif bad=='unsupported_kind': d['groups'][0]['kind']='or'
            else: d['groups'][0]['evidence_ids']=['nope']
            with self.subTest(bad=bad),self.assertRaises(ValueError): k.build(k.encode(data),k.encode(j),source,k.encode(d))

    def test_partial_refinement_is_question_not_established_hierarchy(self):
        data,source,j,d=fixture();d['groups'][0]['completeness']='partial'
        model=k.build(k.encode(data),k.encode(j),source,k.encode(d))
        self.assertFalse(k.active(model['refinement_groups'][0]))
        self.assertTrue(any(i['target_id']=='F1' for i in model['issues']))

    def test_shared_children_and_multiple_roots_preserved(self):
        data,source,j,d=fixture();d['groups'].append(dict(d['groups'][0],group_id='F4',parent_id='G2',child_ids=['G4']))
        model=k.build(k.encode(data),k.encode(j),source,k.encode(d))
        self.assertIn('同一目标的再次引用',k.markdown(model))

    def test_source_tampering_model_tampering_and_stale_report_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp);model,_=case(base);report=k.inspect(model,base)
            changed=copy.deepcopy(model);changed['goals'][0]['statement']='伪造目标'
            with self.assertRaises(ValueError): k.inspect(changed,base)
            report['formal_proof']='passed'
            with self.assertRaises(ValueError): k.package(model,base,base/'delivery',report)
            (base/'attachments/source.txt').write_bytes(b'changed')
            with self.assertRaises(ValueError): k.inspect(model,base)

    def test_feedback_binding_unfinished_forms_duplicate_and_group_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            model,_=case(tmp);p=feedback(model)
            result=k.process_feedback(model,p)
            self.assertEqual(result['affected_group_ids'],['F1','F2','F3'])
            p['entries']=[dict(target_type='group',target_id='F2',decision='modify',comment='请核对该渠道是否足够。')]
            self.assertEqual(k.process_feedback(model,p)['affected_goal_ids'],[])
            for change in ('version','draft','duplicate','unknown'):
                q=copy.deepcopy(p)
                if change=='version':q['model']['version']='old'
                elif change=='draft':q['form_drafts']={'goal:G1':dict(target_type='goal',target_id='G1',decision='',comment='未完')}
                elif change=='duplicate':q['entries']*=2
                else:q['entries'][0]['target_id']='missing'
                with self.subTest(change=change),self.assertRaises(ValueError):k.validate_feedback(q,model,True)

    def test_rebuild_after_feedback_requires_current_proofs_and_returns_pending(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp)/'base';model,raws=case(base);packet=feedback(model)
            revised=k.build(*raws,previous=model,feedback=packet)
            revised['input_artifacts']=copy.deepcopy(model['input_artifacts'])
            for name,value in [('previous-model.json',model),('review-feedback.json',packet)]:
                raw=k.encode(value);(base/'attachments'/name).write_bytes(raw)
                revised['input_artifacts'].append(dict(path='attachments/'+name,sha256=k.digest(raw)))
            self.assertEqual(revised['version'],'v1.r1')
            self.assertEqual(revised['review'],{'status':'pending'})
            self.assertTrue(any('前轮意见尚待处理' in i['message'] for i in revised['issues']))
            self.assertEqual(k.inspect(revised,base)['human'],'pending')
            with self.assertRaises(ValueError): k.build(*raws,previous=model)

    def test_optional_svg_and_fresh_output_preserves_earlier_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp)/'base';model,_=case(base);out=Path(tmp)/'delivery'
            k.package(model,base,out,with_svg=True)
            raw=(out/'goal-model.html').read_bytes()
            with self.assertRaises(ValueError): k.package(model,base,out)
            self.assertEqual((out/'goal-model.html').read_bytes(),raw)
            self.assertIn('<svg',(out/'goal-model.svg').read_text(encoding='utf-8'))

    def test_empty_goals_valid_and_unsupported_goal_cannot_get_supported_group(self):
        data,source,j,d=fixture();j['judgments']['G1']['label']='contradicted'
        d['input_binding']['judgments_sha256']=k.digest(k.encode(j))
        with self.assertRaises(ValueError): k.build(k.encode(data),k.encode(j),source,k.encode(d))
        data['candidates']=[];j=judgment_template(data,k.encode(data));d=k.decision_template(k.encode(data),k.encode(j))
        m=k.build(k.encode(data),k.encode(j),source,k.encode(d))
        self.assertIn('未提取到目标',k.markdown(m))

    def test_local_save_writes_real_file_without_overwrite_or_arbitrary_path(self):
        from serve_model import save_export
        with tempfile.TemporaryDirectory() as tmp:
            model,_=case(tmp);p=feedback(model)
            body=dict(kind='feedback',content=k.encode(p).decode(),path='../do-not-write')
            a=save_export(model,tmp,body);b=save_export(model,tmp,body)
            self.assertNotEqual(a['path'],b['path'])
            self.assertEqual(k.digest(Path(a['path']).read_bytes()),a['sha256'])
            self.assertEqual(Path(a['path']).parent,Path(tmp)/'exports')
            for kind,text in [('model-json','{}'),('model-md','wrong'),('bad','data')]:
                with self.assertRaises(ValueError):save_export(model,tmp,dict(kind=kind,content=text))

    def test_loopback_save_requires_origin_token_and_writes_receipt(self):
        import threading,urllib.request,urllib.error,re
        from serve_model import make_server
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp)/'base';model,_=case(base);out=Path(tmp)/'delivery';k.package(model,base,out)
            server=make_server(out)
            thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
            url='http://127.0.0.1:'+str(server.server_port)
            try:
                text=urllib.request.urlopen(url+'/goal-model.html',timeout=3).read().decode()
                config=json.loads(re.search(r'<script id="local-save-config" type="application/json">(.*?)</script>',text).group(1))
                payload=k.encode(dict(kind='feedback',content=k.encode(feedback(model)).decode()))
                bad=urllib.request.Request(url+'/__goalforge_save',data=payload,headers={'Content-Type':'application/json'},method='POST')
                with self.assertRaises(urllib.error.HTTPError):urllib.request.urlopen(bad,timeout=3)
                request=urllib.request.Request(url+'/__goalforge_save',data=payload,headers={'Content-Type':'application/json','Origin':url,'X-GoalForge-Token':config['token']},method='POST')
                receipt=json.loads(urllib.request.urlopen(request,timeout=3).read())
                self.assertTrue(Path(receipt['path']).is_file())
                self.assertEqual(k.load(receipt['path'])['status'],'submitted')
            finally:server.shutdown();server.server_close();thread.join(timeout=3)

    def test_explicit_feedback_disposition_kept_in_rebuilt_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            model,raws=case(tmp);p=feedback(model);d=json.loads(raws[3])
            d['feedback_dispositions']=[dict(target_type='goal',target_id='G3',status='addressed',reason='已依据原文重新判断；仍需用户审核。')]
            revised=k.build(*raws[:3],k.encode(d),previous=model,feedback=p)
            self.assertFalse(any('前轮意见尚待处理' in i['message'] for i in revised['issues']))
            self.assertEqual(revised['changes'][0]['feedback_dispositions'],d['feedback_dispositions'])

    def test_relationship_quotes_verified_and_not_replaced_with_goal_titles(self):
        data,source,j,d=fixture()
        m=k.build(k.encode(data),k.encode(j),source,k.encode(d))
        index={e['evidence_id']:e for e in m['evidence_index']}
        self.assertIn('任一种渠道',index[m['refinement_groups'][1]['evidence_ids'][0]]['quote'])
        d['groups'][1]['evidence_quotes'][0]['quote']='原文未说的关系'
        with self.assertRaises(ValueError):k.build(k.encode(data),k.encode(j),source,k.encode(d))

    def test_dag_layout_preserves_direction_goals_and_nonoverlapping_ranks(self):
        data,source,j,d=fixture();m=k.build(k.encode(data),k.encode(j),source,k.encode(d))
        diagram=k.dag_layout(m)
        self.assertEqual(sum(n['kind']=='goal' for n in diagram['nodes'].values()),5)
        self.assertEqual(sum(n['kind']=='group' for n in diagram['nodes'].values()),3)
        self.assertEqual(len(diagram['edges']),7)
        for e in diagram['edges']:
            a,b=(diagram['nodes'][e[k]] for k in ('start','end'))
            self.assertLess(a['rank'],b['rank'])
            self.assertLess(a['y']+a['height'],b['y'])
        nodes=list(diagram['nodes'].values())
        for i,a in enumerate(nodes):
            self.assertGreaterEqual(a['x'],0);self.assertLessEqual(a['x']+a['width'],diagram['width'])
            for b in nodes[i+1:]:
                if a['rank']==b['rank']:
                    self.assertTrue(a['x']+a['width']<=b['x'] or b['x']+b['width']<=a['x'])

    def test_dag_shared_goal_drawn_once_and_svg_contains_accessible_targets(self):
        import xml.etree.ElementTree as ET
        data,source,j,d=fixture();d['groups'].append(dict(d['groups'][0],group_id='F4',parent_id='G2',child_ids=['G4']))
        m=k.build(k.encode(data),k.encode(j),source,k.encode(d));diagram=k.dag_layout(m)
        self.assertEqual(len([n for n in diagram['nodes'].values() if n['id']=='G4']),1)
        root=ET.fromstring(k.svg(m));nodes=root.findall('{http://www.w3.org/2000/svg}g')
        self.assertEqual(len([n for n in nodes if n.get('data-goal')=='G4']),1)
        self.assertTrue(all(n.get('role')=='button' and n.get('aria-label') for n in nodes))


if __name__=='__main__':unittest.main()
