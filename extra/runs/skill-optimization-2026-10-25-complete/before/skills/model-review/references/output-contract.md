# 模型检查输出契约

检查由 kaos_model.py inspect 实际执行，schema_version 为 goalforge-kaos-check-1。

| 字段 | 实际含义 |
|---|---|
| model | model_id、version、完整规范对象 sha256 |
| structure | passed 表示实际结构和输入核验已完成，异常时工具拒绝报告通过 |
| independent_semantic | 未运行独立语义审查时为 not_run |
| formal_proof | 未执行形式化证明时为 not_run |
| human | 当前交付保持 pending，分项意见单独记录 |
| readiness | 存在 blocking 问题为 blocked，否则 reviewable |
| note | 当前检查实际证明什么、未证明什么 |

检查实际文件哈希、源文全文引文、目标支持包、精化组成员/引用、循环与模型内容一致性。仅比较一段 passed 字符串不足以证明通过。

finalize 复执行并比对报告，模型或附件变化后不能继续使用不匹配报告。原文精确匹配不证明语义支持，概念层精化判断不等于形式化证明。

反馈处理另输出 goalforge-kaos-revision-request-1 的 revision-request.json：model、feedback_sha256、affected_goal_ids、affected_group_ids、opinions、note、status、next_step、human_acceptance。以及真实 review-feedback.json 和简短修改说明。

机器报告默认由助手维护，用户只看影响判断的问题和真实意见保存状态。反馈字段见[人审契约](human-feedback.md)。

语义复核按[复核规范](semantic-review.md)另存可读记录，与本工程检查报告区分。本轮不新增语义评审 schema 或核心 issues 字段。readiness=blocked 是既有全局汇总值，实际问题范围仍由模型 issues 的目标/组引用说明，不能由此判定所有目标不受支持。
