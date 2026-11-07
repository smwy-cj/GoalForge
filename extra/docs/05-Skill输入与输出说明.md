# 三项 Skill 的输入与输出

三项正式 Skill 保持同级，可按任务调用，也可由同一助手连续完成。goal-extraction 已合并提取与证据核验；阶段记录与原契约仍分别保留。用户无需维护机器字段，完整流程默认只提供最终阅读入口与必要问题。

| Skill | 输入 | 机器交接 | 用户看到 |
|---|---|---|---|
| goal-extraction | 原件、范围、主体；或已有目标与源文；或修订任务/真实反馈 | extraction.json、忠实源文与窗口；候选及覆盖记录；judgments.json、tracing.json | 一目标一核心动作的清单、影响判断的疑点，依据按需展开 |
| goal-model-building | 目标、支持判断、联系/精化判断包与必要反馈 | 模型、独立联系、精化组、证据、版本及清单 | 有向无环目标图、目标联系、短说明；模型 JSON 与独立 SVG 可取出 |
| model-review | 当前模型、实际附件与用户意见 | 检查报告、反馈与受影响对象待办 | 必要问题、意见保存状态与修改说明 |

## 文件职责

- `extraction.json`：只列目标及依据、条件、推断和待确认问题；schema 为 goalforge-extraction-3。
- `judgments.json`：绑定实际目标输入的语义支持判断；schema 为 goalforge-semantic-judgments-1。
- `tracing.json`：只读核验的定位与完整语义支持结果；schema 为 goalforge-tracing-draft-1。
- `source-windows.json`、`raw-candidates.json`、`extraction-ledger.json`：分窗、原始候选及每项最终去向，见[覆盖契约](../skills/goal-extraction/references/coverage-contract.md)；不替代语义支持判断。
- `kaos-decisions.json`：绑定提取与支持包的联系、精化组、场景、假设、原句与问题；新任务 schema 为 goalforge-kaos-decisions-2。
- `goal-model.json`：可复用机器模型，区分独立联系与成立精化；新任务 schema 为 goalforge-kaos-2。
- `inspection.json`：实际执行的检查报告；新任务 schema 为 goalforge-kaos-check-2。
- `goal-model.html`、`goal-model.md`：来自同一模型的审核界面与短说明；SVG 按需生成。
- `review-feedback*.json`：用户对目标、联系或组的意见与未完成草稿；新任务 schema 为 goalforge-simple-feedback-2。
- `revision-request.json`：真实反馈的处理范围与待办；新任务 schema 为 goalforge-kaos-revision-request-2，含受影响联系及组。

历史v1模型及对应判断/反馈/检查继续兼容；不自动升级或混用反馈。明确迁移步骤见[建模工具](../skills/goal-model-building/references/tools.md)。SVG分别导出成立精化图goal-model.svg和目标联系goal-relations.svg。

文件名可加任务或版本后缀，schema 与绑定值不能凭文件名推断。原始资料、完整附件、模型与意见应保留在交付目录，用户通常只需打开 HTML。

详细字段以唯一契约入口为准：[提取](../skills/goal-extraction/references/output-contract.md)、[证据核验](../skills/goal-extraction/references/tracing-contract.md)、[模型](../skills/goal-model-building/references/output-contract.md)、[检查](../skills/model-review/references/output-contract.md)。

goal-extraction 支持默认提取与核验、仅核验、反馈修订、明确只提取四种模式。仅核验不改目标；只提取时核验为 not_run；修订另存新版并重核。旧 goal-tracing 不再作为正式发现入口，旧脚本路径仅转接唯一实现。

本轮未实现 semantic-context.json；必要关联信息使用现有条件、推断、依据和问题承接，不能无损表达的部分列限制，不宣称独立附件已受绑定或展示。
