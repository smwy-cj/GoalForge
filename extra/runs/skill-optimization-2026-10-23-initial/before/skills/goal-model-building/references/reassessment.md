# 人工意见与修订规范

先对当前模型与真实反馈执行 feedback，核对 ID、版本、规范对象哈希、对象引用和表单状态。保留原意见与模型，不从自然语言自动推断用户完整认可。

## 处理范围

- 目标修改或待定：回查原文，重新判断目标支持；所有包含该目标的精化组进入待办。
- 精化组意见：单独重评组的充分性、条件与原句；不强制重提全文目标。
- 补充和遗漏：记录整体问题，只在允许范围中回查并补入有依据内容。
- 未实际解决的意见继续成为问题，不因重建文件而消失。

目标 ID 保持稳定。新判断与当前目标输入绑定，精化包与实际提取、支持文件绑定。反馈处理结果不是语义修复成功的证据。

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
