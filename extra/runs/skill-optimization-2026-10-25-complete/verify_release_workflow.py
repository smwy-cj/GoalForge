"""Exercise all three installed skills against a synthetic, explicitly labelled case."""
import argparse
import copy
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];RUN=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tests'))
from test_kaos_relations import fixture
from test_kaos_model import k


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('release',type=Path);parser.add_argument('output',type=Path);args=parser.parse_args()
    out=k.fresh(args.output.resolve());commands=[]
    def cli(script,*argv):
        command=[sys.executable,'-X','utf8',str(script),*map(str,argv)];start=time.perf_counter()
        process=subprocess.run(command,cwd=out,capture_output=True,text=True,encoding='utf-8',timeout=60)
        commands.append(dict(command=command,exit_code=process.returncode,seconds=time.perf_counter()-start,stdout=process.stdout,stderr=process.stderr))
        (out/'commands.json').write_bytes(k.encode(commands))
        k.require(process.returncode==0,process.stderr)
        return process.stdout
    release=args.release.resolve();installed=out/'skills';releaser=ROOT/'scripts/release_skills.py'
    receipt=json.loads(cli(releaser,'install',release,installed));(out/'install-receipt.json').write_bytes(k.encode(receipt))
    extractor=installed/'goal-extraction/scripts';modeler=installed/'goal-model-building/scripts/kaos_model.py'
    data,source,j,decisions=fixture();(out/'synthetic.txt').write_bytes(source)
    cli(extractor/'prepare_source.py',out/'synthetic.txt',out/'source','--document-id','SYN-RELEASE','--window-size','4','--window-stride','2')
    prepared=k.load(out/'source/source-input.json');windows=k.load(out/'source/source-windows.json')
    def remap(e):
        item=copy.deepcopy(e)
        matches=[s for s in prepared['segments'] if s['original_locator']['start_char']<=e['start_char']<e['end_char']<=s['original_locator']['end_char']]
        k.require(len(matches)==1,'Synthetic evidence remapping failed');item['source_id']=matches[0]['source_id'];return item
    original_goals=data['candidates'];data=copy.deepcopy(prepared)
    data.update(schema_version='goalforge-extraction-3',status='completed',candidates=original_goals,review_questions=[],limitations=['合成工程验收资料与开发者判断，不是真实访谈或用户反馈。'])
    for g in data['candidates']:g['evidence_candidates']=[remap(e) for e in g['evidence_candidates']]
    for obj in decisions['groups']+decisions['relations']:obj['evidence_quotes']=[remap(e) for e in obj['evidence_quotes']]
    (out/'extraction.json').write_bytes(k.encode(data))
    common=['--source-input',out/'source/source-input.json','--source',out/'source/source.txt','--windows',out/'source/source-windows.json']
    cli(extractor/'check_coverage.py','capture-template',*common,'--output',out/'raw-candidates.json')
    capture=k.load(out/'raw-candidates.json')
    for i,g in enumerate(data['candidates'],1):
        sids={e['source_id'] for e in g['evidence_candidates']}
        capture['candidates'].append(dict(candidate_id='C'+str(i),statement=g['statement'],actor=g['actor'],modality='合成资料明确表达',context=g['context'],origin=g['origin'],
            pass_id='P1',window_ids=[w['window_id'] for w in windows['windows'] if sids.intersection(w['source_ids'])],evidence_candidates=g['evidence_candidates']))
    (out/'raw-candidates.json').write_bytes(k.encode(capture))
    common += ['--candidates',out/'raw-candidates.json','--extraction',out/'extraction.json']
    cli(extractor/'check_coverage.py','template',*common,'--output',out/'ledger.json')
    ledger=k.load(out/'ledger.json');ledger['run'].update(planned_passes=1,stop_reason='完成合成工程验收，未调用模型。')
    ledger['run']['passes'][0].update(kind='initial',context='shared',status='completed')
    for item in ledger['run']['passes'][0]['window_results']:item['status']='processed'
    ledger['full_context_review']=dict(status='completed',source_ids=[s['source_id'] for s in prepared['segments']],reason='核对合成原句、允许渠道及目标映射，非独立语义评审。')
    for item,g in zip(ledger['entries'],data['candidates']):item.update(disposition='keep',final_goal_ids=[g['candidate_id']],reason='合成验收中保留完整结果与依据。')
    (out/'ledger.json').write_bytes(k.encode(ledger))
    cli(extractor/'check_coverage.py','check',*common,'--ledger',out/'ledger.json','--output',out/'coverage.json')
    cli(extractor/'trace_candidates.py',out/'extraction.json','--judgment-template',out/'judgments.json')
    judgments=k.load(out/'judgments.json');judgments['judgments']=j['judgments'];(out/'judgments.json').write_bytes(k.encode(judgments))
    cli(extractor/'trace_candidates.py',out/'extraction.json',out/'tracing','--source',out/'source/source.txt','--judgments',out/'judgments.json')
    cli(modeler,'template',out/'extraction.json',out/'judgments.json',out/'decisions.json')
    current=k.load(out/'decisions.json');current['groups']=decisions['groups'];current['relations']=decisions['relations'];(out/'decisions.json').write_bytes(k.encode(current))
    cli(modeler,'assemble',out/'extraction.json',out/'judgments.json',out/'source/source.txt',out/'decisions.json',out/'assembled')
    cli(modeler,'inspect',out/'assembled/model-input.json',out/'inspection.json')
    cli(modeler,'finalize',out/'assembled/model-input.json',out/'inspection.json',out/'delivery','--svg')
    model=k.load(out/'delivery/goal-model.json')
    packet=dict(schema_version='goalforge-simple-feedback-2',model=k.binding(model),status='submitted',note='合成测试意见；不是真实用户反馈。',form_drafts={},
                entries=[dict(target_type='relation',target_id='R1',decision='modify',comment='合成测试：重评联系范围。')])
    (out/'synthetic-feedback.json').write_bytes(k.encode(packet))
    cli(modeler,'feedback',out/'delivery/goal-model.json',out/'synthetic-feedback.json',out/'feedback-output')
    request=k.load(out/'feedback-output/revision-request.json');k.require(request['affected_relation_ids']==['R1'] and request['affected_group_ids']==['F1'],'Dependency propagation differs')
    revised=copy.deepcopy(current);revised['reassessments']=[dict(assessment_id='A1',target_type='relation',target_id='R1',reason='合成工程重评，仍只认定部分贡献。'),dict(assessment_id='A2',target_type='group',target_id='F1',reason='重新核对原句及正常异常场景。')]
    revised['feedback_dispositions']=[dict(target_type='relation',target_id='R1',status='addressed',reason='合成重评完成，结果仍待真实用户审核。')]
    (out/'revised-decisions.json').write_bytes(k.encode(revised))
    cli(modeler,'assemble',out/'extraction.json',out/'judgments.json',out/'source/source.txt',out/'revised-decisions.json',out/'revised','--previous',out/'delivery/goal-model.json','--feedback',out/'feedback-output/review-feedback.json')
    cli(modeler,'inspect',out/'revised/model-input.json',out/'revised-inspection.json')
    cli(modeler,'finalize',out/'revised/model-input.json',out/'revised-inspection.json',out/'revised-delivery','--svg')
    final=k.load(out/'revised-delivery/goal-model.json');k.require(final['review']=={'status':'pending'} and final['parent']==k.binding(model),'Revision state differs')
    result=dict(status='passed',commands=len(commands),installed_paths=receipt['loaded'],coverage=k.load(out/'coverage.json')['workflow'],
                schema=model['schema_version'],relation_ids=request['affected_relation_ids'],group_ids=request['affected_group_ids'],
                revised_version=final['version'],human='pending',application_discovery='not_asserted',scope='Synthetic engineer-authored workflow only; no real feedback or accuracy claim.')
    (out/'verification.json').write_bytes(k.encode(result));print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':main()
