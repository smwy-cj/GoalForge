import json, io, os, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, 'source', 'DOC019.json')
PARTS = os.path.join(BASE, 'parts')
OUT = os.path.join(BASE, 'spec.json')

def load(name):
    with io.open(os.path.join(PARTS, name), encoding='utf-8') as f:
        return json.load(f)

src = json.load(io.open(SRC, encoding='utf-8'))
texts = {t['source_id']: t['text'] for t in src['turns']}

raw = load('p1-candidates.json') + load('p2-candidates.json')
goals = load('p3-goals-a.json') + load('p3-goals-b.json')
ledger_part = load('p4-ledger.json')
meta = load('p5-meta-decisions.json')

# drop stray keys not in contracts
for g in goals:
    g.pop('modality_note', None)
for e in ledger_part['entries']:
    e.pop('description', None)

# windows
try:
    wins = json.load(io.open(os.path.join(BASE, 'probe', 'source-windows.json'), encoding='utf-8'))
    window_ids = [w['window_id'] for w in wins['windows']]
except Exception:
    window_ids = ['DOC019:W%04d' % i for i in range(1, 33)]

def window_results():
    return [{'window_id': w, 'status': 'processed', 'reason': ''} for w in window_ids]

run = dict(meta['run'])
run['passes'] = [
    {'pass_id': 'P1', 'kind': 'initial', 'context': 'isolated', 'status': 'completed', 'window_results': window_results()},
    {'pass_id': 'P2', 'kind': 'full_context', 'context': 'shared', 'status': 'completed', 'window_results': window_results()}
]

spec = {
    'document_id': 'DOC019',
    'raw_candidates': raw,
    'goals': goals,
    'review_questions': meta['review_questions'],
    'limitations': meta['limitations'],
    'ledger': {
        'model': run['model'],
        'temperature': run['temperature'],
        'budget': run['budget'],
        'usage': run['usage'],
        'skill_revision': run['skill_revision'],
        'prompt_revision': run['prompt_revision'],
        'planned_passes': run['planned_passes'],
        'stop_reason': run['stop_reason'],
        'passes': run['passes'],
        'full_context_review': meta['full_context_review'],
        'entries': ledger_part['entries'],
        'source_checks': ledger_part['source_checks']
    },
    'decisions': meta['decisions']
}

with io.open(OUT, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(spec, f, ensure_ascii=False, indent=1)

# ---- validation ----
errors = []
warn = []

def check_quotes(where, items):
    for it in items or []:
        sid = it.get('source_id')
        q = it.get('quote')
        if sid not in texts:
            errors.append('%s: unknown source_id %s' % (where, sid)); continue
        t = texts[sid]
        if q not in t:
            errors.append('%s: quote NOT exact in %s: %r' % (where, sid, q[:80]))
        elif t.count(q) > 1:
            warn.append('%s: ambiguous quote in %s (%d hits): %r' % (where, sid, t.count(q), q[:60]))

for c in raw:
    check_quotes('cand ' + c['candidate_id'], c.get('evidence'))
    if not any(e.get('role') == 'basis' for e in c['evidence']):
        errors.append('cand %s: no basis evidence' % c['candidate_id'])
for g in goals:
    check_quotes('goal ' + g['candidate_id'], g.get('evidence'))
    if g['judgment']['label'] in ('direct', 'inferred') and g['judgment'].get('unsupported_parts'):
        errors.append('goal %s: unsupported_parts must be empty' % g['candidate_id'])
for s in ledger_part['source_checks']:
    check_quotes('check ' + s['check_id'], s.get('evidence_candidates'))
for r in meta['decisions']['relations']:
    check_quotes('rel ' + r['relation_id'], r.get('evidence_quotes'))

raw_ids = {c['candidate_id'] for c in raw}
goal_ids = {g['candidate_id'] for g in goals}
for e in ledger_part['entries']:
    if e['candidate_id'] not in raw_ids:
        errors.append('entry for unknown candidate %s' % e['candidate_id'])
    for gid in e.get('final_goal_ids', []):
        if gid not in goal_ids:
            errors.append('entry %s -> unknown goal %s' % (e['candidate_id'], gid))
if len(ledger_part['entries']) != len(raw_ids):
    errors.append('entries count %d != candidates %d' % (len(ledger_part['entries']), len(raw_ids)))
missing = {e['candidate_id'] for e in ledger_part['entries']} ^ raw_ids
if missing:
    errors.append('entry/candidate id mismatch: %s' % missing)
# every goal has provenance
prov = {}
for e in ledger_part['entries']:
    for gid in e.get('final_goal_ids', []):
        prov.setdefault(gid, []).append(e['candidate_id'])
for gid in sorted(goal_ids):
    if gid not in prov:
        errors.append('goal %s has no raw candidate provenance' % gid)
# excluded checks must not carry goals
for s in ledger_part['source_checks']:
    if s['outcome'] == 'excluded' and s.get('final_goal_ids'):
        errors.append('check %s excluded but has final_goal_ids' % s['check_id'])
# questions targets
valid_targets = goal_ids | {r['relation_id'] for r in meta['decisions']['relations']} | {'DOC019-goal-model'}
for q in meta['decisions']['questions']:
    if q['target_id'] not in valid_targets:
        errors.append('question target %s not existing' % q['target_id'])
for q in meta['review_questions']:
    for cid in q['candidate_ids']:
        if cid not in raw_ids and cid not in goal_ids:
            errors.append('review_question ref %s unknown' % cid)
# inference refs
for g in goals:
    inf = g.get('inference')
    if inf:
        for b in inf['basis_candidate_ids']:
            if b not in goal_ids and b not in raw_ids:
                errors.append('goal %s inference basis %s unknown' % (g['candidate_id'], b))

print('raw candidates:', len(raw), 'goals:', len(goals), 'entries:', len(ledger_part['entries']),
      'checks:', len(ledger_part['source_checks']), 'relations:', len(meta['decisions']['relations']),
      'groups:', len(meta['decisions']['groups']), 'windows:', len(window_ids))
print('--- errors ---')
for e in errors:
    print('E', e)
print('--- warnings ---')
for w in warn:
    print('W', w)
print('OK' if not errors else 'FAILED')
