from pathlib import Path
exec(Path('output1/revised/_authoring/batch1_helpers.py').read_text(encoding='utf-8-sig'))
DOC='DOC017'
g=[
goal(1,'direct','收到符合软件工程或机器学习方向、个人技能和资格条件的职位更新',3,'I would like to get job roles specific to the domain such as software engineering or machine learning roles.','明确个人相关性目的，资格政策由T037补充；不设系统自动录用保证。',['考虑签证、经验和工作资格；本人提到约50%/60%技能匹配会考虑申请，语气含I think非固定统一门槛。'],extra=[(37,'other policies and stuff like visa, status, etcetera, or whether I\'m eligible to work based on my experience.')]),
goal(2,'direct','积极求职时职位发布即获更新，非积极求职时每周更新即可',5,"if I'm actually looking for Job right? So it would be great if I receive at the instant. The job is like posted",'明确按求职状态区分时效，未把每周和即时判矛盾。',['本人对市场每日职位数量判断未经验证。'],extra=[(5,"if I'm not looking actively, then it's okay to receive once in a week")]),
goal(3,'direct','优先通过职业邮箱接收更新，手机通知也可但应避免复杂和塞满通知栏',7,'I would generally prefer getting via emails.','明确渠道偏好并保留手机条件，不变成邮件唯一。',['过多无关通知曾使重要机会淹没，不要求禁用所有通知。'],extra=[(7,"job notifications would also be great unless it's like too complicated. And it's like filling all my notification tab")]),
goal(4,'direct','职位更新邮件简洁并含所需必要详情及直接申请按钮',9,'the email should be very concise','T009整段直接要求简洁、必要详情与按钮；简洁不意味着删关键内容。',['必要详情字段未完整确定。'],extra=[(9,'should be having a direct apply button in the email itself')]),
goal(5,'direct','希望可直接或在页面内申请职位，减少往返应用和公司门户的操作',67,'that would be really great to have integrated right?','认可集成公司申请页的具体建议，结合邮件quick apply减少导航目的；不自动等同未经确认提交。',['页面内公司门户为认可方式；实际可实现性未核验。'],extra=[(9,"so that I don't need to waste time then navigating to the app, and then again, going to the company's portal")]),
goal(6,'direct','评估职位时了解角色适合程度、报酬、地点、公司声誉及员工对工作和技术栈的评价',19,'one is the role like, I\'ll see if the role is really interesting. And I\'m suitable for that role second is the payment. And then comes the location. And of course the company reputation.','保留本人选择因素与次序，不把排名变硬性必需或精化。',['关注具体工作、技术栈和能给团队的贡献；未给权重或工资阈值。'],extra=[(21,'the reviews from the current employees. What work they are specifically working on, what text they are using. And how will I be contributing to their team')]),
goal(7,'direct','将职位详情按列表、卡片或表格等清晰组织，并区分描述与职责以方便定位阅读',23,'formatted in terms of list cars and tables that would be really helpful for me to navigate and get the actual details','本人接受结构化展示建议并明确定位用途，方式是可选举例非要求三种同时。',['本人抱怨长描述需反复滚动；不推断删除全部描述。'],extra=[(65,'having separate ui for the description alone, and having separate for the responsibilities')]),
goal(8,'direct','在个人档案保存角色、经历、技能、项目和可自定义关键词，以持续获得相关职位并减少重复设置',39,"based on my experience, based on my skill sets. And what are the things I think project all that? Maybe I'll be mentioning in my profile.",'本人理想配置与T041/081明确持久化意图，不把自动过滤性能当事实。',['希望列表预先使用档案，而不是每次另加过滤器。'],extra=[(41,'customizing few keywords for the job search to kind of get me the relevant result'),(81,"it kind of persist. Right? I don't wanna again change those.")]),
goal(9,'direct','标记无兴趣或屏蔽的职位后，希望它们不再重复出现',57,"I just say that I'm uninterested. and I hope that it doesn't come.",'已有动作连明确期望，保留hope强度；不推断全类别永久黑名单。'),
goal(10,'direct','职位列表应保持相关和更新，避免申请明显过时的职位',71,"I don't want to apply for jobs which are like one year back, or even 6 months back",'明确避免过时结果，六个月/一年为拒绝的例子而非精确最大年龄。',['不愿继续使用不相关或陈旧列表；未给有效职位的统一截止年龄。']),
goal(11,'direct','申请时自动带入已有资料以减少重复手填，同时允许针对某些职位修改内容',73,"I don't want to have a lot of manual efforts in filling up just a job application.",'明确减少重复录入并保留定制例外，T067认可资料转入公司网站方式。',['部分职位愿意定制；不要求完全禁止编辑。'],extra=[(73,'sometimes I I would like to kind of customize my details for few of the job roles'),(67,'all the details from my job portal is already like transferred')]),
goal(12,'direct','在求职门户内保存和追踪感兴趣职位，方便稍后申请而无须另开笔记应用',77,"It'd be great to have such features in the job portal itself",'认可内置保存追踪建议，原先记职位ID/Notion是策略；不认证LinkedIn是否有书签。',['本人不确定现有平台有无bookmark。'],extra=[(75,"I'm not sure if Linkedin has a bookmark feature.")]),
goal(13,'direct','保持申请职位及个人求职数据私密，避免其他人知道申请方向或从外部平台来联系',83,"I don't want people to know for what job roles I'm applying for.",'明确申请隐私并结合外平台曝光顾虑；不推断禁止必要招聘方处理申请。',['谁可因申请而查看数据的精确授权边界未说明。'],extra=[(85,"I don't want my data to be exposed by other people apart from the platform.")]),
goal(14,'direct','可以用AI发现匹配职位；AI代写申请内容须经本人核实且不能自动进行',95,"if it is like verified by us, then it's good. But yeah, but it shouldn't be automatic.",'回答AI必要性时区分识别职位与写申请，保留人工核实方式约束和不可靠信念。',['AI识别职位受欢迎但未被明确宣称绝对必需；申请撰写自动化不被接受。'],extra=[(93,'it will be great to actually identify jobs.')]),
goal(15,'direct','能追踪自己申请的状态和雇主的回应情况',105,'I want to know what is my status of my application?','明确很重要（自评10/10），不把重要性变精化或量化满足概率。'),
goal(16,'direct','希望收到申请反馈，以改进后续申请',105,'if there is any feedback that would be really great for me to improve in my further applications.','明确改善用途，未要求必须面试或录用。'),
goal(17,'direct','通过发布职位的人建立联系并可能获取转介',17,'it kind of helps me, because I kind of connect with the person some referral for the job.','现有帖子虽慢但有联系转介用途，不能只将其列障碍而丢正面目的。',['对需要快速申请的情况，等对方再发链接不理想。']),
goal(18,'inferred','减少无关职位通知及陌生人的无关求职联系，避免重要机会被淹没',25,'the notification system was not that accurate? And it was sending almost like what? All the jobs right?','无关洪流导致漏重要机会，结合不愿使用理由，正面支持减少噪声的意图而非零通知。',origin='inferred',reason='本人因过量不相关通知错过机会，并说随机通知/人联系会阻止使用，故推断减少这些干扰。',assumptions=['希望避免重演漏机会情境。'],extra=[(27,'I kind of missed few of the important jobs.'),(69,'getting random job notifications. Random people reaching me out')]),
goal(19,'direct','按本人最后的总结，理想职位更新应匹配个人条件并提供快捷申请入口',99,"if it's kind of matching with my criteria.",'T099先列匹配，再提quick apply，T101认可两项总结；将父目标限定于最后这两个要素，非完整理想平台。',['此处只表达最后总结的两个要素；时效、隐私、资料流转仍为独立要求。'],extra=[(99,'if there is a quick, apply button right? Then it will be like, great')])]
f=[group(1,19,[1,5],99,"if it's kind of matching with my criteria.",'在父目标明确限于“匹配个人条件+可快捷申请”两项的范围下，G01给匹配更新，G05给直接/页内申请，二者共同满足父句；T100—101认可。不是全部理想门户充分性。',['父目标仅是最后两项总结，不将简洁邮件、隐私和时效自动算已满足。'],status='supported',completeness='complete')]
q=[question([1,8],'匹配标准、技能比例及签证资格如何具体设定并调整？','50/60%为含糊例示，不足确立统一门槛。'),question([4,6],'邮件必要字段与简洁长度怎么取舍？','需要详尽信息但又要简洁，尚无格式阈值。'),question([11,13,14],'资料可传给哪些公司页面，哪些内容须本人修改核实后才提交？','自动预填、隐私和禁止自动写申请需要具体边界。'),question([10],'如何判断岗位仍开放及过时，多久算太旧？','六个月和一年为例子，未给完整新鲜度标准。')]
r='''# DOC017 生成方语义自检

完整读 T000—T113，114轮全部问题回答，按0—54/55—113分段。未核听、未验证LinkedIn/Handshake功能及市场事实；本记录为同一作者自检。

逐目标：G01方向/技能/资格，比例仅个人含糊经验；G02积极即时/非积极每周条件；G03邮件优先且手机可接受但别刷屏；G04简洁+详情+按钮不删方法；G05认可集成申请页，不擅自自动提交；G06选择因素及原文顺序，未硬化排序；G07列表卡片表格可选及职责分区；G08档案预设持续化/关键词；G09uninterested后希望别重现；G10避免过旧而不造统一年龄；G11预填与针对职位定制例外；G12内置保存追踪的明确建议，不把Notion变必须；G13个人申请私密/外平台曝光，招聘方访问范围待定；G14 AI识别受欢迎但非绝对必需，写申请人工核实且不自动；G15申请状态重要性；G16反馈改进；G17帖子还有转介用途，保留慢与有用共存；G18从错过机会及不愿使用原因推断减噪；G19限于最后两项总结的理想更新。

F01全部端点与整句重核，supported/complete仅针对父句限定的“匹配条件且快捷申请”两个属性；G01涵盖个人条件，G05涵盖快捷申请方式，原文T099及T101确认其总结。不能把该组理解为整个理想应用、成功求职或快速录用的充分方案。已考虑G03/G08/G09/G18对相关通知的贡献：渠道、档案和屏蔽可能帮助，但不保证零漏重要机会，不画充分边；隐私与自动资料转移潜在取舍未假装冲突已证。

正常场景（分析假设）：积极求职者档案匹配技能资格，邮件简洁含申请入口，资料预填后本人定制核实；F01的两个属性满足，时效和隐私仍各自检查。异常场景（分析假设）：职位技能相关但已关闭，F01匹配/快捷不等于G10新鲜度满足。异常场景（分析假设）：AI生成申请有误，按G14不得自动提交，需本人核实。边界场景（分析假设）：非积极求职者每周通知即可，不用即时轰炸；被屏蔽职位再次出现会违反G09期望但不代表全组无效。

没有把Hr/中介可能受益的推测当本人承担需求；没有把受访者推测算法运作当产品事实。未决问题进入交付，人工pending；独立语义/形式证明not_run。实际工程绑定及inspect由冻结脚本执行。
'''
save(DOC,g,f,q,r)
