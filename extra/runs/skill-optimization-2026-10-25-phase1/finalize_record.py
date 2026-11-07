"""Freeze changed-file hashes and a reviewable diff against the pre-edit snapshot."""
import difflib
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]
RUN = Path(__file__).resolve().parent


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    changes, diff, broken = [], [], []
    files = [(path, RUN / 'before' / path.relative_to(ROOT)) for path in (ROOT / 'skills').rglob('*')
             if path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc']
    files += [(ROOT / 'tests' / name, RUN / 'before' / name)
              for name in ('test_goal_extraction_source.py', 'test_extraction_coverage.py')]
    files += [(ROOT / 'docs' / name, RUN / 'before' / name)
              for name in ('17-借鉴论文的Skills优化方案.md', '18-论文方法优化第一阶段实施记录.md')]
    for path, baseline in sorted(files):
        old = baseline.read_bytes() if baseline.exists() else b''
        new = path.read_bytes()
        if old == new:
            continue
        relative = path.relative_to(ROOT).as_posix()
        changes.append(dict(path=relative, status='modified' if baseline.exists() else 'added',
                            before_sha256=sha(old) if baseline.exists() else None, after_sha256=sha(new)))
        text = new.decode('utf-8-sig')
        diff.extend(difflib.unified_diff(old.decode('utf-8-sig').splitlines(True), text.splitlines(True),
                                         fromfile='before/' + relative, tofile='after/' + relative))
        if path.suffix == '.md':
            for target in re.findall(r'\]\(([^)]+)\)', text):
                if '://' in target or target.startswith('#'):
                    continue
                resolved = path.parent / unquote(target.split('#', 1)[0])
                if not resolved.exists():
                    broken.append(dict(file=relative, target=target))
    assert not broken, broken
    result = dict(scope='phase1 repository implementation; no installation or real extraction experiment',
                  changes=changes, local_markdown_links='passed',
                  validation=dict(python_full_suite=dict(tests=110, sandbox_passed=109,
                      sandbox_errors=1, error='Existing loopback save test: WinError 10013',
                      isolated_loopback_rerun='passed outside restricted sandbox', aggregate='110 distinct tests passed across two runs'),
                      skill_validation=dict(skills=3, status='passed with python -X utf8'),
                      real_source_checks=dict(documents=8, status='passed', record='source-verification.json'),
                      semantic_generation='not_run', independent_semantic='not_run', installation='not_run'))
    with (RUN / 'changes.diff').open('x', encoding='utf-8', newline='\n') as handle:
        handle.write(''.join(diff))
    with (RUN / 'verification.json').open('x', encoding='utf-8', newline='\n') as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2)
        handle.write('\n')
    print(json.dumps(dict(changed_files=len(changes), local_links='passed', files=[c['path'] for c in changes]), ensure_ascii=False))


if __name__ == '__main__':
    main()
