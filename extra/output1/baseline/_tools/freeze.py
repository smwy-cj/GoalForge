"""Record existing v1 artifact hashes; no semantic authoring."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

base = Path(__file__).resolve().parents[1]
files = []
for doc in ('DOC010', 'DOC023', 'DOC031'):
    for p in sorted((base / doc / 'v1').rglob('*')):
        if p.is_file():
            files.append(dict(path=p.relative_to(base).as_posix(), sha256=hashlib.sha256(p.read_bytes()).hexdigest(), bytes=p.stat().st_size))
manifest = dict(schema_version='goalforge-baseline-freeze-1', frozen_utc=datetime.now(timezone.utc).isoformat(),
                note='三篇首次生成v1冻结；未使用其他分支或外部复核反馈改写。', files=files)
with (base / 'freeze-manifest.json').open('x', encoding='utf-8', newline='\n') as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)
    f.write('\n')
print('Frozen files:', len(files))
