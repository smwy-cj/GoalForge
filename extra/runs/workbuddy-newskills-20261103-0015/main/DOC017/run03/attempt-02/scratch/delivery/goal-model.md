# 目标模型

版本：v1。人工待审。

- Receive job postings for roles specific to the stakeholder's domain, such as software engineering or machine learning roles.
- Receive job updates matched to the stakeholder's skill set.
- While actively looking for a job, receive a job update at the instant the job is posted on the platform.
  适用条件：the stakeholder is actively looking for a job
- While not actively looking for a job, receive job updates once a week.
  适用条件：the stakeholder is not looking actively
- Receive job updates by email, preferably a professional email.
- Avoid mobile job notifications that are too complicated or that fill up the notification tab.
  适用条件：job notifications are delivered on the stakeholder's mobile
- Receive a concise email that carries the necessary job details.
  适用条件：job updates are delivered by email
- Apply directly with a single quick apply action available in the email or on the job update, instead of navigating to the app and then the company's portal.
  适用条件：a direct/quick apply control is offered where the job update is shown
- See employee reviews, the team's current work and tech stack, and how the applicant would contribute, in the job information.
- View job details such as the tech stack in a list, card or table layout that is easy to navigate.
- Receive job updates that are relevant to the stakeholder, so that important jobs are not missed among irrelevant ones.
- Have AI identify jobs that fit the stakeholder's interests and skill set.
- See work-eligibility information such as visa status and experience-based eligibility for a posting.
- Have the job list generated from the stakeholder's profile (experience, skills, projects) so that no additional filters are needed.
- Customize a few job-search keywords in the profile to get relevant results.
- Mark a job as uninterested or blacklist it so that it stops appearing.
- View the company's job portal in an integrated in-page view inside the app.
- Transfer the details from the job portal to the company's website automatically.
- Avoid random job notifications and random people reaching out to the stakeholder.
- Exclude job postings that are six months to a year old or older.
- Avoid manual re-entry of details already provided in the resume or configured in the profile.
- Customize application details for a few specific job roles.
- Save interesting job postings for later tracking inside the job portal itself.
- Keep the stakeholder's applications private so that others cannot see which roles were applied for.
- Keep the stakeholder's data from being exposed to people or platforms outside the job platform.
- Require the stakeholder to verify AI-drafted application content instead of sending it automatically.
- See the status of each submitted application.
- Receive feedback on applications that helps improve further applications.
- Show the job description and the responsibilities in separate UI sections.

## 目标之间的联系

下列联系不表示充分精化；待确认及已否定记录保留各自状态。

- 有依据的联系：Have the job list generated from the stakeholder's profile (experience, skills, projects) so that no additional filters are needed. —[实现方式]→ Receive job updates matched to the stakeholder's skill set.
  依据：以档案（经验、技能、项目）自动生成岗位列表，是实现'按技能集匹配更新'的一种手段；原文把列表生成依据直接落在经验与技能集上，方向为手段→目的。
  条件／假设：档案内容（经验、技能、项目）足以代表受访者的技能集
- 有依据的联系：Have AI identify jobs that fit the stakeholder's interests and skill set. —[实现方式]→ Receive job updates matched to the stakeholder's skill set.
  依据：原文以算法按兴趣与技能集匹配、给出必要岗位来描述被称赞的 AI 机制，属实现'按技能集接收更新'的方式目标；未声称该方式在所有情况下都充分。
  条件／假设：AI 匹配可作为技能匹配的实现方式
- 有依据的联系：Mark a job as uninterested or blacklist it so that it stops appearing. —[有助于]→ Receive job updates that are relevant to the stakeholder, so that important jobs are not missed among irrelevant ones.
  依据：把不相关岗位标记为不感兴趣并要求其不再出现，有助于减少不相关推送这一目标；单次标记不保证整体相关性，故只作贡献不作精化。
- 有依据的联系：Transfer the details from the job portal to the company's website automatically. —[有助于]→ View the company's job portal in an integrated in-page view inside the app.
  依据：把平台内资料转移到公司网站，能减少页内申请时的重复录入，从而帮助'在应用内页内查看公司门户并申请'这一目标；不构成其充分条件。
  条件／假设：公司网站接受转移的资料
- 有依据的联系：Exclude job postings that are six months to a year old or older. —[有助于]→ Receive job updates that are relevant to the stakeholder, so that important jobs are not missed among irrelevant ones.
  依据：原文把'相关或更新的岗位列表'并列陈述，排除六个月至一年以上的陈旧岗位有助于减少不相关更新；只是贡献，非充分。

## 需要确认

- 原句 'list cars and tables' 中的 'cars' 是否指卡片（cards）？
- 'what text they are using' 是否指团队使用的技术栈（tech）？
- 只接收相关更新是否需要一个可判定的标准（如技能匹配度门槛）？
- 非活跃期的'一周一次'是必须的上限，还是仅表示可接受？若为上限，需明确超过频率即违规。
- '相关'是否需要可判定标准（如技能匹配度或领域限定），还是交由平台自行判断？
- 签证/资格信息是平台应展示的内容，还是受访者自行核对的习惯？原文只说明这是其考虑项。
- 原文为英文访谈转写，含明显识别噪声（'text' 疑为 tech、'cars' 疑为 cards、'Eas' 疑为 AIs、'A can tell you' 疑为 AI can tell you、'those reviews' 疑为衍文），按上下文理解并在目标中未加入额外内容。
- 多处内容是对 LinkedIn/Handshake 现有体验的描述，是否等同对新系统的要求需人工确认；本次按'被问及理想做法时的正面表述'取舍。
- 无音频可核听，转写错词无法逐字校正。
- 未进行独立语义评审，判断仅代表生成会话在同一上下文中的自检。
- C014（个人申请优先级：角色→薪资→地点→公司声誉）未映射为最终目标：原句是对自身申请习惯的描述，未表达系统排序要求，保留为待确认项。

原文与层级依据可在 HTML 中展开。结构检查不等于语义证明，意见导出后交回助手。
