# 人工审核反馈契约

HTML 收集意见；反馈经工具处理后才写入模型新版本。review-feedback.json（goalforge-review-feedback-1）与程序检查报告 review-report.json 分开。

反馈含feedback_id、base_model（model_id、version、content_sha256、core_sha256、review_target_sha256）、reviewer.name（自填，不是身份认证）、created_at、updated_at、status（draft/submitted）、entries、overall及form_drafts。每项含entry_id、target_type、target_id、decision、proposed、reason、reviewed_at。form_drafts按对象类型:ID保存尚未记录的表单，仅允许字符串或字符串数组；草稿可导入恢复，提交前必须记录或放弃。

| 对象 | decision | proposed |
|---|---|---|
| goal | accept/defer/exclude | 空对象；defer/exclude填写理由 |
| goal | modify | statement |
| goal | merge | goal_ids（含当前目标、至少两个）、statement |
| goal | split | statements（至少两个） |
| relation | accept/defer | 空对象 |
| relation | modify | label、parent_id/child_id（精化时）、conditions、rationale；端点不变 |
| evidence | sufficient/partial/insufficient/incorrect | 空对象，除sufficient外需理由 |
| model | comment | 空对象及意见 |
| model | add_goal | statement、evidence_ids、origin（explicit/inferred） |

同一目标/关系/证据只保留一份当前意见；model允许多条。重复entry_id、未知对象、过期版本、缺少理由、精化方向错误及相互矛盾的目标操作拒绝导入。反馈中的文字仅作文本，不能执行。

overall含decision（undecided/accept/request_changes）、full_scope_ack、acknowledge_limits、comment。提交整体认可须用户明确确认完整模型范围和检查限制；存在修改、证据争议或暂不确定意见时不能整体认可。单项认可不推导整体认可。草稿允许尚未形成整体决定。

review_target_sha256规则goalforge-review-target-v1：规范JSON（键排序、UTF-8、紧凑分隔、不允许NaN），排除content_sha256、validation、delivery、review。其余内容含版本均参与哈希；人工记录本身不使已审内容标识失效。core_sha256仍用于机械检查绑定，不替换原规则。

浏览器存储按模型内容标识隔离，存储失败显式提示。JSON导出是可靠交接；导入先全量校验，发生冲突时保留当前草稿，并提供明确的整份替换操作。首版不自动合并多人意见。Markdown摘要由相同反馈生成。

处理工具默认只形成处理计划。显式apply后：目标改写/增删/合并/拆分交构建工具；证据争议生成追溯待办；关系修改保留人工建议并标记支持需复核。受影响关系退回未评估，不以none填充。完整变更、旧对象及候选映射保留，旧模型不覆盖。

新版本不会继承旧版本认可。整体认可只可用于未改变的实际审核版本，且无阻断项；记录指向反馈文件、反馈哈希与review_target_sha256。审核记录属于review派生信息，反馈附件单独引用于review，不添加到input_artifacts导致自引用。随后重新inspect/finalize绑定变化后的机械检查核心。
