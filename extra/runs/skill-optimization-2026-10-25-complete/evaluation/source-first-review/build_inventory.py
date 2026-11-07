"""Write manually judged source-first inventories; no model outputs are read."""
import json, hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[4]
SOURCE = ROOT / 'datasets/processed/goalforge-v1/source'
OUT = Path(__file__).resolve().parent
DOCS = ['DOC003','DOC010','DOC013','DOC020','DOC023','DOC031','DOC028','DOC036']
data = {d: json.loads((SOURCE/f'{d}.json').read_text(encoding='utf-8-sig')) for d in DOCS}
inventories = {}
errors = []

def begin(doc, domain, scope, unresolved):
    inventories[doc] = dict(document_id=doc, artifact_type='isolated_model_reviewer_source_intent_inventory',
        human_gold=False, source_only=True, domain=domain, scope=scope,
        methodology='逐段完整阅读原文后人工式语义判断；条目由评审模型编写，程序仅校验引用和序列化，不以关键词抽取代替理解。未读取技能、论文目标、tests、生成结果或既有评估。条目不是最终目标模型，不规定唯一层次或粒度。',
        intents=[], background_candidates=[], unresolved=unresolved)

def evidence(doc, turn, quote):
    source_id=f'{doc}:T{turn:03d}'
    t=next(t for t in data[doc]['turns'] if t['source_id']==source_id)
    if quote not in t['text']:
        errors.append((source_id,quote))
        return dict(source_id=source_id,quote=quote,invalid=True)
    start=t['start_char']+t['text'].index(quote)
    return dict(source_id=source_id, quote=quote, speaker=t['speaker'],
        quote_start_char=start, quote_end_char=start+len(quote), offsets='canonical .txt character offsets; end exclusive')

def intent(doc, title, subject, conditions, modality, exceptions, certainty, refs, note=''):
    rows=inventories[doc]['intents']
    rows.append(dict(intent_id=f'{doc}:I{len(rows)+1:02d}', intent=title, subject=subject,
        conditions=conditions, modality=modality, exceptions=exceptions,
        epistemic_status=certainty, evidence=[evidence(doc,*r) for r in refs], interpretation_note=note))

def background(doc, title, why, refs, certainty='明确'):
    inventories[doc]['background_candidates'].append(dict(item=title, reason=why,
        epistemic_status=certainty, evidence=[evidence(doc,*r) for r in refs]))

begin('DOC003','航班行程研究与跨网站订票',
      '以受访者使用 Skyscanner 研究现金票为中心，同时保留跨聚合器、供应商、航司、积分票和贵宾室的必要边界。',
      ['行程好坏明确依情境，没有全局固定权重或价格阈值。', '“never log in”有被迫或特殊需求例外，不能写成绝对禁止登录。', '贵宾室整合是有条件愿望；受访者强调现有第三方更新不可靠。', '积分查询为并行旅程，受访者明确不在 Skyscanner 完成。', '价格跟踪与隐私判断是受访者信念，不能当成平台事实。'])
intent('DOC003','找到价格合适且满足行程安排的航班','受访旅客（主要本人，也替亲友）','计划旅行并研究现金票时','明确的主要目的','有时为体验航班接受更贵、更长路线','明确',[(25,'my primary focus is to like get a really good deal'),(107,'Best results for me is a combination of the logistics in terms of the itinerary that I want the price and the flexibility. All 3 aspects combined. mostly focusing on the 1st 2.')])
intent('DOC003','尽量提前订票以获得较好价格','旅客','理想订票时机','偏好而非硬约束','最近国内行程常仅提前一两周；紧急旅行可当天订','明确',[(15,'Mostly I try to aim for at least one to 1.5 months out, just to get like a better price at a better deal.'),(27,'there are rare occasions where I just have to book a flight.')])
intent('DOC003','在不同时间反复比价并探索多个网站的最佳优惠','旅客','有时间研究时','通常行为服务于省钱','可能跨几天或几周，没有固定频率；最后一分钟可很快完成','明确',[(25,'I check like dozens of different websites to just make sure I\'m having the best deal possible.'),(27,'It is very situationally dependent.')])
intent('DOC003','灵活组合区域、国家、邻近机场及日期，缩小到可行行程','旅客','研究起讫地点时','明确策略','不是始终限制本地机场或某个固定城市对','明确',[(31,'I generally do country to country pairs'),(65,'I would rather search with a series of different airports.')])
intent('DOC003','使航班时刻与后续交通、住宿、会面安排和休息相匹配','旅客','比较可行行程时','主要质量标准','可接受红眼，但更愿意睡好；价格太高可接受等车风险','明确',[(31,"I don't end up having to stay in a city"),(119,'Is it matching up with the schedules of the person who, if I\'m going to meet somebody, and that\'s it. Is it matching up with their schedules.'),(119,"I don't mind taking a red eye, but I would rather get my night's sleep.")])
intent('DOC003','比较供应商价格、评价、折扣、优惠券和升级，确定最终总价与订票渠道','旅客','已圈定理想航班后','明确主要目的及策略','可跨聚合器或直接向供应商、航司订票，渠道不固定','明确',[(77,'I look at the price. I take a look at the rating, and I often visit multiple providers from this page.'),(103,'whichever is giving me a better deal with any sort of coupons and discounts that I can apply to it.')])
intent('DOC003','确认每段航班、转机、当地日期时间、终站等物流细节适合自己','旅客','选择行程、跳转供应商前','明确检查目的','展示所有功能本身不等于使用所有过滤器','明确',[(77,'I make sure all the flight details like I said. All the connections and all the times are right for me, and they work for my schedule.'),(31,"I'll just make sure all the terminal, all the logistics. Information is correct.")])
intent('DOC003','按国际或国内场景平衡价格和总旅程时长','旅客','浏览排序结果时','情境偏好','国际主要看 best 避免廉价结果中四五六十小时行程；国内多数看 cheapest；不是一概选最快','明确',[(73,'when I\'m booking domestic, it\'s mostly going through the cheapest tab.'),(73,'the best is like a more medium section, like something that balances between price and the time taken.')])
intent('DOC003','必要时用出到达时窗及最长旅行时长过滤不合适航班','旅客','接续其他交通或有时长上限时','条件性策略','通常很少使用过滤器，不要求所有过滤器均为个人目标','明确',[(69,"The filters. I don't use it very often unless I'm connecting onto something."),(69,"If I also have a hard limit on the number of hours I want to spend in the sky.")])
intent('DOC003','行程不合适时重查替代路线，兼顾紧迫性和预算','旅客','所选航班细节不符合期望时','条件性处理','紧急且无好替代则仍订；学生预算可能优先于时间舒适度','明确',[(81,'I try to just rerun through all of my options. Make sure I\'m not missing something.'),(83,'If the price. Differential was way too high. Then I just couldn\'t afford to like, you know. Spend that much extra')])
intent('DOC003','在陌生市场判断当前价格是否合理','旅客','不熟悉地区票价时','有帮助、可有可无','熟悉后不再需要该功能；并未要求持续预测最低价','明确',[(109,'I can use Google flights for it because it tells me if the price is above, below, or lower than the Median.'),(111,"it would help out for the times when I'm not familiar with the specific market.")])
intent('DOC003','保留足够转机缓冲以应对延误与机场连接','旅客','有中转且无签证障碍时','个人安全偏好','不普遍限制中转次数；一般至少最短转机时间的1.5倍或2倍','明确',[(123,"Unless I have visa issues, I generally don't care very much about it"),(123,'I I generally tend to at least go for 1.5 x or 2 x of that for a stopover.')])
intent('DOC003','核查转机贵宾室是否开放以及自己能否使用','旅客','考虑停留机场、时刻和信用卡/通行证权益时','个人偏好','取决于卡、终站、访问政策、剩余额度及施工；不是保证任一机场可用','明确',[(123,'will the lounge at that airport be open at that point of time?'),(127,"What's their access policy? What's their timings? Is the renovation going on?")])
intent('DOC003','希望最新个人权益信息可与行程研究整合','旅客','有网站能可靠保存并更新卡片权益时','条件性愿望','现有服务更新不好，当前更信任发卡方/通行证官方来源','明确',[(125,'there would be a website that keeps everything updated about what I have and what that would grant me access to. and that would be integrated with skyscanner. That would be wonderful.'),(125,'I prefer going to the source of the truth for the lounge access')])
intent('DOC003','研究现金票时尽量匿名并减少数据分享','旅客','一般浏览 Skyscanner 或 Google Flights 时','强烈隐私偏好','积分票必须登录；极特殊被迫场景可能登录；单纯承诺不售数据不足以取得信任','明确',[(53,'I avoid logging in, and I try to keep myself as anonymized as possible.'),(93,'It would be a very specific scenario that I really need to do this.')])
intent('DOC003','需要积分票时登录持有积分的航空公司查询并兑换','旅客','决定用里程或积分而非现金时','条件性流程','明确不使用 Skyscanner 查询积分票；知道但不亲用第三方积分聚合器','明确',[(57,"if I have to make a points or an award booking, I'd log on to the airline that I have a loyalty account with where I have my points.")])
intent('DOC003','特殊刚需且价格骤升时接收多个路线的降价提醒','旅客','必须出行而现价过高时','过去一次的条件性目标','既有 Google 登录让设置更方便；不是要求新建 Skyscanner 提醒功能，该功能已被受访者确认存在','明确',[(87,'I needed a reminder on a few different routes, just to make sure that if any one of them goes down in price.'),(89,'It does have the same functionality.')])
intent('DOC003','更快、更准确、同时研究大量路线日期舱位组合','旅客','跨城市、日期、舱位及现金/积分方案搜索时','明确改进愿望','未给固定速度阈值或必须节省百分比；长期少量节时也有价值','明确',[(95,'You want to do hundreds of searches at the same time'),(149,'more accurately research for things while spending less time at it.'),(155,"even if it's saving me just a couple of minutes, because they add up.")])
intent('DOC003','在一处取得研究所需信息，减少多站切换','旅客','确定理想订票方案时','由障碍直接支持的改进意图','不能据此把所有外部业务都声明为 Skyscanner 现有职责','推断',[(137,"I don't get to have all of my information at one pace I end up having to visit at least 10 to 12 different sites")])
intent('DOC003','凭熟悉的稳定界面降低搜索操作负担','旅客','大量重复搜索时','明确选择平台的理由','别的平台多半只多花30秒到1分钟；达到更快研究可愿意投入学习','明确',[(143,"the website doesn't change very often the interface remains the same."),(147,'being familiar with the user interface and being able to quickly key in things and search for things just saves you time.')])
intent('DOC003','完成行程和渠道决策后提供旅客资料并付款取得机票','旅客/代订者','最终订票阶段','明确最终行为目的','Skyscanner 只链接供应商行程页，不自行订票；可能需要护照资料和声明','明确',[(131,'enter in all my details and pay for the booking through my card.'),(133,"It links you to the others who can do the bookings.")])
background('DOC003','航空爱好、最长航班和停留城市的故事','说明行程偏好，不能把示例 Singapore–Newark 或无限中转写为每次任务的固定目标。',[(19,'I try to maximize my time in the air.')])
background('DOC003','首页控件和完整过滤器列表','讲解界面能力，非受访者全部需求；其明确很少用过滤器。',[(67,'I also get the ability to filter by flight emissions'),(69,'I rarely make much differentiation over here in terms of the filters.')])
background('DOC003','随机选择的 Indigo 经 Istanbul、Bombay 行程','演示例子，无证据表明是拟订行程。',[(75,'I selected one of the flight paths randomly.')])
background('DOC003','其他聚合器矩阵数量与11,760组合示例','说明组合研究复杂性，不宜误作硬性系统容量或精确需求数量。',[(99,'11,760 different combinations of flights')])

begin('DOC010','天气信息与生活出行规划','受访者的天气应用日常/旅行决策、信息及时性和通知偏好。',
      ['通知每天三次是一般天气的个人设置，降雨时更频繁是明确例外。','语音助手具体失败原因未说明。','天气预测准确与应用同步延迟是两种不同问题。'])
intent('DOC010','依天气决定穿戴和随身物品','受访者','起床或出门前','明确主要目的','在熟悉长期居住地可能不查看','明确',[(7,'plan what I have to wear on a particular day'),(13,'I just plan what I wear or what I should carry on that day.')])
intent('DOC010','依天气安排户外活动和旅行','受访者与朋友','活动及购票之前','明确主要目的','日常多看每日；旅行可看整周','明确',[(7,'plan my outdoor activities. or just plan my trip'),(19,'if I have to plan a trip. I would check whether for entire week.')])
intent('DOC010','避免恶劣天气下不合适的户外活动和无效购票','受访者','如游乐园遇雨或过冷时','明确决策目的','Chicago 和 Six Flags 是实例，无地点限制','明确',[(21,"it's very annoying when it's rain or when it's very cold. So there's no point in buying tickets at that point.")])
intent('DOC010','先通过语音助手快速取得天气，不足时查应用','受访者','通常早上查询时','明确策略','应用足够时无需再查网站；网站是另一个信息渠道','明确',[(13,'I usually ask Siri or AI assistant for the weather information.'),(13,'So I have to open the app itself and look information there.')])
intent('DOC010','在每次外出及陌生地点及时确认天气变化','受访者','去吃饭、咖啡或其他外出前；身处新地点时','明确使用方式与目的','在 Pakistan 长期居住熟悉气候时此前不查；无统一全球固定频率','明确',[(25,'basically, whenever I go out of my apartment. I I do check it.'),(33,"whenever I'm like in the new place. I have to get familiar with the weather conditions there")])
intent('DOC010','获悉极端天气以推迟活动或避免外出','受访者','雷暴、洪水等条件出现时','明确高优先级目的','日常天气仍然重要，不是仅查极端天气','明确',[(35,'I just like postpone the entire event and don\'t. Don\'t go out at all.'),(37,'I use it daily. To decide what I wear, what I carry out.')])
intent('DOC010','极端天气时主动收到通知或预警','受访者','极端条件出现时','明确期待','邮件、短信、县政府和应用为其经历的渠道；未明确选定唯一通知渠道','明确',[(39,"for extreme conditions, I'm just expecting, you know, the weather app to give me notifications or alert")])
intent('DOC010','将一般天气通知调整到符合出门日程且不过度打扰','受访者','一般日常天气','明确个人偏好','每天早中晚三次；不是所有条件均三次','明确',[(41,'now I get it like 3 times per day'),(41,"that's likely to blend in into my routine, because that's when I go. Usually go out.")])
intent('DOC010','降雨期间更频繁取得开始、停止等实时更新','受访者','正在降雨或不利天气时','明确例外偏好','不应把一般天气也改为一直频繁通知','明确',[(49,"when it's about rain, I like have a like frequent notifications."),(63,'hourly, updates are important for extreme conditions when it\'s raining and not raining.')])
intent('DOC010','凭准确及时的天气选择步行或乘车，避免淋雨','受访者','短途出门时','明确实例目的和改进愿望','受访者承认预测技术有限，不是要求保证天气绝对正确','明确',[(51,'make this decision to whether walk to the grocery store or take a bus.'),(51,'real time updates are very important.')])
intent('DOC010','让应用及时刷新且与网站等平台信息一致','受访者','查看当前天气时','明确改进要求','应用显示雨而窗外、网站无雨是实例；区别于天气本身预测误差','明确',[(57,"the apps is they don't show you they don't get updates often."),(71,'should be consistent across all the platforms.')])
intent('DOC010','使用无广告天气体验','受访者','免费/未订阅应用展示随机广告时','明确理想体验','未表示愿意付费或必须提供某收费方案','明确',[(71,'no ads, real time updates and should be consistent across all the platforms.')])
background('DOC010','Pakistan、Chicago、上周买菜和五分钟步行','具体场景支撑熟悉度、活动规划和实时性的判断，非固定地点或时长要求。',[(31,'when I was like back in Pakistan I never checked the weather.'),(51,'the store was just like')])

begin('DOC013','视频观看、发现、上传与直播','受访者以泛化视频服务及现场界面示范讨论 viewer、creator 和平台经营者需求。',
      ['若干观点用 think/could/perhaps 表达，不应升级为确定合规法规。','现场描述的24小时等待是平台现象，不等同普适安全法律。','无障碍颜色可调性与字幕准确性明确未知。'])
intent('DOC013','控制不适合特定观众的内容可见性及禁止某些上传内容','平台经营者/内容发布者/观众','内容含不适宜或不允许传播的材料时','试探性约束建议','未指定年龄阈值、法律、地区或明确分类标准','明确',[(6,'there could be types of content that\'s not suitable for all viewers.'),(6,'some sorts of content that streamers should not be allowed to share with anybody')])
intent('DOC013','按文本、过滤条件找到特定视频或内容','观众','有明确观看目标时','明确必要能力','支持模糊条件仍应有意义结果','明确',[(12,'get a specific type of video or content by searching via text, or perhaps by filters of some sort.'),(14,'search, using vague criteria, but that should still get me meaningful results.')])
intent('DOC013','通过缩略图及描述等信息浏览和选择视频','观众','视觉发现内容时','明确必要能力','题材、演员、创作者等是举例，不要求固定分类全集','明确',[(12,'see a large volume of different options and click through it'),(12,'a thumbnail, so to speak, with a description, perhaps, who made it')])
intent('DOC013','通过观看获取娱乐、教育或快速信息','观众/受访者','使用视频平台时','明确目的','不是强制替代所有书籍','明确',[(16,'for entertainment purposes and for education purposes.'),(16,'I want to have a quick search. Give me some information')])
intent('DOC013','获得连续流畅且合理传输的视频播放','观众','观看内容时','明确质量要求','没有指定带宽、启动时间或缓冲数值','明确',[(14,"I don't want it to freeze constantly. I want a seamless stream of buffered data.")])
intent('DOC013','上传既有视频或发起直播来分享内容','创作者/代上传者','发布内容时','明确功能目的','直播与上传是两条分支，不能视为同一文件发布动作','明确',[(12,'create to upload a video or start a stream.')])
intent('DOC013','为发布内容补充描述、转录、字幕等元数据','创作者','上传/制作内容时','希望能力，部分是 perhaps','语言、标题等亦在示范中出现；未要求所有字段均必填','明确',[(12,'put some sort of description in, add, perhaps a transcript captions of the like.'),(26,'I am asked to give a title'),(26,'languages and things of that nature.')])
intent('DOC013','编辑视频以添加音效、剪辑或裁切','创作者','视频制作/发布时','明确认为有用','未声称现有平台已全部支持','明确',[(12,'to edit those. So I can add sound effects. Trim crop.')])
intent('DOC013','减少格式、时长兼容与上传发布流程的技术障碍','创作者','上传已制作视频时','潜在障碍对应意图','是设问式顾虑，并未确证实际失败或要求没有任何长度限制','推断',[(18,'making sure their formats are compatible with the system, making sure there\'s no length requirements.'),(18,'Is that a simple process? Do they have to sit and wait for the whole video to be published or uploaded before publication.')])
intent('DOC013','在首次上传时建立频道并发布选择的文件','新创作者','现场演示第一次创建内容时','流程性能力','不是每次上传都要新建频道','明确',[(26,"since I've never done this before. It's prompting me for what my account might be."),(26,'So now I have a channel')])
intent('DOC013','满足直播账户启用的等待限制后开播','直播创作者/平台','现场示范首次启用直播时','被描述的现有约束','24小时从 streaming account 设置起算；无证据为法律要求或每次直播都等待','明确',[(28,'after a streaming account is set up.')])
intent('DOC013','通过观看清单和订阅管理想看的内容并追踪创作者更新','观众','组织后续观看时','明确/部分 perhaps','订阅列表展示最新内容；不等同用户上传管理','明确',[(30,'add things to their watch list. or they can perhaps follow or subscribe'),(30,'list out the latest content from said creators, who they are subscribed to.')])
intent('DOC013','以付费方案获得无广告、不间断观看','愿意订阅的观众','选择 premium 时','描述的平台可选能力','个人月/年、最多5人家庭、学生试用是方案示例；受访者没有明确购买承诺','明确',[(32,'a premium tier which promises all content, no interruptions'),(32,'access without the aforementioned ads.')])
intent('DOC013','控制视频播放暂停、音量、静音、字幕与全屏','观众','观看视频时','现场描述可达操作目的','不把按钮图标、位置或切换动画独立当高层目标','明确',[(38,'play button, which, when clicked, turns into a pause button'),(38,'control the volume manually'),(38,"I'm able to toggle and untoggle the full screen.")])
intent('DOC013','了解播放进度并继续观看下一视频','观众','播放中','现场描述能力','下一条在非播放清单场景由内部推荐决定；不是个人化算法新需求','明确',[(38,'current time. Slash total time length.'),(38,'give me the next video it suggests.')])
intent('DOC013','让不熟悉界面的用户发现并理解播放器控制','新观众','控件自动隐藏尤其全屏时','潜在可用性改进','熟悉者自身没有同样困难；未指定工具提示或新按钮方案','推断',[(40,'if someone unfamiliar were to arrive and see these 10 icons, they might not be so well known.'),(40,'They actually disappear when the video is playing.')])
intent('DOC013','改善字幕准确性及考虑色觉障碍等可访问性','非英语母语/需要无障碍的观众','自动字幕、颜色显示等场景','不确定的改进线索','受访者不知道字幕准确率或颜色设置能力，不可断言不存在','不确定',[(40,"I'm not sure how accurate they always are"),(40,"I'm also not sure if things like colors can be tweaked for, say. colorblind viewers")])
background('DOC013','公司服务器和上传下载定义','说明平台管理控制权，不代表单独存储规模或基础设施目标。',[(10,'some large company that\'s going to host all of these videos on their servers.')])
background('DOC013','篮球搜索、广告、图标和屏幕几何位置','现场演示/观察；明确说不喜欢篮球，不能当兴趣画像或必须投放广告的目标。',[(24,"I don't like basketball"),(24,'every 10th or so is a sponsored ad.')])

begin('DOC020','邮件收发、组织与AI辅助','受访者以求职学生身份讨论 Gmail 使用及未来邮件客户端；保留可靠性和AI信任限制。',
      ['受访者说三秒撤回窗口是个人描述，非经验证产品事实。','“BBC”在追问中确认为多人批量发送，但不能额外推导隐私收件人策略。','共享类别/协议设想自称可能不实用，协议细节未定义。','定时摘要最初来自采访者，受访者只同意为一个可行方案。'])
intent('DOC020','不漏掉招聘邮件和学校通知','求职学生','日常检查邮件时','明确主要目的','学校与招聘邮件重要；非仅限这两类用途','明确',[(9,'to get the email from recruiters'),(9,"make sure that I I didn't lose any new information"),(9,'check about the news that broadcasted by school.')])
intent('DOC020','通过邮件预约个人服务、接收商家优惠及偶尔联络朋友','受访者','个人事务时','明确次要用途','朋友邮件较少；不是要求专门医疗预约系统','明确',[(11,'dentist or clinic or booking the appointment.'),(11,'get the information from merchandise, like, if they have sales or discounts'),(11,'rare. But I also use email to contact with my friends.')])
intent('DOC020','快速筛读未读邮件并标记重要内容','受访者','打开邮箱日常检查时','明确工作流','随后才细读重要邮件，非所有邮件直接自动处理','明确',[(15,"I look at those mails that I haven't read"),(15,'if that\'s something I think is important. I will 1st market.')])
intent('DOC020','删除垃圾、无关及已结束对话以保持收件箱清晰','受访者','日常整理时','明确策略','连重要但已经结束的会话也可能删除','明确',[(15,'if those are like trash or spam, I will just delete it.'),(17,'even for the the important males. But if the conversation has reached to the end. I also did it.')])
intent('DOC020','标记暂时不能处理的邮件任务，空闲后回来完成','受访者','需回复或操作而当前无暇时','明确条件性策略','不等同已提出自动截止提醒或任务调度要求','明确',[(15,"I would just like tag it and then leave it there. and when I'm available I will check in and finish the task.")])
intent('DOC020','使用不同邮箱区分重要通知与优惠信息','受访者','组织不同用途邮件时','明确现行策略','原文 separate emails 可能指邮箱账户；不应默认只是文件夹','明确',[(17,'I, I do this by have separate emails.'),(17,'I use it for recruiting.')])
intent('DOC020','由少量要点生成组织良好的邮件，再自行修改','受访者','撰写新邮件或回复时','明确需求，尤其希望内置AI','当前可用外部AI；用户保留修改，不是自动发送','明确',[(19,'I would 1st list my main point.'),(19,'I would adjust it a little bit'),(37,'the AI assistance that is in bills in the email.')])
intent('DOC020','调整字体大小并加粗重要句子','受访者','编辑邮件草稿时','明确现行操作目的','没有提出复杂版式或富媒体编辑器','明确',[(21,'adjust the font size'),(21,'mark the important sentence as bold')])
intent('DOC020','需要分享多媒体时通过云链接便于跨设备查看','受访者和收件人','偶尔发送图片、视频等媒体时','明确偏好','附件并不经常使用，不能据此取消普通附件能力','明确',[(23,'upload it to the cloud and then send the link'),(23,"easier for the client to view it in any platform, including like Mobile or laptop.")])
intent('DOC020','避免自动分类把重要邮件误投垃圾箱','受访者','收件自动分类时','强烈可靠性偏好','宁可收到部分垃圾邮件，也不希望遗漏重要信息','明确',[(25,'some important emails that will like end up in the spans folder.'),(27,'I would rather receive some spans instead of ignoring some important messages.')])
intent('DOC020','发送后可修订邮件，让收件人看到新版本并可查编辑历史','发件人及收件人','发现已发送内容需修改时','明确希望的功能','不是仅延长撤回窗口，也不是发送另一封补充邮件','明确',[(29,'editing the email instead of sending a new one.'),(29,'if they want, they could see the editing history.')])
intent('DOC020','可靠收到应到邮件，特别是网站注册验证邮件','受访者','外部网站声称发信却未到达时','明确障碍对应需求','未确证丢信发生在传输、发送方还是垃圾箱；不应编造根因','推断',[(33,"when you register some website and then send email to your inbox, and for some reason they're just not there.")])
intent('DOC020','在正文提到附件却未附文件时发送前警告','发件人','内容如提到附简历但实际没附件时','明确赞赏的既有功能','不是全自动从云盘附加简历','明确',[(37,"I didn't attach the resume. It will warn me before I send it. I think that is really good.")])
intent('DOC020','用AI提炼来信要点并突出容易漏看的关键词或限制','收件人','阅读邮件时','明确改进要求','不能仅概括掉小字关键限制；需帮助快速理解并避免遗漏','明确',[(41,'Get the main point of that email.'),(45,'highlights the keywords'),(47,"I won't miss missed out some keywords.")])
intent('DOC020','减少逐封阅读大量邮件的时间','受访者','频繁查信时','明确效率目的','定期汇总是采访者提案，受访者仅认为一个可能方案','明确',[(53,'I spend a lot of time just reading every email.'),(55,'that could be one solution.')])
intent('DOC020','重要邮件可即时提醒，但重要性判定必须值得信任','受访者','系统识别重要来信时','有条件偏好','不可靠时不愿完全依赖，包括AI；不支持只看AI筛选而忽略其余邮件','明确',[(59,'good to receive notification for some important messages.'),(59,"I would probably not want to rely on that. Unless it's really reliable.")])
intent('DOC020','期限紧迫时转发及群发给团队以快速协调','受访者/团队','紧截止情境','明确现有关键能力','BCC追问确认是批量触达；不推导群组权限或协同文档','明确',[(71,'forwarding the email. And BBC, like, sent to all the people in my group.'),(73,'very important when it comes to working on deadlines.')])
intent('DOC020','检索邮件并按标签过滤，亦可安排发送时间','受访者','寻找邮件或管理发送时机时','明确优先级判断','搜索最重要；过滤可用搜索完成，所以把调度列第二，不能强行给过滤独立第二名','明确',[(87,'the most important would definitely be searching.'),(87,'the second one will probably be scheduling.')])
intent('DOC020','探索收发双方共享的自定义类别或标识以便分类沟通','受访者及对应朋友/招聘方','未来设想双方使用相同类别编号时','试探性未来愿望','明确自称可能不实用；不应升级为已确定互操作标准','明确',[(91,"it's probably not that practical"),(93,'if my friend also set up this like 8,000 in his app, then we could communicate')])
intent('DOC020','未来维持工作中的专业联系和沟通','未来职场用户','从学生用途发展到工作时','明确未来用途','不限同公司人员','明确',[(95,'mostly at work.'),(99,'not necessarily people in my company, but just like, professionally')])
background('DOC020','安全隐私和崩溃问题并非本人当前主要障碍','本人不发送机密信息且很少遇崩溃；不能从采访者的问题添加强安全新需求或声称客户端不可靠。',[(33,"I don't send confidential messages through email."),(61,"Very, very few. I don't really remember a time.")])
background('DOC020','邮件检查频次和 TikTok 测评经历','频次说明防漏信动机；测评故事说明小字限制遗漏，非要求集成特定招聘测评服务。',[(49,'I used at least 5 times a day.'),(47,'I just missed that night')])

begin('DOC023','LinkedIn 联系人与内推','受访者的联系人数量增长和通过现任员工校友争取求职内推。',
      ['T003 的“3rd company”等转录不清，不据此指定第三家公司。','付费搜索容量和200字符是受访者描述，不是本评审验证的平台事实。','T007 初步结果含前员工，T009明确过滤只留现任员工；优先采用后续澄清。'])
intent('DOC023','增加个人主页的联系人数以显示自己活跃','求职受访者','经营 LinkedIn 个人资料时','明确首要目的之一','并非所有连接行为都只为内推','明确',[(3,'enlarge my the number of my connections on my profile.'),(3,"to show people that I'm active on Linkedin.")])
intent('DOC023','从目标公司现任员工取得内推，提高简历被招聘者看到的机会','求职受访者','申请实习或全职岗位时','明确另一主要目的','不保证内推带来录取或一定看到简历','明确',[(3,'get referrals from current employees'),(3,'a referral really helps to get my resume being seen by recruiters.')])
intent('DOC023','通过公司名与本人学校共同搜索潜在内推人','求职受访者','开始寻找内推连接时','明确搜索策略','后续仍需看个人履历核实，不是搜索命中即满足','明确',[(7,'search on in the search bar. This company name, and also the school name that I am currently attending')])
intent('DOC023','筛选同时满足现任目标公司员工及同校背景的人','求职受访者','检查搜索结果与个人经历时','明确筛选标准','排除前员工、只满足一项或都不满足者；这里只针对内推流程','明确',[(9,"I will only choose people who is currently a company employee and who was my university's student.")])
intent('DOC023','利用校友共同背景提高对方愿意帮助内推的可能性','求职受访者','选择连接和撰写邀请时','明确策略理由','是受访者的概率信念，不保证校友答应','明确',[(11,'Students who attend the same university tends to like want to help the alumni.')])
intent('DOC023','给潜在联系人发邀请并附简短自我介绍和可能的内推请求','求职受访者','确定合适个人后','明确现行操作','通常发 note；内推请求用 maybe，不能要求每次邀请都必须明说','明确',[(7,'hit the connect button'),(7,'add a message to introduce myself'),(7,'I maybe will also tell them')])
intent('DOC023','连接被接受后继续聊天处理内推细节','求职受访者与联系人','对方接受邀请时','明确条件性流程','不接受则待处理，无进一步内容；不是要求强行联系未接受者','明确',[(7,'if they do, I can then start to chat with them for the further details.'),(7,'a pending status for that specific connection.')])
intent('DOC023','减少无关搜索结果筛查并找到足够符合条件的人','求职受访者','免费搜索结果有限且相关性差时','从明确障碍推导的改进意图','不应删掉“公司+学校”的真正筛选条件来机械提升数量','推断',[(13,'go through like a lot of people in the search result'),(13,'one or 2, or even none of the people in the search result.')])
intent('DOC023','按成本和效果选择付费扩展结果或修改搜索词','求职受访者','搜索限制妨碍找到潜在联系人时','明确替代策略','premium 成本高；可删词或更具体地调整，非总是购买','明确',[(15,'purchase the linking premium'),(15,'this costs a lot.'),(15,'modify the keywords')])
intent('DOC023','在连接邀请字符限制内传达所需内容，减少压缩文字的时间','求职受访者','未连接的免费用户发送 note 时','明确障碍对应意图','原文200字符为受访者说法；未明确提出AI写作或取消所有长度限制方案','推断',[(17,'only a limited like number of words to really convey what I want to talk to them.'),(17,'it really takes some time for me to like, shrink them words in my message.')])
background('DOC023','竞争激烈的实习和全职市场','是内推动机背景，不是构建求职申请系统的独立要求。',[(3,"the application for the internships and full time jobs. It's pretty competitive.")])

begin('DOC031','Slack 校园即时沟通与协作','受访者使用 Slack 联系同学、助教、教授、共享文件和浏览校园频道，并提出可达性改进。',
      ['搜索结果过多是已述问题，没有明确指定新过滤器或AI方案。','直接电话是拥有对方号码时的替代，不能取代按姓名发现用户。','窗口变窄是桌面多窗口情境，不是手机布局有问题。'])
intent('DOC031','在校园内即时联系同学、助教和教授','受访学生','日常校园沟通时','明确主要目的','WhatsApp仍是整体最常用即时消息应用；Slack为校园最快方式','明确',[(5,'talk to my peers, my teaching, teaching assistants in various subjects, and also my professors.'),(7,"it's instant communication with anyone I wish to talk to within the university.")])
intent('DOC031','仅凭姓名或姓氏找到校园成员，无需先保存号码或邮箱','受访学生','需要联系成员时','明确偏好和优势','需知道名字或姓；不等于可联系世界上任何人','明确',[(7,"I don't need to like save anybody's information."),(7,'if I know their name, or sometimes even their last name, I can look them up')])
intent('DOC031','在手机或电脑上便捷沟通','受访学生','跨设备使用时','明确便利目的','大屏与手机总体好用，狭窄浏览器另有问题','明确',[(7,"I can do it over my phone. I can do it if my laptop's open")])
intent('DOC031','用频道立即触达广泛受众','受访学生','向群体传递信息时','明确目的','未具体指定公告权限、人数或邮件群发功能','明确',[(9,'the channel feature within slack, where I can reach a wide audience immediately.')])
intent('DOC031','查看入频道前的历史内容与当前校园、专业讨论','受访学生','加入频道或了解动态时','明确优势与信息目的','历史全面也导致搜索结果多，需要保留这种双面性','明确',[(9,'I have access to information that was there before I even joined the channel'),(9,"what's happening around within the department, within the program, what's happening around campus.")])
intent('DOC031','通过私信即时分享团队协作文件','学生与队友','项目协作时','明确高频功能及目的','现场浏览文件夹选文件是当前步骤，不是固定操作路径要求','明确',[(11,'my most used feature is sharing documents when collaborating with teammates.'),(13,'share a document instantly with a teammate.')])
intent('DOC031','按需格式化消息和附加不同类型文件','发送消息的学生','撰写私信/共享文档时','明确可用操作','粗斜体、emoji 为说明，不必独立高层目标化','明确',[(17,'I can format the text, whatever, any way I want.'),(17,'I can attach any type of file I want.')])
intent('DOC031','搜索历史讨论或资料并从大量命中中找到具体消息','受访学生','用关键词查找教授发言等内容时','明确检索目的，改进相关性为推断','未知确切内容时更难；未提出删除历史解决信息过载','明确',[(19,'enter keywords to look, to look for something specific.'),(19,"It's a little difficult to find. You know the message that I want to find?")])
intent('DOC031','更容易发起语音视频通话，尤其群组通话','受访学生/协作群体','需要音视频沟通时','明确改进愿望','已有通话能力，只是入口多窗口不便；不是新增一个完全缺失功能','明确',[(21,'it would be easier if it was just more access.'),(27,'the call feature more accessible as well'),(27,'especially in a group setting')])
intent('DOC031','已知电话号码时可用直接电话快速沟通','受访学生','熟悉对方且有电话号码时','明确替代策略','不会因此放弃 Slack','明确',[(23,'if I have their email with not their emails, or if their phone number with me, I would just call them.'),(25,'I would still use Slack')])
intent('DOC031','从 Slack 快速跳转标准邮件应用给对方发正式邮件','受访学生','向助教、教授等进行预期正式沟通时','明确新增愿望','要求导航到 Outlook/Gmail 等；不等同重做完整内置邮箱','明确',[(27,'a feature that would just immediately navigate to an Outlook or Gmail or any, any standard email app where I can email the person I want to')])
intent('DOC031','在桌面浏览器窗口缩窄并排工作时仍易于导航','受访学生','同时打开多个窗口并缩小 Slack 宽度时','明确改进线索','手机和14寸全屏总体正常；不要求固定三窗布局','明确',[(31,'shrink the size of slack browser window, I feel like it\'s a little hard to navigate through the application.')])
background('DOC031','Microsoft Teams、WhatsApp 与新用户建议','比较和使用背景；不意味着必须复制 Teams 所有功能。新手建议重述姓名查找与文件分享，不新增业务目标。',[(21,'I used to use Microsoft teams a lot in my workplace.'),(29,'definitely highlight the features or collaboration like document sharing')])

begin('DOC028','Reddit 问题求解、经验搜索与休闲浏览','区分有明确问题的主动使用与无特定结果的被动浏览；保留移动端体验和社区发现需求。',
      ['T021“never posted”随即自述曾发多个求助帖，应视为表述不整齐，不能断言从未发帖。','匿名性是受访者认知；其也说 Google 登录和历史可识别人，不能断言绝对匿名。','健康相关仅保留一般学习，受访者不建议依赖具体健康建议。','离线能力、bot事实核查、Google数据同步等是受访者说法，不作为验证事实。'])
intent('DOC028','用真实、情境化的个人经验快速解决具体问题','受访者','有特定疑问时','明确主要目的','个人经验被其认为大多可信，但承认任何网络信息非100%可靠','明确',[(5,'I get personal experiences over facts'),(5,'get more targeted results to the problem that I\'m facing.'),(15,'get to authentic answers much faster.')])
intent('DOC028','查城市活动、技术问题、职业升学等主题资料','受访者','需要某类具体信息或代码帮助时','明确多种用途','Halloween、LeetCode 等为实例，不限单一领域','明确',[(3,"I browse my city's subreddit with keyword. Halloween"),(3,"when I'm stuck on a problem or need like other inputs for a problem.")])
intent('DOC028','在空闲时浏览感兴趣的社区内容以消遣和发现有趣事物','受访者','没有预先定义问题且有闲暇时','明确休闲目的','明确常无特定成果，不应强加所有浏览必须解决问题','明确',[(9,'if I\'m just browsing Reddit, just to look through my interesting subreddits, then there is no particular outcome.'),(25,'I might just open reddit and scroll to see something interesting.')])
intent('DOC028','特定问题通过 Google 加 Reddit 定位帖子，再与帖子互动','受访者','定向问题搜索时','明确常用策略','普通浏览直接 reddit.com；不使用官方移动应用的偏好有体验原因','明确',[(7,'I Google, the question. And then I put Reddit after that.'),(7,'it gives me all the relevant posts.')])
intent('DOC028','根据个人兴趣跟随社区并获得贴合兴趣的帖子','受访者','浏览首页和订阅社区时','明确偏好/现状','大量主题多变；不应把大学或CS设为唯一兴趣','明确',[(19,'any post that comes on my feed is pretty tailored to my specifications.')])
intent('DOC028','在恰当社区发求助帖取得建议或解决方案','求助发帖者','自己需要建议时','明确目的','通常互动对象是帖子和社区，不是特定用户或管理员','明确',[(21,'most of the posts that I\'ve done are posts asking for advice.'),(11,'I usually interact with posts, I would say, and communities and post within communities.')])
intent('DOC028','发布含标题、正文与所需格式或媒体的帖子','发帖者','选好社区后','明确描述的能力','Markdown、图片、视频、链接、投票为可用表达方式，不全都必需','明确',[(21,'Then I can add a title to my post, I can add a body to my post.'),(21,'You can also add images. You can add video, you can add links. You can add polls.')])
intent('DOC028','按社区规则给帖子加标签以便合适的人筛选回答','发帖者/回答者','社区要求标签或主题分类有帮助时','明确条件性策略','只有部分社区强制标签；动物医生实例非全局固定类别','明确',[(21,'some subreddits make it mandatory to add tags.'),(21,"they'll filter out only the dog posts, and they'll only interact with those posts.")])
intent('DOC028','对帖子发表评论或回复特定讨论串','参与者','想与帖子互动时','明确能力','本人总体评论少；不能推为强社交交友目标','明确',[(21,'you can either create a new comment, or you can reply to a thread of comments')])
intent('DOC028','用可信社区的管理减少低质、误导内容','读者/社区管理者','评价信息可靠性时','明确价值判断；管理细节属受访者认知','可靠性取决于管理团队；不能完全排除坏回答','明确',[(29,'if a community has a strong, a strong set of moderators, then the posts themselves are reliable.'),(29,'anything you find on the Internet is not 100% reliable.')])
intent('DOC028','依据不同用途用户的产品评价作购买决策','受访消费者','研究产品或服务时','明确用途','重视比电商更均衡的体验和使用背景；不要求 Reddit 内交易','明确',[(33,'you can also find people from varied backgrounds talking about the product.'),(33,"I've made a lot of purchase decisions because of reviews I've seen on Reddit.")])
intent('DOC028','学习一般健康、运动等问题的经验','受访者','一般信息查询时','明确受限用途','明确不建议具体健康问题依赖 Reddit，也未要求诊疗系统','明确',[(35,"it's good for general health, related questions."),(35,"for specifics I've not used it, nor do I suggest anyone to use it.")])
intent('DOC028','移动端更快、更直观，并支持中途保留发帖草稿','移动用户','手机发帖或使用应用时','明确障碍和改进愿望','desktop 可保存草稿；Android是本人场景，不断言所有设备完全一致','明确',[(27,'The mobile platform is quite slow and clunky'),(27,"you can't save it as a draft which you can do on desktop.")])
intent('DOC028','在手机上清晰跟踪评论层次和讨论串','移动读者/参与者','查看评论时','明确体验改进线索','已有 threads；问题是呈现直观性而非无评论能力','明确',[(27,'you cannot keep track of comments intuitively on Mobile'),(27,'the desktop version is much more clearly put out.')])
intent('DOC028','按主动搜索或被动浏览选择合适内容密度','受访者','切换搜索/休闲模式时','明确视图偏好','被动用 card，主动搜索用 compact；不是统一最佳视图','明确',[(43,'I\'m just using it as a passive activity, I prefer, like card mode'),(43,'searching for something I prefer, like compact mode where I can see all relevant search results.')])
intent('DOC028','按新帖、热门、趋势等标准排序浏览帖子','使用者','希望调整 feed 时','描述的可用能力','没有说明本人始终选某一排序','明确',[(41,'you can sort posts by new by top by trending, rising.')])
intent('DOC028','广告尽量不打扰阅读，必要时用屏蔽或付费获得无广告体验','受访者','遇到广告时','明确偏好及条件性购买意向','当前广告较隐蔽且已有 adblock，暂不迫切付费；不可写成广告严重毁坏体验','明确',[(45,'it doesn\'t interfere with your post experience or your reading experience.'),(47,'in some scenario where ad block is not available, I would buy the premium tier.')])
intent('DOC028','按个人偏好选择外观模式和布局版本','使用者','定制视觉体验时','描述的可选能力','light/dark、legacy/current 只是选项；受访者认为 current UX更好，legacy更快','明确',[(49,'light mode, dark mode.'),(49,'There are customizations that are offered to tailor tailor. Your experience.')])
intent('DOC028','用自然语言/生成式AI找到适合自己具体问题的细分社区','求助者','不知道最合适 subreddit 时','明确首要新增愿望','不是要求用AI直接编造问题答案；更精准社区仍无法完全消除坏回答','明确',[(59,'a Gen. AI tool, to figure out what subreddit I should be accessing to ask my particular question'),(61,"the answers I'd get would be better")])
intent('DOC028','在有限离线缓存范围内继续阅读已载入的 feed','移动读者','失去网络连接时','描述可用能力，需求强度不确定','不能刷新、发布新帖或无限读取；受访者未明确请求扩展离线能力','不确定',[(39,'it will for sure save the existing posts.'),(39,"it won't allow you to make new posts, nor will it refresh the feed")])
background('DOC028','匿名性与隐私信任','是使用价值和自述信念，有信息可追溯的自我修正；未提出新的具体隐私机制。',[(11,'the USP. Of Reddit is anonymity'),(55,'Figure out who you are based on your post history.')])
background('DOC028','国际/印度新闻和广泛当前事件','有限使用且明确不是首要新闻来源，不能把实时全新闻覆盖列为主要需求。',[(31,'Reddit, is not my primary source of news.')])
background('DOC028','社区归属、通知、私信、奖杯和连续登录','受访者未亲身获得强归属，通知没有问题，私信/奖杯末尾自称附加功能。可保留为平台能力证据，不能当核心个人目标。',[(37,"I, personally, don't interact much via comments."),(53,"I don't think the notifications are too troublesome."),(67,'additional features')])

begin('DOC036','Instagram 本地购物、信任判断与有限社交','以本地商家发现、选购礼物、联系商家及控制自身社交应用使用为中心；社交作为相关的次要范围。',
      ['受访者推测搜索自动基于附近位置，后面有手工加地点词的明确策略，不应断言系统定位保证。','T014可疑商家时要求先交货付款，T058通常流程则先付钱后配送；需保留场景差异，不能统一成强制先货后款。','T062明确纠正采访者“排名系统”，其实际是人工看点赞评论与发帖时间是否合理。','T071采访者把匿名浏览扩成匿名发帖，仅获宽泛简短附和；匿名发帖支持较弱。','groups 由 Facebook 类比而来，本人未在 Instagram 使用，不应视为已确证功能。'])
intent('DOC036','在特殊场合寻找并购买合适礼物','受访购物者','如情人节给女友挑蛋糕、花等时','明确主要用途','也可无预定商品浏览；非仅限某节日、女友或蛋糕','明确',[(10,"I use Instagram mainly to shop on days like Valentine's Day"),(10,'get like really good cakes. And and I and I order from there.')])
intent('DOC036','从商品展示获得设计参考并在线下市场寻找类似商品','受访购物者','服饰等购买情境','明确第二购物用途','不是所有购物都在应用内下单或配送','明确',[(10,"I'll go to an actual market and ask for those. These designs I would have seen like online.")])
intent('DOC036','在新地点快速发现本地商家、货品、位置和联系方式','经常搬迁的受访者','不熟悉当地且停留可能短暂时','明确便利目的','出于便利而非明确排斥其他购物渠道','明确',[(56,"when you go to a new place. You don't really know, like the vendors there"),(56,'see where vendors are, cause their bios. You also have their location. which number to call which products they have.')])
intent('DOC036','按商品词搜索商家，必要时加地点使结果相关','购物者','寻找特定产品或供应商时','明确搜索策略','结果为商家账户；附近搜索是否自动定位本人表示不确定','明确',[(12,'if I don\'t see immediately what I\'m looking for, I\'ll just add maybe the name of the location.'),(14,'It. It shows me it would show me the accounts.')])
intent('DOC036','重用历史搜索快速回到以前访问过的商家','购物者','隔一段时间再次使用时','明确赞赏的便利','与不愿登录及清历史自控策略并存，不代表希望永远跨所有场景保留历史','明确',[(24,"I don't have to. Always, you know, search for vendors. I can just pick one I used in the past.")])
intent('DOC036','通过商家图库及商品多样性开放地发现适合的购买选择','购物者','尚无具体商品或比较选项时','明确喜欢的探索方式','不要求每次都先定好产品；具体布局只是当前描述','明确',[(22,"I don't have a particular product in mind."),(22,'see like a bunch of products from one vendor with different varieties.')])
intent('DOC036','查看评论、点赞及其与商品发布时间的合理关系以判断商家可信度','购物者','决定向哪个账户购买时','明确风险筛查策略','不是平台正式排名、认证或单纯点赞越多越好；人工经验也不保证识别所有诈骗','明确',[(24,'The good with the gallery is that when you go to the gallery you have people commenting, and you also have likes.'),(62,'The the products you uploaded 6 months ago would probably have more likes and more engagement than the 2 products you just uploaded today.')])
intent('DOC036','避免恶意商家收款不交货造成损失','购物者','面对可疑账户时','明确安全目的','受访者未实际损失钱；一次通过要求交货后付款避险，不可编造受害结果','明确',[(14,'when you send that money you will not get the product delivered to you'),(14,"I didn't lose my money"),(14,'you have to deliver before I pay you.')])
intent('DOC036','取得商家联系方式并通过适合渠道快速沟通','购物者和商家','选好商品并询问/订购时','明确流程偏好','可用 Instagram chat；通常偏好商家给出的电话/WhatsApp，因为不要求商家总在线','明确',[(16,'in the account, bio, that that is where I would see, like, maybe their phone number'),(16,'I would always prefer to, you know, reach out to the number they\'ve specified, because that way the communication is quicker.')])
intent('DOC036','直接在商家页面看到商品价格以减少联系询价','购物者','比较、考虑商品时','明确改进愿望','对商家不标价的原因只是受访者推测；非已存在标价能力','明确',[(58,'I feel like they should put on the website on. I\'m sorry on the pages'),(58,"They don't put the price of the products.")])
intent('DOC036','沟通价格、付款方式和送货地址并接收交付通知取得商品','购物者/商家','正常确认订单后','明确现行跨应用流程','正常叙述先付款后配送；商家电话告知将到或已到，不是应用内自动追踪保证','明确',[(58,'ask for the phone number I can use for the payment.'),(58,'confirm my address'),(58,"They'll give me a phone call.")])
intent('DOC036','不登录也能浏览、搜索及查看商家资料','购物者','想快速查看商品且不愿显示在线时','明确强烈改进愿望','匿名浏览有直接多处支持；匿名发帖仅采访者后期加入，不应等强度处理','明确',[(24,'I would have loved to use the application without signing in'),(52,'even if it\'s to view the profile of the vendor.'),(54,'Exactly. Yeah.')])
intent('DOC036','限制不必要使用、避免无限滚动等机制耗费时间与影响消费','受访者','无明确购物需要时','明确自我管理目的','有需要时仍用；退出登录、删应用/历史等为自控手段，不是要求平台自动删除所有数据','明确',[(32,'only use it when I have, you know, a need for it.'),(34,'very time consuming.'),(52,'I just I just kinda lock out myself and then delete the application on my phone.')])
intent('DOC036','购物期内暂时保持登录以减少反复登录成本','购物者','如节日前连续寻找礼物时','明确绕行策略','需求完成后再退出，与理想匿名浏览需求区分','明确',[(52,'leave myself to be, you know. locked in.'),(52,"once that period, you know, elapses. I can. And I've I've gotten what I want. I can log out from it.")])
intent('DOC036','把个人分享限定给亲近朋友以保护生活隐私','受访社交用户','偶尔发布生活内容及在线可见性时','明确个人隐私偏好','购物不是唯一讨论范围；本人私密账号，不表示要求商家账号全部私密','明确',[(26,'I make sure I have a private account'),(26,'only very close friends'),(26,'just my very close friends would see I\'m online.')])
intent('DOC036','通过关注关系在电话号码或邮箱变更后仍能重新联系朋友','经常跨国搬迁的社交用户','需要保持或恢复朋友联系时','明确次要社交价值','采访者为简洁主要聚焦购物；该意图仍由受访者明确说出','明确',[(30,'I can always, you know, reconnect with you by getting in touch with you, using using the application.')])
intent('DOC036','参考他人服饰等社交内容形成购买灵感','购物者','看到别人穿戴等内容时','明确影响机制，目标性弱于直接购物目的','本人也担心无意识影响并减少无目的使用；不能误写为希望增加诱导消费','推断',[(32,'it will kind of play a role in me, actually acquiring it'),(32,'I try to stay away from it a lot')])
background('DOC036','Facebook类比的groups、名人关注和hashtags讲解','关于其他功能的一般解释，群组本人未用且推断存在；不是本人的购物核心需求。',[(44,"groups on Instagram I haven't used"),(36,'you could also more or less follow like groups or hashtags.')])
background('DOC036','匿名发帖的后期采访者归纳','T071在已明确匿名浏览之外加了匿名发帖，T072简短同意不能等同详细独立陈述；作为弱候选保留，匹配时不强制认定遗漏。',[(71,'anonymous browsing or anonymous posting.'),(72,'Yeah. Yes.')],'不确定')
background('DOC036','商家业务账户发布产品、Amazon一键支付比较','说明服务边界，受访者为买方；不能由此添加其经营商店、平台托管付款或物流服务目标。',[(10,'have it as a business account on Instagram'),(14,'you need to still get in touch with the vendor')])

# Structural checks verify citations without replacing the preceding semantic judgments.
assert not errors, errors
for doc, inventory in inventories.items():
    inventory['source_document_hash_declared']=data[doc]['document_hash']
    inventory['read_range']={
        'first_source_id':data[doc]['turns'][0]['source_id'],
        'last_source_id':data[doc]['turns'][-1]['source_id'],
        'turn_count':len(data[doc]['turns']),
        'read_completely':True,
        'reading_note':'全文语义阅读；DOC003首次长输出中段被截断后，已单独补读T066–T096。DOC028、DOC036分别按turn分段读完。其他文档完整读取。'}
    dest=OUT/doc/'inventory.json'
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

manifest=dict(
    artifact_type='source_first_inventory_freeze_manifest',
    frozen_at_utc=datetime.now(timezone.utc).isoformat(),
    phase='frozen_before_any_anonymous_model_is_seen',
    reviewer_type='isolated_model_reviewer', human_gold=False,
    prohibition_acknowledgment={
        'skills_read':False,'generated_models_read':False,'paper_targets_read':False,
        'tests_read':False,'old_comparisons_read':False,'baseline_or_candidate_read':False,
        'external_llm_api_called':False,'dependencies_installed':False,'skills_modified':False,
        'subagents_spawned':False},
    source_files_read_or_loaded=[f'datasets/processed/goalforge-v1/source/{d}.{ext}' for d in DOCS for ext in ['txt','json']],
    source_read_note='每篇原文内容完整语义阅读。引用及字符位置从同一原始JSON精确校验；未读取生成目录。仅为核对指定文件做过source目录文件名/大小清单。',
    inventories=[], unresolved_policy='未决项保留于各篇 inventory.json；冻结前不查看模型，不为适配模型更改源文意图。后续只接受根节点明确给出的匿名模型路径。')
for doc in DOCS:
    ipath=OUT/doc/'inventory.json'
    manifest['inventories'].append(dict(document_id=doc,
        inventory_path=f'{doc}/inventory.json',inventory_sha256=sha(ipath),
        source_sha256={ext:sha(SOURCE/f'{doc}.{ext}') for ext in ['txt','json']},
        source_declared_hash=data[doc]['document_hash'],read_range=inventories[doc]['read_range'],
        intent_count=len(inventories[doc]['intents']),background_candidate_count=len(inventories[doc]['background_candidates']),
        unresolved=inventories[doc]['unresolved']))
manifest['builder_sha256']=sha(Path(__file__))
(OUT/'freeze-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':'ready','documents':len(inventories),'intents':sum(len(i['intents']) for i in inventories.values()),'out':str(OUT)},ensure_ascii=False))
