# 目标模型

版本：v1。人工待审。

- Recommend news that matches my interests and reading behaviour, delivered through search-page recommendations and app notifications.
  适用条件：interest areas as reported: technology releases and layoffs, F1 including off-season, cricket, Indian and American politics；recommendation quality is also judged by how well it follows prior searches and reading
- Deliver news of an event within a couple of days of it happening.
  适用条件：F1 news two weeks away from the race weekend is not worth reading because it has likely been read elsewhere
- Show which publication each story comes from.
  适用条件：cited sources are the stated reason the reader rates the application as best on credibility
- Let me compare the same story across multiple sources, including differing opinions.
  适用条件：comparison criteria reported: article length, publication timing, and stance taken on issues
- Curate news notifications so that they do not spam me and important news is not missed.
  适用条件：spam notifications are reported as the cause of missing important news；curation across different applications is the reader's current workaround
- Provide shorter article content that still covers every aspect of the event.
  适用条件：applies to some of the articles, not to all of them；the short version must remain comprehensive and cover every aspect
- Serve news pages without ads, so ads do not cover the article content.
- Compose notifications with the headline, the article image on the left, and a few words of the preface.
  适用条件：preface wording is optional ('can be', 'would be great')
- Share an article directly to WhatsApp by opening the WhatsApp share link automatically.
  适用条件：copying the link into chat applications is the current fallback
- Let me define my own topic buckets, add multiple articles to them, and open a bucket to read its articles later.
  适用条件：existing archive/bookmark features are acknowledged but not sufficient；reference model is self-defined buckets as in Pinterest or Google images
- Do not push an agenda or propaganda at me through automated curation or through my reading data.
  适用条件：concern applies both to automated curation that knows the interests and to publishers holding the data
- Deliver all of the day's breaking news by the end of the day.
  适用条件：breaking news alerts rated 9 out of 10 in importance
- Let me disable a topic, while still showing breaking news on that topic and hiding its in-depth articles.
  适用条件：exception: breaking news of a disabled topic is still shown；in-depth analysis of the disabled topic is not shown
- Make navigation from the homepage to an article and on to related or similar articles clear, without confusion.
  适用条件：related articles include ones similar to the current article and ones already being read
- Keep the interface intuitive so that common actions need no figuring out.
  适用条件：stated as a factor in choosing one news platform over another
- Store only limited reading data and use it only for recommendations.
  适用条件：recommendation systems are the only accepted use of the data；prohibition is on storing all of the data, not on any storage
- Give me all information relevant to my interests in a short time, without a lot of content, in a news aggregation view.
  适用条件：success is defined against the reader's own interests；volume should stay low while coverage stays complete

## 目标之间的联系

下列联系不表示充分精化；待确认及已否定记录保留各自状态。

- 有依据的联系：Recommend news that matches my interests and reading behaviour, delivered through search-page recommendations and app notifications. —[有助于]→ Give me all information relevant to my interests in a short time, without a lot of content, in a news aggregation view.
  依据：G001 让推荐贴合兴趣与阅读行为，直接支撑 G017 所定义的成功标准中“与我兴趣相关的相关信息”这一半；但不保证覆盖全部相关新闻，故只记为贡献而非充分实现。
  条件／假设：兴趣匹配的推荐覆盖了成功标准中“与我的兴趣相关”的部分
- 有依据的联系：Provide shorter article content that still covers every aspect of the event. —[有助于]→ Give me all information relevant to my interests in a short time, without a lot of content, in a news aggregation view.
  依据：G006 缩短文章并保持全面，使 G017 要求的“量不多、时间短”可得；原文明确把千字长文在有限时间内低效作为动机，故为有依据的贡献。
  条件／假设：更短但全面的文章减少了单位信息量的阅读时间
- 有依据的联系：Deliver all of the day's breaking news by the end of the day. —[范围具体化]→ Deliver news of an event within a couple of days of it happening.
  依据：G012 是 G002 在突发新闻情境下的具体目标，但时限更严（当天结束前），属于更窄情境的具体化，不声称覆盖 G002 的全部适用范围。
  条件／假设：对象限定为突发新闻（breaking news）；突发新闻属于需要及时到达的新闻事件的特例
- 有依据的联系：Curate news notifications so that they do not spam me and important news is not missed. —[有助于]→ Deliver all of the day's breaking news by the end of the day.
  依据：原文说明通知刷屏会导致错过重要新闻，故控制通知量有助于当天突发新闻被看到；只是有帮助，不保证到达。
  条件／假设：通知量受控后重要/突发新闻更不易被淹没

## 需要确认

- “within a couple of days”是否需要明确阈值（例如 48 小时或 72 小时）？
- “不应存储我看过的全部数据”的边界是什么（可保留哪些字段、保留多久）？
- “all the relevant information ... in a short amount of time”如何验收？
- 对推送议程的“严重担忧”是否应作为产品约束，而不只是顾虑记录？
- 被关闭话题的“breaking news”如何界定，是否与 G012 的当天突发新闻同一口径？
- 通知量的“不过度”是否有可核对上限（条数/频次）？
- 是否需要补充“聚合需覆盖多来源/多话题”的目标，才能主张 GR1 的共同充分性？当前原文只给出定性成功标准。
- 原文没有总体目的句，是否需要一根“高效获取个性化新闻”的根目标统领 G001/G006/G017？当前未造根，保留多根结构。
- “不要推送议程”是否与 G001 的个性化推荐存在张力（需知道兴趣才能推荐）？原文未给出取舍规则。
- G001 只是 G017 相关性部分的手段，若后续补入覆盖性目标，R1 是否应改为 operationalization？
- 这组层级仍需确认，尚未作为成立的精化展示。
- 访谈转写含重复词、断句与自我修正（如 “the the”、“I I”），引文按原样逐字保留，未作规范化。
- 仅一位受访者（Stakeholder）陈述个人偏好，未涉及其他角色、责任分配或优先级排序，目标强度按原话保留，不推断权重。
- T019、T033、T045、T049 为应答碎片，未形成独立意图；T000/T020/T034 等为采访者追问，未获独立回应处不作目标。
- 未联网、未读取任何参考实现或历史结果；目标集合只依据本文件原文。

原文与层级依据可在 HTML 中展开。结构检查不等于语义证明，意见导出后交回助手。
