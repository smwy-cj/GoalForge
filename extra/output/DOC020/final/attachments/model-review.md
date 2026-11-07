# 目标模型检查记录

模型：DOC020-goal-model · v0.1

结构检查：passed
语义审查：not_run
模型人工状态：pending
检查报告自身人工确认：pending

## 已执行与未执行的检查

- integrity：passed。共享契约、ID、引用、边方向、有向环和关系覆盖检查。
- scope：passed。检查声明的文档范围及证据来源。
- lineage：passed。检查目标与候选双向映射；不自行补造映射。
- representation：passed。正向决策与可视化边一致。
- trace_validity：passed。检查既有支持状态；不重新推断语义支持。
- attachments：passed。核对附件安全路径、可取得性和实际字节哈希。
- human_records：passed。只核对已提供意见的文件与版本绑定，不认证审核人身份。
- source_location：passed。按 Unicode 码点和半开区间核对原句。
- semantic：not_run。未调用独立语义审查模型；只保留上游判断与待审项。

## 问题与待审事项

### I-6eb84288d07f · needs_review

DOC020-G011, DOC020-G015

两处对「重要性判错」的取舍方向相反：T026 说宁可多收垃圾也不愿漏掉重要邮件（接受误报）；T058 说判定不可靠时宁可不收提醒（回避误报）。同一权衡下两种偏好并存，受访者未做统一表态，也可能分别针对「垃圾过滤」与「提醒触发」两个不同环节——无法据此判定二者是互补还是冲突。

人工决定：

修改建议与审核意见：

## 修复记录

```json
[]
```

## 限制

- 结构检查不证明语义正确。
- 未执行独立语义审查；模型人工状态来自实际反馈，检查报告自身未获人工确认。
