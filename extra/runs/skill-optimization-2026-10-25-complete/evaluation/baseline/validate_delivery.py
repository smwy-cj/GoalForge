"""Read only forward artifact verification; writes a fresh validation receipt."""
from pathlib import Path
import hashlib,json

base=Path(__file__).resolve().parent
execution=json.loads((base/'execution.json').read_text('utf-8'))
rows=[]
for doc in execution['scope']:
    d=base/doc
    data=json.loads((d/'extraction.json').read_text('utf-8'))
    text=(d/'source.txt').read_bytes().decode('utf-8')
    assert hashlib.sha256(text.encode()).hexdigest()==data['document_hash']
    segments={s['source_id']:s for s in data['segments']}
    for c in data['candidates']:
        for evidence in c['evidence_candidates']:
            assert text[evidence['start_char']:evidence['end_char']]==evidence['quote']
            assert evidence['quote'] in segments[evidence['source_id']]['text']
    manifest=json.loads((d/'delivery/manifest.json').read_text('utf-8'))
    for item in manifest['files']:
        assert hashlib.sha256((d/'delivery'/item['path']).read_bytes()).hexdigest()==item['sha256']
    inspection=json.loads((d/'inspection.json').read_text('utf-8'))
    assert inspection['structure']=='passed'
    assert inspection['independent_semantic']=='not_run'
    assert inspection['formal_proof']=='not_run'
    assert inspection['human']=='pending'
    model=json.loads((d/'delivery/goal-model.json').read_text('utf-8'))
    trace=json.loads((d/'tracing/tracing.json').read_text('utf-8'))
    assert len(model['goals'])==len(data['candidates'])==len(trace['traces'])
    assert all(t['support']['label'] in ['direct','inferred'] for t in trace['traces'])
    rows.append(dict(document_id=doc,turns_read=len(segments),goals=len(data['candidates']),direct=sum(t['support']['label']=='direct' for t in trace['traces']),inferred=sum(t['support']['label']=='inferred' for t in trace['traces']),refinement_proposals=len(model['refinement_groups']),supported_complete_groups=sum(g['status']=='supported' and g['completeness']=='complete' for g in model['refinement_groups']),structure=inspection['structure'],readiness=inspection['readiness'],manifest_files_verified=len(manifest['files'])))
receipt=dict(status='passed',documents=rows,total_goals=sum(r['goals'] for r in rows),failed_commands=len(execution['failures']),scope='Source hashes, every submitted quotation and segment reference, manifest byte hashes, candidate/trace/model counts and actual inspection states. No semantic accuracy or recall computation; no browser visual QA.',independent_semantic='not_run',formal_proof='not_run',human='pending')
with (base/'engineering-validation.json').open('x',encoding='utf-8',newline='\n') as f:
    json.dump(receipt,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps(receipt,ensure_ascii=False,indent=2))
