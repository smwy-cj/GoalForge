"""Manual anonymous repeat-round judgments; no cross-round label correspondence."""
import json,hashlib
from pathlib import Path
from datetime import datetime,timezone
OUT=Path(__file__).resolve().parent
PACK=OUT.parent/'anonymous'/'repeat'
DOCS=['DOC003','DOC010','DOC013','DOC020','DOC023','DOC031','DOC028','DOC036']
models={(d,s):json.loads((PACK/d/f'{s}.json').read_text(encoding='utf-8-sig')) for d in DOCS for s in ['A','B']}
inventories={d:json.loads((OUT/d/'inventory.json').read_text(encoding='utf-8')) for d in DOCS}
freeze=json.loads((OUT/'freeze-manifest.json').read_text(encoding='utf-8'))
for x in freeze['inventories']:
    assert hashlib.sha256((OUT/x['inventory_path']).read_bytes()).hexdigest()==x['inventory_sha256']

MAP={
('DOC003','A'):[[1],[1],[2],[],[],[],[3],[4],[4],[5],[6],[6],[6],[7],[21],[15],[15],[16],[16],[8],[9],[9],[8],[6],[10],[5,10],[17],[18],[18],[1],[11],[5],[5],[12],[13],[],[14],[14],[14],[13],[13],[13],[6],[19],[18],[18,20]],
('DOC003','B'):[[1],[1],[1],[3,6],[2],[],[],[4],[5],[15],[16],[4],[9],[9],[8],[7],[6],[17],[18],[4,18],[11],[5],[5],[12],[13],[14],[13],[21],[19],[18,20]],
('DOC010','A'):[[2],[1],[2],[2],[4],[4],[1],[2],[3],[5],[5],[6],[6],[7],[8],[9],[9,10],[10],[11],[12],[11],[6]],
('DOC010','B'):[[1,2],[1,4],[2,3],[2,8],[5,11],[5],[6],[7],[8],[9],[9,10,11],[12],[11]],
('DOC013','A'):[[1],[1],[2],[3],[6],[7],[8],[2],[5],[4],[9],[16],[17],[17]],
('DOC013','B'):[[1],[1],[2],[3],[6],[6,11],[7],[7],[8],[8],[8],[2],[5],[4],[4],[4],[9],[9],[9],[12],[12],[16],[17],[17]],
('DOC020','A'):[[1],[1],[2],[2],[2],[3,5],[4,6],[8],[9],[10],[11],[12],[7],[13],[14],[14],[15],[15],[16],[17],[18],[18],[19],[20]],
('DOC020','B'):[[1],[1],[2],[2],[2],[3],[3],[4],[3],[5],[5],[4],[6],[7],[7],[8],[8],[],[9],[9],[10],[11],[11],[11],[12],[7],[13],[14],[14],[15],[15],[16],[17],[17],[18],[18],[18],[19],[20]],
('DOC023','A'):[[1],[1],[2],[3,4,5],[6],[7],[8,9],[8,9],[9],[10]],
('DOC023','B'):[[1],[1],[2],[2],[3],[4],[6],[6],[6],[7],[4],[5],[8,9],[8,9],[10]],
('DOC031','A'):[[1],[2],[3],[4],[5],[5],[6],[8],[9],[11],[9],[12]],
('DOC031','B'):[[1],[2],[3],[4],[5],[5],[6],[8],[8],[9],[10],[11],[12]],
('DOC028','A'):[[2],[3,5],[2],[1],[4],[1],[1],[1],[6],[9],[8],[13],[14],[13],[],[11],[11],[12],[15],[15],[17],[17],[19],[6,19],[13]],
('DOC028','B'):[[2],[1],[1],[3,5],[1],[6],[13],[14],[13],[11],[12],[15],[17],[19],[6,19],[13]],
('DOC036','A'):[[1],[2],[3,4],[8],[9],[6],[12],[12],[5],[7],[15],[15],[16],[13],[13],[13],[3],[10],[11],[7]],
('DOC036','B'):[[1],[2],[3,4],[9],[8],[8],[6],[12],[12],[5],[7],[1,6],[15],[15],[16],[16],[13],[13],[14],[3],[10],[11],[11],[11],[11]],
}
NOTES={}
def note(d,s,g,text,judgment='supported',issues=()):NOTES[d,s,g]=(judgment,text,list(issues))
def issue(category,reason):return dict(category=category,reason=reason)
note('DOC003','A',4,'T017明确本人也给亲友订票；主体范围真实，不是推定自动代理权限。')
note('DOC003','A',5,'T017剩余积分/礼券省钱并用券为明确目的；冻结清单未单列此次级目的，不因此判无依据。')
note('DOC003','A',6,'T019航空爱好形成个人行程偏好；与T069过长行程上限有条件并存，不应一律改最短飞行。')
note('DOC003','A',9,'T031有时独立探索日期，有时探索地点；节点表示比较维度，未声称不同日期都要成行。与G008可按范围分开，非凭参数数目自动判过拆。')
note('DOC003','A',13,'T031明确检查upgrade options，有单独选择升舱的对象；与折扣检查可分，不保证一定升级。')
note('DOC003','A',15,'T031/T131旅客资料、护照/声明和卡付款是完成供应商订票的同一工作流；未机械拆每个字段，同时保留Skyscanner不订票边界，承接充分。')
note('DOC003','A',20,'T069/T073选用cheapest/best标签且区分国际国内，所选浏览方式及例外明确；G023进一步说明国际折衷，可视特化而非纯重复。')
note('DOC003','A',29,'T099明确组合研究还以积分机制重复；分开查询现金与积分合理，未让Skyscanner负责积分票。')
note('DOC003','A',36,'T123明确维持Priority Pass全球准入的个人偏好，冻结清单未另列；不指平台保证全球进场。')
note('DOC003','A',37,'T125希望记录实际持卡，G038推算准入权益、G039与搜索整合，是输入维护、权益输出与系统衔接不同能力，允许拆分。')
note('DOC003','A',42,'T127有限卡才检查余额，statement明确limited-use条件；不把本人无限卡写成需查月余额。')
note('DOC003','B',6,'T017明确有余券积分时帮亲友省钱；是所选办法且有条件，不是所有票都得积分。')
note('DOC003','B',7,'T019享受飞行和不同城市休息室真实；适合旅行的限定保留，不代表每次无上限加长。')
note('DOC003','B',11,'T055支持登录航司查看稀缺奖励座位；T057更明确本人直接用持有积分的航司渠道，statement未保留这一所选具体渠道，I16只能部分。')
note('DOC003','B',20,'G020用泛化多机场/日期/舱位而非固定US–India矩阵目标，T099特定数字仍只是解释，处理合适。')
note('DOC003','B',27,'T127当前本人无限次，只有次数有限的卡才需确认剩余额度。当前statement将剩余次数与所有查询无条件并列，所列condition只有来源不同，未保留关键例外。','needs_revision',[issue('condition_loss','应加“若使用次数有限的卡”，不要让所有持卡情境都要求余额。')])
note('DOC003','B',28,'T135预填行程跳到资料页有据，inferred保持用途；但最终用户填资料、声明与信用卡付款没有目标承接。')

note('DOC010','A',6,'T013助手不足时打开应用是条件性备用策略，与G005先问语音可分；不是每次必须双查。')
note('DOC010','A',13,'T035推迟活动与G022不出门是不同可满足结果，既保留极端条件，不视两个动词为过拆证据。')
note('DOC010','A',19,'T057应用状态迟迟不更新与跨平台一致是相关但不同质量：各平台同样过时仍一致。故G019新鲜性与G021一致性分开合理。')
note('DOC010','B',2,'T013先用助手、失效查应用的方式在support.rationale保留；目标statement较上位，结合解释可以承接而非声称只能语音。')
note('DOC010','B',4,'T019普通每日/出行整周是同一预报范围的分情况策略，合并不损失条件。')
note('DOC010','B',11,'T051短时及时信息服务步行/公交选择，质量目的和决策目的相连，非零误差保证；不强求必须拆两节点。')

note('DOC013','A',5,'T012上传或开播为不同发布途径，上位并列能力承接可以接受；但未保留T028账户建立24小时等候，另在I11记缺口。')
note('DOC013','A',11,'T018格式兼容、发布简单的潜在顾虑均有据且inferred合适；原文长度限制关注未在目标或解释正面保留。')
note('DOC013','B',6,'T028账户设置后24小时等待被放condition并明确为现状，不升级监管普遍法律；直播目标条件完整。')
note('DOC013','B',9,'T012编辑可以加音效，G010 trim时间/G011 crop画面各可独立编辑，作为可选能力分别保留有据；不能因三个例子一律判过拆，也不要求每次做三种。')
note('DOC013','B',18,'T018假设性长度顾虑保留inferred及未知实际限制，不主张无穷时长上传。')
note('DOC013','B',21,'T030订阅并从订阅区访问最新内容是手段及目的，合并保留了两者；与待看列表是不同组织方式。')

note('DOC020','A',6,'T015有空后完成任务的标签策略明确；本节点仅讲待办标记，不能替代日常快速扫未读/判断重要/细读。')
note('DOC020','A',9,'T023所选云链接办法在support.rationale正面保留，因此不因statement只写跨平台结果就判方式全丢失；不强制取消附件。')
note('DOC020','A',13,'T037内置AI为简要要点写成邮件有据；整个模型没有T019生成后本人调整的明确步骤/范围，I07只部分。')
note('DOC020','A',14,'T037喜爱已有附件提醒足以支持维持意图，标inferred略保守但不是错误来源或编造新功能。')
note('DOC020','A',20,'T071–T075紧迫情境下转发及群发都重要；上位协作能力保留所选方式，不声称必须一起做或共同充分。')
note('DOC020','B',11,'T015先tag记录和稍后回来完成是不同满足结果；拆开与顺序都可成立，未进一步把open/click机械拆。')
note('DOC020','B',18,'T021明确格式后send，作为最终发送结果有据，虽冻结未独立收录该操作。')
note('DOC020','B',24,'T029历史查看是可选收件端结果，与新版默认显示G023、发件编辑G022可分；无声称必须展示所有旧文。')
note('DOC020','B',31,'T054来自采访者，T055只同意one possible solution；Consider与condition保留此弱提案状态，不当已确定三封汇总。')
note('DOC020','B',38,'T091明确设想可能不实用，Explore和condition保留未确定协议，不按8000例值强造硬约束。')

note('DOC023','A',4,'T009双条件筛选正确；support.rationale保留校友帮助信念，但T007公司名+学校名具体输入搜索栏的初始方式未在本节点或其他目标保留。','needs_revision',[issue('selected_means_loss','G008虽保留后续改关键词，但不等于初始明确公司名+大学名搜索；应补这一已选方式。')])
note('DOC023','A',5,'T007通常介绍自己，only maybe问内推；statement和rationale把二者都当通常附注诉求，未保留请求可选。','needs_revision',[issue('strength','“介绍自己并询问”应加“可能/适当时询问”，原文maybe不可等同请求口气礼貌就已保留。')])
note('DOC023','A',7,'T015选择付费扩展联系人作为策略，但G007只写更多访问；support.rationale明确购买Premium且非必须，可以算该途径在record内保留。')
note('DOC023','B',9,'T007maybe内推明确保留为可能；与G008通常介绍可分别成立，拆分可保护语气差别。')
note('DOC023','B',15,'T017充分表达目的支持inferred；另有压缩措辞耗时，statement主要保留表达结果，未正面承接减少编辑时间。')

note('DOC031','A',7,'T011最常用是私信内共享文档；目标和解释只有即时共享，未保留私信作为所选渠道。','needs_revision',[issue('selected_means_loss','T011 direct messaging、T017个人页面附件的具体路线在模型目标中消失。')])
note('DOC031','A',8,'T019明确输入keywords，当前仅保留更易从匹配中找到内容，整个模型没有关键词检索方式条目。','needs_revision',[issue('selected_means_loss','结果级效率目的有据，但关键词方式缺失，不能只因引用T019当完整。')])
note('DOC031','B',7,'T011/T013最常用私信即时文档共享的结果和渠道都完整，未混同频道广播。')
note('DOC031','B',10,'T021一般访问改善和T027尤其群组被同一节点保留，条件/粒度合理，不强制另立群组节点。')

note('DOC028','A',7,'T009读到有趣东西产生问题再研究是明确条件性个人过程，虽冻结清单未独立分出新一轮好奇问题，不因此判幻造。')
note('DOC028','A',15,'T031有限了解社区时事/趋势真实，Occasionally且rationale保留非主新闻渠道，冻结背景候选不等于否定该用途。')
note('DOC028','A',17,'T033评测影响购买决定是评价输入G016后的决策目的，因果层次不同，允许拆分。')
note('DOC028','A',25,'T027慢和不直观是两个可分别改善的质量，G014明确速度另列，G025支持流畅；此拆分不同于重复“官方应用更好”。')
note('DOC028','B',16,'T063官方应用应更好重申了移动体验愿望；G009已含速度和直观性，G016没有新增清晰独立结果，作为竞争背景更合适。','needs_revision',[issue('over_split','同一移动改善意图被G009和G016重复目标化，未给新的功能或可独立满足的差异；可把first-party比较放G009理由。')])

note('DOC036','A',4,'T014险些遇到恶意商家但没失钱，inferred避免损失合适；support.rationale保留先送后付为该案例方式，未要求所有交易如此。')
note('DOC036','A',10,'T024点赞评论作为购买线索，G020额外保留T062按年龄分布判断，不建自动信誉排名。')
note('DOC036','A',16,'T052主动退出/删应用/清历史在support.rationale保留为替代自控策略，而非平台默认卸载，强度正确。')
note('DOC036','A',19,'T058价格、付款、地址和收货流程合并可接受，保留先付款普通情境；没有承接T058送达前/到时电话通知，I11部分。')
note('DOC036','B',6,'T014可疑卖家先交付后付款及T058普通先付款互为场景例外，condition明确保留，没有自相矛盾。')
note('DOC036','B',12,'T024评论不仅帮助识别可信度，最后还帮助判断送女友是否适合；独立礼物选择线索有据，冻结清单未单列此作用。')
note('DOC036','B',16,'T030希望进一步了解交流对象并关注是保留联系的选定办法，可与未来丢号再联系结果分开。')
note('DOC036','B',19,'T052只购物期暂留登录，是本人绕行；结束后退出与理想匿名浏览不矛盾。')
note('DOC036','B',25,'T058供应商电话通知已到/将到再收货都保留，非自动端到端物流保证。')

PART={
('DOC003','A'):{20:'G046保留节时和准确性，但T143稳定熟悉UI降低负担这一所选效率来源未明确建模。'},
('DOC003','B'):{3:'G004/G017跨网站/提供方比较有据，但没有T025/T027跨时段反复查询及急行例外的策略。',16:'G011登录航司奖励座位及兑换保留；T057本人直接用持有积分的航空公司这一具体选定渠道较隐。',20:'G030有更快准确与长期切换条件，但稳定熟悉UI的效率来源未保留。',21:'G028只到预填资料页，没有明确填写个人/护照/声明并用卡付款。'},
('DOC010','A'):{8:'G015保留普通每日三次与雨中例外，T041减少不必要频繁弹窗的负担目的没有正面保留。'},
('DOC010','B'):{8:'G009普通三次、G004日预报范围有据；减少普通频繁弹窗的目的隐含，未明确。'},
('DOC013','A'):{9:'G011保留格式和上传发布便利，但T018潜在长度限制顾虑未承接。'},
('DOC020','A'):{3:'G006有待处理邮件标记，快速扫未读及细读重要邮件的日常流程未覆盖。',7:'G013内置AI按要点写信成立，但T019受访者自己修改草稿没有承接。'},
('DOC023','A'):{3:'G004背景双条件正确，G008后续改词存在，仍没有初始公司名+大学名搜索策略。',5:'G004解释含同校可能更愿意帮助的信念，但未保留在消息中强调共同学校的策略。',6:'G005无条件并列介绍与请求，T007内推请求maybe被升格。'},
('DOC023','B'):{10:'G015表达充分有据，T017减少压缩措辞所耗时间的目标没有正面承接。'},
('DOC031','A'):{6:'G007共享文档及时，但私信选定渠道未保留。',8:'G008检索效率改善在，T019关键词方式缺失。'},
('DOC028','A'):{5:'G002关注的有趣社区存在，但T019量身贴合兴趣的feed能力仅隐含。'},
('DOC028','B'):{5:'G004个人兴趣阅读有据，但T019个性化feed未保留。'},
('DOC036','A'):{11:'G019保留价格/付款/地址及收货，T058商家将到/到达时电话通知未承接。'},
}

REL={
'DOC003':[
'T015提前订票用于争取好价，方式关系成立。','T025有时间反复跨站比较为省钱方法，非保证。','T077/T103比较提供方价格为获得该行程好价。','T031适用优惠降低费用，只能贡献。','T031交通住宿衔接帮助行程适合，其他条件仍需。','T083末班火车是地面交通衔接的具体情境。','T119探访对象时间是合适行程的一个维度。','T119睡眠是可让步的适合性贡献。','T123转机余量帮助可行，签证与延误不受其保证。','T087提醒用于必要出行及时找到相对便宜路线，尝试性方式合适。','T031自述先价格/城市再日期，作为本人顺序而非所有搜索普遍流程成立。','T031/T131比较定渠道后资料付款，顺序有据。','T125持卡记录支持权益查询，但需最新政策，贡献恰当。','T125/T127发卡/通行证官方来源是查政策和时刻的选定办法。','T095多组合并行可少手工重输，不保证性能。','T137一处资料有助减少站间切换负担。','T137全参数后便捷找选项是期望简化方式，未当实现保证。','T053/T089匿名少披露是个人隐私方式，不证明彻底匿名。'],
'DOC010':[
'T007穿衣是一般天气规划的具体用例。','T007户外活动是另一明确用例。','T007/T017旅行是天气规划的具体情境。','T019旅行前查整周是该规划所选信息范围。','T021买活动票前看适宜天气是户外计划办法。','T049降雨变化频繁通知是实时更新的具体情境。','T051及时更新帮助步行/公交决策，非保证天气。','T035先知严重天气再推迟活动，描述顺序成立。'],
'DOC013':[
'T014模糊条件搜索是T012特定检索能力的特殊范围。','T012/T016文字/筛选搜索为快速获取所需信息方式，有据。','T012视觉浏览可用于娱乐但未局限娱乐；proposed合理候选，不按已确立充分边处理。','T018格式兼容帮助上传，不能独立保证成功。','T018上传与发布顺序还以设问提出；proposed保留未知，不当已确立必须上传完才发布。','T014/T016流畅观看有助获得视频信息，内容仍可能不相关，贡献合理。'],
'DOC020':[
'T019/T021 AI草拟在最终发送前，顺序有据。','T019人工修改草稿后发送，顺序有据。','T023云链接是跨设备查看容易的所选方式。','T041/T053主旨摘要可减少阅读时间，不保证完整。','T045/T047突出关键限制帮助少漏重要信息，贡献成立。','T054/T055汇总只是tentative可选办法，operationalization不提高采纳强度。','T037内置AI是T019通用AI草拟的具体方案，特化可接受。','T009/T027不漏重要内容有助不漏招聘消息，因招聘是重要场景。','T029先编辑后显示新版，顺序在此方案成立。','T087标签搜索是检索的一种具体条件，特化合理。'],
'DOC023':[
'T003数量是展示活跃的本人所选方式，不保证他人评价。','T003内推有助被招聘看到，概率贡献有据。','T009选现任同校员工帮助争取内推，非充分。','T007先用公司学校检索后看经历，顺序成立。','T007看经历符合才邀请，顺序成立。','T007邀请被接受后聊天，condition保留。','T015删/细化词是该检索调整方式，不承诺一定更准。','该specialization被rejected，与T007检索动作和T009结果筛选并非同一行为的区别一致；不把已否定边当错误成立边。'],
'DOC031':[
'T007姓名检索是即时联络校内成员的所选方式。','T011/T013私信即时文档是即时校园通信的内容特例。','T009频道面对广受众是即时沟通的情境特化。','T009历史帮助了解讨论，不能保证当前信息全。','T027正式邮件可联系教授，但即时性依邮件，保留为贡献而非保证合理。','T017先去对象页面再附件发送有据，但G002“仅凭姓名查找”不在每次文件发送的前序中；支持普通导航的证据不能直接支持这个更具体的目标必然在先。'],
'DOC028':[
'T003编程解法是解决预定义问题的一个场景。','T007Google问题+Reddit为取所需信息的方法。','T005情境经验有助解决问题，不保证适用真实。','T051/T059找到专门社区服务较好答案但仍可能差，方式合理。','T033看不同用户经验有助购买决策，贡献非保证。','T047无法屏蔽时Premium为无广告办法。','T009新疑问可来自被动浏览，也可由Google找到帖子开始；当前proposed保留一条可能路径，缺直接同流证据，保持不确定。','T027手机草稿能减轻移动创作受阻，仅部分可用性。','T027线程更清楚帮助移动可用性，贡献有据。'],
'DOC036':[
'T012搜索供货商是T010礼物采购途径。','T022无预定商品的多样浏览是挑礼物途径。','T024评论可帮助礼物是否适合的判断，不保证合意。','T014可疑卖家先交付再付款是防该损失策略。','T024/T062互动线索可帮助防可疑账号，无安全保证。','T030关注连接是丢号码后仍可联络的所选手段。','T052退出增加访问阻力用于限制无目的使用。','T058先问价再取支付号码支付，顺序有据。','T058普通情境支付后确认地址，别混入可疑先货后款情境。','T058确认地址后等待电话和收货，顺序成立。','T056商家位置和货品信息是T012搜索后获得的价值；原文没有说明先得这些信息再贡献查找帐号，当前方向缺直接依据，宜由搜索贡献到本地商家了解。'],
}
REV={('DOC031','B',6),('DOC036','B',11)}
UNC={('DOC028','A',7)}
GROUP={
('DOC003','A'):['T119这些是主观举例，F001保留proposed/partial并承认签证预算，未强称全部约束充分。','T095/T137并行集中简化是节时方法，F002保留性能/资料未知，partial合适。'],
('DOC003','B'):['F001只有行程和价格，T107还有灵活性；模型自己标partial并说明遗漏，不应把它当错误宣称充分。','T119/T123行程匹配有多个情境例子，F002明确不穷尽；候选组织合理。'],
('DOC010','A'):['T007三种规划用途有据；F001说明携物交通还可缺且partial，未用正例代替充分性证明。'],
('DOC010','B'):['T007/T017/T035对应部分规划情境，F001仅proposed/partial，未过度推成全部规划的必要充分方案。'],
('DOC013','A'):['搜索浏览流畅播放对应T012/T014/T016，F001承认内容相关性未知，只候选部分支持，合理。'],
('DOC013','B'):['T018格式和长度是潜在上传障碍，F001保留partial及网络等未知；分析假设反例没有冒充源文事实。'],
('DOC020','A'):['T027/T033/T047/T059防错分/到达/细节/通知帮助防漏，但用户注意仍必要，partial合理。','T041/T054/T055单信摘要与可选汇总帮助减负，未确定汇总方案或绝对节时，partial合理。'],
('DOC020','B'):['T041/T045/T059辅助可能漏掉重要信息，F001承认AI风险并保持partial；不将所有AI动作执行视为充分。'],
('DOC023','A'):['T003连接数显示活跃为所选办法但非充分，F001只候选partial，强度合适。','T007/T009/T015接触筛选交流可提升内推机会，F002承认对方选择；G005maybe偏差单列，不因此把整个候选结构视为强充分。'],
('DOC023','B'):['T007/T009沟通链有据，F001承认接受和意愿未知，partial合理；正常反例均标分析假设。'],
('DOC031','A'):['T007/T013姓名/设备/文件对沟通有用，F001承认对方可达仍未知，partial合理。'],
('DOC031','B'):['T007/T009/T011只覆盖若干通信场景，F001明确不穷尽且partial；不当普遍AND计划。'],
('DOC028','A'):['T059/T061具体社区问问题可能提高答案质量，F001承认无人答/坏答，partial合适。'],
('DOC028','B'):['T009/T059/T061找到社区和答案可能助解题，但不保证正确或真的解决，F001保留partial。'],
('DOC036','A'):['T012/T016/T022/T058发现选购和收货是购物链，F001承认礼物适合和诚信仍未知，partial恰当。','T024/T062互动只是本人判断线索，F002保持partial，不造平台认证充分性。'],
('DOC036','B'):['T014/T024/T062互动和先交货付款只处理部分风险，F001承认可伪造及普通交易例外，候选partial合理。'],
}

def evidence_text(inv,nums):
    bits=[];seen=set()
    for n in nums:
        e=inv['intents'][n-1]['evidence'][0]
        if e['source_id'] not in seen:
            q=e['quote'];bits.append(e['source_id']+'「'+(q[:80]+'…' if len(q)>80 else q)+'」');seen.add(e['source_id'])
    return '；'.join(bits)

for d in DOCS:
    inv=inventories[d]
    result=dict(document_id=d,round='repeat',reviewer='独立上下文模型评审者',human_gold=False,
        blinding_limit='仅知第二轮A/B匿名代号；没有读取映射或生成分支，不推断跨轮代号对应。语言、粒度和模板特征可被猜测，属于有限盲法。',
        policy='使用同一冻结129条意图，不迎合结果改清单；允许多对多不同粒度。候选/否定关系按其当前状态评价，supported不代表需求已采纳。无标准P/R/F1。',samples=[])
    for s in ['A','B']:
        m=models[d,s];maps=MAP[d,s];assert len(maps)==len(m['goals']),(d,s,len(maps),len(m['goals']))
        im=[]
        for n,i in enumerate(inv['intents'],1):
            ids=[g['id'] for g,mp in zip(m['goals'],maps) if n in mp]
            if not ids:
                status='absent';why='没有目标承接冻结意图“'+i['intent']+'”；'+evidence_text(inv,[n])+'。缺覆盖不自动意味着既有目标错误或必须实现此能力。'
            elif n in PART.get((d,s),{}):status='partial';why=PART[d,s][n]+' 原文：'+evidence_text(inv,[n])
            else:status='complete';why='这些目标共同保留“'+i['intent']+'”的核心结果、条件和所选范围；'+evidence_text(inv,[n])+'。按多对多承接，不要求节点数与冻结清单一致。'
            if d=='DOC028' and n==20 and not ids:why+=' 原文只述有限离线缓存，未提出扩展请求，条目本身目标性不确定，缺失不能等权当主要遗漏。'
            im.append(dict(intent_id=i['intent_id'],goal_ids=ids,status=status,rationale=why))
        ga=[]
        for k,(g,nums) in enumerate(zip(m['goals'],maps),1):
            if (d,s,k) in NOTES:judgment,why,issues=NOTES[d,s,k]
            else:
                assert nums,(d,s,k)
                judgment='supported';issues=[]
                why='与原文“'+'；'.join(inv['intents'][n-1]['intent'] for n in nums)+'”一致；'+evidence_text(inv,nums)+'。依本人的具体场景/记录中保留的条件或推断强度可支持，未解释成普遍保证。'
            ga.append(dict(goal_id=g['id'],judgment=judgment,intent_ids=[f'{d}:I{n:02d}' for n in nums],rationale=why,issues=issues))
        ra=[]
        if m['relations']:
            assert len(REL[d])==len(m['relations']),(d,len(REL[d]),len(m['relations']))
            for k,(r,why) in enumerate(zip(m['relations'],REL[d]),1):
                j='needs_revision' if (d,s,k) in REV else 'uncertain' if (d,s,k) in UNC else 'consistent'
                ra.append(dict(relation_id=r['id'],judgment=j,rationale=why+' 当前按'+r['type']+'/'+r['status']+'状态评价，不等同充分精化。'))
        assert len(GROUP[d,s])==len(m['groups'])
        gr=[dict(group_id=g['id'],judgment='consistent',rationale=why) for g,why in zip(m['groups'],GROUP[d,s])]
        sample=dict(sample='repeat:'+s,intent_matches=im,goal_assessments=ga,relation_assessments=ra,group_assessments=gr)
        assert len(im)==len(inv['intents']) and len({x['intent_id'] for x in im})==len(im)
        for key,idkey,rows in [('goals','goal_id',ga),('relations','relation_id',ra),('groups','group_id',gr)]:assert [x[idkey] for x in rows]==[x['id'] for x in m[key]]
        valid={g['id'] for g in m['goals']};assert all(set(x['goal_ids'])<=valid for x in im)
        result['samples'].append(sample)
    (OUT/d/'review-repeat.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

errata=dict(artifact_type='source_inventory_repeat_errata',human_gold=False,frozen_inventory_modified=False,
    note='另记冻结清单未独立收录的原文意图，不回填129条也不据此重算任何样本指标；首轮errata仍有效。',entries=[
    dict(document_id='DOC023',source_id='DOC023:T007',quote='click into their profile and to see about their experience',note='阅读经历以判断是否适合是明确筛查动作。冻结I04只写双条件筛选，未独立承接此审查目的；首轮A G006/B G004、第二轮B G006保留，第二轮A缺少这一具体策略。'),
    dict(document_id='DOC028',source_id='DOC028:T009',quote='I have specific questions about it, and then I research it further on, Reddit.',note='被动浏览可产生新问题再进一步研究，冻结为一般问题/休闲两类，没有单列转入进一步研究的条件过程；repeat:A G007有明确支持。'),
    dict(document_id='DOC036',source_id='DOC036:T024',quote='this is what you know I might need for for my girlfriend',note='评论不仅作商家可信度线索，也帮助判断礼物适合。冻结未单列后一作用，repeat:B G012保留有据。'),
    ])
(OUT/'errata-repeat.json').write_text(json.dumps(errata,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
validation=dict(status='pass',round='repeat',reviewer='independent_context_model_reviewer',human_gold=False,
    frozen_manifest_sha256=hashlib.sha256((OUT/'freeze-manifest.json').read_bytes()).hexdigest(),frozen_inventory_hashes_unchanged=True,
    counts={d:{s:{'intents':len(inventories[d]['intents']),'goals':len(models[d,s]['goals']),'relations':len(models[d,s]['relations']),'groups':len(models[d,s]['groups'])} for s in ['A','B']} for d in DOCS},
    anonymous_package_sha256={f'{d}/{s}.json':hashlib.sha256((PACK/d/f'{s}.json').read_bytes()).hexdigest() for d in DOCS for s in ['A','B']},
    unique_exact_coverage=True,no_standard_prf=True,no_unblinding=True,no_cross_round_label_correspondence_assumed=True,completed_at_utc=datetime.now(timezone.utc).isoformat())
(OUT/'validation-repeat.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('ready repeat: 8 documents, 16 samples, frozen inventories unchanged; every item reviewed once')
