"""Human-feedback validation. Names are self-reported, not authenticated identities."""
import json
from datetime import datetime

from export_model import feedback_binding, report_hash, review_target_hash

ACTIONS = {"goal": {"accept", "modify", "exclude", "merge", "split", "defer"},
           "relation": {"accept", "modify", "defer"},
           "evidence": {"sufficient", "partial", "insufficient", "incorrect"}, "model": {"comment", "add_goal"}}


def changes(entry):
    return entry["decision"] not in {"accept", "sufficient", "comment"}


def valid_time(value):
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except (AttributeError, TypeError, ValueError):
        return False


def _validate(packet, model, submitted=False):
    errors = []
    def need(ok, message):
        if not ok:
            errors.append(message)
    if not isinstance(packet, dict):
        return ["Feedback must be an object"]
    need(packet.get("schema_version") == "goalforge-review-feedback-1", "Unsupported feedback schema")
    need(packet.get("base_model") == feedback_binding(model), "Feedback model version/content differs")
    need(isinstance(packet.get("feedback_id"), str) and packet["feedback_id"].strip(), "Missing feedback ID")
    need(isinstance(packet.get("reviewer"), dict) and isinstance(packet["reviewer"].get("name"), str), "Invalid reviewer")
    need(packet.get("status") in {"draft", "submitted"}, "Invalid feedback state")
    need(valid_time(packet.get("created_at")) and valid_time(packet.get("updated_at")), "Invalid feedback times")
    entries = packet.get("entries")
    if not isinstance(entries, list):
        return errors + ["Entries must be an array"]
    ids = {"goal": {g["goal_id"] for g in model["goals"]}, "relation": {p["pair_id"] for p in model["pair_decisions"]},
           "evidence": {e["evidence_id"] for e in model["evidence_index"]}, "model": {model["model_id"]}}
    entry_ids, targets, claims, goal_entries = set(), set(), {}, []
    for e in entries:
        if not isinstance(e, dict):
            errors.append("Entry must be an object")
            continue
        eid, kind, target, decision = (e.get(k) for k in ("entry_id", "target_type", "target_id", "decision"))
        if not all(isinstance(x, str) for x in (eid, kind, target, decision)):
            errors.append("Entry keys must be strings")
            continue
        need(eid and eid not in entry_ids, "Duplicate or empty entry ID")
        entry_ids.add(eid)
        if kind not in ACTIONS or target not in ids[kind]:
            errors.append("Unknown review target")
            continue
        need(kind == "model" or (kind, target) not in targets, "Duplicate target opinion")
        targets.add((kind, target))
        need(decision in ACTIONS[kind], "Unsupported decision")
        need(isinstance(e.get("reason"), str), "Invalid review reason")
        need(valid_time(e.get("reviewed_at")), "Invalid entry time")
        if decision not in {"accept", "sufficient"}:
            need(isinstance(e.get("reason"), str) and e["reason"].strip(), "A reason is required")
        p = e.get("proposed")
        if not isinstance(p, dict):
            errors.append("Invalid proposed content")
            continue
        if kind == "goal":
            affected = [target]
            if decision in {"modify", "merge"}:
                need(isinstance(p.get("statement"), str) and p["statement"].strip(), "Missing goal statement")
            if decision == "merge":
                affected = p.get("goal_ids", [])
                ok = (isinstance(affected, list) and all(isinstance(x, str) for x in affected)
                      and len(set(affected)) == len(affected) >= 2 and target in affected and set(affected).issubset(ids["goal"]))
                need(ok, "Invalid merge targets")
                if not ok:
                    affected = []
            if decision == "split":
                rows = p.get("statements", [])
                need(isinstance(rows, list) and len(rows) >= 2 and all(isinstance(s, str) and s.strip() for s in rows)
                     and len(set(str(s) for s in rows)) == len(rows), "Split requires distinct goal statements")
            goal_entries.append((target, decision))
            if decision not in {"accept", "defer"}:
                for gid in affected:
                    need(gid not in claims, "Conflicting goal operations")
                    claims[gid] = eid
        if kind == "relation" and decision == "modify":
            need(p.get("label") in {"refinement", "related", "equivalent", "none", "uncertain"}, "Invalid relation label")
            need(isinstance(p.get("conditions"), list) and all(isinstance(x, str) for x in p["conditions"]), "Invalid conditions")
            need(isinstance(p.get("rationale"), str) and p["rationale"].strip(), "Missing relation rationale")
            if p.get("label") == "refinement":
                pair = next(x for x in model["pair_decisions"] if x["pair_id"] == target)
                need(isinstance(p.get("parent_id"), str) and isinstance(p.get("child_id"), str)
                     and p["parent_id"] != p["child_id"] and {p["parent_id"], p["child_id"]} == {pair["a"], pair["b"]}, "Invalid refinement direction")
        if kind == "model" and decision == "add_goal":
            need(isinstance(p.get("statement"), str) and p["statement"].strip(), "Missing new goal statement")
            need(p.get("origin") in {"explicit", "inferred"}, "Invalid new goal origin")
            ev = p.get("evidence_ids", [])
            need(isinstance(ev, list) and ev and all(isinstance(x, str) for x in ev)
                 and len(set(str(x) for x in ev)) == len(ev) and all(x in ids["evidence"] for x in ev), "New goal needs existing evidence")
    # A merge cannot coexist with an acceptance/exclusion of a retired input node.
    for target, decision in goal_entries:
        if target in claims and decision in {"accept", "defer"}:
            errors.append("Goal opinion conflicts with a merge or modification")
    drafts = packet.get("form_drafts", {})
    need(isinstance(drafts, dict), "Invalid form drafts")
    if isinstance(drafts, dict):
        for key, values in drafts.items():
            kind, _, target = key.partition(":")
            need(kind in ids and target in ids[kind] and isinstance(values, dict)
                 and all(isinstance(v, str) or isinstance(v, list) and all(isinstance(x, str) for x in v) for v in values.values()), "Invalid draft target/content")
    o = packet.get("overall")
    if not isinstance(o, dict):
        return errors + ["Missing overall decision"]
    need(o.get("decision") in {"undecided", "accept", "request_changes"}, "Invalid overall decision")
    need(isinstance(o.get("full_scope_ack"), bool) and isinstance(o.get("acknowledge_limits"), bool)
         and isinstance(o.get("comment"), str), "Invalid overall fields")
    if o.get("decision") == "accept":
        need(o.get("full_scope_ack") and o.get("acknowledge_limits"), "Explicit whole-model acknowledgments required")
        need(not any(changes(e) for e in entries if isinstance(e, dict) and "decision" in e), "Unresolved opinions prevent whole-model acceptance")
        need(model["delivery"]["readiness"] in {"reviewable", "accepted"}, "Blocked/unchecked model cannot be accepted")
    if submitted:
        need(not drafts, "Unfinished forms must be recorded or discarded")
        need(packet.get("status") == "submitted", "Submitted feedback required")
        need(o.get("decision") != "undecided" or entries, "Empty feedback cannot be submitted")
    return list(dict.fromkeys(errors))


def validate(packet, model, submitted=False):
    try:
        return _validate(packet, model, submitted)
    except (TypeError, KeyError, ValueError, AttributeError):
        return ["Malformed feedback fields; original model preserved"]


def approval_valid(model, packet):
    """Acceptance affects review metadata only, bound to unchanged domain/version."""
    acceptance = model.get("review", {}).get("acceptance", {})
    return (isinstance(packet, dict) and packet.get("status") == "submitted"
            and packet.get("overall", {}).get("decision") == "accept"
            and packet["overall"].get("full_scope_ack") is True and packet["overall"].get("acknowledge_limits") is True
            and not any(changes(e) for e in packet.get("entries", []))
            and not packet.get("form_drafts")
            and packet.get("base_model", {}).get("review_target_sha256") == review_target_hash(model)
            and packet["base_model"].get("model_id") == model["model_id"] and packet["base_model"].get("version") == model["version"]
            and acceptance.get("review_target_sha256") == review_target_hash(model)
            and acceptance.get("feedback_sha256") == report_hash(packet)
            and acceptance.get("feedback_id") == packet.get("feedback_id"))
