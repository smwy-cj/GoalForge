# 自检记录（生成方自检，非独立语义评审）

> 本文件由**生成方**在完成 spec 与 harness 运行后自检编制。它不是独立语义审查、不是形式证明，也不代表人工采纳。

## 1. 生成方自检

- **候选是否被压薄**：原始候选 46 条，逐窗（4/步长2，共 51 窗）捕获后未先做“主要需求”摘要。T015 的完整流程（入口→扫视→标星→删除→阅读→打标签）、T017 的两条收纳策略、T037 的三个功能、T087 的三项排序、T093 的分类协议设想均按原句分别落条目。
- **复合是否拆分**：拆了 T015（删邮件 / 打标签待办分开）、T071（转邮件 / BCC 群发分开，二者可独立满足）、T091（写 / 读两类 AI 辅助分别由 G009、G016 承接）；未拆 T021（字号与加粗为同一封邮件排版）、T017（两种删除触发属同一删除动作的限定）、G024（分类地址与其通信结果属一个机制）。
- **条件/否定/强度是否丢失**：保留“rarely”（G005）、“would rather receive spam”（G012）、“would be good / not rely unless really reliable”（G019）、“probably not that practical”（G024）、“very important when working to a deadline”（G020/G021）、“at least five times a day, ten to twenty in practice”（G001 condition）、“instead of sending a new one”（G013）、“instead of attaching”（G011）、“built into the client”（G009）。
- **精化组反例**：GR1 已记录例外场景（关键小字既不在摘要也不在关键词内，T047 例子），因此只作 proposed + partial，未进入成立层级；成立组数为 0。
- **是否造根**：未新增泛化根目标；G018（减少读信时间）来自 T053 的明确陈述，不是为挂子节点而造。T049/T051 的查看频率并入 G001 条件，未单列为行为目标；T061/T063 的“很少崩溃/满意”只作现状，未造维持目标。
- **未采纳但保留的信息**：T054 周期摘要（面试官提议、弱回应）记为 uncertain 并进入模型问题；T087 标签过滤记为 exclude（受访者称可由搜索完成），判断写入 G022 条件。

## 2. 工程检查实际结果（来自 attempt-summary.json）

- `coverage_check`：exit_code 0，structure=`passed`，workflow=`recorded`，pending=[]；counts：source_segments=104、windows=51、raw_candidates=46、final_goals=24、source_checks=11、actual_passes=1；dispositions：keep 20 / merge 15 / exclude 8 / split 2 / uncertain 1。
- `inspection`：structure=`passed`，readiness=`reviewable`，independent_semantic=`not_run`，formal_proof=`not_run`，human=`pending`。
- `counts`：goals=24，relations=2，groups=1，established_groups=0，issues=12，blocking_issues=0。
- 有效支持分布：direct 23 / inferred 1（G014）/ insufficient 0 / contradicted 0；`declared_vs_effective_downgraded`=[]，`warnings`=[]。
- `tracing_status`=completed；windows：51 个，size=4，stride=2。

## 3. 未决问题清单

1. GR1（G018←G016、G017）：“要点摘要 + 关键词高亮”是否足以减少通读时间；T047 的漏读小字是未解决反例，目前 proposed/partial。
2. G019：自动识别重要邮件需达到何种可靠性才可依赖，原文只说“除非它真的可靠”，无阈值与降级方案。
3. G024：分类/协议邮箱地址是否推进，受访者自评“probably not that practical”，采纳程度未知。
4. G013：发送后可编辑的时限与范围（是否任何时间、历史是否对所有收件人可见）原文未说明。
5. 模型级：T054 的周期摘要（早/午/晚 3 封汇总 30 封）仅为面试官提议 + “可以是其中一种方案”，是否纳入需求未定。
6. G001 与 G019 的关系：T049 的高频查看与 T059 的通知意愿之间没有原文连接，未建联系。

## 4. 实际执行情况

- 原文读取：完整读 `source/DOC020.json` 全部 104 轮 1 遍；随后按 51 个重叠窗口逐窗处理（等价于窗口级第二遍回读），并对全篇做一次指代/条件/例外校正回查（T039→T041→T043、T049→T051、T059、T047→T053）。
- 补查：无独立定向补查轮次；发现的跨窗关系（T053 支撑 R1、T027 支撑 R2）在首轮窗口内已见，仍按全篇校正复核，未另记 pass_id。
- 修复次数：0（首次 harness 运行即通过，无降级、无 blocking issue，故未生成 repair-log.md，也未新建 attempt-03）。
- 实际耗时：自报约 40 分钟（单次会话，含技能阅读）。
- 停止原因：一次基础提取 + 全篇校正完成，全部窗口 processed，无新证据可解决的未决项，按语义边界保留问题后停止。

## 5. 没有做的事

- 独立语义审查：not_run（本次自检由生成方完成，不构成独立评审）。
- 形式证明：not_run（精化充分性仅为编制判断，工具只验证结构与绑定）。
- 人工接受：pending（review 状态保持 pending，未替用户采纳）。
- 未联网检索论文/案例答案，未读取任务目录与冻结技能之外的仓库内容。
