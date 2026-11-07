# DOC019 生成方自检（attempt-01）

> **性质声明：本文是生成方自检，不是独立语义评审。** 生成、核验、自检由同一隔离会话连续完成；独立语义审查、形式证明、人工接受均未执行。

## 1. 生成方自检

- **候选是否被压薄**：未压薄。33 条原始候选覆盖全部 32 个窗口，包含背景、习惯、障碍、偏好与提议，未先归纳成“十几条主要需求”。T000–T002、T005–T007、T025–T027、T034–T035、T041–T042、T045、T048–T049、T051、T053、T055–T057、T061–T064 为寒暄/追问/承接，无可捕获意图，窗口仍记 processed。
- **复合目标拆分**：C008 拆为 G005（银行绑定）与 G006（法币↔加密转换）；C018 拆为 G009（看当下走势）与 G010（即时下单）。两处均保留共同情境，理由记入 entries。
- **条件/否定/强度**：保留“印度使用时期”“已上手后”“if it is possible”“I'm not sure how feasible it is”“would be good”“as easy as possible”，未把可行性不确定写成承诺；T050“下单流程不复杂”作为相反证据，未造“简化下单”目标。
- **精化组反例**：无成立组。逐对检查了学习类组合（G002/G003/G012/G013）、G005→G015、G006→G010、G011→G009，均不满足“共同满足足以实现父目标”；详见 kaos-decisions.json 的 model 级 question。
- **是否为凑层级造根**：未造根。四个目标来自 T024 明示的三层目标；“理想的交易应用”只是访谈提问，未升为根目标。
- **关系**：5 条，4 条 supported、1 条 proposed（R5，依赖关系原文未明说），方向均按定义核对，未把贡献画成精化。

## 2. 工程检查实际结果（复制 attempt-summary.json）

- coverage_check：exit_code=0，structure=passed，workflow=recorded，pending=[]
- coverage counts：source_segments=65，windows=32，raw_candidates=33，final_goals=16，source_checks=11，actual_passes=1；dispositions={exclude:10, merge:8, split:2, keep:13}
- inspection：structure=passed，readiness=reviewable，independent_semantic=not_run，formal_proof=not_run，human=pending
- tracing_status=completed；declared_vs_effective_downgraded=[]
- counts：goals=16，relations=5，groups=0（成立组 0），raw_candidates=33，support={direct:16, inferred:0, insufficient:0, contradicted:0}，issues=8，blocking_issues=0
- warnings：无（引文均唯一命中，无 ambiguous）

## 3. 未决问题清单

1. G011：组合仪表盘仅“最常用、喜欢”，无明确维持/改进要求，是否作为偏好型目标保留（review_questions + decisions.questions，重复列出）。
2. G016：语音下单与语音摘要按“or”读作替代，是否应拆为两个目标。
3. G014：共同基金选项在“可行性未知”下是否仍保留为目标。
4. R5：银行绑定是否为法币出入金的必要前提，原文未明说，故标 proposed。
5. 精化组为空（model 级 question 记录检查范围与不成立理由），需人工确认是否接受无层级结果。

## 4. 实际执行情况

- 原文读取：完整读取 65 轮（source/DOC019.json），按 4 轮/步长 2 处理 32 个窗口，逐窗记录处理状态；另做一次全篇回查（指代、条件继承、让步、例外、相反证据）。
- 补查：跨窗回查 T012↔T044、T016/T018↔T028、T030↔T036、T038/T040↔T028；未新增 P2 候选，故 pass 只有 P1。
- 修复次数：0（首次 harness 成功，无降级、无 blocking）。
- 耗时：自报约 35 分钟（含读技能与原文、编制、运行）。
- 停止原因：完成一次基础提取 + 全篇校正 + 建模判断，无新的有据意图可补。

## 5. 没有做的事

- 独立语义审查：not_run（本文为生成方自检）。
- 形式证明：not_run；结构通过不证明精化充分性。
- 人工接受：pending；未提出反对不等于采纳。
- 未读取仓库其他目录、其他 run 或参考答案，未联网检索。
