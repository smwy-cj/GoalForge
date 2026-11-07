# 人工审核意见契约

v2模型使用schema_version：goalforge-simple-feedback-2；历史v1模型继续使用goalforge-simple-feedback-1，两者不可混用。model 为被审模型的 model_id、version、sha256，不能以文件名代替内容绑定。

```json
{"schema_version":"goalforge-simple-feedback-2","model":{"model_id":"DOC-goal-model","version":"v1","sha256":"实际完整对象哈希"},"status":"draft","entries":[],"form_drafts":{},"note":""}
```

entries 每项含 target_type（v2为goal/group/relation/model；v1为goal/group/model）、target_id、decision（accept/modify/defer）、comment。目标、联系或精化组必须存在、同一对象不重复；修改或待定需理由。用户只看到“可以／需修改／暂不确定”。

form_drafts 保存未完成表单，以 type:id 为键，值含目标类型、ID、decision 和 comment；decision 可暂为空。note 是整体补充。导出时可加 exported_at。

status=draft 可保留未完成内容；submitted 要求无未完成表单且至少有分项意见或整体补充。submitted 代表可交回的意见包，允许部分审核，不是完整模型认可。未填写、未展开内容不由程序推断为接受。

导入先校验当前模型绑定和内容，再由用户确认替换；不自动合并多人意见或覆盖草稿。导出提供保存、复制与完整文本，本地保存须真实写入才返回成功回执。浏览器草稿不自动发送给助手。

用户分项目标、联系与精化组判断分别保存，认可一项不扩大范围。反馈工具只生成待办，修订规则见[反馈与重建](../../goal-model-building/references/reassessment.md)。
