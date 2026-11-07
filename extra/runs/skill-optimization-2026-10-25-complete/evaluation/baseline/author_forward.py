"""Forward authoring record. Semantic entries below are authored from the eight complete interviews.
No reference targets, old outputs, external model API, or keyword extraction is used.
"""
from pathlib import Path
import json, hashlib, subprocess, sys, shutil, datetime

ROOT=Path(__file__).resolve().parents[4]
OUT=Path(__file__).resolve().parent
SK=ROOT/'runs/skill-optimization-2026-10-25-phase1/before/skills'
SRC=ROOT/'datasets/processed/goalforge-v1/source'
SPECS={}
def add(doc, turns, statement, reason, inferred=False, conditions=()):
    SPECS.setdefault(doc,[]).append(dict(turns=turns,statement=statement,reason=reason,inferred=inferred,conditions=list(conditions)))

# DOC003: cash-flight research, personal tradeoffs, exceptional login and transport connections.
add('DOC003',[7,9,115],'为自己及亲友研究并选择合适的飞行行程。','受访者明确以旅行计划和合适行程为使用目的；订票通常发生在合作方。')
add('DOC003',[9,25,107,115],'找到适合自己的低价航班与好交易。','反复说明价格是主要目的，并未承诺全市场绝对最低价。')
add('DOC003',[15,27],'条件允许时尽量提前约1至1.5个月或更早订票以获得好价格。','这是理想和努力方向；原文同时承认临时出行与近期较晚订票。',conditions=['临时旅行可能只能在一天内完成订票。'])
add('DOC003',[17],'在有剩余积分或礼券时帮助亲友订票并节省费用、用掉礼券。','目的和适用条件均由受访者陈述。',conditions=['大部分订票仍为自己；并非要求所有亲友订票都使用积分。'])
add('DOC003',[19,23],'在适合的旅行中尽量享受飞行时间、不同城市与机场休息室。','明确愿意选择较长航程以享受飞行，不应改成一律缩短飞行。',conditions=['个人航空爱好；尤其独自旅行时。'])
add('DOC003',[31,65,99,129],'研究不同城市或地区、机场、日期、舱位组合以找出适合的选择。','受访者主动变化搜索参数并希望考察大量组合。')
add('DOC003',[31,77,119,129],'所选行程的时间与个人计划、接续交通及要见面的人的时间相匹配。','匹配具体情境而非统一客观阈值；119列举而非穷尽条件。')
add('DOC003',[31,83],'在价格可承受时避免错过接续火车并长时间滞留等待。','以当年夜间抵达的具体风险为例，明确可因价差太高而让步。',conditions=['价差过大时可能接受错过火车的风险。'])
add('DOC003',[53,89,91,93],'现金航班研究中尽量匿名、不登录并避免额外分享个人数据。','个人隐私偏好明确；不把其跟踪涨价信念当作已验证事实。',conditions=['积分订票或确实被迫的特定情况可能需要登录。'])
add('DOC003',[55,57],'积分订票时登录持有积分的航空公司以查询并兑换有限的奖励座位。','明确选择的查询与兑换方式；此用途不使用Skyscanner。',conditions=['积分奖励订票，与现金订票研究分开。'])
add('DOC003',[69,73],'国际行程中在价格和飞行时长之间取得适合的平衡，避免过长航程。','虽爱飞行仍不愿40至60小时等极长组合；国内通常看最便宜选项。',conditions=['具体时间上限随情境变化；不编造统一阈值。'])
add('DOC003',[77,103,115,131],'比较不同订票提供方的价格、评分、折扣和最终费用，选择合适提供方。','比较是明确目的；优惠是否存在和选择哪家均随情况变化。')
add('DOC003',[81],'紧急且无更好选择时复查备选，必要时接受不够理想的航班。','紧急条件与妥协保留，不把理想行程变成不可让步约束。',conditions=['紧急订票且没有更好替代。'])
add('DOC003',[85,87],'在必须出行且票价过高等情境下获得路线降价提醒，以便及时订相对便宜的航班。','87明确实际提醒需求；85对通用理想提醒准确性持保留。',conditions=['按特定路线与出行需要；不要求系统准确预测所有动态计划。'])
add('DOC003',[95,99,137,149],'能够同时研究更多航班组合，用更少时间、更准确地找到合适选项。','并行搜索和减少研究时间直接陈述；搜索组合数是示例而非固定上限。')
add('DOC003',[137],'研究所需信息尽量集中，减少为确认行程而访问十几个网站。','分散信息被列为主要障碍，由此推断集中获取目标；不指定唯一实现。',True)
add('DOC003',[109,111],'不熟悉某市场时可在Skyscanner看到相对典型价格的比较信息。','受访者认可有帮助且nice to have，熟悉价格后可能不需要。',conditions=['不熟悉具体市场时的可选帮助。'])
add('DOC003',[119],'在可选择时优先获得夜间充分休息，而非红眼航班。','明确更愿意睡好，但并不排斥红眼航班。',conditions=['可接受红眼航班，不是禁止夜间出发。'])
add('DOC003',[123],'中转时通常预留至少约1.5倍至2倍机场最短衔接时间以应对延误。','个人常用安全余量；未声称形式化安全保证。',conditions=['中转可行性还取决于签证等情境；停站数通常不重要。'])
add('DOC003',[123,125,127],'了解自己持有卡或通行证在特定机场休息室的准入、开放时间和可用次数。','明确检查内容及个人使用目的；信息来源因卡和机场变化。')
add('DOC003',[125],'理想情况下有保持个人权益最新信息的网站，并与Skyscanner集成展示休息室准入。','直接提出理想方案，同时怀疑现有第三方更新质量。',conditions=['需可靠更新持有权益；目前偏向向发行方查实。'])
add('DOC003',[135],'从聚合器直接转到所选提供方已填好航班信息的行程页，以继续确认与付款。','135明确解释所需跳转结果，不是Skyscanner自身完成订票。',True)
add('DOC003',[143,147,149,151,155],'长期研究中减少重复搜索的操作负担与耗时，即使每次只省几分钟。','长期愿意切换节时；单次且不忙时学习成本可能不值得。',conditions=['收益与忙碌程度、使用期限和学习成本有关。'])

# DOC010: weather decisions and context-sensitive update cadence.
add('DOC010',[7,13,37],'根据天气决定当天穿什么、携带什么。','明确日常天气规划用途。')
add('DOC010',[7,17,19,21],'依据目的地天气规划旅行、户外活动及是否提前买活动票。','旅行时看全周预报，平时按天检查；雨冷时避免不值得的购票。')
add('DOC010',[13,15],'通过语音助手方便取得所需天气信息，不足时可在应用中取得详细信息。','这是现有使用策略和信息获取目的，推断便利获取目标而非要求永不打开应用。',True)
add('DOC010',[25,33],'外出前尤其在不熟悉的地方掌握当前天气情况。','出门即查看并说明在新地方熟悉天气的用途。')
add('DOC010',[35,39],'获得雷暴、洪水等极端天气的通知或警报，以便推迟活动、避免外出。','明确期望警报并说明行动目的。')
add('DOC010',[41,45,65],'普通天气通知可调整为每天早、中、晚约三次以配合作息。','个人已调整频率且肯定该方式；不推广成全部用户强制频率。')
add('DOC010',[41,49],'减少不必要的频繁天气弹窗，同时允许降雨时更频繁通知。','普通弹窗不需要；降雨例外不能丢失。')
add('DOC010',[49,51,63,69],'降雨或不利天气时及时、频繁获得变化和停止等实时更新。','明确实时更新最重要；未要求技术上不可保证的零误差。')
add('DOC010',[51],'依据可靠的短时天气信息决定步行还是乘公交，减少意外淋雨。','购物步行遭遇预报偏差提供正面目的依据，同时受访者不指责技术未达。',True)
add('DOC010',[57,71],'使用天气服务时不受广告干扰，理想体验没有广告。','71明确说no ads，并非只保留抱怨。')
add('DOC010',[57,59,61,71],'天气信息及时更新并在网站与应用等平台之间保持一致。','网站与应用不一致被具体描述，61及71确认一致性期望。')

# DOC013: distinction between stated requirements and observed generic service features.
add('DOC013',[6],'限制不适合某些观众的内容向这些观众展示。','以合规顾虑提出内容可见性限制，未指定法规或年龄阈值。')
add('DOC013',[6],'阻止创作者分享不应向任何人传播的内容。','与只限制部分观众的内容分开，禁止内容类型尚不明确。')
add('DOC013',[12],'观众能通过文字或适当筛选找到特定类型视频。','明确说essential并描述搜索方式。')
add('DOC013',[12],'观众能通过缩略图、描述及创作者等信息视觉浏览大量内容选项。','明确视觉浏览诉求，信息例子保留为可用内容而不强制每项。')
add('DOC013',[12],'创作者能够上传视频或开始直播以分享内容。','明确希望有上传和开播选项；为并列能力而非彼此精化。')
add('DOC013',[12],'创作者能为内容添加描述，并可添加转写或字幕。','描述与perhaps字幕保留可选语气。')
add('DOC013',[12],'提供视频编辑能力，如音效、修剪与裁切。','明确认为非常有用，属于建议而非已采纳承诺。')
add('DOC013',[14],'即使用模糊搜索条件也能得到有意义的结果。','明确结果要求，不编造搜索准确率。')
add('DOC013',[14],'观看时接收连续缓冲的数据流，避免频繁卡住。','直接表述seamless和不要持续冻结；未编造延迟阈值。')
add('DOC013',[16],'观众通过快速搜索视频获取娱乐、教育所需的信息。','明确用途和获取信息目的，不把书本排除推广成所有用户偏好。')
add('DOC013',[18],'使创作者较顺利地上传并发布已有视频，减少格式兼容和长度限制带来的障碍。','18是假设性上传困难，推断改善目的，具体格式和限制未确定。',True)
add('DOC013',[18],'使视频发布过程简单，减少等待完整上传后才能发布的不便。','原文作为疑问和潜在障碍提出，推断便利性而非要求未上传完成即可发布。',True)
add('DOC013',[40],'让不熟悉界面的观众更易理解并找到视频播放控制。','图标消失与陌生用户困惑为障碍，推断可发现性改进。',True)
add('DOC013',[40],'改善自动字幕对非英语母语观众的准确性。','受访者对准确性不确定，作为可探索改善方向，未声称已证实字幕错误率。',True,conditions=['字幕准确性问题仍需进一步核实。'])
add('DOC013',[40],'探索适合色盲观众的颜色调整能力。','could be grounds for some work为建议，不把未知现有能力写成确定缺失。',True,conditions=['当前颜色调整能力未知，属于建议方向。'])

# DOC020: mail intent, reliability exceptions, AI suggestions and selected existing affordances.
add('DOC020',[9,49],'及时获得招聘方消息，避免遗漏求职新信息。','明确每天多次检查目的，未强制5到20次的操作习惯。')
add('DOC020',[9],'接收并查看学校广播的新闻与通知。','明确第二个目的。')
add('DOC020',[11],'通过邮件安排牙医、诊所等预约。','明确个人用途。')
add('DOC020',[11],'获取商家的促销和折扣信息。','明确用途，不因其商业邮件而一律视为垃圾。')
add('DOC020',[11,99],'通过邮件联系朋友及工作中的专业人士。','朋友联系较少；未来主要职业联系，不限于同公司。')
add('DOC020',[15,17],'通过标记重要邮件、删除不重要或结束的邮件并区分用途账户，保持收件箱清晰可管理。','组织策略明确服务于manageability，不要求自动删除所有已读邮件。')
add('DOC020',[15],'标记暂不能处理的邮件任务，以便有空时回访并完成。','明确延后而不遗漏的意图。')
add('DOC020',[19,21,37],'使用内置AI根据简短要点写出组织良好的邮件，再由用户调整并发送。','37明确想要内置AI；19已有外部辅助习惯，不把无需复核当作需求。')
add('DOC020',[21],'写信时能调整字号并加粗重要句子。','用户主动使用格式强调重点，推断保留该表达能力。',True)
add('DOC020',[23],'需要分享多媒体时优先发送云端链接，以便对方在手机或电脑查看。','明确偏好云链接，不推导禁止附件。',conditions=['多媒体发送并不频繁。'])
add('DOC020',[25,27],'避免重要邮件被自动归为垃圾邮件，即使因此多收到一些垃圾邮件也可接受。','明确避免目标及错分取舍，不要求垃圾邮件零漏过。')
add('DOC020',[29],'发送后能编辑原邮件，收件人默认看新版并可按需查看编辑历史。','直接提出替代另发新邮件的具体方案。')
add('DOC020',[33,35],'可靠收到网站发送的邮件，避免注册邮件等应到信息无故缺失。','真实接收缺失障碍支持可靠到达目的；不采纳采访者网络丢包猜测。',True)
add('DOC020',[37],'发送前发现提到附件却没有附加时给予警告。','明确认为现有提醒很好，应保留维持目标。')
add('DOC020',[41,43,45,47,53],'AI帮助提取邮件主要内容并突出关键字或容易漏看的重要细节，减少阅读负担与遗漏。','用户肯定摘要并补充关键词及漏读案例；同时有节时目的。')
add('DOC020',[54,55],'可考虑定期汇总一批邮件，以减少逐封阅读。','接受采访者提案为一种可行方案，不转成已确定每日三封汇总。',conditions=['建议方案，周期与形式尚未确定。'])
add('DOC020',[59],'重要消息能触发通知，但只有识别足够可靠时才依赖自动重要性判断。','肯定通知价值并明确不愿在漏报时完全依赖AI。',conditions=['当前重要性识别可靠性不足；用户仍需复查。'])
add('DOC020',[71,73,75],'紧迫截止期限下保留转发与群发/BCC能力，快速联系团队成员。','特定情境下明确important；保持受访者说法及74确认的大范围群发含义。')
add('DOC020',[87],'保留日常搜索邮件的能力，并能通过搜索按标签查找。','直接说明每天使用且最重要，属于维持必要能力。')
add('DOC020',[86,87],'能够安排邮件在不同时间发送。','在功能优先级问题中肯定排程为第二重要，未增加自动排程规则。')
add('DOC020',[93],'可探索由通信双方使用同一自定义类别或协议标识来分类交流。','受访者认为可能不实用，例子是8000，未规定正式协议。',conditions=['探索性构想，可行性和确切含义待澄清。'])

# DOC023: connection count, referrals, and precise current-employee intersection.
add('DOC023',[3],'增加个人资料显示的连接人数，以向他人展示自己活跃使用LinkedIn。','连接数和展示活跃是明确手段与目的。')
add('DOC023',[3],'从目标公司的现任员工获得推荐，使招聘者更有可能看到简历。','直接描述求职目的，不保证最终获聘。')
add('DOC023',[7,9,11],'寻找同时是目标公司现任员工和本校学生或校友的潜在推荐联系人。','9明确排除前员工及不满足两条件的人；11校友更愿帮助属于个人信念。')
add('DOC023',[7],'查看潜在联系人的经历，以确认符合希望联系的背景。','明确查看经历的筛选目的。')
add('DOC023',[7,17],'在连接邀请附注中充分介绍自己并表达推荐请求。','真实附注意图；字符限制妨碍表达，不编造需要的字符数。')
add('DOC023',[7],'邀请被接受后能聊天交流推荐细节。','明确后续交流目的，保留接受前不能直接开展的条件。',conditions=['对方已接受连接邀请。'])
add('DOC023',[13,15],'搜索结果更准确地符合目标联系人条件，减少遍历无关人员。','大量无关结果构成障碍并主动调整词汇，支持准确与节时目的。',True)
add('DOC023',[13,15],'获得足够多的潜在联系人搜索结果，同时降低昂贵会员门槛的负担。','希望尽可能访问联系人并因价格考虑替代；不要求所有高级功能免费。',True)
add('DOC023',[17],'减少为适应非会员200字符附注限制而压缩措辞的时间与表达损失。','附注明确需要表达，压缩耗时为障碍，合理推断改善目标。',True)

# DOC031: positive preservation of communication and collaboration, plus concrete improvements.
add('DOC031',[1,5,7,25],'快速与校内同学、助教及教授沟通。','首要使用目的且明确最快通信的价值。')
add('DOC031',[7,29],'仅知道姓名或姓氏就能找到校内联系人，不必先保存电话或邮箱。','反复强调该现有能力的独特价值，保留维持目标。')
add('DOC031',[7],'能够在手机和电脑上方便联系校内人员。','明确喜欢跨设备获取能力，推断维持该便利性。',True)
add('DOC031',[9],'通过频道立即触达较广受众。','明确频道功能的目的。')
add('DOC031',[9],'加入频道后可查阅加入前的历史信息，并了解课程、项目和校园动态。','正面肯定历史信息与随时知晓动态的价值。')
add('DOC031',[11,13,29],'与团队协作时能即时分享文档。','被明确列为最常用和推荐功能，直接关联沟通目的。')
add('DOC031',[19],'更容易从大量历史对话和文件搜索结果中找到所需内容。','信息过量与无法准确定位是明确障碍；推断查找效率目标。',True)
add('DOC031',[21,27],'让语音和视频通话更容易访问，尤其在群组中。','21改善诉求与27明确要求相互支持。')
add('DOC031',[27],'提供快速跳转常用邮件应用向指定联系人发正式邮件的功能。','直接请求具体跳转方式，Outlook或Gmail为例而非唯一实现。',conditions=['需要与助教或教授等进行正式邮件沟通时。'])
add('DOC031',[31],'改善缩窄浏览器窗口时的布局与导航，便于并排使用多个窗口。','个人多窗口情境和可考虑改进的语气直接保留。')

# DOC028: contextual answers, leisure, privacy role, and genuine mobile/AI preferences.
add('DOC028',[3,5,9,15],'针对具体问题快速得到有情境、来自个人经验的答案或解决方案。','将Reddit与一般搜索区分，个人经验真实性是用户判断而非本次验证事实。')
add('DOC028',[3,9,25],'空闲时浏览感兴趣的社区，找到有趣内容并打发时间。','虽说没有特定结果，兴趣与休闲意图明确，不编造每次访问产出。')
add('DOC028',[3,21,23],'在相关社区发问，获得技术、求学或职业等问题的建议。','明确主动发问与寻求帮助的目的，不扩展为保证专家正确答复。')
add('DOC028',[11,55],'参与社区时保有匿名性，避免公开个人身份信息。','11将匿名视为USP，55认为处理得好；推断维持身份隐私而非证明不可追踪。',True,conditions=['帖子历史仍可能暴露身份；不承诺绝对匿名。'])
add('DOC028',[27,63],'改善Android等移动端的速度、直观性和整体使用体验。','63再次明确要求改善官方移动应用。')
add('DOC028',[27],'在移动端保留未完成帖子的草稿。','清楚以桌面可存草稿对比移动障碍，推断所需能力。',True)
add('DOC028',[27],'在移动端更清楚地追踪评论线程。','说明移动线程布局不如桌面清晰，推断可读性改善。',True)
add('DOC028',[29,57],'依靠有能力的社区审核减少低质量和不适合社区的帖子。','肯定审核作用并认为审核质量依社区与团队变化；推断维持目标。',True)
add('DOC028',[31],'在感兴趣的社区了解相关趋势和当前事件。','承认使用但新闻非主用途，保留有限范围。',conditions=['并非主要新闻来源，通常偏好把新闻留给其他应用。'])
add('DOC028',[33],'购置产品前获得不同使用背景的较平衡体验评价，以辅助购买选择。','明确笔电购买示例和不同用途评价价值，不把评价当已核实事实。')
add('DOC028',[35],'获取一般健康或自我改善信息，同时避免依赖Reddit解决具体健康问题。','明确一般用途与不信任具体健康建议的边界。')
add('DOC028',[43],'被动浏览时偏好卡片视图，主动搜索时偏好紧凑视图比较相关结果。','明确个人情境偏好而非全用户默认。')
add('DOC028',[45,47],'在可行时获得无广告体验，无法使用广告拦截时愿考虑付费会员。','明确更好体验和支付条件，未将有广告视为完全不可接受。')
add('DOC028',[51],'维持准确搜索以减少查找所需内容的时间。','明确搜索准确性帮助实现节时，不因现有能力而排除。')
add('DOC028',[51,59,61],'提供生成式AI工具，根据问题找到合适的具体社区，以获得更有价值的回答。','明确选择AI工具方案，准确社区不等于回答永远正确。',conditions=['仍可能有不佳回答，不能完全消除。'])

# DOC036: shopping, authenticity heuristics and private, restrained use.
add('DOC036',[10,56],'找到当地提供所需产品的商家，方便在新地方购买礼物等物品。','明确购物用途及经常迁居的背景。')
add('DOC036',[10,32],'通过商家展示或他人穿着了解设计和款式，辅助线下选购。','明确第二类购物用途；社交影响不升级为算法必须促购。')
add('DOC036',[12,56],'按产品名称和必要时的地点查找相关商家及位置、联系信息。','地点识别机制本人不确定；所需发现结果明确。')
add('DOC036',[16,58],'通过商家提供的电话或WhatsApp等较快渠道询价并联系下单。','偏好指定号码因为不期待商家始终在线；不强制一切交易必须站内。')
add('DOC036',[14,24,62],'购买前识别并避免恶意商家，减少付款后不发货的资金损失。','真实风险与防范行动支持避免目标；互动启发式不当作信誉证明。',True)
add('DOC036',[22,24],'能浏览同一商家多种商品图片，在没有预定商品时灵活挑选。','明确有时开放地看产品并肯定选择灵活性。')
add('DOC036',[24],'无需每次重新搜索即可找回以前搜索过的商家。','明确肯定保存搜索结果的目的，应保留维持便利目标。')
add('DOC036',[24,52,54],'不用登录也能浏览、搜索和查看商家资料，减少登录耗时与被察觉在线。','核心请求多次直接表述并确认匿名浏览；不扩展匿名发帖。')
add('DOC036',[24,62],'能查看商品的评论、点赞和随时间变化的互动，辅助判断商家可信性。','不称为正式排名系统；受访者62纠正了采访者误解。')
add('DOC036',[26],'保持私人账号，使个人帖子只对亲近朋友可见。','主动隐私策略与明确目的，非只陈述当前状态。')
add('DOC036',[26],'在线状态也只让亲近朋友看到。','明确expect而非证明当前系统已满足。')
add('DOC036',[30],'在换电话号码或失去直接联系方式后仍能通过Instagram与朋友重新联系。','明确跨国迁居中的联络维持价值。')
add('DOC036',[32,34,52,54],'按需要有限度地使用Instagram，避免无限滚动和社交追踪占用过多时间或无意识影响购买。','主动远离并确认限制使用目的；不把滚动功能误作为用户希望增强的目标。')
add('DOC036',[58],'商家页面直接显示商品价格，减少另行询价。','明确说should put价格；其猜测商家不标价原因不当作事实。')
add('DOC036',[58],'确认商品价格、付款与送货地址后收到购买的商品，并在送达前得到联系。','实际订购流程服务于收货目的，推断维持完整交付；支付通常使用外部方式。',True)

def sha(b): return hashlib.sha256(b).hexdigest()
def write(path,obj):
    with path.open('x',encoding='utf-8',newline='\n') as f: json.dump(obj,f,ensure_ascii=False,indent=2); f.write('\n')
commands=[]
def run(args, log):
    result=subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
    record={'command':[sys.executable,*map(str,args)],'exit_code':result.returncode,'stdout':result.stdout,'stderr':result.stderr}
    commands.append(record); write(log,record)
    if result.returncode: raise RuntimeError(f'{log}: {result.stderr}')

def main():
    sys.dont_write_bytecode=True
    for doc,specs in SPECS.items():
        d=OUT/doc; d.mkdir(parents=True,exist_ok=False)
        run([SK/'goal-extraction/scripts/prepare_source.py',SRC/(doc+'.json'),d,'--canonical-text',SRC/(doc+'.txt')],d/'01-prepare.log.json')
        shutil.copyfile(SRC/(doc+'.json'),d/'source-original.json')
        data=json.loads((d/'source-input.json').read_text('utf-8'))
        turns={int(s['original_locator']['turn']):s for s in data['segments']}
        data.update(schema_version='goalforge-extraction-3',status='completed',candidates=[],review_questions=[],limitations=[
          '仅以所提供访谈全文为范围；未接触录音，native_text不等于人工核验。',
          '提取、语义核验和模型复核均由当前生成方编制；独立语义审查、形式证明未运行，人工意见待审。',
          '当前契约无独立障碍、贡献及偏好关系层；必要背景通过条件、推断、引文和问题承接，不声称完整传递全部关联语义。'])
        for i,spec in enumerate(specs,1):
            evid=[]
            for t in spec['turns']:
                seg=turns[t]; loc=seg['original_locator']
                evid.append(dict(source_id=seg['source_id'],quote=seg['text'],role='basis',start_char=loc['start_char'],end_char=loc['end_char']))
            inf=dict(basis_candidate_ids=[],reason=spec['reason'],assumptions=['推断限于受访者描述的个人用途或改进诉求，不外推全体用户。']) if spec['inferred'] else None
            data['candidates'].append(dict(candidate_id=f'{doc}-G{i:03}',statement=spec['statement'],origin='inferred' if spec['inferred'] else 'explicit',actor='Stakeholder',context=spec['conditions'],evidence_candidates=evid,inference=inf,review_status='pending'))
        write(d/'extraction.json',data)
        run([SK/'goal-extraction/scripts/trace_candidates.py',d/'extraction.json','--judgment-template',d/'judgments-template.json'],d/'02-judgment-template.log.json')
        jud=json.loads((d/'judgments-template.json').read_text('utf-8'))
        for c,spec in zip(data['candidates'],specs):
            j=jud['judgments'][c['candidate_id']]
            j.update(label='inferred' if spec['inferred'] else 'direct',rationale=spec['reason'],supported_parts=[spec['statement']],unsupported_parts=[],assumptions=inf['assumptions'] if (inf:=c['inference']) else [],reasoning_steps=['已回查所列轮次的问题、回答、后续限制与全文；判断的是当前表述及其条件，不是仅根据引文命中。'])
        write(d/'judgments.json',jud)
        run([SK/'goal-extraction/scripts/trace_candidates.py',d/'extraction.json',d/'tracing','--source',d/'source.txt','--judgments',d/'judgments.json'],d/'03-tracing.log.json')
        run([SK/'goal-model-building/scripts/kaos_model.py','template',d/'extraction.json',d/'judgments.json',d/'decisions-template.json'],d/'04-decision-template.log.json')
        dec=json.loads((d/'decisions-template.json').read_text('utf-8'))
        # Concrete whole-group proposals. They remain partial because no interview establishes sufficiency.
        proposals={
          'DOC003':[(1,[2,7,12],115,'好价格、情境匹配行程和提供方比较有助于选择，但尚未覆盖所有个人约束。'),(7,[8,18,19],119,'交通、休息和中转余量是部分情境条件，受访者明确说仅为例子。')],
          'DOC010':[(2,[4,5,8],19,'当前天气、严重天气和实时变化有助于规划，但不足以共同保证旅行和购票决策。')],
          'DOC013':[(10,[3,4,8,9],16,'搜索、浏览和流畅观看有助于信息获取，内容是否符合教育或娱乐目的仍未知。')],
          'DOC020':[(1,[11,13,17],49,'过滤、到达可靠性和重要消息通知有助于不漏招聘信息，用户阅读和识别仍不可保证。')],
          'DOC023':[(2,[3,4,5,6],7,'筛选、查看、邀请和交流是推荐策略，不能保证对方愿意推荐。')],
          'DOC031':[(1,[2,3,4,6,8],7,'搜索、跨设备、频道、文件及通话提供通信方式，但不是全都共同满足即覆盖所有沟通需求的精化。')],
          'DOC028':[(1,[3,14,15],59,'发问、搜索和社区推荐是可用策略，不能保证真实答案或问题解决。')],
          'DOC036':[(1,[3,4,5,6,15],56,'发现、联系、鉴别、浏览和收货仅是购物策略，不能保证找到合适本地产品。')]}
        for n,(parent,children,t,reason) in enumerate(proposals.get(doc,[]),1):
            seg=turns[t];loc=seg['original_locator']
            dec['groups'].append(dict(group_id=f'{doc}-F{n:03}',parent_id=f'{doc}-G{parent:03}',child_ids=[f'{doc}-G{x:03}' for x in children],kind='and',status='proposed',completeness='partial',rationale=reason,assumptions=['上述内容仅为待核验组织方案；不把操作顺序、贡献或主题相关当作共同充分精化。'],evidence_ids=[],evidence_quotes=[dict(source_id=seg['source_id'],quote=seg['text'],role='basis',start_char=loc['start_char'],end_char=loc['end_char'])]))
        dec['questions']=[dict(target_type='model',target_id=doc+'-goal-model',message='当前精化候选均有共同充分性缺口，仅供审核；未确认方案不展示为成立层级。')] if dec['groups'] else []
        write(d/'decisions.json',dec)
        run([SK/'goal-model-building/scripts/kaos_model.py','assemble',d/'extraction.json',d/'judgments.json',d/'source.txt',d/'decisions.json',d/'assembled'],d/'05-assemble.log.json')
        run([SK/'goal-model-building/scripts/kaos_model.py','inspect',d/'assembled/model-input.json',d/'inspection.json'],d/'06-inspect.log.json')
        run([SK/'goal-model-building/scripts/kaos_model.py','finalize',d/'assembled/model-input.json',d/'inspection.json',d/'delivery'],d/'07-finalize.log.json')
        review=['# 生成方语义自检', '', '本次实际复核：全文、全部目标、全部候选精化组。与另一生成方上下文隔离；不宣称统计独立。没有真实人工反馈。', '', '## 全组场景检查', '']
        for group in dec['groups']:
            review += [f"- {group['group_id']}：{group['rationale']} 正常场景（分析假设）：这些子目标均可有助于父目标。反例（分析假设）：全部做到时，仍可能由于其他偏好、外部主体或内容质量而无法满足父目标。因此保留proposed/partial，不作为成立精化。"]
        review += ['', '## 边界与未决', '', '- 所有候选的主体保留为表达目的的受访者，不代表实现责任已分配。', '- 建议、个人偏好与情境例外保留在标题或条件中；当前没有外部人工采纳。', '- 现有功能只有具有使用目的或正面价值依据时才保留为目标；纯界面观察不自动造节点。', '- 对当前能力的猜测及隐私、审核、信誉信念不当作已验证技术事实。', '- 未定量的性能和准确性没有编造阈值。', '- 独立语义审查：not_run；形式证明：not_run；人工决定：pending。', '- 候选遗漏仍可能存在；本次全篇自检不是需求穷尽证明。']
        (d/'semantic-self-review.md').write_text('\n'.join(review)+'\n',encoding='utf-8')
        print(doc,len(specs),'completed',flush=True)
    paths=[SK/n/'SKILL.md' for n in ['goal-extraction','goal-model-building','model-review']]
    refs={'goal-extraction':['input-processing','goal-boundaries','output-contract','evidence-rules','semantic-judgments','tracing-contract'], 'goal-model-building':['modeling-rules','output-contract','tools'], 'model-review':['tools','output-contract','semantic-review']}
    paths += [SK/n/'references'/(ref+'.md') for n,values in refs.items() for ref in values]
    paths += [SK/n/'scripts'/name for n,name in [('goal-extraction','prepare_source.py'),('goal-extraction','trace_candidates.py'),('goal-extraction','simple_candidates.py'),('goal-extraction','render_review.py'),('goal-model-building','kaos_model.py')]]
    execution=dict(schema_version='goalforge-forward-execution-1',branch='baseline',generated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),scope=list(SPECS),source_scope='All turns of the eight provided canonical interviews, no reference labels.',author='current assistant model',model='unknown',temperature='unknown',tokens='unknown',cost='unknown',external_llm_calls=0,dependency_installations=0,skill_modifications=0,context_isolation='Separate subagent context from the other generation branch; statistical independence is not claimed.',independent_semantic_review='not_run',formal_proof='not_run',human_acceptance='pending',skill_files=[dict(path=str(p.relative_to(ROOT)).replace('\\','/'),sha256=sha(p.read_bytes())) for p in paths],source_files=[dict(path=str((SRC/(doc+ext)).relative_to(ROOT)).replace('\\','/'),sha256=sha((SRC/(doc+ext)).read_bytes())) for doc in SPECS for ext in ['.json','.txt']],counts={d:len(s) for d,s in SPECS.items()},commands=commands,failures=[c for c in commands if c['exit_code']],repairs=[],selection='One forward attempt; all failures and repairs retained. No best-of selection.',forbidden_materials_read=False)
    write(OUT/'execution.json',execution)

if __name__=='__main__': main()
