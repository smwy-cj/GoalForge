# GoalForge

当前仅维护三个技能：目标提取与证据核验、KAOS建模、模型复核。旧版本、历史输出和阶段文档已归入extra。

| 入口 | 内容 |
|---|---|
| [全过程记录](全过程记录.md) | 从首次实施到本次整理的全部阶段、实际数据、修改原因和证据位置 |
| [goal-extraction](skills/goal-extraction/SKILL.md) | 分窗捕获、全篇校正、一目标一核心动作、支持核验与候选覆盖 |
| [goal-model-building](skills/goal-model-building/SKILL.md) | 充分精化与四类独立联系分别建模，HTML/JSON/MD/SVG交付 |
| [model-review](skills/model-review/SKILL.md) | 工程检查、语义复核和真实意见后的待审重建 |
| [数据入口](datasets/README.md) | 原始34篇资料、论文基准、最新开发比较与使用边界 |
| [当前测试](tests) | 当前三个技能的123项Python、13项JavaScript回归用例 |
| [历史归档](extra/README.md) | 旧技能、旧输出、阶段文档、运行证据与恢复位置 |
| [整理验收](extra/organization-2026-10-26/verification.json) | 文件移动哈希、数据完整性、测试及项目安装一致性 |

编辑维护源在`skills`；`.agents/skills`是项目发现副本，两者内容已核对。新任务可直接指定上述技能入口。提取时读取原文，不把基准目标或评审答案送入生成过程。

当前提取契约为extraction-3，模型为kaos-2，保留v1读取与核验。工程通过不等于语义正确、形式证明或人工采纳；八篇比较是开发数据，独立测试集和完整人工Gold尚未建立。

运行工程测试：

```powershell
python -B -X utf8 -m unittest discover -s tests -p 'test_*.py' -v
node --test tests/review_core.test.js tests/simple_review.test.js
```

需要打包或核对安装时使用[scripts/release_skills.py](scripts/release_skills.py)。整理后的快照包位于[extra/dist/goalforge-2026-10-26-organized](extra/dist/goalforge-2026-10-26-organized)，版本标签区分本次目录/旧入口说明整理，目标建模算法未因此变更。

新运行使用新工作目录，保留已存在版本。历史文件中的旧位置不代表当前入口；不要继续往根目录叠加阶段报告或复制另一套旧技能。
