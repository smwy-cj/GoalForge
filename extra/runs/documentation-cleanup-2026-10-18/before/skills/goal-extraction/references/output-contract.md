# 双输出契约 draft 2

> 旧数据兼容规范。新版默认见 [简明目标契约](simple-output.md)。

每份资料交付 extraction.json 和默认 goal-candidates.md，附实际使用的 source.md/txt。批量放在各自 document_id 子目录中。用户指定其他格式且工具可用时替换 Markdown，JSON 不省略。

## JSON 顶层

| 字段 | 约束 |
|---|---|
| schema_version | 固定 goalforge-extraction-draft-2；与 draft-1 不兼容，不覆盖旧产物 |
| document_id | 保留输入 ID，或自动分配的内部 ID |
| document_hash | 转换稿 SHA-256；未实际计算时 null |
| status | completed / partial / input_error |
| materials | 原始材料数组 |
| conversion | 对象：canonical_text_path、method、issues；issues 为含位置与原因的字符串数组 |
| segments | 转换稿片段数组 |
| coverage | scope 为 full_document / provided_material / partial_document；source_ids 为已处理片段；omissions 为遗漏说明数组 |
| candidates | 候选数组 |
| review_questions | 数组，每项含 candidate_ids、question、reason；全局问题允许空 ID 数组 |
| limitations | 字符串数组，记录实际能力和覆盖限制 |

completed 表示已完成所提供可读材料的处理，不代表需求穷尽或人工审核完成。有遗漏材料或关键识别失败时为 partial；全部不可读为 input_error，此时 candidates、segments、source_ids 为空。

材料项字段：material_id、file_name、media_type、original_hash（可为 null）、id_origin（provided/generated）、processing_status（processed/partial/unprocessed）。粘贴文本使用可识别的输入名称。

片段字段：source_id、material_id、text、speaker（可为 null）、original_locator（实际定位字段组成的对象）、recognition_status。source_id 唯一，material_id 必须存在；不编造未知身份或位置。

## 候选项

| 字段 | 约束 |
|---|---|
| candidate_id | 文档内唯一，如 DOC001-C001；按首次证据顺序分配，修订保留，新增追加 |
| category | goal / action / obstacle / preference / uncertain |
| subtype | classification.md 中的子类，或 unspecified |
| statement | 非空中文表述 |
| origin | goal 为 explicit/inferred，其他为 null |
| actor | 源文支持的主体，否则 null |
| context | 条件、时间、范围等字符串数组 |
| evidence_candidates | 每项含 source_id、quote、role（basis/context）、start_char/end_char（整数或 null） |
| classification_reason | 分类和粒度判断理由 |
| inference | inferred 时含 basis_candidate_ids、reason、assumptions；其他为 null |
| review_status | 默认 pending；仅真实用户审核后改变，变更记录另存 |

目标至少有一条 basis 证据；quote 必须能在其 segment.text 中找到。识别稿文字匹配不证明原件识别准确。偏移同时为 null，或为工具核验的标准全文半开区间。跨片段证据分开，不能拼成单一引文。

inference.basis_candidate_ids 仅引用当前候选；无独立诊断项时可为空，但必须有证据、reason 与 assumptions。设计扩展不属于本契约的提取候选。

## Markdown 人工审核文档

用非技术表述呈现：

1. 材料名称、处理范围、转换说明、来源附件和识别风险。
2. 目标概览：编号、表述、类型、显式/推断、待审核状态。
3. 按编号逐项列出所有候选：类别、子类、主体、条件、原文证据及原件位置、分类理由、推断理由与假设；非目标注明用于诊断。
4. 每项留“人工决定”“修改后表述”“审核意见”空栏。可提示保留、修改、排除、暂缓，不能代填。
5. 待确认问题及遗漏/限制。空目标集合或读取失败也交付说明。

用户无需阅读 JSON 或填写内部索引。不得只交目标摘要而隐藏诊断项或假设。两种输出使用相同 ID 与语义内容；人工改写同步前保存审核记录，不能以渲染文档推断已获确认。

默认文档生成方式：`python scripts/render_review.py <extraction.json> <goal-candidates.md>`。

输出路径须是新文件。工具独占创建，已存在则拒绝并保留原内容；要生成修订文档应使用新版本路径，不能覆盖已填人工意见。

脚本对坏引用和缺少依据执行基础检查，不是完整 Schema 验证器或语义评测器。其他格式保持相同信息和意见栏。
