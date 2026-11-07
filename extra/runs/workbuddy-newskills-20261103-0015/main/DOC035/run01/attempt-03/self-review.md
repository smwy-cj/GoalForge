# self-review（DOC035 / run01 / attempt-03）

> **声明：本节是生成方自检（同一会话、同一模型），不是独立语义评审，也不构成人工采纳。**

## 1. 生成方自检

| 检查点 | 结论与说明 |
|---|---|
| 候选是否被压薄 | 未先做摘要式压缩。按 4 轮/步长 2 的 24 个窗口逐窗捕获，得 33 条原始候选（含 T001 查看频率、T003 浏览流程、T003 只看标题等现状句），逐条给了 keep/merge/exclude 去向；排除只针对现状描述，不针对意图。 |
| 复合候选是否按语义拆分 | C010+C013 合为 G006（短而全面，二者是同一动作的两个限定，非独立结果）；C026+C027 合为 G013（关闭话题 + 其突发新闻例外，拆开会丢失例外关系）；C019+C032 合为 G011（同一结果“不被推送议程”，两条通道写入 context）；C007 与 C008 分为 G003/G004（显示来源 vs 跨来源比较是可独立满足的两个结果）。 |
| 条件、否定、强度是否丢失 | G013 保留“突发新闻仍要展示、但不展示深度分析”、G016 保留“不存**全部**数据”“仅用于推荐”、G006 保留“仅部分文章”“仍须覆盖每个方面”、G002 保留原话 “a couple of days”（未编阈值）、G012 保留“当天全部 / 当天结束前 / at least”、G008 保留 “can be / would be great” 的可选强度、G017 保留 “not a lot, but ... all the relevant”。 |
| 是否把偏好/现状/担忧升级为强制 | G003、G004、G001 依据的是对既有能力的肯定，按维持/偏好保留，未写成 must；G015 明确记为“选择平台的因素”而非硬性要求；G011 把 T029 的 concern 与 T047 的 should not 合并，question 中指出两者强度差异。 |
| 精化组是否有未解决反例 | 只有 1 个候选组 GR1（父 G017，子 G001/G006），我判定其**不成立**为 supported+complete：normal 场景 supports，exception 场景（无历史行为的新用户、只有长文可压缩的事件）为 unknown，故保留 `proposed` + `partial`，成立组数为 0。 |
| 是否有为凑层级造根 | 没有。原文没有总体目的句，未造根；G017 是从“如何衡量聚合功能成功”直接得到的成功标准，不是摘要式上层。多根结构保留。 |
| 是否造了无依据的连边 | 只保留 4 条：R1/R2（个性化推荐、短而全面 → 聚合成功标准，contribution）、R3（突发新闻当天到达 → 一般时效，specialization）、R4（通知不刷屏 → 突发新闻不被淹没，contribution）。曾考虑“显示来源 → 跨来源比较”一条，因原文没有该连接句而放弃。 |
| 引文一致性 | 33 条候选、17 个目标、4 条联系、1 个组的全部 quote 均由脚本逐条校验：在对应 `source_id` 的 text 中**恰好命中 1 次**（count==1），大小写与原文一致（曾修正 T021 “They”、T035 “It” 两处大小写）。 |

## 2. 工程检查实际结果（复制 attempt-summary.json）

```json
"coverage_check": {
  "exit_code": 0,
  "structure": "passed",
  "workflow": "recorded",
  "pending": [],
  "counts": {
    "source_segments": 50, "windows": 24, "raw_candidates": 33,
    "final_goals": 17, "source_checks": 10, "actual_passes": 2,
    "dispositions": {"exclude": 3, "merge": 15, "keep": 15}
  }
},
"tracing_status": "completed",
"declared_vs_effective_downgraded": [],
"inspection": {
  "structure": "passed", "readiness": "reviewable",
  "independent_semantic": "not_run", "formal_proof": "not_run", "human": "pending"
},
"counts": {
  "goals": 17, "relations": 4, "groups": 1, "established_groups": 0,
  "raw_candidates": 33,
  "support_labels": {"direct": 17, "inferred": 0, "contradicted": 0, "insufficient": 0},
  "issues": 11, "blocking_issues": 0
}
```

- 有效支持分布：17 个目标全部 direct（无 inferred/insufficient/contradicted），`downgraded=[]`。
- 检查状态：结构 passed、readiness=reviewable、blocking_issues=0、warnings=[]。
- 11 条 issue 全部是待确认问题（6 条提取层 + 4 条判断层 + 1 条“GR1 尚未成立”），没有阻塞项。

## 3. 未决问题清单

**提取层（review_questions）**

1. G002：`within a couple of days` 是否需明确阈值（48/72 小时）？原文无数值，未编造。
2. G016：“不应存储我看过的全部数据”的边界（可留哪些字段、留多久）？
3. G017：`all the relevant information ... in a short amount of time` 如何验收？
4. G011：T029 的“严重担忧”是否应作为产品约束，而非只是顾虑记录？
5. G013：被关闭话题的 “breaking news” 与 G012 的当天突发新闻是否同一口径？
6. G005：通知量的“不过度”是否有可核对上限（条数/频次）？

**判断层（decisions.questions）**

7. GR1：是否需要补“聚合需覆盖多来源/多话题”的目标，才能主张共同充分性？
8. G017：是否需要一根“高效获取个性化新闻”的根目标统领 G001/G006/G017？（当前未造根）
9. G011：避免推送议程 与 G001 个性化推荐（需知道兴趣）存在张力，原文未给取舍规则。
10. R1：G001 只是 G017 相关性部分的手段，若后续补入覆盖性目标，是否应改为 operationalization？
11. GR1：整组层级仍待确认，未作为成立精化展示。

## 4. 实际执行情况

- 原文通读 2 遍：P1 逐窗（24 窗、50 轮全部处理）捕获 33 条候选；P2 全篇校正（指代、问答范围、条件继承、让步、例外、相反证据），未新增候选，故 pass_id 只出现 P1。
- 补查：针对 T039（Google 通知不刷屏）与 T013（其他应用刷屏）做了相反证据核对，按不同产品分别记录，不判为矛盾。
- 修复次数：2 次（attempt-02 修 C010 处置标签；attempt-03 修 model 型 issue 目标）。首次 attempt-01 的 harness 输出因进程中断未完整捕获，其覆盖检查失败原因已由 coverage-check.json 记录。
- 实际耗时：自报约 25 分钟（含 3 次 harness 运行）。
- 停止原因：预算内完成，无 `downgraded`；剩余不确定项按上述问题保留，不以新假设强行闭合。

## 5. 我没有做的事

- 独立语义审查：**not_run**（本文件是生成方自检，同一会话、同一模型，不具独立性）。
- 形式证明：**not_run**（结构无环与引用有效不等于精化充分性成立）。
- 人工接受：**pending**（模型 `review` 状态保持待审，未代表用户采纳任何目标或组）。
- 没有读取 development_reference、baselines、benchmarks、extra/output*、其他任务、全过程记录或比较报告；未联网检索论文或参考答案。
