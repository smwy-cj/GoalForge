"""Synthetic dual-output checks; not a model extraction benchmark."""

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("review", ROOT / "skills/goal-extraction/scripts/render_review.py")
review = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(review)


def sample():
    texts = ["我希望队友立刻看到最新文档。", "我每小时手动刷新。", "小窗口下按钮看不清。", "我更喜欢深色界面。", "夜间不要推送提醒。"]
    categories = ["goal", "action", "obstacle", "preference", "goal"]
    subtypes = ["maintenance", "interaction", "difficulty", "experience", "avoidance"]
    segments, candidates = [], []
    for i, text in enumerate(texts, 1):
        sid = f"SYN001:S{i:03}"
        segments.append(dict(source_id=sid, material_id="M001", text=text, speaker="用户",
                             original_locator={"paragraph": i}, recognition_status="native_text"))
        category = categories[i - 1]
        candidates.append(dict(candidate_id=f"SYN001-C{i:03}", category=category, subtype=subtypes[i - 1],
                               statement=text, origin="explicit" if category == "goal" else None,
                               actor="用户", context=["夜间"] if i == 5 else [],
                               evidence_candidates=[dict(source_id=sid, quote=text, role="basis", start_char=None, end_char=None)],
                               classification_reason="基于合成语句的结果、步骤或体验性质判断。", inference=None, review_status="pending"))
    candidates.append(dict(candidate_id="SYN001-C006", category="goal", subtype="quality",
                           statement="在小窗口下看清操作按钮", origin="inferred", actor="用户", context=["小窗口"],
                           evidence_candidates=[dict(source_id="SYN001:S003", quote=texts[2], role="basis", start_char=None, end_char=None)],
                           classification_reason="从可读性障碍推断期望质量，不指定实现方案。",
                           inference=dict(basis_candidate_ids=["SYN001-C003"], reason="按钮不可读构成使用障碍。", assumptions=["用户希望改善该可读性问题。"]), review_status="pending"))
    return dict(schema_version="goalforge-extraction-draft-2", document_id="SYN001", document_hash=None, status="completed",
                materials=[dict(material_id="M001", file_name="合成访谈.md", media_type="text/markdown", original_hash=None, id_origin="generated", processing_status="processed")],
                conversion=dict(canonical_text_path="source.md", method="合成文本按段落原样登记", issues=[]), segments=segments,
                coverage=dict(scope="provided_material", source_ids=[s["source_id"] for s in segments], omissions=[]), candidates=candidates,
                review_questions=[dict(candidate_ids=["SYN001-C006"], question="是否希望改善小窗口下按钮可读性？", reason="该项为推断而非直接诉求。")], limitations=["合成案例，不代表真实访谈提取效果。"])


class ReviewTests(unittest.TestCase):
    def test_cli_refuses_to_overwrite_handwritten_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, output = Path(tmp) / "extraction.json", Path(tmp) / "review.md"
            source.write_text(json.dumps(sample(), ensure_ascii=False), encoding="utf-8")
            original = "人工意见：保留否定条件。\n".encode("utf-8")
            output.write_bytes(original)
            result = subprocess.run([sys.executable, str(ROOT / "skills/goal-extraction/scripts/render_review.py"), str(source), str(output)], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(output.read_bytes(), original)

    def test_all_candidates_evidence_and_assumptions_visible(self):
        data = sample()
        before = copy.deepcopy(data)
        output = review.render(data)
        self.assertEqual(before, data)
        for c in data["candidates"]:
            self.assertIn(c["candidate_id"], output)
            self.assertIn(c["statement"], output)
            for e in c["evidence_candidates"]:
                self.assertIn(e["quote"], output)
        self.assertIn(data["candidates"][-1]["inference"]["assumptions"][0], output)
        self.assertEqual(output.count("审核意见："), len(data["candidates"]))

    def test_unknown_source_rejected(self):
        data = sample()
        data["candidates"][0]["evidence_candidates"][0]["source_id"] = "missing"
        with self.assertRaises(ValueError):
            review.render(data)

    def test_fabricated_quote_rejected(self):
        data = sample()
        data["candidates"][0]["evidence_candidates"][0]["quote"] = "原文没有这句话"
        with self.assertRaises(ValueError):
            review.render(data)

    def test_duplicate_id_rejected(self):
        data = sample()
        data["candidates"].append(copy.deepcopy(data["candidates"][0]))
        with self.assertRaises(ValueError):
            review.render(data)

    def test_human_confirmation_not_fabricated(self):
        data = sample()
        data["candidates"][0]["review_status"] = "human_confirmed"
        with self.assertRaises(ValueError):
            review.render(data)

    def test_inference_without_reason_rejected(self):
        data = sample()
        data["candidates"][-1]["inference"] = None
        with self.assertRaises(ValueError):
            review.render(data)

    def test_unreadable_audio_still_produces_explanation(self):
        data = sample()
        data.update(status="input_error", candidates=[], segments=[], review_questions=[])
        data["coverage"].update(scope="partial_document", source_ids=[], omissions=["录音未转写"])
        data["conversion"].update(canonical_text_path=None, method="未转换")
        data["materials"][0].update(file_name="访谈.wav", media_type="audio/wav", processing_status="unprocessed")
        data["limitations"] = ["当前测试不具备语音转写工具。"]
        output = review.render(data)
        self.assertIn("无法处理输入", output)
        self.assertIn("录音未转写", output)

    def test_markdown_special_characters_display_as_text(self):
        data = sample()
        data["candidates"][0]["statement"] = "显示 A|B <script> [外链](x)"
        output = review.render(data)
        self.assertNotIn("<script>", output)
        self.assertNotIn("[外链](x)", output)
        self.assertIn("A&#124;B", output)


if __name__ == "__main__":
    unittest.main()
