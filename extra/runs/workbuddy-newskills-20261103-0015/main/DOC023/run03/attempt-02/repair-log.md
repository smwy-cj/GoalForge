# 修复记录（repair-log）

任务：DOC023 / run03。修复轮次：1 次（attempt-01 → attempt-02）。

## 触发原因

attempt-01 首次运行 harness 时，`assemble` 报错退出：

```
ValueError: Source scenario requires evidence
（kaos_model.py:305 require(item.get('evidence_ids') ...)）
```

原因是 GR1 的两条 `origin=source` 场景检查（搜索结果可能为空、非会员结果受限）只写了场景与理由，没有把该场景所依据的原文引文登记为 evidence，违反了“source 场景必须带证据”的结构约束。这是记录缺失，不是语义判断改变。

（首次运行前另有两处引文笔误，与 harness 无关，已在运行前自查修正：C009 的 `and then after this` 应为大写 `And then after this`；C016 的 `if you are a linking premium user` 原文实为 `you are a linking premium user`。）

## 改了什么

1. GR1 的 `evidence_quotes` 增加两条 T013 引文（逐字符匹配原文）：
   - `in the worst case, like there are just like one or 2, or even none of the people in the search result`
   - `But if you are not, you're probably gonna able to access like a limited list of people`
2. GR1 对应两条 `exception` 检查的 `evidence_ids` 分别填 `K0002`、`K0003`（按 assemble 的 K 编号顺序：组引文先编号，随后是 R1–R8 的联系引文）。

## 没改什么

- 目标集（G001–G009）、支持判断（全部 direct）、联系（R1–R8，含 R8 的 rejected 判断）、组状态（proposed/partial）与全部反例判断均未改。
- 未删减任何有依据的目标、引文或检查项以迁就工具通过。

## 目录说明

- `attempt-01/` 保留失败运行的产物（extraction、tracing、coverage-check 等），不覆盖、不再使用。
- `attempt-02/` 为复制 `spec.json` 后修正并成功运行的交付版本（prepare_source 要求全新目录，故新建 attempt-02 而非就地重跑）。
