# 修复记录（attempt-02）

本目录是在前一次 attempt 被外部中断后从原文重新开始的续跑。以下只记录本次 attempt 内 harness 的实际失败与修改。

## 修复 1：prepare_source 拒绝已有输出目录

- 触发：首次运行 harness 报 `prepare_source failed (2): Use a fresh output directory`。
- 原因：我在先读窗口划分时手动运行过一次 `prepare_source.py source/DOC018.json work`，留下 `work/source.txt`、`work/source-input.json`、`work/source-windows.json`；harness 每次都要重建这些文件。
- 修改：删除该 `work/` 目录（仅我本人上一步生成的中间件），未改 `spec.json`。
- 理由：这是工具对输出目录“不可覆盖”的约定，不涉及语义内容。

## 修复 2：review_questions 引用了非候选 ID

- 触发：第二次运行在 `judgment_template` 报 `ValueError: Unknown review question reference`。
- 原因：`extraction.review_questions[1].candidate_ids` 写了 `C012`。C012 只是原始候选（raw-candidates）编号，提取层候选集是 G001–G009，故校验失败。
- 修改：该问题的 `candidate_ids` 改为 `[]`（整体问题），问题正文保留并把“原始候选 C012”写明在文本里；其余对象未动。
- 理由：该问题讨论的是“现有 Kindle 本章剩余时间是否要在新应用中保留”，没有对应的最终目标，按契约用空 ID 表达整体问题最准确，不为了通过校验硬挂到某个 G 目标上。

## 结果

第三次运行通过：`ok=true`，无 `downgraded`，coverage `structure=passed / workflow=recorded`，inspection `structure=passed / readiness=reviewable`，blocking 问题 0。

共 3 次 harness 调用（2 次失败、1 次成功），未改动任何已声明的语义判断。
