# 修复日志（attempt-02，同一 attempt 内）

## 触发原因

harness 第 1 次运行整体 `ok=true`，但 `attempt-summary.json` 中 `coverage_check` 一步
`exit_code=2 / structure=failed / workflow=partial`，`coverage-check.json` 报错：

```
errors: ["C049 keep/merge must map to one final goal"]
```

即覆盖契约要求 `disposition=keep/merge` 的原始候选**恰好映射一个**最终目标，而 C049、C053
被填成了两个。另：修完 spec.json 后第 2 次重跑在第一步 `prepare_source` 失败
（`Use a fresh output directory; existing source artifacts will not be overwritten`），
原因是上一次运行的中间产物仍在 `work/` 等目录；脚本不会覆盖已有输出。

## 改动对象（仅 spec.json 的 ledger 部分，语义目标/关系/组/引文/窗口均未改）

| 对象 | 改动 | 理由 |
|---|---|---|
| `entries.C049` | `final_goal_ids`: `["G014","G027"]` → `["G027"]`（disposition 仍为 merge），理由改写 | T101 是对 T100 两项 criteria 的重复确认；`quick apply button` 已由 C014/G014 承接，本条按同义确认并入技能集 G027。G014 的 evidence 仍包含 T101a，证据未丢失 |
| `entries.C053` | `final_goal_ids`: `["G029","G030"]` → `["G029"]`（disposition 仍为 merge），理由改写 | T097 是对 T096 总结的重复确认；不自动代写已由 C030 承接，本条并入 AI 识别 G029。G030 的 evidence 仍包含 T097a |
| `entries.C006` | 仅 `reason` 措辞 | 原措辞提到"拆为 G006 与 G007"，但 disposition 为 keep；改为说明 `updated` 维度由 C007 独立承接，映射 `["G006"]` 不变 |
| `source_checks.S5` | `candidate_ids`: `["C006"]` → `["C006","C007"]` | 原写法使 C006 同时指向 `[G006,G007]`，与 entries 中 C006→G006 的映射不一致；补上 C007 后与 entries 一致，`evidence_candidates` 保持 T055a/T071a 不变 |
| 中间产物 | 删除 `work/`、`assembled/`、`delivery/`、`tracing/` 及 8 个中间 json | 仅为在同一 attempt 目录内重跑腾出干净输出目录；保留 `spec.json`、`build_spec.py`、`source/`、`brief.md`。**未新建任何 attempt 目录，未改动上级 attempt** |

## 有意未改（非缺陷）

`G043` 的 `label=insufficient` 如实保留，模型因此产生 1 条 blocking issue
（"原文尚不足以支持这项目标"）并使 `inspection.readiness=blocked`。这是按硬性要求
"insufficient 目标如实保留不得升级"的预期结果，不做规避性升级、删除或改状态来凑通过。

## 实际运行次数

- harness 共运行 3 次：第 1 次 coverage 结构失败；第 2 次（修 spec 后）因中间产物未清理在
  `prepare_source` 失败；第 3 次（清理后）成功。
- 语义修正为 1 轮；第 2 次失败属输出目录占用，不涉及语义改动。

## 修复后结果

`coverage_check`: `exit_code=0 / structure=passed / workflow=recorded / pending=[] / errors=[]`；
`downgraded=[]`；`warnings=[]`；`coverage_workflow=recorded`。
