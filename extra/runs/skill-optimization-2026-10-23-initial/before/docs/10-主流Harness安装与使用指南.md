# Harness 安装与使用指南

GoalForge 在可读写文件、执行 Python 的应用中使用，由当前模型阅读资料和编制判断。无需为了这种方式单独搭建模型 API 服务。

## 安装

将项目 skills 下的 goal-extraction、goal-tracing、goal-model-building、model-review 四个完整目录复制到所用应用的项目发现位置，保持同级、目录名和全部 scripts/references/assets。

| 应用 | 项目位置 | 个人位置 |
|---|---|---|
| Codex | .agents/skills/ | ~/.agents/skills/ |
| Claude Code | .claude/skills/ | ~/.claude/skills/ |
| Gemini CLI | .agents/skills/ 或 .gemini/skills/ | ~/.agents/skills/ 或 ~/.gemini/skills/ |

例如 Codex 应能直接找到 `.agents/skills/goal-extraction/SKILL.md`。不要多套目录，也不要只复制 SKILL.md。`~` 是实际执行环境的主目录；远程、WSL 和云端不会自动读取本机文件。

## 确认能使用

在项目中新建对话，确认四项技能实际发现路径、Python、资料读取和输出权限。可以先说：

> 请确认四项 GoalForge Skill 的实际加载路径，检查能否读取本次资料、运行 Python 并输出文件；先不要生成模型。

Codex CLI／IDE 可通过 /skills 或 $ 选择；Claude Code 可使用 /goal-extraction 等命令；Gemini CLI 可用 /skills list 检查。桌面界面按实际技能选择入口操作，也可在任务中点名。发现方式见官方说明：[Codex](https://learn.chatgpt.com/docs/build-skills)、[Claude Code](https://code.claude.com/docs/en/skills)、[Gemini CLI](https://geminicli.com/docs/cli/skills/)。

## 开始与更新

先用小型 MD/TXT 按[操作规范](07-完整流程操作手册.md)跑通阅读、建模、审核、导出和修订，再扩大资料规模。Word/PPT/OCR/录音依赖环境工具，技能安装不会自动补齐。

维护源在项目 skills。修改后同步完整四个安装目录，确认实际加载路径，避免同名副本混淆。需要替换已存在目录时先保留内容，再按应用方式更新；不覆盖未知修改。

安装方法不代表所有应用已经实测。每个环境分别核对资料、执行工具和保存能力；云端需提供允许处理的文件及相应运行环境。审核操作见[界面指南](06-人工审核界面与反馈处理说明.md)。
