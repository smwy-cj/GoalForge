"""Download immutable public paper artifacts into this comparison's inputs."""
from pathlib import Path
import hashlib
import json
import urllib.request
import urllib.parse

COMMIT = '16c4ce8bed513bbfdada7ac900ba6b718617a6eb'
DEST = Path(__file__).resolve().parent / 'inputs' / 'paper'
FILES = [
    'README.md', 'study1/data1/summarized.json', 'study1/data1/sampled-goals.json',
    'study1/data1/graphs.json', 'study1/data1/models.json',
    'study1/data1/extracted-goals.json', 'study1/data1/comps_final.csv',
    'study1/data1/comps_unlabeled.csv',
    'study1/3. Cluster Goals from Repeated Sampling.ipynb',
    'study1/4. Build Goal Refinement Graph.ipynb',
    'study1/5. Extract Goal Graph from Python Code.ipynb',
    'study1/RQ3 - Evaluate Refinement Relations.ipynb',
]

def main():
    records = []
    for name in FILES:
        path = DEST / name
        url = 'https://raw.githubusercontent.com/cmu-relab/goalgeneration/' + COMMIT + '/' + urllib.parse.quote(name)
        if not path.exists():
            request = urllib.request.Request(url, headers={'User-Agent': 'GoalForge-Codex-comparison'})
            with urllib.request.urlopen(request, timeout=90) as response:
                content = response.read()
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open('xb') as output:
                output.write(content)
        content = path.read_bytes()
        records.append({'upstream_path': name, 'url': url, 'bytes': len(content),
                        'sha256': hashlib.sha256(content).hexdigest(), 'local_path': str(path)})
        print(name, len(content), flush=True)
    (DEST.parent / 'download-manifest.json').write_text(json.dumps({'commit': COMMIT, 'files': records}, indent=2), encoding='utf-8')

if __name__ == '__main__':
    main()
