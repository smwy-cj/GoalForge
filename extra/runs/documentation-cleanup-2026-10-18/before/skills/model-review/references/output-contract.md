# 审查与修复输出契约

工具和工程测试已实现；独立语义审查与真实人工采纳仍未执行。报告使用 goalforge-core-v1：保留全部模型顶层字段，仅排除 content_sha256、delivery、validation；因此目标、关系、证据、输入附件哈希、版本、变更和真实人工记录的变化都会使旧报告失效。JSON 按键排序、UTF-8、无额外空格规范序列化，不允许 NaN，再计算 SHA-256。文件实际哈希另存 file_sha256，不与核心哈希混用。

## 审查报告

review-report.json 顶层：schema_version=model-review-draft-1、report_id、mode、input_model（文件实际哈希、model_id、version、core_sha256、哈希规则版本）、checks、issues、summary、repair_attempts、unresolved_issue_ids、limitations、review_status。

每条 check 包含 check_id、type（deterministic/semantic）、scope、status（passed/failed/not_run/needs_review）、依据及执行方式。summary 分开记录结构状态、语义状态与实际覆盖，不把 semantic=reviewed_no_findings 写成正确性保证。

每条 issue 包含 issue_id、rule_id、type、severity、target_ids、evidence_ids、reason、suggested_action、status。status 区分 open、proposed、resolved、needs_review、not_resolved；resolved 需要对应复检依据。

人工审核状态默认为 pending。真实人工意见可以另行登记审核人、目标版本和决定，不能由程序生成假的采纳记录。

report.review_status表示检查报告自身是否获人工确认；model_human_review_status另表示被检查模型的人工状态，避免已导入真实认可后报告仍把模型写成pending。两者均不替代semantic_status。

## 补丁与版本

patches.json 每项含 patch_id、issue_ids、base_version、base_core_sha256、operations、rationale、expected_checks、application_status。

operation 用 entity、id、field 定位，action 固定 replace，before/after 为精确前置条件及新值。白名单见 [工具约定](tools.md)。原件、源文正文、历史运行、ID 和人工确认记录不在补丁可写范围内。

修复记录包含 attempt_id、patch_ids、before/after 版本及核心哈希、实际变化、复检报告、原问题状态、新问题、回滚结果、实际调用/耗时/用量与停止原因。未执行的字段为 null 或 not_run，不填成功默认值。

当前实现将原操作保存在模型 changes 中，将尝试状态、前后版本/哈希、resolved_issue_ids、new_issue_ids、停止原因及耗时保存在 repair_attempts 中；复检报告就是该次输出的 review-report.json。失败尝试不生成 repaired-model.json。model_calls=0，token_usage=null，不能误解为语义审查零成本。

repaired-model.json 使用目标模型契约，生成新 version 和 parent_version；内容哈希变化时重新计算证据/检查的有效范围。无法完成语义复核时保留问题和 pending 状态，不升级 accepted。

## 人工文档

model-review.md 用中文列出检查范围、实际检查项、问题清单及来源、修改前后对照、复检结果、未解决项和限制。每项保留人工决定、修改建议、审核意见空栏。报告版本与权威 JSON 一致；没有实际补丁时不虚构修复模型。

## 人工反馈处理

review-feedback.json使用独立[反馈契约](human-feedback.md)。默认输出feedback-processing.json与feedback-processing.md，含每项意见的接收状态、处理去向与限制；--apply时输出feedback-model.json、反馈/原文附件、当前版本复检JSON和MD。review-tasks.json列出需重新判断的目标和关系；具备标准全文与片段映射时另生成retrace-input.json，保留goal_id与目标模型版本/核心哈希，供goal-tracing读取。缺少片段映射时明确source_segments_unavailable。

改写、增删、合并、拆分由goal-model-building.revise处理，不突破局部补丁脚本的字段白名单。原模型和旧反馈不覆盖；意见未应用、已应用待追溯、待人工决定分别记录。独立语义判断仍需由助手/可用模型依据原件完成，工具不默认通过。
