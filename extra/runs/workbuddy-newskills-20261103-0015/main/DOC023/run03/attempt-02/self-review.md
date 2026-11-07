# 自检记录（生成方自检）

> **这是生成方自检，不是独立语义评审。** 同一会话既做提取、又做判断、又做组核验，不构成独立复核；独立语义审查 not_run，形式证明 not_run，人工接受 pending。

任务：DOC023（19 轮英文访谈转写，2026-11-03）/ run03 / attempt-02（attempt-01 因结构报错作废）。

## 1. 生成方自检

**候选是否被压薄？** 20 条原始候选覆盖 T001、T003、T007、T009、T011、T013、T015、T017 八个有内容的轮次，9 个窗口全部登记 processed。保留了 7 条最终被排除的记录（话题陈述、信念/理由、障碍、流程可能性），未按“主要需求”压缩；排除项都在 ledger 里写了可核对理由，未删除。

**复合目标是否拆分？** 只在有独立意图依据处拆：T003 一句里的“增加连接数”与“获得现任员工转介”拆为 G001/G003；T003 的“让查看者看到我活跃”独立成 G002（原句为 `to make sure that`，是目的而非修辞）。相反，T007 的附言三要素（自我介绍、请求转介、说明同校）按“同一对象（一条附言）的多个限定”合并为 G007，没有机械按分句拆成三项目标。

**条件、否定、强度是否丢失？**
- AND 未被改成 OR：G005 保留“现任员工且校友”同时满足，并保留两类排除项（前员工不能转介；只满足一项或不满足）。核对依据 T009 原文两次使用 and。
- 条件：G004 限定“为求转介时”；G006 限定“经历完全符合目标职位才发起连接”；G007 带 200 字符与非会员平台条件。
- 强度：G008 保留 `usually / simplest way` 与 `costs a lot`（偏好 + 代价，未升级为强制）；G009 保留 `sometimes / other option`（替代方案）；G007 的 `usually`、`maybe` 未被写成必做。
- 否定/例外：T007 的“对方不接受则只保持 pending”没有被改写成“必须接受”。
- 未把信念当事实：C013（校友更愿意帮忙）、C014（只有现任员工能转介）只作为 G004/G005 的判断理由与条件，未建成目标，也未在目标里断言为事实。

**精化组是否有反例未解决？** 有，且已如实收回：GR1 为 `proposed + partial`，三条反例（搜索结果可能只有 1–2 人或没有符合条件者；非会员只能看有限结果；对方接受连接但拒绝转介）未解决，未进入成立精化 DAG。成立组数 = 0，这是原文支持下的真实结果，没有为凑层级改写。

**是否有为凑层级造根？** 没有。只有 G002 作为 T003 明确说出的目的保留为上层目标，其余为多根（G001、G002、G008、G009 等顶层并存）。未新增“职业发展”一类泛化根。R8（precedes）判 rejected，说明了“顺序不等于联系”，未把流程步骤变成层级。

**关系与精化判断是否执行完毕？** 四类逐一检查：
- operationalization：4 条（R1–R4），均为“手段目标 → 获取转介”；
- contribution：3 条（R5 Premium→检索、R6 调关键词→检索、R7 增连接数→显活跃）；
- specialization：已检查，原文没有“一般目标 / 其具体情境版本”的成对表述（G004–G007 是手段而非 G003 的窄化版本），故无此类联系；
- precedes：唯一候选 G004→G007 有流程先后字样（`and then`），但检索结果不是被追求的结果状态，中间还隔着 G005/G006，判 rejected 并留证（本项即“已检查但无依据”的逐条说明）。
未评估的目标对不补写 rejected；相关/同主题不连边（如 G001 与 G003 同属“用 LinkedIn”，未连）。

## 2. 工程检查实际结果

`attempt-summary.json`（原样摘录）：

```
coverage_check: exit_code 0, structure "passed", workflow "recorded", pending []
  counts: source_segments 19, windows 9, raw_candidates 20, final_goals 9,
          source_checks 8, actual_passes 1,
          dispositions {exclude 7, keep 9, merge 4}
tracing_status: "completed"
declared_vs_effective_downgraded: []
inspection: structure "passed", readiness "reviewable",
            independent_semantic "not_run", formal_proof "not_run", human "pending"
counts: goals 9, relations 8, groups 1, established_groups 0, raw_candidates 20,
        support_labels {direct 9, inferred 0, contradicted 0, insufficient 0},
        issues 8, blocking_issues 0
warnings: []
```

说明：8 条 issue 均为非阻断，其中 G003、G008 各出现两次，是因为提取层 `review_questions` 与建模层 `decisions.questions` 分别登记了同一未决点（两层职责不同，未合并）。

## 3. 未决问题

1. G003：`for my 3rd company` 所指不明，现按“所申请的公司”泛化，是否应收窄。
2. G007：200 字符上限只作为条件，是否应把“在限制内完整传达意图”单列为质量目标。
3. G008：购买 Premium 是偏好方案且成本高，是否保留为目标。
4. GR1：三条反例是否需要以新的障碍/目标承接，还是作为该组的未决缺口保留。
5. 模型级：`I can then` 描述的“接受后继续沟通转介细节”未建目标（判为流程可能性），是否应补为条件目标。
6. 转写噪声（Linking=LinkedIn、except=accept、`the Madison`、`seeing his sub membership`）影响个别措辞理解，未取得音频核对。

## 4. 实际执行情况

- 读原文 2 遍：第 1 遍全文逐轮读 + 逐窗（4/步长 2，9 窗）捕获候选；第 2 遍全篇校正指代、条件继承、例外与相反证据（重点核对 T007/T009 的 `they` 指代、T011 的因果解释、T013/T015/T017 的条件）。
- 补查 0 次定向补查；无新增 `P2` 候选（原文较短，一轮覆盖后未发现遗漏意图）。
- 修复 2 次：运行前自查改 2 处引文笔误；运行后 1 次结构性修复（GR1 的 source 场景补证据）→ attempt-02。总计 1 个修复轮次。
- 耗时自报：约 25 分钟（含技能通读、逐窗捕获、建模与检查）。
- 停止原因：原文全部轮次与窗口处理完毕，语义与结构检查均通过，无新证据可推进未决问题。

## 5. 我没有做的事

- 独立语义审查：not_run（本文件是生成方自检）。
- 形式证明：not_run（精化仅为概念层判断，程序只验证引用与结构）。
- 人工接受：pending（未代用户采纳，未把未填写意见当作认可）。
- 未读取仓库其他目录、未联网检索论文或案例答案、未参考任何历史目标/关系/评分。
