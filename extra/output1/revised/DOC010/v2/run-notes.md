# DOC010 运行说明

全部加载路径、SHA-256、实际命令、返回值和输出见 run-record.json；每一步独立回执为 command-01.json 等。

1. 阅读完整原文和三项冻结技能及必要引用。
2. 在 authored-data.json 逐项人工编制语义结果，未用关键词规则产生标签。
3. 复用 source-input，逐段断言原文切片与偏移一致并核对全文哈希。
4. 实际执行冻结脚本生成空 judgments 模板，填入本次判断，执行 trace。
5. 实际生成 KAOS 空包，填入本次整组判断，assemble → inspect → finalize。
6. 生成覆盖全部目标和组的 author-review，保留未决问题。

精确模型、采样参数、预算：unknown。所有人审 pending；同一代理自检不构成独立审查。未使用外部语义答案。没有进行现场 UI 或导出按钮验证。
