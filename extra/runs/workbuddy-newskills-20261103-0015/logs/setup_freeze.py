"""Freeze skills, inventory inputs, build the 102-task manifest.

Run from the repository root:
  python extra/runs/workbuddy-newskills-20261103-0015/logs/setup_freeze.py
"""

import hashlib
import json
import random
import shutil
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = ROOT / "extra/runs/workbuddy-newskills-20261103-0015"
SKILLS = ["goal-extraction", "goal-model-building", "model-review"]
SRC = ROOT / "datasets/processed/goalforge-v1/source"
CST = timezone(timedelta(hours=8))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    for name in ["versions/skills", "inputs/source", "main", "logs",
                 "fixed-goals", "challenges", "external"]:
        (EXP / name).mkdir(parents=True, exist_ok=True)

    # 1. freeze skills
    files = []
    for skill in SKILLS:
        src = ROOT / "skills" / skill
        dst = EXP / "versions/skills" / skill
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        for f in sorted(src.rglob("*")):
            if f.is_file():
                rel = f.relative_to(ROOT / "skills").as_posix()
                files.append({"path": rel, "sha256": sha(f), "bytes": f.stat().st_size})
    tree = hashlib.sha256(
        "\n".join(f"{e['path']}:{e['sha256']}" for e in files).encode()
    ).hexdigest()
    manifest = {
        "frozen_at": datetime.now(CST).isoformat(timespec="seconds"),
        "source_of_truth": "skills/ (repository working tree)",
        "skills": SKILLS,
        "retired_skills_excluded": ["goal-tracing"],
        "extraction_contract": "goalforge-extraction-3",
        "kaos_model_version": "goalforge-kaos-2",
        "file_count": len(files),
        "tree_sha256": tree,
        "files": files,
    }
    (EXP / "versions/manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # 2. input inventory
    docs = []
    for jp in sorted(SRC.glob("DOC*.json")):
        tp = jp.with_suffix(".txt")
        rec = json.loads(jp.read_text(encoding="utf-8"))
        docs.append({
            "document_id": rec["document_id"],
            "json_file": jp.name,
            "json_sha256": sha(jp),
            "txt_file": tp.name,
            "txt_sha256": sha(tp),
            "canonical_hash_recorded": rec["document_hash"],
            "canonical_hash_recomputed": hashlib.sha256(
                "".join(f"[{t['source_id'].split(':', 1)[1]}] {t['speaker']}: {t['text']}\n"
                        for t in rec["turns"]).encode()
            ).hexdigest(),
            "turns": len(rec["turns"]),
            "upstream_id": rec.get("upstream_id"),
            "txt_equals_canonical": tp.read_text(encoding="utf-8") == "".join(
                f"[{t['source_id'].split(':', 1)[1]}] {t['speaker']}: {t['text']}\n"
                for t in rec["turns"]),
        })
    ids = [d["document_id"] for d in docs]
    expected = [f"DOC{i:03d}" for i in range(3, 37)]
    inventory = {
        "checked_at": datetime.now(CST).isoformat(timespec="seconds"),
        "scope": "datasets/processed/goalforge-v1/source/",
        "document_count": len(docs),
        "file_count": len(docs) * 2,
        "document_ids_expected": expected,
        "document_ids_found": ids,
        "id_set_matches": ids == expected,
        "all_canonical_hashes_match": all(
            d["canonical_hash_recorded"] == d["canonical_hash_recomputed"] for d in docs),
        "all_txt_equal_canonical": all(d["txt_equals_canonical"] for d in docs),
        "json_txt_are_representations_of_same_document": True,
        "sample_unit_note": "34 interviews; JSON and TXT are two representations of the same document, counted once.",
        "total_turns": sum(d["turns"] for d in docs),
        "documents": docs,
        "excluded_from_generation": [
            "datasets/processed/goalforge-v1/development_reference/",
            "datasets/baselines/", "datasets/benchmarks/",
            "extra/output/", "extra/output1/",
            "全过程记录.md", "论文结果对比与Skills 两轮修改总结.md",
            "other branches and prior run results",
        ],
    }
    (EXP / "inputs/input-inventory.json").write_text(
        json.dumps(inventory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # whitelisted read-only copy
    for d in docs:
        for f in (d["json_file"], d["txt_file"]):
            shutil.copy2(SRC / f, EXP / "inputs/source" / f)

    # 3. task manifest: 34 docs x 3 runs, interleaved by fixed seed
    tasks = [{"task_id": f"{d}-run{r:02d}", "document_id": d, "run_id": f"run{r:02d}"}
             for d in expected for r in (1, 2, 3)]
    random.Random(20261103).shuffle(tasks)
    for i, t in enumerate(tasks, 1):
        t["order"] = i
        t["output_dir"] = f"main/{t['document_id']}/{t['run_id']}"
    tm = {
        "created_at": datetime.now(CST).isoformat(timespec="seconds"),
        "task_count": len(tasks),
        "documents": len(expected),
        "runs_per_document": 3,
        "ordering": "interleaved; shuffled with fixed seed 20261103",
        "random_seed": 20261103,
        "extraction_contract": "goalforge-extraction-3",
        "kaos_model_version": "goalforge-kaos-2",
        "window_parameters": {"size": 4, "stride": 2, "unit": "turn"},
        "task_prompt_revision": "task-prompt-v1",
        "tasks": tasks,
    }
    (EXP / "task-manifest.json").write_text(
        json.dumps(tm, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # 4. initial status ledger
    with (EXP / "run-index.jsonl").open("w", encoding="utf-8") as fh:
        for t in tasks:
            fh.write(json.dumps({"task_id": t["task_id"], "document_id": t["document_id"],
                                 "run_id": t["run_id"], "order": t["order"],
                                 "attempt_id": None, "status": "pending",
                                 "updated_at": datetime.now(CST).isoformat(timespec="seconds")},
                                ensure_ascii=False) + "\n")
    print("frozen files:", len(files), "tree:", tree[:16])
    print("tasks:", len(tasks), "docs:", len(docs))


if __name__ == "__main__":
    main()
