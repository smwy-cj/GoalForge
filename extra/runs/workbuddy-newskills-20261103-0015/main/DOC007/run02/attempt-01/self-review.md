# 自检记录（生成方自检，非独立语义评审）

文档：DOC007（英文访谈转写，86 轮）｜任务：main/DOC007/run02/attempt-01｜执行次数：harness 首跑成功，0 次重跑。

## 1. 生成方自检

**这是生成方自检，不是独立语义评审。** 提取、核验、建模与检查由同一会话完成，独立性不足。

- 候选是否被压薄：按 4 轮/步长 2 的 42 个窗口逐窗捕获，冻结 22 条原始候选，未先压成“主要需求”；寒暄、使用频率、品牌/价格习惯等无意图窗口没有候选。候选允许复合表达（如 C017 的双周流程），整理阶段才拆分。
- 复合拆分：T078 拆为 G004（降低打字点击）与 G005（清单完整性）；T038 拆出 G003（模板）与 C008（详情困难，标 uncertain）；T068 拆出 G006（双周流程）与 C018（模板复述，merge）。T037/T036 的品牌/数量/价格只作实现细节，未机械拆目标。
- 条件、否定、强度：G001 保留“繁忙周/常规补货”条件，并写明不要求移除探索功能（T050 的否定只针对线上随机浏览）；G002 保留“would be cool”、G009 保留“kind of be interesting”、G010 保留“curious”，未升级为强制；G006 保留双周、确认后才下单、取货三个限定；C012 的缺货替换按“现有能力”排除，未反转成新需求。
- 精化组反例：GR1（G003+G006 → G001）只覆盖常规补货的选品与下单，异常场景（新商品/缺货）仍缺搜索、可用性判断与结算，故记为 proposed + partial，异常场景 outcome=counterexample，未作为成立层级展示。
- 是否为凑层级造根：无。G001 有直接原句（“I'm really there for efficiency”），不是为挂子目标而造的抽象根；G007、G009、G010 保持孤立，未强行连边。
- 相反证据：T050 “I'm not interested really in that function” 与 G009 的推荐流设想并存，按情境（例行补货 vs 类目探索）区分，未判冲突，写入问题。

## 2. 工程检查实际结果（复制自 attempt-summary.json）

- coverage_check：exit_code=0，structure=passed，workflow=recorded，pending=[]；source_segments=86，windows=42，raw_candidates=22，final_goals=10，source_checks=10，actual_passes=1；dispositions={merge:6, keep:10, exclude:5, uncertain:1}。
- inspection：structure=passed，readiness=reviewable，independent_semantic=not_run，formal_proof=not_run，human=pending。
- counts：goals=10，relations=7，groups=1，established_groups=0，support_labels={direct:9, inferred:1, insufficient:0, contradicted:0}，issues=13，blocking_issues=0；declared_vs_effective_downgraded=[]，warnings=[]。

## 3. 关系与精化组判断记录（含“已检查但无依据”）

已建立 7 条联系：R1 G003→G001（operationalization）、R2 G004→G001（contribution）、R3 G003→G005（contribution）、R4 G005→G001（contribution）、R5 G002→G001（contribution）、R6 G006→G001（operationalization，proposed）、R7 G008→G001（contribution）。R6 原句只描述流程未说明目的，故标 proposed，未计入成立组依赖。

逐项检查后**未建立联系**的目标对及理由：

1. G002（自动生成清单）↔ G003（清单模板）：同为清单生成手段，但原文未说明彼此替代、先序或共同服务某上层结果；仅同主题，不构成联系。
2. G004 ↔ G005：同段并列的两个结果（操作代价、漏项风险），彼此无帮助关系，不能互为贡献。
3. G007（按使用推荐功能）↔ G003/G004：原文未说推荐是为了让用户找到模板；只共享“功能被埋没”的背景。
4. G009（类目推荐流）↔ G001：适用情境相反（探索 vs 例行效率），原文未说明推荐流服务效率，故不建贡献边，改为问题保留。
5. G008（店铺可用性）↔ G005（清单完整性）：都涉及“漏”，但一为店铺可用性、一为清单条目，原文未连接。
6. G010（数据使用）↔ 其他目标：仅好奇与隐私顾虑，未与任何目标形成手段/目的或先后关系。

精化组：仅评估出 GR1。另检查 G002+G003+G004 是否能共同充分实现 G001——同样缺少搜索、结算与取货，且 G002 与 G003 在“清单来源”上重叠，无法声称充分，故不建第二组；该结论以 model 级问题（target_id=DOC007-goal-model）写入 kaos-decisions.json。成立组为 0 是实际判断结果，未为产出层级造组。

## 4. 未决问题清单

来自 decisions.questions（13 条 issues，0 blocking，均由本清单与 proposed 对象自动派生）：

1. GR1 只覆盖常规补货的选品与下单，遇新商品/缺货缺口明显，是否需要补充搜索/可用性子目标才可能成立。
2. G008 由抱怨推断、原文无直接请求，是否应降为待确认。
3. G006 的功能受访者怀疑已存在但被埋没，目标应保留为流程目标还是改为可发现性目标。
4. G009 与 G001 适用情境不同，是否需显式区分边界。
5. model 级：其余目标对只能找到贡献/方式类联系，无可声称共同充分的组。

来自 review_questions：G003 与 G004 是否应合并；G001 与 G009 是否冲突；G008 依据是否足够；G010 是否应作为产品目标。

无 blocking issue。

## 5. 实际执行情况

- 读原文：完整读 2 遍（逐窗捕获 1 遍，全篇校正 1 遍）；42 个窗口全部 processed，无 skipped。
- 补查：全篇校正阶段回查指代、问答范围、条件继承、让步/例外、相反证据与被排除片段，未发现需要另记 P2 的新候选。
- 修复：harness 首跑前自查发现 2 处引文归属错误（“search bar, and that's it.” 实为 T030 而非 T028；T079 遗漏“for you know,”），已在 spec 内改正后首跑成功；harness 重跑 0 次，未新建 attempt 目录。
- 耗时（自报）：约 25 分钟。停止原因：完成基础提取与全篇校正，补查无新增有据意图，按原文范围停止。

## 6. 没有做的事

独立语义审查 not_run；形式证明 not_run；人工接受 pending（review.status=pending）。本次自检不能替代上述任一环节。
