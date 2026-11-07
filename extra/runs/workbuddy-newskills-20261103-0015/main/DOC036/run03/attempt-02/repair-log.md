# 修复与重跑记录（DOC036 / run03 / attempt-02）

## 结论

**harness 重跑次数：0。首次运行即 `ok=true`，无报错、无 `downgraded`（`declared_vs_effective_downgraded=[]`）、`warnings=[]`。**

因此未触发 brief 第 7 节的"跨 attempt 修复重跑"，也未产生新的 attempt 目录。本文件记录实际发生的全部修正，区分「生成期自检修正」与「harness 运行」。

## 触发原因

- harness 首次运行输出：`ok=true`，`coverage_workflow=recorded`，`readiness=blocked`，`blocking_issues=1`。
- 唯一的 blocking issue 来自 **G017**（label=insufficient，工具提示"原文尚不足以支持这项目标，或存在相反证据"）。G017 对应 T058 涉众先提议"商家页面应标价"、随即自我让步（标价会减少询价、商家失去定价反馈）的混合冲突。按本轮硬性要求「insufficient 目标如实保留不得升级」，**不修正、不升级、不重跑**；`readiness=blocked` 是该如实保留的预期结果，并非命令失败（10 条 commands 的 stderr 均为空）。
- 其余 20 条 issues 均为非 blocking 的待确认/问题记录。

## 生成期自检修正（均发生在首次运行 harness 之前，不计入 harness 重跑）

| # | 触发原因 | 改了哪些对象 | 理由 |
|---|---|---|---|
| 1 | `_gen_spec.py` 语法错误：ENTRIES 字典用 `]` 闭合 | `_gen_spec.py` 第 459 行 `]` → `}` | 生成脚本需为合法 Python 才能产出 spec.json |
| 2 | 自检断言 `目标缺来路: G010`；且 7 处 `source_checks` 的 `candidate_ids` 含被 exclude 的候选却带 `final_goal_ids` | `C042` 由 `merge→G009` 改为 `split→[G009,G010]`（该复合候选含"远离/只在需要时用"与"避免无意识影响"两个独立结果）；S1/S2/S4/S5/S6/S7/S9 的 `candidate_ids` 收紧为仅映射到所列 `final_goal_ids` 的候选 | 保证每个最终目标有原始候选来路、`source_checks` 与 `entries` 映射一致、复合目标按"一目标一核心动作"拆分 |
| 3 | 引文逐字校验报 `C060` 不匹配 T059 | `C060` 引文 `It sounds like you travel around a lot.` → `So it sounds like you travel around a lot.`（原文为小写 it、带 So 前缀） | 硬性要求 quote 逐字符匹配原文 |

修正后重跑 `_gen_spec.py`：`引文逐字校验: 全部通过`，并写出 `spec.json`。

## 校验口径

- 所有 `raw_candidates` / `goals` / `source_checks` / `relations` 的 `quote` 均用 `quote in source[DOC036.json][source_id].text` 校验通过。
- 结构自检：`raw_candidate_id` / `goal_id` 唯一；每个候选恰好一条 `entries`；每个最终目标有来路；`direct`/`inferred` 的 `unsupported_parts` 为空；`decisions.questions` 的 `target_id` 均为已有 ID（model 级用 `DOC036-goal-model`）；`passes[].window_results` 覆盖全部 38 窗口。

## 未改动项

- 未改 `attempt-01/`（本会话为隔离续跑，不读取、不改动上级其他 attempt）。
- 未删除或降级任何有依据目标；未删除证据；未手改检查报告绕过规则。
