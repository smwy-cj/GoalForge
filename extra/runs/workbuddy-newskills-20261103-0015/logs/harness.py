"""Mechanical runner for one GoalForge task attempt.

The author (an isolated generation context) writes semantic content into spec.json.
This script only performs template generation, offset location, contract binding and
tool invocation. It never invents goals, judgments, relations or groups.

  python harness.py <attempt_dir>

<attempt_dir> must contain spec.json and DOCxxx source is copied from the frozen
whitelist. Outputs follow the frozen skill contracts unchanged.
"""

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

EXP = Path(__file__).resolve().parents[1]
SKILLS = EXP / "versions/skills"
PREPARE = SKILLS / "goal-extraction/scripts/prepare_source.py"
COVERAGE = SKILLS / "goal-extraction/scripts/check_coverage.py"
TRACE = SKILLS / "goal-extraction/scripts/trace_candidates.py"
KAOS = SKILLS / "goal-model-building/scripts/kaos_model.py"
CST = timezone(timedelta(hours=8))


def now():
    return datetime.now(CST).isoformat(timespec="seconds")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def dump(obj, path):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
                          encoding="utf-8")


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


class Runner:
    def __init__(self, attempt):
        self.attempt = Path(attempt).resolve()
        self.log = []
        self.warnings = []

    def run(self, argv, label, allow_fail=False):
        started = time.time()
        proc = subprocess.run([sys.executable, "-B", "-X", "utf8", *map(str, argv)],
                              capture_output=True, text=True, encoding="utf-8", errors="replace")
        entry = {"label": label, "argv": [Path(a).name if Path(str(a)).is_absolute() else str(a) for a in argv],
                 "exit_code": proc.returncode,
                 "seconds": round(time.time() - started, 2),
                 "stdout": proc.stdout[-4000:], "stderr": proc.stderr[-4000:]}
        self.log.append(entry)
        if proc.returncode != 0 and not allow_fail:
            raise RuntimeError(f"{label} failed ({proc.returncode}): {proc.stderr.strip()[-1500:]}")
        return proc


def locate(segments, source, sid, quote):
    """Return (start, end, occurrences) for a quote inside one verified segment."""
    seg = segments[sid]
    base = seg["original_locator"]["start_char"]
    if source[base:base + len(seg["text"])] != seg["text"]:
        raise ValueError(f"segment text does not match canonical source at {sid}")
    hits, start = [], seg["text"].find(quote)
    while start >= 0:
        hits.append(start)
        start = seg["text"].find(quote, start + 1)
    if not hits:
        raise ValueError(f"quote not in {sid}: {quote[:80]}")
    return base + hits[0], base + hits[0] + len(quote), len(hits)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("attempt", type=Path)
    args = parser.parse_args()
    r = Runner(args.attempt)
    a = r.attempt

    spec = load(a / "spec.json")
    doc = spec["document_id"]
    work = a / "work"
    work.mkdir(parents=True, exist_ok=True)
    started_at = now()

    # 1. assign the single whitelisted source
    src_dir = a / "source"
    src_dir.mkdir(exist_ok=True)
    target = src_dir / f"{doc}.json"
    inventory = load(EXP / "inputs/input-inventory.json")["documents"]
    known = {d["document_id"]: d["json_sha256"] for d in inventory}
    if doc in known:
        shutil.copyfile(EXP / "inputs/source" / f"{doc}.json", target)
    else:
        if not spec.get("synthetic"):
            raise RuntimeError(f"document {doc} is not in the frozen whitelist")
        target.write_bytes(Path(spec["synthetic_source"]).read_bytes())
    source_sha = sha(target)
    if doc in known and source_sha != known[doc]:
        raise RuntimeError("assigned source hash does not match frozen inventory")

    # 2. faithful source preparation, 4/2 windows
    r.run([PREPARE, target, work, "--window-size", 4, "--window-stride", 2], "prepare_source")
    source = (work / "source.txt").read_text(encoding="utf-8")
    prepared = load(work / "source-input.json")
    segments = {s["source_id"]: s for s in prepared["segments"]}
    windows = load(work / "source-windows.json")

    def ev(item):
        start, end, hits = locate(segments, source, item["source_id"], item["quote"])
        if hits > 1:
            r.warnings.append(f"ambiguous quote in {item['source_id']} ({hits} hits): {item['quote'][:60]}")
        return {"source_id": item["source_id"], "quote": item["quote"],
                "role": item.get("role", "basis"), "start_char": start, "end_char": end}

    # 3. raw candidates: template first (keeps tool-computed binding), then author content
    r.run([COVERAGE, "capture-template", "--source-input", work / "source-input.json",
           "--source", work / "source.txt", "--windows", work / "source-windows.json",
           "--output", work / "_tpl-candidates.json"], "capture_template")
    raw = load(work / "_tpl-candidates.json")
    (work / "_tpl-candidates.json").unlink()

    win_ids = {}
    for w in windows["windows"]:
        for sid in w["source_ids"]:
            win_ids.setdefault(sid, []).append(w["window_id"])

    raw_candidates = []
    for c in spec["raw_candidates"]:
        evidence = [ev(e) for e in c["evidence"]]
        refs = c.get("window_ids")
        if not refs:
            refs = []
            for e in evidence:
                for wid in win_ids.get(e["source_id"], []):
                    if wid not in refs:
                        refs.append(wid)
        raw_candidates.append({
            "candidate_id": c["candidate_id"], "statement": c["statement"],
            "actor": c.get("actor"), "modality": c.get("modality", "unknown"),
            "context": c.get("context", []), "origin": c.get("origin", "unknown"),
            "pass_id": c.get("pass_id", "P1"), "window_ids": refs,
            "evidence_candidates": evidence})
    raw["candidates"] = raw_candidates
    dump(raw, a / "raw-candidates.json")

    # 4. extraction (one goal = one core action)
    goals = []
    for g in spec["goals"]:
        goals.append({
            "candidate_id": g["candidate_id"], "statement": g["statement"],
            "actor": g.get("actor"), "context": g.get("context", []),
            "evidence_candidates": [ev(e) for e in g["evidence"]],
            "origin": g["origin"], "inference": g.get("inference"),
            "review_status": "pending"})
    extraction = {
        "schema_version": "goalforge-extraction-3", "document_id": doc,
        "document_hash": prepared["document_hash"], "status": spec.get("status", "completed"),
        "materials": prepared["materials"],
        "conversion": {"canonical_text_path": "source.txt",
                       "method": prepared["conversion"]["method"],
                       "issues": prepared["conversion"]["issues"]},
        "segments": prepared["segments"],
        "coverage": {"scope": "provided_material", "source_ids": prepared["coverage"]["source_ids"],
                     "omissions": spec.get("omissions", [])},
        "candidates": goals,
        "review_questions": spec.get("review_questions", []),
        "limitations": spec.get("limitations", [])}
    dump(extraction, a / "extraction.json")

    # 5. judgments, then read-only verification
    r.run([TRACE, a / "extraction.json", "--judgment-template", a / "judgments.json"], "judgment_template")
    judg = load(a / "judgments.json")
    for g in spec["goals"]:
        j = judg["judgments"].get(g["candidate_id"])
        if j is None:
            raise RuntimeError(f"unknown goal in spec: {g['candidate_id']}")
        j.update(label=g["judgment"]["label"], rationale=g["judgment"]["rationale"],
                 supported_parts=g["judgment"].get("supported_parts", []),
                 unsupported_parts=g["judgment"].get("unsupported_parts", []),
                 assumptions=g["judgment"].get("assumptions", []),
                 reasoning_steps=g["judgment"].get("reasoning_steps", []))
    dump(judg, a / "judgments.json")
    r.run([TRACE, a / "extraction.json", a / "tracing", "--source", work / "source.txt",
           "--judgments", a / "judgments.json"], "trace_candidates")
    tracing = load(a / "tracing/tracing.json")
    effective = {t["target_id"]: t["support"]["label"] for t in tracing["traces"]}
    downgraded = [gid for gid, lab in effective.items()
                  if lab not in {"direct", "inferred"}
                  and next(x["judgment"]["label"] for x in spec["goals"] if x["candidate_id"] == gid) in {"direct", "inferred"}]

    # 6. coverage ledger
    r.run([COVERAGE, "template", "--source-input", work / "source-input.json",
           "--source", work / "source.txt", "--windows", work / "source-windows.json",
           "--candidates", a / "raw-candidates.json", "--extraction", a / "extraction.json",
           "--output", a / "extraction-ledger.json"], "ledger_template")
    ledger = load(a / "extraction-ledger.json")
    led = spec["ledger"]
    ledger["run"].update({k: led.get(k, "unknown") for k in
                          ("model", "temperature", "budget", "usage", "skill_revision",
                           "prompt_revision", "planned_passes")})
    ledger["run"]["strategy"] = "windowed"
    ledger["run"]["stop_reason"] = led.get("stop_reason", "")
    passes = led.get("passes")
    if not passes:
        raise RuntimeError("spec.ledger.passes must state the actual passes performed")
    ledger["run"]["passes"] = passes
    ledger["full_context_review"] = led["full_context_review"]
    ledger["full_context_review"]["source_ids"] = [s["source_id"] for s in prepared["segments"]]
    ledger["entries"] = led["entries"]
    checks = []
    for c in led.get("source_checks", []):
        item = dict(c)
        item["evidence_candidates"] = [ev(e) for e in c["evidence_candidates"]]
        checks.append(item)
    ledger["source_checks"] = checks
    ledger["limitations"] = spec.get("limitations", [])
    dump(ledger, a / "extraction-ledger.json")
    cov = r.run([COVERAGE, "check", "--source-input", work / "source-input.json",
                 "--source", work / "source.txt", "--windows", work / "source-windows.json",
                 "--candidates", a / "raw-candidates.json", "--extraction", a / "extraction.json",
                 "--ledger", a / "extraction-ledger.json", "--output", a / "coverage-check.json"],
                "coverage_check", allow_fail=True)
    coverage_report = load(a / "coverage-check.json")

    # 7. modeling decisions
    r.run([KAOS, "template", a / "extraction.json", a / "judgments.json", a / "kaos-decisions.json"],
          "kaos_template")
    decisions = load(a / "kaos-decisions.json")
    spec_dec = spec.get("decisions", {})
    decisions["relations"] = spec_dec.get("relations", [])
    decisions["groups"] = spec_dec.get("groups", [])
    decisions["questions"] = spec_dec.get("questions", [])
    decisions["reassessments"] = spec_dec.get("reassessments", [])
    dump(decisions, a / "kaos-decisions.json")
    r.run([KAOS, "assemble", a / "extraction.json", a / "judgments.json", work / "source.txt",
           a / "kaos-decisions.json", a / "assembled"], "assemble")
    r.run([KAOS, "inspect", a / "assembled/model-input.json", a / "inspection.json"], "inspect")
    r.run([KAOS, "finalize", a / "assembled/model-input.json", a / "inspection.json",
           a / "delivery", "--svg"], "finalize")

    model = load(a / "assembled/model-input.json")
    report = load(a / "inspection.json")
    counts = {
        "goals": len(model["goals"]),
        "relations": len(model.get("relations", [])),
        "groups": len(model["refinement_groups"]),
        "established_groups": sum(1 for g in model["refinement_groups"]
                                  if g.get("status") == "supported" and g.get("completeness") == "complete"),
        "raw_candidates": len(raw_candidates),
        "support_labels": {lab: sum(1 for v in effective.values() if v == lab)
                           for lab in {"direct", "inferred", "insufficient", "contradicted"}},
        "issues": len(model["issues"]),
        "blocking_issues": sum(1 for i in model["issues"] if i["blocking"]),
    }
    delivery_files = {}
    for f in sorted((a / "delivery").rglob("*")):
        if f.is_file():
            delivery_files[str(f.relative_to(a))] = sha(f)
    summary = {
        "task_attempt": str(a.relative_to(EXP)),
        "document_id": doc,
        "started_at": started_at, "finished_at": now(),
        "skill_snapshot": load(EXP / "versions/manifest.json")["tree_sha256"],
        "input_json_sha256": source_sha,
        "source_txt_sha256": sha(work / "source.txt"),
        "windows": {"count": len(windows["windows"]), "size": 4, "stride": 2},
        "coverage_check": {"exit_code": cov.returncode,
                           "structure": coverage_report.get("structure"),
                           "workflow": coverage_report.get("workflow"),
                           "pending": coverage_report.get("pending"),
                           "counts": coverage_report.get("counts")},
        "tracing_status": tracing["status"],
        "declared_vs_effective_downgraded": downgraded,
        "inspection": {"structure": report["structure"], "readiness": report["readiness"],
                       "independent_semantic": report["independent_semantic"],
                       "formal_proof": report["formal_proof"], "human": report["human"]},
        "counts": counts,
        "delivery_files": delivery_files,
        "warnings": r.warnings,
        "commands": r.log,
    }
    dump(summary, a / "attempt-summary.json")
    print(json.dumps({"ok": True, "counts": counts, "readiness": report["readiness"],
                      "coverage_workflow": coverage_report.get("workflow"),
                      "downgraded": downgraded, "warnings": r.warnings}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
