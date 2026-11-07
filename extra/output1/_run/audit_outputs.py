"""Reinspect selected deliveries and independently verify frozen bytes."""
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

OUT=Path(__file__).resolve().parents[1]
ROOT=OUT.parent


def load(p):
    return json.loads(p.read_bytes().decode('utf-8-sig'))


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    inventory=load(OUT/'_run/source-inventory.json')
    errors=[]; source_results=[]; skill_results=[]; deliveries=[]
    for item in inventory:
        doc=item['document_id']; original=ROOT/'datasets/processed/goalforge-v1/source'/doc
        okay=(sha(original.with_suffix('.json'))==item['json_sha256'] and
              sha(original.with_suffix('.txt'))==item['text_sha256'] and
              sha(OUT/'_inputs'/doc/'source.txt')==item['text_sha256'] and
              sha(OUT/'_inputs'/doc/'source-original.json')==item['json_sha256'])
        original_data=load(OUT/'_inputs'/doc/'source-original.json')
        prepared=load(OUT/'_inputs'/doc/'source-input.json')
        expected_turns=[(t['source_id'],t['text'],t['speaker'],t['start_char'],t['end_char']) for t in original_data['turns']]
        prepared_turns=[(s['source_id'],s['text'],s['speaker'],s['original_locator']['start_char'],s['original_locator']['end_char']) for s in prepared['segments']]
        okay=okay and expected_turns==prepared_turns and prepared['document_hash']==item['text_sha256']
        source_results.append(dict(document_id=doc,unchanged=okay))
        if not okay: errors.append('Source changed: '+doc)
    for arm in ('baseline','revised'):
        base=OUT/'_run/skill-snapshots'/arm
        for f in load(base/'manifest.json')['files']:
            actual=sha(base/'skills'/f['path'])
            if actual!=f['sha256']: errors.append('Frozen skill changed: '+arm+'/'+f['path'])
        skill_results.append(dict(arm=arm,verified_files=len(load(base/'manifest.json')['files'])))
    pilot_freeze=OUT/'_run/pilot-freeze.json'
    frozen_pilot_files=0
    if pilot_freeze.exists():
        for packet in load(pilot_freeze):
            for f in packet['files']:
                target=OUT/packet['root']/f['path']
                frozen_pilot_files+=1
                if not target.is_file() or sha(target)!=f['sha256']:
                    errors.append('Frozen pilot v1 changed: '+str(target))
    revised_manifest=load(OUT/'_run/skill-snapshots/revised/manifest.json')
    for f in revised_manifest['files']:
        target=ROOT/'skills'/f['path']
        if not target.is_file() or sha(target)!=f['sha256']:
            errors.append('Authoritative project skill changed during run: '+str(target))
    audit_dir=OUT/'_run/audit-inspections'; audit_dir.mkdir(exist_ok=True)
    for entry in load(OUT/'_run/delivery-index.json')['documents']:
        path=OUT/entry['json']; base=path.parent; model=load(path)
        expected=next(i['text_sha256'] for i in inventory if i['document_id']==entry['document_id'])
        if sha(base/'attachments/source.txt')!=expected:
            errors.append('Delivery uses unexpected source: '+entry['json'])
        for f in load(base/'manifest.json')['files']:
            target=(base/f['path']).resolve()
            if base.resolve() not in target.parents or sha(target)!=f['sha256']:
                errors.append('Manifest mismatch: '+str(target))
        suffix=sha(path)[:12]
        report_path=audit_dir/(entry['arm']+'-'+entry['document_id']+'-'+suffix+'.json')
        tool=OUT/'_run/skill-snapshots'/entry['arm']/'skills/goal-model-building/scripts/kaos_model.py'
        if not report_path.exists():
            result=subprocess.run([sys.executable,'-X','utf8',str(tool),'inspect',str(path),str(report_path)],
                                  capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=60,
                                  env=dict(os.environ,PYTHONIOENCODING='utf-8'))
            if result.returncode:
                errors.append('Inspect failed: '+entry['json']+' '+result.stderr)
                continue
        report=load(report_path)
        deliveries.append(dict(document_id=entry['document_id'],arm=entry['arm'],delivery=entry['json'],
                               model_sha256=sha(path),structure=report['structure'],readiness=report['readiness'],
                               goals=len(model['goals']),groups=len(model['refinement_groups']),
                               source='verified',manifest='verified',report=report_path.relative_to(OUT).as_posix()))
    output=dict(checked_at_utc=datetime.now(timezone.utc).isoformat(),status='passed' if not errors else 'failed',
                sources=source_results,skill_snapshots=skill_results,frozen_pilot_files_verified=frozen_pilot_files,
                authoritative_skills_unchanged=not any('Authoritative project skill changed' in x for x in errors),
                deliveries=deliveries,errors=errors,
                semantic_claim='Engineering and byte-integrity checks only; see separate source-based model review.')
    (OUT/'_run/final-verification.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status=output['status'],sources=len(source_results),deliveries=len(deliveries),errors=errors),ensure_ascii=False))
    if errors:sys.exit(1)


if __name__=='__main__':main()
