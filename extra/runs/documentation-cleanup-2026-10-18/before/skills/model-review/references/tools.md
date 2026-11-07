# 运行方式与补丁白名单

以下路径相对于项目根目录，输出目录必须为空；原始模型和历史交付不覆盖。

```text
python skills/model-review/scripts/review_model.py <模型JSON> <新目录> --mode inspect
python skills/model-review/scripts/review_model.py <模型JSON> <新目录> --mode propose
python skills/model-review/scripts/review_model.py <模型JSON> <新目录> --mode repair --patches <patches.json>
```

inspect 输出 review-report.json 与 model-review.md。propose 额外输出 patches.json；当前仅自动纠正“所有唯一目标对已经完整存在、只是统计数写错”的情况，不补造缺失关系。其他提案由当前助手根据允许资料形成并明确标注依据。

repair 的 patches.json 为补丁数组，每项含 patch_id、issue_ids、base_version、base_core_sha256、rationale、expected_checks、operations。issue_ids 必须来自当前重新检查的问题集。单次调用是一次事务；实际累计两轮后停止，失败不自动重试。

operation 示例：

```json
{"action":"replace","entity":"model","id":null,"field":"relation_coverage","before":{"strategy":"all_pairs","expected_pairs":3,"evaluated_pairs":99},"after":{"strategy":"all_pairs","expected_pairs":3,"evaluated_pairs":3}}
```

| entity | id 对应字段 | 可替换字段 |
|---|---|---|
| model | null | relation_coverage |
| goal | goal_id | statement、origin、actor、context、evidence_ids |
| pair | pair_id | label、a、b、parent_id、child_id、rationale、conditions、evidence_ids |
| edge | edge_id | a、b、parent_id、child_id、type、decision_id、conditions |
| evidence | evidence_id | start_char、end_char、quote、source_id、original_locator |

只能替换已经存在的字段，不增删对象、不改 ID。新增/删除/归并/拆分需交回构建，不作为此脚本的已实现能力。

先在副本核对全部前置条件，再应用并重新检查。新增阻断缺陷时整体回滚；语义变化导致的 needs_retrace 是显式失效标记，可以保留为 blocked 修订，但不能称为语义修复成功。没有任何问题改善时停止。每次保留的修复在 changes 保存完整补丁，版本追加 .r1，parent_version 保留旧版本。

附件只读模型 input_artifacts 中声明的 attachments/ 内文件，验证实际字节哈希并禁止目录逃逸。标准全文约定为 attachments/source.txt，按 Unicode 码点半开区间验证引文。现有工具针对项目契约进行关键检查，不是通用 JSON Schema 引擎。

最终交付调用 goal-model-building 的 finalize_model.py；它会核对报告版本/核心哈希/原文件哈希，重新执行机械检查，保留语义疑点，打包报告和证据附件，再统一生成 JSON/MD/HTML/SVG。reviewable 仅表示可供人工审阅，人工状态仍为 pending。

## 接收HTML人工意见

```text
python skills/model-review/scripts/process_feedback.py <goal-model.json> <review-feedback.json> <新计划目录>
python skills/model-review/scripts/process_feedback.py <goal-model.json> <review-feedback.json> <新修订目录> --apply
python skills/goal-model-building/scripts/finalize_model.py <新修订目录/feedback-model.json> <新修订目录/review-report.json> <新交付目录>
```

首条只校验/分流；第二条才应用明确意见并生成副本、实际反馈记录与复检，第三条统一导出。含语义变更的模型通常是blocked，需依据review-tasks.json重新追溯与关系评估，不把机械改写视作语义修复完成。有retrace-input.json时可交goal-tracing的现有脚本，ID沿用goal_id，判断仍需另行提供。

整体认可仅限submitted反馈，明确完整范围和限制确认，无修改/争议/待定，且实际机械检查无阻断；认可只改变review元数据，不改语义版本。partial仅表示已有意见，不代表整体采纳。应用内容修改后是新版本.h1，人工pending；来源、旧节点/关系与意见保留changes。新目标必须有已声明原文依据，不自动接受设计扩展。

当前证据争议同时列出目标与关系的直接引用：只供关系使用的证据使该关系失效，交building重评；没有目标不代表无需处理。重新编制的目标判断必须按goal-tracing的版本绑定契约提供；完成后由building.reconcile接入实际文件并复检，不再手工改支持状态绕过判断。
