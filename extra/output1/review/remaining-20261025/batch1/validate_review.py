import json, hashlib, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
BASE=Path(__file__).resolve().parent; ROOT=BASE.parents[2]
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
a=read(BASE/'assignment.json'); r=read(BASE/'review.json'); consumed=[]
def add(p,role,scope): consumed.append({'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'role':role,'actual_read_scope':scope})
add(BASE/'assignment.json','assignment','full')
rules=['model-review/SKILL.md','model-review/references/semantic-review.md','goal-extraction/references/goal-boundaries.md','goal-extraction/references/evidence-rules.md','goal-model-building/references/modeling-rules.md']
for rule in rules:
    p=ROOT/'_run/skill-snapshots/revised/skills'/rule; p.read_text(encoding='utf-8'); add(p,'frozen_rule','full')
for d in a['documents']:
    doc=next(x for x in r['documents'] if x['document_id']==d['document_id'])
    assert doc['reviewed_goal_ids']==d['required_goal_ids']
    assert len(doc['goal_reviews'])==len(d['required_goal_ids'])
    sp=ROOT/d['source_path']; ip=ROOT/d['source_input_path']; mp=ROOT/d['model_path']; dp=mp.parent
    text=sp.read_text(encoding='utf-8'); si=read(ip); m=read(mp); e=read(dp/'attachments/extraction.json'); j=read(dp/'attachments/judgments.json'); k=read(dp/'attachments/kaos-decisions.json'); man=read(dp/'manifest.json')
    assert len(text)==d['source_characters']
    assert len(si['segments'])==d['source_turns']
    assert si['document_hash']==sha(sp)==d['source_sha256']
    assert sha(mp)==d['model_sha256']==doc['model_sha256']
    assert {x['source_id'] for x in si['segments']}=={d['document_id']+f':T{i:03d}' for i in range(d['source_turns'])}
    for artifact in m['input_artifacts']:
        assert sha(dp/artifact['path'])==artifact['sha256']
    for f in man['files']:
        if f['path'] in ['goal-model.json','attachments/extraction.json','attachments/judgments.json','attachments/source.txt','attachments/kaos-decisions.json']:
            assert sha(dp/f['path'])==f['sha256']
    for g in m['goals']:
        if g['goal_id'] not in d['required_goal_ids']:continue
        c=next(x for x in e['candidates'] if x['candidate_id']==g['goal_id'])
        for field in ['statement','actor','origin','inference']: assert c[field]==g[field]
        assert c['context']==g['conditions']
        jj=j['judgments'][g['goal_id']]
        assert jj['target_statement']==g['statement']
        for field in ['label','rationale','supported_parts','unsupported_parts','assumptions','reasoning_steps']: assert jj[field]==g['support'][field]
        ev=[x for x in m['evidence_index'] if x['evidence_id'] in g['evidence_ids']]
        assert {(x['source_id'],x['quote']) for x in ev}=={(x['source_id'],x['quote']) for x in c['evidence_candidates']}
    add(sp,'canonical_source','full semantic reading '+doc['source_read_ranges'][0]['first_turn']+'–'+doc['source_read_ranges'][0]['last_turn'])
    add(ip,'source_index','metadata and all segment mappings checked by program; duplicate prose not separately claimed as manual reading')
    add(mp,'current_model','all goal statements for context; complete required goals, evidence, issues; no new group verdict')
    add(dp/'attachments/extraction.json','extraction','required candidates compared field by field with reviewed model; review_questions read')
    add(dp/'attachments/judgments.json','author_judgments','required judgment fields identical to reviewed support package; independently assessed, not treated as authority')
    add(dp/'attachments/kaos-decisions.json','author_kaos','input binding and questions only; no fresh group sufficient-condition review')
    add(dp/'manifest.json','manifest','metadata and declared required attachment hashes')
    add(dp/'attachments/source.txt','duplicate_source_attachment','hash only')
    print(d['document_id'],len(doc['goal_reviews']),'goals: assignment, source, model, required extraction/judgments and attachment hashes consistent')
assert len(r['documents'])==7 and sum(len(x['goal_reviews']) for x in r['documents'])==82
assert r['status']=='completed' and not r['findings']
for risk in r['candidate_omission_risks']:
    d=next(d for d in a['documents'] if d['document_id']==risk['document_id']); si=read(ROOT/d['source_input_path']); sm={s['source_id']:s['text'] for s in si['segments']}
    for ev in risk['source_evidence']: assert ev['quote'] in sm[ev['source_id']]
(BASE/'consumed-files.json').write_text(json.dumps({'review_id':r['review_id'],'files':consumed,'not_read':['author-review','prior semantic reviews except assignment','baseline answers','historical output','development_reference','upstream_reference','research answers','other batches conclusions'],'validation':'programmatic provenance/coverage checks; not a formal proof or human adoption'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(BASE/'validation.json').write_text(json.dumps({'status':'passed','documents':7,'required_goals':82,'reviewed_goals':82,'source_characters':sum(d['source_characters'] for d in a['documents']),'source_turns':sum(d['source_turns'] for d in a['documents']),'model_and_source_hashes_match_assignment':True,'required_attachment_fields_match_reviewed_model':True,'duplicate_source_attachment_hashes_match':True,'all_bound_quotes_exact_in_source_segments':True,'core_inspection':'not_run','formal_proof':'not_run','human_adoption':'pending'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
