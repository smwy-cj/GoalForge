"""Fresh controlled CLI verification of A01/A02/A03/A04; no real user acceptance."""
import copy
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUN = Path(__file__).resolve().parent / "integration"
sys.path.insert(0, str(ROOT / "skills/goal-model-building/scripts"))
from export_model import feedback_binding
from reconcile_model import model_binding

LOG = []


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def run(stage, script, *args, reject=False):
    cmd = [sys.executable, str(ROOT / script)] + [str(a) for a in args]
    r = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8")
    LOG.append(dict(stage=stage, command=cmd, returncode=r.returncode, stdout=r.stdout, stderr=r.stderr))
    if (r.returncode == 0) == reject:
        raise RuntimeError(stage + ": unexpected exit\n" + r.stderr)


TRACE = "skills/goal-tracing/scripts/trace_candidates.py"
INSPECT = "skills/model-review/scripts/review_model.py"
FINALIZE = "skills/goal-model-building/scripts/finalize_model.py"
FEEDBACK = "skills/model-review/scripts/process_feedback.py"
RECONCILE = "skills/goal-model-building/scripts/reconcile_model.py"


def judged(input_path, template_path, output_path, rationale):
    run("blank_bound_semantic_template", TRACE, input_path, "--judgment-template", template_path)
    template = load(template_path)
    for j in template["judgments"].values():
        j.update(label="direct", rationale=rationale, supported_parts=[j["target_statement"]])
    write(output_path, template)


def feedback(model, fid, kind, target, decision, proposed):
    return dict(schema_version="goalforge-review-feedback-1", feedback_id=fid, base_model=feedback_binding(model),
        reviewer=dict(name="工程测试夹具，不是真实人工验收"), created_at="2026-10-16T00:00:00+08:00", updated_at="2026-10-16T00:00:00+08:00", status="submitted", form_drafts={},
        entries=[dict(entry_id=fid + "-E1", target_type=kind, target_id=target, decision=decision, proposed=proposed, reason="受控修复验证。", reviewed_at="2026-10-16T00:00:00+08:00")],
        overall=dict(decision="request_changes", full_scope_ack=False, acknowledge_limits=False, comment="合成工程演练"))


def fill_relations(template_path, output_path, relation_only=False):
    data = load(template_path)
    for p in data["decisions"]:
        p.update(label="none", rationale="当前版本合成关系判断，未建立联系。", evidence_ids=[], conditions=[])
        if p["pair_id"] == "P12":
            p.update(label="refinement", parent_id="FIX-G001", child_id="FIX-G002", interpretation="scope_specialization",
                     rationale="重新核对新目标与原句后，保留降雨和户外活动的范围具体化（合成夹具）。",
                     evidence_ids=["REL-ONLY"] if relation_only else ["trace:E0001", "E0002"])
    write(output_path, data)


def main():
    if RUN.exists():
        raise ValueError("Preserve existing verification; use a new run folder")
    RUN.mkdir(parents=True)
    source = RUN / "original.md"
    lines = ["使用者：我希望根据天气合理安排活动。", "使用者：我希望根据降雨安排户外活动。", "使用者：我希望减少查找信息的费用。"]
    source.write_bytes(("\n".join(lines) + "\n").encode("utf-8"))
    original_raw = source.read_bytes()
    run("prepare", "skills/goal-extraction/scripts/prepare_source.py", source, RUN / "source", "--document-id", "FIX")
    extraction = load(RUN / "source/source-input.json")
    extraction.update(schema_version="goalforge-extraction-draft-2", status="completed", candidates=[], review_questions=[], limitations=["受控预置判断，仅检验衔接。"])
    statements = ["根据天气合理安排活动", "根据降雨安排户外活动", "减少查找信息的费用"]
    for i, (s, segment) in enumerate(zip(statements, extraction["segments"]), 1):
        loc = segment["original_locator"]
        extraction["candidates"].append(dict(candidate_id=f"FIX-C{i:03}", category="goal", subtype="unspecified", statement=s, origin="explicit", actor="使用者", context=[],
            evidence_candidates=[dict(source_id=segment["source_id"], quote=segment["text"], role="basis", start_char=loc["start_char"], end_char=loc["end_char"])],
            classification_reason="合成夹具预置目标。", inference=None, review_status="pending"))
    write(RUN / "extraction.json", extraction)
    run("candidate_review", "skills/goal-extraction/scripts/render_review.py", RUN / "extraction.json", RUN / "goal-candidates.md")
    marker = "\n受控模拟人工意见：请保留来源。\n"
    with (RUN / "goal-candidates.md").open("a", encoding="utf-8") as h:
        h.write(marker)
    before_md = (RUN / "goal-candidates.md").read_bytes()
    run("A04_refuse_overwrite", "skills/goal-extraction/scripts/render_review.py", RUN / "extraction.json", RUN / "goal-candidates.md", reject=True)
    judged(RUN / "extraction.json", RUN / "initial-template.json", RUN / "initial-judgments.json", "当前合成原句直接表达该目标，判断专属此版本。")
    run("trace_initial", TRACE, RUN / "extraction.json", RUN / "tracing", "--source", RUN / "source/source.txt", "--judgments", RUN / "initial-judgments.json")
    legacy_trace = load(RUN / "tracing/tracing.json")
    legacy_trace.pop("semantic_binding", None)
    write(RUN / "unbound-tracing.json", legacy_trace)
    pairs = [dict(pair_id="P12", a="FIX-G001", b="FIX-G002", label="refinement", parent_id="FIX-G001", child_id="FIX-G002", interpretation="scope_specialization",
                  rationale="合成范围具体化。", evidence_ids=["E0001", "E0002"], conditions=[], review_status="pending"),
             dict(pair_id="P13", a="FIX-G001", b="FIX-G003", label="none", rationale="未建立联系。", evidence_ids=[], conditions=[], review_status="pending"),
             dict(pair_id="P23", a="FIX-G002", b="FIX-G003", label="none", rationale="未建立联系。", evidence_ids=[], conditions=[], review_status="pending")]
    write(RUN / "relations.json", pairs)
    run("A01_assemble_refuses_unbound_tracing", "skills/goal-model-building/scripts/assemble_model.py", RUN / "extraction.json", RUN / "unbound-tracing.json", RUN / "relations.json", RUN / "must-not-assemble-unbound", "--source", RUN / "source/source.txt", reject=True)
    run("assemble", "skills/goal-model-building/scripts/assemble_model.py", RUN / "extraction.json", RUN / "tracing/tracing.json", RUN / "relations.json", RUN / "assembled", "--source", RUN / "source/source.txt")
    run("inspect_initial", INSPECT, RUN / "assembled/model-input.json", RUN / "inspection")
    run("deliver_initial", FINALIZE, RUN / "assembled/model-input.json", RUN / "inspection/review-report.json", RUN / "delivery")
    model = load(RUN / "delivery/goal-model.json")
    baseline = (RUN / "delivery/goal-model.json").read_bytes()
    write(RUN / "edit-feedback.json", feedback(model, "FIX-EDIT", "goal", "FIX-G001", "modify", dict(statement="根据天气安排活动")))
    run("apply_edit", FEEDBACK, RUN / "delivery/goal-model.json", RUN / "edit-feedback.json", RUN / "revision", "--apply")
    revised = load(RUN / "revision/feedback-model.json")
    judged(RUN / "revision/retrace-input.json", RUN / "new-template.json", RUN / "new-judgments.json", "重新阅读合成原句，删除修饰词后的新表述仍受支持；未沿用旧判断。")
    run("A01_refuse_initial_bound_judgment", TRACE, RUN / "revision/retrace-input.json", RUN / "must-not-trace-stale", "--source", RUN / "revision/attachments/source.txt", "--judgments", RUN / "initial-judgments.json", reject=True)
    write(RUN / "old-flat-judgments.json", {"FIX-G001": dict(label="direct", rationale="旧格式探针")})
    run("A01_refuse_unbound_judgment", TRACE, RUN / "revision/retrace-input.json", RUN / "must-not-trace-flat", "--source", RUN / "revision/attachments/source.txt", "--judgments", RUN / "old-flat-judgments.json", reject=True)
    run("retrace_current", TRACE, RUN / "revision/retrace-input.json", RUN / "retrace", "--source", RUN / "revision/attachments/source.txt", "--judgments", RUN / "new-judgments.json")
    run("blank_relation_template", RECONCILE, RUN / "revision/feedback-model.json", "--relation-template", RUN / "relation-template.json")
    fill_relations(RUN / "relation-template.json", RUN / "new-relations.json")
    run("A02_reconcile", RECONCILE, RUN / "revision/feedback-model.json", RUN / "reconciled", "--retrace-input", RUN / "revision/retrace-input.json", "--tracing", RUN / "retrace/tracing.json", "--judgments", RUN / "new-judgments.json", "--relations", RUN / "new-relations.json")
    run("deliver_reconciled", FINALIZE, RUN / "reconciled/reconciled-model.json", RUN / "reconciled/review-report.json", RUN / "delivery-reconciled")
    final = load(RUN / "delivery-reconciled/goal-model.json")
    record = load(RUN / "reconciled/reassessment-record.json")
    run("refuse_stale_report", FINALIZE, RUN / "reconciled/reconciled-model.json", RUN / "inspection/review-report.json", RUN / "must-not-deliver-old-report", reject=True)
    # A03: only a relation refers to REL-ONLY; no goal support should be changed.
    special = copy.deepcopy(model)
    ev = copy.deepcopy(special["evidence_index"][0])
    ev["evidence_id"] = "REL-ONLY"
    special["evidence_index"].append(ev)
    special["pair_decisions"][0]["evidence_ids"] = ["REL-ONLY"]
    special_base = RUN / "relation-only-input"
    shutil.copytree(RUN / "delivery/attachments", special_base / "attachments")
    write(special_base / "model.json", special)
    run("inspect_relation_only", INSPECT, special_base / "model.json", RUN / "relation-only-inspection")
    run("deliver_relation_only", FINALIZE, special_base / "model.json", RUN / "relation-only-inspection/review-report.json", RUN / "relation-only-ready")
    special_ready = load(RUN / "relation-only-ready/goal-model.json")
    write(RUN / "relation-only-feedback.json", feedback(special_ready, "FIX-REL", "evidence", "REL-ONLY", "incorrect", {}))
    run("A03_apply_dispute", FEEDBACK, RUN / "relation-only-ready/goal-model.json", RUN / "relation-only-feedback.json", RUN / "relation-only-revision", "--apply")
    special_revision = load(RUN / "relation-only-revision/feedback-model.json")
    special_report = load(RUN / "relation-only-revision/review-report.json")
    run("relation_only_template", RECONCILE, RUN / "relation-only-revision/feedback-model.json", "--relation-template", RUN / "relation-only-template.json")
    fill_relations(RUN / "relation-only-template.json", RUN / "relation-only-new-judgments.json", True)
    run("A03_reassess_relation_only", RECONCILE, RUN / "relation-only-revision/feedback-model.json", RUN / "relation-only-reconciled", "--relations", RUN / "relation-only-new-judgments.json")
    run("deliver_relation_only_fixed", FINALIZE, RUN / "relation-only-reconciled/reconciled-model.json", RUN / "relation-only-reconciled/review-report.json", RUN / "relation-only-final")
    checks = dict(A01_stale_bound_rejected=not (RUN / "must-not-trace-stale").exists(), A01_unbound_rejected=not (RUN / "must-not-trace-flat").exists(),
        A01_unbound_assembly_rejected=not (RUN / "must-not-assemble-unbound").exists(),
        A04_comments_preserved=(RUN / "goal-candidates.md").read_bytes() == before_md,
        A02_end_to_end_reviewable=final["delivery"]["readiness"] == "reviewable", A02_remaining_empty=not record["remaining_goal_ids"] and not record["remaining_pair_ids"],
        A02_mapping_preserved=final["candidate_goal_mapping"] == revised["candidate_goal_mapping"],
        A02_collision_remapped=record["evidence_id_mapping"]["E0001"] != "E0001" and any(e["evidence_id"] == "E0001" for e in final["evidence_index"]),
        A03_dispute_blocked=special_report["summary"]["structure_status"] == "failed" and special_report["summary"]["blocking_count"] > 0,
        A03_pair_invalidated=special_revision["pair_decisions"][0].get("trace_status") == "needs_retrace",
        A03_goals_unchanged=special_revision["goals"] == special_ready["goals"],
        A03_relation_only_completed=load(RUN / "relation-only-final/goal-model.json")["delivery"]["readiness"] == "reviewable",
        old_report_rejected=not (RUN / "must-not-deliver-old-report").exists(),
        source_preserved=source.read_bytes() == original_raw, model_preserved=(RUN / "delivery/goal-model.json").read_bytes() == baseline,
        no_fake_acceptance=final["review"]["status"] == "pending", independent_semantic_not_claimed=final["validation"]["semantic_status"] == "not_run")
    assert all(checks.values()), checks
    write(RUN / "verification-results.json", dict(evaluation_type="controlled_cli_fix_verification_not_semantic_accuracy", checks=checks, model_calls=0,
        final_version=final["version"], final_readiness=final["delivery"]["readiness"], evidence_id_mapping=record["evidence_id_mapping"]))
    write(RUN / "commands.json", LOG)
    print(json.dumps(dict(checks=checks, commands=len(LOG))))


if __name__ == "__main__":
    import argparse
    import re
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-name", default="integration")
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", args.run_name):
        parser.error("Run name must be a simple lowercase directory name")
    RUN = Path(__file__).resolve().parent / args.run_name
    main()
