# -*- coding: utf-8 -*-
"""Build spec.json for DOC014 run01 (author-side semantic content only)."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
SRC = json.loads((BASE / "source/DOC014.json").read_text(encoding="utf-8"))
TURNS = {t["source_id"]: t["text"] for t in SRC["turns"]}
WINDOWS = json.loads((BASE / "probe/source-windows.json").read_text(encoding="utf-8"))["windows"]
SKILL_REV = "a5952d426b1624a3fcb2ce2829e1ae1ceb15e19dc3309d9571f3bc6b465deb6f"


def ev(sid, quote, role="basis"):
    assert sid in TURNS, sid
    assert quote in TURNS[sid], "MISSING in %s: %s" % (sid, quote[:90])
    assert TURNS[sid].find(quote) == TURNS[sid].rfind(quote), "AMBIGUOUS in %s: %s" % (sid, quote[:90])
    return {"source_id": sid, "quote": quote, "role": role}


C = []


def cand(cid, statement, modality, context, origin, evidence, pass_id="P1"):
    C.append({"candidate_id": cid, "statement": statement, "actor": "Stakeholder",
              "modality": modality, "context": context, "origin": origin,
              "pass_id": pass_id, "evidence": evidence})


cand("C001", "check the next day's temperature so as to plan whether to wear a thick coat or a light coat",
     "habitual present use ('usually')", ["the day before"], "explicit",
     [ev("DOC014:T001", "So I use it usually to check the temperature outside, especially like the day before. So like, I can plan whether I should wear my thick coat or my light coat.")])
cand("C002", "when it is super cold, skip cycling and take the bus instead",
     "conditional habit ('might')", ["super cold weather", "cycling in the cold is unpleasant"], "explicit",
     [ev("DOC014:T001", "if it's like super cold, I might skip going through bicycle and just go through the bus")])
cand("C003", "check for rain and make sure to have an umbrella when rain is forecast",
     "habitual present use ('make sure')", ["rain in the forecast"], "explicit",
     [ev("DOC014:T001", "and I also check for rains. So if it's if there is a weather forecast for rain. I I make sure I have my umbrella.")])
cand("C004", "temperature and tomorrow's chance of rain are the two things looked at first",
     "habitual ordering ('1st is usually')", [], "explicit",
     [ev("DOC014:T003", "1st is usually temperature, and like the rain meter, like the chance of happening like a rain happening tomorrow.")])
cand("C005", "check the hourly temperature around the time of going out (morning, before classes) and the precipitation chance, treating 25 percent or more as a good chance of rain",
     "habitual present use ('usually')", ["the next day", "morning before classes"], "explicit",
     [ev("DOC014:T005", "So I check usually like, if if in in the morning time, you know, like before our classes, what what the temperature is around that time."),
      ev("DOC014:T005", "And what's the what's the precipitation chances? So that's like between one and 100 usually 25 plus is like a good chance of rain happening.")])
cand("C006", "open weather.com through a Google search, where it appears among the first links, and the city is already filled in",
     "habitual present use", [], "explicit",
     [ev("DOC014:T005", "Sure, I usually just like Google it. Usually weather.com is like among the 1st few links.")])
cand("C007", "the city is remembered because of earlier use or because the Google link opens the current city",
     "belief/guess ('I think', 'pretty sure')", [], "explicit",
     [ev("DOC014:T007", "So I think if you have used weather.com previously, it like, has that city in build.")])
cand("C008", "weather.com is the first place to learn about important or severe weather events and warns the user, especially for the user's own city",
     "expectation ('would be a good spot', 'definitely notice')", ["the user has not already seen the news"], "explicit",
     [ev("DOC014:T011", "it will like warn me like, for example"),
      ev("DOC014:T011", "if if it's happening for my city, I'll definitely notice it"),
      ev("DOC014:T011", "it will be a good 1st place to like get, get to know about some important weather event that's happening")])
cand("C009", "there is probably some guide or resource for staying safe during a severe weather event",
     "belief/guess ('pretty sure'), later retracted as assumption", [], "explicit",
     [ev("DOC014:T011", "I'm pretty sure that they have some sort of guide to like, you know. Make sure you're safe, or something"),
      ev("DOC014:T013", "No, not really. That's my assumption, because I I've never really, you know, as I said, I've never been in a city at the time of like an extreme weather event.")])
cand("C010", "on receiving a weather alert, open the notification and check the severity and details of the event",
     "hypothetical ('probably')", ["an alert arrives"], "explicit",
     [ev("DOC014:T015", "Well, I'll probably open the notification check. You know the severity and all the details that they have about the typhoon")])
cand("C011", "read the official recommendation to decide whether to evacuate, seek shelter, stay inside, or just take an umbrella and a raincoat",
     "hypothetical ('probably')", ["the recommendation depends on severity and available information"], "explicit",
     [ev("DOC014:T015", "I'll read for what they recommend like, should I? Should I evacuate the city? Should I just seek shelter, not go outside or like, just carry a umbrella and a raincoat?")])
cand("C012", "adjust the day's plan according to the alert's severity and the information given",
     "hypothetical ('I'll adjust')", ["severity of the event"], "explicit",
     [ev("DOC014:T015", "And like, yeah, based on that, I'll adjust my day.")])
cand("C013", "as soon as a trip is decided, check historical data or monthly/seasonal forecasts to get an estimate of the weather",
     "habitual practice ('I immediately')", ["weeks before departure", "trip already decided"], "explicit",
     [ev("DOC014:T017", "So yeah, I immediately. Once I find that I'll be going. I either check for historical data if it's available somewhere, or I check for future weather focus because it gives you focus.")])
cand("C014", "use cloud coverage beyond temperature and precipitation to judge a trip, and reconsider or cancel a beach or astronomy trip if it will be overcast",
     "generic advice ('you might need to reconsider', 'might have to cancel')", ["trips whose purpose needs clear skies"], "explicit",
     [ev("DOC014:T017", "if you're going for a beach vacation, let's say, and it's going to be super cloudy. Then, you know, you might need to reconsider, because usually people go there to enjoy sun."),
      ev("DOC014:T017", "So it might have to cancel the trip.")])
cand("C015", "forecasts become more accurate nearer the date, so a final view is available a few days before the trip",
     "general statement", [], "explicit",
     [ev("DOC014:T017", "as you approach the date, the weather, like the weather forecast, becomes usually more accurate. So like a few days before you can get like a final you know, see on what the situation would be like.")])
cand("C016", "wait until two or three days before the trip and then decide go/no-go on the final temperature",
     "recommendation ('should probably')", ["two or three days before", "forecast accuracy by then"], "explicit",
     [ev("DOC014:T019", "So yeah, you should probably wait till the end and then then decide, based on what the final temperature is like. Couple of days before.")])
cand("C017", "there is no way to report a false reading to weather.com",
     "answer: not aware", [], "explicit",
     [ev("DOC014:T021", "Not that I'm aware of.")])
cand("C018", "meteorological data is probably collected by a central US organisation and only displayed by apps like weather.com",
     "belief/guess ('my guess', 'pretty sure')", [], "explicit",
     [ev("DOC014:T023", "So so my guess is, most likely all of the metrological data is collected by some central organization in us.")])
cand("C019", "the stakeholder offers to check where the app gets its data and report back",
     "offer to the interviewer", [], "explicit",
     [ev("DOC014:T025", "But yeah, I can like check for you and come back on that one.")])
cand("C020", "screenshot a below-zero temperature reading and share it on social media, because such temperatures are unusual where the stakeholder comes from",
     "plan ('planning to do it very soon'), not yet done", ["temperature shown below 0"], "explicit",
     [ev("DOC014:T027", "I've not done it yet, but I'm planning to do it very soon."),
      ev("DOC014:T027", "if it if if I do see like a weather where the temperature is showing below 0, I'll probably like screenshot it and share it on my social medias.")])
cand("C021", "weather.com appears to have no in-app share option; the mobile app was not used so this is not certain",
     "observation with uncertainty ('I don't know for sure')", [], "explicit",
     [ev("DOC014:T029", "No, I have not used, and I'm checking now. It doesn't really seem to have anything that you know can show it like as a share option")])
cand("C022", "the UI is acceptable and gets the job done, showing the main information",
     "evaluation ('okay', 'gets the job done')", [], "explicit",
     [ev("DOC014:T031", "So I mean, the ui is okay. It's fairly modern, but not like super modern or very polished. But it gets the job done, I think.")])
cand("C023", "the table format, tabs and hourly detail are helpful",
     "evaluation ('helpful', 'I like')", [], "explicit",
     [ev("DOC014:T033", "So I like the Ui overall.")])
cand("C024", "ads and the colour scheme hinder the experience",
     "complaint", [], "explicit",
     [ev("DOC014:T035", "I think probably the ads, and maybe the color scheme, too")])
cand("C025", "the dull blue background should be plain black or plain white",
     "preference ('I would prefer that')", [], "explicit",
     [ev("DOC014:T035", "because, like the background, is like a dull blue, which I don't really like, you know, they could just make it plain black or plain white. And I would prefer that.")])
cand("C026", "four or five ads plus video pop-ups are too much and distract from quickly checking the weather, while one or two ads are acceptable",
     "complaint with tolerance threshold", [], "explicit",
     [ev("DOC014:T037", "I can understand, like one or 2 ads. But like, if you have 4 or 5 ads and then couple of video ads. it's just too much like it takes it like distracts you, and it takes away from the enjoyment of just, you know, like quickly checking everything and coming out so.")])
cand("C027", "a paid ad-free tier would be considered only if the app were used more than 20-30 minutes a day, so it is not required",
     "conditional willingness, explicitly not required", ["usage above 20-30 minutes per day"], "explicit",
     [ev("DOC014:T041", "But yeah, just because I'm not, I don't use it that often. It's not required.")])
cand("C028", "the radar section could be better, adding multiple parameters such as snow coverage and precipitation",
     "suggestion ('could be better')", [], "explicit",
     [ev("DOC014:T043", "yeah, I think probably the radar could be better."),
      ev("DOC014:T043", "There are like multiple parameters that you you can see, you know, you know, like the snow coverage precipitation. So there are a lot of things there that can be done in the radar section.")])
cand("C029", "two cities (home city and the city in India the stakeholder came from) are kept in the app",
     "current setting", [], "explicit",
     [ev("DOC014:T045", "So it's usually my home city. And then the the city that I was coming from like in India. So yeah, those 2 cities. I have it open.")])
cand("C030", "temperatures should be shown in Celsius rather than the default Fahrenheit",
     "preference ('I do prefer Celsius')", ["unit switch exists at the top of the page"], "explicit",
     [ev("DOC014:T047", "Yeah, so I do prefer Celsius.")])
cand("C031", "apart from the degree unit and the cities, no other personalisation is set",
     "current state", [], "explicit",
     [ev("DOC014:T049", "No, not really, I think. Besides the besides, the degree and the city, nothing nothing else.")])
cand("C032", "the main page has sections for important weather events around the world, and clicking opens a news tab",
     "described use ('it does show me that')", [], "explicit",
     [ev("DOC014:T051", "if I go to the main page it does have sections for like weather events, not necessarily in my city. But you know, like important weather events. Ha! Happening across the world. So it does show me that. And if I click on it, it opens like a news tab in weather.com.")])
cand("C033", "the news tab gives details about the weather event",
     "described use", [], "explicit",
     [ev("DOC014:T053", "Yeah. And it gives the details about like whatever, whether it, whether event is happening.")])
cand("C034", "prefer no notifications from weather.com and keep them off on the Mac/PC",
     "preference ('usually prefer', 'usually off')", ["Mac/PC use"], "explicit",
     [ev("DOC014:T055", "I usually prefer no notifications, like, when I'm on my Mac, like on my PC, basically, so yeah, usually the notifications are off.")])
cand("C035", "notifications are deliberately kept off",
     "preference confirmed", [], "explicit",
     [ev("DOC014:T057", "Yeah, I just prefer it off. So I've kept it off.")])
cand("C036", "notifications are turned off through the browser's site settings permission",
     "description of the existing flow", [], "explicit",
     [ev("DOC014:T059", "So there is a site setting.")])
cand("C037", "location data kept in the local cache can be cleared, so it is not stored anywhere; being logged in raises a worry that a leak could reveal the city",
     "belief plus conditional concern ('that's my guess', 'a little worried')", ["logged-in state for the concern"], "inferred",
     [ev("DOC014:T061", "So yeah, I think if it's in my local cache, you know, I can always just clear it from my cache, and the data is gone right. I don't have to worry about it being stored anywhere. If I am logged in, though, I might be a little worried, because if there is a leak, then someone can identify which city I'm from")])
cand("C038", "the answer to 'one feature you want' was cut off as 'one of the.'",
     "incomplete utterance", [], "explicit",
     [ev("DOC014:T063", "one of the.")])
cand("C039", "no further features are wanted; the app is comprehensive",
     "negative answer", [], "explicit",
     [ev("DOC014:T065", "No, no features that I can think of. I mean, it's pretty comprehensive.")])
cand("C040", "windy.com is used because its radar section is very detailed and the animations are enjoyable",
     "described use ('I really love')", [], "explicit",
     [ev("DOC014:T067", "I do use windy.com and and it's mostly because, as I mentioned earlier, the radar section."),
      ev("DOC014:T067", "I mean, the entire app is just a radar, and it it gives a lot of details. And I really love seeing the animations.")])
cand("C041", "very local weather for specific places (a hiking trail, a mountain-climbing expedition, a hotel in the middle of nowhere) would be helpful instead of city-level weather",
     "suggestion ('would definitely help')", ["when the destination is not a city"], "explicit",
     [ev("DOC014:T067", "You just want to like, see whether at this particular hotel that's in like middle of nowhere."),
      ev("DOC014:T067", "if you're going in like a hiking trail, or if you're going on a mountain climbing expedition"),
      ev("DOC014:T067", "So yeah, having having that very local data would be definitely helpful.")])
cand("C042", "ads separate the content and force scrolling, so the UI could be squished closer together to make it easier to read",
     "complaint plus tentative suggestion ('maybe they can')", [], "explicit",
     [ev("DOC014:T069", "like, everything is separated by ads, like, when I click on from one tap to the next, like there is a big ad chunk between."),
      ev("DOC014:T069", "Maybe they can like just like squish the ui a little bit, you know, make it more like close to each other. So it makes it. It just it just like easier to read.")])
cand("C043", "the app already has an option to star favourite cities",
     "statement of existing feature", [], "explicit",
     [ev("DOC014:T071", "Maybe like it does have the option to like star your favorite cities.")])
cand("C044", "apart from the starred-cities point, everything else is pretty good",
     "closing evaluation", [], "explicit",
     [ev("DOC014:T073", "Yeah, I think that's only the one thing I didn't mention. I think rest. All is pretty good.")])

G = []


def goal(gid, statement, context, origin, evidence, judgment, inference=None):
    G.append({"candidate_id": gid, "statement": statement, "actor": "Stakeholder", "context": context,
              "origin": origin, "inference": inference, "evidence": evidence, "judgment": judgment})


goal("G001",
     "Check the next day's temperature, including the hourly reading for the time of going out, in order to choose between a thick coat and a light coat.",
     ["Checked the day before", "Hourly temperature read for the morning before classes, around the time of going out"],
     "explicit",
     [ev("DOC014:T001", "So I use it usually to check the temperature outside, especially like the day before. So like, I can plan whether I should wear my thick coat or my light coat."),
      ev("DOC014:T005", "So I check usually like, if if in in the morning time, you know, like before our classes, what what the temperature is around that time.")],
     {"label": "direct", "rationale": "原文明确说用天气信息查看温度以决定穿厚外套还是薄外套，并补充按出门前后的小时级温度查看；主体、对象与预期结果一致。",
      "supported_parts": ["查看次日温度", "用于选择厚/薄外套", "按出门时刻的小时级温度查看"],
      "unsupported_parts": [], "assumptions": [], "reasoning_steps": []})
goal("G002",
     "Check the next day's chance of rain and make sure to carry an umbrella when rain is forecast.",
     ["Checked the day before", "A precipitation chance of 25 percent or more is treated as a good chance of rain"],
     "explicit",
     [ev("DOC014:T001", "and I also check for rains. So if it's if there is a weather forecast for rain. I I make sure I have my umbrella."),
      ev("DOC014:T005", "And what's the what's the precipitation chances? So that's like between one and 100 usually 25 plus is like a good chance of rain happening.")],
     {"label": "direct", "rationale": "原文明确：若有降雨预报就确保带伞；25% 以上算较大降雨可能，来自同一回答，作为其判断标准保留，未另设阈值。",
      "supported_parts": ["查看降雨概率", "有降雨预报时确保带伞", "25% 以上视为较大可能"],
      "unsupported_parts": [], "assumptions": [], "reasoning_steps": []})
goal("G003",
     "Skip cycling and take the bus instead when it is super cold.",
     ["Condition: super cold weather", "Cycling in the cold is unpleasant"],
     "explicit",
     [ev("DOC014:T001", "if it's like super cold, I might skip going through bicycle and just go through the bus")],
     {"label": "direct", "rationale": "原文明确给出天很冷时不骑车、改坐公交的选择，条件与替代方式一致；原文用 might，属习惯性取舍，未写成硬性规则。",
      "supported_parts": ["天很冷时改乘公交", "条件为 super cold"],
      "unsupported_parts": [], "assumptions": [], "reasoning_steps": []})
goal("G004",
     "Notice warnings about important or severe weather events, especially when they affect my own city.",
     ["weather.com is where the stakeholder would first see such events", "Events for the stakeholder's city would definitely be noticed"],
     "explicit",
     [ev("DOC014:T011", "it will like warn me like, for example"),
      ev("DOC014:T011", "if if it's happening for my city, I'll definitely notice it")],
     {"label": "direct", "rationale": "原文明确说站点会警告重要天气事件，且若发生在自己城市一定会注意到，并将其视为获知这类事件的第一处。",
      "supported_parts": ["获知重要/恶劣天气事件的警告", "特别关注发生在自己城市的event"],
      "unsupported_parts": [], "assumptions": [], "reasoning_steps": []})
goal("G005",
     "Read news details about important weather events happening around the world from the main page.",
     ["Main page shows event sections, including events outside the stakeholder's city", "Clicking opens a news tab with details"],
     "explicit",
     [ev("DOC014:T051", "if I go to the main page it does have sections for like weather events, not necessarily in my city. But you know, like important weather events. Ha! Happening across the world. So it does show me that. And if I click on it, it opens like a news tab in weather.com."),
      ev("DOC014:T053", "Yeah. And it gives the details about like whatever, whether it, whether event is happening.")],
     {"label": "direct", "rationale": "受访者自述主页有全球重要天气事件栏目并会点开新闻页查看细节，据此表述阅读全球事件新闻；未添加频率或范围要求。",
      "supported_parts": ["主页提供全球重要天气事件", "点开新闻页查看事件细节"],
      "unsupported_parts": [], "assumptions": [], "reasoning_steps": []})
goal("G006",
     "When an alert about an extreme weather event arrives, open the notification and read the severity, details and official recommendations in order to determine whether to evacuate, seek shelter, stay indoors, or just carry an umbrella and a raincoat.",
     ["Stated as what would probably happen; the stakeholder says they have never been in a city during an extreme weather event",
      "The response depends on the severity and the information given"],
     "explicit",
     [ev("DOC014:T015", "Well, I'll probably open the notification check. You know the severity and all the details that they have about the typhoon"),
      ev("DOC014:T015", "I'll read for what they recommend like, should I? Should I evacuate the city? Should I just seek shelter, not go outside or like, just carry a umbrella and a raincoat?")],
     {"label": "direct", "rationale": "原文明确描述收到警报后会打开通知、查看严重程度与细节，并阅读官方建议以决定撤离/避险/留在室内等做法；属设想情境（受访者未经历过城市极端天气），已在 context 保留。",
      "supported_parts": ["打开警报通知", "查看严重程度与细节", "阅读官方建议以确定行动"],
      "unsupported_parts": [], "assumptions": [], "reasoning_steps": []})
goal("G007",
     "Adjust the day's plan according to the alert's severity and the information provided.",
     ["Based on the alert's severity and the information given"],
     "explicit",
     [ev("DOC014:T015", "And like, yeah, based on that, I'll adjust my day.")],
     {"label": "direct", "rationale": "原文明确“基于此调整我的一天”，条件为警报严重程度与所给信息；未扩展为其他调整方式。",
      "supported_parts": ["按警报信息调整当天安排"],
      "unsupported_parts": [], "assumptions": [], "reasoning_steps": []})
goal("G008",
     "Start checking historical data or monthly/seasonal forecasts as soon as a trip is decided, in order to estimate temperature, precipitation and cloud cover weeks ahead.",
     ["Checked immediately once the trip is known", "Weeks before departure"],
     "explicit",
     [ev("DOC014:T017", "So yeah, I immediately. Once I find that I'll be going. I either check for historical data if it's available somewhere, or I check for future weather focus because it gives you focus.")],
     {"label": "direct", "rationale": "原文明确：一确定要出行就查历史数据或月度/未来预报，以对天气有大致估计；时间条件（提前数周）与查询方式均保留。",
      "supported_parts": ["出行确定后立即查看", "查历史数据或月度预报", "目的是取得天气估计"],
      "unsupported_parts": [], "assumptions": [], "reasoning_steps": []})
goal("G009",
     "Use forecast cloud cover to judge whether the trip's purpose (enjoying sun at a beach, viewing an astronomical event) is still achievable, and reconsider or cancel the trip if it will be overcast.",
     ["Applies to trips whose purpose depends on clear skies"],
     "explicit",
     [ev("DOC014:T017", "if you're going for a beach vacation, let's say, and it's going to be super cloudy. Then, you know, you might need to reconsider, because usually people go there to enjoy sun."),
      ev("DOC014:T017", "So it might have to cancel the trip.")],
     {"label": "direct", "rationale": "原文明确除温度与降水外还看云量，并举海滩晒太阳与观星为例说明可能需重新考虑或取消；原文为泛化第二人称建议，未扩大为所有行程。",
      "supported_parts": ["把云量纳入行程判断", "云量不利时重新考虑或取消"],
      "unsupported_parts": [], "assumptions": [], "reasoning_steps": []})
goal("G010",
     "Wait until two or three days before departure and then make the final go/no-go decision based on the more accurate temperature forecast.",
     ["Two or three days before departure", "Forecast is usually right at that range"],
     "explicit",
     [ev("DOC014:T019", "So yeah, you should probably wait till the end and then then decide, based on what the final temperature is like. Couple of days before."),
      ev("DOC014:T017", "as you approach the date, the weather, like the weather forecast, becomes usually more accurate.")],
     {"label": "direct", "rationale": "原文明确建议等到出发前两三天，再按最终温度决定去不去；保留“probably”的建议强度，未写成硬性规则。",
      "supported_parts": ["等到出发前两三天", "按最终温度做去/不去的决定"],
      "unsupported_parts": [], "assumptions": [], "reasoning_steps": []})
goal("G011",
     "Screenshot a below-zero temperature reading and share it on social media, because such temperatures are unusual where I come from.",
     ["Stated as a plan; not yet done", "When a below-zero temperature reading appears"],
     "explicit",
     [ev("DOC014:T027", "I've not done it yet, but I'm planning to do it very soon."),
      ev("DOC014:T027", "if it if if I do see like a weather where the temperature is showing below 0, I'll probably like screenshot it and share it on my social medias.")],
     {"label": "direct", "rationale": "原文明确说计划很快这么做：显示零下温度时截图并发到社交媒体；同时说明尚未做过，已在 context 标注。",
      "supported_parts": ["零下温度时截图", "分享到社交媒体", "尚未执行，属计划"],
      "unsupported_parts": [], "assumptions": [], "reasoning_steps": []})
goal("G012",
     "See at most one or two ads, with no video pop-ups, so that checking the weather stays quick and undistracted.",
     ["The page currently carries four or five ads, some of them video pop-ups"],
     "explicit",
     [ev("DOC014:T037", "I can understand, like one or 2 ads. But like, if you have 4 or 5 ads and then couple of video ads. it's just too much like it takes it like distracts you, and it takes away from the enjoyment of just, you know, like quickly checking everything and coming out so.")],
     {"label": "direct", "rationale": "原文给出可接受上限（一两条广告），并说四五条加视频弹窗过多、打断快速查看；数量与结果均来自原话。",
      "supported_parts": ["广告数量应为一两条", "不要视频弹窗", "目的是快速、不受打扰地查看"],
      "unsupported_parts": [], "assumptions": [], "reasoning_steps": []})
goal("G013",
     "Arrange related weather information more compactly, as a tentative suggestion, so that it can be read without scrolling past large ad blocks.",
     ["Stated as a tentative suggestion ('maybe they can')"],
     "explicit",
     [ev("DOC014:T069", "Maybe they can like just like squish the ui a little bit, you know, make it more like close to each other. So it makes it. It just it just like easier to read."),
      ev("DOC014:T069", "like, everything is separated by ads, like, when I click on from one tap to the next, like there is a big ad chunk between.")],
     {"label": "direct", "rationale": "原文明确建议把界面压紧、让内容彼此靠近以便阅读，起因是广告把内容隔开、需要上下滚动；保留试探性语气。",
      "supported_parts": ["内容布局更紧凑", "避免大块广告隔断、减少滚动", "属试探性建议"],
      "unsupported_parts": [], "assumptions": [], "reasoning_steps": []})
goal("G014",
     "Make the radar section more detailed and intuitive, with multiple parameters such as snow coverage and precipitation and with animations.",
     ["Compared with windy.com, which the stakeholder uses for its radar and animations"],
     "explicit",
     [ev("DOC014:T043", "yeah, I think probably the radar could be better."),
      ev("DOC014:T043", "There are like multiple parameters that you you can see, you know, you know, like the snow coverage precipitation. So there are a lot of things there that can be done in the radar section."),
      ev("DOC014:T067", "I mean, the entire app is just a radar, and it it gives a lot of details. And I really love seeing the animations.")],
     {"label": "direct", "rationale": "原文明确说雷达可以更好，可加入雪覆盖、降水等多参数，并以更详细直观的雷达产品作参照；动画来自其对 windy.com 的偏好，一并保留在目标中。",
      "supported_parts": ["雷达更详细直观", "支持多参数（雪、降水）", "保留动画偏好"],
      "unsupported_parts": [], "assumptions": [], "reasoning_steps": []})
goal("G015",
     "Provide very local weather for specific places such as a hiking trail, a mountain-climbing route, or a hotel in a remote area, not just city-level weather.",
     ["When the destination is not a city"],
     "explicit",
     [ev("DOC014:T067", "So yeah, having having that very local data would be definitely helpful."),
      ev("DOC014:T067", "You just want to like, see whether at this particular hotel that's in like middle of nowhere."),
      ev("DOC014:T067", "if you're going in like a hiking trail, or if you're going on a mountain climbing expedition")],
     {"label": "direct", "rationale": "原文明确“非常本地的数据会很有帮助”，场景为徒步、登山与偏僻酒店，并说明城市级信息在此不够用。",
      "supported_parts": ["提供非城市地点的本地天气", "场景为徒步/登山/偏僻酒店"],
      "unsupported_parts": [], "assumptions": [], "reasoning_steps": []})
goal("G016",
     "View temperatures in Celsius instead of the default Fahrenheit.",
     ["US default is Fahrenheit", "A unit switch exists at the top of the page"],
     "explicit",
     [ev("DOC014:T047", "Yeah, so I do prefer Celsius.")],
     {"label": "direct", "rationale": "原文明确偏好摄氏显示，且说明可通过顶部下拉切换；作为偏好保留，未升级为强制要求。",
      "supported_parts": ["偏好摄氏"],
      "unsupported_parts": [], "assumptions": [], "reasoning_steps": []})
goal("G017",
     "Keep weather.com notifications turned off.",
     ["On Mac/PC", "Stated as 'I just prefer it off'"],
     "explicit",
     [ev("DOC014:T055", "I usually prefer no notifications, like, when I'm on my Mac, like on my PC, basically, so yeah, usually the notifications are off."),
      ev("DOC014:T057", "Yeah, I just prefer it off. So I've kept it off.")],
     {"label": "direct", "rationale": "原文明确偏好不收通知并已保持关闭，属维持现状的避免型目标；限定在 Mac/PC 使用情境。",
      "supported_parts": ["偏好不接收通知", "已保持关闭"],
      "unsupported_parts": [], "assumptions": [], "reasoning_steps": []})
goal("G018",
     "Keep location data in a locally clearable cache rather than stored on the service, so that a leak cannot reveal which city I am from.",
     ["Concern is conditional on being logged in", "The storage location is the stakeholder's guess, not verified"],
     "inferred",
     [ev("DOC014:T061", "So yeah, I think if it's in my local cache, you know, I can always just clear it from my cache, and the data is gone right. I don't have to worry about it being stored anywhere. If I am logged in, though, I might be a little worried, because if there is a leak, then someone can identify which city I'm from")],
     {"label": "inferred", "rationale": "原文没有直接提出隐私要求，只说数据在本地缓存就能清掉、不必担心被存储，并在登录状态下担心泄露可识别城市。据此推断其希望位置数据可本地清除且不被服务端留存，故判 inferred；未把其“应该只存在本地”的猜测当作已核实事实。",
      "supported_parts": ["希望位置数据可自行清除", "不希望数据被存储", "登录时担心泄露暴露城市"],
      "unsupported_parts": [], "assumptions": ["受访者对缓存/存储位置的判断是猜测，但偏好方向不依赖该判断成立"],
      "reasoning_steps": ["由其“可清缓存、不必担心被存储”的表述推断出对本地可清除的偏好", "由登录状态下对泄露的担忧推断出对服务端留存的回避"]},
     inference={"basis_candidate_ids": ["G018"],
                "reason": "由“数据在本地缓存即可清掉、不必担心被存储”与登录时担心泄露可识别城市，推断出对位置数据本地可清除、不被留存的偏好。",
                "assumptions": ["受访者关于存储位置的判断是猜测；本目标只承接其偏好方向，不声称站点确实不存储。"]})

ENTRIES = {
    "C001": ("keep", ["G001"], "原文明确用次日温度决定厚/薄外套，保留温度查看与选衣结果。"),
    "C002": ("keep", ["G003"], "明确天很冷时不骑车改坐公交，条件与替代方式保留。"),
    "C003": ("keep", ["G002"], "明确有降雨预报就确保带伞。"),
    "C004": ("split", ["G001", "G002"], "同一回答把“最先看温度”和“明日降雨概率”并列为两项查看对象，分别对应温度与降雨目标，未含新条件。"),
    "C005": ("split", ["G001", "G002"], "小时级温度（上课前/出门时）归入温度目标；降雨概率与“25+ 算较大可能”归入带伞目标。"),
    "C006": ("exclude", [], "描述用 Google 打开站点、城市已预填的使用习惯，未表达要达到或维持的结果。"),
    "C007": ("exclude", [], "对城市识别机制（早前使用、从 Google 进入）的猜测，属信念而非目标。"),
    "C008": ("keep", ["G004"], "明确会警告、若发生在自己城市一定注意到，并称其为获知重要事件的第一处。"),
    "C009": ("exclude", [], "关于“应有安全指南/资源”的猜测，T013 自述纯属 assumption 且未见过，不作为目标或事实。"),
    "C010": ("keep", ["G006"], "收到警报后先打开通知看严重程度与细节。"),
    "C011": ("merge", ["G006"], "与 C010 同一动作链：读官方建议以确定撤离/避险/留在室内等做法，合并为一个“读警报与建议”目标。"),
    "C012": ("keep", ["G007"], "“基于此调整我的一天”是与读取信息不同的独立结果。"),
    "C013": ("keep", ["G008"], "一确定出行就查历史数据或月度预报以取得估计。"),
    "C014": ("keep", ["G009"], "云量影响海滩/观星行程，可能需要重新考虑或取消。"),
    "C015": ("merge", ["G010"], "“越接近日期越准、出发前几天可看到最终情况”与 C016“等到最后再决定”同义，合并。"),
    "C016": ("keep", ["G010"], "明确建议等到出发前两三天按最终温度决定。"),
    "C017": ("exclude", [], "回答“没有反馈机制”，未表达希望增加该功能。"),
    "C018": ("exclude", [], "对气象数据来源（中央政府机构）的猜测，属信念。"),
    "C019": ("exclude", [], "只是答应替采访者去查数据来源，非产品目标。"),
    "C020": ("keep", ["G011"], "计划把零下温度截图发社交媒体，条件与动机保留。"),
    "C021": ("exclude", [], "说明站点无站内分享选项且未用移动端，未提出希望。"),
    "C022": ("exclude", [], "对现有 UI“够用、展示主要信息”的评价，无改变要求。"),
    "C023": ("exclude", [], "对表格、标签页与小时级详情的满意描述，属现状能力。"),
    "C024": ("keep", ["G012"], "明确指出广告妨碍体验，作为希望减少的对象。"),
    "C025": ("exclude", [], "对背景配色的口味偏好（暗蓝→纯黑/白），属审美背景，未形成结果性要求。"),
    "C026": ("merge", ["G012"], "与 C024 同一诉求（广告过多、视频弹窗打断快速查看），补充可接受上限“一两条”。"),
    "C027": ("exclude", [], "去广告付费只在每天使用 20-30 分钟以上的假设下才考虑，并明确“not required”。"),
    "C028": ("keep", ["G014"], "明确雷达可以更好，并指出可加雪、降水等多参数。"),
    "C029": ("exclude", [], "只描述已设置的两个城市，未表达维持或改变意图。"),
    "C030": ("keep", ["G016"], "明确偏好摄氏显示。"),
    "C031": ("exclude", [], "回答除单位与城市外无其他个性化，无意图。"),
    "C032": ("keep", ["G005"], "主页有全球重要天气事件栏目、点击进入新闻页，属实际使用。"),
    "C033": ("merge", ["G005"], "与 C032 同一使用：新闻页给出事件细节。"),
    "C034": ("keep", ["G017"], "明确偏好不接收通知且保持关闭。"),
    "C035": ("merge", ["G017"], "与 C034 同一偏好的确认（prefer it off, kept it off）。"),
    "C036": ("exclude", [], "讲述关闭通知的操作路径（站点设置），属操作说明。"),
    "C037": ("keep", ["G018"], "由可清缓存、不希望被存储、登录时担心泄露推断隐私目标（origin=inferred）。"),
    "C038": ("exclude", [], "“one of the.”为被打断的残句，无可判定语义。"),
    "C039": ("exclude", [], "明确表示没有想加的功能，产品已很全面。"),
    "C040": ("merge", ["G014"], "使用 windy.com 主要因雷达详细且喜欢动画，与雷达改进诉求同向。"),
    "C041": ("keep", ["G015"], "希望有非城市级的本地天气（徒步、登山、偏僻酒店）。"),
    "C042": ("split", ["G012", "G013"], "同段既抱怨广告把内容隔开，又建议压缩布局使内容靠近、更易读，两个可独立满足的结果分别成立。"),
    "C043": ("exclude", [], "提到可收藏城市属已有功能，无改变或维持要求。"),
    "C044": ("exclude", [], "收尾评价“其余都不错”，无目标。"),
}

CHECKS = [
    ("S1", [ev("DOC014:T001", "So I use it usually to check the temperature outside, especially like the day before. So like, I can plan whether I should wear my thick coat or my light coat.")],
     ["C001", "C004", "C005"], ["G001", "G002"], "represented", "日常查看温度的原始句，拆分为温度与降雨两目标后均可回查。"),
    ("S2", [ev("DOC014:T001", "if it's like super cold, I might skip going through bicycle and just go through the bus")],
     ["C002"], ["G003"], "represented", "天冷改乘公交的条件与替代方式保留在 G003。"),
    ("S3", [ev("DOC014:T005", "And what's the what's the precipitation chances? So that's like between one and 100 usually 25 plus is like a good chance of rain happening.")],
     ["C005"], ["G001", "G002"], "represented", "小时级查看与 25% 阈值分别归入温度、降雨目标。"),
    ("S4", [ev("DOC014:T011", "if if it's happening for my city, I'll definitely notice it")],
     ["C008"], ["G004"], "represented", "以自己城市为重点的警报意图保留。"),
    ("S5", [ev("DOC014:T013", "No, not really. That's my assumption, because I I've never really, you know, as I said, I've never been in a city at the time of like an extreme weather event.")],
     ["C009"], [], "excluded", "安全指南属受访者自认的猜测，未见过，不作为目标。"),
    ("S6", [ev("DOC014:T015", "And like, yeah, based on that, I'll adjust my day.")],
     ["C010", "C011", "C012"], ["G006", "G007"], "represented", "读取警报信息与调整当天安排分别成立，并保留其依赖关系。"),
    ("S7", [ev("DOC014:T017", "So yeah, I immediately. Once I find that I'll be going. I either check for historical data if it's available somewhere, or I check for future weather focus because it gives you focus.")],
     ["C013"], ["G008"], "represented", "出行前的早期查看与时间条件保留。"),
    ("S8", [ev("DOC014:T017", "if you're going for a beach vacation, let's say, and it's going to be super cloudy. Then, you know, you might need to reconsider, because usually people go there to enjoy sun.")],
     ["C014"], ["G009"], "represented", "云量影响行程目的的判断保留。"),
    ("S9", [ev("DOC014:T019", "So yeah, you should probably wait till the end and then then decide, based on what the final temperature is like. Couple of days before.")],
     ["C015", "C016"], ["G010"], "represented", "等待到出发前再决定的时间条件与建议强度保留。"),
    ("S10", [ev("DOC014:T017", "So it might have to cancel the trip."), ev("DOC014:T019", "So yeah, you should probably wait till the end and then then decide, based on what the final temperature is like. Couple of days before.")],
     ["C014", "C016"], ["G009", "G010"], "uncertain", "原文先说数周前可因云量重新考虑/取消，后又说等出发前两三天再决定，时点关系未定。"),
    ("S11", [ev("DOC014:T027", "I've not done it yet, but I'm planning to do it very soon.")],
     ["C020"], ["G011"], "represented", "分享计划及其未执行状态保留。"),
    ("S12", [ev("DOC014:T037", "I can understand, like one or 2 ads. But like, if you have 4 or 5 ads and then couple of video ads. it's just too much like it takes it like distracts you, and it takes away from the enjoyment of just, you know, like quickly checking everything and coming out so.")],
     ["C024", "C026"], ["G012"], "represented", "广告过多与可接受上限合并为减少广告目标。"),
    ("S13", [ev("DOC014:T069", "Maybe they can like just like squish the ui a little bit, you know, make it more like close to each other. So it makes it. It just it just like easier to read.")],
     ["C042"], ["G012", "G013"], "represented", "同段被拆为广告数量与布局紧凑两个结果。"),
    ("S14", [ev("DOC014:T041", "But yeah, just because I'm not, I don't use it that often. It's not required.")],
     ["C027"], [], "excluded", "付费去广告为条件性设想且明确非必需。"),
    ("S15", [ev("DOC014:T043", "yeah, I think probably the radar could be better.")],
     ["C028", "C040"], ["G014"], "represented", "雷达改进诉求合并，含 windy.com 的动画偏好。"),
    ("S16", [ev("DOC014:T067", "So yeah, having having that very local data would be definitely helpful.")],
     ["C041"], ["G015"], "represented", "非城市地点的本地天气需求保留。"),
    ("S17", [ev("DOC014:T047", "Yeah, so I do prefer Celsius.")],
     ["C030"], ["G016"], "represented", "摄氏偏好保留为软目标。"),
    ("S18", [ev("DOC014:T057", "Yeah, I just prefer it off. So I've kept it off.")],
     ["C034", "C035"], ["G017"], "represented", "关闭通知的偏好与现状合并为维持型目标。"),
    ("S19", [ev("DOC014:T061", "So yeah, I think if it's in my local cache, you know, I can always just clear it from my cache, and the data is gone right. I don't have to worry about it being stored anywhere. If I am logged in, though, I might be a little worried, because if there is a leak, then someone can identify which city I'm from")],
     ["C037"], ["G018"], "represented", "隐私目标按推断处理，并标注其猜测与条件性担忧。"),
    ("S20", [ev("DOC014:T051", "if I go to the main page it does have sections for like weather events, not necessarily in my city. But you know, like important weather events. Ha! Happening across the world. So it does show me that. And if I click on it, it opens like a news tab in weather.com.")],
     ["C032", "C033"], ["G005"], "represented", "全球天气事件新闻的阅读目标保留。"),
    ("S21", [ev("DOC014:T021", "Not that I'm aware of."), ev("DOC014:T025", "But yeah, I can like check for you and come back on that one.")],
     ["C017", "C018", "C019"], [], "excluded", "反馈机制、数据来源与代查承诺均非目标。"),
    ("S22", [ev("DOC014:T035", "because, like the background, is like a dull blue, which I don't really like, you know, they could just make it plain black or plain white. And I would prefer that.")],
     ["C025"], [], "excluded", "配色为审美口味，未产生结果性要求。"),
    ("S23", [ev("DOC014:T045", "So it's usually my home city. And then the the city that I was coming from like in India. So yeah, those 2 cities. I have it open."), ev("DOC014:T049", "No, not really, I think. Besides the besides, the degree and the city, nothing nothing else.")],
     ["C029", "C031"], [], "excluded", "现有设置描述，无维持或改变意图。"),
    ("S24", [ev("DOC014:T029", "No, I have not used, and I'm checking now. It doesn't really seem to have anything that you know can show it like as a share option")],
     ["C021"], [], "excluded", "站内分享缺失属观察，未提出希望。"),
    ("S25", [ev("DOC014:T065", "No, no features that I can think of. I mean, it's pretty comprehensive.")],
     ["C039", "C044"], [], "excluded", "明确表示无额外功能需求。"),
]

WIDS = [w["window_id"] for w in WINDOWS]
passes = []
for pid, kind in (("P1", "initial"), ("P2", "full_context")):
    passes.append({"pass_id": pid, "kind": kind, "context": "isolated", "status": "completed",
                   "window_results": [{"window_id": wid, "status": "processed", "reason": ""} for wid in WIDS]})

RELATIONS = [
    {"relation_id": "R1", "source_id": "G006", "target_id": "G007", "type": "contribution",
     "status": "supported", "conditions": ["alert arrives for the stakeholder's city"], "assumptions": [],
     "rationale": "读取警报的严重程度与官方建议，是随后调整当天安排所依据的信息，属有帮助但不构成充分保证。",
     "evidence_ids": [],
     "evidence_quotes": [ev("DOC014:T015", "And like, yeah, based on that, I'll adjust my day.")]},
    {"relation_id": "R2", "source_id": "G004", "target_id": "G006", "type": "precedes",
     "status": "supported", "conditions": ["a weather alert is issued"], "assumptions": [],
     "rationale": "先收到并注意到警报，才会去打开通知查看细节；原文按此顺序描述。",
     "evidence_ids": [],
     "evidence_quotes": [ev("DOC014:T015", "Well, I'll probably open the notification check. You know the severity and all the details that they have about the typhoon")]},
    {"relation_id": "R3", "source_id": "G008", "target_id": "G010", "type": "precedes",
     "status": "supported", "conditions": [], "assumptions": ["比较对象是同一次行程"],
     "rationale": "原文先说出发前数周开始查看并取得估计，再说临近日期预报更准、出发前几天看到最终情况，最终决定在后。",
     "evidence_ids": [],
     "evidence_quotes": [ev("DOC014:T017", "as you approach the date, the weather, like the weather forecast, becomes usually more accurate. So like a few days before you can get like a final you know, see on what the situation would be like.")]},
]

spec = {
    "document_id": "DOC014",
    "raw_candidates": C,
    "goals": G,
    "review_questions": [
        {"candidate_ids": ["G012", "G013"],
         "question": "减少广告与压缩布局是否应视为同一要求（同一目的的两个手段），还是两个可独立满足的目标？",
         "reason": "两者同源于“广告把内容隔开、影响快速阅读”的抱怨，当前按两个结果分别保留。"},
        {"candidate_ids": ["G018"],
         "question": "隐私目标是否成立：原文以存储位置的猜测和登录状态下的条件性担忧表述，未见明确要求。",
         "reason": "避免把信念当事实或把担忧升级为强制需求。"},
        {"candidate_ids": ["G006", "G007"],
         "question": "警报处置目标全部来自“未经历过极端天气”的设想，是否需要标注为待验证而非既定做法？",
         "reason": "受访者自述没有城市极端天气经历，T011 亦称 not sure。"},
        {"candidate_ids": [],
         "question": "G001-G003 的日常查看是否共享一个未明示的“按天气安排一天”的上层目标？",
         "reason": "原文未提出该上层目标，因此未建根也未建精化组。"},
    ],
    "limitations": [
        "唯一资料为单次访谈转写，只有一位 Stakeholder，没有产品实测、界面截图或官方文档可核对。",
        "转写含识别问题（如 future weather focus 应为 forecast、viney.com、Â°C 编码残留），引用保持原样，未静默改写。",
        "极端天气相关目标基于受访者设想（其自述未在城市经历极端天气），不能当作已发生行为的记录。",
        "隐私目标依赖受访者对缓存与存储位置的猜测，未经核实。",
    ],
    "ledger": {
        "model": "unknown", "temperature": "unknown", "budget": "1 initial pass + <=2 repair rounds",
        "usage": "unknown", "skill_revision": SKILL_REV, "prompt_revision": "task-prompt-v1",
        "planned_passes": 2,
        "stop_reason": "完成一轮逐窗捕获与一轮全篇校正；无新增有据意图，剩余分歧（决策时点、目标合并、隐私推断）无新证据，保留为问题后停止。",
        "passes": passes,
        "full_context_review": {
            "status": "completed",
            "reason": "回查全部 75 轮：核对跨轮指代（it/they/that 指广告、雷达、通知、城市缓存）、条件继承（super cold、若有降雨预报、收到警报、出行确定后、登录状态）、让步与例外（“not necessarily directly from the app”、广告“一两条可以接受”、付费“not required”）、相反证据（T013 否认见过安全指南、T011 自述 not sure、T019 与 T017 的决策时点张力），并复核合并簇与排除项。"},
        "entries": [{"candidate_id": cid, "disposition": d, "final_goal_ids": g, "reason": r}
                    for cid, (d, g, r) in sorted(ENTRIES.items())],
        "source_checks": [{"check_id": cid, "evidence_candidates": e, "candidate_ids": cs,
                           "final_goal_ids": gs, "outcome": oc, "reason": rr}
                          for cid, e, cs, gs, oc, rr in CHECKS],
    },
    "decisions": {
        "relations": RELATIONS,
        "groups": [],
        "questions": [
            {"target_type": "model", "target_id": "DOC014-goal-model",
             "message": "G001-G003 的日常查看目标没有上层目标与精化组；原文未提出“按天气安排一天”这类上层目标，是否需要补充需回到原文确认。"},
            {"target_type": "goal", "target_id": "G010",
             "message": "G010 建议等到出发前两三天决定，与 G009 的提前判断时点不同；当前并列保留、未建立联系，需确认适用行程类型。"},
            {"target_type": "goal", "target_id": "G011",
             "message": "分享零下温度的截图尚未发生（原文为计划），当前保留为目标，需确认是否应按“计划”而非现行做法对待。"},
        ],
        "reassessments": [],
    },
}

(BASE / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# sanity report
missing = [e for g in G for e in g["evidence"] if e["quote"] not in TURNS[e["source_id"]]]
print("goals", len(G), "candidates", len(C), "checks", len(CHECKS), "windows", len(WIDS), "missing", len(missing))
print("entries", len(ENTRIES), "goals covered", sorted({x for _, gs, _ in ENTRIES.values() for x in gs}) == sorted(g["candidate_id"] for g in G))
