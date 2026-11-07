# repair-log（本次 attempt 内修复记录）

同一 attempt-03 目录内共 3 次 harness 运行，2 次失败后在本目录修正 `spec.json` 重跑，未新建 attempt 目录。

## 运行 1（失败：judgment_template）

- 触发原因：`trace_candidates.py --judgment-template` 报 `ValueError: Unknown review question reference`。
- 定位：`review_questions[].candidate_ids` 被校验为必须属于 extraction 的候选集合（即最终目标 Gxxx）；我误填了原始候选 ID（C015/C002/C003/C044/C039）。
- 改动：
  - 把 `C039` 改为 `G025`（该候选的相反证据指向的最终目标）。
  - 把无对应最终目标的 `C015/C002/C003/C044` 改为空数组（契约允许空 ID 数组表示整体问题），并在问题正文中写明所涉原始候选编号，保留可追溯性。
- 语义影响：仅引用形式，问题内容与判断未变。

## 运行 2（失败：prepare_source）

- 触发原因：`prepare_source.py: Use a fresh output directory; existing source artifacts will not be overwritten`。
- 原因：运行 1 已生成 `work/source-input.json`、`work/source.txt`、`work/source-windows.json` 与根目录中间产物；harness 要求全新输出目录。
- 改动：删除运行 1 生成的中间产物（work 下的 source 三件套、extraction.json、raw-candidates.json、judgments.json 等），保留 `spec.json` 与我的工作底稿，未改动任何语义内容。

## 运行 3（成功）

- `ok=true`，33 goals / 12 relations / 0 groups，support：direct 30、inferred 3、insufficient 0、contradicted 0，`downgraded=[]`，`blocking_issues=0`，coverage `structure=passed`、`workflow=recorded`，inspection `readiness=reviewable`。

## 运行 4（成功，最优版本）

- 触发原因：自检发现 `decisions.questions` 与 `review_questions` 有 3 条同义重复（G008/G025/G033），issues 计数 18 含重复噪声。
- 改动：删除 `decisions.questions` 中与 `review_questions` 重复的 3 条目标级问题，保留模型级 2 条、G012 1 条、关系 R10 1 条；同步清空旧产物后重跑。
- 结果：issues 由 18 降为 15，其余指标不变（33/12/0，direct 30、inferred 3，blocking 0，downgraded 空）。

## 其他修正（合并阶段，非 harness 报错）

- 引文精确性：`there is a 1 kind of segmentation...` 首字母大小写与原文不符（原文为 `There is a 1 kind...`），在 C023 与 G020 两处修正后逐字符匹配。
- 字段清理：删除笔误字段 `modality_note`、`description`，避免向契约外写入未定义字段。
