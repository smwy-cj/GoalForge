# repair-log（同一 attempt-01 内修复）

## 第 1 次运行（失败）

- 触发：`python .../logs/harness.py "."` 在 `judgment_template` 步骤报错
  `ValueError: Unknown review question reference`（trace_candidates.py → render_review.py:105）。
- 原因：`spec.json` 的 `review_questions[].candidate_ids` 填的是原始候选 ID（C014/C026/C027 等），
  而提取契约的 `candidates` 即最终目标（G001…），校验要求引用目标 ID。
- 修改对象：仅 `review_questions` 的 5 条 `candidate_ids`，改为对应目标 ID：
  C030→G014、C027/C031→G020、C004/C013→G018,G011、C026→G015、C010→G017。
- 未改动：目标表述、证据、判断、处置记录、relations、groups。

## 第 2 次运行的准备问题

- 触发：`prepare_source` 报 `Use a fresh output directory; existing source artifacts will not be overwritten`。
- 原因：首次失败已在 `work/` 生成 source.txt / source-input.json / source-windows.json，并在根目录生成
  extraction.json / raw-candidates.json / judgments.json；harness 不做幂等覆盖。
- 处理：把自建的辅助文件（reading.txt、窗口副本、构建脚本）移入 `scratch/`，删除上述本次运行生成的中间产物后重跑；
  未删除 `source/`、`brief.md` 与最终 `spec.json`。
- 结果：`ok: true`，`downgraded: []`，`warnings: []`，`blocking_issues: 0`。

## 计数

- 修复轮次：1 次（语义零改动，仅引用类型/中间产物）。
- 最终：goals 21、relations 17、groups 1（成立组 1）、raw_candidates 38。
