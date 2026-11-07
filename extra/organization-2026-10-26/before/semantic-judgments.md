# 语义支持判断规范

判断由当前助手或可用模型依据本次原文编制，工具不通过字符串命中推导语义正确。

schema_version：goalforge-semantic-judgments-1。input_binding 含 data_sha256（完整目标输入对象的规范哈希）与 input_sha256（实际输入文件字节哈希）。judgments 按目标 ID 保存 target_statement、label、rationale、supported_parts、unsupported_parts、assumptions、reasoning_steps。

label 为 direct/inferred/insufficient/contradicted。表述与当前目标一致，理由非空；细节为字符串数组，简短记录支持依据、缺口和必要推断，不填无关过程叙述。完整含义按[证据口径](evidence-rules.md)核验；origin 不决定 label，差异在 rationale 中说明。direct/inferred 不得掩盖尚不受支持部分；工具遇到这类混合声明时保留原提交判断，将有效 support 降为 insufficient 并列出 partial_support 问题。

```text
python skills/goal-extraction/scripts/trace_candidates.py work/extraction.json --judgment-template work/judgments.json
python skills/goal-extraction/scripts/trace_candidates.py work/extraction.json work/tracing --source work/source.txt --judgments work/judgments.json
```

命令从项目根目录执行。模板仅预填 ID、表述与绑定，判断留空；读取原文后编制。使用未占用路径。没有判断时只核对位置，未判断目标保留 semantic_not_run，不能宣称已支持。

规范哈希按键排序、UTF-8、紧凑分隔 JSON 计算 SHA-256，不接受 NaN；主体、条件、依据等变化影响绑定。CLI 还检查实际文件字节，重新排版后也应生成匹配模板。不能通过补写哈希替代重新判断。

tracing.json 保存 semantic_binding、输入与判断文件哈希。建模工具直接消费当前判断并重执行核对；哈希证明一致性，不证明语义或编制者身份。提取、核验、自检、独立审查和人工决定分别记录；未执行的阶段保持 not_run。

脚本是仅核验能力，不自动改目标；默认/修订模式的目标改写由助手另存新输入后重建模板、依据当前原文重新编制受影响判断。未变内容可经核对后沿用其理由，不批量盖章旧包。旧 `skills/goal-tracing/scripts/trace_candidates.py` 仅转接同一实现；正式安装只需要三项目录。
