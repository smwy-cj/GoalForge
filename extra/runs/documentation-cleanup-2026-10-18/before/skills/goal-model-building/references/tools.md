# 当前工具与覆盖范围

## 组装

```text
python scripts/assemble_model.py <extraction.json> <tracing.json> <relation-decisions.json> <新组装目录> --source <标准全文> [--normalized <规范目标JSON>]
```

语义判断必须先保存到输入文件，工具不会替代模型判断。未提供 normalized 时保留所有 category=goal 的候选，不凭空合并；可提供规范节点数组，节点字段含 goal_id、statement、source_candidate_ids、origin、actor、context。文本、情境、主体、来源或归并/拆分变化时，工具标记 needs_retrace，旧证据不能直接作为新表述的支持。

关系决策数组每项至少含 pair_id、a、b、label、rationale、evidence_ids、conditions、review_status。refinement 还需 parent_id、child_id、interpretation。首版必须提供当前冻结节点全部无序对；不存在默认“无关系”填充。

输出 model-input.json 和 attachments 中的输入副本，保留来源哈希。提取/追溯版本不符、原文哈希不符或坏引用时拒绝组装。

## 四输出导出

```text
python scripts/export_model.py <model-input.json> <新交付目录>
```

生成 goal-model.json、goal-model.md、goal-model.html、goal-model.svg，复制证据附件，另保存 delivery-manifest.json。清单记录文件 SHA-256；模型内容标识不含自身与交付清单，四个视图共用同一模型对象。导出不改变节点和关系语义。

使用标准库 SVG 和内嵌 HTML/CSS/JS，不依赖 CDN、外部字体或网络 API。版式为确定性分层/分行布局，保留孤立节点；不是复杂大图的最优布局。默认全景展示已有关系，可切换精化层级或相关联系；没有精化边时明确说明，不把默认无边误导为没有关系。

2026-10-16 的用户体验修订增加：可点击概览、目标图/清单、专注阅读、目标逐项浏览、原文证据卡片、不确定关系列表、平滑聚焦与减少动画、小屏单列清单及详情跳转。原件定位用可读的页码/轮次等呈现，原始字段和哈希集中在版本信息中。权威模型快照保持不变；新增人工审核工作区独立记录意见，不把筛选或布局作为模型修改。

界面模板、样式、浏览逻辑、反馈契约和审核逻辑分别维护在assets/viewer.html、viewer.css、viewer.js、review-core.js、review-ui.js；导出时一次性内嵌。交付清单保存五份源文件哈希，以区分界面修订与模型语义版本。

## 当前限制

- export_model.py 用于 unchecked/blocked 草案；通过状态必须经下面的 finalize 接入真实报告，不接受只有 passed 字样的输入。人工状态只能通过真实反馈与版本绑定处理进入，不从passed字样推导。
- 契约仅实施部分关键字段/引用检查，不是完整 JSON Schema 校验系统。
- 不自动完成语义规范化、关系评估、人工审核或语音/文档格式转换。
- HTML 内嵌查看所需资源和模型，可直接由浏览器读取；本环境内置浏览器不允许 file 协议，因此本轮仅完成 HTTP 本地预览及无外部依赖检查，直接文件打开需在允许的浏览器中另外验收。

## 检查后的最终导出

```text
python skills/goal-model-building/scripts/finalize_model.py <被检查的模型JSON> <review-report.json> <新交付目录>
```

核对报告 schema、模型 ID、版本、goalforge-core-v1 核心哈希及原文件哈希，重新执行确定性检查与附件验证。检查项或问题集不一致、报告过期、附件被改写时拒绝导出。当前只接受语义not_run的程序报告，模型人工状态可为pending/partial/accepted；accepted需实际反馈附件、完整范围与限制确认及未变更内容绑定，保留既有语义疑点。

结构通过且没有阻断项时 delivery.readiness=reviewable，意为“可供人工审阅”；有阻断项保留 blocked。无法渲染的坏图先返回检查修复，不能隐藏坏边强行出图。finalize 不改目标、关系、证据或语义版本，只登记派生 validation 和 delivery 状态。

四输出与清单之外，打包 attachments/review-report.json、attachments/model-review.md 和原有输入/源文附件。validation.report_sha256 使用规范 JSON 的哈希；清单记录实际文件字节哈希。核心哈希排除 content_sha256、delivery、validation，完整内容标识只排除 content_sha256 和 delivery，二者用途不同。

两项 Skill 的检查/哈希规则共用本目录 export_model.py，运行时保留 skills/model-review 与 skills/goal-model-building 的同级目录。

## 人工审核与版本修订

最终HTML提供开始审核、逐项表单、疑点优先/全部目标/全部关系/全部证据、整体建议、汇总及草稿/提交文件导出。导出的JSON交model-review的process_feedback.py；缺少服务端时不直接写回磁盘，也不发送到外部服务。浏览器存储不可用会提示导出。

revise_model.py为反馈处理内部调用模块，支持明确目标改写、排除、合并、拆分、遗漏目标和关系建议。新增ID保留历史不复用；旧对象及来源映射记录changes。受影响支持needs_retrace，关系退回未评估，形成新版本后不能沿用旧认可。

## 当前判断的回填

使用[reassessment约定](reassessment.md)调用reconcile_model.py，支持完整追溯与关系一起回填、仅追溯的部分回填或仅关系重评。新判断必须绑定实际修订模型；空白关系模板可用--relation-template生成，不能自动带入旧label。

工具核验实际追溯输入、结果和绑定语义判断文件，重新执行引文核对，处理trace:引用的新证据ID映射，保存旧对象及来源映射，检查后生成reconciled-model.json、复检报告与回填记录。随后用当前报告finalize。只生成新tracing.json仍不算已更新模型。

首次组装CLI也要求direct/inferred追溯带当前提取输入绑定。旧平铺判断文件不自动迁移；历史模型仍保留，但重新执行时需要当前空白模板与重新编制的判断。
