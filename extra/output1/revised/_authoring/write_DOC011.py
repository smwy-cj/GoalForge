from pathlib import Path
exec(Path('output1/revised/_authoring/batch1_helpers.py').read_text(encoding='utf-8-sig'))
DOC='DOC011'
g=[
goal(1,'direct','与课程队友异步协作修改代码，完成团队课程开发',23,"we are asynchronous collab, asynchronously collaborating on this code. We're making changes and such to get a get through of our course work.",'本人直接说明学生角色主要目的，真实项目不能同场工作进一步支持异步方式。',['学生团队情境；独立开发者无需固定使用PR。'],extra=[(101,'we had a very difficult time finding work session like creating work sessions to collaborate with each other in person.')]),
goal(2,'direct','通过他人审查后再合并，保护主仓库免受未经审查的未知代码变更',83,"it's a great way to make sure that the main repository stays safe from unknown code changes before they are reviewed by others.",'明确保护结果与审查方式，已实现也含继续使用动机；不承诺审查后绝无缺陷。',['协作项目，审查按团队或审阅者标准可批准或拒绝。']),
goal(3,'direct','合作时互相审查提交，使进入主分支的代码达到团队质量标准',107,'I want to ensure that I review their code. If I am collaborating someone else\'s code. They review my code.','明确互审意图，G02强调避免未审，G03强调质量和互相角色，不混淆保证。',['提交可因未达标准被拒；个人项目通常不使用PR。'],extra=[(31,'the code, is up to standard of the team or their personal standard')]),
goal(4,'direct','在PR标题与描述中说明代码变更的上下文，供队友审查',25,'this allows me to provide context for my code changes for my collaborators, like my teammates, to review.','动作含明确审阅目的，保留PR标题描述的方式。'),
goal(5,'direct','团队协作时偏好增量提交，降低每次审查内容量并保持流程顺畅',45,'It provides less content for my collaborators to have to review. and it keeps a more flowing process.','明确个人偏好，不将小PR变全体要求；独立项目反例保留。',['团队协作个人偏好；独立开发通常不用PR，假如用也可更大。'],extra=[(43,'I personally prefer to do it incrementally'),(45,"I wouldn't even use pull requests, in the 1st place, because I don't have any collaborators except for myself.")]),
goal(6,'direct','通过项目看板规划开发、记录待办并讨论分派团队任务与审阅工作',59,'we would meet together as a team. discuss who should be assigned, what?','既有工作方式含团队分配目的，保留backlog初始未分配和会议协商。',['看板可记录要求、变更大小频率及谁审哪个PR；不是软件自动替团队分派责任。'],extra=[(53,"you can facilitate team management that way. You can decide requirements. How big of changes to be made. how frequent"),(55,'We have our backlog, and we would just simply make an issue in that backlog.')]),
goal(7,'direct','将PR关联看板问题，合并时让看板自动反映完成情况',69,'when that port request is merged, the Kanban board would automatically reflect that.','明确便利用途与关联方式；保留仓库和project关联的前置条件。',['项目看板须已关联相应仓库；resolves加问题编号是本人示例。'],extra=[(67,'You just have to make sure that the canva board the project is actually linked to the repository')]),
goal(8,'direct','方便且安全地在云端保存代码，在本机损坏或遗失后可取回到另一机器继续工作',75,'Were my machine to go corrupt, were it to be lost, I would still have my work in a cloud environment that I could simply I\'m gonna use the keyword pull onto a different machine and continue working on my code base.','明确避免丢失和恢复结果，保留云端/pull方式；未扩为自动备份或实时同步。',['同步需手工pull/push；未上传的本地变化不在已云存代码范围。'],extra=[(15,"It's not automatically synced.")]),
goal(9,'direct','能回看保留的PR及其变更，追踪仓库和协作者的历史',83,"It's also a very convenient way to track history.",'已有能力的历史用途明确，不因现状而删除维持意图。',['不是所有历史关系已被当前线性视图清楚表达，G12另含可视化建议。']),
goal(10,'direct','作为助教查看学生项目代码并了解他们的进展',17,'so I can monitor my students code and actually look through and see how they\'re doing on their in their projects.','明确角色目的，未附自动评分或监控指标。'),
goal(11,'direct','更容易找到指导构建Actions工作流的资料，可考虑论坛或博客讨论入口',85,'So if they. Could have a forum or such, or like a a blog, tab forward discussions or information on building these action workflows. It\'d be great.','明确建议，文档难找为背景；未认证产品无论坛或文档缺陷客观事实。',['论坛/博客为可考虑方式，未指定唯一实现。']),
goal(12,'direct','可取但非必需地将分支创建、合并和相关问题按时间可视化，以理解仓库上下文',87,'For this to visually see there was new branches made where they were merged in and within those branches like see issues with like their corresponding timeline.','显式nice to have，保留可视化方式和历史关系，不强化为必需。',['非必要功能，仅便利；既有带时间戳线性提交历史仍可查看。'],extra=[(87,"It's it's not an essential feature, it's more so. Just like convenience.")]),
goal(13,'direct','可以考虑集成AI咨询助手，帮助利用GitHub已有资源并指导创建PR或Actions文件',93,'an assistant to allow users to consult with it to have better to use all the resources available on Github.','直接提出集成建议；后续给出指导PR与action文件实例。',['建议采纳和产品当前有无同类能力未知。'],extra=[(97,'an assistant to guide me through. maybe making a pull request')]),
goal(14,'direct','独立开发时希望AI辅助代码审查并提供可参考的额外反馈',97,'an AI assistant or something that would review help me with code reviews, provide suggestions. I have another source of feedback that I can incorporate','直接期望额外反馈，未替代所有人类审查或保证代码正确。',['个人自审视角有限；AI是额外来源。']),
goal(15,'inferred','按需要将远端最新代码拉到本地并上传自己的更新',15,'you would have to manually synchronize it by running commands, such as get pull','同步方式属现状；结合学生/独立开发主要拉推用途推断继续可同步的目标，而不要求自动。',origin='inferred',reason='课程和个人代码工作都以推拉代码为主要用途，正面支持维持手动同步能力；未把技术解释等同明确新增要求。',assumptions=['主要使用用途体现继续使用此能力的意图。'],extra=[(17,"I'm only really using it to pull code and push code")])]
# 每项support由作者独立确定。
f=[group(1,1,[3,4,6,7],101,'We set up our project boards to make issues to plan out the development process.','真实项目说明看板、PR、互审帮助异步工作，但未证明这些子目标共同足以完成课程开发；还需实际实现代码、访问与课程条件。保留部分候选。')]
q=[question([2,3,14],'团队对必须审阅、质量标准及AI反馈的接受界限是什么？','本人描述标准但未给完整验收准则，AI不能自动等同队友审批。'),question([8,15],'哪些代码需要云端保留，何时推送及如何确认已保存？','手动同步意味着尚未推送的变化可能无法恢复。')]
r='''# DOC011 生成方语义自检

完整读取 T000—T110（111轮），分0—59和60—110，包含术语澄清、界面过程、真实iOS团队场景及个人例外。未核听或核验GitHub现状。本记录为同一作者自检。

G01异步协作完成课程直接；G02他审后合并保护免未知变更直接，非无缺陷保证；G03互审与团队标准直接；G04 PR上下文直接且保留标题描述方式；G05增量偏好只用于协作，独立时大PR或不用PR的反例在条件；G06看板待办与协商分派直接，不赋软件决策责任；G07关联issue后合并自动更新有前置项目关联；G08云存/换机器恢复直接，未造自动同步；G09历史回看为明确既有用途；G10助教了解学生进展直接；G11论坛/博客资料入口为建议，文档难找不转成唯一设计；G12视觉历史是非必要便利；G13集成咨询与流程指导是建议；G14 AI额外审查反馈是建议，不作人审替代；G15同步原文主要现状，依反复工作用途推断维持，支持inferred独立选择。

F01 proposed/partial：真实项目报告这些机制帮助异步协作，但不能推出共同充分完成全部课程开发。也考虑过G02/G03/G04：上下文和互审有助质量，标准未知且不存在零缺陷保证，不建立充分组。PR保留历史并非可视化时间线的完整替代，两者不画OR。未把菜单/检索各类实体、branch解释、actions已有测试能力自动全部提为需求；公共代码查询只有功能介绍而未明确使用目的，保留证据背景而无新增维持断言。

正常场景（分析假设）：队员错开工作，issue分派、各自PR、互审合并，看板更新；验证G01各机制方向，未证明课程成果质量全满足。异常场景（分析假设）：个人代码尚未push即机器损坏，G08只覆盖已云存代码，需同步问题澄清。异常场景（分析假设）：AI建议漏掉严重缺陷，G14满足仍不保证G03质量。边界场景（分析假设）：独立开发直接大批提交，无同伴互审；不把团队增量偏好强加此情境。

未将本人认为GitHub涵盖竞争产品全部能力的信念当事实；替代平台只是失去服务的策略，不作完整OR。问题保留，人审pending；未进行独立语义审查/形式证明。工程结果以冻结工具实际inspect为准。
'''
save(DOC,g,f,q,r,[{'target_type':'group','target_id':'DOC011-F01','message':'实际案例证明贡献而未证明整组足以完成课程开发；候选保持partial。'}])
