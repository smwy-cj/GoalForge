# DOC025 run03 attempt-02 自检记录

## 1. 生成方自检（明确标注：这是生成方自检，不是独立语义评审）

- **候选是否被压薄**：否。逐窗（13 窗，4 轮/步 2）捕获 22 个原始候选，未先压缩成"主要需求"清单；无意图窗口（W0004、W0012、W0013 及纯采访者提问轮）如实记录为处理过但无候选。
- **复合目标是否拆分**：是。C005（打开应用的三个日常意图→G002/G007/G004）、C013（群组帖子+群内连接→G007/G011）、C020（筛选期望+查找目的→G018/G019）按独立意图依据拆分；C008（审阅/提交）与 C007 同义合并入 G006，未机械按动词数拆。
- **条件/否定/强度是否丢失**：核对保留——弱市仍探索（G001 条件）；easy apply 有时需补传简历/答题（G006 条件）；"usually want/sometimes I'll"习惯语气、G019 的 sometimes 情境性、G018 的"I often wish"愿望强度均在表述/理由中保留；T021 两处障碍（筛选粒度受限、网络外连接受限）分别记入 G018 条件与 G020 条件，未取反成补救目标。
- **精化组是否有反例未解决**：未建任何精化组（0 组）。原文无"子目标共同满足足以实现父目标"的声明，为凑层级硬造组的风险不存在；R7（提醒→探索）仅记贡献不记精化，理由已注明。
- **是否为凑层级造根**：否。无根目标、多根扁平模型；9 条联系（2 operationalization、3 specialization、2 precedes、2 contribution，其中 R9 为 proposed）均有实际关系原句，未为连边造节点。
- **已知弱点**：G016/G017（上传简历、open to work）原文仅"you can"功能说明，判 insufficient 保留待确认，导致 2 条 blocking issue、readiness=blocked——这是如实呈现而非错误；R9 依赖渠道假设（proposed）；R1 的方式—目的链依赖 T004 采访者提问框定的问答结构。

## 2. 工程检查实际结果（复制自 attempt-summary.json）

```json
"coverage_check": {"exit_code": 0, "structure": "passed", "workflow": "recorded", "pending": [],
  "counts": {"source_segments": 27, "windows": 13, "raw_candidates": 22, "final_goals": 20,
             "source_checks": 7, "actual_passes": 1,
             "dispositions": {"keep": 16, "split": 3, "merge": 2, "exclude": 1}}},
"tracing_status": "completed",
"declared_vs_effective_downgraded": [],
"inspection": {"structure": "passed", "readiness": "blocked",
               "independent_semantic": "not_run", "formal_proof": "not_run", "human": "pending"},
"counts": {"goals": 20, "relations": 9, "groups": 0, "established_groups": 0, "raw_candidates": 22,
           "support_labels": {"direct": 18, "inferred": 0, "insufficient": 2, "contradicted": 0},
           "issues": 9, "blocking_issues": 2},
"windows": {"count": 13, "size": 4, "stride": 2},
"warnings": []
```

## 3. 未决问题清单

来自 review_questions / decisions.questions / blocking issue：

1. G016（上传简历到 LinkedIn）：仅"you can upload your resume to Linkedin"功能说明，是否保留为目标待人工确认（blocking，insufficient）。
2. G017（open to work 状态）：同为功能说明口吻，是否可结合求职背景推断为目标待确认（blocking，insufficient）。
3. G020：连接受阻按"受阻目的"保留为目标、障碍写入条件，该解读及是否单独登记障碍待确认。
4. R9（G007→G003 贡献，proposed）：信息流是否为其保持行业信息更新的渠道，原文未直述。
5. 模型级：全篇无 AND 精化组，扁平结构是否存在遗漏层级请人工复核。

## 4. 实际执行情况

- 原文完整读取 2 遍（逐窗捕获 1 遍 + 全篇校正/逆向回查 1 遍），27 轮全部覆盖，13/13 窗口 processed（P1 initial，isolated）。
- 补查：全篇校正阶段核对指代（T016 "those"、T009-010 "both of these"、T003 "there"）、例外与相反证据（T021 两处障碍），未新增 P2 候选。
- 修复次数：0（harness 首次运行成功，无 downgraded、无 warnings、无 ambiguous 引文）。
- 实际耗时（自报）：约 50 分钟。
- 停止原因：完成首轮提取+全篇校正，无新有据意图需要追加补查轮；预算 1 initial pass。

## 5. 没有做的事

- 独立语义审查：not_run（生成方自检不能替代）。
- 形式证明：not_run（结构检查通过不证明精化充分性/语义正确性）。
- 人工接受：pending（review 状态保持 pending，等待人工审核）。
