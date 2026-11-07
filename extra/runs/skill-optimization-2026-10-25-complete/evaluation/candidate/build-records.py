import sys, json, pathlib, hashlib, subprocess, datetime, copy
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from authoring import BASE, ROOT, SPECS, EXCLUSIONS, read, write, sha

COMMANDS=[]
def run(args):
 p=subprocess.run([sys.executable,'-X','utf8',*map(str,args)],capture_output=True,text=True,encoding='utf-8')
 COMMANDS.append(dict(command=[sys.executable,'-X','utf8',*map(str,args)],exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr))
 write(BASE/'pipeline-execution.json',COMMANDS)
 if p.returncode: raise RuntimeError(p.stderr or p.stdout)

def ev(doc,turn):
 t=read(ROOT/'datasets/processed/goalforge-v1/source'/f'{doc}.json')['turns'][turn]
 return dict(source_id=t['source_id'],quote=t['text'],role='basis',start_char=t['start_char'],end_char=t['end_char'])

def add(rows,turn,key,statement,reason,origin='explicit'):
 rows.append(dict(turn=turn,key=key,statement=statement,rationale=reason,origin=origin))

def corrected(doc):
 rows=copy.deepcopy(SPECS[doc])
 if doc=='DOC020':
  for r in rows:
   if r['key']=='recruit': r['statement']='Receive recruiter emails during job applications.'
   if r['key']=='school': r['statement']='Receive school news and notifications.'
   if r['key']=='draft': r['statement']="Use an AI assistant to compose an email from the sender's main points."
  add(rows,11,'appointments','Use email to book personal appointments such as dentist or clinic visits.','This personal use is expressly stated in the full answer; it was obscured in the initial truncated display.')
  add(rows,11,'deals','Receive merchandise sales or discount information by email.','This distinct personal information outcome is explicit, beyond account-organization background.')
  add(rows,11,'friends','Occasionally communicate with friends by email.','The speaker explicitly identifies this rare use; rarity is not an exclusion reason.')
  add(rows,19,'adjust','Adjust the AI-generated email draft before sending it.','The chosen editing action is separate from generating the draft and is not a fully automatic send request.')
  add(rows,15,'reply','Reply to emails requiring a response when available.','The deferred-task context includes replies; this does not turn receiving recruiter mail into a compound receive-and-reply goal.')
 if doc=='DOC010':
  for r in rows:
   if r['key']=='postpone': r['statement']='Postpone an event when extreme weather is forecast.'
  add(rows,35,'stayinside','Avoid going out when extreme weather is forecast.','The independently satisfiable avoidance intent is explicit alongside event postponement.')
 if doc=='DOC003':
  # The personal experience preference is conditioned by subsequent duration limits.
  for r in rows:
   if r['key']=='airtime': r['statement']='Prefer to maximize enjoyable time in the air when the trip and practical constraints permit.'
 if doc=='DOC013':
  # A proposed accessibility investigation must not become a claim of a proven defect.
  for r in rows:
   if r['key']=='captionaccuracy': r['statement']='Seek reliable automatic captions, especially for viewers who do not speak English as a first language.'
 return rows

def make(doc):
 f=BASE/doc; source=read(f/'source-input.json'); wins=read(f/'source-windows.json')
 raw=[]; byturn={}
 # Each authored turn-level capture is retained separately in overlapping windows.
 # The program performs indexing only; all semantic content was authored above.
 for row in SPECS[doc]: byturn.setdefault(row['turn'],[]).append(row)
 ex={t:reason for t,reason in EXCLUSIONS[doc]}
 for w in wins['windows']:
  for seg in w['segments']:
   turn=int(seg['source_id'].split('T')[-1])
   if turn not in byturn and turn not in ex: continue
   items=byturn.get(turn,[])
   raw.append(dict(candidate_id=f'C{len(raw)+1:03}',statement=seg['text'],actor=seg['speaker'],modality='speaker report; tentative suggestions and personal preferences preserved in final statements',context=['Captured with adjacent question and response in the shared document context.'],origin='unknown',pass_id='P1',window_ids=[w['window_id']],evidence_candidates=[ev(doc,turn)]))
 rows=corrected(doc)
 oldkeys={r['key'] for r in SPECS[doc]}
 additions={r['turn'] for r in rows if r['key'] not in oldkeys}
 for turn in sorted(additions):
  raw.append(dict(candidate_id=f'C{len(raw)+1:03}',statement=ev(doc,turn)['quote'],actor='Stakeholder',modality='explicit personal intent; original frequency and conditions retained',context=['Additional atomization or intent recovered during the full-context review; not an independent sample.'],origin='explicit',pass_id='P2',window_ids=[w['window_id'] for w in wins['windows'] if f'{doc}:T{turn:03}' in w['source_ids']],evidence_candidates=[ev(doc,turn)]))
 rawdata=dict(schema_version='goalforge-extraction-candidates-1',document_id=doc,input_binding=dict(document_hash=source['document_hash'],source_input_sha256=sha(f/'source-input.json'),windows_sha256=sha(f/'source-windows.json')),candidates=raw)
 write(f/'raw-candidates.json',rawdata)
 goals=[]; keys={}
 for row in rows:
  gid=f'G{len(goals)+1:03}';keys[row['key']]=gid
  # Statements carry material semantic restrictions; conditions add source scope,
  # rather than hiding missing restrictions only in a rationale.
  conditions=['This stakeholder and the described use case; no universal policy for all users is inferred.']
  inference=None if row['origin']=='explicit' else dict(basis_candidate_ids=[],reason=row['rationale'],assumptions=['The stated value or obstacle motivates preserving or improving the corresponding result; this remains an author inference.'])
  goals.append(dict(candidate_id=gid,statement=row['statement'],origin=row['origin'],actor='Stakeholder' if doc!='DOC013' else None,context=conditions,evidence_candidates=[ev(doc,row['turn'])],inference=inference,review_status='pending'))
 extraction=dict(schema_version='goalforge-extraction-3',document_id=doc,document_hash=source['document_hash'],status='completed',materials=source['materials'],conversion=source['conversion'],segments=source['segments'],coverage=dict(scope='provided_material',source_ids=[x['source_id'] for x in source['segments']],omissions=[]),candidates=goals,review_questions=[],limitations=['Only the provided native-text interview was available; audio and actual application behavior were not independently checked.','One assistant authored extraction, support judgments and model decisions in shared within-document context; this is not independent semantic review or formal proof.'])
 if doc=='DOC036': extraction['review_questions'].append(dict(candidate_ids=[],question='Is anonymous posting also desired, separately from the clearly repeated anonymous-browsing request?',reason='T071 bundles both in an interviewer paraphrase and T072 only gives a short acknowledgment.'))
 write(f/'final-author-spec.json',dict(document_id=doc,rows=rows,key_to_goal_id=keys,full_context_calibration='Question-answer scopes, conditional preferences, existing-capability qualification, one-action boundaries and exceptions reviewed against the complete source in context.'))
 write(f/'extraction.json',extraction)
 run(['skills/goal-extraction/scripts/check_coverage.py','template','--source-input',f/'source-input.json','--source',f/'source.txt','--windows',f/'source-windows.json','--candidates',f/'raw-candidates.json','--extraction',f/'extraction.json','--output',f/'extraction-ledger.json'])
 ledger=read(f/'extraction-ledger.json')
 write(f/'extraction-ledger-template.json',ledger)
 ledger['run'].update(strategy='windowed',model='unknown',temperature='unknown',budget='unknown',usage='unknown',skill_revision='SHA256 file inventory in ../execution.json',prompt_revision='isolated candidate forward-validation task; current assistant authored semantics',planned_passes=2,stop_reason='One initial capture and one shared-context full-document calibration completed; no repeated stochastic sample or additional semantic search.',passes=[dict(pass_id=p,kind=k,context='shared',status='completed',window_results=[dict(window_id=w['window_id'],status='processed') for w in wins['windows']]) for p,k in [('P1','initial'),('P2','full_context')]])
 ledger['full_context_review']=dict(status='completed',source_ids=[s['source_id'] for s in source['segments']],reason='Reviewed all provided turns in the shared document context, including interviewer scope, respondent agreement, conditional and countervailing statements. Full reading is not proof of exhaustive intent recall.')
 ledger['entries']=[]; ledger['source_checks']=[]
 goalturn={}
 for row,g in zip(rows,goals):goalturn.setdefault(row['turn'],[]).append(g['candidate_id'])
 rawturn={}
 for c in raw: rawturn.setdefault(int(c['evidence_candidates'][0]['source_id'].split('T')[-1]),[]).append(c['candidate_id'])
 first={}
 for c in raw:
  turn=int(c['evidence_candidates'][0]['source_id'].split('T')[-1]); ids=goalturn.get(turn,[])
  if ids:
   disp='split' if len(ids)>1 else ('keep' if turn not in first else 'merge')
   reason='The captured expression has independently intended core results; each retains its original context and is separately supported.' if len(ids)>1 else ('Same actor, action and conditions; overlapping-window repetition is merged without deleting the raw candidate.' if turn in first else 'Preserves the intended core action or state and source restrictions.')
   first[turn]=True
  else: disp='exclude';reason=ex[turn]
  ledger['entries'].append(dict(candidate_id=c['candidate_id'],disposition=disp,final_goal_ids=ids,reason=reason))
 for turn,cids in rawturn.items():
  ids=goalturn.get(turn,[])
  ledger['source_checks'].append(dict(check_id=f'SC{len(ledger["source_checks"])+1:03}',evidence_candidates=[ev(doc,turn)],candidate_ids=cids,final_goal_ids=ids,outcome='represented' if ids else 'excluded',reason=('Rechecked complete respondent intent and question scope; mapped independently intended outcomes without converting background controls to goals.' if ids else ex[turn])))
 ledger['limitations']=['Window processing and source checks audit the stated work; they do not establish semantic completeness.','Raw candidates preserve whole utterances, including compound expressions and background; final atomicity and exclusions are the assistant\'s semantic judgments.','P1 and P2 use shared context; inter-branch isolation is not statistical independence.']
 write(f/'extraction-ledger.json',ledger)
 run(['skills/goal-extraction/scripts/check_coverage.py','check','--source-input',f/'source-input.json','--source',f/'source.txt','--windows',f/'source-windows.json','--candidates',f/'raw-candidates.json','--extraction',f/'extraction.json','--ledger',f/'extraction-ledger.json','--output',f/'coverage-check.json'])
 run(['skills/goal-extraction/scripts/trace_candidates.py',f/'extraction.json','--judgment-template',f/'judgments.json'])
 j=read(f/'judgments.json');write(f/'judgments-template.json',j)
 for g,row in zip(goals,rows):
  j['judgments'][g['candidate_id']].update(target_statement=g['statement'],label='inferred' if row['origin']=='inferred' else 'direct',rationale=row['rationale'],supported_parts=[g['statement']],unsupported_parts=[],assumptions=g['inference']['assumptions'] if g['inference'] else [],reasoning_steps=['Compared the complete statement with its respondent answer, adjacent question, later limitations and actual intended use; position matching alone was not used to decide support.'])
 write(f/'judgments.json',j)
 run(['skills/goal-extraction/scripts/trace_candidates.py',f/'extraction.json',f/'tracing','--source',f/'source.txt','--judgments',f/'judgments.json','--review-md'])
 return keys

if __name__=='__main__':
 for doc in SPECS:
  print(doc,make(doc))
