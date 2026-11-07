# 当前数据入口

| 数据 | 位置 | 用法 |
|---|---|---|
| 原始上游快照及许可 | [raw/goalgeneration](raw/goalgeneration) | 固定提交来源，不改写 |
| 34篇完整访谈、2,692轮 | [processed/goalforge-v1/source](processed/goalforge-v1/source) | 目标生成时只读此处或同版本documents.jsonl |
| 文档索引与哈希 | [document_inventory.csv](processed/goalforge-v1/document_inventory.csv) | 按DOC003—DOC036定位材料 |
| 三篇开发参考 | [development_reference](processed/goalforge-v1/development_reference) | 27目标、111关系对；含助手判断与19个不确定项，不是完整人工Gold |
| 原划分及接触范围 | [split_manifest.json](processed/goalforge-v1/split_manifest.json) | 独立测试集为空；储备资料后来已被项目使用 |
| 作者公开代码与基准产物 | [baselines/paper-study1](baselines/paper-study1) | 固定作者提交；summarized为1,600条建模输入，其他文件不能混计 |
| 最近八篇两轮开发比较 | [benchmarks/skill-comparison-2026-10-26](benchmarks/skill-comparison-2026-10-26) | 32份模型快照、原文清单、匿名材料与评审；来源和哈希见该目录manifest |
| 完整数据整理历史说明 | [归档数据集说明](../extra/docs/12-最终采用数据集说明.md) | 原文保持不变，按当时日期理解状态 |

生成目标时不要读取development_reference、upstream_reference或benchmarks中的目标/评审来补答案。语义评审、对比和工程测试才读取对应参考，并如实记录用途。

`processed/goalforge-v1`是冻结发布，原始89份文件及release_manifest均保留原字节。其中旧README指向的docs已移入extra；请通过本入口访问准确位置，不为移动说明文档而改写冻结数据。

本项目没有独立人工Gold或未接触测试集。当前工程测试位于根目录[tests](../tests)，合成输入在测试文件中；八篇资料是开发比较数据，不能改名后宣称为独立测试集。
