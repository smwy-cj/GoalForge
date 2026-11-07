# repair-log（attempt-02）

## 1. 触发原因

attempt-01 首次运行 harness 在 `assemble` 步骤失败（exit 1）：

```
ValueError: Unknown issue target
  at kaos_model.py check_structure → target_ids(model, issue['target_type'])
```

定位：`spec.decisions.questions` 中有一条 `target_type="model"`、`target_id="G002"` 的问题。`target_ids()` 对 `model` 类型只接受 `model['model_id']`，不接受目标 ID，因此该问题被判定为非法 issue 目标。目标、判断、证据、关系均未触发任何错误。

## 2. 改动对象

| 对象 | 改动 | 说明 |
|---|---|---|
| `decisions.questions` 末条（target_type=model, target_id=G002） | 删除 | 该条只是"本次未建立 AND 精化组"的说明性备注，不承载语义判断；其内容移入 `self-review.md` 的未决清单与 `decisions.questions` 已有的模型层说明 |
| 其余全部对象 | 未改 | 8 个目标、23 条原始候选、8 条判断、12 条 source_checks、R1/R2、groups=[]、全部引文逐字符未变 |

## 3. 理由

- 契约要求 issue 的 `target_id` 必须落在该 `target_type` 的允许集合内；`model` 级问题应指向 `model_id`，而该说明又不针对具体模型对象，删除比改指向更忠实。
- 这是结构性引用错误，不是语义修订，因此不需要回改目标、判断或覆盖记录；所有引文偏移与绑定在重跑时由工具重新计算并保持一致。
- 未通过删除有依据的目标、证据或改状态来凑通过。

## 4. 重跑结果

attempt-02 harness 成功：`ok=true`，goals=8、relations=2、groups=0、established_groups=0、raw_candidates=23，有效支持 direct=8 / inferred=0 / insufficient=0 / contradicted=0，`downgraded=[]`，warnings 为空，coverage `structure=passed / workflow=recorded`，inspection `structure=passed / readiness=reviewable`，blocking_issues=0。
