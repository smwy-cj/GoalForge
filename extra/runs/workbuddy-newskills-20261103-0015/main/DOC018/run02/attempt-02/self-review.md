# 自检记录（DOC018 / run02 / attempt-02）

> 本节是**生成方自检**，由编制 spec.json 的同一个会话完成，**不是独立语义评审**，也不代表人工接受。

## 1. 生成方自检

### 1.1 候选是否被压薄

- 按 4 轮窗口 / 步长 2 逐窗处理 34 个窗口（70 轮全覆盖），共 17 条原始候选，未先做“主要需求”摘要。
- 有明显意图但没有进入目标的三处都保留了候选与去向：T011 的 Kindle 网页版设想（C001，exclude）、T015 的新闻试用模式（C002，exclude）、T019 的下载-Drive-Adobe 现有流程（C003，exclude）。
- T037 一轮含三个可独立满足的结果（减少步骤 / 导出到 Drive / 一个地方容纳两种格式），分别建成 G001/G002/G003，未压成一条。
- 边界项 C012（Kindle 已有“本章剩余时间”）记为 uncertain，未强行造维持目标，也未直接删除。

### 1.2 复合目标拆分与条件传递

- C008（同一应用支持 PDF 与 ebook、在一个地方打开）与 C007（阅读散落多处）合并为 G003，把“必须同时支持两种格式”“至少覆盖学校材料”“新闻网页是否纳入未定”写进 statement/context，没有把 AND 改成 OR。
- C010（门户导出）并入 G002，导出目的地保留为“Google Drive / Kindle 账户 / 独立应用”的未定选择，未把其中任一写成强制。
- C009（Kindle 应用管理 PDF）保留“it will be easier”的比较性偏好强度，没有升级为“必须”。
- G008 保留 T057 的设想语气（in my imagination / would be interesting），未写成已采纳方案。

### 1.3 条件、否定、强度是否丢失

- 保有：iPad 为主设备、课程门户为 Canvas 类网站、课程结束后材料不可访问这一条件。
- 保有否定/限制：PDF 目前不能转到 Kindle（T023）作为 G004 的 context。
- 保有强度：G009 的“They should be included”保留犹豫（I don't know），未写成明确商业要求。
- 保有排序但不升级：T055 的功能排序（导出第一 / 保存第二 / 时间筛选第三 / 章节百分比第四）写入各目标 judgment.rationale，未被当作强制或精化依据。

### 1.4 精化组是否有反例未解决

- 只有 1 个候选组 GR1（G003 ← {G002, G004}），状态 proposed / partial，未进入成立 DAG。
- 反例已显式记录：新闻阅读仍在官网、导出目的地可能是 Drive 而非阅读应用、学校自建应用（G008）可能取代导出。这些反例正是该组不能标 supported/complete 的原因。
- 未为凑层级造根目标：9 个目标均为原文明示，无泛化上层节点。

### 1.5 关系方向

- R1 G002→G001（contribution）：导出服务于减少步骤，方向为“手段帮助目的”。
- R2 G004→G003（operationalization）：Kindle 管 PDF 是实现“一个地方”的方式。
- R3 G002→G003（contribution）：导出到唯一目的地有助于集中，不声称充分。
- R4 G008→G001（operationalization）：学校自建应用直投文章服务于减少步骤。
- 未把操作先后当精化，未给同主题目标连边（如 G006 与 G005 仅在“以后找回”上相邻，未建立联系）。

## 2. 工程检查实际结果

- windows：34 个，size=4 / stride=2。
- coverage_check：exit_code=0，structure=passed，workflow=recorded，pending=[]；counts：source_segments=70，raw_candidates=17，final_goals=9，source_checks=12，actual_passes=1，dispositions={keep:9, merge:4, exclude:3, uncertain:1}。
- tracing：status=completed，declared_vs_effective_downgraded=[]，warnings=[]。
- inspection：structure=passed，readiness=reviewable，independent_semantic=not_run，formal_proof=not_run，human=pending。
- counts：goals=9，relations=4，groups=1，established_groups=0，issues=6，blocking_issues=0；支持分布 direct=9 / inferred=0 / insufficient=0 / contradicted=0。

## 3. 未决问题清单

来自 `review_questions` 与 `decisions.questions`（均非 blocking）：

1. G007：章节百分比针对新阅读应用还是现有 Kindle 应用（T049 说 this application，T055 说 more for application）。
2. 整体（原 C012）：现有 Kindle 的“本章剩余时间”是否要在新应用中保留，只有正面评价与 T065 的概括认可。
3. GR1：G002 的导出目的地未定，能否把它当作通向“一个地方”的稳定手段。
4. G008：学校自建阅读应用与门户导出功能是替代还是并存，T057 仅为设想语气。
5. G009：“They should be included”的包含范围（学费已含 / 仅不愿额外付费）不明确。

模型自动附带的一条信息性问题：GR1 尚未作为成立精化展示（与第 3 条同源）。

## 4. 实际执行情况

- 读原文：1 遍完整通读（70 轮），随后按 34 个窗口逐窗核对，并做 1 次全篇校正（指代、条件继承、例外、相反证据、采访者汇总的确认范围）。
- 补查：无新增 pass；全篇校正未发现需另记 P2 的新候选，已把边界项记入 uncertain/exclude。
- 修复：本次 attempt 内 3 次 harness 调用（2 次失败、1 次成功），详见 `repair-log.md`。
- 耗时：约 30 分钟（自报，含读 3 个技能与 70 轮原文）。
- 停止原因：完成一次全篇分窗捕获与全篇校正，无新证据支持更多目标，按预算停止。

## 5. 没有做的事

- 独立语义审查：not_run（本文件只是生成方自检）。
- 形式证明（精化充分性/完整性）：not_run，inspection 的 note 也明确说明。
- 人工接受：pending，所有目标与关系均待审。
- 未读取任何参考模型、历史目标、评分或外部论文资料。
