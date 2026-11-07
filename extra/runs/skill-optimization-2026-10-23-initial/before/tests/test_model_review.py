import copy
import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

from test_goal_model_building import sample, exporter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/model-review/scripts"))
import review_model as reviewer
SPEC = importlib.util.spec_from_file_location("finalize_model", ROOT / "skills/goal-model-building/scripts/finalize_model.py")
finalizer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(finalizer)


def fixture(folder):
    model = sample()
    model["candidate_goal_mapping"] = [dict(candidate_id=g["source_candidate_ids"][0], goal_id=g["goal_id"], action="retained") for g in model["goals"]]
    text = "\n".join(e["quote"] for e in model["evidence_index"])
    for e in model["evidence_index"]:
        e.update(start_char=text.index(e["quote"]), end_char=text.index(e["quote"]) + len(e["quote"]), source_id="SYN:T1")
    path = Path(folder) / "attachments/source.txt"
    path.parent.mkdir(parents=True)
    path.write_bytes(text.encode("utf-8"))
    model["input_artifacts"] = [dict(path="attachments/source.txt", sha256=hashlib.sha256(path.read_bytes()).hexdigest())]
    return model


def patch_for(model, report, entity="model", id=None, field="relation_coverage", after=None):
    before = model[field] if entity == "model" else next(x for x in model[reviewer.FIELDS[entity][0]] if x[reviewer.FIELDS[entity][1]] == id)[field]
    return [dict(patch_id="PATCH1", issue_ids=report["unresolved_issue_ids"], base_version=model["version"],
                 base_core_sha256=exporter.core_hash(model), rationale="受控注入缺陷修复", expected_checks=["integrity"],
                 operations=[dict(action="replace", entity=entity, id=id, field=field, before=copy.deepcopy(before), after=after)])]


class ReviewTests(unittest.TestCase):
    def test_proposer_corrects_counts_without_inventing_missing_pairs(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = fixture(tmp)
            m["relation_coverage"]["evaluated_pairs"] = 100
            p = reviewer.propose(m, reviewer.inspect(m, tmp))
            self.assertEqual(p[0]["operations"][0]["after"]["evaluated_pairs"], 3)
            m["pair_decisions"][0]["assessment_status"] = "not_run"
            p = reviewer.propose(m, reviewer.inspect(m, tmp))
            self.assertEqual(p[0]["operations"][0]["after"]["evaluated_pairs"], 2)
            m["pair_decisions"].pop()
            self.assertEqual(reviewer.propose(m, reviewer.inspect(m, tmp)), [])

    def test_core_hash_ignores_derived_status_but_tracks_human_and_semantic_changes(self):
        m = sample()
        sha = exporter.core_hash(m)
        m["validation"]["structure_status"] = "passed"
        m["delivery"]["readiness"] = "reviewable"
        self.assertEqual(exporter.core_hash(m), sha)
        m["review"]["records"].append(dict(reviewer="human", decision="pending"))
        self.assertNotEqual(exporter.core_hash(m), sha)

    def test_mechanical_pass_does_not_claim_semantic_or_human_acceptance(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = fixture(tmp)
            r = reviewer.inspect(m, tmp)
            self.assertEqual(r["summary"]["structure_status"], "passed")
            self.assertEqual(r["summary"]["semantic_status"], "not_run")
            self.assertEqual(r["review_status"], "pending")
            self.assertEqual(len([i for i in r["issues"] if i["type"] == "semantic"]), 1)
            self.assertEqual(r["issues"][0]["target_ids"], ["G2", "G3"])

    def test_missing_tampered_and_escaping_attachments_block(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = fixture(tmp)
            (Path(tmp) / "attachments/source.txt").write_text("changed", encoding="utf-8")
            self.assertEqual(reviewer.inspect(m, tmp)["summary"]["structure_status"], "failed")
            m["input_artifacts"][0]["path"] = "attachments/../../outside.txt"
            self.assertTrue(any("Unsafe" in i["reason"] for i in reviewer.inspect(m, tmp)["issues"]))
            self.assertEqual(reviewer.inspect(m)["summary"]["structure_status"], "failed")

    def test_quote_offset_and_cross_document_scope_block(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = fixture(tmp)
            m["evidence_index"][0].update(start_char=1, source_id="OTHER:T1")
            rules = {i["rule_id"] for i in reviewer.inspect(m, tmp)["issues"]}
            self.assertIn("source_location", rules)
            self.assertIn("scope", rules)

    def test_lineage_and_omitted_positive_edge_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = fixture(tmp)
            m["candidate_goal_mapping"].pop()
            m["edges"] = []
            rules = {i["rule_id"] for i in reviewer.inspect(m, tmp)["issues"]}
            self.assertIn("lineage", rules)
            self.assertIn("representation", rules)

    def test_atomic_repair_and_original_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = fixture(tmp)
            correct = copy.deepcopy(m["relation_coverage"])
            m["relation_coverage"]["evaluated_pairs"] = 99
            old = copy.deepcopy(m)
            r = reviewer.inspect(m, tmp)
            fixed, after, attempt = reviewer.repair(m, patch_for(m, r, after=correct), tmp)
            self.assertEqual(m, old)
            self.assertEqual(attempt["status"], "applied")
            self.assertEqual(after["summary"]["structure_status"], "passed")
            self.assertEqual(fixed["parent_version"], m["version"])
            self.assertEqual(fixed["review"]["status"], "pending")

    def test_stale_patch_and_precondition_rollback(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = fixture(tmp)
            r = reviewer.inspect(m, tmp)
            patches = patch_for(m, r, after={})
            for field, value in [("base_core_sha256", "old"), ("base_version", "v0")]:
                p = copy.deepcopy(patches)
                p[0][field] = value
                fixed, _, a = reviewer.repair(m, p, tmp)
                self.assertEqual(fixed, m)
                self.assertEqual(a["status"], "rolled_back")
            patches[0]["operations"][0]["before"] = {}
            self.assertEqual(reviewer.repair(m, patches, tmp)[0], m)

    def test_new_bad_reference_rolls_back_whole_transaction(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = fixture(tmp)
            correct = copy.deepcopy(m["relation_coverage"])
            m["relation_coverage"]["evaluated_pairs"] = 99
            patches = patch_for(m, reviewer.inspect(m, tmp), after=correct)
            patches[0]["operations"].append(dict(action="replace", entity="edge", id="R1", field="child_id", before="G2", after="absent"))
            fixed, _, attempt = reviewer.repair(m, patches, tmp)
            self.assertEqual(fixed, m)
            self.assertEqual(attempt["status"], "rolled_back")

    def test_evidence_repair_invalidates_support(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = fixture(tmp)
            original = m["evidence_index"][0]["quote"]
            m["evidence_index"][0]["quote"] = "wrong quote"
            patches = patch_for(m, reviewer.inspect(m, tmp), "evidence", "E1", "quote", original)
            fixed, after, attempt = reviewer.repair(m, patches, tmp)
            self.assertEqual(attempt["status"], "applied")
            self.assertEqual(fixed["goals"][0]["trace_status"], "needs_retrace")
            self.assertEqual(after["summary"]["structure_status"], "failed")

    def test_round_budget_and_unknown_operation_stop(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = fixture(tmp)
            m["changes"] = [dict(kind="local_repair"), dict(kind="local_repair")]
            p = patch_for(m, reviewer.inspect(m, tmp), after={})
            self.assertIn("budget", reviewer.repair(m, p, tmp)[2]["stop_reason"])
            m["changes"] = []
            p = patch_for(m, reviewer.inspect(m, tmp), after={})
            p[0]["operations"][0]["entity"] = "source"
            self.assertEqual(reviewer.repair(m, p, tmp)[0], m)

    def test_finalize_packages_bound_report_without_changing_semantics(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = fixture(tmp)
            r = reviewer.inspect(m, tmp)
            out = Path(tmp) / "delivery"
            result = finalizer.finalize(m, r, tmp, out)
            self.assertEqual(result["delivery"]["readiness"], "reviewable")
            self.assertEqual(result["review"]["status"], "pending")
            self.assertEqual(result["goals"], m["goals"])
            self.assertEqual(exporter.core_hash(result), exporter.core_hash(m))
            self.assertTrue((out / "attachments/review-report.json").is_file())
            manifest = json.loads((out / "delivery-manifest.json").read_text(encoding="utf-8"))
            for path, sha in manifest["files"].items():
                self.assertEqual(hashlib.sha256((out / path).read_bytes()).hexdigest(), sha)

    def test_stale_and_forged_report_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = fixture(tmp)
            r = reviewer.inspect(m, tmp)
            changed = copy.deepcopy(m)
            changed["goals"][0]["statement"] += "新增条件"
            with self.assertRaises(ValueError):
                finalizer.finalize(changed, r, tmp, Path(tmp) / "out")
            r["checks"] = []
            with self.assertRaises(ValueError):
                finalizer.finalize(m, r, tmp, Path(tmp) / "out")

    def test_attachment_tampered_after_review_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = fixture(tmp)
            r = reviewer.inspect(m, tmp)
            (Path(tmp) / "attachments/source.txt").write_text("tampered", encoding="utf-8")
            with self.assertRaises(ValueError):
                finalizer.finalize(m, r, tmp, Path(tmp) / "out")


if __name__ == "__main__":
    unittest.main()
