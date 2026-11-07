# DOC031 baseline v1运行说明

已加载冻结快照中的goal-extraction、goal-tracing、goal-model-building、model-review四项SKILL.md及接入、契约、证据、判断、精化和执行引用。具体路径及SHA-256见run-record.json。

顺序：完整阅读访谈 → 手工目标与语义判断 → 冻结trace脚本生成空模板 → 填入本次判断 → 实际trace → 冻结kaos模板 → 填入候选组 → assemble → inspect → finalize --svg → 清单文件哈希和全文引文核验。命令、时间、退出码及原始输出见execution-log.json。

源文三件套按提供版本复用并保留；源文与轮次逐一核对。脚本不以关键词生成目标、支持标签或精化结论。

模型精确标识：unknown；采样参数：unknown；预算：unknown。未调用外部模型API。

inspect是工程检查；作者自检为author-review.md，独立语义审查与形式证明均未执行，人工待审。没有浏览器交互测试。所有产物均在output1/baseline。
