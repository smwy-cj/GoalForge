# 检查与反馈执行

项目根目录执行，由同级 goal-model-building 的 kaos_model.py 提供公共检查和反馈逻辑。

```text
python skills/goal-model-building/scripts/kaos_model.py inspect work/assembled/model-input.json work/inspection.json
python skills/goal-model-building/scripts/kaos_model.py feedback work/delivery/goal-model.json work/review-feedback.json work/feedback-output
```

检查字段见[报告契约](output-contract.md)。feedback 校验实际交付与输入文件，保留意见和受影响目标/精化组；不自动改写目标。之后由助手回查资料并按[修订规范](../../goal-model-building/references/reassessment.md)重建与复检。

检查失败不得手工写 passed。定位问题、模型语义疑点、资料缺失分别说明；只读相关上下文，不重复穷举目标对。结构、当前作者判断、独立审查、形式证明和人工决定保持可区分。

每次使用新输出路径，保留原件、实际意见和父版本。用户只收到必要问题、简短处理说明与可审核模型。
