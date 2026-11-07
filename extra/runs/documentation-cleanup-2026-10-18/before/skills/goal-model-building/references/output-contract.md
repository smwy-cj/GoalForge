# 目标模型与最终交付契约初版

> 旧模型兼容规范。新版默认见 [KAOS 简明契约](simple-kaos.md)，不自动转换本文件中的旧 refinement。

本文件定义模型数据及交付约定。用户于2026-10-16认可 JSON、Markdown、离线 HTML、SVG 四输出；各工具实际覆盖范围以测试记录为准。与现有 goalforge-extraction-draft-2、goalforge-tracing-draft-1 通过显式字段映射连接，不直接改写上游产物。

## 权威 JSON

goal-model.json 顶层建议字段：

| 字段 | 内容 |
|---|---|
| schema_version | goalforge-model-draft-1 |
| model_id、version、parent_version | 当前模型与父版本；首次 parent_version 为 null |
| input_artifacts | 候选、源文、追溯、用户意见和检查结果的文件引用、实际哈希及版本 |
| document_scope | 允许的文档/材料清单，是否允许跨材料建模及依据 |
| goals | 正式进入当前草案的目标节点 |
| pair_decisions | 已评估目标对、标签、理由、证据和条件，包括 none/uncertain |
| edges | 图中表达的 refinement/related 关系及引用的决策 ID |
| evidence_index | 证据 ID、source_id、原件/转换稿位置、引文或可取得的证据附件、追溯结果引用 |
| candidate_goal_mapping | 候选到目标的保留、合并、拆分或排除映射及原因 |
| diagnostics | 未入模型的动作、障碍、偏好、约束等，或指向完整记录的有效附件 |
| relation_coverage | 节点版本、应评估/已评估对数、未评估范围与采用的策略 |
| issues、assumptions | 未解决问题、阻断级别、条件与推断/设计假设 |
| validation | 实际检查报告引用、检查对象哈希、结构状态与语义状态 |
| review | 人工审核状态和有依据的记录；未审核为 pending |
| changes | 相对父版本的节点、关系和证据变化 |
| delivery | mode、readiness、limitations、实际生成的交付文件清单 |

目标节点至少含 goal_id、statement、origin、actor、context、evidence_ids、source_candidate_ids、trace_status、review_status。origin 沿用 explicit/inferred；用户明确授权的 design_extension 单列并记录提出者与来源，不要求其具备源文直接证据。

精化边包含 edge_id、parent_id、child_id、interpretation、conditions、decision_id；相关边用 a/b 并在图中声明对称关系。所有节点引用都必须存在，ID 不直接拿任意目标表述充当图语法标识。

equivalent 决策尚未归并时留在 pair_decisions 和待审项，不伪装成精化。none、uncertain、未评估对不上精化图；在文档中交代范围和数量，不从权威数据中丢弃。

## 状态与有效检查

- validation.structure_status：not_run / passed / failed。
- validation.semantic_status：not_run / needs_review / reviewed_with_findings / reviewed_no_findings。语义检查未发现问题不保证目标正确。
- review.status：pending / partial / accepted / rejected；accepted 需要真实人工审核记录，不能由模型赋予。
- delivery.readiness：unchecked / blocked / reviewable / accepted。

unchecked 表示缺少当前版本有效检查，blocked 表示存在阻断问题；reviewable 至少要求实际结构检查通过且没有阻断项，仍可以有明确披露的非阻断疑点；accepted 还需要对该版本有效的真实人工采纳记录。修复后的模型哈希改变时旧报告不能直接沿用。

结构检查至少覆盖契约、唯一 ID、有效引用、证据对象、跨文档范围、自环、重复边与精化有向环。finalize 消费实际检查结果并复核文件引用，不将口头确认或程序尚未实现写成 passed。

## 默认模型文档

goal-model.md 包含：

1. 模型范围、版本、来源、准备状态与限制。
2. Mermaid 目标图：保留孤立节点和多个根，父目标指向子目标；用图例区分精化、相关与条件关系。
3. 节点表：编号、表述、类型/来源、主体、情境、证据索引和审核状态。
4. 关系表：端点、方向、解释、适用条件、依据及审核状态。
5. 来源与证据索引：接收者能取得的原件/转换稿位置和附件。
6. 未决问题、不确定/未评估对、排除及归并摘要、检查与修复情况。
7. 版本变化和必要的人工意见栏。

图只是视图，若为可读性分成多个子图，声明覆盖范围并确保全部目标可查。图和表不能独立改语义或隐藏未通过问题；节点表述作为文本安全转义，不能将源资料插入为可执行代码。

纯 finalize 可以由确定性程序完成，无需再次调用模型。不存在对应工具时按可用方式交付并如实说明，不能声称生成了未产生的图像或文档。

## 离线 HTML 与 SVG

默认四份文件同目录：goal-model.json、goal-model.md、goal-model.html、goal-model.svg；必要证据附件放在 attachments 中，引用为相对路径。HTML 内嵌查看所需数据和资源，不通过 fetch 读取旁边 JSON，保证直接打开本地文件也可用。

HTML 首版至少支持：缩放/平移、重置布局、目标搜索、显式/推断及待审筛选、相关边显示开关、节点/关系点击详情、证据原文与原件位置、未决问题列表定位。孤立节点与多根默认保留。筛选隐藏的节点/边说明数量，不改变底层模型；none/uncertain 关系在决策列表保留，不渲染成已确认精化边。

用户体验修订后默认显示全景关系，通过“全景关系/目标层级/相关联系”切换取代单一相关边开关。提供概览入口、专注阅读、目标清单、逐项导航和原文证据卡片；没有层级或搜索无结果时分别说明原因并提供恢复入口。选择节点时高亮真实已有关系，不根据视觉需要新增或修改关系。视口较窄时优先清单阅读，并可返回目标清单。

SVG 是固定布局的静态矢量图，包含实际版本、交付状态、图例和全部目标，精化与相关采用不同线型/颜色，并保留明确文字说明，不能只靠颜色表达。复杂图允许分图但总览和索引不能漏节点。

模型视图保持权威模型快照，拖动/筛选不改变内容；HTML另设可操作的人工审核工作区，意见独立保存，不直接覆盖模型。目标支持认可、改写、排除、合并、拆分、待定；关系支持认可、改类型/方向/条件、待定；证据支持充分/部分/不足/错误；整体支持遗漏目标建议、总体意见及明确的版本认可。

意见采用goalforge-review-feedback-1，详见[人工反馈契约](../../model-review/references/human-feedback.md)。用户可保存/恢复浏览器草稿，导出review-feedback.json与.md，并导入文件继续。尚未记录的表单可随草稿保存，提交前必须记录或放弃。存储失败必须提示，导出的JSON才是可靠交接。导入核对版本、内容、对象、重复、冲突与字段，不静默合并/覆盖当前草稿。

界面显示已记录/未填写/建议修改或待定数量，不从空白推导认可。整体认可要求用户明确确认完整范围与限制，且无未完成表单、修改或争议；审阅包含全部关系判断和原文依据。界面下载不等于模型修改已应用，必须明确下一步交给助手处理。

人工意见应用后，字段review.records保存实际反馈及其基准版本；review.feedback_artifacts声明可取得的反馈文件和实际字节哈希。整体认可另保存review.acceptance，绑定feedback_id、反馈规范哈希、反馈路径及review_target_sha256。反馈文件不进入input_artifacts，避免认可内容包含其自身；review_target_hash排除review/validation/delivery/content_sha256，其余字段含版本全部参与。版本或语义内容改变后不能继承认可，core_hash仍用于机械报告绑定。

新增/改写节点影响的关系使用assessment_status=not_run和显式未评估说明，不冒充已完成的uncertain判断；relation_coverage.evaluated_pairs仅计已评估条目，unassessed_pair_ids另列，存在未评估关系时阻断正式准备状态。原节点、关系和来源映射保存在changes中。

输出模型完整性标识，并在交付清单保存各文件SHA-256；完整性标识针对不含自身哈希/交付清单的模型内容计算，避免自引用。该标识只证明内容一致，不等于语义正确或审核通过。

不加载外部脚本、字体或埋点，不把源文当作 HTML/JS 执行。测试至少包含离线打开、过滤与恢复、详情查看、长中文标签、证据/否定符号安全呈现、孤立节点、多根、版本一致和静态图文字溢出检查。
