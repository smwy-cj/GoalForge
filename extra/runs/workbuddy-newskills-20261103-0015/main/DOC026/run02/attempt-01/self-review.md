# 自检记录（生成方自检，非独立语义评审）

> 本文件由生成方在同一隔离会话内编写。它不是独立语义审查，也不是形式证明或人工接受。

## 1. 生成方自检

- **候选是否被压薄**：未按“主要需求”压缩。30 条原始候选取自 T005–T045 的实际表述，含使用习惯、赞许、知识不确定等弱信号；22 条进入最终目标，7 条排除、1 条待确认，均写去向理由。
- **复合目标是否拆分**：T019/T021 的“租车 vs 公交 vs Uber”拆为不同情境目标（G009/G011/G013），T011 的价格、等待、选最便宜、看附近司机拆为 G004/G005/G006，T037 的单目的地偏好与多站点加速拆为 G016/G017。操作步骤（点地址、看地图）未机械拆成目标。
- **条件/否定/强度是否丢失**：保留“除非多人同行”（G004）、“约一个半小时”（G003）、“不熟悉地区不坐公交”（G012）、“费用由雇主承担”（G010）、“工作免费公交卡”（G011）、“I think/记不清”的保留语气（G021 判 inferred）。已选定的方式（直接告知司机而非应用内改点，G020）进入目标正文，不只写在理由里。
- **精化组是否有未解决反例**：本次 0 组。租车/公交/Uber 属替代方式，不能写成 AND 共同满足；工作出行时间优先与总的时间/价格判断只构成具体化联系，不构成整组充分性。没有为产出层级造根。
- **是否造根/凑边**：未新增“出行体验”之类泛化根；仅保留 2 条有原句依据的联系（R1 具体化、R2 实现方式），未把同主题或操作先后连边。
- **已知瑕疵**：G007/G019/G021 的待确认问题在 `review_questions` 与 `decisions.questions` 各出现一次，措辞略有差异，模型 issue 列表因此有 3 组重复提示；不影响结构与支持标签，未为此另起修复轮。

## 2. 工程检查实际结果

- coverage_check：exit_code=0，structure=passed，workflow=recorded，pending=[]；counts：source_segments=48，windows=23，raw_candidates=30，final_goals=22，source_checks=17，actual_passes=1，dispositions={keep:22, exclude:7, uncertain:1}。
- tracing：status=completed；declared_vs_effective_downgraded=[]。
- inspection：structure=passed，readiness=reviewable，independent_semantic=not_run，formal_proof=not_run，human=pending。
- counts：goals=22，relations=2，groups=0，established_groups=0，issues=7（blocking=0）；支持分布 direct=19，inferred=3，insufficient=0，contradicted=0。

## 3. 未决问题

1. G007（避免匹配失败）是否超出“单次问题描述”，原句只有抱怨与对应用夸大/司机拒单的猜测。
2. G019（多站点迟到告知司机）是假设情境下“会有帮助”的评价，受访者自述未必做过。
3. G021（使用当前位置时改上车点）依赖受访者有保留的记忆与绕行做法。
4. 模型级：单一样本的个人偏好（最便宜、单目的地）能否视为产品通用需求。
5. 提取级：T015“start a ride to cancel it”措辞含糊，保留为 uncertain 候选，未建立目标。

## 4. 实际执行情况

- 原文通读 1 遍（48 轮全文），按 4 轮窗口/步长 2 处理全部 23 个窗口，逐窗记录 processed。
- 全篇校正回查：T007 条件与步行替代、T011 限定与等待、T013 对答范围、T015 措辞、T019 价格/时间反转、T021 公交条件、T031 人工客服、T041 语气保留、T045 回看费用目的；采访者未获回应处（T017/T023/T028）未当作涉众目标。
- 修复次数：0（首次 harness 即通过，无降级、无 blocking）。
- 耗时：约 20 分钟（自报，未计时）。停止原因：一次整篇读取加全篇校正后无新增有据意图，按预算停止。

## 5. 我没有做的事

- 独立语义审查：not_run。
- 形式化证明：not_run。
- 人工接受：pending（模型 review 保持 pending）。
