# source 批量处理总览（34 篇）

> 生成时间：2026-10-19｜工具链：goal-extraction → goal-tracing → goal-model-building → model-review
> 全部文档状态：版本 v0.1、结构检查 passed、交付 readiness=reviewable、人工审核 pending。

| 文档 | 目标数 | 关系对 | related | refinement | uncertain | 孤立节点 | 交付 |
|---|---|---|---|---|---|---|---|
| DOC003 | 14 | 91 | 11 | 3 | 1 | 1 | final/goal-model.html |
| DOC004 | 12 | 66 | 9 | 0 | 0 | 3 | final/goal-model.html |
| DOC005 | 8 | 28 | 18 | 0 | 0 | 0 | final/goal-model.html |
| DOC006 | 6 | 15 | 6 | 0 | 0 | 0 | final/goal-model.html |
| DOC007 | 9 | 36 | 9 | 0 | 1 | 3 | final/goal-model.html |
| DOC008 | 8 | 28 | 6 | 0 | 1 | 1 | final/goal-model.html |
| DOC009 | 13 | 78 | 7 | 0 | 1 | 3 | final/goal-model.html |
| DOC010 | 7 | 21 | 4 | 2 | 0 | 1 | final/goal-model.html |
| DOC011 | 11 | 55 | 11 | 0 | 0 | 1 | final/goal-model.html |
| DOC012 | 14 | 91 | 11 | 0 | 0 | 1 | final/goal-model.html |
| DOC013 | 13 | 78 | 7 | 0 | 0 | 3 | final/goal-model.html |
| DOC014 | 13 | 78 | 5 | 0 | 1 | 5 | final/goal-model.html |
| DOC015 | 13 | 78 | 8 | 0 | 0 | 3 | final/goal-model.html |
| DOC016 | 13 | 78 | 9 | 0 | 0 | 2 | final/goal-model.html |
| DOC017 | 13 | 78 | 8 | 0 | 0 | 3 | final/goal-model.html |
| DOC018 | 9 | 36 | 7 | 0 | 0 | 0 | final/goal-model.html |
| DOC019 | 11 | 55 | 10 | 0 | 0 | 0 | final/goal-model.html |
| DOC020 | 19 | 171 | 13 | 0 | 1 | 6 | final/goal-model.html |
| DOC021 | 17 | 136 | 19 | 0 | 1 | 0 | final/goal-model.html |
| DOC022 | 11 | 55 | 16 | 0 | 0 | 0 | final/goal-model.html |
| DOC023 | 10 | 45 | 16 | 0 | 1 | 0 | final/goal-model.html |
| DOC024 | 10 | 45 | 8 | 0 | 1 | 0 | final/goal-model.html |
| DOC025 | 14 | 91 | 13 | 0 | 0 | 0 | final/goal-model.html |
| DOC026 | 13 | 78 | 11 | 0 | 1 | 1 | final/goal-model.html |
| DOC027 | 14 | 91 | 13 | 0 | 1 | 0 | final/goal-model.html |
| DOC028 | 13 | 78 | 13 | 0 | 0 | 0 | final/goal-model.html |
| DOC029 | 8 | 28 | 9 | 0 | 0 | 0 | final/goal-model.html |
| DOC030 | 15 | 105 | 12 | 0 | 0 | 0 | final/goal-model.html |
| DOC031 | 10 | 45 | 9 | 0 | 1 | 1 | final/goal-model.html |
| DOC032 | 8 | 28 | 6 | 0 | 0 | 1 | final/goal-model.html |
| DOC033 | 12 | 66 | 9 | 0 | 1 | 1 | final/goal-model.html |
| DOC034 | 13 | 78 | 9 | 0 | 0 | 1 | final/goal-model.html |
| DOC035 | 13 | 78 | 11 | 0 | 0 | 0 | final/goal-model.html |
| DOC036 | 11 | 55 | 9 | 0 | 0 | 0 | final/goal-model.html |

**合计**：34 篇 / 398 个目标 / 2263 个目标对（related 342，uncertain 13）。

## 各文档目录结构

```
output/DOCxxx/
  extraction.json        目标候选（schema goalforge-extraction-3）
  goal-candidates.md     提取阶段的审核清单
  source.txt / source-input.json   忠实转换稿与片段映射
  tracing/               语义判断 + tracing.json + 追溯审核文档
  relation-decisions.json  两两关系判断（全枚举）
  model/model-input.json 组装草案（附输入哈希）
  review/                结构检查报告
  final/                 goal-model.html / .json / .md / .svg + delivery-manifest.json
```

## 说明

- 每个目标都由原文引文支撑，引文位置经字符偏移核验（location_status=exact）。
- 语义支持度（direct / inferred）由本次会话助手编制，**非独立盲测**：所有模型 semantic_status=not_run。
- 关系判断对每个文档做完全枚举（n(n-1)/2），none 也逐对留痕，未做选择性省略。
- 人工审核状态一律 pending，未生成任何采纳记录。
- DOC005 另有 v0.1-accepted 版本（已完成人工认可绑定），其余 33 篇均为首版待审。
