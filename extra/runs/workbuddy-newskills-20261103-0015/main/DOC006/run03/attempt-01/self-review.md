# self-review — DOC006 / run03 / attempt-01

> **本文件是生成方自检，不是独立语义评审。** 生成与自检由同一隔离会话完成；未执行独立语义审查、形式证明，人工接受仍为 pending。

## 1. 生成方自检

### 1.1 是否被压薄
- 逐窗捕获 36 条原始候选（22 个窗口，4 轮/步长 2，全部窗口 processed），未先写“主要需求”再反推；窗口无意图者不强行造候选（W0022 仅收尾语，无候选）。
- 保留了口语中的弱语气与保留意见：`might want`（G005）、`would be better`（G004/G007）、`maybe`（G011）、`might just`（G009）、`kind of satisfied`（C021，排除项）。

### 1.2 复合目标是否拆分
- T019 一句含两项信息需求（招聘流程人数 / 面试者反馈）→ 拆为 G005、G006，各自保留目的从句。
- T023 一句含“分开娱乐与有用内容”与“不想看时过滤”→ 归为一个核心动作（过滤）+ 预期结果（分离），未机械按两个动词拆点；条件“不想看时”写入 statement 与 context。
- T007 的“滚动主页 / 每日排行”两条操作属被问“你采取什么动作”的现状路径，未拆成目标（C007/C008 exclude）；其结果由 G001 承接。
- T011/T013/T015 三处同一愿望（地区检索）合并为 G004，未因重复出现造三节点；实现形态（专门按钮或类似功能）作为未定方式记入 context，未固化为“按钮”目标。

### 1.3 条件/否定/强度是否丢失
- 否定：G002 为避免型目标（`do not want to miss out`），未改写为“获取重要信息”。
- 条件：G007 限定“不想看时”，未升级为全局过滤；G004 的“以租房为例、岗位侧问题较小”保留在 context，未把示例固化为独立业务目标。
- 相反证据：T031/T033/T035/T037 的“接受泄露、不在意”与 T039 的弱建议分别处理，未把抱怨或建议当强制要求；T041 明确否认应用内隐私手段，故未建隐私功能目标（C033 exclude）。
- 未把已实现能力（搜索栏、滚动、图文娱乐）自动当作要求；仅当原文明示必要/偏好时才建维持型目标（G008、G011）。

### 1.4 精化组是否有未解决反例
- 唯一组 GR1（G002 ← G001 + G003）标 `proposed`/`partial`：异常场景“重要信息只出现在应用外或私信/群组”构成未解决反例，故不标 supported/complete。成立组数 0，未为产出层级硬造。
- 未为凑层级造根：11 个目标均为多根独立节点（无虚构上层“提升用户体验”根）。

### 1.5 联系方向
- R1/R2 为方式→目的（operationalization），方向未写反；R3/R6/R7 为有帮助→受帮助（contribution）；R4/R5 因“帮助求职搜索”属分析推断而标 proposed，未冒充 supported。

## 2. 工程检查实际结果（复制自 attempt-summary.json）

```
coverage_check: exit_code 0, structure=passed, workflow=recorded, pending=[]
  counts: source_segments=46, windows=22, raw_candidates=36, final_goals=11,
          source_checks=14, actual_passes=2,
          dispositions={keep:11, merge:10, exclude:14, uncertain:1}
tracing_status: completed
declared_vs_effective_downgraded: []
inspection: structure=passed, readiness=reviewable,
            independent_semantic=not_run, formal_proof=not_run, human=pending
counts: goals=11, relations=7, groups=1, established_groups=0, raw_candidates=36,
        support_labels={direct:11, inferred:0, insufficient:0, contradicted:0},
        issues=11, blocking_issues=0
warnings: []
```

## 3. 未决问题清单

来自 `review_questions`：
1. G009（不向第三方出售数据）与 T033/T037“接受泄露、不在意”是否属同一情境下的相反意愿；本稿保留为弱建议是否为最佳处置。
2. G007 的娱乐过滤是仅在实用内容检索时生效还是全局可开关（与 G011 并存）。
3. G005/G006 是求职搜索的一部分还是独立的雇主评估需求。

来自 `decisions.questions`：
4. GR1 是否还应纳入其他重要信息类型（本地事件、私信、群组公告），否则无法判断共同充分性。
5. R4 招聘流程人数是否真正帮助求职搜索（保留 proposed）。
6. R5 面试者反馈是否改变其搜索/投递行为（保留 proposed）。

blocking issue：0 条。

## 4. 实际执行情况

- 原文读取：完整读取 46 轮 1 遍（全文 JSON），随后按 22 个重叠窗口逐窗处理 1 遍（P1），再通篇回查 1 遍（全篇校正），另做 1 次定向补查（P2，聚焦 T003 含糊句与 T011/T013 条件继承）。
- 补查结果：新增 1 条候选 C036（uncertain，未建目标），无新的有据目标；按预算停止。
- 修复次数：0（首次 harness 即通过，无降级、无 blocking）。
- 耗时（自报）：约 8 秒 harness 机械执行；人工/模型阅读与编制过程未单独计时（unknown）。
- 停止原因：完成基础提取 + 全篇校正 + 一次定向补查，无新有据意图；保留未决问题。

## 5. 我没有做的事

- 独立语义审查：**not_run**（本文件为生成方自检）。
- 形式证明 / 精化充分性证明：**not_run**。
- 人工接受：**pending**（`review.status=pending`，未替用户采纳）。
- 未读取仓库其他目录、未联网检索论文或案例答案、未参考任何历史目标或评分。
