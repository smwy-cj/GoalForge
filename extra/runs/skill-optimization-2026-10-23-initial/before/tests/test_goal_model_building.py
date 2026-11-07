import copy
import importlib.util
import json
import re
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

FOLDER = Path(__file__).resolve().parents[1] / "skills/goal-model-building/scripts"
SPEC = importlib.util.spec_from_file_location("export_model", FOLDER / "export_model.py")
exporter = importlib.util.module_from_spec(SPEC)
sys.modules["export_model"] = exporter
SPEC.loader.exec_module(exporter)
SPEC2 = importlib.util.spec_from_file_location("assemble_model", FOLDER / "assemble_model.py")
assembler = importlib.util.module_from_spec(SPEC2)
SPEC2.loader.exec_module(assembler)


def sample():
    goals = [dict(goal_id=f"G{i}", statement=s, origin="explicit" if i < 3 else "inferred", actor="用户",
                  context=[], evidence_ids=[f"E{i}"], source_candidate_ids=[f"C{i}"], trace_status="direct" if i < 3 else "inferred", review_status="pending")
             for i, s in enumerate(["根据天气合理安排活动", "根据降雨安排户外活动", "减少搜索费用"], 1)]
    decisions = [dict(pair_id="P12", a="G1", b="G2", label="refinement", parent_id="G1", child_id="G2",
                      rationale="合成示例：户外活动为范围具体化。", interpretation="scope_specialization", evidence_ids=["E1", "E2"], conditions=[]),
                 dict(pair_id="P13", a="G1", b="G3", label="none", rationale="材料未建立联系。", evidence_ids=[], conditions=[]),
                 dict(pair_id="P23", a="G2", b="G3", label="uncertain", rationale="需用户确认。", evidence_ids=[], conditions=[])]
    return dict(schema_version="goalforge-model-draft-1", model_id="合成层级示例", version="v0.1", parent_version=None,
                input_artifacts=[], document_scope=dict(document_ids=["SYN"], cross_document_allowed=False), goals=goals,
                pair_decisions=decisions, edges=[dict(edge_id="R1", type="refinement", parent_id="G1", child_id="G2", decision_id="P12", conditions=[])],
                evidence_index=[dict(evidence_id=f"E{i}", source_id=f"S{i}", quote=g["statement"], original_locator=dict(paragraph=i), location_status="exact", recognition_status="native_text") for i, g in enumerate(goals, 1)],
                candidate_goal_mapping=[], diagnostics=[], relation_coverage=dict(strategy="all_pairs", expected_pairs=3, evaluated_pairs=3),
                issues=[dict(code="uncertain", reason="需审核G2与G3关系。", target_ids=["G2", "G3"], severity="needs_review")], assumptions=[],
                validation=dict(structure_status="not_run", semantic_status="not_run", report_path=None), review=dict(status="pending", records=[]),
                changes=[], delivery=dict(mode="assemble", readiness="unchecked", limitations=["合成例，不代表实际提取效果。"], files=[]))


class ModelTests(unittest.TestCase):
    def assembly_inputs(self):
        model = sample()
        candidates, traces = [], []
        for g, evidence in zip(model["goals"], model["evidence_index"]):
            cid = g["source_candidate_ids"][0]
            candidates.append(dict(candidate_id=cid, category="goal", statement=g["statement"], origin=g["origin"], actor=g["actor"], context=[], inference=None))
            evidence = dict(evidence, source_version_status="verified")
            traces.append(dict(target_id=cid, statement=g["statement"], support=dict(label=g["trace_status"]), submitted_evidence=[evidence], located_evidence=[]))
        normalized = [{k: g[k] for k in ("goal_id", "statement", "origin", "actor", "context", "source_candidate_ids")} for g in model["goals"]]
        return dict(document_id="SYN", candidates=candidates), dict(traces=traces), model["pair_decisions"], normalized

    def test_changed_normalization_requires_retracing(self):
        extraction, tracing, decisions, normalized = self.assembly_inputs()
        normalized[0]["statement"] += "且两秒内完成"
        model = assembler.assemble(extraction, tracing, decisions, normalized)
        self.assertEqual(model["goals"][0]["trace_status"], "needs_retrace")
        self.assertEqual(model["delivery"]["readiness"], "blocked")
        self.assertEqual(extraction["candidates"][0]["statement"], "根据天气合理安排活动")

    def test_stale_trace_statement_rejected(self):
        extraction, tracing, decisions, normalized = self.assembly_inputs()
        tracing["traces"][0]["statement"] = "不同的旧目标"
        with self.assertRaisesRegex(ValueError, "version"):
            assembler.assemble(extraction, tracing, decisions, normalized)

    def test_four_outputs_and_same_embedded_model(self):
        data = sample()
        before = copy.deepcopy(data)
        with tempfile.TemporaryDirectory() as tmp:
            result = exporter.export(data, Path(tmp) / "delivery")
            folder = Path(tmp) / "delivery"
            self.assertEqual(data, before)
            for name in ("json", "md", "html", "svg"):
                self.assertTrue((folder / f"goal-model.{name}").exists())
            page = (folder / "goal-model.html").read_text(encoding="utf-8")
            embedded = json.loads(re.search(r'<script id="model-data" type="application/json">(.*?)</script>', page, re.S).group(1))
            self.assertEqual(embedded, result)
            self.assertEqual(json.loads((folder / "goal-model.json").read_text(encoding="utf-8")), result)
            self.assertNotIn("fetch(", page)
            self.assertNotIn('<script src=', page)
            svg = ET.fromstring((folder / "goal-model.svg").read_text(encoding="utf-8"))
            self.assertEqual(len([n for n in svg.iter() if "data-node" in n.attrib]), 3)

    def test_invalid_ref_and_cycles_rejected(self):
        data = sample()
        data["edges"][0]["child_id"] = "absent"
        with self.assertRaises(ValueError):
            exporter.check(data)
        data = sample()
        data["pair_decisions"][1].update(label="refinement", parent_id="G3", child_id="G1")
        data["pair_decisions"][2].update(label="refinement", parent_id="G2", child_id="G3")
        data["edges"] += [dict(edge_id="R2", type="refinement", parent_id="G3", child_id="G1", decision_id="P13"), dict(edge_id="R3", type="refinement", parent_id="G2", child_id="G3", decision_id="P23")]
        with self.assertRaisesRegex(ValueError, "cycle"):
            exporter.check(data)

    def test_incomplete_pair_coverage_rejected(self):
        data = sample()
        data["pair_decisions"].pop()
        data["relation_coverage"]["evaluated_pairs"] = 2
        with self.assertRaises(ValueError):
            exporter.check(data)

    def test_unbound_passed_state_rejected(self):
        data = sample()
        data["delivery"]["readiness"] = "reviewable"
        data["validation"]["structure_status"] = "passed"
        with self.assertRaises(ValueError):
            exporter.check(data)

    def test_html_payload_and_template_tokens_safe(self):
        data = sample()
        bad = '</script><script>alert(1)</script> __MODEL_SVG__ __VIEWER_JS__ __VIEWER_CSS__ & 中文'
        data["goals"][0]["statement"] = bad
        with tempfile.TemporaryDirectory() as tmp:
            exporter.export(data, Path(tmp) / "delivery")
            page = (Path(tmp) / "delivery/goal-model.html").read_text(encoding="utf-8")
            embedded = json.loads(re.search(r'<script id="model-data" type="application/json">(.*?)</script>', page, re.S).group(1))
            self.assertEqual(embedded["goals"][0]["statement"], bad)
            self.assertNotIn('<script>alert(1)</script>', page)

    def test_long_labels_expand_nodes_and_preserve_text(self):
        data = sample()
        data["goals"][0]["statement"] = "这是带有条件和否定的较长中文目标表述" * 12
        data["content_sha256"] = exporter.content_hash(data)
        svg = ET.fromstring(exporter.render_svg(data))
        node = next(n for n in svg.iter() if n.attrib.get("data-node") == "G1")
        texts = [n.text for n in node if n.tag.endswith("text")]
        self.assertEqual("".join(texts[1:]), data["goals"][0]["statement"])
        self.assertGreater(float(next(n for n in node if n.tag.endswith("rect")).attrib["height"]), 110)

    def test_existing_delivery_not_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / "delivery"
            exporter.export(sample(), folder)
            with self.assertRaises(ValueError):
                exporter.export(sample(), folder)


if __name__ == "__main__":
    unittest.main()
