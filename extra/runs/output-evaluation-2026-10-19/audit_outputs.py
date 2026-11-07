"""Read-only audit of the 34 frozen final models; writes evaluation files only."""
import hashlib
import json
import re
from collections import Counter, defaultdict, deque
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEST = Path(__file__).resolve().parent


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def graph_stats(ids, edges):
    adjacency = defaultdict(list)
    indegree = dict.fromkeys(ids, 0)
    touched = set()
    for edge in edges:
        a, b = edge["parent_id"], edge["child_id"]
        adjacency[a].append(b)
        indegree[b] += 1
        touched.update([a, b])
    queue = deque(k for k, n in indegree.items() if n == 0)
    depths = dict.fromkeys(ids, 0)
    visited = 0
    while queue:
        node = queue.popleft()
        visited += 1
        for child in adjacency[node]:
            depths[child] = max(depths[child], depths[node] + 1)
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    return {"acyclic": visited == len(ids), "max_depth_edges": max(depths.values(), default=0),
            "participating_goals": len(touched), "isolated_goals": len(ids) - len(touched)}


def audit():
    rows = []
    counts = Counter()
    errors = []
    inputs = []
    for model_path in sorted((ROOT / "output").glob("DOC*/final/goal-model.json")):
        doc_dir = model_path.parents[1]
        doc = doc_dir.name
        final = model_path.parent
        model = read(model_path)
        extraction = read(doc_dir / "extraction.json")
        report = read(final / "attachments/review-report.json")
        manifest = read(final / "delivery-manifest.json")
        source = (final / "attachments/source.txt").read_text(encoding="utf-8")
        ids = [g["goal_id"] for g in model["goals"]]
        valid_ids = set(ids)
        pairs = model["pair_decisions"]
        labels = Counter(p["label"] for p in pairs)
        actual_pairs = [tuple(sorted((p["a"], p["b"]))) for p in pairs]
        pair_complete = len(actual_pairs) == len(set(actual_pairs)) and set(actual_pairs) == set(combinations(sorted(ids), 2))
        refs = [e for e in model["edges"] if e["type"] == "refinement"]
        graph = graph_stats(ids, refs)
        touched = set()
        for edge in model["edges"]:
            touched.update([edge.get("a"), edge.get("b"), edge.get("parent_id"), edge.get("child_id")])
        evidence = model["evidence_index"]
        quote_ok = 0
        for item in evidence:
            start, end = item.get("start_char"), item.get("end_char")
            correct = isinstance(start, int) and isinstance(end, int) and 0 <= start < end <= len(source) and source[start:end] == item["quote"]
            quote_ok += correct
            if not correct:
                errors.append({"doc": doc, "kind": "quote_slice", "id": item["evidence_id"]})
        attachment_ok = 0
        for item in model["input_artifacts"]:
            target = final / item["path"]
            correct = target.is_file() and sha(target) == item["sha256"]
            attachment_ok += correct
            if not correct:
                errors.append({"doc": doc, "kind": "attachment_hash", "path": item["path"]})
        manifest_ok = 0
        for name, expected in manifest["files"].items():
            target = final / name
            correct = target.is_file() and sha(target) == expected
            manifest_ok += correct
            if not correct:
                errors.append({"doc": doc, "kind": "manifest_hash", "path": name})
        same_source = (doc_dir / "source.txt").read_bytes() == (ROOT / "datasets/processed/goalforge-v1/source" / (doc + ".txt")).read_bytes()
        question_count = len(extraction.get("review_questions", []))
        row = {"document_id": doc, "schema": model["schema_version"], "goal_count": len(ids),
               "candidate_count": len(extraction["candidates"]), "pair_count": len(pairs),
               "pair_labels": dict(labels), "pair_complete": pair_complete,
               "refinement_graph": graph, "isolated_in_all_edges": sum(x not in touched for x in ids),
               "evidence_count": len(evidence), "quote_slices_valid": quote_ok,
               "input_attachments": len(model["input_artifacts"]), "input_attachment_hashes_valid": attachment_ok,
               "manifest_files": len(manifest["files"]), "manifest_hashes_valid": manifest_ok,
               "source_equal_to_dataset": same_source, "source_turn_count": len(re.findall(r"^\[T\d+\]", source, re.M)),
               "extraction_questions": question_count, "model_issues": len(model["issues"]),
               "report_summary": report["summary"], "human_review": model["review"]["status"],
               "origins": dict(Counter(g["origin"] for g in model["goals"])),
               "trace_statuses": dict(Counter(g["trace_status"] for g in model["goals"])),
               "refinement_groups_present": "refinement_groups" in model,
               "none_decisions_with_no_evidence": sum(p["label"] == "none" and not p.get("evidence_ids") for p in pairs),
               "template_none_rationales": sum(p["label"] == "none" and "两处分别出自不同话题段" in p["rationale"] for p in pairs)}
        rows.append(row)
        for key in ["goal_count", "candidate_count", "pair_count", "evidence_count", "quote_slices_valid", "input_attachments",
                    "input_attachment_hashes_valid", "manifest_files", "manifest_hashes_valid", "source_turn_count", "extraction_questions", "model_issues",
                    "none_decisions_with_no_evidence", "template_none_rationales", "isolated_in_all_edges"]:
            counts[key] += row[key]
        counts.update({"documents": 1, "docs_with_refinement": bool(refs), "hierarchy_participating_goals": graph["participating_goals"],
                       "hierarchy_isolated_goals": graph["isolated_goals"], "acyclic_documents": graph["acyclic"],
                       "complete_pair_documents": pair_complete, "dataset_source_equal_documents": same_source})
        counts.update({"label_" + k: v for k, v in labels.items()})
        counts.update({"origin_" + k: v for k, v in row["origins"].items()})
        inputs.append({"model": model_path.relative_to(ROOT).as_posix(), "sha256": sha(model_path),
                       "source_sha256": sha(final / "attachments/source.txt")})
        if not pair_complete or not graph["acyclic"] or not same_source or len(ids) != len(valid_ids):
            errors.append({"doc": doc, "kind": "graph_pair_source_or_id_check"})
    accepted_path = ROOT / "output/DOC005/v0.1-accepted/goal-model.json"
    accepted = read(accepted_path)
    result = {"scope": "34 DOC*/final models only; accepted DOC005 analyzed separately", "date": "2026-10-19",
              "totals": dict(counts), "max_refinement_depth_edges": max(r["refinement_graph"]["max_depth_edges"] for r in rows),
              "schemas": dict(Counter(r["schema"] for r in rows)),
              "structure_status": dict(Counter(r["report_summary"]["structure_status"] for r in rows)),
              "semantic_status": dict(Counter(r["report_summary"]["semantic_status"] for r in rows)),
              "human_review": dict(Counter(r["human_review"] for r in rows)),
              "accepted_DOC005": {"review": accepted["review"], "goals": len(accepted["goals"]),
                                  "semantic_status": accepted["validation"]["semantic_status"]},
              "paper_derived_metrics": {"TP": 227, "TN": 170, "FP": 73, "FN": 80,
                                        "accuracy": 397 / 550, "precision": 227 / 300,
                                        "recall": 227 / 307, "f1": 454 / 607},
              "errors": errors, "documents": rows, "inputs": inputs}
    (DEST / "audit-results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k not in ["documents", "inputs", "accepted_DOC005"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    audit()
