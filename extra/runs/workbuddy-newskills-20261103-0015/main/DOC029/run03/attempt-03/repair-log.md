# attempt-03 修复记录

## 触发原因
attempt-02 的 coverage-check 仍为 structure=failed，错误变为 `S4 final goals has duplicate or unknown IDs`。

## 原因定位
S4 把 C008、C009、C010 三项都映射到 G006，`final_goal_ids` 出现重复 G006。检查器要求该字段内 ID 唯一；三项的 entries 合并关系本身正确。

## 修改对象
- S4：`candidate_ids` 改为 `["C008"]`，`final_goal_ids` 改为 `["G006"]`，理由说明 C009/C010 已并入 G006。
- 其余 source_checks、entries、目标、判断、联系与组均未改动（S2 的修正沿用 attempt-02）。

## 说明
这是同一类机械映射问题的第二次、也是最后一次修复（预算 attempt-03 用尽）。若仍失败，将保留现状并如实报告。
