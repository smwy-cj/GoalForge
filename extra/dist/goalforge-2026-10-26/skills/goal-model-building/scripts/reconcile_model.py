"""Transactionally merge version-bound reassessments into a model copy and reinspect."""
import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path

from export_model import check_structure, core_hash

SKILLS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILLS / "goal-extraction/scripts"))
sys.path.insert(0, str(SKILLS / "model-review/scripts"))
from trace_candidates import trace, sha
from review_model import artifact_bytes, encode, inspect, markdown


def model_binding(model):
    return dict(model_id=model["model_id"], version=model["version"], core_sha256=core_hash(model))


def relation_template(model):
    goals = {g["goal_id"]: g for g in model["goals"]}
    pending = [p for p in model["pair_decisions"] if p.get("trace_status") == "needs_retrace" or p.get("assessment_status") == "not_run"]
    return dict(schema_version="goalforge-relation-reassessment-1", base_model=model_binding(model), decisions=[dict(
        pair_id=p["pair_id"], a=p["a"], b=p["b"], target_statements={gid: goals[gid]["statement"] for gid in (p["a"], p["b"])},
        label=None, rationale="", evidence_ids=[], conditions=[], parent_id=None, child_id=None, interpretation=None) for p in pending])


def read_input(path):
    raw = Path(path).read_bytes()
    return raw, json.loads(raw.decode("utf-8-sig"))


def verify_quote(item, canonical, document_ids):
    a, b, quote = item.get("start_char"), item.get("end_char"), item.get("quote")
    if (type(a) is not int or type(b) is not int or not isinstance(quote, str) or not quote
        or not 0 <= a < b <= len(canonical) or canonical[a:b] != quote):
        raise ValueError("Reassessment evidence quote/offset differs from canonical source")
    source = item.get("source_id", "")
    if not isinstance(source, str) or ":" not in source or source.split(":", 1)[0] not in document_ids:
        raise ValueError("Reassessment evidence is outside document scope")


def reconcile(model, base, retrace_input=None, tracing_result=None, judgments=None, relations=None):
    """Paths are explicit inputs. No arbitrary paths from JSON artifacts are followed."""
    if not (retrace_input or relations):
        raise ValueError("Provide tracing inputs and/or a relation reassessment bundle")
    if any((retrace_input, tracing_result, judgments)) and not all((retrace_input, tracing_result, judgments)):
        raise ValueError("Retrace input, tracing result and bound judgments must be supplied together")
    attachments, problems = artifact_bytes(model, base)
    if problems:
        raise ValueError("; ".join(problems))
    if "attachments/source.txt" not in attachments:
        raise ValueError("Canonical source attachment required")
    canonical = attachments["attachments/source.txt"].decode("utf-8")
    binding = model_binding(model)
    result = copy.deepcopy(model)
    goals = {g["goal_id"]: g for g in result["goals"]}
    pairs = {p["pair_id"]: p for p in result["pair_decisions"]}
    evidence = {e["evidence_id"]: e for e in result["evidence_index"]}
    additions, evidence_map, goal_ids, pair_ids = [], {}, set(), set()
    trace_issues = []

    def attach(role, raw):
        digest = sha(raw)
        path = "attachments/reassessment-" + role + "-" + digest[:16] + ".json"
        if path in attachments and attachments[path] != raw:
            raise ValueError("Reassessment artifact filename collision")
        attachments[path] = raw
        if not any(a["path"] == path for a in result["input_artifacts"]):
            result["input_artifacts"].append(dict(path=path, sha256=digest))
        additions.append(dict(role=role, path=path, sha256=digest))
        return path

    if retrace_input:
        input_raw, data = read_input(retrace_input)
        trace_raw, traced = read_input(tracing_result)
        judgment_raw, bundle = read_input(judgments)
        if data.get("target_model") != binding or data.get("target_kind") != "goal":
            raise ValueError("Retracing input targets a different model version/core")
        if data.get("document_hash") != sha(attachments["attachments/source.txt"]) or data.get("document_id") not in model["document_scope"]["document_ids"]:
            raise ValueError("Retracing source version/scope differs")
        for c in data["candidates"]:
            gid = c["candidate_id"]
            if gid not in goals or c.get("category") != "goal" or any(c.get(k) != goals[gid].get(k) for k in ("statement", "origin", "actor", "context")):
                raise ValueError("Retraced goal differs from frozen model node")
        if (traced.get("schema_version") != "goalforge-tracing-draft-1" or traced.get("input_artifact", {}).get("sha256") != sha(input_raw)
            or traced.get("judgment_artifact", {}).get("sha256") != sha(judgment_raw)):
            raise ValueError("Tracing result input/judgment artifact digest mismatch")
        actual = trace(data, bundle, canonical, sha(input_raw))
        for key in ("traces", "sources", "status", "semantic_binding", "target_model"):
            if actual[key] != traced.get(key):
                raise ValueError("Tracing result differs from re-executed bound inputs: " + key)
        if not actual["traces"]:
            raise ValueError("No goals reassessed")
        if any(i["code"] == "semantic_not_run" for t in actual["traces"] for i in t["issues"]):
            raise ValueError("Unassessed goals cannot be merged as completed semantic judgments")
        attach("retrace-input", input_raw)
        trace_path = attach("tracing", trace_raw)
        attach("semantic-judgments", judgment_raw)
        for t in actual["traces"]:
            gid = t["target_id"]
            if t["target_kind"] != "goal" or t["statement"] != goals[gid]["statement"]:
                raise ValueError("Tracing target kind/statement mismatch")
            refs = []
            for item in t["submitted_evidence"] + t["located_evidence"]:
                verify_quote(item, canonical, model["document_scope"]["document_ids"])
                if (item.get("location_status") != "exact" or item.get("verification_scope") != "full_text"
                    or item.get("source_version_status") != "verified"):
                    raise ValueError("Reassessment requires actually verified full-text evidence")
                old_id = item["evidence_id"]
                if old_id in evidence_map:
                    raise ValueError("Duplicate tracing evidence ID")
                i = 1
                while "ET" + str(i).zfill(4) in evidence:
                    i += 1
                eid = "ET" + str(i).zfill(4)
                evidence_map[old_id] = eid
                copied = copy.deepcopy(item)
                copied.update(evidence_id=eid, reassessment_original_id=old_id)
                evidence[eid] = copied
                refs.append(eid)
            goals[gid].update(evidence_ids=refs, trace_status=t["support"]["label"], review_status="pending",
                              trace_result=dict(path=trace_path, target_id=gid, support=copy.deepcopy(t["support"])))
            goal_ids.add(gid)
            trace_issues.extend(dict(code="reassessment_" + i["code"], severity="needs_review", target_ids=[gid], reason=i["reason"]) for i in t["issues"])
        # Updated support can change relation evidence. No stale relation is silently retained.
        for p in pairs.values():
            if {p["a"], p["b"]} & goal_ids:
                old = copy.deepcopy(p)
                p.update(previous_decision=old, label="uncertain", assessment_status="not_run", trace_status="needs_retrace",
                         rationale="目标支持已重新判断，关联关系需匹配新依据重评。", review_status="pending")
                p.pop("parent_id", None)
                p.pop("child_id", None)

    if relations:
        relation_raw, bundle = read_input(relations)
        if bundle.get("schema_version") != "goalforge-relation-reassessment-1" or bundle.get("base_model") != binding:
            raise ValueError("Relation reassessment model version/core mismatch")
        decisions = bundle.get("decisions")
        if not isinstance(decisions, list):
            raise ValueError("Relation decisions must be an array")
        for proposed in decisions:
            pid = proposed["pair_id"]
            if pid not in pairs or pid in pair_ids:
                raise ValueError("Unknown or duplicate reassessed pair")
            p = pairs[pid]
            if ({proposed["a"], proposed["b"]} != {p["a"], p["b"]} or
                proposed.get("target_statements") != {gid: goals[gid]["statement"] for gid in (p["a"], p["b"])}):
                raise ValueError("Relation endpoints/target statements changed")
            label = proposed["label"]
            if label not in {"refinement", "related", "equivalent", "none", "uncertain"}:
                raise ValueError("Invalid reassessed relation label")
            if not isinstance(proposed.get("rationale"), str) or not proposed["rationale"].strip():
                raise ValueError("Relation reassessment requires a new rationale")
            conditions, refs = proposed.get("conditions"), proposed.get("evidence_ids")
            if not isinstance(conditions, list) or not all(isinstance(c, str) for c in conditions):
                raise ValueError("Relation conditions must be a string array")
            if not isinstance(refs, list) or not all(isinstance(e, str) for e in refs):
                raise ValueError("Relation evidence must be explicit identifiers")
            resolved = []
            for ref in refs:
                eid = evidence_map.get(ref[6:]) if ref.startswith("trace:") else ref
                if eid not in evidence:
                    raise ValueError("Unknown relation evidence reference; use trace:<ID> for incoming tracing evidence")
                verify_quote(evidence[eid], canonical, model["document_scope"]["document_ids"])
                if eid not in resolved:
                    resolved.append(eid)
            if label in {"refinement", "related"} and not resolved:
                raise ValueError("Positive reassessed relation requires source evidence")
            old = copy.deepcopy(p)
            p.update(previous_decision=old, label=label, rationale=proposed["rationale"], conditions=conditions,
                     evidence_ids=resolved, assessment_status="assessed", trace_status="reviewed", review_status="pending")
            p.pop("parent_id", None)
            p.pop("child_id", None)
            if label == "refinement":
                a, b = proposed.get("parent_id"), proposed.get("child_id")
                if a == b or {a, b} != {p["a"], p["b"]}:
                    raise ValueError("Invalid reassessed refinement direction")
                interpretation = proposed.get("interpretation")
                if not isinstance(interpretation, str) or not interpretation.strip() or interpretation.lower() in {"and", "or"}:
                    raise ValueError("Refinement requires an explicit contextual/scope interpretation")
                p.update(parent_id=a, child_id=b, interpretation=interpretation)
            pair_ids.add(pid)
        attach("relations", relation_raw)
    if not goal_ids and not pair_ids:
        raise ValueError("No reassessment supplied")

    result["evidence_index"] = list(evidence.values())
    old_edges = {e["decision_id"]: e for e in model["edges"]}
    used_ids = {e["edge_id"] for e in model["edges"]}
    result["edges"] = []
    for p in pairs.values():
        if p["label"] not in {"related", "refinement"}:
            continue
        if p["pair_id"] in old_edges and p["pair_id"] not in pair_ids:
            result["edges"].append(copy.deepcopy(old_edges[p["pair_id"]]))
            continue
        eid = old_edges.get(p["pair_id"], {}).get("edge_id")
        if not eid:
            i = 1
            while "RA" + str(i).zfill(4) in used_ids:
                i += 1
            eid = "RA" + str(i).zfill(4)
            used_ids.add(eid)
        e = dict(edge_id=eid, type=p["label"], decision_id=p["pair_id"], conditions=p.get("conditions", []), review_status="pending")
        if p["label"] == "refinement":
            e.update(parent_id=p["parent_id"], child_id=p["child_id"], interpretation=p["interpretation"])
        else:
            e.update(a=p["a"], b=p["b"])
        result["edges"].append(e)
    result["relation_coverage"] = dict(strategy="all_pairs", expected_pairs=len(pairs),
        evaluated_pairs=sum(p.get("assessment_status") != "not_run" for p in pairs.values()),
        unassessed_pair_ids=[p["pair_id"] for p in pairs.values() if p.get("assessment_status") == "not_run"])
    resolved_ids = pair_ids | {gid for gid in goal_ids if goals[gid]["trace_status"] in {"direct", "inferred"}}
    result["issues"] = [i for i in result["issues"] if i.get("code") != "uncertain_relation" and not (
        i.get("code") in {"needs_retrace", "retrace", "unassessed_relation"} and i.get("target_ids") and set(i["target_ids"]).issubset(resolved_ids))]
    result["issues"].extend(trace_issues)
    result["issues"].extend(dict(code="uncertain_relation", severity="needs_review", target_ids=[p["a"], p["b"]], reason=p["rationale"])
                            for p in pairs.values() if p["label"] in {"uncertain", "equivalent"} and p.get("assessment_status") != "not_run")
    result["parent_version"], result["version"] = model["version"], model["version"] + ".a1"
    result["changes"].append(dict(kind="reassessment_merge", parent_core_sha256=core_hash(model), artifacts=additions,
        evidence_id_mapping=evidence_map, updated_goal_ids=sorted(goal_ids), updated_pair_ids=sorted(pair_ids),
        before_goals=copy.deepcopy(model["goals"]), before_pairs=copy.deepcopy(model["pair_decisions"]), before_edges=copy.deepcopy(model["edges"])))
    result.pop("content_sha256", None)
    result["review"] = dict(status="pending", records=copy.deepcopy(model["review"].get("records", [])),
                            feedback_artifacts=copy.deepcopy(model["review"].get("feedback_artifacts", [])))
    result["validation"] = dict(structure_status="not_run", semantic_status="not_run", report_path=None)
    result["delivery"].update(mode="reassessment", readiness="unchecked", files=[])
    check_structure(result)  # Includes cycles, graph direction, counts and unknown references.
    record = dict(schema_version="goalforge-reassessment-record-1", base_model=binding, output_version=result["version"],
        goal_ids=sorted(goal_ids), pair_ids=sorted(pair_ids), evidence_id_mapping=evidence_map, artifacts=additions,
        remaining_goal_ids=[g["goal_id"] for g in result["goals"] if g.get("trace_status") not in {"direct", "inferred"}],
        remaining_pair_ids=[p["pair_id"] for p in pairs.values() if p.get("trace_status") == "needs_retrace" or p.get("assessment_status") == "not_run"],
        model_calls=0, human_review="pending", independent_semantic_review="not_run")
    return result, record, attachments


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output_dir", type=Path, nargs="?")
    parser.add_argument("--retrace-input", type=Path)
    parser.add_argument("--tracing", type=Path)
    parser.add_argument("--judgments", type=Path)
    parser.add_argument("--relations", type=Path)
    parser.add_argument("--relation-template", type=Path, help="Write blank version-bound relation decisions; no model is updated")
    args = parser.parse_args()
    if args.relation_template:
        if args.output_dir or args.retrace_input or args.tracing or args.judgments or args.relations:
            parser.error("Template mode cannot be combined with reassessment inputs/output")
        _, model = read_input(args.input)
        args.relation_template.parent.mkdir(parents=True, exist_ok=True)
        with args.relation_template.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(relation_template(model), handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        return
    if args.output_dir is None:
        parser.error("A fresh output directory is required")
    if args.output_dir.exists() and any(args.output_dir.iterdir()):
        raise ValueError("Use a fresh output directory")
    _, model = read_input(args.input)
    result, record, attachments = reconcile(model, args.input.parent, args.retrace_input, args.tracing, args.judgments, args.relations)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for relative, raw in attachments.items():
        path = args.output_dir / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    raw = encode(result)
    (args.output_dir / "reconciled-model.json").write_bytes(raw)
    report = inspect(result, args.output_dir, sha(raw))
    record["check_summary"] = report["summary"]
    (args.output_dir / "review-report.json").write_bytes(encode(report))
    (args.output_dir / "model-review.md").write_text(markdown(report), encoding="utf-8")
    (args.output_dir / "reassessment-record.json").write_bytes(encode(record))
    lines = ["# 重新判断结果回填记录", "", "原模型：" + model["version"], "新版本：" + result["version"],
             "", "已回填目标：" + ", ".join(record["goal_ids"]), "已回填关系：" + ", ".join(record["pair_ids"]),
             "", "仍需核对目标：" + ", ".join(record["remaining_goal_ids"]), "仍需重评关系：" + ", ".join(record["remaining_pair_ids"]),
             "", "结构检查：" + report["summary"]["structure_status"], "人工状态：pending；独立语义审查：not_run。", "",
             "新判断来自输入文件，工具未调用模型；回填和复检不等于人工采纳。原模型与来源映射保留。", ""]
    (args.output_dir / "reassessment-review.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(dict(version=result["version"], checks=report["summary"], remaining_pairs=record["remaining_pair_ids"])))


if __name__ == "__main__":
    main()
