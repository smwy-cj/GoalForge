"""Freeze source files, audit existing outputs, validate all published graph runs."""
import contextlib
import csv
import hashlib
import importlib.util
import io
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[1]
PAPER = RUN / 'inputs/paper/study1/data1'
RAW = ROOT / 'datasets/raw/goalgeneration/16c4ce8bed513bbfdada7ac900ba6b718617a6eb/transcripts.json'

def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def write(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def graph_stats(nodes, edges):
    adj = {k: set() for k in nodes}
    unknown = []
    for a, b in edges:
        if a not in adj or b not in adj:
            unknown.append([a,b])
        else:
            adj[a].add(b)
    indeg = dict.fromkeys(nodes, 0)
    for vs in adj.values():
        for b in vs: indeg[b] += 1
    queue = [n for n in nodes if indeg[n] == 0]
    depth = dict.fromkeys(nodes, 0)
    count = 0
    while queue:
        a = queue.pop()
        count += 1
        for b in adj[a]:
            depth[b] = max(depth[b],depth[a]+1)
            indeg[b] -= 1
            if indeg[b] == 0: queue.append(b)
    touched = set(x for e in edges for x in e) & set(nodes)
    dag = count == len(nodes) and not unknown
    closure = []
    if dag:
        for a in nodes:
            seen, stack = set(), list(adj[a])
            while stack:
                b = stack.pop()
                if b in seen: continue
                seen.add(b)
                stack.extend(adj[b])
            closure.extend([a,b] for b in sorted(seen))
    return {'dag':dag,'unknown_edges':unknown,'node_count':len(nodes),'edge_count':len(set(map(tuple,edges))),
            'duplicate_edges':len(edges)-len(set(map(tuple,edges))), 'participating_nodes':len(touched),
            'isolated_nodes':len(nodes)-len(touched),'depth_edges':max(depth.values(),default=0) if dag else None,
            'closure':closure}

def main():
    spec = importlib.util.spec_from_file_location('historical_audit', ROOT / 'runs/output-evaluation-2026-10-19/audit_outputs.py')
    audit_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(audit_module)
    audit_module.DEST = RUN
    with contextlib.redirect_stdout(io.StringIO()): audit_module.audit()
    audit = read(RUN / 'audit-results.json')
    audit['date'] = '2026-10-22'
    audit['execution_note'] = 'Re-executed historical deterministic audit on current input files; paper-derived historical metrics removed.'
    audit.pop('paper_derived_metrics',None)
    write(RUN / 'audit-results.json',audit)

    raw, summary, graphs = read(RAW),read(PAPER/'summarized.json'),read(PAPER/'graphs.json')
    model_runs = read(PAPER/'models.json')
    mapping, graph_rows = [],[]
    tracked = [RAW,ROOT/'docs/14-Codex结果比对方案.md',RUN/'protocol.md',RUN/'prepare_comparison.py',ROOT/'runs/output-evaluation-2026-10-19/audit_outputs.py', ROOT/'output/DOC005/v0.1-accepted/goal-model.json']
    tracked.extend(p for p in (ROOT/'skills').rglob('*') if p.is_file() and p.suffix in ('.md','.py','.js','.html','.css'))
    for source_json in sorted((ROOT/'datasets/processed/goalforge-v1/source').glob('DOC*.json')):
        source = read(source_json)
        key, ix, doc = source['upstream_id'],source['upstream_index_zero_based'],source['document_id']
        raw_id = str(raw['ids'][ix])
        turns = raw['transcript'][ix]
        exact = len(turns)==len(source['turns']) and all(str(a['turn'])==str(b['turn']) and a['speaker']==b['speaker'] and a['text']==b['text'] for a,b in zip(turns,source['turns']))
        mapping.append({'document_id':doc,'upstream_id':key,'array_index_zero_based':ix,'upstream_id_agrees':key==raw_id,
                        'turns_exact':exact,'turn_count':len(turns),'source_sha256':sha(source_json.with_suffix('.txt')),
                        'paper_goals':len(summary[key]),'paper_runs':len(graphs[key])})
        tracked.extend([source_json,source_json.with_suffix('.txt')])
        tracked.extend(p for p in (ROOT/'output'/doc).rglob('*') if p.is_file() and 'v0.1-accepted' not in p.parts)
        model=read(ROOT/'output'/doc/'final/goal-model.json')
        ev={e['evidence_id']:e for e in model['evidence_index']}
        goals=[]
        for g in model['goals']:
            goals.append({**g,'quotes':[ev[e] for e in g['evidence_ids']]})
        packet={'document_id':doc,'source':source['turns'],'local_goals':goals,
                'paper_goals':[{'paper_id':f'g{i}','statement':t} for i,t in enumerate(summary[key])],
                'local_edges':model['edges']}
        write(RUN/'packets'/f'{doc}.json',packet)
        compact = [f'# {doc}', '## LOCAL']
        for g in goals:
            compact.append(f"{g['goal_id'].split('-')[-1]} {g['statement']} | context: {'; '.join(g.get('context',[]))}")
            for e in g['quotes']:
                compact.append(f"  {e['evidence_id']} {e.get('source_id','')} {e['quote']}")
        compact.append('## PAPER summarized goals')
        compact.extend(f"g{i} {t}" for i,t in enumerate(summary[key]))
        (RUN/'packets'/f'{doc}.txt').write_text('\n'.join(compact),encoding='utf-8')
        for run_ix,(nodes,edges,implied) in enumerate(graphs[key]):
            stats=graph_stats(nodes,edges)
            base_errors=[f'g{i}' for i,t in enumerate(summary[key]) if nodes.get(f'g{i}')!=t]
            graph_rows.append({'document_id':doc,'run_index':run_ix,'implied_ids':implied,
                               'base_goal_mismatches':base_errors,'model_pass_present':bool(model_runs[key][run_ix].get('pass')),
                               **stats})
    tracked.extend(p for p in (RUN/'inputs').rglob('*') if p.is_file())
    unique=sorted(set(tracked))
    manifest={'created_at_utc':datetime.now(timezone.utc).isoformat(),'commit':'16c4ce8bed513bbfdada7ac900ba6b718617a6eb',
              'generator_model':'unknown','generator_skill_revision':'unknown','generator_budget':'unknown',
              'reviewer':'Codex in this chat; automatic semantic review; exact backend model identifier not exposed',
              'document_mapping':mapping,'files':[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size} for p in unique]}
    write(RUN/'input-manifest.json',manifest)
    write(RUN/'paper-graph-audit.json',{'runs':graph_rows,'totals':{
        'documents':len(mapping),'runs':len(graph_rows),'dag_runs':sum(r['dag'] for r in graph_rows),
        'base_goal_mismatch_runs':sum(bool(r['base_goal_mismatches']) for r in graph_rows),
        'paper_summary_goals':sum(len(v) for v in summary.values())}})
    rows=list(csv.DictReader((PAPER/'comps_final.csv').open(encoding='utf-8-sig',newline='')))
    labels=Counter((r['rater1'],r['rater2']) for r in rows)
    normalize = lambda s: s.strip().upper().replace(' ', '_')
    paired = [r for r in rows if r['rater1'].strip() and r['rater2'].strip()]
    normalized_agreement = sum(normalize(r['rater1']) == normalize(r['rater2']) for r in paired)
    pair_groups = {}
    for i,r in enumerate(rows): pair_groups.setdefault((r['G1'],r['G2']),[]).append((i,r))
    duplicate_groups = [{'goals':list(k),'row_indices_zero_based':[i for i,r in v],
                         'rater2_labels':sorted({normalize(r['rater2']) for i,r in v})}
                        for k,v in pair_groups.items() if len(v)>1]
    write(RUN/'relation-label-profile.json',{'rows':len(rows),'exact_agreement':sum(r['rater1']==r['rater2'] for r in rows),
         'double_labeled_rows':len(paired),'missing_rater1_rows':sum(not r['rater1'].strip() for r in rows),
         'normalized_agreement_among_double_labeled':normalized_agreement,
         'normalization':"strip, uppercase, replace spaces with underscore; FLASE not silently corrected",
         'label_pairs':[{'rater1':a,'rater2':b,'count':n} for (a,b),n in labels.items()],
         'distinct_ordered_pairs':len({(r['G1'],r['G2']) for r in rows}),
         'duplicate_groups':duplicate_groups,
         'duplicate_groups_with_conflicting_rater2':sum(len(x['rater2_labels'])>1 for x in duplicate_groups),
         'calibration_status':'not_run; labels profiled for integrity; do not claim blind held-out performance in this chat'})
    print(json.dumps({'local_audit':audit['totals'],'audit_errors':audit['errors'],
       'mapping_exact':all(x['upstream_id_agrees'] and x['turns_exact'] for x in mapping),
       'paper_goals':sum(len(v) for v in summary.values()),'paper_runs':len(graph_rows),'dag_runs':sum(r['dag'] for r in graph_rows),
       'paper_label_rows':len(rows),'exact_label_agreement':sum(r['rater1']==r['rater2'] for r in rows)},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
