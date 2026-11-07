"""Compare v1/v2 assembly on identical frozen goals, not new LLM generations."""
import copy
import json
import sys
import time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];RUN=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'skills/goal-model-building/scripts'))
import kaos_model as k


def main():
    selections=json.loads((RUN/'evaluation/blinding-map-first.json').read_bytes())
    rows=[]
    for selected in selections['records']:
        if selected['branch']!='candidate':continue
        path=RUN/selected['source_model'];raw=path.read_bytes()
        k.require(k.digest(raw)==selected['source_sha256'],'Initial candidate changed after freezing')
        original=json.loads(raw);proof=k.read_artifacts(original,path.parent)
        data=proof['attachments/extraction.json'];judgments=proof['attachments/judgments.json'];source=proof['attachments/source.txt']
        actual=k.inspect(original,path.parent)
        d2=json.loads(proof['attachments/kaos-decisions.json'])
        d1=k.decision_template(data,judgments,1)
        d1['groups']=[{key:copy.deepcopy(value) for key,value in g.items() if key not in {'relation_ids','checks'}} for g in d2['groups']]
        d1['questions']=[copy.deepcopy(q) for q in d2.get('questions',[]) if q['target_type']!='relation']
        outputs={}
        for label,decisions in [('groups-only-v1',d1),('typed-relations-v2',d2)]:
            hashes=[];durations=[]
            for repeat in range(3):
                start=time.perf_counter();model=k.build(data,judgments,source,k.encode(decisions));durations.append(time.perf_counter()-start);hashes.append(k.object_hash(model))
            k.require(len(set(hashes))==1,'Deterministic rebuild differs')
            base=k.fresh(RUN/'fixed-goal-modeling'/selected['document_id']/label/'assembled')
            for name,content in [('extraction.json',data),('judgments.json',judgments),('source.txt',source),('kaos-decisions.json',k.encode(decisions))]:
                target=base/'attachments'/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(content)
                model['input_artifacts'].append(dict(path='attachments/'+name,sha256=k.digest(content)))
            (base/'model-input.json').write_bytes(k.encode(model));report=k.inspect(model,base)
            k.package(model,base,base.parent/'delivery',report,with_svg=True)
            outputs[label]=dict(model=model,rebuild_hashes=hashes,rebuild_seconds=durations)
        a,b=outputs['groups-only-v1'],outputs['typed-relations-v2']
        k.require(a['model']['goals']==b['model']['goals'],'Goal set differs across model contracts')
        rows.append(dict(document_id=selected['document_id'],goal_count=len(original['goals']),goals_byte_semantics_identical=True,
                         goal_state_sha256=k.object_hash(original['goals']),source_sha256=k.digest(source),
                         v1_groups=len(a['model']['refinement_groups']),v2_groups=len(b['model']['refinement_groups']),
                         v1_active=sum(k.active(g) for g in a['model']['refinement_groups']),v2_active=sum(k.active(g) for g in b['model']['refinement_groups']),
                         v2_relations=len(b['model']['relations']),deterministic_rebuilds_each=3,
                         deterministic_hashes={name:value['rebuild_hashes'] for name,value in outputs.items()}))
    result=dict(status='passed',scope='same frozen goal set, declaration/assembly contract comparison only',documents=rows,
                limitations=['Three rebuilds are deterministic engineering repetition, not stochastic model samples.','Relation judgments come from candidate authoring; larger relation count is not evidence of greater accuracy.'])
    with (RUN/'fixed-goal-modeling.json').open('xb') as handle:handle.write(k.encode(result))
    print(json.dumps(dict(status='passed',documents=len(rows),all_goal_sets_identical=True),ensure_ascii=False))


if __name__=='__main__':main()
