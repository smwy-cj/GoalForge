"""Serialize manually judged blinded first-round semantic reviews, not a scorer."""
import json, hashlib
from pathlib import Path
from datetime import datetime, timezone
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
PACK=OUT.parent/'anonymous'/'first'
DOCS=['DOC003','DOC010','DOC013','DOC020','DOC023','DOC031','DOC028','DOC036']
models={(d,s):json.loads((PACK/d/f'{s}.json').read_text(encoding='utf-8-sig')) for d in DOCS for s in ['A','B']}
inventories={d:json.loads((OUT/d/'inventory.json').read_text(encoding='utf-8')) for d in DOCS}
manifest=json.loads((OUT/'freeze-manifest.json').read_text(encoding='utf-8'))
for x in manifest['inventories']:
    assert hashlib.sha256((OUT/x['inventory_path']).read_bytes()).hexdigest()==x['inventory_sha256']

# Each row is one explicit manual goal-to-intent judgment, in the package's goal order.
# A list permits many-to-many acceptance rather than imposing inventory granularity.
MAP={
('DOC003','A'):[[1],[1],[2],[],[],[4,18],[5,7],[5,10],[15],[16],[8,9],[6],[10],[17],[18],[19],[11],[5],[12],[13],[14],[21],[20]],
('DOC003','B'):[[1],[1],[1],[2],[],[],[],[3],[],[4],[5],[6],[7],[21],[21],[15],[15],[16],[16],[4],[9],[9],[8],[8],[5,7],[6],[10],[5,10],[17],[15],[18],[4,18],[6],[1],[11],[5],[5],[12],[13],[],[14],[13],[13],[6],[18],[19],[20],[18],[20]],
('DOC010','A'):[[1],[2,3],[4],[5],[6,7],[8],[8,9],[9],[10],[12],[11]],
('DOC010','B'):[[2],[1],[2],[4],[1],[2],[2],[3],[5],[5],[6],[6],[7],[8],[9],[10],[9,10],[12],[11],[9],[8],[11],[6]],
('DOC013','A'):[[2,3],[6],[1],[1],[2],[3],[6],[6],[7],[7],[8],[2],[5],[4],[4],[4],[9],[9],[9],[12],[12],[12],[16],[17],[17]],
('DOC013','B'):[[1],[1],[2],[3],[6],[7],[8],[2],[5],[4],[9],[9],[16],[17],[17]],
('DOC020','A'):[[1],[1],[3],[3],[4],[3],[5],[4],[6],[7],[8],[8],[],[9],[10],[11],[11],[12],[7],[13],[14],[14],[1],[15],[15],[16],[17],[17],[18],[18],[18],[19],[20],[2],[2],[2],[7],[5]],
('DOC020','B'):[[1],[1],[2],[2],[2,20],[3,4,6],[5],[7],[8],[9],[10],[11],[12],[13],[14,15],[15],[16],[17],[18],[18],[19]],
('DOC023','A'):[[1],[1],[2],[2],[3,4],[4],[6],[6],[7],[4],[5],[8],[8,9],[9],[10]],
('DOC023','B'):[[1],[2],[3,4,5],[4],[6],[7],[8],[8,9],[10]],
('DOC031','A'):[[1],[1],[2],[3],[4],[5],[5],[6],[8],[8],[9],[10],[11],[9],[12]],
('DOC031','B'):[[1],[2],[3],[4],[5],[6],[8],[9],[11],[12]],
('DOC028','A'):[[2],[3],[2],[1],[1],[4],[1],[1],[6],[9],[13],[13],[14],[],[11],[12],[15],[15],[17],[17],[1],[19],[6,19],[19],[13]],
('DOC028','B'):[[1,2],[3],[2,6],[],[13],[13],[14],[10],[],[11],[12],[15],[17],[1],[19]],
('DOC036','A'):[[1,3],[2,17],[3,4],[9,11],[8],[1,6],[5],[12],[7],[15],[15],[16],[13],[10],[1,11]],
('DOC036','B'):[[1],[2],[3,4],[8],[8],[9],[6],[12],[12],[5],[7],[15],[15],[15],[16],[17],[13],[13],[14],[3],[10],[11],[11],[11],[11],[7]],
}

# Nuance, revisions, and items beyond the frozen inventory are adjudicated here.
NOTES={}
def note(d,s,g,text,judgment='supported',issues=()):
    NOTES[d,s,g]=(judgment,text,list(issues))
def issue(cat,reason):return dict(category=cat,reason=reason)

note('DOC003','A',4,'T017明确愿用剩余积分/礼券帮亲友省钱并用掉礼券；虽冻结清单未单列此用途，不因此判无依据。')
note('DOC003','A',5,'T019、T023确有享受飞行和机场的偏好；“适合的旅行”条件及后文不接受极长航程的限制被保留。目的、体验例子合并可接受，并非要求所有行程最大化时长。')
note('DOC003','A',6,'T031/T065支持组合搜索，T099支持舱位变化；同时研究更多组合是手段与范围，未因并列参数判混合目标。')
note('DOC003','A',13,'T081在不合适时通常重查，紧急无替代则接受。当前把“复查备选”也限定为紧急且无替代，缩窄了原文常规应对。','needs_revision',[issue('condition_loss','T081先说明不合适会做更多研究和rerun all options，只有接受不理想方案才受urgent/no alternative限制。')])
note('DOC003','A',22,'T135直接跳到已填好行程页确实有据，且明确交由供应商继续；但只说“继续确认与付款”尚不足承接T031/T131填写旅客、护照资料与卡付款的完整最终阶段。')
note('DOC003','B',5,'T017明确替亲友订票，冻结清单主体已保留该用途；这不是软件自动代订承诺。')
note('DOC003','B',6,'T017明确有剩余积分或礼券时帮别人省钱；是条件策略，不需把每位亲友均设为必须用积分。')
note('DOC003','B',7,'T019明确喜爱更长飞行；statement保留practical constraints，未把无限飞行当硬性约束。')
note('DOC003','B',9,'T029明确下一次冬假旅行意向，但不是聚合器持久功能要求。作为Stakeholder一次出行目标有源文支持，建议与稳定应用目标区分；不因冻结清单未收录即判错。')
note('DOC003','B',12,'T031确实检查coupon与upgrade；与G026最终提供方比较有细分对象，可保留为过程层目标。')
note('DOC003','B',18,'T055登录看有限奖励座位、T057到持有积分航司兑换是可分阶段；与G019并列不是把同一事实机械重复。')
note('DOC003','B',32,'T099的US–India矩阵为解释规模的例子；虽rationale说illustrative，仍立成独立G032并连specialization，容易将示例固化为常驻特定地理目标。宜降为G031的场景示例。','needs_revision',[issue('background','T099用let us say的机场/七天/舱位计算说明搜索复杂性，不是另立固定US–India查询需求。')])
note('DOC003','B',40,'T123明确“I like to maintain global access through priority pass”；属个人持续权益偏好，冻结清单未单列不代表无依据。不能解释成平台必须提供全球准入。')
note('DOC003','B',43,'T127确实要求有限次数卡检查有效和余额；本人用无限卡，故保留For a limited-use条件作为一般化举例即可，不能说本人余额不足。')
note('DOC003','B',45,'T137希望统一给参数找合适选项；已标inferred且rationale排除数学绝对最优保证，强度合适。')
note('DOC003','B',47,'T143/T147以熟悉稳定界面解释节时，G047只保留节时/认知负担结果；与G048更快准确和G049长期切换意愿可相容，虽有重叠不必一概合并。')

note('DOC010','A',2,'T017–T021目的地查天气、整周旅行计划、户外活动购票形成同一决策链；合并没有抹去条件，rationale保留日常按天/旅行按周。')
note('DOC010','A',7,'T041普通弹窗不需频繁，T049降雨例外；既有G006普通频率和G008降雨更新，这里额外一节点重复同一对比，未增加可区分满足结果。','needs_revision',[issue('over_split','G007与G006、G008均承接T041/T049同一通知策略；可把不必要打扰和降雨例外作为两节点条件，而非另立重复节点。')])
note('DOC010','B',8,'T021游乐园雨冷购票确有明确avoidance意图；是活动选择的具体实例，不应要求任何地点一律禁止购票，rationale保留了该场景。')
note('DOC010','B',12,'T035推迟活动与不出门可独立：取消活动后仍可能外出，或不外出但活动在线进行。与G023分开可接受，不以多动词数自动判过拆。')
note('DOC010','B',17,'T051被雨淋经历和T069明确实时更新愿望支持，准确为目标而非保证，rationale已保留技术限制。')
note('DOC010','B',19,'T057/T059的应用网站不同步是具体问题；G022扩至T071所有平台，可视为具体与一般范围，不自动认定重复。')
note('DOC010','B',20,'T063说hourly与G015雨开始停止通知有时间范围差别，合理作为更密集监测方式。不存在无条件全时每小时推送承诺。')

note('DOC013','A',1,'T004先描述viewer选择观看内容，T012后续确认为搜索/视觉浏览；可作上位选择目的，非凭角色名自动扩需求。')
note('DOC013','A',2,'T004明确streamer分享内容，T012上传和开播为两种方式；上位分享目的成立。')
note('DOC013','A',3,'T006语气有think/could，但也说have to make sure；support.rationale明确标为tentative且规则未定，未把它当已证实法规，接受该保守范围。')
note('DOC013','A',4,'T006区分不得向任何人分享的内容与只不适合部分观众的内容，分两目标保留了实际不同的限制对象。')
note('DOC013','A',10,'T012“perhaps a transcript captions”是可选建议；support已写proposed capability，不能因statement未逐字写perhaps就认定系统强制每个视频有字幕。')
note('DOC013','A',18,'T018只把确保无长度要求作为潜在障碍；inferred及无数字阈值保持试探，未外推所有格式或无限时长保障。')
note('DOC013','A',22,'T030明确订阅后中央区域查看最新内容；与订阅动作G021有后续取用目的，分开合理。')
note('DOC013','A',24,'T040是准确性未知，support.rationale将其写成inferred concern而非证实缺陷；允许保留为待探索字幕目标。')
note('DOC013','A',25,'T040不知道颜色能否调但认为可做工作；Consider配合解释保留探索性，不是断言缺少颜色设置。')
note('DOC013','B',5,'T012上传既有视频与开始实时直播是可分别满足的发布方式，模型以“或”并列能力承接，不声称精化充分；作为上位内容分享范围可接受，但覆盖不能替代首次频道及直播等待条件。')
note('DOC013','B',11,'T018格式/长度为潜在障碍，上传与发布是一个有上下游的交付目的；但发布便利又有G012，建议明确G011范围为上传兼容，不使同一发布简化重复。','needs_revision',[issue('compound','G011同时含上传成功、发布成功、格式兼容、长度障碍；T018将这些列为不同可能困难，且发布简单性已另立G012。')])
note('DOC013','B',12,'T018只问是否要等上传完才能发布。statement“减少等待完整上传后才能发布的不便”容易选定提前发布改进，虽rationale否认，声明与解释应一致。','needs_revision',[issue('strength','原文是potential questions，不足把等待完整上传认作已确定不便；可写“探索简化上传到发布过程，等待要求待核实”。')])
note('DOC013','B',14,'T040现状未知，inferred且condition需核实避免强称已知错误，判断supported仅指合理候选建议。')

note('DOC020','A',4,'T015先扫未读、标重要、再细读；标记与细读是可区别操作，成立，但它对识别前序工作不是反向因果（见R001）。')
note('DOC020','A',13,'T021明确编辑后send，作为现行发送操作有据，虽冻结清单未单列发送节点。')
note('DOC020','A',17,'T029新版默认、旧版/历史可按需看是编辑后的收件端结果；与发件人编辑动作G016可分。')
note('DOC020','A',19,'T037内置是比T019外部AI更具体的改进；G010与G019通过所选方式关系连接，非无意义复制。')
note('DOC020','A',25,'提案来自T054采访者，T055仅说one solution；statement Consider与解释准确保留这一较弱接受状态。')
note('DOC020','A',32,'T091称可能不实际，T093为未定义类别设想；Explore及rationale明确未知，未虚构协议规范。')
note('DOC020','A',38,'T015需要回复而当前无暇时稍后处理有据；与G007记录任务的标签动作可区分为记录手段和完成结果，允许分开。不能由此要求所有来信必回复。')
note('DOC020','B',5,'T011偶尔朋友联系与T095/T099未来工作专业联系有不同时间和目的；support.rationale已保留rare/未来，所以不另判条件丢失，但单个目标把可独立满足的社交与专业用途混合。','needs_revision',[issue('compound','朋友联系与工作专业联系来自不同情境；建议分别作用途或建立上位邮件沟通目标，保留现今偶尔与未来主要的范围。')])
note('DOC020','B',6,'T015–T017三种整理手段确为manageability服务，层次合并可接受；但其statement未含浏览未读/细读，不能把I03的完整日常筛读判已覆盖。')
note('DOC020','B',8,'T019 AI草拟后人工调整，T037希望内置；作为保留人类编辑的整体写信结果可接受，不要求每一步都独立成目标。')
note('DOC020','B',15,'T041要点摘要与T045–T047突出微小限制可分别达成；但两者共同构成AI阅读辅助，合并仍保留两项，不因粒度较粗自动判错。')
note('DOC020','B',18,'T071/T075明确转发与群发在紧期限场景重要；并列保留能力，不声称必须同时执行或充分完成团队沟通，接受该上位协作条目。')

note('DOC023','A',5,'T007公司+学校是实际搜索选词；G005仅说找到匹配的人，未保留选定公司名/学校名关键词搜索的方式，尽管rationale提及不能代替目标可执行含义。','needs_revision',[issue('selected_means_loss','T007明确search bar company name and school name；当前statement是结果筛选，G006/G010也未补齐搜索词方式。')])
note('DOC023','A',13,'T015付费扩大可见结果且成本高；when worthwhile保留选择性，与G014改词作替代，非强制购买。')
note('DOC023','B',3,'T009同时条件保留正确；但finding结果与T007具体公司名+学校名搜索方式、T009现任筛选应区别，statement没保留所选搜索词。','needs_revision',[issue('selected_means_loss','源文明确在search bar输入company name和school name，不能只以“找符合条件的人”认作完整方式承接。')])
note('DOC023','B',5,'T007通常介绍自己，但只maybe加入内推请求；这里无条件“并表达”提高了请求的必然性。','needs_revision',[issue('strength','T007“I maybe will also tell them”不支持每次附注都必须包含推荐请求；应保留可选/适当时。')])
note('DOC023','B',8,'T013/T015支持数量与成本负担改善，但把明确购买Premium或删/改关键词两条已选应对策略抽象成门槛负担，未完整承接策略。','needs_revision',[issue('selected_means_loss','T015明确purchase premium或modify keywords/remove/be specific；G007只含更准确结果，没有保留改词动作。')])

note('DOC031','A',8,'T011明确私信中共享文档；statement只剩队友共享，没有保留本人的direct messaging选择（T017给出个人页面附件）。','needs_revision',[issue('selected_means_loss','即时文件分享目的成立，但原文最常用方式是direct messaging，不能把泛化共享视为完整已选方式。')])
note('DOC031','A',11,'T021通话入口绕多窗是一般问题，G014是T027特别强调群组，可按一般/情境特化保留，不必判两节点重复。')
note('DOC031','B',5,'T009历史访问与关注当前动态是相关而可分的信息目的；作为频道获取信息的上位条目保留两项，没有声称历史必能覆盖当前事件，允许合并。')
note('DOC031','B',6,'T011–T017选定私信附加文档；现只写协作中即时分享，缺direct messaging路线。','needs_revision',[issue('selected_means_loss','原文明确最常用direct messaging中的sharing documents；结果级泛化使已选路径消失。')])
note('DOC031','B',7,'T019明确按keywords搜索；当前只留从大量搜索结果找到内容的结果级目标，未保留关键词策略。','needs_revision',[issue('selected_means_loss','T019“I would enter keywords”；全模型无关键词检索条目，不能只因引用该turn判完整。')])

note('DOC028','A',14,'T031承认有限使用社区相关趋势，随后明确非主要新闻源；Occasionally/relevant限制合适，不因背景候选就否定这个弱用途。')
note('DOC028','A',21,'T051称search准确帮助自己节时，可推维持该能力，虽冻结I01较上位仍可承接。')
note('DOC028','A',23,'T021发问与T059在特别合适的细分社区发问有不同精确度；G009/G023可保留一般和特殊策略，非必然过拆。')
note('DOC028','A',25,'T063官方应用应更好是移动改善的重申/竞争背景，当前再独立G025并贡献到G011几乎未增加可验收结果；建议合并为G011的定位。','needs_revision',[issue('over_split','G011已是官方移动可用性/响应改善；T063重新强调同一愿望，未规定额外市场份额或独立功能。')])
note('DOC028','B',4,'T011把匿名性视为USP，T055承认历史可识别；inferred并明确不保证绝对匿名，属于合理维护偏好，冻结清单只当背景不应使其自动无依据。')
note('DOC028','B',8,'T029/T057认可管理团队对低质信息的作用；inferred限定为维护能力且依社区而变，合适。')
note('DOC028','B',9,'T031有限趋势/当前事件用途真实，condition明确非主要新闻来源，接受该次要条目。')
note('DOC028','B',15,'T051/T059明确Gen AI工具找到细分社区，T061有坏答案例外；工具是选定方式而非直接AI诊断答案，保留正确。')

note('DOC036','A',1,'T010礼物购物与T056新地点找商家是目的与情境相连；与G006选择、G015收货多对多共同承接购物，不把单一发现步骤当独自充分。')
note('DOC036','A',2,'T010先看设计再线下买、T032他人穿衣影响购买有据；作为设计参考方式可共存，不把无意识影响改为促购要求。')
note('DOC036','A',9,'T062明确纠正不是ranking，statement保留跨时间互动比较并说辅助判断，正确。')
note('DOC036','A',15,'T058询价、支付、给地址和送达电话是完整订单流程；合并为收货目标可接受，仍保留重要信息，不将它当充分防诈骗方案。')
note('DOC036','B',5,'T014面对可疑账号要求先到货付款，statement明确when suspicious；与T058普通先付款流程不构成自相矛盾。')
note('DOC036','B',9,'T024匿名搜索也为不显示online，和G008访问方式可分目的；与G013仅给朋友看online的社交场景不同。')
note('DOC036','B',14,'T026明确担心个人生活公开未来伤害并用私密账号防范，受访者目的真实；不当作实际已被攻击。')
note('DOC036','B',16,'T032说个人喜欢cool穿法，作为购买品味确有依据；没有保留社交见闻如何成为购买灵感，故只能部分承接I17。')
note('DOC036','B',19,'T052节日前保持登录是绕行策略；只在计划购物周期内而非所有时间，条件保留正确。')
note('DOC036','B',25,'T058包含到货前/送达时电话联系，G025只写在约定地点收货，且G022–G024无通知目标，完整交付通知仍缺失。')
note('DOC036','B',26,'T062澄清跨商品年龄互动模式，和G011一般浏览评论有专门判别条件；可作细化，不视为纯重复。')

# Intent coverage exceptions are manual, not inferred from counts or word matches.
PART={
('DOC003','A'):{1:'G001/G002保留价格和合适行程，但未显式保留T107 flexibility这一较次质量维度。',3:'G012跨提供方比较存在，但未保留T025/T027不同时间反复检查及跨许多网站的研究策略。',7:'G007时间/连接适合有据，未单列T031终站与物流信息正确性核查。',9:'G011保留价格时长平衡，未保留T069出到达时窗过滤的所选手段。',10:'G013把重查选项也限定为紧急无替代，丢失一般不合适也重查情境。',20:'G023节时负担和学习成本有据，但T143稳定熟悉UI这个选定效率来源较隐。',21:'G022承接预填跳转和继续付款，未覆盖T031/T131输入个人/护照信息及卡付款。'},
('DOC003','B'):{21:'G014卡付款、G015预填跳转均在，T031/T131用户填写个人/护照资料和声明没有目标承接。'},
('DOC010','A'):{},('DOC010','B'):{8:'G014日常三次、G021日预报符合偏好，但T041从频繁弹窗降到合适频率的减少打扰目的未明确。'},
('DOC013','A'):{},
('DOC013','B'):{9:'G011/G012承接潜在上传发布顾虑，但G012statement较强地把等待当已定不便。'},
('DOC020','A'):{},('DOC020','B'):{3:'G006只保留标记重要，T015快速扫未读及细读重要邮件未建模。'},
('DOC023','A'):{3:'G005公司/学校背景结果存在，但原文公司名+学校名输入search bar的方式未保留。'},
('DOC023','B'):{3:'G003只有结果双条件，没有T007所选公司名+学校名搜索方式。',5:'G003rationale提校友愿意帮忙，但缺发送消息强调共同学校这一策略。',6:'G005附注保留介绍和请求，但T007maybe请求被升格为无条件并列；邀请动作也仅隐含。',9:'G008仅抽象为数量/成本，未留购买Premium或删改关键词的明确替代策略。'},
('DOC031','A'):{6:'G008保留即时分享，未保留私信这一主要所选渠道。'},
('DOC031','B'):{6:'G006有即时文档共享，私信方式丢失。',8:'G007覆盖结果过量和查找效率，但关键词搜索方式未保留。'},
('DOC028','A'):{5:'G002提followed communities，未明确T019 feed应贴合本人兴趣；没有把兴趣类别固化。',7:'G009有发问，但标题/正文/Markdown/媒体表达能力无承接。'},
('DOC028','B'):{5:'G002感兴趣社区存在，T019按本人偏好定制feed未明确。'},
('DOC036','A'):{},
('DOC036','B'):{11:'G022–G025覆盖询价/支付/地址/收货，但没有T058送达前电话联系。',17:'G016个人cool风格不等于T032从他人穿着获得购买灵感；G002是商家设计参考。'},
}

# Related but insufficient edges are accepted at their stated contribution/means/order type.
REL={
'DOC003':[
'T015提前买为了好价，作为尝试性手段成立，不保证便宜。','T017剩余积分/券帮助替亲友订票，条件性手段成立。','T025跨站重复比较为找优惠方式，非充分条件。','T065国家区域输入扩大机场组合，操作方式成立。','T069接续时限筛选为配合交通安排，方向正确。','T073国际价格时间折衷是一般替代评估的情境特化。','T073国内便宜标签是另一情境特化，非所有行程规则。','T077最终费用/优惠比较服务于T103选定行程价格。','T081重查是找到可行方案的应对方式，并保留无替代妥协。','T083末班火车是接续交通的具体场景，预算可让步。','T087提醒可能帮助低价出现时及时订，不保证降价。','T053匿名是减少数据披露的本人方式，不确认跟踪涨价事实。','T089不多给另一方数据是隐私目标特化。','T099只是说明规模的例子；将其建为独立特化目标会固化地理例子，宜改为场景注释。','T109/T111市场价比较辅助判断价格，不直接产出最低报价。','T119会面对象时间是旅程适合的具体条件。','T119睡眠偏好对适合性有帮助，可接受红眼。','T123转机余量帮助接续，无法保证延误不发生。','T125权益整合可能帮助贵宾室机会判断，但权益与开放是不同维度，只能有限贡献。','T127发卡方来源可查开放时间和政策，作为所选信息源成立。','T095/T147并行查组合减少重复研究，有贡献而非充分。','T137信息集中减少站点切换，与认知时间负担有关。','T047/T135供应商页面在付款之前，顺序成立。','T031核对物流再付款，顺序成立而非充分。'],
'DOC010':[
'T007穿戴是天气生活规划的具体用途。','T007户外活动是明确的规划用途。','T017目的地查天气为旅行决策所选手段。','T019旅行时整周范围服务于出行前查天气，不强制日常按周。','T013取得天气信息帮助衣物选择，不自动作决定。','T013天气信息也帮助携带物品决策。','T035看到严重天气后取消活动，源文顺序成立。','T039预警为获知极端天气方式。','T049频繁降雨状态通知是T051实时更新的一种具体情况。','T051实时信息影响走路/公交选择，不保证预测绝对正确。','T063恶劣天气每小时监测是更新方式，不把日常也改为每小时。','T057具体应用网站一致性属于T071跨平台一致性的情境。','T065日常预报帮助日常计划，贡献成立。'],
'DOC013':[
'T012文字筛选搜索帮助viewer选择视频，为所选方式。','T012视觉缩略图浏览为另一内容选择方式。','T012上传是分享内容方式，不是唯一方式。','T012直播为分享内容的替代方式。','T014模糊条件仍有意义是搜索能力的特殊范围。','T016检索帮助快速获信息，内容相关性仍必要。','T016教育观看可贡献获取信息，并非所有教育都快速。','T018格式兼容帮助上传，不能保证传输完成。','T018减少长度障碍帮助上传，规则仍未定。','T030先订阅后可从订阅区取最新内容，条件性顺序成立。'],
'DOC020':[
'T015先扫读判断重要再标记；目前G004标记反向贡献到G003“识别重要”会混淆先后，标记更直接支持之后注意/回访。','T015快速扫未读后细读重要，顺序有据。','T015标签记录暂不能回的任务然后有空完成，作为顺序成立；并不声称每封邮件都需回复。','T017分账户可减少重要招聘邮件混杂，不保证不遗漏。','T019生成草稿先于用户修改，顺序有据。','T019/T021用户改好后再send，顺序成立。','T021字号调整是当前发信前步骤，不是发送前普遍必要条件。','T021加粗强调在发送前，保留场景后成立。','T025/T027避免错分有助不漏招聘消息，不是到达保证。','T037内置AI是T019按要点写信的具体方案。','T041/T053摘要可节省逐封阅读，非保证摘要无遗漏。','T045/T047突出容易漏看条目帮助重要邮件理解，关联成立。','T054/T055批量摘要只是可考虑办法；operationalization保留候选语气方成立。','T059可靠提醒可帮助防漏，但用户明确不完全依赖。','T087搜索是标签过滤可能采用的实现方式，方向正确。'],
'DOC023':[
'T003连接数用于向他人显示活跃，作为贡献而非活跃证明成立。','T003内推提高招聘者看简历机会，概率贡献成立。','T007明确搜索公司名+学校；当前源节点只写找到相同背景，rationale补充搜索才可成立，应先修G005所选手段。','T007先看经历再邀请，顺序成立。','T007接受邀请后才聊天，顺序关系和目标条件一致。','T007可选附注介绍/请求有助内推，不保证回应。','T009现任员工同校条件比T007混合前/现员工结果更窄，特化成立。','T011校友助人意愿是本人预期，贡献不当普遍事实。','T015改关键词为提高相关性策略，方式明确。','T015结果可访问更多可能助找内推人，非充分。','T017减少压缩负担帮助附注表达，贡献合理。'],
'DOC031':[
'T007即时性将一般校园沟通目标加质量条件，特化成立。','T007姓名检索减少保存联系方式是即时触达所选方式。','T007手机/电脑提供沟通通道，不保证对方在线。','T009频道是即时校园通信的广受众特例。','T009历史帮助了解课程校园，不能保证最新事件完整。','T011/T013直接把共享文档联系即时沟通，关系成立；源节点应补私信方式。','T019减少命中过多的难度有助定位历史内容。','T023已知号码直接电话是更快联络的条件性替代。','T027转邮件应用服务正式校园沟通，不自动代发。','T027群组是通话入口改善特别强调的场景。','T031窄窗改进可帮助并排工作的沟通，贡献合理。'],
'DOC028':[
'T003技术代码问题是具体问题求助的子类。','T005情境经验有助针对问题答案，不证明真实性。','T007问题+Reddit的Google搜索是所选路径。','T009针对问题的答案可能解决问题，不是必然。','T021社区发问是获得相关建议的一种途径。','T027移动存草稿修复一个具体可用性障碍。','T027线程清晰修复另一个障碍，不能修复所有慢问题。','T033产品评测是特定问题答案的具体应用。','T035一般健康学习是信息获取子类，保留不依赖具体医疗建议。','T043被动卡片浏览为休闲阅读的选定显示方式。','T043紧凑视图帮助比较定向搜索结果，方式明确。','T047无adblock才考虑premium，是无广告方式之一。','T051准确结果帮助更快找到信息，贡献成立。','T059找到具体社区然后发问是所提工具流程，顺序合理。','T061细分社区发问预期回答更好但仍可差，贡献合理。','T051/T059工具找到社区可服务较佳答案，但中间需发问/回应；非充分，作为方式可接受。','T063只是重申官方移动端应更好，与G011近同义；重复节点之间再建贡献无新增语义。'],
'DOC036':[
'T010/T012搜索相关本地商家是礼物来源的方式。','T014可疑商家先交货后付款是防该风险方式，非全球交易规则。','T016快速联系商家帮助购物，但不保证有货发货。','T022无固定商品时浏览品种为挑礼物方式。','T024不登录是避免被见在线的本人方式，不证明绝对技术匿名。','T024复用历史是回到已知商家的另一方式，不是G003“按产品地点搜索附近新商家”的操作化；应指向更上位商家取回/发现目的。','T024评论点赞有助识别可疑账户，非安全证明。','T026私密账号为避免公开个人生活风险的策略。','T026在线只给朋友可降低公开曝光，贡献有据。','T052退出删应用等是限制使用的自控方式。','T052在计划购物期暂留登录是受控使用的绕行方案，并非否定理想匿名浏览。','T056新地点商家信息帮助采购，礼物是其既述用途。','T058通常先问价再支付，顺序成立。','T058普通流程支付后给地址，T014可疑案例例外已保留。','T058地址帮助交付但不能保证诚实商家，贡献成立。','T062跨年龄互动模式是本人判断风险的具体方式，不是自动排名。'],
}

REL_REVISE={('DOC003','B',14),('DOC020','A',1),('DOC023','A',3),('DOC028','A',17),('DOC036','B',6)}

GROUP={
('DOC003','A'):['F001把价格、情境行程和供应商比较作为研究组织候选，T115/T129支持这些方面；proposed/partial没有宣称充分。','F002交通、睡眠、转机余量对应T083/T119/T123，T119明确仅examples；部分候选分组合理，不要求所有行程同时满足。'],
('DOC003','B'):['T119明确时间匹配例子，F001保留proposed/partial；签证和预算例外未变硬约束，组织合理。','T015/T025/T077/T087这些优惠策略依场景而用，F002明确非强制AND且partial，因此不因不充分判错。','T095/T137并行与集中资料针对研究负担；F003只提出部分方案，没有保证快速准确。'],
('DOC010','A'):['当前天气、严重天气、实时变化均影响规划（T025/T035/T051），但不包含所有整周旅行信息；proposed/partial准确承认限制。'],
('DOC010','B'):['F001三个规划用途来自T007/T017；声明partial合适，非强称覆盖全部日常决策。','F002具体应用网站是一致性局部范围（T057/T071）；未把单一对子当所有平台已覆盖。'],
('DOC013','A'):['上传和直播是T012两条替代方式，F001自身明确alternatives/proposed/partial，因此不能按已成立AND精化审判；保留发布权限未知。','T018格式长度仅潜在上传障碍，F002部分候选并未宣称足够；示例反例标analysis_assumption而非伪造源文。'],
('DOC013','B'):['T012/T014/T016搜索浏览和流畅观看有助获取信息，F001保持partial；内容是否合适仍未知，没有过度充分声明。'],
('DOC020','A'):['T017/T027/T059的策略有助防漏，F001保留partial并承认收不到/识别失败，不把人工信任例外消掉。','T041/T045/T054摘要、突出细节、批量汇总是互补/替代策略；F002承认准确性未知，未强称充分。'],
('DOC020','B'):['分类/到达/提醒对应T027/T033/T059，F001以proposed/partial承认仍可能漏看，成立。'],
('DOC023','A'):['T007邀请交流工作流只提升内推机会，F001保留proposed/partial且反例允许拒绝；没有将对方意愿当系统保证。'],
('DOC023','B'):['T007筛选/看经历/邀请/聊天是有据候选结构；F001自己承认对方未必推荐，不能因不充分本身判错；G005可选请求偏差另评。'],
('DOC031','A'):['T007/T009/T011/T021不同场景沟通方式并非都必须一起执行；F001解释正这样限定并保持partial，合理。'],
('DOC031','B'):['F001将姓名查找、设备、频道、文件和通话视为通信支持方式，proposed/partial未错误声称AND共同充分；结果不保证对方立即回复。'],
('DOC028','A'):['T005/T059/T061支持经验与具体社区可能带来更好答案，F001保留坏答例外和partial；不当成专家正确保证。','T027移动草稿/线程只是两项具体障碍，F002明确还会慢，故部分候选判断合适。'],
('DOC028','B'):['T007/T021/T059检索、发问和社区发现是不同可选策略；F001没有把全部执行写成充分，partial合理。'],
('DOC036','A'):['本地发现、浏览、联络、防风险和收货对应T012/T014/T022/T058，F001只候选部分组织；适合商品及诚信未知均未虚假保证。'],
('DOC036','B'):['T014/T024/T062风险识别与付款防范有据，F001承认可伪造互动，partial合理。','T012/T022/T016/T058购物流程有据，F002仍需真实商家和适合礼物，明确partial，不强称收货保证。'],
}

def iid(d,n):return f'{d}:I{n:02d}'
def gid(n):return f'G{n:03d}'
def shorten(s,n=120):return s if len(s)<=n else s[:n]+'…'
def evidence_text(inv,nums):
    bits=[]
    for n in nums:
        e=inv['intents'][n-1]['evidence'][0]
        if e['source_id'] not in [x[0] for x in bits]:bits.append((e['source_id'],shorten(e['quote'],80)))
    return '；'.join(f'{sid}「{q}」' for sid,q in bits)

for d in DOCS:
    inv=inventories[d]
    result=dict(document_id=d,reviewer='独立上下文模型评审者',human_gold=False,
        round='first',blinding_limit='仅知A/B匿名代号，未读映射或其他分支；语言、节点粒度、解释模板等方法特征可被猜测，因此属于有限盲法，非严格不可猜方法的双盲。',
        policy='冻结129条意图不修改；允许多对多和不同粒度。supported评价源文支持及合理推断，不代表需求已采纳；proposed/partial结构按候选强度评价。未计算标准P/R/F1。',samples=[])
    for s in ['A','B']:
        m=models[d,s];maps=MAP[d,s];assert len(maps)==len(m['goals'])
        matches=[]
        for n,intent in enumerate(inv['intents'],1):
            ids=[g['id'] for g,mp in zip(m['goals'],maps) if n in mp]
            if not ids:
                status='absent';why='未找到目标承接。冻结条目为“'+intent['intent']+'”；'+evidence_text(inv,[n])+'。这表示模型覆盖缺口，不直接证明现有目标错误或此能力应强制实施。'
            elif n in PART.get((d,s),{}):
                status='partial';why=PART[d,s][n]+' 原文：'+evidence_text(inv,[n])
            else:
                status='complete';why='这些目标共同保留“'+intent['intent']+'”的实质结果与适用范围；'+evidence_text(inv,[n])+'。不要求独立节点数或层次与清单一致。'
            # Explicitly unknown current capability remains unknown, not converted to a demanded feature.
            if n==20 and d=='DOC028' and not ids:
                why+=' 原文仅描述有限离线缓存、并未请求扩展；该清单条目的目标性本来不确定，遗漏权重应低。'
            matches.append(dict(intent_id=intent['intent_id'],goal_ids=ids,status=status,rationale=why))
        ga=[]
        for k,(g,nums) in enumerate(zip(m['goals'],maps),1):
            if (d,s,k) in NOTES:
                judgment,why,issues=NOTES[d,s,k]
            else:
                judgment='supported';issues=[]
                assert nums,(d,s,k)
                why='与源文“'+'；'.join(inv['intents'][n-1]['intent'] for n in nums)+'”相符；'+evidence_text(inv,nums)+'。作为该受访者的目的、条件性方式或已标明的改进推断可保留，未额外读成普遍保证。'
            ga.append(dict(goal_id=g['id'],judgment=judgment,intent_ids=[iid(d,n) for n in nums],rationale=why,issues=issues))
        ra=[]
        if m['relations']:
            assert len(REL[d])==len(m['relations']),(d,len(REL[d]),len(m['relations']))
            for k,(r,why) in enumerate(zip(m['relations'],REL[d]),1):
                ra.append(dict(relation_id=r['id'],judgment='needs_revision' if (d,s,k) in REL_REVISE else 'consistent',rationale=why+' 当前关系按包内'+r['type']+'/'+r['status']+'评价，不等同一组充分精化。'))
        assert len(GROUP[d,s])==len(m['groups'])
        groups=[dict(group_id=g['id'],judgment='consistent',rationale=why) for g,why in zip(m['groups'],GROUP[d,s])]
        sample=dict(sample='first:'+s,intent_matches=matches,goal_assessments=ga,relation_assessments=ra,group_assessments=groups)
        assert len(matches)==len(inv['intents']) and len({x['intent_id'] for x in matches})==len(matches)
        for key,objkey,idkey,items in [('goal_assessments','goals','goal_id',ga),('relation_assessments','relations','relation_id',ra),('group_assessments','groups','group_id',groups)]:
            assert [x[idkey] for x in items]==[x['id'] for x in m[objkey]]
        valid={g['id'] for g in m['goals']}
        assert all(set(x['goal_ids'])<=valid for x in matches)
        result['samples'].append(sample)
    (OUT/d/'review-first.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

errata=dict(artifact_type='source_inventory_errata_separate_from_freeze',reviewer='独立上下文模型评审者',human_gold=False,
    frozen_inventory_modified=False,
    note='以下是阅读匿名包后发现的原清单边界与遗漏，单独记录；不能回写冻结清单并以此改善任何样本覆盖。',
    entries=[
        dict(document_id='DOC003',type='omitted_explicit_intent',source_id='DOC003:T017',quote='if I\'ve got like extra points, or like gift vouchers left over, so I can help friends book their own flights',note='替亲友订票主体已保留，但以剩余积分/礼券帮忙省钱并用券的具体目的未单列；A G004、B G006有支持。'),
        dict(document_id='DOC003',type='omitted_personal_plan',source_id='DOC003:T029',quote="I'll definitely be traveling somewhere during the winter break.",note='冬假旅行是明确的一次个人出行意向，可能仅为示范场景；未列持久应用意图。B G009保留它不自动算幻造。'),
        dict(document_id='DOC003',type='omitted_continuing_preference',source_id='DOC003:T123',quote='I like to maintain global access through priority pass.',note='本人维持Priority Pass权益有明确语句；清单只列使用贵宾室与查权益，未单列维持权益目的。B G040有依据。'),
        dict(document_id='DOC013',type='goal_vs_capability_boundary',source_id='DOC013:T038',quote="I'm able to toggle and untoggle the full screen.",note='I14/I15包括现场播放器能力描述，目标意图强度弱于T012明确essential需求；未覆盖仍记absent，但不能按每个控件缺失断言模型质量差。'),
        dict(document_id='DOC028',type='goal_vs_capability_boundary',source_id='DOC028:T039',quote="there is an offline capability, but it's not very comprehensive.",note='I20明确标不确定，原文只描述缓存能力而未提出扩展愿望，缺失应低权重。'),
        dict(document_id='DOC028',type='background_can_support_inference',source_id='DOC028:T011',quote='the USP. Of Reddit is anonymity',note='冻结为背景候选并非否定需求；结合T055身份可推保留匿名性的有限偏好，B G004可支持。'),
        dict(document_id='DOC031',type='coverage_status_correction',source_id='DOC031:T019',quote='I would enter keywords',note='原清单I08同时包含方式与结果；A G009/G010完整，而B G007结果级条目未留关键词。多对多评审保留这个区别。'),
    ])
(OUT/'errata-first.json').write_text(json.dumps(errata,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
checks=dict(status='pass',round='first',reviewer='independent_context_model_reviewer',human_gold=False,
    frozen_manifest_sha256=hashlib.sha256((OUT/'freeze-manifest.json').read_bytes()).hexdigest(),
    frozen_inventory_hashes_unchanged=True,
    counts={d:{s:{'intents':len(inventories[d]['intents']),'goals':len(models[d,s]['goals']),'relations':len(models[d,s]['relations']),'groups':len(models[d,s]['groups'])} for s in ['A','B']} for d in DOCS},
    anonymous_package_sha256={f'{d}/{s}.json':hashlib.sha256((PACK/d/f'{s}.json').read_bytes()).hexdigest() for d in DOCS for s in ['A','B']},
    unique_exact_coverage=True,no_standard_prf=True,no_unblinding=True,completed_at_utc=datetime.now(timezone.utc).isoformat())
(OUT/'validation-first.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('ready first: 8 documents, 16 samples; inventories unchanged; every intent/goal/relation/group reviewed once')
