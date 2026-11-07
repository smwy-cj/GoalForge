import json,sys,hashlib
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
A=json.loads((OUT/'assignment.json').read_text(encoding='utf-8-sig'))
def read(p):
    p=ROOT/p
    b=p.read_bytes()
    logp=OUT/'consumed-files.json'
    log=json.loads(logp.read_text(encoding='utf-8')) if logp.exists() else {}
    log[str(p.relative_to(ROOT)).replace('\\','/')]={'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
    logp.write_text(json.dumps(log,ensure_ascii=False,indent=2),encoding='utf-8')
    return b.decode('utf-8-sig')
def obj(p):return json.loads(read(p))
mode,doc=sys.argv[1:3]
d=next(x for x in A['documents'] if x['document_id']==doc)
if mode=='source':
    lines=read(d['source_path']).splitlines()
    lo=int(sys.argv[3]) if len(sys.argv)>3 else 0
    hi=int(sys.argv[4]) if len(sys.argv)>4 else len(lines)
    print('\n'.join(lines[lo:hi]))
elif mode=='input':
    s=obj(d['source_input_path'])
    print(json.dumps({k:v for k,v in s.items() if k!='segments'},ensure_ascii=False))
    print('segments',len(s['segments']),'first',s['segments'][0]['source_id'],'last',s['segments'][-1]['source_id'])
elif mode in ('semantics','authors','extras'):
    m=obj(d['model_path']); base=Path(d['model_path']).parent
    lo=int(sys.argv[3]) if len(sys.argv)>3 else 0
    hi=int(sys.argv[4]) if len(sys.argv)>4 else 1000
    gs=[g for g in m['goals'] if g['goal_id'] in d['required_goal_ids']][lo:hi]
    if mode=='semantics':
        for g in gs:
            print(json.dumps({k:v for k,v in g.items() if k not in ('support','inference','origin')},ensure_ascii=False))
        for e in m['evidence_index']:
            if any(e['evidence_id'] in g['evidence_ids'] for g in gs):
                print(json.dumps({k:e[k] for k in ('evidence_id','source_id','quote','evidence_role')},ensure_ascii=False))
    elif mode=='authors':
        for g in gs:print(json.dumps({k:g[k] for k in ('goal_id','origin','inference','support')},ensure_ascii=False))
        for i in m.get('issues',[]):
            if i.get('target_id') in [g['goal_id'] for g in gs]:print(json.dumps(i,ensure_ascii=False))
    else:
        for fn in ('extraction.json','judgments.json','kaos-decisions.json'):
            o=obj(str(base/'attachments'/fn))
            print(fn,'keys',list(o))
            if fn=='extraction.json':
                for c in o.get('candidates',[]):
                    if c.get('candidate_id') in d['required_goal_ids']:
                        print(json.dumps({k:v for k,v in c.items() if k in ('candidate_id','context')},ensure_ascii=False))
                for k in ('review_questions','questions','issues'): 
                    if k in o:print(k,json.dumps(o[k],ensure_ascii=False))
            elif fn=='judgments.json':
                for k in ('review_questions','questions','issues'):
                    if k in o:print(k,json.dumps(o[k],ensure_ascii=False))
            else:print(json.dumps(o,ensure_ascii=False))
        mf=obj(str(base/'manifest.json')); print('manifest',json.dumps(mf,ensure_ascii=False))
        print('all_goal_statements',json.dumps([(g['goal_id'],g['statement']) for g in m['goals']],ensure_ascii=False))
        print('groups/issues',json.dumps(m.get('refinement_groups',[]),ensure_ascii=False),json.dumps([i for i in m.get('issues',[]) if i.get('target_type')=='group'],ensure_ascii=False))
