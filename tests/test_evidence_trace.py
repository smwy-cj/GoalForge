import hashlib
import importlib.util
import copy
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("tracing", Path(__file__).resolve().parents[1] / "skills/goal-extraction/scripts/trace_candidates.py")
tracing = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(tracing)


class TracingTests(unittest.TestCase):
    def setUp(self):
        self.canonical = "😀希望及时收到消息。\n"
        self.segment = dict(source_id="D:S1", material_id="M1", text="希望及时收到消息。", recognition_status="native_text",
                            original_locator=dict(start_char=1))
        self.expected = hashlib.sha256(self.canonical.encode("utf-8")).hexdigest()
        self.evidence = dict(source_id="D:S1", quote="及时收到消息", role="basis", start_char=None, end_char=None)

    def test_unicode_full_text_location(self):
        e = tracing.locate(self.evidence, self.segment, self.canonical, self.expected, 1)
        self.assertEqual(e["location_status"], "exact")
        self.assertEqual(self.canonical[e["start_char"]:e["end_char"]], self.evidence["quote"])

    def test_repeated_quote_is_ambiguous(self):
        self.segment["text"] = "通知通知"
        self.evidence["quote"] = "通知"
        e = tracing.locate(self.evidence, self.segment, None, None, 1)
        self.assertEqual(e["location_status"], "ambiguous")
        self.assertEqual(len(e["candidate_locations"]), 2)
        self.assertIsNone(e["start_char"])

    def test_version_mismatch_never_passes(self):
        e = tracing.locate(self.evidence, self.segment, self.canonical, "wrong", 1)
        self.assertEqual(e["source_version_status"], "version_mismatch")
        self.assertNotEqual(e["location_status"], "exact")
        self.assertIsNone(e["start_char"])

    def test_segment_without_full_text_has_no_full_offsets(self):
        e = tracing.locate(self.evidence, self.segment, None, None, 1)
        self.assertEqual(e["location_status"], "exact")
        self.assertEqual(e["verification_scope"], "segment")
        self.assertIsNone(e["start_char"])

    def test_tampered_segment_cannot_pass_against_real_source(self):
        self.segment["text"] = "原文中不存在的目标"
        self.evidence["quote"] = "不存在的目标"
        e = tracing.locate(self.evidence, self.segment, self.canonical, self.expected, 1)
        self.assertEqual(e["location_status"], "not_found")

    def test_missing_and_changed_quotes(self):
        self.assertEqual(tracing.locate(self.evidence, None, None, None, 1)["location_status"], "source_unavailable")
        self.evidence["quote"] = "两秒内收到消息"
        self.assertEqual(tracing.locate(self.evidence, self.segment, None, None, 1)["location_status"], "not_found")

    def test_exact_match_does_not_automatically_mean_direct(self):
        c = dict(candidate_id="D-C1", category="goal", statement="两秒内收到消息", origin="explicit", evidence_candidates=[self.evidence])
        data = dict(document_id="D", document_hash=self.expected, candidates=[c], segments=[self.segment])
        out = tracing.trace(data, canonical=self.canonical)
        self.assertEqual(out["traces"][0]["submitted_evidence"][0]["location_status"], "exact")
        self.assertEqual(out["status"], "partial")
        self.assertEqual(out["traces"][0]["support"]["label"], "insufficient")
        self.assertIn("semantic_not_run", [i["code"] for i in out["traces"][0]["issues"]])

    def test_supplied_semantic_judgment_does_not_change_target(self):
        c = dict(candidate_id="D-C1", category="goal", statement="两秒内收到消息", origin="explicit", evidence_candidates=[self.evidence])
        data = dict(document_id="D", document_hash=self.expected, candidates=[c], segments=[self.segment])
        judgment = dict(label="insufficient", rationale="原文未给两秒阈值。", unsupported_parts=["两秒"])
        bundle = tracing.judgment_template(data)
        bundle["judgments"]["D-C1"].update(judgment)
        out = tracing.trace(data, bundle, self.canonical)
        self.assertEqual(out["traces"][0]["statement"], c["statement"])
        self.assertEqual(out["traces"][0]["support"]["unsupported_parts"], ["两秒"])

    def test_old_flat_judgments_and_changed_input_rejected(self):
        c = dict(candidate_id="D-C1", category="goal", statement="收到消息", origin="explicit", evidence_candidates=[self.evidence])
        data = dict(document_id="D", document_hash=self.expected, candidates=[c], segments=[self.segment])
        with self.assertRaisesRegex(ValueError, "Version-bound"):
            tracing.trace(data, {"D-C1": dict(label="direct", rationale="旧判断")}, self.canonical)
        bundle = tracing.judgment_template(data)
        bundle["judgments"]["D-C1"].update(label="direct", rationale="本版本原文直接表达。")
        changed = copy.deepcopy(data)
        changed["candidates"][0]["statement"] += "且两秒内完成"
        with self.assertRaisesRegex(ValueError, "version/hash"):
            tracing.trace(changed, bundle, self.canonical)

    def test_target_statement_and_actual_input_file_binding_required(self):
        c = dict(candidate_id="D-C1", category="goal", statement="收到消息", origin="explicit", evidence_candidates=[self.evidence])
        data = dict(document_id="D", document_hash=self.expected, candidates=[c], segments=[self.segment])
        bundle = tracing.judgment_template(data, b"exact input bytes")
        bundle["judgments"]["D-C1"].update(label="direct", rationale="当前输入判断。")
        with self.assertRaisesRegex(ValueError, "version/hash"):
            tracing.trace(data, bundle, self.canonical, "another-file-sha")
        bundle["judgments"]["D-C1"]["target_statement"] = "旧表述"
        with self.assertRaisesRegex(ValueError, "statement"):
            tracing.trace(data, bundle, self.canonical, tracing.sha(b"exact input bytes"))


if __name__ == "__main__":
    unittest.main()
