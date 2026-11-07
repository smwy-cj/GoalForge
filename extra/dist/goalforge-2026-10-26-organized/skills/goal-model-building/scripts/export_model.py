"""Export one unchanged model to JSON, Markdown, offline HTML and SVG."""

import argparse
import copy
import hashlib
import html
import json
import re
import unicodedata
from pathlib import Path


def content_hash(model):
    data = copy.deepcopy(model)
    data.pop("content_sha256", None)
    data.pop("delivery", None)
    raw = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def core_hash(model):
    """goalforge-core-v1: all top-level fields except derived review/delivery fields."""
    data = {k: v for k, v in model.items() if k not in {"content_sha256", "delivery", "validation"}}
    raw = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def report_hash(report):
    raw = json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def review_target_hash(model):
    data = {k: v for k, v in model.items() if k not in {"content_sha256", "delivery", "validation", "review"}}
    return report_hash(data)


def feedback_binding(model):
    return dict(model_id=model["model_id"], version=model["version"], content_sha256=content_hash(model),
                core_sha256=core_hash(model), review_target_sha256=review_target_hash(model))


def check_structure(model):
    """Shared deterministic export integrity checks; semantic audit is separate."""
    if model["schema_version"] != "goalforge-model-draft-1":
        raise ValueError("Unsupported model schema")
    goals = {g["goal_id"]: g for g in model["goals"]}
    if len(goals) != len(model["goals"]):
        raise ValueError("Duplicate goal_id")
    evidence = {e["evidence_id"]: e for e in model["evidence_index"]}
    if len(evidence) != len(model["evidence_index"]):
        raise ValueError("Duplicate evidence_id")
    decisions = {p["pair_id"]: p for p in model["pair_decisions"]}
    if len(decisions) != len(model["pair_decisions"]):
        raise ValueError("Duplicate pair_id")
    pairs = set()
    for p in decisions.values():
        pair = frozenset((p["a"], p["b"]))
        if len(pair) != 2 or not pair.issubset(goals) or pair in pairs:
            raise ValueError("Invalid or duplicate decision pair")
        if p["label"] not in {"refinement", "related", "equivalent", "none", "uncertain"}:
            raise ValueError("Invalid pair label")
        if not set(p.get("evidence_ids", [])).issubset(evidence):
            raise ValueError("Unknown pair evidence")
        pairs.add(pair)
    edge_ids, seen, adjacency = set(), set(), {gid: [] for gid in goals}
    for edge in model["edges"]:
        if edge["edge_id"] in edge_ids:
            raise ValueError("Duplicate edge_id")
        edge_ids.add(edge["edge_id"])
        label = edge["type"]
        a, b = endpoints(edge)
        if a not in goals or b not in goals or a == b:
            raise ValueError("Invalid edge endpoint")
        key = (label, (a, b) if label == "refinement" else tuple(sorted((a, b))))
        if key in seen:
            raise ValueError("Duplicate edge")
        seen.add(key)
        decision = decisions.get(edge["decision_id"])
        if not decision or decision["label"] != label or {a, b} != {decision["a"], decision["b"]}:
            raise ValueError("Edge does not match pair decision")
        if label == "refinement":
            if decision.get("parent_id") != a or decision.get("child_id") != b:
                raise ValueError("Refinement direction differs from decision")
            adjacency[a].append(b)
    # Cycles are blocked rather than omitted or silently laid out as a tree.
    colors = {}
    def visit(node):
        if colors.get(node) == 1:
            raise ValueError("Refinement cycle")
        if colors.get(node) == 2:
            return
        colors[node] = 1
        for child in adjacency[node]:
            visit(child)
        colors[node] = 2
    for gid in goals:
        visit(gid)
    for g in goals.values():
        if not set(g["evidence_ids"]).issubset(evidence):
            raise ValueError("Unknown goal evidence")
        if g["origin"] not in {"explicit", "inferred", "design_extension"}:
            raise ValueError("Invalid goal origin")
    n = len(goals)
    coverage = model["relation_coverage"]
    evaluated = sum(p.get("assessment_status") != "not_run" for p in decisions.values())
    if coverage["expected_pairs"] != n * (n - 1) // 2 or coverage["evaluated_pairs"] != evaluated:
        raise ValueError("Pair coverage count mismatch")
    if coverage.get("strategy") == "all_pairs" and len(pairs) != n * (n - 1) // 2:
        raise ValueError("Incomplete all-pairs decisions")
    return goals


def check(model, report=None, feedback=None):
    goals = check_structure(model)
    readiness = model["delivery"]["readiness"]
    status = model["review"]["status"]
    if status not in {"pending", "partial", "accepted"}:
        raise ValueError("Unsupported human review state")
    if status == "accepted":
        import sys
        sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "model-review/scripts"))
        from feedback_contract import approval_valid
        if report is None or not approval_valid(model, feedback):
            raise ValueError("Actual version-bound human acceptance feedback required")
    if report is not None:
        binding = report["input_model"]
        if (report.get("schema_version") != "model-review-draft-1" or
            binding.get("hash_rule_version") != "goalforge-core-v1" or
            binding.get("core_sha256") != core_hash(model) or
            binding.get("model_id") != model["model_id"] or binding.get("version") != model["version"]):
            raise ValueError("Review report does not match model version/content")
        if model["validation"].get("report_sha256") != report_hash(report):
            raise ValueError("Review report digest mismatch")
        if model["validation"]["structure_status"] != report["summary"]["structure_status"]:
            raise ValueError("Review structure status mismatch")
        if model["validation"]["semantic_status"] != report["summary"]["semantic_status"]:
            raise ValueError("Review semantic status mismatch")
        expected = "reviewable" if report["summary"]["structure_status"] == "passed" and not any(
            i["severity"] == "blocking" and i["status"] != "resolved" for i in report["issues"]) else "blocked"
        if expected == "reviewable" and status == "accepted":
            expected = "accepted"
        if readiness != expected:
            raise ValueError("Readiness differs from bound review report")
        return goals
    if status != "pending":
        raise ValueError("Human review states require a bound executed report")
    if readiness not in {"unchecked", "blocked"}:
        raise ValueError("Invalid delivery readiness")
    if model["validation"]["structure_status"] != "not_run":
        raise ValueError("Do not import unverified model-review status into the draft exporter")
    return goals


def endpoints(edge):
    if edge["type"] == "refinement":
        return edge["parent_id"], edge["child_id"]
    if edge["type"] == "related":
        return edge["a"], edge["b"]
    raise ValueError("Only refinement and related can be graph edges")


def wrap(text, width=25):
    rows, row, length = [], "", 0
    for char in str(text):
        units = 2 if unicodedata.east_asian_width(char) in "WF" else 1
        if char == "\n" or length + units > width:
            rows.append(row)
            row, length = "", 0
            if char == "\n":
                continue
        row += char
        length += units
    if row:
        rows.append(row)
    return rows or [""]


def layout(model):
    goals = model["goals"]
    levels = {g["goal_id"]: 0 for g in goals}
    for _ in goals:
        for e in model["edges"]:
            if e["type"] == "refinement":
                levels[e["child_id"]] = max(levels[e["child_id"]], levels[e["parent_id"]] + 1)
    positions, y = {}, 160
    for level in sorted(set(levels.values())):
        group = [g for g in goals if levels[g["goal_id"]] == level]
        for start in range(0, len(group), 3):
            row = group[start:start + 3]
            heights = [max(110, 58 + 22 * len(wrap(g["statement"]))) for g in row]
            for i, g in enumerate(row):
                positions[g["goal_id"]] = (50 + i * 365, y, 310, heights[i])
            y += max(heights) + 100
    return positions, max(440, y + 110)


def render_svg(model):
    esc = lambda value: html.escape(str(value), quote=True)
    positions, height = layout(model)
    lines = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1140 {height}" role="img" aria-label="目标模型图" data-height="{height}">',
             '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="#40516c"/></marker></defs>',
             '<style>text{font-family:Arial,"Microsoft YaHei",sans-serif}.edge{cursor:pointer}.edge path{fill:none;stroke:#546881;stroke-width:2}.edge.related path{stroke:#8193ac;stroke-dasharray:4 6}.edge.conditional path{stroke-dasharray:10 5}.node{cursor:pointer}.node rect{fill:#fff;stroke:#455e7c;stroke-width:1.5}.node.inferred rect{fill:#fff8e6;stroke:#ad7c1b;stroke-dasharray:5 3}.node:focus rect{stroke:#18768b;stroke-width:4}.hidden{display:none}.selected rect{stroke:#087f8c;stroke-width:4}</style>',
             '<rect width="100%" height="100%" fill="#f5f7fb"/>',
             f'<text x="50" y="40" font-size="22" fill="#182c42">{esc(model["model_id"])} · {esc(model["version"])}</text>',
             f'<text x="50" y="70" font-size="13" fill="#536277">状态：{esc(model["delivery"]["readiness"])} · 人工审核：{esc(model["review"]["status"])} · 精化有箭头 / 相关为点线 / 条件为长虚线</text>',
             f'<text x="50" y="96" font-size="12" fill="#536277">显式目标白底；推断目标浅黄虚线框。节点总数 {len(model["goals"])}，不确定判断见决策列表。</text>']
    for e in model["edges"]:
        a, b = endpoints(e)
        ax, ay, aw, ah = positions[a]
        bx, by, bw, bh = positions[b]
        x1, y1, x2, y2 = ax + aw / 2, ay + ah, bx + bw / 2, by
        if ay == by:
            y1, y2 = ay + ah / 2, by + bh / 2
            x1, x2 = ax + aw, bx
        control = max(35, abs(y2 - y1) / 2)
        path = f"M{x1} {y1} C{x1} {y1 + control} {x2} {y2 - control} {x2} {y2}"
        classes = "edge " + e["type"] + (" conditional" if e.get("conditions") else "")
        marker = ' marker-end="url(#arrow)"' if e["type"] == "refinement" else ""
        name = "精化" if e["type"] == "refinement" else "相关"
        if e.get("conditions"):
            name += "（条件）"
        lines += [f'<g class="{classes}" data-edge="{esc(e["edge_id"])}" data-a="{esc(a)}" data-b="{esc(b)}" tabindex="0" role="button" aria-label="{esc(name + a + b)}">',
                  f'<path d="{path}"{marker}/><path d="{path}" style="stroke:transparent;stroke-width:16"/>',
                  f'<title>{esc(name + "：" + a + " / " + b)}</title></g>']
    for g in model["goals"]:
        x, y, w, h = positions[g["goal_id"]]
        lines += [f'<g class="node {esc(g["origin"])}" data-node="{esc(g["goal_id"])}" tabindex="0" role="button" aria-label="{esc(g["statement"])}">',
                  f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12"/>',
                  f'<text x="{x + 18}" y="{y + 26}" fill="#63738a" font-size="12">{esc(g["goal_id"])}</text>']
        for i, row in enumerate(wrap(g["statement"])):
            lines.append(f'<text x="{x + 18}" y="{y + 53 + i * 22}" fill="#182c42" font-size="16">{esc(row)}</text>')
        lines += ["</g>"]
    lines += [f'<text x="50" y="{height - 35}" font-size="11" fill="#63738a">内容标识：{esc(model["content_sha256"])}</text>', "</svg>"]
    return "\n".join(lines)


def render_markdown(model):
    def safe(value):
        return html.escape(str(value)).replace("|", "&#124;").replace("\n", "<br>")
    lines = ["# 目标模型说明", "", f"模型：{safe(model['model_id'])}；版本：{safe(model['version'])}", "",
             f"交付状态：{safe(model['delivery']['readiness'])}；结构：{safe(model['validation']['structure_status'])}；人工审核：{safe(model['review']['status'])}", "",
             "[交互模型](goal-model.html) · [矢量图](goal-model.svg) · [权威数据](goal-model.json)", "",
             "## 目标图", "", "![目标模型矢量图](goal-model.svg)", "", "```mermaid", "flowchart TD"]
    aliases = {g["goal_id"]: f"N{i}" for i, g in enumerate(model["goals"])}
    for g in model["goals"]:
        label = g["statement"].replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", " ")
        lines.append(f'  {aliases[g["goal_id"]]}["{label}"]')
    for e in model["edges"]:
        a, b = endpoints(e)
        connector = "-->|精化|" if e["type"] == "refinement" else "-.-|相关|"
        lines.append(f"  {aliases[a]} {connector} {aliases[b]}")
    lines += ["```", "", "## 目标", "", "| 编号 | 表述 | 来源 | 情境 | 证据 |", "|---|---|---|---|---|"]
    for g in model["goals"]:
        lines.append("| " + " | ".join(safe(v) for v in [g["goal_id"], g["statement"], g["origin"], "；".join(g["context"]), ", ".join(g["evidence_ids"])]) + " |")
    lines += ["", "## 关系判断（含不确定与无关系）", ""]
    for p in model["pair_decisions"]:
        lines += [f"- {safe(p['a'])} / {safe(p['b'])}：{safe(p['label'])}。{safe(p['rationale'])}"]
    lines += ["", "## 证据", ""]
    for e in model["evidence_index"]:
        lines += [f"### {safe(e['evidence_id'])} · {safe(e['source_id'])}", "", "> " + safe(e["quote"]), "",
                  "原件位置：" + safe(json.dumps(e.get("original_locator", {}), ensure_ascii=False)), ""]
    lines += ["## 问题、限制与版本", ""]
    for issue in model["issues"]:
        lines.append("- " + safe(issue.get("reason", str(issue))))
    lines += ["- " + safe(x) for x in model["delivery"]["limitations"]]
    lines += ["", "内容标识：" + model["content_sha256"], "", "人工决定：", "", "审核意见：", ""]
    return "\n".join(lines)


def export(model, output_dir, attachments=None, report=None, feedback=None):
    check(model, report, feedback)
    output_dir = Path(output_dir)
    if output_dir.exists() and any(output_dir.iterdir()):
        raise ValueError("Use a fresh output directory to preserve prior versions")
    for relative in (attachments or {}):
        target = output_dir / relative
        if output_dir.resolve() not in target.resolve().parents or not relative.startswith("attachments/"):
            raise ValueError("Attachments must remain in the attachments directory")
    result = copy.deepcopy(model)
    result["content_sha256"] = content_hash(result)
    result["delivery"]["files"] = ["goal-model.json", "goal-model.md", "goal-model.html", "goal-model.svg", "delivery-manifest.json"]
    svg = render_svg(result)
    # Escape script terminators and HTML markup inside JSON; template uses textContent.
    payload = json.dumps(result, ensure_ascii=False).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    assets = Path(__file__).resolve().parents[1] / "assets"
    template = (assets / "viewer.html").read_text(encoding="utf-8-sig")
    # Substitute against the template once; user text containing a token remains literal.
    replacements = {"MODEL_JSON": payload, "MODEL_SVG": svg,
                    "REVIEW_BINDING": json.dumps(feedback_binding(result), ensure_ascii=False).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026"),
                    "VIEWER_CSS": (assets / "viewer.css").read_text(encoding="utf-8"),
                    "VIEWER_JS": "\n".join((assets / name).read_text(encoding="utf-8") for name in ("review-core.js", "viewer.js", "review-ui.js"))}
    page = re.sub(r"__(MODEL_JSON|MODEL_SVG|REVIEW_BINDING|VIEWER_CSS|VIEWER_JS)__", lambda match: replacements[match.group(1)], template)
    files = {"goal-model.json": json.dumps(result, ensure_ascii=False, indent=2) + "\n",
             "goal-model.md": render_markdown(result), "goal-model.svg": svg, "goal-model.html": page}
    output_dir.mkdir(parents=True, exist_ok=True)
    hashes = {}
    for name, content in files.items():
        raw = content.encode("utf-8")
        (output_dir / name).write_bytes(raw)
        hashes[name] = hashlib.sha256(raw).hexdigest()
    for relative, raw in (attachments or {}).items():
        target = output_dir / relative
        if target.resolve() == output_dir.resolve() or output_dir.resolve() not in target.resolve().parents or not relative.startswith("attachments/"):
            raise ValueError("Attachments must remain in the attachments directory")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        hashes[relative] = hashlib.sha256(raw).hexdigest()
    manifest = dict(model_id=result["model_id"], version=result["version"], content_sha256=result["content_sha256"], files=hashes,
                    viewer_sources={name: hashlib.sha256((assets / name).read_bytes()).hexdigest()
                                    for name in ("viewer.html", "viewer.css", "viewer.js", "review-core.js", "review-ui.js")})
    (output_dir / "delivery-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    model = json.loads(args.input.read_text(encoding="utf-8-sig"))
    attachments = {}
    for item in model["input_artifacts"]:
        if item["path"].startswith("attachments/"):
            raw = (args.input.parent / item["path"]).read_bytes()
            if hashlib.sha256(raw).hexdigest() != item["sha256"]:
                raise ValueError("Attachment hash mismatch")
            attachments[item["path"]] = raw
    export(model, args.output_dir, attachments)


if __name__ == "__main__":
    main()
