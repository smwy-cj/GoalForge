# Skill 初步修改内容对照

修改日期：2026-10-23。依据：[第13号优化方案](13-Skill结构与内容优化方案.md)。

本轮已修改项目内的 skills：正式入口从四项合并为三项，迁移了实际工具依赖，补齐目标边界、完整支持核验、精化与语义审查规则，并完成工程回归。**这是首轮可运行修改，不是第13号方案全部验收完成；尚未通过同源重新生成证明语义质量提升。**

## 1. 修改基线与适用范围

- 修改依据是任务开始时的工作区文件，不是 Git HEAD。任务开始前 README、docs 等已有未提交或未跟踪内容，本轮保留其既有内容并作局部更新。
- 修改前 skills、tests、README 与 docs 共 60 个文件已另存 [before](../runs/skill-optimization-2026-10-23-initial/before)，哈希与环境见 [baseline.json](../runs/skill-optimization-2026-10-23-initial/baseline.json)。这不是源文、历史 output 和生成环境的完整实验冻结。
- 正式维护源仍是项目 `skills/`。本轮没有同步任何全局/其他 Harness 安装位置；实际应用加载路径需在安装后核对。
- 保持核心 schema：goalforge-extraction-3、goalforge-semantic-judgments-1、goalforge-tracing-draft-1、goalforge-kaos-1 及现有精化、检查、反馈契约。没有静默增加目标分类或附件输入。
- 历史 output 与此前运行目录保留；本轮新材料集中在 [本轮运行目录](../runs/skill-optimization-2026-10-23-initial)。

## 2. 修改前后对照

下表是规则与实现的对照，不能解读为真实资料前后错误率比较。

| 修改项 | 修改前 | 本轮修改后 | 主要文件 |
|---|---|---|---|
| 正式入口 | 提取、追溯、建模、检查四项 | goal-extraction 合并提取与核验，与建模、检查组成三项 | [提取入口](../skills/goal-extraction/SKILL.md) |
| 调用模式 | 提取后转交独立 tracing；仅核验分散在旧 skill | 明确默认提取核验、仅核验、反馈修订、明确只提取四种模式 | 提取入口 |
| 修改权限 | 旧 tracing 只读，合并后如何修订未定义 | 仅核验保持只读；默认/反馈模式由助手另存修订、保留 ID 对应与原因后重核 | 提取入口、[核验契约](../skills/goal-extraction/references/tracing-contract.md) |
| 目标资格 | 简述动作、偏好、规则、困难作为依据/条件/问题 | 按语义成分判断，不因有偏好、困难或已实现状态就排除目标；补维持、避免与改善意图 | [goal-boundaries.md](../skills/goal-extraction/references/goal-boundaries.md) |
| 强度与来源 | 有 explicit/inferred 和支持标签，但跨越风险说明较少 | 分开判断意图来源、支持、语气、采纳、优先与满足标准；禁止偏好变必须、习惯变默认、信念变事实 | 边界规则、[证据口径](../skills/goal-extraction/references/evidence-rules.md) |
| 复合目标 | 支持细节可记录，但部分支持仍可能声明 direct/inferred | 逐项核验；未支持部分需修订或保留不足。工具将含 unsupported_parts 的正向声明降为 insufficient，保留原声明 | [trace_candidates.py](../skills/goal-extraction/scripts/trace_candidates.py) |
| 上下文与例外 | 核验指定证据及必要上下文 | 明确检查问题、回答、后续解释、例外以及标题/context 一致性；准确位置不等于整句支持 | 证据口径 |
| 建模权限 | 目标组织、精化和反馈规则已有，但回退边界不够集中 | 新增、拆合或实质改写目标须回到提取核验；当前 candidate_id 直接沿用为 goal_id | [建模入口](../skills/goal-model-building/SKILL.md)、[建模规则](../skills/goal-model-building/references/modeling-rules.md) |
| 精化与场景 | AND 共同充分、多个完整组表示 OR，允许多根共享 | 增加 Why/How、整组核验、正常/异常场景与反例检查；构造场景须标分析假设 | 建模规则 |
| 辅助关系 | 障碍仅简述挂到问题 | 明确偏好、障碍、贡献、冲突、操作化和责任的边界；不混进精化边，无法承接时记限制 | 建模规则 |
| 语义复核 | 泛指忠实性、充分性、条件与主体 | 分成语义偏差、来源推断、表达不足、候选遗漏风险、精化问题、正确/边界案例；优先全部精化组及争议项 | [semantic-review.md](../skills/model-review/references/semantic-review.md) |
| 证据层次 | 已区分程序、独立审查、形式证明和人工决定 | 补充分阶段自检、后验复核与独立性边界；未执行保持 not_run，不将候选遗漏风险计真实漏提 | 语义复核规则 |
| 空目标核验 | 合法空目标清单被 trace 标为 input_error | 空 traces 可正常完成，不虚构目标 | 核验脚本、迁移测试 |
| 工具依赖 | kaos_model、reconcile 等导入 goal-tracing | 导入唯一的 goal-extraction 实现；旧反馈规划及修订回跳改为合并入口 | 建模/审核脚本 |
| 旧路径兼容 | 旧目录有完整入口与实现 | 旧脚本仅转接，旧参考文档仅导航；原 SKILL.md 归入本轮 before，旧目录不再有正式入口 | [兼容脚本](../skills/goal-tracing/scripts/trace_candidates.py) |
| 使用说明 | README 与安装/操作文档按四项描述 | 同步三项安装、合并模式、核验路径及兼容说明 | README、docs/05、07、10 |

## 3. 文件迁移与维护位置

| 原位置 | 当前权威位置 | 旧位置状态 |
|---|---|---|
| goal-tracing/scripts/trace_candidates.py | goal-extraction/scripts/trace_candidates.py | 兼容 CLI 与公开 Python 函数导入，调用唯一实现 |
| goal-tracing/references/evidence-rules.md | goal-extraction/references/evidence-rules.md | 只保留导航 |
| goal-tracing/references/semantic-judgments.md | goal-extraction/references/semantic-judgments.md | 只保留导航 |
| goal-tracing/references/output-contract.md | goal-extraction/references/tracing-contract.md | 只保留导航，避免覆盖提取契约 |
| goal-tracing/SKILL.md | 合并到 goal-extraction/SKILL.md | 原件保存在 before，不再参与项目 skills 发现 |

新增两个正式参考文件：goal-extraction/references/goal-boundaries.md 与 model-review/references/semantic-review.md。前者统一内容资格，后者定义复核视角；建模与审核引用共同规则，不复制整套定义。

调用者迁移包括 kaos_model.py、reconcile_model.py、revise_model.py、process_feedback.py 和原追溯测试。旧输出文件名 `goal-tracing-review.md` 与既有 schema 名保留，避免无必要的格式迁移。

正式安装只复制 goal-extraction、goal-model-building、model-review 三个完整同级目录。项目内旧命令需与新的 goal-extraction 同级；转接目标缺失时明确报错，不回调旧实现。

完整逐文件清单及前后 SHA-256 见 [changed-files.json](../runs/skill-optimization-2026-10-23-initial/changed-files.json)，文本行级差异见 [changes.diff](../runs/skill-optimization-2026-10-23-initial/changes.diff)。

## 4. 已执行验证及其边界

实际结果见 [verification.json](../runs/skill-optimization-2026-10-23-initial/verification.json)。

| 检查 | 结果 | 能证明的范围 |
|---|---|---|
| 修改前 Python 基线 | 88/88 通过 | 修改前已有工具测试通过 |
| 修改后 Python 全集 | 94/94 通过，新增 6 项迁移/行为测试 | 既有流程及本轮确定性行为未发现工程回归 |
| JavaScript | 11/11 通过 | 原有审核数据处理测试通过；本轮未改 UI 资源 |
| 三项 skill 结构校验 | 3/3 通过 | frontmatter、命名与入口基本合法，不代表语义质量通过 |
| 三项隔离安装 | 通过 | 无旧目录时，可运行模板、核验、构建、检查、交付、部分反馈和待审副本重建 |
| 旧命令/导入兼容 | 通过 | 新旧核验结果一致、模板一致、输入不改；缺目标明确失败 |
| 部分支持保护 | 通过 | direct/inferred 带未支持部分时降为不足，原提交判断保留，不能作为成立精化前提；其他目标可继续 |
| 绑定与未决问题 | 通过 | 条件变化即使标题不变也使旧支持失效；反馈重建保留未解决问题并保持 pending |

原结构校验器在 Windows 默认 GBK 下读取中文失败，改用 `python -X utf8` 后三项通过；没有修改系统校验器或全局编码配置。

四种模式的验证状态需分别理解：

| 模式 | 本轮实际完成 | 尚未完成 |
|---|---|---|
| 默认提取与核验 | 入口/职责已定义；预先编制的合成目标与支持包可跑通交付 | 未由新版 skill 对真实源文重新提取并评审 |
| 仅核验 | 新旧 CLI 及导入均实测不修改输入，保存支持范围与缺口 | 模型是否总能作出正确语义判断尚待实测 |
| 反馈修订 | 修订回跳、输入失效、反馈范围及未决项保留已实测 | 合成重建没有实际改写句义；真实反馈驱动的语义修复尚待实测 |
| 明确只提取 | 规则要求不运行核验、不标已支持 | 尚未开展真实对话模式验收；脚本本身不负责自动提取 |

可复查的隔离安装结果见 [isolated-install-result.json](../runs/skill-optimization-2026-10-23-initial/isolated-install-result.json)，其中包含安装副本、合成输入、判断、交付和反馈重建文件。这里的“用户反馈”是工程测试数据，不能当真实用户验收。

内容边界另列了 [10 个合成开发回归案例](../runs/skill-optimization-2026-10-23-initial/semantic-regression-plan.md)，状态均为 not_run。不能用规则已写入、脚本已通过或目标数变化宣称语义准确率提高。独立语义审查、形式证明、人工决定均未执行。

## 5. 与原方案阶段的对应及后续工作

| 阶段 | 本轮状态 | 剩余工作 |
|---|---|---|
| A 冻结与基线 | 部分完成 | 已备份技能/相关文档/测试及环境；真实源文、历史产物、生成模型/参数/预算仍需实验冻结 |
| B 结构合并 | 工程迁移完成，模式验收未全部完成 | 三项隔离流程和旧兼容已通过；四种模式尚需真实语义行为验收 |
| C 语义边界修订 | 规则完成，确定性保护已实现 | 合成边界与真实开发案例须实际生成复核，不能提前判“已知问题不再出现” |
| D 跨阶段保留 | 未实现独立附件 | 先定义 semantic-context 唯一版本契约，再整体实现读写、源文/目标绑定、映射、依赖失效、展示和反馈传播 |
| E 精化与场景 | 规则完成，未验证效果 | 在稳定且受支持的输入上生成候选组、检查反例、评估整组充分性与辅助关系 |
| F 同源比较与发布记录 | 本地首轮版本记录完成；比较未执行 | 固定同源资料与口径，在新目录运行原四项、仅结构合并、内容优化三组；记录成本、退化与未决项 |

保留的实现限制：

1. 当前没有 semantic-context.json；关键条件仍在目标/conditions，其他信息由现有推断、依据、问题承接。无法无损表达时只能声明限制，不能冒充完整附件支持。
2. 核心 issues 尚无稳定问题 ID、分类与完整状态生命周期。本轮要求在可读语义复核记录中保存稳定标识，并把关键未决项同步到现有问题结构；尚未实现自动结构化传播。
3. 当前 inspection.readiness 仍对任一 blocking 问题汇总为 blocked；语义报告须说明具体受影响对象，不能据此断言整篇无效。没有改变既有检查契约绕过阻塞。
4. 新实现会将旧包中“正向支持且仍列未支持部分”的情况降级；这类旧模型需要重核、重建检查，不能只重填哈希复用旧通过状态。历史输出不被批量改写。
5. 本轮没有全量重生成 34 篇，也没有受控测量 token、成本、准确率或精化质量变化。未知历史生成信息继续为 unknown。

建议下一轮先完成 D 的契约与完整链路，再用 DOC010、DOC023、DOC031 等已接触开发资料和其他长度/复杂度资料作同源生成与语义复核；已接触案例不能当作未见测试。只有实际结果支持后，才报告优化效果或扩大应用范围。
