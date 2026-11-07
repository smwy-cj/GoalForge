# 自检记录（生成方自检，非独立语义评审）

本文件由**生成方**在同一隔离会话中编写，属生成方自检；**不是**独立语义审查，也不构成人工接受。

## 1. 生成方自检

- **候选是否被压薄**：48 轮按 4 轮窗口/步长 2 切成 23 个窗口逐窗捕获，共 37 条原始候选，未先压成“主要需求”。无意图的窗口（W1 寒暄、W8 追问、W11/W17/W21/W23 仅复述或收尾）记录为 processed 且无候选；W21 的访谈者复述（T042）与受访者确认（T043）作为 G021 的上下文证据，未另造候选。
- **复合候选是否拆分**：T007 的“按时间与价格决定是否叫车”与“约 1.5 小时宁可走路”按同一决策规则合并为 G002（阈值例不单独建点）；T011“最便宜除非多人同行”、T011“价格高就等”拆为 G003、G004（不同动作、不同条件）；T037 的“偏好单一目的地”与“中途停留要快”拆为 G016、G017；T045 的“分摊”“报销”共用同一动作（查看车费），合并为 G022 并在条件中保留两类情境。
- **条件、否定、强度是否丢失**：“除非多人同行”“价格太高且不必现在出发”“费用可报销”“不熟悉地区”“公交需步行或换乘”“用当前位置下单”“自述未实践”“我猜应用夸大了可用性（信念）”“通常/更愿意/大概”等均写入 statement 或 context；未把偏好升级为必须，未把信念当事实（G006 的评分理由、C013 的猜测均标注为信念并排除为诊断）。
- **精化组是否有未解决反例**：本模型 **0 个精化组**，未声称任何“共同满足”。R1（G021→G020 实现方式）为 supported，R2（G019→G017 贡献）为 proposed，理由中说明只是缓解、未证明使停留变短，缺口留在问题里。
- **是否为凑层级造根**：未造根目标。22 个目标全部直接来自候选映射（21 keep + 拆分/合并映射），无仅为连边而增的节点；父目标、组均为空是实际判断结果，已在模型级问题中说明。
- **残留风险（自查）**：G007 依赖一句口语重复的转写（“I kind of wish that I don't want to just start a ride to cancel it”），G019 依据的是“有帮助”的评价而非实践，G005/G014/G020 为推断目标；四项均已进入 review_questions 与 decisions.questions。

## 2. 工程检查实际结果（复制 attempt-summary.json）

- coverage_check：`exit_code=0`，`structure=passed`，`workflow=recorded`，`pending=[]`
  - counts：source_segments 48，windows 23，raw_candidates 37，final_goals 22，source_checks 15，actual_passes 1，dispositions {keep 21, merge 6, exclude 10}
- inspection：`structure=passed`，`readiness=reviewable`，`independent_semantic=not_run`，`formal_proof=not_run`，`human=pending`
- counts：goals 22，relations 2，groups 0，established_groups 0，issues 10，blocking_issues 0
- 有效支持分布：direct 18 / inferred 4 / insufficient 0 / contradicted 0；`declared_vs_effective_downgraded=[]`，`warnings=[]`
- tracing_status：completed

## 3. 未决问题清单

来自 review_questions / decisions.questions / 非阻断 issue：

1. G007：转写句是口语重复还是双重否定？“取消前不必先开始行程”的读法需核对原录音；是否区分取消已预约与进行中行程。
2. G019：受访者自述未实践但认为“有帮助”，应作为偏好还是仅作功能评价？
3. G020：改点困难是否只发生在“用当前位置起单”的流程？若应用内本不支持改点，是否改写为“通过司机协调完成改点”？
4. G005、G014：由抱怨/失败推断的“顺利订车”“预估准确”是否应作为明确要求保留？
5. 模型级：0 个精化组、仅 2 条联系；是否需要回查“顺利完成一次行程”类上层目的（未在本次证据范围内成立，未补造）。

## 4. 实际执行情况

- 读原文：2 遍（整篇逐轮通读一遍；随后按 23 个窗口坐标逐窗复核一遍，并做全篇指代/条件/例外回查）。
- 是否补查：无额外独立补查轮次（planned_passes=1，pass P1 覆盖全部 23 窗口）；全篇校正中发现并接管的跨窗指代：T008→T007、T042→T041、T043→T042 的确认、T045 的“it”→车费、T041 的“it”→应用内改点。
- 修复次数：1 次（attempt-01 因 inferred 目标缺 `inference.reason` 在 judgment_template 失败 → attempt-02 补齐四个目标的 inference 后通过）。
- 实际耗时（自报）：约 35 分钟（含 attempt-01 失败与 attempt-02 重跑）。
- 停止原因：完成一次全篇窗口化捕获与全篇校正，未再发现新的有据意图；剩余未决项保留为问题，不再重复同一判断（见 extraction-ledger run.stop_reason）。

## 5. 没有做的事

- 独立语义审查：not_run（本文件是生成方自检）。
- 形式化证明：not_run；概念层 AND 精化未被声称成立。
- 人工接受：pending（模型 review 状态保持 pending，无任何分项意见）。
- 未联网检索论文或案例答案；未读取 development_reference、baselines、benchmarks 或其他任务目录；未参考任何历史目标/关系/评分。
