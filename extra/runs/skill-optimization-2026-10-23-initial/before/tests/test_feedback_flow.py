import copy
import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from test_model_review import fixture, finalizer, reviewer
from test_goal_model_building import exporter
from feedback_contract import validate
from process_feedback import apply, plan, handoff

ROOT = Path(__file__).resolve().parents[1]
TIME = "2026-10-16T08:00:00+00:00"


def packet(model, entries=None, overall="request_changes"):
    return dict(schema_version="goalforge-review-feedback-1", feedback_id="FB-controlled-test", base_model=exporter.feedback_binding(model),
                reviewer=dict(name="受控测试审核人，不是真实用户验收"), created_at=TIME, updated_at=TIME, status="submitted", entries=entries or [], form_drafts={},
                overall=dict(decision=overall, full_scope_ack=overall == "accept", acknowledge_limits=overall == "accept", comment="工程测试"))


def entry(kind, target, decision, proposed=None, eid="ENTRY1"):
    return dict(entry_id=eid, target_type=kind, target_id=target, decision=decision, proposed=proposed or {}, reason="受控测试意见", reviewed_at=TIME)


def ready(folder):
    m = fixture(folder)
    r = reviewer.inspect(m, folder)
    return finalizer.finalize(m, r, folder, Path(folder) / "initial")


def persist(folder, model, attachments):
    folder = Path(folder)
    folder.mkdir(parents=True)
    for relative, data in attachments.items():
        path = folder / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    raw = reviewer.encode(model)
    (folder / "feedback-model.json").write_bytes(raw)
    return reviewer.inspect(model, folder, hashlib.sha256(raw).hexdigest())


class FeedbackTests(unittest.TestCase):
    def test_relation_only_evidence_dispute_invalidates_pair_and_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = ready(tmp)
            e = copy.deepcopy(m["evidence_index"][0])
            e["evidence_id"] = "E-RELATION-ONLY"
            m["evidence_index"].append(e)
            m["pair_decisions"][0]["evidence_ids"] = [e["evidence_id"]]
            p = packet(m, [entry("evidence", e["evidence_id"], "incorrect")])
            result, processing, raw = apply(m, p, Path(tmp) / "initial")
            relation = next(x for x in result["pair_decisions"] if x["pair_id"] == "P12")
            self.assertEqual(relation["trace_status"], "needs_retrace")
            self.assertEqual(relation["assessment_status"], "not_run")
            self.assertEqual(processing["routes"][0]["affected_pair_ids"], ["P12"])
            self.assertEqual(processing["routes"][0]["next_skill"], "goal-model-building")
            self.assertEqual(result["goals"], m["goals"])
            self.assertFalse(any(e["decision_id"] == "P12" for e in result["edges"]))
            report = persist(Path(tmp) / "relation-only", result, raw)
            self.assertEqual(report["summary"]["structure_status"], "failed")
            self.assertNotEqual(result["version"], m["version"])

    def test_malformed_nested_feedback_is_reported_as_invalid(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = ready(tmp)
            p = packet(m, [entry("relation", "P12", "modify", dict(label={}, conditions=[], rationale="test"))])
            self.assertTrue(validate(p, m, submitted=True))
            p["entries"] = [None]
            self.assertTrue(validate(p, m, submitted=True))

    def test_retrace_handoff_preserves_goal_id_and_new_version_binding(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = ready(tmp)
            p = packet(m, [entry("goal", "G1", "modify", dict(statement="改写后的目标"))])
            result, _, raw = apply(m, p, Path(tmp) / "initial")
            source = raw["attachments/source.txt"].decode("utf-8")
            raw["attachments/extraction.json"] = reviewer.encode(dict(schema_version="goalforge-extraction-draft-2", document_id="SYN",
                materials=[], conversion={}, segments=[dict(source_id="SYN:T1", text=source, original_locator=dict(start_char=0), recognition_status="native_text")]))
            tasks, data = handoff(result, raw)
            self.assertEqual(tasks["goal_ids"], ["G1"])
            self.assertEqual(data["candidates"][0]["candidate_id"], "G1")
            self.assertEqual(data["target_model"]["version"], result["version"])
            self.assertEqual(data["target_model"]["core_sha256"], exporter.core_hash(result))

    def test_plan_does_not_mutate_model_or_apply_suggestions(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = ready(tmp)
            p = packet(m, [entry("goal", "G1", "modify", dict(statement="新的建议目标"))])
            before = copy.deepcopy(m)
            result = plan(m, p)
            self.assertFalse(result["model_modified"])
            self.assertEqual(m, before)

    def test_stale_duplicate_unknown_and_incomplete_feedback_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = ready(tmp)
            p = packet(m, [entry("goal", "G1", "accept")])
            for bad in [dict(base_model={}), dict(entries=p["entries"] * 2), dict(entries=[entry("goal", "unknown", "accept")]),
                        dict(entries=[entry("goal", "G1", "modify")]), dict(status="draft"), dict(form_drafts={"goal:G1": {"statement": "未完成"}})]:
                candidate = dict(p, **bad)
                self.assertTrue(validate(candidate, m, submitted=True))

    def test_merge_conflicts_with_another_target_opinion(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = ready(tmp)
            p = packet(m, [entry("goal", "G1", "merge", dict(goal_ids=["G1", "G2"], statement="合并建议")), entry("goal", "G2", "accept", eid="E2")])
            self.assertTrue(validate(p, m, submitted=True))

    def test_goal_edit_invalidates_incident_pairs_and_old_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = ready(tmp)
            original = copy.deepcopy(m)
            p = packet(m, [entry("goal", "G1", "modify", dict(statement="根据天气更灵活地安排活动"))])
            result, processing, raw = apply(m, p, Path(tmp) / "initial")
            self.assertEqual(m, original)
            self.assertNotEqual(result["version"], m["version"])
            self.assertEqual(result["goals"][0]["trace_status"], "needs_retrace")
            self.assertEqual(result["relation_coverage"]["evaluated_pairs"], 1)
            self.assertEqual(len(result["relation_coverage"]["unassessed_pair_ids"]), 2)
            self.assertEqual(result["review"]["status"], "pending")
            self.assertEqual(reviewer.inspect(result)["summary"]["structure_status"], "failed")

    def test_merge_split_exclusion_preserve_lineage_and_actual_coverage(self):
        for decision, proposed, count in [("merge", dict(goal_ids=["G1", "G2"], statement="合并后的目标"), 2),
                                           ("split", dict(statements=["拆分后的目标一", "拆分后的目标二"]), 4), ("exclude", {}, 2)]:
            with self.subTest(decision=decision), tempfile.TemporaryDirectory() as tmp:
                m = ready(tmp)
                if decision == "merge":
                    m["goals"][0].update(context=["条件一"], actor="主体甲")
                    m["goals"][1].update(context=["条件二"], actor="主体乙")
                result, processing, raw = apply(m, packet(m, [entry("goal", "G1", decision, proposed)]), Path(tmp) / "initial")
                self.assertEqual(len(result["goals"]), count)
                self.assertTrue(any(x.get("previous_goal_id") == "G1" for x in result["candidate_goal_mapping"]))
                self.assertEqual(result["relation_coverage"]["expected_pairs"], count * (count - 1) // 2)
                exporter.check_structure(result)
                if decision == "merge":
                    merged = next(g for g in result["goals"] if g["goal_id"] != "G3")
                    self.assertEqual(merged["context"], ["条件一", "条件二"])
                    self.assertIn("主体甲", merged["actor"])
                    self.assertIn("主体乙", merged["actor"])

    def test_missing_goal_uses_selected_evidence_and_pending_new_relations(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = ready(tmp)
            p = packet(m, [entry("model", m["model_id"], "add_goal", dict(statement="用户指出的遗漏目标", evidence_ids=["E1"], origin="inferred"))])
            result, _, _ = apply(m, p, Path(tmp) / "initial")
            self.assertEqual(len(result["goals"]), 4)
            self.assertEqual(len(result["candidate_additions"]), 1)
            self.assertEqual(len(result["relation_coverage"]["unassessed_pair_ids"]), 3)
            self.assertEqual(result["goals"][-1]["evidence_ids"], ["E1"])

    def test_relation_correction_requires_evidence_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = ready(tmp)
            p = packet(m, [entry("relation", "P13", "modify", dict(label="refinement", parent_id="G3", child_id="G1", rationale="用户给出的方向理由", conditions=[]))])
            result, _, _ = apply(m, p, Path(tmp) / "initial")
            relation = next(x for x in result["pair_decisions"] if x["pair_id"] == "P13")
            self.assertEqual(relation["trace_status"], "needs_retrace")
            self.assertTrue(any(e.get("parent_id") == "G3" for e in result["edges"]))

    def test_evidence_dispute_does_not_rewrite_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = ready(tmp)
            p = packet(m, [entry("evidence", "E1", "incorrect")])
            result, _, raw = apply(m, p, Path(tmp) / "initial")
            self.assertEqual(result["evidence_index"], m["evidence_index"])
            self.assertEqual(raw["attachments/source.txt"], (Path(tmp) / "initial/attachments/source.txt").read_bytes())
            self.assertEqual(result["goals"][0]["trace_status"], "needs_retrace")

    def test_explicit_whole_model_approval_bound_to_content_then_finalize(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = ready(tmp)
            p = packet(m, overall="accept")
            result, processing, raw = apply(m, p, Path(tmp) / "initial")
            report = persist(Path(tmp) / "approved", result, raw)
            self.assertEqual(result["version"], m["version"])
            self.assertEqual(exporter.review_target_hash(result), exporter.review_target_hash(m))
            final = finalizer.finalize(result, report, Path(tmp) / "approved", Path(tmp) / "final")
            self.assertEqual(final["review"]["status"], "accepted")
            self.assertEqual(final["delivery"]["readiness"], "accepted")
            self.assertEqual(final["validation"]["semantic_status"], "not_run")
            self.assertEqual(final["goals"], m["goals"])
            altered = copy.deepcopy(result)
            altered["goals"][0]["statement"] += "被改变"
            bad = reviewer.inspect(altered, Path(tmp) / "approved")
            self.assertTrue(any(i["rule_id"] == "human_records" for i in bad["issues"]))

    def test_partial_acceptance_does_not_become_whole_approval_and_double_apply_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = ready(tmp)
            p = packet(m, [entry("goal", "G1", "accept")], overall="undecided")
            result, _, raw = apply(m, p, Path(tmp) / "initial")
            report = persist(Path(tmp) / "partial", result, raw)
            final = finalizer.finalize(result, report, Path(tmp) / "partial", Path(tmp) / "final")
            self.assertEqual(final["review"]["status"], "partial")
            self.assertEqual(final["delivery"]["readiness"], "reviewable")
            with self.assertRaises(ValueError):
                apply(result, p, Path(tmp) / "partial")

    def test_approval_requires_explicit_scope_and_no_unresolved_opinions(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = ready(tmp)
            p = packet(m, overall="accept")
            p["overall"]["full_scope_ack"] = False
            self.assertTrue(validate(p, m, submitted=True))
            p["overall"]["full_scope_ack"] = True
            p["entries"] = [entry("goal", "G1", "defer")]
            self.assertTrue(validate(p, m, submitted=True))

    def test_proposed_cycle_rolls_back_original(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = ready(tmp)
            original = copy.deepcopy(m)
            entries = [entry("relation", "P13", "modify", dict(label="refinement", parent_id="G3", child_id="G1", rationale="测试方向", conditions=[])),
                       entry("relation", "P23", "modify", dict(label="refinement", parent_id="G2", child_id="G3", rationale="测试方向", conditions=[]), eid="E2")]
            with self.assertRaisesRegex(ValueError, "cycle"):
                apply(m, packet(m, entries), Path(tmp) / "initial")
            self.assertEqual(m, original)


if __name__ == "__main__":
    unittest.main()
