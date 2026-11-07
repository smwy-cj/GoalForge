"""Freeze de-labelled review packets after the source-first inventory is frozen."""
import argparse
import hashlib
import json
from pathlib import Path

RUN=Path(__file__).resolve().parent
DOCS=('DOC003','DOC010','DOC013','DOC020','DOC023','DOC031','DOC028','DOC036')


def sha(raw):return hashlib.sha256(raw).hexdigest()
def encode(data):return (json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode('utf-8')


def discover(branch):
    models={}
    for path in (RUN/'evaluation'/branch).rglob('goal-model.json'):
        if 'attachments' in path.parts or 'exports' in path.parts:continue
        data=json.loads(path.read_bytes());doc=data['scope']['document_id']
        if doc not in DOCS:continue
        if doc in models:raise ValueError('Multiple delivered versions; explicit selection required: '+branch+' '+doc)
        models[doc]=(path,data)
    if set(models)!=set(DOCS):raise ValueError('Missing documents: '+branch+' '+str(set(DOCS)-set(models)))
    return models


def anonymize(model):
    goal_ids={g['goal_id']:'G'+str(i+1).zfill(3) for i,g in enumerate(model['goals'])}
    group_ids={g['group_id']:'F'+str(i+1).zfill(3) for i,g in enumerate(model['refinement_groups'])}
    relation_ids={r['relation_id']:'R'+str(i+1).zfill(3) for i,r in enumerate(model.get('relations',[]))}
    evidence={e['evidence_id']:dict(source_id=e['source_id'],quote=e['quote'],start_char=e['start_char'],end_char=e['end_char'],role=e['evidence_role']) for e in model['evidence_index']}
    def refs(ids):return [evidence[e] for e in ids]
    def inference(value):
        if value is None:return None
        result=dict(value);result['basis_candidate_ids']=[goal_ids.get(g,g) for g in value['basis_candidate_ids']];return result
    goals=[dict(id=goal_ids[g['goal_id']],statement=g['statement'],actor=g['actor'],conditions=g['conditions'],origin=g['origin'],
                inference=inference(g['inference']),support=g['support'],evidence=refs(g['evidence_ids'])) for g in model['goals']]
    groups=[]
    for g in model['refinement_groups']:
        checks=[]
        for c in g.get('checks',[]):
            item={key:value for key,value in c.items() if key!='evidence_ids'}
            item['evidence']=refs(c.get('evidence_ids',[]));checks.append(item)
        groups.append(dict(id=group_ids[g['group_id']],parent=goal_ids[g['parent_id']],children=[goal_ids[c] for c in g['child_ids']],
                           status=g['status'],completeness=g['completeness'],rationale=g['rationale'],assumptions=g['assumptions'],
                           evidence=refs(g['evidence_ids']),checks=checks,relation_ids=[relation_ids[r] for r in g.get('relation_ids',[])]))
    relations=[dict(id=relation_ids[r['relation_id']],source=goal_ids[r['source_id']],target=goal_ids[r['target_id']],type=r['type'],
                    status=r['status'],conditions=r['conditions'],assumptions=r['assumptions'],rationale=r['rationale'],evidence=refs(r['evidence_ids'])) for r in model.get('relations',[])]
    return dict(document_id=model['scope']['document_id'],goals=goals,groups=groups,relations=relations),dict(goals=goal_ids,groups=group_ids,relations=relation_ids)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('round',choices=('first','repeat'));args=parser.parse_args()
    review=RUN/'evaluation/source-first-review/freeze-manifest.json'
    if not review.exists():raise ValueError('Freeze source-first review before preparing packets')
    arms=['baseline','candidate'] if args.round=='first' else ['baseline-repeat','candidate-repeat']
    loaded={arm:discover(arm) for arm in arms}
    destination=RUN/'evaluation/anonymous'/args.round
    if destination.exists():raise ValueError('Do not overwrite review packets')
    records=[]
    for doc in DOCS:
        ordered=sorted(arms,key=lambda arm:sha((args.round+doc+arm+'goalforge-review').encode()))
        for label,arm in zip(('A','B'),ordered):
            path,model=loaded[arm][doc];packet,mapping=anonymize(model)
            target=destination/doc/(label+'.json');target.parent.mkdir(parents=True,exist_ok=True);raw=encode(packet);target.write_bytes(raw)
            records.append(dict(document_id=doc,label=label,branch=arm,source_model=str(path.relative_to(RUN)),source_sha256=sha(path.read_bytes()),
                                anonymous=str(target.relative_to(RUN)),anonymous_sha256=sha(raw),id_mapping=mapping))
    record=dict(round=args.round,inventory_manifest_sha256=sha(review.read_bytes()),records=records,
                blinding='branch labels and original object IDs removed; structural method clues can remain')
    (RUN/'evaluation'/('blinding-map-'+args.round+'.json')).write_bytes(encode(record))
    print(json.dumps(dict(round=args.round,packets=len(records),destination=str(destination)),ensure_ascii=False))


if __name__=='__main__':main()
