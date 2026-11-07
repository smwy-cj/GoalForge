# 目标模型

版本：v1。人工待审。

- Receive job updates for roles in the user's domain (e.g. software engineering, machine learning) that match the user's skill set
- Receive a job update at the instant the job is posted on the platform while actively looking for a job
  适用条件：while actively looking for a job
- Receive job updates once a week when not actively looking for a job
  适用条件：when not actively looking for a job
- Have the job list derived automatically from the profile (roles, work done, experience, skill sets, projects) so no additional filters need to be added
  适用条件：profile details already provided
- Customize a few keywords for the job search in the profile to get relevant results
- Receive only job postings relevant to the user's criteria, not a random or unrelated job list
- Have the job list kept up to date so that postings one year or even 6 months old are not presented
  适用条件：postings older than about 6 months to 1 year
- Be able to blacklist a job or mark it as uninterested so that it no longer comes back
- Receive job updates by professional email
- Also receive job updates as mobile notifications provided they are not too complicated and do not fill up the mobile notification tab
  适用条件：unless too complicated or filling the mobile notification tab
- Not miss important job opportunities because notifications were inaccurate or unrelated
  适用条件：notification system inaccurate / unrelated jobs
- Have the job notification email be very concise
- Have all the necessary job details present in the notification email itself
- Apply to a job directly from where the update is received via a direct apply button in the email or a quick apply button in the portal, instead of navigating to the app and then the company's portal
  适用条件：in the email itself / in the portal
- Complete a job application quickly
- View and apply through the company's job portal in an in-page (integrated) view inside the application instead of being navigated to another page
- Have profile details already entered in the job portal transferred into the company's website/application form instead of filling them in again after uploading a resume
  适用条件：after uploading a resume
- Be able to customize application details for a few specific job roles
  适用条件：for a few specific job roles；without a lot of manual effort
- Avoid getting jobs through a person's post that requires several rounds of messaging and waiting for a link
  适用条件：when navigating to a job from a person's post
- Be able to connect with the person who posted the job to get a referral
  适用条件：via a person's post
- Decide which job postings to apply for by weighing role interest and suitability, payment, location and company reputation
- See reviews from current employees of the company
- See what work the team is specifically working on and what stack they are using
  适用条件：transcribed 'what text they are using', read as tech stack by context
- See how the user would be contributing to the team or to the company
- Have tech stack and similar details formatted as lists, cards or tables so they can be navigated quickly
- Have the job description and the responsibilities shown in separate UI sections instead of one long block
- Have the necessary skill set explicitly defined in a job posting
- Have a tool or plugin that matches the required skill set against the user's and gives a match percentage
- Use AI to identify and signal jobs that match the user's interest and skill set
  适用条件：AI used for identifying jobs, not writing applications
- Not have AI write the application automatically; anything AI produces for writing should be verified by the user
  适用条件：writing applications
- Have visa status, work eligibility and similar policy conditions taken into account when judging a job posting
- Save or bookmark interesting job postings inside the job portal to apply to them later
  适用条件：LinkedIn bookmark feature uncertain
- Have every job-related activity available inside the job portal without navigating to another application or the company's portal
- See and track the status of submitted applications
- Receive employer feedback on applications in order to improve later applications
- Keep applications private so other people cannot see which job roles are being applied for
- Not have personal data exposed to people or platforms outside the job platform
- Not be contacted by random or irrelevant people or recruiters through the platform
- Let the company's HR find the perfect candidate for a role through this feature
- Be able to enter more detailed profile information such as work experience and schooling
- Have configured profile details persist so they do not have to be entered again
- Not be given a huge list of jobs that leaves the user confused about what to apply for
- Have job agencies benefit from these job update features

## 目标之间的联系

下列联系不表示充分精化；待确认及已否定记录保留各自状态。

- 有依据的联系：Apply to a job directly from where the update is received via a direct apply button in the email or a quick apply button in the portal, instead of navigating to the app and then the company's portal —[实现方式]→ Complete a job application quickly
  依据：直接/快速申请按钮是快速完成申请的明确实现方式，T009 用 'so that I don't need to waste time' 连接方式与目的
- 有依据的联系：View and apply through the company's job portal in an in-page (integrated) view inside the application instead of being navigated to another page —[范围具体化]→ Have every job-related activity available inside the job portal without navigating to another application or the company's portal
  依据：页面内嵌申请是'一切在门户内完成、不跳转别处'在公司门户申请这一具体情境下的具体化
- 有依据的联系：Save or bookmark interesting job postings inside the job portal to apply to them later —[范围具体化]→ Have every job-related activity available inside the job portal without navigating to another application or the company's portal
  依据：门户内置收藏是'不跳转到另一个应用'在保存职位这一具体情境下的具体化
- 有依据的联系：Receive job updates by professional email —[实现方式]→ Receive job updates for roles in the user's domain (e.g. software engineering, machine learning) that match the user's skill set
  依据：T006 明确问通过哪些渠道接收职位更新，专业邮箱是接收匹配职位更新的选定渠道
- 有依据的联系：Also receive job updates as mobile notifications provided they are not too complicated and do not fill up the mobile notification tab —[实现方式]→ Receive job updates for roles in the user's domain (e.g. software engineering, machine learning) that match the user's skill set
  依据：移动端通知是接收职位更新的另一渠道，且保留 unless 例外
- 有依据的联系：Customize a few keywords for the job search in the profile to get relevant results —[实现方式]→ Receive only job postings relevant to the user's criteria, not a random or unrelated job list
  依据：T041 明确用 'to kind of get me the relevant result' 表明关键词自定义服务于获得相关结果
- 有依据的联系：Have the job list derived automatically from the profile (roles, work done, experience, skill sets, projects) so no additional filters need to be added —[实现方式]→ Receive only job postings relevant to the user's criteria, not a random or unrelated job list
  依据：资料驱动的自动筛选服务于提供已匹配的相关职位列表，无需再加筛选
- 有依据的联系：Have a tool or plugin that matches the required skill set against the user's and gives a match percentage —[实现方式]→ Receive only job postings relevant to the user's criteria, not a random or unrelated job list
  依据：T032 问如何定义相关职位，T033 以技能匹配百分比工具作为判断相关性的方式，'So with that, I'll consider'
- 有依据的联系：Not have personal data exposed to people or platforms outside the job platform —[实现方式]→ Not be contacted by random or irrelevant people or recruiters through the platform
  依据：T085 用 'So' 连接：不希望被其他平台的人联系，因此不希望数据暴露给平台之外，前者以后者为实现方式
- 有依据的联系：Receive a job update at the instant the job is posted on the platform while actively looking for a job —[范围具体化]→ Receive job updates for roles in the user's domain (e.g. software engineering, machine learning) that match the user's skill set
  依据：T004 问接收频率，主动求职时即时接收是接收匹配职位更新在该情境下的具体化
- 有依据的联系：Receive job updates once a week when not actively looking for a job —[范围具体化]→ Receive job updates for roles in the user's domain (e.g. software engineering, machine learning) that match the user's skill set
  依据：非主动求职时每周接收是接收匹配职位更新在另一情境下的具体化

## 需要确认

- 原文尚不足以支持这项目标，或存在相反证据。
- 邮件既要 'very concise' 又要 'All the details are present in the email'，两者的边界（哪些详情、多长）如何确定？
- 邮件既要 'very concise' 又要 'All the details are present in the email'，两者的边界（哪些详情、多长）如何确定？
- 希望在资料中填写更详尽的工作经历与教育背景，同时又要求申请与数据保密；二者如何同时满足？
- 希望在资料中填写更详尽的工作经历与教育背景，同时又要求申请与数据保密；二者如何同时满足？
- 希望在资料中填写更详尽的工作经历与教育背景，同时又要求申请与数据保密；二者如何同时满足？
- 招聘中介被列为受益方，但原文未说明其具体需求或使用方式，是否需要补充访谈？
- T015 'When I want to do my application quickly' 一句转写断裂（'do my up'），快速申请的验收标准（步数/耗时）未给出
- 'once in a week' 是期望频率还是仅为可接受下限？
- T021 'what text they are using' 疑为 tech stack 的转写错误，按上下文理解为所用技术栈，需核对录音
- 除通知准确外，原文未说明防止错过重要职位的具体机制（置顶、二次提醒等）
- 'verified by us' 的具体含义（逐字确认还是整体确认）与 AI 可参与的边界未明确
- AI 用于识别职位与不得自动代写之间的分界（如自动填充表单字段是否属于代写）未说明
- AI 用于识别职位与不得自动代写之间的分界（如自动填充表单字段是否属于代写）未说明
- G033 的子目标只覆盖申请与保存，未覆盖查看员工评价/技术栈/职责区块、跟踪状态与反馈等操作；需确认是否可声称整组充分，否则维持 proposed/partial
- 招聘中介无具体意图内容，目标为 insufficient，需补访谈或明确排除
- 与 G013 的邮件详略张力未解决
- 与 G012 的邮件详略张力未解决
- label 为 inferred，仅由负面经历推断，需确认防错过机制与可接受的支持强度
- T015 转写断裂，快速申请的判定标准未给出
- label 为 inferred，签证/资格是否由系统判断、信息来源为何未明
- 原文 'what text they are using' 存在转写歧义，需核对录音
- G037→G038 的操作化方向依赖 T085 中 'So' 的因果读法，需确认方向未写反
- 全篇为单人访谈，多个目标来自偏好、现状体验或让步推断，无第二受访者交叉验证；成立精化组数为 0
- 这组层级仍需确认，尚未作为成立的精化展示。
- 只读取 source/DOC017.json 提供的 114 轮访谈转写，未读取其他材料或参考答案，未联网
- 原文为访谈转写，存在多处转写异常（'what text they are using'、'list cars'、'Eas'、'Sean and Chris'、'do my up'、T027/T029 跨轮断裂），按上下文理解并在 context/问题中记录，未改动原文
- 窗口按 size=4/stride=2 生成，共 56 个；逐窗捕获后做一次全篇校正，未做独立重复采样
- 未执行独立语义审查与形式证明；精化充分性为编制者判断，非程序证明

原文与层级依据可在 HTML 中展开。结构检查不等于语义证明，意见导出后交回助手。
