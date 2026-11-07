# repair-log（attempt-02）

## 触发原因

attempt-01 运行 harness 失败，`coverage-check.json` 报结构错误：

```
structure: failed
errors: ["C010 split requires at least two final goals"]
```

原因是我把 C010（千字长文低效、想要更小的内容）标为 `split`，但只映射到 G006 一个目标；工具要求 `split` 至少对应两个最终目标。

## 修改对象

- `ledger.entries` 中 C010：`disposition` 由 `split` 改为 `keep`，`final_goal_ids` 仍为 `["G006"]`。
- C010 的 `reason` 改写为：本条是短内容目标的主依据，“仍要全面”的限定由 C013 补充并共同支撑同一目标。

## 理由

语义上 C010 与 C013 是同一核心动作（给出更短的内容）下的两个限定，不是两个可独立满足的结果，因此 `keep` + 另一条 `merge`（C013）是准确记录；改用 `split` 会虚增目标数并与实际映射矛盾。

## 复跑结果

- 覆盖检查：`structure=passed`、`workflow=recorded`，`dispositions: exclude 3 / merge 15 / keep 15`。
- 后续 `kaos assemble` 失败：`ValueError: Unknown issue target`（见 attempt-03/repair-log.md）。
