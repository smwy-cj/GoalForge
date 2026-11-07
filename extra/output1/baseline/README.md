# Baseline 独立生成结果

三篇 v1 已完成，所有分析仅基于冻结 baseline 技能与提供的源文三件套。未读取另一分支、当前项目技能、旧输出或参考答案；未修改输入与冻结技能。

执行跨至 Asia/Shanghai 2026-10-24；运行与冻结记录使用机器返回的实际 UTC 时间。输入是用户提供的已处理转写文本；识别准确性与事实真实性均未独立核验，源索引中的 native_text 仅表示此次接入为文本，不表示录音或事实已获人工确认。

| 文档 | 目标 | 候选精化组 | 成立精化组 | 实际 inspect |
|---|---:|---:|---:|---|
| DOC010 | 10 | 2 | 0 | passed / reviewable |
| DOC023 | 8 | 3 | 0 | passed / reviewable |
| DOC031 | 9 | 2 | 0 | passed / reviewable |

每篇的 `v1/delivery/goal-model.html` 为最终阅读入口，同目录有 JSON、MD、SVG、附件与交付清单。`v1` 中另有 extraction.json、judgments.json、tracing.json、kaos-decisions.json、实际 inspection.json、author-review.md、execution-log.json、run-record.json、run-notes.md 和核验结果。空判断模板一并保留。

7 个候选组均有原文依据与逐组分析，但未确认共同充分性，全部为 proposed / partial，不进入已成立层级图。作者自检还记录了不构建其他精化的原因。模型允许多根和孤立节点。

实际执行冻结工具的 template、trace、assemble、inspect、finalize；最终交付清单哈希全部一致，62 条目标引文均全文精确定位，精化组引文亦经 assemble/inspect 校验。工程 passed 不代表语义充分性被形式证明。独立语义审查 not_run；形式证明 not_run；人工 pending；浏览器交互测试未执行。

模型精确标识、采样参数与预算均为 unknown。源文中的口语断裂、拼写和编码痕迹保留；源文事实未外部核验。本轮没有构造新的使用场景，分析性的充分性判断与访谈事实分开记录。

加载说明：四项 SKILL.md 均完整阅读；阅读了 goal-extraction/references 下 input-processing、output-contract，goal-tracing/references 下 evidence-rules、semantic-judgments、output-contract，goal-model-building/references 下 modeling-rules、output-contract、tools，以及 model-review/references 下 tools、output-contract。阅读并实际运行的脚本包括 trace_candidates.py、kaos_model.py，执行时其导入的 simple_candidates.py 与 render_review.py参与校验，finalize加载 simple-viewer.html/css/js 与 simple-core.js。完整冻结目录文件哈希（inventory，并不表示每一文件均作为语义规则加载）保存在每篇 run-record.json；运行路径和命令见 execution-log.json。

`freeze-manifest.json` 记录三篇 v1 的逐文件字节哈希。冻结后不依据其他分支或复核意见改写本轮产物。
