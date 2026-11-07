# GoalForge

当前包含四项项目内 Skill、工具和验证产物。2026-10-18 起新任务默认采用简明提取与 KAOS 核心层级模型，交付可审核 HTML、JSON 和短说明，旧版工具保留兼容。由所在 Harness 的模型执行判断，无需另建 API；未实现独立 API 调度，也未执行全局 Skill 安装。

- [新版简明 KAOS 模型：打开示例并人工审核](docs/14-新版简明KAOS模型人工审核说明.md)
- [本机审核入口（需本地服务运行）](http://127.0.0.1:8773/goal-model.html)

- [Skills 实施进度与当前限制](docs/03-Skills实施进度.md)
- [四项 Skill 的输入与输出](docs/05-Skill输入与输出说明.md)
- [DOC023 可操作审核界面：结构已检查，人工待审](runs/skill-tests/human-review-v1/delivery-v4/goal-model.html)
- [人工审核操作与反馈处理](docs/06-人工审核界面与反馈处理说明.md)
- [完整流程操作手册](docs/07-完整流程操作手册.md)
- [Codex、Claude Code、Gemini CLI 安装与使用指南](docs/10-主流Harness安装与使用指南.md)
- [修复前全流程审核报告](docs/08-全流程审核报告.md)
- [审核问题修复方案与验证结果](docs/09-审核问题修复方案与验证结果.md)
- [简明目标提取与 KAOS 模型修改方案](docs/13-简明目标提取与KAOS模型修改方案.md)

流程审核发现的3处缺陷及回填工具缺口已修复，71项Python与7项JavaScript测试通过，并完成工具回填闭环演练。语义判断仍由助手或可用模型依据实际资料编制；多格式真实验收、独立模型API与Agent调度仍待建设。

- [最终采用数据集说明](docs/12-最终采用数据集说明.md)
- [初步研究方案与阶段决策](docs/01-初步研究方案与阶段决策.md)
- [处理后数据集与目录说明](datasets/processed/goalforge-v1/README.md)
- [固定版本原始数据](datasets/raw/goalgeneration/16c4ce8bed513bbfdada7ac900ba6b718617a6eb/manifest.json)
