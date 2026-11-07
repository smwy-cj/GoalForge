# repair-log（attempt-03）

## 触发原因

attempt-02 的 harness 退出码为 0，但 `coverage-check.json` 报 `structure: failed`：

```
S6 requires basis evidence
```

`check_coverage.py` 的 `check_evidence` 要求每条 `source_checks` 至少有一条 `role=basis` 的引文；S6 原先把 T087 的片段标成 `role=context`，导致该检查项只有 context 引文。

## 改了哪些对象

- `ledger.source_checks` 中 S6 的 `evidence_candidates`：由 T087 尾句片段（role=context）改为 T087 完整整句（role=basis），理由同步改写为“同一句既给‘搜索最重要、每天使用’，也给出日程/过滤的排序”。

## 理由与影响核对

- 原文 T087 是同一整句连续表述，引整句可同时覆盖“搜索优先”与“排序”两部分，语义比截取尾句更完整，也让该回查项具备 basis 依据。
- 未改动目标、判断标签、关系、精化组、其他候选或其余 source_checks；未新增或删除任何对象。
- 修复仅限被点名的引用记录，不超过允许的两次局部修复预算（本轮为第 2 次）。

## 复跑结果

见本目录 `attempt-summary.json`（coverage_check 的 structure/workflow 与 counts）。
