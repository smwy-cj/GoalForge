# 简明目标契约 v3

默认 `schema_version: goalforge-extraction-3`。`candidates` 数组只放目标，不含 category、subtype、classification_reason；每个元素均为目标。

顶层继续包含 document_id、document_hash（UTF-8 标准全文实际 SHA-256）、status、materials、conversion、segments、coverage、candidates、review_questions、limitations。资料索引和位置定义沿用[旧契约](output-contract.md)，不删除可回溯性。

每项目标：candidate_id、statement、origin（explicit/inferred）、actor（未知为 null）、context（必要条件字符串数组）、evidence_candidates、inference、review_status（pending）。不填无用细分类。

每条依据：source_id、quote、role（basis/context）、start_char/end_char（未知同为 null，否则 Unicode 码点半开区间）。至少一条 basis；推断须有 inference.reason、assumptions、basis_candidate_ids，非推断 inference 为 null。

暂不能确定是否是目标的内容放 review_questions，每项 candidate_ids、question、reason；允许空 candidate_ids 表示整体问题。动作、规则和困难留在原文，必要时引用为 context 或条件，不逐项生成分类记录。

单独提取或要求阶段审核时生成短 MD：资料名、目标列表、必要问题、统一意见区。不重复逐项原文与分类解释；原文和推断能按需读取。完整任务由助手继续证据核对与建模，不默认推送全部中间结果。

render_review.py 同时读取 v3 和旧 draft-2，已有文档拒绝覆盖。旧 classification.md 仅解释旧数据，不是新版分类依据。迁移时仅选原 goal，并核对诊断记录是否含必要条件，不擅自丢弃未解决问题。
