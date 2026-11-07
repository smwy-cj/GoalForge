from pathlib import Path
exec(Path('output1/revised/_authoring/batch1_helpers.py').read_text(encoding='utf-8-sig'))
DOC='DOC005'
g=[
goal(1,'direct','通过背景音乐缓解现实生活压力并感觉生活仍在继续',13,"I think it kind of distracts me from the stress of the real world.",'回答为何高频听音乐，直接表达主观作用和动机；不声明医疗效果。',['考试或压力大时听得较少，但仍需要背景声音。']),
goal(2,'direct','尽量有声音在背景播放，以避免难以适应的安静',79,"But I always need something playing in the background.",'在应用都不可用的假设问题下明确持续背景声音需求，音乐、电影、电视、广播是可替代策略，不强制单一应用。'),
goal(3,'direct','按当下需要播放熟悉的歌单，并使用随机播放及整单循环',27,"Think of what do I really read? Need right now? Click on the playlist. I put it on shuffle. and then I put it on a repeat once the entire playlist is over.",'有结果意图的常用方式，保留已选shuffle及整单重复，不改成固定流程适用于所有使用。',['约七成使用为此方式，其余使用会搜索新曲。']),
goal(4,'direct','通过情绪或关键词搜索公共歌单，找到贴合当前感受的歌',33,"I search for either the emotion that I'm feeling or keywords that I feel like someone might have already created a public playlist, too.",'明确情绪匹配意图，搜索方式来自本人。',['感到特定情绪时。']),
goal(5,'direct','为脑中舞蹈等创作构想寻找匹配歌曲并获得灵感',33,'I want to find songs to match the vision I have in my mind.','明确构想匹配及灵感目标，未将不清楚的shopping转写擅自解释成编舞事实。',['通过关键词试听不同歌单和歌曲，是否获得灵感未保证。'],extra=[(33,'just listen through and see if inspiration strikes with any one of them.')]),
goal(6,'direct','听到感兴趣的歌曲片段后找到完整歌曲，并继续发现相似且喜欢的新歌',55,'I search for that particular song. I try to listen to it fully','有发现意图的现有完整播放与相似推荐用途，非单纯能力罗列。',['也会在原歌单收听期间想听新歌。'],extra=[(55,'it plays songs similar to that. So then I\'m like, Okay, Vibe, what are the other songs that are there?')]),
goal(7,'direct','保留适合自己口味的个性化歌单，以更容易找到更多喜欢的歌曲',85,'with this made for you, but by spotify, I would say the chances go up to around 10 to 12 songs out of 20.','T081/085赞赏用途，T105称不可缺，支持已有功能维持；10至12是个人估计而非验收保证。',['包括当前常听、昔日喜爱、日常及相似歌手混合；口味会随时间改变。'],extra=[(105,'Definitely. Playlist is one made for use. Another.')]),
goal(8,'direct','睡前可按歌曲结束或所选时长停止播放音乐',65,'at the end of the song music stops playing, or 30Â min or 25Â min.','本人喜欢已有sleep timer并说明睡着情境，支持维持此方式，不自动补所有分钟选项。',['睡前使用，原文时间为选项示例。'],extra=[(67,'And fall asleep. I I like that.')]),
goal(9,'direct','能创建便于他人查看的共享歌单，并保留一起听歌的社交选项',67,"And then Scott also has the starter jam options, which I think is really cool, and the shared playlists over here.",'明确赞赏的社交用途且转平台回答提到能力价值；为偏好维持意图，未断言竞争产品当前缺失。',['关于Apple Music缺失的判断仅为过去使用经验，当前是否更新本人未知。'],extra=[(67,'So creating a playlist for people to view is quite easy.'),(69,"I don't know if it is updated.")]),
goal(10,'direct','保留可收听的优质环境声音内容',105,"sometimes I like to listen to ambient noise, so without that I don't think spotify would be spotify.",'不可缺陈述明确维持意图，不能因已实现而排除。',['有时听环境声音；音乐内容还包含电影、音乐剧和独立艺术家作品。']),
goal(11,'direct','希望首页展示普通用户创建并受欢迎的公共精选歌单',93,'it would be nice to maybe have something on the home screen, like featured playlists. which are public playlists created by random people, not just by any curators that get the most traction.','显式nice/maybe建议，保留首页和普通人方式，不强化为必须。',['主要动机是不同视角，社交只是兼有作用。']),
goal(12,'direct','可以考虑根据相近听歌者推荐他们听的歌单，以获得不同的人类视角',99,'if they find someone else listening to kind of the same songs. if they can suggest a playlist that they will listen to.','提出基于所存所听歌单匹配他人的具体建议；情绪算法限制是本人信念，效果本人不确定。',['建议是否有效未确定，不代表已采纳或技术可行性已证。'],extra=[(101,'an algorithm cannot really replicate human emotions.'),(103,"I'm not sure how much it would work, though.")]),
goal(13,'inferred','在主要平台找不到特定混音时仍能通过其他平台听到它',31,"Sometimes spotify don't have specific mixes that maybe I find on the Internet or something.",'由缺内容时改用YouTube Music的明确情境推断可获得内容的意图，非要求Spotify拥有全部版权。',origin='inferred',reason='受访者解释约5%改用另一平台是因为特定混音缺失，行为正面支持仍想听该内容。',assumptions=['替代平台使用与前句内容缺失是因果说明。'])]
f=[group(1,6,[7,11,12],99,'More of, you know, a different perspective.','个性化和他人歌单都可能帮助发现，但未保证能找到某一片段的完整歌，且两种推荐建议可能是替代或补充；不构成共同充分。')]
q=[question([11,12],'首页热门公共歌单与相似听歌者推荐应如何组合，什么样的推荐算有价值？','两项为不同视角的建议，效果及关系未定。'),question([8],'睡眠计时所需的具体可选时长有哪些？','25/30分钟及歌曲结束只是原文示例。')]
r='''# DOC005 生成方语义自检

完整读取 T000—T115 全部116轮，包含采访者提问、回答、少量中断及结尾。按0—54、55—115分段，未依赖摘要。没有核听、产品事实验证或独立评审。

逐项：G01为主观减压动机；G02是假设断供下明确背景声音需求，不推音乐唯一；G03常用歌单shuffle/整单repeat方式保留，非全时固定；G04情绪搜索；G05构想与灵感意图保留，含混转写shopping不擅改；G06片段到整曲及相似发现有用途支持；G07由喜欢理由与不可缺维持个性化，不将自估命中比例写成KPI；G08睡眠timer为喜欢且有目的的现有能力；G09社交共享不因已实现过滤，竞争产品历史判断不认证；G10 ambient不可缺明确维持；G11普通人公共歌单首页建议保留maybe；G12具体协同推荐建议含本人对效果的不确定，不把算法不能模拟情绪当事实；G13替代平台缺混音情境仅作推断。播客、偶尔应朋友请求查看歌单为旁支使用情境，未升级为新的强制产品功能；已由G09和内容选择承接其相关性。

F01 proposed/partial：这些渠道可能贡献新歌发现，但不保证查到给定片段完整歌曲，也未说明三个渠道必需共同使用。未按70/15/15比例建立优先等级，访谈中的other50%口误不作精确统计。没有制造抽象满意度根节点。已考虑G01/G02：声音背景可在主观上帮助减压，因未证充分性不画边。G03/G07/G10为不可缺功能并列，不等于共同足以实现全部流媒体需求。

正常场景（分析假设）：心情平常时选熟悉歌单shuffle并循环，个性化推荐可增发现；G03/G07可同时满足。异常场景（分析假设）：特定混音缺失则走YouTube Music，G13不等同主要平台覆盖全部曲库。异常场景（分析假设）：无音乐服务可用仍放电影/电台，支持G02但未证明减压效果。边界场景（分析假设）：相近用户歌单仍不喜欢，不能据此把G12当已成立充分方案。

全文搜索范围中本人对Spotify整体满意；广告是免费用户的转述抱怨，未给本人创造避广告新增目标。未决推荐关系、计时范围保留，人审pending。冻结工具进行实际绑定和检查，结构检查不证明语义；独立语义与形式证明not_run。
'''
save(DOC,g,f,q,r,[{'target_type':'group','target_id':'DOC005-F01','message':'发现渠道是贡献或建议，不能证明共同充分；需澄清方案关系。'}])
