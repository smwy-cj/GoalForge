# 新版三技能实验协议（workbuddy-newskills-20261103-0015）

本文件在执行前冻结。执行期间不修改技能规则、源代码或测试标准；任何偏离都写入 `logs/deviations.md`。

## 1. 版本与冻结

| 项 | 值 |
|---|---|
| 技能来源 | `skills/goal-extraction`、`skills/goal-model-building`、`skills/model-review` |
| 冻结副本 | `versions/skills/`（逐文件 SHA-256 见 `versions/manifest.json`） |
| 技能树哈希 | 见 `versions/manifest.json` 的 `tree_sha256` |
| 提取契约 | `goalforge-extraction-3` |
| 模型版本 | `goalforge-kaos-2` |
| 已退役 | `goal-tracing` 不使用；旧版 skills 不重跑 |

所有正式运行只调用 `versions/skills/` 下的脚本，命令记录在每次 attempt 的 `attempt-summary.json.commands`。

## 2. 数据隔离

- 唯一生成输入：`inputs/source/DOC003..DOC036.json`（白名单副本，哈希见 `inputs/input-inventory.json`）。
- 单个任务工作目录只含：分配的原文、`brief.md`（统一任务说明）、冻结技能（只读引用）、该任务自己的输出目录。
- 生成任务禁止读取：`development_reference/`、任何人工目标/关系标签/参考答案、`datasets/baselines/`、`datasets/benchmarks/`、`extra/output/`、`extra/output1/`、历史运行结果、论文比较报告、`全过程记录.md`、`论文结果对比与Skills 两轮修改总结.md`、其他分支或重复运行结果、评审答案与裁决记录。
- 不联网检索论文目标或案例答案。
- 调度程序只读取完成状态与技术错误，不把已完成任务的目标内容传给后续任务。

### 上下文隔离

每个任务由**独立的新建生成会话**执行（独立系统上下文、独立工作目录、互不可见）。同一文档的 run01/run02/run03 之间不共享候选、目标、判断、模型或修订内容。

- `context_isolation = isolated_session`：每个任务一个新会话；`shared` 不出现。
- 三个重复仍是同模型、同提示、同参数的**隔离重复**，不据此声明统计独立。
- 本轮执行会话在此前对话中未读取参考答案或历史运行结果；生成会话仅见白名单材料。若某任务实际读到了越界材料，记录在 `logs/deviations.md` 并把该任务标 `contaminated`。

## 3. 主实验

34 篇 × 3 次 = 102 任务，`DOCxxx-runNN`。顺序与种子见 `task-manifest.json`（seed 20261103，交错排列）。

每次重复从原文重新开始，不复用上一轮任何中间产物。

统一任务文本（`brief.md` 第 3 节，`prompt_revision = task-prompt-v1`）：

> 依据分配的完整原文，使用冻结的三个 skills，完成目标提取、证据核验、目标建模、模型检查及交付。保留原文的主体、条件、否定、强度、例外和明确选定的方式。不参考历史答案，不追求特定目标数量、连边数量或精化组数量。

### 生成模型与参数

| 项 | 记录值 |
|---|---|
| 执行平台 | WorkBuddy（产品名） |
| 生成引擎 | WorkBuddy 隔离子代理会话（agent runtime） |
| 精确底层模型标识 | `unknown`（平台未暴露） |
| 温度 | `unknown` |
| token / 费用 | `unknown`（平台未提供逐任务计量） |
| 可观测调用数 | 每次 attempt 的 harness 命令数（记录在 attempt-summary） |

产品名称与底层模型标识分开记录，不互相替代。

### 预算与停止规则（执行前声明）

- 每任务：1 次语义编制主轮 + 至多 2 轮局部修复（对应 relation-discovery 的“最多两轮局部修复”）。
- 停止条件：结构检查通过且覆盖记录 recorded；或 2 轮修复后仍失败（记 failed，保留未决）。
- 无新证据可解决的语义问题不再循环，保留未决状态，继续其他目标。
- 平台会话未提供可设定的 token/时长预算，故 `planned_budget` 记为「1 主轮 + ≤2 修复轮」，token 预算 `unknown`；不声称预算受控。

### 每次运行流程

1. `prepare_source.py --window-size 4 --window-stride 2` 生成 `source.txt`、`source-input.json`、`source-windows.json`（保留说话者、轮次、字符位置）。
2. 逐窗局部捕获候选，保存原始候选（不先压缩为“主要需求”）。
3. 全篇校正指代、条件、例外、相反证据；语义拆合与排除。
4. 保存每个候选去向与理由，运行 `check_coverage.py`（覆盖记录）。
5. 按“一目标一核心动作及其预期结果”整理最终目标（保留状态、维持、避免、改善意图）。
6. 编制语义判断，`trace_candidates.py` 执行证据核验（位置核验不等于语义支持）。
7. 建模：先判断四类独立联系（specialization/operationalization/contribution/precedes），再单独判断 AND 精化组（含 normal/exception 场景检查）。
8. `assemble` → `inspect` → `finalize --svg`，交付 HTML/JSON/MD/MANIFEST/两份 SVG。
9. 生成方自检（model-review 视角）写入 `self-review.md`；独立语义评审、形式证明、人工接受保持 not_run / pending。

窗口是读取组织方式，不等于每窗一次模型调用。

### 阶段保留

| 阶段 | 文件 |
|---|---|
| raw | `raw-candidates.json`（含初始暂定 origin） |
| first_submission | 技能内部核验完成后的首次 `assembled/` + `inspection.json` + 首次 `delivery/` |
| repairs | 修复轮各自 `attempt-0N/`，原因写入 `repair-log.md` |
| delivery | 该任务最后可交付版本的 `delivery/` |

`first_submission` 不是跳过内部核验的粗稿；后续修复不覆盖首次提交。

重试属于同一任务的 attempt，不冒充新的独立重复。

### 失败与入账

工程检查失败、生成中断、源文读取失败、超预算、无法交付都入账；单任务失败不删除任务、不移出总数。`inspection.structure` 的 passed 只来自真实工具输出，不手工修改。

## 4. 辅助实验

| 目录 | 状态 |
|---|---|
| `experiment-inputs/fixed-goals/` | 不存在 → `awaiting_inputs` |
| `experiment-inputs/challenges/` | 不存在 → `awaiting_inputs` |
| `experiment-inputs/external/` | 不存在 → `awaiting_inputs` |

缺失时对应实验标 `awaiting_inputs`，清单见 `missing-inputs.md`。不自行生成挑战题及答案，不执行消融。

## 5. 合成预检

`logs/smoke/`：自造 9 轮合成访谈（非数据集语料），跑通 prepare → 候选 → 覆盖 → 核验 → 建模 → inspect → finalize 全链路，确认工具可调用。不计入 102 次。

## 6. 判定口径（本轮不越界）

本轮不比较新旧效果、不判断论文局限是否缓解、不评优劣。目标数、联系数、组数、工程通过率一律不视为语义质量指标。
