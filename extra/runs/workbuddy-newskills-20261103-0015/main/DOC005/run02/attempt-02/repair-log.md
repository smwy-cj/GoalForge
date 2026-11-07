# 修复记录（attempt-02）

## 1. 触发原因

attempt-01 在执行 `judgment_template` 时失败，工具报错：

```
ValueError: Unknown inference reference
```

定位：`spec.json` 中 G003 的 `inference.basis_candidate_ids` 写成了三个**原始候选 ID**（C008、C014、C036）。`render_review.validate` 只接受本任务最终目标集合内的 candidate_id（即 G 前缀 ID），原始候选 ID 不被视为可引用的 basis。

附带情况：attempt-01 已在失败前生成 `work/`、`extraction.json`、`judgments.json`；`prepare_source` 拒绝写入已有产物的目录，因此无法在原目录重跑。按 brief 第 7 节，复制 `spec.json` 到 `attempt-02` 后修正重跑，未改动 `attempt-01/` 的既有产物（attempt-01 的 spec.json 保留失败版本）。

## 2. 改了哪些对象

| 对象 | 字段 | 修改前 | 修改后 |
|---|---|---|---|
| G003 | `inference.basis_candidate_ids` | ["C008","C014","C036"] | ["G001"] |
| G003 | `inference.reason` | “原文给出的是反复出现的操作流程与占比……” | “T027 给出稳定的播放流程、T033 给出 70% 占比，且 G001 要求背景持续有声音；据此推断他希望继续以自有歌单支撑该状态。” |
| G003 | `inference.assumptions` | ["反复描述且占 70% 的流程反映其稳定意图"] | ["反复出现且占 70% 的固定流程反映其希望维持这种使用方式"] |

其余 raw_candidates、goals、judgments、ledger、decisions 未改。

## 3. 理由

G003 的 origin 仍是 inferred（由固定播放流程推断意图），但推断依据只能指向已核验的最终目标。G001（始终有背景音）是该播放方式所服务的上位状态，且其支持为 direct，作为 basis 在语义上成立：以自有歌单 shuffle+repeat 维持背景音。改后 `origin vs label` 的差异仍保留在 G003 的 rationale 中，工具另给出非阻断提示（来源与支持标签不同），未覆盖原值。

## 4. 修复次数

1 次（attempt-01 失败 → attempt-02 通过）。未使用 attempt-03。
