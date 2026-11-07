"""Record actual artifact revisions and failed attempts without changing models."""
import hashlib
import json
from pathlib import Path

OUT=Path(__file__).resolve().parents[1]


def load(p):
    return json.loads(p.read_bytes().decode('utf-8-sig'))


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    entries=[]
    for record in load(OUT/'_run/delivery-index.json')['documents']:
        if record['arm']!='revised' or not record['other_deliveries']:
            continue
        latest=OUT/record['json']; after=load(latest)
        for relative in record['other_deliveries']:
            previous=OUT/relative; before=load(previous)
            old_goals={g['goal_id']:g for g in before['goals']}; new_goals={g['goal_id']:g for g in after['goals']}
            old_groups={g['group_id']:g for g in before['refinement_groups']}; new_groups={g['group_id']:g for g in after['refinement_groups']}
            goal_changes=[]
            for identifier in sorted(set(old_goals)|set(new_goals)):
                a,b=old_goals.get(identifier),new_goals.get(identifier)
                if a!=b:
                    fields=sorted(k for k in set(a or {})|set(b or {}) if (a or {}).get(k)!=(b or {}).get(k))
                    goal_changes.append(dict(goal_id=identifier,changed_fields=fields))
            changed_groups=[g for g in sorted(set(old_groups)|set(new_groups)) if old_groups.get(g)!=new_groups.get(g)]
            notes=[]
            for p in [latest.parent.parent/'revision-notes.md',OUT/'revised/_authoring'/(record['document_id']+'-v2-revision-note.md')]:
                if p.exists(): notes.append(p.relative_to(OUT).as_posix())
            entries.append(dict(document_id=record['document_id'],before=relative,after=record['json'],
                                before_sha256=sha(previous),after_sha256=sha(latest),
                                before_internal_version=before['version'],after_internal_version=after['version'],
                                parent_in_after=after['parent'],source_unchanged=sha(previous.parent/'attachments/source.txt')==sha(latest.parent/'attachments/source.txt'),
                                changed_goals=goal_changes,changed_group_ids=changed_groups,revision_notes=notes,
                                human_acceptance=after['review']['status']))
    failures=[]
    for p in sorted((OUT/'revised').rglob('*')):
        if p.is_file() and ('failure' in p.name or '.failed.' in p.name):
            failures.append(dict(path=p.relative_to(OUT).as_posix(),sha256=sha(p),bytes=p.stat().st_size))
    result=dict(complete_delivery_revisions=entries,failed_attempt_records=failures,
                note='Paths and actual SHA-256 distinguish outer artifact revisions. The frozen model tool may keep internal version=v1 and parent=null for assistant revisions; no human feedback or acceptance is fabricated. Exact field differences are not automatic semantic verdicts.')
    (OUT/'_run/revision-ledger.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(delivery_revision_pairs=len(entries),failure_records=len(failures))))


if __name__=='__main__':main()
