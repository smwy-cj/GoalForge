import json

d = json.load(open('source/DOC021.json', encoding='utf-8'))
segs = {t['source_id']: t['text'] for t in d['turns']}
spec = json.load(open('spec.json', encoding='utf-8'))

items = []
for c in spec['raw_candidates']:
    for e in c['evidence']:
        items.append((c['candidate_id'], e))
for g in spec['goals']:
    for e in g['evidence']:
        items.append((g['candidate_id'], e))
for r in spec['decisions']['relations']:
    for e in r['evidence_quotes']:
        items.append((r['relation_id'], e))
for g in spec['decisions']['groups']:
    for e in g['evidence_quotes']:
        items.append((g['group_id'], e))
for s in spec['ledger']['source_checks']:
    for e in s['evidence_candidates']:
        items.append((s['check_id'], e))

bad = 0
for owner, e in items:
    t = segs.get(e['source_id'])
    if t is None:
        print('NO SEG', owner, e['source_id'])
        bad += 1
        continue
    n = t.count(e['quote'])
    if n != 1:
        print('BAD', owner, e['source_id'], n, e['quote'][:90])
        bad += 1
print('total', len(items), 'bad', bad)

# id consistency
goals = {g['candidate_id'] for g in spec['goals']}
cands = {c['candidate_id'] for c in spec['raw_candidates']}
ent = {e['candidate_id']: e for e in spec['ledger']['entries']}
print('cands', len(cands), 'entries', len(ent), 'goals', len(goals))
print('missing entries', cands - set(ent), 'extra', set(ent) - cands)
for e in spec['ledger']['entries']:
    for g in e['final_goal_ids']:
        if g not in goals:
            print('bad goal ref', e['candidate_id'], g)
mapped = {g for e in spec['ledger']['entries'] for g in e['final_goal_ids']}
print('goals without provenance', goals - mapped)
assert all(len(w['window_results']) == 38 for w in spec['ledger']['passes'])
print('windows ok')
