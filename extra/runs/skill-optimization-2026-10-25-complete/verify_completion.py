"""Bind final delivery evidence without modifying frozen experiment records."""
import difflib
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUN = Path(__file__).resolve().parent


def load(path):
    return json.loads(path.read_bytes())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    spec = importlib.util.spec_from_file_location('release', ROOT/'scripts/release_skills.py')
    release = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(release)
    installed = release.verify_installed(ROOT/'dist/goalforge-2026-10-26', ROOT/'.agents/skills')
    require(release.skill_files(ROOT/'skills') == release.skill_files(ROOT/'dist/goalforge-2026-10-26/skills'), 'Source differs from release')
    require(installed['files'] == 44, 'Unexpected release file count')

    metrics = load(RUN/'evaluation/metrics.json')
    inventory_root = RUN/'evaluation/source-first-review'
    freeze_path = inventory_root/'freeze-manifest.json'
    require(sha(freeze_path) == metrics['inventory_manifest_sha256'], 'Inventory manifest changed')
    freeze = load(freeze_path)
    for item in freeze['inventories']:
        require(sha(inventory_root/item['inventory_path']) == item['inventory_sha256'], 'Source inventory changed')
    bindings = {(b['document_id'], b['branch']): b for b in metrics['bindings']}
    reviewed = dict(samples=0, intents=0, goals=0, relations=0, groups=0)
    for round_name in ('first', 'repeat'):
        mapping = load(RUN/'evaluation'/('blinding-map-'+round_name+'.json'))
        require(mapping['inventory_manifest_sha256'] == sha(freeze_path), 'Packet freeze mismatch')
        validation = load(inventory_root/('validation-'+round_name+'.json'))
        require(validation['status'] == 'pass' and validation['human_gold'] is False, 'Review validation failed')
        for item in mapping['records']:
            b = bindings[item['document_id'], item['branch']]
            require(sha(RUN/item['source_model']) == item['source_sha256'] == b['model_sha256'], 'Frozen model changed')
            require(sha(RUN/item['anonymous']) == item['anonymous_sha256'] == b['anonymous_sha256'], 'Frozen anonymous packet changed')
            review_path = inventory_root/item['document_id']/('review-'+round_name+'.json')
            require(sha(review_path) == b['review_sha256'], 'Frozen review changed')
            samples = load(review_path)['samples']
            sample = next(s for s in samples if s['sample'] == round_name+':'+item['label'])
            reviewed['samples'] += 1
            for key, field in [('intents','intent_matches'), ('goals','goal_assessments'), ('relations','relation_assessments'), ('groups','group_assessments')]:
                reviewed[key] += len(sample[field])
    require(reviewed == dict(samples=32, intents=516, goals=683, relations=193, groups=45), 'Review counts differ')

    py = (RUN/'python-tests-release.log').read_text(encoding='utf-8-sig')
    js = (RUN/'javascript-tests-release.log').read_text(encoding='utf-8-sig')
    require('Ran 125 tests' in py and '\nOK' in py, 'Python test log failed')
    require('pass 13' in js and 'fail 0' in js, 'JavaScript test log failed')
    validator = Path('C:/Users/cjsmwy/.codex/skills/.system/skill-creator/scripts/quick_validate.py')
    structure = []
    for name in release.SKILLS:
        process = subprocess.run([sys.executable, '-B', '-X', 'utf8', str(validator), str(ROOT/'skills'/name)], capture_output=True, text=True, encoding='utf-8')
        require(process.returncode == 0, process.stdout+process.stderr)
        structure.append(dict(skill=name, output=process.stdout.strip()))
    browser = load(RUN/'browser-verification.json')
    browser_checks = sum(len(r['checks']) for r in browser['runs'])
    require(browser['status'] == 'passed' and browser_checks == 19, 'Browser checks failed')
    legacy = load(RUN/'legacy-compatibility.json')
    require(legacy['passed'] == 34 and all(d['structure'] == 'passed' and d['originals_unchanged'] for d in legacy['documents']), 'Legacy compatibility failed')
    fixed = load(RUN/'fixed-goal-modeling.json')
    require(fixed['status'] == 'passed' and len(fixed['documents']) == 8, 'Fixed-goal comparison failed')
    isolated = load(RUN/'isolated-release-workflow-2/verification.json')
    require(isolated['status'] == 'passed' and isolated['commands'] == 15, 'Installed workflow failed')

    report = next((ROOT/'docs').glob('19-*.md'))
    docs = [ROOT/'README.md']
    for prefix in ('03-', '05-', '06-', '07-', '10-', '17-', '19-'):
        docs.append(next((ROOT/'docs').glob(prefix+'*.md')))
    links = 0
    for doc in docs:
        for target in re.findall(r'\]\(([^\n)]+)\)', doc.read_text(encoding='utf-8')):
            if re.match(r'^[a-zA-Z]+://', target) or target.startswith('#'):
                continue
            target = target.split('#')[0].split(' "')[0].strip('<>')
            from urllib.parse import unquote
            require((doc.parent/unquote(target)).exists(), 'Broken local link: '+str(doc)+' -> '+target)
            links += 1

    before = RUN/'before'
    names = {'README.md', 'scripts/release_skills.py'}
    for tree in ('skills', 'tests', 'docs'):
        for base in (before, ROOT):
            names.update(p.relative_to(base).as_posix() for p in (base/tree).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc')
    changes = []
    diff = []
    for name in sorted(names):
        old, new = before/name, ROOT/name
        old_raw = old.read_bytes() if old.exists() else b''
        new_raw = new.read_bytes() if new.exists() else b''
        if old_raw == new_raw:
            continue
        changes.append(dict(path=name, change='modified' if old.exists() and new.exists() else 'added' if new.exists() else 'removed', before_sha256=sha(old) if old.exists() else None, after_sha256=sha(new) if new.exists() else None))
        diff.extend(difflib.unified_diff(old_raw.decode('utf-8-sig').splitlines(keepends=True), new_raw.decode('utf-8-sig').splitlines(keepends=True), fromfile='before/'+name, tofile='after/'+name))
    with (RUN/'changes.diff').open('x', encoding='utf-8', newline='\n') as handle:
        handle.write(''.join(diff))
    with (RUN/'changes.json').open('x', encoding='utf-8') as handle:
        json.dump(dict(scope='Current complete-phase snapshot; phase-1 and atomic-action changes have separate historical records. release_skills.py is newly added in this phase.', files=changes), handle, indent=2)

    evidence_paths = ['python-tests-release.log', 'javascript-tests-release.log', 'browser-verification.json', 'legacy-compatibility.json', 'fixed-goal-modeling.json', 'isolated-release-workflow-2/verification.json', 'project-install-receipt.json', 'evaluation/metrics.json', 'evaluation/generation-snapshot.json', 'evaluation/source-first-review/review-summary.json', 'changes.json', 'changes.diff']
    result = dict(status='passed', completed_at_utc=datetime.now(timezone.utc).isoformat(), phases=[1,2,3], release=installed,
        python_tests=125, javascript_tests=13, skill_structure=structure, browser_checks=browser_checks, legacy_models=34, fixed_goal_documents=8, deterministic_rebuilds_each=3, installed_workflow_commands=15,
        frozen_review=reviewed, inventory_manifest_sha256=sha(freeze_path), reviewed_hash_bindings=32, local_document_links=links, changed_files=len(changes),
        report=dict(path=report.relative_to(ROOT).as_posix(), sha256=sha(report)),
        evidence=[dict(path=p, sha256=sha(RUN/p)) for p in evidence_paths],
        limits=metrics['limitations']+['Final generic semantic rule corrections followed frozen development evaluation; no post-correction blind-test claim.', 'Synthetic feedback is engineer-authored; human acceptance remains pending. Application discovery/hot reload is not asserted.'],
        preserved_attempts=['Initial sandbox loopback/browser restrictions; browser harness selector repair.', 'Candidate DOC036 invalid question target repaired in new assembly; original failed records retained.', 'Installed workflow relative-output harness failure retained; corrected runner passed in a fresh directory.', 'Page placeholder collision proof retained; production fix covered by v1/v2 regression tests.'])
    with (RUN/'verification.json').open('x', encoding='utf-8') as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2)
    print(json.dumps(dict(status=result['status'], files=installed['files'], reviewed=reviewed, changed_files=len(changes), local_links=links)))


if __name__ == '__main__':
    main()
