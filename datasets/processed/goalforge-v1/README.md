# GoalForge 数据发布 v1

固定上游34份访谈，共2692轮；3篇开发试标、31篇未补标储备。

详细说明见 [最终采用数据集说明](../../../docs/12-最终采用数据集说明.md)。

| 文件 | 用途 |
|---|---|
| documents.jsonl / source/ | 无目标标签的完整访谈运行输入 |
| turns.jsonl | 2692个可定位轮次；切片索引，不能当独立访谈随机划分 |
| document_inventory.csv | 文档级数量、哈希与使用范围 |
| development_reference/ | 27个已采纳目标、111对开发关系记录；19对不确定；来源分级 |
| upstream_reference/ | 原始上游标注隔离区；不送入生成器、不执行图代码 |
| split_manifest.json | 3篇开发、31篇储备，独立测试为空 |
| quality/ | 哈希、空值、重复、偏移与字符问题检查 |
| provenance.json / LICENSE.upstream.md | 固定来源与原始许可 |

运行提取时只加载source或documents.jsonl。目录级隔离不等于权限沙箱，Runner还需按允许字段加载。
