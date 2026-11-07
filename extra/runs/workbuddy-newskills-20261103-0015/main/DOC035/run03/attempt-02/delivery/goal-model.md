# 目标模型

版本：v1。人工待审。

- Get the news of an event within a couple of days of the event happening
  适用条件：For events that have just happened；Timing matters for personal interests in fast-moving technology and politics
- Receive all breaking news of the day by the end of the day, instead of 4 days later when already read or heard
  适用条件：Importance rated 9 on a 0 to 10 scale；Applies to the web application or application used to read news
- Have article content that is small but comprehensive, covering every aspect of the event
  适用条件：For at least some articles；So that a roughly thousand-word article need not be read in limited time；Short and comprehensive are required together, not as alternatives
- Have no ads on the news page and a reading experience not hammered by unnecessary ads
  适用条件：Ads that cover content make the article difficult to read
- Avoid excessive/spam notifications that lead to missing important news
  适用条件：Notifications from news websites and applications；Missing important news is the stated consequence to be avoided
- Present a notification with just the headline on top, plus the article image on the left if there is one, plus a few words of the preface if written
  适用条件：Image is included only if the article has one；Preface words are included only if a preface was written；Purpose is to catch interest so the article is read from the notification
- Receive news updates via notifications tailored to my reading behavior and interests (preferred channel)
  适用条件：Stated preference (great channel), not a mandatory requirement；Applies when using mobile news applications/portals
- Receive news recommendations curated to my habits and interests (best-liked feature and a reason to choose a platform)
  适用条件：Explicit preference (big fan / best feature), not upgraded to a mandatory requirement；Recommendations are based on searches and Google App activity
- Have a feature to disable a topic/event so less related news is shown
  适用条件：Analogous to Instagram seeing less of certain reels/posts
- Still show breaking news for a disabled topic/event, but not its in-depth articles or analysis
  适用条件：Applies when a topic/event has been disabled via G009；This is the stated caveat/exception to the disable-topic feature
- Have user-defined topic buckets to group multiple news articles and later read all articles of a chosen topic
  适用条件：Like Pinterest / Google Images topic buckets；In addition to existing archive/bookmark features, not replacing them
- Share news articles directly via WhatsApp (auto-opening the WhatsApp link), as the best way to share
  适用条件：Stated preference (the best way), not a mandatory requirement；Current alternative is copying the link into chat applications
- Have a news aggregation feature provide all relevant information matched to my interests in a short time, not a lot of news
  适用条件：Stated as the success criterion of a news aggregation feature (collecting news into a single view)
- Navigate from the homepage to articles to related/similar articles without getting confused
  适用条件：Navigation includes articles similar to the one just read and articles previously read；A reason to choose one news platform over another
- Have a user-friendly, intuitive UI so actions need no thought and news reading is smoother
  适用条件：An unintuitive UI would make me choose another news platform；Purpose is a smoother news reading experience
- See multiple sources and different stances for the same news, not only one source or one side
- Have news sources cited so the origin of the news is visible
- The company should not be able to store all the data I have been looking at
  适用条件：Data privacy concern
- News-publishing companies should not use my data to push their own agenda or propaganda
  适用条件：Data privacy concern；Concerns the companies publishing the news
- Limit use of my data to recommendation systems as the only acceptable scope
  适用条件：The only limit the stakeholder is convinced to go to considering data privacy
- Avoid an automated news curation system using knowledge of my interests to push an agenda on me
  适用条件：Expressed as a very serious concern with may/might (belief, not established fact)；Related to but not identical with recommendation features
- Have news content available on topics I am interested in: technology (devices, AI models, companies, layoffs), sports (F1, cricket), and Indian and American politics
  适用条件：Stated interests/preferences, not a mandatory content filter；Mentioned as found in recommendations or headlines
- Stick to headlines only whenever I don't have time
  适用条件：Conditional on not having time；Described as part of the usual reading process
- Use Google News as the preferred platform for reading news
  适用条件：Stated preference, not a mandate or an exclusive requirement

## 需要确认

- 原文尚不足以支持这项目标，或存在相反证据。
- T035 关于聚合功能成功标准的原句多处破碎（it should provide a law、Make a deem），not a lot 与 all the relevant information 的关系及验收判据需回原文确认；本轮按支持不足如实保留，未升级。
- T029 对自动策展系统推议程的表述使用 may/might，是顾虑/信念而非已证实事实；请确认是否应作为明确的避免型需求，以及其与偏好推荐并存的条件差异。
- T011/T039 对来源被引用、多来源多立场是现状功能的正面评价，未出现 should/must；请确认将其作为推断的维持意图是否恰当。
- T011/T039 对来源被引用、多来源多立场是现状功能的正面评价，未出现 should/must；请确认将其作为推断的维持意图是否恰当。
- T007 列出的技术/体育/政治兴趣类别属于口味背景，是否应作为推荐系统的内容范围条件而非独立目标，需确认。
- T041 的 caveat（被禁用话题仍显示突发新闻、不显示深度文章）已拆为独立目标并保留例外方向；请确认拆分粒度与例外是否完整传递。
- T041 的 caveat（被禁用话题仍显示突发新闻、不显示深度文章）已拆为独立目标并保留例外方向；请确认拆分粒度与例外是否完整传递。
- 整篇为需求获取访谈，多处为现状流程、寒暄与偏好描述；本轮对纯现状/寒暄窗口不另造目标，请确认提取范围与口径。
- 原文未出现明确的具体化/实现方式/贡献/过程先后关系原句（多为同主题并列、操作先后、偏好张力或条件例外），本轮不建立独立 relations 与 AND 精化组；请确认该建模判断是否恰当、是否遗漏可成立的联系方式。
- 聚合功能成功标准原句破碎，需回原文确认 not a lot 与 all the relevant information 的关系及验收判据，再决定是否收窄表述或补充依据；当前按 insufficient 保留。
- 原文为英文访谈转写，含大量重复、自我修正与破碎语句（如 T035 的 it should provide a law / Make a deem、T019/T033/T045 仅语气词），按原样保留未润色，不静默纠正。
- 未联网、未读取任何参考答案、历史目标、关系或评分；仅使用本任务目录的原文与冻结技能只读目录。
- 本任务为同一任务的续跑 attempt-02，从原文重新开始；未参考被外部中断的前一 attempt 产物（本目录初始仅有 brief.md 与 source/DOC035.json）。
- 转写中的 news caution system (T028)、automated use curation (T029)、a law (T035) 等按原音转写理解，未作拼写或同音纠正。
- 语义判断、独立联系与精化组判断由本生成会话编制；未执行独立语义评审或形式证明，人工接受状态保持待审。

原文与层级依据可在 HTML 中展开。结构检查不等于语义证明，意见导出后交回助手。
