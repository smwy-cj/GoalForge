# 修复记录 attempt-03（第 2 次修复，最终成功）

## 触发原因

`attempt-02` 运行
`python .../logs/harness.py "."`
在 `judgment_template` 步骤失败：

```
ValueError: Unknown review question reference
  render_review.py line 105
```

原因：`review_questions` 中的第一条把 `candidate_ids` 写成了原始候选 `["C014"]`。
核验阶段的目标集合是最终目标（`G***`），`C014` 在覆盖记录里处置为 `uncertain`、没有对应目标，
因此该引用无法解析。

## 改动的对象

1. 删除 `review_questions` 中指向 `C014` 的那条问题（个人申请优先级：角色→薪资→地点→公司声誉）。
   该疑问没有消失，改记入 `limitations`：
   “C014（个人申请优先级…）未映射为最终目标：原句是对自身申请习惯的描述，未表达系统排序要求，保留为待确认项。”
   处置本身仍为 `uncertain`，`source_checks` S4 仍为 `uncertain`，语义判断未变。
2. 删除 `decisions.questions` 中 `target_type=model` 的整体问题（内容与 `limitations` 重复，
   且模型级 target_id 不是目标 ID，存在解析风险）；该保留意见仍在 `limitations` 中。
3. 删除 `review_questions` 中与 `decisions.questions` 重复的 `G011` 问题（“相关”判定标准），
   只保留 `decisions.questions` 中的一条，避免同一疑问在 issues 中重复出现。

未改动：29 个目标、57 个原始候选的处置、5 条联系、12 条 `source_checks`、全部引文与支持标签。

## 为什么新建 attempt-03

`attempt-02` 已被失败运行写入 `extraction.json`、`raw-candidates.json`、`assembled/` 等文件，
`prepare_source` 拒绝覆盖既有源文产物；按任务说明第 7 节，把 `spec.json` 复制到新 attempt 后重跑。
`attempt-01`、`attempt-02` 的内容全部保留原样。

## 本次结果的确认

`attempt-03` 运行成功：`ok=true`、`downgraded=[]`、`warnings=[]`、
coverage `structure=passed / workflow=recorded`、inspection `structure=passed / readiness=reviewable`、
`blocking_issues=0`。
