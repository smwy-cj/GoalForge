# repair-log（attempt-02）

本次为被中断任务的续跑，从原文重新开始。harness 共运行 3 次，前 2 次报错并在本目录内修正 `spec.json` 后重跑，第 3 次成功。

## 第 1 次运行：judgment_template 失败

- 报错：`ValueError: Unexpected inference`（`trace_candidates.py --judgment-template` → `render_review.validate`）。
- 触发原因：契约要求 `origin=explicit` 的目标其 `inference` 必须为 null。G002（按时/截止日期前提交）我声明为 `origin=explicit` 但同时填了 `inference`。
- 修改对象：仅 G002 的 `origin` 由 `explicit` 改为 `inferred`。
- 理由：该目标本就由 T027 的习惯描述与 T133 的“in time”推断而来，判 inferred 与已填写的 `inference` 一致；语义内容与引文未改动。

## 第 2 次运行：assemble 失败

- 报错：`ValueError: Source scenario requires evidence`（`kaos_model.py check_structure`）。
- 触发原因：GR1、GR2 中 `origin=source` 的场景检查未带 `evidence_ids`；v2 契约要求来自原文的场景必须绑定实际证据。
- 修改对象（仅这两组）：
  - GR1 增加一条 `evidence_quotes`（DOC012:T104 “There's no videos I really want to watch. So then I would I solve that by usually going to the watch later.”），使推荐失效兜底这一原文场景有依据；该组 source 场景检查绑定 `evidence_ids=["K0003"]`。
  - GR2 增加一条 `evidence_quotes`（DOC012:T059 “what part of your assignment received better grade like a subgrade. And what part of it is not as good.”）；normal 场景检查绑定 `["K0006"]`，exception 场景检查绑定 `["K0005"]`（T061 的全局评论反例）。
- 理由：新增引文只用于绑定已有场景，未改变任何目标、关系、组的状态或判断；K 编号按“先组后关系、按数组顺序”的实际生成规则对应。

## 其他说明

- harness 的 `prepare_source` / `trace_candidates` 拒绝覆盖已存在输出。前两次失败在本目录留下了 `work/`、`extraction.json`、`judgments.json`、`raw-candidates.json`、`tracing/`、`kaos-decisions.json` 等中间产物；这些均由 `spec.json` 重新生成，为确保干净重跑已将其移除（未改动 `source/`、未改动 `brief.md`）。
- 未因报错删除任何有依据的目标、证据或降低任何支持标签；两处 insufficient（G023、G024）为原文依据不足的如实保留。
