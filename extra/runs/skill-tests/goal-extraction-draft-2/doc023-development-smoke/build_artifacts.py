"""Package current-assistant development decisions; does not call a model."""

import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
spec = importlib.util.spec_from_file_location("review", ROOT / "skills/goal-extraction/scripts/render_review.py")
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)
data = json.loads((HERE / "source-input.json").read_text(encoding="utf-8"))
decisions = json.loads((HERE / "candidate-decisions.json").read_text(encoding="utf-8"))
canonical = (HERE / "source.txt").read_bytes().decode("utf-8")
segments = {s["source_id"]: s for s in data["segments"]}
candidates = []
for index, decision in enumerate(decisions, 1):
    evidence = []
    for sid, quote in decision["evidence"]:
        segment = segments[sid]
        if segment["speaker"] != "Stakeholder":
            raise ValueError("Basis must come from stakeholder in this interview")
        if segment["text"].count(quote) != 1:
            raise ValueError(f"Ambiguous or missing quote: {sid}: {quote}")
        start = segment["original_locator"]["start_char"] + segment["text"].index(quote)
        end = start + len(quote)
        if canonical[start:end] != quote:
            raise ValueError("Full-text quote mismatch")
        evidence.append(dict(source_id=sid, quote=quote, role="basis", start_char=start, end_char=end))
    candidates.append(dict(candidate_id=f"DOC023-C{index:03}", category=decision["category"], subtype=decision["subtype"],
                           statement=decision["statement"], origin=decision["origin"], actor="受访者",
                           context=decision["context"], evidence_candidates=evidence,
                           classification_reason=decision["reason"], inference=decision.get("inference"), review_status="pending"))
data.update(schema_version="goalforge-extraction-draft-2", status="completed", candidates=candidates,
            review_questions=[
                dict(candidate_ids=["DOC023-C003", "DOC023-C004", "DOC023-C009"], question="内推、简历曝光及内推意愿是否分别保留？", reason="候选处于不同目的层次，留待规范化及人工审核。"),
                dict(candidate_ids=["DOC023-C008", "DOC023-C012"], question="匹配联系人与扩大可访问范围是否分别保留？", reason="准确性和访问范围不同，当前阶段不合并。"),
                dict(candidate_ids=["DOC023-C014", "DOC023-C017"], question="是否接受这两项由障碍反推的目标？", reason="推断尚未得到用户确认。")],
            limitations=["开发试运行：由当前会话助手依照 Skill 作出候选判断，非独立模型盲测。",
                         "当前会话早期接触过 DOC023 开发参考；本轮不重新读取参考，仍不能排除历史上下文影响。",
                         "仅验证已有原生文本与源文 JSON；未测试真实 Word/PPT/OCR/录音。",
                         "候选尚无人审，不报告提取准确率或效果提升。"])
data["coverage"]["scope"] = "full_document"
review.validate(data)
(HERE / "extraction.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(HERE / "goal-candidates.md").write_text(review.render(data), encoding="utf-8")
paths = [ROOT / "skills/goal-extraction/SKILL.md", *sorted((ROOT / "skills/goal-extraction/references").glob("*.md")),
         ROOT / "skills/goal-extraction/scripts/prepare_source.py", ROOT / "skills/goal-extraction/scripts/render_review.py",
         HERE / "candidate-decisions.json", HERE / "source.txt", HERE / "source-input.json", HERE / "build_artifacts.py"]
manifest = dict(test_kind="current_assistant_development_smoke", model_provider_call=False,
                independent=False, prior_reference_exposure=True, document_id="DOC023",
                turns=len(segments), candidates=len(candidates), goals=sum(c["category"] == "goal" for c in candidates),
                explicit=sum(c["origin"] == "explicit" for c in candidates), inferred=sum(c["origin"] == "inferred" for c in candidates),
                evidence_slices=sum(len(c["evidence_candidates"]) for c in candidates),
                files={p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
(HERE / "run-record.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: v for k, v in manifest.items() if k != "files"}, ensure_ascii=False))
