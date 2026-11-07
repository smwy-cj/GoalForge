# 版本绑定的语义判断

当前追溯工具只接受goalforge-semantic-judgments-1。旧的“目标ID→label/rationale”平铺文件会被拒绝，不自动补上新哈希后沿用旧判断。历史产物保留，但重新执行应依据当前原文和目标编制新文件。

## 编制步骤

```text
python skills/goal-tracing/scripts/trace_candidates.py <目标输入JSON> --judgment-template <新模板.json>
```

工具仅创建空白模板：input_binding、目标ID和target_statement已经填写，label为null、rationale为空。助手读取本次原件与上下文后，填写label、rationale、supported_parts、unsupported_parts、assumptions、reasoning_steps，另存当前判断文件；不能把旧判断自动重包装成新版本。

```text
python skills/goal-tracing/scripts/trace_candidates.py <同一目标输入JSON> <新追溯目录> --source <标准全文> --judgments <当前判断.json>
```

未提供judgments时仍可做位置检查，但语义为semantic_not_run。模板和追溯输出均使用新路径，模板不覆盖已填写文件。

## 契约

```json
{
  "schema_version": "goalforge-semantic-judgments-1",
  "input_binding": {"data_sha256": "规范JSON哈希", "input_sha256": "输入文件实际字节哈希"},
  "judgments": {
    "目标ID": {"target_statement": "本次完整目标表述", "label": "direct", "rationale": "当前原文支持依据",
      "supported_parts": [], "unsupported_parts": [], "assumptions": [], "reasoning_steps": []}
  }
}
```

data_sha256按完整输入对象的键排序、UTF-8、紧凑分隔序列化计算SHA-256，不允许NaN；因此主体、条件、来源、证据、target_model等变化也使旧判断失效。CLI额外验证input_sha256为实际输入文件字节哈希；文件重排格式后也应重新生成模板。内部无文件API使用规范对象哈希，不伪造文件哈希。

逐项target_statement必须与当前目标相同；未知ID、旧格式、错误输入版本、未填写label/rationale或错误字段类型拒绝。可以只判断部分目标，未判断项仍是semantic_not_run，不能算作已完成支持判断。

tracing.json保存semantic_binding（契约版本、输入绑定、规范判断包哈希），CLI另保存判断文件实际哈希。assemble入口对direct/inferred追溯要求当前提取输入的绑定；回填工具会重新执行位置检查并与实际追溯JSON比较，不能只改输出label冒充新结果。

哈希仅控制版本和内容一致，不证明判断的语义正确或编制者身份。全模型独立语义审查与人工采纳仍单列。
