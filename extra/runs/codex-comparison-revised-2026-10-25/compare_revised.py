"""Read frozen deliveries and assemble an explicitly authored content comparison."""
import csv
import hashlib
import json
import argparse
from collections import Counter
from pathlib import Path

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[1]
OLD = ROOT / 'runs/codex-comparison-2026-10-22'
PAPER = OLD / 'inputs/paper/study1/data1'

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def prepare():
    index = read(ROOT / 'output1/_run/delivery-index.json')
    paper = read(PAPER / 'summarized.json')
    entries = [d for d in index['documents'] if d['arm'] == 'revised']
    assert len(entries) == 34 and len({d['document_id'] for d in entries}) == 34
    records, files = [], {}
    for entry in entries:
        doc = entry['document_id']
        path = ROOT / 'output1' / entry['json']
        model = read(path)
        source_path = ROOT / f'datasets/processed/goalforge-v1/source/{doc}.json'
        source = read(source_path)
        key = source['upstream_id']
        old_model = read(ROOT / f'output/{doc}/final/goal-model.json')
        old_comparison = read(OLD / f'per-document/{doc}.json')
        ev = {e['evidence_id']: e for e in model['evidence_index']}
        assert len(model['goals']) == entry['goals']
        packet = {'document_id': doc, 'upstream_id': key,
                  'model_path': path.relative_to(ROOT).as_posix(), 'model_sha256': sha(path),
                  'goals': model['goals'], 'refinement_groups': model['refinement_groups'],
                  'evidence_index': model['evidence_index'],
                  'paper_goals': [{'paper_id':f'g{i}', 'statement':s} for i,s in enumerate(paper[key])],
                  'old_goal_count':len(old_model['goals']), 'old_counts':old_comparison['counts']}
        write(RUN / f'packets/{doc}.json', packet)
        lines = [f'# {doc}', '## NEW']
        for g in model['goals']:
            lines.append(f"{g['goal_id'].split('-')[-1]} {g['statement']} | conditions: {'; '.join(g.get('conditions',[]))} | origin: {g.get('origin')} | support: {g['support']['label']}")
        lines.append('## PAPER')
        lines.extend(f'g{i} {s}' for i,s in enumerate(paper[key]))
        (RUN / f'packets/{doc}.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')
        records.append({'document_id':doc,'model_path':packet['model_path'],'model_sha256':packet['model_sha256'],
                        'old_goals':len(old_model['goals']),'revised_goals':len(model['goals']),
                        'paper_goals':len(paper[key]),'groups':len(model['refinement_groups']),
                        'supported_complete_groups':sum(g['status']=='supported' and g['completeness']=='complete' for g in model['refinement_groups'])})
        for f in [path, source_path, source_path.with_suffix('.txt'), ROOT / f'output/{doc}/final/goal-model.json', OLD / f'per-document/{doc}.json']:
            files[f.relative_to(ROOT).as_posix()] = sha(f)
    for f in [PAPER/'summarized.json', PAPER/'sampled-goals.json', ROOT/'output1/_run/delivery-index.json',
              ROOT/'output1/_run/run-config.json', ROOT/'output1/review/remaining-20261025/summary.json']:
        files[f.relative_to(ROOT).as_posix()] = sha(f)
    for f in (ROOT/'output1/_run/skill-snapshots/revised/skills').rglob('*.md'):
        files[f.relative_to(ROOT).as_posix()] = sha(f)
    write(RUN/'input-manifest.json',{'date':'2026-10-25','selected_from':'output1/_run/delivery-index.json revised entries; exact paths and SHA-256 frozen',
          'documents':records,'files':files,'reviewer':'Codex in current chat; no new independent reviewer or human Gold',
          'source_semantic_review':'Existing output1 reviews are provenance only; present pass compares goal content, with targeted source rechecks.',
          'generator_controls':'Exact model, sampling and budget not controlled; no causal skills uplift claim.'})
    print(json.dumps({'documents':len(records),'old_goals':sum(r['old_goals'] for r in records),'revised_goals':sum(r['revised_goals'] for r in records),
                      'paper_goals':sum(r['paper_goals'] for r in records),'groups':sum(r['groups'] for r in records),'supported_complete_groups':sum(r['supported_complete_groups'] for r in records)},ensure_ascii=False))

LABELS = {'e':'equivalent','b':'local_broader','n':'local_narrower','p':'partial_overlap','l':'local_only','u':'uncertain'}
ZH = {'equivalent':'等价','local_broader':'新版更宽','local_narrower':'新版更窄','partial_overlap':'部分重叠','local_only':'新版单方','uncertain':'待确认'}

def cell(value):
    return str(value).replace('|','／').replace('\n',' ')

def assemble():
    from content_decisions import DECISIONS, CONTRASTS
    manifest = read(RUN/'input-manifest.json')
    errors, records, paper_records, summary, groups, evidence_checks = [], [], [], [], [], []
    for rel, frozen_sha in manifest['files'].items():
        if sha(ROOT/rel) != frozen_sha:
            errors.append({'changed_input':rel})
    for item in manifest['documents']:
        doc = item['document_id']
        packet = read(RUN/f'packets/{doc}.json')
        model = read(ROOT/item['model_path'])
        assert model['goals'] == packet['goals'] and model['refinement_groups'] == packet['refinement_groups']
        rows = DECISIONS[doc]
        assert len(rows) == len(packet['goals']), (doc,len(rows),len(packet['goals']))
        assert len({g['goal_id'] for g in packet['goals']}) == len(rows)
        paper = {g['paper_id']:g['statement'] for g in packet['paper_goals']}
        ev = {e['evidence_id']:e for e in packet['evidence_index']}
        source_path = ROOT/f'datasets/processed/goalforge-v1/source/{doc}.txt'
        text = source_path.read_text(encoding='utf-8-sig')
        for evidence in ev.values():
            start, end = evidence.get('start_char'), evidence.get('end_char')
            valid = isinstance(start,int) and isinstance(end,int) and text[start:end] == evidence['quote']
            evidence_checks.append({'document_id':doc,'evidence_id':evidence['evidence_id'],'slice_valid':valid})
            if not valid:
                errors.append({'document_id':doc,'evidence_id':evidence['evidence_id'],'error':'source quote interval mismatch'})
        doc_rows, represented = [], set()
        for goal,(indices,short,reason) in zip(packet['goals'],rows):
            ids = [f'g{int(i)}' for i in indices.split()]
            assert len(ids) == len(set(ids)) and all(i in paper for i in ids)
            label = LABELS[short]
            assert bool(ids) == (label != 'local_only')
            if label == 'equivalent':
                assert goal['support']['label'] != 'insufficient'
            if label != 'uncertain':
                represented.update(ids)
            qualified_id = f"{doc}-{goal['goal_id'].split('-')[-1]}"
            contrasts = [{'paper_id':i,'paper_statement':paper[i],'rationale':r} for i,r in CONTRASTS.get(qualified_id,[])]
            row = {'document_id':doc,'revised_id':goal['goal_id'],'qualified_id':qualified_id,'revised_statement':goal['statement'],
                   'conditions':goal.get('conditions',[]),'origin_from_generator':goal.get('origin'),
                   'support_from_generator':goal['support']['label'],'model_path':item['model_path'],
                   'model_sha256':item['model_sha256'],'paper_ids':ids,
                   'paper_statements':[paper[i] for i in ids],'correspondence':label,'rationale':reason,
                   'contrast_only':contrasts,'evidence':[ev[eid] for eid in goal['evidence_ids']],
                   'source_support_rejudged_in_this_run':False,
                   'reviewer':'current Codex chat; content correspondence; not independent Gold'}
            doc_rows.append(row)
        unmatched = []
        for pid, statement in paper.items():
            matched_by = [r['revised_id'] for r in doc_rows if pid in r['paper_ids'] and r['correspondence']!='uncertain']
            uncertain_by = [r['revised_id'] for r in doc_rows if pid in r['paper_ids'] and r['correspondence']=='uncertain']
            entry = {'document_id':doc,'paper_id':pid,'paper_statement':statement,'revised_candidate_ids':matched_by,
                     'uncertain_candidate_ids':uncertain_by,
                     'status':'candidate_correspondence' if matched_by else 'uncertain' if uncertain_by else 'paper_only',
                     'source_adjudication_in_this_run':'not_run; not automatically a missed goal'}
            paper_records.append(entry)
            if not matched_by:
                unmatched.append(entry)
        counts = Counter(r['correspondence'] for r in doc_rows)
        group_counts = Counter((g['status'],g['completeness']) for g in packet['refinement_groups'])
        active = sum(n for (s,c),n in group_counts.items() if s=='supported' and c=='complete')
        summary.append({**item,'revised_minus_old':item['revised_goals']-item['old_goals'],
                        'revised_with_candidate_correspondence':sum(r['correspondence'] not in ('local_only','uncertain') for r in doc_rows),
                        'paper_with_candidate_correspondence':len(represented),
                        'paper_without_resolved_correspondence':len(paper)-len(represented),
                        **{k:counts[k] for k in ZH}})
        groups.extend({'document_id':doc,'model_path':item['model_path'],**g} for g in packet['refinement_groups'])
        write(RUN/f'per-document/{doc}.json',{'document_id':doc,'model_path':item['model_path'],
            'model_sha256':item['model_sha256'],'scope':'all revised goal statements/conditions versus full paper list; not full source adjudication',
            'counts':summary[-1],'goals':doc_rows,'paper_without_resolved_correspondence':unmatched,
            'refinement_groups':packet['refinement_groups']})
        lines=[f'# {doc} 新版目标与论文公开目标内容比较','',
               f"旧版 {item['old_goals']} 项；新版 {item['revised_goals']} 项；论文 {item['paper_goals']} 项。",'',
               f"新版版本：`{item['model_path']}`；SHA-256：`{item['model_sha256']}`。",'',
               '评价：当前会话Codex逐项内容对应；不是独立人审或提取准确率。支持标签为生成方标签，本轮未对全部源文重新裁决。', '',
               '| 新版目标 | 条件与例外 | 论文ID | 对应 | 理由 |','|---|---|---|---|---|']
        for r in doc_rows:
            lines.append('| '+' | '.join(cell(v) for v in [r['revised_id']+' '+r['revised_statement'],'；'.join(r['conditions']),', '.join(r['paper_ids']) or '无',ZH[r['correspondence']],r['rationale']])+' |')
        lines+=['','## 未获得已判定对应的论文目标','','未对应不等于漏提；本轮未逐项裁决这些目标的原文资格。','',
                '| 论文ID | 英文原始表述 | 状态 |','|---|---|---|']
        for r in unmatched:
            lines.append('| '+' | '.join(cell(v) for v in [r['paper_id'],r['paper_statement'],r['status']])+' |')
        if any(r['contrast_only'] for r in doc_rows):
            lines+=['','## 不作为匹配计数的对照','','| 新版ID | 论文ID | 实际区别 |','|---|---|---|']
            for r in doc_rows:
                for c in r['contrast_only']:
                    lines.append(f"| {r['revised_id']} | {c['paper_id']} | {cell(c['rationale'])} |")
        lines+=['','## 精化组','',f"本篇 {len(packet['refinement_groups'])} 组，其中 {active} 组标为 supported/complete。组语义不与论文二元边数直接评分。",'',
                '绑定原句、英文对应、版本和每组理由见同名 JSON；成立标签不是形式证明。','']
        (RUN/f'per-document/{doc}.md').write_text('\n'.join(lines),encoding='utf-8')
        records.extend(doc_rows)
    for name,data in [('goal-alignment.jsonl',records),('paper-goal-correspondence.jsonl',paper_records)]:
        (RUN/name).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in data),encoding='utf-8')
    write(RUN/'refinement-groups.json',groups)
    write(RUN/'evidence-validation.json',evidence_checks)
    with (RUN/'document-summary.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(summary[0]));writer.writeheader();writer.writerows(summary)
    labels=Counter(r['correspondence'] for r in records)
    support=Counter(r['support_from_generator'] for r in records)
    metrics={'date':'2026-10-25','scope':'34 selected revised deliveries; all 559 goals content-compared against paper summarized list',
             'counts':{'documents':len(summary),'old_goals':sum(r['old_goals'] for r in summary),'revised_goals':len(records),
                       'paper_goals':len(paper_records),'revised_with_candidate_correspondence':sum(r['correspondence'] not in ('local_only','uncertain') for r in records),
                       'revised_local_only':labels['local_only'],'revised_uncertain':labels['uncertain'],
                       'paper_with_candidate_correspondence':sum(r['status']=='candidate_correspondence' for r in paper_records),
                       'paper_without_resolved_correspondence':sum(r['status']!='candidate_correspondence' for r in paper_records)},
             'correspondence_labels':dict(labels),'support_labels_from_generator':dict(support),
             'groups':{'total':len(groups),'supported_complete':sum(g['status']=='supported' and g['completeness']=='complete' for g in groups),
                       'other':sum(not(g['status']=='supported' and g['completeness']=='complete') for g in groups)},
             'evidence':{'total_unique_model_entries':len(evidence_checks),'valid_slices':sum(e['slice_valid'] for e in evidence_checks)},
             'source_full_adjudication_this_run':False,'independent_context_review_this_run':False,'human_gold':False,
             'old_vs_revised_label_counts_directly_comparable':False,
             'limits':['Content correspondences are authored candidates, not precision/recall or semantic support judgments.',
                       'Current reviewer has prior context; more explicit contrast-only exclusions mean aggregate mapping counts are not a controlled before/after experiment.',
                       'All unmatched paper goals remain source-unadjudicated in this pass.',
                       'Exact generator models, sampling and budgets unknown; revised outputs include more revision and review work.',
                       'Existing output1 independent-context source reviews are separate provenance, not this run or human Gold.']}
    write(RUN/'metrics.json',metrics)
    checks={'all_34_documents':len(summary)==34,'all_559_revised_goals':len(records)==559,
            'all_1600_paper_goals':len(paper_records)==1600,'all_44_groups':len(groups)==44,
            'unique_document_goal_keys':len({(r['document_id'],r['revised_id']) for r in records})==len(records),
            'all_source_quote_slices_valid':all(e['slice_valid'] for e in evidence_checks),
            'frozen_inputs_unchanged':not any('changed_input' in e for e in errors),
            'uncertain_candidate_not_counted_as_equivalent':all(r['correspondence']!='equivalent' for r in records if r['support_from_generator']=='insufficient')}
    write(RUN/'validation.json',{'checks':checks,'errors':errors,'passed':all(checks.values()) and not errors})
    print(json.dumps({'metrics':metrics,'validation':checks,'errors':errors[:8]},ensure_ascii=False,indent=2))

if __name__ == '__main__':
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=['prepare','assemble'],nargs='?',default='prepare')
    args=parser.parse_args()
    prepare() if args.stage=='prepare' else assemble()
