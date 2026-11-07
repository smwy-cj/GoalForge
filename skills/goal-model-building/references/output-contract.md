# KAOS目标与联系契约

新任务默认 `goalforge-kaos-2`；历史 `goalforge-kaos-1` 继续读取、检查和导出，不自动迁移。两者均为概念层子集，不代表形式化证明。运行命令见[工具](tools.md)，联系语义见[联系发现](relation-discovery.md)。

## 模型

共同字段：model_id、version、parent、scope、goals、refinement_groups、evidence_index、issues、limitations、input_artifacts、review、changes。goals保留goal_id、statement、actor、conditions、origin、inference、support、evidence_ids。candidate_id直接作为goal_id，新增/拆合必须返回提取核验。actor不是实现责任分配。

v2增加relations及source_binding（sha256为实际标准全文字节哈希）；issues.target_type可为goal/group/relation/model。relation_id与goal_id、group_id互不冲突。review始终pending，实际分项意见另存。input_artifacts只引用attachments中的实际文件与SHA-256，inspect由附件重建全部内容，不信任手改模型。

v1不接受relations字段；无类型来源的旧关系不会被猜测迁移。semantic-context.json及提取ledger不是模型语义输入，必要上下文仍以已核验目标条件和判断包表达。

## 判断包

新包为 `goalforge-kaos-decisions-2`，input_binding绑定extraction_sha256、judgments_sha256的实际字节，包含relations、groups、questions、reassessments。v1判断包继续采用旧格式。命令template默认v2；Python库兼容默认v1，新调用须明确version=2。

relations每项示例：

```json
{"relation_id":"R1","source_id":"G2","target_id":"G1","type":"contribution","status":"proposed","conditions":[],"assumptions":[],"rationale":"说明有帮助但未证明充分的依据","evidence_ids":[],"evidence_quotes":[{"source_id":"DOC:S1","quote":"实际关系原句","role":"basis","start_char":0,"end_char":6}]}
```

示例引文与位置须按真实原文编制。type为specialization/operationalization/contribution/precedes，方向按[联系定义](relation-discovery.md)；status为supported/proposed/rejected。必须有非空理由及实际定位的basis依据，supported的两端目标支持须为direct/inferred。conditions与assumptions为字符串数组。v2按各自类型检查循环，不对贡献关系一概要求DAG。

目标依据保留E前缀；groups和relations中的evidence_quotes经全文核验后作为K前缀进入evidence_index，并写入对象evidence_ids。引用准确不证明语义判断成立。最终relations不再携带未定位的evidence_quotes。

## 精化组

groups每项包含group_id、parent_id、child_ids、kind=and、status=supported/proposed、completeness=complete/partial、rationale、assumptions、evidence_ids、evidence_quotes。同一父目标多个完整组为OR替代，每组内子目标共同满足；引用有效，不自环、无重复方案、精化图无环。

v2可增加relation_ids与checks。relation_ids声明实际依赖的联系，端点须在本组父/子目标内。checks每项为kind=normal/exception、origin=source/analysis_assumption、scenario、outcome=supports/counterexample/unknown、rationale；source场景另有evidence_ids。缺少场景时可保留候选组，但supported+complete必须包含正常和异常两类，且全部outcome=supports，所有依赖联系为supported，所有目标支持有效。

只有supported+complete进入成立精化DAG。其余候选及反例继续留作问题，不因有贡献或先后关系就成立。场景检查仅记录编制者判断，不自动证明充分性。

## 反馈、失效与明确迁移

questions含target_type、target_id、message。feedback_dispositions含目标类型、ID、status=addressed/unresolved、reason；真实意见未明确处理时继续保留为问题。

reassessments每项含assessment_id、target_type=relation/group、target_id、reason。目标语义、支持或证据变化及真实修改/待定意见会传播到相关联系与组；联系变化/争议传播到声明依赖它的组。比较实际证据内容，不能因引用编号没变沿用判断；标准全文变更时所有旧目标及相关联系/组均重查。受影响且保留的对象缺重评记录时拒绝构建，不能只更换哈希。详见[修订规范](reassessment.md)。

升级先执行upgrade-template：生成空relations/groups及migration_parent旧模型绑定，由助手重新编制。assemble --migrate-from保留已核验的同一目标集合，生成新版本和迁移快照；未重新编制的旧组记录removed_group_ids并保留可见问题，不能静默消失。v1旧文件只读保留，不把旧related或proposed判断自动变成v2 supported。迁移与反馈修订参数不可混用。

## 交付

v2交付manifest为goalforge-kaos-delivery-2；检查报告为goalforge-kaos-check-2；反馈与待办为对应v2契约。旧v1维持原版本。

HTML提供成立精化图、目标清单和独立联系视图。联系逐项显示方向/类型/状态、条件、假设及原句，可单独反馈；已否定记录仍保留。JSON与MD包含全部记录；SVG分为goal-model.svg与goal-relations.svg，不把贡献画成成立精化箭头。共享目标仍只在精化图画一个节点。

所有导出来自同一冻结模型；manifest列实际文件哈希，HTML内置同版本导出内容，本地保存核验实际内容后返回回执。模型、附件或报告变更后重新inspect/finalize，旧检查不继续有效。
