# KAOS 简明模型契约与操作

## 边界与来源

概念层 KAOS 核心子集：目标、AND 精化组、OR 替代方案、责任、条件与问题。不是完整形式化工具；形式证明保持 not_run。参考[KAOS 项目](https://webperso.info.ucl.ac.be/~avl/gore.php)与[建模说明](https://objectiver.com/index.php?id=85)。

## 数据

模型 schema：goalforge-kaos-1。工具输出 model_id、version、parent、scope、goals、refinement_groups、evidence_index、issues、limitations、input_artifacts、review、changes。goals 保留候选 ID、简短完整表述、主体、条件、推断、当前支持和依据。

精化包 schema：goalforge-kaos-decisions-1。先 template 绑定实际 extraction 与 judgments 文件字节哈希，再基于原文编制，不给旧判断换哈希冒充重评。groups 每项：

```json
{
  "group_id": "F1",
  "parent_id": "G1",
  "child_ids": ["G2", "G3"],
  "kind": "and",
  "status": "supported",
  "completeness": "complete",
  "rationale": "说明为何子目标在给定条件下足以满足父目标",
  "assumptions": [],
  "evidence_ids": ["E0001"]
}
```

一个组是一套共同满足父目标的子目标；同一父目标多个组是替代方案，每组内部仍全部满足。支持单成员方案，不用二元边混淆共同充分性。引用须真实存在；禁止循环与重复方案。共享子目标复用 ID。

未确认关系 status=proposed，精化不完整 completeness=partial，记录原因；HTML 只作为问题展示，不进入成立层级。非目标或无依据父目标不能为构图加入。一般相关不纳入新核心模型；未评估不是 none。

questions 可附 target_type（goal/group/model）、target_id、message。未解决问题保留。未支持目标不能进入成立精化组。组的 evidence_ids 引用真实依据，但有引用不证明精化成立；作者必须实际阅读关系与假设的上下文。可另提供 evidence_quotes（source_id、quote、role、start_char/end_char）；工具在实际全文定位这些关系原句，生成 K 开头的依据 ID，优先在层级详情展示，避免只引用无关的目标标题。

## 助手运行顺序

先按 goal-extraction v3 产出 extraction.json 与 source.txt，再用 goal-tracing 生成绑定模板并编制 judgments.json。用户不填写技术文件。

```text
python scripts/kaos_model.py template extraction.json judgments.json kaos-decisions.json
```

模板 groups/questions 为空，由助手实际编制。随后：

```text
python scripts/kaos_model.py assemble extraction.json judgments.json source.txt kaos-decisions.json assembled
python scripts/kaos_model.py inspect assembled/model-input.json inspection.json
python scripts/kaos_model.py finalize assembled/model-input.json inspection.json delivery
```

构建用实际判断重执行位置核验，不要求先生成单独追溯报告。输出用新目录/新文件。finalize 再核对原件、绑定、模型及检查报告。

默认交付 HTML、JSON、短 MD、机器清单与必要 attachments。SVG 可在 HTML 导出，或 finalize --svg。内置导出载荷来自同一模型；单独复制 HTML 仍可取出 JSON/MD/SVG，但不包含原件备份。

## 人工审核与回流

反馈 schema：goalforge-simple-feedback-1。model 为实际模型 ID、version、完整规范对象 SHA-256。entries 按 target_type=goal/group/model 与 target_id 分别记录 decision=accept/modify/defer、comment。form_drafts 保留未完成内容；note 为整体补充。

submitted 是可交回的意见包，允许部分审核，不是整份模型认可。未完成表单只能保存 draft。未审内容不由工具推断。

```text
python scripts/kaos_model.py feedback delivery/goal-model.json review-feedback.json feedback-output
```

feedback 校验版本，保留意见，列受影响目标/精化组，不自动决定语义修改。助手依原文编制必要的新目标、新绑定判断与精化包，保留 ID；删除/新增说明，旧对象快照保留。然后：

```text
python scripts/kaos_model.py assemble new-extraction.json new-judgments.json source.txt new-kaos-decisions.json revised --previous delivery/goal-model.json --feedback feedback-output/review-feedback.json
python scripts/kaos_model.py inspect revised/model-input.json revised-inspection.json
python scripts/kaos_model.py finalize revised/model-input.json revised-inspection.json revised-delivery
```

新结果保留父模型快照与反馈，review=pending。未实际解决的意见继续成为问题，不称为自动应用。相同内容重建只是记录版本，不代表已解决修改要求。

修订精化包可加 feedback_dispositions，逐项写 target_type、target_id、status（addressed/unresolved）、reason。未说明 addressed 的修改/待定意见由工具自动保留为新问题；说明只代表作者处理记录，不等于用户认可。整体补充继续保留给下一轮核对。

## 有保存回执的本地预览

```text
python scripts/serve_model.py delivery --port 8772
```

仅监听 127.0.0.1。页面点击保存时将明确选择的内容写入本交付目录的 exports，文件独占创建、核验字节与哈希后返回实际路径，不改模型。模型文件需同版本，反馈需通过版本校验。同源令牌只用于本次本地进程，无外部服务。

普通静态预览或独立 HTML 没有文件保存回执，继续使用浏览器下载、复制和完整文本；页面不把下载请求声称为保存成功。本地服务不可用时显示失败并保留可复制文本，不丢草稿。

## 兼容

旧模型工具与反馈保持原契约。新版 assemble 只接受 v3 与绑定判断；不将旧 refinement 机械映射成 KAOS。旧分类、全对判断要求与四文件默认输出仅用于旧版。
