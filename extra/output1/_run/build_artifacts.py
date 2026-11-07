"""Assemble human/model-authored decisions using frozen skills; no semantic inference."""
import argparse
import copy
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]


def raw_json(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8')


def load(path):
    return json.loads(Path(path).read_bytes().decode('utf-8-sig'))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def write(path, value):
    with Path(path).open('xb') as f:
        f.write(raw_json(value))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('authoring', type=Path)
    parser.add_argument('--arm', choices=['baseline', 'revised'], default='revised')
    parser.add_argument('--revision', default='v1')
    args = parser.parse_args()
    author = load(args.authoring)
    doc = author['document_id']
    assert doc in load(OUT/'_run/run-config.json')['all_documents'], 'Unknown document'
    assert args.revision.replace('-', '').replace('_', '').isalnum(), 'Unsafe revision name'
    source_dir = OUT/'_inputs'/doc
    source = (source_dir/'source.txt').read_bytes()
    text = source.decode('utf-8')
    data = load(source_dir/'source-input.json')
    assert sha(source) == data['document_hash']
    segments = {s['source_id']: s for s in data['segments']}

    def evidence(item):
        sid = item['source_id']
        segment = segments[sid]
        quote = item['quote']
        assert isinstance(quote, str) and quote, 'Empty quote'
        starts = [i for i in range(len(segment['text'])) if segment['text'].startswith(quote, i)]
        if 'segment_offset' in item:
            offset = item['segment_offset']
            assert offset in starts, 'Invalid explicit quote location'
        else:
            assert len(starts) == 1, f'Quote must occur exactly once in {sid}: {quote!r}'
            offset = starts[0]
        start = segment['original_locator']['start_char'] + offset
        assert text[start:start+len(quote)] == quote
        return dict(source_id=sid, quote=quote, role=item.get('role', 'basis'), start_char=start, end_char=start+len(quote))

    goals = []
    for entry in author['goals']:
        # All semantic fields must be authored explicitly, never inferred here.
        goal = {k: copy.deepcopy(entry[k]) for k in ('candidate_id','statement','origin','actor','context','inference')}
        goal['evidence_candidates'] = [evidence(e) for e in entry['evidence']]
        goal['review_status'] = 'pending'
        goals.append(goal)
        assert entry['support']['label'] in {'direct','inferred','insufficient','contradicted'}
        assert entry['support']['rationale'].strip()
    data.update(schema_version='goalforge-extraction-3', status=author['status'], candidates=goals,
                review_questions=author['review_questions'], limitations=author['limitations'])
    target = OUT/args.arm/doc/args.revision
    target.mkdir(parents=True, exist_ok=False)
    (target/'source.txt').write_bytes(source)
    write(target/'extraction.json', data)
    (target/'authoring.json').write_bytes(args.authoring.read_bytes())
    skill_root = OUT/'_run/skill-snapshots'/args.arm/'skills'
    trace_skill = 'goal-tracing' if args.arm == 'baseline' else 'goal-extraction'
    tracer = skill_root/trace_skill/'scripts/trace_candidates.py'
    builder = skill_root/'goal-model-building/scripts/kaos_model.py'
    commands = []

    def run(script, *parameters):
        command = [sys.executable, '-X', 'utf8', str(script), *(str(p) for p in parameters)]
        result = subprocess.run(command, cwd=str(OUT), capture_output=True, text=True, encoding='utf-8',
                                errors='replace', timeout=60, env=dict(os.environ, PYTHONIOENCODING='utf-8'))
        commands.append(dict(command=command, exit_code=result.returncode, stdout=result.stdout, stderr=result.stderr))
        write(target/('command-' + str(len(commands)).zfill(2) + '.json'), commands[-1])
        if result.returncode:
            raise RuntimeError(result.stdout + result.stderr)

    run(tracer, target/'extraction.json', '--judgment-template', target/'judgment-template.json')
    bundle = load(target/'judgment-template.json')
    for entry in author['goals']:
        bundle['judgments'][entry['candidate_id']].update(copy.deepcopy(entry['support']))
        assert bundle['judgments'][entry['candidate_id']]['target_statement'] == entry['statement']
    write(target/'judgments.json', bundle)
    run(tracer, target/'extraction.json', target/'tracing', '--source', target/'source.txt', '--judgments', target/'judgments.json')
    run(skill_root/'goal-extraction/scripts/render_review.py', target/'extraction.json', target/'goal-candidates.md')
    run(builder, 'template', target/'extraction.json', target/'judgments.json', target/'decision-template.json')
    decisions = load(target/'decision-template.json')
    for group in author['groups']:
        g = {k: copy.deepcopy(group[k]) for k in ('group_id','parent_id','child_ids','kind','status','completeness','rationale','assumptions')}
        g['evidence_ids'] = []
        g['evidence_quotes'] = [evidence(e) for e in group['evidence']]
        decisions['groups'].append(g)
    decisions['questions'] = author['model_questions']
    write(target/'kaos-decisions.json', decisions)
    run(builder, 'assemble', target/'extraction.json', target/'judgments.json', target/'source.txt', target/'kaos-decisions.json', target/'assembled')
    run(builder, 'inspect', target/'assembled/model-input.json', target/'inspection.json')
    run(builder, 'finalize', target/'assembled/model-input.json', target/'inspection.json', target/'delivery')
    (target/'author-review.md').write_bytes(author['author_review'].encode('utf-8'))
    report = load(target/'inspection.json')
    record = dict(document_id=doc, arm=args.arm, revision=args.revision, completed_at_utc=datetime.now(timezone.utc).isoformat(),
                  authoring_sha256=sha(args.authoring.read_bytes()), source_sha256=sha(source),
                  skill_manifest_sha256=sha((skill_root.parent/'manifest.json').read_bytes()),
                  model='inherited agent model; exact identifier unknown', sampling_parameters='unknown', token_budget='unknown',
                  generated_by='model-authored semantic decisions; deterministic assembly', goals=len(goals), groups=len(decisions['groups']),
                  structure=report['structure'], readiness=report['readiness'], independent_semantic=report['independent_semantic'],
                  formal_proof=report['formal_proof'], human=report['human'], commands=commands)
    write(target/'run-record.json', record)
    print(json.dumps({k:record[k] for k in ('document_id','arm','revision','goals','groups','structure','readiness')},ensure_ascii=False))


if __name__ == '__main__':
    main()
