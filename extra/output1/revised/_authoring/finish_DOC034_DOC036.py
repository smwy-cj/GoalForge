# -*- coding: utf-8 -*-
from pathlib import Path

ROOT = Path('output1/revised/_authoring')
ns = {}
exec((ROOT / 'batch1_helpers.py').read_text(encoding='utf-8-sig'), ns)
ns['DOC'] = 'DOC034'
goal, group, question, save = (ns[x] for x in ('goal', 'group', 'question', 'save'))

g = [
    goal(1, 'direct', '与同事或过去的同学保持职业联系，了解彼此近况', 3,
         'networking just connecting with other colleagues, or maybe kind of past classmates see what they\'re up to.',
         '本人明确列为主要用途；非泛指必须向所有陌生人拓展网络。'),
    goal(2, 'direct', '向业内专业人士开展营销、提升知名度与曝光，并希望最终获得业务', 9,
         'posting, marketing information are posting like a marketing post just for awareness.',
         'T003营销对象及T009意识/曝光到希望业务的目的明确，业务结果保留hopefully的愿望强度。',
         ['曝光相对其他渠道更好为本人经验；不承诺发布必然成交。'],
         extra=[(9, 'hopefully, eventually win some business.'), (3, 'We work with a lot of other professionals.')]),
    goal(3, 'direct', '利用平台寻找和招募人才，同时考虑渠道成本及候选人与领域的匹配', 3,
         'We do a lot of recruiting as well through Linkedin. just good source a lot of people. And it\'s fairly low cost compared to some of the other competitors.',
         '招募意图、成本考虑明确；T015指出特定技术社区其他渠道可得更好候选人，保留情境性选择。',
         ['LinkedIn招聘相对成本较低是本人判断；Laravel领域他认为Lara jobs候选人可能更好，不把平台设为唯一渠道。'],
         extra=[(15, 'If you post something there, you actually get better candidates than you might get from yeah posting something on Linkedin.')]),
    goal(4, 'direct', '浏览个人工作机会和薪资范围，了解市场并保持动力', 3,
         'See what else is out there in the world, and just see what some of the salary ranges and things like that, you know, always keeps you motivated.',
         '本人明确浏览机会与薪资的用途；没有承诺正在主动换工作。'),
    goal(5, 'direct', '有时间和精力时查看社区会议等活动，以免仅靠大量邮件难以跟上信息', 3,
         'when I have the availability, and I think I, you know, can have the bandwidth. I can go on and check and see kind of what events are, you know, being put on the community.',
         '明确按自身可用时间检查活动，保留精力条件；不推出实时全覆盖通知需求。'),
    goal(6, 'direct', '让客户可通过身份、资历和照片核对自己，增强可信度', 5,
         'It\'s mostly to just signal to like my other to my clients, for example, that I I. You know I exist.',
         '本人把可信身份作为实际用途；不将他人查看资料等同身份认证已完成。',
         ['自述职业发展主要来自口碑及原有网络，平台在个人发展上作用有限。'],
         extra=[(5, 'If they get an email from me I am who I say I am, and the picture there matches the picture that they see on, you know, Zoom, or or you know, when I meet in person.')]),
    goal(7, 'direct', '保留易用的营销发布和定向推广方式，使内容触达合适的专业受众', 7,
         'tools that they have to like post you know, marketing things are are very, very easy and user friendly.',
         '本人正面评价易用性并说明定向营销用途，支持有目的的维持意图；并非因功能已存在自动立目标。',
         ['发帖时按个人或公司身份切换，图片、视频、背景与表情是本人描述的当前表达工具，不逐一升级成独立强制要求。'],
         extra=[(7, 'you can get, you know, pretty targeted.'), (19, 'so that your posts make in front of the right people.')]),
    goal(8, 'direct', '推广时清楚查看费用和预期提升，并跟踪曝光量等营销指标', 7,
         'They just tell you here\'s how much it\'s gonna cost. And you know, here\'s how much it\'s gonna get boosted.',
         '成本与boost可见、跟踪impressions的用途明确；不把平台预测当实现保证。',
         ['营销资源费用高是本人顾虑；招聘相对便宜是不同任务语境，不互相抵消。'],
         extra=[(7, 'So you can kind of keep track of all your impressions and all of your different marketing metrics.')]),
    goal(9, 'direct', '可把营销帖预约在自己预计受众上线的时间发布，以争取更多曝光', 9,
         'I can hit this post button, or I can schedule it for later.',
         '本人明确选择预约与原因；次晨9点是会议场景中的策略例子，不是统一发布时间。',
         ['认为早上比晚上有更多受众和曝光属于本人判断，未外部验证。'],
         extra=[(9, '9 Am. Tomorrow, when people 1st show up at the office, and I\'ll get a nice kind of boost in some of the impressions.')]),
    goal(10, 'direct', '需要时快速深入了解技术栈或营销做法，获取专业、完善的学习内容', 7,
         'If you want to do kind of a quick, deep dive into a certain. You know technology stack, or you want to kind of get a better understanding of like, how do I, you know, do something in marketing a little bit better.',
         '本人明确e-learning用途和正面质量评价；不与T005职业发展总体作用有限冲突。',
         ['相对YouTube质量更高是主观经验；产品收购名称与历史未核实。']),
    goal(11, 'direct', '需要了解潜在业务对象时查找其职业背景与共同点，可能再建立联系；通常主要添加认识的人', 11,
         'I want to get a little background on them, I\'ll you know, search them in the search function, pull up their profile, kind of take a quick look at their background to see if there\'s any kind of common threads,',
         '本人明确背景了解与可能加联系的策略；保留很少cold add的习惯，非禁止陌生联系。',
         extra=[(11, 'If it\'s somebody I know, I\'ll reach out and add them but I don\'t reach out too much as kind of cold call or cold.')]),
    goal(12, 'inferred', '减少广告、无关定向内容和拥挤界面对发帖等既定任务的干扰', 17,
         'all of this other stuff is kind of just added noise. And I yeah, don\'t necessarily care for it.',
         '明确抱怨干扰目的性发帖，支持希望减轻噪声的推断；未提出彻底移除所有广告或定向推荐。',
         origin='inferred', reason='由“有任务要发帖/转化曝光”与无关内容被称为噪声的对比，推断减轻干扰的结果意图。',
         assumptions=['对任务无帮助的界面噪声被视作应减轻的负担；未确定具体简化方案。']),
    goal(13, 'direct', '更多自动化支持营销内容制作，减少对庞大营销团队和耗时设计流程的依赖', 21,
         'support for content development, and then, you know, would be great to have more of that kind of automated. So we don\'t have to have as big of a marketing team,',
         '明确改进提议与目的，保留“更多自动化”而非全自动或取消所有人工审核。',
         ['设计资源紧张且耗时为本人报告；团队规模目标无具体数字。'],
         extra=[(23, 'Design is at a premium, and that just always takes a while.')]),
    goal(14, 'direct', '更省时地发布具有专业观感的内容，减少反复审核和冗长营销流程的负担', 23,
         'it\'d be great to be able to post, you know, professional looking stuff without having to be, you know, reviewed 6 times, and go through kind of the whole marketing funnel.',
         '本人明确希望的质量与流程改善，6次为反复审核示例，不要求一律零审核或设置精确次数阈值。')
]
f = [
    group(1, 14, [13], 23,
          'it\'d be great to be able to post, you know, professional looking stuff without having to be, you know, reviewed 6 times,',
          '自动化可能减少制作和审核负担，但不保证专业质量、合规审批或总体用时，单子目标不是充分实现父目标；仅候选部分贡献。',
          assumptions=['自动化产物在质量与审批上可用是未验证分析假设，不能据此宣称充分。']),
    group(2, 2, [7, 8, 9, 14], 9, 'hopefully, eventually win some business.',
          '易用定向发布、指标透明、预约与专业内容可能贡献曝光和业务；受众反应、转化和其他业务条件未知，整组不足以保证父目标。')
]
q = [
    question([3,8], '不同招聘与营销任务的可接受费用及渠道选择标准是什么？', '两种费用评价指向不同任务，没有预算或ROI阈值。'),
    question([13,14], '哪些内容制作步骤适合自动化，哪些质量与审核条件必须保留？', '本人希望减少多轮流程但未明确取消全部审核。'),
    question([12], '哪些无关内容或界面区域最妨碍任务，怎样判断干扰已减轻？', '改善结果为合理推断，具体方式与标准未明确。')
]
r = '''# DOC034 生成方语义自检

完整读取T000—T026共27轮，无问答遗漏；保留源文编码异常与“Linda”等名称的原貌，未核听、未外部验证LinkedIn历史、功能、价格或效果。续作生成助手完成本篇所有提取、判断、建模、自检；非独立语义审查。

逐目标14/14：G01联系同事旧同学而非无差别扩网；G02营销知名度/曝光与hopefully业务，未保证转化；G03招聘与成本、技术社区替代选项同保留；G04看机会薪资是市场了解和激励，不擅自确认为求职；G05有时间精力才查活动，不加实时推送；G06客户核对身份/资历/照片是可信目的，不是平台已验证真实；G07既有易用定向营销具明确继续用途，支持维持；G08费用与预期提升可见且跟踪指标，预测不是保证；G09预约并保留本人预计受众在线和9点例示，未固定时间；G10快速专业学习和T005总体职业发展有限相容；G11查销售对象背景、共同点及可能加联系，保留主要认识者的习惯；G12从噪声抱怨及任务目的推断减轻干扰，不推成零广告；G13自动化为明确选定方式及减少大团队依赖，不等同替代所有人；G14专业观感与减少反复流程两部分同有来源，6次不变阈值。13项explicit/direct分别核验；G12的origin与support分别根据意图推断和正面证据判定为inferred，不按字段自动映射。

全部2个组核验：F01（G14←G13）只有贡献，自动化可能仍产出欠佳内容或仍需审核，proposed/partial。F02（G02←G07/G08/G09/G14）涉及曝光与营销操作，但业务成功还依赖受众、产品和转化，proposed/partial。没有强造职业发展根目标；G01/G03/G04/G05/G06/G10/G11为不同用途，不当AND。未把LinkedIn和小众招聘平台画完整OR，因为候选人质量和招聘成功条件未明。

正常场景（分析假设）：会议上制作带图片的公司营销内容，查看推广价格，预约次晨发布并追踪曝光；符合G02/G07—09/G14，但仍只希望获业务。正常场景（分析假设）：客户查照片与资历建立初步信任，G06不等于认证。异常场景（分析假设）：定向、时机和专业观感均良好仍无业务线索，否定F02充分性。异常场景（分析假设）：自动化图文仍需多轮品牌或事实审核，F01不成立；不通过补造“免审批”假设修图。边界场景（分析假设）：Laravel招聘成本不高但专业候选人不合适，可用其他社区，G03不是排他平台约束。

稳定问题：REV34-01（G03/G08，未解决）预算与渠道收益标准未知；REV34-02（G13/G14/F01，未解决）自动化范围、专业质量和必须审核条件未知；REV34-03（G12，未解决）减轻干扰具体措施未明；REV34-04（F02，未解决）曝光到业务的缺失充分条件。对应关键问题进机器questions/issues，人审pending。

遗漏与边界：日常频率只是现状，不推为每天登录目标；提到新AI工具有趣不等于采纳明确生成方式，已有G13覆盖自动化建议；个人职业发展作用有限不得反向造“需要更多职业发展”目标；未把每个当前发帖按钮强制化。全部目标和组已自检，独立语义审查、形式证明not_run，精确模型/采样/预算unknown。工程检查以实际inspect输出为准。
'''
save('DOC034', g, f, q, r, [
    {'target_type':'group','target_id':'DOC034-F01','message':'自动化支持不充分保证专业质量及减少审核，保持部分候选。'},
    {'target_type':'group','target_id':'DOC034-F02','message':'发布和指标能力不保证曝光与业务转化，保持部分候选。'}])

ns['DOC'] = 'DOC036'
g = [
    goal(1, 'direct', '在情人节等特殊场合为亲近的人选购合适礼物，例如女友喜欢的蛋糕', 10,
         'I use Instagram mainly to shop on days like Valentine\'s Day, for example.',
         '本人明确购物目的及蛋糕选择动机；主要用途不等于只许买蛋糕。',
         ['当前下单流程是联系商家问价、确认付款号码和地址，支付后等派送/到达电话取货（T058）；此为报告的做法，不逐一新增强制产品能力。'],
         extra=[(10, 'because I know my girlfriend likes like eating cakes a lot.')]),
    goal(2, 'direct', '来到陌生地点或短暂停留时，快速找到当地商家的位置、联系方式及所售商品', 56,
         'would quickly, you know, help you to see where vendors are, cause their bios. You also have their location. which number to call which products they have.',
         '本人明确旅行中发现本地商家、获得信息的便利目的；不声称绝对偏好此平台。',
         ['使用源于方便，不是明确优于所有替代品；地点和商品信息真实与否未核验。']),
    goal(3, 'direct', '按想买的商品类别搜索商家，需要时补充地点词以找到相关本地店铺', 12,
         'if I don\'t see immediately what I\'m looking for, I\'ll just add maybe the name of the location.',
         '主动搜索类别及必要时地点的方式明确；保留对自动本地搜索是否内置的不确定。',
         ['本人不确定系统是否集成本地定位；结果主要是商家账号，而非像商品电商直接交易。'],
         extra=[(12, 'in my case, I would be like cakes.')]),
    goal(4, 'direct', '还没确定具体商品时，浏览商家的多种商品图像，从现有选择中灵活挑选', 22,
         'I don\'t have a particular product in mind. I I just go, and I would, you know, shuffle through like a bunch of images and a bunch of products they have.',
         '本人明确开放浏览、更多选择及喜欢该能力的用途，支持有目的维持。',
         extra=[(22, 'The fact that I can see like a bunch of products from one vendor with different varieties. It\'s it\'s a really good thing.')]),
    goal(5, 'direct', '可以先在线查看服装款式，再去实体市场寻找看中的设计', 10,
         'see the designs they have in store. and and I\'ll go to an actual market and ask for those. These designs I would have seen like online.',
         '本人明确第二种购买用途；T032衣着话题支持衣服语境，源文address等转写异常不擅自修正文。',
         ['线上浏览可启发线下购买，不强制通过平台完成支付。']),
    goal(6, 'direct', '联系商家时偏好使用其公开指定的号码，通过电话或WhatsApp更快沟通；应用内聊天也可选', 16,
         'I would always prefer to, you know, reach out to the number they\'ve specified, because that way the communication is quicker.',
         '本人明确偏好和理由且同段允许Instagram聊天，不把偏好升级为排他要求；速度为本人经验。',
         ['活跃账号有时回复很快；不预期商家一直在线。'],
         extra=[(16, 'You can. You can do a Instagram chat to that number, and then they will get back to you right,')]),
    goal(7, 'direct', '尽量避免向恶意商家付款后收不到商品，减少购物损失', 14,
         'when you send that money you will not get the product delivered to you right, and you\'ve lost the money,',
         '本人说明亲遇可疑账号并采取避免付款措施，后段明确帮助决定应买/不应买且省钱，意图明确；不声称其已实际被骗损失。',
         ['他说那次没有损失钱；商家确属恶意为受访者判断，未作外部核实。'],
         extra=[(62, 'It just helps me to know which accounts are probably good and which ones are not good I should buy from, and I should not buy from.')]),
    goal(8, 'direct', '查看商品评论、点赞及其随发布时间的分布，作为辨别可疑商家和辅助选购的线索', 62,
         'the products you uploaded 6 months ago would probably have more likes and more engagement than the 2 products you just uploaded today.',
         '本人纠正采访者的ranking解释，强调不同发布时间互动是否合理；当前目标只称线索，不等于高点赞安全认证。',
         ['互动相似或过少被本人视为可疑，是经验性判断；真实商家也可能少互动，恶意商家也可能伪造互动。'],
         extra=[(24, 'once I peruse, and I see the people who have spoken about it, and the comments can say, Oh, yeah, maybe this is what you know I might need')]),
    goal(9, 'direct', '无需登录也能浏览、搜索并查看商家资料，方便快速查找所需商品', 52,
         'even if it\'s to view the profile of the vendor. it\'s a bit disturbing. I would. I would have hoped that. You know I could do things without needing to log in',
         '本人反复明确免登录诉求，T053/054明确确认匿名浏览；不扩成匿名发布的确定要求。',
         ['当前会暂时留登录来完成节日前购物，是应对不便的策略而非偏好强制登录。']),
    goal(10, 'direct', '只想快速查购物信息时有时不让人知道自己在线；社交使用时希望在线状态仅亲近朋友可见', 24,
         'Sometimes I don\'t want someone to know online. I just want to go and search for what I\'m searching for.',
         '两个在线状态语境分别保留：有时不想被知在线、社交时只期望亲近朋友知道；不误作所有场景全员可见或永远隐身。',
         extra=[(26, 'if I\'m online, I would expect that just my very close friends would see I\'m online.')]),
    goal(11, 'direct', '分享私人生活内容时保留私密账号，使帖子仅亲近朋友可见、公众无法查看', 26,
         'if I am to do that, then I make sure I have a private account, because my account currently is private.',
         '已有私密状态同时有明确控制受众意图，属于维持目标；不因当前已实现而删除。',
         ['担忧公开生活内容可能日后伤害自己为本人风险信念，不当已证必然后果。'],
         extra=[(26, 'if I post something, if someone in the public will not have access to it, which is good,')]),
    goal(12, 'direct', '从保存的历史搜索中选回用过的商家，减少再次查找', 24,
         'which is also a good feature, because then I don\'t have to. Always, you know, search for vendors. I can just pick one I used in the past.',
         '赞赏搜索历史并说明重复访问用途，支持维持；一个月为例，不编造保留期限。'),
    goal(13, 'direct', '更换国家、号码或失去直接联系方式后，仍能通过平台与朋友重新联系', 30,
         'if we were friends and you\'re we are friends on Instagram, I can always, you know, reconnect with you by getting in touch with you, using using the application.',
         '本人明确旅行换号情境下的社交益处；不把购物焦点作为删去已确认社交目的的理由。'),
    goal(14, 'direct', '仅在有需要时使用平台，并通过用后退出、移除应用等方式控制耗时和无意识消费影响', 32,
         'I try to stay away from it when I\'m when I\'m not having any use for it, and only use it when I have, you know, a need for it.',
         '本人明确限制使用目的与T052选定自管策略；不推出必须删除无限滚动或完全停用。',
         ['有购物节需要时可提前几天开始浏览并暂留登录，用完再退出；卸载、网页清历史是当前策略而非平台强制流程。',
          '无限滚动与追赶他人动态被描述为耗时/成瘾因素；服装社交影响可能促进消费但本人对此有保留。'],
         extra=[(52, 'I just I just kinda lock out myself and then delete the application on my phone.')]),
    goal(15, 'direct', '希望商家商品页面直接显示价格，减少先联系询价的需要', 58,
         'that is also something I feel like they should put on the website on. I\'m sorry on the pages, the business.',
         '本人在说明问价后明确说应页面放价格，当前标题直接展示及减少询价由明确上下文支持；保留商家为何不列价只是猜测。',
         ['猜测商家希望收到询价反馈不是已验证商业动机。'],
         extra=[(58, 'They don\'t put the price of the products. They just show you what the products are.')]),
    goal(16, 'direct', '面对可疑商家时要求先交货再付款，避免那次可疑交易的预付损失', 14,
         'I didn\'t lose my money, because maybe I was very wise to understand that. You know you have to deliver before I pay you.',
         '本人明确该可疑交易采取的方式；T058普通订单先付再送并存，因此限定可疑情境，不升级为所有订单一律货到付款。'),
    goal(17, 'insufficient', '希望能够匿名发帖', 72, 'Yeah. Yes.',
         'T071把免登录浏览、匿名发帖及恶意账号混在同一归纳，T072简短肯定无法分辨是否独立采纳匿名发帖。明确反复表达的只是浏览匿名性；当前整句支持不足。',
         ['仅由采访者并列归纳与简短应答形成待确认候选；不当已确认需求，也不用作成立精化前提。'],
         origin='inferred', reason='综合归纳得到肯定可能包含发帖意图，但材料不能辨明，故保留候选而不判已支持。',
         assumptions=['若要成立，须确认肯定包含匿名发帖，而非只指浏览匿名性或恶意账号问题。'],
         extra=[(71, 'Being anonymous. So maybe a feature request that you would have is being able to do anonymous browsing or anonymous posting. as well as having some accounts that are malicious.')])
]
g[-1]['support']['supported_parts'] = ['重视浏览时的匿名性（已由G09/G10承接）']
g[-1]['support']['unsupported_parts'] = ['匿名发帖而非仅免登录浏览的独立意图']
f = [group(1, 7, [8,16], 62,
           'It just helps me to know which accounts are probably good and which ones are not good I should buy from, and I should not buy from.',
           '互动分布和可疑时先货后款可能减少损失，但互动可伪造、可疑判断会漏判，且普通订单仍会先付款；整组不充分保证免受恶意交易损失，仅部分候选。',
           assumptions=['评论/点赞可作为本人经验线索，不假定真实完整；商家是否同意先交货未知。'])]
q = [
    question([7,8,16], '遇到互动可伪造、商家不接受先货后款或先付款普通订单时，怎样进一步确认可信度？', '经验线索和单次交易措施无法覆盖全部欺诈风险。'),
    question([9,10,11,17], '需要的是免登录购物浏览、在线状态控制，还是也确实需要匿名发帖？', 'T071/072并列总结的确认范围不清，匿名发帖仍支持不足。'),
    question([14], '怎样在节前暂留登录与限制平时使用之间设定合适边界？', '本人有灵活策略但没有时长或频率指标。'),
    question([15], '价格应包含哪些费用，未知价格和线下议价应如何呈现？', '只明确希望展示商品价格，运费等未说明。')
]
r = '''# DOC036 生成方语义自检

实际范围：按T000—T039、T040—T076分段完整读取共77轮，包含全部购物/社交问答、T062对排名解释的纠正，以及末尾T071/072模糊确认。未核听录音；没有外部核实Instagram功能、地区习惯、商家或个人经历。当前续作助手作全部语义判断并自检，不构成独立评审。

逐目标17/17：G01特殊节日礼物，蛋糕是主用例而非唯一商品；G02旅行短停本地信息，未声称排他平台偏好；G03商品类别和必要时地点词搜索，保留定位是否内置未知；G04开放浏览多种商品为明确喜欢的灵活用途；G05线上款式到实体市场，服装语境结合T032保留但不篡改源文address；G06指定电话/WhatsApp偏好和应用聊天备选同时保留，快为主观经验；G07避免恶意付款未收货且那次并没损失，未声称真实被骗；G08互动量须结合新旧发布时间，按T062纠正不叫评分排名或安全保证；G09反复明确免登录浏览，暂留登录是回避摩擦；G10有时购物不被知在线与社交仅亲友可见分语境；G11私密账号的当前状态具明确维持意图；G12历史搜索的重复访问用途明确，不添加保留期；G13换号码/国家后的重联目的虽属社交仍保留；G14限制使用及退出/移除应用方式与节日前留登录例外同保留，无强制删除无限滚动方案；G15页面价格是明确希望，商家为了反馈而不放价格为猜测；G16先货后款限定那次可疑情境，避免与T058普通先付再送冲突；G17匿名发帖单列待确认候选，origin=inferred，support=insufficient，支持部分只到匿名浏览，当前匿名发帖未获独立明确支持。

origin与support分别评判：G01—G16均为明确目的、选定策略或带用途的维持意图，整句条件范围回读后direct；并非从explicit自动给标签。G17意图来源只能推测、当前整句不足，不能因有“Yeah. Yes.”的精确引文就标direct。该候选不进入任何精化前提。

全部组与其他关系：F01（G07←G08/G16）proposed/partial。评论点赞线索与可疑时先货后款并不保证识别所有恶意账号；先付款普通交易和伪造互动是反例。未把直接电话和应用聊天画完整OR，因为二者是沟通偏好/备选，联系成功及更快仍未知。G02发现本地店、G04选品、G06沟通、G15价格有助G01购物，但库存、实际交付与礼物适合性未覆盖，不画充分流程树；G03搜索方式不足保证G02信息真实和完整。G09免登录、G11私密内容、G14自管使用不能简单拼成隐私总目标AND，因为触发情境与上位范围不同。

正常场景（分析假设）：新到一地在节日前搜索蛋糕加地点词，看图和新旧评论，查商家电话问价，下单、提供地址并在到达电话后取货；目的相容，非平台已支持完整交易的证明。正常场景（分析假设）：不确定礼物时浏览多款，又选择服装设计线下找，同属可选场景，不强行要求网上支付。异常场景（分析假设）：新开真商家互动很少会被误疑，恶意账号可购入互动而显正常，F01不足，G08只为线索。异常场景（分析假设）：已判可疑但商家拒绝先货后款，本人可放弃，是否有其他验证策略pending。边界场景（分析假设）：普通可信订单先付款而可疑订单要求先交货，两者不同条件不矛盾。边界场景（分析假设）：节前暂留登录方便查商品又增加沉迷机会，G14保留个人取舍无统一时间限制。隐私场景（分析假设）：免登录浏览可满足购物匿名性，仍不能由此推出匿名发帖所需身份或滥用边界。

稳定问题及状态：REV36-01（G07/G08/G16/F01，未解决）互动并不证明商家真实、先货后款覆盖有限；REV36-02（G09/G10/G11/G17，未解决）匿名浏览/在线状态/私密发布/匿名发帖范围要分辨，G17支持不足；REV36-03（G14，未解决）便利与用时管理取舍指标未知；REV36-04（G15，未解决）价格是否含运费等未知。这些关键未决项已进questions/issues。G17不足只影响该候选及其潜在依赖，不能把全篇其余目标称不可信。

遗漏与反向检查：T044本人未用Instagram groups，且类比Facebook是猜测，不提炼群组新需求；T036关注名人/标签的能力介绍和觉得无关不等于必须屏蔽名人；T058派送电话是现有流程，无明确维护意图不单独升级为“系统必须通知”；T061采访者说高点赞必然安全被T062纠正；T071并列匿名发帖保留不足而非删去或当确认。现有契约没有完整独立障碍/偏好层，恶意账号、成瘾和隐私顾虑在条件、依据及问题中传递，未宣称无损关系建模。

精确模型、采样参数、预算unknown；执行者为当前续作生成助手。来源事实未外部核验，独立语义审查与形式证明not_run，人审pending。工程inspect仅以实际运行报告为准。
'''
save('DOC036', g, f, q, r, [
    {'target_type':'group','target_id':'DOC036-F01','message':'互动线索与可疑时先货后款不保证避免恶意交易损失，保持部分候选。'},
    {'target_type':'goal','target_id':'DOC036-G17','message':'匿名发帖仅见并列采访者归纳和简短肯定，独立意图未明确；支持不足，pending。'}])
