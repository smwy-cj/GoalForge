# repair-log（attempt-01）

## 第 1 次失败

- 触发：`harness.py` 在 `trace_candidates --judgment-template` 阶段退出码 1，stderr 为
  `ValueError: Inference reason required`（`render_review.py` 校验 `origin=inferred` 的目标必须带非空 `inference.reason`）。
- 定位对象：G021（隐私/本地缓存偏好）。该目标 origin 为 `inferred`，但 `inference` 为 `null`。
- 修改：仅为 G021 补 `inference`（`basis_candidate_ids`、`reason`、`assumptions`），不改变 statement、证据与判断标签；其余目标、候选、ledger 未动。
- 理由：原表述确为推断而非明确请求，不能改为 explicit；补推断依据即符合契约。

## 第 2 次失败（产物目录冲突，非语义问题）

- 触发：`prepare_source` 报 `Use a fresh output directory; existing source artifacts will not be overwritten`。
- 原因：上次失败已生成 `work/`、`extraction.json`、`raw-candidates.json`、`judgments.json`（均为工具派生产物）。
- 处理：将首轮派生产物原样移入 `archive-run1/` 保留，不删除、不改内容；`spec.json` 保持唯一语义输入后重跑。
- 结果：第 3 次运行成功，`ok=true`、`readiness=reviewable`、`downgraded=[]`。

## 汇总

- 内容修复：1 次（G021 inference）。
- 工程性重跑：2 次（含产物目录冲突 1 次）。
- 未做的改写：未删除任何有依据目标、未改证据、未改支持标签、未增设精化组。
