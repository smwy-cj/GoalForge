# 目标模型

版本：v1。人工待审。

- Search a city subreddit with a keyword to learn about a specific local topic.
  适用条件：when wanting to learn about a particular topic
- Scroll the newsfeed of followed subreddits during idle downtime until an interesting post appears, then open and interact with it.
  适用条件：when no search target is predefined；usually during downtime such as lunch or the bus
- Use technical-help subreddits as an alternative to Stack Overflow when stuck on a problem or needing other input.
  适用条件：when stuck on a problem；when needing other input on a problem
- Get results targeted to the specific problem being faced rather than generalized search results.
- Get personal, contextual experiences from other people rather than general facts when evaluating something.
- Reach the relevant post directly through a Google search with Reddit appended, instead of searching inside Reddit, when a problem is targeted.
  适用条件：when the problem is targeted
- Solve a problem that was defined before logging in, so that the session ends with the problem solved.
  适用条件：the problem is defined before logging in
- Reach authentic answers quickly on Reddit for specific queries, without spending a lot of time searching.
  适用条件：for specific queries
- Ask for advice in the relevant communities when a question is better answered by others.
  适用条件：when the question is one that others can answer
- Stay updated on trends through Reddit, mainly for events tied to followed subreddits or major worldwide events on the popular page.
  适用条件：Reddit is not the primary news source；only events tied to followed subreddits or major worldwide events surface
- Keep news out of Reddit, using it to satisfy curiosity rather than as a news source.
  适用条件：news is followed on other apps
- Research products on Reddit before buying to get balanced perspectives from people of varied backgrounds, and use those reviews in purchase decisions.
  适用条件：before a purchase
- Get general health information from a community answered by healthcare professionals, such as beginner yoga routines.
  适用条件：for general, not specific, health questions
- Avoid using or recommending Reddit for specific health problems, because specifics there are not trustworthy.
  适用条件：for specific health problems
- Choose the feed view by mode of use: card view for passive scrolling and compact view to compare all relevant search results before opening one.
  适用条件：passive browsing versus active search
- Have an ad-free reading experience.
- Buy the premium tier when an ad blocker is unavailable, to remove ads.
  适用条件：only when ad blocking is unavailable
- Find the exact subreddit for a topic or question instead of searching through many overlapping subreddits.
- Add a Gen-AI tool that turns a described topic into the exact subreddit to use.
  适用条件：a Gen-AI tool is the explicitly chosen way
- Post questions in the most specific relevant subreddit so that responders who know the subject matter give better answers.
  适用条件：posting a question
- Save an unfinished post as a draft on mobile after an interruption, as is possible on desktop.
  适用条件：when a post is left mid-way
- Track comment threads clearly on mobile, comparable to the desktop view.
- Improve the mobile app UI so that the first-party app is better than third-party wrapper apps.
  适用条件：to compete with wrapper apps built on the API
- Get reliable information by relying on communities with strong moderation, including automated checks and human moderators, while accepting that nothing online is fully reliable.
  适用条件：moderation quality varies by subreddit and team size

## 目标之间的联系

下列联系不表示充分精化；待确认及已否定记录保留各自状态。

- 有依据的联系：Reach the relevant post directly through a Google search with Reddit appended, instead of searching inside Reddit, when a problem is targeted. —[实现方式]→ Get results targeted to the specific problem being faced rather than generalized search results.
  依据：T007 把'有具体问题'与'走 Google 链接'直接绑定：该入口是为定位到针对该问题的帖子，属于实现方式而非独立目的。
  条件／假设：when the problem is already articulated as a query
- 有依据的联系：Use technical-help subreddits as an alternative to Stack Overflow when stuck on a problem or needing other input. —[范围具体化]→ Solve a problem that was defined before logging in, so that the session ends with the problem solved.
  依据：T003 说明技术类 subreddit 用于卡住或需要额外输入时；T009 说明预先定义问题的会话结果是问题被解决，属具体情境对一般目标的细化。
  条件／假设：the problem is technical and the user is stuck；technical help is still aimed at solving that problem
- 有依据的联系：Search a city subreddit with a keyword to learn about a specific local topic. —[实现方式]→ Get results targeted to the specific problem being faced rather than generalized search results.
  依据：T003 的按关键词搜索城市 subreddit 是把结果限定到具体话题的一种做法；T005 说明使用 Reddit 的目的是得到针对问题的结果。
  条件／假设：a subreddit matching the topic exists
- 有依据的联系：Add a Gen-AI tool that turns a described topic into the exact subreddit to use. —[实现方式]→ Find the exact subreddit for a topic or question instead of searching through many overlapping subreddits.
  依据：T059 明确说会实现 Gen-AI 工具来找具体 subreddit；T051 描述其行为是输入主题给出确切 subreddit，直接服务于'找到确切 subreddit'。
- 有依据的联系：Find the exact subreddit for a topic or question instead of searching through many overlapping subreddits. —[有助于]→ Post questions in the most specific relevant subreddit so that responders who know the subject matter give better answers.
  依据：T059 把'发在具体 subreddit 更有价值'与'找到该 subreddit 很有用'连在一起：找到正确 subreddit 有助于把问题发到那里，但不保证回答质量。
  条件／假设：the found subreddit matches the question topic；that subreddit still has active respondents

## 需要确认

- C012（浏览中读到感兴趣内容后继续在 Reddit 深挖）以 'might be' 描述可能结果，未建为独立目标；是否需要补充？
- 移动端改进目标（G023）是否需要明确必须解决的缺陷范围（草稿、评论串、性能、直观性）？
- 关系判断已逐对执行：只建立 5 条有明确原句依据的联系（R1-R5）。其余组合经检查不成立：G002 与 G007 是同一用户两种互斥使用模式（无预设目标 vs 有预设问题），非具体化或贡献；G005 与 G012 是信息质量与购前调研的同主题重叠，无实现或贡献原句；G010 与 G011 是趋势与新闻的边界划分，方向相反而非帮助；G016 与 G017 是同一偏好与其条件化行动，G017 已含条件，不再另建边。
- 精化组判断已执行：只保留 GR1（proposed/partial）。检查过但未建组：G004+G005+G008 缺少'比 Google 更有价值'的父目标（原文是比较性信念，不是目标，造父目标会违反不凑层级）；G018+G020 已是单一目的-手段链，二者不构成共同满足另一父目标；G021+G022 归入 GR1 而不单独立组。
- 移动端体验是否只由草稿保存与评论串跟踪两项构成？原文另有缓慢、笨重、不直观等抱怨，本组因此只作部分覆盖，待确认完整子目标集合。
- 无预设目标的浏览被受访者描述为 'no particular outcome'，现保留为'填充空闲时间'的意图；是否应作为目标而非背景行为，请确认。
- 新闻与趋势的边界（关注 subreddit 内事件、popular 页全球事件 vs 其它新闻）是否稳定？当前按原文保留为条件，未与 G010 合并。
- 这组层级仍需确认，尚未作为成立的精化展示。
- 转写稿有识别噪声（Reddit 被写作 credit/edit，'I've never posted something on reddit' 与后文 'posts that I've done' 矛盾）；发帖量仅作背景，不影响目标判断。
- 受访者为单一用户，结论仅覆盖其个人使用情境，不代表全体用户。
- 原文未给出数量化阈值（如查找时长上限、错误率），目标中未编造阈值。

原文与层级依据可在 HTML 中展开。结构检查不等于语义证明，意见导出后交回助手。
