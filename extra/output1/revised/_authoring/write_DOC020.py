from pathlib import Path
exec(Path('output1/revised/_authoring/batch1_helpers.py').read_text(encoding='utf-8-sig'))
DOC='DOC020'
g=[
goal(1,'direct','及时掌握招聘方的新邮件信息，避免漏掉求职进展',9,"check my email every day to make sure that I I didn't lose any new information on that.",'明确接收招聘信息目的，频繁查看是个人策略非系统频率要求。'),
goal(2,'direct','通过邮件了解学校广播的新闻和活动通知',9,'check about the news that broadcasted by school.','本人第二目的直接，不把采访者networking推测自动纳入。'),
goal(3,'direct','通过邮件预约诊所或牙医，并接收商家优惠，偶尔联系朋友',11,'For booking. I let\'s say, dentist or clinic or booking the appointment.','同属本人说明的个人通信用途；商家优惠与朋友联系逐项有原文支持。',['朋友联系少见；未赋予优先级或硬阈值。'],extra=[(11,'get the information from merchandise, like, if they have sales or discounts'),(11,'rare. But I also use email to contact with my friends.')]),
goal(4,'direct','先标记重要邮件，并将暂时无法处理的任务邮件留待有空时完成',15,'if there\'s some task I have to, I have to do after reply or something. But I couldn\'t do it now. I would just like tag it','动作与延后完成意图明确，保留tag方式，不推断必须自动提醒。',['本人会先快速看未读，删垃圾，再读重要邮件。'],extra=[(15,"when I'm available I will check in and finish the task.")]),
goal(5,'direct','通过删除无关或已结束会话的邮件并分开不同用途的邮箱，让收件箱清楚可管理',17,'make sure that my inbox is manageable','两项本人选定整理策略，不强制所有重要邮件永久留存或保留全部历史。',['本人会删已结束的重要会话；招聘学校与商家优惠使用不同邮箱。'],extra=[(17,'if the conversation has reached to the end. I also did it.'),(17,'I do this by have separate emails.')]),
goal(6,'direct','从简短要点生成组织清晰的邮件，并由本人调整文本、字号和重点加粗后发送',19,'I would 1st list my main point.','常用AI协助写作有明确输入/结果/个人修改方式，保留不必内置的现状。',['目前AI工具不一定内置；G12另为内置愿望。'],extra=[(19,'I would ask the AI Assistant tool to compose an email for me. and I would adjust it a little bit'),(21,'adjust the font size and mark the marks. The sentence. mark the important sentence as bold')]),
goal(7,'direct','少量需要发多媒体时，优先上传云端后发送链接以便收件人在不同设备查看',23,'I would probably upload it to the cloud and then send the link, because I think it\'s easier for the client to view it in any platform','明确有结果的所选方式与probably强度；不是要求所有附件禁止发送。',['多媒体少见，手机和电脑跨平台查看是本人目的。']),
goal(8,'direct','避免重要邮件被误放垃圾箱而忽略，宁愿多收到一些垃圾邮件',27,'I would rather receive some spans instead of ignoring some important messages.','明确避免型目标和误判取舍，未设零漏判或禁止垃圾分类。',['现有自动分类会误判是本人体验；仍会手工删除垃圾。']),
goal(9,'direct','希望发送后能编辑邮件，让收件人先看到新版并可查看旧版和编辑历史',29,'it would probably be better if there\'s an function of editing the email instead of sending a new one.','明确建议保留发送后编辑方式；并非仅延长撤销窗口。',['可取的功能；跨客户端可实现性未知；本人关于3秒撤销为历史体验未验证。'],extra=[(29,'they could see the new email and old email, but they will see the new one. And if they want, they could see the editing history.')]),
goal(10,'inferred','减少网站注册等邮件未能到达收件箱的问题，可靠收到预期来信',33,"when you register some website and then send email to your inbox, and for some reason they're just not there.",'将未收到预期邮件列可靠性障碍，正面支持改善到达意图；不把采访者丢包猜测当原因。',origin='inferred',reason='本人明确将注册后邮件不见视为障碍，因此推断希望预期来信可靠到达。',assumptions=['未到达的预期来信希望被收到；实际发送/投递根因未知。']),
goal(11,'direct','发送前若文中提到附件却未附上，希望收到遗漏提醒',37,"But I didn't attach the resume. It will warn me before I send it. I think that is really good.",'赞赏已有附件遗漏提醒，具体防漏用途明确，维持而非只列功能事实。'),
goal(12,'direct','希望邮件客户端内置AI，将简短意图直接整理成邮件',37,'the feature I want is the AI assistance that is in bills in the email.','明确内置方式愿望，不因结果抽象丢掉集成约束。',['举给教授问作业为例，不要求AI自动发送。']),
goal(13,'direct','希望AI提取来信主旨并突出关键词，减少阅读时间和遗漏关键限制',41,'If AI assistant could help me. Get the main point of that email.','后续明确关键词及错过评测限制造成无效准备的经历；目的与方式都有依据。',['本人不会完全依赖尚不可靠的重要性识别。'],extra=[(45,'And this highlights the keywords'),(47,"I just missed that night, and and I was like wasting some time.")]),
goal(14,'direct','可以考虑定期汇总多封来信以减轻逐封阅读负担',55,'that that could be one solution.','明确接受采访者定期汇总建议为一种方案，未将早午晚三次/30变3升格固定规格。',['只是可选方案，重要信息不能被误漏。'],extra=[(53,'I spend a lot of time just reading every email.')]),
goal(15,'direct','重要来信可以通知，但仅在识别足够可靠时才依赖该机制',59,"I would probably not want to rely on that. Unless it's really reliable.",'明确条件性通知偏好与不完全依赖，不能强造全自动筛重要邮件。',['担心AI漏重要消息；足够可靠阈值未给。'],extra=[(59,'it would be good to receive notification for some important messages.')]),
goal(16,'direct','临近期限团队协作时能转发或群发邮件，让组内多人迅速收到信息',71,'Including the function of forwarding the email. And BBC, like, sent to all the people in my group.','本人选既有关键功能，后续确认BCC在此指快速群发；保留方式不推断强隐私目的。',['紧迫期限场景；T075接受快速广泛送达解释。'],extra=[(73,'That would be very important when it comes to working on deadlines.')]),
goal(17,'direct','保留日常可用的邮件搜索能力，包括按标签等条件查找',87,"the most important would definitely be searching. That's really important. I use it every day",'本人声明不可缺价值，足以支持维持而非现状自动造目标；过滤可由搜索承接。',['在给定选项中搜索最重要，过滤未被当独立次级必须功能。']),
goal(18,'direct','可按计划时间发送邮件，其重要性低于搜索',87,'the second one will probably be scheduling.','在明确解释定时发送后本人排序认可，有偏好意图，probably不强化。',['未给发送时间规则，排序不是AND关系。']),
goal(19,'direct','可以探索双方约定同一类别标识的邮件分类或协议，以方便特定用途的沟通',93,'if my friend also set up this like 8,000 in his app, then we could communicate through like we could identify self, identify the category','未来设想保留双方共享标识方式；8000为例示，受访者承认可能不实际。',['本人称可能不实用；招聘通知/HR为例子；不是已采纳协议标准。']),
goal(20,'direct','未来在工作中通过邮件与公司内外人员保持专业联系',99,'not necessarily people in my company, but just like, professionally','本人说明未来用途，未认证所有外部人都有数据权限。')]
f=[group(1,1,[4,8,13,15],59,'sometimes AI would miss some important message','标记、避免误分类、摘要关键词和通知均可贡献不漏招聘信息，但识别可靠性未定，人工阅读与关注变化也未穷尽；不能保证整组充分。')]
q=[question([8,13,14,15],'怎样衡量重要邮件识别可靠性，摘要与通知遗漏时如何保留原文和人工回查？','本人宁可多垃圾也不愿漏关键，阈值和回退方式待定。'),question([9],'发送后编辑应在什么时间范围、哪些客户端生效，如何呈现新版与历史？','愿望明确，跨系统语义及可实现性未给。'),question([19],'共享分类标识如何协调、冲突或未支持时怎样处理？','仅未来设想且本人不确定实际性。')]
r='''# DOC020 生成方语义自检

完整阅读T000—T103共104轮，按0—54/55—103分段，含所有澄清、假设、排序和结尾。未核听、未核验Gmail撤销时间或邮件投递机制；同一助手自检。

逐目标：G01招聘信息不漏；G02学校通知；G03预约/优惠/偶尔朋友逐项证据；G04标记延后任务；G05删除加分邮箱两策略，保留已结束重要会话也删；G06 AI从要点组织且本人调整样式后发；G07多媒体少见且偏云链接跨设备；G08避免误屏蔽且宁多垃圾，未造零误差；G09发后编辑新版优先历史可查，非撤销延时；G10注册来信不到为推断可靠到达，丢包是采访者猜测不采用；G11附件漏附提醒为有用途维持；G12内置AI是明确方式；G13主旨关键词用于时间与不漏限制，已保留不全依赖AI；G14定期摘要仅一种方案，频次数字是采访者例示；G15通知依赖以可靠为条件；G16期限团队转发/BCC群发认可，未自行赋BCC隐私目的；G17搜索不可缺维持，标签过滤可用搜索；G18排序认可定时发送而非硬性所有邮件排程；G19双方类别标识为不确定未来协议建议；G20未来专业联系含公司外。

F01 proposed/partial。T059明确AI仍会漏，摘要与通知不能保证不遗漏，重要性没有阈值。考虑G06/G12：现有外部AI与希望内置是部署方式差异，不当两个完整OR；G04/G05属于管理策略，未证明收件箱管理所有情境充分；G16转发与群发为快速联系手段，执行序列/渠道不证明信息被理解。

正常场景（分析假设）：招聘来信未误判，关键词突出限制，本人标记任务稍后处理；相关目标可满足，仍需人工判断。异常场景（分析假设）：摘要遗漏“不要第二次测评”，G13不满足且G14方案不能保证G01；保留原文回查问题。异常场景（分析假设）：过滤把关键邮件丢垃圾箱，按G08愿接受更多垃圾作为取舍，但不能推出禁用一切过滤。边界场景（分析假设）：收件人客户端不支持编辑历史，G09理想功能未知而非已实现。正常期限场景（分析假设）：转发或群发给全组，不需要每人逐个新建邮件。

本人没有发机密信息且未提出具体安全障碍，不凭采访者问题创造加密需求；崩溃少且满意不自动造零崩溃指标。反复查看的5/10/20次数含不清转写，不设系统频率。所有未决保持pending，独立审查/形式证明not_run；工程检查实际由冻结工具执行。
'''
save(DOC,g,f,q,r,[{'target_type':'group','target_id':'DOC020-F01','message':'识别和摘要的遗漏风险未消除，整组只能作为部分贡献候选。'}])
