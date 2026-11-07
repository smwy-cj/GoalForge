"""Create one task workspace: source copy, brief, task.json. Idempotent."""

import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

EXP = Path(__file__).resolve().parents[1]
CST = timezone(timedelta(hours=8))
BRIEF = (EXP / "logs/brief-template.md").read_text(encoding="utf-8")


def prep(task_id, attempt_no=1):
    manifest = json.loads((EXP / "task-manifest.json").read_text(encoding="utf-8"))
    task = next(t for t in manifest["tasks"] if t["task_id"] == task_id)
    doc, run = task["document_id"], task["run_id"]
    root = EXP / "main" / doc / run
    attempt = root / f"attempt-{attempt_no:02d}"
    (attempt / "source").mkdir(parents=True, exist_ok=True)
    src = EXP / "inputs/source" / f"{doc}.json"
    target = attempt / "source" / f"{doc}.json"
    if not target.exists():
        shutil.copyfile(src, target)
    brief = (BRIEF.replace("<attempt_dir>", str(attempt).replace("\\", "/"))
             .replace("<EXP>", str(EXP).replace("\\", "/"))
             .replace("DOCxxx", doc))
    (attempt / "brief.md").write_text(brief, encoding="utf-8")
    config = {
        "task_id": task_id, "document_id": doc, "run_id": run, "order": task["order"],
        "attempt_id": f"attempt-{attempt_no:02d}",
        "prompt_revision": "task-prompt-v1",
        "skill_snapshot": json.loads((EXP / "versions/manifest.json").read_text(encoding="utf-8"))["tree_sha256"],
        "input_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
        "context_isolation": "isolated_session",
        "engine": "WorkBuddy isolated generation session",
        "exact_model_id": "unknown",
        "temperature": "unknown",
        "planned_budget": "1 initial pass + <=2 repair rounds; token budget unknown",
        "created_at": datetime.now(CST).isoformat(timespec="seconds"),
        "workspace": str(attempt).replace("\\", "/"),
    }
    (root / "task.json").write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"task_id": task_id, "workspace": str(attempt)}, ensure_ascii=False))


if __name__ == "__main__":
    for tid in sys.argv[1:]:
        name, _, no = tid.partition("#")
        prep(name, int(no) if no else 1)
