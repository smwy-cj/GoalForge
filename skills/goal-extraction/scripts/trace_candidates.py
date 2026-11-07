"""Locate evidence deterministically; semantic judgments must be supplied separately."""

import argparse
import hashlib
import json
from pathlib import Path


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def object_hash(value):
    return sha(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8"))


def is_goal(data, candidate):
    if data.get('schema_version') == 'goalforge-extraction-3':
        # Full validation runs at template/trace entry; no category is needed.
        return True
    return candidate['category'] == 'goal'


def validate_input(data):
    if data.get('schema_version') == 'goalforge-extraction-3':
        import sys
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from simple_candidates import validate
        validate(data)


def judgment_template(data, input_bytes=None):
    """Blank authoring template, never copy/stamp old semantic decisions as current."""
    validate_input(data)
    return dict(schema_version="goalforge-semantic-judgments-1",
                input_binding=dict(data_sha256=object_hash(data), input_sha256=sha(input_bytes) if input_bytes is not None else None),
                judgments={c["candidate_id"]: dict(target_statement=c["statement"], label=None, rationale="", supported_parts=[],
                              unsupported_parts=[], assumptions=[], reasoning_steps=[]) for c in data["candidates"] if is_goal(data, c)})


def validate_judgments(data, bundle, input_sha256=None):
    if not isinstance(bundle, dict) or bundle.get("schema_version") != "goalforge-semantic-judgments-1":
        raise ValueError("Version-bound semantic judgments required; generate a blank judgment template and re-author decisions for this input")
    binding = bundle.get("input_binding", {})
    if binding.get("data_sha256") != object_hash(data) or (input_sha256 is not None and binding.get("input_sha256") != input_sha256):
        raise ValueError("Semantic judgment input version/hash mismatch")
    judgments = bundle.get("judgments")
    targets = {c["candidate_id"]: c for c in data["candidates"] if is_goal(data, c)}
    if not isinstance(judgments, dict) or not set(judgments).issubset(targets):
        raise ValueError("Unknown semantic judgment target")
    for cid, judgment in judgments.items():
        if not isinstance(judgment, dict) or judgment.get("target_statement") != targets[cid]["statement"]:
            raise ValueError("Semantic judgment target statement differs from current input")
        if judgment.get("label") not in {"direct", "inferred", "insufficient", "contradicted"} or not isinstance(judgment.get("rationale"), str) or not judgment["rationale"].strip():
            raise ValueError("Invalid or unfinished semantic judgment")
        for key in ("supported_parts", "unsupported_parts", "assumptions", "reasoning_steps"):
            if not isinstance(judgment.get(key, []), list) or not all(isinstance(x, str) for x in judgment.get(key, [])):
                raise ValueError("Semantic judgment detail must be a string array")
    return judgments


def occurrences(text, quote):
    starts, pos = [], 0
    while quote:
        pos = text.find(quote, pos)
        if pos < 0:
            break
        starts.append(pos)
        pos += 1
    return starts


def locate(evidence, segment, canonical, expected_hash, index):
    version = "unverified" if canonical is None or not expected_hash else (
        "verified" if sha(canonical.encode("utf-8")) == expected_hash else "version_mismatch")
    result = dict(evidence_id=f"E{index:04}", source_id=evidence.get("source_id"),
                  material_id=segment.get("material_id") if segment else None,
                  quote=evidence.get("quote", ""), evidence_role="context" if evidence.get("role") == "context" else "supporting",
                  location_status="source_unavailable", verification_scope="none", start_char=None, end_char=None,
                  candidate_locations=[], original_locator=segment.get("original_locator", {}) if segment else {},
                  recognition_status=segment.get("recognition_status", "unknown") if segment else "unknown",
                  source_version_status=version, location_reason="来源片段不可用。")
    if segment is None or version == "version_mismatch":
        if version == "version_mismatch":
            result["location_reason"] = "标准全文版本不符，停止使用旧位置。"
        return result
    quote = result["quote"]
    starts = occurrences(segment["text"], quote)
    result.update(location_status="not_found", verification_scope="segment", location_reason="指定片段未找到原提交引文。")
    if not starts:
        return result
    base = segment.get("original_locator", {}).get("start_char")
    full = (canonical is not None and type(base) is int and base >= 0
            and canonical[base:base + len(segment["text"])] == segment["text"])
    if canonical is not None and not full:
        segment_locations = occurrences(canonical, segment["text"])
        if not segment_locations:
            result.update(location_status="not_found", verification_scope="full_text",
                          location_reason="提供的片段不在标准全文中，不能使用片段内的命中冒充源文证据。")
            return result
        if len(segment_locations) == 1:
            base, full = segment_locations[0], True
    supplied_start, supplied_end = evidence.get("start_char"), evidence.get("end_char")
    if full and type(supplied_start) is int and type(supplied_end) is int:
        local_start = supplied_start - base
        if local_start in starts and supplied_end == supplied_start + len(quote):
            starts = [local_start]
    result["candidate_locations"] = [dict(source_id=result["source_id"], segment_start=p, segment_end=p + len(quote),
                                           start_char=base + p if full else None,
                                           end_char=base + p + len(quote) if full else None) for p in starts]
    if len(starts) > 1:
        result.update(location_status="ambiguous", location_reason="片段内多处命中，未选定唯一位置。")
        return result
    result.update(location_status="exact", verification_scope="full_text" if full else "segment",
                  location_reason="原文片段唯一精确命中；位置核验不代表语义支持。")
    if full:
        result.update(start_char=base + starts[0], end_char=base + starts[0] + len(quote))
    return result


def trace(data, judgments=None, canonical=None, input_sha256=None):
    validate_input(data)
    bundle = judgments
    judgments = validate_judgments(data, bundle, input_sha256) if bundle is not None else {}
    candidates = data["candidates"]
    ids = {c["candidate_id"] for c in candidates}
    if len(ids) != len(candidates) or not set(judgments).issubset(ids):
        raise ValueError("Duplicate targets or unknown judgment target")
    segments = {s["source_id"]: s for s in data["segments"]}
    if len(segments) != len(data["segments"]):
        raise ValueError("Duplicate source_id")
    traces, counter = [], 0
    for c in candidates:
        if not is_goal(data, c):
            continue
        evidence, issues = [], []
        for item in c["evidence_candidates"]:
            counter += 1
            found = locate(item, segments.get(item["source_id"]), canonical, data.get("document_hash"), counter)
            evidence.append(found)
            if found["source_version_status"] == "version_mismatch":
                issues.append(dict(code="version_mismatch", reason="原文版本校验失败。"))
            if found["recognition_status"] in {"ocr_unverified", "transcript_unverified"}:
                issues.append(dict(code="recognition_risk", reason="证据来自未经人工确认的识别稿。"))
        judgment = judgments.get(c["candidate_id"])
        if judgment:
            if judgment["label"] not in {"direct", "inferred", "insufficient", "contradicted"} or not judgment["rationale"].strip():
                raise ValueError("Invalid semantic judgment")
            support = {k: judgment.get(k, []) for k in ("supported_parts", "unsupported_parts", "assumptions", "reasoning_steps")}
            support.update(label=judgment["label"], rationale=judgment["rationale"])
            if support["label"] in {"direct", "inferred"} and support["unsupported_parts"]:
                support.update(label="insufficient", rationale="当前整句仍有不受支持部分；原提交判断保留，需收窄表述或补充依据。")
                issues.append(dict(code="partial_support", reason="局部支持不能证明完整目标；请核对列出的不受支持部分。"))
        else:
            support = dict(label="insufficient", rationale="尚未进行语义判断；此标签不代表已判定原文缺少支持。",
                           supported_parts=[], unsupported_parts=[], assumptions=[], reasoning_steps=[])
            issues.append(dict(code="semantic_not_run", reason="需另行提供语义判断。"))
        if not any(e["location_status"] == "exact" and e["evidence_role"] != "context" for e in evidence):
            support.update(label="insufficient", rationale="未核验到可用的目标依据，保留原提交判断但不宣称支持。")
            issues.append(dict(code="no_verified_basis", reason="依据缺失、定位歧义或版本不符。"))
        if judgment and ((c["origin"] == "explicit" and judgment["label"] == "inferred") or
                         (c["origin"] == "inferred" and judgment["label"] == "direct")):
            issues.append(dict(code="origin_mismatch", reason="来源与支持标签不同；两者不必相等，请在判断理由中解释差异，未自动覆盖原值。"))
        traces.append(dict(target_id=c["candidate_id"], target_kind=data.get("target_kind", "candidate"), statement=c["statement"],
                           document_id=data["document_id"], submitted_evidence=evidence, located_evidence=[],
                           search_scope=dict(source_ids=[e["source_id"] for e in evidence], policy="仅核对指定片段，不宣称全文穷尽检索"),
                           support=support, submitted_semantic_judgment=judgment, issues=issues,
                           suggested_changes=[], review_status="pending"))
    incomplete = any(any(i["code"] in {"semantic_not_run", "version_mismatch", "no_verified_basis"} for i in t["issues"]) for t in traces)
    return dict(schema_version="goalforge-tracing-draft-1", input_artifact={}, target_model=data.get("target_model"),
                semantic_binding=copy_binding(bundle) if bundle is not None else None,
                sources=[dict(document_id=data["document_id"], expected_hash=data.get("document_hash"),
                              actual_hash=sha(canonical.encode("utf-8")) if canonical is not None else None,
                              availability="available" if segments else "source_unavailable")],
                status="partial" if incomplete else "completed", traces=traces, review_questions=[],
                limitations=["定位工具不判断语义；语义结论来自另外保存的当前助手或人工判断，非独立审核。",
                             ("处理目标清单中已有目标；不会自动新增或改写目标。" if data.get('schema_version') == 'goalforge-extraction-3' else
                              "仅处理候选中 category=goal 的目标；其他诊断项仍留在提取产物中。")])


def copy_binding(bundle):
    return dict(schema_version=bundle["schema_version"], input_binding=dict(bundle["input_binding"]), bundle_sha256=object_hash(bundle))


def render(data):
    def text(value):
        return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    labels = dict(direct="直接支持", inferred="推断支持", insufficient="支持不足或尚未判断", contradicted="存在反证")
    lines = ["# 目标证据追溯审核文档", "", "定位核验与语义判断分开；本文件不表示人工确认。", ""]
    for t in data["traces"]:
        lines += [f"## {text(t['target_id'])} {text(t['statement'])}", "",
                  f"支持判断：{labels[t['support']['label']]}", "", text(t["support"]["rationale"]), ""]
        for e in t["submitted_evidence"] + t["located_evidence"]:
            lines += [f"> {text(e['quote']).replace(chr(10), chr(10) + '> ')}", "",
                      f"来源：{text(e['source_id'])}；定位：{e['location_status']}；范围：{e['verification_scope']}；"
                      f"全文位置：{e['start_char']}—{e['end_char']}；识别状态：{e['recognition_status']}", ""]
        if t["support"]["assumptions"]:
            lines += ["推断假设：" + text("；".join(t["support"]["assumptions"])), ""]
        lines += ["问题：" + text("；".join(i["reason"] for i in t["issues"]) or "未另列问题"), "",
                  "人工决定：", "", "修改意见：", "", "审核备注：", ""]
    lines += ["## 限制", ""] + ["- " + text(x) for x in data["limitations"]]
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("extraction", type=Path)
    parser.add_argument("output_dir", type=Path, nargs="?")
    parser.add_argument("--source", type=Path)
    parser.add_argument("--judgments", type=Path)
    parser.add_argument("--judgment-template", type=Path, help="Write a fresh blank, version-bound template; no tracing is run")
    parser.add_argument("--review-md", action="store_true", help="Also render the optional human tracing report")
    args = parser.parse_args()
    raw = args.extraction.read_bytes()
    data = json.loads(raw.decode("utf-8-sig"))
    if args.judgment_template:
        if args.judgments or args.output_dir:
            parser.error("Template generation cannot be combined with tracing outputs or judgments")
        args.judgment_template.parent.mkdir(parents=True, exist_ok=True)
        with args.judgment_template.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(judgment_template(data, raw), handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        return
    if args.output_dir is None:
        parser.error("A fresh output directory is required for tracing")
    canonical = args.source.read_bytes().decode("utf-8") if args.source else None
    judgments = json.loads(args.judgments.read_text(encoding="utf-8-sig")) if args.judgments else None
    result = trace(data, judgments, canonical, sha(raw))
    result["input_artifact"] = dict(path=str(args.extraction), sha256=sha(raw), model_version=data["schema_version"])
    if data.get("target_model"):
        result["target_model"] = data["target_model"]
    if args.judgments:
        result["judgment_artifact"] = dict(path=str(args.judgments), sha256=sha(args.judgments.read_bytes()))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    human_report = args.review_md or data.get('schema_version') != 'goalforge-extraction-3'
    for name in (["tracing.json", "goal-tracing-review.md"] if human_report else ["tracing.json"]):
        if (args.output_dir / name).exists():
            parser.error("Use fresh outputs to preserve earlier runs")
    (args.output_dir / "tracing.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if human_report:
        (args.output_dir / "goal-tracing-review.md").write_text(render(result), encoding="utf-8")


if __name__ == "__main__":
    main()
