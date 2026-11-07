# self-review（生成方自检）

> 本文件是**生成方自检**，由同一生成会话编写，不是独立语义评审，也不构成形式证明或人工接受。

## 1. 生成方自检

- **候选是否被压薄**：35 条原始候选逐窗捕获（P1，24 个窗口全部 processed），未先压缩成"主要需求"。每窗至少给出处置理由，无候选的窗口（W0001/W0004/W0010/W0011/W0018/W0021–W0024）为寒暄、提问或访谈流程语句，已在窗口记录中标记 processed。
- **复合目标是否拆分**：拆了 6 处——T006 分为观众侧屏蔽（G006）与 streamer 禁分享（G007）；T012 分为定位（G001）、可视化浏览（G002）、创建/上传/开播（G003）、描述与字幕（G004）、剪辑（G005）；T014 分为模糊检索相关性（G008）与播放不卡顿（G009）；T030 分为观看列表（G021）与订阅（G022）；T032 分为高级档权益（G018）、方案组合（G019）、选择与付款（G020）。不拆的：G001 内 text search/filters 为同一动作的替代方式，G003 内上传/开播为替代，G005 内音效/裁剪/切割为同一编辑动作的限定，G019 内三种方案为同一订阅产品的限定。
- **条件/否定/强度是否丢失**：保留 `must`（G006/G007 的 have to / should not be allowed）、`essential`（G001）、`very useful`（G005）、`perhaps`（G004 字幕可选）、`not sure`（G016/G017）、`could be grounds for some work`（G017 建议强度）、`24 h` 与 `only`（G023）、`up to 5 members` / `1 month free trial`（G019）。T018 的三处反问未被升级为 must，分别标 inferred 与 insufficient。
- **是否有相反证据未解决**：G018 的 "all content" 与 G006 的内容屏蔽在原文中未给优先级，已作为问题保留，未当作冲突处理，也未据此删改目标。
- **精化组是否有反例未解决**：GR1（G010 ← G001+G008）在异常场景（检索命中但播放卡顿、或内容未收录）出现反例，因此维持 `proposed` + `partial`，未进入成立精化图；成立组数为 0。
- **是否有为凑层级造根**：没有造根目标。23 个目标全部多根并存，未新增"平台应提供服务"一类的泛化父目标；G010 是原文明确表达的目的（"I want to gain information… quick search"），不是为连边补的根。
- **关系判断是否执行到底**：见第 3 节，含逐条"已检查但无依据"。
- **可疑处（自检发现，未擅自处理）**：G013/G014/G016 三条目标自评即为 insufficient，仍保留在模型中（按要求不升级、也不删除），因此 readiness 呈 `blocked`；是否需要把它们降为"待确认候选而非目标"，属于评审/人工判断。

## 2. 工程检查实际结果（复制自 attempt-summary.json）

- `coverage_check`：`{"exit_code": 0, "structure": "passed", "workflow": "recorded", "pending": [], "counts": {"source_segments": 50, "windows": 24, "raw_candidates": 35, "final_goals": 23, "source_checks": 11, "actual_passes": 1, "dispositions": {"exclude": 9, "keep": 23, "merge": 3}}}`
- `inspection`：`{"structure": "passed", "readiness": "blocked", "independent_semantic": "not_run", "formal_proof": "not_run", "human": "pending"}`
- `counts`：`{"goals": 23, "relations": 5, "groups": 1, "established_groups": 0, "raw_candidates": 35, "support_labels": {"direct": 16, "inferred": 4, "insufficient": 3, "contradicted": 0}, "issues": 24, "blocking_issues": 3}`
- 其他：`tracing_status=completed`，`declared_vs_effective_downgraded=[]`，`warnings=[]`。
- 3 条 blocking 均为"原文尚不足以支持这项目标"（G013、G014、G016），无其它结构类阻断。

## 3. 关系与精化组判断（含"已检查但无依据"）

成立/提出的联系 5 条（4 supported、1 proposed）：

| ID | 方向 | 类型 | 状态 | 依据 |
|---|---|---|---|---|
| R1 | G001 → G010 | operationalization | supported | T016 快速搜索拿到信息 |
| R2 | G008 → G001 | contribution | supported | T014 模糊条件仍要有意义结果 |
| R3 | G004 → G002 | contribution | supported | T012 浏览卡片需附描述，描述由创作者填写 |
| R4 | G023 → G007 | contribution | proposed | T028 把 24h 等待连回"安全合规"，但机制未说明 |
| R5 | G005 → G003 | contribution | proposed | 剪辑可提升上传成品，但原文只说"很有用" |

**已检查但无依据（不建边，理由随 decisions.questions 一并写入 kaos-decisions.json）**：

1. G021（观看列表）→ G002（可视化浏览）：同属内容发现，原文未说明列表帮助浏览，仅主题相近。
2. G019（订阅方案）→ G018（高级档权益）：原文并列陈述定价方案与权益，未说明方案是达成"无广告全内容"的手段。
3. G009（播放流畅）→ G010（快速获得信息）：T014 分别谈检索与观看两类障碍，未把播放质量联系到信息获取。
4. G006/G007 → G023：观众侧屏蔽、streamer 禁分享与 24h 账号等待是三种不同机制，原文未给前后依赖。
5. G002（浏览）→ G001（检索）：属同一"找内容"目的的两种方式，若建边会把替代关系写成实现/贡献，故不建。
6. G016（字幕准确）→ G017（色盲配色）：同属无障碍关注，但对象与结果不同，无共同目的目标可挂，按同主题处理。
7. G003（上传/开播）→ G004、G005 作为 AND 精化：元数据与剪辑均为可选增强（"perhaps"/"very useful"），不满足"共同充分"，故不建组。
8. G018/G019/G020 三者的层级：方案与付款是同一订阅流程的不同环节，缺少明确父目标，不造中间层。

精化组：仅评估了 GR1（G010 ← G001+G008）。normal 场景 supports，exception 场景（播放卡顿 / 内容未收录）为 counterexample，故 `proposed` + `partial`，未成立。原文没有任何一组子目标能被声称"共同满足即足以实现父目标"，成立组为 0 属如实结果。

## 4. 未决问题清单

- G016：非母语英语观众的字幕准确度没有要求或阈值（原文只有"not sure"）。
- G013 / G014：发布"简单"与"不必等整段上传"是要求还是提问，未获回答。
- G018 vs G006：premium "all content" 与合规屏蔽的优先级未定。
- G011 / G012：格式兼容、无时长限制是明确要求还是对技术麻烦的猜测（判 inferred 依赖假设）。
- GR1：是否需纳入播放质量（G009）与内容可得性才能声称共同充分。
- R4：24h 等待是否为内容合规手段，原文只说"security and compliance"。
- 模型级：平台运营方（大型公司）与合规责任方边界未定，责任未分配给软件。

## 5. 实际执行情况

- 原文读取：完整读 1 遍（50 轮全文），按 4/步 2 的 24 个窗口逐窗捕获；随后全篇回查 1 遍（指代、问答范围、条件继承、例外、相反证据），未另开补查 pass，故 `planned_passes=1`、`actual_passes=1`。
- 修复次数：2 次重跑（推断基准 ID 非法；work 目录已存在），均在同一 attempt 内局部修正，见 `repair-log.md`。
- 实际耗时（自报）：约 12 分钟（含技能阅读、捕获、建模、两次修复与重跑）；harness 成功运行本身约 9 秒。
- 停止原因：24 个窗口处理完毕、全篇回查完成、无新增有据意图；未决项受原文所限，按规则停止该问题循环。

## 6. 没有做的事

- 独立语义审查：**not_run**（本文件是生成方自检，不是独立评审）。
- 形式证明：**not_run**。
- 人工接受：**pending**（`review.status` 仍为待审，未替用户采纳）。
- 未读取仓库其它目录、其它 run、参考模型或历史答案；未联网检索。
