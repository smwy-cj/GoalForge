# repair-log（attempt-01 内重跑）

说明：本次任务指令要求「在本目录内修正 spec.json 后重跑并写 repair-log.md」，因此未另建 attempt-02/03。每次重跑前只清理上一次失败运行留下的中间文件（work/、extraction.json、raw-candidates.json、judgments.json、extraction-ledger.json、coverage-check.json、inspection.json、attempt-summary.json、kaos-decisions.json、tracing/、assembled/、delivery/），不改写已成功的语义内容。semantic 内容实际改动 3 次，环境清理 2 次；harness 共调用 6 次，最后一次成功。

| 次序 | 触发环节 | 报错/现象 | 改动对象 | 理由 |
|---|---|---|---|---|
| 1 | `trace_candidates --judgment-template` | `ValueError: Unknown inference reference` | G013 的 `inference.basis_candidate_ids` 由 `["C030","C031"]` 改为 `["G004"]`，并改写 `reason` | 契约要求 `basis_candidate_ids` 指向目标集合（G 前缀），原始候选 ID 不被接受；G013 的推断情境正是 G004（睡前播放、留白噪音）。 |
| 2 | `prepare_source` | 拒绝覆盖已存在的 `work/` | 无 spec 改动，删除残留 `work/` 等失败中间物 | 上一轮失败留下的目录导致工具按设计拒绝覆盖，属环境问题。 |
| 3 | `kaos_model template` | `FileExistsError: kaos-decisions.json` | 无 spec 改动，清理全部生成物 | 同上，残留文件未清干净。 |
| 4 | `check_coverage` | `exit 2`，errors：`S10 contradicts candidate dispositions` | `source_checks.S10.final_goal_ids` 由 `["G008","G007"]` 改为 `["G008"]`，理由中注明该句同时是 R1 的关系原句 | S10 只对应 C036，其处置映射到 G008；把 G007 列入与 entries 不一致。 |
| 5 | 模型组装后的复核问题 | G008/G011 的同一段问题被按每个目标各生成一条，md 中出现重复 | `review_questions` 中该条只保留 `["G008"]`，G011 的张力仍在 `decisions.questions`（target G008）中说明 | 去除重复文案，不改变语义判断。 |
| 6 | 全流程 | `ok: true`，coverage `recorded`，readiness `blocked`（G015 insufficient） | 未再改动 | 达到交付条件；blocking 为如实保留的支持不足目标，按任务要求不升级。 |

未做的事：没有为了让检查通过而删除有依据的目标、删除证据或改动支持标签；没有改动任何 evidence 引文去迁就工具。
