# 修复记录（attempt-02）

## 触发原因

第一次 harness 运行失败于 `assemble`（`kaos_model.py` 结构检查）：

- `ValueError: Source scenario requires evidence`（check_structure，kaos_model.py:305）
- 同次运行 `coverage-check.json` 另报 `structure: failed`，错误为 `C085 merge requires another source candidate`（check_coverage.py:214）

## 改动对象与理由（共 1 轮修复）

1. **三个精化组的场景检查 origin 改写**（GR1/GR2/GR3 的 `checks[].origin`：source → analysis_assumption）
   - 理由：这三个 normal/exception 场景是我依据原文做法构造的复合情形（如"内容合规但创作者未提供转写文本"），并非原文中已有的独立场景句；契约要求 `origin=source` 的场景必须绑定实际 evidence_ids，改判为 analysis_assumption 与场景的真实来源一致，不改任何场景内容、outcome 或父/子目标。
2. **C085 的 disposition 改写**（merge → keep，仍映射 G046）
   - 理由：G046（不在 UI/UX、导航与细节上妥协）只由 C085 一条原始候选承接，`merge` 要求同目标另有来源候选；改为 keep 后消解该结构错误，理由同步写明"仅由本候选承接"。
   - 未因此新增或删除目标、未改动其他 86 条处置。

## 未改动的内容

- 未改动任何 goal 的 statement、context、evidence、judgment（首轮即无 downgraded、无 ambiguous 警告）。
- 未改动 31 条 relations、3 个 groups 的端点、方向与状态。
- 未删除任何有依据的目标或证据以换取通过。

## 重跑结果

第二次运行 harness 成功：`ok=true`，`coverage_check.structure=passed`、`workflow=recorded`、`pending=[]`，`inspection.structure=passed`、`readiness=reviewable`、`blocking_issues=0`，`downgraded=[]`、`warnings=[]`。
