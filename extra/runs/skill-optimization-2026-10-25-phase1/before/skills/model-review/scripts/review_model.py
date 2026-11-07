"""Inspect a frozen model and apply explicit, version-bound local patches to a copy."""

import argparse
import copy
import hashlib
import json
import sys
import time
from pathlib import Path

# The two project skills share integrity/hash rules, never semantic judgments.
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "goal-model-building/scripts"))
from export_model import check_structure, core_hash


def encode(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def artifact_bytes(model, base):
    """Read only declared, contained attachments. Never follow paths outside the package."""
    result, problems = {}, []
    root = Path(base).resolve() if base is not None else None
    for item in model.get("input_artifacts", []) + model.get("review", {}).get("feedback_artifacts", []):
        relative = item.get("path", "")
        if relative in result:
            problems.append("Duplicate attachment: " + relative)
            continue
        path = root / relative if root else None
        if not relative.startswith("attachments/") or (path and root not in path.resolve().parents):
            problems.append("Unsafe attachment path: " + relative)
            continue
        if not path or not path.is_file():
            problems.append("Missing attachment: " + relative)
            continue
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != item.get("sha256"):
            problems.append("Attachment hash mismatch: " + relative)
            continue
        result[relative] = raw
    return result, problems


def inspect(model, base=None, file_sha=None):
    checks, issues = [], []

    def issue(rule, reason, targets=None, kind="deterministic", severity="blocking", evidence=None):
        key = json.dumps([rule, targets or [], reason], ensure_ascii=False, sort_keys=True)
        iid = "I-" + hashlib.sha256(key.encode("utf-8")).hexdigest()[:12]
        issues.append(dict(issue_id=iid, rule_id=rule, type=kind, severity=severity,
                           target_ids=targets or [], evidence_ids=evidence or [], reason=reason,
                           suggested_action="核对问题对象与原始依据，保留修订记录。",
                           status="needs_review" if severity == "needs_review" else "open"))

    def checked(rule, status, detail, kind="deterministic"):
        checks.append(dict(check_id=rule, type=kind, scope="current_model", status=status,
                           evidence=detail, execution="python-stdlib" if kind == "deterministic" else "not_run"))

    try:
        check_structure(model)
        checked("integrity", "passed", "共享契约、ID、引用、边方向、有向环和关系覆盖检查。")
    except (KeyError, TypeError, ValueError, RecursionError) as error:
        issue("integrity", str(error))
        checked("integrity", "failed", str(error))
    goals = model.get("goals", [])
    ids = {g.get("goal_id") for g in goals}
    scope = model.get("document_scope", {})
    documents = set(scope.get("document_ids", []))
    start = len(issues)
    if not documents or (len(documents) > 1 and not scope.get("cross_document_allowed")):
        issue("scope", "Document scope is empty or crosses documents without authorization")
    for e in model.get("evidence_index", []):
        source = e.get("source_id", "")
        if ":" in source and source.split(":", 1)[0] not in documents:
            issue("scope", "Evidence source outside document scope", [e.get("evidence_id")])
    checked("scope", "failed" if len(issues) > start else "passed", "检查声明的文档范围及证据来源。")
    start = len(issues)
    mappings = model.get("candidate_goal_mapping", [])
    for m in mappings:
        if m.get("goal_id") is not None and m["goal_id"] not in ids:
            issue("lineage", "Mapping references missing goal", [m.get("candidate_id")])
    for g in goals:
        gid = g.get("goal_id")
        for cid in g.get("source_candidate_ids", []):
            if not any(m.get("candidate_id") == cid and m.get("goal_id") == gid for m in mappings):
                issue("lineage", "Goal candidate mapping missing", [gid, cid])
        if not g.get("source_candidate_ids") and g.get("origin") != "design_extension":
            issue("lineage", "Source goal has no candidate lineage", [gid])
    checked("lineage", "failed" if len(issues) > start else "passed", "检查目标与候选双向映射；不自行补造映射。")
    start = len(issues)
    for p in model.get("pair_decisions", []):
        represented = [e for e in model.get("edges", []) if e.get("decision_id") == p.get("pair_id")]
        if p.get("label") in {"related", "refinement"} and len(represented) != 1:
            issue("representation", "Positive decision must have exactly one graph edge", [p.get("pair_id")])
        if p.get("trace_status") == "needs_retrace":
            issue("retrace", "Changed relation requires renewed evidence review", [p.get("pair_id")])
        if p.get("assessment_status") == "not_run":
            issue("unassessed_relation", "Relation has not been reassessed after node changes", [p.get("pair_id")])
    checked("representation", "failed" if len(issues) > start else "passed", "正向决策与可视化边一致。")
    start = len(issues)
    for g in goals:
        if not g.get("evidence_ids") or g.get("trace_status") not in {"direct", "inferred"}:
            issue("retrace", "Goal has missing or invalidated evidence support", [g.get("goal_id")])
    checked("trace_validity", "failed" if len(issues) > start else "passed", "检查既有支持状态；不重新推断语义支持。")
    raw, problems = artifact_bytes(model, base)
    for problem in problems:
        issue("attachments", problem)
    if not model.get("input_artifacts"):
        issue("attachments", "No source/input attachments declared")
    checked("attachments", "failed" if problems or not model.get("input_artifacts") else "passed", "核对附件安全路径、可取得性和实际字节哈希。")
    start = len(issues)
    review = model.get("review", {})
    for record in review.get("records", []):
        try:
            packet = json.loads(raw[record["feedback_path"]].decode("utf-8"))
            from export_model import report_hash
            if (record["feedback_sha256"] != report_hash(packet) or record["feedback_id"] != packet["feedback_id"]
                or any(record[k] != packet[k] for k in ("entries", "overall", "reviewer", "base_model"))):
                raise ValueError("Human record differs from actual feedback")
        except (KeyError, TypeError, ValueError, UnicodeDecodeError):
            issue("human_records", "Human review record is missing or differs from feedback attachment")
    if review.get("status") == "partial" and not review.get("records"):
        issue("human_records", "Partial review requires actual human feedback records")
    if review.get("status") == "accepted":
        try:
            from feedback_contract import approval_valid
            packet = json.loads(raw[review["acceptance"]["feedback_path"]].decode("utf-8"))
            if not approval_valid(model, packet):
                raise ValueError("Approval no longer covers this model")
        except (KeyError, TypeError, ValueError, UnicodeDecodeError):
            issue("human_records", "Whole-model acceptance missing or stale")
    checked("human_records", "failed" if len(issues) > start else "passed", "只核对已提供意见的文件与版本绑定，不认证审核人身份。")
    # Source text is explicitly declared by assembly as attachments/source.txt.
    source = raw.get("attachments/source.txt")
    if source is None:
        issue("source_location", "Canonical source text unavailable")
        checked("source_location", "not_run", "缺少标准全文，不能重新验证引文偏移。")
    else:
        start = len(issues)
        try:
            text = source.decode("utf-8")
            for e in model.get("evidence_index", []):
                a, b = e.get("start_char"), e.get("end_char")
                if (not isinstance(a, int) or isinstance(a, bool) or not isinstance(b, int) or isinstance(b, bool)
                    or not 0 <= a < b <= len(text) or text[a:b] != e.get("quote")):
                    issue("source_location", "Quote/Unicode offsets differ from canonical source", [e.get("evidence_id")], evidence=[e.get("evidence_id")])
            checked("source_location", "failed" if len(issues) > start else "passed", "按 Unicode 码点和半开区间核对原句。")
        except UnicodeDecodeError:
            issue("source_location", "Source is not UTF-8")
            checked("source_location", "failed", "源文编码错误。")
    # Existing semantic doubts remain visible, including uncertainty that is not an error.
    for original in model.get("issues", []):
        issue("model_" + original.get("code", "issue"), original.get("reason", "Existing model issue"),
              original.get("target_ids", []), "semantic", original.get("severity", "needs_review"))
    for p in model.get("pair_decisions", []):
        if p.get("label") in {"uncertain", "equivalent"}:
            if not any(i["type"] == "semantic" and set(i["target_ids"]) == {p.get("a"), p.get("b")} for i in issues):
                issue("unresolved_relation", "关系尚需人工判断：" + p["label"], [p.get("pair_id")], "semantic", "needs_review")
    checked("semantic", "not_run", "未调用独立语义审查模型；只保留上游判断与待审项。", "semantic")
    structure = "failed" if any(i["type"] == "deterministic" and i["severity"] == "blocking" for i in issues) else "passed"
    core = core_hash(model)
    return dict(schema_version="model-review-draft-1", report_id="REVIEW-" + core[:16], mode="inspect",
                input_model=dict(file_sha256=file_sha, model_id=model.get("model_id"), version=model.get("version"),
                                 core_sha256=core, hash_rule_version="goalforge-core-v1"),
                checks=checks, issues=issues,
                summary=dict(structure_status=structure, semantic_status="not_run", goal_count=len(goals),
                             pair_count=len(model.get("pair_decisions", [])), blocking_count=sum(i["severity"] == "blocking" for i in issues),
                             needs_review_count=sum(i["severity"] == "needs_review" for i in issues)),
                repair_attempts=[], unresolved_issue_ids=[i["issue_id"] for i in issues],
                limitations=["结构检查不证明语义正确。", "未执行独立语义审查；模型人工状态来自实际反馈，检查报告自身未获人工确认。"],
                model_human_review_status=model.get("review", {}).get("status", "pending"), review_status="pending")


FIELDS = {"goal": ("goals", "goal_id", {"statement", "origin", "actor", "context", "evidence_ids"}),
          "pair": ("pair_decisions", "pair_id", {"label", "a", "b", "parent_id", "child_id", "rationale", "conditions", "evidence_ids"}),
          "edge": ("edges", "edge_id", {"a", "b", "parent_id", "child_id", "type", "decision_id", "conditions"}),
          "evidence": ("evidence_index", "evidence_id", {"start_char", "end_char", "quote", "source_id", "original_locator"})}


def propose(model, report):
    """Only a uniquely determined count correction; never choose semantic edits."""
    goals = {g["goal_id"] for g in model["goals"]}
    pairs = {frozenset((p["a"], p["b"])) for p in model["pair_decisions"]}
    expected = len(goals) * (len(goals) - 1) // 2
    coverage = model["relation_coverage"]
    if (coverage.get("strategy") != "all_pairs" or len(pairs) != expected or len(pairs) != len(model["pair_decisions"])
        or any(len(p) != 2 or not p.issubset(goals) for p in pairs)):
        return []
    corrected = dict(coverage, expected_pairs=expected,
                     evaluated_pairs=sum(p.get("assessment_status") != "not_run" for p in model["pair_decisions"]))
    related = [i["issue_id"] for i in report["issues"] if i["rule_id"] == "integrity" and "coverage" in i["reason"].lower()]
    if corrected == coverage or not related:
        return []
    return [dict(patch_id="PATCH-coverage", issue_ids=related, base_version=model["version"],
                 base_core_sha256=core_hash(model), rationale="现有唯一目标对完整，只纠正统计数，不补造关系。",
                 expected_checks=["integrity"], application_status="proposed",
                 operations=[dict(action="replace", entity="model", id=None, field="relation_coverage", before=coverage, after=corrected)])]


def repair(model, patches, base=None):
    """One atomic transaction per call; at most two retained repair rounds."""
    started = time.monotonic()
    before = inspect(model, base)
    result = copy.deepcopy(model)
    attempt = dict(attempt_id="A" + str(len(model.get("changes", [])) + 1), patch_ids=[],
                   before_version=model["version"], before_core_sha256=core_hash(model), status="rolled_back",
                   model_calls=0, token_usage=None, stop_reason=None)
    try:
        if len([c for c in model.get("changes", []) if c.get("kind") == "local_repair"]) >= 2:
            raise ValueError("Repair round budget exhausted (2)")
        if not patches:
            raise ValueError("No patch supplied")
        issue_ids = set(before["unresolved_issue_ids"])
        touched = set()
        for patch in patches:
            if patch["base_version"] != model["version"] or patch["base_core_sha256"] != core_hash(model):
                raise ValueError("Stale patch version or core hash")
            if not patch.get("issue_ids") or not set(patch["issue_ids"]).issubset(issue_ids):
                raise ValueError("Patch must reference current issue IDs")
            if not patch.get("rationale") or not patch.get("expected_checks"):
                raise ValueError("Patch requires rationale and expected checks")
            attempt["patch_ids"].append(patch["patch_id"])
            if len(set(attempt["patch_ids"])) != len(attempt["patch_ids"]):
                raise ValueError("Duplicate patch ID")
            for op in patch["operations"]:
                key = (op["entity"], op.get("id"), op["field"])
                if key in touched:
                    raise ValueError("Conflicting operations")
                touched.add(key)
                if op.get("action") != "replace":
                    raise ValueError("Only explicit field replacement is implemented")
                if op["entity"] == "model" and op["field"] == "relation_coverage":
                    obj = result
                else:
                    collection, id_field, fields = FIELDS[op["entity"]]
                    if op["field"] not in fields:
                        raise ValueError("Field is outside patch whitelist")
                    matches = [x for x in result[collection] if x[id_field] == op["id"]]
                    if len(matches) != 1:
                        raise ValueError("Unknown or non-unique object")
                    obj = matches[0]
                if op["field"] not in obj or obj[op["field"]] != op["before"]:
                    raise ValueError("Patch precondition differs from current value")
                obj[op["field"]] = copy.deepcopy(op["after"])
                if op["entity"] == "goal":
                    obj["trace_status"] = "needs_retrace"
                    for p in result["pair_decisions"]:
                        if obj["goal_id"] in {p["a"], p["b"]}:
                            p["trace_status"] = "needs_retrace"
                elif op["entity"] in {"pair", "edge", "evidence"}:
                    # Field replacements in evidence/relations may change semantic meaning.
                    affected = {op["id"]} if op["entity"] == "pair" else set()
                    if op["entity"] == "edge":
                        affected.add(obj["decision_id"])
                        if op["field"] == "decision_id":
                            affected.add(op["before"])
                    if op["entity"] == "evidence":
                        for g in result["goals"]:
                            if op["id"] in g["evidence_ids"]:
                                g["trace_status"] = "needs_retrace"
                                affected.update(p["pair_id"] for p in result["pair_decisions"] if g["goal_id"] in {p["a"], p["b"]})
                        affected.update(p["pair_id"] for p in result["pair_decisions"] if op["id"] in p.get("evidence_ids", []))
                    for p in result["pair_decisions"]:
                        if p["pair_id"] in affected:
                            p["trace_status"] = "needs_retrace"
        # Compare actual domain changes before adding bookkeeping/version fields.
        if result == model:
            raise ValueError("No content improvement")
        result["parent_version"] = model["version"]
        result["version"] = model["version"] + ".r1"
        result.pop("content_sha256", None)
        result["validation"] = dict(structure_status="not_run", semantic_status="not_run", report_path=None)
        result["delivery"].update(mode="repair", readiness="blocked", files=[])
        result["changes"].append(dict(kind="local_repair", parent_core_sha256=core_hash(model), patches=copy.deepcopy(patches)))
        after = inspect(result, base)
        old = {i["issue_id"] for i in before["issues"] if i["severity"] == "blocking"}
        new = [i for i in after["issues"] if i["severity"] == "blocking" and i["issue_id"] not in old and i["rule_id"] != "retrace"]
        if new:
            raise ValueError("Patch introduces new blocking defects")
        resolved = issue_ids - set(after["unresolved_issue_ids"])
        # Semantic changes pending retrace are retained as proposals, never claimed fixed.
        if not resolved:
            raise ValueError("No issue improved; stop for human/source review")
        attempt.update(status="applied", after_version=result["version"], after_core_sha256=core_hash(result),
                       resolved_issue_ids=sorted(resolved), new_issue_ids=sorted(set(after["unresolved_issue_ids"]) - issue_ids), stop_reason="one_transaction_complete")
    except (KeyError, TypeError, ValueError) as error:
        result, after = copy.deepcopy(model), before
        attempt["stop_reason"] = str(error)
    attempt["elapsed_seconds"] = round(time.monotonic() - started, 6)
    after = copy.deepcopy(after)
    after["mode"] = "repair"
    after["repair_attempts"] = [attempt]
    return result, after, attempt


def markdown(report):
    safe = lambda x: str(x).replace("<", "&lt;").replace(">", "&gt;")
    lines = ["# 目标模型检查记录", "", "模型：" + safe(report["input_model"]["model_id"]) + " · " + safe(report["input_model"]["version"]),
             "", "结构检查：" + report["summary"]["structure_status"], "语义审查：" + report["summary"]["semantic_status"],
             "模型人工状态：" + report.get("model_human_review_status", "pending"), "检查报告自身人工确认：pending", "", "## 已执行与未执行的检查", ""]
    for c in report["checks"]:
        lines.append("- " + c["check_id"] + "：" + c["status"] + "。" + safe(c["evidence"]))
    lines += ["", "## 问题与待审事项", ""]
    for i in report["issues"]:
        lines += ["### " + i["issue_id"] + " · " + i["severity"], "", safe(", ".join(i["target_ids"])), "", safe(i["reason"]),
                  "", "人工决定：", "", "修改建议与审核意见：", ""]
    lines += ["## 修复记录", "", "```json", json.dumps(report["repair_attempts"], ensure_ascii=False, indent=2), "```", "", "## 限制", ""]
    lines += ["- " + safe(x) for x in report["limitations"]]
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--mode", choices=["inspect", "propose", "repair"])
    parser.add_argument("--patches", type=Path, help="Apply explicit patches in a copy; absent means inspect")
    args = parser.parse_args()
    if args.output_dir.exists() and any(args.output_dir.iterdir()):
        raise ValueError("Use a fresh output directory")
    raw = args.input.read_bytes()
    model = json.loads(raw.decode("utf-8-sig"))
    mode = args.mode or ("repair" if args.patches else "inspect")
    if mode == "repair" and not args.patches:
        raise ValueError("Repair requires an explicit patches file")
    if mode != "repair" and args.patches:
        raise ValueError("Patches are only accepted in repair mode")
    report = inspect(model, args.input.parent, hashlib.sha256(raw).hexdigest())
    report["mode"] = mode
    result = None
    patches = propose(model, report) if mode == "propose" else []
    if args.patches:
        patches = json.loads(args.patches.read_text(encoding="utf-8-sig"))
        result, report, attempt = repair(model, patches, args.input.parent)
        if attempt["status"] != "applied":
            result = None
    args.output_dir.mkdir(parents=True, exist_ok=True)
    if result is not None:
        raw_result = encode(result)
        (args.output_dir / "repaired-model.json").write_bytes(raw_result)
        report["input_model"]["file_sha256"] = hashlib.sha256(raw_result).hexdigest()
        attachments, problems = artifact_bytes(result, args.input.parent)
        for relative, data in attachments.items():
            path = args.output_dir / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    else:
        report["input_model"]["file_sha256"] = hashlib.sha256(raw).hexdigest()
    if args.patches or mode == "propose":
        (args.output_dir / "patches.json").write_bytes(encode(patches))
    (args.output_dir / "review-report.json").write_bytes(encode(report))
    (args.output_dir / "model-review.md").write_text(markdown(report), encoding="utf-8")
    print(json.dumps(report["summary"], ensure_ascii=True))


if __name__ == "__main__":
    main()
