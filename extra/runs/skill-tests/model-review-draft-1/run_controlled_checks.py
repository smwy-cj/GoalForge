"""Reproducible controlled corruption; never a natural-model-error evaluation."""
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent / "controlled-count-repair"
SOURCE = ROOT / "runs/skill-tests/goal-model-building-draft-1/doc023-development/assembled"
REVIEW = ROOT / "skills/model-review/scripts/review_model.py"
FINALIZE = ROOT / "skills/goal-model-building/scripts/finalize_model.py"


def main():
    if RUN.exists():
        raise ValueError("Use a fresh controlled-run directory; preserve earlier results")
    original = (SOURCE / "model-input.json").read_bytes()
    before_sha = hashlib.sha256(original).hexdigest()
    model = json.loads(original)
    model["relation_coverage"]["evaluated_pairs"] = 999  # deliberate single defect
    RUN.mkdir(parents=True)
    shutil.copytree(SOURCE / "attachments", RUN / "attachments")
    (RUN / "injected-model.json").write_text(json.dumps(model, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    commands = [[sys.executable, str(REVIEW), str(RUN / "injected-model.json"), str(RUN / "proposal"), "--mode", "propose"],
                [sys.executable, str(REVIEW), str(RUN / "injected-model.json"), str(RUN / "repaired"), "--patches", str(RUN / "proposal/patches.json")],
                [sys.executable, str(FINALIZE), str(RUN / "repaired/repaired-model.json"), str(RUN / "repaired/review-report.json"), str(RUN / "delivery")]]
    executed = []
    for cmd in commands:
        result = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8")
        executed.append(dict(command=cmd, returncode=result.returncode, stdout=result.stdout, stderr=result.stderr))
        if result.returncode:
            raise RuntimeError(result.stderr)
    patches = json.loads((RUN / "proposal/patches.json").read_text(encoding="utf-8"))
    patches[0]["base_core_sha256"] = "deliberately-stale"
    (RUN / "stale-patches.json").write_text(json.dumps(patches, ensure_ascii=False, indent=2), encoding="utf-8")
    subprocess.run([sys.executable, str(REVIEW), str(RUN / "injected-model.json"), str(RUN / "rejected"), "--patches", str(RUN / "stale-patches.json")], cwd=str(ROOT), check=True)
    report = json.loads((RUN / "repaired/review-report.json").read_text(encoding="utf-8"))
    rejected = json.loads((RUN / "rejected/review-report.json").read_text(encoding="utf-8"))
    unchanged = hashlib.sha256((SOURCE / "model-input.json").read_bytes()).hexdigest() == before_sha
    assert unchanged
    assert report["summary"]["structure_status"] == "passed"
    assert report["repair_attempts"][0]["status"] == "applied"
    assert rejected["repair_attempts"][0]["status"] == "rolled_back"
    assert not (RUN / "rejected/repaired-model.json").exists()
    record = dict(evaluation_type="controlled_injection_not_natural_errors", injected_defect="evaluated_pairs=999",
                  original_model_sha256=before_sha, original_preserved=unchanged, executed=executed,
                  repair=report["repair_attempts"], rejected_patch=rejected["repair_attempts"], semantic_review="not_run",
                  human_review="pending", model_calls=0, token_usage=None)
    (RUN / "run-record.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Controlled repair, reinspection, finalize and stale-patch rollback passed; source preserved.")


if __name__ == "__main__":
    main()
