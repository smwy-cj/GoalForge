"""Render the human review document from extraction JSON; no model calls."""

import argparse
import json
from pathlib import Path


LABELS = {
    "goal": "目标", "action": "动作", "obstacle": "障碍",
    "preference": "偏好", "uncertain": "待判断",
    "explicit": "显式", "inferred": "推断", "pending": "待审核",
    "completed": "已完成所提供材料的处理", "partial": "部分处理",
    "input_error": "无法处理输入", "basis": "依据", "context": "上下文",
    "achievement": "达成结果", "maintenance": "维持状态", "quality": "质量要求",
    "avoidance": "避免结果", "interaction": "操作步骤", "workaround": "临时应对",
    "difficulty": "使用困难", "limitation": "能力或权限限制", "solution": "方式偏好",
    "experience": "体验偏好", "ambiguous": "语义不明", "constraint": "约束归属待定",
    "proposed": "未确认提议", "recognition": "识别待确认", "unspecified": "未细分",
    "native_text": "原生文本", "ocr_unverified": "文字识别稿，未经人工确认",
    "transcript_unverified": "录音转写稿，未经人工确认", "human_verified": "人工已核验",
    "processed": "已处理", "unprocessed": "未处理", "full_document": "完整文档",
    "provided_material": "本次提供的材料", "partial_document": "部分文档",
}


def label(value):
    return LABELS.get(value, value)


def locator_text(locator):
    names = {"paragraph": "段落", "slide": "幻灯片", "page": "页码", "line_start": "起始行",
             "line_end": "结束行", "time_start_ms": "起始毫秒", "time_end_ms": "结束毫秒",
             "turn": "轮次", "start_char": "全文起始位置", "end_char": "全文结束位置"}
    return "；".join(f"{names.get(k, k)}：{v}" for k, v in locator.items()) or "原件位置未确定"


def safe(value):
    """Display material as text, including in Markdown tables."""
    return (str(value).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace("|", "&#124;")
            .replace("`", "&#96;").replace("[", "&#91;")
            .replace("]", "&#93;").replace("*", "&#42;")
            .replace("_", "&#95;").replace("\n", "<br>"))


def validate(data):
    if data.get("schema_version") == "goalforge-extraction-3":
        from simple_candidates import validate as validate_simple
        return validate_simple(data)
    if data["schema_version"] != "goalforge-extraction-draft-2":
        raise ValueError("Unsupported schema version")
    if data["status"] not in {"completed", "partial", "input_error"}:
        raise ValueError("Invalid status")
    segments = {s["source_id"]: s for s in data["segments"]}
    if len(segments) != len(data["segments"]):
        raise ValueError("Duplicate source_id")
    materials = {m["material_id"] for m in data["materials"]}
    if len(materials) != len(data["materials"]):
        raise ValueError("Duplicate material_id")
    if any(s["material_id"] not in materials for s in segments.values()):
        raise ValueError("Unknown material reference")
    ids = {c["candidate_id"] for c in data["candidates"]}
    if len(ids) != len(data["candidates"]):
        raise ValueError("Duplicate candidate_id")
    if not set(data["coverage"]["source_ids"]).issubset(segments):
        raise ValueError("Unknown coverage reference")
    if data["status"] == "input_error" and (ids or segments or data["coverage"]["source_ids"]):
        raise ValueError("Unreadable input must not contain extracted content")
    for c in data["candidates"]:
        if c["category"] not in {"goal", "action", "obstacle", "preference", "uncertain"}:
            raise ValueError("Invalid category")
        if c["review_status"] != "pending":
            raise ValueError("Draft renderer accepts unreviewed output only")
        if not c["statement"].strip():
            raise ValueError("Empty statement")
        if c["category"] == "goal":
            if c["origin"] not in {"explicit", "inferred"}:
                raise ValueError("Goal origin required")
            if not any(e["role"] == "basis" for e in c["evidence_candidates"]):
                raise ValueError("Goal basis required")
        elif c["origin"] is not None:
            raise ValueError("Non-goal origin must be null")
        if c["origin"] == "inferred":
            inf = c["inference"]
            if not inf or not inf["reason"].strip():
                raise ValueError("Inference reason required")
            if not set(inf["basis_candidate_ids"]).issubset(ids):
                raise ValueError("Unknown inference reference")
        elif c["inference"] is not None:
            raise ValueError("Unexpected inference")
        for e in c["evidence_candidates"]:
            if e["source_id"] not in segments:
                raise ValueError("Unknown evidence reference")
            if not e["quote"] or e["quote"] not in segments[e["source_id"]]["text"]:
                raise ValueError("Evidence quote is not in the referenced segment")
            if e["role"] not in {"basis", "context"}:
                raise ValueError("Invalid evidence role")
            start, end = e["start_char"], e["end_char"]
            if (start is None) != (end is None):
                raise ValueError("Offsets must both be null or present")
            if start is not None and (type(start) is not int or type(end) is not int or start < 0 or end <= start):
                raise ValueError("Invalid offsets")
    for q in data["review_questions"]:
        if not set(q["candidate_ids"]).issubset(ids):
            raise ValueError("Unknown review question reference")
    return segments


def render(data):
    if data.get("schema_version") == "goalforge-extraction-3":
        from simple_candidates import render as render_simple
        return render_simple(data)
    segments = validate(data)
    lines = ["# 目标候选人工审核文档", "", "候选尚未经过人工确认，请在每项下填写决定及意见。", "",
             "## 材料与处理范围", "", f"- 文档编号：{safe(data['document_id'])}",
             f"- 处理状态：{LABELS[data['status']]}"]
    for m in data["materials"]:
        lines.append(f"- 原始材料：{safe(m['file_name'])}（{safe(label(m['processing_status']))}）")
    lines += [f"- 转换稿：{safe(data['conversion']['canonical_text_path'] or '未生成')}",
              f"- 转换方法：{safe(data['conversion']['method'])}",
              f"- 处理范围：{safe(label(data['coverage']['scope']))}", "", "## 目标候选概览", "",
              "| 编号 | 目标表述 | 类型 | 来源 | 状态 |", "|---|---|---|---|---|"]
    goals = [c for c in data["candidates"] if c["category"] == "goal"]
    for c in goals:
        lines.append("| " + " | ".join(safe(v) for v in [c["candidate_id"], c["statement"], label(c["subtype"]), LABELS[c["origin"]], "待审核"]) + " |")
    if not goals:
        lines += ["", "本次没有可列出的目标候选；请查看处理限制和诊断项。"]
    lines += ["", "## 全部候选与审核栏", ""]
    for c in data["candidates"]:
        lines += [f"### {safe(c['candidate_id'])} {safe(c['statement'])}", "",
                  f"- 类别：{LABELS[c['category']]}；子类：{safe(label(c['subtype']))}",
                  f"- 用途：{'目标候选' if c['category'] == 'goal' else '诊断项，尚非目标'}",
                  f"- 来源：{LABELS.get(c['origin'], '不适用')}",
                  f"- 主体：{safe(c['actor'] or '未确定')}",
                  f"- 情境与条件：{safe('；'.join(c['context']) or '无额外说明')}",
                  f"- 分类理由：{safe(c['classification_reason'])}", "", "原文依据：", ""]
        for e in c["evidence_candidates"]:
            s = segments[e["source_id"]]
            loc = locator_text(s["original_locator"])
            lines += [f"> {safe(e['quote'])}", "",
                      f"位置：{safe(s['material_id'])} / {safe(e['source_id'])} / {safe(loc)}；"
                      f"角色：{LABELS[e['role']]}；识别状态：{safe(label(s['recognition_status']))}", ""]
        if c["inference"]:
            inf = c["inference"]
            lines += [f"推断理由：{safe(inf['reason'])}", "",
                      f"关联诊断：{safe('、'.join(inf['basis_candidate_ids']) or '直接依据原文')}", "",
                      f"推断假设：{safe('；'.join(inf['assumptions']) or '无额外假设')}", ""]
        lines += ["人工决定（保留 / 修改 / 排除 / 暂缓）：", "", "修改后表述：", "", "审核意见：", ""]
    lines += ["## 待确认问题", ""]
    for q in data["review_questions"]:
        lines += [f"- {safe('、'.join(q['candidate_ids']) or '全局')}：{safe(q['question'])} 原因：{safe(q['reason'])}"]
    if not data["review_questions"]:
        lines.append("未另列问题。")
    lines += ["", "## 转换风险、遗漏与限制", ""]
    issues = data["conversion"]["issues"] + data["coverage"]["omissions"] + data["limitations"]
    lines.extend(f"- {safe(item)}" for item in issues)
    if not issues:
        lines.append("未记录额外限制；候选仍需人工审核与后续追溯。")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve():
        parser.error("Input JSON and review document must use different paths")
    data = json.loads(args.input.read_text(encoding="utf-8-sig"))
    content = render(data)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation also protects hand-written comments from a check/write race.
    try:
        with args.output.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
    except FileExistsError:
        parser.error("Existing review document preserved; choose a fresh output path")


if __name__ == "__main__":
    main()
