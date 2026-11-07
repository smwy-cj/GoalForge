# 四项 Skill 的输入与输出

四项 Skill 保持独立，可单独调用，也可由同一助手连续完成。用户无需维护机器字段；完整流程默认只提供最终阅读入口与必要问题。

| Skill | 输入 | 机器交接 | 用户看到 |
|---|---|---|---|
| goal-extraction | 原件、范围、目标主体说明 | extraction.json、忠实源文和位置映射 | 单独提取或请求阶段审核时的短目标清单 |
| goal-tracing | 当前目标、源文、实际编制的支持判断 | judgments.json；运行核对时的 tracing.json | 目标旁影响判断的疑点，原文可展开 |
| goal-model-building | 目标、支持判断、精化包与必要反馈 | 模型、精化组、证据、版本及清单 | 有向无环目标图、短说明；模型 JSON 与 SVG 可取出 |
| model-review | 当前模型、实际附件与用户意见 | 检查报告、反馈与受影响对象待办 | 必要问题、意见保存状态与修改说明 |

## 文件职责

- `extraction.json`：只列目标及依据、条件、推断和待确认问题；schema 为 goalforge-extraction-3。
- `judgments.json`：绑定实际目标输入的语义支持判断；schema 为 goalforge-semantic-judgments-1。
- `kaos-decisions.json`：绑定提取与支持包的精化组、假设、关系原句与问题；schema 为 goalforge-kaos-decisions-1。
- `goal-model.json`：可复用机器模型；schema 为 goalforge-kaos-1。
- `inspection.json`：实际执行的检查报告；schema 为 goalforge-kaos-check-1。
- `goal-model.html`、`goal-model.md`：来自同一模型的审核界面与短说明；SVG 按需生成。
- `review-feedback*.json`：用户意见与未完成草稿；schema 为 goalforge-simple-feedback-1。
- `revision-request.json`：真实反馈的处理范围与待办；schema 为 goalforge-kaos-revision-request-1。

文件名可加任务或版本后缀，schema 与绑定值不能凭文件名推断。原始资料、完整附件、模型与意见应保留在交付目录，用户通常只需打开 HTML。

详细字段以各 Skill 的 output-contract.md 为唯一契约入口： [提取](../skills/goal-extraction/references/output-contract.md)、[追溯](../skills/goal-tracing/references/output-contract.md)、[模型](../skills/goal-model-building/references/output-contract.md)、[检查](../skills/model-review/references/output-contract.md)。
