"""Assemble frozen model judgments; never invent normalization or relation labels."""

import argparse
import hashlib
import json
from pathlib import Path

from export_model import check


def assemble(extraction, tracing, decisions, normalized=None):
    candidates = {c["candidate_id"]: c for c in extraction["candidates"]}
    traces = {t["target_id"]: t for t in tracing["traces"]}
    if len(traces) != len(tracing["traces"]):
        raise ValueError("Duplicate trace target")
    for cid, t in traces.items():
        if cid not in candidates or t["statement"] != candidates[cid]["statement"]:
            raise ValueError("Tracing does not match the candidate version")
    selected = normalized if normalized is not None else [dict(goal_id=c["candidate_id"].replace("-C", "-G"),
        statement=c["statement"], source_candidate_ids=[c["candidate_id"]], origin=c["origin"],
        actor=c["actor"], context=c["context"]) for c in candidates.values() if c["category"] == "goal"]
    goals, mapping, evidence, issues = [], [], {}, []
    for g in selected:
        refs = g["source_candidate_ids"]
        if not refs or not set(refs).issubset(candidates) or any(candidates[r]["category"] != "goal" for r in refs):
            raise ValueError("Model nodes must refer to extracted goal candidates")
        evidence_ids, supports = [], []
        changed = len(refs) != 1 or any(g.get(k) != candidates[refs[0]].get(k) for k in ("statement", "origin", "actor", "context"))
        for cid in refs:
            t = traces.get(cid)
            if not t:
                supports.append("needs_retrace")
                continue
            supports.append(t["support"]["label"])
            for item in t["submitted_evidence"] + t["located_evidence"]:
                if item["evidence_id"] in evidence and evidence[item["evidence_id"]] != item:
                    raise ValueError("Conflicting evidence ID")
                evidence[item["evidence_id"]] = item
                if item["evidence_id"] not in evidence_ids:
                    evidence_ids.append(item["evidence_id"])
                if item["location_status"] != "exact" or item["source_version_status"] == "version_mismatch":
                    changed = True
        support = "needs_retrace" if changed or not supports else (
            supports[0] if len(set(supports)) == 1 else "needs_retrace")
        node = dict(g, evidence_ids=evidence_ids, trace_status=support, review_status="pending")
        goals.append(node)
        for cid in refs:
            mapping.append(dict(candidate_id=cid, goal_id=g["goal_id"], action="retained" if not changed else "changed", reason="保持来源映射；实质变化需重新追溯。"))
        if support in {"needs_retrace", "insufficient", "contradicted"}:
            issues.append(dict(code="needs_retrace", severity="blocking", target_ids=[g["goal_id"]], reason="目标语义、证据或支持状态需重新核对。"))
    edges = []
    for p in decisions:
        if p["label"] in {"related", "refinement"}:
            edge = dict(edge_id=f"R{len(edges)+1:03}", type=p["label"], decision_id=p["pair_id"],
                        conditions=p.get("conditions", []), review_status="pending")
            if p["label"] == "related":
                edge.update(a=p["a"], b=p["b"])
            else:
                edge.update(parent_id=p["parent_id"], child_id=p["child_id"], interpretation=p["interpretation"])
            edges.append(edge)
        if p["label"] == "uncertain":
            issues.append(dict(code="uncertain_relation", severity="needs_review", target_ids=[p["a"], p["b"]], reason=p["rationale"]))
    n = len(goals)
    selected_ids = {cid for g in goals for cid in g["source_candidate_ids"]}
    diagnostics = [c for cid, c in candidates.items() if cid not in selected_ids]
    for c in diagnostics:
        mapping.append(dict(candidate_id=c["candidate_id"], goal_id=None, action="diagnostic", reason="未进入当前目标集合，保留原记录。"))
    model = dict(schema_version="goalforge-model-draft-1", model_id=extraction["document_id"] + "-goal-model",
                 version="v0.1", parent_version=None, input_artifacts=[],
                 document_scope=dict(document_ids=[extraction["document_id"]], cross_document_allowed=False),
                 goals=goals, pair_decisions=decisions, edges=edges, evidence_index=list(evidence.values()),
                 candidate_goal_mapping=mapping, diagnostics=diagnostics,
                 relation_coverage=dict(strategy="all_pairs", expected_pairs=n*(n-1)//2, evaluated_pairs=len(decisions)),
                 issues=issues, assumptions=[dict(candidate_id=c["candidate_id"], **c["inference"]) for c in candidates.values() if c["inference"]],
                 validation=dict(structure_status="not_run", semantic_status="not_run", report_path=None),
                 review=dict(status="pending", records=[]), changes=[],
                 delivery=dict(mode="assemble", readiness="blocked" if any(i["severity"] == "blocking" for i in issues) else "unchecked",
                               limitations=["模型尚未经过 model-review；导出完整性检查不能替代模型质量审核。",
                                            "当前会话助手的开发判断，非独立盲测；无人工采纳记录。"], files=[]))
    check(model)
    return model


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("extraction", type=Path)
    parser.add_argument("tracing", type=Path)
    parser.add_argument("decisions", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--normalized", type=Path)
    args = parser.parse_args()
    load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
    extraction, traced = load(args.extraction), load(args.tracing)
    if traced["input_artifact"].get("sha256") != hashlib.sha256(args.extraction.read_bytes()).hexdigest():
        raise ValueError("Trace input hash differs from extraction")
    if any(t["support"]["label"] in {"direct", "inferred"} for t in traced["traces"]):
        binding = traced.get("semantic_binding", {}).get("input_binding", {}) if traced.get("semantic_binding") else {}
        canonical = json.dumps(extraction, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
        if (binding.get("input_sha256") != hashlib.sha256(args.extraction.read_bytes()).hexdigest()
            or binding.get("data_sha256") != hashlib.sha256(canonical).hexdigest()):
            raise ValueError("Version-bound tracing required; re-author semantic judgments for the current extraction")
    if hashlib.sha256(args.source.read_bytes()).hexdigest() != extraction["document_hash"]:
        raise ValueError("Source hash differs from extraction")
    model = assemble(extraction, traced, load(args.decisions), load(args.normalized) if args.normalized else None)
    if args.output_dir.exists() and any(args.output_dir.iterdir()):
        raise ValueError("Use a fresh output directory")
    artifacts = [(args.extraction, "extraction.json"), (args.tracing, "tracing.json"),
                 (args.decisions, "relation-decisions.json"), (args.source, "source.txt")]
    if args.normalized:
        artifacts.append((args.normalized, "normalization.json"))
    for path, name in artifacts:
        relative = "attachments/" + name
        target = args.output_dir / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        raw = path.read_bytes()
        target.write_bytes(raw)
        model["input_artifacts"].append(dict(path=relative, sha256=hashlib.sha256(raw).hexdigest()))
    (args.output_dir / "model-input.json").write_text(json.dumps(model, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
