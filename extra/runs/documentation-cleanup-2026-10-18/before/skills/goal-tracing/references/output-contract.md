# 追溯输出契约初版

> 新版 v3 默认只交接机器结果，人工报告按需。判断绑定机制保持不变；旧输入沿用下文报告行为。

初版已获用户“暂无修改建议”的反馈，现进入实现与测试。定位工具只负责确定性核验；语义支持由独立保存的模型/人工判断提供，不能按匹配结果自动生成 direct。

## 顶层

- schema_version：goalforge-tracing-draft-1。
- input_artifact：输入目标文件路径、实际可计算哈希和模型版本；未知项为 null。
- sources：本次允许的来源、原件/转换稿路径、预期与实际哈希、availability、识别状态及实际处理范围。
- status：completed / partial / input_error。completed 表示追溯流程完成，不表示每项目标均受支持。
- traces：按输入顺序的逐项目标结果。
- review_questions：关联目标 ID、问题与理由。
- limitations：无法读取、版本问题及其他限制。

当前输出另有semantic_binding：记录版本绑定判断契约、完整输入绑定和判断包规范哈希；CLI的input_artifact与judgment_artifact保存实际文件哈希。target_model在修订回流时保留模型ID、版本和核心哈希。新判断输入契约及空模板见[版本绑定说明](semantic-judgments.md)。旧追溯产物可保留查看，新组装的正向支持不能省略当前绑定。

至少包含目标 ID 和目标表述才可建立追溯条目。没有目标 ID 时系统生成并映射，不要求用户填写；连目标都没有时为 input_error。只有目标没有源文仍保留所有目标，status=partial，各条目标明 source_unavailable。

## 每项目标结果

| 字段 | 内容 |
|---|---|
| target_id、target_kind、statement | 保留输入 candidate/goal 的 ID 与表述；target_kind 为 candidate/goal |
| document_id | 关联原文文档；未知时 null |
| submitted_evidence | 原提交证据及各自定位结果，不覆盖原数据 |
| located_evidence | 本轮新定位或补充证据、变化原因 |
| search_scope | 实际查找的来源、片段及遗漏范围 |
| support | label 为 direct/inferred/insufficient/contradicted；rationale、supported_parts、unsupported_parts、assumptions、reasoning_steps |
| issues | 如 source_unavailable、version_mismatch、recognition_risk、origin_mismatch、context_conflict，附依据和定位 |
| suggested_changes | 仅建议，含目标定位、建议内容、理由；没有则空数组 |
| review_status | 默认 pending，不继承为新的人工确认 |

## 每条证据结果

- evidence_id：本条结果内稳定唯一。
- source_id、material_id、quote：源片段及原文引文；来源无法识别时 ID 可为 null，不能补造。
- evidence_role：supporting / opposing / context；只表示其对目标的作用，不代表支持充分。
- location_status：exact / ambiguous / not_found / source_unavailable。
- verification_scope：full_text / segment / none。
- start_char、end_char：已核验的全文半开区间；未知或非唯一时均为 null。
- candidate_locations：歧义时的实际候选位置数组，禁止从中擅自选一项。
- original_locator：实际可确定的页码/段落/幻灯片/时间段等。
- recognition_status：沿用真实识别状态，不自动记为 human_verified。
- source_version_status：verified / unverified / version_mismatch。
- location_reason：匹配、失败或更换的依据。

版本问题与定位失败分开表达；version_mismatch 下不能把旧位置标为 verified。只有实际核验且唯一的全文切片才能同时具有 exact、full_text 和非空偏移。未进行语义判断的证据不能单凭 exact 推导 direct。

## 人工文档

goal-tracing-review.md 默认中文，先说明范围和限制，再列每个目标及支持结论。逐条呈现原提交/本轮新增引文、真实来源位置、定位与识别状态、支持理由、推断假设或不足、相反证据、建议变化。

每项目标保留“人工决定”“修改意见”“审核备注”空栏。JSON 与文档使用相同 ID 与判断；用户另选文件格式时保留全部信息和 JSON，不把未匹配或未支持的目标从文档移除。
