# self-review（生成方自检）

> **这是生成方自检，不是独立语义评审。** 编制与判断由同一隔离会话完成，未执行独立语义审查、形式化证明，也未取得人工采纳。

## 1. 生成方自检

### 1.1 候选是否被压薄

- 逐窗（4 轮窗口 / 步长 2，共 38 窗）捕获原始候选 51 条，未先压成“主要需求”。其中 23 条 keep、19 条 merge、6 条 split、3 条 exclude。
- 允许复合表达保留在原始候选：如 C014（无更新时间 + 表单不知去向 + 无法简短沟通）、C022（注册 + 未知按钮 + 跳过站点）、C009（联系 + 回复速度影响取舍），在整理阶段才拆分。
- 窗口本身不作语义裁决：T019/T021 的抱怨与 T071/T073 的重申跨窗合并到同一目标（G014/G015/G028）；T033 的“喜欢/不喜欢”三分（地图画圈、评论、额外步骤）分入 G007/G017/G021/G022。

### 1.2 复合目标是否拆分

拆分判据是“可独立满足且有独立语句依据”，不按动词数：

- C009 → G010（联系房东）+ G011（用回复速度/完整度收窄）。
- C014 → G014（看最后更新时间）+ G015（看提交后会发生什么）+ G016（简短直接沟通）。
- C019 → G010 + G012（站内表单 / 地图找联系方式两条路径）。
- C022 → G021（不强制注册）+ G022（避免冗长不明流程）。
- C050 → G015 + G028（看清流程 / 把沟通留在站内）。
- 未拆的情形：C033 的价格区间/床位浴位/房屋类型/搬家日期/宠物/水电是同一“筛选”动作的多个限定，合并为 G008，未拆成六个目标；C007 与之合并。

### 1.3 条件、否定、强度是否丢失

- 条件：G012 保留“未回复时”触发；G028 保留“流程清楚快速”；G020 保留“双方确认之后”；G019 把必填字段清单写进 context；G021 保留“注册可留作可选”。
- 否定/避免：G022 是避免型目标（不喜欢冗长不明流程、会跳过该类网站）；G019 是否定式要求（不填全部必填项）。
- 强度：G005/G002 保留 usually；G011 保留 might；G018 保留 maybe（弱建议）；G026 保留 maybe / would love；G029 保留 sometimes（非硬截止）；G009 保留“次要条件”的较低优先级；G025 是对现状可选项的维持意图，未升级为新增要求。
- 未做的跨越：未把“现有详情已足够”（T065/T067/T069）当成新增要求；未把“不信任站内沟通”的信念当事实；“房东不回复说明管理不善”只作判断标准排除，未升级为已证障碍。

### 1.4 精化组：是否有反例未解决

只有 1 个候选组，且**没有成立组**（`established_groups = 0`）：GR1（G001 ← G002/G006/G008/G009/G010）记为 `proposed + partial`。正常场景（按原文顺序完成并获回应）判 supports，异常场景（子目标全达成但房东始终不回复 / 价格租期谈不成）判 counterexample，故完整性只能 partial，未进入成立 DAG。反例来源有原文支撑（T013/T019：站内常无人回应），不是纯假设。

### 1.5 是否为了凑层级造根

没有新增根目标。G001 是原文 T003 明说的“需要找新住所”，不是为画树抽象出来的；没有任何“主题概述”型节点。所有 29 个目标都能追到原始候选（`goals without provenance = 0`）。

## 2. 关系与精化组判断的实际执行记录（含“已检查但无依据”）

### 2.1 已成立/已记录的联系（12 条，全部 supported）

| ID | 方向 | 类型 | 依据要点 |
|---|---|---|---|
| R1 | G002 → G006 | precedes | T005 “choose … and then I start searching by such keywords” |
| R2 | G003 → G002 | operationalization | T007 “One of the ways” |
| R3 | G004 → G002 | operationalization | T007 “the other ways … asking people” |
| R4 | G005 → G002 | operationalization | T007 “if I have a specific job … I will usually pick” |
| R5 | G007 → G002 | operationalization | T033 “more flexibility on selecting the area” |
| R6 | G008 → G009 | precedes | T009 “after that … filtering it down” |
| R7 | G009 → G010 | precedes | T011 “after filtering it down … communication process” |
| R8 | G012 → G013 | specialization | T013 改用邮箱/电话 + T017 沟通在站外 |
| R9 | G021 → G022 | specialization | T033 把“要求注册”列为额外步骤的实例 |
| R10 | G015 → G028 | contribution | T073 “trust the feature more … keep the communication in the website” |
| R11 | G010 → G020 | precedes | T027 信息在双方确认后才提供 |
| R12 | G008 → G027 | contribution | T057 “filters … will give me an overview about the price ranges” |

循环检查：precedes 子图 G002→G006、G008→G009→G010→G020 无环；specialization 子图 G012→G013、G021→G022 无环；operationalization 子图 G003/G004/G005/G007→G002 无环。

### 2.2 逐条“已检查但无依据 / 不足以记录”的判断

1. **G014（看更新时间）→ G028（沟通留在站内）contribution**：T021 只说更新时间带来信任与投入意愿（“more enthusiasm to go and engage in the activity”），没说要留在站内；T073 的留站内结论挂在“看清沟通过程”上。故不记录，避免把两个不同收益混成一条边。
2. **G026（包含未填写项）→ G009（收窄选项）contribution**：两者方向相反（一个防漏、一个收窄），原文只说“怕漏掉未填写条件的房源”，没有任何句子说该功能帮助收窄；不记录。
3. **G019（不填必填项）→ G010（联系房东）contribution**：原文是“因此跳过站内申请”（T023），说明当前表单反而阻碍联系；这是障碍线索而非帮助关系，未记为 contribution，也未把“障碍”伪装成联系。
4. **G022（避免冗长流程）→ G021（免注册）contribution**：方向应为具体化（免注册是额外步骤的实例），已按 specialization 记为 R9，不再叠加 contribution。
5. **G017（评论）→ G014 / G027 贡献**：T033 只说评论让房源更可信、信息集中，T069 把评论列为现有详情之一；无“帮助获得价格总览”或“帮助确认最新”的语句，不记录。
6. **G018（照片规则）→ G028 / G017**：T059 只说统一照片格式会带来更多信任，未指向站内沟通或评论；不记录。
7. **G024（比较）→ G027（总览）**：T037/T071 说想把 3-4 个选项放一页看主要特征，与“价格区间总览”不是同一结果，且无比价帮助总览的原句；不记录（同主题不等于联系）。
8. **G011（按回复收窄）→ G009 / G010**：G011 与 G010 是同一沟通过程的两个侧面（T011 同句），属时间重叠而非先后或帮助；不记录，避免自造 order。
9. **G025（筛选可选）→ G026（包含未填写项）**：两者都改筛选行为，但无共同目的句，也无一方帮助另一方的依据；不记录。
10. **反向方向复核**：R2/R3/R4/R5 若改成“G002→G003”会把方式写成目的，已按定义纠正；R10 若反向（G028→G015）则成为“目的帮助手段”，与原文因果（看清流程→留站内）相反，已纠正。

未记录任何 `rejected`：本轮没有出现“同一条件下明确相反”的目标对，按契约不对未评估或仅弱相关的目标对补写否定。

### 2.3 精化组判断明细（含未建组的理由）

1. **GR1（G001 ← G002/G006/G008/G009/G010）= proposed + partial**：见 1.4。子目标之间存在 precedes（R1/R6/R7），而原文没有“做完这些就能找到房子”的句子；反例（房东不回复）在原文明说（T013/T019）。因此不标 supported/complete。
2. **G002 ← G003/G004/G005（OR 替代）**：原文用 “One of the ways / the other ways / Another thing” 明示三者是并列方式而非共同必需，不能写成 AND 组；若作为 OR，每组须“单独充分”，而原文只说“many ways”且“it depends”，未声称任一方式单独足以选定社区（G005 还带 if 条件）。故不建组，作为问题保留。
3. **G019 + G020 ← 假想父目标“无负担地联系房东”**：两者分别管“填什么”和“何时填”，可独立满足（可以只改字段而不改时点）；原文没有把它们合为一个结果的句子，父目标只能由我抽象出来 → 属造根，放弃。
4. **G025 + G026 ← 假想父目标“筛选不丢有效选项”**：同上，父目标无原句依据，且两者可分别满足；放弃。
5. **G014 + G015 ← 假想父目标“信息与流程透明”**：T021 同句提到两者，但同时提到只是“might be more comfortable”，没有“共同满足即足以透明”的声称；主题相近不构成充分性，放弃。
6. **G017 + G018 ← 假想父目标“房源可信”**：T033 与 T059 分属不同问答（首访体验 / 详情页），无共同充分性语句；放弃。

结论：**成立组 0 个**是本次原文支持的结果，不是遗漏；所有候选组与候选联系都已逐条判断并留下理由。

## 3. 工程检查实际结果（复制自 attempt-summary.json）

```
coverage_check: exit_code=0, structure=passed, workflow=recorded, pending=[]
  counts: source_segments=77, windows=38, raw_candidates=51, final_goals=29,
          source_checks=10, actual_passes=1,
          dispositions={keep:23, merge:19, split:6, exclude:3}
tracing_status: completed
declared_vs_effective_downgraded: []
windows: count=38, size=4, stride=2
inspection: structure=passed, readiness=reviewable,
            independent_semantic=not_run, formal_proof=not_run, human=pending
counts: goals=29, relations=12, groups=1, established_groups=0,
        raw_candidates=51,
        support_labels={direct:28, inferred:1, insufficient:0, contradicted:0},
        issues=8, blocking_issues=0
```

交付文件（manifest 内）：`delivery/goal-model.html`、`goal-model.json`、`goal-model.md`、`goal-model.svg`、`goal-relations.svg`、`manifest.json`、`attachments/{extraction,judgments,kaos-decisions,source,inspection}.*`。

## 4. 未决问题清单

建模层（`decisions.questions`，均非 blocking）：

1. `model / DOC021-goal-model`：G003/G004/G005 是三条并列选社区方式，未建 OR 组；是否要建三个单方案组并逐一核对完整性？
2. `group / GR1`：该组缺“房东回应并达成租赁”的结果；是否应把 G001 拆成“找到候选并建立联系”与“达成租赁”后重评？
3. `goal / G016`：由抱怨反推、无直接祈使，是否只保留 G028？
4. `goal / G018`：照片规则以 maybe 提出且依赖网站约束房东，是否降为方案？
5. `model / DOC021-goal-model`：C011（完全不回复=管理不善）目前作判断标准排除，若需“避免管理不善房源”应回提取新增目标。

提取层（`review_questions`）：G016、G018 两条与上列第 3、4 条为同一未决点，分别记录在提取层与建模层，未合并删除。

## 5. 实际执行情况

- 原文通读 2 遍：先整篇读完 77 轮，再在整理与引文定位时按 turn 精读并回查指代/条件/例外。
- 定向补查：T019/T021（可见性与信任）、T033/T049（地图与筛选）、T051/T053/T055（未填写项）、T059/T065/T067/T069（详情与更新时间）、T071/T073（单一平台与时限）交叉比对；相反证据（T065/T067/T069 认为详情已足够）已用于收窄 G014，未另造目标。
- 修复次数：1 次（inference 引用层级错误，详见 repair-log.md），同一 attempt 内完成，未新建 attempt。
- 实际耗时：未计时（unknown）。
- 停止原因：38 窗全部处理、全篇回查完成；关系与精化组判断执行后无新的有据目标或联系。

## 6. 未做的事

- 独立语义审查：not_run（本文件是生成方自检）。
- 形式化证明（精化充分性/完整性）：not_run。
- 人工接受：pending（模型 review 状态为 pending，无任何分项意见或采纳记录）。
- 未读取其他 run、参考模型、论文比较报告或任何历史答案；未联网检索。
