"""Check coverage, references, evidence slices, scoring arithmetic and source integrity."""
import hashlib
import json
from pathlib import Path
RUN=Path(__file__).resolve().parent
ROOT=RUN.parents[1]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def jl(p):return [json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x]
def main():
    checks={}
    m=read(RUN/'metrics.json');a=jl(RUN/'goal-alignment.jsonl');p=jl(RUN/'paper-goal-correspondence.jsonl');r=jl(RUN/'relation-comparison.jsonl')
    checks['local_goal_coverage']=len(a)==len({x['local_id'] for x in a})==398
    checks['paper_goal_coverage']=len(p)==len({(x['document_id'],x['paper_id']) for x in p})==1600
    checks['document_deliverables']=all((RUN/'per-document'/f'DOC{i:03}.md').exists() and (RUN/'per-document'/f'DOC{i:03}.json').exists() for i in range(3,37))
    checks['local_pair_coverage']=len(r)==len({(x['document_id'],tuple(sorted(x['local_pair']))) for x in r})==2263
    papers={(x['document_id'],x['paper_id']) for x in p}
    checks['alignment_paper_references']=all((x['document_id'],pid) in papers for x in a for pid in x['paper_ids'])
    invalid_evidence=[]
    for x in a:
        src=(ROOT/'output'/x['document_id']/'source.txt').read_text(encoding='utf-8')
        for e in x['evidence']:
            if src[e['start_char']:e['end_char']]!=e['quote'] or not e['source_turn_ids']:invalid_evidence.append([x['local_id'],e['evidence_id']])
    checks['alignment_evidence_slices_and_turns']=not invalid_evidence
    checks['matching_counts']=sum(m['correspondence_labels'].values())==398 and m['counts']['paper_with_correspondence']+m['counts']['paper_only']==1600
    key=read(RUN/'relation-benchmark-key.json');scored=read(RUN/'relation-benchmark-scored.json')
    checks['benchmark_cases_unique_and_complete']=len(key)==len(scored)==len({x['case_id'] for x in scored})==60
    checks['benchmark_pair_split_disjoint']=len({(x['A'],x['B']) for x in key})==60
    for split,stats in m['relation_benchmark'].items():
        if split=='same_context_order_swap':continue
        rows=[x for x in scored if x['split']==split]
        checks['score_'+split]=(stats['n']==len(rows) and stats['correct']==sum(x['prediction']==x['reference'] for x in rows) and stats['resolved']+stats['abstained']==stats['n'])
    checks['five_existing_refinements_reviewed']=len([x for x in read(RUN/'source-based-relation-reviews.json') if x['document_id'] in ['DOC003','DOC010']])==5
    inputs=read(RUN/'input-manifest.json')
    changed=[x['path'] for x in inputs['files'] if hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()!=x['sha256']]
    checks['all_frozen_inputs_unchanged']=not changed
    result={'checks':checks,'passed':all(checks.values()),'invalid_evidence':invalid_evidence,'changed_inputs':changed}
    (RUN/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if not result['passed']:raise SystemExit(1)
if __name__=='__main__':main()
