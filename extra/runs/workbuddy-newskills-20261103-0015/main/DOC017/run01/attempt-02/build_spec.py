# -*- coding: utf-8 -*-
"""Local builder for spec.json. Verifies every quote is an exact substring of its turn text."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
doc = json.loads((HERE / "source" / "DOC017.json").read_text(encoding="utf-8"))
TURNS = {t["source_id"]: t["text"] for t in doc["turns"]}


def E(sid, quote, role="basis"):
    assert sid in TURNS, "unknown source_id " + sid
    assert quote in TURNS[sid], "QUOTE NOT FOUND %s: %r" % (sid, quote)
    return {"source_id": sid, "quote": quote, "role": role}


# ---------------------------------------------------------------- evidence quotes
Q = {
    "T003a": E("DOC017:T003", "I would like to get job roles specific to the domain such as software engineering or machine learning roles."),
    "T003b": E("DOC017:T003", "job updates based on whatever is my skill set"),
    "T005a": E("DOC017:T005", "so it would be great if I'm actually looking for Job right? So it would be great if I receive at the instant. The job is like posted in the platform"),
    "T005b": E("DOC017:T005", "if I'm not looking actively, then it's okay to receive once in a week"),
    "T005c": E("DOC017:T005", "since I'm kind of market is kind of little dull, and they kinda release one or 2 jobs per day"),
    "T007a": E("DOC017:T007", "I would generally prefer getting via emails. It'll be great if I get via professional emails."),
    "T007b": E("DOC017:T007", "I would generally prefer getting via emails."),
    "T007c": E("DOC017:T007", "job notifications would also be great unless it's like too complicated. And it's like filling all my notification tab in my mobile"),
    "T007d": E("DOC017:T007", "job notifications would also be great unless it's like too complicated."),
    "T009a": E("DOC017:T009", "the email should be very concise"),
    "T009b": E("DOC017:T009", "It should have the necessary details which I kinda wanted to see in the platform"),
    "T009c": E("DOC017:T009", "it'll be great if everything is in the email. All the details are present in the email."),
    "T009d": E("DOC017:T009", "should be having a direct apply button in the email itself, so that I don't need to waste time then navigating to the app, and then again, going to the company's portal and applying right?"),
    "T009e": E("DOC017:T009", "should be having a direct apply button in the email itself, so that I don't need to waste time then navigating to the app"),
    "T011a": E("DOC017:T011", "I kind of go to the app filter based on my roles. And then companies what else? Location, etcetera. Right? So I apply all the filters."),
    "T011b": E("DOC017:T011", "I think today, Linkedin has this skill set percentage more than 50% or more than 60%. I think I will apply for that job."),
    "T011c": E("DOC017:T011", "And even for applying, I need to go to the company's portal, and then again, apply."),
    "T013a": E("DOC017:T013", "they kinda add a lot big message, and then they ask us whether they are interested, whether we are interested, and then they send us the link. So that is like a lot of process. And there's a lot of waiting time over there itself."),
    "T015a": E("DOC017:T015", "Yeah, I would say, it's not helpful in terms of like, what is it? When it's when I want to do my up when I do want. When I want to do my application quickly right."),
    "T017a": E("DOC017:T017", "in other ways it kind of helps me, because I kind of connect with the person some referral for the job."),
    "T019a": E("DOC017:T019", "one is the role like, I'll see if the role is really interesting. And I'm suitable for that role second is the payment. And then comes the location. And of course the company reputation."),
    "T021a": E("DOC017:T021", "I would consider the reviews from the current employees."),
    "T021b": E("DOC017:T021", "What work they are specifically working on, what text they are using."),
    "T021c": E("DOC017:T021", "how will I be contributing to their team right? Or to the company?"),
    "T023a": E("DOC017:T023", "if it's kinda like, what is it formatted in terms of list cars and tables that would be really helpful for me to navigate and get the actual details about the tech stack"),
    "T023b": E("DOC017:T023", "So it's like I need to navigate up and down and go to the specific location."),
    "T025a": E("DOC017:T025", "I I actually missed a job opportunity. Like, what 2 years back."),
    "T025b": E("DOC017:T025", "the notification system was not that accurate? And it was sending almost like what? All the jobs right? So few of the jobs were not relevant to me."),
    "T027a": E("DOC017:T027", "And with that I kind of missed few of the important jobs."),
    "T029a": E("DOC017:T029", "Apply. And that's that was a bad time. Yeah."),
    "T033a": E("DOC017:T033", "whenever I see a job posting, I see if there is a a skill set defined, necessary, skill set defined."),
    "T033b": E("DOC017:T033", "I kind of use some tool out Plugin. I see if I can actually match those skill sets with me, and it can also give some percentage out of it. So with that, I'll consider."),
    "T033c": E("DOC017:T033", "I see if I can actually match those skill sets with me, and it can also give some percentage out of it. So with that, I'll consider."),
    "T035a": E("DOC017:T035", "A can tell you that. Okay, this job is really like you can go for it. You can apply your perfect for this job."),
    "T037a": E("DOC017:T037", "the other policies and stuff like visa, status, etcetera, or whether I'm eligible to work based on my experience."),
    "T039a": E("DOC017:T039", "I kinda assume that it's already set right when it provides me the job list. and I don't need to add any more filters"),
    "T039b": E("DOC017:T039", "I will actually like, provide what are works I have done so far"),
    "T041a": E("DOC017:T041", "Also customizing few keywords for the job search to kind of get me the relevant result right?"),
    "T041b": E("DOC017:T041", "customizing few keywords for the job search to kind of get me the relevant result right?"),
    "T043a": E("DOC017:T043", "That will be great to have a that will be great to customize in my profile. Yeah."),
    "T047a": E("DOC017:T047", "Of course, the company's Hr right. Whoever is using this feature to actually like get the perfect candidate for the role."),
    "T049a": E("DOC017:T049", "And of course, even the job agency said."),
    "T051a": E("DOC017:T051", "Yeah. So these are a few people, I think, would really benefit out of these job update features."),
    "T055a": E("DOC017:T055", "it lists like unrelevant jobs to us. And I kind of get frustrated with that."),
    "T057a": E("DOC017:T057", "So I just like, sometimes I kind of blacklist those jobs. And yeah, I just remove those from. I just say that I'm uninterested. and I hope that it doesn't come."),
    "T059a": E("DOC017:T059", "if there is giving me a huge list of jobs I'll get confused. What to apply for."),
    "T059b": E("DOC017:T059", "whenever I go for a job application in Linkedin, right? It again navigates me to another page."),
    "T061a": E("DOC017:T061", "there is no point in having Linkedin. In the 1st place, when I have to like navigate to other place right."),
    "T061b": E("DOC017:T061", "So that's an extra efforts I should be putting from my end"),
    "T065a": E("DOC017:T065", "if we can differentiate with the ui like having separate ui for the description alone, and having separate for the responsibilities, etc."),
    "T065b": E("DOC017:T065", "in Linkedin for each job there's a huge list of description, details, responsibilities, etc. which is kind of annoying right and time myself."),
    "T067a": E("DOC017:T067", "Yeah, that would be really great to have integrated right?"),
    "T067b": E("DOC017:T067", "I would also prefer that all the details from my job portal is already like transferred to those reviews or Company's website."),
    "T069a": E("DOC017:T069", "Any reasons. Okay, one is getting random job notifications. Random people reaching me out in Linkedin or what there it is."),
    "T071a": E("DOC017:T071", "not having a relevant or updated job list."),
    "T071b": E("DOC017:T071", "I don't want to apply for jobs which are like one year back, or even 6 months back."),
    "T073a": E("DOC017:T073", "it's it's a hindrance for me to again fill all those details. Right? It's like a lot of manual effort. and it consumes a lot of time as well."),
    "T073b": E("DOC017:T073", "sometimes I I would like to kind of customize my details for few of the job roles right?"),
    "T075a": E("DOC017:T075", "I'm not sure if Linkedin has a bookmark feature."),
    "T075b": E("DOC017:T075", "have I just note down what the job id or whatever in a separate Doc, or something right? Maybe use notion, etc, right? And then maybe track in the later days of the week."),
    "T077a": E("DOC017:T077", "It'd be great to have such features in the job portal itself, because I again, as I said, I don't want to navigate to another application"),
    "T079a": E("DOC017:T079", "Everything is present in the job portal. It will be really great right."),
    "T081a": E("DOC017:T081", "I would say the AI feature from Linkedin that is really great to have."),
    "T081b": E("DOC017:T081", "If I configure my details in the Linkedin, it kind of persist. Right? I don't wanna again change those."),
    "T083a": E("DOC017:T083", "I don't want to. Expose my applications. Right. I don't want people to know for what job roles I'm applying for."),
    "T083b": E("DOC017:T083", "So it would be great to have everything private."),
    "T085a": E("DOC017:T085", "I don't want to people reaching me out from other platforms, right? So I don't want my data to be exposed by other people apart from the platform."),
    "T087a": E("DOC017:T087", "And there are a lot of even the customization features are missing."),
    "T089a": E("DOC017:T089", "You can't tell more details about your work experience, or your schooling and stuff."),
    "T089b": E("DOC017:T089", "And because of that, I think people reach you out for irrelevant roles."),
    "T091a": E("DOC017:T091", "it kind of list, you relevant tools. Right? It does some algorithm in the back. And it just finds your interest and matches with your skill set and gets you the necessary roles."),
    "T093a": E("DOC017:T093", "Of course it will be great to actually identify jobs."),
    "T093b": E("DOC017:T093", "but when it comes for writing applications, I think I kind of still feel that Eas are uncertain, right? They are not reliable."),
    "T095a": E("DOC017:T095", "So, of course, if it is like verified by us, then it's good. But yeah, but it shouldn't be automatic."),
    "T097a": E("DOC017:T097", "Exactly. Yeah."),
    "T099a": E("DOC017:T099", "if there is a quick, apply button right? Then it will be like, great yeah."),
    "T100a": E("DOC017:T100", "Oh, okay, so the needed criteria that you wish to have in a portal the skill sets and a quick apply button."),
    "T101a": E("DOC017:T101", "Yeah, yeah, that'll be great. Yeah."),
    "T105a": E("DOC017:T105", "I I would say 10 right? I mean I want to know what is my status of my application?"),
    "T105b": E("DOC017:T105", "if there is any feedback that would be really great for me to improve in my further applications."),
    "T107a": E("DOC017:T107", "They don't like provide proper feedbacks."),
    "T109a": E("DOC017:T109", "Even if I apply today I might get it's uncertain that I'll get what to say. Interview, call."),
    "T111a": E("DOC017:T111", "It would be great if I can track those status."),
}

# ---------------------------------------------------------------- raw candidates
# (cid, statement, actor, modality, context, origin, pass_id, [quote keys])
RAW = [
    ("C001", "Get job roles specific to the domain (e.g. software engineering or machine learning) and job updates based on whatever is my skill set", "Stakeholder", "would like / great to have", [], "explicit", "P1", ["T003a", "T003b"]),
    ("C002", "Receive at the instant the job is posted in the platform when actively looking for a job", "Stakeholder", "it would be great if", ["while actively looking for a job"], "explicit", "P1", ["T005a"]),
    ("C003", "It is okay to receive job updates once in a week when not looking actively", "Stakeholder", "okay to", ["when not looking actively"], "explicit", "P1", ["T005b"]),
    ("C004", "Have my roles, works done, experience, skill sets and projects already defined in the profile so the job list is already set and no more filters need to be added", "Stakeholder", "assume / would like", ["profile details provided"], "explicit", "P1", ["T039a", "T039b"]),
    ("C005", "Customize a few keywords for the job search to get relevant results", "Stakeholder", "would be great to have", [], "explicit", "P1", ["T041a"]),
    ("C006", "Do not get a job list that is not relevant or updated, and do not get unrelated jobs", "Stakeholder", "avoidance / frustration", [], "explicit", "P1", ["T071a", "T055a"]),
    ("C007", "Do not apply for jobs that are one year or even 6 months back; will not go ahead with the application if they are too old", "Stakeholder", "explicit negation", ["postings older than about 6 months to 1 year"], "explicit", "P1", ["T071b"]),
    ("C008", "Blacklist those jobs, remove them and say I am uninterested, hoping that they do not come again", "Stakeholder", "sometimes / hope", [], "explicit", "P1", ["T057a"]),
    ("C009", "Generally prefer getting job updates via emails, and it is great to get them via professional emails", "Stakeholder", "generally prefer", [], "explicit", "P1", ["T007a"]),
    ("C010", "Job notifications would also be great unless they are too complicated and fill all the notification tab in the mobile", "Stakeholder", "preference with exception", ["unless too complicated or filling the mobile notification tab"], "explicit", "P1", ["T007c"]),
    ("C011", "Actually missed a job opportunity about 2 years back because the notification system was not accurate and sent almost all jobs, and with that missed few important jobs", "Stakeholder", "negative experience", ["notification system inaccurate / unrelated jobs"], "explicit", "P1", ["T025a", "T025b", "T027a"]),
    ("C012", "The email should be very concise", "Stakeholder", "should", [], "explicit", "P1", ["T009a"]),
    ("C013", "The email should have the necessary details and everything is in the email with all the details present", "Stakeholder", "should / great if", [], "explicit", "P1", ["T009b", "T009c"]),
    ("C014", "Have a direct apply button in the email itself so no time is wasted navigating to the app and then the company's portal to apply", "Stakeholder", "should be having", ["in the email itself"], "explicit", "P1", ["T009d"]),
    ("C015", "It is not helpful when I want to do my application quickly", "Stakeholder", "complaint about slow application", [], "inferred", "P1", ["T015a"]),
    ("C016", "Have the company's specific job portal in an in-page view / integrated instead of being navigated to another page", "Stakeholder", "really great to have", [], "explicit", "P1", ["T067a", "T059b"]),
    ("C017", "Have all the details from my job portal already transferred to the company's website instead of filling all those details again", "Stakeholder", "would prefer / hindrance", ["after uploading resume"], "explicit", "P1", ["T067b", "T073a"]),
    ("C018", "Sometimes like to customize my details for a few of the job roles", "Stakeholder", "sometimes / in a good way", ["for a few specific job roles", "but without a lot of manual effort"], "explicit", "P1", ["T073b"]),
    ("C019", "Through a person's post on Linkedin there is a lot of big message, asking whether interested, then sending the link - a lot of process and waiting time", "Stakeholder", "complaint / not helpful", ["when navigating to a job from a person's post"], "explicit", "P1", ["T013a", "T015a"]),
    ("C020", "In other ways posts help because I connect with the person for some referral for the job", "Stakeholder", "helps me", ["via a person's post"], "inferred", "P1", ["T017a"]),
    ("C021", "Prioritize which job postings to apply for by role interest and suitability, payment, location and company reputation", "Stakeholder", "I'll see / considering all these factors", [], "explicit", "P1", ["T019a"]),
    ("C022", "Consider the reviews from the current employees", "Stakeholder", "I would consider", [], "explicit", "P1", ["T021a"]),
    ("C023", "See what work they are specifically working on and what text they are using", "Stakeholder", "important information", ["transcribed as 'what text they are using'"], "explicit", "P1", ["T021b"]),
    ("C024", "See how I will be contributing to their team or to the company", "Stakeholder", "important information", [], "explicit", "P1", ["T021c"]),
    ("C025", "Have tech stack details formatted in terms of list, cards and tables to navigate and get the actual details", "Stakeholder", "would be really helpful", [], "explicit", "P1", ["T023a"]),
    ("C026", "Differentiate with the UI, having a separate UI for the description alone and a separate one for the responsibilities", "Stakeholder", "if we can", [], "explicit", "P1", ["T065a", "T065b"]),
    ("C027", "See whether there is a necessary skill set defined in a job posting; the needed criteria in a portal are the skill sets and a quick apply button", "Stakeholder", "I see if / criteria you wish to have", [], "explicit", "P1", ["T033a", "T100a", "T101a"]),
    ("C028", "Use some tool or plugin to match those skill sets with me and give a percentage, as Linkedin does with 50% or 60%", "Stakeholder", "I kind of use", [], "explicit", "P1", ["T033b", "T011b"]),
    ("C029", "Use AI features in Linkedin to identify jobs, list relevant tools and signal that a job is perfect to apply for", "Stakeholder", "really great to have / exactly", ["AI used for identifying jobs"], "explicit", "P1", ["T035a", "T093a", "T091a", "T081a"]),
    ("C030", "When it comes to writing applications AI is uncertain and not reliable; if verified by us it is good but it should not be automatic", "Stakeholder", "explicit negation / verified by us", ["writing applications"], "explicit", "P1", ["T093b", "T095a", "T097a"]),
    ("C031", "Also consider other policies like visa status and whether I am eligible to work based on my experience", "Stakeholder", "of course / all comes up", [], "inferred", "P1", ["T037a"]),
    ("C032", "Note down the job id in a separate Doc or notion to track later, and it would be great to have such features in the job portal itself", "Stakeholder", "not sure / great to have", ["LinkedIn bookmark feature uncertain"], "explicit", "P1", ["T075a", "T075b", "T077a"]),
    ("C033", "Everything is present in the job portal and I do not want to navigate to another application or to another place", "Stakeholder", "really great / no point in", [], "explicit", "P1", ["T079a", "T077a", "T061a"]),
    ("C034", "Know what is the status of my application (10 out of 10) and be able to track those status", "Stakeholder", "10 / want to know", [], "explicit", "P1", ["T105a", "T111a", "T109a"]),
    ("C035", "Get feedback that would be really great for improving further applications; job portals do not provide proper feedbacks", "Stakeholder", "would be really great", [], "explicit", "P1", ["T105b", "T107a"]),
    ("C036", "Do not expose my applications, do not want people to know what job roles I am applying for, everything private", "Stakeholder", "explicit negation", [], "explicit", "P1", ["T083a", "T083b"]),
    ("C037", "Do not want my data exposed by other people apart from the platform", "Stakeholder", "explicit negation", [], "explicit", "P1", ["T085a"]),
    ("C038", "Do not want random job notifications and random people reaching me out on Linkedin, nor people reaching out for irrelevant roles", "Stakeholder", "explicit negation / reasons not to use", [], "explicit", "P1", ["T069a", "T089b"]),
    ("C039", "The company's HR, whoever is using this feature, can get the perfect candidate for the role", "Company HR", "of course / would benefit", [], "explicit", "P1", ["T047a"]),
    ("C040", "Be able to tell more details about work experience and schooling, and provide what works I have done so far in my profile", "Stakeholder", "missing in handshake / would like", [], "explicit", "P1", ["T089a", "T039b", "T087a"]),
    ("C041", "If I configure my details in Linkedin it persists and I do not want to change those again", "Stakeholder", "maintain / do not want", [], "explicit", "P1", ["T081b"]),
    ("C042", "Not be given a huge list of jobs that makes me confused about what to apply for", "Stakeholder", "challenge / confusion", [], "explicit", "P1", ["T059a"]),
    ("C043", "Even the job agency would benefit from these job update features", "Job agency", "benefit claim", [], "explicit", "P1", ["T049a", "T051a"]),
    ("C044", "Today I use Linkedin, go to the app, filter based on my roles, companies and location, pick suitable jobs based on skill set", "Stakeholder", "reported current habit", [], "unknown", "P1", ["T011a"]),
    ("C045", "Apply. And that was a bad time", "Stakeholder", "fragment / bad experience", ["continues T027 about missing important jobs"], "unknown", "P2", ["T029a"]),
    ("C046", "That will be great to customize in my profile", "Stakeholder", "great to have", [], "explicit", "P1", ["T043a"]),
    ("C047", "These are a few people I think would really benefit out of these job update features", "Stakeholder", "summary", [], "explicit", "P1", ["T051a"]),
    ("C048", "The AI feature from Linkedin is really great to have", "Stakeholder", "really great", [], "explicit", "P1", ["T081a"]),
    ("C049", "Yeah, that'll be great", "Stakeholder", "confirmation", ["confirms T100 criteria"], "explicit", "P1", ["T101a"]),
    ("C050", "Even if I apply today it is uncertain I will get an interview call", "Stakeholder", "tough / uncertain", [], "explicit", "P1", ["T109a"]),
    ("C051", "There are a lot of customization features missing in handshake", "Stakeholder", "missing", [], "explicit", "P1", ["T087a"]),
    ("C052", "Linkedin lists relevant tools, does some algorithm, finds your interest and matches with your skill set and gets you the necessary roles", "Stakeholder", "reported capability", [], "explicit", "P1", ["T091a"]),
    ("C053", "Exactly. Yeah.", "Stakeholder", "confirmation", ["confirms T096 summary about manual writing vs AI identification"], "explicit", "P1", ["T097a"]),
    ("C054", "One is getting random job notifications. Random people reaching me out in Linkedin", "Stakeholder", "reasons not to use", [], "explicit", "P1", ["T069a"]),
    ("C055", "In Linkedin for each job there is a huge list of description, details, responsibilities, which is annoying and time consuming", "Stakeholder", "annoying / time", [], "explicit", "P1", ["T065b"]),
    ("C056", "The market is kind of little dull and they release one or 2 jobs per day", "Stakeholder", "background fact", [], "unknown", "P1", ["T005c"]),
    ("C057", "Even for applying I need to go to the company's portal and then again apply", "Stakeholder", "reported current process", [], "unknown", "P1", ["T011c"]),
    ("C058", "I need to navigate up and down and go to the specific location", "Stakeholder", "current difficulty", [], "explicit", "P1", ["T023b"]),
    ("C059", "That is an extra effort I should be putting from my end", "Stakeholder", "complaint", [], "explicit", "P1", ["T061b"]),
]

raw_candidates = []
for cid, statement, actor, modality, context, origin, pass_id, qkeys in RAW:
    raw_candidates.append({
        "candidate_id": cid,
        "statement": statement,
        "actor": actor,
        "modality": modality,
        "context": context,
        "origin": origin,
        "pass_id": pass_id,
        "evidence": [Q[k] for k in qkeys],
    })

# ---------------------------------------------------------------- final goals
# (gid, statement, actor, context, origin, label, rationale, inference_or_None, quote_keys,
#  supported_parts, unsupported_parts, assumptions, reasoning_steps)
GOALS = [
    ("G001", "Receive job updates for roles in the user's domain (e.g. software engineering, machine learning) that match the user's skill set", "Stakeholder", [], "explicit", "direct",
     "原文直接陈述希望获得特定领域的职位角色，并希望职位更新基于自身技能集；主体、对象与范围均一致。", None,
     ["T003a", "T003b"], [], [], [], []),
    ("G002", "Receive a job update at the instant the job is posted on the platform while actively looking for a job", "Stakeholder", ["while actively looking for a job"], "explicit", "direct",
     "原文以 'it would be great if I receive at the instant' 明确表达即时接收意愿，并绑定主动求职这一条件与发布时刻。", None,
     ["T005a"], [], [], [], []),
    ("G003", "Receive job updates once a week when not actively looking for a job", "Stakeholder", ["when not actively looking for a job"], "explicit", "direct",
     "原文明确说非主动求职时每周一次 'is okay'，是可让步但明确选定的频率；未升级为必须。", None,
     ["T005b"], [], [], [], []),
    ("G004", "Have the job list derived automatically from the profile (roles, work done, experience, skill sets, projects) so no additional filters need to be added", "Stakeholder", ["profile details already provided"], "explicit", "direct",
     "原文明确表示期望资料中的角色、经验、技能、项目已设置好，提供职位列表时不需要再加筛选。", None,
     ["T039a", "T039b"], [], [], [], []),
    ("G005", "Customize a few keywords for the job search in the profile to get relevant results", "Stakeholder", [], "explicit", "direct",
     "原文明确说自定义少量搜索关键词以获得相关结果，并在 T043 再次确认为在资料中自定义。", None,
     ["T041a", "T043a"], [], [], [], []),
    ("G006", "Receive only job postings relevant to the user's criteria, not a random or unrelated job list", "Stakeholder", [], "explicit", "direct",
     "T071 将 'not having a relevant or updated job list' 列为不使用职位应用的理由，T055 明确抱怨不相关职位，均为明确的相关性要求；非仅凭抱怨推断。", None,
     ["T071a", "T055a", "T069a"], [], [], [], []),
    ("G007", "Have the job list kept up to date so that postings one year or even 6 months old are not presented", "Stakeholder", ["postings older than about 6 months to 1 year"], "explicit", "direct",
     "原文明确表达不会申请一年甚至半年前的职位，且太旧就不会继续申请；时间限定保留。", None,
     ["T071b", "T071a"], [], [], [], []),
    ("G008", "Be able to blacklist a job or mark it as uninterested so that it no longer comes back", "Stakeholder", [], "explicit", "direct",
     "原文描述其屏蔽、移除、标记不感兴趣并希望不再出现的行为，属于明确的避免与结果意图。", None,
     ["T057a"], [], [], [], []),
    ("G009", "Receive job updates by professional email", "Stakeholder", [], "explicit", "direct",
     "原文 'I would generally prefer getting via emails' 与 'It'll be great if I get via professional emails' 明确表达渠道偏好，保留 generally 与 professional，不升级为强制。", None,
     ["T007a"], [], [], [], []),
    ("G010", "Also receive job updates as mobile notifications provided they are not too complicated and do not fill up the mobile notification tab", "Stakeholder", ["unless too complicated or filling the mobile notification tab"], "explicit", "direct",
     "原文用 'unless' 明确给出接受移动端通知的例外条件，否定与条件完整保留。", None,
     ["T007c"], [], [], [], []),
    ("G011", "Not miss important job opportunities because notifications were inaccurate or unrelated", "Stakeholder", ["notification system inaccurate / unrelated jobs"], "inferred", "inferred",
     "原文只陈述了因通知不准确、群发不相关职位而错过重要机会的负面经历；由该经历及 G006 的相关性要求正面推断其希望不再错过，未新增具体机制。",
     {"basis_candidate_ids": ["G006"], "reason": "从'错过重要职位'的负面经历与对相关、准确通知的明确要求，推断出避免再次错过的期望结果", "assumptions": ["更准确且相关的通知能避免错过重要职位"]},
     ["T025a", "T025b", "T027a", "T029a"], [], [], ["通知准确性提升可减少漏看"], ["定位负面经历", "确认原文有相关性诉求", "推断避免型结果"]),
    ("G012", "Have the job notification email be very concise", "Stakeholder", [], "explicit", "direct",
     "原文 'the email should be very concise' 明确表达简洁要求，强度为 should 而非 must。", None,
     ["T009a"], [], [], [], []),
    ("G013", "Have all the necessary job details present in the notification email itself", "Stakeholder", [], "explicit", "direct",
     "原文明确说邮件应含必要详情、'everything is in the email'、'All the details are present in the email'；详略与 G012 的张力记入 review_questions。", None,
     ["T009b", "T009c"], [], [], [], []),
    ("G014", "Apply to a job directly from where the update is received via a direct apply button in the email or a quick apply button in the portal, instead of navigating to the app and then the company's portal", "Stakeholder", ["in the email itself / in the portal"], "explicit", "direct",
     "T009 明确要求邮件内直接申请按钮以免跳转应用与公司门户；T099/T101 与 T100 明确门户网站需要 quick apply button，同一核心动作合并并保留两种载体。", None,
     ["T009d", "T099a", "T100a", "T101a"], [], [], [], []),
    ("G015", "Complete a job application quickly", "Stakeholder", [], "inferred", "inferred",
     "原文以'在想快速申请时，帖子方式没帮助'的形式表达，快速申请为隐含的期望结果而非直接陈述的系统要求；转写有断裂但语义可判定。",
     {"basis_candidate_ids": ["G014"], "reason": "由'想快速完成申请'的意愿与对慢流程的否定评价，推断出快速完成申请这一结果", "assumptions": ["在更新所在位置直接提交即为快速申请的实现方式"]},
     ["T015a"], [], [], ["快速申请以直接申请入口为实现方式"], ["识别否定评价", "提取隐含期望结果", "不补造阈值"]),
    ("G016", "View and apply through the company's job portal in an in-page (integrated) view inside the application instead of being navigated to another page", "Stakeholder", [], "explicit", "direct",
     "T067 确认页面内嵌视图 'would be really great to have integrated'，T059 明确抱怨被导航到另一页，主体与对象一致。", None,
     ["T067a", "T059b", "T011c"], [], [], [], []),
    ("G017", "Have profile details already entered in the job portal transferred into the company's website/application form instead of filling them in again after uploading a resume", "Stakeholder", ["after uploading a resume"], "explicit", "direct",
     "T067 明确希望职位门户资料自动转移到公司网站；T073 明确重复填写全部信息是障碍、耗时。", None,
     ["T067b", "T073a"], [], [], [], []),
    ("G018", "Be able to customize application details for a few specific job roles", "Stakeholder", ["for a few specific job roles", "without a lot of manual effort"], "explicit", "direct",
     "T073 在让步句中明确表示有时希望针对少数职位角色自定义申请资料，保留 'sometimes'、'few' 与不要大量手工的约束。", None,
     ["T073b"], [], [], [], []),
    ("G019", "Avoid getting jobs through a person's post that requires several rounds of messaging and waiting for a link", "Stakeholder", ["when navigating to a job from a person's post"], "inferred", "inferred",
     "原文明确评价该方式流程多、等待时间长、在想快速申请时没帮助；由此推断其希望避免该多轮往返方式，并保留 T017 的内推价值为相反证据。",
     {"basis_candidate_ids": ["G015"], "reason": "由对帖子方式多步骤与等待的明确负面评价，推断出避免该方式的期望结果", "assumptions": ["存在可直接获取职位链接的替代途径"]},
     ["T013a", "T015a"], [], [], ["替代途径存在"], ["识别负面评价", "区分症状与结果", "保留 T017 让步"]),
    ("G020", "Be able to connect with the person who posted the job to get a referral", "Stakeholder", ["via a person's post"], "inferred", "inferred",
     "原文仅说明现有帖子方式在内推方面'helps me'，是对现有体验的正面评价；由此推断其希望保留该价值，未表达为新系统的明确要求。",
     {"basis_candidate_ids": ["G019"], "reason": "由对帖子方式可带来内推的正面评价，推断其希望延续该获益途径", "assumptions": ["内推价值应延续到新系统"]},
     ["T017a"], [], [], ["内推价值应保留"], ["识别正面评价", "区分现状与要求", "标为推断"]),
    ("G021", "Decide which job postings to apply for by weighing role interest and suitability, payment, location and company reputation", "Stakeholder", [], "explicit", "direct",
     "T019 明确列举四项排序因素并说 'considering all these factors' 才申请；同一动作的多项限定不机械拆分。", None,
     ["T019a"], [], [], [], []),
    ("G022", "See reviews from current employees of the company", "Stakeholder", [], "explicit", "direct",
     "T021 明确说 'I would consider the reviews from the current employees'，是最重要的职位信息之一。", None,
     ["T021a"], [], [], [], []),
    ("G023", "See what work the team is specifically working on and what stack they are using", "Stakeholder", ["transcribed 'what text they are using', read as tech stack by context"], "explicit", "direct",
     "T021 明确列出希望看到的工作内容与技术栈信息；原文转写为 'what text they are using'，按上下文理解为技术栈并在 context 记录该歧义。", None,
     ["T021b"], [], [], [], []),
    ("G024", "See how the user would be contributing to the team or to the company", "Stakeholder", [], "explicit", "direct",
     "T021 明确说要了解自己将如何为团队或公司做贡献，属于独立的信息需求。", None,
     ["T021c"], [], [], [], []),
    ("G025", "Have tech stack and similar details formatted as lists, cards or tables so they can be navigated quickly", "Stakeholder", [], "explicit", "direct",
     "T023 明确说用 list/cards/tables 格式化 'would be really helpful' 以便导航获取技术栈详情；保留原文 'list cars' 的转写形式于引文。", None,
     ["T023a", "T023b"], [], [], [], []),
    ("G026", "Have the job description and the responsibilities shown in separate UI sections instead of one long block", "Stakeholder", [], "explicit", "direct",
     "T065 明确提议用单独 UI 区分描述与职责，并说明长篇混排令人厌烦且耗时。", None,
     ["T065a", "T065b"], [], [], [], []),
    ("G027", "Have the necessary skill set explicitly defined in a job posting", "Stakeholder", [], "explicit", "direct",
     "T033 说明其查看职位时先看是否定义了必要技能集，T100/T101 确认门户需要的 criteria 包含 skill sets。", None,
     ["T033a", "T100a", "T101a"], [], [], [], []),
    ("G028", "Have a tool or plugin that matches the required skill set against the user's and gives a match percentage", "Stakeholder", [], "explicit", "direct",
     "T033 明确说使用插件匹配技能集并给出百分比 'So with that, I'll consider'；T011 补充 Linkedin 的 50%/60% 百分比。", None,
     ["T033b", "T011b"], [], [], [], []),
    ("G029", "Use AI to identify and signal jobs that match the user's interest and skill set", "Stakeholder", ["AI used for identifying jobs, not writing applications"], "explicit", "direct",
     "T093 'Of course it will be great to actually identify jobs' 与 T097 确认明确认可 AI 用于识别职位；T035 说明 AI 会告知职位非常匹配，T091 说明算法匹配兴趣与技能集，T081 认可 AI 功能。", None,
     ["T093a", "T035a", "T091a", "T081a", "T097a"], [], [], [], []),
    ("G030", "Not have AI write the application automatically; anything AI produces for writing should be verified by the user", "Stakeholder", ["writing applications"], "explicit", "direct",
     "T093 明确认为 AI 代写申请不可靠，T095 明确 'it shouldn't be automatic' 且 'verified by us, then it's good'，T097 确认；否定与人工确认条件完整保留。", None,
     ["T093b", "T095a", "T097a"], [], [], [], []),
    ("G031", "Have visa status, work eligibility and similar policy conditions taken into account when judging a job posting", "Stakeholder", [], "inferred", "inferred",
     "原文在回答'如何定义相关职位'时补充 'the other policies ... visa, status ... whether I'm eligible to work ... all comes up'；由该纳入考虑的表述推断其希望相关性判断涵盖这些条件，未假定由系统自动判定。",
     {"basis_candidate_ids": ["G006"], "reason": "由相关性判断中'其他政策与工作资格也会纳入考虑'的表述，推断其希望这些条件被考虑", "assumptions": ["系统能获知签证状态与工作资格信息"]},
     ["T037a"], [], [], ["签证/资格信息可得"], ["定位问答范围", "识别补充条件", "推断而非升级为自动判定"]),
    ("G032", "Save or bookmark interesting job postings inside the job portal to apply to them later", "Stakeholder", ["LinkedIn bookmark feature uncertain"], "explicit", "direct",
     "T075 描述其记录职位 id 并稍后跟踪的做法且不确定 Linkedin 是否有书签功能；T077 明确 'It'd be great to have such features in the job portal itself'。", None,
     ["T075a", "T075b", "T077a"], [], [], [], []),
    ("G033", "Have every job-related activity available inside the job portal without navigating to another application or the company's portal", "Stakeholder", [], "explicit", "direct",
     "T079 'Everything is present in the job portal'、T077 'I don't want to navigate to another application'、T061 'no point in having Linkedin ... navigate to other place' 反复明确表达集中完成的诉求。", None,
     ["T079a", "T077a", "T061a"], [], [], [], []),
    ("G034", "See and track the status of submitted applications", "Stakeholder", [], "explicit", "direct",
     "T105 明确 'I want to know what is my status' 且自评重要性为 10；T111 明确 'It would be great if I can track those status'。", None,
     ["T105a", "T111a", "T109a"], [], [], [], []),
    ("G035", "Receive employer feedback on applications in order to improve later applications", "Stakeholder", [], "explicit", "direct",
     "T105 明确 'if there is any feedback that would be really great for me to improve in my further applications'，T107 补充现状缺乏反馈。", None,
     ["T105b", "T107a"], [], [], [], []),
    ("G036", "Keep applications private so other people cannot see which job roles are being applied for", "Stakeholder", [], "explicit", "direct",
     "T083 明确 'I don't want to Expose my applications'、'I don't want people to know for what job roles I'm applying for' 与 'everything private'。", None,
     ["T083a", "T083b"], [], [], [], []),
    ("G037", "Not have personal data exposed to people or platforms outside the job platform", "Stakeholder", [], "explicit", "direct",
     "T085 明确 'I don't want my data to be exposed by other people apart from the platform'，主体与数据边界一致。", None,
     ["T085a"], [], [], [], []),
    ("G038", "Not be contacted by random or irrelevant people or recruiters through the platform", "Stakeholder", [], "explicit", "direct",
     "T069 将 'Random people reaching me out in Linkedin' 列为不使用应用的理由，T089 说明因资料不足被不相关职位的人联系。", None,
     ["T069a", "T089b"], [], [], [], []),
    ("G039", "Let the company's HR find the perfect candidate for a role through this feature", "Company HR", [], "explicit", "direct",
     "T047 在回答'谁还能受益'时明确说明公司 HR 使用该功能以获得职位的完美候选人，主体为 HR 而非受访者。", None,
     ["T047a"], [], [], [], []),
    ("G040", "Be able to enter more detailed profile information such as work experience and schooling", "Stakeholder", [], "explicit", "direct",
     "T089 指出 handshake 无法填写更详细的工作经历与教育背景，T039 明确表示愿意提供已完成的工作，T087 指出自定义功能缺失。", None,
     ["T089a", "T039b", "T087a"], [], [], [], []),
    ("G041", "Have configured profile details persist so they do not have to be entered again", "Stakeholder", [], "explicit", "direct",
     "T081 明确说在 Linkedin 配置的资料会 persist 且 'I don't wanna again change those'，属于有继续维持意图的维持型目标。", None,
     ["T081b"], [], [], [], []),
    ("G042", "Not be given a huge list of jobs that leaves the user confused about what to apply for", "Stakeholder", [], "explicit", "direct",
     "T059 明确说大量职位列表会让其困惑、不知申请哪个，属于避免型结果意图。", None,
     ["T059a"], [], [], [], []),
    ("G043", "Have job agencies benefit from these job update features", "Job agency", [], "explicit", "insufficient",
     "T049 仅将招聘中介列为受益方，T051 为总结句，均未说明中介的具体需求、使用方式或期望结果；内容不足以判定一个可独立满足的目标，如实保留为 insufficient，不升级为 direct/inferred。", None,
     ["T049a", "T051a"], [], ["具体受益方式与使用需求未表达"], [], []),
]

goals = []
for (gid, statement, actor, context, origin, label, rationale, inference, qkeys,
     supported_parts, unsupported_parts, assumptions, reasoning_steps) in GOALS:
    goals.append({
        "candidate_id": gid,
        "statement": statement,
        "actor": actor,
        "context": context,
        "origin": origin,
        "inference": inference,
        "evidence": [Q[k] for k in qkeys],
        "judgment": {
            "label": label,
            "rationale": rationale,
            "supported_parts": supported_parts,
            "unsupported_parts": unsupported_parts,
            "assumptions": assumptions,
            "reasoning_steps": reasoning_steps,
        },
    })

# ---------------------------------------------------------------- ledger entries
# (cid, disposition, [gids], reason)
ENTRIES = [
    ("C001", "keep", ["G001"], "领域与技能集匹配为同一接收更新的两个限定，整体保留为一个目标"),
    ("C002", "keep", ["G002"], "即时接收绑定主动求职条件，独立保留"),
    ("C003", "keep", ["G003"], "非主动求职时每周一次为独立情境频率，保留"),
    ("C004", "keep", ["G004"], "资料自动匹配、无需再加筛选为独立结果"),
    ("C005", "keep", ["G005"], "关键词自定义为独立动作"),
    ("C006", "keep", ["G006"], "'relevant or updated' 中本条承接相关性，'更新/过期'维度由 C007 独立承接"),
    ("C007", "keep", ["G007"], "过期职位为独立的时间维度结果"),
    ("C008", "keep", ["G008"], "屏蔽与标记不感兴趣为独立避免动作"),
    ("C009", "keep", ["G009"], "邮件渠道偏好保留 generally 与 professional"),
    ("C010", "keep", ["G010"], "移动端通知含 unless 例外，独立保留"),
    ("C011", "keep", ["G011"], "错过机会的经历作为避免型目标来路，标 inferred"),
    ("C012", "keep", ["G012"], "邮件简洁为独立质量意图"),
    ("C013", "keep", ["G013"], "邮件含全部详情与 G012 有张力但为独立结果，不合并"),
    ("C014", "keep", ["G014"], "直接申请按钮为独立动作"),
    ("C015", "keep", ["G015"], "快速申请为隐含目的，标 inferred"),
    ("C016", "keep", ["G016"], "页面内嵌申请为具体情境，独立保留"),
    ("C017", "keep", ["G017"], "资料自动转移为独立结果"),
    ("C018", "keep", ["G018"], "针对少数角色自定义申请资料是 T073 让步中的独立意图，保留"),
    ("C019", "keep", ["G019"], "避免帖子多步骤流程为独立避免结果，标 inferred"),
    ("C020", "keep", ["G020"], "内推为现有方式的正面价值，标 inferred 并保留为 G019 的相反证据"),
    ("C021", "keep", ["G021"], "四项优先级因素为同一决定动作的多限定，不机械拆分"),
    ("C022", "keep", ["G022"], "员工评价为独立信息项"),
    ("C023", "keep", ["G023"], "工作内容与技术栈为独立信息项，转写歧义写入 context"),
    ("C024", "keep", ["G024"], "个人贡献预期为独立信息项"),
    ("C025", "keep", ["G025"], "结构化展示为独立动作"),
    ("C026", "keep", ["G026"], "描述/职责分离 UI 为独立动作"),
    ("C027", "keep", ["G027"], "职位定义技能集为独立结果"),
    ("C028", "keep", ["G028"], "匹配百分比工具为独立系统功能"),
    ("C029", "keep", ["G029"], "AI 识别匹配职位为独立结果"),
    ("C030", "keep", ["G030"], "AI 不自动代写为独立否定型结果"),
    ("C031", "keep", ["G031"], "签证/资格条件为相关性判断的独立补充维度，标 inferred"),
    ("C032", "keep", ["G032"], "门户内保存职位为独立动作"),
    ("C033", "keep", ["G033"], "一切在门户内完成为反复表达的独立一般目标"),
    ("C034", "keep", ["G034"], "查看/跟踪申请状态为独立结果"),
    ("C035", "keep", ["G035"], "雇主反馈为独立结果"),
    ("C036", "keep", ["G036"], "申请保密为独立隐私结果"),
    ("C037", "keep", ["G037"], "数据不外泄为独立数据边界结果"),
    ("C038", "keep", ["G038"], "不被不相关人员联系为独立避免结果"),
    ("C039", "keep", ["G039"], "HR 找到合适候选人为其他主体的独立目标"),
    ("C040", "keep", ["G040"], "填写详尽资料为独立结果"),
    ("C041", "keep", ["G041"], "资料持久化为独立维持型结果"),
    ("C042", "keep", ["G042"], "避免大列表困惑为独立结果"),
    ("C043", "keep", ["G043"], "招聘中介仅列受益方，保留为 insufficient 目标，不升级"),
    ("C044", "exclude", [], "仅描述在 Linkedin 按角色/地点过滤并挑选职位的现有习惯，未表达对系统的期望结果；其中跳转公司门户的诉求由 C057 承接"),
    ("C045", "merge", ["G011"], "T029 为跨窗断裂片段，结合 T027 理解为错过申请，与错过机会同源，记 P2 补查"),
    ("C046", "merge", ["G005"], "T043 再次确认在资料中自定义，与关键词自定义同义"),
    ("C047", "merge", ["G039"], "T051 为受益方总结句，无新增意图，并入 HR 受益"),
    ("C048", "merge", ["G029"], "对 Linkedin AI 功能的认可与 AI 识别职位同源"),
    ("C049", "merge", ["G027"], "T101 是对 T100 两项 criteria 的重复确认；其中 quick apply button 已由 C014/G014 承接，本条按同义确认并入技能集 G027"),
    ("C050", "merge", ["G034"], "面试通知不确定是申请状态跟踪的现状补充，并入 G034"),
    ("C051", "merge", ["G040"], "handshake 自定义功能缺失与详细资料诉求同源"),
    ("C052", "merge", ["G029"], "Linkedin 算法匹配推荐与 AI 识别匹配职位同源"),
    ("C053", "merge", ["G029"], "T097 是对 T096 总结的重复确认；其中不自动代写已由 C030 承接，本条按同义确认并入 AI 识别 G029"),
    ("C054", "split", ["G038", "G006"], "T069 含两个独立结果：随机通知（并入相关性 G006）与陌生人联系（G038）"),
    ("C055", "merge", ["G026"], "长篇描述令人厌烦是分离 UI 诉求的现状依据"),
    ("C056", "exclude", [], "市场发布量小的背景事实，非目标意图"),
    ("C057", "merge", ["G016"], "需跳转公司门户申请的现状是页面内嵌申请诉求的障碍依据"),
    ("C058", "merge", ["G025"], "上下滚动找信息是结构化展示诉求的现状依据"),
    ("C059", "merge", ["G033"], "额外跳转 effort 是一切在门户内完成诉求的现状依据"),
]

entries = [{"candidate_id": c, "disposition": d, "final_goal_ids": g, "reason": r}
           for c, d, g, r in ENTRIES]
assert len({e["candidate_id"] for e in entries}) == len(RAW), "entries/RAW mismatch"
assert {e["candidate_id"] for e in entries} == {r[0] for r in RAW}

# ---------------------------------------------------------------- source_checks
SC = [
    ("S1", ["T009a", "T009c"], ["C012", "C013"], ["G012", "G013"], "represented", "回查 T009：同句既要求 very concise 又要求 All the details are present，二者均保留为独立目标，张力记入 review_questions"),
    ("S2", ["T015a", "T017a"], ["C019", "C020"], ["G019", "G020"], "represented", "回查 T014-T017：帖子方式既被否定（流程/等待）又被肯定（内推），避免目标与内推价值分别保留，不互相抵消"),
    ("S3", ["T073a", "T073b"], ["C017", "C018"], ["G017", "G018"], "represented", "回查 T073：重复填写是障碍，但让步句明确认可针对少数角色自定义，两者分别保留且不把偏好升级为强制"),
    ("S4", ["T093a", "T093b", "T095a", "T097a"], ["C029", "C030"], ["G029", "G030"], "represented", "回查 T092-T097：AI 用于识别职位被认可、代写申请被否定且须人工确认，T097 明确确认该区分"),
    ("S5", ["T055a", "T071a"], ["C006", "C007"], ["G006", "G007"], "represented", "回查 T052-T055 与 T071：系统推荐不匹配职位与列表不相关/不更新为同一相关性诉求的两处证据，并拆出过期职位维度"),
    ("S6", ["T049a", "T051a"], ["C043"], ["G043"], "uncertain", "回查 T044-T051：招聘中介仅被列为受益方，无具体意图内容，保留 insufficient 目标与待确认问题"),
    ("S7", ["T011a"], ["C044"], [], "excluded", "回查 T011：在 Linkedin 按角色/地点过滤为现状描述，非系统要求，排除；跳转申请部分改由 C057 承接"),
    ("S8", ["T005c"], ["C056"], [], "excluded", "回查 T005：市场发布量小为条件背景，不计为目标"),
    ("S9", ["T021b"], ["C023"], ["G023"], "represented", "回查 T021/T023：'what text they are using' 疑为 tech stack 转写错误，按 T023 的技术栈上下文理解并写入 context 与问题"),
    ("S10", ["T025a", "T027a", "T029a"], ["C011", "C045"], ["G011"], "represented", "回查 T025-T031：跨窗合并错过机会的断裂叙述，标 inferred 且不补造防错过机制"),
    ("S11", ["T075a", "T077a"], ["C032"], ["G032"], "represented", "回查 T074-T079：对 Linkedin 是否有书签功能表示不确定，但明确要求门户内置该功能，不确定性与明确要求分别保留"),
    ("S12", ["T065a", "T065b"], ["C026", "C055"], ["G026"], "represented", "回查 T065：含转写不清片段 'Sean and Chris'，不影响其后分离 UI 的明确诉求，按可判定部分保留"),
]
source_checks = [{"check_id": c, "evidence_candidates": [Q[k] for k in q], "candidate_ids": cids,
                  "final_goal_ids": gids, "outcome": o, "reason": r} for c, q, cids, gids, o, r in SC]

# ---------------------------------------------------------------- windows
WINDOW_IDS = ["DOC017:W%04d" % i for i in range(1, 57)]
WINDOW_RESULTS = [{"window_id": w, "status": "processed", "reason": ""} for w in WINDOW_IDS]

# ---------------------------------------------------------------- relations
RELATIONS = [
    ("R1", "G014", "G015", "operationalization", "supported", "T009e", "直接/快速申请按钮是快速完成申请的明确实现方式，T009 用 'so that I don't need to waste time' 连接方式与目的"),
    ("R2", "G016", "G033", "specialization", "supported", "T061a", "页面内嵌申请是'一切在门户内完成、不跳转别处'在公司门户申请这一具体情境下的具体化"),
    ("R3", "G032", "G033", "specialization", "supported", "T077a", "门户内置收藏是'不跳转到另一个应用'在保存职位这一具体情境下的具体化"),
    ("R4", "G009", "G001", "operationalization", "supported", "T007b", "T006 明确问通过哪些渠道接收职位更新，专业邮箱是接收匹配职位更新的选定渠道"),
    ("R5", "G010", "G001", "operationalization", "supported", "T007d", "移动端通知是接收职位更新的另一渠道，且保留 unless 例外"),
    ("R6", "G005", "G006", "operationalization", "supported", "T041b", "T041 明确用 'to kind of get me the relevant result' 表明关键词自定义服务于获得相关结果"),
    ("R7", "G004", "G006", "operationalization", "supported", "T039a", "资料驱动的自动筛选服务于提供已匹配的相关职位列表，无需再加筛选"),
    ("R8", "G028", "G006", "operationalization", "supported", "T033c", "T032 问如何定义相关职位，T033 以技能匹配百分比工具作为判断相关性的方式，'So with that, I'll consider'"),
    ("R9", "G037", "G038", "operationalization", "supported", "T085a", "T085 用 'So' 连接：不希望被其他平台的人联系，因此不希望数据暴露给平台之外，前者以后者为实现方式"),
    ("R10", "G002", "G001", "specialization", "supported", "T005a", "T004 问接收频率，主动求职时即时接收是接收匹配职位更新在该情境下的具体化"),
    ("R11", "G003", "G001", "specialization", "supported", "T005b", "非主动求职时每周接收是接收匹配职位更新在另一情境下的具体化"),
]
relations = [{"relation_id": rid, "source_id": s, "target_id": t, "type": typ, "status": st,
              "conditions": [], "assumptions": [], "rationale": rat, "evidence_ids": [],
              "evidence_quotes": [Q[qk]]} for rid, s, t, typ, st, qk, rat in RELATIONS]

# ---------------------------------------------------------------- group (proposed / partial)
GROUPS = [{
    "group_id": "GR1", "parent_id": "G033", "child_ids": ["G016", "G032"], "kind": "and",
    "status": "proposed", "completeness": "partial",
    "rationale": "G016（页面内申请）与 G032（门户内收藏）都是 G033（一切在门户内完成）的具体情境，但原文提到的查看员工评价、技术栈、职位职责区块、申请状态与反馈等操作未由这两个子目标共同覆盖，不能声称整组共同满足足以实现父目标，故保留 proposed/partial",
    "assumptions": ["门户内还包含查看职位信息与跟踪状态等其他操作", "这些其他操作是否也须在门户内完成未获原文确认"],
    "evidence_ids": [],
    "evidence_quotes": [Q["T079a"]],
    "relation_ids": ["R2", "R3"],
    "checks": [
        {"kind": "normal", "origin": "analysis_assumption",
         "scenario": "用户在门户内收到匹配更新，点击后在页面内嵌视图完成公司门户申请，并把该职位加入门户内收藏列表，全程未跳转外部应用",
         "outcome": "supports", "rationale": "该场景下申请与保存两个子目标共同满足'一切在门户内完成'，为编制者构造的分析假设"},
        {"kind": "exception", "origin": "analysis_assumption",
         "scenario": "用户需要在同一门户内查看在职员工评价、团队技术栈、职责区块，或跟踪申请状态与雇主反馈（G022/G023/G024/G026/G034/G035）",
         "outcome": "counterexample", "rationale": "原文未说明这些操作也在门户内完成，G016 与 G032 未覆盖父目标全部范围，故整组不完整且存在未解决反例"},
    ],
}]

# ---------------------------------------------------------------- questions
REVIEW_QUESTIONS = [
    (["G012", "G013"], "邮件既要 'very concise' 又要 'All the details are present in the email'，两者的边界（哪些详情、多长）如何确定？", "同句内两个质量意图存在张力，原文未给出取舍标准"),
    (["G040", "G036", "G037"], "希望在资料中填写更详尽的工作经历与教育背景，同时又要求申请与数据保密；二者如何同时满足？", "更多信息与隐私收紧方向相反，原文未说明可见范围控制"),
    (["G043"], "招聘中介被列为受益方，但原文未说明其具体需求或使用方式，是否需要补充访谈？", "当前目标为 insufficient，不能升级为已支持"),
    (["G015"], "T015 'When I want to do my application quickly' 一句转写断裂（'do my up'），快速申请的验收标准（步数/耗时）未给出", "影响目标完整语义但无阈值可依据，未补造"),
    (["G003"], "'once in a week' 是期望频率还是仅为可接受下限？", "原文用 'it's okay to'，强度为可让步，未确认是否为首选"),
    (["G023"], "T021 'what text they are using' 疑为 tech stack 的转写错误，按上下文理解为所用技术栈，需核对录音", "识别歧义可能影响目标对象范围"),
    (["G011"], "除通知准确外，原文未说明防止错过重要职位的具体机制（置顶、二次提醒等）", "inferred 目标不补造实现机制"),
    (["G030"], "'verified by us' 的具体含义（逐字确认还是整体确认）与 AI 可参与的边界未明确", "影响否定型目标的适用范围"),
    (["G029", "G030"], "AI 用于识别职位与不得自动代写之间的分界（如自动填充表单字段是否属于代写）未说明", "两项均原文明确，但交界处无依据"),
]

DECISION_QUESTIONS = [
    ("group", "GR1", "G033 的子目标只覆盖申请与保存，未覆盖查看员工评价/技术栈/职责区块、跟踪状态与反馈等操作；需确认是否可声称整组充分，否则维持 proposed/partial"),
    ("goal", "G043", "招聘中介无具体意图内容，目标为 insufficient，需补访谈或明确排除"),
    ("goal", "G012", "与 G013 的邮件详略张力未解决"),
    ("goal", "G013", "与 G012 的邮件详略张力未解决"),
    ("goal", "G011", "label 为 inferred，仅由负面经历推断，需确认防错过机制与可接受的支持强度"),
    ("goal", "G015", "T015 转写断裂，快速申请的判定标准未给出"),
    ("goal", "G031", "label 为 inferred，签证/资格是否由系统判断、信息来源为何未明"),
    ("goal", "G023", "原文 'what text they are using' 存在转写歧义，需核对录音"),
    ("relation", "R9", "G037→G038 的操作化方向依赖 T085 中 'So' 的因果读法，需确认方向未写反"),
    ("model", "DOC017-goal-model", "全篇为单人访谈，多个目标来自偏好、现状体验或让步推断，无第二受访者交叉验证；成立精化组数为 0"),
]

# ---------------------------------------------------------------- assemble
spec = {
    "document_id": "DOC017",
    "raw_candidates": raw_candidates,
    "goals": goals,
    "review_questions": [{"candidate_ids": c, "question": q, "reason": r} for c, q, r in REVIEW_QUESTIONS],
    "limitations": [
        "只读取 source/DOC017.json 提供的 114 轮访谈转写，未读取其他材料或参考答案，未联网",
        "原文为访谈转写，存在多处转写异常（'what text they are using'、'list cars'、'Eas'、'Sean and Chris'、'do my up'、T027/T029 跨轮断裂），按上下文理解并在 context/问题中记录，未改动原文",
        "窗口按 size=4/stride=2 生成，共 56 个；逐窗捕获后做一次全篇校正，未做独立重复采样",
        "未执行独立语义审查与形式证明；精化充分性为编制者判断，非程序证明",
    ],
    "ledger": {
        "model": "unknown", "temperature": "unknown",
        "budget": "1 initial pass + 1 full-context correction pass + <=2 repair rounds",
        "usage": "unknown",
        "skill_revision": "a5952d426b1624a3fcb2ce2829e1ae1ceb15e19dc3309d9571f3bc6b465deb6f",
        "prompt_revision": "task-prompt-v1",
        "planned_passes": 2,
        "stop_reason": "已读完 114 轮原文、逐窗处理全部 56 个窗口并完成一次全篇指代/条件/例外/相反证据校正；原文无新增有据意图，剩余未决为需人工或补充访谈的语义缺口，按预算停止",
        "passes": [
            {"pass_id": "P1", "kind": "initial", "context": "isolated", "status": "completed",
             "window_results": WINDOW_RESULTS},
            {"pass_id": "P2", "kind": "full_context", "context": "isolated", "status": "completed",
             "window_results": WINDOW_RESULTS},
        ],
        "full_context_review": {
            "status": "completed",
            "reason": "回查全部 114 轮，重点核对：T002-T009 的问答范围与 unless 例外；T014-T017 帖子方式既否定又有内推价值的让步；T025-T031 跨轮断裂的错过机会叙述；T052-T055 不相关职位条件；T066-T067 页面内嵌申请；T073 重复填写与自定义资料的让步；T092-T097 AI 识别与代写的区分；T100-T101 对 ideal update 的确认；T104-T111 状态与反馈；以及全文中反复出现的'不跳转别处'诉求。跨窗证据按实际窗口引用，补查片段另记 P2",
        },
        "entries": entries,
        "source_checks": source_checks,
    },
    "decisions": {
        "relations": relations,
        "groups": GROUPS,
        "questions": [{"target_type": t, "target_id": i, "message": m} for t, i, m in DECISION_QUESTIONS],
        "reassessments": [],
    },
}

# ---------------------------------------------------------------- integrity checks
all_gids = {g["candidate_id"] for g in goals}
all_cids = {c["candidate_id"] for c in raw_candidates}
for g in goals:
    if g["judgment"]["label"] in ("direct", "inferred"):
        assert g["judgment"]["unsupported_parts"] == [], "nonempty unsupported_parts on %s" % g["candidate_id"]
for e in entries:
    assert e["candidate_id"] in all_cids
    for gid in e["final_goal_ids"]:
        assert gid in all_gids, "unknown goal id " + gid
for r in relations:
    assert r["source_id"] in all_gids and r["target_id"] in all_gids
for g in GROUPS:
    assert g["parent_id"] in all_gids
    for c in g["child_ids"]:
        assert c in all_gids
for q in DECISION_QUESTIONS:
    if q[0] in ("goal", "group", "relation"):
        assert q[1] in all_gids or q[1] in {"GR1"} or q[1].startswith("R"), "bad target_id " + q[1]
for q in REVIEW_QUESTIONS:
    for cid in q[0]:
        assert cid in all_gids
assert len(WINDOW_IDS) == 56

out = HERE / "spec.json"
out.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("OK: %d raw candidates, %d goals, %d relations, %d groups, %d windows, %d entries, %d source_checks" %
      (len(raw_candidates), len(goals), len(relations), len(GROUPS), len(WINDOW_IDS), len(entries), len(source_checks)))
