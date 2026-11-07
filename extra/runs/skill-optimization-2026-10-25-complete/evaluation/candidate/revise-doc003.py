"""Actual source-driven focused repair; never overwrites the first delivery."""
import pathlib,sys,copy,importlib.util
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from authoring import BASE,read,write,sha
s=importlib.util.spec_from_file_location('records',BASE/'build-records.py');r=importlib.util.module_from_spec(s);s.loader.exec_module(r)
r.COMMANDS=read(BASE/'pipeline-execution.json')
old=BASE/'DOC003';new=old/'revision-2';new.mkdir()
for name in ['source.txt','source-input.json','source-windows.json']:(new/name).write_bytes((old/name).read_bytes())
a=read(old/'final-author-spec.json');e=read(old/'extraction.json');keys=a['key_to_goal_id'];rows=a['rows']
extra=[(19,'visitcity','Visit different cities encountered during enjoyable travel when practical.','The respondent deliberately welcomes stops to visit different cities; this result was not fully represented by maximizing flight time.'),(123,'visitlounge','Visit different airport lounges during travel when access and opening times permit.','The respondent expressly likes visiting lounges in different countries; checking whether they are open is a means and must not replace the distinct visit intention.')]
for turn,key,statement,reason in extra:
 gid=f'G{len(e["candidates"])+1:03}';keys[key]=gid
 rows.append(dict(turn=turn,key=key,statement=statement,rationale=reason,origin='explicit'))
 evidence=[r.ev('DOC003',turn)]
 if key=='visitlounge':evidence.append(r.ev('DOC003',19))
 e['candidates'].append(dict(candidate_id=gid,statement=statement,origin='explicit',actor='Stakeholder',context=['Personal travel preference; logistical, visa, lounge-access and timing constraints remain situational.'],evidence_candidates=evidence,inference=None,review_status='pending'))
write(new/'extraction.json',e);write(new/'final-author-spec.json',a)
raw=read(old/'raw-candidates.json');windows=read(new/'source-windows.json')['windows']
for turn,key,statement,reason in extra:
 raw['candidates'].append(dict(candidate_id=f'C{len(raw["candidates"])+1:03}',statement=r.ev('DOC003',turn)['quote'],actor='Stakeholder',modality='personal preference; not universal default or mandatory visit',context=['Actual focused post-delivery recheck of T018-T020 and T122-T127; same generating assistant and shared context.'],origin='explicit',pass_id='P3',window_ids=[w['window_id'] for w in windows if f'DOC003:T{turn:03}' in w['source_ids']],evidence_candidates=[r.ev('DOC003',turn)]))
write(new/'raw-candidates.json',raw)
r.run(['skills/goal-extraction/scripts/check_coverage.py','template','--source-input',new/'source-input.json','--source',new/'source.txt','--windows',new/'source-windows.json','--candidates',new/'raw-candidates.json','--extraction',new/'extraction.json','--output',new/'extraction-ledger.json'])
template=read(new/'extraction-ledger.json');write(new/'extraction-ledger-template.json',template)
ledger=read(old/'extraction-ledger.json');ledger['input_binding']=template['input_binding']
affected={19,123};turngoals={}
for row,g in zip(rows,e['candidates']):turngoals.setdefault(row['turn'],[]).append(g['candidate_id'])
entrymap={x['candidate_id']:x for x in ledger['entries']}
for c in raw['candidates']:
 turn=int(c['evidence_candidates'][0]['source_id'].split('T')[-1])
 if turn in affected:
  ent=dict(candidate_id=c['candidate_id'],disposition='split',final_goal_ids=turngoals[turn],reason='Focused source recheck separates the desired visits from flight-time preference or lounge-opening checks; existing intended results and conditions remain represented.')
  entrymap[c['candidate_id']]=ent
ledger['entries']=list(entrymap.values())
for check in ledger['source_checks']:
 turn=int(check['evidence_candidates'][0]['source_id'].split('T')[-1])
 if turn in affected:
  check['final_goal_ids']=turngoals[turn]
  check['candidate_ids']=[c['candidate_id'] for c in raw['candidates'] if c['evidence_candidates'][0]['source_id']==f'DOC003:T{turn:03}']
  check['reason']='Actual focused reverse check found visit intentions distinct from checking information; mappings were semantically reassessed rather than only rebound.'
ledger['run']['planned_passes']=3
ledger['run']['stop_reason']='Source-driven focused review recovered two distinct visit intentions; original first attempt preserved. No statistical independence or exhaustion claim.'
ledger['run']['passes'].append(dict(pass_id='P3',kind='focused',context='shared',status='completed',window_results=[dict(window_id=w['window_id'],status='processed') if any(s in w['source_ids'] for s in ['DOC003:T018','DOC003:T019','DOC003:T020','DOC003:T122','DOC003:T123','DOC003:T124','DOC003:T125','DOC003:T126','DOC003:T127']) else dict(window_id=w['window_id'],status='skipped',reason='Outside the actual focused source recheck; initial and full-context passes already record the prior provided-material reading.') for w in windows]))
ledger['limitations'].append('This is a post-first-delivery repair, not the frozen first-attempt evaluation sample. P3 reread only T018-T020 and T122-T127; no new complete-document pass was claimed.')
write(new/'extraction-ledger.json',ledger)
r.run(['skills/goal-extraction/scripts/check_coverage.py','check','--source-input',new/'source-input.json','--source',new/'source.txt','--windows',new/'source-windows.json','--candidates',new/'raw-candidates.json','--extraction',new/'extraction.json','--ledger',new/'extraction-ledger.json','--output',new/'coverage-check.json'])
r.run(['skills/goal-extraction/scripts/trace_candidates.py',new/'extraction.json','--judgment-template',new/'judgments.json'])
j=read(new/'judgments.json');write(new/'judgments-template.json',j)
for row,g in zip(rows,e['candidates']):
 j['judgments'][g['candidate_id']].update(target_statement=g['statement'],label='inferred' if row['origin']=='inferred' else 'direct',rationale=row['rationale'],supported_parts=[g['statement']],unsupported_parts=[],assumptions=g['inference']['assumptions'] if g['inference'] else [],reasoning_steps=['Current final statement and its conditions checked against the provided source in context; new visit intentions individually checked during actual P3 targeted reading.'])
write(new/'judgments.json',j)
r.run(['skills/goal-extraction/scripts/trace_candidates.py',new/'extraction.json',new/'tracing','--source',new/'source.txt','--judgments',new/'judgments.json','--review-md'])
r.run(['skills/goal-model-building/scripts/kaos_model.py','template',new/'extraction.json',new/'judgments.json',new/'decisions.json'])
d=read(new/'decisions.json');write(new/'decisions-template.json',d);prev=read(old/'decisions.json')
for k in ['relations','groups','questions']:d[k]=prev[k]
for src,target,turn,reason in [('lounge','visitlounge',123,'Checking that a lounge is open helps make a desired lounge visit possible, but does not ensure access or a completed visit.'),('pass','visitlounge',123,'Maintained lounge access supports the desired visits; opening times and specific entitlement constraints still apply.')]:
 d['relations'].append(dict(relation_id=f'R{len(d["relations"])+1:03}',source_id=keys[src],target_id=keys[target],type='contribution',status='supported',conditions=['Subject to the actual airport, timing and valid entitlement.'],assumptions=[],rationale=reason,evidence_ids=[],evidence_quotes=[r.ev('DOC003',turn)]))
write(new/'decisions.json',d)
write(new/'revision-record.json',dict(source='source-driven generating-assistant self-check; no reference answers or other branch',first_attempt={'path':'../delivery/goal-model.json','sha256':sha(old/'delivery/goal-model.json')},changes=[{'new_goal_id':keys[key],'source_id':f'DOC003:T{turn:03}','reason':reason} for turn,key,statement,reason in extra],unchanged_goal_mapping={g['candidate_id']:g['candidate_id'] for g in read(old/'extraction.json')['candidates']},reassessment='Rechecked existing conditions and source support; new goals independently supported. Reviewed prior relations and all three partial groups; their insufficiency findings remain. New contribution relations cannot make a refinement sufficient.',formal_proof='not_run',independent_semantic='not_run',human='pending'))
(new/'author-semantic-review.md').write_text('# Focused generating-assistant self-check\n\nP3 actually reread T018-T020 and T122-T127. The first attempt had represented time in the air and lounge checks but missed the independently intended city and lounge visits. G050 and G051 now preserve these personal preferences, including practical constraints. Two contribution links connect lounge availability/access to a hoped-for visit. These helpful conditions are not sufficient refinement. Prior 49 statements and all existing relations/groups were checked for impact; no existing identifier changed. All three candidate refinement groups remain proposed/partial.\n\nThis is a source-driven repair after the frozen first attempt, not independent semantic review, human Gold, statistical replication or formal proof. It does not establish complete recall.\n',encoding='utf-8')
r.run(['skills/goal-model-building/scripts/kaos_model.py','assemble',new/'extraction.json',new/'judgments.json',new/'source.txt',new/'decisions.json',new/'assembled'])
r.run(['skills/goal-model-building/scripts/kaos_model.py','inspect',new/'assembled/model-input.json',new/'inspection.json'])
r.run(['skills/goal-model-building/scripts/kaos_model.py','finalize',new/'assembled/model-input.json',new/'inspection.json',new/'delivery','--svg'])
print('DOC003 revision-2',len(e['candidates']),len(d['relations']),len(d['groups']))
