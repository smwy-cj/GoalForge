# 修复与重跑记录（DOC014-run03 / attempt-01）

本文件记录 harness 两次报错后的修正与重跑。所有改动均在本目录内完成，未复制 spec.json 到 attempt-02/03（按本次隔离会话指令"在本目录内修正后重跑"执行）。

## 触发原因

1. **首次运行失败**：`judgment_template failed (1)` → `ValueError: Inference reason required`。
   定位：`versions/skills/goal-extraction/scripts/render_review.py:83-88` 规定 `origin=inferred` 的目标必须提供非空 `inference.reason`，且 `basis_candidate_ids` 必须是已有 candidate_id 的子集；`origin!=inferred` 时 `inference` 必须为 null。
   我的 spec.json 中 4 个推断目标把 `inference` 填成了 `null`，违反该契约。

2. **第二次运行失败**：`prepare_source failed (2)` → `Use a fresh output directory; existing source artifacts will not be overwritten`。
   定位：`versions/skills/goal-extraction/scripts/prepare_source.py:155-156` 拒绝覆盖已有输出。首次失败前已生成 `work/` 及根目录下 `raw-candidates.json`、`extraction.json`、`judgments.json` 等中间产物，导致重跑时第一步即失败。

## 改了哪些对象

- **spec.json（语义修正，仅 4 处）**：为 G007、G018、G021、G025 四个 `origin=inferred` 目标补齐 `inference` 结构（`basis_candidate_ids` 指向已有目标、`reason` 中文非空、`assumptions` 非空）。其余 21 个 explicit 目标仍为 `inference: null`；所有 `statement`、`context`、`evidence` 的逐字符引文、`judgment`、ledger、decisions 内容均未改动。
- **中间产物（工程清理，非语义修改）**：删除首次运行生成的 `work/` 目录与根目录下 `raw-candidates.json`、`extraction.json`、`judgments.json`。这些均为 harness 程序输出，不是输入资料；删除仅为让 prepare_source 能重新生成。未触碰 `brief.md`、`source/DOC014.json` 与 `spec.json` 的语义内容。

## 理由

只修被点名的 inference 契约问题，并按 brief.md 第 5 节"只修被点名的引用/记录/判断，不做无关改写"约束；清理是重跑必需的工程步骤，不构成对目标、证据或判断的改写。补齐 inference 后复验：引文逐字符 0 错误、`inferred_bad=[]`、`explicit_bad=[]`、direct/inferred 的 `unsupported_parts` 均为空。

## 次数与最终结果

- harness 共运行 **3 次**：首次 1 次 + 重跑 2 次；其中**语义修复 1 轮**（inference 补齐）、**工程清理重跑 1 次**（删除中间产物）。均在 `<=2 repair rounds` 预算内。
- 最终一次成功：`ok=true`，`downgraded=[]`，`warnings=[]`，`coverage_workflow=recorded`，已生成 delivery 全套文件。
