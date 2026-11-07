"""Reproduce audit boundaries in isolated synthetic copies; no production/user edits."""
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = Path(__file__).resolve().parent
RUN = BASE / "boundary-probes"
sys.path.insert(0, str(ROOT / "skills/goal-model-building/scripts"))
sys.path.insert(0, str(ROOT / "skills/model-review/scripts"))
from export_model import feedback_binding
from review_model import inspect
from finalize_model import finalize
from process_feedback import apply


def main():
    if RUN.exists():
        raise ValueError("Use fresh probe outputs")
    RUN.mkdir(parents=True)
    original = json.loads((BASE / "native-text-smoke/delivery/goal-model.json").read_text(encoding="utf-8"))
    model = copy.deepcopy(original)
    evidence = copy.deepcopy(model["evidence_index"][0])
    evidence["evidence_id"] = "E-RELATION-ONLY"
    model["evidence_index"].append(evidence)
    model["pair_decisions"][0]["evidence_ids"] = ["E-RELATION-ONLY"]
    source_base = BASE / "native-text-smoke/delivery"
    ready = finalize(model, inspect(model, source_base), source_base, RUN / "relation-only-base")
    packet = dict(schema_version="goalforge-review-feedback-1", feedback_id="AUDIT-RELATION-EVIDENCE-DISPUTE", base_model=feedback_binding(ready),
        reviewer=dict(name="受控工程测试"), created_at="2026-10-16T00:00:00+08:00", updated_at="2026-10-16T00:00:00+08:00", status="submitted", form_drafts={},
        entries=[dict(entry_id="E1", target_type="evidence", target_id="E-RELATION-ONLY", decision="incorrect", proposed={},
            reason="受控质疑只由关系引用的证据，不是真实用户意见。", reviewed_at="2026-10-16T00:00:00+08:00")],
        overall=dict(decision="request_changes", full_scope_ack=False, acknowledge_limits=False, comment="边界复现"))
    revised, processing, attachments = apply(ready, packet, RUN / "relation-only-base")
    revised_base = RUN / "relation-only-result"
    revised_base.mkdir()
    for relative, data in attachments.items():
        path = revised_base / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    (revised_base / "feedback-model.json").write_text(json.dumps(revised, ensure_ascii=False, indent=2), encoding="utf-8")
    report = inspect(revised, revised_base)
    (revised_base / "review-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    relation = revised["pair_decisions"][0]
    evidence_gap = relation.get("trace_status") != "needs_retrace" and report["summary"]["structure_status"] == "passed"
    # Regenerate a copy containing a simulated hand-written review comment.
    md = RUN / "review-with-simulated-comment.md"
    token = "AUDIT_ONLY_SIMULATED_HUMAN_COMMENT"
    md.write_text("# Synthetic comment\n" + token + "\n", encoding="utf-8")
    before = hashlib.sha256(md.read_bytes()).hexdigest()
    cmd = [sys.executable, str(ROOT / "skills/goal-extraction/scripts/render_review.py"), str(BASE / "native-text-smoke/extraction.json"), str(md)]
    result = subprocess.run(cmd, cwd=str(ROOT), text=True, encoding="utf-8", capture_output=True)
    overwrite_gap = result.returncode == 0 and token not in md.read_text(encoding="utf-8")
    record = dict(evaluation_type="isolated_boundary_probes_not_natural_errors", findings=[
        dict(id="A03", name="Relation-only evidence dispute not invalidated", reproduced=evidence_gap,
             affected_pair=relation["pair_id"], actual_trace_status=relation.get("trace_status"), report_summary=report["summary"], routes=processing["routes"]),
        dict(id="A04", name="Existing candidate review Markdown overwritten", reproduced=overwrite_gap, command=cmd,
             returncode=result.returncode, before_sha256=before, after_sha256=hashlib.sha256(md.read_bytes()).hexdigest())])
    (RUN / "audit-results.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    assert evidence_gap and overwrite_gap, record
    print(json.dumps(record, ensure_ascii=True))


if __name__ == "__main__":
    main()
