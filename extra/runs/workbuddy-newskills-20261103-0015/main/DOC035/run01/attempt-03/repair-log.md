# repair-log（attempt-03）

## 触发原因

attempt-02 覆盖检查已通过，但 `kaos_model.py assemble` 失败：

```
kaos_model.py line 312, in check_structure
    require(issue.get('target_id') in allowed ...)
ValueError: Unknown issue target
```

原因是 `decisions.questions` 中有一条 `target_type="model"`、`target_id="DOC035"` 的问题；组装器只接受落在当前目标/组/联系 ID 集合内的 issue 目标，`DOC035` 不是任一节点 ID。

## 修改对象

- 该条问题：`target_type` 由 `model` 改为 `goal`，`target_id` 改为 `G017`，message 改为“原文没有总体目的句，是否需要一根……根目标统领 G001/G006/G017？当前未造根，保留多根结构。”
- 其余目标、证据、判断、联系、精化组一概未动。

## 理由

这条问题问的是层级形态（是否需要根目标），其影响范围正落在 G017（聚合成功标准）这一层，绑到 G017 不改变问题含义，也不改变任何语义判断；同时满足组装器对 issue 目标必须是实际节点的约束。没有通过删除问题来绕过检查。

## 复跑结果

harness 输出 `ok: true`，`readiness=reviewable`，`established_groups=0`，`downgraded=[]`，`warnings=[]`，`blocking_issues=0`。
