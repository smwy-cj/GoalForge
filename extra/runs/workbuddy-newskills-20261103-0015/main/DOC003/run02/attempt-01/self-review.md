# self-review（生成方自检，非独立语义评审）

> 本文件由**生成方**在 harness 成功后自检编写，属于作者自查，**不是**独立语义评审，也不构成人工接受。

## 1. 生成方自检

- **候选是否被压薄**：38 条原始候选覆盖 81 个窗口中的实质意图窗；空窗（寒暄、屏幕共享限制、UI 操作旁白）无候选但有 `processed` 记录，未用"主要需求"摘要替代底层候选。
- **复合目标是否拆分**：C007（区域检索+按价格/日期/物流收敛+供应商核价）、C021（广度+耗时）、C027（受访者自述三目标）等按"能否独立满足"拆分，共 11 条 split；同时避免了机械拆动词——C012 的"起降时段+空中时长上限"作为同一组筛选限定保留为一个目标。
- **条件/否定/强度是否丢失**：G005 保留"probably never log in"与里程票登录例外；G008 保留 `at least 1–1.5 months`；G011 保留 `would rather not`（未写成禁止）；G015 保留 `nice to have`；G021 保留"不介意红眼但更想睡整觉"；G001 保留价格差过大时的让步与紧急时的回退。
- **状态/避免型意图**：G005（不登录）、G006（数据不被共享）、G011（避免超长行程）、G021（避免红眼）均按状态/避免意图保留，未因缺动作句式删除。
- **信念未当事实**：T053 的"追踪会抬价"、T093 的"除非看到源码否则不信"仅作为理由/条件，未写成已验证事实。
- **已实现能力**：Skyscanner 支持按国家检索、跳转供应商页面等能力描述（C023）未自动升级为要求；只有受访者自述的做法与目的才进入目标。
- **精化组反例**：GR1 的正常/异常两类场景均为 `analysis_assumption` 且 `outcome=supports`，未发现未解决反例；里程票场景因父目标已限定为现金票而排除在组外，此点在 `assumptions` 中写明。
- **是否为凑层级造根**：唯一上层目标 G020 直接来自 T115/T129 的自述（"三个目标"），非摘要生成；其余 20 个目标多根并存，无固定层数。
- **未做硬造关系**：G011↔G018、G017↔G005、G006↔G002/G003 已逐一检查后判定"无原文关系句"，理由写入 `decisions.questions`（model 级，target_id=DOC003-goal-model），未省略该阶段。

## 2. 工程检查实际结果（复制自 attempt-summary.json）

- `coverage_check`：`exit_code=0`，`structure=passed`，`workflow=recorded`，`pending=[]`；
  `counts`: source_segments 163、windows 81、raw_candidates 38、final_goals 21、source_checks 17、actual_passes 2、
  dispositions {split 11, keep 11, exclude 4, merge 12}。
- `inspection`：`structure=passed`，`readiness=reviewable`，`independent_semantic=not_run`，`formal_proof=not_run`，`human=pending`。
- `counts`：goals 21、relations 17、groups 1（established_groups 1）、support_labels {direct 21, inferred 0, insufficient 0, contradicted 0}、issues 14、blocking_issues 0。
- `declared_vs_effective_downgraded=[]`，`warnings=[]`。

## 3. 未决问题清单

来自 `review_questions`（5 条）与 `decisions.questions`（7 条），blocking issue 为 0：

1. G014 休息室权益聚合：愿望与"更信任发卡方源头信息"并存，是否保留为需求待确认。
2. G020 作为三目标之上的组织层是否符合受访者本意（分析者组织，非原话）。
3. G011 与 G018 在"同一行程"上同时适用时的取舍，原文未说明。
4. G015 只是 nice to have，是否进入需求集合。
5. G017 里程票流程是否属于本应用范围（T046 范围未完全确定）。
6. GR1 在紧急出行只剩一条行程时退化为单一选项，是否仍视为满足父目标。
7. R11（G014→G013）保持 proposed，待确认是否应否定。
8. model 级四条：G011↔G018、G017↔G005、G006↔G002/G003 已检查无关系依据；G008/G004/G007/G003 对 G002 不构成充分精化，故不建第二组。

## 4. 实际执行情况

- 原文通读：1 遍完整通读（T000–T162，分 3 段连续读完，无跳读、无抽样）；T031 单轮超 2000 字符，首次阅读视图被截断，已用完整原文重新核对后引用。
- 全篇校正：P2 全篇复核 64 个窗口（跨窗指代、条件继承、让步、例外、相反证据），其余 17 个窗口因无相关争议 `skipped` 并写明理由。
- 修复次数：1 次（review_questions 引用类型错误），语义零改动；另有 1 次中间产物清理后重跑。
- 耗时：约 40 分钟（自报）。
- 停止原因：163 轮全部处理、81 窗全覆盖，无新证据可推进的未决项转入问题清单。

## 5. 没有做的事

- 独立语义审查：not_run（本文件是生成方自检）。
- 形式证明：not_run（结构无环不等于精化充分）。
- 人工接受：pending。
- 未读取仓库其他目录、其他 run、参考资料或参考答案；未联网。
