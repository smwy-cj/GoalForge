import json
import struct
import sys
import zlib
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

root = Path(__file__).resolve().parents[2]
data = (root / '第10章.模型驱动方法.ppt').read_bytes()
u32 = lambda b, p: struct.unpack_from('<I', b, p)[0]
sector_size = 1 << struct.unpack_from('<H', data, 30)[0]
sector = lambda n: data[(n + 1) * sector_size:(n + 2) * sector_size]
fat_sectors = list(struct.unpack_from('<109I', data, 76))
next_difat = u32(data, 68)
for _ in range(u32(data, 72)):
    block = sector(next_difat)
    fat_sectors.extend(struct.unpack_from('<%dI' % (sector_size // 4 - 1), block))
    next_difat = u32(block, sector_size - 4)
fat = []
for n in fat_sectors:
    if n < 0xfffffffa:
        fat.extend(struct.unpack('<%dI' % (sector_size // 4), sector(n)))

def chain(start):
    chunks, seen = [], set()
    while start < 0xfffffffa:
        if start in seen:
            raise ValueError('Cyclic stream')
        seen.add(start)
        chunks.append(sector(start))
        start = fat[start]
    return b''.join(chunks)

directory = chain(u32(data, 48))
entries = []
for p in range(0, len(directory), 128):
    e = directory[p:p + 128]
    if len(e) != 128 or e[66] == 0:
        continue
    name_len = struct.unpack_from('<H', e, 64)[0]
    name = e[:name_len - 2].decode('utf-16le')
    entries.append((name, u32(e, 116), struct.unpack_from('<Q', e, 120)[0]))
print('Streams:', entries)
name, start, length = next(e for e in entries if e[0] == 'PowerPoint Document')
assert length >= 4096
stream = chain(start)[:length]

def records(blob, lo=0, hi=None, path=()):
    hi = len(blob) if hi is None else hi
    p = lo
    while p + 8 <= hi:
        vi, kind, size = struct.unpack_from('<HHI', blob, p)
        end = p + 8 + size
        if end > hi:
            break
        payload = blob[p + 8:end]
        yield p, kind, vi >> 4, payload, path
        if vi & 15 == 15:
            yield from records(blob, p + 8, end, path + ((kind, p, vi >> 4),))
        p = end

texts = []
for p, kind, instance, payload, path in records(stream):
    if kind in (4000, 4008):
        text = payload.decode('utf-16le' if kind == 4000 else 'cp1252', errors='replace')
        texts.append({'offset': p, 'path': path, 'text': text})
    elif kind == 1011:
        texts.append({'offset': p, 'path': path, 'slide_persist': list(struct.unpack('<%dI' % (len(payload)//4), payload))})
out = Path(__file__).parent / 'ppt-text-records.json'
out.write_text(json.dumps(texts, ensure_ascii=False, indent=2), encoding='utf-8')
persist_offsets = {}
for p, kind, instance, payload, path in records(stream):
    if kind == 6002:
        at = 0
        while at < len(payload):
            head = u32(payload, at)
            start_id, count = head & 0xfffff, head >> 20
            at += 4
            for index in range(count):
                persist_offsets[start_id + index] = u32(payload, at)
                at += 4
slides = []
for t in texts:
    if 'slide_persist' not in t or t['path'][-1][2] != 0:
        continue
    slide_offset = persist_offsets[t['slide_persist'][0]]
    contents = [x['text'] for x in texts if 'text' in x and any(a[0] == 1006 and a[1] == slide_offset for a in x['path'])]
    slides.append({'slide': len(slides) + 1, 'offset': slide_offset, 'text': '\n'.join(contents)})
(out.parent / 'ppt-slides.json').write_text(json.dumps(slides, ensure_ascii=False, indent=2), encoding='utf-8')
image_dir = out.parent / 'ppt-images'
image_dir.mkdir(exist_ok=True)
for name, start, length in entries:
    if name != 'Pictures':
        continue
    for index, (p, kind, instance, payload, path) in enumerate(records(chain(start)[:length]), 1):
        if kind == 0xf01e:
            at = payload.find(b'\x89PNG\r\n\x1a\n')
            assert at >= 0
            (image_dir / ('image-%02d.png' % index)).write_bytes(payload[at:])
        elif kind in (0xf01a, 0xf01b):
            raw = zlib.decompress(payload[50:])
            (image_dir / ('image-%02d.%s' % (index, 'emf' if kind == 0xf01a else 'wmf'))).write_bytes(raw)
print('Slides:', len(slides))
print('Text records:', sum('text' in t for t in texts))
for item in texts:
    if 'text' in item:
        print(item['offset'], item['text'].replace('\r', '\n'))
    else:
        print('SLIDE', item['slide_persist'])
