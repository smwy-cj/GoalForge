# 人工意见与修订规范

先对当前模型与真实反馈执行 feedback，核对 ID、版本、规范对象哈希、对象引用和表单状态。保留原意见与模型，不从自然语言自动推断用户完整认可。

## 处理范围

- 目标修改或待定：回查原文，重新判断目标支持；所有包含该目标的精化组进入待办。
- v2的端点联系也进入待办；联系修改或待定会使声明relation_ids依赖它的组进入待办。实际目标语义、条件、支持或证据变化，即使反馈没有点名也传播失效。
- 精化组意见：单独重评组的充分性、条件与原句；不强制重提全文目标。
- 补充和遗漏：记录整体问题，只在允许范围中回查并补入有依据内容。
- 未实际解决的意见继续成为问题，不因重建文件而消失。
- 只更正关联信息也可能影响含义：现有条件、推断、依据或问题中涉及偏好、障碍、现状及信念的内容发生变化时，回到 goal-extraction 重核受影响目标，并重评依赖这些条件的组。

目标 ID 保持稳定。新判断与当前目标输入绑定，精化包与实际提取、支持文件绑定。反馈处理结果不是语义修复成功的证据。

新增/拆合保留新旧 ID 对应及原因，不能用旧 ID 掩盖不同含义。核验和组判断的实际输入变化后，重建绑定与检查；同一助手连续提取、核验和建模仍不是独立评审。

v2判断包的reassessments记录assessment_id、target_type=relation/group、target_id、reason。每个仍保留的受影响联系/组必须有一次明确重评，否则assemble拒绝沿用结论；删除对象保留旧快照及删除ID，依赖它的剩余组仍需更新。理由是作者重评记录，不是人工确认。feedback_dispositions单独回答真实意见是否已处理，两者不能互相替代。v1修订保持旧版流程，不静默增加新版字段。

## 重建

助手准备 work/revised-extraction.json、revised-judgments.json 与 revised-decisions.json 后：

```text
python skills/goal-model-building/scripts/kaos_model.py assemble work/revised-extraction.json work/revised-judgments.json work/source.txt work/revised-decisions.json work/revised --previous work/delivery/goal-model.json --feedback work/feedback-output/review-feedback.json
python skills/goal-model-building/scripts/kaos_model.py inspect work/revised/model-input.json work/revised-inspection.json
python skills/goal-model-building/scripts/kaos_model.py finalize work/revised/model-input.json work/revised-inspection.json work/revised-delivery
```

两个修订参数一并提供。模型保留身份、父绑定、原节点与组快照、删除 ID、真实反馈和处理说明。目标、原句或支持不符时拒绝，原交付不变。

精化包 feedback_dispositions 逐项说明 target_type、target_id、status（addressed/unresolved）、reason。未说明 addressed 的修改/待定意见由工具保留为新问题；说明仅为作者处理记录，不是用户认可。整体补充继续保留供核对。

修订结果人工 pending；每次交付都让用户审核实际变化。没有需要修改的分项意见可仅记录，不能为制造版本自动扩写目标。
