from pathlib import Path
exec(Path('output1/revised/_authoring/batch1_helpers.py').read_text(encoding='utf-8-sig'))
DOC='DOC021'
g=[
goal(1,'direct','搬往新地区或国家时找到适合居住的房源',3,'when I move to a new neighborhood or to a new country, I need to find a new place.','明确搬迁找住处目的；不假定购买而非租赁。'),
goal(2,'direct','先找到目标地区常用的房源网站，了解当地可选房源及价格范围',5,"I want to be familiar with which websites are the most popular or most used there.",'明确陌生地区资源发现与概览用途，后续概括信息收集。',['可能参考当地人建议；网站选择不等于保证真实。'],extra=[(57,'give me an overview about the price ranges about the available options')]),
goal(3,'direct','按预算、面积或卧室数筛选房源，并在需要时靠近工作或学校',9,'I will search by like the size of the place, or sometimes by bedroom counts. and with also a budget limit.','本人主要条件直接；近工作/学校为条件性通常偏好。',['设施、附加功能和外观为次要进一步取舍，未设权重。'],extra=[(7,"I will usually pick a neighborhood that's close to that area")]),
goal(4,'direct','通过沟通获得足够信息并根据回复情况进一步判断和缩小房源选择',11,'when I contact them, sometimes like how fast they will reply might affect my choices','明确沟通在决策中的用途；不回复管理差是本人判断而非已证事实。',['可转用电话、邮件或房源自己网站；平台主要用于发现。'],extra=[(11,'communication process, which will help me also to narrow down my options.')]),
goal(5,'direct','希望房源信息可信且能看到最后更新时间，以判断是否仍然有效',69,"I just want to be assured that it's it's up to date.",'反复明确新鲜度和可见时间，保留实际更新与可知时间两个相关结果。',['详情现有地址、照片、户型、价格、单位数量和设施等本人觉得充分，主要缺更新时间。'],extra=[(59,'to be able to see when it was last updated.')]),
goal(6,'direct','联系房源前后能清楚看到流程、下一步及预计回复时间，增强使用信任',25,'I would love like to know if I just proceeded with this option, what will happen when they would they respond to me? What will be next?','明确过程可见意图与回复期望；实际回复也可能很快但UI不清楚。',['可用小时间线等视觉方式；一周至一月为常见决策窗口，不设所有人最大等待。'],extra=[(73,'They might reply like, very, very fast, but it\'s not clear to me.')]),
goal(7,'direct','希望可从已列出的具体房源规格中直接选感兴趣选项，避免被要求先精确自定义所有需求',25,'they can just list it with their specification, and I can have something similar to the concept of. Add to cart','本人明确电商式选现有选项建议；不擅自把选房变立即付款订购。',['咨询时需求可能灵活，还未确定卧室、浴室和日期；类似加入购物车是选择概念。'],extra=[(23,"Sometimes you're flexible. You just want to communicate, to know more or to get specific information.")]),
goal(8,'direct','双方确认房源可用且有意继续后再分享个人资料，避免向所有感兴趣选项预先交出大量信息',27,'giving the information could be after confirming the availability from the 2 parties','明确分享时机和方式限制；不改成永远不提供姓名电话。',['房源先表明可用，自己感兴趣，双方确认继续后才可能分享。'],extra=[(27,"I will not be comfortable to share my information with all options that I might be interested in.")]),
goal(9,'direct','可用地图画定搜索区域，更灵活地包含邻近合适房源',33,'a map with a drawing tool where you can just draw a circle around the place you\'re interested in','既有功能有避免被邻区名称排除的明确用途，支持维持。',['2米邻近为例示，不作固定半径。']),
goal(10,'direct','查看住过房源者的评价，汇集信息并帮助建立信任',33,'reviews from people, makes. makes places feel more trusted','既有评价信息的明确用途，未把评价当绝对真实证明。'),
goal(11,'direct','将几个感兴趣房源集中在一页，同时比较主要特征',37,'I want to collect them all in in like a single page. So I can look in the main features at the same time.','明确比较建议，3或4项是例子而非上限。'),
goal(12,'direct','收藏房源后能在导航栏或至少菜单第一层找到保存项',39,'It should be like on the nav bar, or at least at the menu, at the like 1st level of the menu.','直接选定易找位置的建议；本人不知道收藏在哪里，未断言实际未保存。',['收藏用于保存感兴趣房源，常与比较联系。'],extra=[(35,"I can't find where where it's saving it.")]),
goal(13,'direct','不强制注册或登录即可搜索、查看信息并与房源方沟通，注册可供自愿保存或预填资料',43,'It could be optional thing like if you want your information saved and to be filled directly you can register. But it should not be required.','明确可选注册，保留直接全功能使用的愿望和资料保存例外。',['本人认为无必要个性化是其信念；非已证架构不能需要账户。'],extra=[(45,'Just start searching and seeing the whole functionality directly.')]),
goal(14,'direct','保留可选的筛选项，不强迫在需求尚不确定时填写所有条件',51,"I like that. The filters are optional. They don't enforce you to enter everything",'赞赏现状并说明不确定需求用途，明确维持意图而非自动把功能当目标。'),
goal(15,'direct','筛选如宠物政策时可选择同时包含明确允许与未填写者，或仅显示明确允许者',55,"The one who allowed and the one who didn't specify, and if I didn't click on the checkbox, I will have the ones who only specify that they allow.",'T051—055给出明确checkbox方式与双模式；未把未填当确定允许。',['可考虑增加“包含未说明”复选框；不包含明确不允许的选项。'],extra=[(53,'a check box called include, for example, like the options that didn\'t determine')]),
goal(16,'direct','可以考虑要求房源照片采用特定拍摄规范，以更可信地呈现房源',59,'if the website has some sort of rules that enforces people who own these properties to take the picture in a specific format','明确maybe建议且保留规范方式，阳光与角度为例，不认证规范必然防美化。',['担心差照片误弃好房或照片优于真实；可信度效果未知。']),
goal(17,'direct','若沟通过程清楚且快捷，希望在单一平台内完成房源沟通',71,'It will be so good like to have all the communication through a single platform.','明确有条件的一站式沟通愿望；不因目前外部联系就误删该结果。',['当前因为平台过程不清会用电话邮件，未知回复速度是体验不透明，不必然房源方慢。'],extra=[(71,'If the process was clear and fast.')]),
goal(18,'direct','信息与流程更透明时对房源更有信任并愿意继续参与选房过程',21,'it gives you more trust, and it gives you more enthusiasm to go through the process','明确希望透明带来舒适和参与；主观软目标，未设量化信任指标。',['更新时间和小时间线是本人提出的因素，不保证全部欺诈风险消失。'])]
f=[group(1,18,[5,6,10,16],21,'If they just show me more about what will happen? I might be more comfortable','更新可见、流程、评论和照片规范可能共同帮助信任，但原文might及其他真实性风险未排除，整组仅候选partial。'),group(2,1,[2,3,4,11,17],71,'if these websites made communication easier it will be. It will be great to have all the housing communication in a single place.','研究、筛选、比较和沟通贡献找房，未涵盖看房、合同、实际可用性或其他完成条件，不能宣称足以找到可入住住房。')]
q=[question([6,17],'预计回复时限、超时状态及后续流程应如何展示？','主要问题是过程未知，实际可能回复很快；没有固定时限。'),question([8,13],'初步咨询最低需要哪些资料，何时双方确认可以共享更多？','保留可选账号与延后数据分享边界，最少字段未定。'),question([15],'未填政策如何标识和后续核实，避免被误解为确定允许？','本人要包含未知而非把未知变肯定。'),question([16,18],'照片规范要约束哪些内容，如何判断可信度提升？','拍摄方式只是建议，不能证明信息真实性。')]
r='''# DOC021 生成方语义自检

完整读T000—T076共77轮，按0—59/60—76覆盖所有问答与最终重申。未核听、未验证网站功能；同一生成者自检。

逐目标：G01搬迁找住所；G02陌生地区常用网站和概览；G03预算/面积/卧室与近工作学校，附次要设施不强化；G04沟通用于筛选，管理差属推测；G05新鲜且可知更新时间，详情现状足够不重复造全部字段节点；G06下一步/回复时间透明而非已证慢；G07选已列规格的类购物车建议，不变成在线购买；G08双方确认后才可能分享数据；G09地图画区域已有明确用途；G10评论作为信任线索；G11单页比较；G12收藏入口明确导航位置，保存是否发生本人未知；G13注册可选且用于保存预填的例外；G14可选筛选为有目的维持；G15含未知复选框/双模式完整保留，未知不当允许；G16照片规范是maybe建议；G17清楚快捷条件下平台内沟通；G18主观信任与继续参与软目标。

F01/F02均proposed/partial：透明因素是信任贡献，不证明真实性；找房过程因素不是共同充分保证实际居住结果。未把外部联系和平台内联系画完整OR，前者是当前回退，后者是条件性期望；未把“更喜欢”“信任”误当充分方案。G15虽有两显示模式，也不能各自当完整OR满足用户能任选两种模式的父目标，未制造此错误。

正常场景（分析假设）：迁居时用预算与地图圈选，比较数个房源，看到新更新时间与清楚回复预期后选择一套表达兴趣，双方确认再分享资料；各目标在条件内一致。异常场景（分析假设）：房东允许宠物但未填字段，G15可保留候选而不保证允许；须核实。异常场景（分析假设）：照片规范/近期更新时间均满足但内容虚假，F01不能证明信任正当或安全。边界场景（分析假设）：平台提示预计快速回复但仍无回音，可转电话邮件，G17条件未实现不与当前策略冲突。

范围与遗漏：T065/067/069说详情大体充分，只缺更新保证；未将每个字段都自动变新需求。登录行为不等于想强制登录，后续明确相反。未知收藏保存位置和政策缺失的担忧均按不确定保存。全部问题待审，独立语义/形式证明not_run，冻结inspect实际执行。
'''
save(DOC,g,f,q,r,[{'target_type':'group','target_id':'DOC021-F01','message':'可信线索不能保证真实且原文保留might；整组部分贡献。'},{'target_type':'group','target_id':'DOC021-F02','message':'找房研究与沟通没有覆盖实际入住全部条件，保持部分候选。'}])
