# attempt-02 修复记录

## 触发原因
attempt-01 的 harness 运行完成（readiness=reviewable，无降级、无 blocking），但 `coverage-check.json` 报 structure=failed，错误为 `S2 final goals has duplicate or unknown IDs`。

## 原因定位
`source_checks` 的 S2 把三个候选（C003、C004、C005）映射到 G003、G003、G004，重复列了 G003，触发检查器的重复 ID 规则；覆盖本身无误，C004 已按 entries 合并进 G003。

## 修改对象
- S2：`candidate_ids` 改为 `["C003","C005"]`，`final_goal_ids` 改为 `["G003","G004"]`，理由说明 C004 已并入 G003。C004 的 entries 记录不变。
- `review_questions`：置空。三条内容与 `decisions.questions` 完全重复，保留在模型问题层即可，避免同一问题重复出现在交付问题清单。

## 未改动
36 条原始候选、10 个目标、证据引文、判断标签、3 条联系、GR1（proposed/partial）均未改动。
