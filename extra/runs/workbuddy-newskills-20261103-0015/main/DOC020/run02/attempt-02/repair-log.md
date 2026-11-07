# repair-log（attempt-02）

## 触发原因

attempt-01 的 harness 本身退出码为 0，但 `coverage-check.json` 报 `structure: failed`：

```
C035 keep/merge must map to one final goal
```

即 `check_coverage.py` 规定 `keep/merge` 处置必须恰好映射一个最终目标，而 C035 被写成 `merge → [G013, G014]`。

## 改了哪些对象

- `ledger.entries` 中 C035：`final_goal_ids` 由 `["G013", "G014"]` 改为 `["G014"]`，理由改写为“该句紧接 BCC 发给全组之后，强调团队群发在截止日期情境下的重要性”。

## 理由与影响核对

- 原文 T073（"Team. That would be very important when it comes to working on deadlines."）紧接 T071 的 "And BBC, like, sent to all the people in my group." 与 "Team."，语义落点是团队群发，因此映射到 G014 比同时映射两项更贴合原句。G013（转发）的独立性依据仍由 C034（`split → [G013, G014]`）保留，两个目标各自仍有候选来路。
- 未改动任何目标正文、引文、判断标签、关系或精化组；未新增/删除目标与候选；未改 evidence 引文。
- 复跑后覆盖检查应为 `structure: passed`；若仍报错再另开 attempt-03。

## 复跑结果

见本目录 `attempt-summary.json`（coverage_check.structure / workflow 与 counts）。
