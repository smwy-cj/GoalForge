# self-review（生成方自检）

**本文件是生成方自检，不是独立语义评审。** 生成、核验、自检由同一会话完成；没有独立评审者，也没有形式证明与人工接受。

## 1. 生成方自检

### 1.1 候选是否被压薄

- 原文 65 轮全部读取（T000–T064，T020/T022 曾被阅读工具截断，已单独完整读取）。按 4 轮窗口、步长 2 生成 32 个窗口，逐窗捕获，共 65 条原始候选（`raw_candidates`）；其中 4 条为 P2 全篇校正补记（C063–C065 及 C006 的复核），未伪称首轮已发现。
- 保留了"没有目标"的窗口（W0001/W0003/W0005/W0007/W0013/W0017/W0021/W0024/W0028/W0031/W0032 等仅寒暄、复述或追问），未为凑数造候选。
- 处置分布：keep 32、merge 18、split 1、exclude 13、uncertain 1。13 条排除均给出可核对理由，并集中登记在 14 条 `source_checks`（S1–S14）中，包括 3 条明确判"采访者用词/研究目的"不转为涉众目标的项（C063、C064）与 4 条"现状/描述性使用"项（C002、C003、C040、C044）。

### 1.2 复合目标是否拆分

- T024 一次回答含首要/次要/第三层四类结果 → G001–G004，保留 primary/secondary/tertiary 的层次用语。
- T028 理想体验一句含五个结果 → G010、G013、G012（+G014 为 or 并列方式）、G007；`or` 保留为替代，未写成同时要求。
- T032 典型会话 → 查看订单并入 G019、下单并入 G012（C043 记 split）、自选股 G018、组合页 G017；PIN 登录与账户账单页按无意图排除。
- T022 决策过程 → 判断维度 G020 与三类决策动作 G021/G022/G023（例外 G023 单列），小市值下跌仍持有的例外未被撤出规则吸收。
- T020 长期/规避/蓝筹/配置比例 → G024–G027 分列，未把"规避高波动"与"股票投入远高于加密"合并成一条。

### 1.3 条件、否定、强度是否丢失

- 强度/不确定性逐条留在 `context`：`I am not sure of this`（G005）、`I don't know if they have done it now`（G006）、`I'm not sure how feasible it is / if that is their goal`（G028）、`if it is possible`（G029/G030）、`mostly not intraday`（G024）、`I don't use it a lot`（G018）、`I would be inclined to`（G021）、`unless and until ... mind blowing feature`（G032）。
- 条件保留：监管限制与印度客户情境在 G012 的 context；3/6 个月观察窗口在 G020；加密约两周复盘在 G015；`I was not able to do that` 的缺口在 G011。
- 否定保留：G025 为避免型目标，未反写成零加密持仓（与 G026 正向买入并存）；未把 G032 写成绝对不换应用。

### 1.4 精化组是否有未解决反例

- 本轮 **groups = 0**，无成立组亦无候选组。理由已写入 `decisions.questions`：T058 的语音下单/语音摘要是 `or` 替代，不构成 AND 共同充分；G005/G006 对 G002/G003 只是"实现方式之一"，不满足"整组共同满足即足以实现父目标"。
- 未为产出层级造根目标：33 个目标全部为多根，未新增"提升投资体验"之类泛化父节点。

### 1.5 是否有为凑层级/边数造对象

- 关系 12 条，均为原句可指认的类型联系（operationalization 5、contribution 3、precedes 1、specialization 1、operationalization(proposed) 2），其中 3 条因依赖推断或不确定记为 `proposed`，未硬标 `supported`。
- 主动放弃了若干"同主题但无方向依据"的连边（如 G012 与 G019、G013 与 G020、G003 与 G004），也放弃了"已实现=维持要求"的推断（C003、C040、C044）。

### 1.6 已知薄弱处（自查）

- G008（新闻正/负标记）与 G009（依赖外部新闻）为 inferred，依据是对 Coinbase 功能的正面描述与"99% 是新闻"，属推断而非明确要求。
- G033（通用易用性）与 G010/G012 的易用条件可能有重叠，已登记为问题。
- G019（查看已下订单）为 inferred，原文只是描述典型会话。
- G028→G001、G027→G025 两条联系为 proposed，依据为隐含关联。

## 2. 工程检查实际结果（取自 attempt-summary.json）

```json
coverage_check = {"exit_code": 0, "structure": "passed", "workflow": "recorded", "pending": [],
 "counts": {"source_segments": 65, "windows": 32, "raw_candidates": 65, "final_goals": 33,
            "source_checks": 14, "actual_passes": 2,
            "dispositions": {"keep": 32, "merge": 18, "split": 1, "exclude": 13, "uncertain": 1}}}

inspection = {"structure": "passed", "readiness": "reviewable",
              "independent_semantic": "not_run", "formal_proof": "not_run", "human": "pending"}

counts = {"goals": 33, "relations": 12, "groups": 0, "established_groups": 0, "raw_candidates": 65,
          "support_labels": {"direct": 30, "inferred": 3, "insufficient": 0, "contradicted": 0},
          "issues": 15, "blocking_issues": 0}
```

- `downgraded = []`、`warnings = []`：声明的 direct/inferred 未被工具降级，`unsupported_parts` 均为空。
- 32 个窗口在两个 pass 中均记为 processed；无 skipped。
- 引文全部逐字符匹配（合并前用脚本对 65 条候选、33 个目标、14 条回查、12 条关系共约 130 处 quote 做过 `in` 校验），同一 turn 内无多义命中告警。

## 3. 未决问题清单

模型 `issues` 共 15 条（0 blocking），来源：
- `review_questions` 8 条：C015（印度版功能是否为目标）、C002（在美交易）、C003（维持使用 Binance）、C044（账户账单页）、G025（规避波动 vs 接受全损）、G008（正负标记是否明确要求）、G033（易用性是否单列）、G009（外部新闻是否维持目标）。
- `decisions.questions` 4 条：模型级 2 条（无 AND 精化组；T032 描述性页面的漏提风险）、G012（采访者"绕过监管"措辞未采纳）、R10（具体化方向待确认）。
- 工具自动生成的 3 条 proposed 关系提示（R10、R11、R12）。
- 覆盖检查另标 `uncertain_candidate_ids = ["C015"]`。

## 4. 实际执行情况

- 读原文：通读 2 遍（第一遍按轮次完整读取，含单独补读 T020/T022 全文；第二遍为全篇校正 P2，逐窗回看指代、条件继承、例外与相反证据）。
- 窗口：32 个，4/步长 2，两遍均全部处理，无 skipped。
- 补查：P2 期补记 3 条候选（C063 采访者目的、C064 采访者措辞、C065 加密复盘频率），另把 C006 归入过去事实并排除。
- harness 运行：4 次（2 次失败后修正重跑，1 次成功，1 次为去重后最终成功），未新建 attempt 目录，详见 `repair-log.md`。
- 耗时：自报约 45 分钟（含技能阅读、逐窗捕获、引文脚本校验与 4 次 harness 运行）。
- 停止原因：全部窗口处理完、全篇校正无新增有据意图、无新证据可解未决项，按预算停止。

## 5. 我没有做的事

- 独立语义审查 **not_run**（同一会话的生成方自检不算独立评审）。
- 形式证明 **not_run**（结构无环与检查通过不证明精化充分性或可实现性）。
- 人工接受 **pending**（未向用户征求分项意见，`review` 保持 pending）。
- 未读取任何参考答案、历史目标、开发参考或比对报告，未联网检索论文或案例答案。
