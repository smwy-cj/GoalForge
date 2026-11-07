"""Source processing invariants using temporary synthetic files."""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("source", Path(__file__).resolve().parents[1] / "skills/goal-extraction/scripts/prepare_source.py")
source = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(source)


class SourceTests(unittest.TestCase):
    def test_native_text_preserves_meaning_and_unicode_offsets(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "材料.md"
            raw = "# 需求😀\r\n\r\n夜间不要通知；阈值为2秒。\r\n".encode("utf-8-sig")
            path.write_bytes(raw)
            canonical, data = source.prepare(path)
            self.assertEqual(path.read_bytes(), raw)
            self.assertEqual(canonical, "# 需求😀\n\n夜间不要通知；阈值为2秒。\n")
            for s in data["segments"]:
                loc = s["original_locator"]
                self.assertEqual(canonical[loc["start_char"]:loc["end_char"]], s["text"])
            self.assertEqual(data["segments"][1]["original_locator"]["line_start"], 3)
            self.assertEqual(source.prepare(path)[1]["document_id"], data["document_id"])

    def test_label_fields_not_forwarded(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "source.json"
            canonical = "[T000] Stakeholder: 希望及时收到消息。\n"
            start = len("[T000] Stakeholder: ")
            record = dict(document_id="TEST001", document_hash=source.digest(canonical.encode("utf-8")),
                          goals=["SHOULD_NOT_LEAK"], turns=[dict(source_id="TEST001:T000", speaker="Stakeholder",
                          turn="0", text="希望及时收到消息。", start_char=start, end_char=len(canonical)-1,
                          goal_annotation="SHOULD_NOT_LEAK")])
            path.write_text(json.dumps(record), encoding="utf-8")
            _, data = source.prepare(path)
            self.assertNotIn("SHOULD_NOT_LEAK", json.dumps(data))
            self.assertEqual(data["segments"][0]["source_id"], "TEST001:T000")
            record["document_hash"] = "bad"
            path.write_text(json.dumps(record), encoding="utf-8")
            with self.assertRaises(ValueError):
                source.prepare(path)

    def test_empty_text_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "empty.txt"
            path.write_text("  \n", encoding="utf-8")
            with self.assertRaises(ValueError):
                source.prepare(path)

    def test_audio_does_not_become_fake_transcript(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "input.wav"
            path.write_bytes(b"not a real transcript")
            with self.assertRaises(ValueError):
                source.prepare(path)

    def test_windows_cover_short_odd_and_even_sources_without_redundant_tail(self):
        for count, expected in [(1, 1), (4, 1), (5, 2), (6, 2), (7, 3)]:
            with self.subTest(count=count), tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / 'source.txt'
                path.write_text('\n'.join(f'片段{i}😀，保持原文。' for i in range(count)), encoding='utf-8')
                canonical, data = source.prepare(path)
                bundle = source.build_windows(data, canonical, 4, 2)
                self.assertEqual(len(bundle['windows']), expected)
                self.assertEqual(bundle['parameters']['unit'], 'segment')
                seen = set()
                for w in bundle['windows']:
                    self.assertEqual(canonical[w['start_char']:w['end_char']], w['text'])
                    for s in w['segments']:
                        seen.add(s['source_id'])
                        self.assertEqual(w['text'][s['window_start_char']:s['window_end_char']], s['text'])
                        self.assertEqual(canonical[s['start_char']:s['end_char']], s['text'])
                self.assertEqual(seen, {s['source_id'] for s in data['segments']})

    def test_windows_reject_gaps_invalid_sizes_and_reordered_segments(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'source.txt'
            path.write_text('第一段\n第二段\n第三段', encoding='utf-8')
            canonical, data = source.prepare(path)
            for size, stride in [(0, 1), (4, 0), (2, 3), (True, 1), (4, 1.5)]:
                with self.subTest(size=size, stride=stride), self.assertRaises(ValueError):
                    source.build_windows(data, canonical, size, stride)
            data['segments'].reverse()
            with self.assertRaises(ValueError):
                source.build_windows(data, canonical)


if __name__ == "__main__":
    unittest.main()
