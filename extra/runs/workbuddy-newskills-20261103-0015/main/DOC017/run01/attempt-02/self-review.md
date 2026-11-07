# 自检与交付记录（DOC017 / run01 / attempt-02）

## 1. 生成方自检（明确：这是生成方自检，**不是独立语义评审**）

- **候选是否被压薄**：未先压成"十几条主要需求"。逐窗（56 个窗口，size=4/stride=2）按达到/维持/避免/改善捕获，
  冻结 59 条原始候选，其中含复合表达（如 C001 领域+技能集、C069 随机通知+陌生人联系），
  整理阶段才拆合。entries 覆盖全部 59 条：keep 43、merge 13、split 1、exclude 2。
- **复合目标是否拆分**：按"一目标一核心动作"整理。拆分例：C006 的"相关/更新"拆为 G006 与 G007；
  C054 拆为 G038 与 G006；C069 相关。合并例：邮件内 direct apply 与门户 quick apply 合并为 G014（同一核心动作，避免重复节点）；
  C021 的四项优先级因素保持为一个目标（同一动作的多限定，不按动词数拆）。
- **条件/否定/强度是否丢失**：保留 while actively looking / when not looking actively（G002/G003）、
  unless too complicated（G010）、6 months / one year（G007）、generally prefer（G009）、
  it's okay to（G003，未升级为必须）、sometimes / few roles（G018）、should not be automatic 与 verified by us（G030）、
  I don't want to expose（G036/G037）、linkedin 帖子方式的让步（G019 vs G020）。
  现有能力/事实（LinkedIn 过滤习惯、市场发布量）标 exclude 或现状，未升级为系统要求。
- **精化组是否有反例未解决**：GR1（G033 ← G016+G032）保留 `proposed/partial`，
  exception 场景明确记为 `counterexample`（门户内查看员工评价/技术栈/职责区块、跟踪状态与反馈等未被子目标覆盖），
  未收回成立、未补造目标扩边。成立组数 0，属正常结果。
- **是否为凑层级造根**：G033（一切在门户内完成）有 T079/T077/T061 反复明确依据，非为画树补的抽象摘要；
  未造根、未固定层数，多根与孤立目标（如 G039 HR）保留。
- **支持判断**：37 direct / 5 inferred / 1 insufficient / 0 contradicted；direct 与 inferred 的
  `unsupported_parts` 均为空；无 downgraded。G043 的 insufficient 如实保留。

## 2. 工程检查实际结果（复制自 `attempt-summary.json`）

```json
"coverage_check": {
  "exit_code": 0, "structure": "passed", "workflow": "recorded",
  "pending": [],
  "counts": {
    "source_segments": 114, "windows": 56, "raw_candidates": 59, "final_goals": 43,
    "source_checks": 12, "actual_passes": 2,
    "dispositions": {"keep": 43, "exclude": 2, "merge": 13, "split": 1}
  }
},
"inspection": {
  "structure": "passed", "readiness": "blocked",
  "independent_semantic": "not_run", "formal_proof": "not_run", "human": "pending"
},
"counts": {
  "goals": 43, "relations": 11, "groups": 1, "established_groups": 0,
  "raw_candidates": 59,
  "support_labels": {"direct": 37, "inferred": 5, "contradicted": 0, "insufficient": 1},
  "issues": 25, "blocking_issues": 1
}
```

补充：`coverage-check.json` 的 `errors=[]`、`pending=[]`；`declared_vs_effective_downgraded=[]`；
`warnings=[]`；`full_context_review.status=completed` 且 `source_ids` 覆盖 T000–T113 全部 114 轮。
`readiness=blocked` 唯一来源是 G043 的 insufficient 产生的 blocking issue。

## 3. 未决问题清单

来自 `review_questions`（提取层）：
1. G012/G013：邮件"very concise"与"All the details are present"的详略边界。
2. G040/G036/G037：填写更详尽资料与申请/数据保密如何同时满足。
3. G043：招聘中介的具体需求未说明，是否需补访谈。
4. G015：T015 转写断裂，快速申请验收标准未给出。
5. G003：每周一次是期望频率还是可接受下限。
6. G023：`what text they are using` 疑为 tech stack 转写错误，需核对录音。
7. G011：缺乏防错过机制的具体依据。
8. G030：`verified by us` 的含义与 AI 边界。
9. G029/G030：AI 识别与不得代写的分界。

来自 `decisions.questions`（模型层）：GR1 充分性未确认；G043 insufficient 需补访谈或排除；
G012/G013 详略张力；G011/G015/G031 的 inferred 与转写缺口；G023 转写歧义；R9 方向依赖 'So' 因果读法；
模型级为单人访谈、多目标来自偏好/现状推断、无交叉验证、成立精化组 0。

来自 blocking issue：`G043 原文尚不足以支持这项目标，或存在相反证据`（blocking=true）。

## 4. 实际执行情况

- **原文阅读**：完整读 `source/DOC017.json` 全部 114 轮（T000–T113）一遍；按 56 个重叠窗口逐窗处理一遍
  （passes：P1 initial + P2 full_context，各覆盖 56 窗口，均 completed）；再做一次全篇校正，
  source_checks 登记 12 处重点回查（含跨轮断裂 T025–T029、让步 T014–T017 / T073、AI 区分 T092–T097）。
- **补查**：是，P2 全篇校正；跨窗断裂片段 T029 另记 pass_id=P2，未伪称首轮发现。
- **修复次数**：语义修正 1 轮；harness 共运行 3 次（第 1 次 coverage 结构失败，第 2 次因中间产物未清理在
  prepare_source 失败，第 3 次成功）。详见 `repair-log.md`。
- **实际耗时（自报）**：harness 单次运行约 10 秒（attempt-summary 的 started_at/finished_at 相差约 10 秒）；
  语义编制、逐窗捕获与全篇校正在本会话内连续完成，未单独计时。
- **停止原因**：已读完原文、覆盖全部窗口并完成一次全篇指代/条件/例外/相反证据校正，
  原文无新增有据意图；剩余未决为需人工或补充访谈的语义缺口，按 `budget` 停止。

## 5. 没有做的事

- 独立语义审查：**not_run**（本文件第 1 节为生成方自检，非独立评审）。
- 形式证明：**not_run**（精化充分性为编制者判断，非程序证明）。
- 人工接受：**pending**（`review` 保持 pending，未替用户采纳）。
- 未读取仓库其他目录、其他 attempt 目录；未联网查找论文或参考答案；未参考任何历史目标/关系/评分。
