# 语义支持判断规范

判断由当前助手或可用模型依据本次原文编制，工具不通过字符串命中推导语义正确。

schema_version：goalforge-semantic-judgments-1。input_binding 含 data_sha256（完整目标输入对象的规范哈希）与 input_sha256（实际输入文件字节哈希）。judgments 按目标 ID 保存 target_statement、label、rationale、supported_parts、unsupported_parts、assumptions、reasoning_steps。

label 为 direct/inferred/insufficient/contradicted。表述与当前目标一致，理由非空；细节为字符串数组，简短记录支持依据、缺口和必要推断，不填无关过程叙述。

```text
python skills/goal-tracing/scripts/trace_candidates.py work/extraction.json --judgment-template work/judgments.json
python skills/goal-tracing/scripts/trace_candidates.py work/extraction.json work/tracing --source work/source.txt --judgments work/judgments.json
```

命令从项目根目录执行。模板仅预填 ID、表述与绑定，判断留空；读取原文后编制。使用未占用路径。没有判断时只核对位置，未判断目标保留 semantic_not_run，不能宣称已支持。

规范哈希按键排序、UTF-8、紧凑分隔 JSON 计算 SHA-256，不接受 NaN；主体、条件、依据等变化影响绑定。CLI 还检查实际文件字节，重新排版后也应生成匹配模板。不能通过补写哈希替代重新判断。

tracing.json 保存 semantic_binding、输入与判断文件哈希。建模工具直接消费当前判断并重执行核对；哈希证明一致性，不证明语义或编制者身份。独立审查和人工决定分别记录。
