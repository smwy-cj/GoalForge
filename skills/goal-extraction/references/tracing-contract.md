# 证据核对输出契约

输入为目标提取契约和实际标准全文，支持判断按[判断规范](semantic-judgments.md)编制。输出 `tracing.json`；人工报告用 --review-md 按需生成，不默认推送。

## 机器结果

实际 schema_version 为 goalforge-tracing-draft-1。input_artifact 保存实际输入路径、哈希和契约标识，judgment_artifact 保存判断文件哈希；semantic_binding 保存输入绑定与判断包规范哈希。sources 记录 document_id、预期与实际哈希、可取得性。

status 为 completed/partial/input_error；流程完成不等于所有目标受支持。traces 按输入顺序保存目标，limitations 记录实际检查范围。target_model 存在时沿用实际绑定。

每条 trace：target_id、target_kind、statement、document_id、submitted_evidence、located_evidence、search_scope、support、submitted_semantic_judgment、issues、suggested_changes、review_status。

support 含 label（direct/inferred/insufficient/contradicted）、rationale、supported_parts、unsupported_parts、assumptions、reasoning_steps。缺判断时记录 semantic_not_run，不能把不足标签解释为已经证明原文不支持。

## 定位依据

证据含 evidence_id、source_id、material_id、quote、evidence_role、location_status、verification_scope、start_char/end_char、candidate_locations、original_locator、recognition_status、source_version_status、location_reason。

- location_status：exact/ambiguous/not_found/source_unavailable。
- verification_scope：full_text/segment/none；全文准确位置必须经实际切片核验。
- source_version_status：verified/unverified/version_mismatch；来源变化需重新定位。
- recognition_status 来自实际识别过程，不由位置命中升级为 human_verified。

返回影响目标含义的短问题，不改目标、不新增目标、不判定精化。direct/inferred 同时声明非空 unsupported_parts 时，有效 support 为 insufficient，原声明保存在 submitted_semantic_judgment，增加 partial_support 问题；该项不进入成立精化前提。相关判断边界见[证据口径](evidence-rules.md)。

本契约描述只读核验产物；合并入口的默认/反馈修订模式可另存新版目标后再运行核验。核验输入原件、旧结果与新结果均保留。仅提取模式没有运行核验时，不伪造 tracing 已完成状态。没有目标时允许 completed 与空 traces，不将合法空目标输入误报 input_error。
