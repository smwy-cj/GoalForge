"""Read-only source round-trip check; not an extraction or semantic experiment."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUN = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'skills/goal-extraction/scripts'))
from prepare_source import digest, encode
from check_coverage import source_inputs


def main():
    rows = []
    for doc in ('DOC003', 'DOC010', 'DOC013', 'DOC020', 'DOC023', 'DOC031', 'DOC028', 'DOC036'):
        original = ROOT / 'datasets/processed/goalforge-v1/source' / (doc + '.json')
        canonical = original.with_suffix('.txt')
        originals = {p: p.read_bytes() for p in (original, canonical)}
        output = RUN / 'source-checks' / doc
        command = [sys.executable, '-X', 'utf8', str(ROOT / 'skills/goal-extraction/scripts/prepare_source.py'),
                   str(original), str(output), '--canonical-text', str(canonical), '--window-size', '4', '--window-stride', '2']
        result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', timeout=30)
        if result.returncode:
            raise RuntimeError(result.stdout + result.stderr)
        raws = {k: (output / v).read_bytes() for k, v in dict(source='source.txt', source_input='source-input.json', windows='source-windows.json').items()}
        data, text = source_inputs(raws)
        assert raws['source'] == originals[canonical]
        assert all(p.read_bytes() == raw for p, raw in originals.items())
        seen = {sid for w in data['windows']['windows'] for sid in w['source_ids']}
        assert seen == {s['source_id'] for s in data['source_input']['segments']}
        assert data['windows']['parameters']['unit'] == 'turn'
        for window in data['windows']['windows']:
            for segment in window['segments']:
                assert text[segment['start_char']:segment['end_char']] == segment['text']
                assert window['text'][segment['window_start_char']:segment['window_end_char']] == segment['text']
        rows.append(dict(document_id=doc, source_sha256=digest(raws['source']),
                         turns=len(seen), windows=len(data['windows']['windows']),
                         original_unchanged=True, canonical_byte_identical=True,
                         all_turns_covered=True, all_offsets_exact=True))
    output = RUN / 'source-verification.json'
    with output.open('xb') as handle:
        handle.write(encode(dict(scope='deterministic source/window check only', documents=rows,
                                 semantic_extraction='not_run', independent_review='not_run')))
    print(json.dumps(rows, ensure_ascii=False))


if __name__ == '__main__':
    main()
