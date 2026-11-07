# -*- coding: utf-8 -*-
import datetime
import hashlib
import json
import pathlib

OUT = pathlib.Path(__file__).resolve().parent
ROOT = OUT.parents[1]


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


old_path = ROOT / "revised/DOC025/v1/delivery/goal-model.json"
new_path = ROOT / "revised/DOC025/v2/delivery/goal-model.json"
old = read(old_path)
new = read(new_path)
revision_path = new_path.parents[1] / "revision-record.json"
revision = read(revision_path)
manifest_path = new_path.parent / "manifest.json"
manifest = read(manifest_path)
prior_manifest = read(OUT / "review-manifest.json")
initial_checks = [
    {"path": item["path"], "sha256": sha(OUT / item["path"]), "unchanged": sha(OUT / item["path"]) == item["sha256"]}
    for item in prior_manifest["files"]
]
old_source = old_path.parent / "attachments/source.txt"
new_source = new_path.parent / "attachments/source.txt"
input_checks = [
    {"path": a["path"], "sha256": sha(new_path.parent / a["path"]), "matches": sha(new_path.parent / a["path"]) == a["sha256"]}
    for a in new["input_artifacts"]
]
checks = {
    "before_model_hash_matches_revision_record": sha(old_path) == revision["before_model_sha256"],
    "after_model_hash_matches_revision_record": sha(new_path) == revision["after_model_sha256"],
    "all_nine_goal_objects_exactly_equal": len(new["goals"]) == 9 and old["goals"] == new["goals"],
    "source_bytes_unchanged": old_source.read_bytes() == new_source.read_bytes(),
    "all_input_artifact_hashes_match": all(a["matches"] for a in input_checks),
    "all_manifest_file_hashes_match": all(sha(new_path.parent / a["path"]) == a["sha256"] for a in manifest["files"]),
    "initial_review_files_unchanged": all(a["unchanged"] for a in initial_checks),
    "group_identity_endpoints_and_status_unchanged": all(
        old["refinement_groups"][0][k] == new["refinement_groups"][0][k]
        for k in ["group_id", "parent_id", "child_ids", "kind", "status", "completeness", "evidence_ids"]
    ),
    "new_group_has_no_recruiter_response_criterion": all(
        x not in json.dumps(new["refinement_groups"][0], ensure_ascii=False)
        for x in ["招聘回应", "雇主", "回应", "聘用"]
    ),
    "human_pending": new["review"]["status"] == manifest["human"] == "pending",
    "internal_version_and_parent_from_assembler": new["version"] == "v1" and new["parent"] is None,
}
assert all(checks.values()), checks
source_text = new_source.read_text(encoding="utf-8")
evidence = []
for turn, quote in [
    (3, "And also I can explore job opportunities there."),
    (5, "sometimes it will prompt me to upload additional resume or answers specific questions."),
    (5, "after reviewing the application, I can just tap, submit to send the application."),
    (13, "I believe the recommendations are based on the saved filters"),
    (21, "I often wish there was a way to filter the jobs by specific skills or technologies"),
]:
    offset = 0
    matches = []
    for line in source_text.splitlines(keepends=True):
        if line.startswith(f"[T{turn:03d}]"):
            assert line.count(quote) == 1
            matches.append(offset + line.index(quote))
        offset += len(line)
    assert len(matches) == 1
    start = matches[0]
    evidence.append({"source_id": f"DOC025:T{turn:03d}", "quote": quote, "start_char": start, "end_char": start + len(quote), "source_id_and_quote_uniquely_checked": True})

scope = ["DOC025-G01", "DOC025-G04", "DOC025-G05", "DOC025-G06", "DOC025-G07"]
data = {
    "schema_version": "goalforge-independent-review-followup-1",
    "review_id": "expanded-batch2-followup-DOC025-v2",
    "created_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "finding_id": "ER-B2-001",
    "previous_status": "confirmed_non_material",
    "followup_status": "resolved",
    "resolved_scope": "DOC025-F1 rationale and assumptions in the specifically hashed v2 delivery",
    "original_review_preserved": True,
    "before_model": {"path": old_path.relative_to(ROOT).as_posix(), "sha256": sha(old_path), "model_id": old["model_id"], "embedded_version": old["version"]},
    "after_model": {"path": new_path.relative_to(ROOT).as_posix(), "sha256": sha(new_path), "model_id": new["model_id"], "embedded_version": new["version"], "parent": new["parent"]},
    "source": {"path": new_source.relative_to(ROOT).as_posix(), "sha256": sha(new_source), "previous_full_read": "DOC025 T000-T026 in initial independent review", "turns_reread": ["T000-T005", "T012-T015", "T020-T021"]},
    "reviewed_goal_ids": scope,
    "reviewed_group_ids": ["DOC025-F1"],
    "semantic_scope": "Reread changed group rationale/assumptions/issues and complete current parent/child semantics; retain initial full nine-goal review because all nine goal objects and source are exactly equal.",
    "current_parent_statement": new["goals"][0]["statement"],
    "current_group": new["refinement_groups"][0],
    "source_evidence": evidence,
    "semantic_assessment": {
        "scope_alignment": "新理由及假设只涉及检索/匹配、提交申请所需材料及筛选/提醒组合覆盖范围，已删除雇主回应这一父目标范围外的判据。",
        "source_support": "T003是探索职位意图；T005的复核、追加简历/问题与提交说明申请范围；T013为推荐机制的belief；T021给出细粒度技能筛选愿望。新理由没有把产品猜测、额外招聘结果或他人回应当作父目标。",
        "joint_sufficiency": "G04-G07为寻找和申请的部分支持路径；材料没有定义岗位合适的完整判据，也未证明列出路径在各申请情境中的组合覆盖。保留proposed/partial恰当，不应因本次移除不当理由就改为supported/complete。",
        "scenario_check": "复核者分析假设：已有相关筛选、提醒和便捷申请能力，但所用条件不能覆盖本人全部岗位适配条件，或个别申请流程有未说明的必需材料；不能推出已完整满足探索并申请合适机会。此场景不要求雇主回复或获聘，也不冒充访谈事实。",
        "goal_preservation": "九目标含陈述、条件、origin、inference、support、证据引用完全相同；Easy Apply的复核与补充材料、推荐机制不确定性及接收方选择边界均未退化。",
        "new_issues": [],
        "recommended_group_status": "proposed",
        "recommended_group_completeness": "partial",
    },
    "binding_checks": checks,
    "input_artifacts": input_checks,
    "revision_record": {"path": revision_path.relative_to(ROOT).as_posix(), "sha256": sha(revision_path)},
    "manifest": {"path": manifest_path.relative_to(ROOT).as_posix(), "sha256": sha(manifest_path)},
    "initial_review_file_checks": initial_checks,
    "independence": {"context": "/root/review_expanded_batch2", "author_review_read": False, "author_review_scenario_claim_independently_verified": False, "model_id": "unknown", "sampling": "unknown", "budget": "unknown", "external_human": False, "formal_proof": "not_run"},
    "status_boundaries": {"independent_semantic_recheck": "completed_for_affected_scope", "human_review": "pending", "core_inspection_manually_changed": False, "feedback_fabricated": False, "generated_artifacts_modified_by_reviewer": False},
    "delivery_blockers": [],
    "conclusion": "ER-B2-001在DOC025/v2指定哈希模型中已解决；未发现受影响范围内真实新问题。初始发现对v1的历史判断保留，v2仍为候选partial，人工待审。",
}
(OUT / "followup.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
lines = [
    "# ER-B2-001 修订后独立补查",
    "",
    data["conclusion"],
    "",
    "本次完整重读当前父G01及子G04–G07的目标、条件、origin、推断、support与问题，重读原文T000–T005、T012–T015、T020–T021，核对F1新理由与假设。九个目标对象与原文均与初审完全相同，因此沿用初审九目标完整复核，不宣称本次又全篇重审。",
    "",
    "新理由把不充分性限定于职位匹配、申请材料及筛选/提醒组合覆盖范围。T003支持探索意图，T005支持复核/补材料/提交，T013的推荐原理仍保留belief，T021明确技能筛选愿望。招聘方回应已不再作为父目标完成条件；ER-B2-001可标为本修订中已解决。",
    "",
    "G04–G07仍是部分支持路径。原文未给出岗位合适的完整判据，也未证明这些能力在各申请情境中的组合覆盖，因此维持proposed/partial恰当。分析假设：筛选、提醒和便捷申请能力均存在，但本人岗位适配条件或个别材料环节没有完整覆盖；这一反例不涉及雇主回复或获得聘用。无须增加目标、增加边或升级组状态。",
    "",
    "绑定核对全部通过：前后模型哈希与revision-record吻合，9目标完全相同、来源字节不变，全部input_artifacts与manifest文件哈希匹配，原始评审文件未变。父、子ID及组kind/status/completeness/evidence引用不变。",
    "",
    f"- 原模型：{data['before_model']['path']}，SHA-256 {data['before_model']['sha256']}",
    f"- 新模型：{data['after_model']['path']}，SHA-256 {data['after_model']['sha256']}",
    f"- 来源：{data['source']['path']}，SHA-256 {data['source']['sha256']}",
    f"- 修订记录：{data['revision_record']['path']}，SHA-256 {data['revision_record']['sha256']}",
    "",
    "外层修订目录是v2，内部version仍为冻结工具生成的v1且parent为null；不伪造feedback。没有读取author-review作为确认依据，因此不独立背书其场景文本是否修改；补查结论直接来自机器模型与原文。初始report.md/review.json保持原样，此补查只追加v2的解决状态。",
    "",
    "无真实新问题或交付阻断。核心inspection不手改，人审仍pending，形式证明not_run；精确模型、采样和预算unknown。全部逐项校验、受影响范围与输入哈希见followup.json。",
]
(OUT / "followup.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
(OUT / "followup-manifest.json").write_text(json.dumps({"review_id": data["review_id"], "files": [{"path": name, "sha256": sha(OUT / name)} for name in ["build_followup.py", "followup.md", "followup.json"]]}, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"finding_id": "ER-B2-001", "status": "resolved", "new_issues": [], "blocking": [], "checks": checks, "followup_json_sha256": sha(OUT / "followup.json")}, ensure_ascii=False))
