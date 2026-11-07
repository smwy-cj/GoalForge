# -*- coding: utf-8 -*-
"""Author spec.json for DOC027: content is authored here, harness only binds offsets."""
import json
import sys
from pathlib import Path

A = Path(__file__).resolve().parents[1]
src = json.loads((A / "source/DOC027.json").read_text(encoding="utf-8"))
TEXT = {t["source_id"]: t["text"] for t in src["turns"]}

problems = []


def ev(sid, quote, role="basis"):
    if sid not in TEXT:
        problems.append(("missing turn", sid, quote))
        return {"source_id": sid, "quote": quote, "role": role}
    n = TEXT[sid].count(quote)
    if n != 1:
        problems.append((f"hits={n}", sid, quote))
    return {"source_id": sid, "quote": quote, "role": role}


C = []


def cand(cid, statement, modality, origin, ctx, evidence):
    C.append({"candidate_id": cid, "statement": statement, "actor": "Stakeholder",
              "modality": modality, "context": ctx, "origin": origin, "pass_id": "P1",
              "evidence": evidence})


cand("C001",
     "Use Twitter as my go-to news app because its trending hashtags let me go through everything happening around the world.",
     "explicit preference", "explicit", [],
     [ev("DOC027:T005", "Twitter is kind of like my go to news app because there are a lot of trends that are happening around the world")])

cand("C002",
     "Use Snapchat to stay connected with my friends in real time by sending photos and videos instantaneously.",
     "explicit purpose", "explicit", [],
     [ev("DOC027:T005", "It's very easy for me to connect to stay connected to my friends in real time.")])

cand("C003",
     "Join Reddit interest groups, ask questions or help other people, while keeping my anonymity intact.",
     "explicit preference", "explicit", [],
     [ev("DOC027:T005", "And I can join those interest groups and ask like, maybe a question, or maybe help other people. And all of this while be while maintaining my anonymity")])

cand("C004",
     "Get to know the news and things happening back in India even though the Twitter feed is set to my location in the US.",
     "conditional wish with a stated obstacle", "explicit",
     ["feed geolocation set to the US"],
     [ev("DOC027:T009", "if I wanna get to know about the news or the things that are happening back in India, then that might not be possible, because Twitter is kind of now set to my location in us")])

cand("C005",
     "Have authentication as the most important feature so that nobody else can access my accounts on any social media platform.",
     "strong requirement ('most important')", "explicit", [],
     [ev("DOC027:T011", "because I don't want anyone else accessing my accounts on any social media platforms")])

cand("C006",
     "Keep my tweets and posts on the platform until I delete or archive them; they should not disappear on their own.",
     "explicit expectation", "explicit", [],
     [ev("DOC027:T013", "they should be there until, and unless I delete them or I archive them")])

cand("C007",
     "Have platform outages only sporadically rather than regularly; sporadic outages are acceptable but too regular outages would lose me as a customer.",
     "graded preference", "explicit", ["network conditions affect speed"],
     [ev("DOC027:T013", "I don't want those outages to be that often, if they are like sporadic, I'm fine with it, but if they are too regular, then they might lose me as a customer")])

cand("C008",
     "Keep the 2FA backup code saved, for example in a digital vault, so that only I can get back into the account.",
     "explicit requirement in the described practice", "explicit", [],
     [ev("DOC027:T019", "it will give you like a backup code, which is a really long, I don't know. Like maybe 16 to 30 digit code you have to keep it saved"),
      ev("DOC027:T023", "You have to keep it saved somewhere, maybe in like a digital vault or something.")])

cand("C009",
     "When selecting a platform, rank Reddit first for anonymity, Signal second for authentication, privacy and encryption, and Twitter third for news, tech news, memes and trends.",
     "present opinion, explicitly tentative", "explicit", ["'my present opinion'"],
     [ev("DOC027:T027", "reddit reddit kind of comes for most because of the anonymity that it provides the next will be signal because of like high authentication and privacy and data encryption"),
      ev("DOC027:T031", "And finally, it will be Twitter. Because right now, I I am really interested in learning about what is happening around the world.")])

cand("C010",
     "Open Reddit from the social-media folder, log back in with 2FA if logged out, scroll the homepage and tap into threads on interesting campus topics.",
     "description of a routine use sequence", "explicit", [],
     [ev("DOC027:T033", "the 1st one the 1st icon you'll see is reddit I'll click on that particular icon"),
      ev("DOC027:T035", "if you want to see the answers or the responses to that particular question, you'll probably have to tap that particular card")])

cand("C011",
     "Prevent people I do not know from seeing through my texts or my conversations with my friends.",
     "explicit frustration and wish", "explicit", [],
     [ev("DOC027:T039", "I don't want other people to other people as in the people that I don't even know like kind of like see through my text or my conversation with my friends")])

cand("C012",
     "Stop seeing the same kind of ads over and over just because I talked about a topic once, although ads are occasionally helpful when I actually want to buy something.",
     "explicit frustration with a stated exception", "explicit",
     ["ads can be helpful when actively shopping, but that is rare"],
     [ev("DOC027:T045", "I'm kind of like annoyed like I don't want to see the same kind of ads over and over again, just because I talked about it one time."),
      ev("DOC027:T043", "I've I've realized that it's kind of helpful sometimes when I actually want to like buy something, and it gives me those ads, but that's rare.")])

cand("C013",
     "Treat data privacy as the first priority, especially data encryption.",
     "explicit priority", "explicit", [],
     [ev("DOC027:T045", "So the 1st important thing is, I think, data privacy for me."),
      ev("DOC027:T047", "Like especially data encryption.")])

cand("C014",
     "Avoid missing posts when the feed stops loading mid-scroll and I have to jump back to the top to refresh.",
     "complaint about a workaround; desired state not stated directly", "inferred", [],
     [ev("DOC027:T049", "So it's easier for me to just go at like the top and then start like a new kind of like a refresh, instead of just like going through the same kind of my session. So that's kind of annoying, because I have to like go back up."),
      ev("DOC027:T049", "maybe I just missed one particular post or one particular item because")])

cand("C015",
     "Obtain information for particular situations by searching Reddit, and get recommendations and discussions from random people there.",
     "explicit practice", "explicit",
     ["the topic must already have Reddit discussions"],
     [ev("DOC027:T053", "whenever I wanna obtain information like out going out of my way, not not something that's already been displayed in my homepage. it's mostly when I am in a particular situation where I wanna search for something very particular"),
      ev("DOC027:T057", "I just go to Reddit to like, figure out whatever question I want to ask")])

cand("C016",
     "For a very niche situation, Reddit may have nobody who has been through it, so no answers would come back.",
     "stated limitation", "explicit", [],
     [ev("DOC027:T055", "I probably wouldn't get any answers for that.")])

cand("C017",
     "Explain to a new user the basic credentials, account, groups and content/posts as the important concepts of social media use.",
     "answer to a hypothetical teaching request", "explicit", [],
     [ev("DOC027:T059", "The 1st thing that I'll introduce to them is like their basic credentials and managing those credentials across all the social media platforms.")])

cand("C018",
     "Keep a digital vault on my phone that tracks all my accounts and credentials for every social networking platform, because losing it would mean losing most account details.",
     "current practice called important", "explicit", [],
     [ev("DOC027:T065", "I do have like a a digital vault that I keep on my phone which helps me to keep. Keep a track of all the accounts, my credentials for all the social networking platforms."),
      ev("DOC027:T065", "if I lose that particular vault then it'll probably I'll probably end up losing most of my account details")])

cand("C019",
     "Use Google Password Manager as a reliable tool that autofills the credentials and only leaves pressing login.",
     "positive report of an existing tool", "explicit", [],
     [ev("DOC027:T067", "It's quite reliable. And it usually like helps me to just like I can just tap in and whenever I log into any any like social media.")])

cand("C020",
     "Know what is happening in the world so that I do not miss something really big that happened.",
     "explicit motivation", "explicit", [],
     [ev("DOC027:T075", "That's 1 of my biggest motivation to be on like different social media platforms, so that I know what's happening in the world.")])

cand("C021",
     "Also know what is happening in my friend circle, with friends back in India, on campus and in class.",
     "explicit motivation", "explicit", [],
     [ev("DOC027:T075", "It's also about knowing what's happening in my friend Circle, or with the with my friends back in India."),
      ev("DOC027:T077", "Let's say, what's happening on campus, what's happening in class. what's happening like with my classmates stuff like that")])

cand("C022",
     "Be shown different kinds of content instead of the similar content Instagram keeps repeating after I like something.",
     "explicit wish", "explicit", [],
     [ev("DOC027:T079", "whereas I want to be shown like different kind of content")])

cand("C023",
     "Get different kinds of trends and things happening in the world, not the same food videos and pictures again and again.",
     "explicit wish with purpose", "explicit", [],
     [ev("DOC027:T081", "So that I get different kind of like trends that are happening in the world, things that are happening."),
      ev("DOC027:T081", "I don't want Instagram to just keep showing me that over and over again.")])

cand("C024",
     "Get an assortment of content rather than one particular stream of content; a single stream would only be wanted from a specific channel or group.",
     "explicit preference", "explicit", [],
     [ev("DOC027:T087", "for me, I want like an assortment of content, not just one particular stream of content.")])

cand("C025",
     "Remain able to filter what is authentic on social media and therefore not be misinformed, while being willing to modify my opinion toward the actual truth.",
     "reported current state and personal stance", "explicit", [],
     [ev("DOC027:T099", "I can kind of easily filter out what is authentic and what is not authentic. And in that way I'm never misinformed because of social media.")])

cand("C026",
     "Have social media apps use basic human judgment instead of throwing random ads at me just because I said one particular name.",
     "magic-wand wish", "explicit", [],
     [ev("DOC027:T101", "make these social media apps to use basic human judgment and not just throw random ads at me just because I said that one particular name.")])

cand("C027",
     "Modify the advertising algorithm so that it finds the right balance, for example showing a couple of ads and stopping if they are skipped.",
     "magic-wand wish with illustrative example", "explicit",
     ["the '2 ads then stop' is an illustrative example, not a fixed threshold"],
     [ev("DOC027:T103", "So so basically modifying their current advertising algorithm so that they they just find the right balance")])

cand("C028",
     "Have a common platform I can design for myself that holds all my favorite applications and shows their good content in one place.",
     "magic-wand wish", "explicit", [],
     [ev("DOC027:T105", "I would be really happy if there was like this common platform which. Like I can design for myself."),
      ev("DOC027:T105", "it will have all of my favorite applications in one place, and give me, like an assortment of different kind of content")])

cand("C029",
     "Open one app and get all the content without wasting time switching between apps.",
     "explicit wish", "explicit", [],
     [ev("DOC027:T107", "I just want to open 1 1 app and get all the content and be done with it."),
      ev("DOC027:T107", "Because I kind of like waste a lot of time just switching between apps which I don't want.")])

G = []


def goal(gid, statement, ctx, evidence, label, rationale, supported, assumptions=None, steps=None, inference=None):
    G.append({"candidate_id": gid, "statement": statement, "actor": "Stakeholder",
              "context": ctx, "origin": "inferred" if label == "inferred" or inference else "explicit",
              "inference": inference,
              "evidence": evidence,
              "judgment": {"label": label, "rationale": rationale, "supported_parts": supported,
                           "unsupported_parts": [], "assumptions": assumptions or [],
                           "reasoning_steps": steps or []}})


goal("G001",
     "Stay informed about news and trends around the world, including what is happening back in India, with Twitter as my go-to news app.",
     ["the Twitter feed follows my current location (US), so India news is not surfaced automatically"],
     [ev("DOC027:T005", "Twitter is kind of like my go to news app because there are a lot of trends that are happening around the world"),
      ev("DOC027:T075", "That's 1 of my biggest motivation to be on like different social media platforms, so that I know what's happening in the world."),
      ev("DOC027:T009", "if I wanna get to know about the news or the things that are happening back in India, then that might not be possible, because Twitter is kind of now set to my location in us")],
     "direct",
     "T005 明说 Twitter 是“我的首选新闻应用”，用标签浏览世界各地发生的事；T075 说明动机是不想漏掉世界大事；T009 明确想了解印度新闻、但承认美国定位会限制可见范围。主体、对象、方式（Twitter 趋势）、条件（定位）均保留在目标与 context 中。",
     ["Twitter 作为主要新闻入口", "关注全球趋势与大事", "希望了解印度新闻", "定位限制可见范围"])

goal("G002",
     "Stay connected with my friends in real time by instantly sharing photos and videos of daily moments.",
     [],
     [ev("DOC027:T005", "It's very easy for me to connect to stay connected to my friends in real time."),
      ev("DOC027:T005", "my friends back in India they they still know, like what I ate yesterday for my dinner, because I just send them that picture through Snapchat.")],
     "direct",
     "T005 以“stay connected to my friends in real time”明确目的，并以即时发送照片/视频、印度朋友能看到他昨天吃了什么作为实现方式；目标保留即时性与分享内容，未扩大到其他平台。",
     ["与朋友实时保持联系", "即时分享照片和视频"])

goal("G003",
     "Stay aware of what is happening in my immediate circle of friends, campus and class, beyond global news.",
     [],
     [ev("DOC027:T075", "It's also about knowing what's happening in my friend Circle, or with the with my friends back in India."),
      ev("DOC027:T077", "Let's say, what's happening on campus, what's happening in class. what's happening like with my classmates stuff like that")],
     "direct",
     "T075 把朋友圈动态与“世界”并列，T077 进一步限定为“不那么全球”的校园、班级、同学；范围明确且与 G001 的全球新闻区分，未把两者混为一个目标。",
     ["朋友与印度友人的动态", "校园与班级里的事"])

goal("G004",
     "Ask questions and help other people in interest-group communities such as subreddits while keeping my identity anonymous.",
     [],
     [ev("DOC027:T005", "And I can join those interest groups and ask like, maybe a question, or maybe help other people. And all of this while be while maintaining my anonymity"),
      ev("DOC027:T027", "reddit reddit kind of comes for most because of the anonymity that it provides the next will be signal because of like high authentication and privacy and data encryption")],
     "direct",
     "T005 明确加入兴趣小组、提问或帮助他人，并两次强调维持匿名；T027 以匿名性作为 Reddit 排第一的理由。目标把“参与”与“匿名”作为同一动作的条件保留，未把匿名单列成抽象状态。",
     ["加入兴趣小组提问或帮助他人", "保持身份匿名"])

goal("G005",
     "Find answers to specific questions by searching discussions on Reddit.",
     ["only where the topic already has Reddit discussions; very niche situations may get no answers"],
     [ev("DOC027:T053", "whenever I wanna obtain information like out going out of my way, not not something that's already been displayed in my homepage. it's mostly when I am in a particular situation where I wanna search for something very particular"),
      ev("DOC027:T057", "I just go to Reddit to like, figure out whatever question I want to ask")],
     "direct",
     "T053 说明在具体情境下主动搜索并期待讨论与推荐，T057 明确“去 Reddit 弄清想问的问题”。T055 的“小众问题可能没人回答”作为适用范围条件保留，未夸大为总是能获得答案。",
     ["为具体情境主动搜索", "从讨论中获得回答与推荐"])

goal("G006",
     "Ensure that only I can access my social-media accounts through strong authentication, such as a 2FA backup code required when signing in from a new device.",
     [],
     [ev("DOC027:T011", "because I don't want anyone else accessing my accounts on any social media platforms"),
      ev("DOC027:T023", "Because that kind of makes me feel like my particular account cannot be accessed by anyone else other than me. because I have those particular code.")],
     "direct",
     "T011 把认证列为最重要功能，理由是不想让任何人访问自己的账号；T023 用备份码说明“只有本人能进入”。2FA 备份码作为示例保留，原文未要求所有平台一律采用同一机制，故用“such as”限定。",
     ["认证是最重要的功能", "只有本人能访问账号", "新设备登录需要备份码（示例）"])

goal("G007",
     "Keep my posts available on the platform until I delete or archive them myself.",
     [],
     [ev("DOC027:T013", "they should be there until, and unless I delete them or I archive them")],
     "direct",
     "T013 的“they should be there until, and unless I delete them or I archive them”直接给出保留条件与删除/归档的主动方式。注意 T012 仅有“I.”、T013 以“Want my tweets”开头，否定词在轮次边界被截断；本目标只依据意义完整的后半句，未补写缺失否定词。",
     ["帖子在本人删除或归档前一直保留"])

goal("G008",
     "Experience platform outages only sporadically, not on a regular basis.",
     ["occasional outages are acceptable; speed also depends on my network"],
     [ev("DOC027:T013", "I don't want those outages to be that often, if they are like sporadic, I'm fine with it, but if they are too regular, then they might lose me as a customer")],
     "direct",
     "T013 明确区分偶发（可接受）与经常（不可接受，并可能导致流失），强度与条件都保留。同段提到的“speed”未给阈值且归结于网络，未写成速度目标。",
     ["偶发宕机可接受", "经常性宕机不可接受"])

goal("G009",
     "Keep my conversations and data private from people I do not know, with data encryption.",
     [],
     [ev("DOC027:T039", "I don't want other people to other people as in the people that I don't even know like kind of like see through my text or my conversation with my friends"),
      ev("DOC027:T045", "So the 1st important thing is, I think, data privacy for me."),
      ev("DOC027:T047", "Like especially data encryption.")],
     "direct",
     "T039 明确不想让不认识的人看穿自己与朋友的对话；T045 把数据隐私列为首要；T047 点明尤其要数据加密。主体（不认识的人）、对象（对话与数据）、选定方式（加密）均保留。",
     ["陌生人不能看到对话内容", "数据隐私是首要", "采用数据加密"])

goal("G010",
     "Stop seeing the same ads repeatedly just because I mentioned a topic once, so that ad delivery finds a balance instead of following a single mention.",
     ["ads can be occasionally helpful when I am actively shopping, though that is rare"],
     [ev("DOC027:T045", "I'm kind of like annoyed like I don't want to see the same kind of ads over and over again, just because I talked about it one time."),
      ev("DOC027:T101", "make these social media apps to use basic human judgment and not just throw random ads at me just because I said that one particular name.")],
     "direct",
     "T045 直接说出不想因提过一次就反复看到同类广告；T101 以“基本人类判断、不要因为提了一个名字就乱推”重述同一诉求；T043 的“偶尔有用”作为例外保留。T103 的“先推两条、跳过就停止”是假设示例，未写成固定阈值。",
     ["不因一次提及反复推同类广告", "广告投放要有判断与平衡", "购物时偶尔有用（例外）"])

goal("G011",
     "Be shown a varied assortment of content rather than the same kind of content repeated.",
     [],
     [ev("DOC027:T079", "whereas I want to be shown like different kind of content"),
      ev("DOC027:T087", "for me, I want like an assortment of content, not just one particular stream of content.")],
     "direct",
     "T079 明确想看到不同内容而不是被算法重复同类内容；T081 说明是为看到世界上的不同趋势、不要反复食物内容；T087 明确要 assortment 而非单一内容流。多处同一结果，合并为一个目标。",
     ["看到不同种类的内容", "不接受单一内容流反复出现"])

goal("G012",
     "Keep all social-media account credentials and 2FA backup codes recorded in a digital vault on my phone so that account details are not lost.",
     ["using Google Password Manager as the vault"],
     [ev("DOC027:T065", "I do have like a a digital vault that I keep on my phone which helps me to keep. Keep a track of all the accounts, my credentials for all the social networking platforms."),
      ev("DOC027:T023", "You have to keep it saved somewhere, maybe in like a digital vault or something."),
      ev("DOC027:T067", "It's quite reliable. And it usually like helps me to just like I can just tap in and whenever I log into any any like social media.")],
     "direct",
     "T065 自述手机数字保险库用于跟踪所有平台账号与凭证，并说明丢失保险库会失去大部分账号信息（即需要防止这种丢失）；T023 说明 2FA 备份码也需保存在保险库；T067 说明所用工具是 Google Password Manager。现有实践与“重要”评价共同支持该维护目标。",
     ["凭证集中保存在手机保险库", "2FA 备份码一并保存", "使用 Google Password Manager"])

goal("G013",
     "Keep new posts loading as I scroll so that posts are not missed when the feed stalls.",
     [],
     [ev("DOC027:T049", "So it's easier for me to just go at like the top and then start like a new kind of like a refresh, instead of just like going through the same kind of my session. So that's kind of annoying, because I have to like go back up."),
      ev("DOC027:T049", "maybe I just missed one particular post or one particular item because")],
     "inferred",
     "T049 描述滚动时内容加载中断、只能回顶部刷新，并担心“可能漏掉了某个帖子”。这是抱怨加临时应对，原文没有直接说出“希望持续加载”。结合其保持了解朋友圈/校园动态的目标（G003），可正面推断出“不要漏帖、信息流继续加载”的意图；具体刷新机制未被要求。",
     ["加载中断导致回顶部刷新", "担心漏掉帖子"],
     ["他把“可能漏掉帖子”视为需要避免的后果", "未要求特定加载或刷新机制"],
     ["确认抱怨的对象是信息流中断而非内容质量", "结合其了解动态的目标推断避免漏帖的意图", "剔除原文未支持的具体机制要求"],
     {"basis_candidate_ids": ["G003"],
      "reason": "T049 的漏帖担忧与其“了解朋友圈、校园与班级动态”的目标一致，据此推断避免漏帖的信息流目标。",
      "assumptions": ["保持了解动态依赖信息流不中断", "抱怨可正面支持避免型目标"]})

goal("G014",
     "Have one customizable platform that aggregates content from the social apps I choose, so that I can get all content without switching between apps.",
     [],
     [ev("DOC027:T105", "I would be really happy if there was like this common platform which. Like I can design for myself."),
      ev("DOC027:T107", "I just want to open 1 1 app and get all the content and be done with it.")],
     "direct",
     "T105 明确想要一个可自行设计、把常用应用放在一处并展示各应用内容的平台；T107 说明目的是不想在应用间切换、浪费时间。目标保留“可自选应用”“聚合内容”“不切换应用”三个已明确成分，未指定具体技术实现。",
     ["一个可自行配置的公共平台", "聚合所选应用的内容", "不用在应用间切换"])

ENTRIES = [
    ("C001", "keep", ["G001"], "直接表达以 Twitter 为首选新闻应用、跟进全球趋势；保留为 G001。"),
    ("C002", "keep", ["G002"], "直接表达通过 Snapchat 与朋友实时联系、即时分享；保留为 G002。"),
    ("C003", "keep", ["G004"], "直接表达在兴趣小组提问或帮助他人并保持匿名；保留为 G004。"),
    ("C004", "merge", ["G001"], "同属“了解世界/家乡新闻”的同一结果；T009 补充地区范围与定位限制，并入 G001 的 statement/context。"),
    ("C005", "keep", ["G006"], "直接表达认证最重要、不让任何人访问账号；保留为 G006。"),
    ("C006", "keep", ["G007"], "直接给出帖子保留到本人删除或归档的条件；保留为 G007。"),
    ("C007", "keep", ["G008"], "直接区分偶发与经常性宕机；保留为 G008。"),
    ("C008", "keep", ["G012"], "2FA 备份码需保存在数字保险库，是凭证保存目标的具体来源；保留为 G012 的主候选。"),
    ("C009", "exclude", [], "这是对已分别捕获的匿名性（G004）、认证/隐私（G006、G009）、新闻（G001）三类偏好的相对排序，属方案取舍；排名不等于强制要求，也不构成独立结果状态，故不单列目标，另在 decisions.questions 中保留。"),
    ("C010", "exclude", [], "描述打开 Reddit、必要时重新登录并完成 2FA、滚动首页、点开帖子读串的日常操作序列；目的（了解校园/朋友动态、获取信息）已由 G003、G005 承接，无独立结果意图。"),
    ("C011", "keep", ["G009"], "直接表达不让不认识的人看穿与朋友的对话；保留为 G009 主候选。"),
    ("C012", "keep", ["G010"], "直接表达不因一次提及反复看到同类广告，并含“偶尔有用”的例外；保留为 G010 主候选。"),
    ("C013", "merge", ["G009"], "“data privacy 尤其 data encryption”是对同一隐私结果的强调与选定方式，并入 G009 的 statement/context，不另立加密手段目标。"),
    ("C014", "keep", ["G013"], "加载中断、回顶部刷新、担心漏帖构成避免型意图的正面依据，按 inferred 保留为 G013。"),
    ("C015", "keep", ["G005"], "直接表达为具体情境搜索 Reddit 讨论并获取信息；保留为 G005。"),
    ("C016", "exclude", [], "说明极小众问题在 Reddit 上可能无人回答，是对 G005 适用范围的限制；已作为 G005 的条件保留，不单独成目标。"),
    ("C017", "exclude", [], "回答“该向从未用过社媒的人解释哪些概念”的假设教学问题，列举凭证、账户、群组、内容等术语；不是本人期望达到的结果。"),
    ("C018", "merge", ["G012"], "手机数字保险库跟踪所有账号凭证，与 C008 的备份码保存同属一项维护动作，并入 G012。"),
    ("C019", "merge", ["G012"], "对 Google Password Manager 可靠性与自动填充的现状报告，是 G012 的选定工具与背景，并入 context，不另立便利性目标。"),
    ("C020", "merge", ["G001"], "使用多平台的总体动机是了解世界大事，与 C001 的新闻目标同一结果，并入 G001。"),
    ("C021", "keep", ["G003"], "直接表达了解朋友圈、印度友人、校园与班级动态；保留为 G003。"),
    ("C022", "keep", ["G011"], "直接表达想看到不同内容而非算法重复同类内容；保留为 G011 主候选。"),
    ("C023", "merge", ["G011"], "“想看不同趋势、不要反复食物内容”与 C022 同一结果，并入 G011，并作为其目的依据。"),
    ("C024", "merge", ["G011"], "“要 assortment 而非单一内容流”与 C022 同一结果，并入 G011。"),
    ("C025", "exclude", [], "T099 是对现状的正面评价（自认能分辨真假、未被误导）与态度（愿按事实修正观点），未表达要求平台维持或改变的状态；不据此另造目标。"),
    ("C026", "merge", ["G010"], "“用基本人类判断、不要因一个名字乱推广告”与 C012 同一诉求，并入 G010。"),
    ("C027", "merge", ["G010"], "“修改广告算法找平衡”与 C012 同一诉求；其中“2 条广告后停止”是示例，未写成阈值，并入 G010。"),
    ("C028", "keep", ["G014"], "直接表达想要可自设计的公共聚合平台；保留为 G014 主候选。"),
    ("C029", "merge", ["G014"], "“打开一个应用拿到全部内容、不浪费时间切换”是 G014 的目的，并入 G014。"),
]

SOURCE_CHECKS = [
    ("S1", [("DOC027:T013", "they should be there until, and unless I delete them or I archive them")],
     ["C006"], ["G007"], "represented",
     "回查被轮次边界截断的否定句，确认后半句给出明确的保留条件，已由 G007 承接。"),
    ("S2", [("DOC027:T009", "if I wanna get to know about the news or the things that are happening back in India, then that might not be possible, because Twitter is kind of now set to my location in us")],
     ["C004"], ["G001"], "represented",
     "回查地缘定位对新闻可见范围的影响，已作为 G001 的范围与条件保留。"),
    ("S3", [("DOC027:T043", "I've I've realized that it's kind of helpful sometimes when I actually want to like buy something, and it gives me those ads, but that's rare.")],
     ["C012"], ["G010"], "represented",
     "回查广告的让步/例外（偶尔有用），已写入 G010 的 context，未把广告一律否定。"),
    ("S4", [("DOC027:T055", "I probably wouldn't get any answers for that.")],
     ["C016"], [], "excluded",
     "回查极小众问题可能无回答的限制，作为 G005 的条件保留而非目标，故不映射最终目标。"),
    ("S5", [("DOC027:T027", "reddit reddit kind of comes for most because of the anonymity that it provides the next will be signal because of like high authentication and privacy and data encryption")],
     ["C009"], [], "excluded",
     "回查平台优先级排序，确认其是对既有偏好的排序而非独立结果，保持排除并转入问题。"),
    ("S6", [("DOC027:T099", "I can kind of easily filter out what is authentic and what is not authentic. And in that way I'm never misinformed because of social media.")],
     ["C025"], [], "excluded",
     "回查对自身辨别真假能力的现状评价，未见维持或改变的要求，保持排除。"),
    ("S7", [("DOC027:T049", "maybe I just missed one particular post or one particular item because")],
     ["C014"], ["G013"], "represented",
     "回查漏帖担忧，作为 G013 推断的正面依据保留。"),
    ("S8", [("DOC027:T059", "The 1st thing that I'll introduce to them is like their basic credentials and managing those credentials across all the social media platforms.")],
     ["C017"], [], "excluded",
     "回查假设教学场景的解释内容，确认不属于受访者本人的结果意图，保持排除。"),
    ("S9", [("DOC027:T077", "Let's say, what's happening on campus, what's happening in class. what's happening like with my classmates stuff like that")],
     ["C021"], ["G003"], "represented",
     "回查“本地圈层”与全球新闻的区分，已由 G003 单独承接。"),
    ("S10", [("DOC027:T103", "So so basically modifying their current advertising algorithm so that they they just find the right balance")],
     ["C027"], ["G010"], "represented",
     "回查“magic wand”中的广告平衡要求，确认与 G010 同一诉求；示例数量未写成阈值。"),
    ("S11", [("DOC027:T023", "Because that kind of makes me feel like my particular account cannot be accessed by anyone else other than me. because I have those particular code.")],
     ["C008"], ["G012"], "represented",
     "回查备份码保存与账号独占访问的联系，已用于 G012 及关系 R1。"),
    ("S12", [("DOC027:T105", "it will have all of my favorite applications in one place, and give me, like an assortment of different kind of content")],
     ["C028"], ["G014"], "represented",
     "回查聚合平台的完整表述，确认“一处聚合 + 多应用内容”由 G014 承接。"),
    ("S13", [("DOC027:T005", "Twitter is kind of like my go to news app because there are a lot of trends that are happening around the world")],
     ["C001", "C002", "C003"], ["G001", "G002", "G004"], "represented",
     "回查“每个平台满足不同需要”的首段，确认三项分别由 G001/G002/G004 承接，未合并成一锅。"),
    ("S14", [("DOC027:T013", "I don't want those outages to be that often, if they are like sporadic, I'm fine with it, but if they are too regular, then they might lose me as a customer")],
     ["C007"], ["G008"], "represented",
     "回查宕机的强度区分（偶发可接受/经常不可接受），已由 G008 承接。"),
]

WINDOWS = [f"DOC027:W{i:04d}" for i in range(1, 56)]

RELATIONS = [
    {"relation_id": "R1", "source_id": "G012", "target_id": "G006", "type": "contribution",
     "status": "supported", "conditions": [], "assumptions": ["数字保险库仅本人可解锁"],
     "rationale": "T023 直接把“把备份码保存在数字保险库”与“账号无法被本人以外的人访问”联系起来：保存好凭证/备份码有助于维持账号独占访问。但保存不等于认证机制本身，也不保证所有平台，故为 contribution 而非共同充分精化。",
     "evidence_ids": [],
     "evidence_quotes": [{"source_id": "DOC027:T023", "quote": "Because that kind of makes me feel like my particular account cannot be accessed by anyone else other than me. because I have those particular code.", "role": "basis"}]},
    {"relation_id": "R2", "source_id": "G011", "target_id": "G001", "type": "contribution",
     "status": "supported", "conditions": ["原句语境是 Instagram 兴趣推荐算法；结论限于平台内容呈现影响可见趋势范围"],
     "assumptions": ["多样化内容会带来不同领域的世界趋势信息"],
     "rationale": "T081 用“So that I get different kind of like trends that are happening in the world”明示想要不同内容的目的是看到世界各地不同的趋势；内容多样性有助于世界新闻目标，但不保证新闻覆盖，故为 contribution。",
     "evidence_ids": [],
     "evidence_quotes": [{"source_id": "DOC027:T081", "quote": "So that I get different kind of like trends that are happening in the world, things that are happening.", "role": "basis"}]},
]

QUESTIONS = [
    {"target_type": "model", "target_id": "DOC027-goal-model",
     "message": "平台优先级排序（Reddit 因匿名性第一、Signal 因认证/隐私/加密第二、Twitter 因新闻第三；T027/T031）是否应作为独立的平台选择目标？当前按“排名不等于强制要求、也不构成独立结果状态”排除（C009），排序信息未进入目标正文。"},
    {"target_type": "model", "target_id": "DOC027-goal-model",
     "message": "本次未建立任何 AND 精化组。已逐项检查：G001 由 G011/G014 精化、G006 由 G012 精化、G009 由 G006/G010 精化、G011 由 G014 精化、G003 由 G002 精化，均无法在原句中找到“整组共同满足父目标”的充分性依据；是否还有遗漏的父目标或整组依据需要补充？"},
    {"target_type": "goal", "target_id": "G013",
     "message": "G013 由 T049 的抱怨（加载中断、回顶部刷新、担心漏帖）推断而来，原文未直接说出“希望持续加载”；是否接受该推断目标，或应降为使用体验问题？"},
]

spec = {
    "document_id": "DOC027",
    "raw_candidates": C,
    "goals": G,
    "review_questions": [],
    "limitations": [
        "T012 仅含“I.”、T013 以“Want my tweets...”开头：原句否定词在轮次边界被截断。G007 只依据 T013 中意义完整的“they should be there until, and unless I delete them or I archive them”判定，未补写缺失的否定词。",
        "原文为访谈口语转写，存在断句、重复和指代省略（如“I they should be there”）；语义按上下文判断，未做逐字语法修正。",
        "T013 提到 speed 后转入 outages，未给出速度阈值，故未把“速度”单列为目标；T047-T051 的加载滞后另按 G013 处理。",
        "T007 关于印度与东南亚平台使用差异是观察性背景，未表达本人目标，未建节点。",
        "原文未说明各项目标的实现责任方（平台、本人或第三方），模型未做责任分配。",
    ],
    "ledger": {
        "model": "deepseek-v4.1-flash",
        "temperature": "unknown",
        "budget": "1 initial pass + <=2 repair rounds",
        "usage": "unknown",
        "skill_revision": "a5952d426b1624a3fcb2ce2829e1ae1ceb15e19dc3309d9571f3bc6b465deb6f",
        "prompt_revision": "task-prompt-v1",
        "planned_passes": 1,
        "stop_reason": "已完成 111 轮全文的逐窗捕获与全篇校正；未发现需要继续补查的新增有据意图，按预算停止。",
        "passes": [{"pass_id": "P1", "kind": "initial", "context": "isolated", "status": "completed",
                    "window_results": [{"window_id": w, "status": "processed", "reason": ""} for w in WINDOWS]}],
        "full_context_review": {
            "status": "completed",
            "reason": "逐窗捕获后回看全部 111 轮：核对 T011-T013 的指代与截断否定、T009 的定位条件、T043 的广告让步、T045/T047 的隐私与加密衔接、T055 的小众范围限制、T075/T077 的世界与本地圈层区分、T099 与 T087 的相反/让步证据，以及 T101-T107 的“magic wand”示例与目标的关系；未新增 P1 之外的候选。",
        },
        "entries": [{"candidate_id": cid, "disposition": d, "final_goal_ids": gids, "reason": why}
                    for cid, d, gids, why in ENTRIES],
        "source_checks": [{"check_id": cid, "evidence_candidates": [{"source_id": s, "quote": q, "role": "basis"} for s, q in evs],
                           "candidate_ids": cs, "final_goal_ids": gs, "outcome": oc, "reason": why}
                          for cid, evs, cs, gs, oc, why in SOURCE_CHECKS],
    },
    "decisions": {"relations": RELATIONS, "groups": [], "questions": QUESTIONS, "reassessments": []},
}

if problems:
    for p in problems:
        print("QUOTE PROBLEM:", p)
    sys.exit(1)

# structural self-checks
cids = [c["candidate_id"] for c in C]
gids = [g["candidate_id"] for g in G]
assert len(cids) == len(set(cids)) and len(gids) == len(set(gids))
assert set(cids) == {e[0] for e in ENTRIES}, "entry coverage"
for cid, d, gs, why in ENTRIES:
    assert why.strip()
    if d in {"keep", "merge"}:
        assert len(gs) == 1, cid
    if d in {"exclude", "uncertain", "pending"}:
        assert gs == [], cid
for g in G:
    assert g["evidence"], g["candidate_id"]
    assert any(e["role"] == "basis" for e in g["evidence"])
    if g["judgment"]["label"] in {"direct", "inferred"}:
        assert g["judgment"]["unsupported_parts"] == []
    if g["inference"]:
        assert set(g["inference"]["basis_candidate_ids"]) <= set(gids)

(A / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("OK candidates=%d goals=%d entries=%d windows=%d" % (len(C), len(G), len(ENTRIES), len(WINDOWS)))
