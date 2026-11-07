# batch3 来源读取检查点

执行者：独立语义复核子代理 remaining_review3；精确模型标识、采样参数和预算 unknown。仅使用 assignment、指定访谈和指定模型及必要附件、冻结语义规则。未读取先前语义报告、author-review、其他批次报告或开发参考答案。作者标签仅为被审对象。

冻结规则已读：model-review/SKILL.md、model-review/references/semantic-review.md、goal-extraction/references/goal-boundaries.md、evidence-rules.md、goal-model-building/references/modeling-rules.md。

## DOC011

- 完整读取 source.txt：T000–T055、T056–T085、T086–T110；最初将 source-input 和全文合并输出发生截断，已分段补读，未以截断结果声称完整。
- 原始 source-input 已核对 T000–T035 及元数据，全文轮次依据 source.txt。后续索引与哈希由 read_inputs.py 实测。
- 已先从全文形成语义判断，再核模型：个人增量偏好有独立开发例外；云端恢复以已经上传代码为限；历史可视化是 nice-to-have；AI 是建议和额外反馈；pull/push 维持目标依主要用途合理推断。

## DOC017

- 在读取模型前完整读取 source.txt T000–T113（114轮，5530-token工具输出无截断）；source-input 轮数114，源哈希实测匹配 assignment。
- 来源检查点：主动求职即时、非主动每周；偏好邮件但手机通知可接受且不能淹没；简洁信息并希望快速申请；帖子慢但有推荐人脉价值；资料转移减少重复填写但保留按岗自定义；AI识别岗位可用，写申请必须人审且不自动；保存/跟踪应集成，隐私和后续状态/反馈为明确诉求。

## DOC018

- 在读取模型前完整读取 source.txt T000–T069（70轮，无截断）；source-input 轮数70，源哈希实测匹配 assignment。
- 来源检查点：iPad为主要阅读设备；Google Drive/Kindle导出与新学校阅读app都是候选；原有Kindle处理PDF被认为更容易；个人库保存有价值课程PDF供以后复查；按年月检索源于记忆策略；章节百分比与既有剩余时间功能须区别；费用希望已包含在学校费用中；本人不知有无网页版，不能变产品事实。

## DOC019

- 在读取模型前完整读取 source.txt T000–T064（65轮，无截断）；source-input 轮数65，源哈希实测匹配 assignment。
- 来源检查点：主要长期退休财务规划，次要金融知识、再其次求职相关算法知识；本人将大小盘/加密安全性当经验信念；Coinbase地区定位明说assumption；银行接入/兑换需更容易而非法律绕行；交易本身认为简单，上手接银行仍复杂；新闻、进阶算法/期权教育、共同基金、语音均不同强度建议；换平台意愿低但有不可或缺功能例外。

## DOC021

- 在读取模型前完整读取 source.txt T000–T076（77轮，无截断）；source-input 轮数77，源哈希实测匹配 assignment。
- 来源检查点：基本筛选与额外设施优先级不同，筛选可选；宠物条件可选择包括未填写者，不推断其真允许；外部联系是当前策略，清楚快的站内单处沟通仍受欢迎；表单早索个人信息令人不适，希望双方确认有房和兴趣后再提供；喜欢地图圈选、评论；希望比较3/4项与易找到收藏；详情基本足够，更新日期不足是重点；照片规范是建议而非已证欺诈。

## DOC036

- 在读取模型前完整读取 source.txt T000–T039、T040–T076（77轮，两次输出均无截断）；source-input 轮数77，源哈希实测匹配 assignment。
- 来源检查点：为节日女友买蛋糕/礼品，或先看款式去实体市场；到新地区快速发现本地商家及联系方式；认为地理搜索可能自动定位而不确定；通常偏好商家电话/WhatsApp但站内聊天可用；欣赏图片多样性、搜索历史和社交联系用途；匿名浏览/控制耗时有明确意图；私密账户只希望近友可见；互动年龄启发式是个人判断不是平台排名或安全认证；交货后付款是曾遇可疑商家策略，后续正常购物也描述先付款，不能推广唯一付款顺序；明说应显示价格，商家隐藏动机只是猜测。

## 完成检查点

- DOC011 10/10、DOC017 16/16、DOC018 8/8、DOC019 17/17、DOC021 7/7、DOC036 13/13，共71/71；6篇514轮全部读取，source/model字节哈希实测均匹配assignment。
- 每目标完整statement/actor/conditions/origin/inference/support、绑定引文和相关questions/issues均已核对；相关extraction/judgments映射与模型必要字段逐项对照，作者标签不作为答案。
- DOC019 model原始综合输出中G09–G11附近有截断，已单独完整补读G09/G10/G11；不是来源全文截断。DOC036分两块全文阅读，两块无截断。
- DOC018为核对RR3-001，另读G02/G05/G06/G07完整statement/conditions/evidence，使12目标现有覆盖检查完整；这4目标不加入本轮已审目标数。T049章节剩余时间在G06/G07证据中，但无statement/conditions独立表达；正面赞赏可支持维持推断，独立/合并表达方式仍未知，保留候选风险。
- 本轮新确证实质语义错误0，未确证遗漏风险1（RR3-001）。精化组仅读依赖上下文，没有重新核组，reviewed_group_ids均空。未重新评价非assignment目标，也未查看先前G17结论。

