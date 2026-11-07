# -*- coding: utf-8 -*-
"""Build spec.json for DOC021 attempt-01 (authorial semantic content)."""
import json

T = "DOC021:T"


def ev(sid, quote, role="basis"):
    return {"source_id": T + sid, "quote": quote, "role": role}


raw = []


def cand(cid, statement, modality, context, origin, evidence, pass_id="P1"):
    raw.append({"candidate_id": cid, "statement": statement, "actor": "Stakeholder",
                "modality": modality, "context": context, "origin": origin,
                "pass_id": pass_id, "evidence": evidence})


cand("C001", "When moving to a new neighborhood or a new country, the stakeholder needs to find a new place to live.",
     "declared need ('I need to')", ["relocation trigger"], "explicit",
     [ev("003", "Mainly when I move to a new neighborhood or to a new country, I need to find a new place.")])
cand("C002", "Choose the neighborhood or place where the house should be before starting the keyword search, then search with keywords for that area.",
     "usual practice ('usually I choose ... and then I start searching')", ["search starts from a chosen area"], "explicit",
     [ev("005", "So usually I choose a neighborhood or a place where I want to find a house in, and then I start searching by such keywords to find relevant websites for that specific area")])
cand("C003", "Find out which websites are the most popular or most used in the target area, especially when it is another country.",
     "stated want ('I want to be familiar')", ["area may be abroad"], "explicit",
     [ev("005", "So I want to be familiar with which websites are the most popular or most used there.")])
cand("C004", "Use listing sites to spot the neighborhoods where options fitting the budget and requirements are clustered.",
     "one way among several", ["listing sites show available houses and apartments"], "explicit",
     [ev("007", "Sometimes there are options that fits my budget and fits my requirements more clustered in specific neighborhoods")])
cand("C005", "Ask people who live in the country for recommendations about places.",
     "one way among several ('another way')", ["people living in the target country"], "explicit",
     [ev("007", "is asking people who lives, for example in that country, if they have any recommendation for the places")])
cand("C006", "Pick a neighborhood close to a fixed destination such as a job or a college.",
     "usual practice ('I will usually pick')", ["only when a job or college anchors the location"], "explicit",
     [ev("007", "if I have a specific job, or if I'm studying at specific college, I will usually pick a neighborhood that's close to that area")])
cand("C007", "Search listings by size of the place or bedroom counts together with a budget limit.",
     "usual practice ('I will search')", ["budget limit applies with size"], "explicit",
     [ev("009", "So actually, I will search by like the size of the place, or sometimes by bedroom counts. and with also a budget limit.")])
cand("C008", "After getting many options, filter them down with less important criteria such as amenities, extra features and how good looking the place is.",
     "usual practice ('I can start filtering')", ["secondary criteria, explicitly called not very important"], "explicit",
     [ev("009", "when I get many options, I can start filtering it down, using other non very important criteria, such as if they have, like some amenities, or if they have, like. some extra features, or like how good looking is the place")])
cand("C009", "After filtering down to several options, contact the people offering the places, which helps narrow the options further.",
     "hedged ('I might start contacting')", ["several shortlisted options"], "explicit",
     [ev("011", "so usually, after filtering it down into several options, I'll start with the communication process, which will help me also to narrow down my options.")])
cand("C010", "Let reply speed, completeness of the information provided and the provider's attitude affect the choice among options.",
     "hedged ('might affect my choices')", ["some providers reply fast with full information, others do not"], "explicit",
     [ev("011", "So after that steps I might start contacting like the people who offer these places, and when I contact them, sometimes like how fast they will reply might affect my choices")])
cand("C011", "When a provider does not respond, look for the place name, website, URL or phone number and try other communication methods such as email or phone.",
     "usual practice ('I'll try')", ["triggered by no response on the platform"], "explicit",
     [ev("013", "So I'll try to communicate with them using other methods like email or phone.")])
cand("C012", "A missing response is taken as a bad sign that the management is not good.",
     "belief ('It's just a bad sign')", ["assessment of the provider, no separate action requested"], "explicit",
     [ev("013", "It's just a bad sign that the management is not very good, otherwise they won't just skip any type of communication.")])
cand("C013", "Use these platforms mainly to discover places and proceed with a different type of communication outside the apps.",
     "usual practice ('I mainly use ... I actually usually proceed')", ["distrust of in-app communication"], "explicit",
     [ev("017", "So I mainly use this type of platforms like as a way to discover places. But I actually usually proceed with different type of communication outside of these apps.")])
cand("C014", "See when the listing information was last updated, because it may be outdated or wrong.",
     "strong dislike of the current lack ('I hated that')", ["information may be outdated or wrong"], "explicit",
     [ev("019", "You don't know when was the time the information was lastly updated. There are no such information. It might be like outdated.")])
cand("C015", "Have a short communication path instead of a long form whose submission and outcome are unknown.",
     "stated preference ('you feel like the provider is unreachable')", ["few buttons, long form, unclear submission"], "explicit",
     [ev("019", "you will have this long form that you don't know how it will be submitted")])
cand("C016", "If another familiar way of communication exists, move to that option.",
     "usual practice ('I usually move to that option')", ["alternative channel available"], "explicit",
     [ev("019", "So if I can find another familiar way of communication, I usually move to that option.")])
cand("C017", "See a small visual timeline of the next steps and of what to expect, including what happens if the attempt fails.",
     "hedged want ('I might be more comfortable')", ["after finding a place"], "explicit",
     [ev("021", "and I can see, like a small visual of the timeline that, like the website, can show me what are the next steps. If I fail, therefore, what should I expect?")])
cand("C018", "Reach a provider without having to fill all the required personal details (first name, last name, email, mobile, move dates, beds, baths, custom message).",
     "complaint with clear preference", ["all fields are currently required"], "explicit",
     [ev("023", "and all of them are required fields, and you still don't know a lot about the one who is providing this house, so it doesn't feel very comfortable to give all this information")])
cand("C019", "Not write a custom message; just pick the available option the stakeholder likes.",
     "stated preference ('sometimes you don't want to')", ["when the user only wants to select an existing option"], "explicit",
     [ev("023", "Sometimes you don't want to write a custom message. You just want to pick the available option you like.")])
cand("C020", "Know more about the provider before sharing personal information.",
     "comfort requirement", ["little is known about the provider at form time"], "explicit",
     [ev("023", "you still don't know a lot about the one who is providing this house, so it doesn't feel very comfortable to give all this information")])
cand("C021", "Pick a specific apartment from the listed options, e-commerce 'add to cart' style, because housing options are limited and not customised.",
     "wish ('I would love', 'maybe')", ["limited set of existing apartments with given specifications"], "explicit",
     [ev("025", "they can just list it with their specification, and I can have something similar to the concept of. Add to cart")])
cand("C022", "Know what will happen next, including when the provider would respond, before proceeding with an option.",
     "wish ('I would love like to know')", ["like shipping estimates in e-commerce"], "explicit",
     [ev("025", "I would love like to know if I just proceeded with this option, what will happen when they would they respond to me? What will be next?")])
cand("C023", "Share personal information only after both parties confirm availability and interest.",
     "proposal ('I think ... could be after')", ["mutual confirmation of availability and interest"], "explicit",
     [ev("027", "I think like giving the information could be after confirming the availability from the 2 parties like if they said, this apartment is available, and I said, I'm interested."),
      ev("027", "before that step I think it's not necessary to give all the information")])
cand("C024", "The current flow is: visit a site, log in, use a search bar with filters, open details, then either fill the in-site form with unknown response time or find the provider on Google Maps to communicate directly.",
     "description of current process", ["process summary requested by the interviewer"], "explicit",
     [ev("029", "I will have 2 ways either to fill the form inside the website, and I never know when they will respond to me and how efficient is this process. or just to take their location from the map, then try to find more about them, using other websites like Google Map")])
cand("C025", "Select the search area by drawing a circle on a map, because neighborhood-name search is too specific.",
     "liked feature ('one of the things that I like')", ["a good option 2 meters away would be missed by name search"], "explicit",
     [ev("033", "One of the things that I like is that they provide sometimes a map with a drawing tool where you can just draw a circle around the place you're interested in in the map"),
      ev("033", "because sometimes searching by the neighborhood name will be very specific, like, if there is a very good option just 2 meters away, it will not be considered")])
cand("C026", "Have reviews from people available, which makes places feel more trusted and keeps the information together.",
     "liked feature ('another thing that I like')", [], "explicit",
     [ev("033", "Also, another thing that I like is providing reviews, I think reviews from people, makes. makes places feel more trusted, and could help let you have all the information together.")])
cand("C027", "Avoid mandatory registration and unknown buttons or extra steps whose outcome is unclear; prefer a site with minimal options and a list of things to do.",
     "dislike with clear avoidance ('one of the things that I don't like')", ["unknown process leads to leaving the site"], "explicit",
     [ev("033", "one of the things that I don't like is actually these extra steps like requiring you to register in the website. And then you have, like, multiple, unknown, like multiple buttons that you don't know. What would they proceed you to?"),
      ev("033", "this type of long, unknown process makes me just skip the website and look for a website with like minimal options and and list things to do.")])
cand("C028", "Be able to find the items saved through the favorites button afterwards, since there is no bookmark or saved section in the menu.",
     "expectation of a normal user ('I assume as a normal user')", ["favorites button exists but the saved place is not findable"], "explicit",
     [ev("035", "there is a button called favorites. It should like, I assume as a normal user that if I click on favorites it should save the thing I'm looking for. But actually, I can't find where where it's saving it.")])
cand("C029", "Not be required to register just to do research on the site.",
     "dislike ('throws me off')", ["registration before any search"], "explicit",
     [ev("035", "And also another thing is that when they require you to register just to do a research, so these things throws me off of the of the website.")])
cand("C030", "Compare three or four liked options on a single page with the main features side by side.",
     "wish ('I wish')", ["3 or 4 options at a time"], "explicit",
     [ev("037", "I wish, if there is an option for comparison, like, sometimes I like 3 or 4 options like, I want to collect them all in in like a single page. So I can look in the main features at the same time.")])
cand("C031", "Put the favorites entry in the nav bar or at least the first level of the menu.",
     "normative expectation ('It should be')", ["saved items must be reachable in one step"], "explicit",
     [ev("039", "It should be like on the nav bar, or at least at the menu, at the like 1st level of the menu.")])
cand("C032", "Make registration optional (for saving information and autofill) instead of required, since communicating with a provider does not need an account.",
     "proposal ('it should not be required')", ["no need for personalisation in this process"], "explicit",
     [ev("043", "Maybe he could. It could be optional thing like if you want your information saved and to be filled directly you can register. But it should not be required.")])
cand("C033", "Start searching and see the whole functionality directly, without logging in.",
     "stated preference ('Just start searching')", ["instead of logging in"], "explicit",
     [ev("045", "Just start searching and seeing the whole functionality directly.")])
cand("C034", "Search the information wanted conveniently, without steps the stakeholder does not believe are beneficial.",
     "stated primary goal ('your primary goal ... It's like')", ["purpose behind skipping login"], "explicit",
     [ev("047", "It's like to be more convenient just to search the information you want without having steps that you don't believe it's beneficial.")])
cand("C035", "Filter by price range, beds and baths, home type, and extra criteria such as move-in date, pets and utilities.",
     "positive assessment ('that's very beneficial')", ["filters offered after the location is set"], "explicit",
     [ev("049", "You can filter by price range. you can filter by the number of beds and baths you can also filter by the home type whether you want a house, an apartment."),
      ev("049", "and also you can filter by extra criteria, like the move-in date, or any other things that you want, like allowing pets, for example, having utilities, and so on.")])
cand("C036", "Keep the filters optional instead of forcing the user to fill everything, because the user may be unsure what they want.",
     "liked behaviour ('I like that')", ["uncertain requirements at search time"], "explicit",
     [ev("051", "I like that. The filters are optional. They don't enforce you to enter everything, because sometimes you're not very assured about what do you want")])
cand("C037", "Avoid missing options whose attributes the provider did not specify when filtering by such an attribute.",
     "fear / wish ('I have this fear')", ["owner may allow pets without stating it"], "explicit",
     [ev("051", "What if I filter by some criteria, and then I lost all the options where the owners didn't specify."),
      ev("051", "because sometimes I have this fear that maybe I filtered by something, and I missed options that were not entered appropriately.")])
cand("C038", "Add a checkbox such as 'include options that didn't determine' inside an attribute filter like pet policy.",
     "suggestion ('maybe if there is')", ["checkbox in the pet policy dropdown"], "explicit",
     [ev("053", "maybe if there is like a check box called include, for example, like the options that didn't determine, or something like that.")])
cand("C039", "With the checkbox ticked show both allowed and unspecified listings; without it show only listings that specify they allow.",
     "stated behaviour of the proposal", ["depends on the checkbox state"], "explicit",
     [ev("055", "The one who allowed and the one who didn't specify, and if I didn't click on the checkbox, I will have the ones who only specify that they allow.")])
cand("C040", "Get an overview of the available options, price ranges, reviews and locations, especially when moving to another country.",
     "stated benefit ('it will help me to get information')", ["information not obtainable without such websites"], "explicit",
     [ev("057", "especially when I'm moving to another country. So I want to be able to know what are the options? And what are the price ranges, and so on."),
      ev("057", "So these types of filters, and also these types of websites will collect a lot of options together will give me an overview about the price ranges about the available options, and to see the reviews, to see the locations.")])
cand("C041", "See when the listing was last updated in order to be assured that the information is accurate.",
     "strong wish ('I would really love')", ["feeling that the information may not be up to date"], "explicit",
     [ev("059", "Also, another thing that I would really love is to have to be able to see when it was last updated.")])
cand("C042", "Have website rules that enforce owners to photograph properties in a specific format (sunlight, specific angles), so that users trust the site more.",
     "tentative suggestion ('maybe ... Maybe this will')", ["photos currently vary in quality and can be misleading"], "explicit",
     [ev("059", "maybe if the website has some sort of rules that enforces people who own these properties to take the picture in a specific format, for example, on, for example, sunlight using like specific angles. Maybe this will give people more trust to use a website over another one.")])
cand("C043", "No information on the details page seems unimportant; the page seems good as it is.",
     "satisfied assessment", ["no change requested for the information set"], "explicit",
     [ev("065", "I can't see, like any information that it's not really important, like It seems good to me, or.")])
cand("C044", "The details are sufficient apart from the last-updated information.",
     "satisfied with one exception", ["exception: last updated"], "explicit",
     [ev("067", "Oh, it feels sufficient. It's only the part where I said about like when it was last updated.")])
cand("C045", "Be assured that the listing information is up to date.",
     "stated want ('I just want to be assured')", ["details page otherwise sufficient"], "explicit",
     [ev("069", "It just. I just want to be assured that it's it's up to date.")])
cand("C046", "Have all housing communication with property owners through the website as a single platform, if the process is clear and fast.",
     "strong preference ('It will be so good')", ["conditional on a clear and fast process"], "explicit",
     [ev("071", "it will be very sufficient to communicate with the property owners through these websites. If the process was clear and fast. It will be so good like to have all the communication through a single platform.")])
cand("C047", "Make the send-message process clear instead of a vague button that leads to a form with an unknown outcome.",
     "complaint with clear preference", ["reason the stakeholder does not communicate on the site"], "explicit",
     [ev("071", "You just have a vague button called. Send a message where you will fill a form and never know what will happen next.")])
cand("C048", "Give the user insight into how the communication process will go, so that the user trusts the feature and keeps the communication on the website.",
     "proposal ('maybe it's changing something in the ui')", ["trust leads to staying on the site"], "explicit",
     [ev("073", "So maybe it's changing something in in the ui to make the user have some insight about, how would the communication process be? This will make him like, trust the feature more, and never try something else, and just keep the communication in in the website.")])
cand("C049", "Decide on a home within a week or at most a month.",
     "contextual constraint ('sometimes you want to decide')", ["time pressure on the whole search"], "explicit",
     [ev("073", "I think, like finding a home. It's it's not a long process, like, sometimes you want to decide within a week or maximum a month.")])

assert len(raw) == 49, len(raw)

goals = []


def goal(gid, statement, context, origin, evidence, label, rationale, unsupported=None, assumptions=None, steps=None):
    goals.append({"candidate_id": gid, "statement": statement, "actor": "Stakeholder",
                  "context": context, "origin": origin, "inference": None,
                  "evidence": evidence,
                  "judgment": {"label": label, "rationale": rationale, "supported_parts": [],
                               "unsupported_parts": unsupported or [], "assumptions": assumptions or [],
                               "reasoning_steps": steps or []}})


goal("G001", "Find a new place to live when moving to a new neighborhood or a new country.",
     ["Trigger: relocation to a new neighbourhood or another country"], "explicit",
     [ev("003", "Mainly when I move to a new neighborhood or to a new country, I need to find a new place.")],
     "direct", "原句直述搬迁时需要找到新住处，主体、触发情境与结果一致，无附加条件被删改。")
goal("G002", "Choose the neighborhood or area to search in before starting the keyword search for that area.",
     ["The keyword search then targets the chosen area"], "explicit",
     [ev("005", "So usually I choose a neighborhood or a place where I want to find a house in, and then I start searching by such keywords to find relevant websites for that specific area")],
     "direct", "原句以“usually”描述先定区域再按关键词搜索的顺序，目标保留顺序与通常强度。")
goal("G003", "Identify which rental websites are the most popular or most used in the target area, especially when it is another country.",
     ["The area may be in another country"], "explicit",
     [ev("005", "So I want to be familiar with which websites are the most popular or most used there.")],
     "direct", "“I want to be familiar with which websites are the most popular or most used there”直接支持该目标，范围限定在该地区。")
goal("G004", "Pick a neighborhood close to a fixed destination such as a job or a college.",
     ["Only when a job or a college anchors the location"], "explicit",
     [ev("007", "if I have a specific job, or if I'm studying at specific college, I will usually pick a neighborhood that's close to that area")],
     "direct", "条件句明确给出“有固定上班或上学地点时选附近街区”，条件保留在 context。")
goal("G005", "Ask people who live in the target country for recommendations about places.",
     ["One of several ways to choose a neighbourhood, not the only method"], "explicit",
     [ev("007", "is asking people who lives, for example in that country, if they have any recommendation for the places")],
     "direct", "原文把它列为多种选街区方式之一，目标保留该动作，未提升为唯一方式。")
goal("G006", "Spot the neighborhoods where listings that fit the budget and requirements are clustered.",
     ["Based on sites showing available houses and apartments"], "explicit",
     [ev("007", "Sometimes there are options that fits my budget and fits my requirements more clustered in specific neighborhoods")],
     "direct", "原句说明预算与要求相符的房源集中在特定街区，据此选街区，支撑该目标。")
goal("G007", "Search listings by primary criteria: price range, size or bedroom and bathroom counts, and home type.",
     ["Size or bedroom count is paired with a budget limit",
      "Home type distinguishes a house from an apartment"], "explicit",
     [ev("009", "So actually, I will search by like the size of the place, or sometimes by bedroom counts. and with also a budget limit."),
      ev("049", "You can filter by price range. you can filter by the number of beds and baths you can also filter by the home type whether you want a house, an apartment.")],
     "direct", "两轮原句分别给出主筛选维度（面积/卧室数+预算）与价格、卫浴数、房型，均为同一“按主要属性筛选”动作的限定。")
goal("G008", "Narrow the results down with secondary criteria such as amenities, utilities, pet policy, move-in date and how good the place looks.",
     ["Applied after the primary search returns many options",
      "These criteria are described as less important than size and price"], "explicit",
     [ev("009", "when I get many options, I can start filtering it down, using other non very important criteria, such as if they have, like some amenities, or if they have, like. some extra features, or like how good looking is the place"),
      ev("049", "and also you can filter by extra criteria, like the move-in date, or any other things that you want, like allowing pets, for example, having utilities, and so on.")],
     "direct", "原文明确这是首轮筛选后的次级筛选，目标保留“非很重要”的强度与具体维度。")
goal("G009", "Contact the people offering the shortlisted places to narrow the options down, letting reply speed, completeness of information and provider attitude affect the choice.",
     ["After filtering down to several options",
      "A provider attitude that raises suspicion counts against the option"], "explicit",
     [ev("011", "so usually, after filtering it down into several options, I'll start with the communication process, which will help me also to narrow down my options."),
      ev("011", "So after that steps I might start contacting like the people who offer these places, and when I contact them, sometimes like how fast they will reply might affect my choices")],
     "direct", "原句说明筛选后进入沟通以进一步缩小范围，并列出回复速度等因素影响取舍；同一动作的两项限定合并保留。")
goal("G010", "Get an overview of the available options and price ranges, including reviews and locations, when looking in a new market.",
     ["Especially when moving to another country",
      "Information the stakeholder could not obtain without such websites"], "explicit",
     [ev("057", "especially when I'm moving to another country. So I want to be able to know what are the options? And what are the price ranges, and so on."),
      ev("057", "So these types of filters, and also these types of websites will collect a lot of options together will give me an overview about the price ranges about the available options, and to see the reviews, to see the locations.")],
     "direct", "原句说明网站聚合房源带来价格区间、选项、评论与位置的总体认识，主体与范围一致。")
goal("G011", "Reach a provider through their own website, email or phone found via the place name and Google Maps when the in-app contact gets no response.",
     ["Triggered when the provider does not answer through the platform"], "explicit",
     [ev("013", "So I'll try to communicate with them using other methods like email or phone."),
      ev("019", "So if I can find another familiar way of communication, I usually move to that option.")],
     "direct", "原句给出无回应时改用邮箱、电话等其它渠道的做法，触发条件与手段均保留。")
goal("G012", "Use listing platforms mainly to discover places and carry the communication on outside the apps.",
     ["Current practice, described as usual"], "explicit",
     [ev("017", "So I mainly use this type of platforms like as a way to discover places. But I actually usually proceed with different type of communication outside of these apps.")],
     "direct", "原句直述当前主要用途是发现房源、沟通放在站外，目标保留“mainly/usually”的现状强度。")
goal("G013", "See when a listing's information was last updated so that I can be assured it is current.",
     ["Because the information may be outdated or wrong"], "explicit",
     [ev("019", "You don't know when was the time the information was lastly updated. There are no such information. It might be like outdated."),
      ev("059", "Also, another thing that I would really love is to have to be able to see when it was last updated."),
      ev("069", "It just. I just want to be assured that it's it's up to date.")],
     "direct", "多次陈述缺少更新时间导致不信任，并在结尾再次强调“只想确认信息是最新的”，支持该单一目标。")
goal("G014", "See a timeline of the next steps and of what to expect after an inquiry, including what happens if it fails.",
     ["Would make the stakeholder more comfortable and more willing to engage"], "explicit",
     [ev("021", "and I can see, like a small visual of the timeline that, like the website, can show me what are the next steps. If I fail, therefore, what should I expect?"),
      ev("025", "I would love like to know if I just proceeded with this option, what will happen when they would they respond to me? What will be next?"),
      ev("073", "So maybe it's changing something in in the ui to make the user have some insight about, how would the communication process be? This will make him like, trust the feature more, and never try something else, and just keep the communication in in the website.")],
     "direct", "三处均要求看到后续步骤与预期，包含失败时的预期；合并为同一“流程可见性”目标。")
goal("G015", "Contact a provider with a short message instead of a long mandatory form and without handing over all personal details up front.",
     ["The current form requires first name, last name, email, mobile, move dates, beds, baths and a custom message"], "explicit",
     [ev("019", "you will have this long form that you don't know how it will be submitted"),
      ev("023", "and all of them are required fields, and you still don't know a lot about the one who is providing this house, so it doesn't feel very comfortable to give all this information"),
      ev("071", "You just have a vague button called. Send a message where you will fill a form and never know what will happen next.")],
     "direct", "原句反复把“长表单+必填个人信息+提交不明”作为联系障碍，目标以短消息联系为核心动作，未删去表单负担这一条件。")
goal("G016", "Share personal details only after both sides confirm availability and interest.",
     ["Before that confirmation the information is not considered necessary"], "explicit",
     [ev("027", "I think like giving the information could be after confirming the availability from the 2 parties like if they said, this apartment is available, and I said, I'm interested."),
      ev("027", "before that step I think it's not necessary to give all the information")],
     "direct", "原句明确给出“双方确认后再提供信息”的时序与理由，目标保留条件性。")
goal("G017", "Pick a specific available unit from the listed options instead of writing a custom message.",
     ["Housing options are limited and not customised, unlike made-to-order goods"], "explicit",
     [ev("023", "Sometimes you don't want to write a custom message. You just want to pick the available option you like."),
      ev("025", "they can just list it with their specification, and I can have something similar to the concept of. Add to cart")],
     "direct", "原句要求“挑选已有选项”替代“写自定义消息”，并以加购物车作类比，目标保留替代关系。")
goal("G018", "Search and use the full functionality without being required to register or log in, keeping registration optional for saving information.",
     ["Registration is acceptable only as an option to save details and autofill"], "explicit",
     [ev("043", "Maybe he could. It could be optional thing like if you want your information saved and to be filled directly you can register. But it should not be required."),
      ev("045", "Just start searching and seeing the whole functionality directly.")],
     "direct", "原句明确“注册可自愿但不应强制”，目标保留“可选”这一例外而非全面禁止注册。")
goal("G019", "Search the information I want conveniently, without steps I do not consider beneficial.",
     ["Stated as the primary goal behind skipping login"], "explicit",
     [ev("047", "It's like to be more convenient just to search the information you want without having steps that you don't believe it's beneficial.")],
     "direct", "受访者自述这是跳过登录背后的首要目标，原句即支持便利与去除无益步骤两点。")
goal("G020", "Keep the interface to few, clearly understood actions and avoid unknown buttons or extra steps.",
     ["Unknown extra steps make the stakeholder leave the site"], "explicit",
     [ev("033", "one of the things that I don't like is actually these extra steps like requiring you to register in the website. And then you have, like, multiple, unknown, like multiple buttons that you don't know. What would they proceed you to?"),
      ev("033", "this type of long, unknown process makes me just skip the website and look for a website with like minimal options and and list things to do.")],
     "direct", "原句以“不喜欢未知按钮与多余步骤、转而找选项最少的网站”表达明确避免意图。")
goal("G021", "Select the search area by drawing a circle on a map instead of relying only on neighborhood names.",
     ["Neighborhood-name search is too specific and misses nearby options"], "explicit",
     [ev("033", "One of the things that I like is that they provide sometimes a map with a drawing tool where you can just draw a circle around the place you're interested in in the map"),
      ev("033", "because sometimes searching by the neighborhood name will be very specific, like, if there is a very good option just 2 meters away, it will not be considered")],
     "direct", "原句把画圈选区域列为喜欢的功能并给出理由，目标保留“而非只按街区名”的对比含义。")
goal("G022", "Read reviews from people about a place so that it feels more trusted and the information sits together.",
     [], "explicit",
     [ev("033", "Also, another thing that I like is providing reviews, I think reviews from people, makes. makes places feel more trusted, and could help let you have all the information together.")],
     "direct", "原句直接说明喜欢评论及其带来的信任与信息集中效果。")
goal("G023", "Compare three or four liked options on a single page with their main features side by side.",
     ["The stakeholder has not found a website that offers this"], "explicit",
     [ev("037", "I wish, if there is an option for comparison, like, sometimes I like 3 or 4 options like, I want to collect them all in in like a single page. So I can look in the main features at the same time."),
      ev("071", "I just want to mention it again about comparing between several options like, I wish, if there is such feature that helps me to compare")],
     "direct", "两处（含结尾重申）均要求把若干备选放一页对比主要特征，数量 3-4 与单页方式保留。")
goal("G024", "Save interesting options to a favorites list that can be found from the nav bar or the first level of the menu.",
     ["Currently the saved items cannot be located after saving"], "explicit",
     [ev("035", "there is a button called favorites. It should like, I assume as a normal user that if I click on favorites it should save the thing I'm looking for. But actually, I can't find where where it's saving it."),
      ev("039", "It should be like on the nav bar, or at least at the menu, at the like 1st level of the menu.")],
     "direct", "原句要求收藏能保存并可找到，且给出应位于导航栏或菜单一级的位置要求。")
goal("G025", "Avoid losing suitable options whose attributes the provider left unspecified when filtering.",
     ["Example: an owner may allow pets without stating it in the profile"], "explicit",
     [ev("051", "What if I filter by some criteria, and then I lost all the options where the owners didn't specify."),
      ev("051", "because sometimes I have this fear that maybe I filtered by something, and I missed options that were not entered appropriately.")],
     "direct", "原句明确表达筛选可能漏掉未填写属性房源的担心与避免意图。")
goal("G026", "Keep the filters optional rather than forcing the user to fill every field.",
     ["Sometimes the stakeholder is not sure what he wants"], "explicit",
     [ev("051", "I like that. The filters are optional. They don't enforce you to enter everything, because sometimes you're not very assured about what do you want")],
     "direct", "这是对现有“筛选非必填”的肯定，属维持型意图，原文明确表达喜欢。")
goal("G027", "Include listings that did not specify a criterion when the user asks for it, for example through a checkbox, so that both confirmed and unspecified options are shown.",
     ["Without the checkbox only listings that confirm the criterion are shown"], "explicit",
     [ev("053", "maybe if there is like a check box called include, for example, like the options that didn't determine, or something like that."),
      ev("055", "The one who allowed and the one who didn't specify, and if I didn't click on the checkbox, I will have the ones who only specify that they allow.")],
     "direct", "原句提出勾选框及勾选前后的两种结果，目标保留“按需包含未指定”的条件与方式。")
goal("G028", "Have the website enforce a standard photo format (light and angles) for listings so that the photos are more trustworthy.",
     ["Proposed tentatively ('maybe'); expected effect is more trust in the site"], "explicit",
     [ev("059", "maybe if the website has some sort of rules that enforces people who own these properties to take the picture in a specific format, for example, on, for example, sunlight using like specific angles. Maybe this will give people more trust to use a website over another one.")],
     "direct", "原句以“maybe”提出网站规则约束拍照格式，目标保留这一建议强度并写入 context，未升格为硬性要求。")
goal("G029", "Keep all housing communication with property owners inside the website, provided the process is clear and fast.",
     ["Condition: the communication process is clear and fast",
      "The stakeholder wants to decide within a week or at most a month"], "explicit",
     [ev("071", "it will be very sufficient to communicate with the property owners through these websites. If the process was clear and fast. It will be so good like to have all the communication through a single platform."),
      ev("073", "This will make him like, trust the feature more, and never try something else, and just keep the communication in in the website.")],
     "direct", "原句把“全部沟通放在站内”与“流程清晰且快”的条件绑定，目标保留该条件句。")

gmap = {g["candidate_id"]: g for g in goals}

relations = [
    {"relation_id": "R1", "source_id": "G021", "target_id": "G002", "type": "operationalization", "status": "supported",
     "conditions": ["a map with a drawing tool is available"], "assumptions": ["在地图上画圈仍属于选择搜索区域的实现方式"],
     "rationale": "画圈选区域是受访者选街区/区域这一目的的具体实现方式，原句同时给出“街区名太具体”的理由，方向为方式→目的。",
     "evidence_ids": [],
     "evidence_quotes": [{"source_id": T + "033", "quote": "One of the things that I like is that they provide sometimes a map with a drawing tool where you can just draw a circle around the place you're interested in in the map", "role": "basis"}]},
    {"relation_id": "R2", "source_id": "G004", "target_id": "G002", "type": "specialization", "status": "supported",
     "conditions": ["the stakeholder has a job or a college that fixes the location"], "assumptions": ["就近上班/上学是选街区的一般目标的一个具体情境"],
     "rationale": "“有固定上班或上学地点时选附近街区”是选街区目标在特定情境下的具体化，方向为具体→一般。",
     "evidence_ids": [],
     "evidence_quotes": [{"source_id": T + "007", "quote": "if I have a specific job, or if I'm studying at specific college, I will usually pick a neighborhood that's close to that area", "role": "basis"}]},
    {"relation_id": "R3", "source_id": "G006", "target_id": "G002", "type": "operationalization", "status": "supported",
     "conditions": ["listing sites show where budget-fitting options cluster"], "assumptions": ["以房源聚集街区反推目标街区是可行性判断的方法"],
     "rationale": "观察预算相符房源的聚集街区，是决定选哪个街区的具体方法，属方式→目的。",
     "evidence_ids": [],
     "evidence_quotes": [{"source_id": T + "007", "quote": "Sometimes there are options that fits my budget and fits my requirements more clustered in specific neighborhoods", "role": "basis"}]},
    {"relation_id": "R4", "source_id": "G005", "target_id": "G002", "type": "operationalization", "status": "supported",
     "conditions": ["people living in the target country can be asked"], "assumptions": ["向当地人打听是获取街区信息的渠道之一"],
     "rationale": "原句把“问当地人推荐”列为选街区的一种方式，属实现方式→目的；未声称它是唯一或充分方式。",
     "evidence_ids": [],
     "evidence_quotes": [{"source_id": T + "007", "quote": "is asking people who lives, for example in that country, if they have any recommendation for the places", "role": "basis"}]},
    {"relation_id": "R5", "source_id": "G018", "target_id": "G019", "type": "operationalization", "status": "supported",
     "conditions": [], "assumptions": ["强制登录被受访者归入“无益步骤”"],
     "rationale": "受访者把“跳过登录”直接解释为“更方便地搜索、去掉无益步骤”，即免登录服务于便利搜索这一目的。",
     "evidence_ids": [],
     "evidence_quotes": [{"source_id": T + "047", "quote": "It's like to be more convenient just to search the information you want without having steps that you don't believe it's beneficial.", "role": "basis"}]},
    {"relation_id": "R6", "source_id": "G014", "target_id": "G029", "type": "contribution", "status": "supported",
     "conditions": ["the user can see the process before deciding"], "assumptions": ["对流程的可见性会提高站内沟通的信任"],
     "rationale": "原句说明让用户了解沟通过程会使其更信任该功能并留在站内沟通，属于帮助关系而非充分条件。",
     "evidence_ids": [],
     "evidence_quotes": [{"source_id": T + "073", "quote": "So maybe it's changing something in in the ui to make the user have some insight about, how would the communication process be? This will make him like, trust the feature more, and never try something else, and just keep the communication in in the website.", "role": "basis"}]},
    {"relation_id": "R7", "source_id": "G015", "target_id": "G029", "type": "contribution", "status": "supported",
     "conditions": ["contacting does not require the long form"], "assumptions": ["表单与不明结果是把沟通推到站外的原因之一"],
     "rationale": "原句把“模糊按钮+表单+不知后续”列为不在站内沟通的原因，缩短联系路径因此有助于把沟通留在站内。",
     "evidence_ids": [],
     "evidence_quotes": [{"source_id": T + "071", "quote": "You just have a vague button called. Send a message where you will fill a form and never know what will happen next.", "role": "basis"}]},
    {"relation_id": "R8", "source_id": "G011", "target_id": "G009", "type": "contribution", "status": "supported",
     "conditions": ["the provider is reachable outside the platform"], "assumptions": ["换渠道联系仍服务于缩小备选范围"],
     "rationale": "站外渠道是在平台无回应时继续联系房源方的补救，帮助“联系房源方以缩小范围”这一目标推进，但不保证成功。",
     "evidence_ids": [],
     "evidence_quotes": [{"source_id": T + "013", "quote": "So I'll try to communicate with them using other methods like email or phone.", "role": "basis"}]},
    {"relation_id": "R9", "source_id": "G007", "target_id": "G010", "type": "contribution", "status": "supported",
     "conditions": ["listings are aggregated on the site"], "assumptions": ["筛选与聚合共同带来价格区间的总体认识"],
     "rationale": "原句说明筛选与网站聚合房源一起帮助形成价格区间与可选项总览，属有帮助但不等于充分。",
     "evidence_ids": [],
     "evidence_quotes": [{"source_id": T + "057", "quote": "So these types of filters, and also these types of websites will collect a lot of options together will give me an overview about the price ranges about the available options", "role": "basis"}]},
    {"relation_id": "R10", "source_id": "G022", "target_id": "G010", "type": "contribution", "status": "supported",
     "conditions": [], "assumptions": ["评论被视为总览的一部分信息"],
     "rationale": "原句把“看评论、看位置”列为网站给出的总体信息的一部分，评论有助于形成市场总览。",
     "evidence_ids": [],
     "evidence_quotes": [{"source_id": T + "057", "quote": "and to see the reviews, to see the locations", "role": "basis"}]},
    {"relation_id": "R11", "source_id": "G027", "target_id": "G025", "type": "operationalization", "status": "supported",
     "conditions": ["the filter field supports an include-unspecified option"], "assumptions": ["勾选框能按用户选择决定是否纳入未填写项"],
     "rationale": "勾选“包含未注明”的控件是避免漏掉未填写属性房源这一目的的具体做法，方向为方式→目的。",
     "evidence_ids": [],
     "evidence_quotes": [{"source_id": T + "051", "quote": "maybe I would love if there is an option where I can have like. I can also allow the people who didn't specify, so I can see both", "role": "basis"}]},
    {"relation_id": "R12", "source_id": "G008", "target_id": "G009", "type": "precedes", "status": "supported",
     "conditions": [], "assumptions": ["“after that steps”指筛选完成之后才联系"],
     "rationale": "原句明确说明先完成筛选再开始联系，属先后关系；未据此声称因果或精化。",
     "evidence_ids": [],
     "evidence_quotes": [{"source_id": T + "011", "quote": "So after that steps I might start contacting like the people who offer these places", "role": "basis"}]},
    {"relation_id": "R13", "source_id": "G017", "target_id": "G015", "type": "contribution", "status": "supported",
     "conditions": [], "assumptions": ["挑选已有选项可省去写自定义消息"],
     "rationale": "原句说明不想写自定义消息时希望直接挑选已有选项，挑选因此有助于实现“短联系、不长表单”的目标。",
     "evidence_ids": [],
     "evidence_quotes": [{"source_id": T + "023", "quote": "Sometimes you don't want to write a custom message. You just want to pick the available option you like.", "role": "basis"}]},
]

groups = [
    {"group_id": "GR1", "parent_id": "G029", "child_ids": ["G014", "G015"], "kind": "and",
     "status": "proposed", "completeness": "partial",
     "rationale": "原文把“流程不清”和“表单冗长、结果不明”同时列为不在站内沟通的原因，短联系加流程可见性共同覆盖了其中一部分；但未覆盖响应时限、房主不回应等情形，不能声称整组已足以实现父目标。",
     "assumptions": ["若站内流程透明且联系成本低，用户会放弃站外电话/邮件", "房主仍会通过站内渠道回应"],
     "evidence_ids": [],
     "evidence_quotes": [{"source_id": T + "071", "quote": "But the reason why I'm not having this experience until now is that the process is not clear.", "role": "basis"}],
     "relation_ids": ["R6", "R7"],
     "checks": [
         {"kind": "normal", "origin": "analysis_assumption",
          "scenario": "用户对某套房源产生兴趣：用短消息即可发出询问，并能在页面上看到下一步与预期回复时间。",
          "outcome": "supports",
          "rationale": "按原句（T071、T073）构造的正常场景，两个子目标各自覆盖“联系简单”与“流程可见”，场景内未出现反例。"},
         {"kind": "exception", "origin": "analysis_assumption",
          "scenario": "房主长期不回应或平台无人维护，即使界面清晰、表单很短。",
          "outcome": "counterexample",
          "rationale": "受访者自己说在无回应时会转用电话或邮件，说明两个子目标不能保证沟通留在站内，故整组只记为 proposed/partial。"}]}
]

questions_dec = [
    {"target_type": "model", "target_id": "DOC021-goal-model",
     "message": "G012 描述的是当前主要在站外沟通，而 G029 期望把沟通留在站内：应理解为“流程清晰后才回到站内”的条件性偏好，还是两条并行渠道？"},
    {"target_type": "group", "target_id": "GR1",
     "message": "GR1 只覆盖流程可见与短联系，未覆盖响应时限与房主不回应；是否需要另一个“响应时限/可达性”目标才能共同充分？"},
    {"target_type": "goal", "target_id": "G012",
     "message": "G012 是现状做法（站外沟通），与 G029 方向相反；它应作为需要保留的现状，还是视为待改变的行为？"},
    {"target_type": "goal", "target_id": "G028",
     "message": "照片格式强制只以“maybe”提出，是否保留为目标而非仅列为偏好？"},
]

spec = {
    "document_id": "DOC021",
    "raw_candidates": raw,
    "goals": goals,
    "review_questions": [
        {"candidate_ids": ["G001"], "question": "“搬迁时找到新住处”是流程的触发情境，作为独立目标是否过泛？", "reason": "它更像整段流程的目的背景，可能不承载独立验收维度。"},
        {"candidate_ids": ["G028"], "question": "以“maybe”提出的照片格式规则，是否应保持为暂定建议而不作为承诺？", "reason": "语气为试探性建议，采纳与否未知。"},
    ],
    "limitations": [
        "转写稿含口语重复、断句与自我更正，引文按原文逐字复制，未做语言润色。",
        "仅依据本任务分配的原文判断，未联网检索，也未参考其他资料或历史结果。",
        "个别窗口（如 W0031–W0034 的细节页问答）以确认现状为主，未产生新目标。",
        "支持标签为生成方判断，未执行独立语义评审与形式证明。",
    ],
    "ledger": {
        "model": "deepseek-v4.1-flash", "temperature": "unknown",
        "budget": "1 initial pass + <=2 repair rounds", "usage": "unknown",
        "skill_revision": "a5952d426b1624a3fcb2ce2829e1ae1ceb15e19dc3309d9571f3bc6b465deb6f",
        "prompt_revision": "task-prompt-v1", "planned_passes": 1,
        "stop_reason": "完成一次全篇逐窗捕获与全篇校正，覆盖 38 个窗口；未再追加补查轮次。",
        "passes": [{"pass_id": "P1", "kind": "initial", "context": "isolated", "status": "completed",
                    "window_results": [{"window_id": "DOC021:W%04d" % i, "status": "processed", "reason": ""} for i in range(1, 39)]}],
        "full_context_review": {"status": "completed",
                                "reason": "回看全部 77 轮：核对指代（“this type of apps/websites”“the process”）、问答范围、条件继承（搬迁、海外、有固定上班地点）、让步（filters 可选、注册可自愿）、例外（勾选后才含未注明项）与相反证据（现状在站外沟通 vs 期望站内沟通）。"},
        "entries": [],
        "source_checks": [],
    },
    "decisions": {"relations": relations, "groups": groups, "questions": questions_dec, "reassessments": []},
}

entries = [
    ("C001", "keep", ["G001"], "搬迁情境下找新住处的明确需求，直接成目标。"),
    ("C002", "keep", ["G002"], "先定区域再按关键词搜索的通常做法，独立成目标。"),
    ("C003", "keep", ["G003"], "明确想了解当地最常用的网站，与选区域不同，单列。"),
    ("C004", "keep", ["G006"], "用房源聚集判断街区，保留为独立目标。"),
    ("C005", "keep", ["G005"], "问当地人推荐，是原文列出的独立做法。"),
    ("C006", "keep", ["G004"], "就近上班/上学选街区，条件已保留在 context。"),
    ("C007", "keep", ["G007"], "面积/卧室数加预算的主筛选，成目标。"),
    ("C008", "keep", ["G008"], "主筛选后的次级筛选，与 G007 分属不同阶段。"),
    ("C009", "keep", ["G009"], "筛选后联系房源方以缩小范围，含“might”的强度。"),
    ("C010", "merge", ["G009"], "回复速度、信息完整度与态度是同一联系取舍动作的限定，合并入 G009。"),
    ("C011", "keep", ["G011"], "无回应时改用其它渠道，独立成目标。"),
    ("C012", "exclude", [], "对管理方的评价性信念，无独立期望动作；其作用体现在 G011 的触发理由中。"),
    ("C013", "keep", ["G012"], "站点只用于发现、沟通在站外的现状，作为现状目标保留。"),
    ("C014", "keep", ["G013"], "看不到更新时间的抱怨，明确指向更新可见性。"),
    ("C015", "keep", ["G015"], "反对长表单与不明提交，构成短联系目标的核心。"),
    ("C016", "merge", ["G011"], "“转到其它熟悉渠道”与 C011 同义，合并。"),
    ("C017", "keep", ["G014"], "要求看到后续步骤与失败预期，独立成目标。"),
    ("C018", "merge", ["G015"], "必填个人信息造成负担，属同一“短联系、少填表”目标。"),
    ("C019", "keep", ["G017"], "不想写自定义消息、只想挑选项，独立成目标。"),
    ("C020", "merge", ["G016"], "“先了解房源方再给信息”与 C023 的确认后再提供同指信息时序，合并。"),
    ("C021", "merge", ["G017"], "加购物车式挑房，与 C019 同一核心动作，合并。"),
    ("C022", "merge", ["G014"], "“接下来会怎样、何时回复”与 C017 的流程可见性同义。"),
    ("C023", "keep", ["G016"], "双方确认后再提供信息，含明确条件与时序。"),
    ("C024", "exclude", [], "面试官要求复述的现有流程，属过程描述；各环节已由 G007/G011/G015 承接，不另立目标。"),
    ("C025", "keep", ["G021"], "地图画圈选区域，含理由，独立成目标。"),
    ("C026", "keep", ["G022"], "评论带来的信任，独立成目标。"),
    ("C027", "split", ["G018", "G020"], "同一句既反对强制注册，也反对未知按钮与多余步骤：前者指向免登录（G018），后者指向界面动作清晰（G020）。"),
    ("C028", "keep", ["G024"], "收藏后找不到，指向可保存且可找到。"),
    ("C029", "merge", ["G018"], "仅为研究就要求注册，与免强制注册同义。"),
    ("C030", "keep", ["G023"], "3-4 个选项单页对比，独立成目标。"),
    ("C031", "merge", ["G024"], "收藏入口应在一级菜单，是同一收藏目标的位置限定。"),
    ("C032", "merge", ["G018"], "注册可自愿、不应强制，与 C029/C033 同义。"),
    ("C033", "merge", ["G018"], "“直接开始搜索并看到全部功能”即免登录使用的具体表述。"),
    ("C034", "keep", ["G019"], "受访者自述的首要目标，独立成目标。"),
    ("C035", "split", ["G007", "G008"], "同一段列出主筛选（价格、床卫数、房型）与附加条件（入住日期、宠物、水电），按筛选阶段分属两个目标。"),
    ("C036", "keep", ["G026"], "肯定筛选非必填，属维持型目标。"),
    ("C037", "keep", ["G025"], "担心漏掉未填写属性的房源，独立成目标。"),
    ("C038", "keep", ["G027"], "提出勾选框包含未注明项。"),
    ("C039", "merge", ["G027"], "勾选前后的两种结果，是同一勾选框目标的限定。"),
    ("C040", "keep", ["G010"], "网站聚合带来的价格区间与选项总览，独立成目标。"),
    ("C041", "merge", ["G013"], "“很想看到更新时间”与 C014 同义，合并。"),
    ("C042", "keep", ["G028"], "照片格式规则，含“maybe”的试探强度，单列。"),
    ("C043", "exclude", [], "对细节页“没有不重要信息”的满意评价，无改变意图，不构成目标。"),
    ("C044", "merge", ["G013"], "细节页够用、只差更新时间，作为更新目标的补充证据。"),
    ("C045", "merge", ["G013"], "只求确认信息最新，与 C014/C041 同义。"),
    ("C046", "keep", ["G029"], "希望全部沟通留在站内，附带“流程清晰且快”的条件。"),
    ("C047", "merge", ["G015"], "反对模糊按钮与不明结果，属同一短联系目标。"),
    ("C048", "merge", ["G014"], "让用户看到沟通流程，与 C017/C022 同指流程可见性。"),
    ("C049", "exclude", [], "一周到一月的决策时限是流程约束，作为 G029/G014 的 context 保留，不单独成目标。"),
]
spec["ledger"]["entries"] = [{"candidate_id": c, "disposition": d, "final_goal_ids": g, "reason": r} for c, d, g, r in entries]

checks = [
    ("S1", [("003", "Mainly when I move to a new neighborhood or to a new country, I need to find a new place.")],
     ["C001"], ["G001"], "represented", "搬迁触发找房的原句已由 G001 承接。"),
    ("S2", [("005", "So usually I choose a neighborhood or a place where I want to find a house in, and then I start searching by such keywords to find relevant websites for that specific area")],
     ["C002"], ["G002"], "represented", "先定区域再搜索的顺序完整保留。"),
    ("S3", [("009", "when I get many options, I can start filtering it down, using other non very important criteria, such as if they have, like some amenities, or if they have, like. some extra features, or like how good looking is the place"),
            ("049", "You can filter by price range. you can filter by the number of beds and baths you can also filter by the home type whether you want a house, an apartment.")],
     ["C007", "C008", "C035"], ["G007", "G008"], "represented", "主筛选与次级筛选两组原句分别落到 G007、G008。"),
    ("S4", [("019", "You don't know when was the time the information was lastly updated. There are no such information. It might be like outdated.")],
     ["C014", "C041", "C044", "C045"], ["G013"], "represented", "更新时间缺失与不信任在 G013 合并，四个候选同一目标。"),
    ("S5", [("023", "and all of them are required fields, and you still don't know a lot about the one who is providing this house, so it doesn't feel very comfortable to give all this information")],
     ["C018", "C020", "C023"], ["G015", "G016"], "represented", "必填信息负担归入 G015，确认后才提供归入 G016，条件未混用。"),
    ("S6", [("033", "one of the things that I don't like is actually these extra steps like requiring you to register in the website. And then you have, like, multiple, unknown, like multiple buttons that you don't know. What would they proceed you to?")],
     ["C027"], ["G018", "G020"], "represented", "同一句中的强制注册与未知按钮分别拆到 G018、G020。"),
    ("S7", [("035", "there is a button called favorites. It should like, I assume as a normal user that if I click on favorites it should save the thing I'm looking for. But actually, I can't find where where it's saving it."),
            ("039", "It should be like on the nav bar, or at least at the menu, at the like 1st level of the menu.")],
     ["C028", "C031"], ["G024"], "represented", "收藏保存与入口位置合并为 G024。"),
    ("S8", [("051", "What if I filter by some criteria, and then I lost all the options where the owners didn't specify."),
            ("053", "maybe if there is like a check box called include, for example, like the options that didn't determine, or something like that.")],
     ["C037", "C038", "C039"], ["G025", "G027"], "represented", "“担心漏掉”与“勾选框”分别落到 G025、G027，目的与方式分开。"),
    ("S9", [("071", "it will be very sufficient to communicate with the property owners through these websites. If the process was clear and fast. It will be so good like to have all the communication through a single platform."),
            ("073", "So maybe it's changing something in in the ui to make the user have some insight about, how would the communication process be? This will make him like, trust the feature more, and never try something else, and just keep the communication in in the website.")],
     ["C046", "C048"], ["G029", "G014"], "represented", "站内沟通与流程可见性分别成目标，条件“清晰且快”随 G029 保留。"),
    ("S10", [("013", "It's just a bad sign that the management is not very good, otherwise they won't just skip any type of communication.")],
     ["C012"], [], "excluded", "对管理方的评价属信念，不单独立目标；触发替代渠道的作用已在 G011 记录。"),
    ("S11", [("029", "I will have 2 ways either to fill the form inside the website, and I never know when they will respond to me and how efficient is this process. or just to take their location from the map, then try to find more about them, using other websites like Google Map")],
     ["C024"], [], "excluded", "面试官要求复述的现有流程，仅作背景；其成分已分别由 G007/G011/G015 承接。"),
    ("S12", [("065", "I can't see, like any information that it's not really important, like It seems good to me, or.")],
     ["C043"], [], "excluded", "满意度评价无改变意图，不构成目标。"),
    ("S13", [("073", "I think, like finding a home. It's it's not a long process, like, sometimes you want to decide within a week or maximum a month.")],
     ["C049"], [], "excluded", "一周到一月是决策时限，作为 G029/G014 的 context 保留，不单列目标。"),
]
spec["ledger"]["source_checks"] = [
    {"check_id": cid, "evidence_candidates": [ev(s, q) for s, q in evs],
     "candidate_ids": cids, "final_goal_ids": gids, "outcome": outcome, "reason": reason}
    for cid, evs, cids, gids, outcome, reason in checks]

with open("spec.json", "w", encoding="utf-8") as f:
    json.dump(spec, f, ensure_ascii=False, indent=2)
    f.write("\n")
print("ok", len(raw), len(goals), len(relations), len(groups))
