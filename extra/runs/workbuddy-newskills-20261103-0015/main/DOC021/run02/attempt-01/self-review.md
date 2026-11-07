# 自检记录（DOC021 / run02 / attempt-01）

> **这是生成方自检，不是独立语义评审。** 同一会话内由生成者回看，不能替代他人复核；独立语义审查、形式证明、人工接受均未运行。

## 1. 生成方自检（内容层面）

- **候选是否被压薄**：按 4 轮/步长 2 的 38 个窗口逐窗捕获 63 条原始候选，未先压成“主要需求”；同一愿望在后续轮次重复出现时保留为新候选并 `merge`（如 C054/C055/C056 → G012），不新造节点。
- **复合是否拆开**：T009 的“按面积/卧室数+预算搜索”与“次要条件再筛选”拆为 G007/G008；T019–T023 的“长表单”“必填字段”“想简短沟通”合为 G014（同一核心动作：低信息量联系）；T025 的“列规格+加入清单”与“预计回复/下一步”拆为 G016/G013；T027 的“确认后分享信息”独立为 G015。
- **条件/否定/强度**：保留 `usually`（G006）、`maybe` 建议（G026）、条件句（G027 “only if clear and fast”）、避免型（G011 站外沟通、G021 未知按钮）、维持型（G023 筛选可选）；未把偏好升级为强制，未编造阈值。
- **精化组反例**：GR1（G027 ← G013+G014）保留 `proposed/partial`，异常场景“房东不活跃、不在平台回复”（T017）记为 `counterexample`，未强行写成成立。G004/G005/G006 被原文称为 “many ways”，判为 OR 替代，未建 AND 组；G001 下的 G002/G007/G008 组合因缺联系与核验环节判为不充分。三条判断均写入 `kaos-decisions.json` 的 model 级 questions，不是沉默跳过。
- **是否为凑层级造根**：G001 来自 T003 明说“搬家需要找新住处”，不是抽象摘要；无其它人造根，未设固定层数。
- **已知薄弱处**：G011 的“维持站外沟通”依据是习惯陈述＋“never trusted much”，若视为纯过去行为应降为 insufficient（已写入 rationale 与 review_questions）；G026 只是 “maybe” 建议；G027 的“清晰且快速”无标准。

## 2. 工程检查实际结果

复制 `attempt-summary.json`：

- `coverage_check`：exit_code 0，structure `passed`，workflow `recorded`，pending `[]`；
  counts：source_segments 77、windows 38、raw_candidates 63、final_goals 27、source_checks 12、actual_passes 2；dispositions: keep 27 / merge 30 / exclude 6。
- `inspection`：structure `passed`，readiness `reviewable`，independent_semantic `not_run`，formal_proof `not_run`，human `pending`。
- `counts`：goals 27，relations 9，groups 1，established_groups 0，raw_candidates 63，support_labels direct 27 / inferred 0 / insufficient 0 / contradicted 0，issues 8，blocking_issues 0。
- `declared_vs_effective_downgraded`：`[]`；`warnings`：`[]`（无 ambiguous 引文）。
- 交付：`delivery/` 下 goal-model.html/json/md、goal-model.svg、goal-relations.svg、manifest.json 与 attachments（extraction/judgments/source/kaos-decisions/inspection）。

## 3. 未决问题

来自 `review_questions`：

1. G011：维持站外沟通是否算稳定偏好（仅由现状＋不信任推断）。
2. G026：照片格式规则只是 maybe 建议，是否作为对平台的要求保留。
3. G027：“流程清晰且快速”缺可核对标准，是否需补充定义。

来自 `decisions.questions`（model 级，均指向 DOC021-goal-model）：

4. G004/G005/G006 属 OR 替代，未建 AND 组，是否需要以多方案表达。
5. G002/G007/G008 对 G001 不构成共同充分，未建组。
6. GR1 的异常场景（房东不活跃）未解决，需确认是否接受 partial。
7. G011 与 G027 条件不同不判冲突；流程改善后是否放弃站外渠道未知。

Blocking issue：无（0）。

## 4. 实际执行情况

- 读原文：2 遍（先完整通读 77 轮并按窗口通读 38 窗，再做全篇校正）；无追加定向补查。
- 补查：无新候选；全篇校正处理了指代（“the other ways”）、条件继承（“before that step”）、例外（未标注属性房源）、相反证据（T017 站外沟通 vs T071 条件性站内单平台）。
- 修复：harness 运行 4 次，前 3 次失败（work 目录非空、inference 引用指向原始候选、judgments.json 残留），详见 `repair-log.md`；成功 1 次。
- 耗时（自报）：约 45 分钟（含阅读、编写与修复）。
- 停止原因：完成一次逐窗捕获与一次全篇校正，补查未再有据新增意图，保留未决问题后停止。

## 5. 未做的事

- 独立语义审查：not_run。
- 形式化证明：not_run。
- 人工接受：pending（模型 `review.status=pending`）。
- 未读取仓库其他目录、未联网查答案、未参考任何历史目标/关系/评分。
