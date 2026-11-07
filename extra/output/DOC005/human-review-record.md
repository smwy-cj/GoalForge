# 人工审核记录：目标候选（提取阶段）

- 日期：2026-10-18 12:21
- 审核对象：output/DOC005/goal-candidates.md（与 extraction.json 同源生成），共 20 个候选与 7 个待确认问题
- 审核人：用户（对话中明确指示）
- 决定：**全部保留，无修改意见；以当前候选版本继续后续阶段（证据追溯、关系判断、模型组装与结构检查）。**

## 说明

- 7 个待确认问题（含 T005「a fool」疑为「a four」、T033 比例矛盾等）均按「保留现状」处理，未对任何候选做改写、合并或排除。
- 依据「先记录人工意见、再同步结构化数据」的契约要求，本记录独立存放；extraction.json 保持原样未改写，以维持追溯阶段的版本绑定哈希链完整。
- 本记录仅表示**提取阶段**的人工决定。目标模型层面的人工审核状态仍为 pending，需通过最终交付的审核界面（goal-model.html）或用户后续明确指示完成，不由本记录自动升级。

---

# 后续阶段执行记录（追溯 / 建模 / 检查）

- 日期：2026-10-18 13:30
- 执行者：助手（按用户「由你依据原文编制当前版本的语义判断并维护中间文件」的指示）
- 人工状态：**保持 pending**。以下均为程序判断与助手编制的判断，未经人工确认，不构成人工采纳。

## goal-tracing

- 版本绑定：`semantic-judgments.json` 由 `tracing/judgment-template.json` 填充生成，绑定当前 extraction 的 `data_sha256` 与 `input_sha256`。
- 8 个目标全部完成语义判断：7 项 direct、1 项 inferred（G015 个性化命中率，依据 S086 的 3/20 与 10-12/20 对比推断）。
- 25 条证据全部 `location_status=exact`、`verification_scope=full_text`，无 not_found、无 version_mismatch。
- 每项判断均记录 supported_parts / unsupported_parts / assumptions / reasoning_steps；不支持部分如实保留（例：G001「始终」强于原文「almost all the time, but not every moment」）。

## goal-model-building

- 规范化：未做合并/拆分/排除，8 个候选 1:1 保留为 G001/G005/G006/G010/G015/G016/G017/G018；12 个非目标候选留在 diagnostics。
- 关系：首版全枚举 8×(8−1)/2 = 28 个无序对，全部已评估（assessment_status=assessed）：18 条 related、10 条 none；无 refinement、无 equivalent、无 uncertain。
- **当前版本没有精化边**，因此图中有多个独立根，属如实结果，非为形成树状结构补造。HTML 已提示该情形，Markdown 未单列此说明（导出工具行为，记录为已知限制）。
- 无 blocking 问题，readiness=unchecked 交检查阶段。

## model-review 与 finalize

- 结构检查：structure_status=passed、semantic_status=not_run、blocking=0、needs_review=0（报告：final/attachments/review-report.json）。
- finalize 后 readiness=reviewable、review.status=pending、version=v0.1、core 哈希 goalforge-core-v1。
- 四份产物同源于同一模型对象；HTML 无外部依赖（无 fetch、无 CDN），SVG 含版本/状态/线型图例与全部 8 个目标。

## 限制

- 语义判断由本次会话助手编制，非独立盲测；独立语义审查（semantic_status=not_run）未执行。
- G015 的 3/20 与 10-12/20 为受访者自述估计值；S034 的 15%/15% 与「the other 50%」不自洽，均已在判断与目标情境中标注，未做静默修正。
- 文档来源仅为 DOC005 一份，未跨材料归并。

---

# 人工审核采纳记录（模型阶段）

- 日期：2026-10-18 13:56
- 审核对象：DOC005-goal-model v0.1（`final/goal-model.json`，content_sha256 `d5217313e7e4ac6c16c97fe484487b5495471a6f6b08371cfd85f29aa9a63ac0`）
- 审核人：用户（对话确认，身份为自填、未经认证）
- 结论：**全部认可，无修改**
  - 8 个目标：accept
  - 28 条关系判断（18 related / 10 none）：accept
  - 25 条证据：sufficient
  - 整体：accept，`full_scope_ack=true`、`acknowledge_limits=true`

## 反馈来源与性质（须明确）

- 用户未导出浏览器审核文件，`review-feedback.json` 由助手依据对话中「已人工审核完毕，请继续工作」及选项中选定的「全部认可，无修改」**转录**生成，不是浏览器导出产物。
- 转录事实以 `attachments/human-feedback-887cd0e0d6b30fd0.json` 内的 model 级 comment 条目显式记录，接收方可核查该条来源说明。
- 反馈包哈希 `887cd0e0…ad91e1`；`review_target_sha256=4b923d76…e527d9`（goalforge-review-target-v1），与采纳记录一致。

## 采纳绑定

- feedback_id：`DOC005-FB-20261018-01`；status=submitted；entries 62 条（61 条认可/充分 + 1 条来源说明）。
- 应用后：`review.status=accepted`、`delivery.readiness=accepted`、结构检查 passed、semantic_status=not_run。
- 采纳只影响 review 派生字段；目标、关系、证据与版本均未改动（`modified=false`）。

## 一处已修正的交付矛盾

- 首次 finalize 生成的限制清单含「…无人工采纳记录。」，与 accepted 状态冲突，且同一句被重复追加（因该轮输入本身是已 finalize 的模型）。
- 处理方式：从输入侧改正限制文本后重走 inspect → apply → finalize，未手改任何交付文件；旧目录已删除。
- 结果：限制清单为 2 条，无矛盾、无重复；manifest 全部哈希校验通过，`approval_valid=true`。
