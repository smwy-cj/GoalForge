---
name: goal-tracing
description: 核对目标与当前原文的支持和位置，保留版本绑定证据，将需确认事项附在目标旁；默认只交接机器结果，避免重复人工报告。
---

# 目标证据核对

核对已有目标来自哪里、原文是否支持完整含义。位置匹配不能证明语义正确。默认消费 goal-extraction 的简明目标 JSON，也兼容旧候选文件；缺来源时标为不足，不凭记忆补证据。

## 核对

1. 固定当前目标与原文版本，读取已有依据及必要上下文；只有出现主体、否定、条件或多义问题时扩大阅读范围。
2. 定位原文，分别记录识别可靠性、位置与语义支持。多处命中不默选；原文哈希变化不能沿用旧偏移。
3. 判断直接支持、合理推断、证据不足或相反证据；缺少提及不等于反证。推断保留必要假设。
4. 问题简短挂到对应目标。关键条件缺失、材料不完整与识别风险不得隐藏，原文和历史意见不覆盖。

按[绑定判断契约](references/semantic-judgments.md)生成空模板，再依据当前原文编制判断；禁止给旧结论补新哈希冒充重新判断。脚本定位不替代模型判断。具体边界按需读[证据口径](references/evidence-rules.md)。不得读取研究参考答案。

## 运行与交接

```text
python scripts/trace_candidates.py extraction.json --judgment-template judgments.json
python scripts/trace_candidates.py extraction.json tracing-output --source source.txt --judgments judgments.json
```

模板留空项须由当前助手或可用模型编制。支持 goalforge-extraction-3，无需增加 category。保持对真实输入字节与完整目标对象的绑定。

新版默认只输出 tracing.json，结果交构建阶段；单独要求报告时加 --review-md。完整流程不让用户逐项阅读追溯报告。旧输入仍保留原报告行为与[旧契约](references/output-contract.md)。

反馈指向目标或依据时只重新核对受影响内容，ID 保留；目标变化后的精化组交 goal-model-building 重评。未经实际核对不得登记通过或人工认可。
