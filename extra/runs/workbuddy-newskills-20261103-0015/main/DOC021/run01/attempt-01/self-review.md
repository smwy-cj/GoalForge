# 自检记录（生成方自检，非独立语义评审）

DOC021 / run01 / attempt-01。本文件由**生成方**编写，属于生成后的自我核对，不构成独立的语义评审、形式证明或人工接受。

## 1. 生成方自检

- **候选是否被压薄**：按 38 个 4 轮窗口（步长 2）逐窗捕获，得 49 条原始候选，未先压成“主要需求”清单；W0031–W0034 等以确认现状为主的窗口没有新目标，也未强行补条目（C043、C044 只作现状/补充证据）。
- **复合项拆分**：C027（强制注册 + 未知按钮）拆为 G018/G020；C035（主筛选 + 附加条件）拆为 G007/G008；C010、C016、C021、C022、C039、C047、C048 等确认为同义或同一动作的限定并合并，理由逐条写入 `ledger.entries`。
- **条件/否定/强度**：G004 保留“有固定上班或上学地点”、G016 保留“双方确认后”、G018 保留“注册可自愿但不应强制”、G027 保留“勾选后才包含未注明项”、G028 保留“maybe”的试探强度（同时写入 context）、G029 保留“流程清晰且快”的条件与“一周至一月”的时限 context。G012 是现状（站外沟通）而非要求，未改写成禁止站内沟通。
- **精化组是否有反例**：仅建 1 组 GR1（G029 ← G014+G015），本身存在反例（房主不回应时用户仍转电话/邮件，T013/T017），故记为 `proposed/partial`，未作为成立层级展示。成立组 = 0，未为层级造根。
- **是否为凑数造目标/连边**：29 个目标均有独立候选来路与各自证据；13 条联系均引实际关系原句，未把“同主题/先后操作”写成精化（唯一 `precedes` 只声明先后并注明非因果）；未发现为增加边数扩写目标的情形。
- **遗留风险（自检视角）**：G001 偏情境化，G028 为弱建议；C049（时限）只作 context 未单列，属判断取舍，已写入问题。

## 2. 工程检查实际结果（复制自 attempt-summary.json）

- `coverage_check`：exit_code 0，structure `passed`，workflow `recorded`，pending `[]`；counts：source_segments 77、windows 38、raw_candidates 49、final_goals 29、source_checks 13、actual_passes 1；dispositions：keep 27 / merge 16 / split 2 / exclude 4。
- `tracing_status`：completed；`declared_vs_effective_downgraded`：`[]`；warnings：`[]`。
- `inspection`：structure `passed`，readiness `reviewable`，independent_semantic `not_run`，formal_proof `not_run`，human `pending`。
- `counts`：goals 29、relations 13、groups 1、established_groups 0、support direct 29 / inferred 0 / insufficient 0 / contradicted 0、issues 7、blocking 0。

## 3. 未决问题

1. model：G012（现状在站外沟通）与 G029（希望沟通留在站内）应理解为条件性偏好还是并行渠道。
2. group GR1：仅覆盖“流程可见 + 短联系”，未覆盖响应时限与房主不回应，是否还缺一个“可达性/时限”目标。
3. goal G012：作为现状保留，还是视为待改变的行为。
4. goal G028：以“maybe”提出的照片格式规则，是否保留为目标而非偏好。
5. goal G001：搬迁找房是流程触发情境，作为独立目标是否过泛。
6. （工具派生）GR1 因未成立，按规则挂一条“仍需确认”的提示，非新增异议。

## 4. 实际执行情况

- 原文通读 1 遍（77 轮全文），并按 4/步 2 的 38 个窗口逐一捕获；另做 1 次全篇校正（回看指代、问答范围、条件继承、例外与相反证据）。
- 补查：0 次独立补查轮次（P1 内完成跨窗校正）；新建候选均记 `pass_id=P1`，未伪称额外轮次。
- 修复次数：0（attempt-01 一次通过，无 downgraded、无 blocking）。
- 引文校验：编制期用本地脚本核对 136 条引文与对应 turn 文本逐字一致且唯一。
- 实际耗时：自报约 45 分钟（含读技能、读原文、编制与校验）。
- 停止原因：完成一次全篇逐窗捕获与全篇校正，覆盖全部 38 个窗口，无待处理覆盖项。

## 5. 没有做的事

- 独立语义审查：not_run（本文件是生成方自检）。
- 形式证明（精化充分性/完整性）：not_run。
- 人工接受：pending，未替用户采纳，review 状态保持 pending。
