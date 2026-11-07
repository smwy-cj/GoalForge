# self-review（attempt-03，最终交付）

> **性质说明：本文是生成方自检，不是独立语义评审。** 同一会话既生成目标又做自查，不构成独立复核，也不代表人工采纳。独立语义审查、形式证明、人工接受均未执行（见第 5 节）。

## 1. 生成方自检

### 1.1 候选是否被压薄

- 原文 104 轮，按 4 轮/步长 2 切成 51 个窗口，逐窗捕获 41 条原始候选；单窗最多 5 条（W0007 T012–T015 的流程句）。
- 10 个窗口无候选：W0003（自我介绍/过渡）、W0032–W0034（可靠性确认后的情境题澄清）、W0038–W0042（BCC 含义确认与“用邮件之前”的回忆）、W0051（收尾致谢）。均为问答澄清或背景，无达到/维持/避免/改善某状态的意图，属真空窗而非漏采。
- 未先把原文压成“主要需求”再回填：候选保留了口语原文的复合表达（如 C007 的完整日常流程、C034 的转发+BCC 合句），拆分发生在整理阶段，并在 `entries` 中逐条记录去向。

### 1.2 复合候选的拆分与合并是否合理

- 拆分 1 处：C034 → G013（转发）与 G014（BCC 群发）。理由是同一回答点名两个可独立满足的能力；共同条件“截止日期情境”同时传入两项，未丢条件。
- 合并 12 处，均为同义或同目的不同侧面，例如 C009/C010/C011 → G006（同一“收件箱可控”目的下的两项删除方式与分账户策略）、C024 → G010（T039 未完成句由 T041 补全）、C028/C029 → G001（同一目标的频次与理由）。合并理由写在 `entries.reason`，可逐条回查。
- 未因动词数量拆点：T015 的“打开浏览器→扫描→加星→删除→阅读”保留为整条候选后整体排除（现状流程），未拆成五个目标。

### 1.3 条件、否定、强度、例外是否丢失

保留在 statement 或 context 的关键限定：

- 条件：G012“仅当重要度识别真正可靠”、G013/G014“截止日期情境”、G001“求职期间”。
- 否定/取舍：G007“宁可多收垃圾邮件也不忽略重要消息”，未扩写为“零误判”；G012“不完全依赖 AI”。
- 强度：G008/G009 保留偏好语气（“would probably be better”“ideal scenario”）；G016 保留受访者自评“probably not that practical”；G005 保留“rare”；G019 按正面评价推断为偏好而非强制。
- 例外/相反证据：T033 明确“不担心安全、不发机密邮件”→ 未建安全目标（C019 排除）；T061 无崩溃/卡顿 → 未建可靠性性能目标（C033 排除）。

### 1.4 是否有为凑层级造根或造组

- 未造根目标：G017（内置 AI 协助读写）有原文直述（T037“the feature I want”、T091 未来第一需求），不是抽象摘要节点；其余目标保持多根、互不隶属。
- 精化组仅 1 个（GR1，proposed/partial），成立组 0 个。理由是写侧附件提醒（G019）与格式调整不在组内、阅读侧受访者自述“AI 可能漏掉重要消息”（T059），无法声称整组共同充分；已在 checks 中记录反例、在 questions 中保留待确认。未为凑层级把它标成 supported+complete。
- 联系仅 4 条（3 条 specialization、1 条 operationalization），均写明方向、条件、假设与关系原句；未把“相关/同主题/先后操作”写成联系，也未给 G013/G014、G019 等旁支强行连边。

### 1.5 自检中仍存疑的点

- G006 把受访者“自己的整理习惯＋目的”写成一个保持型目标，是否应解读为新客户端要求，属边界判断；已写入问题，未擅自升级为强制功能。
- G018、G019 为推断目标（障碍的反面、正面评价的保留意愿），推理步骤与假设已写明；若评审要求“只保留直述”，这两项应降为问题而非目标。
- G015 只保留“搜索最高优先、每日使用”，日程排第二、标签过滤可由搜索承担仅存于 context；若评审认为排序本身即需求，则需补建节点。

## 2. 工程检查实际结果（attempt-03）

`coverage_check`：

```json
{"exit_code": 0, "structure": "passed", "workflow": "recorded", "pending": [],
 "counts": {"source_segments": 104, "windows": 51, "raw_candidates": 41, "final_goals": 20,
            "source_checks": 12, "actual_passes": 1,
            "dispositions": {"exclude": 10, "keep": 18, "merge": 12, "split": 1}}}
```

`inspection`：

```json
{"structure": "passed", "readiness": "reviewable", "independent_semantic": "not_run",
 "formal_proof": "not_run", "human": "pending"}
```

`counts`：

```json
{"goals": 20, "relations": 4, "groups": 1, "established_groups": 0, "raw_candidates": 41,
 "support_labels": {"direct": 18, "inferred": 2, "insufficient": 0, "contradicted": 0},
 "issues": 9, "blocking_issues": 0}
```

其他：`tracing_status = completed`；`declared_vs_effective_downgraded = []`（无被工具降级的 direct/inferred）；`warnings = []`（无歧义引文）；51 个窗口全部记为 processed。

模型内 9 条 issue 全部为 `blocking=false`：8 条来自 `review_questions`/`decisions.questions`，1 条是工具对未成立组 GR1 的自动提示。

## 3. 未决问题清单

来自 `review_questions` 与 `decisions.questions`：

1. G016：类别/协议邮件设想同段自评“probably not that practical”，保留为弱需求还是仅作备选设想。
2. G006：“收件箱可控”无量化标准；删除与分账户是现状习惯，是否要求新客户端支持。
3. G012：“unless it's really reliable”的可靠性判定方式与阈值缺失。
4. G018：未送达问题的范围（邮件类型、是否含验证码）与可接受处理方式（重发/告警/回执）未说明。
5. G020：读信耗时无量化指标，验收方式（是否以摘要替代通读）未知。
6. GR1：缺写侧附件提醒（G019）与格式调整，阅读侧存在 AI 漏判反例；补入子目标还是保持不成立需人工定。
7. R4：摘要减少读信时间属分析判断，原文只给“会很有帮助”的期望。
8. 模型级：采访者提出的周期摘要（T054：3 封摘要代替 30 封）仅获“could be one solution”，未建目标，是否需要补入。

blocking issue：无。

## 4. 实际执行情况

- 原文阅读：整篇精读 2 遍（第一遍通读 104 轮并逐窗捕获；第二遍全篇校正，专查指代、问答范围、条件继承、让步、例外与相反证据，含 T039→T041 的未完成句、T071→T075 的 BCC 复述、T087 的排序、T091–T093 的自评不确定）。
- 补查轮次：1 轮全篇校正，未另开定向补查；无候选需要另记 pass_id（全部 41 条候选均落在 P1 的窗口处理范围内）。
- 修复次数：2 次（attempt-02 修 C035 处置映射；attempt-03 修 S6 证据 role）。两次均为工具点名的记录/引用问题，未改目标正文、判断标签、关系或组。
- 耗时：未精确计时；按会话进程自报约 60–90 分钟（不可核对）。
- 停止原因：51 窗口处理完毕、全篇校正完成、coverage 结构通过且无 pending；剩余缺口均为原文本身未给出（阈值、采纳、可靠性判定），无新证据可解，按限制保留。

## 5. 没有做的事

- 独立语义审查：not_run（本文件为生成方自检）。
- 形式证明：not_run（精化充分性只是编制者判断，工具只校验结构与引用）。
- 人工接受：pending（`review.status = pending`，模型内 `human: pending`）。
- 覆盖检查的 `workflow=recorded` 只表示去向与声明范围已记录，不代表意图穷尽或语义完整。

## 6. 交付路径

`attempt-03/delivery/`（`goal-model.html`、`goal-model.json`、`goal-model.md`、`goal-model.svg`、`goal-relations.svg`、`manifest.json`、`attachments/`）。attempt-01、attempt-02 的产物与 `repair-log.md` 原样保留，未回改。
