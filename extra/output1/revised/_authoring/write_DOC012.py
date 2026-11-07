from pathlib import Path
exec(Path('output1/revised/_authoring/batch1_helpers.py').read_text(encoding='utf-8-sig'))
DOC='DOC012'
g=[
goal(1,'direct','按课程要求在截止前通过指定平台提交作业',27,'I submitted. Like before the due date.','结合课程责任与提交描述直接支持按时提交，未将约10次/周变验收指标。',['平台由教师偏好和作业类型决定；可能Canvas取题、Gradescope提交或外站取题。'],extra=[(45,"that's the work I need to do for my course."),(49,"it depends on the Professor's preference, and also based on the nature of the assignment.")]),
goal(2,'direct','提交前取得并查看作业说明，知道要做什么',31,'I will open the description for that assignment and fetch the information that I need to do the assignment','有明确完成作业目的的取题行为；不等于所有说明都在提交平台。',['题目可能是PDF、页面或与成绩页面共用入口。']),
goal(3,'direct','按作业所需类型上传文档，或从GitHub提取最新提交来交代码',31,'I will use the feature in the grade school to fetch my latest commit from the Github and submit the my code base','保留本人代码来源方式；PDF等文档使用文件上传。',['具体方式依文件类型；不是所有作业都要求仓库。'],extra=[(31,"if it's a Pdf report, then I will just upload the file using the file uploaded")]),
goal(4,'direct','代码提交后尽快看到构建和自动评分结果，并理解它不是最终成绩',31,'I will know my grade immediately. But that is not a final grade.','现有自动评分与知晓成绩用途明确；不把即时分等同最终评分。'),
goal(5,'direct','查看教师或助教对所交作业的评语，以了解可以改进之处',33,'So I can get some more detail like information, for where I can improve.','目的明确；评语查看作为维持目标，来源教授/助教。',['已评分后回到对应作业页或详细文档视图。'],extra=[(35,"It's the Professor, or Tas.")]),
goal(6,'inferred','更容易识别每条反馈针对作业的哪一部分',61,'I need to find really hard, like what the comment or feedback is related to which part of my assignment','由反馈全局放置导致找对应位置困难推断改善意图；未将猜测教师不熟悉软件当事实。',origin='inferred',reason='反馈目的是改进，难以关联具体部分被本人列为障碍，因此推断希望关联更明确。',assumptions=['所述困难是希望改善的体验。']),
goal(7,'direct','通过评分rubric中的分项成绩了解哪些部分做得好、哪些不足',59,'what part of your assignment received better grade like a subgrade. And what part of it is not as good.','既有rubric被明确称为有帮助的间接反馈，支持维持。',['关于两平台是否有rubric是本人猜测，未认证差异。']),
goal(8,'direct','参考当前已评分作业的估计总成绩，决定课程投入时间及是否争取额外学分',59,'can be helpful to decide like how much time you are going to spend on the course, and whether or not you are going to try an extra extra credit','明确估分用途，估计不变成最终成绩保证。'),
goal(9,'inferred','对疑似不适用的评语或扣分能方便地申请复核并解释问题',61,'I can submit a recreate request whenever I think. Oh, maybe that comment is wrong or not applicable to my assignment','本人已有复核用途与另一平台不便导致放弃共同支持方便复核意图；不保证申请必然加分。',['取决于教师通信渠道；Slack便利，可能只能邮件。'],origin='inferred',reason='明确使用复核请求并因额外通信不便放弃，支持减少复核成本，但未直接要求某平台唯一实现。',assumptions=['希望可以实际表达评分异议而非仅描述能力差异。']),
goal(10,'inferred','更容易找到作业说明、提交入口和成绩信息，减少入口安排带来的混淆',55,'that can sometimes be confusing, because you need to go to see your grade, to pick up your assignment.','由入口混淆和实际取题目的推断可发现性改善，不要求统一所有课程组织方式。',origin='inferred',reason='需要取题却被成绩入口混淆，说明希望更明确导航；具体方案未提出。',assumptions=['混淆是希望减少的障碍。']),
goal(11,'direct','在骑车、跑步或做饭等期间通过视频或音乐获得娱乐、打发时间',82,'I I want to be able to be entertained as I run or or go on the bike','后半采访对象明确娱乐目的，T128认可总结包含驾驶/做饭。',['驾驶中原文为听预下载内容，未要求看屏。'],extra=[(118,"I'll just listen to it as I drive.")]),
goal(12,'direct','在健身房使用耳机听内容，以免打扰其他人',90,"plugged in like my headphones because I don't want to disturb anyone else at the gym",'明确避免影响他人的目的，保留耳机方式。'),
goal(13,'direct','找到符合当前兴趣、心情与精力的内容观看或收听',96,"Well, it's how I feel at the time.",'本人解释选择因素，困难数学只在精神好时、轻松内容随时及想学主题。',['难数学内容需较休息好；可按游戏、地理、历史等当前兴趣选择。'],extra=[(96,'Then I would pick a video that caters to that.')]),
goal(14,'direct','将感兴趣但当时不想看的视频保存至稍后观看，并在需要时取用',92,"if I see one that I want to watch, but not at the moment. I'll put it in the watch later.",'现有功能有明确延后观看与找不到当前推荐时回退用途，支持维持。'),
goal(15,'direct','持续获得足够多样且贴合个人兴趣的视频推荐，容易找到下一段想看的内容',114,"it's easy for me to find a new thing that I want to watch",'对数量、多样和长期个性推荐的偏好有实际不换平台理由；不是无限推荐必须保证命中。',['不合意可到稍后观看或按兴趣搜索；推荐不总成功。'],extra=[(114,'Youtube has the quantity of videos that you want. And it has, like the diversity.'),(116,"That's a big part of it. Yeah.")]),
goal(16,'direct','推荐不合意时通过稍后观看或搜索感兴趣主题找到想看的视频',104,'I solve that by usually going to the watch later. or if not, then I like, I would think about something that I\'m interested in and try and find a video on that','明确回退策略与目标，不假定推荐、搜索等各自都足以保证找到好视频。'),
goal(17,'direct','按可用时间挑选独立可跳看的视频，通常填满剩余骑车时间或选约10至30分钟',98,"I would aim for like filling exactly that time, if not like a 10 to 30. Minute video is like a safe bet for me",'明确时间匹配偏好，T114独立次序和注意力解释；保留更长和退出例外。',['通常不来YouTube看极短Shorts；相对连续剧更喜欢较短非虚构独立内容；时间充足可选40分钟或一小时，不喜欢可退出。'],extra=[(114,'I\'d rather have a bunch of stuff that I can just watch out of order, or watch in whatever order I want, or skip')]),
goal(18,'direct','长途出行前利用良好Wi-Fi预下载视频，以便途中收听和填补时间',118,"if I'm going on a long trip. and I have, like really good Wi-fi beforehand. I'll download like 10Â h worth of videos or something",'下载是明确本人选定方式和出行目的，10小时为例示，不强制容量。',['途中以听为主；缓冲本人认为是其他因素，不已证为应用故障。']),
goal(19,'direct','希望评论区内容更有质量，可考虑评论前的基础测试等门槛',110,'maybe if they had like, an IQ test, or even just like like, just sort of basic any sort of basic test before people were allowed to comment.','保留受访者提出的方法建议与maybe强度，不代为认同测验效果或其对评论者的评价。',['本人少评论，主要为阅读体验；也举清醒程度/酒精测试为例，实际适用与有效性未知。'],extra=[(110,'or like a sobriety test. Even so, you have to like take a breathalyzer or something before you leave a comment')]),
goal(20,'direct','希望内容分类更贴合自己划分兴趣的方式，以便找到想看的内容',126,'I would divide the content like differently. So it would be easier for me to watch','明确分类改进目的，保留个人兴趣分法而不普遍要求全部用户同一体系。',['所举音乐类别、桌游、数学等为例；网页与手机音乐使用场景不同。']),
goal(21,'direct','想重听音乐时可搜索目标歌曲或从最近收听记录快速再次播放',98,'it gives you a history of like the most recent stuff you listen to in case you want to start watching, listening to it again.','现有历史记录有重听目的，搜索为本人使用方式；不要求永久历史或增加隐私数据。')]
for x in g:
    n=int(x['candidate_id'][-2:]);x['actor']='前半受访者（源speaker=Stakeholder）' if n<=10 else '后半受访者（源speaker=Interviewer）'
f=[group(1,5,[6,7],59,'So you can see a detailed decomposition of your assignment like grading','反馈定位和rubric可帮助改进，但即使得到两者也未必理解全部改进点，内容质量和教师解释未知；整组部分。'),group(2,13,[14,15,16],104,"Sometimes I don't. There's no videos I really want to watch.",'推荐、保存和搜索是发现渠道与回退策略，并不共同保证匹配当前兴趣精力；不能由顺序产生充分精化。')]
q=[question([6,9,10],'课程允许怎样的复核方式，反馈能否按具体作业位置关联，入口能如何组织？','教师设置与平台组织造成局部障碍，所需改善边界未定。'),question([19],'评论前测试建议的具体目标、适用范围和有效性如何判断？','为个人建议，测试未被证为改善评论质量的充分方案。'),question([20],'希望哪些分类可自行定义，哪些可继续由推荐系统提供？','本人不同于当前分法，未给完整分类体系。')]
r='''# DOC012 生成方语义自检

完整读 T000—T141 共142轮，按0—59、60—109、110—141分段。注意T077后双方交换采访角色：G01—10主体为原speaker Stakeholder，G11—21主体为原speaker Interviewer，未按静态speaker标签误认后半回答为采访者建议。开场录制、末尾交作业讨论读入但不是自动当产品要求。未核听或验证平台事实。

逐目标：G01按课程指定及期限；G02取题说明；G03文档上传/最新GitHub提交；G04即时自动分非最终；G05教师/助教评语为改进；G06对应位置困难推断易关联，教师不熟悉只是猜测；G07rubric分项反馈用途，平台是否有是猜测；G08估分用于投入和额外学分；G09复核从不便放弃的正面动机推断；G10导航混淆推断改善，非强制统一课程结构。G11后半娱乐填时且驾驶为听；G12耳机不扰人；G13按心情精力兴趣；G14保存后看；G15推荐数量多样及个性化为留用理由；G16回退搜索/列表方式；G17剩余时间与独立观看偏好，允许长视频和退出；G18离线预下载方式，10小时例示；G19保留有争议测试建议的maybe及有效性未知，不替其强化或净化；G20个人分类方式；G21音乐搜索/最近记录重听用途。

F01/F02全组核验为proposed/partial：反馈机制不保证理解改进，发现机制不保证想看内容。未把不同作业文件类型或不同平台画完整OR（课程指定决定，非任意可替代）；未将推荐→列表→搜索先后画成立层级；未将两位受访者目标合成一个“满意用户”根。

正常场景（分析假设）：按课要求上传PDF或提取已推GitHub代码，自动分仅初步，再读教师定位评语及rubric；G01—07条件一致，不构成成绩提高保证。异常场景（分析假设）：全局评语难对应且无方便复核入口，G05可部分实现但G06/G09有障碍，需课程层确认。正常场景（分析假设）：骑车剩20分钟选独立视频戴耳机看，符合G11/12/17。异常场景（分析假设）：推荐不喜欢且收藏过时，搜索也无合适内容，F02仍不足。异常场景（分析假设）：旅途网络差，预下载若可用支持听内容；未下载或下载失效的恢复未给。边界场景（分析假设）：评论测试通过者仍发低质评论，G19方法不保证结果。

遗漏/强度检查：无广告套餐是现状且未进一步说明维持意图，未自动新增强制免广告；偶看Netflix/Hulu仅背景。后半所说短内容相对连续剧，与T098不想看Shorts按情境区分，非矛盾。全部未决问题保留，人审pending；工程inspect实际执行，独立语义及形式证明not_run。
'''
save(DOC,g,f,q,r,[{'target_type':'group','target_id':'DOC012-F01','message':'反馈形式的并列不足以保证得到可用的改进理解，保留部分候选。'},{'target_type':'group','target_id':'DOC012-F02','message':'渠道与回退过程不保证内容匹配；候选不可当成立层级。'}])
