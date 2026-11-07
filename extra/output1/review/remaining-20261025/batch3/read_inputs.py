import json, sys, hashlib
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
assignment = json.loads((HERE/'assignment.json').read_text(encoding='utf-8'))
doc = next(x for x in assignment['documents'] if x['document_id'] == sys.argv[1])
mode = sys.argv[2]
def read(path):
    p=ROOT/path
    data=p.read_bytes()
    log=HERE/'consumed-files.json'
    items=json.loads(log.read_text(encoding='utf-8')) if log.exists() else []
    entry={'path':str(p),'sha256':hashlib.sha256(data).hexdigest()}
    if entry not in items:
        items.append(entry)
        log.write_text(json.dumps(items,ensure_ascii=False,indent=2),encoding='utf-8')
    return data.decode('utf-8-sig')
def js(path): return json.loads(read(path))
def show(x): print(json.dumps(x,ensure_ascii=False))
if mode == 'source':
    text=read(doc['source_path'])
    inp=js(doc['source_input_path'])
    start,end=int(sys.argv[3]),int(sys.argv[4])
    lines=text.splitlines()
    show({'document_id':doc['document_id'],'source_sha256_actual':hashlib.sha256((ROOT/doc['source_path']).read_bytes()).hexdigest(),'matches_assignment':hashlib.sha256((ROOT/doc['source_path']).read_bytes()).hexdigest()==doc['source_sha256'],'lines':len(lines),'segments':len(inp['segments']),'range_inclusive':[start,end],'source_metadata':{k:v for k,v in inp.items() if k!='segments'}})
    print('\n'.join(lines[start:end+1]))
elif mode in ('model','author'):
    model=js(doc['model_path']); base=Path(doc['model_path']).parent
    ext=js(str(base/'attachments/extraction.json'))
    jud=js(str(base/'attachments/judgments.json'))
    dec=js(str(base/'attachments/kaos-decisions.json'))
    manifest=js(str(base/'manifest.json'))
    ids=doc['required_goal_ids']
    if len(sys.argv)>3:
        ids=[doc['document_id']+'-'+x for x in sys.argv[3].split(',')]
    if mode == 'model':
        ev={x['evidence_id']:x for x in model['evidence_index']}
        show({'document_id':doc['document_id'],'actual_model_sha256':hashlib.sha256((ROOT/doc['model_path']).read_bytes()).hexdigest(),'hash_matches_assignment':hashlib.sha256((ROOT/doc['model_path']).read_bytes()).hexdigest()==doc['model_sha256'],'goals':[{k:v for k,v in x.items() if k not in ('origin','support')}|{'bound_evidence':[{k:v for k,v in ev[e].items() if k in ('evidence_id','source_id','quote','evidence_role')} for e in x['evidence_ids']]} for x in model['goals'] if x['goal_id'] in ids], 'other_goals_context':[{k:v for k,v in x.items() if k in ('goal_id','statement','conditions')} for x in model['goals'] if x['goal_id'] not in ids], 'questions':ext.get('review_questions'), 'issues':model.get('issues')})
    else:
        em={x['candidate_id']:x for x in ext['candidates']}
        ev={x['evidence_id']:x for x in model['evidence_index']}
        alignment=[]
        for g in model['goals']:
            if g['goal_id'] not in ids: continue
            e=em[g['goal_id']]
            fields={'statement':e.get('statement')==g['statement'],'actor':e.get('actor')==g['actor'],'context':e.get('context')==g['conditions'],'origin':e.get('origin')==g['origin'],'inference':e.get('inference')==g['inference']}
            quotes=[x for x in e['evidence_candidates'] if (x['source_id'],x['quote']) not in [(ev[y]['source_id'],ev[y]['quote']) for y in g['evidence_ids']]]
            j=jud['judgments'][g['goal_id']]
            jdiff={k:v for k,v in j.items() if k!='target_statement' and g['support'].get(k)!=v}
            alignment.append({'goal_id':g['goal_id'],'extraction_model_fields_equal':fields,'different_extraction_fields':{k:e.get(k if k!='context' else 'context') for k,v in fields.items() if not v},'extra_extraction_quotes':quotes,'judgment_statement_equal':j.get('target_statement')==g['statement'],'judgment_support_differences':jdiff})
        show({'document_id':doc['document_id'],'author_goals':[{k:v for k,v in x.items() if k in ('goal_id','origin','inference','support')} for x in model['goals'] if x['goal_id'] in ids], 'attachment_alignment':alignment, 'manifest':manifest,'group_context':model.get('refinement_groups'),'kaos_questions':dec.get('questions')})
