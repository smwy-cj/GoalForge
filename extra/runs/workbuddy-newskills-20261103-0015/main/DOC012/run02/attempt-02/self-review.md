# self-review（DOC012 / run02 / attempt-02）

## 1. 生成方自检（**这是生成方自检，不是独立语义评审**）

- **候选是否被压薄**：先按 4 轮窗口、步长 2 共 70 个窗口逐窗捕获（每个窗口一条 processed 记录），保留 36 条原始候选（含整段复合句，如 T031、T049、T059、T061、T092、T098、T114），再整理为 60 个最终目标；未先压成十几条“主要需求”。处置分布：split 15、keep 14、exclude 3、uncertain 3、merge 1。
- **复合目标是否拆分**：T031 拆为读说明 / PDF 上传（Canvas）/ 代码库（Gradescope+GitHub）/ 立即出分；T059 拆为 rubric 分项、实时预估成绩、决定投入时间、决定是否争取额外学分；T061 拆为评论绑定位置（推断）、GradeScope regrade、Canvas 缺失；T092/T098/T114 同样按独立结果拆分。目的与手段分开保留（G048 与 G049）。
- **条件/否定/强度是否丢失**：保留了“取决于文件类型”“取决于教授偏好/课程组织方式”“仅 GradeScope 有”“Canvas 没有”“不是最终成绩”“maybe / I'd rather / I really want to”“I don't want to disturb”“I don't really like stories”“取决于教授是否设 Slack 频道”等。未把偏好写成强制，未把习惯写成流程，未把信念（教师不熟悉应用、算法“了解我”）当事实。
- **未升级项**：G023（剩余时间提示）、G024（不经过成绩页取作业）如实保留为 insufficient；C007（希望 Canvas 直达作业页）、C018（缓冲）、C036（采访者未获确认的总结）保留为 uncertain；C004、C034、C035 排除并写明理由。
- **精化组是否有反例未解决**：两组均为 proposed/partial。GR1 有 1 项 unknown 场景（推荐与 Watch later 都无可看内容且无可预下载场景）；GR2 有 1 项 counterexample（教师把评论插在全局位置，T061）。因此成立组数为 0，未把贡献或先后关系伪装成成立精化。
- **是否为凑层级造根**：未新增泛化摘要根；G027（各活动时间被娱乐）来自经本人确认的访谈总结（T127/T128）与自述（T136），不是为造层级而补。作业域与流媒体域各自多根、多孤立目标。
- **反向检查**：T056 的采访者总结未获确认，未据此建上层目标；T126 的“我用手机而非网页版”作为 G060 的条件而非新目标；T104 的具体桌游仅作 G045 的情境例；T041 的两应用差异比较保留为不确定项。

## 2. 工程检查实际结果（来自 attempt-summary.json）

- `coverage_check`：`exit_code=0`，`structure=passed`，`workflow=recorded`，`pending=[]`；counts：source_segments 142、windows 70、raw_candidates 36、final_goals 60、source_checks 11、actual_passes 1；dispositions：split 15 / keep 14 / exclude 3 / uncertain 3 / merge 1。
- `inspection`：`structure=passed`，`readiness=blocked`，`independent_semantic=not_run`，`formal_proof=not_run`，`human=pending`。
- `counts`：goals 60、relations 21、groups 2、`established_groups=0`、raw_candidates 36；support_labels：direct 50、inferred 8、insufficient 2、contradicted 0；issues 19，blocking_issues 2。
- `declared_vs_effective_downgraded=[]`（无降级）；`warnings=[]`；`tracing_status=completed`；73 条引文全部 `location_status=exact`、`verification_scope=full_text`，无 ambiguous / not_found。

## 3. 未决问题清单

- 阻塞 2 项（insufficient 目标）：G023 剩余时间提示是否构成需求；G024 作业与成绩页混用期望如何改进。
- 其余未决（non-blocking）：短内容粒度（G043 vs G052 是否同一偏好的不同粒度）；G031 无广告为推断；G056 推荐体现长期偏好基于主观判断；G013 是否希望 Canvas 也有 regrade；G058 缓冲是否算应用侧诉求；G011 评论位置绑定为障碍推断；G007 立即出分是否主动期望；model 级：两段互访中说话人标签与身份互换，目标按 speaker 标签归属是否合预期。
- 提取侧 review_questions：G023/G024 保留还是退回排除；G043/G052 是否合并；G002“按时提交”是否算要求。
- 两组层级（GR1、GR2）均带未解决场景，尚未作为成立精化展示。

## 4. 实际执行情况

- 原文 142 轮完整通读 1 遍（转写导出全文），再按 70 个窗口逐窗处理 1 遍，随后做全篇校正；对 T031/T037/T039/T049/T055/T059/T061/T098/T104/T110/T114/T118/T126-T128 等重点片段做了定向回查（11 条 source_checks）。
- harness 运行 3 次：2 次报错并在本目录修正后重跑（详见 repair-log.md），第 3 次成功。
- 实际耗时（自报）：约 40 分钟，其中原文阅读与候选捕获约 25 分钟、建模与校验约 10 分钟、修复与重跑约 5 分钟。
- 停止原因：完成一次基础逐窗提取 + 全篇校正 + 定向回查；补查未再产生有依据的新意图，剩余缺口均属原文未说明，故停止并记录未决问题。

## 5. 本次**没有**做的事

- 独立语义审查：not_run（未执行，本报告为生成方自检）。
- 形式证明：not_run（未做精化充分性的形式化验证）。
- 人工接受：pending（无人工作出接受/修改决定）。
- 未读取仓库其他目录、未读取其他 attempt、未联网查询论文或参考答案；未参考任何历史目标、关系或评分。
