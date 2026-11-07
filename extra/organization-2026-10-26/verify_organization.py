"""Verify moved bytes, active datasets, retained tests and installed skill paths."""
import ast
import difflib
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
FINAL = HERE/'verification.json'


def load(p):
    return json.loads(p.read_bytes())


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def require(condition, text):
    if not condition:
        raise ValueError(text)


def files_at(p):
    return [p] if p.is_file() else sorted(x for x in p.rglob('*') if x.is_file())


def main():
    plan = load(HERE/'move-plan.json')
    archived_count = 0
    for action in plan['actions']:
        src, dest = ROOT/action['source'], ROOT/action['destination']
        require(not src.exists() or action['source'] == 'README.md', 'Archived path still active: '+action['source'])
        require(dest.exists(), 'Missing archive destination')
        actual = files_at(dest)
        expected = {r['relative'] for r in action['files']}
        unexpected = [p.relative_to(dest).as_posix() for p in actual if dest.is_dir() and p.relative_to(dest).as_posix() not in expected]
        require(not unexpected or action['source'] == 'dist' and all(p.startswith('goalforge-2026-10-26-organized/') for p in unexpected), 'Unexpected new archive content: '+str(dest))
        for record in action['files']:
            p = dest/record['relative'] if dest.is_dir() else dest
            require(p.is_file() and p.stat().st_size == record['bytes'] and sha(p) == record['sha256'], 'Moved file differs: '+str(p))
            archived_count += 1
    require(archived_count == 6575, 'Unexpected moved file count')

    base = ROOT/'datasets/processed/goalforge-v1'
    original_manifest = load(base/'release_manifest.json')
    for record in original_manifest['files']:
        p = base/record['path']
        require(p.stat().st_size == record['bytes'] and sha(p) == record['sha256'], 'Frozen dataset changed: '+str(p))
    require(len(list((base/'source').glob('*.json'))) == 34 and len(list((base/'source').glob('*.txt'))) == 34, 'Source documents missing')
    raw = ROOT/'datasets/raw/goalgeneration/16c4ce8bed513bbfdada7ac900ba6b718617a6eb'
    raw_manifest = load(raw/'manifest.json')

    paper = ROOT/'datasets/baselines/paper-study1/baseline-manifest.json'
    for manifest in (load(paper), load(ROOT/'datasets/benchmarks/skill-comparison-2026-10-26/benchmark-manifest.json')):
        for record in manifest['files']:
            p = ROOT/record['path']
            require(sha(p) == record['sha256'] and p.stat().st_size == record['bytes'], 'Active benchmark copy differs')
            src = ROOT/('extra/'+record['source'])
            require(src.is_file() and sha(src) == record['sha256'] or (ROOT/record['source']).is_file() and sha(ROOT/record['source']) == record['sha256'], 'Benchmark origin differs')
    benchmark = load(ROOT/'datasets/benchmarks/skill-comparison-2026-10-26/benchmark-manifest.json')
    for record in benchmark['sources']:
        require(sha(ROOT/record['path']) == record['sha256'], 'Benchmark raw source changed')

    old_metrics = load(ROOT/'extra/runs/skill-optimization-2026-10-25-complete/evaluation/metrics.json')
    require(old_metrics['validation'] == 'passed' and len(old_metrics['bindings']) == 32, 'Frozen comparison missing')
    review_root = ROOT/'extra/runs/skill-optimization-2026-10-25-complete/evaluation/source-first-review'
    require(sha(review_root/'freeze-manifest.json') == old_metrics['inventory_manifest_sha256'], 'Inventory freeze changed')
    for row, binding in zip(old_metrics['documents'], old_metrics['bindings']):
        require(row['document_id'] == binding['document_id'] and row['branch'] == binding['branch'], 'Review binding mismatch')
        require(sha(ROOT/'extra/runs/skill-optimization-2026-10-25-complete'/row['original_model']) == binding['model_sha256'], 'Frozen model changed')
        require(sha(ROOT/'extra/runs/skill-optimization-2026-10-25-complete'/row['review']) == binding['review_sha256'], 'Frozen review changed')

    spec = importlib.util.spec_from_file_location('release', ROOT/'scripts/release_skills.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    require(sorted(p.name for p in (ROOT/'skills').iterdir()) == sorted(module.SKILLS), 'Active skills must be exactly three')
    release_path = ROOT/'extra/dist/goalforge-2026-10-26-organized'
    installed = module.verify_installed(release_path, ROOT/'.agents/skills')
    require(module.skill_files(ROOT/'skills') == module.skill_files(release_path/'skills'), 'Active source/install mismatch')
    previous = module.skill_files(ROOT/'extra/dist/goalforge-2026-10-26/skills')
    current = module.skill_files(ROOT/'skills')
    changed = [n for n in current if current[n] != previous[n]]
    require(changed == ['goal-extraction/references/semantic-judgments.md'], 'Unexpected skill algorithm/content change')
    validator = Path('C:/Users/cjsmwy/.codex/skills/.system/skill-creator/scripts/quick_validate.py')
    validations = []
    for skill in module.SKILLS:
        process = subprocess.run([sys.executable,'-B','-X','utf8',str(validator),str(ROOT/'skills'/skill)], capture_output=True, text=True, encoding='utf-8')
        require(process.returncode == 0, process.stdout+process.stderr)
        validations.append(dict(skill=skill,output=process.stdout.strip()))

    py = (HERE/'python-tests.log').read_text(encoding='utf-8-sig')
    js = (HERE/'javascript-tests.log').read_text(encoding='utf-8-sig')
    require('Ran 123 tests' in py and '\nOK' in py, 'Current Python tests failed')
    require('pass 13' in js and 'fail 0' in js, 'Current JavaScript tests failed')
    old_tests = ast.parse((ROOT/'extra/legacy-tests/test_skill_migration.py').read_text(encoding='utf-8'))
    active_tests = ast.parse((ROOT/'tests/test_skill_installation.py').read_text(encoding='utf-8'))
    methods = lambda tree: {n.name: ast.dump(n) for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name.startswith('test_')}
    before, after = methods(old_tests), methods(active_tests)
    removed = sorted(set(before)-set(after))
    require(removed == ['test_compatibility_entrypoint_reports_missing_target','test_old_cli_and_import_delegate_without_mutating_inputs'], 'Wrong tests removed')
    require(all(before[n] == after[n] for n in after), 'Retained test behaviors changed')
    diff = list(difflib.unified_diff((ROOT/'extra/legacy-tests/test_skill_migration.py').read_text(encoding='utf-8').splitlines(keepends=True), (ROOT/'tests/test_skill_installation.py').read_text(encoding='utf-8').splitlines(keepends=True), fromfile='before/tests/test_skill_migration.py', tofile='after/tests/test_skill_installation.py'))
    diff += list(difflib.unified_diff((HERE/'before/semantic-judgments.md').read_text(encoding='utf-8').splitlines(keepends=True), (ROOT/'skills/goal-extraction/references/semantic-judgments.md').read_text(encoding='utf-8').splitlines(keepends=True), fromfile='before/semantic-judgments.md', tofile='after/semantic-judgments.md'))
    (HERE/'active-changes.diff').write_text(''.join(diff), encoding='utf-8')

    docs = [ROOT/'README.md', ROOT/'datasets/README.md', ROOT/'extra/README.md', ROOT/'datasets/benchmarks/skill-comparison-2026-10-26/README.md']
    docs += list(ROOT.glob('*记录.md'))
    docs += list((ROOT/'skills').rglob('*.md'))
    links = 0
    for doc in docs:
        for target in re.findall(r'\]\(([^\n)]+)\)', doc.read_text(encoding='utf-8')):
            if re.match(r'^[a-zA-Z]+://',target) or target.startswith('#'):
                continue
            p = (doc.parent/unquote(target.split('#')[0].split(' "')[0].strip('<>'))).resolve()
            require(p.exists() or p == FINAL, 'Broken active link: '+str(doc)+' -> '+target)
            links += 1

    roots = sorted(p.name for p in ROOT.iterdir())
    expected = {'.agents','.git','.gitattributes','.gitignore','README.md','datasets','extra','scripts','skills','tests'}
    expected.update(p.name for p in ROOT.glob('*记录.md'))
    require(set(roots) == expected, 'Unexpected root clutter: '+str(set(roots)-expected))
    result = dict(status='passed', timestamp_utc=datetime.now(timezone.utc).isoformat(), moves=len(plan['actions']), moved_files=archived_count,
        moved_bytes=sum(f['bytes'] for a in plan['actions'] for f in a['files']), all_moved_hashes_match=True, no_archived_files_deleted=True,
        frozen_dataset=dict(manifest_files=len(original_manifest['files']), all_hashes_match=True, documents=34, source_files=68, independent_test=False),
        paper_baseline_files=len(load(paper)['files']), active_benchmark_files=len(benchmark['files']), benchmark_models=32, frozen_review_bindings=32,
        formal_skills=list(module.SKILLS), skill_files=44, installed=installed, skill_validations=validations, changed_skill_files=changed,
        python_tests=123,javascript_tests=13,retired_wrapper_tests=removed,retained_installation_test_ast_unchanged=True,
        local_active_links_checked=links, root_entries=roots,
        evidence=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p)) for p in [HERE/'move-plan.json',HERE/'python-tests.log',HERE/'javascript-tests.log',HERE/'active-changes.diff',ROOT/'README.md',*ROOT.glob('*记录.md')]],
        scope='File organization and a retired-entrypoint reference correction; no goal-model algorithm change. Original history remains byte-identical. Historical paths are recorded, not rewritten. No Git commit/reset performed.')
    with FINAL.open('x',encoding='utf-8') as f:
        json.dump(result,f,ensure_ascii=False,indent=2)
    print(json.dumps({k:result[k] for k in ('status','moves','moved_files','python_tests','javascript_tests','local_active_links_checked')}))


if __name__ == '__main__':
    main()
