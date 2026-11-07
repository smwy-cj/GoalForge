# 自检记录（DOC024 / run01 / attempt-01）

> **性质声明：本文件是生成方自检，不是独立语义评审。** 同一会话内的复核不构成第三方审查，也不能替代人工接受。

## 1. 生成方自检

- **候选是否被压薄**：未压缩。按 4 轮窗口/步长 2 逐窗捕获，30 条原始候选覆盖全部 17 个窗口（每个窗口至少一条候选），未设数量上限；14 条最终目标各有原始候选来路，`keep 14 / merge 9 / exclude 7`。
- **复合候选是否拆分**：T007 一句同时含"解释术语"与"项目创意"，在捕获阶段即分为 C004/C005，避免把两个结果压成一条。反向检查（是否机械拆分）：C017/C018（组织措辞、附附件）同为使问题被理解的手段，按同一结果合并；C026/C031（慢/卡住 → 重生成 → 耗额度与时间）是同一痛点链条，合并为一个避免目标；C010（生成图 + 按需求细化）因结果是"符合要求的图"这一单一结果保留为一个目标，频率限制另写。
- **条件、否定、强度是否丢失**：
  - 保留强度梯度：G006 用 "Prefer not to"（原文 "don't really like"），未写成禁止；G003 保留 "often" 的概率语气；G008 保留 "sometimes" 的可选性。
  - 保留否定与自我纠正：G012 保留 "not without limit"（原文当场纠正 "unlimited"）。
  - 保留条件：G001 的"无 office hours / 随时可问"、G003 的"项目开始前"、G007 的"不常使用"、G011 的"需要逻辑推理的问题"。
  - 未编造任何时间、次数、准确率阈值。
- **精化组是否有未解决反例**：GR1（父 G010，子 G004/G005/G011）保留 `proposed + partial`。异常场景（高层概念问题无文献条目、无复算基准，o1 仍可能错，见 T013）为明确反例，故不进入成立精化；成立组 0 个，属正常结果，未为凑层级造根。
- **是否有为凑层级造根**：无。G010 不是概括性摘要，而是原文反复以 "very important / pay attention to the logic / more accurate" 表达的质量要求，并作为 R1–R4 的实际目的端点；未新建任何仅用于连边的泛化根目标。
- **关系判断是否真正执行**：逐对检查了同场景目标（见第 3 节"已检查但无依据"清单），只保留 5 条有实际关系原句支撑的联系；未把相关、相似、操作先后当作联系。
- **insufficient 是否被升级**：G014 保持 `insufficient`，blocking issue 如实保留（inspection readiness=blocked 由该目标引起）。

## 2. 工程检查实际结果

`coverage_check`：

```json
{"exit_code": 0, "structure": "passed", "workflow": "recorded", "pending": [],
 "counts": {"source_segments": 36, "windows": 17, "raw_candidates": 30, "final_goals": 14,
            "source_checks": 16, "actual_passes": 1,
            "dispositions": {"exclude": 7, "keep": 14, "merge": 9}}}
```

`inspection`：

```json
{"structure": "passed", "readiness": "blocked",
 "independent_semantic": "not_run", "formal_proof": "not_run", "human": "pending"}
```

`counts`：

```json
{"goals": 14, "relations": 5, "groups": 1, "established_groups": 0,
 "raw_candidates": 30,
 "support_labels": {"contradicted": 0, "direct": 12, "inferred": 1, "insufficient": 1},
 "issues": 9, "blocking_issues": 1}
```

`declared_vs_effective_downgraded`: `[]`；`warnings`: `[]`；`tracing_status`: `completed`。

## 3. 未决问题清单

1. **G014（blocking）**：宕机相关目标只有第三人称描述（他人依赖 ChatGPT 按时提交工作而慌乱），无本人意图，保留 `insufficient`；`readiness=blocked` 由该项引起，其余对象可正常审阅。
2. **G006**：`don't really like to use` 是软偏好还是回避要求？当前按偏好保留，未升级为禁止。
3. **G007**：图片生成被明确说成不常使用（T033），是否仍作独立目标，还是仅作偶发场景？
4. **GR1**：G004/G005/G011 无法覆盖高层概念类问题，缺少非术语/非计算类答案的核对依据；异常场景为反例，保留待确认。

**已检查但未建立联系/精化组的对象（逐条理由，与 `kaos-decisions.json` 的 model 级 questions 一致）**：

- G001 ↔ G009：历史回看用于复习已学内容，不帮助"取得解释"本身，无有向联系依据。
- G007 ↔ G002/G003：产品可视化是独立任务，原文未说它支持项目构思。
- G006 ↔ G010；G008 ↔ G001/G003：原文给出的是偏好理由与"帮助理解问题"的说明，被帮助的结果未被表达为目标，不构成四类联系之一。
- G013/G014 ↔ 其余目标：仅痛点陈述，未见受影响目标，不建贡献或先后联系。
- 精化组：G003 作为 G002 的子目标只有单成员，不构成 AND 组；G001/G002/G007/G009 之间无"整组共同满足父目标"的依据；G011+G012 只提高模型能力与追问次数，不能覆盖全部答案类型。故仅 GR1 为待确认组，成立组 0。

## 4. 实际执行情况

- 原文通读 1 次（36 轮全量），其后引文逐字校验 1 次、全篇语义回查 1 次（指代、条件继承、让步、例外与相反证据）；未另开补查 pass。
- 17 个窗口全部 `processed`，无 `skipped`。
- harness 首次运行即成功：**修复/重跑次数 0**，未出现 `downgraded`。因无失败，未生成 `repair-log.md`。
- 耗时：未精确计时（自报为单次会话内完成，约 20 分钟量级）。
- 停止原因：完成一次覆盖全篇的基础提取与全篇校正；补查无新增有据意图，剩余不确定项已保留为问题。

## 5. 没有做的事

- 独立语义审查：**not_run**（本文件只是生成方自检）。
- 形式证明：**not_run**（结构检查通过不证明精化充分性或语义正确）。
- 人工接受：**pending**（未从任何分项意见推断认可）。
