"""Audit extraction provenance and dispositions, never semantic completeness.

All inputs are read-only. A template contains pending decisions, not inferred ones.
"""
import argparse
import json
from collections import Counter
from pathlib import Path

from prepare_source import build_windows, digest, encode, validate_segments
from simple_candidates import validate as validate_extraction


INPUTS = ("source_input", "source", "windows", "candidates", "extraction")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def strings(value, label):
    require(isinstance(value, list) and all(nonempty(x) for x in value), label + " must be a string array")
    return value


def ids(value, allowed, label):
    strings(value, label)
    require(len(value) == len(set(value)) and set(value) <= set(allowed), label + " has duplicate or unknown IDs")
    return value


def index(items, key, label):
    require(isinstance(items, list), label + " must be an array")
    require(all(isinstance(x, dict) and nonempty(x.get(key)) for x in items), label + " has missing IDs")
    require(len({x[key] for x in items}) == len(items), label + " has duplicate IDs")
    return {x[key]: x for x in items}


def binding(raws):
    return {name + "_sha256": digest(raws[name]) for name in INPUTS}


def check_evidence(items, segments, source, label):
    require(isinstance(items, list) and items, label + " requires evidence")
    for e in items:
        require(isinstance(e, dict) and e.get("source_id") in segments, label + " has unknown evidence source")
        loc = segments[e["source_id"]]["original_locator"]
        start, end = e.get("start_char"), e.get("end_char")
        require(type(start) is int and type(end) is int and
                loc["start_char"] <= start < end <= loc["end_char"] and
                nonempty(e.get("quote")) and source[start:end] == e["quote"], label + " has invalid evidence offsets/quote")
        require(e.get("role") in {"basis", "context"}, label + " has invalid evidence role")
    require(any(e["role"] == "basis" for e in items), label + " requires basis evidence")


def source_inputs(raws):
    data = {k: json.loads(raws[k].decode("utf-8-sig")) for k in ("source_input", "windows")}
    source = raws["source"].decode("utf-8")
    prepared, windows = data["source_input"], data["windows"]
    validate_segments(prepared, source)
    params = windows["parameters"]
    expected = build_windows(prepared, source, params["size"], params["stride"], digest(raws["source_input"]))
    require(windows == expected, "Window content, coverage, offsets or input binding mismatch")
    return data, source


def capture_template(raws):
    data, _ = source_inputs(raws)
    return dict(schema_version="goalforge-extraction-candidates-1", document_id=data["source_input"]["document_id"],
                input_binding=dict(document_hash=data["source_input"]["document_hash"],
                                   source_input_sha256=digest(raws["source_input"]),
                                   windows_sha256=digest(raws["windows"])), candidates=[])


def validate_inputs(raws):
    data, source = source_inputs(raws)
    for name in ("candidates", "extraction"):
        data[name] = json.loads(raws[name].decode("utf-8-sig"))
    prepared, windows, candidates, extraction = (data[k] for k in ("source_input", "windows", "candidates", "extraction"))
    require(candidates.get("schema_version") == "goalforge-extraction-candidates-1", "Unsupported candidate schema")
    require(candidates.get("document_id") == extraction.get("document_id") == prepared["document_id"], "Document ID mismatch")
    require(candidates.get("input_binding") == dict(document_hash=prepared["document_hash"],
            source_input_sha256=digest(raws["source_input"]), windows_sha256=digest(raws["windows"])), "Candidate input binding mismatch")
    require(extraction.get("document_hash") == prepared["document_hash"], "Extraction source hash mismatch")
    validate_extraction(extraction)
    require(extraction["segments"] == prepared["segments"], "Extraction must preserve prepared source segments")
    segments = index(prepared["segments"], "source_id", "segments")
    window_index = index(windows["windows"], "window_id", "windows")
    raw_index = index(candidates["candidates"], "candidate_id", "raw candidates")
    goals = index(extraction["candidates"], "candidate_id", "final goals")
    for cid, c in raw_index.items():
        require(nonempty(c.get("statement")) and nonempty(c.get("pass_id")), cid + " requires statement/pass_id")
        require(c.get("origin") in {"explicit", "inferred", "unknown"}, cid + " has invalid tentative origin")
        require("actor" in c and (c["actor"] is None or nonempty(c["actor"])), cid + " has invalid actor")
        require(nonempty(c.get("modality")), cid + " requires modality (unknown is allowed)")
        strings(c.get("context"), cid + " context")
        refs = ids(c.get("window_ids"), window_index, cid + " windows")
        require(refs, cid + " requires source windows, including for full-context additions")
        check_evidence(c.get("evidence_candidates"), segments, source, cid)
        available = {sid for wid in refs for sid in window_index[wid]["source_ids"]}
        require(all(e["source_id"] in available for e in c["evidence_candidates"]), cid + " evidence lies outside its declared windows")
    for gid, g in goals.items():
        check_evidence(g["evidence_candidates"], segments, source, gid)
    return data, source, segments, window_index, raw_index, goals


def template(raws):
    data, _, segments, windows, candidates, _ = validate_inputs(raws)
    pass_ids = list(dict.fromkeys(c["pass_id"] for c in candidates.values()))
    return dict(schema_version="extraction-ledger-1", document_id=data["source_input"]["document_id"],
                input_binding=binding(raws), run=dict(
                    strategy="windowed", model="unknown", temperature="unknown", budget="unknown",
                    usage="unknown", skill_revision="unknown", prompt_revision="unknown",
                    planned_passes="unknown", stop_reason="", passes=[dict(
                        pass_id=pid, kind="unknown", context="unknown", status="not_run",
                        window_results=[dict(window_id=wid, status="pending", reason="") for wid in windows]
                    ) for pid in pass_ids]),
                full_context_review=dict(status="not_run", source_ids=[], reason=""),
                entries=[dict(candidate_id=cid, disposition="pending", final_goal_ids=[], reason="") for cid in candidates],
                source_checks=[], limitations=[])


def audit(raws, ledger):
    """Return an inspectable report even for stale files or malformed decisions."""
    report = dict(schema_version="goalforge-coverage-check-1", input_binding=binding(raws),
                  structure="failed", workflow="partial", semantic_completeness="not_assessed",
                  errors=[], pending=[], uncertain_candidate_ids=[], uncertain_source_check_ids=[], counts={},
                  limitations=["仅验证所提交记录的绑定、位置、处置与声明范围；不证明候选语义正确或原文意图穷尽。",
                               "不会验证模型名称、采样独立性或运行次数的真实性；这些是作者运行记录。",
                               "覆盖记录不被当前 KAOS 模型自动消费；目标支持仍需独立执行现有核验流程。"])
    try:
        _audit(raws, ledger, report)
    except (ValueError, KeyError, TypeError, AttributeError) as exc:
        report["structure"] = "failed"
        report["workflow"] = "partial"
        report["errors"].append(str(exc))
    return report


def _audit(raws, ledger, report):
    data, source, segments, windows, candidates, goals = validate_inputs(raws)
    require(ledger.get("schema_version") == "extraction-ledger-1", "Unsupported ledger schema")
    require(ledger.get("document_id") == data["source_input"]["document_id"], "Ledger document ID mismatch")
    require(ledger.get("input_binding") == binding(raws), "Ledger input version/hash mismatch; re-author affected decisions")
    strings(ledger.get("limitations"), "limitations")
    run = ledger["run"]
    require(run.get("strategy") in {"windowed", "full_document"}, "Invalid extraction strategy")
    for key in ("model", "skill_revision", "prompt_revision"):
        require(nonempty(run.get(key)), "Run requires " + key + " (unknown is allowed)")
    for key in ("temperature", "budget", "usage"):
        require(key in run and run[key] is not None, "Run requires " + key + " (unknown is allowed)")
    planned = run.get("planned_passes")
    require(planned == "unknown" or (type(planned) is int and planned >= 1), "Invalid planned_passes")
    passes = index(run.get("passes"), "pass_id", "passes")
    if not passes:
        report["pending"].append("run:no_passes")
    base_complete = False
    for pid, p in passes.items():
        require(p.get("kind") in {"initial", "repeat", "focused", "full_context", "unknown"}, pid + " invalid kind")
        require(p.get("context") in {"shared", "isolated", "unknown"}, pid + " invalid context")
        require(p.get("status") in {"completed", "partial", "not_run"}, pid + " invalid status")
        results = index(p.get("window_results"), "window_id", pid + " window results")
        require(set(results) == set(windows), pid + " must account for every window")
        for wid, result in results.items():
            require(result.get("status") in {"processed", "skipped", "pending"}, wid + " invalid processing status")
            if result["status"] == "skipped":
                require(nonempty(result.get("reason")), wid + " skipped without reason")
            if result["status"] == "pending":
                report["pending"].append(pid + ":" + wid)
        require(p["status"] != "not_run" or all(r["status"] == "pending" for r in results.values()), pid + " not_run conflicts with window processing")
        require(p["status"] != "completed" or all(r["status"] != "pending" for r in results.values()), pid + " completed with pending windows")
        if p["status"] != "completed" or p["kind"] == "unknown":
            report["pending"].append(pid + ":run_metadata")
        if p["kind"] == "initial" and p["status"] == "completed" and all(r["status"] == "processed" for r in results.values()):
            base_complete = True
    if not base_complete:
        report["pending"].append("run:initial_full_source_pass")
    if not nonempty(run.get("stop_reason")):
        report["pending"].append("run:stop_reason")
    for cid, c in candidates.items():
        require(c["pass_id"] in passes, cid + " unknown pass_id")
        p = passes[c["pass_id"]]
        done = {r["window_id"] for r in p["window_results"] if r["status"] == "processed"}
        if not set(c["window_ids"]) <= done:
            report["pending"].append(cid + ":unprocessed_source_windows")
    review = ledger["full_context_review"]
    require(review.get("status") in {"completed", "partial", "not_run"}, "Invalid full-context status")
    reviewed = ids(review.get("source_ids"), segments, "full-context source_ids")
    require(review["status"] != "not_run" or not reviewed, "not_run full-context review has reviewed sources")
    if review["status"] == "completed":
        require(set(reviewed) == set(segments) and nonempty(review.get("reason")), "Completed full-context review requires all sources and a reason")
    else:
        report["pending"].append("full_context_review")
    entries = index(ledger.get("entries"), "candidate_id", "dispositions")
    require(set(entries) == set(candidates), "Every raw candidate must have exactly one disposition")
    target_counts = Counter(gid for e in entries.values() for gid in e.get("final_goal_ids", []))
    for cid, entry in entries.items():
        disposition = entry.get("disposition")
        require(disposition in {"keep", "merge", "split", "exclude", "uncertain", "pending"}, cid + " invalid disposition")
        targets = ids(entry.get("final_goal_ids"), goals, cid + " final goals")
        if disposition == "pending":
            require(not targets, cid + " pending disposition cannot map final goals")
            report["pending"].append(cid + ":disposition")
            continue
        require(nonempty(entry.get("reason")), cid + " disposition requires a reason")
        if disposition in {"keep", "merge"}:
            require(len(targets) == 1, cid + " keep/merge must map to one final goal")
        if disposition == "merge":
            require(target_counts[targets[0]] >= 2, cid + " merge requires another source candidate")
        if disposition == "split":
            require(len(targets) >= 2, cid + " split requires at least two final goals")
        if disposition == "exclude":
            require(not targets, cid + " excluded candidate cannot map to final goals")
        if disposition == "uncertain":
            report["uncertain_candidate_ids"].append(cid)
    for gid in goals:
        if not target_counts[gid]:
            report["pending"].append(gid + ":no_candidate_provenance")
    checks = index(ledger.get("source_checks"), "check_id", "source checks")
    for check_id, check in checks.items():
        check_evidence(check.get("evidence_candidates"), segments, source, check_id)
        cids = ids(check.get("candidate_ids"), candidates, check_id + " candidates")
        gids = ids(check.get("final_goal_ids"), goals, check_id + " final goals")
        require(check.get("outcome") in {"represented", "excluded", "uncertain"}, check_id + " invalid outcome")
        require(nonempty(check.get("reason")), check_id + " requires a reason")
        if check["outcome"] == "represented":
            require(gids, check_id + " represented span requires final goals")
        if check["outcome"] == "excluded":
            require(not gids, check_id + " excluded span cannot map final goals")
        if check["outcome"] == "uncertain":
            report["uncertain_source_check_ids"].append(check_id)
        if cids and gids:
            require(set(gids) <= {g for cid in cids for g in entries[cid]["final_goal_ids"]}, check_id + " contradicts candidate dispositions")
    report["counts"] = dict(source_segments=len(segments), windows=len(windows), raw_candidates=len(candidates),
                            final_goals=len(goals), source_checks=len(checks),
                            actual_passes=sum(p["status"] != "not_run" for p in passes.values()),
                            dispositions=dict(Counter(e["disposition"] for e in entries.values())))
    report["structure"] = "passed"
    report["workflow"] = "partial" if report["pending"] else "recorded"
    # 'recorded' means declarations are accounted for, never that all intentions exist.


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("capture-template", "template", "check"))
    for name in INPUTS:
        parser.add_argument("--" + name.replace("_", "-"), type=Path, required=name in {"source_input", "source", "windows"})
    parser.add_argument("--ledger", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "check" and args.ledger is None:
        parser.error("check requires --ledger")
    if args.command != "check" and args.ledger is not None:
        parser.error("template does not consume old decisions")
    names = ("source_input", "source", "windows") if args.command == "capture-template" else INPUTS
    if any(getattr(args, name) is None for name in names):
        parser.error("template/check require --candidates and --extraction")
    if args.command == "capture-template" and (args.candidates or args.extraction):
        parser.error("capture-template only consumes source inputs")
    paths = [getattr(args, name) for name in names] + ([args.ledger] if args.ledger else [])
    if args.output.exists() or args.output.resolve() in {p.resolve() for p in paths}:
        parser.error("Use a new output path; inputs and existing files will not be overwritten")
    try:
        raws = {name: getattr(args, name).read_bytes() for name in names}
        if args.command == "capture-template":
            result = capture_template(raws)
        elif args.command == "template":
            result = template(raws)
        else:
            ledger_raw = args.ledger.read_bytes()
            result = audit(raws, json.loads(ledger_raw.decode("utf-8-sig")))
            result["ledger_sha256"] = digest(ledger_raw)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("xb") as handle:
            handle.write(encode(result))
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.error(str(exc))
    if args.command == "check":
        raise SystemExit(2 if result["structure"] != "passed" else 1 if result["workflow"] == "partial" else 0)


if __name__ == "__main__":
    main()
