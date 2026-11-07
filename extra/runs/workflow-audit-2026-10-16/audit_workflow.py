"""Controlled CLI workflow audit. Fixtures/judgments are not model-quality evaluation."""
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUN = Path(__file__).resolve().parent / "native-text-smoke"
LOG = []


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def run(stage, script, *arguments, expected_failure=False):
    cmd = [sys.executable, str(ROOT / script)] + [str(x) for x in arguments]
    result = subprocess.run(cmd, cwd=str(ROOT), text=True, encoding="utf-8", capture_output=True)
    LOG.append(dict(stage=stage, command=cmd, returncode=result.returncode, stdout=result.stdout, stderr=result.stderr))
    if (result.returncode == 0) == expected_failure:
        raise RuntimeError(stage + ": unexpected exit code\n" + result.stderr)


def main():
    if RUN.exists():
        raise ValueError("Preserve prior audit; use a fresh run directory")
    RUN.mkdir(parents=True)
    source = RUN / "original.md"
    lines = ["使用者：我希望根据天气安排活动。", "使用者：我希望根据降雨安排户外活动。", "使用者：我希望减少查找信息的费用。"]
    source.write_bytes(("\n".join(lines) + "\n").encode("utf-8"))
    original_sha = hashlib.sha256(source.read_bytes()).hexdigest()
    run("prepare_native_source", "skills/goal-extraction/scripts/prepare_source.py", source, RUN / "source", "--document-id", "AUDIT")
    extraction = load(RUN / "source/source-input.json")
    statements = ["根据天气安排活动", "根据降雨安排户外活动", "减少查找信息的费用"]
    candidates = []
    for i, (statement, segment) in enumerate(zip(statements, extraction["segments"]), 1):
        loc = segment["original_locator"]
        candidates.append(dict(candidate_id=f"AUDIT-C{i:03}", category="goal", subtype="unspecified", statement=statement,
            origin="explicit", actor="使用者", context=[], evidence_candidates=[dict(source_id=segment["source_id"], quote=segment["text"], role="basis",
            start_char=loc["start_char"], end_char=loc["end_char"])], classification_reason="受控夹具预置期望结果，非实际模型提取评测。", inference=None, review_status="pending"))
    extraction.update(schema_version="goalforge-extraction-draft-2", status="completed", candidates=candidates, review_questions=[],
                      limitations=["受控合成资料；候选与语义判断预置，只验证阶段衔接。"])
    write(RUN / "extraction.json", extraction)
    run("render_candidates", "skills/goal-extraction/scripts/render_review.py", RUN / "extraction.json", RUN / "goal-candidates.md")
    judgments = {c["candidate_id"]: dict(label="direct", rationale="受控夹具预置直接表达；不是独立语义评测。",
        supported_parts=[c["statement"]], unsupported_parts=[], assumptions=[], reasoning_steps=[]) for c in candidates}
    write(RUN / "semantic-judgments.json", judgments)
    run("trace", "skills/goal-tracing/scripts/trace_candidates.py", RUN / "extraction.json", RUN / "tracing", "--source", RUN / "source/source.txt", "--judgments", RUN / "semantic-judgments.json")
    pairs = [dict(pair_id="P12", a="AUDIT-G001", b="AUDIT-G002", label="refinement", parent_id="AUDIT-G001", child_id="AUDIT-G002",
                  interpretation="scope_specialization", rationale="受控示例：降雨与户外活动是范围具体化。", evidence_ids=["E0001", "E0002"], conditions=[], review_status="pending"),
             dict(pair_id="P13", a="AUDIT-G001", b="AUDIT-G003", label="none", rationale="夹具未建立联系。", evidence_ids=[], conditions=[], review_status="pending"),
             dict(pair_id="P23", a="AUDIT-G002", b="AUDIT-G003", label="none", rationale="夹具未建立联系。", evidence_ids=[], conditions=[], review_status="pending")]
    write(RUN / "relation-decisions.json", pairs)
    run("assemble", "skills/goal-model-building/scripts/assemble_model.py", RUN / "extraction.json", RUN / "tracing/tracing.json", RUN / "relation-decisions.json", RUN / "assembled", "--source", RUN / "source/source.txt")
    run("inspect", "skills/model-review/scripts/review_model.py", RUN / "assembled/model-input.json", RUN / "inspection")
    run("finalize", "skills/goal-model-building/scripts/finalize_model.py", RUN / "assembled/model-input.json", RUN / "inspection/review-report.json", RUN / "delivery")
    model = load(RUN / "delivery/goal-model.json")
    sys.path.insert(0, str(ROOT / "skills/goal-model-building/scripts"))
    from export_model import feedback_binding
    packet = dict(schema_version="goalforge-review-feedback-1", feedback_id="AUDIT-EDIT-NOT-REAL-USER", base_model=feedback_binding(model),
        reviewer=dict(name="工程测试，不是真实人工验收"), created_at="2026-10-16T00:00:00+08:00", updated_at="2026-10-16T00:00:00+08:00", status="submitted", form_drafts={},
        entries=[dict(entry_id="AUDIT-E1", target_type="goal", target_id="AUDIT-G001", decision="modify", proposed=dict(statement="根据天气和时间安排活动"),
            reason="受控增加时间条件，验证原支持是否失效。", reviewed_at="2026-10-16T00:00:00+08:00")],
        overall=dict(decision="request_changes", full_scope_ack=False, acknowledge_limits=False, comment="受控CLI衔接测试"))
    write(RUN / "edit-feedback.json", packet)
    baseline = (RUN / "delivery/goal-model.json").read_bytes()
    run("feedback_plan", "skills/model-review/scripts/process_feedback.py", RUN / "delivery/goal-model.json", RUN / "edit-feedback.json", RUN / "feedback-plan")
    run("feedback_apply", "skills/model-review/scripts/process_feedback.py", RUN / "delivery/goal-model.json", RUN / "edit-feedback.json", RUN / "revision", "--apply")
    run("retrace_without_judgments", "skills/goal-tracing/scripts/trace_candidates.py", RUN / "revision/retrace-input.json", RUN / "retrace-pending", "--source", RUN / "revision/attachments/source.txt")
    run("finalize_blocked_revision", "skills/goal-model-building/scripts/finalize_model.py", RUN / "revision/feedback-model.json", RUN / "revision/review-report.json", RUN / "revision-delivery")
    run("reject_stale_report", "skills/goal-model-building/scripts/finalize_model.py", RUN / "revision/feedback-model.json", RUN / "inspection/review-report.json", RUN / "must-not-export", expected_failure=True)
    # Probe a known boundary: judgments currently bind IDs, not target statements/input hash.
    write(RUN / "unbound-old-judgment.json", {"AUDIT-G001": copy.deepcopy(judgments["AUDIT-C001"])})
    run("probe_reused_semantic_judgment", "skills/goal-tracing/scripts/trace_candidates.py", RUN / "revision/retrace-input.json", RUN / "unbound-judgment-probe", "--source", RUN / "revision/attachments/source.txt", "--judgments", RUN / "unbound-old-judgment.json")
    probe = load(RUN / "unbound-judgment-probe/tracing.json")
    pending = load(RUN / "retrace-pending/tracing.json")
    revised = load(RUN / "revision-delivery/goal-model.json")
    manifest = load(RUN / "delivery/delivery-manifest.json")
    checks = dict(initial_reviewable=model["delivery"]["readiness"] == "reviewable", initial_human_pending=model["review"]["status"] == "pending",
        revised_blocked=revised["delivery"]["readiness"] == "blocked", changed_goal_needs_retrace=revised["goals"][0]["trace_status"] == "needs_retrace",
        unassessed_pairs=len(revised["relation_coverage"]["unassessed_pair_ids"]) == 2,
        semantic_not_run_without_judgment=any(i["code"] == "semantic_not_run" for i in pending["traces"][0]["issues"]),
        original_model_preserved=(RUN / "delivery/goal-model.json").read_bytes() == baseline,
        original_source_preserved=hashlib.sha256(source.read_bytes()).hexdigest() == original_sha,
        manifest_valid=all(hashlib.sha256((RUN / "delivery" / p).read_bytes()).hexdigest() == sha for p, sha in manifest["files"].items()),
        stale_report_did_not_export=not (RUN / "must-not-export").exists())
    assert all(checks.values()), checks
    write(RUN / "audit-results.json", dict(evaluation_type="controlled_cli_handoff_not_semantic_accuracy", checks=checks,
        confirmed_findings=[dict(id="A01", subject="Unbound semantic judgment reuse", reproduced=probe["traces"][0]["support"]["label"] == "direct",
        description="旧语义判断按ID重投给增加时间条件的新目标，工具仍接受direct。此为边界复现，不是可信追溯结果。"),
        dict(id="A02", subject="Reassessment return requires assistant-managed model update", description="已生成追溯输入及关系待办；目前没有自动回填修订模型的独立工具。")]))
    write(RUN / "commands.json", LOG)
    print(json.dumps(dict(checks=checks, unbound_semantic_judgment_reproduced=probe["traces"][0]["support"]["label"] == "direct")))


if __name__ == "__main__":
    main()
