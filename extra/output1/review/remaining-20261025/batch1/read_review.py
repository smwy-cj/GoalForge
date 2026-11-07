import json, sys, hashlib
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[3]
BASE=Path(__file__).resolve().parent
A=json.loads((BASE/'assignment.json').read_text(encoding='utf-8'))
def read(p):
    return json.loads(p.read_text(encoding='utf-8'))
d=next(x for x in A['documents'] if x['document_id']==sys.argv[1])
mp=ROOT/d['model_path']; dp=mp.parent
mode=sys.argv[2]
if mode=='baseline':
    s=(ROOT/d['source_path']).read_text(encoding='utf-8')
    si=read(ROOT/d['source_input_path'])
    sh=hashlib.sha256((ROOT/d['source_path']).read_bytes()).hexdigest()
    assert sh==d['source_sha256']
    assert len(si['segments'])==d['source_turns']
    for seg in si['segments']:
        assert seg['text'] in s
    with (BASE/'source-baseline.md').open('a',encoding='utf-8') as f:
        f.write(f"\n- {d['document_id']}: source.txt 已完整实际读取 T000–T{d['source_turns']-1:03d}；{len(s)}字符；SHA256 {sh} 与 assignment 一致。source-input 的 document_hash、全部 {len(si['segments'])} 个source_id/轮次及文本映射已程序交叉核验；下步审模型。\n")
    print(d['document_id'],len(s),len(si['segments']),sh)
elif mode=='core':
    m=read(mp)
    print(json.dumps([{k:g[k] for k in ('goal_id','statement','actor','conditions')} for g in m['goals']],ensure_ascii=False))
    print('ISSUES',json.dumps(m['issues'],ensure_ascii=False))
elif mode=='author':
    m=read(mp); e=read(dp/'attachments/extraction.json'); j=read(dp/'attachments/judgments.json'); k=read(dp/'attachments/kaos-decisions.json'); man=read(dp/'manifest.json')
    for g in m['goals']:
        if g['goal_id'] not in d['required_goal_ids']: continue
        print(json.dumps(g,ensure_ascii=False))
        print('BOUND',json.dumps([{k:x[k] for k in ['evidence_id','source_id','quote','evidence_role']} for x in m['evidence_index'] if x['evidence_id'] in g['evidence_ids']],ensure_ascii=False))
    print('EXTRACTION',json.dumps([{k:v for k,v in x.items() if k not in ['statement','actor','origin','inference','evidence_candidates']} for x in e['candidates'] if x['candidate_id'] in d['required_goal_ids']],ensure_ascii=False))
    print('QUESTIONS',json.dumps(e['review_questions'],ensure_ascii=False))
    jj={gid:x for gid,x in j['judgments'].items() if gid in d['required_goal_ids']}
    print('JUDGMENTS',json.dumps(jj,ensure_ascii=False))
    print('KAOS-NECESSARY',json.dumps({k:v for k,v in k.items() if k in ['schema_version','input_binding','questions','issues','limitations']},ensure_ascii=False))
    print('MANIFEST',json.dumps(man,ensure_ascii=False))
