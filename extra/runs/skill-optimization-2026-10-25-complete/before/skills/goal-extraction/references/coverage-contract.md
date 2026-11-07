# 提取覆盖记录契约与工具

用途是审计“源文→原始候选→最终目标”。最终目标仍为 `goalforge-extraction-3`，模型仍为 `goalforge-kaos-1`；以下附件不改变支持判断，也不被模型组装器自动读取。旧结果没有记录时注明未执行，不补写虚构过程。

## 文件与绑定

| 文件 | 版本/内容 |
|---|---|
| source-input.json、source.txt | 既有忠实源文；偏移为标准全文 Unicode 码点半开区间 |
| source-windows.json | `goalforge-source-windows-1`：document_id，input_binding（document_hash、source_input_sha256），parameters（size、stride、unit），windows |
| raw-candidates.json | `goalforge-extraction-candidates-1`：document_id，input_binding（document_hash、source_input_sha256、windows_sha256），candidates |
| extraction-ledger.json | `extraction-ledger-1`：document_id，input_binding，run，full_context_review，entries，source_checks，limitations |
| coverage-check.json | `goalforge-coverage-check-1`：实际输入及 ledger 哈希、structure、workflow、pending、uncertain_*、counts、errors、limitations |

哈希均为对应文件实际字节 SHA-256，不是路径或重新序列化后的猜测值。ledger 的 input_binding 含 source_input_sha256、source_sha256、windows_sha256、candidates_sha256、extraction_sha256，由模板工具计算。任何绑定文件变化都使旧记录失效，保存旧版后重评受影响处置并生成新版本，不能只替换哈希继续沿用结论。

窗口包含 window_id、source_ids、start_char/end_char、text、segments。segments 保留 source_id、speaker、text、全局 start_char/end_char 及 window_start_char/window_end_char。unit=turn 仅用于所有片段均有原轮次定位的资料，否则为 segment；最后窗口抵达文末后停止，不再产生纯重复尾窗。size/stride 为正整数且 stride≤size。检查器重建窗口逐项比较，遗漏、错序或位置改写均不通过。

## 原始候选

每项含 candidate_id、statement、actor（未知 null）、modality（原语气简述，未知 unknown）、context（字符串数组）、origin（暂定 explicit/inferred/unknown）、pass_id、window_ids、evidence_candidates。原始 ID 如 C001，与最终 G001 分开，不因排序改变。

证据沿用 source_id、quote、role=basis/context、start_char/end_char，至少一条 basis。覆盖工具要求已确定的全局偏移；引用必须在所列窗口对应的源片段内。跨窗校正可增加窗口引用，不能悄悄更换引文。未定位可靠时保留读取限制，不能伪造位置以通过检查。

合并、拆分或排除都不删除冻结候选；原始记录可保留后来被否定的候选及原暂定判断。新发现的推断上层目标也先形成候选并走最终核验，不直接在模型中造节点。

## 处置与重要片段回查

entries 每个原始 candidate_id 恰好一项，含 disposition、final_goal_ids、reason。理由是简短可核对的语义依据，不能用“聚类相近”或“出现较少”代替。

| disposition | 映射规则 |
|---|---|
| keep | 一个最终目标，保留本意；表述整理说明关键条件仍在 |
| merge | 一个最终目标，另有候选映射到同一目标；说明为何同义及哪些条件保留 |
| split | 至少两个不同最终目标，说明各自核心动作/结果的独立意图依据及共同、局部条件如何分配 |
| exclude | 无最终目标；说明背景、重复以外的排除理由或不支持部分 |
| uncertain | 可无目标，也可映射待确认目标；说明缺口，不因此升级语义支持 |
| pending | 空映射及待编制判断；工具报告未完成 |

同一最终目标可以承接多个候选；保留主候选为 keep、其他同义候选为 merge 亦可。每个最终目标必须有原始候选来路，否则报告待补记录。复杂拆合按逐候选最终去向记录，不能为满足标签删除语义。

“一目标一核心动作”用于最终目标整理，冻结原始候选允许含复合表达。拆分后保留原始候选ID与各最终目标ID的对应，每项单独核验；合并理由应说明核心动作、主体和条件一致。检查器只核对映射、引用与版本，不自动识别动词、判定原子性或继承原候选的语义支持。

source_checks 只登记实际回查的重要片段，不要求逐句分类。每项 check_id、evidence_candidates、candidate_ids、final_goal_ids、outcome（represented/excluded/uncertain）、reason。represented 至少有最终目标；excluded 不带最终目标；若同时列候选与最终目标，其映射须与 entries 一致。待确认项持续显示。空数组不代表已经检查所有意图；是否漏掉应检查的片段由语义复核判断。

## 运行与全文校正记录

run 含 strategy（windowed/full_document）、model、temperature、budget、usage、skill_revision、prompt_revision、planned_passes、stop_reason、passes。不可获得项写 unknown；可获得的模型/技能版本或哈希、预算单位、实际耗时/token/费用写清楚。planned_passes 为正整数或 unknown，actual_passes 由非 not_run 的 pass 数计得，是作者声明的实际记录，不是工具观测模型调用。

每个 pass 含 pass_id、kind（initial/repeat/focused/full_context；模板 unknown 待填）、context（shared/isolated/unknown）、status（completed/partial/not_run）、window_results。每个窗口恰好一项，status=processed/skipped/pending，skipped 必须有 reason。定向补查可以跳过无关窗；至少一次 initial 完成全部窗口，才能报告基础处理范围已记录。整篇策略也填写全部窗口处理状态，表明原文范围，不伪称分别调用了模型。

full_context_review 含 status（completed/partial/not_run）、source_ids、reason。completed 要求核对全部源片段，并简述指代、条件、例外回查的实际范围；不是独立评审或形式证明。

## 操作

以下相对路径相对于任务工作目录；脚本路径替换为实际加载的技能路径。已有输出拒绝覆盖，修订使用新文件或目录。

```text
python <skill>/scripts/prepare_source.py input.json work --window-size 4 --window-stride 2
python <skill>/scripts/check_coverage.py capture-template --source-input work/source-input.json --source work/source.txt --windows work/source-windows.json --output work/raw-candidates.json
```

助手逐窗编制候选、保存运行记录，再整理 extraction.json。候选模板允许空集合；工具不会生成目标、推断处置或断言无目标。

```text
python <skill>/scripts/check_coverage.py template --source-input work/source-input.json --source work/source.txt --windows work/source-windows.json --candidates work/raw-candidates.json --extraction work/extraction.json --output work/extraction-ledger.json
```

填入真实运行与处置。空模板的 not_run/pending 是占位，不能当已执行；没有候选也需要记录实际基础读取轮次。然后检查：

```text
python <skill>/scripts/check_coverage.py check --source-input work/source-input.json --source work/source.txt --windows work/source-windows.json --candidates work/raw-candidates.json --extraction work/extraction.json --ledger work/extraction-ledger.json --output work/coverage-check.json
```

退出码0为结构通过且 workflow=recorded，1为结构通过但仍有 pending，2为结构/绑定错误。uncertain 不自动阻止 recorded，它表示去向已记录、语义仍未知；两种状态均不表示意图完整或精化可成立。报告恒为 semantic_completeness=not_assessed。随后照常执行 trace_candidates 核验当前目标及建模流程。

只进行局部反馈修订时，不为了得到 recorded 假装重读全部资料；可保留 partial 及实际范围。审计记录与提取文件一同保存，但当前模型交付不会自动携带它，向用户说明其用途和位置。
