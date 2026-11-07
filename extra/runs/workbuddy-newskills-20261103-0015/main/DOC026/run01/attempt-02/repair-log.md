# 修复记录 attempt-02

## 触发

attempt-01 首次运行 harness 在 `judgment_template` 步骤退出码 1：

```
ValueError: Inference reason required
（goal-extraction/scripts/render_review.py:86，经 simple_candidates.validate → trace_candidates.validate_input）
```

原因：G005、G014、G019、G020 四个目标的 `origin` 为 `inferred`，但 `inference` 为 `null`。提取契约要求 origin=inferred 时必须给出 `inference.reason` 且 `basis_candidate_ids` 指向本任务已有候选。

## 处置

未修改 attempt-01 已生成产物（spec.json、extraction.json、raw-candidates.json、work/ 均保留原样）；把 spec.json 的编制脚本复制到 attempt-02，仅补下列四个对象的 `inference`：

| 目标 | 补充内容 |
|---|---|
| G005 顺利订车 | basis=[G001]；理由：订车失败直接阻断“从一处到另一处”的交通目的；假设：把失败视为对 G001 的阻碍 |
| G014 配送时间预估准确 | basis=[G013]；理由：预估不准是求助客服的直接起因；假设：抱怨预估不准等于希望预估准确 |
| G019 中途超时告知司机 | basis=[G017]；理由：告知司机是为避免中途停留拖延的做法，受访者称“有帮助”；假设：认为有帮助等于希望这样做 |
| G020 下单后易改上车点 | basis=[G021]；理由：因应用内改点不便才改用直接告知司机；假设：难度对比意味着希望更容易改点 |

其余目标、判断、覆盖记录、联系与问题均未改动。

## 结果

attempt-02 harness 一次通过：`ok=true`，`downgraded=[]`，`warnings=[]`，coverage `structure=passed / workflow=recorded`，inspection `structure=passed / readiness=reviewable / blocking_issues=0`。
