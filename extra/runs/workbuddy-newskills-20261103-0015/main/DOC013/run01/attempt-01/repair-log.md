# repair-log（同一 attempt 内修正）

本文件记录 attempt-01 内两次 harness 失败、修改对象与依据。按任务说明，不新建 attempt 目录；首次失败产物已归档到 `_failed_run1/`（work/、extraction.json、raw-candidates.json、judgments.json），未删除。

## 失败 1：judgment_template — Unknown inference reference

- 触发：`trace_candidates.py --judgment-template` 在 `render_review.validate` 抛出 `ValueError: Unknown inference reference`。
- 原因：7 个 inferred 目标的 `inference.basis_candidate_ids` 填的是原始候选 ID（C017/C018/C019/C020/C033/C034/C035），而校验要求 basis 必须属于最终目标集合（extraction 的 candidates 即 G001–G023）。
- 修改对象：G011、G012、G013、G014、G015、G016、G017 的 `inference`。
- 修改内容与理由：
  - G011–G014 的 basis 改为 `["G003"]`（创作者上传能力是这四项格式/时长/发布推断的所属目标），并改写 reason 说明推断挂靠点。
  - G015/G016/G017 的依据是 T040 的障碍观察本身，没有可作为基础的既有目标；为避免虚构联系，basis 置为空数组，并在 reason 中写明依据是 C033/C034/C035 的观察，不指向任何目标。
- 未改动：目标表述、证据引文、判断标签、覆盖记录。

## 失败 2：prepare_source — 输出目录已存在

- 触发：`prepare_source.py` 返回 2，提示 "Use a fresh output directory"。
- 原因：失败 1 已在 `work/` 生成 source-text/windows 等产物，重跑时工具拒绝覆盖。
- 处理：把失败产物整体移入 `_failed_run1/`，使 `work/` 成为全新目录后重跑；spec.json 内容未因该步改变。
- 重跑结果：`ok=true`，coverage `structure=passed / workflow=recorded`，tracing `completed`，无 downgraded、无 warnings；readiness `blocked`，3 条 blocking 全部来自 3 个 insufficient 目标（G013/G014/G016），属如实保留、不升级的结果。

## 计数

- 实际重跑次数：2（首次异常 + 目录冲突），均为局部修正，未做无关改写。
