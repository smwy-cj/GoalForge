import json, hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

records = []
for branch in ('baseline', 'revised'):
    for doc in ('DOC010', 'DOC023', 'DOC031'):
        folder = ROOT / 'output1' / branch / doc / 'v1'
        model = read(folder / 'delivery/goal-model.json')
        extract = read(folder / 'extraction.json')
        judgments = read(folder / 'judgments.json')['judgments']
        decisions = read(folder / 'kaos-decisions.json')
        text = (ROOT / 'output1/_inputs' / doc / 'source.txt').read_text(encoding='utf-8-sig')
        sources = {s['source_id']: s for s in read(ROOT / 'output1/_inputs' / doc / 'source-input.json')['segments']}
        errors = []
        for e in model['evidence_index']:
            if text[e['start_char']:e['end_char']] != e['quote']:
                errors.append('quote mismatch: ' + e['evidence_id'])
            if e['quote'] not in sources[e['source_id']]['text']:
                errors.append('source mismatch: ' + e['evidence_id'])
        goals = {g['goal_id']: g for g in model['goals']}
        for c in extract['candidates']:
            g = goals[c['candidate_id']]
            for key in ('statement','actor','origin','inference'):
                if c.get(key) != g.get(key): errors.append('candidate projection '+c['candidate_id']+' '+key)
            if c['context'] != g['conditions']: errors.append('context projection '+c['candidate_id'])
            j = judgments[c['candidate_id']]
            for key in ('label','rationale','supported_parts','unsupported_parts','assumptions','reasoning_steps'):
                if j.get(key) != g['support'].get(key): errors.append('judgment projection '+c['candidate_id']+' '+key)
        groups = {g['group_id']:g for g in model['refinement_groups']}
        for d in decisions['groups']:
            g = groups[d['group_id']]
            for key in ('parent_id','child_ids','kind','status','completeness','rationale','assumptions'):
                if d.get(key) != g.get(key): errors.append('group projection '+d['group_id']+' '+key)
        if sha(folder/'source.txt') != sha(ROOT/'output1/_inputs'/doc/'source.txt'): errors.append('source text differs')
        if sha(folder/'source-input.json') != sha(ROOT/'output1/_inputs'/doc/'source-input.json'): errors.append('source input differs')
        if sha(folder/'assembled/model-input.json') != sha(folder/'delivery/goal-model.json'): errors.append('assembly/delivery differs')
        inspection = read(ROOT/'output1/review/engineering'/f'{branch}-{doc}-inspection.json')
        records.append({'branch':branch,'document':doc,'model_sha256_bytes':sha(folder/'delivery/goal-model.json'),
                        'goals':len(goals),'groups':len(groups),'source_turns':len(sources),'exact_quotes_checked':len(model['evidence_index']),
                        'projection_and_quote_errors':errors,'independent_inspect':inspection})
out = ROOT/'output1/review/engineering/projection-and-evidence-audit.json'
out.write_text(json.dumps({'scope':'Read-only projections, source/evidence equality, re-executed inspect; not semantic proof','records':records},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps([{'branch':r['branch'],'doc':r['document'],'goals':r['goals'],'groups':r['groups'],'quotes':r['exact_quotes_checked'],'errors':r['projection_and_quote_errors'],'inspect':r['independent_inspect']['structure']} for r in records],ensure_ascii=False))
