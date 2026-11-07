# 运行期组装输入说明

`build_artifacts.py` 只定位引文、计算绑定、调用冻结版脚本，不作提取或支持判断。作者必须先阅读完整指定原文及所分配版本 skills；不能用关键词规则生成目标或标签。

输入 JSON 字段如下（不改变正式 skill 的交接契约）：

- document_id；status（通常 completed，实际范围受限则如实记录）；limitations 字符串数组。
- goals 数组。每项必须有 candidate_id、statement、origin、actor、context、inference；与 extraction 契约相同。另含 evidence 数组和 support 对象。
- evidence 每项有 source_id（如 DOC003:T007）、quote（真实连续子串）、可选 role=basis/context。片段内重复引文须由作者给出 segment_offset；默认要求唯一命中。
- support 必须由作者填写 label、rationale、supported_parts、unsupported_parts、assumptions、reasoning_steps；不要填 target_statement，组装器从当前目标填入。
- review_questions 为正式提取契约的 candidate_ids/question/reason 数组。
- groups 数组：group_id、parent_id、child_ids、kind=and、status、completeness、rationale、assumptions、evidence（同上）。只能根据资料与明确假设作充分性判断。允许空数组，但自检须说明考虑过的关系及不成立原因。
- model_questions 为 target_type（goal/group/model）、target_id、message 数组。model 类型的 ID 是 `<document_id>-goal-model`。
- author_review 是完整 Markdown 字符串：说明实际覆盖范围、逐目标/组核验、争议/遗漏风险、精化或不精化依据、正常/异常分析场景及未决项。生成方自检不能称独立审查。

推荐在自己被分配的 `output1/revised/_authoring/<DOC>.json` 保存输入，再执行：

```text
python -X utf8 output1/_run/build_artifacts.py output1/revised/_authoring/DOC003.json --arm revised --revision v1
```

生成路径为 `output1/revised/DOC003/v1/`，必须未占用。失败的目录与执行日志保留；修正输入后选择新的修订号，并写明修正原因与实际最新版本。不要伪造人工 feedback 来绑定助手自行修正。

只依赖冻结源文与自己分支的 skills，不读取另一分支、历史输出、评审答案。所有输出放 output1。完成后告知父代理最新版本与文件路径。
