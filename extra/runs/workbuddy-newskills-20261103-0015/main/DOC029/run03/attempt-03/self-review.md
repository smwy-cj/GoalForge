# self-review — DOC029 run03（生成方自检）

> **这是生成方自检，不是独立语义评审。** 提取、判断、建模与本次自检均由同一隔离会话完成，不构成独立复核、形式证明或人工采纳。

## 1. 生成方自检

- **候选是否被压薄**：36 条原始候选逐窗捕获，含复合表达（如 T029 的提醒+优先+省钱）。10 条排除项均有具体理由（界面描述、内容库背景、个人对 games 的使用意向、无对象的小 bug），未按“次要”批量丢弃；T041 的相反证据单列。
- **复合目标拆分**：T033 拆为 G007（片段轮播试看）与 G008（播放入口进正片），二者可独立满足；T029 拆出动作 G006，把“优先观看/避免另买订阅”并入其结果与目的，未虚增节点。G003 合并了“续播 + 进度/时间戳”，因属同一续播结果。
- **条件/否定/强度**：保留“用餐时”（G002）、“My List + 下架前约一个月”（G006）、“决定观看后”（G008）、“约 2-3 分钟、悬停播放、多类型”（G007）、“can probably / if I may”（G006、G008 的建议强度在 rationale 说明）。未把偏好升级为必须，未把现状自动写成要求（搜索栏、筛选、账号操作均排除）。
- **精化组反例**：GR1（G004+G005 满足 G001）保留 proposed/partial；异常场景（按场合/模糊情绪选片，如母亲节）判为 counterexample 且未解决，因此不进入成立图。**成立组为 0，属预期结果，没有为凑层级造根。**
- **为凑层级造根**：未新增泛化根目标；G009（留存）有 T037/T039 原句支撑，G010（一致性维持）标为 inferred 并写明假设。
- **已知薄弱点**：G010 依赖推断；G002 的“点击起点”边界未定；G006 未承接“该片在哪个平台”的痛点。均进入问题清单。

## 2. 工程检查实际结果（attempt-03）

```json
coverage_check: {"exit_code": 0, "structure": "passed", "workflow": "recorded", "pending": [],
  "counts": {"source_segments": 56, "windows": 27, "raw_candidates": 36, "final_goals": 10,
             "source_checks": 12, "actual_passes": 1,
             "dispositions": {"keep": 10, "merge": 16, "exclude": 10}}}
inspection: {"structure": "passed", "readiness": "reviewable",
             "independent_semantic": "not_run", "formal_proof": "not_run", "human": "pending"}
counts: {"goals": 10, "relations": 3, "groups": 1, "established_groups": 0,
         "raw_candidates": 36, "support_labels": {"direct": 9, "inferred": 1,
         "insufficient": 0, "contradicted": 0}, "issues": 6, "blocking_issues": 0}
declared_vs_effective_downgraded: []
warnings: []
```

## 3. 未决问题

1. G006：下架前提醒是否要同时告知该片之后在哪个平台可看？原文只说“找不到在哪个平台”。
2. G002：少点击的起点是否包含登录与选择 profile？原文以点开影片到播放为语境。
3. G007：预览片段是正片片段、预告还是“personalized review”？原文以 maybe 收尾。
4. GR1：类型轮播 + 相似推荐是否算个性化呈现的主要方式？场合型个性化不在覆盖内。
5. model：games 仅被描述为既有功能且受访者自述不用，模型未纳入游戏目标。
6. blocking issue：0 条。

## 4. 实际执行情况

- 全文通读 1 遍（56 轮），再按 27 个窗口（4/步 2）逐窗复核，未做第二遍独立重读。
- 跨窗回查：T025→T029→T031 的痛点—建议—确认链；T033→T035→T037 的功能—形态—留存链；T041 相反证据；T043 母亲节实例；T047 games 与一致性。
- 修复次数：2 次（attempt-02 修 S2 重复 ID；attempt-03 修 S4 重复 ID），均为覆盖记录的机械映射问题，未改语义内容。attempt-01/02 的失败产物原样保留。
- 停止原因：coverage passed/recorded、无降级、无 blocking，预算内完成；实际耗时未计量（unknown）。

## 5. 没有做的事

- 独立语义审查：not_run。
- 形式证明（精化充分性/完整性证明）：not_run。
- 人工接受：pending（模型 review 始终 pending）。
- 未核对音频、未做 OCR（原文为既有转写稿）。
