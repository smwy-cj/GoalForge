"""Build run-index.jsonl and delivery-index.csv from actual artifacts.

Reads only status/technical data and generated models; it never feeds one task's
content into another task. Re-runnable: always regenerates from disk.
"""

import csv
import hashlib
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

EXP = Path(__file__).resolve().parents[1]
CST = timezone(timedelta(hours=8))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def attempt_record(attempt, task):
    rec = {"attempt_id": attempt.name, "path": str(attempt.relative_to(EXP)).replace("\\", "/")}
    summary_p = attempt / "attempt-summary.json"
    rec["has_spec"] = (attempt / "spec.json").exists()
    rec["has_self_review"] = (attempt / "self-review.md").exists()
    rec["has_repair_log"] = (attempt / "repair-log.md").exists()
    delivery = attempt / "delivery"
    rec["has_delivery"] = (delivery / "goal-model.json").exists() and (delivery / "manifest.json").exists()
    assembled = attempt / "assembled/model-input.json"
    rec["has_assembled"] = assembled.exists()
    if summary_p.exists():
        s = load(summary_p)
        rec.update({
            "status": "completed" if s["counts"] and rec["has_delivery"] else "failed",
            "started_at": s["started_at"], "finished_at": s["finished_at"],
            "calls": len(s["commands"]),
            "seconds": round(sum(c["seconds"] for c in s["commands"]), 1),
            "counts": s["counts"], "inspection": s["inspection"],
            "coverage_check": s["coverage_check"], "tracing_status": s["tracing_status"],
            "downgraded": s["declared_vs_effective_downgraded"], "warnings": s["warnings"],
            "source_txt_sha256": s["source_txt_sha256"], "windows": s["windows"],
            "command_exit_codes": [c["exit_code"] for c in s["commands"]],
            "failed_commands": [c["label"] for c in s["commands"] if c["exit_code"] != 0],
        })
        if rec["has_delivery"]:
            rec["delivery_files"] = {k: v for k, v in s["delivery_files"].items()
                                     if k.startswith("delivery/")}
            rec["final_model_sha256"] = s["delivery_files"].get("delivery/goal-model.json")
    else:
        # no harness summary: the session stopped before the pipeline finished.
        # With no artifacts at all this is an interruption, not a semantic failure.
        rec["status"] = "interrupted"
        rec["calls"] = None
        rec["seconds"] = None
        rec["counts"] = None
        stages = []
        if not rec["has_spec"]:
            stages.append("no spec.json written")
        if not rec["has_assembled"]:
            stages.append("no assembled model")
        stages.append("no attempt-summary.json (harness did not complete)")
        rec["failed_stage"] = "session interrupted before pipeline finished; " + "; ".join(stages)
        if assembled.exists():
            m = load(assembled)
            rec["counts"] = {"goals": len(m["goals"]), "relations": len(m.get("relations", [])),
                             "groups": len(m["refinement_groups"]),
                             "established_groups": sum(1 for g in m["refinement_groups"]
                                                       if g.get("status") == "supported" and g.get("completeness") == "complete")}
        rec["inspection"] = None
        rec["coverage_check"] = None
        rec["delivery_files"] = {}
    rec["input_sha256"] = task["input_sha256"]
    return rec


def main():
    manifest = load(EXP / "task-manifest.json")
    snapshot = load(EXP / "versions/manifest.json")["tree_sha256"]
    records = []
    for task in manifest["tasks"]:
        root = EXP / "main" / task["document_id"] / task["run_id"]
        cfg = load(root / "task.json") if (root / "task.json").exists() else {}
        attempts = sorted(p for p in root.glob("attempt-*") if p.is_dir())
        ars = [attempt_record(a, cfg) for a in attempts]
        finished = [a for a in ars if a.get("has_delivery")]
        first = next((a for a in ars if a.get("has_assembled")), None)
        last = finished[-1] if finished else (ars[-1] if ars else None)
        status = "pending" if not ars else (
            "completed" if finished else
            ("interrupted" if (ars[-1]["status"] == "interrupted") else "failed"))
        rec = {
            "task_id": task["task_id"], "document_id": task["document_id"],
            "run_id": task["run_id"], "order": task["order"],
            "attempt_id": last["attempt_id"] if last else None,
            "status": status,
            "attempt_count": len(ars),
            "repairs": max(0, len(ars) - 1),
            "engine": cfg.get("engine", "unknown"),
            "exact_model_id": cfg.get("exact_model_id", "unknown"),
            "temperature": cfg.get("temperature", "unknown"),
            "skill_snapshot": snapshot,
            "input_sha256": cfg.get("input_sha256", "unknown"),
            "prompt_revision": cfg.get("prompt_revision", "unknown"),
            "context_isolation": cfg.get("context_isolation", "unknown"),
            "planned_budget": cfg.get("planned_budget", "unknown"),
            "actual_usage": {"tool_calls": last.get("calls") if last else None,
                             "tokens": "unknown", "cost": "unknown",
                             "seconds": last.get("seconds") if last else None},
            "stop_reason": ("structural checks passed and delivery produced"
                            if status == "completed" else
                            (last or {}).get("failed_stage", "no attempt")),
            "started_at": (ars[0].get("started_at") if ars else None),
            "finished_at": (last.get("finished_at") if last else None),
            "counts": last.get("counts") if last else None,
            "inspection": last.get("inspection") if last else None,
            "coverage_check": last.get("coverage_check") if last else None,
            "downgraded": last.get("downgraded") if last else None,
            "warnings": last.get("warnings") if last else None,
            "first_submission_path": (f"{first['path']}/assembled/model-input.json" if first else None),
            "delivery_path": (f"{last['path']}/delivery" if last and last.get("has_delivery") else None),
            "delivery_manifest_sha256": (sha(EXP / last["path"] / "delivery/manifest.json")
                                         if last and last.get("has_delivery") else None),
            "self_review_path": (f"{last['path']}/self-review.md"
                                 if last and last.get("has_self_review") else None),
            "attempts": [{k: v for k, v in a.items() if k not in {"delivery_files"}} for a in ars],
        }
        records.append(rec)

    with (EXP / "run-index.jsonl").open("w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")

    cols = ["task_id", "document_id", "run_id", "order", "status", "attempts", "repairs",
            "goals", "relations", "candidate_groups", "established_groups",
            "direct", "inferred", "insufficient", "contradicted",
            "coverage_structure", "coverage_workflow", "inspect_structure", "readiness",
            "blocking_issues", "first_submission", "delivery", "delivery_manifest_sha256"]
    with (EXP / "delivery-index.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        for r in records:
            c = r["counts"] or {}
            lab = (c.get("support_labels") or {})
            w.writerow([r["task_id"], r["document_id"], r["run_id"], r["order"], r["status"],
                        r["attempt_count"], r["repairs"], c.get("goals"), c.get("relations"),
                        c.get("groups"), c.get("established_groups"),
                        lab.get("direct"), lab.get("inferred"), lab.get("insufficient"),
                        lab.get("contradicted"),
                        (r["coverage_check"] or {}).get("structure"),
                        (r["coverage_check"] or {}).get("workflow"),
                        (r["inspection"] or {}).get("structure"),
                        (r["inspection"] or {}).get("readiness"),
                        c.get("blocking_issues"),
                        r["first_submission_path"], r["delivery_path"], r["delivery_manifest_sha256"]])

    done = sum(1 for r in records if r["status"] == "completed")
    print(json.dumps({"tasks": len(records), "completed": done,
                      "failed": sum(1 for r in records if r["status"] == "failed"),
                      "interrupted": sum(1 for r in records if r["status"] == "interrupted"),
                      "pending": sum(1 for r in records if r["status"] == "pending")}, ensure_ascii=False))
    todo = sorted((r for r in records if r["status"] in ("pending", "interrupted")),
                  key=lambda r: r["order"])[:3]
    for r in todo:
        nxt = r["attempt_count"] + 1
        print(f"NEXT {r['task_id']} order={r['order']} status={r['status']} "
              f"next_attempt=attempt-{nxt:02d}")


if __name__ == "__main__":
    main()
