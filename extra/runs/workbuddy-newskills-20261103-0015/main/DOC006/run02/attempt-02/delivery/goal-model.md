# 目标模型

版本：v1。人工待审。

- Browse news and general daily information on the social network web application.
  适用条件：Used daily; general feed scrolling counts as this browsing
- Avoid missing important information such as major international events and new job postings.
  适用条件：The stakeholder treats the platform as the place where such information should surface
- Search for job posting information on the platform.
  适用条件：Occasional rather than daily use
- Recommend content from the user's recorded likes, comments and browsing history so that the recommendations fit the user's taste.
  适用条件：The stakeholder calls this a necessary feature for social applications；Recommendations are expected to keep pushing the latest matching information
- Show how many people are already in the hiring process for a job so the user can judge whether the company is hiring in large numbers.
- Show feedback from people who recently interviewed at the company so the user can judge how demanding the interview is.
- Provide a specific button or feature that restricts a search to a specific region such as a city.
  适用条件：Needed for region-bound listings such as house rentals；Current platforms return results randomly with no region filter, which filters out useful postings
- Filter entertainment content out of the results when the user is searching for useful content such as jobs or housing.
  适用条件：Conditional: only when the user does not want to see entertainment content
- Push light entertainment content such as daily jokes to the user.
  适用条件：Soft preference ('maybe'), not a firm requirement；On this application entertainment arrives as photos and texts
- Improve the company's data management so that user data is not sold to other parties.
  适用条件：Framed conditionally: what the company could do if it chose to address the issue ('might just')；The stakeholder otherwise tolerates data leakage and says it does not affect his experience
- Strengthen handling of matrix accounts so that duplicate marketing content stops flooding the feed and degrading the user experience.
  适用条件：Addressed to the platform development team；Should-level requirement

## 目标之间的联系

下列联系不表示充分精化；待确认及已否定记录保留各自状态。

- 有依据的联系：Browse news and general daily information on the social network web application. —[实现方式]→ Avoid missing important information such as major international events and new job postings.
  依据：新闻/日常信息浏览是受访者用来避免遗漏重要信息的主要手段：T003 在被问 'why do you think [information browsing] is important' 时直接给出不想遗漏的回答。方式→目的方向。
- 有依据的联系：Search for job posting information on the platform. —[实现方式]→ Avoid missing important information such as major international events and new job postings.
  依据：职位检索被视为获取同一类不可遗漏信息的手段：T003 把新的职位发布列为不想遗漏的信息，而 T001 的职位搜索正是获取它的方式。
- 有依据的联系：Recommend content from the user's recorded likes, comments and browsing history so that the recommendations fit the user's taste. —[有助于]→ Search for job posting information on the platform.
  依据：受访者明确说职位列表问题较少，因为 AI 推荐会推送合适的职位；个性化推荐帮助（不保证充分）职位检索目标。
- 有依据的联系：Filter entertainment content out of the results when the user is searching for useful content such as jobs or housing. —[有助于]→ Search for job posting information on the platform.
  依据：受访者说做职位/房产搜索时平台把娱乐和有用内容混在一起推送，过滤娱乐内容有助于检索到有用内容；仅为帮助关系，不代表充分实现。
  条件／假设：When searching for useful content such as jobs or housing
- 待确认联系：Strengthen handling of matrix accounts so that duplicate marketing content stops flooding the feed and degrading the user experience. —[有助于]→ Browse news and general daily information on the social network web application.
  依据：原文只说矩阵账号刷屏 'interferes with user experience'，未点名新闻浏览目标，故只作待确认的帮助关系。
  条件／假设：信息流刷屏主要影响新闻/信息浏览体验

## 需要确认

- T003 末句 'I can't get the 1st information from social web applications' 转写可疑（可能为 'can get the first-hand information'），是否影响 G002 的强度判断？
- 条件性公司建议（'They might just improve their management'）是否足以作为目标，而非仅为一个可选项？
- 职位搜索被描述为体验良好（T021、T023），G003 是否只是现状使用而非改进需求？
- 是否应把 G001、G003 与 G004（推荐推送）组织成 '不遗漏重要信息' 的 AND 精化组？现有材料只说明多个手段，无法声称这组子目标共同充分，故未建组。
- G010 来自 'might just' 的条件性建议，且受访者多次表示对数据泄露不在意；应保留为低优先级建议还是视为非需求？
- 娱乐内容仅以 'maybe' 提及，是否需要作为稳定使用目标保留，还是仅作为 G008 过滤目标的情境背景？
- 这项联系尚待确认，不表示充分精化。
- 原文为访谈转写，存在重复词、断句与疑似识别错误（如 T003 末句、T007 的 'hardest'），仅在语义可辨处取证。
- 未取得音频或人工核对，识别置信度按转写稿处理。
- 本次为单一隔离生成会话，未做独立语义评审或人工采纳。

原文与层级依据可在 HTML 中展开。结构检查不等于语义证明，意见导出后交回助手。
