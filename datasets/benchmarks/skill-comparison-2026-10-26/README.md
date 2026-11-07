# 八篇两轮技能开发比较数据

本目录保留最近比较实际使用的冻结数据，不保存所有中间命令和页面副本。

- [benchmark-manifest.json](benchmark-manifest.json)：97份复制文件的来源、SHA-256和现位置；另列八篇JSON/TXT原文位置与哈希。
- `models/<branch>/<DOC>.json`：基线首次、新版首次、基线重复、新版重复，共32份模型；DOC003首次49目标，不以51目标修订替换。
- `source-review/<DOC>`：先于模型冻结的意图清单，以及两轮逐项判断；根层保留冻结清单、校验、errata和总结。
- `anonymous`：实际匿名评审输入；现在是事后归档数据，不再作为新的盲测。
- [metrics.json](metrics.json)、[protocol.md](protocol.md)：当时冻结的统计和方法，原字节保留。

八篇：DOC003、DOC010、DOC013、DOC020、DOC023、DOC031、DOC028、DOC036。原文仍从`datasets/processed/goalforge-v1/source`读取，不再复制八篇源文制造另一个维护位置。

单个模型JSON是比较快照，完整交付附件保存在[归档运行](../../../extra/runs/skill-optimization-2026-10-25-complete)。复制的历史文件仍保留当时相对路径；实际当前位置以本目录manifest为准。评审清单、模型和评审没有因整理而改写，不能把它们称为人工Gold或未见测试集。
