import json, collections

spec = json.load(open('spec.json', encoding='utf-8'))
src = json.load(open('source/DOC025.json', encoding='utf-8'))
T = {t['source_id']: t['text'] for t in src['turns']}


def chk(items, label):
    for e in items:
        t = T[e['source_id']]
        q = e['quote']
        if q not in t:
            print('MISSING', label, e['source_id'], q[:60])
        elif t.count(q) > 1:
            print('AMBIG', label, e['source_id'], q[:60])


for c in spec['raw_candidates']:
    chk(c['evidence'], c['candidate_id'])
for g in spec['goals']:
    chk(g['evidence'], g['candidate_id'])
for r in spec['decisions']['relations']:
    chk(r['evidence_quotes'], r['relation_id'])
for s in spec['ledger']['source_checks']:
    chk(s['evidence_candidates'], s['check_id'])

print('goals', [g['candidate_id'] for g in spec['goals']])
print('n_candidates', len(spec['raw_candidates']), 'n_entries', len(spec['ledger']['entries']))
entries = {e['candidate_id']: e for e in spec['ledger']['entries']}
print('missing_entries', sorted(set(c['candidate_id'] for c in spec['raw_candidates']) - set(entries)))
cnt = collections.Counter(g for e in entries.values() for g in e['final_goal_ids'])
for e in entries.values():
    if e['disposition'] in ('keep', 'merge') and len(e['final_goal_ids']) != 1:
        print('BAD one_goal', e['candidate_id'])
    if e['disposition'] == 'merge' and cnt[e['final_goal_ids'][0]] < 2:
        print('BAD merge_count', e['candidate_id'])
    if e['disposition'] == 'split' and len(e['final_goal_ids']) < 2:
        print('BAD split', e['candidate_id'])
    if e['disposition'] == 'exclude' and e['final_goal_ids']:
        print('BAD exclude', e['candidate_id'])
for g in [x['candidate_id'] for x in spec['goals']]:
    if not cnt[g]:
        print('NO_PROVENANCE', g)
for s in spec['ledger']['source_checks']:
    union = {g for cid in s['candidate_ids'] for g in entries[cid]['final_goal_ids']}
    if not set(s['final_goal_ids']) <= union:
        print('BAD check', s['check_id'], set(s['final_goal_ids']) - union)
print('windows_in_pass', len(spec['ledger']['passes'][0]['window_results']))
print('support', {g['candidate_id']: g['judgment']['label'] for g in spec['goals']})
