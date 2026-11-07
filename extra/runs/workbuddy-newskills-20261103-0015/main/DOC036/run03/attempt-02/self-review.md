# 生成方自检与交付记录（DOC036 / run03 / attempt-02）

> **明确标注：本文是「生成方自检」，不是独立语义评审。** 独立语义审查 `not_run`、形式证明 `not_run`、人工接受 `pending`。程序检查通过、覆盖记录为 recorded，均不表示语义穷尽或精化可成立。

## 1. 生成方自检（生成方自检，非独立语义评审）

- **候选是否被压薄：否。** 按 4 轮窗口/步长 2 处理，38 个窗口全部 `processed`，逐窗捕获 70 条原始候选；T010 / T012 / T014 / T016 / T024 / T026 / T030 / T032 / T036 / T044 / T052 / T056 / T058 / T062 等超长复合段的多个子意图分别捕获，原始候选保留完整复合表达，未先压成十几条"主要需求"、未设数量上限。寒暄/简短确认窗口无意图，仅记录 `processed`。
- **复合目标是否拆分：是，按独立意图依据拆。** T010 拆为 G001（特殊场合买特定礼物）、G003（看联系方式并联系下单）、G005（服装看设计→去实体市场求购同款）；C052（采访者两方面总结）按 `split` 映射 G008+G009；C042 拆为 G009（限制/管理使用）与 G010（避免被无意识影响）。操作步骤（找不到时加地点名、登出/删应用/删历史、情人节期间保持登录）、前提条件、同一对象的多个限定未机械拆分。
- **条件/否定/强度/方式是否丢失：保留。** `mainly`/`for example`（G001）、`always prefer`（G004，偏好不升 must）、`would have loved`/`wish`/`hoped`（G008，愿望不升强制）、`tend to be careful`（G015）、`have to deliver before I pay you`（G012，明确强度）、"匿名"与"免登录"两层、"若未立即看到就加地点名"（G002 局部条件）、私密账户/只在需要时用等维持与避免型意图均保留；状态、维持、避免型目标未因缺动词删除。T058 标价提议后的自我让步作为相反证据保留，G017 如实判 `insufficient`，**未升级**。采访者 T071 的 `anonymous posting` 因仅获泛泛确认（T072 "Yeah. Yes."）未升级为目标，写入问题。
- **精化组是否有反例未解决：无成立组，故不存在"成立组带未解决反例"情形。** 逐条检查了 G011←{G012,G013}、G015←{G014}、购物流程组及 supported+complete 所需 normal/exception 场景，均因原文未声称"共同满足足以实现"而保留为空组 + 具体问题（详见第 6 节），未绘成成立层级。
- **是否有为凑层级造根：否。** 未提取泛化父目标/根目标；G001/G005/G006/G007 为并列用例或具体情境，未强行拼 general–special 配对；`groups=[]`、0 成立组。
- **一目标一核心动作**：17 个最终目标各为一个核心动作及其预期结果；`origin` 与 `support` 分别判断，G007 为 `inferred`（依使用动机，写明假设）、G017 为 `insufficient`，其余 15 个 `direct`；`direct`/`inferred` 的 `unsupported_parts` 均为空数组。

## 2. 工程检查实际结果（复制自 attempt-summary.json / inspection.json）

- `coverage_check`：`exit_code=0`，`structure=passed`，`workflow=recorded`，`pending=[]`；`counts`：source_segments=77、windows=38、raw_candidates=70、final_goals=17、source_checks=18、actual_passes=1、dispositions={keep:14, merge:15, exclude:38, split:2, uncertain:1}。
- `inspection`：`structure=passed`，`readiness=blocked`，`independent_semantic=not_run`，`formal_proof=not_run`，`human=pending`。
- `counts`：goals=17、relations=3、groups=0、established_groups=0、raw_candidates=70、support_labels={direct:15, insufficient:1, inferred:1, contradicted:0}、issues=21、blocking_issues=1。
- `tracing_status=completed`；`declared_vs_effective_downgraded=[]`（无降级）；`warnings=[]`；`windows={count:38, size:4, stride:2}`；`coverage_workflow=recorded`。
- **`readiness=blocked` 的唯一原因**：G017（insufficient）产生 1 条 blocking issue（"原文尚不足以支持这项目标，或存在相反证据"）。按硬性要求「insufficient 目标如实保留不得升级」，不修正、不重跑；其余 20 条为非 blocking 问题/待确认项。10 条 commands 的 stderr 均为空，harness 首次运行即 `ok=true`。

## 3. 未决问题清单

来自 `review_questions`（8 条）、`decisions.questions`（12 条）与 blocking issue：

1. G017 商家页面应标价：T058 提议后自我让步，混合冲突，judgment 保留 insufficient，待人工裁决（对应唯一 blocking issue）。
2. G008：采访者 T071 "anonymous posting" 是否应作为独立目标（仅泛泛确认，未升级）。
3. G010：社交/服装内容无意识影响的具体范围（涉众自述 "I don't know the other things"）。
4. G005：T010 "purchase address"/"showcasing this plot" 是否为转写误差。
5. G007：依据使用动机的 inferred 目标是否保留（"just out of convenience"）。
6. 整体：采访者 T061 "ranking system" 被 T062 否定，是否提取为目标（已回查，不提取）。
7. 整体：T034 "addictive and very time consuming" 是否隐含"避免沉迷/减少耗时"目标（抱怨不自动证明障碍，未提取）。
8. 整体：T014 "必须联系商家" 是否意味着希望改为直接下单（相反证据 "definitely good that way"，未提取）。
9–20. 关系与精化组判断的逐条问题（见第 6 节，均已写入 `kaos-decisions.json`）。

## 4. 实际执行情况

- **读了几遍原文**：完整通读 `source/DOC036.json` 77 轮 1 遍；对长轮按 160 字符折行逐字复读，并用脚本对全部 `quote` 做 `quote in text` 逐字符校验（结果：全部通过）。窗口清单由 `prepare_source.py --window-size 4 --window-stride 2` 实测为 38 个（W0001–W0038）。
- **是否补查**：做了全篇校正，`full_context_review.status=completed`。回查跨窗指代（T026 "it" 指私密账户安排、T024 "the other account" 指 T014 恶意账户、T062 纠正 T061 的 ranking system）、问答范围（采访者 T011/T019/T053/T071 总结与涉众 T054/T072/T074 泛泛确认）、条件继承（T012 加地点名、T052 情人节应对方式）、让步与例外（T058 标价后自我让步、T014 "definitely good that way"、T044 "not the same thing"）、被排除项与不确定项；登记 18 条 `source_checks`。校正**未新增候选**，故未另起 P2（`planned_passes=1`、`actual_passes=1`）。
- **修复次数**：harness **重跑 0 次**（首次即 `ok=true`）；生成期 3 处自检修正见 `repair-log.md`。
- **实际耗时（自报）**：单次隔离会话约 20–35 分钟（自报、未精确计时；含逐字复读与引文校验）。
- **停止原因**：完成全部 38 窗口逐窗捕获、全篇校正、目标整理，以及四类独立联系与 AND 精化组的逐条判断（含"已检查但无依据"记录）；无新增有据候选、无可解决的新证据，按 brief 停止该问题循环。

## 5. 没有做的事

- 独立语义审查 **not_run**（本文为生成方自检，另一调用亦不天然独立）。
- 形式证明 **not_run**。
- 人工接受 **pending**。
- 未联网、未读取参考答案/论文案例答案、未读取其他 attempt 目录、`datasets/`、`extra/output*`、`全过程记录.md` 或论文比较报告；未参考任何历史目标、关系或评分。

## 6. 关系建模与精化组判断：逐条执行记录（本轮重点，未留空、未跳过）

本阶段**真正执行完毕**：先判断四类独立联系，再单独判断 AND 精化组。结论逐条写入 `kaos-decisions.json` 的 `questions`（target_type=model、target_id=`DOC036-goal-model`，均为已有 ID），不是省略、也不是为凑数硬造关系。

### 6.1 四类独立联系（逐条）

| 类型 | 判断结论 | 依据/理由 |
|---|---|---|
| specialization | **已检查但无依据** | 逐窗核对全部目标对，未提取成对的"一般目标/具体情境目标"：G001/G005/G006 为并列不同购物用例；G007 为新地方情境但无对应一般父目标。不为凑层级造泛化根，故不建。 |
| operationalization | **已检查，建 R1、R3；其余无依据** | R1：G012（先交货再付款）→G011（避免被骗），T014 "I didn't lose my money, because ... you have to deliver before I pay you"；R3：G014（私密账户）→G015（避免被盯上），T026 "So it kind of helps to weed away ... people preying on your life"（"it" 经全篇回查指私密账户安排）。其余"方式→目的"候选（加地点名再搜、情人节保持登录、电话询价）均为同一目标内的操作步骤/现有流程，未形成独立目标端点，**无依据，不建**。 |
| contribution | **已检查，建 R2；其余无依据** | R2：G013（画廊互动判断账户）→G011，T062 "It just helps me to know which accounts ... I should buy from, and I should not buy from" 及 "And it saved me some money actually"、T024 "helped me to spot ... malicious account"；有帮助但未证明充分，按 contribution 而非精化。其余（搜索下拉复用、按地区返回供应商、社交内容促成购买）为现状能力/正面评价或观察，缺独立端点或仅同主题相关，**无依据，不建**。 |
| precedes | **已检查但无依据** | 回查 T010/T024/T058 流程顺序（搜索→看联系方式→联系→询价→付款→确认地址→等待→取货），"then/once" 均为涉众**现有操作流程的步骤顺序**，不是两个目标结果之间的先后声明；按规则不把操作先后当 precedes 联系，故不建。 |

成立关系 3 条（均有实际关系原句 `evidence_quotes`、两端目标为 `direct`、方向正确）：
`R1 operationalization G012→G011 supported`、`R2 contribution G013→G011 supported`、`R3 operationalization G014→G015 supported`。无自环、无重复同类型同方向记录。

### 6.2 AND 精化组（单独判断，逐条）

| 候选组 | 判断结论 | 理由 |
|---|---|---|
| G011 ← {G012, G013} | **已检查但无依据** | 两者是避免被骗的两种方式/帮助，原文未声称二者共同满足足以避免损失（仍有其他诈骗手法与其他判断方式），不能声称"共同满足足以实现父目标"；不建 supported+complete 组，不为凑边扩写目标。 |
| G015 ← {G014} 或其他组合 | **已检查但无依据** | 单子目标不构成 AND 组，且原文无共同充分性声明；G008/G009/G010 等为独立愿望/维持目标，彼此无父子充分关系。 |
| 购物流程组（{G002, G003, ...} → G001 等） | **已检查但无依据** | 它们是不同用例/独立结果，不是共同满足某父目标的充分条件；且原文无充分性声明。 |
| supported+complete 场景要求 | **已检查但无依据** | 需至少一条 normal 与一条 exception 场景、全部 `outcome=supports`、所有端点支持有效、所有依赖联系 supported；原文仅提供单次事件（T014 一次恶意账户经历、T062 省过一次钱），不足以证明任一组共同充分性。 |

**结论**：`groups=[]`、0 成立组、0 幅成立精化 DAG 边。这是"判断执行完毕后的结果"，不是跳过判断；普通联系（3 条 supported）单独展示，不转换成成立精化箭头；无记录也不表示已排除其他影响。

## 7. 交付路径（本 attempt 目录内）

- `spec.json`（编制输入）、`kaos-decisions.json`（含 3 关系 + 12 条逐条判断记录）
- `delivery/`：`goal-model.html`、`goal-model.json`、`goal-model.md`、`goal-model.svg`、`goal-relations.svg`、`manifest.json`、`attachments/`（extraction.json、judgments.json、kaos-decisions.json、inspection.json、source.txt）
- 工程记录：`attempt-summary.json`、`coverage-check.json`、`inspection.json`、`extraction-ledger.json`、`tracing/tracing.json`、`work/source-windows.json`
- 自检记录：`repair-log.md`、`self-review.md`
