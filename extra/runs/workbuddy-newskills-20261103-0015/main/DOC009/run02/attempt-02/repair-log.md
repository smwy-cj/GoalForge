# 修复记录（DOC009 / run02 / attempt-02）

本次为续跑 attempt，前一次 attempt 被外部中断、未产出交付，故从原文重新开始，并在本目录内完成全部修复。共运行 harness 3 次（1 次首次失败 + 2 次修复后重跑），未改动 attempt-01 或其他目录的任何产物。

## 修复 1：judgment_template 失败 —— `ValueError: Inference reason required`

- 触发原因：`trace_candidates.py --judgment-template` 校验 extraction 契约，凡 `origin=inferred` 的目标必须带非空 `inference`（含 `reason` 与 `basis_candidate_ids`）。我在首次编制时把 G018、G019、G020、G021 的 `inference` 留为 `null`。
- 改了哪些对象：
  - G018（事实准确）：补 `inference`，`basis_candidate_ids=["G001"]`（G001 含"除非需要完全事实正确"的例外条件），reason 说明推断链条与假设。
  - G019（自动化流水线）：补 `inference`，`basis_candidate_ids=["G014"]`（T043 把自动化与提高生产力直接相连），reason 说明反事实愿望与假设。
  - G020（检测纠正幻觉）：补 `inference`，`basis_candidate_ids=["G018"]`，reason 说明其服务于事实准确性且自述无方案。
  - G021（界面不分散注意力）：`origin` 由 `inferred` 改为 `explicit`（界面不满在 T053 是明确表达），`inference` 保持 `null`；`judgment.label` 仍为 `inferred`，并在 rationale 中说明"origin 与 support 分别判断"的差异（目标表述的泛化需要推断步骤）。
- 理由：契约与技能均要求 origin 与支持分别判断、推断必须有依据与假设；不通过把 label 改成 direct 来规避该校验，G021 也不因省事而改判支持强度。

## 修复 2：assemble 失败 —— `ValueError: Source scenario requires evidence`

- 触发原因：`kaos_model.py` 的 `check_structure` 要求 `checks` 中 `origin=source` 的场景必须带非空 `evidence_ids` 且引用真实存在的 evidence。我的 GR1、GR2 异常场景取自原文（T041 人工复核、T015 作业撰写长文档），却未引用 evidence。
- 改了哪些对象：
  - GR1：在其 `evidence_quotes` 中补入 T041（关键任务仍需人眼复核、不能开箱即用地自动化），异常场景 `evidence_ids=["K0003"]`。
  - GR2：在其 `evidence_quotes` 中补入 T015（作业还需撰写长文档），异常场景 `evidence_ids=["K0005"]`。
  - K 前缀编号按 assemble 的固定顺序（先 refinement_groups 后 relations，组内按引文顺序）推算：GR1 三条约 K0001–K0003，GR2 两条约 K0004–K0005；结果与 assembled 实际生成的 `evidence_ids`（GR1=[K0003,K0002,K0001]，GR2=[K0005,K0004]）一致。
- 理由：来自原文的场景必须绑定真实引文，不能把有原文依据的场景改标为分析假设来绕过校验（那会丢失来源标注），也不冒充访谈事实。

## 修复 3：coverage_check 结构错误 —— `S12 contradicts candidate dispositions`

- 触发原因：覆盖检查要求 `source_checks` 所列 `final_goal_ids` 与所列候选在 `entries` 中的映射一致。S12 列了候选 C025（disposition=exclude，映射为空）与 C026（→G018），却把 G019 写进 `final_goal_ids`，而 G019 来自另一个候选 C027。
- 改了哪些对象：S12 收敛为 `candidate_ids=["C026"]`、`final_goal_ids=["G018"]`；C025（关键任务需人工复核）的回查另立 S18，`final_goal_ids=[]`、`outcome=excluded`，理由写明其含义作为相反/限制证据写入 G019 的 context 与 model 问题。
- 理由：不通过把 C025 强行映射到 G019 来消错；人工复核是受访者的现状判断与信念，按目标边界不作为独立目标，也不伪造映射。

## 未做的改动

- 未修改任何目标表述、支持标签或联系状态来换取检查通过；`downgraded=[]`，两个 `insufficient`（G010、G020）如实保留。
- 未删减有依据的目标或引文；未改动冻结技能目录。
