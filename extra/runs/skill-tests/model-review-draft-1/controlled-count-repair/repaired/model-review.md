# 目标模型检查记录

模型：DOC023-goal-model · v0.1.r1

结构检查：passed
语义审查：not_run
人工审核：pending

## 已执行与未执行的检查

- integrity：passed。共享契约、ID、引用、边方向、有向环和关系覆盖检查。
- scope：passed。检查声明的文档范围及证据来源。
- lineage：passed。检查目标与候选双向映射；不自行补造映射。
- representation：passed。正向决策与可视化边一致。
- trace_validity：passed。检查既有支持状态；不重新推断语义支持。
- attachments：passed。核对附件安全路径、可取得性和实际字节哈希。
- source_location：passed。按 Unicode 码点和半开区间核对原句。
- semantic：not_run。未调用独立语义审查模型；只保留上游判断与待审项。

## 问题与待审事项

### I-ee6c6a0f13a0 · needs_review

DOC023-G001, DOC023-G003

联系人数量增加可能影响内推，但访谈没有确认数量本身与内推的关系。

人工决定：

修改建议与审核意见：

### I-8ed4b75760ef · needs_review

DOC023-G001, DOC023-G008

泛化的联系人数量与合资格内推联系人可能重叠，但适用目的未被充分区分。

人工决定：

修改建议与审核意见：

### I-61f7bfcfa650 · needs_review

DOC023-G003, DOC023-G012

更多可访问联系人是否改善内推结果未被直接确认，保留待审。

人工决定：

修改建议与审核意见：

### I-b480fdf1cf24 · needs_review

DOC023-G004, DOC023-G009

内推意愿与简历曝光存在可能的间接路径，但未直接说明，保留不确定。

人工决定：

修改建议与审核意见：

### I-354b289a3140 · needs_review

DOC023-G008, DOC023-G012

访问更多候选与找到合资格联系人可能有关，但不是所有更多结果都符合资格。

人工决定：

修改建议与审核意见：

### I-e3a9687a3742 · needs_review

DOC023-G009, DOC023-G017

更充分表达可能影响内推意愿，但访谈未明确该作用。

人工决定：

修改建议与审核意见：

## 修复记录

```json
[
  {
    "attempt_id": "A1",
    "patch_ids": [
      "PATCH-coverage"
    ],
    "before_version": "v0.1",
    "before_core_sha256": "4ce77a0e382a583285896572b521152ab8ccba7b755e6c5bd5482f50eaa9d9d0",
    "status": "applied",
    "model_calls": 0,
    "token_usage": null,
    "stop_reason": "one_transaction_complete",
    "after_version": "v0.1.r1",
    "after_core_sha256": "47188fd80d189ed550e4ba2f9bd6b511dbc841f3b4f6c194e7f92592d33d229b",
    "resolved_issue_ids": [
      "I-6813c5d5afac"
    ],
    "new_issue_ids": [],
    "elapsed_seconds": 0.0
  }
]
```

## 限制

- 结构检查不证明语义正确。
- 未执行独立语义审查或人工采纳。
