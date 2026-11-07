# 生成方自检（DOC004 / run02 / attempt-02）

> **这是生成方自检，不是独立语义评审。** 工程检查（覆盖、定位、结构、版本绑定）由冻结工具执行；语义判断与建模决策由本生成会话编制并自行复核，未经第三方审核或人工接受。

## 1. 生成方自检

- **候选是否被压薄**：未压薄。按 4/步2 的 33 个窗口逐窗捕获，原始候选保留为 21 条复合表达（含习惯性用途、定义、评价、信念、抱怨、让步、缺口观察、采访者任务），未先压缩成"十几条主要需求"。`ledger.passes[0].window_results` 覆盖全部 `DOC004:W0001`–`W0033`，均标 `processed`。
- **复合目标是否拆分**：C001（T005 一句含 Zelle 分摊、转储蓄赚利息、Apple Pay 付款三个独立意图）以 `split` 拆为 G001/G002/G003；其余按"一目标一核心动作"整理，最终 9 条目标。操作步骤、前提、同一对象的多个限定未机械拆。
- **条件/否定/强度是否丢失**：逐项保留并在 `context`/`rationale` 标注。例如 G002 的"支票账户资金较多"条件与 `normally` 强度、G005 的"资金在储蓄账户故限额当前不触发"例外与未来使用意图、G007 的偏好强度与"a few limitations"让步、G008 的"不常用/理解"让步、G009 的已实现能力张力，`sell/cell`→Zelle 的 ASR 指代校正。采访者任务数值（T028 每笔 100 美元、T040 的 $1）未写成受访者固定业务目标。
- **精化组是否有反例未解决**：未建立任何精化组（`groups=[]`），因此不存在被掩盖的反例。已识别的相反证据（T023 现有按交易类型分类、无 groceries/fuel 消费类别指示）作为 G004 的缺口证据保留在 `source_checks` 与其 `unsupported_parts`。
- **是否为凑层级造根**：否。`relations=[]`、`groups=[]`，没有成立组；未造根目标、未为凑边/凑组扩写目标。G004 如实保留为 `insufficient`，未升级为 direct/inferred。

## 2. 工程检查实际结果（复制自 attempt-summary.json）

**coverage_check**
```json
{"exit_code": 0, "structure": "passed", "workflow": "recorded", "pending": [],
 "counts": {"source_segments": 67, "windows": 33, "raw_candidates": 21, "final_goals": 9,
            "source_checks": 10, "actual_passes": 1,
            "dispositions": {"split": 1, "exclude": 9, "keep": 6, "merge": 5}}}
```

**inspection**
```json
{"structure": "passed", "readiness": "blocked", "independent_semantic": "not_run",
 "formal_proof": "not_run", "human": "pending"}
```
> `readiness=blocked` 仅由 1 条 blocking issue 引起：G004 被如实保留为 insufficient，工具据此自动登记"原文尚不足以支持这项目标，或存在相反证据"。这是保留而非失败；结构检查 `passed`。

**counts**
```json
{"goals": 9, "relations": 0, "groups": 0, "established_groups": 0, "raw_candidates": 21,
 "support_labels": {"insufficient": 1, "inferred": 2, "direct": 6, "contradicted": 0},
 "issues": 9, "blocking_issues": 1}
```

其他：`tracing_status=completed`，`declared_vs_effective_downgraded=[]`，`warnings=[]`，10 条命令 `exit_code` 全为 0。全部 50 条 quote 经本地脚本校验为对应 `source_id` 文本的精确子串且无歧义命中。

## 3. 未决问题清单

**blocking issue（1）**
- `goal / G004`：`原文尚不足以支持这项目标，或存在相反证据。`（由 insufficient 支持标签自动登记；不升级、不隐藏）

**review_questions（4）**
- `G004`：按消费类别的花费分解是否为受访者本人目标，还是对采访者措辞的附和？（"data analysis / expense categories"来自 T020，受访者自述不确定现有跟踪能力）
- `G007`：聊天/文字支持是否应升格为强要求？（原文仅偏好强度，并含可行性限制让步）
- `G009`：对已实现 dashboard 的正面评价是否构成独立维持型目标？（已实现能力不自动成为要求 vs 维持/避免型意图应保留）
- `DOC004-goal-model`（model 级）：是否遗漏其他达到/维持/避免类意图？

**decisions.questions（4）**
- `G004`：按消费类别的数据分析/有价值洞察措辞来自采访者，需确认是否为本人需求；自述不确定系统是否按消费类别跟踪。
- `G007`：网站聊天支持由偏好与建议强度推断，需确认作为正式要求还是仅保留为偏好。
- `G009`：由对现有 dashboard 的正面评价推断的维持/避免型意图是否应保留为独立目标。
- `DOC004-goal-model`（model 级）：本次未建立任何独立联系或 AND 精化组，需复核是否存在被遗漏、两端均有依据的 contribution/operationalization 联系或可声称共同满足的精化组。

## 4. 实际执行情况

- **读原文**：完整读取 1 遍（Read 工具 + 脚本补读被截断的 T043）；逐窗处理 33 个窗口；全篇校正回看全部 67 轮。
- **是否补查**：是。补查 T043 完整文本；全篇校正覆盖指代（`sell/cell`→Zelle）、问答范围、T025（移动 app）与 T035/T037（网站）的范围差异、条件继承、让步、例外、相反证据（T023）。`full_context_review.status=completed`。
- **修复次数**：0 次 harness 修复轮次。harness 首次运行即成功（无 downgraded、无 warning、无 stderr），故未生成 `repair-log.md`。注：生成 `spec.json` 之前的本地自检曾修正 2 处引文错误（`q38` 的 `Doc004`→`DOC004` 拼写、`q44` 的 `1 to 1`→`1 to one`），属生成前校验，不计入 harness 重跑。
- **实际耗时（自报）**：harness 10 条命令合计约 5.4 秒（`seconds` 求和）；语义编制、逐窗捕获与全篇校正合计约数十分钟（自报，未计时工具）。
- **停止原因**：逐窗捕获、全篇校正、一目标一核心动作整理均已完成；不存在可声称"共同满足足以实现父目标"的 AND 精化组，亦不存在两端目标支持有效且有实际关系原句的独立联系，故 `relations`/`groups` 置空；G004 如实保留 insufficient。达到停止条件。

## 5. 没有做的事

- 独立语义审查：`not_run`
- 形式证明：`not_run`
- 人工接受：`pending`

> 覆盖记录与语义判断为生成方编制与自检，仅验证所提交记录的绑定、位置、处置与声明范围；不证明候选语义正确或原文意图穷尽，也不代替人工确认。
