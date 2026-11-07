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

最终 candidates 默认每项表达一个核心动作及其预期结果；状态、维持、避免及质量意图按[目标边界](goal-boundaries.md)保留。多个独立动作整理为不同 candidate_id，条件与明确方式仍写入 statement/context；不新增 action、atomicity 等未定义字段。粒度是助手的语义判断，现有格式校验通过不证明“一目标一核心动作”已满足。

每条 evidence_candidates 含 source_id、quote、role（basis/context）、start_char/end_char。至少一条 basis，quote 在实际片段中存在。偏移为标准全文 Unicode 码点半开区间，未知同为 null。位置匹配不能证明语义支持或识别正确。

推断的 inference 含 basis_candidate_ids、reason、assumptions；引用存在，理由非空。明确表达时 inference 为 null。必要的动作、困难、偏好、信念、现状或策略通过原文、条件、推断或问题保留；它们也可能同时支持目标，按[目标边界](goal-boundaries.md)判断，不逐项增加诊断候选。

origin 与支持标签分别判断，不自动互相覆盖。建议强度、例外及选定方式影响目标含义时保留在 statement/context，不能仅藏在备注。修订另存输入原件、新版与 ID 对应和原因，随后为新版重建支持包；仅核验模式不改目标。不得静默添加 kind、hard/soft、mandatory 等分类字段。

本轮仍用原契约，不定义或消费 semantic-context.json；当前字段不能无损承接的信息须说明限制。后续若实现关联附件，先定义唯一契约及绑定、验证和展示，不能自行添加未绑定的跨阶段语义输入。

新提取另存[候选与覆盖记录](coverage-contract.md)，审计源文、候选处置及最终目标的哈希绑定。它不增加本契约字段，也不替代支持包；当前模型工具不消费该审计附件。模型生成前的目标核验仍以本文件及当前判断包为准。旧结果不要求补造历史记录。

## 交付

extraction.json、忠实源文与位置映射供后续读取。默认继续按[判断规范](semantic-judgments.md)核验，结果见[核验契约](tracing-contract.md)。明确只提取时标明核验 not_run，不能把候选当已支持。单独提取或请求阶段审核时生成 goal-candidates.md：资料名、目标列表、必要问题与统一意见区；原文依据可按需展开。已有文件拒绝覆盖。
