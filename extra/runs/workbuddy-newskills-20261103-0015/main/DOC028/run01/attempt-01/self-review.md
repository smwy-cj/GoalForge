# DOC028 自检记录（生成方自检）

> 本文件是**生成方自检**，不是独立语义评审，也不代表人工接受。生成与自检由同一会话完成。

## 1. 生成方自检

- **候选是否被压薄**：未先摘要后提取。34 个窗口逐窗记录 61 条原始候选（含无最终目标的 18 条排除项与 1 条 uncertain），未按"主要需求"压缩；排除项均保留证据与原句位置。
- **复合目标是否拆分**：T003 的三种用途拆为 G001/G002/G003；T033 的"调研 + 影响购买决定"保留为一个动作及其结果（调研的预期结果即购买决定），未机械按动词拆；T035 的"一般健康可用 / 具体健康不信任"拆为 G013/G014，因两者是可独立满足的不同结果且方向相反。
- **条件、否定、强度、方式是否丢失**：
  - 条件：G006（有具体问题才走 Google 入口）、G007（登录前已定义问题）、G017（仅无广告拦截时才买 premium）、G010（Reddit 非主要新闻源、仅关注版或全球事件）、G015（被动/主动两种情境）、G023（相对 wrapper 竞争）。
  - 否定/避免：G011（把新闻排除）、G014（避免用于具体健康问题）、G016/G017 的"有广告拦截则无需 premium"反条件。
  - 强度：G016 明确保留为偏好（原文 "it is better to"），未升级为强制；G012 的"平衡视角"保留为偏好对象而非平台义务。
  - 选定方式：Gen-AI 工具（G019）作为原文明确选定的方式保留为独立目标，而不是只写在解释里；卡/紧凑视图（G015）、Google 加 Reddit 入口（G006）同样进入目标正文。
- **精化组是否有反例未解决**：GR1 只作 proposed/partial，并写入 exception 反例（草稿与评论串修好后，缓慢/笨重/不直观仍在）。未把部分覆盖包装成成立层级。
- **是否有为凑层级造根**：没有。24 个目标无共同根；明确放弃了"比 Google 更有价值"这一候选父目标，因为它只是比较性信念（T005/T015），不是原文表达的目标。
- **insufficient 是否被升级**：没有 insufficient 目标；被判断为弱依据的项（C012 的 may-be 链式结果、C039 离线能力、C061 匿名性）均未升级为目标，而是 exclude/uncertain 并记录理由。

## 2. 工程检查实际结果（复制自 attempt-summary.json）

- coverage_check：exit_code=0，structure=`passed`，workflow=`recorded`，pending=[]；
  counts：source_segments=70，windows=34，raw_candidates=61，final_goals=24，source_checks=12，
  actual_passes=2，dispositions={keep:24, merge:18, exclude:18, uncertain:1}。
- tracing：status=`completed`，declared_vs_effective_downgraded=[]。
- inspection：structure=`passed`，readiness=`reviewable`，independent_semantic=`not_run`，formal_proof=`not_run`，human=`pending`。
- counts：goals=24，relations=5，groups=1，established_groups=0，support_labels={direct:24, inferred:0, insufficient:0, contradicted:0}，issues=8，blocking_issues=0。
- warnings：无（无 ambiguous/not_found 引文）。

## 3. 关系与精化组判断（重点说明，已实际执行）

关系：逐对检查后仅建立 5 条，均 supported（两端目标 direct，各有一条定位到原文的关系原句）：

| ID | 方向 | 类型 | 依据 |
|---|---|---|---|
| R1 | G006→G004 | operationalization | T007 把"有具体问题"与走 Google 加 Reddit 入口直接绑定 |
| R2 | G003→G007 | specialization | T003 技术求助为"卡住"时的具体情境；T009 说明该会话结果为问题解决 |
| R3 | G001→G004 | operationalization | T003 关键词检索是把结果限定到话题的做法；T005 说明目的是针对性结果 |
| R4 | G019→G018 | operationalization | T059 明确用 Gen-AI 工具找具体 subreddit |
| R5 | G018→G020 | contribution | T059 把"发在具体版更有价值"与"找到该版很有用"连写 |

已检查但无依据（故不建边，理由同步写入 kaos-decisions.json 的 model 级问题）：

- G002 与 G007：T009 明确把两种模式并列（无预设结果 / 有预设问题），是互斥使用情境，不是具体化、贡献或先后。
- G005 与 G012：都涉及"他人经验"，但一个是信息质量准则、一个是购前调研活动，仅同主题；原文没有把前者作为后者手段的句子。
- G010 与 G011：趋势跟进与新闻排除方向相反，属范围划分而非帮助；硬连边会把相反倾向说成支持。
- G016 与 G017：同一偏好的条件化行动，条件已写入 G017，另建边属重复。
- G022 与 G023 / G021 与 G023：子目标与父目标已由 GR1 表达，避免用 contribution 重复表达层级。

精化组：仅 GR1（parent=G023，children=G021、G022），status=proposed、completeness=partial，含 normal（supports）与 exception（counterexample）两条分析假设场景，relation_ids=[]（组内无可依赖联系）。

已检查但不成立（理由同步写入 model 级问题）：

- G004+G005+G008：缺少"比 Google 更有价值"的父目标；该表述是信念/比较判断，造父目标会违反"不为凑层级造根"。
- G018+G020：已是目的—手段链（R5），二者不共同满足另一个父目标，不构成 AND 组。
- G013+G014：一为取得一般信息、一为避免具体问题，方向相反，不能共同满足同一父目标。
- G021+G022+其它移动端缺陷：正是 GR1 的反例来源，故只作部分覆盖。

## 4. 未决问题清单

来自 review_questions / decisions.questions（均为非阻断）：

1. C012：浏览中读到感兴趣内容后"继续在 Reddit 深挖"以 `might be` 描述，未建目标，是否需补充。
2. G023：移动端改进是否需明确必须解决的缺陷范围（草稿、评论串、性能、直观性）。
3. GR1：移动端体验是否只由草稿保存与评论串跟踪构成；当前只作部分覆盖。
4. G002：`no particular outcome` 的浏览是否算目标而非背景行为。
5. G011：新闻与趋势的边界（关注版内事件、popular 页全球事件 vs 其它新闻）是否稳定。
6. 转写噪声：`credit`/`edit` 指 Reddit；"I've never posted something on reddit" 与后文 "posts that I've done" 矛盾；发帖量未用于任何目标判断。

## 5. 实际执行情况

- 原文读取：完整通读 70 轮 1 遍（逐轮），随后按 34 个窗口（size=4, stride=2）逐窗捕获，最后全篇回查 1 遍（指代、条件继承、例外、相反证据）。共 2 个 pass（P1 初始、P2 全篇校正）。
- 补查：针对 T003/T005/T007/T009/T025/T027/T031/T033/T035/T045/T047/T051/T059/T061/T063 逐条回读原句；对 G002/G010/G011/G018/G019/G020/G023 的合并与拆分做了反向回查（该意图现落在哪个目标）。
- 修复/重跑：1 次。首次 harness 已成功（无报错、无降级），随后发现 G002 的主候选处置标为 merge 而非 keep（24 个最终目标中唯一无 keep 来路者），修正 C002 处置后在同一 attempt 目录清理生成物并重跑。未新建 attempt 目录，未改动任何原文或判断标签。
- 耗时：自报约 10 分钟（10:29 建目录 → 10:38 交付；未精确计时）。
- 停止原因：基础窗口与全篇校正均完成；关系与组判断已执行；剩余 5 项不确定点无新证据可解，按限制保留后停止。

## 6. 没有做的事

- 独立语义审查：not_run（本文件为生成方自检）。
- 形式证明（精化充分性/完整性）：not_run，工具结构检查不证明语义充分。
- 人工接受：pending；未把"未反对"当作采纳。
- 未读取任务目录与冻结技能目录之外的任何文件；未联网检索论文或参考答案。
