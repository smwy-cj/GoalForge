"""Bind a matching executed review report and export one frozen model version."""

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path

from export_model import core_hash, export, report_hash

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "model-review/scripts"))
from review_model import artifact_bytes, inspect, markdown


def finalize(model, report, base, output_dir, input_bytes=None):
    binding = report.get("input_model", {})
    if (binding.get("core_sha256") != core_hash(model) or binding.get("version") != model["version"]
        or binding.get("model_id") != model["model_id"] or binding.get("hash_rule_version") != "goalforge-core-v1"):
        raise ValueError("Stale or mismatched review report")
    if input_bytes is not None and binding.get("file_sha256") != hashlib.sha256(input_bytes).hexdigest():
        raise ValueError("Review report file hash differs from input file")
    actual = inspect(model, base)
    # Rerun mechanical checks against real attachments; do not trust a passed string.
    actual_checks = [c for c in actual["checks"] if c["type"] == "deterministic"]
    given_checks = [c for c in report["checks"] if c["type"] == "deterministic"]
    actual_issues = [i for i in actual["issues"] if i["type"] == "deterministic"]
    given_issues = [i for i in report["issues"] if i["type"] == "deterministic"]
    if (actual_checks != given_checks or actual_issues != given_issues
        or actual["summary"]["structure_status"] != report["summary"]["structure_status"]):
        raise ValueError("Executed checks differ from supplied report")
    if report["summary"]["semantic_status"] != "not_run":
        raise ValueError("Independent semantic review ingestion is not implemented")
    if report.get("schema_version") != "model-review-draft-1" or report.get("review_status") != "pending":
        raise ValueError("Unsupported report schema or human review state")
    if any(i not in report["issues"] for i in actual["issues"] if i["type"] == "semantic"):
        raise ValueError("Existing semantic doubts must remain visible")
    result = copy.deepcopy(model)
    blocked = any(i["severity"] == "blocking" and i["status"] != "resolved" for i in report["issues"])
    attachments, problems = artifact_bytes(model, base)
    feedback = None
    if model["review"]["status"] == "accepted":
        from feedback_contract import approval_valid
        path = model["review"].get("acceptance", {}).get("feedback_path")
        if path not in attachments:
            raise ValueError("Human acceptance feedback attachment missing")
        feedback = json.loads(attachments[path].decode("utf-8"))
        if not approval_valid(model, feedback) or blocked or report["summary"]["structure_status"] != "passed":
            raise ValueError("Human acceptance is stale or checks are blocked")
    result["validation"] = dict(structure_status=report["summary"]["structure_status"],
                                semantic_status=report["summary"]["semantic_status"],
                                report_path="attachments/review-report.json", report_sha256=report_hash(report),
                                core_sha256=core_hash(model), hash_rule_version="goalforge-core-v1")
    result["delivery"].update(mode="finalize", readiness="reviewable" if not blocked and report["summary"]["structure_status"] == "passed" else "blocked")
    if result["review"]["status"] == "accepted":
        result["delivery"]["readiness"] = "accepted"
    result["delivery"]["limitations"] = [s for s in result["delivery"]["limitations"] if "model-review" not in s]
    result["delivery"]["limitations"].append("结构检查已绑定当前版本；独立语义审查未执行；人工状态以实际审核记录为准。")
    if problems:
        raise ValueError("Cannot package missing or altered attachments: " + "; ".join(problems))
    attachments["attachments/review-report.json"] = (json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    attachments["attachments/model-review.md"] = markdown(report).encode("utf-8")
    return export(result, output_dir, attachments, report=report, feedback=feedback)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("report", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    raw = args.input.read_bytes()
    model = json.loads(raw.decode("utf-8-sig"))
    report = json.loads(args.report.read_text(encoding="utf-8-sig"))
    result = finalize(model, report, args.input.parent, args.output_dir, raw)
    print(json.dumps(dict(readiness=result["delivery"]["readiness"], human_review=result["review"]["status"])))


if __name__ == "__main__":
    main()
