# 目标提取契约

schema_version 为 `goalforge-extraction-3`。candidates 每项即一个目标。机器字段由助手维护，用户阅读短清单或最终模型。

## 顶层

| 字段 | 约束 |
|---|---|
| document_id / document_hash | 稳定资料 ID；标准全文 UTF-8 实际 SHA-256 |
| status | completed / partial / input_error；不表示人工认可或需求穷尽 |
| materials | material_id、file_name、media_type、original_hash、id_origin、processing_status |
| conversion | canonical_text_path、method、issues（字符串数组） |
| segments | source_id、material_id、text、speaker、original_locator、recognition_status |
| coverage | scope、source_ids、omissions；记录实际范围 |
| candidates | 目标数组，允许空集合 |
| review_questions | candidate_ids、question、reason；空 ID 数组表示整体问题 |
| limitations | 影响读取或判断的实际限制 |

材料 ID、片段 ID 与目标 ID 各自唯一，引用有效。speaker、未知原件哈希可为 null。id_origin 为 provided/generated；处理状态 processed/partial/unprocessed；范围 full_document/provided_material/partial_document。input_error 时不带虚构目标、片段或已处理范围。

## 目标

candidate_id、statement、origin（explicit/inferred）、actor（未知 null）、context（必要条件数组）、evidence_candidates、inference、review_status（pending）。保持稳定 ID、简短完整含义；不加入专业分类字段。

每条 evidence_candidates 含 source_id、quote、role（basis/context）、start_char/end_char。至少一条 basis，quote 在实际片段中存在。偏移为标准全文 Unicode 码点半开区间，未知同为 null。位置匹配不能证明语义支持或识别正确。

推断的 inference 含 basis_candidate_ids、reason、assumptions；引用存在，理由非空。明确表达时 inference 为 null。必要的动作、困难或规则留在源文并通过条件、上下文或问题引用，不逐项增加诊断候选。

## 交付

extraction.json、忠实源文与位置映射供后续读取。单独提取或请求阶段审核时生成 goal-candidates.md：资料名、目标列表、必要问题与统一意见区；原文依据可按需展开。已有文件拒绝覆盖。
