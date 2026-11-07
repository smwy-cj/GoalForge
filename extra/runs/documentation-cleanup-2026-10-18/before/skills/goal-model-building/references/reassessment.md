# 重新判断结果回填

reconcile_model.py接收已冻结修订模型的当前目标追溯和关系重评，事务性更新副本并复检；不调用模型生成语义结论，不新增顶层Skill。

## 输入与命令

完整回填输入：

- 修订模型及声明的原文/历史反馈附件。
- 该模型生成的retrace-input.json，含goal_id、新目标表述与target_model。
- 使用绑定语义判断生成的tracing.json及实际判断文件。
- 该模型版本的关系重评包；可以只提交部分关系，剩余项继续阻断。

先准备并填写语义判断，按goal-tracing的[绑定判断说明](../../goal-tracing/references/semantic-judgments.md)执行。关系模板使用：

```text
python skills/goal-model-building/scripts/reconcile_model.py <feedback-model.json> --relation-template <新关系模板.json>
```

仅列当前needs_retrace/not_run关系，label与理由留空。读取新目标与原文后另存已填写关系文件，不自动照搬旧标签。

```text
python skills/goal-model-building/scripts/reconcile_model.py <feedback-model.json> <新回填目录> --retrace-input <retrace-input.json> --tracing <tracing.json> --judgments <绑定语义判断.json> --relations <关系重评.json>
```

只有关系需要重评时，可以只提供--relations。只有目标追溯先完成时可以不提供--relations，但其关联关系重新标为未评估，检查继续阻断，不能借新目标支持绕过关系重评。

## 关系重评包

schema_version为goalforge-relation-reassessment-1，base_model包含model_id、version、core_sha256，必须匹配实际修订模型。decisions为数组，每项包含：

| 字段 | 约束 |
|---|---|
| pair_id、a、b | 现有唯一目标对；不新增或改换端点 |
| target_statements | 以两个goal_id为键，逐项保存当前完整表述 |
| label | refinement/related/equivalent/none/uncertain，必须实际填写 |
| rationale、conditions | 新判断依据非空；条件为字符串数组 |
| evidence_ids | 已有证据ID，或trace:加本次追溯证据ID；正向关系至少有实际来源证据 |
| parent_id、child_id、interpretation | refinement必填，方向限当前两个目标，明确范围/情境解释，不自动写AND/OR |

本次追溯的E0001可能与旧模型E0001不同，必须用trace:E0001指向新证据；直接E0001仍表示旧证据。工具为新证据分配ET开头的唯一ID，保存映射，不覆盖旧索引和历史引用。

## 核对与更新

1. 验证实际附件字节、标准全文和模型ID/版本/核心哈希；不根据JSON内的任意文件路径读取材料。
2. 验证追溯输入目标的完整表述、主体、情境与来源等级；核对输入及判断文件的实际哈希。
3. 用相同绑定输入重新执行追溯，对比traces、sources、semantic_binding等结果；未完成语义判断不能作为完成结果回填。
4. 新证据必须实际匹配标准全文中的Unicode半开区间，具有已核验的全文位置；保存新旧证据映射。
5. 更新目标支持，关联关系先失效；再应用匹配当前节点的明确重评。未提交的关系不默认为none，负面/不足支持不提升为direct。
6. 保留候选映射和旧对象历史，检查坏引用、方向、重复与精化环。未知对象、过期包、伪造结果、坏证据或新有向环导致整项失败，原模型不变。

仅清理被当前判断实际解决的失效标记，不删除无关阻断项；不确定/等价关系保留为待审。生成父版本关系及.a1版本后，人工回到pending，旧认可不继承。

## 输出与最终交付

- reconciled-model.json：回填后的模型副本，validation尚未导入检查状态。
- review-report.json、model-review.md：针对该副本实际执行的复检。
- reassessment-record.json、reassessment-review.md：更新对象、输入证明、证据ID映射及未完成目标/关系。
- attachments/：源文、历史反馈以及本轮实际输入和判断文件，均有哈希。

再执行：

```text
python skills/goal-model-building/scripts/finalize_model.py <reconciled-model.json> <review-report.json> <新交付目录>
```

全部机械阻断解除后可为reviewable，仍不等于人工accepted或独立语义审查通过。部分回填、负面支持、未完成关系或其他阻断项继续交付blocked。语义结论仍由当前助手或可用模型根据实际原文编制，工具回填没有替代该判断。
