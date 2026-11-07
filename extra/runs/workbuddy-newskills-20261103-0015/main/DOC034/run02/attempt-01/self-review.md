# 自检记录（DOC034 / run02 / attempt-01）

> 本文件是**生成方自检**，由同一生成会话完成后编写，**不是独立语义评审**，也不构成人工接受。
> 独立语义审查：not_run；形式证明：not_run；人工决定：pending。

## 1. 生成方自检

### 1.1 候选是否被压薄

- 13 个窗口（4 轮 / 步长 2）逐一处理，全部 `processed`；W0012、W0013 只有收尾寒暄，无候选，照实记录。
- 原始候选 29 条，未按“主要需求”压缩：同一窗口（T003、T007、T009、T017）内的多个结果分别保留为独立候选，未做摘要式合并。
- 18 条最终目标全部有候选来路；4 条 merge、18 条 keep、7 条 exclude，无“只留抽象上层”的情况。

### 1.2 复合目标是否拆分

- T003 一句话里的五类用途拆为 G001–G005（联系、营销、招聘、求职观察、社区活动），各自有独立结果与可独立满足性；营销、招聘另有 T007／T015 的补充依据。
- T007 的“付费推广 + 跟踪指标”未拆成两个目标：付费推广是取得指标的方式，写在 G009 的 context；若把它当目标会与“跟踪”共享同一句依据而变成重复节点。
- T009 的发布流程：核心动作“发布 awareness 贴”保留为 G010；身份切换（公司页 / 个人页）与图片、视频、背景、表情作为同一对象的前提与步骤并入 context；“定时到次日上午”因有独立结果（impressions）与明确的否定项（晚上不合适）拆为 G011。
- T021／T023 分别成 G017（内容开发自动化）与 G018（免多轮评审的专业外观发布），两者目的不同（减少团队规模 / 减少评审流程），未合并成“减轻营销负担”这种抽象节点。

### 1.3 条件、否定、强度是否丢失

- 条件：G005 保留“当有 availability 与 bandwidth 时”；G012 保留“通常只加认识的人”；G014 保留“if you post something there”的条件语气；G011 保留“晚上发不合适”的否定项；G001…G014 的 context 保留比较基准（Google Ads／Facebook、竞争对手、YouTube、LinkedIn 招聘贴）。
- 强度：G004 保留 “sometimes it's nice”；G008 保留过去时（“I did like”）；G012 保留 “don't often／don't reach out too much”（写作 typically，未变成禁止）；G017／G018 保留 “would be great” 的愿望强度；G006 保留 “a little bit of credibility”。
- 否定与相反证据：C009（否认职业发展作用）、C023（“only game in town” 的信念）、C026（平台演进观察）、C018（“hopefully” 期望）均记录后排除，未改写成要求；现状能力（C011 工具易用）未升级为维持要求。
- 已实现能力与偏好：C013 学习内容保留为偏好型目标并标注过去时；C010 成本顾虑作为 G002 的条件而非独立目标；C012 的“you can”泛指能力在 G009 判断理由中说明为何仍判 direct，并列为首条待确认问题。

### 1.4 精化组是否有未解决反例

- 未建任何 AND 精化组（groups = 0）。尝试过的候选是“G010 发布 + G011 定时 + G009 跟踪”共同满足 G002 的曝光目的，但原文没有说明这三者共同足以实现“曝光优于 Google Ads／Facebook”，缺受众定向与内容策略，因此不建组，并把该判断写入 model 级问题（`DOC034-goal-model`）。
- 没有把贡献关系（R2、R3）当作精化箭头使用：R2、R3 只进入 relations 层，`refinement_groups` 为空。

### 1.5 是否为了层级造根

- 没有新增根目标。图中 18 个目标基本并列，只有一处 specialization（G010 → G002）与两处 contribution（G011 → G010、G016 → G010），均由原句直接给出目的/结果关系。
- 未把“赢得生意”（C018）、“专业发展”（C009 为否定）、“平台定位”（C001）升级成上层目标。

### 1.6 需要留意的主观判断（自检发现，非结论）

1. G006 与 G007 同出于 T005 的一段话，拆为“展示资质/存在”与“让他人核实身份”两条；两者可独立满足，但也可被视为同一“可信形象”意图的两面，已在判断理由中写明拆分依据。
2. G015、G016 是挫折陈述转成的避免型目标，origin 与 label 均标为 inferred，并在 `inference` 中写明推断链与假设（basis 分别为 G001、G010）；未把它们写成受访者明示的要求。
3. G009 的原文主语是泛指的 “you”，判为 direct 有争议，已列入 review_questions 第 1 条。
4. G002 把 C010 的成本顾虑吸收为条件，可能低估“成本”作为独立约束的分量；原文只说 “cost is definitely a consideration”，未给阈值，故未单独立目标。

## 2. 工程检查实际结果（复制自 attempt-summary.json / coverage-check.json / inspection.json）

```json
"coverage_check": {"exit_code": 0, "structure": "passed", "workflow": "recorded", "pending": [],
  "counts": {"source_segments": 27, "windows": 13, "raw_candidates": 29, "final_goals": 18,
             "source_checks": 11, "actual_passes": 1,
             "dispositions": {"exclude": 7, "keep": 18, "merge": 4}}}

"tracing_status": "completed"
"declared_vs_effective_downgraded": []

"inspection": {"structure": "passed", "readiness": "reviewable",
               "independent_semantic": "not_run", "formal_proof": "not_run", "human": "pending"}

"counts": {"goals": 18, "relations": 3, "groups": 0, "established_groups": 0,
           "raw_candidates": 29,
           "support_labels": {"direct": 16, "inferred": 2, "insufficient": 0, "contradicted": 0},
           "issues": 6, "blocking_issues": 0}

"warnings": []
```

- coverage-check 的 `errors` 为空、`pending` 为空、`uncertain_candidate_ids` 与 `uncertain_source_check_ids` 均为空。
- 6 条 issues 全部为 blocking=false，且都是主动登记的问题（3 条 review_questions、3 条 decisions.questions），没有降级项。

## 3. 未决问题清单

来自 `review_questions`：

1. G009 依据 “you can kind of keep track of all your impressions” 这类泛指能力，是否确为其本人要求。
2. G008 用过去时描述，是否仍代表当前偏好。
3. G014 的 Lara jobs 是明确渠道要求，还是一次比较经验。

来自 `decisions.questions`：

4. （model）G010／G011／G009 是否应组成 G002 的 AND 精化——原文不足以声称共同充分，未建组。
5. （G012）避免冷连接与 G013 “查资料后再添加”是否为例外关系，原文只有 “maybe”。
6. （G003）LinkedIn 招聘与 Lara jobs 招聘的优先级／适用条件未说明。

blocking issue：无。

## 4. 实际执行情况

- 原文读取：完整读 1 遍（27 轮全文，`source/DOC034.json`），随后按 13 个重叠窗口逐窗处理；工具生成的 `work/source-windows.json` 与自建临时窗口文件坐标一致（临时目录已删除，`work/` 为 harness 产物）。
- 全篇校正：回看全部 27 轮 1 遍，核对指代（“the task”“that process”“it”）、问答范围（T016／T018／T020 三个提问的回答边界）、条件继承（T003 的 availability、T011 的 maybe、T015 的 if）、相反证据（T005 的否定、T015 的渠道比较、T017 的挫折）；未发现需另记 P2 的新候选，故只有 P1。
- 修复次数：0（首次 harness 运行即通过，无 downgraded、无 ambiguous 引文警告，未进入 attempt-02／03）。
- 实际耗时（自报）：约 20–25 分钟，含技能文件通读、逐窗提取、spec 编制、引文逐条字符校验与 1 次 harness 运行。
- 停止原因：完成 13 窗捕获与全篇校正；剩余分歧属于原文信息不足（泛指表述、时态、渠道强度），无新证据可继续，按限制保留为问题。

## 5. 我没有做的事

- 独立语义审查：not_run（本文件是生成方自检，不是独立评审）。
- 形式证明／充分性证明：not_run；inspect 的 `structure=passed` 只证明引用与无环等结构，不证明精化充分性（本次也没有成立组）。
- 人工接受：pending（模型 `review.status = pending`）。
- 未读取仓库其他目录（development_reference、baselines、benchmarks、extra/output*、其他任务、全过程记录、比较报告），未联网检索论文或参考答案。
