"""Apply explicit validated human proposals; preserve lineage and invalidate affected support."""
import copy
from itertools import combinations

from export_model import check_structure, core_hash, report_hash


def revise(model, feedback):
    result = copy.deepcopy(model)
    original_goals = {g["goal_id"]: copy.deepcopy(g) for g in model["goals"]}
    node_map = {g["goal_id"]: g for g in result["goals"]}
    changed, retired, routes, disputed_pairs = set(), set(), [], set()
    old_pairs = copy.deepcopy(result["pair_decisions"])
    used_ids = set(node_map) | {cid for g in model["goals"] for cid in g["source_candidate_ids"]}
    used_ids.update(g["goal_id"] for change in model.get("changes", []) for g in change.get("before_goals", []))
    used_ids.update(c["candidate_id"] for c in model.get("candidate_additions", []))
    def new_id(prefix):
        index = 1
        while prefix + str(index).zfill(3) in used_ids:
            index += 1
        value = prefix + str(index).zfill(3)
        used_ids.add(value)
        return value
    def invalidate(ids):
        for gid in ids:
            if gid in node_map:
                node_map[gid]["trace_status"] = "needs_retrace"
                node_map[gid]["review_status"] = "pending"
                changed.add(gid)
    def make_node(statement, originals, entry):
        base = copy.deepcopy(originals[0]) if originals else dict(actor="未指定", context=[], origin=entry["proposed"]["origin"], source_candidate_ids=[], evidence_ids=[])
        base["goal_id"] = new_id(model["document_scope"]["document_ids"][0] + "-GH")
        base["statement"] = statement
        base["source_candidate_ids"] = list(dict.fromkeys(cid for g in originals for cid in g["source_candidate_ids"]))
        base["evidence_ids"] = list(dict.fromkeys(eid for g in originals for eid in g["evidence_ids"]))
        if originals:
            base["context"] = list(dict.fromkeys(c for g in originals for c in g["context"]))
            actors = list(dict.fromkeys(g["actor"] for g in originals))
            base["actor"] = actors[0] if len(actors) == 1 else "主体待核对：" + "；".join(str(a) if a is not None else "未指定" for a in actors)
            base["origin"] = "inferred" if any(g["origin"] == "inferred" for g in originals) else originals[0]["origin"]
        if not originals:
            cid = new_id(model["document_scope"]["document_ids"][0] + "-CH")
            base["source_candidate_ids"] = [cid]
            base["evidence_ids"] = entry["proposed"]["evidence_ids"][:]
            result.setdefault("candidate_additions", []).append(dict(candidate_id=cid, category="goal", statement=statement,
                origin=base["origin"], evidence_ids=base["evidence_ids"][:], source="human_feedback", entry_id=entry["entry_id"]))
        base.update(trace_status="needs_retrace", review_status="pending")
        node_map[base["goal_id"]] = base
        changed.add(base["goal_id"])
        for cid in base["source_candidate_ids"]:
            result["candidate_goal_mapping"].append(dict(candidate_id=cid, goal_id=base["goal_id"], action=entry["decision"], reason=entry["reason"]))
        return base["goal_id"]
    for e in feedback["entries"]:
        kind, decision, target, p = (e[k] for k in ("target_type", "decision", "target_id", "proposed"))
        route = dict(entry_id=e["entry_id"], decision=decision, target_id=target, status="recorded", next_skill=None)
        if kind == "goal" and decision == "modify":
            node_map[target]["statement"] = p["statement"].strip()
            invalidate([target])
            route.update(status="applied_needs_retrace", next_skill="goal-tracing")
        elif kind == "goal" and decision == "exclude":
            retired.add(target)
            route.update(status="applied", next_skill="model-review")
        elif kind == "goal" and decision in {"merge", "split"}:
            inputs = p["goal_ids"] if decision == "merge" else [target]
            originals = [original_goals[gid] for gid in inputs]
            statements = [p["statement"]] if decision == "merge" else p["statements"]
            route["new_goal_ids"] = [make_node(s.strip(), originals, e) for s in statements]
            retired.update(inputs)
            route.update(status="applied_needs_retrace", next_skill="goal-tracing")
        elif kind == "model" and decision == "add_goal":
            route.update(new_goal_ids=[make_node(p["statement"].strip(), [], e)], status="applied_needs_retrace", next_skill="goal-tracing")
        elif kind == "evidence" and decision != "sufficient":
            affected = [gid for gid, g in node_map.items() if target in g["evidence_ids"]]
            direct_pairs = [p["pair_id"] for p in result["pair_decisions"] if target in p.get("evidence_ids", [])]
            disputed_pairs.update(direct_pairs)
            invalidate(affected)
            route.update(status="needs_retrace" if affected or direct_pairs else "recorded_unreferenced_evidence",
                         next_skill="goal-tracing" if affected else "goal-model-building" if direct_pairs else None,
                         affected_goal_ids=affected, affected_pair_ids=direct_pairs)
        elif decision == "defer":
            route.update(status="needs_human_decision")
        routes.append(route)
    for gid in retired:
        node_map.pop(gid, None)
    for m in result["candidate_goal_mapping"]:
        if m.get("goal_id") in retired:
            m.update(previous_goal_id=m["goal_id"], goal_id=None, action="retired_by_human_proposal", reason="原目标已排除或由合并/拆分后的新目标替代；见changes。")
    result["goals"] = list(node_map.values())
    pairs = {}
    for p in result["pair_decisions"]:
        if p["a"] not in node_map or p["b"] not in node_map:
            continue
        if {p["a"], p["b"]} & changed or p["pair_id"] in disputed_pairs:
            p.update(previous_decision=copy.deepcopy(p), label="uncertain", assessment_status="not_run", trace_status="needs_retrace",
                     rationale="目标或证据已变化，该关系退回待评估；原判断保留在previous_decision。", review_status="pending")
            p.pop("parent_id", None)
            p.pop("child_id", None)
        pairs[frozenset([p["a"], p["b"]])] = p
    pair_ids = {p["pair_id"] for p in model["pair_decisions"]}
    for a, b in combinations(node_map, 2):
        if frozenset([a, b]) not in pairs:
            i = 1
            while "PH" + str(i).zfill(4) in pair_ids:
                i += 1
            pid = "PH" + str(i).zfill(4)
            pair_ids.add(pid)
            pairs[frozenset([a, b])] = dict(pair_id=pid, a=a, b=b, label="uncertain", assessment_status="not_run",
                trace_status="needs_retrace", rationale="新节点关系尚未评估；不能作为已判断的不确定或无关系。", evidence_ids=[], conditions=[], review_status="pending")
    for e in feedback["entries"]:
        if e["target_type"] == "relation" and e["decision"] == "modify":
            p = next((p for p in pairs.values() if p["pair_id"] == e["target_id"]), None)
            route = next(r for r in routes if r["entry_id"] == e["entry_id"])
            if not p:
                raise ValueError("Relation proposal refers to a retired goal; resolve conflicting feedback first")
            p.update(previous_decision=copy.deepcopy(p), **copy.deepcopy(e["proposed"]), trace_status="needs_retrace",
                     assessment_status="human_proposed", review_status="pending")
            if p["label"] != "refinement":
                p.pop("parent_id", None)
                p.pop("child_id", None)
            route.update(status="applied_needs_evidence_review", next_skill="goal-model-building")
    result["pair_decisions"] = list(pairs.values())
    result["edges"] = []
    old_edges = {e["decision_id"]: e for e in model["edges"]}
    used_edges = {e["edge_id"] for e in model["edges"]}
    for p in result["pair_decisions"]:
        if p["label"] not in {"related", "refinement"}:
            continue
        eid = old_edges.get(p["pair_id"], {}).get("edge_id")
        if not eid:
            i = 1
            while "RH" + str(i).zfill(4) in used_edges:
                i += 1
            eid = "RH" + str(i).zfill(4)
            used_edges.add(eid)
        edge = dict(edge_id=eid, type=p["label"], decision_id=p["pair_id"], conditions=p.get("conditions", []), review_status="pending")
        if p["label"] == "refinement":
            edge.update(parent_id=p["parent_id"], child_id=p["child_id"], interpretation=p.get("interpretation", "scope_specialization"))
        else:
            edge.update(a=p["a"], b=p["b"])
        result["edges"].append(edge)
    result["relation_coverage"] = dict(strategy="all_pairs", expected_pairs=len(pairs),
        evaluated_pairs=sum(p.get("assessment_status") != "not_run" for p in pairs.values()),
        unassessed_pair_ids=[p["pair_id"] for p in pairs.values() if p.get("assessment_status") == "not_run"])
    relevant = set(node_map) | {e["evidence_id"] for e in result["evidence_index"]} | {p["pair_id"] for p in pairs.values()}
    result["issues"] = [i for i in result["issues"] if i.get("code") != "uncertain_relation" and (not i.get("target_ids") or set(i["target_ids"]).issubset(relevant))]
    result["issues"].extend(dict(code="uncertain_relation", severity="needs_review", target_ids=[p["a"], p["b"]], reason=p["rationale"])
                            for p in pairs.values() if p["label"] == "uncertain" and p.get("assessment_status") != "not_run")
    domain_changed = (result["goals"] != model["goals"] or result["pair_decisions"] != model["pair_decisions"]
                      or result["edges"] != model["edges"] or bool(retired))
    if domain_changed:
        result["version"] = model["version"] + ".h1"
        result["parent_version"] = model["version"]
        result["changes"].append(dict(kind="human_feedback_revision", feedback_id=feedback["feedback_id"], feedback_sha256=report_hash(feedback),
            parent_core_sha256=core_hash(model), before_goals=list(original_goals.values()), before_pairs=old_pairs,
            before_edges=copy.deepcopy(model["edges"]), entries=copy.deepcopy(feedback["entries"]), routes=routes))
        result["validation"] = dict(structure_status="not_run", semantic_status="not_run", report_path=None)
        result["review"] = dict(status="pending", records=copy.deepcopy(model["review"].get("records", [])),
                               feedback_artifacts=copy.deepcopy(model["review"].get("feedback_artifacts", [])))
        result["delivery"].update(mode="human_revision", readiness="blocked" if changed or disputed_pairs else "unchecked", files=[])
        result.pop("content_sha256", None)
    check_structure(result)
    return result, routes, domain_changed
