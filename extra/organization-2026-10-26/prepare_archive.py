# -*- coding: utf-8 -*-
"""Prepare a hash-bound, reversible archive plan and active benchmark data."""
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def write(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('x', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def copy_record(source, target):
    assert not target.exists(), target
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    assert sha(source) == sha(target)
    return dict(path=target.relative_to(ROOT).as_posix(), source=source.relative_to(ROOT).as_posix(), sha256=sha(target), bytes=target.stat().st_size)


def main():
    moves = [('runs','extra/runs'), ('output','extra/output'), ('output1','extra/output1'),
             ('docs','extra/docs'), ('dist','extra/dist'), ('.workbuddy','extra/tool-state/.workbuddy'),
             ('skills/goal-tracing','extra/legacy-skills/goal-tracing'),
             ('tests/test_skill_migration.py','extra/legacy-tests/test_skill_migration.py'),
             ('tests/test_goal_tracing.py','tests/test_evidence_trace.py'),
             ('README.md','extra/previous-root/README.md')]
    moves += [(p.name, 'extra/materials/'+p.name) for p in ROOT.glob('*.ppt')]
    for parent in ('skills','tests','scripts'):
        moves += [(p.relative_to(ROOT).as_posix(), 'extra/cache/'+p.relative_to(ROOT).as_posix()) for p in (ROOT/parent).rglob('__pycache__') if p.is_dir() and 'goal-tracing' not in p.parts]
    actions = []
    for src, dst in moves:
        s, d = (ROOT/src).resolve(), (ROOT/dst).resolve()
        assert ROOT in s.parents and ROOT in d.parents and s.exists() and not d.exists(), (src,dst)
        files = [s] if s.is_file() else sorted(p for p in s.rglob('*') if p.is_file())
        assert not s.is_symlink() and not any(p.is_symlink() for p in files)
        records = [dict(relative=p.relative_to(s).as_posix() if s.is_dir() else '', sha256=sha(p), bytes=p.stat().st_size) for p in files]
        actions.append(dict(source=src, destination=dst, files=records))
    assert len({a['source'] for a in actions}) == len(actions)
    write(HERE/'move-plan.json', dict(schema_version='goalforge-archive-plan-1', root=str(ROOT), policy='Move only; preserve every archived file byte; no deletion or Git mutation.', actions=actions))

    paper = ROOT/'runs/codex-comparison-2026-10-22/inputs/paper'
    destination = ROOT/'datasets/baselines/paper-study1'
    paper_files = [copy_record(p,destination/p.relative_to(paper)) for p in sorted(paper.rglob('*')) if p.is_file()]
    paper_files.append(copy_record(paper.parent/'download-manifest.json', destination/'download-manifest.json'))
    paper_files.append(copy_record(ROOT/'datasets/raw/goalgeneration/16c4ce8bed513bbfdada7ac900ba6b718617a6eb/LICENSE.md', destination/'LICENSE.upstream.md'))
    old_map = json.loads((ROOT/'runs/codex-comparison-2026-10-22/input-manifest.json').read_bytes())
    write(destination/'document-map.json', dict(upstream_commit=old_map['commit'], documents=old_map['document_mapping']))
    write(destination/'baseline-manifest.json', dict(kind='frozen author artifacts; not human Gold or reproduced paper scores', upstream_commit=old_map['commit'], files=paper_files, historical_source_after_archive='extra/runs/codex-comparison-2026-10-22/inputs/paper', role='summarized.json is the 1600-item modeling input; other generated artifacts retain their distinct roles; never execute generated code'))

    run = ROOT/'runs/skill-optimization-2026-10-25-complete'
    target = ROOT/'datasets/benchmarks/skill-comparison-2026-10-26'
    metrics = json.loads((run/'evaluation/metrics.json').read_bytes())
    records = []
    for row in metrics['documents']:
        source = run/row['original_model']
        dest = target/'models'/row['branch']/(row['document_id']+'.json')
        record = copy_record(source,dest)
        record.update(document_id=row['document_id'],branch=row['branch'],archived_original='extra/'+source.relative_to(ROOT).as_posix(),role='frozen model snapshot for comparison; full delivery attachments remain in archived original run')
        records.append(record)
    review_root = run/'evaluation/source-first-review'
    for doc in sorted({r['document_id'] for r in metrics['documents']}):
        for filename in ('inventory.json','review-first.json','review-repeat.json'):
            records.append(copy_record(review_root/doc/filename,target/'source-review'/doc/filename))
    for filename in ('freeze-manifest.json','validation-first.json','validation-repeat.json','errata-first.json','errata-repeat.json','review-summary.json','review-summary.md'):
        records.append(copy_record(review_root/filename,target/'source-review'/filename))
    for filename in ('metrics.json','protocol.md'):
        records.append(copy_record(run/'evaluation'/filename,target/filename))
    for round_name in ('first','repeat'):
        for source in sorted((run/'evaluation/anonymous'/round_name).rglob('*.json')):
            records.append(copy_record(source,target/'anonymous'/round_name/source.relative_to(run/'evaluation/anonymous'/round_name)))
    sources = []
    for doc in sorted({r['document_id'] for r in metrics['documents']}):
        for suffix in ('.json','.txt'):
            source = ROOT/'datasets/processed/goalforge-v1/source'/(doc+suffix)
            sources.append(dict(document_id=doc,path=source.relative_to(ROOT).as_posix(),sha256=sha(source)))
    write(target/'benchmark-manifest.json', dict(schema_version='goalforge-active-development-benchmark-1', source_documents=8, generation_samples=32, independent_test=False, human_gold=False, files=records, sources=sources, note='Actual benchmark paths are declared here. Copied frozen metrics/review files preserve historical relative paths; full runs are now under extra/runs. Generation must read source only, never these models/reviews.'))
    print(json.dumps(dict(move_actions=len(actions), archived_files=sum(len(a['files']) for a in actions), paper_files=len(paper_files), benchmark_files=len(records))))


if __name__ == '__main__':
    main()
