# KAOS 目标模型契约

schema_version：goalforge-kaos-1。建模原则见[精化规则](modeling-rules.md)，运行见[工具](tools.md)。本契约是可执行的概念层核心子集，不代表完整形式化 KAOS。

## 模型

| 字段 | 约束 |
|---|---|
| model_id / version / parent | 模型身份、当前版本、实际父模型绑定；首次 parent=null |
| scope | document_id、实际 coverage |
| goals | goal_id、statement、actor、conditions、origin、inference、support、evidence_ids |
| refinement_groups | 精化组数组，每组一种共同满足方案 |
| evidence_index | 位置核验后的原文依据，E 前缀为目标依据，K 前缀为关系原句 |
| issues | target_type（goal/group/model）、target_id、message、blocking |
| limitations | 实际资料与处理限制 |
| input_artifacts | attachments 下真实文件路径与 SHA-256 |
| review | 当前工具保持 status=pending，实际分项意见单独保存 |
| changes | 父对象快照、真实反馈哈希、删除 ID 与意见处理说明 |

actor 表示原文支持的主体，不据此自动认定 KAOS 系统代理责任。未知主体为 null，缺少完成条件记问题，不编造指标。

## 精化判断包

schema_version：goalforge-kaos-decisions-1。input_binding 绑定 extraction_sha256 和 judgments_sha256 的实际字节。groups 每项：

```json
{"group_id":"F1","parent_id":"G1","child_ids":["G2","G3"],"kind":"and","status":"supported","completeness":"complete","rationale":"说明共同满足的依据","assumptions":[],"evidence_ids":["E0001"],"evidence_quotes":[]}
```

同一父目标的多个组表示完整替代方案；单成员组允许。status 为 supported/proposed，completeness 为 complete/partial；仅 supported+complete 进入成立的层级图。每组有真实依据与非空理由，成员、端点、方向有效，不自环或形成有向环，不重复同一方案。

evidence_quotes 每条含 source_id、quote、role、start_char/end_char，用于定位说明关系的原句；工具核验后加入 K 依据并优先显示。引用存在不证明精化语义成立。

questions 每项为 target_type、target_id、message。修订时 feedback_dispositions 含目标类型、ID、status（addressed/unresolved）与 reason，处理范围见[修订规范](reassessment.md)。

## 交付视图

HTML、JSON、短 MD 来自同一冻结模型，附实际源文、判断与检查记录。SVG 按需生成。DAG 每目标一个节点，精化组为连接点，箭头从父目标向子目标展开；共享节点不复制，孤立目标保留。未知精化不伪装成成立边。

manifest.json 列实际文件与哈希。HTML 内置同版本的 JSON、MD、DAG SVG 导出内容；完整原件仍在附件中。目标图、清单和文字说明不得自行补写语义。接口文件名可按任务调整，机器契约标识保持明确。
