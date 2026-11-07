# self-review（DOC018 / run03 / attempt-02）

> **这是生成方自检，不是独立语义评审。** 检查者与生成者是同一会话、同一上下文，未做独立复核，也未替用户采纳任何目标。独立语义审查 = not_run，形式证明 = not_run，人工接受 = pending。

## 1. 生成方自检

### 1.1 候选是否被压薄

- 34 个窗口（4 轮/步长 2，覆盖 70 轮）全部逐窗处理，共产出 23 条原始候选，含 8 条显式排除（含 5 条纯障碍/现状、1 条低强度愿望、1 条排序、1 条对第三方建议）。没有先把 70 轮压成"十几条主要需求"。
- 没有意图的窗口（W0001 开场介绍、W0003–W0004 阅读比例与 Kindle 使用方式、W0013–W0014 场景导入、W0031–W0034 收尾）未强行造候选，只记录 processed。
- 边缘项按规则处理而非删掉：T011 的 web 版愿望、T015 的试用不付费习惯、T049 现存的"章节剩余时间"能力都建了候选再写排除理由，避免"因偏好或已实现而过滤"。

### 1.2 复合目标是否拆分、是否过度拆分

- T037 一句话含两个独立结果：减少步骤/直接导出（→G001）与"阅读散落多处、需要一个能放 ebooks 和 PDFs 的应用"（→G002），拆分依据是两者可独立满足。
- T049 一句含"现存能力（剩余时间）"与"新增诉求（按章节百分比）"，前者排除、后者→G005。
- T055 是四项功能排序，未整体建目标，四个分项分别映射到 G001/G003/G004/G005，排序本身按取舍信息排除（C016）。
- 反向检查：G001 未把"点击下载"这一操作步骤拆成独立目标；G003 未把"个人图书馆"与"保存"拆成两点（同一动作的两个限定）；G002 未把"PDF"与"ebook"拆成两个目标（同一应用须同时支持，AND 未改成 OR）。

### 1.3 条件、否定、强度、方式是否丢失

- 条件：「at least for the school」保留在 G002 的 statement 与 context；「without being downloaded to the computer first」保留在 G001；「after the course material is no longer available」保留在 G003。
- 强度：G006 保留 "it will be easier"（弱比较偏好，未升级为必须）；G007/G008 保留 "should"；G001 的目的地保留 "such as"（原文 "I don't know"）。
- 方式：G006（现有 Kindle 应用管理 PDF）作为明确选定的方式保留为独立目标，未只写在解释里；G001 的"直接导出、不经电脑"作为方式写入目标本身。
- 否定/例外：T023「PDF 无法转入 Kindle」作为 G006 的条件背景保留；T059 的付费否定（不愿另付）以 G008 承接。

### 1.4 精化组是否有未解决反例、是否为凑层级造根

- 本次 `groups=[]`。理由是：现有 8 个目标均为并列的功能/方式诉求，找不到"某组子目标共同满足足以实现父目标"的原文依据；唯一可想的父目标（G002 与 G007 的共同上层）本身可能是重复节点，未确认前不建组。
- 未造根目标，未为连边新增节点。R1/R2 两条联系各有独立原句，方向按定义（方式→目的；有帮助→受帮助）。

### 1.5 已知薄弱点（自检发现，未在本轮改动）

- G002 与 G007 存在近义节点风险：都以"学校阅读材料集中"为背景，区别在格式整合 vs 提供方与文章投递。已作为问题保留，未合并以免丢掉"学校提供"这一主体要求。
- G008 的 "included" 承载对象（学费/学校订阅/既有平台）原文未说明，判断中以免责式 assumption 记录，未在目标里补造。
- `review_questions` 与 `decisions.questions` 内容有 4 组重叠，导致模型 issues 出现 9 条（去重后 5 个不同问题）。这是记录冗余，不是语义冲突；未再开 attempt 仅为去重。

## 2. 工程检查实际结果（复制自 attempt-summary.json）

```json
"coverage_check": {
  "exit_code": 0,
  "structure": "passed",
  "workflow": "recorded",
  "pending": [],
  "counts": {
    "source_segments": 70, "windows": 34, "raw_candidates": 23,
    "final_goals": 8, "source_checks": 12, "actual_passes": 1,
    "dispositions": {"exclude": 8, "keep": 7, "merge": 8}
  }
}
"tracing_status": "completed"
"declared_vs_effective_downgraded": []
"inspection": {"structure": "passed", "readiness": "reviewable",
               "independent_semantic": "not_run", "formal_proof": "not_run", "human": "pending"}
"counts": {"goals": 8, "relations": 2, "groups": 0, "established_groups": 0,
           "raw_candidates": 23,
           "support_labels": {"direct": 8, "inferred": 0, "insufficient": 0, "contradicted": 0},
           "issues": 9, "blocking_issues": 0}
"warnings": []
```

- 支持分布：direct 8、inferred 0、insufficient 0、contradicted 0；声明标签与工具有效标签一致，无降级。
- 引文：全部 quote 在提交前逐条比对源片段，`not_found=0`、`ambiguous=0`；harness warnings 为空。
- delivery 文件 11 个（goal-model.html / .json / .md / .svg / goal-relations.svg / manifest.json 及 attachments）。

## 3. 未决问题清单

摘自 `review_questions` 与 `decisions.questions`（去重后 5 项）：

1. G002 与 G007 是否应合并为一个目标（格式整合 vs 学校提供 + 文章投递）？
2. G008 中 "included" 具体纳入什么？影响验收条件。
3. G001 的导出目的地是否需要定死（Google Drive vs Kindle 账户），原文为 "I don't know"。
4. T043 的回答对象存在指代歧义（T044–T045 显示问句被误解），是否应把 G006 视为更低强度建议、并重判 R1 的方向？
5. 本次未建立任何 AND 精化组：8 个目标为并列诉求，缺少"共同满足"的原文依据；若需要层级，应先确认共同上层目的。

blocking issue：0。

## 4. 实际执行情况

- 原文阅读：整篇 70 轮通读 1 遍（含逐轮打印原文核对字符），随后按 34 个窗口映射回看 1 遍；另对 T040/T041、T052/T053、T064/T065、T038–T045 做了定向补查（含确认轮与指代澄清），补查未发现需要新增 `pass_id` 的候选，故仍记为单次 P1。
- 引文校验：提交前用脚本对 23 条候选、8 个目标、12 条 source_checks、2 条关系的全部引文做逐字符比对，未匹配 0 条、重复命中 0 条。
- 修复次数：1 次（attempt-01 assemble 失败 → attempt-02 删除一条 target_type=model 的非法 issue 目标，见 `../attempt-02/repair-log.md`）。
- 耗时：自报约 35 分钟（含读技能、读原文、写 spec、一次修复与重跑）。
- 停止原因：34 个窗口全部处理、全篇校正完成；剩余 5 个歧义无新证据可解，转为问题保留，停止该循环。
- 交付路径：`main/DOC018/run03/attempt-02/delivery/`。attempt-01 的中间产物（失败运行）原样保留未改。

## 5. 我没有做的事

- 独立语义审查：not_run（本文件是生成方自检，不构成独立评审）。
- 形式证明：not_run（工具只校验结构、引用与绑定，不证明精化充分性）。
- 人工接受：pending（所有目标 review_status=pending，默认未采纳）。
- 未读取 `development_reference/`、`datasets/baselines/`、`datasets/benchmarks/`、`extra/output*`、其他任务、全过程记录或比较报告；未联网检索论文或案例答案；未参考任何历史目标、关系或评分。
