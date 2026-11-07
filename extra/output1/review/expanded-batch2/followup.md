# ER-B2-001 修订后独立补查

ER-B2-001在DOC025/v2指定哈希模型中已解决；未发现受影响范围内真实新问题。初始发现对v1的历史判断保留，v2仍为候选partial，人工待审。

本次完整重读当前父G01及子G04–G07的目标、条件、origin、推断、support与问题，重读原文T000–T005、T012–T015、T020–T021，核对F1新理由与假设。九个目标对象与原文均与初审完全相同，因此沿用初审九目标完整复核，不宣称本次又全篇重审。

新理由把不充分性限定于职位匹配、申请材料及筛选/提醒组合覆盖范围。T003支持探索意图，T005支持复核/补材料/提交，T013的推荐原理仍保留belief，T021明确技能筛选愿望。招聘方回应已不再作为父目标完成条件；ER-B2-001可标为本修订中已解决。

G04–G07仍是部分支持路径。原文未给出岗位合适的完整判据，也未证明这些能力在各申请情境中的组合覆盖，因此维持proposed/partial恰当。分析假设：筛选、提醒和便捷申请能力均存在，但本人岗位适配条件或个别材料环节没有完整覆盖；这一反例不涉及雇主回复或获得聘用。无须增加目标、增加边或升级组状态。

绑定核对全部通过：前后模型哈希与revision-record吻合，9目标完全相同、来源字节不变，全部input_artifacts与manifest文件哈希匹配，原始评审文件未变。父、子ID及组kind/status/completeness/evidence引用不变。

- 原模型：revised/DOC025/v1/delivery/goal-model.json，SHA-256 2485a16d20935b2b73078f66e739da4b0da0b0c5581c7cf30500d34122f028fa
- 新模型：revised/DOC025/v2/delivery/goal-model.json，SHA-256 f9485516c44937707857479808092cf9a1a54af47e2614a8116ce6f6bb436f5f
- 来源：revised/DOC025/v2/delivery/attachments/source.txt，SHA-256 60dd50ac11eedde508a572585eef2739e31ba01a2f48fdce984f23f1f9af7a85
- 修订记录：revised/DOC025/v2/revision-record.json，SHA-256 2d8b6d35aa1261f81a0337facd4fa33149e11984ce872aee130aaf379e4168a6

外层修订目录是v2，内部version仍为冻结工具生成的v1且parent为null；不伪造feedback。没有读取author-review作为确认依据，因此不独立背书其场景文本是否修改；补查结论直接来自机器模型与原文。初始report.md/review.json保持原样，此补查只追加v2的解决状态。

无真实新问题或交付阻断。核心inspection不手改，人审仍pending，形式证明not_run；精确模型、采样和预算unknown。全部逐项校验、受影响范围与输入哈希见followup.json。
