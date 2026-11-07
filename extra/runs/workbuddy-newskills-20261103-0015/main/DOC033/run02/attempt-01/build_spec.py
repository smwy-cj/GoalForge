# -*- coding: utf-8 -*-
"""Build spec.json for DOC033-run02 and verify every quote byte-exactly."""
import json, sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
doc = json.loads((BASE / "source/DOC033.json").read_text(encoding="utf-8"))
TURNS = {t["source_id"]: t["text"] for t in doc["turns"]}
TURN_IDS = [t["source_id"] for t in doc["turns"]]

E = lambda sid, q, role="basis": {"source_id": sid, "quote": q, "role": role}


def check(ev):
    for item in ev:
        text = TURNS[item["source_id"]]
        n = text.count(item["quote"])
        if n != 1:
            print("QUOTE PROBLEM", item["source_id"], "count=", n, repr(item["quote"]))
            sys.exit(1)


raw = []


def C(cid, statement, modality, context, origin, evidence, window_turn):
    c = {
        "candidate_id": cid,
        "statement": statement,
        "actor": "Stakeholder",
        "modality": modality,
        "context": context,
        "origin": origin,
        "pass_id": "P1",
        "evidence": evidence,
    }
    check(evidence)
    raw.append(c)


C("C001", "When bored, she watches YouTube Shorts to be entertained and to occupy or distract her mind.",
  "explicit; present-tense habit", ["On her phone"], "explicit",
  [E("DOC033:T021", "So Youtube shorts is when I'm bored and I want to be entertained. or when I just want to. you know, think about other things.")], 21)
C("C002", "She watches a full long-form video when she wants to dive deeper into a subject.",
  "explicit; present-tense habit", [], "explicit",
  [E("DOC033:T021", "And long form content is, for when like I said I'd I'd want to dive deeper into a subject. That's when I watch like a full video.")], 21)
C("C003", "She keeps long-form content playing in the background while performing other tasks on her laptop.",
  "explicit; habitual", ["On the laptop"], "explicit",
  [E("DOC033:T023", "I like to keep it playing in the background sometimes when I'm performing like other tasks on my laptop.")], 23)
C("C004", "She listens mainly to the audio rather than watching the video, because she has little patience for watching.",
  "explicit; habitual with stated limitation", [], "explicit",
  [E("DOC033:T025", "I listen mainly to the audio. I don't have that much patience for watching the video most of the time.")], 25)
C("C005", "She uses YouTube to listen to things more than to watch things.",
  "explicit; self-summary", [], "explicit",
  [E("DOC033:T041", "I use it to listen to things more than watching things.")], 41)
C("C006", "Unwinding with YouTube Shorts is one of her main uses of the platform.",
  "explicit; enumeration of main uses", [], "explicit",
  [E("DOC033:T045", "one would be like unwinding with Youtube shorts.")], 45)
C("C007", "Playing long-form content in the background is one of her main uses of the platform.",
  "explicit; enumeration of main uses", [], "explicit",
  [E("DOC033:T045", "the other would be playing long form content in the background.")], 45)
C("C008", "She plays videos to fall asleep, leaving some white noise on.",
  "explicit; not that frequent but does happen", [], "explicit",
  [E("DOC033:T045", "Is playing videos to fall asleep like leaving some sort of white noise on.")], 45)
C("C009", "She also listens to music on YouTube.",
  "explicit but clause garbled at the end", ["Only mention in the interview; purpose unclear"], "explicit",
  [E("DOC033:T045", "Those are like the 3 main and listening to music, probably to be sick.")], 45)
C("C010", "She picks content that works in the background - podcasts, streams, audiobooks - where facial expressions do not matter and the value comes from listening.",
  "explicit; habitual selection rule", [], "explicit",
  [E("DOC033:T047", "you know podcasts or streams where I'm not really that concerned about, like the person's facial expressions as much.")], 47)
C("C011", "She does not spend much time searching and can just click around her YouTube recommendations.",
  "explicit; habitual", ["Feed is personalized from viewing history"], "explicit",
  [E("DOC033:T049", "So I don't spend that much time searching. I can just click around in my Youtube recommendations most of the time.")], 49)
C("C012", "She never searches in Shorts and finds searching in Shorts really hard, so she takes whatever the algorithm gives her.",
  "explicit; habitual plus obstacle", [], "explicit",
  [E("DOC033:T049", "I don't think I ever search for anything in shorts. And it's also really hard to search in shorts.")], 49)
C("C013", "Her feed is customized from viewing history even though she does not follow creators or channels.",
  "explicit; reported current state", [], "explicit",
  [E("DOC033:T051", "It's my feed has been customized.")], 51)
C("C014", "She wanted YouTube to give her recommendations; unrelated recommendations all over her feed were annoying when she only wanted to relax, so she switched viewing history on.",
  "explicit; past decision with reason", ["Signed in with her Google account"], "explicit",
  [E("DOC033:T053", "a lot of times on Youtube, I just wanted them to give me recommendations"),
   E("DOC033:T053", "seeing recommendations that were not related to what I wanted to watch all over my feed was pretty annoying when all I wanted to do was relax."),
   E("DOC033:T053", "So I actually switched on viewing history.")], 53)
C("C015", "She leaves watch history on because there are no visible downsides and there are upsides of a personalized feed.",
  "explicit; decision rationale", [], "explicit",
  [E("DOC033:T057", "And there are upsides of me having a personalized feed.")], 57)
C("C016", "She revisits content from memory and does not use watch later; if it is not already on her mind she would rather start afresh for the moment than go back to a list.",
  "explicit; stated preference with rationale", [], "explicit",
  [E("DOC033:T061", "So if there's anything I want to revisit, I remember it well enough to go back and watch it.")], 61)
C("C017", "Mindlessly scrolling YouTube helps her space out and have a moment to herself, especially right after waking and after coming back home before homework.",
  "explicit; routine description", [], "explicit",
  [E("DOC033:T063", "mindlessly scrolling on Youtube helps")], 63)
C("C018", "Long-form in the background keeps one portion of her brain occupied while she works on something else and helps her focus, though sometimes it fails when she gets too deep into work.",
  "explicit; benefit with stated exception", [], "explicit",
  [E("DOC033:T065", "Long form content is useful for me to keep one portion of my brain occupied while the other portion is busy doing something else.")], 65)
C("C019", "She values that YouTube is probably the largest accessible repository of videos.",
  "explicit; valuation", [], "explicit",
  [E("DOC033:T121", "It's probably like the largest accessible repository of videos.")], 121)
C("C020", "She can keep looking until she finds something she likes because of the sheer volume of content available.",
  "explicit; valuation with consequence", [], "explicit",
  [E("DOC033:T123", "But now I can keep looking until I find something I like, just because of, like the sheer volume of content available.")], 123)
C("C021", "When searching for long-form content she uses the time filter and puts greater than 20 min to filter videos.",
  "explicit; habitual", [], "explicit",
  [E("DOC033:T129", "when I'm trying to search for long form content, I put the greater than 20")], 129)
C("C022", "Of the five filter types she uses duration most and sometimes upload date, and does not care much about the rest.",
  "explicit; habitual", [], "explicit",
  [E("DOC033:T133", "the ones that I use the most are probably duration.")], 133)
C("C023", "Duration and upload date help her find the kind of content she is looking for; for an evolved technical concept she looks for the latest video that explains it in depth.",
  "explicit; habitual plus purpose", [], "explicit",
  [E("DOC033:T135", "So duration helps me find like the kind of content I'm looking for. and same with the upload date.")], 135)
C("C024", "She uses the share button to share Shorts on WhatsApp to keep in touch with friends and family.",
  "explicit; habitual", ["Shorts only"], "explicit",
  [E("DOC033:T137", "I use the share button to share videos shorts on Whatsapp with. to keep in touch with friends and family.")], 137)
C("C025", "She would hate to send anything longer than a Short to someone.",
  "explicit; strong negative preference", [], "explicit",
  [E("DOC033:T139", "I would hate to send anything longer than a short to someone.")], 139)
C("C026", "It is hard to find a Short again once watched because she remembers random details and the titles are not memorable or conducive to searching.",
  "explicit; obstacle report", [], "explicit",
  [E("DOC033:T141", "It's like hard to find a short once you watched it because you remember random details about it.")], 141)
C("C027", "She wanted to send a Short to her sister that she had watched before but could only remember what happened in it.",
  "explicit; concrete instance", [], "explicit",
  [E("DOC033:T143", "wanting to send something to my sister that I had watched previously")], 143)
C("C028", "Apart from the Shorts revisiting aspect she is comfortable with YouTube and has no complaints.",
  "explicit; current-state evaluation", [], "explicit",
  [E("DOC033:T145", "Apart from that, I'd say I'm pretty comfortable with Youtube. There's no like complaints off the top of my head.")], 145)
C("C029", "When tired of a set of things she wants to immediately erase all of that from her feed, but there is no direct way to do it.",
  "explicit; wish plus obstacle", [], "explicit",
  [E("DOC033:T151", "sometimes when I'm tired of a set of things, then I want to immediately erase all of that into from my feed but there's like no direct way of doing that.")], 151)
C("C030", "When she leaves a video on to sleep it goes into advertisements, sometimes two-hour advertisements, which is annoying.",
  "explicit complaint", [], "explicit",
  [E("DOC033:T151", "sometimes it goes into advertisements that themselves are 2")], 151)
C("C031", "It would be better if these issues were fixed, but they are not deal breakers and she would not switch platforms over them.",
  "explicit; priority limitation", [], "explicit",
  [E("DOC033:T155", "I mean, it would definitely be better if they're fixed, but not to the point where if a different platform has it.")], 155)
C("C032", "The biggest thing for her is being able to search YouTube Shorts more effectively.",
  "explicit; strongest missing capability", [], "explicit",
  [E("DOC033:T163", "the biggest thing for me is being able to search Youtube shorts more effectively.")], 163)
C("C033", "She suggests being able to customize recommendations more effectively, for example by writing descriptions of what she wants and does not want to see so they are taken into account instead of just watch history.",
  "hedged suggestion (maybe); not framed as a requirement", [], "explicit",
  [E("DOC033:T165", "Maybe you could write descriptions of what you want to see and what you don't want to see, and maybe they can take that also into consideration when recommending your feed instead of just like your watch history.")], 165)
C("C034", "Sometimes people want to refresh their watch history temporarily, not completely: pause this kind of videos for a while and then show new content.",
  "hedged suggestion; generalized to people, 'show me' in first person", [], "explicit",
  [E("DOC033:T167", "I think sometimes people just want to refresh their watch history, but not like completely. but just for temporarily")], 167)
C("C035", "The fresh start would not help her day-to-day routine and she has not felt that in a long time, though she remembers times in the past.",
  "explicit; self-caveat", [], "explicit",
  [E("DOC033:T173", "So the fresh start again would not help me in my day to day routine.")], 173)
C("C036", "Searching YouTube Shorts would help her share videos more easily when she does not share them as soon as she sees them.",
  "explicit; benefit statement", [], "explicit",
  [E("DOC033:T173", "And searching Youtube shorts would help me share videos more easily, because sometimes I don't share videos as soon as I see them.")], 173)
C("C037", "She does not remember the fatigue instances and felt that less towards YouTube and more towards other social media platforms.",
  "explicit; uncertainty about the past need", [], "explicit",
  [E("DOC033:T175", "I also think I felt that less towards Youtube and more towards")], 175)
C("C038", "She rates her overall YouTube experience 9 out of 10 and is pretty satisfied.",
  "explicit; rating", [], "explicit",
  [E("DOC033:T177", "Yeah, I would say it's 9.")], 177)
C("C039", "She does not want YouTube to change too many things because the experience is close to how useful it is to her and changes might make it worse.",
  "explicit; avoidance with reason", [], "explicit",
  [E("DOC033:T179", "I kind of don't want them to change too many things, because. like like I said, it's pretty close to how useful it is to me. and I think changing things might just make it worse.")], 179)
C("C040", "She clicks the video and changes the tab to go back to work, and does not use the mobile app for background playing.",
  "explicit; procedure with device constraint", [], "explicit",
  [E("DOC033:T095", "So I would click on the video. and then I would just change the tab and go back to what I was working on."),
   E("DOC033:T097", "No, I do not use the mobile app when I want to do that.")], 95)
C("C041", "Picture-in-picture collapses the video into a small window so she can browse other YouTube videos.",
  "explicit; feature description", [], "explicit",
  [E("DOC033:T107", "When I click it, it collapses down into a small screen at the bottom of the chrome window")], 107)
C("C042", "She has never used the sleep timer but probably will.",
  "explicit; weak future intention", [], "explicit",
  [E("DOC033:T107", "Sleep timer. is useful again. I've never used it, but I probably will.")], 107)
C("C043", "She did not even notice the ad until asked, which suggests a habit of skipping it.",
  "explicit; habitual inattention", [], "explicit",
  [E("DOC033:T071", "I actually didn't even notice")], 71)
C("C044", "She ignores new features and live videos because she does not know what they are.",
  "explicit; stated approach to novelty", [], "explicit",
  [E("DOC033:T161", "So I'm the kind of person who just ignores new features like I mentioned.")], 161)
C("C045", "She was a late adopter and thought Shorts would not be a valuable addition, but it was.",
  "explicit; retrospective", [], "explicit",
  [E("DOC033:T157", "I just like, was not never curious enough to click on the short links. and I thought it would like not be a valuable addition to my life. But it was.")], 157)
C("C046", "She spends about 15 min twice a day on Shorts.",
  "explicit; rough frequency estimate", [], "explicit",
  [E("DOC033:T031", "So I would say, maybe 15")], 31)
C("C047", "She uses long-form only on days when she needs something in the background; otherwise she would probably not use it at all.",
  "explicit; conditional use", [], "explicit",
  [E("DOC033:T033", "if I can't have something playing in the background then, would probably not use it at all.")], 33)
C("C048", "Mobile is more frequent because it is more accessible, while laptop time is longer during three to four hour work sessions.",
  "explicit; device and time split", [], "explicit",
  [E("DOC033:T029", "Mobile phone would be more frequent just because it's more accessible.")], 29)

# ---------------- goals ----------------
def J(label, rationale, sp=None, up=None, asm=None, steps=None):
    return {"label": label, "rationale": rationale,
            "supported_parts": sp or [], "unsupported_parts": up or [],
            "assumptions": asm or [], "reasoning_steps": steps or []}


goals = [
    dict(candidate_id="G001",
         statement="Watch YouTube Shorts on her phone to be entertained and distract her mind when she is bored or wants to unwind.",
         actor="Stakeholder",
         context=["On her phone",
                  "Typically when bored or wanting to unwind, including right after waking and after coming back home before homework"],
         origin="explicit", inference=None,
         evidence=[E("DOC033:T021", "So Youtube shorts is when I'm bored and I want to be entertained. or when I just want to. you know, think about other things."),
                   E("DOC033:T023", "So on my phone, I usually use it for Youtube shorts"),
                   E("DOC033:T045", "one would be like unwinding with Youtube shorts."),
                   E("DOC033:T063", "mindlessly scrolling on Youtube helps")],
         judgment=J("direct", "原句明确说出动机与结果：无聊时想被娱乐、占据注意力、分散自己；又两次把『用 Shorts 放松』列为主要用途。设备条件（手机）与场景（醒后、回家后）分别见 T023、T063，均在同一说话人语境中，未扩大范围，也未把频率数字写进目标。",
                    sp=["主体：受访者本人", "动作：看 YouTube Shorts", "结果：被娱乐、分散注意力"]))
    ,
    dict(candidate_id="G002",
         statement="Play long-form content in the background on her laptop while performing other tasks, to keep part of her mind occupied and help her focus.",
         actor="Stakeholder",
         context=["On the laptop; she does not use the mobile app for this",
                  "Listens mainly to the audio with little patience for watching",
                  "Picks audio-conducive content: podcasts, streams, audiobooks",
                  "Sometimes it does not work: when she gets too deep into work she zones out and the video has changed unnoticed"],
         origin="explicit", inference=None,
         evidence=[E("DOC033:T023", "I like to keep it playing in the background sometimes when I'm performing like other tasks on my laptop."),
                   E("DOC033:T065", "Long form content is useful for me to keep one portion of my brain occupied while the other portion is busy doing something else."),
                   E("DOC033:T025", "I listen mainly to the audio. I don't have that much patience for watching the video most of the time."),
                   E("DOC033:T047", "you know podcasts or streams where I'm not really that concerned about, like the person's facial expressions as much."),
                   E("DOC033:T065", "sometimes When I get too deep into my work I have to go back and and see what video is being played")],
         judgment=J("direct", "T023 给出动作与设备（笔记本、边做其他事边放），T065 给出目的（一部分大脑被占据、帮助专注），T025/T047 给出听觉优先与内容选择条件，T065 末尾的失败情形作为例外保留，没有把例外藏起来或强化为无条件有效。",
                    sp=["主体：受访者本人", "动作：在笔记本上后台播放长视频", "结果：占据部分注意力、帮助专注", "例外：专注过深时会走神"]))
    ,
    dict(candidate_id="G003",
         statement="Watch a full long-form video to dive deeper into a subject.",
         actor="Stakeholder",
         context=["Long-form, full video"],
         origin="explicit", inference=None,
         evidence=[E("DOC033:T021", "And long form content is, for when like I said I'd I'd want to dive deeper into a subject. That's when I watch like a full video.")],
         judgment=J("direct", "原句把长视频的用途直接说成『想更深入某个主题』并落到『看完整视频』，动作、对象、结果一致；未把这条与 G002 的后台占位混为一谈。",
                    sp=["主体：受访者本人", "动作：看完整长视频", "结果：深入某个主题"]))
    ,
    dict(candidate_id="G004",
         statement="Play videos to fall asleep, leaving white noise on.",
         actor="Stakeholder",
         context=["Not that frequent, but it does happen",
                  "Sleep timer is noted as a feature she has never used but probably will"],
         origin="explicit", inference=None,
         evidence=[E("DOC033:T045", "Is playing videos to fall asleep like leaving some sort of white noise on."),
                   E("DOC033:T107", "Sleep timer. is useful again. I've never used it, but I probably will.")],
         judgment=J("direct", "T045 在列举主要用途时明确『放视频入睡、留白噪音』，并说明频率不高；T107 的睡眠定时器只是『大概会用』的弱预期，作为方式/线索写入 context，没有升级为必须使用。",
                    sp=["主体：受访者本人", "动作：睡前播放视频/白噪音", "强度：偶发用途"]))
    ,
    dict(candidate_id="G005",
         statement="Keep her watch history enabled so YouTube keeps recommending content related to what she wants to watch instead of unrelated recommendations.",
         actor="Stakeholder",
         context=["Signed in with her Google account", "She had paused watch history in the past and switched it back on"],
         origin="explicit", inference=None,
         evidence=[E("DOC033:T053", "But I realized that I wasn't getting as much value as I wanted from it, because, a lot of times on Youtube, I just wanted them to give me recommendations"),
                   E("DOC033:T053", "seeing recommendations that were not related to what I wanted to watch all over my feed was pretty annoying when all I wanted to do was relax."),
                   E("DOC033:T053", "So I actually switched on viewing history."),
                   E("DOC033:T057", "And there are upsides of me having a personalized feed.")],
         judgment=J("direct", "T053 同时给出期望（希望平台给推荐）、负面情形（无关推荐铺满首页、妨碍放松）与实际动作（重新打开观看历史），T057 补充理由（个性化收益、无明显代价）。主体、方向（保持开启）与结果均一致；过去关闭的理由只在 context 里作为背景，不构成相反要求。",
                    sp=["主体：受访者本人", "动作：保持观看历史开启", "结果：推荐与想看的内容相关，避免无关推荐"]))
    ,
    dict(candidate_id="G006",
         statement="Apply the duration (over 20 minutes) and upload-date filters when searching long-form content, to find the latest in-depth video on an evolved technical concept.",
         actor="Stakeholder",
         context=["Only when searching for long-form content, e.g. learning a technical concept that has several iterations"],
         origin="explicit", inference=None,
         evidence=[E("DOC033:T129", "when I'm trying to search for long form content, I put the greater than 20"),
                   E("DOC033:T133", "the ones that I use the most are probably duration."),
                   E("DOC033:T135", "So duration helps me find like the kind of content I'm looking for. and same with the upload date."),
                   E("DOC033:T135", "I would also want a video that explains it in depth.")],
         judgment=J("direct", "T129/T133 给出实际使用的筛选项与阈值（>20 分钟），T135 给出两个筛选项各自的目的与组合条件（要最新、也要讲得深入）。两个限定作用于同一检索对象（同时满足），因此保留为一个目标而非拆成两个。",
                    sp=["主体：受访者本人", "动作：在搜索里套用时长与上传日期筛选", "条件：检索长视频/演进中的技术概念", "结果：找到最新且深入的视频"]))
    ,
    dict(candidate_id="G007",
         statement="Share Shorts through the share button on WhatsApp with friends and family to keep in touch.",
         actor="Stakeholder",
         context=["Shorts only: she would hate to send anything longer than a Short", "Via WhatsApp"],
         origin="explicit", inference=None,
         evidence=[E("DOC033:T137", "I use the share button to share videos shorts on Whatsapp with. to keep in touch with friends and family."),
                   E("DOC033:T139", "I would hate to send anything longer than a short to someone.")],
         judgment=J("direct", "T137 明确动作（用分享按钮）、渠道（WhatsApp）、对象（朋友家人）、目的（保持联系）；T139 明确只分享 Shorts、不发更长内容，作为否定性限定写入 context。",
                    sp=["主体：受访者本人", "动作：分享 Shorts 到 WhatsApp", "对象：朋友与家人", "限定：不分享长视频"]))
    ,
    dict(candidate_id="G008",
         statement="Be able to search YouTube Shorts effectively to find a Short she watched earlier.",
         actor="Stakeholder",
         context=["Described as the biggest missing thing; would help her share videos she did not share immediately",
                  "Titles of Shorts are not memorable or conducive to searching"],
         origin="explicit", inference=None,
         evidence=[E("DOC033:T163", "the biggest thing for me is being able to search Youtube shorts more effectively."),
                   E("DOC033:T141", "It's like hard to find a short once you watched it because you remember random details about it."),
                   E("DOC033:T173", "And searching Youtube shorts would help me share videos more easily, because sometimes I don't share videos as soon as I see them.")],
         judgment=J("direct", "T163 直接表述希望『更有效地搜索 Shorts』并称其为最重要的缺口；T141 说明找不到的具体成因，T173 说明它服务于延后分享。目标是能力期望，未虚构具体实现方案（未写排序、索引等方式）。",
                    sp=["主体：受访者本人", "动作：搜索已看过的 Shorts", "结果：找回并分享此前的短视频"]))
    ,
    dict(candidate_id="G009",
         statement="Be able to temporarily pause the kinds of videos she is tired of and see new content, without refreshing her watch history completely.",
         actor="Stakeholder",
         context=["Temporary only, not a complete refresh",
                  "She says it would not help her day-to-day routine and she has not felt this in a long time; it happened in the past"],
         origin="explicit", inference=None,
         evidence=[E("DOC033:T151", "sometimes when I'm tired of a set of things, then I want to immediately erase all of that into from my feed but there's like no direct way of doing that."),
                   E("DOC033:T167", "I think sometimes people just want to refresh their watch history, but not like completely. but just for temporarily"),
                   E("DOC033:T173", "So the fresh start again would not help me in my day to day routine.")],
         judgment=J("direct", "T151 以第一人称说出『想立刻把这一批内容从首页清掉、但没有直接办法』，T167 把范围限定为临时、非彻底，T173 说明其优先级与近年发生频率。目标按原话保留为『临时暂停/换新』，未升级为彻底重置；自评的低价值写入 context 而不是删除该目标。",
                    sp=["主体：受访者本人", "动作：临时暂停某类视频/换取新内容", "限定：不彻底清空观看历史"]))
    ,
    dict(candidate_id="G010",
         statement="Have the recommendation feed take her written descriptions of content she wants and does not want into account, in addition to watch history.",
         actor="Stakeholder",
         context=["Presented as a tentative suggestion ('maybe'), not a requirement"],
         origin="explicit", inference=None,
         evidence=[E("DOC033:T165", "Maybe you could write descriptions of what you want to see and what you don't want to see, and maybe they can take that also into consideration when recommending your feed instead of just like your watch history.")],
         judgment=J("direct", "T165 明确提出让推荐除了观看历史之外也考虑『写下来的想看/不想看描述』，动作与期望结果清楚；但语气是『maybe』、并自认不知道方案，因此只保留为建议强度的目标，context 标明非强制。",
                    sp=["主体：受访者本人（提议）", "动作：用文字描述想看/不想看的内容", "结果：推荐同时参考描述而非只看观看历史"]))
    ,
    dict(candidate_id="G011",
         statement="Avoid major changes to YouTube that could make her experience worse, keeping it close to its current usefulness.",
         actor="Stakeholder",
         context=["Rates the current experience 9 out of 10 and is pretty satisfied"],
         origin="explicit", inference=None,
         evidence=[E("DOC033:T179", "I kind of don't want them to change too many things, because. like like I said, it's pretty close to how useful it is to me. and I think changing things might just make it worse."),
                   E("DOC033:T177", "Yeah, I would say it's 9.")],
         judgment=J("direct", "T179 明确表达不希望大幅改动、并给出理由（现在已经够好用、改动可能更糟）；T177 的 9 分作为当前基线写入 context。属维持/避免型目标，按边界规则保留。",
                    sp=["主体：受访者本人", "动作：避免大幅改动", "结果：保持当前可用性"]))
    ,
    dict(candidate_id="G012",
         statement="Keep looking through YouTube's large volume of videos until she finds content she likes.",
         actor="Stakeholder",
         context=["Relies on the sheer volume of available videos"],
         origin="explicit", inference=None,
         evidence=[E("DOC033:T123", "But now I can keep looking until I find something I like, just because of, like the sheer volume of content available."),
                   E("DOC033:T121", "It's probably like the largest accessible repository of videos.")],
         judgment=J("direct", "T123 直接表述『可以一直找，直到找到喜欢的』并给出原因（内容量），T121 说明内容库规模。动作（持续浏览寻找）与结果（找到喜欢的）一致，未把内容库规模本身当成独立目标。",
                    sp=["主体：受访者本人", "动作：在大量视频中持续浏览", "结果：找到喜欢的内容"]))
    ,
    dict(candidate_id="G013",
         statement="Avoid advertisements that run for hours when a video is left playing to fall asleep.",
         actor="Stakeholder",
         context=["Reported as annoying, not a deal breaker; she would not switch platforms over it"],
         origin="inferred",
         inference={"basis_candidate_ids": ["G004"],
                    "reason": "她没有直接提出『不要长广告』的要求，只描述了 G004（睡前播放、留白噪音）时偶尔进入长达两小时广告并称其烦人，随后说这些问题『修好会更好』。由该场景下的抱怨加改进意愿推断出希望避免该状态的意图。",
                    "assumptions": ["把『烦人』与『修好会更好』视为对该状态的负面评价与改进意愿，而非纯背景叙述"]},
         evidence=[E("DOC033:T151", "sometimes it goes into advertisements that themselves are 2"),
                   E("DOC033:T155", "I mean, it would definitely be better if they're fixed, but not to the point where if a different platform has it.")],
         judgment=J("inferred", "推断依据来自 T151 的具体现象（睡前播放进入数小时广告、称其烦人）与 T155 的改进意愿；但原文没有直接的『避免』诉求，强度也明确不是 deal breaker。据此仅作为弱目标保留，未写成硬性要求。",
                    sp=["情境：睡前播放视频", "现象：进入时长数小时的广告", "态度：烦人，修好会更好"],
                    asm=["抱怨与『修好会更好』能够支持对避免该状态的推断"]))
    ,
    dict(candidate_id="G014",
         statement="Avoid keeping a watch-later list, revisiting content from memory or starting afresh for the current mood instead.",
         actor="Stakeholder",
         context=["If the content is not already on her mind, she does not want to go back to a list"],
         origin="explicit", inference=None,
         evidence=[E("DOC033:T061", "So if there's anything I want to revisit, I remember it well enough to go back and watch it."),
                   E("DOC033:T061", "I don't want to go back to a list I want to like, start afresh and see what I'm feeling it.")],
         judgment=J("direct", "T061 明确拒绝 watch later/列表，并说明替代方式（凭记忆回看、按当下心情重新开始）。属避免型偏好，按边界规则保留为维持/避免目标；未把它扩大为『禁止任何收藏功能』。",
                    sp=["主体：受访者本人", "动作：不维护稍后观看列表", "替代：凭记忆回看或按当下心情重来"]))
    ,
    dict(candidate_id="G015",
         statement="Listen to music on YouTube alongside the other uses.",
         actor="Stakeholder",
         context=["Mentioned once; the clause after it is garbled and the purpose is unknown"],
         origin="explicit", inference=None,
         evidence=[E("DOC033:T045", "Those are like the 3 main and listening to music, probably to be sick.")],
         judgment=J("insufficient", "原句确实提到『listening to music』，但仅此一处，且句尾『probably to be sick』无法解析，无法确认用途、场景、频率与强度；T041 只说『听多于看』，不能补足音乐用途。因此保留候选为目标但降为支持不足，不升级为已成立诉求。",
                    sp=["提到『听音乐』这一用途"],
                    up=["用途与目的（句尾含混）", "发生情境与频率", "与其他用途的相对重要性"]))
]

# ---------------- decisions ----------------
relations = [
    {"relation_id": "R1", "source_id": "G008", "target_id": "G007", "type": "contribution",
     "status": "supported",
     "conditions": ["When she does not share the Short immediately and wants to share it later"],
     "assumptions": ["A Short she watched earlier can be found again if search works well"],
     "rationale": "原句直接说搜索 Shorts 会让分享更容易：她常常不是看到就分享，而是过后再找。搜索是帮助分享的手段，但不保证分享一定发生，故为贡献而非精化。",
     "evidence_ids": [],
     "evidence_quotes": [E("DOC033:T173", "And searching Youtube shorts would help me share videos more easily, because sometimes I don't share videos as soon as I see them.")]},
    {"relation_id": "R2", "source_id": "G006", "target_id": "G003", "type": "contribution",
     "status": "supported",
     "conditions": ["When the subject is a technical concept that has several iterations"],
     "assumptions": ["Filtered results still contain a video that explains the concept in depth"],
     "rationale": "时长与上传日期筛选帮助找到既新又深入的视频，服务于『看完整长视频以深入主题』的目的；筛选只提高命中率，不保证一定找到或看完。",
     "evidence_ids": [],
     "evidence_quotes": [E("DOC033:T135", "If I want to learn a technical concept right? Sometimes there are several iterations of a technical concept because it's evolved."),
                          E("DOC033:T135", "I would also want a video that explains it in depth.")]},
    {"relation_id": "R3", "source_id": "G005", "target_id": "G012", "type": "contribution",
     "status": "supported",
     "conditions": ["When she browses the recommendation feed rather than searching"],
     "assumptions": ["The personalized feed still contains content she may like"],
     "rationale": "个性化推荐让她不必搜索、直接在推荐流里点选，帮助她一直看到找到喜欢的内容；推荐质量不等于必然命中，故为贡献而非充分实现。",
     "evidence_ids": [],
     "evidence_quotes": [E("DOC033:T049", "So I don't spend that much time searching. I can just click around in my Youtube recommendations most of the time.")]}
]

groups = [
    {"group_id": "GR1", "parent_id": "G012", "child_ids": ["G005", "G006"], "kind": "and",
     "status": "proposed", "completeness": "partial",
     "rationale": "两个子目标分别作用于『刷推荐流』与『主动搜索』两种情境，都能帮助找到喜欢的内容；但同时具备并不足以保证找到，且两者并非在同一情境下同时需要，更像按情境的替代而不是共同满足，因此只保留为待确认候选。",
     "assumptions": ["她会在推荐流与搜索两种情境之间切换", "内容库中存在她可能喜欢的内容"],
     "evidence_ids": [],
     "evidence_quotes": [E("DOC033:T123", "But now I can keep looking until I find something I like, just because of, like the sheer volume of content available."),
                          E("DOC033:T049", "So I don't spend that much time searching. I can just click around in my Youtube recommendations most of the time.")],
     "relation_ids": ["R3"],
     "checks": [
         {"kind": "normal", "origin": "analysis_assumption",
          "scenario": "她在手机上刷 Shorts 推荐流，觉得当前推荐不合口味",
          "outcome": "unknown",
          "rationale": "此情境只用得上个性化推荐（G005），时长/上传日期筛选（G006）不参与，无法证明两者需要同时具备。"},
         {"kind": "exception", "origin": "analysis_assumption",
          "scenario": "她想学一个已演进的技术概念，套用 >20 分钟与最新上传筛选后仍没有合适视频",
          "outcome": "counterexample",
          "rationale": "即使两项能力都在，也可能找不到合适内容，说明该组不满足『共同满足足以实现父目标』，只能算有帮助。"}
     ]}
]

questions = [
    {"target_type": "model", "target_id": "DOC033-goal-model",
     "message": "关系判断记录（已逐项检查、无独立依据故未建边）：G001→G007 只有『先看到再分享』的时间先后（T173），未建 precedes；G013 与 G004 是同一睡前场景中的负面因素，不构成贡献关系；G002 与 G003 同为长视频但目的不同（背景占位 vs 深入主题），不构成精化；G006→G012 与 G006→G003 重叠且『找到喜欢的』范围过宽，未重复连边。是否需要补充其中任一条？"},
    {"target_type": "model", "target_id": "DOC033-goal-model",
     "message": "精化组判断记录（已逐项检查）：G003←[G006] 与 G007←[G008] 都只有一个子目标，不能构成 AND 组；G002←[内容选择, 设备/切标签] 属于 G002 已承接的手段，拆出即为机械拆分；G001←[醒后, 回家后] 是同一目标的两个情境例，不构成共同满足。仅 GR1（G012←[G005,G006]）保留为 proposed/partial，并附一条反例检查。是否接受不建立其他精化组？"},
    {"target_type": "goal", "target_id": "G008",
     "message": "G008（搜索 Shorts）与 G011（不要大改）存在张力：她同时说这些问题不是 deal breaker、不会因此换平台（T155）。此外她明确不要『稍后观看列表』（G014），搜索能力是否会被她视为同一类负担？"},
    {"target_type": "goal", "target_id": "G009",
     "message": "G009 是否应保留为正式目标？她自评临时刷新对日常帮助不大、近年很少发生，且更多发生在其他平台（T173/T175）。"},
    {"target_type": "goal", "target_id": "G010",
     "message": "G010 只是『maybe』式建议，且她随后归纳问题时只数了搜索 Shorts 与临时刷新两项（T170-T172）。是否应降级为低优先级建议而非目标？"},
    {"target_type": "goal", "target_id": "G013",
     "message": "G013 仅由『烦人』与『修好会更好』推断，且明确非 deal breaker；保留为独立目标，还是并入 G004 的例外条件更合适？"},
    {"target_type": "goal", "target_id": "G015",
     "message": "T045 结尾『listening to music, probably to be sick』转写含混，『听音乐』是否应作为独立用途保留？"}
]

# ---------------- ledger ----------------
entries = []


def EN(cid, disp, gids, reason):
    entries.append({"candidate_id": cid, "disposition": disp, "final_goal_ids": gids, "reason": reason})


EN("C001", "keep", ["G001"], "无聊时看 Shorts 求娱乐/分散注意力，是 G001 的主依据。")
EN("C002", "keep", ["G003"], "长视频用于深入主题，构成独立的 G003。")
EN("C003", "keep", ["G002"], "笔记本后台播放长视频，构成 G002 的主依据。")
EN("C004", "merge", ["G002"], "主要听音频、缺乏看视频的耐心，是 G002 的方式条件，不另立目标。")
EN("C005", "merge", ["G002"], "『听多于看』是同一后台收听习惯的概括，并入 G002。")
EN("C006", "merge", ["G001"], "主要用途之一，与 C001 同义，并入 G001。")
EN("C007", "merge", ["G002"], "主要用途之一，与 C003 同义，并入 G002。")
EN("C008", "keep", ["G004"], "睡前播放/白噪音是独立用途，单列 G004。")
EN("C009", "keep", ["G015"], "提到听音乐但句尾含混，保留为支持不足的 G015，不升级。")
EN("C010", "merge", ["G002"], "按可否只听声音选内容，是 G002 的选择条件。")
EN("C011", "merge", ["G005"], "少搜索、直接点推荐，是个性化首页带来的结果，并入 G005。")
EN("C012", "merge", ["G008"], "『Shorts 里从不搜索、也很难搜』是 G008 的现状与障碍线索。")
EN("C013", "exclude", [], "现状描述（不关注创作者），无独立意图；个性化事实已由 C011/C014 承接。")
EN("C014", "keep", ["G005"], "希望得到相关推荐、无关推荐妨碍放松并因此重开历史，构成 G005。")
EN("C015", "merge", ["G005"], "保持历史开启的理由，与 C014 同一目标。")
EN("C016", "keep", ["G014"], "不要列表、凭记忆或按当下心情重来，构成 G014。")
EN("C017", "merge", ["G001"], "醒后/回家后滑 YouTube 是 G001 的典型情境，并入其 context。")
EN("C018", "merge", ["G002"], "后台长视频帮助专注及走神例外，均属 G002。")
EN("C019", "keep", ["G012"], "看重内容库规模，构成 G012 的前提。")
EN("C020", "merge", ["G012"], "能一直找到喜欢的内容，是 G012 的核心结果。")
EN("C021", "keep", ["G006"], "使用 >20 分钟时长筛选，构成 G006。")
EN("C022", "merge", ["G006"], "常用筛选项与不在意其他筛选项，是同一检索行为。")
EN("C023", "merge", ["G006"], "两个筛选项的组合目的（最新+深入），并入 G006。")
EN("C024", "keep", ["G007"], "分享 Shorts 到 WhatsApp 保持联系，构成 G007。")
EN("C025", "merge", ["G007"], "只发 Shorts、不发更长内容，是 G007 的否定性限定。")
EN("C026", "keep", ["G008"], "看过之后难以找回，构成 G008 的障碍依据。")
EN("C027", "merge", ["G008"], "想发给妹妹却找不到，是 G008 的具体实例。")
EN("C028", "exclude", [], "总体满意度与『没有其他抱怨』是现状评价，无独立意图；作为 G011 的背景。")
EN("C029", "keep", ["G009"], "想立刻清掉一批内容却无直接办法，构成 G009。")
EN("C030", "keep", ["G013"], "睡前播放进入长广告且烦人，构成 G013。")
EN("C031", "merge", ["G013"], "『修好会更好』是非 deal breaker 的强度限定，主要作为 G013 的推断依据，也限定 G008/G010 的优先级。")
EN("C032", "merge", ["G008"], "把搜索 Shorts 称为最大缺口，强化 C026 的同一目标。")
EN("C033", "keep", ["G010"], "用文字描述想看/不想看，构成 G010（建议强度）。")
EN("C034", "merge", ["G009"], "临时、非彻底地刷新历史，是 G009 的范围限定。")
EN("C035", "merge", ["G009"], "自评对日常帮助不大、近年少发生，作为 G009 的 context 保留。")
EN("C036", "merge", ["G008"], "搜索 Shorts 有助于延后分享，是 G008 的收益说明。")
EN("C037", "merge", ["G009"], "记不清具体情形、更多发生在其他平台，作为 G009 的存疑背景。")
EN("C038", "merge", ["G011"], "9 分满意度是 G011『维持现状』的基线。")
EN("C039", "keep", ["G011"], "不希望大改、怕变差，构成 G011。")
EN("C040", "merge", ["G002"], "点开后切标签继续工作、不用手机端，是 G002 的操作与设备条件。")
EN("C041", "exclude", [], "画中画功能描述，无独立意图；属功能观察。")
EN("C042", "merge", ["G004"], "睡眠定时器『大概会用』，作为 G004 的弱方式线索。")
EN("C043", "exclude", [], "没注意到广告、习惯性跳过，是行为习惯，未提出任何目标。")
EN("C044", "exclude", [], "忽略新功能与直播，是使用习惯，无意图。")
EN("C045", "exclude", [], "对 Shorts 的态度转变回顾，无当前意图。")
EN("C046", "exclude", [], "15 分钟×2 的频次是背景量化，无独立意图；目标不写死数字。")
EN("C047", "merge", ["G002"], "只在需要背景声的日子使用，是 G002 的条件。")
EN("C048", "exclude", [], "按设备的使用频次/时长拆分是背景量化；设备条件已由 T023 在 G001/G002 中承接。")

checks = [
    {"check_id": "S1", "evidence_candidates": [E("DOC033:T021", "So Youtube shorts is when I'm bored and I want to be entertained. or when I just want to. you know, think about other things.")],
     "candidate_ids": ["C001", "C002"], "final_goal_ids": ["G001", "G003"],
     "outcome": "represented", "reason": "同一句里两个用途（Shorts 消遣/长视频深入）分别落到 G001、G003。"},
    {"check_id": "S2", "evidence_candidates": [E("DOC033:T045", "Those are like the 3 main and listening to music, probably to be sick.")],
     "candidate_ids": ["C008", "C009"], "final_goal_ids": ["G004", "G015"],
     "outcome": "represented", "reason": "睡前视频实体化为 G004；听音乐因句尾含混只保留为 insufficient 的 G015。"},
    {"check_id": "S3", "evidence_candidates": [E("DOC033:T053", "So I actually switched on viewing history.")],
     "candidate_ids": ["C014"], "final_goal_ids": ["G005"],
     "outcome": "represented", "reason": "回查确认动作是『重新打开历史』，不是仅表达偏好。"},
    {"check_id": "S4", "evidence_candidates": [E("DOC033:T061", "I don't want to go back to a list I want to like, start afresh and see what I'm feeling it.")],
     "candidate_ids": ["C016"], "final_goal_ids": ["G014"],
     "outcome": "represented", "reason": "回查确认她拒绝的是列表式回看，并给出替代方式。"},
    {"check_id": "S5", "evidence_candidates": [E("DOC033:T065", "sometimes When I get too deep into my work I have to go back and and see what video is being played")],
     "candidate_ids": ["C018"], "final_goal_ids": ["G002"],
     "outcome": "represented", "reason": "例外（走神后视频已换）写入 G002 的 context，未删去。"},
    {"check_id": "S6", "evidence_candidates": [E("DOC033:T135", "I would also want a video that explains it in depth.")],
     "candidate_ids": ["C023"], "final_goal_ids": ["G006"],
     "outcome": "represented", "reason": "回查确认两个筛选项是同时满足（最新且深入），未拆成两个目标。"},
    {"check_id": "S7", "evidence_candidates": [E("DOC033:T141", "It's like hard to find a short once you watched it because you remember random details about it."),
                                               E("DOC033:T163", "the biggest thing for me is being able to search Youtube shorts more effectively.")],
     "candidate_ids": ["C026", "C032"], "final_goal_ids": ["G008"],
     "outcome": "represented", "reason": "障碍与期望合并为同一目标，未把『标题不可搜索』当成独立目标。"},
    {"check_id": "S8", "evidence_candidates": [E("DOC033:T151", "sometimes it goes into advertisements that themselves are 2")],
     "candidate_ids": ["C030"], "final_goal_ids": ["G013"],
     "outcome": "represented", "reason": "仅有抱怨时按 inferred 保留，并在 questions 中标注强度疑问。"},
    {"check_id": "S9", "evidence_candidates": [E("DOC033:T155", "I mean, it would definitely be better if they're fixed, but not to the point where if a different platform has it.")],
     "candidate_ids": ["C031"], "final_goal_ids": ["G013"],
     "outcome": "represented", "reason": "强度限定（非 deal breaker）写入 G013 context 与理由。"},
    {"check_id": "S10", "evidence_candidates": [E("DOC033:T173", "And searching Youtube shorts would help me share videos more easily, because sometimes I don't share videos as soon as I see them.")],
     "candidate_ids": ["C036"], "final_goal_ids": ["G008"],
     "outcome": "represented", "reason": "跨窗回查确认该句是 G008 的收益依据，同时作为 R1（G008→G007）的关系原句。"},
    {"check_id": "S11", "evidence_candidates": [E("DOC033:T145", "There's no like complaints off the top of my head.")],
     "candidate_ids": ["C028"], "final_goal_ids": [],
     "outcome": "excluded", "reason": "『没有其他抱怨』是现状评价，不能据此造目标，也不能否定已列问题。"},
    {"check_id": "S12", "evidence_candidates": [E("DOC033:T071", "I actually didn't even notice")],
     "candidate_ids": ["C043"], "final_goal_ids": [],
     "outcome": "excluded", "reason": "对广告无感/习惯性跳过，没有可提取的意图。"}
]

passes = [{"pass_id": "P1", "kind": "initial", "context": "isolated", "status": "completed",
           "window_results": [{"window_id": "DOC033:W%04d" % i, "status": "processed", "reason": ""}
                              for i in range(1, 96)]}]

spec = {
    "document_id": "DOC033",
    "raw_candidates": raw,
    "goals": goals,
    "review_questions": [
        {"candidate_ids": ["G009"], "question": "临时刷新 feed 是否应保留为正式目标？她自评对日常帮助不大、近年少发生。", "reason": "支持存在但强度与价值存疑。"},
        {"candidate_ids": ["G013"], "question": "由『烦人 + 修好会更好』推断出的避免长广告，是否足以成为独立目标？", "reason": "origin 为 inferred，且明确非 deal breaker。"},
        {"candidate_ids": ["G015"], "question": "听音乐是否应作为一个用途保留？原句结尾无法解析。", "reason": "只有一处且转写含混，支持不足。"},
        {"candidate_ids": ["G008"], "question": "搜索 Shorts 的改进诉求与『不要大改』（G011）如何取舍？两者同时存在，她未给出优先级。", "reason": "两个目标指向相反方向，需要人工判断取舍。"}
    ],
    "limitations": [
        "原文为自动转写，多处含混或字符异常（如 '30Â min'、'one r easily'、'probably to be sick'），影响 G015 与频次类信息。",
        "单次访谈、单一受访者，所述行为均为自报，没有观察、日志或界面证据。",
        "没有屏幕截图或录像，功能细节（睡眠定时器、画中画、自动播放）无法独立核对。",
        "未进行独立语义评审、形式证明与人工确认。"
    ],
    "ledger": {
        "model": "unknown", "temperature": "unknown", "budget": "1 initial pass + <=2 repair rounds",
        "usage": "unknown",
        "skill_revision": "a5952d426b1624a3fcb2ce2829e1ae1ceb15e19dc3309d9571f3bc6b465deb6f",
        "prompt_revision": "task-prompt-v1",
        "planned_passes": 1,
        "stop_reason": "191 轮全部读完，95 个窗口逐一处置；全篇回查后无新的有据意图，按预算停止。",
        "passes": passes,
        "full_context_review": {
            "status": "completed",
            "source_ids": TURN_IDS,
            "reason": "回查全部 191 轮：核对指代（T019→T020 的 'other question'、T045 的 '3 main'、T170-T172 的 'these 2 issues'）、条件继承（T033/T097 的后台播放条件、T139 只分享 Shorts）、例外（T065 走神、T155 非 deal breaker、T173 近年少发生）、相反证据（T145『没有抱怨』与 T141/T151 的问题并存；T061『记得住』与 T141『Shorts 找不到』分属不同对象）。"
        },
        "entries": entries,
        "source_checks": checks
    },
    "decisions": {"relations": relations, "groups": groups, "questions": questions, "reassessments": []}
}

# final validations
for g in goals:
    check(g["evidence"])
    if g["judgment"]["label"] in ("direct", "inferred"):
        assert not g["judgment"]["unsupported_parts"], g["candidate_id"]
for r in relations:
    check(r["evidence_quotes"])
for gr in groups:
    check(gr["evidence_quotes"])

goal_ids = {g["candidate_id"] for g in goals}
assert len(goal_ids) == len(goals)
for e in entries:
    assert set(e["final_goal_ids"]) <= goal_ids, e
assert {e["candidate_id"] for e in entries} == {c["candidate_id"] for c in raw}
assert len({c["candidate_id"] for c in raw}) == len(raw)

out = BASE / "spec.json"
out.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")
print("candidates", len(raw), "goals", len(goals), "relations", len(relations), "groups", len(groups), "checks", len(checks))
