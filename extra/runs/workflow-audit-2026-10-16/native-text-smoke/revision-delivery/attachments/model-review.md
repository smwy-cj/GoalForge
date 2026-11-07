# 目标模型检查记录

模型：AUDIT-goal-model · v0.1.h1

结构检查：failed
语义审查：not_run
模型人工状态：pending
检查报告自身人工确认：pending

## 已执行与未执行的检查

- integrity：passed。共享契约、ID、引用、边方向、有向环和关系覆盖检查。
- scope：passed。检查声明的文档范围及证据来源。
- lineage：passed。检查目标与候选双向映射；不自行补造映射。
- representation：failed。正向决策与可视化边一致。
- trace_validity：failed。检查既有支持状态；不重新推断语义支持。
- attachments：passed。核对附件安全路径、可取得性和实际字节哈希。
- human_records：passed。只核对已提供意见的文件与版本绑定，不认证审核人身份。
- source_location：passed。按 Unicode 码点和半开区间核对原句。
- semantic：not_run。未调用独立语义审查模型；只保留上游判断与待审项。

## 问题与待审事项

### I-fc1c4a052c24 · blocking

P12

Changed relation requires renewed evidence review

人工决定：

修改建议与审核意见：

### I-476389a15e6f · blocking

P12

Relation has not been reassessed after node changes

人工决定：

修改建议与审核意见：

### I-bd9af84e93f5 · blocking

P13

Changed relation requires renewed evidence review

人工决定：

修改建议与审核意见：

### I-e4ec45194bf4 · blocking

P13

Relation has not been reassessed after node changes

人工决定：

修改建议与审核意见：

### I-363e9478e239 · blocking

AUDIT-G001

Goal has missing or invalidated evidence support

人工决定：

修改建议与审核意见：

### I-17e7312e8f3c · needs_review

P12

关系尚需人工判断：uncertain

人工决定：

修改建议与审核意见：

### I-bc758605b5a9 · needs_review

P13

关系尚需人工判断：uncertain

人工决定：

修改建议与审核意见：

## 修复记录

```json
[]
```

## 限制

- 结构检查不证明语义正确。
- 未执行独立语义审查；模型人工状态来自实际反馈，检查报告自身未获人工确认。
