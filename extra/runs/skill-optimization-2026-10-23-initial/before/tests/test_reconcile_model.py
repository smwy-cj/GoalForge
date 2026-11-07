import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

from test_feedback_flow import ready, packet, entry, persist
from test_model_review import reviewer, finalizer
from test_goal_model_building import exporter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/goal-model-building/scripts"))
import reconcile_model as reconciler
import trace_candidates as tracer


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = reviewer.encode(value)
    path.write_bytes(raw)
    return raw


def setup_case(tmp, collision=False):
    from process_feedback import apply
    root = Path(tmp)
    model = ready(root)
    if collision:
        model["evidence_index"][0]["evidence_id"] = "E0001"
        for g in model["goals"]:
            g["evidence_ids"] = ["E0001" if e == "E1" else e for e in g["evidence_ids"]]
        for p in model["pair_decisions"]:
            p["evidence_ids"] = ["E0001" if e == "E1" else e for e in p["evidence_ids"]]
    modified, _, attachments = apply(model, packet(model, [entry("goal", "G1", "modify", dict(statement="根据天气安排活动"))]), root / "initial")
    base = root / "revision"
    persist(base, modified, attachments)
    canonical = attachments["attachments/source.txt"].decode("utf-8")
    g = modified["goals"][0]
    ev = modified["evidence_index"][0]
    data = dict(schema_version="goalforge-extraction-draft-2", document_id="SYN", document_hash=tracer.sha(canonical.encode("utf-8")),
                target_kind="goal", target_model=reconciler.model_binding(modified),
                segments=[dict(source_id="SYN:T1", material_id="M1", text=canonical, original_locator=dict(start_char=0), recognition_status="native_text")],
                candidates=[dict(candidate_id="G1", category="goal", statement=g["statement"], actor=g["actor"], context=g["context"], origin=g["origin"],
                                 evidence_candidates=[dict(source_id="SYN:T1", quote=ev["quote"], role="basis", start_char=ev["start_char"], end_char=ev["end_char"])])])
    inputs = root / "inputs"
    raw = write(inputs / "input.json", data)
    bundle = tracer.judgment_template(data, raw)
    bundle["judgments"]["G1"].update(label="direct", rationale="新版本合成判断，未新增时间条件。", supported_parts=[g["statement"]])
    jraw = write(inputs / "judgments.json", bundle)
    traced = tracer.trace(data, bundle, canonical, tracer.sha(raw))
    traced["input_artifact"] = dict(sha256=tracer.sha(raw))
    traced["judgment_artifact"] = dict(sha256=tracer.sha(jraw))
    write(inputs / "tracing.json", traced)
    nodes = {n["goal_id"]: n for n in modified["goals"]}
    decisions = []
    for p in modified["pair_decisions"]:
        if "G1" not in {p["a"], p["b"]}:
            continue
        d = dict(pair_id=p["pair_id"], a=p["a"], b=p["b"], label="none", rationale="新版本的合成关系判断。", evidence_ids=[], conditions=[],
                 target_statements={gid: nodes[gid]["statement"] for gid in (p["a"], p["b"])})
        if p["pair_id"] == "P12":
            d.update(label="refinement", parent_id="G1", child_id="G2", interpretation="scope_specialization", evidence_ids=["trace:E0001", "E2"])
        decisions.append(d)
    relation_bundle = dict(schema_version="goalforge-relation-reassessment-1", base_model=reconciler.model_binding(modified), decisions=decisions)
    write(inputs / "relations.json", relation_bundle)
    return modified, base, inputs, data, bundle, traced, relation_bundle


def merge(case, with_relations=True):
    model, base, inputs, *_ = case
    return reconciler.reconcile(model, base, inputs / "input.json", inputs / "tracing.json", inputs / "judgments.json", inputs / "relations.json" if with_relations else None)


class ReconcileTests(unittest.TestCase):
    def test_complete_merge_reinspects_and_exports_without_changing_lineage(self):
        with tempfile.TemporaryDirectory() as tmp:
            case = setup_case(tmp)
            model = copy.deepcopy(case[0])
            template = reconciler.relation_template(model)
            self.assertEqual(len(template["decisions"]), 2)
            self.assertTrue(all(p["label"] is None for p in template["decisions"]))
            result, record, raw = merge(case)
            self.assertEqual(case[0], model)
            self.assertEqual(result["candidate_goal_mapping"], model["candidate_goal_mapping"])
            self.assertEqual(result["goals"][0]["statement"], model["goals"][0]["statement"])
            self.assertEqual(result["goals"][0]["trace_status"], "direct")
            self.assertFalse(record["remaining_pair_ids"])
            report = persist(Path(tmp) / "merged", result, raw)
            self.assertEqual(report["summary"]["structure_status"], "passed")
            exported = finalizer.finalize(result, report, Path(tmp) / "merged", Path(tmp) / "delivery")
            self.assertEqual(exported["delivery"]["readiness"], "reviewable")
            self.assertEqual(exported["review"]["status"], "pending")
            self.assertEqual(exported["validation"]["semantic_status"], "not_run")
            self.assertEqual(result["parent_version"], model["version"])

    def test_existing_and_incoming_evidence_ids_never_overwrite_each_other(self):
        with tempfile.TemporaryDirectory() as tmp:
            case = setup_case(tmp, collision=True)
            old = copy.deepcopy(case[0]["evidence_index"][0])
            result, record, _ = merge(case)
            new_id = record["evidence_id_mapping"]["E0001"]
            self.assertNotEqual(new_id, "E0001")
            self.assertEqual(next(e for e in result["evidence_index"] if e["evidence_id"] == "E0001"), old)
            self.assertIn(new_id, next(p for p in result["pair_decisions"] if p["pair_id"] == "P12")["evidence_ids"])

    def test_retracing_without_relation_reassessment_remains_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            case = setup_case(tmp)
            result, record, raw = merge(case, False)
            self.assertEqual(set(record["remaining_pair_ids"]), {"P12", "P13"})
            report = persist(Path(tmp) / "partial", result, raw)
            self.assertEqual(report["summary"]["structure_status"], "failed")

    def test_stale_model_and_stale_relation_bundle_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            case = setup_case(tmp)
            case[0]["version"] += ".changed"
            with self.assertRaisesRegex(ValueError, "model version"):
                merge(case)
        with tempfile.TemporaryDirectory() as tmp:
            case = setup_case(tmp)
            case[6]["base_model"]["core_sha256"] = "old"
            write(case[2] / "relations.json", case[6])
            with self.assertRaisesRegex(ValueError, "version/core"):
                merge(case)

    def test_modified_tracing_result_and_mismatched_artifacts_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            case = setup_case(tmp)
            case[5]["traces"][0]["support"]["rationale"] = "伪造结果"
            write(case[2] / "tracing.json", case[5])
            with self.assertRaisesRegex(ValueError, "re-executed"):
                merge(case)
            case[5]["input_artifact"]["sha256"] = "old"
            write(case[2] / "tracing.json", case[5])
            with self.assertRaisesRegex(ValueError, "digest"):
                merge(case)

    def test_unknown_pair_statement_mismatch_and_unknown_evidence_rejected(self):
        for mode in ("pair", "statement", "evidence", "positive_without_evidence"):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as tmp:
                case = setup_case(tmp)
                d = case[6]["decisions"][0]
                if mode == "pair":
                    d["pair_id"] = "UNKNOWN"
                elif mode == "statement":
                    d["target_statements"]["G1"] = "旧目标"
                elif mode == "evidence":
                    d["evidence_ids"] = ["trace:UNKNOWN"]
                else:
                    d["evidence_ids"] = []
                write(case[2] / "relations.json", case[6])
                with self.assertRaises(ValueError):
                    merge(case)

    def test_new_cycle_rolls_back_all_in_memory_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            case = setup_case(tmp)
            old = copy.deepcopy(case[0])
            nodes = {g["goal_id"]: g for g in old["goals"]}
            case[6]["decisions"][1].update(label="refinement", parent_id="G3", child_id="G1", interpretation="scope_specialization", evidence_ids=["E3"])
            case[6]["decisions"].append(dict(pair_id="P23", a="G2", b="G3", label="refinement", parent_id="G2", child_id="G3", interpretation="scope_specialization",
                rationale="受控注入有向环。", evidence_ids=["E2"], conditions=[], target_statements={gid: nodes[gid]["statement"] for gid in ("G2", "G3")}))
            write(case[2] / "relations.json", case[6])
            with self.assertRaisesRegex(ValueError, "cycle"):
                merge(case)
            self.assertEqual(case[0], old)

    def test_changed_source_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            case = setup_case(tmp)
            (case[1] / "attachments/source.txt").write_text("变更后的源文", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "hash mismatch"):
                merge(case)

    def test_negative_new_judgment_does_not_become_supported(self):
        with tempfile.TemporaryDirectory() as tmp:
            case = setup_case(tmp)
            case[4]["judgments"]["G1"].update(label="insufficient", rationale="受控判断：尚不足以支持。")
            jraw = write(case[2] / "judgments.json", case[4])
            actual = tracer.trace(case[3], case[4], (case[1] / "attachments/source.txt").read_text(encoding="utf-8"), tracer.sha((case[2] / "input.json").read_bytes()))
            actual["input_artifact"] = case[5]["input_artifact"]
            actual["judgment_artifact"] = dict(sha256=tracer.sha(jraw))
            write(case[2] / "tracing.json", actual)
            result, record, raw = merge(case)
            self.assertIn("G1", record["remaining_goal_ids"])
            self.assertEqual(result["goals"][0]["trace_status"], "insufficient")
            self.assertEqual(persist(Path(tmp) / "negative", result, raw)["summary"]["structure_status"], "failed")

    def test_relation_only_evidence_reassessment_can_complete_without_goal_tracing(self):
        from process_feedback import apply
        with tempfile.TemporaryDirectory() as tmp:
            model = ready(tmp)
            ev = copy.deepcopy(model["evidence_index"][0])
            ev["evidence_id"] = "REL-ONLY"
            model["evidence_index"].append(ev)
            model["pair_decisions"][0]["evidence_ids"] = ["REL-ONLY"]
            revised, _, raw = apply(model, packet(model, [entry("evidence", "REL-ONLY", "incorrect")]), Path(tmp) / "initial")
            base = Path(tmp) / "revision"
            persist(base, revised, raw)
            bundle = dict(schema_version="goalforge-relation-reassessment-1", base_model=reconciler.model_binding(revised), decisions=[dict(
                pair_id="P12", a="G1", b="G2", label="refinement", parent_id="G1", child_id="G2", interpretation="scope_specialization",
                rationale="受控新判断：重新核对来源后保留该方向。", evidence_ids=["REL-ONLY"], conditions=[],
                target_statements={g["goal_id"]: g["statement"] for g in revised["goals"] if g["goal_id"] in {"G1", "G2"}})])
            path = Path(tmp) / "relations.json"
            write(path, bundle)
            result, record, raw = reconciler.reconcile(revised, base, relations=path)
            self.assertFalse(record["remaining_pair_ids"])
            self.assertEqual(persist(Path(tmp) / "complete", result, raw)["summary"]["structure_status"], "passed")


if __name__ == "__main__":
    unittest.main()
