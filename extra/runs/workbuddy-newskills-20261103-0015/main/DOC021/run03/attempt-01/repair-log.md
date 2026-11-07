# repair-log（同一 attempt 内修正）

## 第 1 次失败

- 触发：`harness.py .` 在 `judgment_template` 阶段退出码 1。
- 报错：`ValueError: Unknown inference reference`（render_review.py:88）。
- 定位对象：`spec.json` → `goals[G016].inference.basis_candidate_ids` 原写 `["C014","C050"]`（原始候选 ID）；该字段只接受本次目标集合内的 candidate_id。
- 修正：改为 `["G015","G028"]`（对应的最终目标），并把理由中的引用说明改为指向这两个目标。
- 语义影响：无。推断依据仍是同一段原文（T019 的抱怨）与 T071/T073 的正面表述，只是引用编号层级从原始候选改为目标。

## 修正后的重跑

- 为在同一 attempt 内重跑，删除了上次失败留下的中间产物：`work/`、`extraction.json`、`judgments.json`、`raw-candidates.json`（均为可重建文件，`spec.json` 未回滚）。
- 第二次运行成功：coverage `structure=passed / workflow=recorded / pending=[]`，inspection `structure=passed / readiness=reviewable`，`downgraded=[]`。
- 除上述一处引用外，未改动任何目标、判断、关系或组。
