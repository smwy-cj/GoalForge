# 修复记录（attempt-02）

## 触发原因

`attempt-01` 运行 harness 时，前序步骤（prepare_source、capture_template、judgment_template、trace_candidates、ledger_template、coverage_check、kaos_template）均通过，`assemble` 退出码 1：

```
ValueError: Unknown issue target
  kaos_model.py:312  require(issue.get('target_id') in allowed ...)
```

定位：`decisions.questions` 中有一条 `target_type="model"` 的问题，但 `target_id` 填了 `G002`。`kaos_model.py:209-213` 规定 `model` 类型只接受 `model_id`（即 `DOC006-goal-model`），因此被结构检查拒绝。

## 改了哪些对象

| 对象 | 改动 | 理由 |
|---|---|---|
| `decisions.questions[0]`（target_type=model） | `target_id`：`G002` → `DOC006-goal-model` | 该问题讨论的是"是否应为 G002 建 AND 精化组"，属模型级疑问；按契约 model 类型只能指向 model_id。问题文本仍点名 G002，语义未变。 |

其余内容一律未改：24 条原始候选、11 个目标、判断包、覆盖记录（entries/source_checks/passes）、5 条关系、0 个精化组、其余两条 goal 级问题保持原样。

## 修复方式与结果

- 新建 `attempt-02/`，复制 `attempt-01/spec.json` 后只改上述字段并重跑 harness。
- 修复轮次：1 次（未到 attempt-03 上限）。
- 重跑结果：`ok: true`，coverage `structure=passed / workflow=recorded / pending=[]`，inspect `structure=passed / readiness=reviewable`，`declared_vs_effective_downgraded=[]`，blocking issues 0。
- `attempt-01/` 的产物（含失败的 assemble 之前各步输出）原样保留，未做任何回写。
