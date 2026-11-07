# 建模与交付工具

命令从项目根目录执行，三项正式 Skill（goal-extraction、goal-model-building、model-review）保持同级；只用本次资料和判断。输出文件或目录需尚未被占用。

## 准备判断

先按[提取契约](../../goal-extraction/references/output-contract.md)生成 work/extraction.json 与 work/source.txt，再按[支持判断](../../goal-extraction/references/semantic-judgments.md)生成空模板并依据原文编制 work/judgments.json。核验脚本已迁入 goal-extraction，建模不再依赖旧 goal-tracing 目录。

```text
python skills/goal-model-building/scripts/kaos_model.py template work/extraction.json work/judgments.json work/kaos-decisions.json
```

默认生成v2判断包。relations、groups、questions由助手根据原文填写，不复制空标签当结论；字段见[模型契约](output-contract.md)。仅维护旧流程时加template --schema-version 1；Python库的decision_template保留version=1兼容默认，新调用显式传version=2。

## 构建、核验、交付

```text
python skills/goal-model-building/scripts/kaos_model.py assemble work/extraction.json work/judgments.json work/source.txt work/kaos-decisions.json work/assembled
python skills/goal-model-building/scripts/kaos_model.py inspect work/assembled/model-input.json work/inspection.json
python skills/goal-model-building/scripts/kaos_model.py finalize work/assembled/model-input.json work/inspection.json work/delivery
```

assemble 用实际支持包重执行核对，不要求重复输出人工追溯报告。inspect 核对当前结构、实际源文和输入；finalize 比对实际检查与内容，不接受口头 passed。阻断问题显式保留，资料或绑定错误拒绝交付。

默认 HTML/JSON/短 MD、必要附件和清单。v2的JSON/MD包含全部联系，HTML可单独审核联系。加 finalize --svg 同时输出层级goal-model.svg与联系goal-relations.svg；HTML可导出这两份独立图，联系不混进精化DAG。

## 明确升级旧模型

```text
python skills/goal-model-building/scripts/kaos_model.py upgrade-template old/goal-model.json work/upgrade-decisions.json
python skills/goal-model-building/scripts/kaos_model.py assemble old/attachments/extraction.json old/attachments/judgments.json old/attachments/source.txt work/upgrade-decisions.json work/upgraded --migrate-from old/goal-model.json
```

先编制upgrade-decisions再assemble。模板仅绑定旧模型及实际输入，groups/relations均为空，不自动复制旧判断或猜测类型。升级保持同一核验过的目标集合；若需改目标，先完成版本修订。旧文件保留，新模型保存迁移父绑定，再inspect/finalize。

## 本地预览与保存

```text
python skills/goal-model-building/scripts/serve_model.py work/delivery --port 8774
```

仅监听 127.0.0.1，保存是页面上的明确动作；校验同源令牌和实际内容，独占写入当前交付目录 exports，核验后返回路径与哈希。不自动应用意见，不上传外部服务。静态 HTML 继续提供浏览器下载请求、复制与完整文本，不误报落盘。

端口按实际可用情况选择。已有当前预览时直接使用，不重复启动同一端口。

## 反馈

```text
python skills/goal-model-building/scripts/kaos_model.py feedback work/delivery/goal-model.json work/review-feedback.json work/feedback-output
```

此步记录真实意见并生成待办，不做自然语言语义修改。之后按[修订规范](reassessment.md)重新判断、构建和交付。保存选择器、其他应用和文件打开方式按实际环境验证，不预设均可用。
