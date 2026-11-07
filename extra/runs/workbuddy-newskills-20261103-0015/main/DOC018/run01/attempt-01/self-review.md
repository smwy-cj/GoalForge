# 生成方自检记录（DOC018 / run01 / attempt-01）

> **性质声明：以下是生成方自检，不是独立语义评审。** 检查者与生成者为同一会话，未引入外部评审、形式证明或人工接受；下文的“通过”仅指本会话按技能契约自检与工具结构检查的结果。

## 1. 生成方自检

- **候选是否被压薄**：原文 70 轮全部读取，34 个窗口逐窗处理（无 skipped），得到 28 条原始候选、9 个最终目标。未按“十几条主要需求”压缩：T037 同一段里的“少步骤导入”“直接导出到 Drive 不经电脑”“新应用集中电子书/PDF”分别落为 G002/G003/G001；T055 的四项排名分别落为 G003/G004/G005/G006，没有合并成一条笼统的“改进阅读体验”。
- **复合候选拆分**：C009/C010/C011 共享 T037 引文但分别核验；C028（采访者复述）按四项拆到 G001/G004/G005/G006，`disposition=split`，并注明复述措辞风险（“when they're added”）。
- **条件、否定、强度、方式**：G002 保留 “without first downloading them to a computer” 的否定条件；G003 保留“一个选定目的地”且不固定目的地（原文 “I don't know”）；G008 保留 “it will be easier” 的偏好强度而非必须；G009 保留 “should” 的弱强度；G005 保留“月或年”的粒度；G001 把“至少对学校”保留在 context，未写成全校/全场景强制；G006 保留“按章”而非整本，未编造百分比阈值。
- **是否把现状/偏好/信念升为目标**：C001/C002/C004/C005/C008 为角色、现状或设备事实，C006 为能力限制，均排除并写明理由；C003 的 “will be cool” 弱设想排除；C007/C026 的抱怨只作为 G002 的问题描述，未当成已证明障碍，也未从抱怨反推唯一方案。
- **精化组是否有未解决反例**：本模型 `groups=[]`。自检理由：四项功能是并列候选，导出（G003）与学校应用（G007）更像替代路径而非 AND 互补；若强行以 {G004, G005} 共同满足“以后能找到资料”，反例是受访者明确说记不住书名/ISBN、需要按时间回忆，说明缺标题检索等仍不充分，故不建组。没有为凑层级造根目标或中间层。
- **是否过度拆分**：G007 与 G001 用 `specialization` 连接，未把“教授直接发文章”另立目标（C025 合并入 G007）；G009 独立保留付费态度并标为开放点，避免把它塞进 G007 的条件里。
- **已知呈现问题**：`review_questions`（提取层）与 `decisions.questions`（模型层）记录了同一批开放点，交付 MD 的“需要确认”因此每条出现两次（14 条 issues = 7 组重复 + 1 条模型级说明）。这是记录层重复，不改变目标、联系或支持判断；按“不手改工具产物”的要求未改动交付文件，在此披露。

## 2. 工程检查实际结果（摘自 attempt-summary.json）

- `coverage_check`：`exit_code=0`，`structure=passed`，`workflow=recorded`，`pending=[]`
  - counts：source_segments 70；windows 34；raw_candidates 28；final_goals 9；source_checks 9；actual_passes 1；dispositions：keep 9 / merge 11 / exclude 7 / split 1
- `inspection`：`structure=passed`，`readiness=reviewable`，`independent_semantic=not_run`，`formal_proof=not_run`，`human=pending`
- `counts`：goals 9；relations 3；groups 0；established_groups 0；raw_candidates 28；support_labels：direct 9 / inferred 0 / insufficient 0 / contradicted 0；issues 14；blocking_issues 0
- `tracing_status=completed`；`declared_vs_effective_downgraded=[]`；`warnings=[]`

## 3. 未决问题清单

1. G001/G007：统一应用是全新独立应用、现有 Kindle 应用的扩展，还是学校门户内功能？学校应用与个人统一应用是同一产品还是两个方案？
2. G005：按时间分类指“阅读时间”还是“加入资料库的时间”（T055 原话 vs T064 复述）？
3. G003：导出目的地是 Google Drive、Kindle 账户，还是统一应用本身（受访者说 “I don't know”）？
4. G006：是否同时保留整本书的百分比（T049 先用整本 20% 举例，后要求按章）？
5. G009：“They should be included”纳入何处（学费/学校服务/应用功能），责任方与验收未定。
6. G002：“不先下载到电脑”是硬条件还是仅更快路径？
7. 模型级：未建立 AND 精化组；若需层级，需补充共同充分性证据。
8. 重复问题记录（见第 1 节末）导致的 issues 重复展示，未作修复。

## 4. 实际执行情况

- 原文阅读：2 遍（第一遍整篇 T000–T069；第二遍按 4 轮/步长 2 的 34 个窗口逐窗捕获，并回读 T003–T065 校正指代、条件、让步、例外与替代说法）。
- 补查：对 32 条拟用引文做逐字符校验，修正 1 处大小写（T051 应为 “so I think it will be very valuable…”）；补查未新增有据意图，故只有 P1，一个 pass 覆盖全部 34 窗。
- 修复次数：0（首次 harness 即成功，无 downgraded、无 blocking）。
- 耗时（自报）：人工阅读与编制约 50 分钟；harness 全流程 9 秒。
- 停止原因：完成一次整篇读取 + 全部窗口处理 + 全篇回查，预算内无新增有据意图。

## 5. 没有做的事

- 独立语义审查：not_run（本文件是生成方自检，不构成独立评审）。
- 形式证明：not_run（结构检查不证明精化充分性或语义正确）。
- 人工接受：pending（模型 review 状态仍为待审）。
- 未读取任务目录与冻结技能之外的材料，未联网检索论文或参考答案，未参考历史目标/关系/评分。
