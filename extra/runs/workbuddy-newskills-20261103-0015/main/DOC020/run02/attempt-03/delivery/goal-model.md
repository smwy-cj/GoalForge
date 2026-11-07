# 目标模型

版本：v1。人工待审。

- Check email at least daily so that no newly arrived recruiting information is missed while applying for jobs.
  适用条件：while applying for jobs；reported use at least 5 times a day, rising to 10-20 times a day
- Receive and check school-broadcast news and notifications through email.
- Book dentist or clinic appointments through email for personal purposes.
  适用条件：personal purposes
- Receive merchant sales and discount information through email.
- Contact friends by email, occasionally.
  适用条件：reported as rare
- Keep the inbox manageable by deleting unimportant mail and threads that have ended, and by keeping separate accounts for each purpose (recruiting, school notifications, special deals).
  适用条件：stakeholder's own practices, stated as the way he keeps the inbox manageable；no numeric standard for 'manageable'
- Ensure important emails do not end up in the spam folder, accepting extra spam rather than losing important messages.
  适用条件：automatic categorization is the reported cause；explicit trade-off: extra spam is acceptable
- Allow editing an email after it has been sent instead of sending a new one, with the recipient seeing the latest version and being able to view the edit history.
  适用条件：expressed as a preference ('would probably be better')；current client only allows cancelling a send within 3 seconds
- Have the AI assistant compose a well-organized email from a few listed main points, which the sender then adjusts.
  适用条件：currently done with an external AI tool, not built into the client；ideal case: a two-line request becomes a well-organized email
- Have the AI assistant extract the main points of a received email.
- Highlight keywords in received emails so that important details are not missed.
  适用条件：based on a real case where a small line about not retaking an assessment was missed
- Receive notifications for important messages only where importance detection is reliable, without relying fully on AI to identify important mail.
  适用条件：condition: only if identification is 'really reliable'；explicit refusal to rely fully on AI
- Keep email forwarding available as a critical capability when working under tight deadlines.
  适用条件：under tight deadlines；existing feature he rates as very important
- Keep BCC bulk sending to a whole group or team available when working under tight deadlines.
  适用条件：under tight deadlines；interviewer confirmed the meaning as bulk mail to many people quickly
- Provide search as the highest-priority email feature, since it is used every day.
  适用条件：ranked above scheduling; tag filtering is considered coverable by search；scheduling ranked second
- Support self-assigned category IDs so that people who set the same category (for example recruiting or HR notifications) can communicate through it.
  适用条件：stakeholder qualifies the idea as 'probably not that practical'；sender and receiver both set the same category id
- Have AI assistance built into the email client to help read and write emails.
  适用条件：named as the feature he wants；also stated as the first future need
- Ensure that emails expected to arrive, such as website sign-up or verification emails, actually reach the inbox.
  适用条件：reported as a reliability obstacle；includes sign-up/verification mail from websites
- Warn the sender before sending when the message refers to an attachment that is not attached.
  适用条件：existing behaviour he evaluates positively；evaluated as 'really good', not stated as mandatory
- Reduce the time spent reading every email in the inbox.
  适用条件：no target metric given；AI assistance proposed as the means

## 目标之间的联系

下列联系不表示充分精化；待确认及已否定记录保留各自状态。

- 有依据的联系：Have the AI assistant compose a well-organized email from a few listed main points, which the sender then adjusts. —[范围具体化]→ Have AI assistance built into the email client to help read and write emails.
  依据：G009 是 G017（内置 AI 协助读写邮件）在撰写方向的具体情境形态，范围更窄，不覆盖读侧，也不覆盖其他协助方式，符合具体化方向。
  条件／假设：AI 撰写是“内置 AI 协助读写”在写侧的具体形态
- 有依据的联系：Have the AI assistant extract the main points of a received email. —[范围具体化]→ Have AI assistance built into the email client to help read and write emails.
  依据：G010 是 G017 在读侧的具体形态（取收件主要点），范围窄于“AI 协助读写”，方向为具体→一般。
  条件／假设：AI 提取要点是“内置 AI 协助读写”在读侧的具体形态
- 有依据的联系：Highlight keywords in received emails so that important details are not missed. —[范围具体化]→ Have AI assistance built into the email client to help read and write emails.
  依据：G011 在 T045 紧接 AI 读取功能的语境中提出，是 G017 读侧的另一具体能力；仅管关键词，不覆盖整体阅读协助。
  条件／假设：关键词高亮属于“AI 协助阅读”的具体能力
- 有依据的联系：Have the AI assistant extract the main points of a received email. —[实现方式]→ Reduce the time spent reading every email in the inbox.
  依据：T053 把“读所有邮件耗时”列为待简化任务，并把 AI 助手作为手段；G010（AI 取主要点）是该手段的具体实现方式，服务于 G020。仅属帮助关系，不声称足以消除全部读信时间。
  条件／假设：以 AI 助手承担阅读工作；摘要主要点可减少逐封通读的耗时

## 需要确认

- 类别/协议邮件设想在同段被自评为“probably not that practical”，应作为弱需求保留还是仅作备选设想？
- “收件箱可控”没有量化标准，删除与分账户是受访者现状习惯，是否要求新客户端支持这些做法？
- “unless it's really reliable”未给可靠性的判定方式或阈值，何时允许依赖自动识别重要邮件仍需确认。
- 未送达问题的范围（哪些邮件类型、是否包含验证码）与可接受的处理方式（重发、告警、回执）原文未说明。
- 读信耗时没有量化指标，无法设定验收阈值；是否以“摘要替代通读”为验收方式也未说明。
- 本组缺写侧附件提醒（G019）与格式调整，且阅读侧存在 AI 漏判的反例；是补入子目标还是保持不成立，需人工确认。
- 摘要是否真能减少读信时间属于分析判断，原文只给“会很有帮助”的期望；若需更强依据请补充。
- 采访者提出的周期摘要（T054：3 封摘要代替 30 封）仅获“could be one solution”弱认可，现未建为目标，请确认是否需要补入。
- 这组层级仍需确认，尚未作为成立的精化展示。
- 原文为英文访谈自动转写，含重复词、断句与疑似识别错误（如 'spans' 应为 spam、'1st market' 应为 mark it、'BBC' 应为 BCC），判断按上下文理解，未逐字纠正原文。
- 访谈未涉及可量化验收标准（阅读耗时、可靠性、通知准确率等），相关目标只能保留方向性表述。
- 采访者提出的方案（如周期摘要）与受访者的弱认可已分开记录，采纳状态未知。

原文与层级依据可在 HTML 中展开。结构检查不等于语义证明，意见导出后交回助手。
