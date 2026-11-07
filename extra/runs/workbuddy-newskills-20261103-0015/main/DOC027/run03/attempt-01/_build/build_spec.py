# -*- coding: utf-8 -*-
"""生成 spec.json（DOC027 run03 attempt-01）。内建引文逐字符校验。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = json.loads((ROOT / "source/DOC027.json").read_text(encoding="utf-8"))
TURNS = {t["source_id"]: t["text"] for t in SRC["turns"]}
WINDOWS = json.loads((ROOT / "_win/source-windows.json").read_text(encoding="utf-8"))
WIN_IDS = [w["window_id"] for w in WINDOWS["windows"]]

errors = []


def ev(source_id, quote, role="basis"):
    text = TURNS.get(source_id)
    if text is None:
        errors.append(f"missing turn {source_id}")
        return None
    if quote not in text:
        errors.append(f"NOT FOUND {source_id}: {quote[:60]}")
        return None
    if text.count(quote) != 1:
        errors.append(f"AMBIGUOUS x{text.count(quote)} {source_id}: {quote[:60]}")
        return None
    return {"source_id": source_id, "quote": quote, "role": role}


def c(cid, statement, modality, origin, source_id, quote, context=None, actor="Stakeholder", role="basis"):
    item = {
        "candidate_id": cid,
        "statement": statement,
        "actor": actor,
        "modality": modality,
        "context": context or [],
        "origin": origin,
        "pass_id": "P1",
        "evidence": [ev(source_id, quote, role)],
    }
    return item


raw = []
raw.append(c("C001",
             "Use Twitter as the go-to news app by tapping a trending hashtag and going through everything happening around the world.",
             "stated reason (want)", "explicit", "DOC027:T005",
             "Twitter is kind of like my go to news app because there are a lot of trends that are happening around the world, and Twitter just makes it very easy for me to just tap like one particular hashtag whatever is trending, and then go through everything that is happening around the world."))
raw.append(c("C002",
             "Stay connected to friends in real time by sending photos and videos instantaneously on Snapchat.",
             "stated benefit (want)", "explicit", "DOC027:T005",
             "For Snapchat. It's very easy for me to connect to stay connected to my friends in real time."))
raw.append(c("C003",
             "Keep anonymity intact while joining Reddit interest groups and asking questions or helping other people.",
             "stated benefit (want)", "explicit", "DOC027:T005",
             "And I can join those interest groups and ask like, maybe a question, or maybe help other people. And all of this while be while maintaining my anonymity"))
raw.append(c("C004",
             "Find questions and discussions about a specific problem (recipe, where to find an item in the city) inside a relevant subreddit.",
             "stated benefit (want)", "explicit", "DOC027:T005",
             "I can almost always like find different kind of questions or different kind of issues that I'm stuck in"))
raw.append(c("C005",
             "Platform choice differs by geolocation: WhatsApp for daily communication in India, WeChat among Southeast Asian friends in the US, Reddit a niche crowd in India.",
             "observation (fact)", "explicit", "DOC027:T007",
             "So in India, a lot of people use whatsapp for day to day communications"))
raw.append(c("C006",
             "Get news about what is happening back in India even though Twitter is now set to the current US location.",
             "complaint", "inferred", "DOC027:T009",
             "But if but if I wanna get to know about the news or the things that are happening back in India, then that might not be possible, because Twitter is kind of now set to my location in us.",
             context=["feed is bound to current geolocation"]))
raw.append(c("C007",
             "Treat authentication as the most important feature because nobody else should access my accounts on any social media platform.",
             "strong want (most important)", "explicit", "DOC027:T011",
             "is authentication, because I don't want anyone else accessing my accounts on any social media platforms."))
raw.append(c("C008",
             "Keep tweets and Reddit/Instagram posts online until I delete or archive them myself.",
             "want (obligation: should be there until)", "explicit", "DOC027:T013",
             "they should be there until, and unless I delete them or I archive them."))
raw.append(c("C009",
             "Keep outages sporadic rather than too regular, because regular outages would lose me as a customer.",
             "want (negative, tolerance stated)", "explicit", "DOC027:T013",
             "I don't want those outages to be that often, if they are like sporadic, I'm fine with it, but if they are too regular, then they might lose me as a customer",
             context=["sporadic outages are acceptable"]))
raw.append(c("C010",
             "Use a long saved backup code as the 2FA and re-enter it whenever logging in from a new device or starting a new web session.",
             "approved mechanism", "explicit", "DOC027:T019",
             "it will give you like a backup code, which is a really long, I don't know. Like maybe 16 to 30 digit code you have to keep it saved, because that is going to be your 2 fa for the rest of your life"))
raw[-1]["evidence"].append(ev("DOC027:T021",
                              "whenever you try to log back in from a new device. Or let's say you start a new session on your on your web app for the same particular for the same signal application it will ask you to give you the backup code that it gave you for the 1st time you logged in"))
raw.append(c("C011",
             "Rank platforms by feature priority: Reddit first for anonymity, Signal second for authentication, privacy and data encryption.",
             "preference ranking", "explicit", "DOC027:T027",
             "reddit reddit kind of comes for most because of the anonymity that it provides the next will be signal because of like high authentication and privacy and data encryption"))
raw.append(c("C012",
             "Avoid ads following me on Google and other search engines after I mention something (a refrigerator) while chatting on Instagram or WhatsApp.",
             "complaint / privacy worry", "explicit", "DOC027:T029",
             "And the next day I like start seeing these ads on Google and any other like search engines that like about my about like a refrigerator or something"))
raw.append(c("C013",
             "Use Twitter to learn what is happening around the world, including tech news, memes and easily followed trends.",
             "stated interest", "explicit", "DOC027:T031",
             "Because right now I I am really interested in learning about what is happening around the world. Twitter also has really great tech news. It it also has really great memes to laugh about. and I can also, like follow trends on Twitter pretty easily."))
raw.append(c("C014",
             "Stay logged in so logging back in stays rare, and log back in (with 2FA) only when logged out.",
             "described valued state", "explicit", "DOC027:T033",
             "I'm almost always logged in into my system into my account, basically. But by some means, if I get logged out, which is rare on Reddit."))
raw.append(c("C015",
             "See the question highlighted on a post card and tap the card to reach the thread of answers and conversations.",
             "described use", "explicit", "DOC027:T035",
             "the question is highlighted. or like whoever is asking the question, of course, like in anonymous way. And the if you, if you want to see the answers or the responses to that particular question, you'll probably have to tap that particular card"))
raw.append(c("C016",
             "Scroll the aggregated homepage and open threads about events of current interest, e.g. a campus event such as Halloween dress code.",
             "described use", "explicit", "DOC027:T037",
             "So I'll probably I'm right now interested about that, so I'll probably click that I'll go through the threads that are happening."))
raw.append(c("C017",
             "Prevent people I do not even know from seeing through my text or my conversation with my friends.",
             "main frustration (negative want)", "explicit", "DOC027:T039",
             "I don't want other people to other people as in the people that I don't even know like kind of like see through my text or my conversation with my friends."))
raw.append(c("C018",
             "Stop ads being pushed at me on top of everything else.",
             "complaint (fragment)", "explicit", "DOC027:T041",
             "Also like then on top of that give ads to me around."))
raw.append(c("C019",
             "Accept ads as sometimes helpful when I actually want to buy something, although this is very rare.",
             "concession / exception", "explicit", "DOC027:T043",
             "lately, I've I've realized that it's kind of helpful sometimes when I actually want to like buy something, and it gives me those ads, but that's rare. That's very rare, mostly."))
raw.append(c("C020",
             "Not see the same kind of ads over and over again just because I talked about it one time.",
             "want (negative)", "explicit", "DOC027:T045",
             "I don't want to see the same kind of ads over and over again, just because I talked about it one time. So the 1st important thing is, I think, data privacy for me."))
raw.append(c("C021",
             "Have content keep loading while scrolling instead of hitting a lag where no more posts load.",
             "complaint (negative want)", "explicit", "DOC027:T047",
             "the lack of content like whenever I scroll through like reddit or twitter. At 1 point there will be like kind of like a lag where the data isn't being loaded or the."))
raw.append(c("C022",
             "Have my data encrypted, named as the first requirement alongside data privacy.",
             "stated requirement (emphasis)", "explicit", "DOC027:T047",
             "Like especially data encryption. apart from that, I would say, the lack of content like whenever I scroll through like reddit or twitter."))
raw[-1]["evidence"].append(ev("DOC027:T045",
                              "So the 1st important thing is, I think, data privacy for me."))
raw.append(c("C023",
             "Go back to the top and refresh when loading stalls, and avoid missing a post because of the stall.",
             "remedy + worry", "explicit", "DOC027:T049",
             "So it's easier for me to just go at like the top and then start like a new kind of like a refresh, instead of just like going through the same kind of my session."))
raw[-1]["evidence"].append(ev("DOC027:T049", "maybe I just missed one particular post or one particular item", "context"))
raw.append(c("C024",
             "Load content at the right time rather than after a stall.",
             "fragment (no independent intent)", "unknown", "DOC027:T051",
             "Than just loading in the right time."))
raw.append(c("C025",
             "Search Reddit for something very particular (best Indian restaurants in the city) and get good recommendations from random people.",
             "stated use", "explicit", "DOC027:T053",
             "it's mostly when I am in a particular situation where I wanna search for something very particular like. Let's say, what are the best Indian restaurants in the city?"))
raw[-1]["evidence"].append(ev("DOC027:T053",
                              "I probably would end up with, like some good recommendations from like random people on reddit", "context"))
raw.append(c("C026",
             "Get answers for a very niche situation (someone who passed a specific company interview), which Reddit often cannot provide.",
             "obstacle + underlying want", "explicit", "DOC027:T055",
             "if I go to Reddit and search for Hi, if if there's like anyone who passed this interview, how was your experience. I probably wouldn't get any answers for that."))
raw.append(c("C027",
             "Go to Reddit rather than the open internet to ask whatever question I want.",
             "preference (Reddit overpowers internet)", "explicit", "DOC027:T057",
             "So that's why I just go to Reddit to like, figure out whatever question I want to ask."))
raw.append(c("C028",
             "Explain basic credentials and managing credentials across all platforms first, because that is essential to access an account.",
             "explanation to a novice (concept)", "explicit", "DOC027:T059",
             "The 1st thing that I'll introduce to them is like their basic credentials and managing those credentials across all the social media platforms."))
raw.append(c("C029",
             "Treat tweets as a kind of post when explaining platform terminology.",
             "explanation to a novice (concept)", "explicit", "DOC027:T061",
             "Twitter usually uses tweets, but they can still be categorized as posts."))
raw.append(c("C030",
             "Treat posts as the main content shown on the homepage.",
             "explanation to a novice (concept)", "explicit", "DOC027:T063",
             "So all of these kind of like have these posts which are the main content that you see mostly on your like."))
raw.append(c("C031",
             "Keep a digital vault on my phone that tracks all my accounts and credentials, because losing the vault would lose most of my account details.",
             "current practice + importance", "explicit", "DOC027:T065",
             "So I do have like a a digital vault that I keep on my phone which helps me to keep. Keep a track of all the accounts, my credentials for all the social networking platforms."))
raw[-1]["evidence"].append(ev("DOC027:T065",
                              "if I lose that particular vault then it'll probably I'll probably end up losing most of my account details", "context"))
raw.append(c("C032",
             "Rely on a password manager that offers my user name in a pop-up when I open a social media login page.",
             "described use (valued)", "explicit", "DOC027:T067",
             "wherever I log into any any like social media. A web page there will be like a pop up which says that this is my user"))
raw.append(c("C033",
             "Have credentials autofilled so I only have to press login.",
             "described use (convenient)", "explicit", "DOC027:T069",
             "That, and it'll Autofill everything for me, and I just have to press login. and that is pretty much it."))
raw.append(c("C034",
             "Stay connected to the world so I never miss that something really big has happened.",
             "motivation (strong want)", "explicit", "DOC027:T075",
             "I wouldn't like the fact that something really big has happened, and I just didn't. I just did not know about it like that won't be a feeling that I would want to experience."))
raw[-1]["evidence"].append(ev("DOC027:T075",
                              "That's 1 of my biggest motivation to be on like different social media platforms, so that I know what's happening in the world.", "context"))
raw.append(c("C035",
             "Know what is happening in my friend circle, including my friends back in India.",
             "valued connection", "explicit", "DOC027:T075",
             "It's also about knowing what's happening in my friend Circle, or with the with my friends back in India."))
raw.append(c("C036",
             "Know what is happening around me on campus and in class, including things that are non-verbal but shareable through social apps.",
             "valued connection", "explicit", "DOC027:T077",
             "Let's say, what's happening on campus, what's happening in class. what's happening like with my classmates stuff like that stuff that are like non verbal, but can be shared through like social networking apps."))
raw.append(c("C037",
             "Be shown different kinds of content instead of the similar content Instagram's algorithm keeps repeating; this is why I skip Instagram.",
             "want (negative)", "explicit", "DOC027:T079",
             "whereas I want to be shown like different kind of content"))
raw.append(c("C038",
             "Get different trends happening in the world instead of only food videos and pictures over and over.",
             "want (negative)", "explicit", "DOC027:T081",
             "So that I get different kind of like trends that are happening in the world, things that are happening."))
raw[-1]["evidence"].append(ev("DOC027:T081",
                              "I don't want Instagram to just keep showing me that over and over again.", "context"))
raw.append(c("C039",
             "Receive an assortment of content rather than one particular stream, going to a specific channel or group when I want a single stream.",
             "want (preference with exception)", "explicit", "DOC027:T087",
             "I want like an assortment of content, not just one particular stream of content."))
raw.append(c("C040",
             "Get an assortment of everything when I am not deliberately digging into a specific group.",
             "want", "explicit", "DOC027:T089",
             "then I I want like an assortment of like everything."))
raw.append(c("C041",
             "Avoid a Twitter feed where the latest Elon Musk tweet comes first and every fifth tweet is his, because it biases my mind.",
             "complaint (negative want)", "explicit", "DOC027:T095",
             "the moment I open twitter, the 1st thing that will that Twitter will show me is the latest Elon Musk's tweet, and every 5th tweet is Elon Musk's tweet. So that kind of actually creates a bias on my mind"))
raw.append(c("C042",
             "Believe that a one-sided Twitter feed would incline me towards what that person says because I like the platform.",
             "belief about effect", "explicit", "DOC027:T097",
             "that would easily just make me inclined towards whatever Elon Musk is saying, because I like that particular platform"))
raw.append(c("C043",
             "Filter authentic from inauthentic content so I am never misinformed by social media, and modify my opinion when the actual truth differs.",
             "reported ability + desired state", "explicit", "DOC027:T099",
             "I can kind of easily filter out what is authentic and what is not authentic. And in that way I'm never misinformed because of social media."))
raw.append(c("C044",
             "Have apps use basic human judgement and not throw random ads at me just because I said one particular name.",
             "wish (magic wand)", "explicit", "DOC027:T101",
             "And I'll use that wand to. To make these social media apps to use basic human judgment and not just throw random ads at me just because I said that one particular name."))
raw.append(c("C045",
             "Give about two ads for something I may want and stop showing them if I skip them, because repeated ads make me leave the app.",
             "wish + mechanism (magic wand)", "explicit", "DOC027:T103",
             "So kind of like, find a balance like, okay, maybe this person wants to buy a refrigerator. So let's just give them 2 ads. And if they skip those ads, then we will stop showing refrigerator ads."))
raw[-1]["evidence"].append(ev("DOC027:T103",
                              "the moment I keep seeing like these advertisements on Instagram or any other social media apps, I'll just easily get frustrated, and I'll exit the app and go to somewhere else, which which doesn't have ads.", "context"))
raw.append(c("C046",
             "Have one common platform I design myself that gathers my favorite apps and gives an assortment of their content in one place.",
             "wish (would be really happy)", "explicit", "DOC027:T105",
             "So I'd say that I would be really happy if there was like this common platform which. Like I can design for myself."))
raw[-1]["evidence"].append(ev("DOC027:T105",
                              "and give me, like an assortment of different kind of content, let's say, some good content from Twitter, some good content from Reddit, some good content from Instagram, and give it all in one place", "context"))
raw.append(c("C047",
             "Open one app and get all the content instead of wasting time switching between apps.",
             "want (negative)", "explicit", "DOC027:T107",
             "Because I kind of like waste a lot of time just switching between apps which I don't want. I just want to open 1 1 app and get all the content and be done with it."))

# ---------------- goals ----------------
goals = []


def g(gid, statement, origin, cand_ids, quotes, context=None, inference=None, label="direct", rationale="", supported=None):
    goals.append({
        "candidate_id": gid,
        "statement": statement,
        "actor": "Stakeholder",
        "context": context or [],
        "origin": origin,
        "inference": inference,
        "evidence": quotes,
        "judgment": {
            "label": label,
            "rationale": rationale,
            "supported_parts": supported or [],
            "unsupported_parts": [],
            "assumptions": [],
            "reasoning_steps": [],
        },
        "_cands": cand_ids,
    })


g("G001",
  "Use Twitter's trending hashtags to go through everything that is happening around the world, so Twitter serves as my go-to news app.",
  "explicit", ["C001", "C013"],
  [ev("DOC027:T005", "Twitter is kind of like my go to news app because there are a lot of trends that are happening around the world, and Twitter just makes it very easy for me to just tap like one particular hashtag whatever is trending, and then go through everything that is happening around the world."),
   ev("DOC027:T031", "Twitter also has really great tech news. It it also has really great memes to laugh about. and I can also, like follow trends on Twitter pretty easily.")],
  rationale="受访者明确说 Twitter 是 go-to news app，并说明靠点开热门 hashtag 浏览全球动态；T031 补充同一动作的目的（科技新闻、梗、追趋势）。主体、对象（hashtag/趋势）、范围一致。",
  supported=["Twitter 作为主要新闻来源的定位", "通过热门 hashtag 查看全球动态", "追趋势与科技新闻"])

g("G002",
  "Send photos and videos instantaneously on Snapchat to stay connected with my friends in real time.",
  "explicit", ["C002"],
  [ev("DOC027:T005", "For Snapchat. It's very easy for me to connect to stay connected to my friends in real time.")],
  rationale="原句直接说出用 Snapchat 即时发照片视频的目的是与朋友保持实时联系，动作与结果均在同一句。",
  supported=["即时发送照片/视频", "与朋友保持实时联系"])

g("G003",
  "Join Reddit interest groups and ask questions or help others while keeping my anonymity intact.",
  "explicit", ["C003"],
  [ev("DOC027:T005", "And I can join those interest groups and ask like, maybe a question, or maybe help other people. And all of this while be while maintaining my anonymity")],
  rationale="受访者明确把“保持匿名”与“加入兴趣组提问/帮助他人”绑定为使用 Reddit 的方式与结果。",
  supported=["加入兴趣组", "提问或帮助他人", "保持匿名"])

g("G004",
  "Search interest-group communities on Reddit to find answers to my specific questions, preferring Reddit over the open internet.",
  "explicit", ["C004", "C025", "C026", "C027"],
  [ev("DOC027:T005", "I can almost always like find different kind of questions or different kind of issues that I'm stuck in"),
   ev("DOC027:T057", "So that's why I just go to Reddit to like, figure out whatever question I want to ask.")],
  context=["answers are not guaranteed for very niche situations where no one has posted"],
  rationale="T005/T053 说明在 subreddit 搜索具体问题并获得推荐，T057 明确选定的方式是直接去 Reddit 而非开放互联网；T055 的“小众情境可能没人回答”作为限制保留在 context，未夸大为总是可得。",
  supported=["按具体问题在 subreddit 检索", "以 Reddit 而非通用搜索为主要渠道", "小众情境可能无答案（限制）"])

g("G005",
  "Get news about what is happening back in India even when the platform feed is set to my current location in the US.",
  "inferred", ["C006"],
  [ev("DOC027:T009", "But if but if I wanna get to know about the news or the things that are happening back in India, then that might not be possible, because Twitter is kind of now set to my location in us.")],
  context=["feed follows the current geolocation"],
  inference={"basis_candidate_ids": ["G001"],
              "reason": "受访者已把 Twitter 当作获取全球动态的工具（G001），此处说明地理定位使其看不到印度本地新闻，由此推断其希望按关注地区获取新闻。",
              "assumptions": ["所在地与关注地区不一致是持续状态，而非一次性举例"]},
  label="inferred",
  rationale="原文只有抱怨（定位导致看不到印度新闻），没有直接提出功能要求；“希望按地区看新闻”是由其既有新闻获取目标与抱怨正面推断，故记 inferred，强度按偏好处理。",
  supported=["定位绑定导致无法看到来源地区新闻（障碍）", "对来源地区新闻有需求（推断）"])

g("G006",
  "Require authentication on every social media platform so that no one else can access my accounts.",
  "explicit", ["C007"],
  [ev("DOC027:T011", "is authentication, because I don't want anyone else accessing my accounts on any social media platforms.")],
  context=["stated as the most important feature"],
  rationale="原句明确把 authentication 列为最重要的功能，并给出结果性理由（不希望他人访问任何平台上的账号）；主体、范围（所有平台）与强度（最重要）均保留。",
  supported=["认证为最重要功能", "任何他人都不能访问我的账号", "适用于所有社交平台"])

g("G007",
  "Keep my tweets and posts online until I delete or archive them myself.",
  "explicit", ["C008"],
  [ev("DOC027:T013", "they should be there until, and unless I delete them or I archive them.")],
  rationale="原句用 should 明确规定内容保留期限由本人删除/归档决定，条件（until unless）与否定（不自动消失）均在目标中。",
  supported=["内容持续在线", "仅由本人删除或归档后移除"])

g("G008",
  "Keep platform outages sporadic rather than regular, because regular outages would make me leave the service.",
  "explicit", ["C009"],
  [ev("DOC027:T013", "I don't want those outages to be that often, if they are like sporadic, I'm fine with it, but if they are too regular, then they might lose me as a customer")],
  context=["sporadic outages are explicitly acceptable"],
  rationale="原句给出可接受边界（偶发可以）与不可接受边界（过于频繁），并说明后果（流失）；未把“零故障”写成要求。",
  supported=["不接受过于频繁的中断", "偶发中断可接受", "后果为流失用户"])

g("G009",
  "Require the long saved backup code when I log in from a new device or start a new web session, so that only I can reach the account.",
  "inferred", ["C010"],
  [ev("DOC027:T021", "whenever you try to log back in from a new device. Or let's say you start a new session on your on your web app for the same particular for the same signal application it will ask you to give you the backup code that it gave you for the 1st time you logged in"),
   ev("DOC027:T023", "that kind of makes me feel like my particular account cannot be accessed by anyone else other than me. because I have those particular code.")],
  context=["backup code is a 16-30 digit code kept in a digital vault"],
  inference={"basis_candidate_ids": ["G006"],
              "reason": "受访者把 Signal 的备份码机制作为正面范例，说明它让其相信账号只有自己能访问；这是为满足“他人不得访问账号”而明确选定的方式。",
              "assumptions": ["受访者希望其他平台采用同类新设备二次验证，而不只是在描述 Signal"]},
  label="inferred",
  rationale="原文是对 Signal 机制的描述与赞许，没有直接要求其他平台照做；“在新设备/新会话要求备份码”是由其账号保护目标与所称信任感推断，故记 inferred 并保留方式（长备份码、保存于密码库）。",
  supported=["新设备或新会话需二次验证", "验证凭据为长期保存的备份码", "目的为只有本人可访问账号"])

g("G010",
  "Stay signed in after the first login until I log out myself or switch devices.",
  "inferred", ["C014"],
  [ev("DOC027:T033", "I'm almost always logged in into my system into my account, basically. But by some means, if I get logged out, which is rare on Reddit.")],
  inference={"basis_candidate_ids": ["G006"],
              "reason": "受访者把“几乎总是已登录、被登出很少见”描述为常态，并只把登出当作异常补救；由此推断其希望维持登录状态。",
              "assumptions": ["“几乎总是登录”是可维持的偏好，而非仅陈述现状"]},
  label="inferred",
  rationale="原句是现状描述（几乎总是登录、很少被登出），没有明说要求；维持登录的意图由现状与其“罕见/例外”的表述正面推断，强度按偏好处理。",
  supported=["常态为保持登录", "登出为罕见例外"])

g("G011",
  "Encrypt my conversations so that people I do not know cannot read my texts and conversations with friends.",
  "explicit", ["C017", "C022"],
  [ev("DOC027:T039", "I don't want other people to other people as in the people that I don't even know like kind of like see through my text or my conversation with my friends."),
   ev("DOC027:T047", "Like especially data encryption.")],
  rationale="T039 明确主体（不认识的人）、对象（与朋友的文本/对话）和否定（不能被看穿），T047 把 data encryption 列为第一要求，二者同一诉求（对话私密性）合并。",
  supported=["陌生他人不可读取我的对话", "以加密为手段", "适用于与朋友的私聊"])

g("G012",
  "Stop ads being targeted at me on Google and other apps just because I mentioned something once in a conversation.",
  "explicit", ["C012", "C044"],
  [ev("DOC027:T101", "And I'll use that wand to. To make these social media apps to use basic human judgment and not just throw random ads at me just because I said that one particular name."),
   ev("DOC027:T029", "And the next day I like start seeing these ads on Google and any other like search engines that like about my about like a refrigerator or something")],
  context=["ads currently follow a single mentioned item across apps"],
  rationale="T101 以“魔法棒”愿望形式明确要求不要因为提到某个名字就乱投广告，T029 给出具体现象（对话后 Google 出现冰箱广告）；合并为同一结果（不得由一次提及触发定向广告）。",
  supported=["不得因一次提及就定向投放广告", "跨应用（Google/搜索引擎）范围"])

g("G013",
  "Cap ads for something I may want at about two and stop showing them once I skip them.",
  "explicit", ["C020", "C045", "C019"],
  [ev("DOC027:T103", "So kind of like, find a balance like, okay, maybe this person wants to buy a refrigerator. So let's just give them 2 ads. And if they skip those ads, then we will stop showing refrigerator ads."),
   ev("DOC027:T045", "I don't want to see the same kind of ads over and over again, just because I talked about it one time.")],
  context=["ads are occasionally helpful when I am actually buying something, though rarely"],
  rationale="T103 给出明确数量（2 条）与停止条件（跳过即停），T045 给出同一抱怨；T043 的让步（真正想买时偶有帮助）作为例外保留在 context，未把广告一禁了之。",
  supported=["重复次数上限约为两条", "用户跳过后停止展示", "广告在真正购物时偶有帮助（例外）"])

g("G014",
  "Keep content loading continuously as I scroll, so I do not miss posts when the feed stalls and I have to refresh from the top.",
  "explicit", ["C021", "C023"],
  [ev("DOC027:T047", "the lack of content like whenever I scroll through like reddit or twitter. At 1 point there will be like kind of like a lag where the data isn't being loaded or the."),
   ev("DOC027:T049", "maybe I just missed one particular post or one particular item")],
  rationale="T047 指出滚动时加载停滞，T049 说明补救（回顶部刷新）与担心（漏掉帖子）；同一结果（连续加载、不漏内容）合并，未虚构速度指标。",
  supported=["滚动时持续加载", "避免因停滞而漏掉帖子"])

g("G015",
  "Show me an assortment of different content rather than the same stream of content the algorithm thinks I like.",
  "explicit", ["C037", "C038", "C039", "C040"],
  [ev("DOC027:T087", "I want like an assortment of content, not just one particular stream of content."),
   ev("DOC027:T079", "whereas I want to be shown like different kind of content")],
  context=["when I want a single stream I go to a specific channel or group myself"],
  rationale="T079/T081/T087/T089 反复表达同一结果（要多样化内容、不要算法重复推送同类），并给出例外（想专一时自己去找特定组）；合并为一个目标，例外写入 context。",
  supported=["要不同类型的内容", "不要重复同类内容", "需要单一主题时自行进入特定组（例外）"])

g("G016",
  "Keep my Twitter feed from being dominated by one account's posts, such as every fifth tweet being Elon Musk's, so my view is not biased.",
  "inferred", ["C041", "C042"],
  [ev("DOC027:T095", "the moment I open twitter, the 1st thing that will that Twitter will show me is the latest Elon Musk's tweet, and every 5th tweet is Elon Musk's tweet. So that kind of actually creates a bias on my mind"),
   ev("DOC027:T097", "that would easily just make me inclined towards whatever Elon Musk is saying, because I like that particular platform")],
  inference={"basis_candidate_ids": ["G015"],
              "reason": "受访者已提出要多样化内容、不要单一流（G015），此处把“某一个人占据信息流”视为造成偏见的同类问题，由此推断其希望限制单一账号的支配。",
              "assumptions": ["反对的是单一账号占比过高，而非反对该账号本身"]},
  label="inferred",
  rationale="原文陈述现象（首条与每第五条都是同一人）并称其造成 bias，但没有提出明确要求；“限制单一账号支配信息流”由多样性目标正面推断，故记 inferred。",
  supported=["单一账号占据信息流（现象）", "造成观点偏见（后果）"])

g("G017",
  "Filter authentic from inauthentic content so that I am not misinformed by social media, and revise my opinion when the actual truth differs.",
  "inferred", ["C043"],
  [ev("DOC027:T099", "I can kind of easily filter out what is authentic and what is not authentic. And in that way I'm never misinformed because of social media.")],
  inference={"basis_candidate_ids": ["G020"],
              "reason": "受访者的核心动机是不错过世界大事（G020）；此处把“不被社交媒体误导”描述为达成该动机的前提，故推断其希望维持这一状态。",
              "assumptions": ["“never misinformed”被理解为期望维持的结果，而非纯事实断言"]},
  label="inferred",
  rationale="原句更像对自身辨别能力的自评（can easily filter），但落脚在“因此从不被误导”的期望状态；按维持意图推断为 inferred，并保留“愿意据事实修正观点”的条件。",
  supported=["辨别内容真实性（自评能力）", "不被误导（期望状态）", "愿按事实修正观点"])

g("G018",
  "Keep all my social media credentials in a digital vault on my phone so that I can track the accounts and do not lose my account details.",
  "inferred", ["C031"],
  [ev("DOC027:T065", "So I do have like a a digital vault that I keep on my phone which helps me to keep. Keep a track of all the accounts, my credentials for all the social networking platforms."),
   ev("DOC027:T065", "if I lose that particular vault then it'll probably I'll probably end up losing most of my account details")],
  inference={"basis_candidate_ids": ["G006"],
              "reason": "账号保护（G006）依赖凭据不丢失；受访者称数字保险库“kind of important”并指出丢失后果，故推断其希望维持集中保管。",
              "assumptions": ["受访者希望继续使用现有保险库，而非只是描述现状"]},
  label="inferred",
  rationale="原句描述现有做法与其重要性，未直接提出要求；“集中保管凭据以免丢失”由现状与丢失后果正面推断，故记 inferred，方式（手机上的数字保险库）保留在目标中。",
  supported=["凭据集中存放于手机数字保险库", "避免丢失账号信息"])

g("G019",
  "Have my saved credentials autofilled when I log in to a social media web page, so that I only have to press login.",
  "inferred", ["C032", "C033"],
  [ev("DOC027:T069", "That, and it'll Autofill everything for me, and I just have to press login. and that is pretty much it."),
   ev("DOC027:T067", "wherever I log into any any like social media. A web page there will be like a pop up which says that this is my user")],
  inference={"basis_candidate_ids": ["G018"],
              "reason": "受访者以正面语气描述密码管理器的自动填充流程（“pretty much it”），这是其凭据管理做法的具体使用方式，故推断其希望保留自动填充。",
              "assumptions": ["“方便/可靠”的评价被理解为希望继续使用，而非纯流程描述"]},
  label="inferred",
  rationale="原文描述当前登录流程（弹窗提示用户名、自动填充、按登录），没有明说要求；自动填充的意图由其对密码管理器“quite reliable”的评价推断，故记 inferred，强度按偏好。",
  supported=["登录页弹出已保存的用户名", "自动填充凭据", "仅需按登录"])

g("G020",
  "Stay connected to the world so that I do not miss that something big has happened.",
  "explicit", ["C034"],
  [ev("DOC027:T075", "I wouldn't like the fact that something really big has happened, and I just didn't. I just did not know about it like that won't be a feeling that I would want to experience."),
   ev("DOC027:T075", "That's 1 of my biggest motivation to be on like different social media platforms, so that I know what's happening in the world.")],
  rationale="受访者明确称这是使用多个平台的最大动机之一，并给出结果（知道世界发生了什么、不想错过大事）；主体、范围（世界范围）与强度（最大动机之一）保留。",
  supported=["知道世界发生了什么", "不愿错过重大事件", "为使用多平台的主要动机"])

g("G021",
  "Know what is happening in my friend circle, with my friends back in India, and around me on campus and in class.",
  "explicit", ["C035", "C036"],
  [ev("DOC027:T075", "It's also about knowing what's happening in my friend Circle, or with the with my friends back in India."),
   ev("DOC027:T077", "Let's say, what's happening on campus, what's happening in class. what's happening like with my classmates stuff like that stuff that are like non verbal, but can be shared through like social networking apps.")],
  context=["includes non-verbal things that can only be shared through social apps"],
  rationale="T075/T077 明确列出关心的范围（朋友圈、印度朋友、校园、班级、同学）与其性质（非全球、可为非语言信息）；合并为同一“知悉身边动态”的状态目标。",
  supported=["知悉朋友圈与印度朋友动态", "知悉校园与班级动态", "包含非语言型信息"])

g("G022",
  "Open threads about events that interest me, such as campus events, from my aggregated Reddit homepage feed.",
  "inferred", ["C016", "C015"],
  [ev("DOC027:T037", "So I'll probably I'm right now interested about that, so I'll probably click that I'll go through the threads that are happening."),
   ev("DOC027:T035", "the question is highlighted. or like whoever is asking the question, of course, like in anonymous way. And the if you, if you want to see the answers or the responses to that particular question, you'll probably have to tap that particular card")],
  context=["homepage aggregates posts from the subreddits I joined"],
  inference={"basis_candidate_ids": ["G021"],
              "reason": "受访者描述从聚合首页点开校园事件帖子的常规做法，其动机与前文所述“想知道校园/班级发生什么”（G021）一致，故推断这是为知悉身边动态而进行的动作。",
              "assumptions": ["该浏览习惯被理解为持续使用方式，而非一次性叙述"]},
  label="inferred",
  rationale="原文是使用流程描述（滚动首页、点开感兴趣的帖子），没有直接要求；其目的可由 G021 的既述动机推断，故记 inferred，并保留“标题即问题、点击进入讨论串”的方式。",
  supported=["从聚合首页点开感兴趣的帖子", "进入该问题的讨论串"])

g("G023",
  "Use one common platform I design myself that gathers content from my favorite apps in one place, so that I do not waste time switching between apps.",
  "explicit", ["C046", "C047"],
  [ev("DOC027:T105", "So I'd say that I would be really happy if there was like this common platform which. Like I can design for myself."),
   ev("DOC027:T107", "Because I kind of like waste a lot of time just switching between apps which I don't want. I just want to open 1 1 app and get all the content and be done with it.")],
  context=["content comes from Twitter, Reddit and Instagram; I choose which apps to add"],
  rationale="T105 明确表达愿望（会很开心有这样一个可自选的公共平台并汇总各应用内容），T107 给出结果（不必在应用间切换、节省时间）；方式（自选添加哪些应用）保留在 context。",
  supported=["单一自选聚合平台", "汇总多个应用的精选内容", "避免在应用间切换耗时"])

# ---------------- ledger ----------------
entries = []


def entry(cid, disp, gids, reason):
    entries.append({"candidate_id": cid, "disposition": disp, "final_goal_ids": gids, "reason": reason})


entry("C001", "keep", ["G001"], "Twitter 作为新闻入口、点 hashtag 看全球动态，直接成为 G001 主体动作。")
entry("C002", "keep", ["G002"], "Snapchat 即时收发照片/视频以保持实时联系，单独成目标。")
entry("C003", "keep", ["G003"], "匿名 + 兴趣组提问/帮助他人为同一结果，成 G003。")
entry("C004", "keep", ["G004"], "在 subreddit 检索具体问题并取得答案是 G004 的核心动作。")
entry("C005", "exclude", [], "各国平台流行度的事实陈述，未表达希望达到的状态；不构成目标。")
entry("C006", "keep", ["G005"], "定位导致看不到印度新闻的抱怨，推断为按关注地区获取新闻，保留障碍条件。")
entry("C007", "keep", ["G006"], "认证最重要且他人不得访问账号，成 G006。")
entry("C008", "keep", ["G007"], "内容保留到本人删除/归档，成 G007。")
entry("C009", "keep", ["G008"], "中断频率要求（偶发可接受、过频流失），成 G008。")
entry("C010", "keep", ["G009"], "备份码 2FA 与新设备/新会话重验证为同一机制，合并为 G009。")
entry("C011", "exclude", [], "平台优先级排序是偏好表达，未提出需达到的结果；其内容（匿名、加密）已由 G003/G011 承接。")
entry("C012", "keep", ["G012"], "对话后跨应用出现定向广告，成 G012。")
entry("C013", "merge", ["G001"], "同一 Twitter 新闻动作的补充说明（科技新闻、梗、追趋势），与 C001 同义合并。")
entry("C014", "keep", ["G010"], "几乎总是已登录、被登出罕见，推断为维持登录，成 G010。")
entry("C015", "merge", ["G022"], "点击问题卡片进入讨论串是 G022 的同一浏览动作，合并。")
entry("C016", "keep", ["G022"], "滚动聚合首页并点开感兴趣事件帖子，成 G022。")
entry("C017", "keep", ["G011"], "陌生人不可读到与朋友的对话，成 G011。")
entry("C018", "exclude", [], "片段式抱怨（give ads to me around），语义不完整；同诉求已由 C020/C045 更完整表达。")
entry("C019", "merge", ["G013"], "广告偶有帮助的让步，作为 G013 的例外条件保留，不另立目标。")
entry("C020", "keep", ["G013"], "不要因一次提及就反复看到同类广告，成 G013 主诉求。")
entry("C021", "keep", ["G014"], "滚动时加载停滞，成 G014。")
entry("C022", "merge", ["G011"], "data encryption 为 G011 同一隐私诉求的强调，合并保留“加密”方式。")
entry("C023", "merge", ["G014"], "回顶部刷新与漏帖担忧是 G014 的补救与后果，合并。")
entry("C024", "exclude", [], "残句“than just loading in the right time”，无法确定独立意图。")
entry("C025", "merge", ["G004"], "搜索具体信息（餐厅推荐）为 G004 的同一检索动作，合并。")
entry("C026", "merge", ["G004"], "小众情境拿不到答案属 G004 的限制条件，写入 context，不另立目标。")
entry("C027", "merge", ["G004"], "优先去 Reddit 而非开放互联网是 G004 的选定渠道，合并。")
entry("C028", "exclude", [], "向新人解释概念（凭据、账号）的教学性表述，非产品诉求。")
entry("C029", "exclude", [], "术语归类说明（tweet 属 post），非产品诉求。")
entry("C030", "exclude", [], "术语说明（posts 是首页主要内容），非产品诉求。")
entry("C031", "keep", ["G018"], "数字保险库集中保管凭据、避免丢失，成 G018。")
entry("C032", "keep", ["G019"], "登录页弹窗提示已保存用户名，成 G019。")
entry("C033", "merge", ["G019"], "自动填充只需按登录，是 G019 同一流程的另一句描述，合并。")
entry("C034", "keep", ["G020"], "不愿错过世界大事、知晓世界动态为使用动机，成 G020。")
entry("C035", "keep", ["G021"], "知悉朋友圈与印度朋友动态，成 G021。")
entry("C036", "merge", ["G021"], "校园/班级/同学动态为 G021 同一范围的补充，合并。")
entry("C037", "keep", ["G015"], "希望看到不同类型内容而非算法重复推送，成 G015。")
entry("C038", "merge", ["G015"], "不要只反复推食物内容为 G015 同一诉求，合并。")
entry("C039", "merge", ["G015"], "要 assortment 而非单一流，并保留“想专一时自己去特定组”的例外，合并。")
entry("C040", "merge", ["G015"], "“要什么都有一些”与 C039 同义，合并。")
entry("C041", "keep", ["G016"], "信息流被单一账号支配并造成偏见，成 G016。")
entry("C042", "merge", ["G016"], "对偏见后果的信念，作为 G016 的支持与后果保留，合并。")
entry("C043", "keep", ["G017"], "辨别真伪、不被误导并愿修正观点，成 G017。")
entry("C044", "merge", ["G012"], "以“人的判断”替代按名字乱投广告，与 C012 同一结果，合并。")
entry("C045", "merge", ["G013"], "两条广告后跳过即停的机制，与 C020 同一诉求，合并并保留数量与停止条件。")
entry("C046", "keep", ["G023"], "自选公共平台汇总多应用内容，成 G023。")
entry("C047", "merge", ["G023"], "打开一个应用拿全部内容、避免切换耗时，是 G023 的同一结果，合并。")

# source checks
source_checks = [
    {"check_id": "S1",
     "evidence_candidates": [{"source_id": "DOC027:T005",
                              "quote": "I have like different kind of social media apps that kind of cater to different needs of mind."}],
     "candidate_ids": ["C001", "C002", "C003", "C004"], "final_goal_ids": ["G001", "G002", "G003", "G004"],
     "outcome": "represented",
     "reason": "回查 T005 整段：受访者按平台列出的四类需求（新闻、实时联系、匿名、找答案）分别对应 G001-G004，未把“每个平台一个需求”压成单一目标。"},
    {"check_id": "S2",
     "evidence_candidates": [{"source_id": "DOC027:T013",
                              "quote": "they should be there until, and unless I delete them or I archive them."}],
     "candidate_ids": ["C008"], "final_goal_ids": ["G007"], "outcome": "represented",
     "reason": "回查 T012-T013 跨轮句子：否定（不神秘消失）由 T013 的 until/unless 条件句承接，未误写成永久保留。"},
    {"check_id": "S3",
     "evidence_candidates": [{"source_id": "DOC027:T021",
                              "quote": "it will ask you to give you the backup code that it gave you for the 1st time you logged in"}],
     "candidate_ids": ["C010"], "final_goal_ids": ["G009"], "outcome": "represented",
     "reason": "核对 T019/T021/T023 三处：备份码作为 2FA、新设备/新会话要求、以及信任结果，均进入 G009；未把 Signal 的其他功能当作要求。"},
    {"check_id": "S4",
     "evidence_candidates": [{"source_id": "DOC027:T043",
                              "quote": "it's kind of helpful sometimes when I actually want to like buy something, and it gives me those ads, but that's rare"}],
     "candidate_ids": ["C019"], "final_goal_ids": ["G013"], "outcome": "represented",
     "reason": "核对让步句：广告偶有帮助限定为“真正想买时且罕见”，作为 G013 的例外保留，避免把广告一律禁止。"},
    {"check_id": "S5",
     "evidence_candidates": [{"source_id": "DOC027:T055",
                              "quote": "I probably wouldn't get any answers for that."}],
     "candidate_ids": ["C026"], "final_goal_ids": ["G004"], "outcome": "represented",
     "reason": "核对限制句：小众情境可能拿不到答案，写入 G004 的 context 作为限制，未夸大为总是可得。"},
    {"check_id": "S6",
     "evidence_candidates": [{"source_id": "DOC027:T041", "quote": "Also like then on top of that give ads to me around."},
                             {"source_id": "DOC027:T051", "quote": "Than just loading in the right time."}],
     "candidate_ids": ["C018", "C024"], "final_goal_ids": [], "outcome": "excluded",
     "reason": "两处均为跨轮断句的残片，单独无法判断主体与结果；同主题已有更完整候选，故排除并保留原文。"},
    {"check_id": "S7",
     "evidence_candidates": [{"source_id": "DOC027:T083",
                              "quote": "it thinks that what you're doing is what you will still like in the future"}],
     "candidate_ids": [], "final_goal_ids": ["G015", "G016"], "outcome": "represented",
     "reason": "核对算法解释段（T083/T085）属信念陈述：仅作为多样性诉求的背景解释，未当作已证事实，也未据此新增目标。"},
    {"check_id": "S8",
     "evidence_candidates": [{"source_id": "DOC027:T099",
                              "quote": "I can kind of easily filter out what is authentic and what is not authentic."}],
     "candidate_ids": ["C043"], "final_goal_ids": ["G017"], "outcome": "uncertain",
     "reason": "该句是能力自评，是否构成“要求”仍有歧义；保留为 inferred 目标并列入待确认问题。"},
    {"check_id": "S9",
     "evidence_candidates": [{"source_id": "DOC027:T045",
                              "quote": "I don't want to see the same kind of ads over and over again, just because I talked about it one time."},
                             {"source_id": "DOC027:T103",
                              "quote": "let's just give them 2 ads. And if they skip those ads, then we will stop showing refrigerator ads."}],
     "candidate_ids": ["C020", "C045"], "final_goal_ids": ["G013"], "outcome": "represented",
     "reason": "核对两处广告诉求是否同一：一为重复次数，一为数量上限与停止条件，合并后两条均保留在目标与 context。"},
    {"check_id": "S10",
     "evidence_candidates": [{"source_id": "DOC027:T009",
                              "quote": "because Twitter is kind of now set to my location in us"}],
     "candidate_ids": ["C006"], "final_goal_ids": ["G005"], "outcome": "uncertain",
     "reason": "地理定位限制为抱怨，是否要求产品按关注地区提供新闻不确定，故推断为目标并列入待确认问题。"},
]

window_results_p1 = [{"window_id": w, "status": "processed", "reason": ""} for w in WIN_IDS]
window_results_p2 = [{"window_id": w, "status": "processed", "reason": "全篇校正回查指代、条件继承与相反证据"} for w in WIN_IDS]

ledger = {
    "model": "unknown", "temperature": "unknown", "budget": "1 initial pass + <=2 repair rounds",
    "usage": "unknown",
    "skill_revision": "a5952d426b1624a3fcb2ce2829e1ae1ceb15e19dc3309d9571f3bc6b465deb6f",
    "prompt_revision": "task-prompt-v1",
    "planned_passes": 2,
    "stop_reason": "完成 1 轮逐窗捕获（55 窗口）+ 1 轮全篇校正后，新增候选已归入既有簇，连续补查无新有据意图，停止并保留待确认问题。",
    "passes": [
        {"pass_id": "P1", "kind": "initial", "context": "isolated", "status": "completed", "window_results": window_results_p1},
        {"pass_id": "P2", "kind": "full_context", "context": "isolated", "status": "completed", "window_results": window_results_p2},
    ],
    "full_context_review": {"status": "completed", "reason": "逐窗记录后回读全部 111 轮：核对跨轮指代（T011→T012/T013 的 data、T019→T021→T023 的备份码）、问答范围（T024/T027 平台排序、T058 术语解释）、让步（T043 广告偶有帮助）、例外（T087 想专一时自行进组）与相反证据（T099 自称不被误导 vs T095 承认受偏见影响）；据此把 C013/C015/C022/C033/C036/C038/C040/C042/C047 归并到既有目标。"},
    "entries": entries,
    "source_checks": source_checks,
}

# ---------------- decisions ----------------
relations = [
    {"relation_id": "R1", "source_id": "G009", "target_id": "G006", "type": "operationalization",
     "status": "supported", "conditions": [], "assumptions": ["其他平台可采用同类新设备验证机制"],
     "rationale": "新设备/新会话要求备份码是受访者为“只有本人能访问账号”明确选定的实现方式，方向为实现方式→目的。",
     "evidence_ids": [],
     "evidence_quotes": [{"source_id": "DOC027:T023",
                          "quote": "that kind of makes me feel like my particular account cannot be accessed by anyone else other than me. because I have those particular code.",
                          "role": "basis"}]},
    {"relation_id": "R2", "source_id": "G001", "target_id": "G020", "type": "specialization",
     "status": "supported", "conditions": [], "assumptions": [],
     "rationale": "G001 是“通过 Twitter 趋势看全球动态”的具体情境目标，G020 是“知道世界发生了什么”的一般目标；T075 明确把使用多平台（含 Twitter 新闻用途）说成为了解世界。",
     "evidence_ids": [],
     "evidence_quotes": [{"source_id": "DOC027:T075",
                          "quote": "That's 1 of my biggest motivation to be on like different social media platforms, so that I know what's happening in the world.",
                          "role": "basis"}]},
    {"relation_id": "R3", "source_id": "G002", "target_id": "G021", "type": "specialization",
     "status": "supported", "conditions": [], "assumptions": [],
     "rationale": "G002 是借助 Snapchat 与朋友实时联系的具体目标，G021 是知悉朋友圈动态的一般目标，T075 明确把“朋友圈、印度朋友”列为所关心的连接内容。",
     "evidence_ids": [],
     "evidence_quotes": [{"source_id": "DOC027:T075",
                          "quote": "It's also about knowing what's happening in my friend Circle, or with the with my friends back in India.",
                          "role": "basis"}]},
    {"relation_id": "R4", "source_id": "G022", "target_id": "G021", "type": "contribution",
     "status": "supported", "conditions": [], "assumptions": ["相关事件在 subreddit 有帖子"],
     "rationale": "从聚合首页点开校园事件帖子有助于知悉校园/班级动态，但不保证覆盖全部身边信息，故为贡献而非精化。",
     "evidence_ids": [],
     "evidence_quotes": [{"source_id": "DOC027:T037",
                          "quote": "let's say I'm in a university's subreddit. And there's like some kind of like event happening.",
                          "role": "basis"}]},
    {"relation_id": "R5", "source_id": "G023", "target_id": "G015", "type": "contribution",
     "status": "supported", "conditions": [], "assumptions": ["各平台内容可按受访者选择汇入"],
     "rationale": "单一聚合平台把 Twitter/Reddit/Instagram 的精选内容汇到一处，有助于获得多样化内容，但多样性还取决于各源内容本身，故为贡献。",
     "evidence_ids": [],
     "evidence_quotes": [{"source_id": "DOC027:T105",
                          "quote": "and give me, like an assortment of different kind of content, let's say, some good content from Twitter, some good content from Reddit, some good content from Instagram, and give it all in one place",
                          "role": "basis"}]},
]

groups = [
    {"group_id": "GR1", "parent_id": "G021", "child_ids": ["G002", "G022"], "kind": "and",
     "status": "proposed", "completeness": "partial",
     "rationale": "G002（与朋友实时分享近况）与 G022（从聚合首页点开校园/班级事件帖子）共同覆盖“知悉朋友圈与身边动态”；但两条路径都依赖对方在平台上留下内容，无法声称整组充分。",
     "assumptions": ["朋友圈与校园同学分别至少在一处使用 Snapchat 或 Reddit 发帖"],
     "evidence_ids": [],
     "evidence_quotes": [{"source_id": "DOC027:T077",
                          "quote": "Let's say, what's happening on campus, what's happening in class.",
                          "role": "basis"}],
     "relation_ids": ["R3", "R4"],
     "checks": [
         {"kind": "normal", "origin": "analysis_assumption",
          "scenario": "朋友在 Snapchat 即时发照片、校园事件在 subreddit 有帖子：两类信息都能进入受访者视野",
          "outcome": "supports", "rationale": "两条路径分别覆盖朋友近况与校园事件，合起来满足知悉身边动态的常见情形。"},
         {"kind": "exception", "origin": "analysis_assumption",
          "scenario": "朋友只在见面或电话里讲述某事，或校园事件没有任何帖子：两条路径都拿不到该信息",
          "outcome": "counterexample", "rationale": "存在未被这两个子目标覆盖的信息来源，故整组不满足充分性，保留 proposed/partial。"},
     ]},
]

questions = [
    {"target_type": "goal", "target_id": "G005",
     "message": "按关注地区（印度）看新闻是明确的产品要求，还是仅对当前定位限制的抱怨？"},
    {"target_type": "group", "target_id": "GR1",
     "message": "朋友圈/校园信息若只通过线下或电话传播，是否还需要其他子目标才能覆盖？"},
    {"target_type": "goal", "target_id": "G016",
     "message": "“单一账号占据信息流”是否只是 G015 多样性诉求的一个实例，应合并为一个目标？"},
    {"target_type": "goal", "target_id": "G017",
     "message": "“从不被误导”是受访者的自我能力评估还是对平台的要求？若为后者需要何种辨别机制？"},
    {"target_type": "goal", "target_id": "G019",
     "message": "自动填充是希望保留的便利，还是仅描述现有密码管理器的使用流程？"},
    {"target_type": "model", "target_id": "DOC027-goal-model",
     "message": "同一诉求分散在多个平台（Twitter 新闻、Reddit 问答、Snapchat 联系），目标是否应按平台再分层，而不是保持平台无关表述？"},
]

review_questions = [
    {"candidate_ids": ["G005", "G016", "G017", "G019"],
     "question": "这四个目标均由现状/抱怨/自评推断而来，是否应保留为正式目标还是降为背景信息？",
     "reason": "它们缺少直接的“希望/要求”措辞，强度可能被高估。"},
    {"candidate_ids": ["G015", "G016"],
     "question": "“内容多样”与“不被单一账号支配”是否应合并为一个目标？",
     "reason": "两者对象不同（主题重复 vs 单一账号占比），但结果相近，存在重复建点风险。"},
    {"candidate_ids": ["G004"],
     "question": "“找答案”目标是否应把“小众情境通常无答案”写成明确的失败容忍条件？",
     "reason": "原文只说明现状困难，未给出可接受的替代方案。"},
]

limitations = [
    "原文为口语访谈转写，含断句、重复与残片（如 T041、T051），个别片段无法判断独立意图，已按覆盖记录排除并保留原文。",
    "T012/T013、T019/T021/T023 等跨轮句子按同一说话人连续语流理解，未做逐字合并。",
    "G005/G010/G016/G017/G018/G019/G022 为推断目标，强度按偏好/现状处理，未升级为强制要求。",
    "本轮只做生成方自检，未执行独立语义评审与形式证明。",
]

spec = {
    "document_id": "DOC027",
    "raw_candidates": raw,
    "goals": [{k: v for k, v in item.items() if k != "_cands"} for item in goals],
    "review_questions": review_questions,
    "limitations": limitations,
    "ledger": ledger,
    "decisions": {"relations": relations, "groups": groups, "questions": questions, "reassessments": []},
}

if errors:
    print("EVIDENCE ERRORS:")
    for e in errors:
        print(" -", e)
    raise SystemExit(1)

(ROOT / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")
print("candidates", len(raw), "goals", len(goals), "relations", len(relations), "groups", len(groups))
print("entries", len(entries), "checks", len(source_checks))
