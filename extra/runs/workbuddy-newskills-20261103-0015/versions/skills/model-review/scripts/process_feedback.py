"""Validate exported human opinions, plan routes, optionally create a checked model copy."""
import argparse
import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from review_model import artifact_bytes, encode, inspect, markdown
from feedback_contract import changes, validate
from export_model import report_hash, review_target_hash
from export_model import core_hash
from revise_model import revise


def handoff(model, attachments):
    goals = [g for g in model["goals"] if g.get("trace_status") == "needs_retrace"]
    pairs = [p for p in model["pair_decisions"] if p.get("trace_status") == "needs_retrace" or p.get("assessment_status") == "not_run"]
    binding = dict(model_id=model["model_id"], version=model["version"], core_sha256=core_hash(model))
    tasks = dict(schema_version="goalforge-review-tasks-1", target_model=binding, goal_ids=[g["goal_id"] for g in goals],
                 pair_ids=[p["pair_id"] for p in pairs], relations=copy.deepcopy(pairs),
                 instructions="先重新判断目标证据支持，再评估列出的关系；不得以旧判断或none填充未评估项。")
    extraction = json.loads(attachments["attachments/extraction.json"].decode("utf-8")) if "attachments/extraction.json" in attachments else None
    if not goals or extraction is None or "attachments/source.txt" not in attachments:
        tasks["retrace_input_status"] = "not_needed" if not goals else "source_segments_unavailable"
        return tasks, None
    evidence = {e["evidence_id"]: e for e in model["evidence_index"]}
    data = {k: copy.deepcopy(extraction[k]) for k in ("schema_version", "document_id", "materials", "conversion", "segments") if k in extraction}
    data.update(document_hash=hashlib.sha256(attachments["attachments/source.txt"]).hexdigest(), target_kind="goal", target_model=binding, candidates=[])
    for g in goals:
        refs = []
        for eid in g["evidence_ids"]:
            e = evidence[eid]
            refs.append(dict(source_id=e["source_id"], quote=e["quote"], role="context" if e.get("evidence_role") == "context" else "basis",
                             start_char=e.get("start_char"), end_char=e.get("end_char"), original_evidence_id=eid))
        data["candidates"].append(dict(candidate_id=g["goal_id"], category="goal", statement=g["statement"], origin=g["origin"],
            actor=g["actor"], context=g["context"], evidence_candidates=refs, review_status="pending"))
    tasks["retrace_input_status"] = "prepared"
    return tasks, data


def plan(model, packet):
    errors = validate(packet, model, submitted=True)
    if errors:
        raise ValueError("; ".join(errors))
    routes = []
    for e in packet["entries"]:
        decision, kind = e["decision"], e["target_type"]
        target = ("goal-extraction" if (kind == "goal" and decision in {"modify", "exclude", "merge", "split"}
            or decision == "add_goal") else "goal-model-building" if kind == "relation" and decision == "modify" else None)
        if kind == "evidence" and decision != "sufficient":
            goal_refs = any(e["target_id"] in g["evidence_ids"] for g in model["goals"])
            pair_refs = any(e["target_id"] in p.get("evidence_ids", []) for p in model["pair_decisions"])
            target = "goal-extraction" if goal_refs else "goal-model-building" if pair_refs else None
        routes.append(dict(entry_id=e["entry_id"], target_id=e["target_id"], next_skill=target,
                           status="proposed" if target else "needs_human_decision" if decision == "defer" else "record_only"))
    return dict(schema_version="goalforge-feedback-processing-1", feedback_id=packet["feedback_id"], base_model=packet["base_model"],
                mode="plan", routes=routes, overall_decision=packet["overall"]["decision"], model_modified=False,
                limitations=["审核人名称为自填，不是身份验证。", "人工认可不替代语义正确性证明。"])


def apply(model, packet, base):
    processing = plan(model, packet)
    raw, problems = artifact_bytes(model, base)
    if problems:
        raise ValueError("; ".join(problems))
    if any(r.get("feedback_id") == packet["feedback_id"] for r in model["review"].get("records", [])):
        raise ValueError("Feedback already processed; do not apply twice")
    semantic_operations = any(changes(e) and e["decision"] != "defer" for e in packet["entries"])
    if semantic_operations:
        result, routes, modified = revise(model, packet)
        processing["routes"] = routes
    else:
        result, modified = copy.deepcopy(model), False
    whole_accept = packet["overall"]["decision"] == "accept"
    if whole_accept:
        executed = inspect(model, base)
        if executed["summary"]["structure_status"] != "passed" or executed["summary"]["blocking_count"]:
            raise ValueError("Whole-model acceptance blocked by actual checks")
        if modified:
            raise ValueError("Changed model requires a new human review")
    digest = report_hash(packet)
    path = "attachments/human-feedback-" + digest[:16] + ".json"
    data = encode(packet)
    raw[path] = data
    record = dict(feedback_id=packet["feedback_id"], feedback_sha256=digest, feedback_path=path,
                  base_model=copy.deepcopy(packet["base_model"]), reviewer=copy.deepcopy(packet["reviewer"]),
                  entries=copy.deepcopy(packet["entries"]), overall=copy.deepcopy(packet["overall"]),
                  imported_at=datetime.now(timezone.utc).isoformat(), applied_to_version=result["version"])
    result["review"].setdefault("records", []).append(record)
    result["review"].setdefault("feedback_artifacts", []).append(dict(path=path, sha256=hashlib.sha256(data).hexdigest()))
    result["review"]["status"] = "accepted" if whole_accept else "pending" if modified else "partial"
    result["review"].pop("acceptance", None)
    if whole_accept:
        result["review"]["acceptance"] = dict(feedback_id=packet["feedback_id"], feedback_path=path,
            feedback_sha256=digest, review_target_sha256=review_target_hash(result), hash_rule_version="goalforge-review-target-v1")
    result.pop("content_sha256", None)
    result["validation"] = dict(structure_status="not_run", semantic_status="not_run", report_path=None)
    result["delivery"].update(readiness="unchecked", mode="human_feedback", files=[])
    processing.update(mode="apply", model_modified=modified, output_version=result["version"], human_review=result["review"]["status"],
                      feedback_artifact=path, semantic_status="not_run")
    # Include feedback bytes before inspecting the new core. Source attachments remain immutable.
    return result, processing, raw


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("feedback", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if args.output_dir.exists() and any(args.output_dir.iterdir()):
        raise ValueError("Use a fresh output directory")
    model = json.loads(args.input.read_text(encoding="utf-8-sig"))
    if args.feedback.stat().st_size > 5 * 1024 * 1024:
        raise ValueError("Feedback file exceeds 5MB")
    packet = json.loads(args.feedback.read_text(encoding="utf-8-sig"))
    processing = plan(model, packet)
    if args.apply:
        result, processing, attachments = apply(model, packet, args.input.parent)
        args.output_dir.mkdir(parents=True)
        for relative, data in attachments.items():
            target = args.output_dir / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        data = encode(result)
        (args.output_dir / "feedback-model.json").write_bytes(data)
        report = inspect(result, args.output_dir, hashlib.sha256(data).hexdigest())
        (args.output_dir / "review-report.json").write_bytes(encode(report))
        (args.output_dir / "model-review.md").write_text(markdown(report), encoding="utf-8")
        processing["check_summary"] = report["summary"]
        tasks, retrace = handoff(result, attachments)
        (args.output_dir / "review-tasks.json").write_bytes(encode(tasks))
        if retrace is not None:
            (args.output_dir / "retrace-input.json").write_bytes(encode(retrace))
    else:
        args.output_dir.mkdir(parents=True)
    (args.output_dir / "feedback-processing.json").write_bytes(encode(processing))
    lines = ["# 人工意见处理结果", "", "模式：" + processing["mode"], "", "原模型保留。意见记录、实际修改、待追溯及待评估分别列出。", ""]
    for route in processing["routes"]:
        lines.append("- " + route["entry_id"] + "：" + route["status"] + "；后续：" + str(route["next_skill"]))
    if args.apply:
        lines += ["", "输出版本：" + processing["output_version"], "人工状态：" + processing["human_review"],
                  "", "如有目标/关系/证据变化，旧认可不适用于新版本；支持失效项须重新追溯，不能称为语义修复完成。"]
    (args.output_dir / "feedback-processing.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(dict(mode=processing["mode"], modified=processing["model_modified"])))


if __name__ == "__main__":
    main()
