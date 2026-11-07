# 统一任务说明（task-prompt-v1）

你是一个**隔离的生成会话**，只负责一个 GoalForge 任务。除了本文件指定的材料，不要读取仓库中任何其他内容。

## 1. 你能看到的材料

- 你的任务目录（当前工作目录）：`D:/Desktop/summer_pro/GoalForge/GoalForge/extra/runs/workbuddy-newskills-20261103-0015/main/DOC031/run02/attempt-01`
- 分配的原文：`D:/Desktop/summer_pro/GoalForge/GoalForge/extra/runs/workbuddy-newskills-20261103-0015/main/DOC031/run02/attempt-01/source/DOC031.json`（唯一输入资料）
- 冻结技能：`D:/Desktop/summer_pro/GoalForge/GoalForge/extra/runs/workbuddy-newskills-20261103-0015/versions/skills/`（只读，可读 SKILL.md 与 references，不改）
- 本说明：`D:/Desktop/summer_pro/GoalForge/GoalForge/extra/runs/workbuddy-newskills-20261103-0015/main/DOC031/run02/attempt-01/brief.md`
- 你的输出目录：`D:/Desktop/summer_pro/GoalForge/GoalForge/extra/runs/workbuddy-newskills-20261103-0015/main/DOC031/run02/attempt-01/` 下的各文件

**禁止**：读取仓库其他目录（尤其 `datasets/processed/goalforge-v1/development_reference/`、`datasets/baselines/`、`datasets/benchmarks/`、`extra/output*`、`extra/runs` 其他任务、`全过程记录.md`、论文比较报告）；不联网查论文或案例答案；不参考任何历史目标、关系或评分。

## 2. 任务

> 依据分配的完整原文，使用冻结的三个 skills，完成目标提取、证据核验、目标建模、模型检查及交付。保留原文的主体、条件、否定、强度、例外和明确选定的方式。不参考历史答案，不追求特定目标数量、连边数量或精化组数量。

原文是英文访谈转写。**目标表述（statement/raw candidate）用英文，与原文同语言**；理由、问题、限制用中文。

## 3. 必读技能文件（按序，只读）

1. `versions/skills/goal-extraction/SKILL.md`
2. `versions/skills/goal-extraction/references/`：`input-processing.md`、`extraction-strategy.md`、`goal-boundaries.md`、`coverage-contract.md`、`output-contract.md`、`evidence-rules.md`、`semantic-judgments.md`、`tracing-contract.md`
3. `versions/skills/goal-model-building/SKILL.md` 与其 `references/`：`relation-discovery.md`、`modeling-rules.md`、`output-contract.md`、`tools.md`
4. `versions/skills/model-review/SKILL.md` 与其 `references/semantic-review.md`

## 4. 你的实际工作

### 4.1 读原文、逐窗捕获候选

先读完整原文（`source/DOC031.json` 的 `turns`：`source_id`、`speaker`、`text`、`start_char`、`end_char`）。按 4 轮窗口/步长 2 的顺序处理（窗口文件由工具生成，你可在 `work/source-windows.json` 读到同样的窗口与坐标）。

每个窗口都要真实处理：捕获一切达到、维持、避免、改善某状态的意图，**不要先压缩成十几条“主要需求”**，不设数量上限。没有意图的窗口可以没有候选。

允许原始候选是复合表达（一句话里有多个结果就先整条捕获）。`evidence` 引文必须是该 `source_id` 对应 `text` 中的**精确子串**（逐字符一致，含负面词、条件词），尽量取足以判断语义的完整句子。

### 4.2 全篇校正

回看指代、问答范围、条件继承、让步、例外、相反证据。窗口不是语义裁决边界。跨窗证据可引用多个窗口。补查发现的候选要另记 `pass_id`（如 `P2`），不要伪称首轮已发现。

### 4.3 整理最终目标：一目标一核心动作及其预期结果

- 独立动作有独立意图依据 → 拆成不同目标；操作步骤、前提、同一对象的多个限定 → 不机械拆。
- 保留主体、对象、条件、否定、强度（must/usually/prefer/not sure）、时间、数量、明确选定的方式。
- 状态、维持、避免、质量意图保留（不要因为没动词就删）。
- 已实现能力不自动成为要求；偏好不自动变强制；信念不当事实；抱怨不自动证明障碍。
- 不为凑层级造根目标。

### 4.4 覆盖记录

每个原始候选**恰好一条** `entries`，`disposition` ∈ keep/merge/split/exclude/uncertain，给简短可核对理由。每个最终目标必须有原始候选来路。

`source_checks` 只登记你实际回查的重要片段（重要原句、合并簇、被排除项、不确定项），`outcome` ∈ represented/excluded/uncertain。

`full_context_review.status` 写实际状态；`passes` 要覆盖**全部窗口**（每个窗口一条 `processed`/`skipped` 记录，skipped 必须写理由）。

### 4.5 语义判断

每个目标一条：`label` ∈ direct/inferred/insufficient/contradicted，`rationale` 非空。

**重要**：`label` 为 direct 或 inferred 时，`unsupported_parts` 必须为空数组；否则工具会把有效支持降为 insufficient 并记 blocking 问题（届时你需修正或接受降级）。不支持的缺口写进 `rationale` 或改判 insufficient。

分别核对：位置命中 ≠ 语义支持；主体/范围/条件/强度/方式/来源版本逐项看。

### 4.6 建模

**先**判断独立联系（可为 0 条）：

- `specialization` 具体情境目标 → 一般目标
- `operationalization` 实现方式/策略目标 → 所服务的目的
- `contribution` 有帮助的目标 → 受帮助的目标
- `precedes` 先发生的结果 → 后发生的结果

方向不要写反；`supported` 要求两端目标支持为 direct/inferred，否则写 `proposed`。每项要一条实际关系原句作为 `evidence_quotes`（`source_id` + 精确 `quote`）。不为了连边造节点，相关/相似/同主题不构成联系。

**再**单独判断 AND 精化组：

- 只在能声称“这组子目标共同满足足以实现父目标”时才建组。
- `status=supported` + `completeness=complete` 需要：至少一条 normal 和一条 exception 场景检查，全部 `outcome=supports`，所有目标支持有效，所有 `relation_ids` 联系为 supported。
- 不足就写 `proposed` + `partial`，并把缺口写进 `checks`/`questions`。不为增加边数扩写目标。
- 父子方向：`parent_id` 是上层目标，`child_ids` 共同满足它。精化图必须无环。

没有成立组是完全正常的结果，不要为了产出层级硬造。

## 5. 执行方式

在工作目录写 `spec.json`（语义内容由你编制），然后运行：

```
python "D:/Desktop/summer_pro/GoalForge/GoalForge/extra/runs/workbuddy-newskills-20261103-0015/logs/harness.py" "."
```

harness 只做模板、偏移定位、契约绑定和工具调用（prepare_source → 覆盖检查 → trace → kaos assemble/inspect/finalize --svg），不会替你编造语义。它会打印每个目标的**有效支持标签**；若出现 `downgraded`，说明你声明的 direct/inferred 被工具降级，需按 4.5 修正后重跑（新 attempt 目录，见第 7 节）。

失败时读 `attempt-summary.json` 的 `commands[].stderr` 定位，只修被点名的引用/记录/判断，不做无关改写。

## 6. spec.json 结构

```json
{
  "document_id": "DOC031",
  "raw_candidates": [
    {"candidate_id": "C001", "statement": "英文原句意涵（可复合）", "actor": "Stakeholder",
     "modality": "原语气简述，未知写 unknown", "context": [], "origin": "explicit|inferred|unknown",
     "pass_id": "P1",
     "evidence": [{"source_id": "DOC031:T012", "quote": "逐字符精确子串", "role": "basis"}]}
  ],
  "goals": [
    {"candidate_id": "G001", "statement": "英文，一个核心动作及其预期结果", "actor": "Stakeholder",
     "context": ["必要条件"], "origin": "explicit|inferred",
     "inference": null,
     "evidence": [{"source_id": "DOC031:T012", "quote": "精确子串", "role": "basis"}],
     "judgment": {"label": "direct", "rationale": "中文理由", "supported_parts": [],
                  "unsupported_parts": [], "assumptions": [], "reasoning_steps": []}}
  ],
  "review_questions": [{"candidate_ids": ["G001"], "question": "中文问题", "reason": "为什么"}],
  "limitations": ["实际读取或判断限制"],
  "ledger": {
    "model": "unknown", "temperature": "unknown", "budget": "1 initial pass + <=2 repair rounds",
    "usage": "unknown", "skill_revision": "<manifest tree_sha256>", "prompt_revision": "task-prompt-v1",
    "planned_passes": 1, "stop_reason": "中文停止原因",
    "passes": [{"pass_id": "P1", "kind": "initial", "context": "isolated", "status": "completed",
                "window_results": [{"window_id": "DOC031:W0001", "status": "processed", "reason": ""}]}],
    "full_context_review": {"status": "completed", "reason": "中文说明回查范围"},
    "entries": [{"candidate_id": "C001", "disposition": "keep", "final_goal_ids": ["G001"], "reason": "中文理由"}],
    "source_checks": [{"check_id": "S1", "evidence_candidates": [{"source_id": "DOC031:T012", "quote": "精确子串"}],
                       "candidate_ids": ["C001"], "final_goal_ids": ["G001"],
                       "outcome": "represented", "reason": "中文理由"}]
  },
  "decisions": {
    "relations": [{"relation_id": "R1", "source_id": "G002", "target_id": "G001",
                   "type": "contribution", "status": "supported", "conditions": [], "assumptions": [],
                   "rationale": "中文理由", "evidence_ids": [],
                   "evidence_quotes": [{"source_id": "DOC031:T020", "quote": "精确子串", "role": "basis"}]}],
    "groups": [{"group_id": "GR1", "parent_id": "G001", "child_ids": ["G002", "G003"],
                "kind": "and", "status": "proposed", "completeness": "partial",
                "rationale": "中文理由", "assumptions": ["至少一条"], "evidence_ids": [],
                "evidence_quotes": [{"source_id": "DOC031:T030", "quote": "精确子串", "role": "basis"}],
                "relation_ids": [],
                "checks": [{"kind": "normal", "origin": "analysis_assumption", "scenario": "中文场景",
                            "outcome": "supports", "rationale": "中文理由"}]}],
    "questions": [{"target_type": "goal|group|relation|model", "target_id": "G001", "message": "中文问题"}],
    "reassessments": []
  }
}
```

补充约束：

- `evidence` 的 `quote` 必须存在于该 `source_id` 的 `text` 内；同一 turn 内多处命中会触发 `ambiguous` 警告，尽量引足上下文使其唯一。
- `inference` 非空时结构为 `{"basis_candidate_ids": ["G001"], "reason": "…", "assumptions": ["…"]}`，引用必须指向本任务已有的 candidate_id。
- 原始候选可引用最终目标 ID 之外的内容；`basis_candidate_ids` 指向目标集合。
- `skill_revision` 填 `versions/manifest.json` 的 `tree_sha256`。
- 允许 `decisions.relations` 与 `groups` 为空数组。

## 7. 修复与重试

首次 harness 失败或出现降级：**不要**改 `attempt-01/` 里已生成的产物。复制 `spec.json` 到 `attempt-02/`，修正后重跑；最多到 `attempt-03`。每次在 `attempt-0N/repair-log.md` 写：触发原因、改了哪些对象、理由。

## 8. 自检与交付记录

harness 成功后，在 attempt 目录写 `self-review.md`，内容包括：

1. 生成方自检（**明确标注这是生成方自检，不是独立语义评审**）：候选是否被压薄、复合目标是否拆分、条件/否定/强度是否丢失、精化组是否有反例未解决、是否有为凑层级造根。
2. 工程检查实际结果：复制 `attempt-summary.json` 的 `coverage_check`、`inspection`、`counts`。
3. 未决问题清单（来自 `review_questions`、`decisions.questions`、blocking issue）。
4. 实际执行情况：读了几遍原文、是否补查、修复次数、实际耗时（自报）、停止原因。
5. 你**没有**做的事：独立语义审查 not_run、形式证明 not_run、人工接受 pending。

## 9. 结束时回报

只回一段简短结论：goals / relations / groups（成立组数）/ 有效支持分布 / coverge 与 inspection 结果 / 修复次数 / 主要未决问题。不要复述全文，不要评价新旧优劣。
