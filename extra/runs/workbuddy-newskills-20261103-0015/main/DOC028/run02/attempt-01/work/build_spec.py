# -*- coding: utf-8 -*-
"""Assemble spec.json for DOC028/run02 (author-written semantics) and verify quotes."""
import json
import re
from pathlib import Path

A = Path(__file__).resolve().parents[1]
SRC = json.loads((A / "source/DOC028.json").read_text(encoding="utf-8"))
TEXT = {t["source_id"]: t["text"] for t in SRC["turns"]}


ERRS = []


def check(sid, q):
    n = TEXT[sid].count(q)
    if n == 0:
        ERRS.append("MISSING in %s: %r" % (sid, q))
    if n > 1:
        ERRS.append("AMBIGUOUS %s (%d): %r" % (sid, n, q[:70]))
    return {"source_id": sid, "quote": q, "role": "basis"}


def ev(pairs):
    return [check(s, q) for s, q in pairs]


RAW = []


def raw(cid, statement, origin, modality, ctx, pairs, role_pairs=None):
    e = ev(pairs)
    RAW.append({"candidate_id": cid, "statement": statement, "actor": "Stakeholder",
                "modality": modality, "context": ctx, "origin": origin,
                "pass_id": "P1", "evidence": e})


raw("C001",
    "When they want to learn about a particular topic, search the relevant subreddit (e.g. the city subreddit) with a keyword to get information about it.",
    "explicit", "描述性的常规做法",
    ["topic learning, e.g. what happens during Halloween"],
    [("DOC028:T003", "So I browse my city's subreddit with keyword. Halloween, search to get information about that.")])

raw("C002",
    "Log in and scroll through the subreddits they follow just to kill time.",
    "explicit", "描述性的常规做法",
    ["no predefined time or purpose"],
    [("DOC028:T003", "So I log in just to kill some time following the subredd itself.")])

raw("C003",
    "Use technical-help or code-query subreddits when stuck on a problem or needing other input, as an alternative to Stack Overflow.",
    "explicit", "描述性的常规做法",
    ["when stuck on a problem or needing other inputs"],
    [("DOC028:T003", "I also use Reddit as an alternative for stack overflow."),
     ("DOC028:T003", "So I use those when I'm stuck on a problem or need like other inputs for a problem.")])

raw("C004",
    "There is no predefined time when they log in; usage depends on being free or needing information.",
    "explicit", "对使用时间的说明",
    [],
    [("DOC028:T003", "there's no predefined time where I log in")])

raw("C005",
    "Prefer personal experiences over facts on Reddit because those experiences are legitimate and contextual, and more valuable than a Google search.",
    "explicit", "明确的理由陈述",
    ["primary reason for using Reddit"],
    [("DOC028:T005", "I get personal experiences over facts, and these personal experiences are mostly legitimate.")])

raw("C006",
    "Get more targeted results to the problem being faced, as the one-word summary of why they use Reddit.",
    "explicit", "自我概括",
    ["same primary reason as C005"],
    [("DOC028:T005", "it's to get more targeted results to the problem that I'm facing.")])

raw("C007",
    "Learn how a new workout integrated into their routine has affected other people and what results those people have seen.",
    "explicit", "假设举例",
    ["hypothetical example introduced with let's pick an example"],
    [("DOC028:T005", "I really want to know how that workout has impacted other people, and how what kind of what kind of results they've seen from it.")])

raw("C008",
    "When searching for something specific, Google the question with 'reddit' appended and open the relevant posts directly.",
    "explicit", "明确选定的方式",
    ["specific search target"],
    [("DOC028:T007", "So I Google, the question. And then I put Reddit after that. So it gives me all the relevant posts.")])

raw("C009",
    "Open reddit.com and scroll the newsfeed until something interesting appears, then open that post and interact with it.",
    "explicit", "描述性的常规做法",
    ["when not starting from a Google search"],
    [("DOC028:T007", "I just scroll through the newsfeed till I find something that interests me, and I go into that post and interact with the post.")])

raw("C010",
    "When a problem is predefined before logging in, use Reddit so that the problem ends up being solved.",
    "explicit", "明确的预期结果",
    ["predefined problem"],
    [("DOC028:T009", "The outcome of that usage of Reddit will result in the problem being solved.")])

raw("C011",
    "When browsing without a predefined goal, read something interesting and research further on Reddit if specific questions arise.",
    "explicit", "描述性的常规做法",
    ["no predefined goal", "no particular outcome claimed for browsing"],
    [("DOC028:T009", "It's just that I just browse them to find and read something interesting.")])

raw("C012",
    "Interact with posts within communities rather than with specific users or moderators.",
    "explicit", "对互动对象的描述",
    [],
    [("DOC028:T011", "I usually interact with posts, I would say, and communities and post within communities. not specific users or moderators")])

raw("C013",
    "Belong to a wide variety of communities (grad admissions, study abroad, CS career questions, personal finance, fitness, cars, books).",
    "explicit", "对所属社区的描述",
    [],
    [("DOC028:T011", "It's a it's a very wide variety of communities.")])

raw("C014",
    "Value anonymity as Reddit's unique selling point: a post is hard to trace back to a person because only a modifiable username is visible.",
    "explicit", "对平台特性的价值判断",
    [],
    [("DOC028:T011", "I think, the USP. Of Reddit is anonymity, so it's really hard to trace a post back to the person")])

raw("C015",
    "Reddit is problem-solution oriented and not part of their daily routine; not using it would not drastically change their life or routine.",
    "explicit", "对影响程度的否定说明",
    [],
    [("DOC028:T015", "It's not part of my daily routine.")])

raw("C016",
    "Save time on specific queries by getting authentic answers much faster than Google.",
    "explicit", "明确的结果陈述",
    ["specific queries"],
    [("DOC028:T015", "It saves me time when I have specific queries, because I can get to authentic answers much faster.")])

raw("C017",
    "Interact with all posts that come on the feed because the feed is tailored to their specifications.",
    "unknown", "对现状的描述与正面评价",
    [],
    [("DOC028:T019", "So I normally interact with all the posts that come on my feed.")])

raw("C018",
    "Create a post by choosing the community first, then adding a title and a Markdown body (headings, images, video, links, polls) and adding tags where the subreddit makes them mandatory.",
    "explicit", "描述性的操作流程",
    ["some subreddits make tags mandatory"],
    [("DOC028:T021", "The 1st thing you have to choose is a community that you want to post in.")])

raw("C019",
    "Most of their own posts ask for advice in communities such as CS career questions and grad school admissions, where asking for advice is helpful.",
    "explicit", "描述性的常规做法",
    [],
    [("DOC028:T021", "So most of the posts that I've done are posts asking for advice.")])

raw("C020",
    "Comment on a post by pressing comment and either writing a new comment or replying within an existing comment thread.",
    "explicit", "描述性的操作流程",
    [],
    [("DOC028:T021", "commenting is pretty simple, like, you just go to any post that you want to interact with.")])

raw("C021",
    "Reddit posts boil down to two types: sharing information for others to draw insights from, and asking for advice or solutions.",
    "explicit", "分类说明",
    [],
    [("DOC028:T023", "But again, it just boils down to whether are you sharing information, or are you looking for interaction to gain insights from them.")])

raw("C022",
    "Share information or experience so that others can absorb it.",
    "explicit", "分类说明",
    [],
    [("DOC028:T023", "The common trend in those posts is you sharing information that others can absorb.")])

raw("C023",
    "No time preference when searching for something specific; browsing happens during downtime such as lunch or the bus.",
    "explicit", "对使用时间的说明",
    [],
    [("DOC028:T025", "If I am, then I don't have a time preference.")])

raw("C024",
    "Keep use bounded to the downtime activity (bus, eating) rather than letting one question turn into hours of browsing.",
    "unknown", "对实际使用时长的描述",
    [],
    [("DOC028:T025", "But If I'm just doing it on the bus or while eating, it's normally restricted to that activity.")])

raw("C025",
    "The desktop platform presents no barriers.",
    "explicit", "对现状的否定说明",
    [],
    [("DOC028:T027", "I would say, on the desktop desktop platform. No.")])

raw("C026",
    "The mobile platform is slow, clunky and heavyweight and its UI is not intuitive; mobile UX/UI is a frustration.",
    "explicit", "明确的挫败陈述",
    [],
    [("DOC028:T027", "The mobile platform is quite slow and clunky, like the Ui. Is not very intuitive.")])

raw("C027",
    "Save an in-progress post as a draft on mobile when leaving it mid-way, as is possible on desktop.",
    "explicit", "明确的挫败陈述",
    ["mobile post creation"],
    [("DOC028:T027", "you can't save it as a draft which you can do on desktop. So that is something that is frustrating.")])

raw("C028",
    "Keep track of comment threads intuitively on mobile, as clearly as the desktop version does.",
    "explicit", "明确的比较性不满",
    ["mobile comment reading"],
    [("DOC028:T027", "you cannot keep track of comments intuitively on Mobile")])

raw("C029",
    "Rely on strongly moderated communities with auto-moderator bots that fact-check and alert human moderators, so that posts are reliable.",
    "explicit", "明确说明的可靠性依据",
    ["human moderators keep track of low quality or low effort posts"],
    [("DOC028:T029", "So I feel that if a community has a strong, a strong set of moderators, then the posts themselves are reliable.")])

raw("C030",
    "Acknowledges that anything found on the internet is not 100% reliable.",
    "explicit", "保留与限定",
    [],
    [("DOC028:T029", "of course, anything you find on the Internet is not 100% reliable.")])

raw("C031",
    "Use Reddit, including the news subreddit, to stay updated on trends.",
    "explicit", "明确的使用目的",
    ["trends tied to followed subreddits", "worldwide events such as the Olympics or Nobel Prize"],
    [("DOC028:T031", "So I do use reddit to stay updated on trends.")])

raw("C032",
    "Keep news out of Reddit and use other apps as the primary news source, because Reddit is used to satisfy curiosity rather than to follow news.",
    "explicit", "明确的取舍",
    [],
    [("DOC028:T031", "But I just find it more convenient to keep news out of Reddit, because it's more of a it's more to satisfy curiosity, and not for news.")])

raw("C033",
    "Worldwide events such as the Olympics or the Nobel Prize surface on Reddit's popular page.",
    "explicit", "对平台能力的描述",
    [],
    [("DOC028:T031", "So if there's something as big as Olympics or a Nobel Prize. It will show up there.")])

raw("C034",
    "Research products and services on Reddit to get a balanced perspective from people of varied backgrounds, rather than mostly positive marketplace reviews.",
    "explicit", "明确的使用目的",
    ["e.g. a laptop researched in February"],
    [("DOC028:T033", "Reddit is more of a balanced perspective, and you can also find people from varied backgrounds talking about the product.")])

raw("C035",
    "Has made many purchase decisions because of reviews seen on Reddit.",
    "explicit", "已发生的结果",
    [],
    [("DOC028:T033", "I've made a lot of purchase decisions because of reviews I've seen on Reddit.")])

raw("C036",
    "Search general health questions on Reddit, including AskDoctors where healthcare professionals answer, for topics such as beginner yoga routines.",
    "explicit", "描述性的常规做法",
    ["does not follow health communities; searches by query"],
    [("DOC028:T035", "I'd say it's good for general health, related questions.")])

raw("C037",
    "Do not rely on Reddit for specific health problems and do not recommend it to others for those.",
    "explicit", "明确的否定与不推荐",
    [],
    [("DOC028:T035", "But for specifics I've not used it, nor do I suggest anyone to use it.")])

raw("C038",
    "Does not feel a personal sense of community on Reddit and does not interact much via comments.",
    "explicit", "对自身状况的否定说明",
    [],
    [("DOC028:T037", "I, personally, don't interact much via comments.")])

raw("C039",
    "Offline mode shows the previously saved feed, posts, comments and pictures without a connection but cannot post or refresh; the capability is not comprehensive.",
    "explicit", "对现有能力的描述",
    [],
    [("DOC028:T039", "So I'd say, yes, there is an offline capability, but it's not very comprehensive.")])

raw("C040",
    "Sort feed posts by new, top, trending or rising using the filter option.",
    "explicit", "对现有功能的描述",
    [],
    [("DOC028:T041", "the filter option basically, you can sort posts by new by top by trending, rising.")])

raw("C041",
    "Prefer card view when passively scrolling and compact view when actively searching so that all relevant results are visible before choosing one.",
    "explicit", "明确的偏好",
    ["passive browsing versus active searching"],
    [("DOC028:T043", "If I'm using it actively, searching for something I prefer, like compact mode where I can see all relevant search results. Before I choose to click on one.")])

raw("C042",
    "Find the ads subtle and non-blocking, consider an ad-free experience better, and use a browser ad blocker.",
    "explicit", "明确的偏好与做法",
    ["ads stay in one location and one at a time"],
    [("DOC028:T045", "But of course, like any other app it, it is better to have an ad free experience")])

raw("C043",
    "Buy the premium tier in scenarios where ad blocking is unavailable, since removing ads is its only advantage.",
    "explicit", "有条件的意愿",
    ["ad block currently available"],
    [("DOC028:T047", "But in some scenario where ad block is not available, I would buy the premium tier.")])

raw("C044",
    "Would like to buy the premium tier sometime soon, but is fine without it while ad blocking works.",
    "explicit", "明确的意愿与保留",
    [],
    [("DOC028:T047", "I would actually buy it.")])

raw("C045",
    "Customize appearance with light/dark mode or legacy Reddit, and consider the current Reddit better from a user experience point of view.",
    "explicit", "功能描述与口味比较",
    [],
    [("DOC028:T049", "from a user experience point of view, I think the current Reddit is better.")])

raw("C046",
    "Search accuracy meets expectations, so finding something does not take long.",
    "explicit", "对现状的正面评价",
    [],
    [("DOC028:T051", "the accuracy of the search results are as expected")])

raw("C047",
    "Finding the right subreddit is complicated because anyone can create a subreddit about anything without checking whether one already exists.",
    "explicit", "障碍陈述",
    [],
    [("DOC028:T051", "So the ability to find a subreddit is quite complicated at this point")])

raw("C048",
    "Add a generative-AI tool where typing a description returns the exact subreddit needed, which would improve the experience.",
    "explicit", "明确的改进提议",
    [],
    [("DOC028:T051", "I think a feature that would improve the user experience would be where you just type in like a Gen. AI tool where you want to subreddit about Xyz, and it gives you the exact subreddit that you need.")])

raw("C049",
    "Ads hinder the experience to some extent.",
    "explicit", "障碍陈述",
    [],
    [("DOC028:T051", "I need to find something hindering, I would say the ads to some extent.")])

raw("C050",
    "Notifications are configurable and not troublesome; on the browser they only arrive while Reddit is open.",
    "explicit", "对现状的满意评价",
    [],
    [("DOC028:T053", "I don't think the notifications are too troublesome. They don't really get in the way of you doing anything.")])

raw("C051",
    "Privacy and data handling are well handled; no personal issues so far and correct protocols are assumed.",
    "explicit", "信念与现状评价",
    [],
    [("DOC028:T055", "Personally, I haven't faced any issues till now")])

raw("C052",
    "Moderation is very good, although it depends on the subreddit and the size and quality of the moderation team; no changes suggested.",
    "explicit", "满意评价",
    [],
    [("DOC028:T057", "I think the moderation is very good it does depend on the subreddit.")])

raw("C053",
    "Add a generative-AI tool to figure out which subreddit to ask a particular question in, because posting in a specific subreddit has much more value.",
    "explicit", "明确的改进提议",
    [],
    [("DOC028:T059", "So I would implement, like a geni tool to find a particular subreddit.")])

raw("C054",
    "Expect better answers when posting in a specific subreddit because responders there are expected to know the subject matter, though bad responses can never be fully eliminated.",
    "explicit", "预期结果与限定",
    [],
    [("DOC028:T061", "I think the answers I'd get would be better, because when I post in a particular subreddit, people who are responding in that subreddit are expected to know the subject matter")])

raw("C055",
    "The mobile app UI should be much better; the official app should be the best app for the platform instead of trailing third-party wrappers.",
    "explicit", "明确的改进要求",
    [],
    [("DOC028:T063", "I'd say the mobile app ui again should be much better")])

raw("C056",
    "Third-party wrapper apps built on Reddit's API having a higher market share than the official app is a problem.",
    "explicit", "问题陈述",
    [],
    [("DOC028:T063", "Those apps have a higher market share than you, so I think one thing they can improve is their mobile app.")])

raw("C057",
    "Additional features include direct messaging and trophies for login streaks.",
    "explicit", "功能清单说明",
    [],
    [("DOC028:T067", "You have like recently, there are like trophies that are announced.")])


def goal(gid, statement, ctx, pairs, label, rationale, origin="explicit", assumptions=None):
    return {"candidate_id": gid, "statement": statement, "actor": "Stakeholder",
            "context": ctx, "origin": origin, "inference": None, "evidence": ev(pairs),
            "judgment": {"label": label, "rationale": rationale,
                         "supported_parts": [], "unsupported_parts": [],
                         "assumptions": assumptions or [], "reasoning_steps": []}}


GOALS = [
    goal("G001",
         "Search a specific topic by keyword in the relevant subreddit (for example the city subreddit for Halloween) to get information about that topic.",
         ["When the user wants to learn more about a particular topic"],
         [("DOC028:T003", "So I browse my city's subreddit with keyword. Halloween, search to get information about that.")],
         "direct",
         "原句明确以关键词在相关 subreddit 搜索特定话题并取得信息，主体、对象、方式一致；例句中的 city subreddit 与 Halloween 保留为情境例，未升格为固定业务目标。"),

    goal("G002",
         "Browse the feed of followed subreddits during downtime to pass time and find something interesting to read, with no predefined outcome for the session.",
         ["Usually in fragmented downtime such as eating lunch or riding the bus", "No predefined goal; no particular outcome is claimed"],
         [("DOC028:T003", "So I log in just to kill some time following the subredd itself."),
          ("DOC028:T007", "I just scroll through the newsfeed till I find something that interests me, and I go into that post and interact with the post."),
          ("DOC028:T025", "it's usually when I have like some downtime like maybe when I'm eating lunch, or if I'm on the bus")],
         "direct",
         "三处原句分别支持消磨时间、滚动信息流直到发现感兴趣内容、以及碎片时间的适用条件；同时保留“没有预定目标/没有特定结果”的否定限定，未把它改成任务型目标。"),

    goal("G003",
         "Turn to technical help or code-query subreddits for other input when stuck on a problem, as an alternative to Stack Overflow.",
         ["When stuck on a problem or needing other input"],
         [("DOC028:T003", "So I use those when I'm stuck on a problem or need like other inputs for a problem."),
          ("DOC028:T003", "I also use Reddit as an alternative for stack overflow.")],
         "direct",
         "原句明确说明在卡住或需要其他输入时使用技术类 subreddit，并明示其定位是 Stack Overflow 的替代，主体、条件与方式均保留。"),

    goal("G004",
         "Get targeted answers grounded in other people's personal experience to the specific problem at hand, faster than a generic Google search, so that the problem gets solved.",
         ["Only when a problem is defined before logging in"],
         [("DOC028:T005", "I get personal experiences over facts, and these personal experiences are mostly legitimate."),
          ("DOC028:T005", "it's to get more targeted results to the problem that I'm facing."),
          ("DOC028:T009", "The outcome of that usage of Reddit will result in the problem being solved."),
          ("DOC028:T015", "It saves me time when I have specific queries, because I can get to authentic answers much faster.")],
         "direct",
         "原句同时给出目的（针对当前问题的结果）、依据（个人经历优先且被认为可信）、比较基准（比 Google 搜索更快省时）与结果（问题被解决）；四项均有直接原句，未加入原文没有的阈值。"),

    goal("G005",
         "Reach the relevant posts directly by Googling the question with 'reddit' appended, when the search target is specific.",
         ["Specific search target"],
         [("DOC028:T007", "So I Google, the question. And then I put Reddit after that. So it gives me all the relevant posts."),
          ("DOC028:T007", "So I just open the post directly")],
         "direct",
         "原句明确描述以 Google 加 reddit 关键词取得相关帖子并直接打开的方式，属原文明确选定的实现方式，按其自身内容保留为独立目标。"),

    goal("G006",
         "Create an advice-seeking post in the relevant community with a title, a Markdown body and any tags the subreddit makes mandatory, so that the members who filter on those tags answer it.",
         ["Most of the user's own posts ask for advice, for example in CS career questions and grad school admissions"],
         [("DOC028:T021", "The 1st thing you have to choose is a community that you want to post in."),
          ("DOC028:T021", "So most of the posts that I've done are posts asking for advice."),
          ("DOC028:T021", "you can add tags to your post, so some subreddits make it mandatory to add tags.")],
         "direct",
         "原句给出发布求助帖这一核心动作，并明确社区选择、标题与正文、以及部分社区强制标签的条件与目的（标签让合适成员筛选并回应）；操作步骤作为同一动作的组成保留，未机械拆成多个目标。"),

    goal("G007",
         "Rely on strongly moderated communities — auto-moderator bots that fact-check and alert human moderators, plus human moderators who remove low-quality posts — as the basis for treating posts as reliable.",
         ["Nothing found on the internet is treated as 100% reliable", "Reliability depends on the strength of the moderation team"],
         [("DOC028:T029", "So I feel that if a community has a strong, a strong set of moderators, then the posts themselves are reliable."),
          ("DOC028:T029", "So they fact check your posts, and they alert the human moderators if they feel that a post is not correctly, not entirely factual.")],
         "direct",
         "原句直接给出可靠性判断的条件（审核团队强）与机制（自动审核机器人核查并向人工版主告警、人工版主清理低质帖），并保留“并非 100% 可靠”的限定，未把它扩大为零误差要求。"),

    goal("G008",
         "Use Reddit, including the news subreddit, to stay updated on trends.",
         ["Trends related to followed subreddits, plus worldwide events such as the Olympics or the Nobel Prize"],
         [("DOC028:T031", "So I do use reddit to stay updated on trends.")],
         "direct",
         "原句明确“do use reddit to stay updated on trends”，主体与目的直接一致；范围按原句限定为 trends，未扩写为全部时事。"),

    goal("G009",
         "Keep news out of Reddit and use other apps as the primary news source, because Reddit is used to satisfy curiosity rather than to follow news.",
         ["Reddit is not the primary news source"],
         [("DOC028:T031", "But I just find it more convenient to keep news out of Reddit, because it's more of a it's more to satisfy curiosity, and not for news.")],
         "direct",
         "原句为明确的取舍与否定（把新闻排除在 Reddit 之外、以其他应用为主要新闻来源），并给出理由（Reddit 用于满足好奇心而非新闻）；保留否定方向，未改写成“多用 Reddit 看新闻”。"),

    goal("G010",
         "Research products and services on Reddit to get a balanced perspective from people of varied backgrounds before making a purchase decision.",
         ["Because marketplace reviews are mostly positive"],
         [("DOC028:T033", "Reddit is more of a balanced perspective, and you can also find people from varied backgrounds talking about the product."),
          ("DOC028:T033", "I've made a lot of purchase decisions because of reviews I've seen on Reddit.")],
         "direct",
         "原句说明在 Reddit 上做产品调研以取得平衡、多元背景的视角，并说明其已影响多次购买决定；比较对象（电商评价多为好评）作为理由保留在条件中。"),

    goal("G011",
         "Search general health questions on Reddit, including AskDoctors where healthcare professionals answer, for topics such as beginner yoga routines.",
         ["The user does not follow health communities; queries are searched case by case"],
         [("DOC028:T035", "I'd say it's good for general health, related questions.")],
         "direct",
         "原句明确 Reddit 适合一般健康问题，并给出 AskDoctors 由医疗从业者回答与新手瑜伽示例；“不专门关注健康社区、按需搜索”的条件一并保留。"),

    goal("G012",
         "Avoid relying on Reddit for specific health problems, and do not recommend it to others for those.",
         ["Reddit is judged suitable only for general health questions"],
         [("DOC028:T035", "But for specifics I've not used it, nor do I suggest anyone to use it."),
          ("DOC028:T035", "But at the same time I would not trust for health, related things specific, related things on Reddit.")],
         "direct",
         "原句为双重否定式表达（具体健康问题不用、也不建议他人使用、不信任具体健康内容），保留否定与不推荐的对象范围，未扩大为否定全部健康用途。"),

    goal("G013",
         "Match the feed view to the activity: compact view when actively searching so that all relevant results are visible before choosing one, and card view when passively scrolling.",
         ["Passive browsing versus active searching"],
         [("DOC028:T043", "If I'm using it actively, searching for something I prefer, like compact mode where I can see all relevant search results. Before I choose to click on one."),
          ("DOC028:T043", "I prefer, like card mode where I can just scroll through posts.")],
         "direct",
         "原句分别说明主动搜索时偏好紧凑视图（先看到全部相关结果再点开）与被动浏览时偏好看板视图；保留为有条件的偏好，未升级为强制或统一默认。"),

    goal("G014",
         "Keep the reading experience ad-free by using a browser ad blocker, since the inline ads are judged subtle and non-blocking.",
         ["Ads are tolerable when they stay in one location and do not block posts"],
         [("DOC028:T045", "But of course, like any other app it, it is better to have an ad free experience"),
          ("DOC028:T045", "I am using an ad block on my browser.")],
         "direct",
         "原句明确“无广告体验更好”并使用浏览器广告拦截器，同时保留对现有广告“不破坏阅读、位置固定、数量少”的评价；未把广告描述为严重障碍。"),

    goal("G015",
         "Buy the premium tier when ad blocking is not available, since removing ads is its only advantage.",
         ["Ad blocking currently makes the premium tier unnecessary"],
         [("DOC028:T047", "But in some scenario where ad block is not available, I would buy the premium tier."),
          ("DOC028:T047", "the only advantage of the premium tier, I'd say, like from my usage point of view, the only advantage is no ads")],
         "direct",
         "原句为带条件的购买意愿（广告拦截不可用时购买），并说明唯一好处是去广告、当前有拦截器所以不需要；条件与强度按原样保留为意愿而非承诺。"),

    goal("G016",
         "Save an in-progress post as a draft on mobile when leaving it mid-way, as is possible on desktop.",
         ["Mobile post creation"],
         [("DOC028:T027", "you can't save it as a draft which you can do on desktop. So that is something that is frustrating.")],
         "inferred",
         "原文明确陈述移动端无法保存草稿、桌面端可以，并称其为 frustrating；据此推断希望移动端具备草稿保存能力，原文未出现“希望/应该”字样，故支持标签为推断，缺失的能力本身即为推断依据。",
         assumptions=["把明确的挫败陈述与桌面端对照视为对该能力的正面期望"]),

    goal("G017",
         "Follow comment threads clearly on mobile, to the clarity that the desktop version provides.",
         ["Mobile comment reading"],
         [("DOC028:T027", "you cannot keep track of comments intuitively on Mobile"),
          ("DOC028:T027", "but I feel that the desktop version is much more clearly put out.")],
         "inferred",
         "原文明确说移动端无法直观跟踪评论、桌面端展示更清楚，属比较性不满；由该不满与对照推断希望移动端评论线索同样清晰，原文无直接请求句式，故记为推断。",
         assumptions=["把比较性不满视为对移动端评论线索清晰度的改善期望"]),

    goal("G018",
         "Improve the mobile app so that it is fast, intuitive and lightweight and remains the best app for the platform instead of trailing third-party wrapper apps.",
         ["Mobile UI judged slow, clunky, heavyweight and unintuitive", "Third-party wrapper apps built on the API have a higher market share than the official app"],
         [("DOC028:T027", "The mobile platform is quite slow and clunky, like the Ui. Is not very intuitive."),
          ("DOC028:T063", "I'd say the mobile app ui again should be much better"),
          ("DOC028:T063", "I think one thing they can improve is their mobile app.")],
         "direct",
         "原句直接要求移动端 UI 应明显更好、应改进移动应用，并给出慢、笨重、不直观与第三方封装应用份额更高的理由；强度“should be much better”保留，未写成必须达到具体指标。"),

    goal("G019",
         "Add a generative-AI tool that returns the exact subreddit for a given question, so that the question is posted where responders know the subject matter and the answers are better.",
         ["Bad responses can never be fully eliminated"],
         [("DOC028:T051", "I think a feature that would improve the user experience would be where you just type in like a Gen. AI tool where you want to subreddit about Xyz, and it gives you the exact subreddit that you need."),
          ("DOC028:T059", "So I would implement, like a geni tool to find a particular subreddit."),
          ("DOC028:T061", "I think the answers I'd get would be better, because when I post in a particular subreddit, people who are responding in that subreddit are expected to know the subject matter")],
         "direct",
         "三处原句构成提议（加生成式 AI 工具找准确 subreddit）、实现方式（输入描述给出目标 subreddit）与预期结果（回答者更懂主题、答案更好），并保留“坏回答无法完全消除”的限定。"),
]

ENTRIES = [
    ("C001", "keep", ["G001"], "关键词搜索特定话题以取得信息，与 G001 的核心动作和对象一致。"),
    ("C002", "merge", ["G002"], "与 C009、C011 同为“碎片时间滚动已关注 subreddit 的信息流”，同义合并，消磨时间的目的保留在 G002。"),
    ("C003", "keep", ["G003"], "卡住时求助技术类 subreddit 并作为 Stack Overflow 替代，独立成目标。"),
    ("C004", "exclude", [], "仅说明没有固定登录时间、视空闲或信息需要而定，属使用时机描述；相关情境已分别在 G002、G004 的条件中承接，不单独立目标。"),
    ("C005", "keep", ["G004"], "个人经历优先、比 Google 更有价值，是 G004 的核心依据与目的。"),
    ("C006", "merge", ["G004"], "“取得更有针对性的结果”是 C005 同一使用理由的自我概括，合并到 G004。"),
    ("C007", "exclude", [], "以“let's pick an example”引入的假设情境（健身计划），用于说明一般能力；按目标边界作为 G004 的情境例，不另立固定业务目标。"),
    ("C008", "keep", ["G005"], "Google 加 reddit 后直接打开帖子是原文明确选定的检索方式，保留为独立方式目标。"),
    ("C009", "merge", ["G002"], "与 C002 同一“滚动信息流—打开感兴趣帖子”的核心动作，合并并保留“发现感兴趣内容后互动”的结果。"),
    ("C010", "merge", ["G004"], "“问题被解决”是取得针对性答案的结果，与 G004 同一意图，合并为该目标的结果部分。"),
    ("C011", "merge", ["G002"], "无预定目标时浏览并阅读感兴趣内容是 C002/C009 的同一动作，合并；其中“有疑问再继续查”随 G002 的浏览结果保留。"),
    ("C012", "exclude", [], "描述互动对象是社区内的帖子而非特定用户或版主，属使用方式背景，未表达期望达到或避免的状态。"),
    ("C013", "exclude", [], "列举所属社区范围，属背景信息，未提出目标。"),
    ("C014", "exclude", [], "把匿名性称为平台 USP，属对平台特性的价值判断；受访者未表达自身对匿名的要求或避免被识别的意图，不据此造目标。"),
    ("C015", "exclude", [], "说明 Reddit 不是日常 routine、不使用也不会大幅改变生活，属影响程度的否定说明，无期望状态。"),
    ("C016", "merge", ["G004"], "省时与更快取得真实答案是同一“取得针对性答案”动作的预期结果，合并到 G004。"),
    ("C017", "uncertain", [], "信息流贴合个人偏好且会浏览全部推送，属正面现状描述；是否构成“信息流应保持贴合”的维持目标无法从原句确定，故留待确认。"),
    ("C018", "keep", ["G006"], "选社区、写标题与 Markdown 正文、按需加标签是发帖动作的组成，保留在 G006。"),
    ("C019", "merge", ["G006"], "自身发帖以求助为主（CS career questions、grad school admissions），与 C018 同一发帖动作，合并为 G006 的目的。"),
    ("C020", "exclude", [], "描述评论与楼中楼回复的操作流程，未表达期望结果；受访者亦自述很少通过评论互动。"),
    ("C021", "exclude", [], "把帖子归为分享信息与寻求建议两类，属分类说明，不是目标。"),
    ("C022", "exclude", [], "描述他人分享信息供吸收的帖子类型；受访者自述其发帖以求助为主，该方向无自身意图依据。"),
    ("C023", "exclude", [], "说明搜索时无时间偏好、碎片时间浏览，属使用时机；情境已在 G002 条件中承接。"),
    ("C024", "uncertain", [], "描述碎片时间使用通常受限于该活动、有时会连锁浏览两小时，语气为描述而非明确期望；是否构成“避免长时间沉浸”的目标无法确定。"),
    ("C025", "exclude", [], "仅说明桌面端没有障碍，属现状陈述；未表达维持该状态的意图，按现有能力不自动成为要求。"),
    ("C026", "keep", ["G018"], "移动端慢、笨重、界面不直观并被称为挫败，是 G018 的主要依据。"),
    ("C027", "keep", ["G016"], "移动端无法像桌面端保存发帖草稿并明确称其令人挫败，独立成目标。"),
    ("C028", "keep", ["G017"], "移动端无法直观跟踪评论、桌面端更清楚，独立成目标。"),
    ("C029", "keep", ["G007"], "以强审核团队（自动审核 + 人工版主）作为帖子可靠的依据，独立成目标。"),
    ("C030", "exclude", [], "对网络信息可靠性的保留说明，作为 G007 的限定条件承接，不单独立目标。"),
    ("C031", "keep", ["G008"], "明确用 Reddit（含 news subreddit）跟进趋势，独立成目标。"),
    ("C032", "keep", ["G009"], "明确把新闻排除在 Reddit 之外、以其他应用为主要新闻来源，是否定型取舍，独立成目标。"),
    ("C033", "exclude", [], "说明奥运会、诺奖级事件会出现在 popular 页，属平台能力描述，无自身期望。"),
    ("C034", "keep", ["G010"], "在 Reddit 调研产品以取得平衡、多元背景视角，独立成目标。"),
    ("C035", "merge", ["G010"], "多次购买决定受 Reddit 评价影响，是 C034 调研目标的已发生结果，合并保留。"),
    ("C036", "keep", ["G011"], "一般健康问题在 Reddit（含 AskDoctors）搜索，独立成目标。"),
    ("C037", "keep", ["G012"], "具体健康问题不用、也不建议他人使用，是否定型目标，独立保留。"),
    ("C038", "exclude", [], "自述没有个人社区感、很少通过评论互动，属否定性现状，未提出目标。"),
    ("C039", "exclude", [], "描述离线可查看已缓存信息流但不能发帖或刷新、能力不全面，属现状能力报告；按目标边界先保留现状，未表达维持或改善意图。"),
    ("C040", "exclude", [], "描述可按 new/top/trending/rising 排序，属现有功能说明，未表达期望结果。"),
    ("C041", "keep", ["G013"], "主动搜索用紧凑视图、被动浏览用看板视图的偏好，含明确目的，保留为条件性偏好目标。"),
    ("C042", "keep", ["G014"], "无广告体验更好并使用浏览器广告拦截器，独立成目标。"),
    ("C043", "keep", ["G015"], "广告拦截不可用时购买高级订阅，是带条件的意愿，独立成目标。"),
    ("C044", "merge", ["G015"], "“最近可能就会买”的总体意愿与 C043 同一购买动作，合并并保留“有广告拦截时不需要”的限定。"),
    ("C045", "exclude", [], "描述浅色/深色模式与旧版界面可选，并对两者作口味比较；属功能说明与偏好背景，无明确结果意图。"),
    ("C046", "exclude", [], "对现有搜索准确性符合预期的正面评价；未提出维持或改善要求，其相关可行动意图由 C047/C048（subreddit 搜索）承接。"),
    ("C047", "exclude", [], "找不到合适 subreddit 的障碍陈述，不独立成目标；其补救指向 G019（工具化定位 subreddit）。"),
    ("C048", "keep", ["G019"], "提议加入生成式 AI 工具，输入描述即给出准确 subreddit，独立成目标。"),
    ("C049", "merge", ["G014"], "广告在一定程度上妨碍体验，与 C042 同一去广告目的，合并为 G014 的依据。"),
    ("C050", "exclude", [], "通知可配置、不打扰、仅浏览器打开时到达，属满意性现状评价，未提出要求。"),
    ("C051", "exclude", [], "认为隐私与数据处理得当、本人未遇问题并相信其遵守规范，属信念与现状评价，不构成目标。"),
    ("C052", "exclude", [], "认为审核很好但取决于 subreddit 与团队规模，且明确没有改进建议，属满意评价而非目标。"),
    ("C053", "merge", ["G019"], "与 C048 同一“用 AI 工具定位应发问的 subreddit”提议，合并；保留“具体 subreddit 更有价值”的理由。"),
    ("C054", "merge", ["G019"], "在具体 subreddit 发问可获得更懂主题的回答，是 C048/C053 工具的预期结果，合并到 G019。"),
    ("C055", "merge", ["G018"], "移动端 UI 应明显更好，与 C026 同一改善对象，合并为 G018 的明确要求。"),
    ("C056", "merge", ["G018"], "第三方封装应用份额高于官方应用是问题，是 G018 改进移动应用的理由，合并。"),
    ("C057", "exclude", [], "列举私信、连续登录奖杯等附加功能，属功能清单，未表达目标。"),
]

CHECKS = [
    ("S1", [("DOC028:T003", "So I browse my city's subreddit with keyword. Halloween, search to get information about that.")],
     ["C001"], ["G001"], "represented", "回查关键词搜索话题的原句，确认作为一般能力目标保留，例句未固化。"),
    ("S2", [("DOC028:T003", "So I use those when I'm stuck on a problem or need like other inputs for a problem.")],
     ["C003"], ["G003"], "represented", "回查卡住时求助技术社区的原句，条件与 Stack Overflow 替代定位均保留。"),
    ("S3", [("DOC028:T005", "I get personal experiences over facts, and these personal experiences are mostly legitimate.")],
     ["C005"], ["G004"], "represented", "回查首要使用理由，确认“个人经历优先且被认为可信”进入 G004，而非仅取“更快”一句。"),
    ("S4", [("DOC028:T007", "So I Google, the question. And then I put Reddit after that. So it gives me all the relevant posts.")],
     ["C008"], ["G005"], "represented", "回查明确选定的检索方式，确认方式本身有独立目标承接，而非只写在理由里。"),
    ("S5", [("DOC028:T009", "It's just that I just browse them to find and read something interesting.")],
     ["C011"], ["G002"], "represented", "回查无预定目标时的浏览结果，确认 G002 保留“无特定结果”的限定。"),
    ("S6", [("DOC028:T011", "I think, the USP. Of Reddit is anonymity, so it's really hard to trace a post back to the person")],
     ["C014"], [], "excluded", "回查匿名性陈述，判定为平台特性与价值判断，受访者未表达自身要求，故不建目标。"),
    ("S7", [("DOC028:T015", "It saves me time when I have specific queries, because I can get to authentic answers much faster.")],
     ["C016"], ["G004"], "represented", "回查省时与更快取得真实答案，确认并入 G004 的预期结果而非另立效率目标。"),
    ("S8", [("DOC028:T021", "you can add tags to your post, so some subreddits make it mandatory to add tags.")],
     ["C018"], ["G006"], "represented", "回查发帖流程与强制标签条件，确认标签的条件性与目的（便于对口成员筛选）保留。"),
    ("S9", [("DOC028:T025", "If I am, then I don't have a time preference.")],
     ["C023"], [], "excluded", "回查“无时间偏好”陈述，判定为使用时机说明，情境已进入 G002 条件。"),
    ("S10", [("DOC028:T027", "you can't save it as a draft which you can do on desktop. So that is something that is frustrating.")],
     ["C027"], ["G016"], "represented", "回查移动端草稿挫败句，确认按推断处理并单独成目标。"),
    ("S11", [("DOC028:T027", "you cannot keep track of comments intuitively on Mobile")],
     ["C028"], ["G017"], "represented", "回查移动端评论线索句，确认与桌面端对照进入 G017。"),
    ("S12", [("DOC028:T031", "But I just find it more convenient to keep news out of Reddit, because it's more of a it's more to satisfy curiosity, and not for news.")],
     ["C032"], ["G009"], "represented", "回查“把新闻排除在外”的取舍句，确认否定方向与理由同时保留，且未与 G008 混为一条。"),
    ("S13", [("DOC028:T035", "But for specifics I've not used it, nor do I suggest anyone to use it.")],
     ["C037"], ["G012"], "represented", "回查具体健康问题的否定与不推荐，确认保留为独立 Avoid 目标。"),
    ("S14", [("DOC028:T039", "So I'd say, yes, there is an offline capability, but it's not very comprehensive.")],
     ["C039"], [], "excluded", "回查离线能力描述，判定为现状能力报告，未表达维持或改善意图。"),
    ("S15", [("DOC028:T045", "But of course, like any other app it, it is better to have an ad free experience")],
     ["C042"], ["G014"], "represented", "回查无广告偏好，确认与广告拦截做法合并入 G014。"),
    ("S16", [("DOC028:T047", "But in some scenario where ad block is not available, I would buy the premium tier.")],
     ["C043"], ["G015"], "represented", "回查有条件购买意愿，确认条件与“意愿非承诺”的强度保留。"),
    ("S17", [("DOC028:T051", "So the ability to find a subreddit is quite complicated at this point")],
     ["C047"], [], "excluded", "回查 subreddit 查找困难的障碍句，判定为障碍线索而非目标，补救方向记入 G019。"),
    ("S18", [("DOC028:T053", "I don't think the notifications are too troublesome. They don't really get in the way of you doing anything.")],
     ["C050"], [], "excluded", "回查通知评价，判定为满意性现状，无改善要求。"),
    ("S19", [("DOC028:T055", "Personally, I haven't faced any issues till now")],
     ["C051"], [], "excluded", "回查隐私评价，判定为信念与现状，不据此造目标。"),
    ("S20", [("DOC028:T057", "I think the moderation is very good it does depend on the subreddit.")],
     ["C052"], [], "excluded", "回查审核评价，确认受访者明确没有改进建议。"),
    ("S21", [("DOC028:T063", "I'd say the mobile app ui again should be much better")],
     ["C055"], ["G018"], "represented", "回查收尾处的移动端改善要求，确认与 T027 的 UI 挫败合并为 G018。"),
    ("S22", [("DOC028:T019", "So I normally interact with all the posts that come on my feed.")],
     ["C017"], [], "uncertain", "回查信息流贴合度陈述，是否构成维持型目标无法判定，保留待确认。"),
]

RELATIONS = [
    {"relation_id": "R1", "source_id": "G005", "target_id": "G004", "type": "operationalization",
     "status": "supported", "conditions": ["specific search target"], "assumptions": [],
     "rationale": "以 Google 追问加 reddit 关键词并直接打开帖子，是受访者为实现“针对具体问题取得答案”所选定的检索方式；方式目标指向其服务的目的目标，方向为手段→目的。",
     "evidence_ids": [],
     "evidence_quotes": [{"source_id": "DOC028:T007", "quote": "So one is, if I open Reddit and I want to like, search for something specific. Then I open it through Google.", "role": "basis"}]},

    {"relation_id": "R2", "source_id": "G003", "target_id": "G004", "type": "specialization",
     "status": "supported", "conditions": ["stuck on a technical problem"], "assumptions": [],
     "rationale": "“卡住时到技术类社区求助”是“针对具体问题取得答案”在技术问题这一具体情境下的目标；只覆盖该情境，不声称覆盖 G004 的全部适用情形。",
     "evidence_ids": [],
     "evidence_quotes": [{"source_id": "DOC028:T003", "quote": "So I use those when I'm stuck on a problem or need like other inputs for a problem.", "role": "basis"}]},

    {"relation_id": "R3", "source_id": "G015", "target_id": "G014", "type": "operationalization",
     "status": "supported", "conditions": ["ad blocking is not available"], "assumptions": [],
     "rationale": "在广告拦截不可用的情形下购买高级订阅，是受访者为维持无广告阅读所给出的替代手段，其唯一好处被明确为去广告。",
     "evidence_ids": [],
     "evidence_quotes": [{"source_id": "DOC028:T047", "quote": "the only advantage of the premium tier, I'd say, like from my usage point of view, the only advantage is no ads", "role": "basis"}]},

    {"relation_id": "R4", "source_id": "G019", "target_id": "G006", "type": "contribution",
     "status": "supported", "conditions": ["when the right community for a question is unclear"], "assumptions": [],
     "rationale": "AI 定位 subreddit 的工具直接帮助发帖者选对社区，从而提高求助帖被对口成员回应的机会；有帮助不等于充分保证被回答。",
     "evidence_ids": [],
     "evidence_quotes": [{"source_id": "DOC028:T059", "quote": "But there, there's much more value in posting in a specific subreddit, and finding that subreddit would be very useful.", "role": "basis"}]},
]

PASSES = [
    {"pass_id": "P1", "kind": "initial", "context": "isolated", "status": "completed",
     "window_results": []},
    {"pass_id": "P2", "kind": "full_context", "context": "isolated", "status": "completed",
     "window_results": []},
]

WINDOWS = [w["window_id"] for w in json.loads((A / "work/_prep/source-windows.json").read_text(encoding="utf-8"))["windows"]]
for p in PASSES:
    p["window_results"] = [{"window_id": w, "status": "processed", "reason": ""} for w in WINDOWS]

spec = {
    "document_id": "DOC028",
    "status": "completed",
    "raw_candidates": RAW,
    "goals": GOALS,
    "review_questions": [
        {"candidate_ids": ["G016", "G017", "G018"],
         "question": "移动端三项（草稿保存、评论线索清晰度、整体 UI）是否应合并为一个改善目标或视为同一父目标的子目标？原文分别陈述，未给出层级关系。",
         "reason": "避免为凑层级硬造父子关系，同时确认拆分是否过细。"},
        {"candidate_ids": [],
         "question": "原文多处对现状表示满意（桌面端无障碍、搜索准确性、通知不打扰、隐私处理、审核质量）；本次未建维持型目标，是否需要补充维持目标？",
         "reason": "已实现能力不自动成为要求，但也可能含维持意图，需确认取舍。"},
    ],
    "limitations": [
        "转写稿存在识别噪声（如 'credit posts'、'lead code'、'geni tool'、'@it.com'），引文按原样保留，未做文字修正。",
        "单一受访者、单次访谈，未提供其他佐证材料，无法核验其所述平台能力的真实性。",
        "未联网核对 Reddit 现有功能或第三方信息，全部判断仅基于本转写稿。",
    ],
    "ledger": {
        "model": "unknown", "temperature": "unknown",
        "budget": "1 initial pass + <=2 repair rounds",
        "usage": "unknown",
        "skill_revision": "a5952d426b1624a3fcb2ce2829e1ae1ceb15e19dc3309d9571f3bc6b465deb6f",
        "prompt_revision": "task-prompt-v1",
        "planned_passes": 2,
        "stop_reason": "完成 34 个窗口的逐窗捕获与全篇回查；重复出现的同义要求（如 AI 定位 subreddit、移动端改善）已合并，未再出现有新增依据且可独立成目标的意图，故停止。",
        "passes": PASSES,
        "full_context_review": {
            "status": "completed",
            "reason": "通读全部 70 轮，逐项回查指代（如 'that' 指向的挫败点）、条件继承（碎片时间、具体问题、广告拦截不可用）、否定（不把新闻放在 Reddit、不建议用于具体健康问题、没有预定结果）与例外（不关注健康社区但会搜索），并补核 T039、T053、T055、T057 等现状评价是否含目标意图。",
        },
        "entries": [{"candidate_id": c, "disposition": d, "final_goal_ids": g, "reason": r} for c, d, g, r in ENTRIES],
        "source_checks": [
            {"check_id": cid, "evidence_candidates": ev(pairs), "candidate_ids": cs,
             "final_goal_ids": gs, "outcome": oc, "reason": rs}
            for cid, pairs, cs, gs, oc, rs in CHECKS
        ],
    },
    "decisions": {
        "relations": RELATIONS,
        "groups": [],
        "questions": [
            {"target_type": "goal", "target_id": "G018",
             "message": "移动端改善的四个要点（速度、直观性、草稿、评论线索）现分布在 G016/G017/G018 三个目标，是否应合并为一个目标？"},
            {"target_type": "goal", "target_id": "G009",
             "message": "G008（用 news subreddit 跟进趋势）与 G009（把新闻排除在 Reddit 外）是否存在范围张力？原文以 trends 与 news 区分，但未给出判据。"},
        ],
        "reassessments": [],
    },
}

# consistency checks
goal_ids = [g["candidate_id"] for g in GOALS]
seen = set()
for e in ENTRIES:
    assert e[0] not in seen
    seen.add(e[0])
    for g in e[2]:
        assert g in goal_ids, g
assert seen == {c["candidate_id"] for c in RAW}
counts = {}
for e in ENTRIES:
    for g in e[2]:
        counts[g] = counts.get(g, 0) + 1
for g in goal_ids:
    assert counts.get(g), "no provenance " + g

if ERRS:
    print("\n".join(ERRS))
    raise SystemExit(1)
(A / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("goals", len(GOALS), "raw", len(RAW), "entries", len(ENTRIES), "checks", len(CHECKS))
print("ok")
