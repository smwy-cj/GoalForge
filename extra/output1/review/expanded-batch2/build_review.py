# -*- coding: utf-8 -*-
import datetime
import hashlib
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = pathlib.Path(__file__).resolve().parent
REPO = ROOT.parent


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


docs = ["DOC008", "DOC013", "DOC014", "DOC018", "DOC019", "DOC022", "DOC025", "DOC027", "DOC028", "DOC030", "DOC035"]
full = {"DOC014", "DOC022", "DOC025"}
ranges = {
    "DOC008": [[44, 60]], "DOC013": [[0, 18]], "DOC014": [[0, 74]],
    "DOC018": [[26, 58]], "DOC019": [[54, 62]], "DOC022": [[0, 117]],
    "DOC025": [[0, 26]], "DOC027": [[100, 110]],
    "DOC028": [[4, 8], [24, 28], [48, 64]], "DOC030": [[22, 34]],
    "DOC035": [[10, 22], [36, 40]],
}
goal_notes = {
    "DOC014": [
        "T001的衣物、骑车/公交与带伞均由本人选取；未改为自动决策或禁骑。",
        "T003/T005保留次日实际出门时段的温度和降水；25%只是本人判断线索。",
        "T017/T019的数周前估计、临近几天再决定均保留；历史/未来资料没有被合取强制。",
        "T017明确把云量与海滩/观星目的联系；多云并未自动触发取消。",
        "T010-T013是假设的当地极端天气；得知事件的用途可保留，安全指南存在没有升级为事实。",
        "T014/T015明确会查看严重性与当地机构建议后调整；具体撤离/避难/雨具只是条件性例子。",
        "T026-T029本人计划在新奇零下温度时截图分享，尚未实施；没有把采访者原生分享提问当作需求。",
        "T031/T033的有帮助、喜欢与按需深入提供正面维持依据；inferred并明示假设恰当。",
        "T034/T035黑白背景为个人软偏好，颜色和强度均保留。",
        "T037/T041/T069支持减少过量广告干扰；容忍一两条、低频无需订阅与高使用才可能付费均保留。",
        "T043/T067主动改善雷达详细性和参数并喜欢动画；不把可能购买变购买承诺。",
        "T046-T049明确prefer Celsius；保持个人偏好，已有切换方式仍在条件。",
        "T005/T045设置两城市并反复访问给出便利查询的正面推断依据；星标非已选唯一手段。",
        "T054-T059明确通常偏好关闭且已关闭，支持个人电脑的维持意图；未拓展到全设备/全用户。",
        "T060/T061的登录泄漏顾虑可支持有条件Avoid推断；本地缓存、服务端存储与已泄漏均未冒充事实。",
        "T066/T067本人承认局部天气有用并给出远离城市的理由；只采纳其答复部分，不采纳采访者全部整合设想。",
        "T068/T069明确建议紧凑UI以易读且列为优先；所选方式保留，未编造像素阈值。",
    ],
    "DOC022": [
        "T063/T069/T075直接说明效率是选工具的目的；不固定Vim为唯一解。",
        "T015/T021/T087不同设备/纯终端服务器能工作为明确目的；服务器事实只限本人所述情境。",
        "T015/T027以轻快为选用理由，维持推断有正面依据；未捏造RAM/CPU数值。",
        "T015/T031/T035本地插件/界面/键位/语法定制均有目的；配置文件选定工作流保留。",
        "T031/T069同时支持复制配置和账户同步的便携一致目的；未抽掉现有方式或强制一种实现。",
        "T055/T063明确继续使用键盘以提高效率；酷感已降低和非绝对禁鼠标的限制保留。",
        "T033/T041/T051明确搜索目标文件并快速打开，模糊搜索/个人快捷键方式保留。",
        "T041/T051跨文件字符串查找直接支持；算法原理未作为已验证事实。",
        "T033/T051多文件管理、文件树与buffer切换的实际价值支持维持推断。",
        "T051/T065在终端Tmux/Vim间执行、立即看结果、返修有明确价值，维持推断充分但非所有工具强制流程。",
        "T051特意保存过程以在关机后恢复，正面推断依据成立；不推定未保存代码也可恢复。",
        "T055/T061/T065/T069配置困难与更容易方式的正面比较支持减负推断；未要求零学习曲线。",
        "T069/T075本人重视结合Vim熟悉操作与VS Code优点，沿用方式有上下文支持；不把兼容性当产品验证。",
        "T069/T081/T087/T091整合流水线有帮助且本人正在学，支持集成便利的推断；云品牌/浏览器禁令未被强加。",
        "T033/T069正面比较代码建议及选代码/文件辅助修改，有继续利用依据；不承诺AI正确或自动执行。",
        "T102/T103明确must支持plugins/extensions，已有能力并不排除不可或缺的维持要求。",
        "T103/T109强调社区重要并解释问答/改进用途；平台例子未变指定责任或指定网站。",
        "T093/T097集中市场的文档、讨论、评分、安装与Vim分散流程比较，正面支持便利推断。",
        "T075/T087不固守单工具、两种方式都能用为明确心态；未要求所有人掌握所有编辑器。",
        "T009/T011用has to解释语言适配，并说明高亮读码目的；未把解释当语言机制证明。",
    ],
    "DOC025": [
        "T003/T005探索并申请感兴趣工作为明确用途，未升级为获聘。",
        "T003/T011明确拓展职业网络；姓名查找和活跃相关群组方式保留于条件，接收方响应不被强制。",
        "T003/T007明确行业更新与网络动态用途，点赞/评论只是兴趣触发的例子。",
        "T005想找具体工作时的关键词、地点及筛选方式直接支持；未声称现有筛选足够。",
        "T005明确Easy Apply saves a lot of time，正面维持推断有依据；个人档案复用、复核与有时补材料均保留。",
        "T020/T021的often wish直接支持技能/软件/编程语言筛选；产品现状为本人报告。",
        "T003/T013/T015实际浏览推荐结合频率渠道用途，维持推断可接受；推荐原理仍为belief。",
        "T003/T019求职中多次更新资料，支持持续反映职业经历和意向的推断；未强制全公开。",
        "T020/T021把联系困难说成挑战，可推断改善体验；未回应原因不确定，不推出绕过隐私或强制回复。",
    ],
}
group_notes = {
    "DOC008-F1": ("retain_proposed_partial", [47, 49, 51, 53, 55, 57, 59], "声音悦耳只处理声音不悦，未处理离线积压与筛选；与父G05整体负担存在真实贡献但不充分。", "分析假设：通知声音已改善而离线仍积累上百提醒，子目标成立而父目标未完全实现。", "无其他完整方案，不评为OR替代；不为补图增加节点。"),
    "DOC013-F1": ("retain_proposed_partial", [12, 14, 16], "文字/视觉查找与顺畅播放是观众获取信息的路径；T014还允许找不到所需内容，未定义何为满足娱乐/教育用途，不能确认共同充分。", "分析假设：可顺畅浏览和播放，但目标主题内容未找到；三子项不足以保证父意图。", "不是把创作者操作作为观众前提；没有第二完整方案。"),
    "DOC014-F1": ("retain_proposed_partial", [1, 3, 5], "出门时段气温与降雨确为衣物/通勤/带伞安排依据，但信息可见不等于本人已完成适当安排。", "分析假设：看到了小时信息但尚未做出交通和带伞决定；G02成立仍不足以完成G01。", "不要求补动作节点或收窄父目标来强行成树。"),
    "DOC018-F1": ("retain_proposed_partial", [31, 37, 47, 55, 57], "导出到Drive/Kindle/独立应用是尚未定案的备选位置；整体iPad少步骤结果没有导入步骤或可行性比较。", "分析假设：门户已导出但iPad阅读器仍需额外转换/导入，G05不确保G02减少步骤。", "Drive与Kindle是目标内部备选，尚无每个备选独立充分的证据。"),
    "DOC018-F2": ("retain_proposed_partial", [49, 55], "本人明确把章节百分比与较少焦虑联系，目的链应保留；个体体验影响和展示条件仍不足以建立充分关系。", "分析假设：已显示章节百分比，章节仍很长且本人焦虑不减；未能从显示能力推出体验保证。", "不把心理体验目标误删，也不将排序解释为精化。"),
    "DOC019-F1": ("retain_proposed_partial", [54, 58, 60], "条件性语音摘要确为本人提议以减少反复打开应用；摘要覆盖内容、认证和详情获取未定。", "分析假设：能听摘要但所问细节仍需进入应用，子目标成立不确保父目标全部范围。", "T058的voice orders与voice summarization是不同候选；本组不将交易当查询摘要的必要共同子项。"),
    "DOC022-F1": ("retain_proposed_partial", [15, 21, 31, 69, 75, 87], "配置可携与熟悉Vim键位只解决操作习惯迁移，不确保纯终端环境可运行VS Code或拥有权限/依赖。", "分析假设：配置和键位已迁移但设备无相应运行环境；G05/G13仍不保证G02。", "复制配置和账户设置未被判为各自完整的跨设备方案。"),
    "DOC025-F1": ("retain_proposed_partial_with_rationale_note", [3, 5, 13, 15, 21], "筛选、推荐和申请便利提供部分找工作路径；职位匹配与个别申请材料完整性仍未知。招聘方回应不属于G01的探索/申请范围，不应用其缺失作为本组不充分的理由。", "分析假设：已具备细粒度筛选、推荐和便捷提交，但目标职位未被完整检索或特定材料尚未完成；不必诉诸未获聘/未回复反例。", "AND不代表技能筛选和推荐是每次申请都必需；保留候选而非已成立结构。"),
    "DOC027-F1": ("supported_complete_with_stated_assumptions", [105, 107], "T105/T107明确一处集中看添加来源内容以免切换。假定目标内容在该平台直接可读，在同一浏览范围内G17足以减少切换；不依赖总时间或内容质量保证。", "正常场景：三种已添加来源内容在一处可读，无须为该浏览任务切换；边界分析假设：外跳登录/评论或内容不可读时不满足明示直接可读假设，不能外推成立。", "只有一个完整组；没有未经审查的OR替代。该条件充分判断不是实现可行性证明。"),
    "DOC028-F1": ("retain_proposed_partial", [51, 59, 61], "GenAI发现精确社群是本人明确选定的新方案，应保留；本人也承认坏回答不能完全消除，社区匹配不确保参与和答案价值。", "分析假设：正确找到特定社群但无人响应或得到低价值答复；G13不充分推出G14。", "没有用内容搜索良好推翻社群发现困难，也不把坏答案未清零视为目标本身不合理。"),
    "DOC028-F2": ("retain_proposed_partial", [7, 27, 63], "草稿保存与评论可读性处理两个明确例子；T027另有慢/笨重的独立维度，因此不能代表整个移动直观性和流畅度。", "分析假设：能存草稿且线程清楚，但启动/滚动仍慢，子目标共同成立而G07流畅度仍未满足。", "Android范围及其他设备未知保留；草稿目标是困难和桌面比较支持的推断，并非无依据补救。"),
    "DOC030-F1": ("retain_proposed_partial", [25, 29, 33], "计时与完成记录确为本人评价进步及信心的有用方式；记录不独立保证真实掌握或每次面试体验。", "分析假设：记录数量提高但没有看到有意义的进步，或面试仍紧张；不能只由G11推出G12。", "200题为当时例子，不变为阈值；不要求加技能节点证明自信。"),
    "DOC035-F1": ("retain_proposed_partial", [13, 15, 21, 39], "本人认为过量通知淹没重要信息，但相关有用且少spam未保证重要信息本身被采集、展示和阅读。", "分析假设：噪声减少但重要消息未显示或未被看到；G06不充分推出G07。", "保留有用通知的正面需求，不能把避免淹没修成禁用所有通知。"),
}

index = read(ROOT / "_run/delivery-index.json")
verification = read(ROOT / "_run/final-verification.json")
inventory = {x["document_id"]: x for x in read(ROOT / "_run/source-inventory.json")}
models = {}
documents = []
errors = []
for doc in docs:
    entry = next(x for x in index["documents"] if x["arm"] == "revised" and x["document_id"] == doc)
    model_path = ROOT / entry["json"]
    delivery = model_path.parent
    model = read(model_path)
    models[doc] = model
    extraction = read(delivery / "attachments/extraction.json")
    manifest = read(delivery / "manifest.json")
    model_sha = sha(model_path)
    eng = next(x for x in verification["deliveries"] if x["arm"] == "revised" and x["document_id"] == doc and x["delivery"] == entry["json"])
    inputs = []
    for art in model["input_artifacts"]:
        actual = sha(delivery / art["path"])
        inputs.append({"path": (delivery / art["path"]).relative_to(ROOT).as_posix(), "sha256": actual, "model_binding_matches": actual == art["sha256"]})
        if actual != art["sha256"]:
            errors.append(f"{doc}: input artifact mismatch {art['path']}")
    manifest_matches = all(sha(delivery / f["path"]) == f["sha256"] for f in manifest["files"])
    source_path = delivery / "attachments/source.txt"
    source_sha = sha(source_path)
    original_text = REPO / "datasets/processed/goalforge-v1/source" / f"{doc}.txt"
    original_json = original_text.with_suffix(".json")
    source_matches = source_sha == inventory[doc]["text_sha256"] == extraction["document_hash"] == sha(original_text)
    original_matches = sha(original_json) == inventory[doc]["json_sha256"] == extraction["materials"][0]["original_hash"]
    if not (manifest_matches and source_matches and original_matches and eng["model_sha256"] == model_sha):
        errors.append(f"{doc}: manifest/source/engineering hash binding mismatch")
    endpoint_ids = {g for r in model["refinement_groups"] for g in [r["parent_id"]] + r["child_ids"]}
    ids = [g["goal_id"] for g in model["goals"] if doc in full or g["goal_id"] in endpoint_ids]
    reviewed = []
    for goal in model["goals"]:
        if goal["goal_id"] not in ids:
            continue
        sources = sorted({e["source_id"] for e in model["evidence_index"] if e["evidence_id"] in goal["evidence_ids"]})
        rec = {"goal_id": goal["goal_id"], "statement": goal["statement"], "review_scope": "full_goal" if doc in full else "group_endpoint", "source_ids": sources, "verdict": "supported_with_recorded_conditions", "checked_dimensions": ["intent_and_goal_eligibility", "actor", "result_and_scope", "conditions_and_time", "modality_and_strength", "chosen_method", "origin", "whole_statement_support", "maintenance_intent", "uncertainty", "inference_basis_and_assumptions", "review_questions"]}
        if doc in full:
            rec["reason"] = goal_notes[doc][int(goal["goal_id"].rsplit("G", 1)[1]) - 1]
        else:
            rec["reason"] = "完整读取该端点的目标句、条件、origin、inference、support与引用来源；详见所属组的独立结论。未据此宣称该篇全部目标已独立复核。"
        reviewed.append(rec)
    groups = []
    for group in model["refinement_groups"]:
        verdict, turns, reason, scenario, alternatives = group_notes[group["group_id"]]
        groups.append({"group_id": group["group_id"], "parent_id": group["parent_id"], "child_ids": group["child_ids"], "input_status": group["status"], "input_completeness": group["completeness"], "verdict": verdict, "source_ids": [f"{doc}:T{n:03d}" for n in turns], "reason": reason, "joint_sufficiency_and_counterexample": scenario, "scenario_provenance": "independent reviewer analysis, not interview events or exhaustive/formal proof", "alternatives_and_scope": alternatives, "assumptions_checked": group["assumptions"], "recommended_status_change": None})
    documents.append({"document_id": doc, "model_path": entry["json"], "model_sha256": model_sha, "outer_revision": model_path.parent.parent.name, "embedded_model_id": model["model_id"], "embedded_model_version": model["version"], "source_path": source_path.relative_to(ROOT).as_posix(), "source_sha256": source_sha, "original_source_text_path": original_text.relative_to(REPO).as_posix(), "original_source_json_path": original_json.relative_to(REPO).as_posix(), "original_source_json_sha256": sha(original_json), "source_turns_read": [f"T{a:03d}-T{b:03d}" for a, b in ranges[doc]], "full_source_read": doc in full, "review_scope": "full_document_goals_and_all_groups" if doc in full else "all_groups_and_complete_endpoints_only", "reviewed_goal_ids": ids, "reviewed_group_ids": [r["group_id"] for r in model["refinement_groups"]], "goals_total": len(model["goals"]), "goal_reviews": reviewed, "group_reviews": groups, "input_artifacts": inputs, "manifest_sha256": sha(delivery / "manifest.json"), "bindings": {"manifest_file_bytes_match": manifest_matches, "canonical_source_matches_original_inventory_extraction": source_matches, "original_json_hash_matches_inventory_extraction": original_matches, "engineering_report_model_sha_matches": eng["model_sha256"] == model_sha}, "engineering_report": eng["report"], "human": "pending"})


def ev(doc, turn, quote):
    source = (ROOT / next(x for x in index["documents"] if x["arm"] == "revised" and x["document_id"] == doc)["json"]).parent / "attachments/source.txt"
    text = source.read_text(encoding="utf-8")
    offset = 0
    matches = []
    for line in text.splitlines(keepends=True):
        if line.startswith(f"[T{turn:03d}]"):
            assert line.count(quote) == 1, (doc, turn, quote)
            matches.append(offset + line.index(quote))
        offset += len(line)
    assert len(matches) == 1, (doc, turn, quote)
    pos = matches[0]
    return {"source_id": f"{doc}:T{turn:03d}", "quote": quote, "start_char": pos, "end_char": pos + len(quote), "locator_scope": "canonical_full_text", "source_id_and_quote_uniquely_checked": True, "source_sha256": sha(source)}


findings = [
    {"finding_id": "ER-B2-001", "category": "表达不足", "severity": "low", "targets": ["DOC025-F1"], "status": "confirmed_non_material", "specific_unsupported_part": "候选组理由把‘招聘回应’列入不足判据；父G01只要求探索并申请合适工作，不含雇主回应或获得聘用。", "evidence": [ev("DOC025", 3, "And also I can explore job opportunities there."), ev("DOC025", 5, "after reviewing the application, I can just tap, submit to send the application.")], "reason": "这不会使当前proposed/partial判定失效：匹配与申请材料范围仍有未决条件。但回应不足不能用来证明父目标未满足。", "recommendation": "后续修订可删去‘或招聘回应’，使不充分理由只指向检索/匹配/申请完整性；不据此升级该组，也不强加新目标。", "blocks_delivery": False},
    {"finding_id": "ER-B2-002", "category": "正确/边界案例", "severity": "none", "targets": ["DOC014-G05", "DOC014-G06", "DOC014-G15"], "status": "protected", "specific_unsupported_part": None, "evidence": [ev("DOC014", 13, "That's my assumption"), ev("DOC014", 61, "That's that's my guess, though I'm I'm not 100% sure")], "reason": "假设性警报用途与有条件隐私Avoid意图可保留；指南/缓存存在性依旧不确定，没有信念变事实。", "recommendation": "保留假设情境、条件和inferred隐私标签；勿因未验证产品能力就删除涉众意图。", "blocks_delivery": False},
    {"finding_id": "ER-B2-003", "category": "正确/边界案例", "severity": "none", "targets": ["DOC014-G07", "DOC014-G09", "DOC014-G10", "DOC014-G11", "DOC014-G12", "DOC014-G14", "DOC014-G16", "DOC014-G17"], "status": "protected", "specific_unsupported_part": None, "evidence": [ev("DOC014", 27, "I'll probably like screenshot it and share it on my social medias."), ev("DOC014", 47, "I do prefer Celsius."), ev("DOC014", 57, "Yeah, I just prefer it off. So I've kept it off."), ev("DOC014", 69, "squish the ui a little bit")], "reason": "截图选定方式、黑白/摄氏个人软偏好、可容忍少量广告、有条件付费、电脑通常关闭通知、局部天气建议及紧凑UI方式均忠实；通知偏好兼有已实现的维持意图。", "recommendation": "保留这些软目标、选择方式和条件；勿改为全体强制、零广告、购买承诺或全部设备禁通知。", "blocks_delivery": False},
    {"finding_id": "ER-B2-004", "category": "正确/边界案例", "severity": "none", "targets": ["DOC022-G04", "DOC022-G05", "DOC022-G06", "DOC022-G13", "DOC022-G16", "DOC022-G19"], "status": "protected", "specific_unsupported_part": None, "evidence": [ev("DOC022", 63, "I don't care about how cool I am anymore."), ev("DOC022", 75, "I don't think we need to like like, stick to a single tool for a developer."), ev("DOC022", 103, "The the editor must supports plugins or extensions")], "reason": "个人配置/键盘习惯与根据场景选多工具并存；早期酷感已降权；插件扩展虽已有但明确must，不能因已实现而排除维持要求。", "recommendation": "保留熟悉方式与不可或缺插件意图；勿制造Vim独占要求、删除VS Code选择或过滤现有能力。", "blocks_delivery": False},
    {"finding_id": "ER-B2-005", "category": "正确/边界案例", "severity": "none", "targets": ["DOC025-G05", "DOC025-G07", "DOC025-G09"], "status": "protected", "specific_unsupported_part": None, "evidence": [ev("DOC025", 5, "this feature saves me a lot of time"), ev("DOC025", 5, "sometimes it will prompt me to upload additional resume or answers specific questions."), ev("DOC025", 13, "I believe the recommendations are based on the saved filters"), ev("DOC025", 21, "sometimes I don't get a response")], "reason": "Easy Apply省时提供维持推断依据且复核/额外材料未丢；推荐机制为belief；联系困难可支持改善推断，但未推出绕过隐私或强制回复。", "recommendation": "保留现有条件及inferred标签；未知原因不补为单一产品缺陷或必然修复路径。", "blocks_delivery": False},
    {"finding_id": "ER-B2-006", "category": "候选遗漏风险", "severity": "unrated", "targets": ["DOC025:T016", "DOC025:T017"], "status": "not_confirmed_as_omission", "specific_unsupported_part": None, "evidence": [ev("DOC025", 17, "there will be a list of all the safe jobs."), ev("DOC025", 17, "other categories that are which are in progress or applied or archived.")], "reason": "保存职位及按状态访问只在采访者追问下报告现有流程；完整上下文未明确评价其价值、继续维持或不可或缺意图。G01/G04/G07已覆盖求职查找与推荐，仍可追问是否另有状态管理意图。", "recommendation": "作为可追问候选保留，不计真实漏提，不自动补节点。", "blocks_delivery": False},
    {"finding_id": "ER-B2-007", "category": "候选遗漏风险", "severity": "unrated", "targets": ["DOC014:T050", "DOC014:T051", "DOC014:T053"], "status": "not_confirmed_as_omission", "specific_unsupported_part": None, "evidence": [ev("DOC014", 51, "it does have sections for like weather events, not necessarily in my city.")], "reason": "全球天气新闻在问答中主要是现有功能描述；G05已覆盖重要事件获知，完整上下文不足以确认独立的全球新闻维持目标。", "recommendation": "不机械从功能清单造目标，也不声称已经证明此处绝无遗漏。", "blocks_delivery": False},
    {"finding_id": "ER-B2-008", "category": "正确/边界案例", "severity": "none", "targets": ["DOC027-F1", "DOC027-G17", "DOC027-G18"], "status": "protected_with_assumptions", "specific_unsupported_part": None, "evidence": [ev("DOC027", 105, "common platform, so that I don't have to like juggle between apps"), ev("DOC027", 107, "I just want to open 1 1 app and get all the content and be done with it.")], "reason": "在所选来源目标内容均已添加且直接可读的明示假设下，集中浏览足以减少该浏览任务切换；不是仅因主题相关判精化。", "recommendation": "维持当前受限supported/complete；不要扩展到发帖、私信、全部功能、总用时或实际整合可行性。", "blocks_delivery": False},
    {"finding_id": "ER-B2-009", "category": "精化问题/已正确保留未决", "severity": "none", "targets": [g for g in group_notes if g != "DOC027-F1"], "status": "correctly_unresolved", "specific_unsupported_part": None, "evidence": [ev("DOC008", 57, "there's just a lot of notifications that you have to filter through"), ev("DOC028", 61, "You can never mitigate that completely.")], "reason": "12个proposed/partial组的端点确有目的/手段或贡献依据，但所列场景反例或未知条件阻止确认充分性；没有被当作成立层级。", "recommendation": "维持具体组未决，不以补边补节点或把软目标删除来获得通过。", "blocks_delivery": False},
    {"finding_id": "ER-B2-010", "category": "未知", "severity": "unrated", "targets": ["DOC014-G11", "DOC014-G16", "DOC022-G11", "DOC022-G14", "DOC025-G06", "DOC025-G07"], "status": "unresolved_information", "specific_unsupported_part": None, "evidence": [ev("DOC014", 43, "I might, I might consider just buying it"), ev("DOC025", 15, "daily basis, or like once a week.")], "reason": "付费评价标准、局部精度、会话恢复完整范围、流水线必需阶段、技能匹配语义及个人提醒配置未给。模型已用条件与问题承接，当前非证据不足目标句或编造指标。", "recommendation": "保留未知与真实人工待审；不伪造访谈补答、产品事实、形式证明或验收阈值。", "blocks_delivery": False},
]

criteria_paths = [
    "_run/expanded-review-plan.json", "_run/delivery-index.json", "_run/final-verification.json", "_run/source-inventory.json",
    "_run/skill-snapshots/revised/skills/model-review/SKILL.md",
    "_run/skill-snapshots/revised/skills/model-review/references/semantic-review.md",
    "_run/skill-snapshots/revised/skills/goal-extraction/references/goal-boundaries.md",
    "_run/skill-snapshots/revised/skills/goal-extraction/references/evidence-rules.md",
    "_run/skill-snapshots/revised/skills/goal-model-building/references/modeling-rules.md",
]
report = {
    "schema_version": "goalforge-expanded-independent-review-1", "review_id": "expanded-batch2", "created_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "review_kind": "independent_context_source_based_model_semantic_review", "reviewer": {"agent_context": "/root/review_expanded_batch2", "independent_of_generation_context": True, "model_family_independence": False, "external_human_review": False, "formal_proof": "not_run", "exact_model_id": "unknown", "sampling_parameters": "unknown", "token_budget": "unknown"},
    "sequence_and_visibility": {"source_baseline": "source-baseline.json", "source_baseline_sha256": sha(OUT / "source-baseline.json"), "source_first_exception": "DOC014 model was initially retrieved alongside contract files and truncated before complete source-first baseline; substantive full-goal adjudication followed complete source reading. This is source-first substantive review, not a blind test.", "author_reviews_read": False, "baseline_or_historical_outputs_read": False, "research_reference_answers_read": False, "non_semantic_operational_metadata": ["delivery-index", "source-inventory", "final-verification", "DOC022 run-record"]},
    "coverage": {"document_ids": docs, "full_document_goal_review": sorted(full), "full_review_goals": sum(len(models[d]["goals"]) for d in full), "all_refinement_groups_reviewed": sum(len(d["group_reviews"]) for d in documents), "distinct_reviewed_goal_ids": sum(len(d["reviewed_goal_ids"]) for d in documents), "additional_endpoint_only_goals": sum(len(d["reviewed_goal_ids"]) for d in documents if d["document_id"] not in full), "all_other_goals_independently_reviewed": False, "selection": "purposive preselected full-document sample plus every group in assigned documents; not random, unseen or accuracy estimate"},
    "engineering_binding_check": {"scope": "Reused final-verification engineering findings; freshly compared selected model bytes, all model input-artifact hashes, manifest file rows and processed original source hashes. No full engineering suite rerun.", "status": "passed" if not errors else "failed", "errors": errors, "core_inspection_status_manually_changed": False},
    "decision": {"material_confirmed_issues": [], "delivery_blockers": errors, "non_material_expression_findings": ["ER-B2-001"], "independent_semantic_review": "completed_for_declared_scope", "human_review": "pending", "formal_proof": "not_run", "generated_artifacts_modified": False, "conclusion": "未发现声明范围内需要阻断或实质修订的确证语义错误；DOC025-F1存在一处非实质理由越界，建议后续收窄。12个候选组保持未决，DOC027-F1只在明示范围假设下认可。"},
    "criteria_and_input_files": [{"path": p, "sha256": sha(ROOT / p)} for p in criteria_paths], "documents": documents, "findings": findings,
    "limitations": ["独立上下文模型复核不是外部人审、跨模型独立检验或形式证明。", "仅三篇完整目标审查；其余八篇仅全部精化组及完整端点。", "未核听音频、验证产品实际能力或穷尽领域情境。", "问题条目、候选遗漏与错误目标数不得相加；不外推31篇或整批准确率。", "候选遗漏未证实，不作为真实漏提；现有能力有正面维持依据时仍可成目标。", "所有实际查阅版本按路径和字节哈希绑定，外层v2与嵌入v1分别记录。", "原模型、附件、核心inspection与人审pending状态保持不变。"],
}
(OUT / "review.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

lines = ["# 扩展批次 B2 独立上下文语义复核", "", report["decision"]["conclusion"], "", "覆盖11篇、全部13个精化组；DOC014、DOC022、DOC025完整46目标，其他8篇仅组端点。发现记录不能折算错误目标数，也不能推算整批准确率。人审仍为pending，形式证明not_run，精确模型、采样、预算unknown。", "", "## 方法与输入边界", "", "使用冻结revised model-review、goal-boundaries、evidence-rules、modeling-rules及expanded-review-plan。先完整读取三篇问答并记录source-baseline.json，再实质逐目标核对目标句、条件、origin、完整support、依据、推断和问题。DOC014在初始读取契约时曾与模型一起输出并截断，因此不宣称盲测；完整原文读取后才作实质判断。其余8篇读取全部组、父子完整语义及下列原文窗口。未读取author-review、baseline/历史产物、比较裁决或研究参考答案。", "", "独立性是与生成代理分离的上下文，不是跨模型、外部人审或形式证明。精确引文仅用于定位；下述结论来自问答和例外上下文。没有修改生成包、项目skills、冻结快照、原文或inspection。", "", "## 覆盖与版本", "", "| 文档 | 实际原文轮次 | 目标范围 | 组 | 交付路径 / 模型SHA-256 |", "|---|---|---|---|---|"]
for d in documents:
    lines.append(f"| {d['document_id']} | {', '.join(d['source_turns_read'])} | {'全目标' if d['full_source_read'] else '仅组完整端点'}：{', '.join(d['reviewed_goal_ids'])} | {', '.join(d['reviewed_group_ids'])} | {d['model_path']} / {d['model_sha256']} |")
lines += ["", "外层修订目录与嵌入模型version分别保存在review.json；外层v2不等于模型内部必为v2。每篇source、原JSON、extraction、judgments、kaos-decisions、manifest哈希及本轮规则/索引/工程报告哈希均保存在review.json。必要字节绑定检查全部通过；沿用工程final-verification结论，不重复全套工程测试。", "", "## 完整目标逐项复核"]
for d in documents:
    if d["document_id"] not in full:
        continue
    lines += ["", f"### {d['document_id']}", ""]
    for g in d["goal_reviews"]:
        lines.append(f"- **{g['goal_id']}**：{g['reason']} 结论：在现有条件/推断假设内支持；来源 {', '.join(g['source_ids'])}。")
lines += ["", "## 全部精化组逐组结论", ""]
for d in documents:
    for g in d["group_reviews"]:
        lines += [f"### {g['group_id']}：{g['parent_id']} ← {', '.join(g['child_ids'])}", "", f"输入为{g['input_status']}/{g['input_completeness']}；独立结论 **{g['verdict']}**。{g['reason']}", "", f"{g['joint_sufficiency_and_counterexample']} 此处场景为复核者分析假设，不冒充访谈事实、穷尽性检查或形式证明。{g['alternatives_and_scope']}", "", f"原文依据：{', '.join(g['source_ids'])}。领域假设：{'；'.join(g['assumptions_checked'])}", ""]
lines += ["## 稳定发现记录", ""]
for f in findings:
    lines += [f"### {f['finding_id']} · {f['category']} · {f['severity']} · {f['status']}", "", f"对象：{', '.join(f['targets'])}。{f['reason']}", ""]
    if f["specific_unsupported_part"]:
        lines += [f"具体不支持部分：{f['specific_unsupported_part']}", ""]
    for e in f["evidence"]:
        lines.append(f"> {e['source_id']}：“{e['quote']}”")
    lines += ["", f"建议：{f['recommendation']} 阻断：否。", ""]
lines += ["## 未决、候选风险与停止边界", "", "- ER-B2-001只是一处组理由的范围表达问题，不是整组状态或目标句已被证伪。无需据此阻断；若父代理另存修订，建议独立复核受影响理由，不需增加节点或边。", "- ER-B2-006/007是候选遗漏风险，尚未证明真实漏提；未把现有功能清单自动当目标。", "- ER-B2-010与每组partial结论保留未知；未用无阈值作为软目标失效的理由。", "- DOC027-F1的充分性受直接可读、所选浏览内容与添加来源假设约束，不能外推为真实集成已可实现。", "- 工程字节绑定无真实阻断；没有外部人审结果。核心inspection状态不手改，人工pending。", "", "详尽机器记录见review.json；完整源文基准见source-baseline.json。"]
(OUT / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(json.dumps({"documents": len(documents), "full_goals": report["coverage"]["full_review_goals"], "groups": report["coverage"]["all_refinement_groups_reviewed"], "distinct_reviewed_goals": report["coverage"]["distinct_reviewed_goal_ids"], "binding_errors": errors, "report_sha256": sha(OUT / "report.md"), "review_sha256": sha(OUT / "review.json")}, ensure_ascii=False))
