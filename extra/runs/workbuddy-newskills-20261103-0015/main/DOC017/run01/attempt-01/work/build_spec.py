# -*- coding: utf-8 -*-
"""Build spec.json for DOC017-run01 with exact-quote verification."""
import json, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(BASE)
src = json.load(open(os.path.join(TASK, "source", "DOC017.json"), encoding="utf-8"))
TEXT = {t["source_id"]: t["text"] for t in src["turns"]}

def ev(sid, quote, role="basis"):
    assert sid in TEXT, sid
    assert quote in TEXT[sid], "QUOTE MISS in %s: %r" % (sid, quote[:60])
    assert TEXT[sid].count(quote) == 1, "AMBIGUOUS in %s: %r" % (sid, quote[:60])
    return {"source_id": sid, "quote": quote, "role": role}

def cand(cid, statement, modality, context, origin, evidence, pass_id="P1"):
    return {"candidate_id": cid, "statement": statement, "actor": "Stakeholder",
            "modality": modality, "context": context, "origin": origin,
            "pass_id": pass_id, "evidence": evidence}

raw = []
raw.append(cand("C001", "The stakeholder wants to receive job roles specific to his domain, such as software engineering or machine learning roles.",
    "wish ('would like to get')", ["domain-specific role targeting"], "explicit",
    [ev("DOC017:T003", "So I would like to get job roles specific to the domain such as software engineering or machine learning roles.")]))
raw.append(cand("C002", "The stakeholder wants job updates based on whatever his skill set is.",
    "wish ('would say', 'would be really great')", [], "explicit",
    [ev("DOC017:T003", "job updates based on whatever is my skill set. So that would be really great to have.")]))
raw.append(cand("C003", "The stakeholder wants to receive a job update at the instant a job is posted when he is actively looking, and accepts receiving updates once a week when he is not actively looking.",
    "conditional wish ('it would be great if ... or ... it's okay to')", ["depends on whether he is actively looking for a job", "stated premise: the market currently releases one or two jobs per day"], "explicit",
    [ev("DOC017:T005", "So it would be great if I receive at the instant. The job is like posted in the platform, or if I'm not looking actively, then it's okay to receive once in a week, right.")]))
raw.append(cand("C004", "The stakeholder generally prefers receiving job updates via professional email.",
    "preference ('would generally prefer', 'it'll be great')", [], "explicit",
    [ev("DOC017:T007", "I would generally prefer getting via emails. It'll be great if I get via professional emails.")]))
raw.append(cand("C005", "Mobile job notifications are acceptable to the stakeholder unless they are too complicated and fill up the notification tab on his phone.",
    "conditional acceptance ('would also be great unless')", ["mobile notification channel"], "explicit",
    [ev("DOC017:T007", "And yeah, job notifications would also be great unless it's like too complicated. And it's like filling all my notification tab in my mobile yeah.")]))
raw.append(cand("C006", "The job email should be concise and contain the necessary details that the stakeholder would otherwise look up on the platform.",
    "requirement ('should be very concise', 'should have')", ["email channel"], "explicit",
    [ev("DOC017:T009", "So the email should be very concise, right? It should have the necessary details which I kinda wanted to see in the platform")]))
raw.append(cand("C007", "The email should carry a direct apply button so the stakeholder does not have to navigate to the app and then to the company's portal to apply.",
    "requirement ('should be having')", ["email channel", "avoid navigation to app and company portal"], "explicit",
    [ev("DOC017:T009", "should be having a direct apply button in the email itself, so that I don't need to waste time then navigating to the app, and then again, going to the company's portal and applying right?")]))
raw.append(cand("C008", "The stakeholder currently opens LinkedIn, applies filters on roles, companies and location, and picks jobs from the returned list.",
    "current practice (fact)", [], "explicit",
    [ev("DOC017:T011", "I kind of go to the app filter based on my roles. And then companies what else? Location, etcetera. Right? So I apply all the filters.")]))
raw.append(cand("C009", "The stakeholder uses the platform's skill-set match percentage (above 50 or 60 percent) as the trigger to apply.",
    "decision rule ('I think I will apply')", [], "explicit",
    [ev("DOC017:T011", "Now, I think today, Linkedin has this skill set percentage more than 50% or more than 60%. I think I will apply for that job.")]))
raw.append(cand("C010", "Job posts by individuals on LinkedIn involve a long message, an interest check and a link sent later, so there is a lot of process and waiting time.",
    "complaint (fact + evaluation)", [], "explicit",
    [ev("DOC017:T013", "they kind of add a lot big message, and then they ask us whether they are interested, whether we are interested, and then they send us the link. So that is like a lot of process. And there's a lot of waiting time over there itself.")]))
raw.append(cand("C011", "LinkedIn posts are not helpful when the stakeholder wants to complete an application quickly.",
    "evaluation ('it's not helpful')", [], "explicit",
    [ev("DOC017:T015", "it's not helpful in terms of like, what is it? When it's when I want to do my up when I do want. When I want to do my application quickly right.")]))
raw.append(cand("C012", "LinkedIn posts do help the stakeholder connect with the person for a referral.",
    "positive evaluation ('it kind of helps me')", [], "explicit",
    [ev("DOC017:T017", "But in other ways it kind of helps me, because I kind of connect with the person some referral for the job.")]))
raw.append(cand("C013", "The stakeholder prioritizes role interest and suitability, then payment, then location, then company reputation when deciding to apply.",
    "self-described decision order", [], "explicit",
    [ev("DOC017:T019", "Okay, so one is the role like, I'll see if the role is really interesting. And I'm suitable for that role second is the payment. And then comes the location. And of course the company reputation.")]))
raw.append(cand("C014", "The stakeholder considers current-employee reviews, what work the team does, the tech stack, and how he would contribute as the most important job-posting information.",
    "importance ranking ('I would consider')", ["importance, not a hard requirement"], "explicit",
    [ev("DOC017:T021", "I would consider the reviews from the current employees. What work they are specifically working on, what text they are using. And how will I be contributing to their team right? Or to the company?")]))
raw.append(cand("C015", "The stakeholder wants job and tech-stack details formatted as lists, cards or tables so he can navigate to the actual details.",
    "wish ('would be really helpful')", [], "explicit",
    [ev("DOC017:T023", "But if it's kinda like, what is it formatted in terms of list cars and tables that would be really helpful for me to navigate and get the actual details about the tech stack or whatever it is.")]))
raw.append(cand("C016", "The stakeholder's earlier portal sent almost all jobs as notifications, its notification system was inaccurate, and few of the jobs were relevant to him.",
    "past negative experience (fact)", [], "explicit",
    [ev("DOC017:T025", "I think that time the portal they kind of spam lot of notification, I mean, the notification system was not that accurate? And it was sending almost like what? All the jobs right? So few of the jobs were not relevant to me.")]))
raw.append(cand("C017", "The stakeholder missed a few important jobs because of the inaccurate, spam-like notifications, and calls that a bad time.",
    "negative outcome ('I kind of missed', 'that was a bad time')", [], "explicit",
    [ev("DOC017:T027", "And with that I kind of missed few of the important jobs."),
     ev("DOC017:T029", "Apply. And that's that was a bad time. Yeah.")]))
raw.append(cand("C018", "For the stakeholder a job posting is relevant when it defines the necessary skill set he can compare against.",
    "relevance criterion", [], "explicit",
    [ev("DOC017:T033", "whenever I see a job posting, I see if there is a a skill set defined, necessary, skill set defined.")]))
raw.append(cand("C019", "The stakeholder uses a tool or plugin that matches his skill sets against a posting and returns a percentage.",
    "current practice + preference", [], "explicit",
    [ev("DOC017:T033", "I kind of use some tool out Plugin. I see if I can actually match those skill sets with me, and it can also give some percentage out of it.")]))
raw.append(cand("C020", "An AI assistant that tells the stakeholder a job is a good fit and he can apply supports his decision to apply.",
    "positive evaluation", [], "explicit",
    [ev("DOC017:T035", "this job is really like you can go for it. You can apply your perfect for this job.")]))
raw.append(cand("C021", "The stakeholder also weighs policies such as visa status and whether his experience makes him eligible to work.",
    "importance ('all comes up')", [], "explicit",
    [ev("DOC017:T037", "And then, of course, the other policies and stuff like visa, status, etcetera, or whether I'm eligible to work based on my experience. Right? So all comes up.")]))
raw.append(cand("C022", "The stakeholder wants his roles, past work, experience and skills already set from his profile, so that he does not need to add more filters to get a job list.",
    "wish + assumption ('I kinda assume that it's already set', 'I don't need to add any more filters')", [], "explicit",
    [ev("DOC017:T039", "I think I would actually have my roles defined. I mean, like, I will actually like, provide what are works I have done so far"),
     ev("DOC017:T039", "I kinda assume that it's already set right when it provides me the job list. and I don't need to add any more filters, right?")]))
raw.append(cand("C023", "The stakeholder wants to customize a few job-search keywords in his profile to get relevant results.",
    "wish ('customizing few keywords ... that will be great')", [], "explicit",
    [ev("DOC017:T041", "Also customizing few keywords for the job search to kind of get me the relevant result right?")]))
raw.append(cand("C024", "The stakeholder wants the keyword customization to live in his profile.",
    "wish ('that will be great')", [], "explicit",
    [ev("DOC017:T043", "That will be great to have a that will be great to customize in my profile.")]))
raw.append(cand("C025", "The stakeholder expects company HR staff who use the feature to find the perfect candidate to benefit from the job-update application.",
    "expectation about other beneficiaries", [], "explicit",
    [ev("DOC017:T047", "Of course, the company's Hr right. Whoever is using this feature to actually like get the perfect candidate for the role.")]))
raw.append(cand("C026", "The stakeholder expects job agencies to benefit from the job-update features.",
    "expectation about other beneficiaries", [], "explicit",
    [ev("DOC017:T049", "And of course, even the job agency said.")]))
raw.append(cand("C027", "The stakeholder summarizes that a few groups of people would benefit from job-update features.",
    "summary", [], "explicit",
    [ev("DOC017:T051", "So these are a few people, I think, would really benefit out of these job update features.")]))
raw.append(cand("C028", "Handshake lists irrelevant jobs because it does not collect much profile detail, which frustrates the stakeholder.",
    "complaint", ["Handshake as the named comparison platform"], "explicit",
    [ev("DOC017:T055", "I think we have this handshake portal where we don't provide much of our profess like profile details. and it lists like unrelevant jobs to us. And I kind of get frustrated with that.")]))
raw.append(cand("C029", "The stakeholder blacklists or marks jobs as uninterested and hopes they stop appearing.",
    "action + wish ('I hope that it doesn't come')", [], "explicit",
    [ev("DOC017:T057", "So I just like, sometimes I kind of blacklist those jobs. And yeah, I just remove those from. I just say that I'm uninterested. and I hope that it doesn't come.")]))
raw.append(cand("C030", "A huge list of jobs confuses the stakeholder about what to apply for.",
    "complaint", [], "explicit",
    [ev("DOC017:T059", "So that if the if there is giving me a huge list of jobs I'll get confused. What to apply for.")]))
raw.append(cand("C031", "Applying on LinkedIn navigates the stakeholder to another page, which is extra effort.",
    "complaint", [], "explicit",
    [ev("DOC017:T059", "whenever I go for a job application in Linkedin, right? It again navigates me to another page.")]))
raw.append(cand("C032", "The stakeholder sees no point in using LinkedIn if he still has to navigate elsewhere to apply.",
    "evaluation", [], "explicit",
    [ev("DOC017:T061", "So that's an extra efforts I should be putting from my end, and there is no point in having Linkedin. In the 1st place, when I have to like navigate to other place right.")]))
raw.append(cand("C033", "Each LinkedIn job carries a huge list of description, details and responsibilities that annoys the stakeholder and takes time; he wants separate UI for the description and for the responsibilities.",
    "complaint + wish ('if we can differentiate with the ui')", [], "explicit",
    [ev("DOC017:T065", "in Linkedin for each job there's a huge list of description, details, responsibilities, etc. which is kind of annoying right and time myself."),
     ev("DOC017:T065", "and also if it is, if we can differentiate with the ui like having separate ui for the description alone, and having separate for the responsibilities, etc.")]))
raw.append(cand("C034", "The stakeholder wants an integrated in-page view of the company's job portal so that he is more likely to apply.",
    "wish ('that would be really great to have integrated')", ["answer to the interviewer's question about an in-page view"], "explicit",
    [ev("DOC017:T066", "Would it be more likely to that you apply if you have an in page view of the company's specific job portal."),
     ev("DOC017:T067", "Yeah, that would be really great to have integrated right?")]))
raw.append(cand("C035", "The stakeholder wants all his details from the job portal already transferred to the company's website.",
    "preference ('I would also prefer')", [], "explicit",
    [ev("DOC017:T067", "And also, I would also prefer that all the details from my job portal is already like transferred to those reviews or Company's website. So that would be really great feature.")]))
raw.append(cand("C036", "Getting random job notifications is a reason the stakeholder might not want to use a job listing application.",
    "reason against using", [], "explicit",
    [ev("DOC017:T069", "Any reasons. Okay, one is getting random job notifications. Random people reaching me out in Linkedin or what there it is.")]))
raw.append(cand("C037", "Random people reaching out to the stakeholder on LinkedIn is a reason he might not want to use a job listing application.",
    "reason against using", [], "explicit",
    [ev("DOC017:T069", "Any reasons. Okay, one is getting random job notifications. Random people reaching me out in Linkedin or what there it is.")]))
raw.append(cand("C038", "The stakeholder does not want a list without relevant or updated jobs, will not apply to jobs that are a year or six months old, and will not proceed if postings are too old.",
    "rejection ('I don't want', 'I won't go ahead')", [], "explicit",
    [ev("DOC017:T071", "not having a relevant or updated job list. Right? I don't want to apply for jobs which are like one year back, or even 6 months back."),
     ev("DOC017:T071", "I won't go ahead with my application at all if those are like too old.")]))
raw.append(cand("C039", "Refilling all the details after uploading a resume is a hindrance for the stakeholder: a lot of manual effort that consumes time.",
    "complaint (hindrance)", [], "explicit",
    [ev("DOC017:T073", "Yeah, it's it's a hindrance for me to again fill all those details. Right? It's like a lot of manual effort. and it consumes a lot of time as well.")]))
raw.append(cand("C040", "The stakeholder sometimes wants to customize his details for a few specific job roles, and that is good, while not wanting a lot of manual effort in filling an application.",
    "concession ('sometimes I would like', 'in that way I think it's great. But again ...')", ["concession paired with the complaint about manual effort"], "explicit",
    [ev("DOC017:T073", "sometimes I I would like to kind of customize my details for few of the job roles right?"),
     ev("DOC017:T073", "I don't want to have a lot of manual efforts in filling up just a job application.")]))
raw.append(cand("C041", "The stakeholder currently notes the job id in a separate document or Notion and tracks it later in the week.",
    "current workaround (fact)", [], "explicit",
    [ev("DOC017:T075", "I just note down what the job id or whatever in a separate Doc, or something right? Maybe use notion, etc, right? And then maybe track in the later days of the week.")]))
raw.append(cand("C042", "The stakeholder wants such tracking features inside the job portal itself because he does not want to navigate to another application.",
    "wish ('It'd be great')", [], "explicit",
    [ev("DOC017:T077", "It'd be great to have such features in the job portal itself, because I again, as I said, I don't want to navigate to another application, right for just")]))
raw.append(cand("C043", "The stakeholder wants everything present in the job portal.",
    "wish ('It will be really great')", [], "explicit",
    [ev("DOC017:T079", "Simple purpose. Everything is present in the job portal. It will be really great right.")]))
raw.append(cand("C044", "The stakeholder finds LinkedIn's AI feature really great to have.",
    "positive evaluation", [], "explicit",
    [ev("DOC017:T081", "I would say the AI feature from Linkedin that is really great to have.")]))
raw.append(cand("C045", "Configured profile details persist in LinkedIn and the stakeholder does not want to change them again.",
    "maintain ('I don't wanna again change those')", [], "explicit",
    [ev("DOC017:T081", "If I configure my details in the Linkedin, it kind of persist. Right? I don't wanna again change those.")]))
raw.append(cand("C046", "The stakeholder does not want his applications exposed or people to know which job roles he is applying for; he wants everything private.",
    "rejection + wish ('it would be great to have everything private')", [], "explicit",
    [ev("DOC017:T083", "I don't want to. Expose my applications. Right. I don't want people to know for what job roles I'm applying for."),
     ev("DOC017:T083", "So it would be great to have everything private.")]))
raw.append(cand("C047", "The stakeholder does not want people to reach him from other platforms and does not want his data exposed by anyone apart from the platform.",
    "rejection ('I don't want')", [], "explicit",
    [ev("DOC017:T085", "And also I don't want to people reaching me out from other platforms, right? So I don't want my data to be exposed by other people apart from the platform.")]))
raw.append(cand("C048", "LinkedIn uses AI features that the stakeholder values, while Handshake is newer and lacks customization features.",
    "comparison", ["LinkedIn vs Handshake comparison"], "explicit",
    [ev("DOC017:T087", "So Linkedin kind of uses AI features, which is really great. And if I see handshake is kind of new right? And there are a lot of even the customization features are missing.")]))
raw.append(cand("C049", "On Handshake the stakeholder cannot state more details about work experience or schooling, and because of that people reach out for irrelevant roles.",
    "complaint + causal claim", ["Handshake as the named platform"], "explicit",
    [ev("DOC017:T089", "You can't tell more details about your work experience, or your schooling and stuff. And because of that, I think people reach you out for irrelevant roles.")]))
raw.append(cand("C050", "LinkedIn's back-end algorithm finds the stakeholder's interest, matches his skill set and returns the necessary roles.",
    "positive evaluation of mechanism", [], "explicit",
    [ev("DOC017:T091", "In case of linkedin it kind of list, you relevant tools. Right? It does some algorithm in the back. And it just finds your interest and matches with your skill set and gets you the necessary roles.")]))
raw.append(cand("C051", "The stakeholder agrees it would be great for AI to identify jobs.",
    "agreement ('Of course it will be great')", [], "explicit",
    [ev("DOC017:T093", "Of course it will be great to actually identify jobs. but when it comes for writing applications, I think I kind of still feel that Eas are uncertain, right? They are not reliable.")]))
raw.append(cand("C052", "The stakeholder finds AI unreliable for writing applications and keeps that as a doubt.",
    "doubt ('uncertain', 'not reliable')", ["writing applications, as opposed to identifying jobs"], "explicit",
    [ev("DOC017:T093", "when it comes for writing applications, I think I kind of still feel that Eas are uncertain, right? They are not reliable.")]))
raw.append(cand("C053", "AI-written application content would be acceptable if verified by the stakeholder, but it should not be automatic.",
    "condition ('if it is like verified by us, then it's good. But ... it shouldn't be automatic')", [], "explicit",
    [ev("DOC017:T095", "So, of course, if it is like verified by us, then it's good. But yeah, but it shouldn't be automatic.")]))
raw.append(cand("C054", "The stakeholder's ideal job update matches his criteria, fits his skill sets, and offers a quick apply button.",
    "wish ('it will be like, great')", [], "explicit",
    [ev("DOC017:T099", "okay, if it's kind of matching with my criteria. One is that. And if the skill sets okay, if there is a quick, apply button right? Then it will be like, great yeah.")]))
raw.append(cand("C055", "The stakeholder rates seeing application status as 10 out of 10 in importance and wants to know the status of his application.",
    "importance 10/10", [], "explicit",
    [ev("DOC017:T105", "I would say 10 right? I mean I want to know what is my status of my application?")]))
raw.append(cand("C056", "The stakeholder would value employer feedback so that he can improve his further applications.",
    "wish ('would be really great')", [], "explicit",
    [ev("DOC017:T105", "And of course, if there is any feedback that would be really great for me to improve in my further applications.")]))
raw.append(cand("C057", "Most job portals and companies do not provide proper feedback, which the stakeholder finds tough.",
    "complaint", [], "explicit",
    [ev("DOC017:T107", "Today. I think most of the job portals or any company, even companies. Job portals right? They don't like provide proper feedbacks.")]))
raw.append(cand("C058", "Even after applying, the stakeholder finds it uncertain whether he will get an interview call.",
    "concern", [], "explicit",
    [ev("DOC017:T109", "Even if I apply today I might get it's uncertain that I'll get what to say. Interview, call.")]))
raw.append(cand("C059", "The stakeholder wants to track the status of his applications.",
    "wish ('It would be great if I can track')", [], "explicit",
    [ev("DOC017:T111", "It would be great if I can track those status.")]))

goals = []
def goal(gid, statement, context, origin, evidence, label, rationale, inference=None, supported_parts=None):
    goals.append({
        "candidate_id": gid, "statement": statement, "actor": "Stakeholder",
        "context": context, "origin": origin, "inference": inference,
        "evidence": evidence,
        "judgment": {"label": label, "rationale": rationale,
                     "supported_parts": supported_parts or [],
                     "unsupported_parts": [], "assumptions": [], "reasoning_steps": []},
    })

goal("G001", "Receive job roles that are specific to my domain, such as software engineering or machine learning roles.",
     ["domain-specific role targeting"], "explicit",
     [ev("DOC017:T003", "So I would like to get job roles specific to the domain such as software engineering or machine learning roles.")],
     "direct", "受访者明确说想要特定领域（软件工程或机器学习）的岗位，主体、对象与范围逐字对应，无强度或条件差异。")

goal("G002", "Receive job updates matched to my own skill set.",
     ["match is judged against the stakeholder's own skills, not a generic profile"], "explicit",
     [ev("DOC017:T003", "job updates based on whatever is my skill set. So that would be really great to have."),
      ev("DOC017:T033", "whenever I see a job posting, I see if there is a a skill set defined, necessary, skill set defined.")],
     "direct", "原文两处以技能集为条件：T003 说更新应依据技能集，T033 说判断相关性要看岗位是否列出必备技能；主体与结果一致。")

goal("G003", "Receive a job-posting update immediately when a job is posted while I am actively looking for a job, and accept only weekly updates when I am not actively looking.",
     ["frequency depends on whether the stakeholder is actively job hunting",
      "stated premise: the market currently releases one or two jobs per day"], "explicit",
     [ev("DOC017:T005", "So it would be great if I receive at the instant. The job is like posted in the platform, or if I'm not looking actively, then it's okay to receive once in a week, right.")],
     "direct", "原文一句话给出两档频率并各自绑定条件（积极求职→发布即收到；不积极→每周一次可接受），目标保留该条件分支，未把任一档写成无条件要求，也未把“once in a week”强化为上限。")

goal("G004", "Receive job updates by professional email as my generally preferred channel.",
     ["preference, not an exclusive channel"], "explicit",
     [ev("DOC017:T007", "I would generally prefer getting via emails. It'll be great if I get via professional emails.")],
     "direct", "原文用 generally prefer 与 it'll be great，属偏好强度；目标保留 prefer 语气，不写成必须或唯一渠道。")

goal("G005", "Keep mobile job notifications from becoming too complicated or filling up the phone's notification tab.",
     ["mobile notifications are acceptable to the stakeholder only up to that limit"], "explicit",
     [ev("DOC017:T007", "And yeah, job notifications would also be great unless it's like too complicated. And it's like filling all my notification tab in my mobile yeah.")],
     "direct", "原文以 unless 给出移动通知的可接受上限（不要太复杂、不要占满通知栏）；目标是该上限本身，未推出禁止移动通知。")

goal("G006", "Receive a concise job email that already contains the necessary job details I would otherwise look up on the platform.",
     ["email channel"], "explicit",
     [ev("DOC017:T009", "So the email should be very concise, right? It should have the necessary details which I kinda wanted to see in the platform")],
     "direct", "原文对邮件同时要求 concise 与 necessary details，二者共同限定同一封邮件的内容，故合为一个目标而非拆成两条语句。")

goal("G007", "Apply to the job directly from the email through an apply button, without navigating to the app or to the company's portal.",
     ["email channel", "the stated reason is to avoid wasted time navigating"], "explicit",
     [ev("DOC017:T009", "should be having a direct apply button in the email itself, so that I don't need to waste time then navigating to the app, and then again, going to the company's portal and applying right?")],
     "direct", "原文明确要求邮件内自带直接申请按钮，并说明要避免先到应用、再到公司门户的两段导航；方式与要避免的结果均保留。")

goal("G008", "See current-employee reviews, the work the team is doing, the tech stack, and how I would contribute when I look at a job posting.",
     ["the stakeholder ranked this as the most important posting information, not as a hard requirement"], "explicit",
     [ev("DOC017:T021", "I would consider the reviews from the current employees. What work they are specifically working on, what text they are using. And how will I be contributing to their team right? Or to the company?")],
     "direct", "答“什么岗位信息最重要”时逐项列出员工评价、团队在做什么、技术栈与自身贡献方式；四项同属一次评估动作，故保留为一个目标下的并列信息。“what text they are using”按 T023 的 tech stack 语境理解为技术栈，属识别疑点，未改写原文。")

goal("G009", "See job and tech-stack details laid out in list, card or table formats rather than in long message text.",
     ["refers to the posting's detail and tech-stack information"], "explicit",
     [ev("DOC017:T023", "But if it's kinda like, what is it formatted in terms of list cars and tables that would be really helpful for me to navigate and get the actual details about the tech stack or whatever it is.")],
     "direct", "原文以“list cars and tables”（cards 的口语/识别变体）作为期望排版，并说明目的是便于导航到技术栈等实际细节；方式明确，未改成必须同时使用三种排版。")

goal("G010", "See the job description and the job responsibilities in separate UI sections.",
     ["same posting page"], "explicit",
     [ev("DOC017:T065", "and also if it is, if we can differentiate with the ui like having separate ui for the description alone, and having separate for the responsibilities, etc.")],
     "direct", "原文明确要求描述与职责各有独立 UI 区块；这与 G009 的列表/卡片排版是不同验收维度，故未合并。")

goal("G011", "Avoid missing important job opportunities because of notification noise.",
     ["inferred from a reported past miss attributed to inaccurate, spam-like notifications"], "inferred",
     [ev("DOC017:T027", "And with that I kind of missed few of the important jobs."),
      ev("DOC017:T029", "Apply. And that's that was a bad time. Yeah.")],
     "inferred", "受访者未直接说“不要错过”，但陈述了因通知不准而错过重要岗位、并称“that was a bad time”，属明确的负面结果与厌恶；据此推断避免该结果的意愿，并假设该意愿适用于新应用的通知设计。",
     inference={"basis_candidate_ids": ["G012"],
                "reason": "通知系统把几乎所有岗位都推送、相关性不足，受访者由此错过重要岗位；避免错过是其对该因果的负面反应。",
                "assumptions": ["受访者会以“是否错过重要岗位”评价通知设计", "该厌恶可迁移到新的岗位更新应用"]},
     supported_parts=["错过重要岗位的负面结果", "原因指向通知噪音与不准确"])

goal("G012", "Receive notifications only for jobs that are relevant to me, not for almost every job on the platform.",
     ["relevance is defined by the stakeholder's skill set and profile"], "explicit",
     [ev("DOC017:T025", "I think that time the portal they kind of spam lot of notification, I mean, the notification system was not that accurate? And it was sending almost like what? All the jobs right? So few of the jobs were not relevant to me."),
      ev("DOC017:T069", "Any reasons. Okay, one is getting random job notifications. Random people reaching me out in Linkedin or what there it is.")],
     "direct", "原文把“几乎所有岗位都推送、只有少数相关”作为问题，并在“不愿使用的理由”中列出 random job notifications；相关性与排除无关通知两点均有直接表述。")

goal("G013", "See a percentage showing how well my skill set matches a job posting.",
     ["match percentage is used as an apply/no-apply signal"], "explicit",
     [ev("DOC017:T033", "I kind of use some tool out Plugin. I see if I can actually match those skill sets with me, and it can also give some percentage out of it."),
      ev("DOC017:T011", "Now, I think today, Linkedin has this skill set percentage more than 50% or more than 60%. I think I will apply for that job.")],
     "direct", "T033 明确说工具可给出匹配百分比，T011 说明他以 50%/60% 以上的百分比作为申请判断；目标只保留“看到百分比”，未把阈值写成系统规则。")

goal("G014", "See eligibility information, such as visa status and whether my experience qualifies me, when I look at a job posting.",
     ["ranked among the important posting information"], "explicit",
     [ev("DOC017:T037", "And then, of course, the other policies and stuff like visa, status, etcetera, or whether I'm eligible to work based on my experience. Right? So all comes up.")],
     "direct", "原文在“重要信息”回答中列出签证/身份与基于经验的工作资格；属信息呈现要求，强度按 importance 保留，未升级为硬性门槛。")

goal("G015", "Get a job list already filtered from my profile (roles, experience, skills, projects), so that I do not have to add more filters.",
     ["profile is assumed to be pre-filled by the stakeholder"], "explicit",
     [ev("DOC017:T039", "I think I would actually have my roles defined. I mean, like, I will actually like, provide what are works I have done so far"),
      ev("DOC017:T039", "I kinda assume that it's already set right when it provides me the job list. and I don't need to add any more filters, right?")],
     "direct", "原文说档案里会有角色与过往工作，并假设列表给出时筛选已设好、无需再加过滤条件；这是“省去重复筛选”的结果，未扩展为自动投递。")

goal("G016", "Customize job-search keywords in my profile to get relevant results.",
     ["keywords are stored at profile level"], "explicit",
     [ev("DOC017:T041", "Also customizing few keywords for the job search to kind of get me the relevant result right?"),
      ev("DOC017:T043", "That will be great to have a that will be great to customize in my profile.")],
     "direct", "T041 提出定制少量关键词以获得相关结果，T043 明确希望定制放在档案中；两处同指一个定制动作，故合并。")

goal("G017", "Mark a job posting as uninterested or blacklisted so that it stops appearing.",
     ["applies to postings judged irrelevant"], "explicit",
     [ev("DOC017:T057", "So I just like, sometimes I kind of blacklist those jobs. And yeah, I just remove those from. I just say that I'm uninterested. and I hope that it doesn't come.")],
     "direct", "原文描述了标记/移除动作，并明确希望该岗位不再出现；动作与预期结果均在句内。")

goal("G018", "See only current job postings, not listings that are six months to a year old.",
     ["the stakeholder gives six months and one year as spoken examples of 'too old', not a single threshold"], "explicit",
     [ev("DOC017:T071", "not having a relevant or updated job list. Right? I don't want to apply for jobs which are like one year back, or even 6 months back."),
      ev("DOC017:T071", "I won't go ahead with my application at all if those are like too old.")],
     "direct", "原文明确不接受一年前或六个月前的岗位，并说太旧就不会申请；目标保留口语区间，未擅自给出统一阈值。")

goal("G019", "Apply to a job inside the application through an in-page view of the company's job portal.",
     ["the interviewer's question framed this as an in-page view of the company portal"], "explicit",
     [ev("DOC017:T066", "Would it be more likely to that you apply if you have an in page view of the company's specific job portal."),
      ev("DOC017:T067", "Yeah, that would be really great to have integrated right?")],
     "direct", "答句“that would be really great to have integrated”直接回应站内嵌公司门户的申请方式；主体为求职者申请人，方式（in-page view）保留在目标中。")

goal("G020", "Have my profile and application details carried over to the employer's site so that I do not re-enter them manually.",
     ["applies to applications that continue on a company site"], "explicit",
     [ev("DOC017:T067", "And also, I would also prefer that all the details from my job portal is already like transferred to those reviews or Company's website. So that would be really great feature."),
      ev("DOC017:T073", "Yeah, it's it's a hindrance for me to again fill all those details. Right? It's like a lot of manual effort. and it consumes a lot of time as well.")],
     "direct", "T067 要求把门户里的资料转到公司网站，T073 抱怨上传简历后仍要重填全部信息；两处同指“不重复录入”，故合并，并保留“转到雇主站点”的适用范围。")

goal("G021", "Keep the ability to customize my details for a specific job role when I apply.",
     ["concession that qualifies automatic reuse of details"], "explicit",
     [ev("DOC017:T073", "sometimes I I would like to kind of customize my details for few of the job roles right?"),
      ev("DOC017:T073", "I don't want to have a lot of manual efforts in filling up just a job application.")],
     "direct", "原文在抱怨重填之后作出让步：有时想针对个别岗位定制细节。该让步与 G020 的自动化并非矛盾，故单列为保留型目标。")

goal("G022", "Save job postings of interest and track them later inside the job portal, without switching to another application such as Notion.",
     ["the current workaround is noting job ids in a separate document or Notion"], "explicit",
     [ev("DOC017:T077", "It'd be great to have such features in the job portal itself, because I again, as I said, I don't want to navigate to another application, right for just"),
      ev("DOC017:T079", "Simple purpose. Everything is present in the job portal. It will be really great right.")],
     "direct", "T075 说明现状是记到外部文档/Notion 并在几天后跟踪，T077/T079 要求在门户内提供同类功能且不再跳转；保存与后续跟踪属同一动作链，合为一个目标。")

goal("G023", "Keep my configured profile details persistent so that I do not have to enter them again.",
     ["reported as a valued behaviour of the current platform"], "explicit",
     [ev("DOC017:T081", "If I configure my details in the Linkedin, it kind of persist. Right? I don't wanna again change those.")],
     "direct", "原文把“配置一次即保持”列为喜欢的特性并说不想再改；属维持型目标，依据是正面的现状评价而非既有功能自动成为要求。")

goal("G024", "Use AI features to identify and match relevant jobs.",
     ["limited to identification and matching, not to writing applications"], "explicit",
     [ev("DOC017:T081", "I would say the AI feature from Linkedin that is really great to have."),
      ev("DOC017:T093", "Of course it will be great to actually identify jobs. but when it comes for writing applications, I think I kind of still feel that Eas are uncertain, right? They are not reliable.")],
     "direct", "原文称 LinkedIn 的 AI 特性“really great to have”，并把 AI 的价值限定在 identify jobs；范围（识别/匹配）来自 T093 的对比句。")

goal("G025", "Keep application writing non-automatic, with any AI-written content used only after I verify it.",
     ["contrast between AI for identification (accepted) and AI for writing (conditional)"], "explicit",
     [ev("DOC017:T093", "when it comes for writing applications, I think I kind of still feel that Eas are uncertain, right? They are not reliable."),
      ev("DOC017:T095", "So, of course, if it is like verified by us, then it's good. But yeah, but it shouldn't be automatic.")],
     "direct", "原文先说 AI 代写不可靠，再给出条件：经本人核验可以，但不得自动；两个限定都指向同一动作（代写申请），故保留为一个目标。")

goal("G026", "Keep my job applications private so that other people cannot see which roles I am applying for.",
     ["motivated by competition in the job market"], "explicit",
     [ev("DOC017:T083", "I don't want to. Expose my applications. Right. I don't want people to know for what job roles I'm applying for."),
      ev("DOC017:T083", "So it would be great to have everything private.")],
     "direct", "原文两次否定“暴露申请/让人知道申请哪些岗位”，并以“everything private”收束；对象与范围一致。")

goal("G027", "Keep my data inside the platform so that people cannot reach me or use my data from other platforms.",
     ["applies to contact and data use outside the platform"], "explicit",
     [ev("DOC017:T085", "And also I don't want to people reaching me out from other platforms, right? So I don't want my data to be exposed by other people apart from the platform.")],
     "direct", "原文把“不要被其他平台的人联系”与“数据不得被平台之外的人暴露”并列陈述，指向同一数据边界；合为一个目标，未扩展到平台内部的可见性（那是 G026）。")

goal("G028", "See the current status of each application I have submitted.",
     ["rated 10 out of 10 in importance"], "explicit",
     [ev("DOC017:T105", "I would say 10 right? I mean I want to know what is my status of my application?"),
      ev("DOC017:T111", "It would be great if I can track those status.")],
     "direct", "T105 给出 10/10 的重要性并说想了解申请状态，T111 再次要求跟踪状态；同一动作的两处表述，合并。")

goal("G029", "Receive employer feedback on my applications so that I can improve my further applications.",
     ["feedback is wanted for improving later applications"], "explicit",
     [ev("DOC017:T105", "And of course, if there is any feedback that would be really great for me to improve in my further applications."),
      ev("DOC017:T107", "Today. I think most of the job portals or any company, even companies. Job portals right? They don't like provide proper feedbacks.")],
     "direct", "原文明确希望得到反馈并说明目的是改进后续申请；T107 的现状抱怨作背景，单独成句但指向同一反馈缺口，未另造目标。")

goal("G030", "Have a quick apply button on job postings in the portal.",
     ["portal listing channel, distinct from the email apply button in G007"], "explicit",
     [ev("DOC017:T099", "okay, if it's kind of matching with my criteria. One is that. And if the skill sets okay, if there is a quick, apply button right? Then it will be like, great yeah.")],
     "direct", "原文把“quick apply button”作为理想更新的组成部分；与 G007 的邮件内按钮分属不同渠道，故未合并。")

WINDOWS = [w["window_id"] for w in json.load(open(os.path.join(TASK, "work", "source-windows.json"), encoding="utf-8"))["windows"]]
assert len(WINDOWS) == 56

passes = [{"pass_id": "P1", "kind": "initial", "context": "isolated", "status": "completed",
           "window_results": [{"window_id": w, "status": "processed", "reason": ""} for w in WINDOWS]}]

entries = [
 {"candidate_id": "C001", "disposition": "keep", "final_goal_ids": ["G001"], "reason": "原文直接表达，动作与范围一致。"},
 {"candidate_id": "C002", "disposition": "keep", "final_goal_ids": ["G002"], "reason": "技能集条件为原文明确表述。"},
 {"candidate_id": "C003", "disposition": "keep", "final_goal_ids": ["G003"], "reason": "两档频率及各自条件均保留在目标正文。"},
 {"candidate_id": "C004", "disposition": "keep", "final_goal_ids": ["G004"], "reason": "偏好强度保留，未升级为必须。"},
 {"candidate_id": "C005", "disposition": "keep", "final_goal_ids": ["G005"], "reason": "unless 条件即目标内容，未推出禁止移动通知。"},
 {"candidate_id": "C006", "disposition": "keep", "final_goal_ids": ["G006"], "reason": "邮件内容要求单列，与申请按钮目标分开。"},
 {"candidate_id": "C007", "disposition": "keep", "final_goal_ids": ["G007"], "reason": "邮件内直接申请方式与避免导航的结果均保留。"},
 {"candidate_id": "C008", "disposition": "exclude", "final_goal_ids": [], "reason": "现状流程描述（打开 LinkedIn 逐项筛选），无期望结果，仅作背景；作为 G015 的反衬背景记录在案。"},
 {"candidate_id": "C009", "disposition": "merge", "final_goal_ids": ["G013"], "reason": "与 C019 同指匹配百分比，只保留“看到百分比”，阈值不写入目标。"},
 {"candidate_id": "C010", "disposition": "exclude", "final_goal_ids": [], "reason": "对帖子渠道过程的描述与等待抱怨，未提出独立期望结果；与“减少跳转”类目标同源，不另建。"},
 {"candidate_id": "C011", "disposition": "exclude", "final_goal_ids": [], "reason": "仅评价帖子渠道不利于快速申请，属背景障碍线索，不成目标。"},
 {"candidate_id": "C012", "disposition": "exclude", "final_goal_ids": [], "reason": "帖子带来人脉/内推的正面评价，未表达对新应用的维持要求，保留为背景以免误删。"},
 {"candidate_id": "C013", "disposition": "exclude", "final_goal_ids": [], "reason": "受访者自述申请决策的考虑顺序，未要求系统按此排序或展示，故不造排序目标。"},
 {"candidate_id": "C014", "disposition": "keep", "final_goal_ids": ["G008"], "reason": "四项信息同属一次评估动作，按 importance 强度保留。"},
 {"candidate_id": "C015", "disposition": "keep", "final_goal_ids": ["G009"], "reason": "排版方式明确（list/cards/tables），保留为方式约束。"},
 {"candidate_id": "C016", "disposition": "keep", "final_goal_ids": ["G012"], "reason": "“推送几乎所有岗位、多数不相关”为相关性目标的主依据。"},
 {"candidate_id": "C017", "disposition": "keep", "final_goal_ids": ["G011"], "reason": "错过重要岗位及其负面评价支持避免型目标（inferred）。"},
 {"candidate_id": "C018", "disposition": "merge", "final_goal_ids": ["G002"], "reason": "以岗位必备技能作为比对前提，与技能集匹配同义。"},
 {"candidate_id": "C019", "disposition": "keep", "final_goal_ids": ["G013"], "reason": "百分比展示的主依据。"},
 {"candidate_id": "C020", "disposition": "merge", "final_goal_ids": ["G024"], "reason": "AI 判断“适合申请”属识别/匹配用途，归入 AI 识别目标。"},
 {"candidate_id": "C021", "disposition": "keep", "final_goal_ids": ["G014"], "reason": "签证/经验资格信息单列，不与技能匹配混同。"},
 {"candidate_id": "C022", "disposition": "keep", "final_goal_ids": ["G015"], "reason": "档案预筛、免加过滤器的要求完整保留。"},
 {"candidate_id": "C023", "disposition": "keep", "final_goal_ids": ["G016"], "reason": "关键词定制的独立要求。"},
 {"candidate_id": "C024", "disposition": "merge", "final_goal_ids": ["G016"], "reason": "同一关键词定制，仅补充“放在档案中”的位置。"},
 {"candidate_id": "C025", "disposition": "exclude", "final_goal_ids": [], "reason": "谈其他受益方（公司 HR），非受访者自身目标，也无系统要求。"},
 {"candidate_id": "C026", "disposition": "exclude", "final_goal_ids": [], "reason": "同上，招聘中介受益，属背景。"},
 {"candidate_id": "C027", "disposition": "exclude", "final_goal_ids": [], "reason": "对上述受益方的概括，无新增意图。"},
 {"candidate_id": "C028", "disposition": "merge", "final_goal_ids": ["G012"], "reason": "Handshake 推送不相关岗位是其相关性要求的反面证据。"},
 {"candidate_id": "C029", "disposition": "keep", "final_goal_ids": ["G017"], "reason": "标记/拉黑并要求不再出现的动作与结果均在原文。"},
 {"candidate_id": "C030", "disposition": "exclude", "final_goal_ids": [], "reason": "“列表太大导致困惑”是抱怨，未提出列表规模或排序要求；不把抱怨直接当需求。"},
 {"candidate_id": "C031", "disposition": "exclude", "final_goal_ids": [], "reason": "申请跳转到其他页面属障碍线索，已由 G007/G019 承接减少跳转的意图，不重复建点。"},
 {"candidate_id": "C032", "disposition": "exclude", "final_goal_ids": [], "reason": "对现有平台价值的评价句，与 C031 同源，不另立目标。"},
 {"candidate_id": "C033", "disposition": "keep", "final_goal_ids": ["G010"], "reason": "描述与职责分区为明确的 UI 要求；冗长抱怨作背景。"},
 {"candidate_id": "C034", "disposition": "keep", "final_goal_ids": ["G019"], "reason": "站内嵌公司门户申请，含问句语境一并引用。"},
 {"candidate_id": "C035", "disposition": "keep", "final_goal_ids": ["G020"], "reason": "资料转移到公司网站的主依据。"},
 {"candidate_id": "C036", "disposition": "merge", "final_goal_ids": ["G012"], "reason": "“随机岗位通知”与相关性要求同指一事。"},
 {"candidate_id": "C037", "disposition": "keep", "final_goal_ids": ["G027"], "reason": "被外部平台陌生人联系，属数据边界目标的一部分。"},
 {"candidate_id": "C038", "disposition": "keep", "final_goal_ids": ["G018"], "reason": "拒绝过期岗位，保留六个月/一年的口语区间。"},
 {"candidate_id": "C039", "disposition": "merge", "final_goal_ids": ["G020"], "reason": "重填资料的抱怨与 T067 的资料转移同指免除重复录入。"},
 {"candidate_id": "C040", "disposition": "keep", "final_goal_ids": ["G021"], "reason": "让步句单列为保留型目标，避免自动化吞掉按岗位定制。"},
 {"candidate_id": "C041", "disposition": "exclude", "final_goal_ids": [], "reason": "现状做法（记到 Doc/Notion 再跟踪），非期望结果；仅作 G022 的需要背景。"},
 {"candidate_id": "C042", "disposition": "keep", "final_goal_ids": ["G022"], "reason": "要求在门户内提供保存/跟踪，且不再跳转其他应用。"},
 {"candidate_id": "C043", "disposition": "merge", "final_goal_ids": ["G022"], "reason": "“一切都在门户内”是同一要求的概括。"},
 {"candidate_id": "C044", "disposition": "keep", "final_goal_ids": ["G024"], "reason": "对 AI 特性的正面评价，支持以 AI 识别岗位。"},
 {"candidate_id": "C045", "disposition": "keep", "final_goal_ids": ["G023"], "reason": "档案配置持久化的维持型目标。"},
 {"candidate_id": "C046", "disposition": "keep", "final_goal_ids": ["G026"], "reason": "申请保密与不暴露申请岗位。"},
 {"candidate_id": "C047", "disposition": "keep", "final_goal_ids": ["G027"], "reason": "平台外联系与数据暴露的合并要求。"},
 {"candidate_id": "C048", "disposition": "exclude", "final_goal_ids": [], "reason": "LinkedIn 与 Handshake 的功能比较，属背景；AI 与定制两项已分别由 G024、G016 承接。"},
 {"candidate_id": "C049", "disposition": "merge", "final_goal_ids": ["G002"], "reason": "档案信息不足导致不相关触达，属技能/档案匹配的反面证据。"},
 {"candidate_id": "C050", "disposition": "merge", "final_goal_ids": ["G024"], "reason": "算法按兴趣与技能匹配岗位，属 AI 识别的机制描述。"},
 {"candidate_id": "C051", "disposition": "merge", "final_goal_ids": ["G024"], "reason": "“AI 识别岗位会很好”与 C044 同义。"},
 {"candidate_id": "C052", "disposition": "keep", "final_goal_ids": ["G025"], "reason": "AI 代写不可靠，是代写限制的主依据。"},
 {"candidate_id": "C053", "disposition": "merge", "final_goal_ids": ["G025"], "reason": "本人核验后方可使用、且不得自动，属同一代写条件。"},
 {"candidate_id": "C054", "disposition": "split", "final_goal_ids": ["G030", "G002"], "reason": "该句含两个可独立满足的结果：快速申请按钮（G030）与按条件/技能匹配（并入 G002）；分别保留，未把 AND 变 OR。"},
 {"candidate_id": "C055", "disposition": "keep", "final_goal_ids": ["G028"], "reason": "10/10 重要性并要求知道申请状态。"},
 {"candidate_id": "C056", "disposition": "keep", "final_goal_ids": ["G029"], "reason": "希望反馈以改进后续申请，目的明确。"},
 {"candidate_id": "C057", "disposition": "merge", "final_goal_ids": ["G029"], "reason": "门户不给反馈的现状抱怨，指向同一反馈缺口。"},
 {"candidate_id": "C058", "disposition": "exclude", "final_goal_ids": [], "reason": "对是否能获面试的不确定感，是情绪/顾虑而非新要求；作为 G028 的背景，不升级为目标。"},
 {"candidate_id": "C059", "disposition": "merge", "final_goal_ids": ["G028"], "reason": "再次要求跟踪状态，与 C055 同义。"},
]

source_checks = [
 {"check_id": "S1", "evidence_candidates": [
     {"source_id": "DOC017:T025", "quote": "I think that time the portal they kind of spam lot of notification, I mean, the notification system was not that accurate? And it was sending almost like what? All the jobs right? So few of the jobs were not relevant to me."},
     {"source_id": "DOC017:T055", "quote": "I think we have this handshake portal where we don't provide much of our profess like profile details. and it lists like unrelevant jobs to us. And I kind of get frustrated with that."},
     {"source_id": "DOC017:T069", "quote": "Any reasons. Okay, one is getting random job notifications. Random people reaching me out in Linkedin or what there it is."}],
  "candidate_ids": ["C016", "C028", "C036"], "final_goal_ids": ["G012"], "outcome": "represented",
  "reason": "三处不同平台/情境的相关性抱怨合并到一个目标，条件（技能与档案）与“只推相关岗位”均保留。"},
 {"check_id": "S2", "evidence_candidates": [
     {"source_id": "DOC017:T027", "quote": "And with that I kind of missed few of the important jobs."},
     {"source_id": "DOC017:T029", "quote": "Apply. And that's that was a bad time. Yeah."}],
  "candidate_ids": ["C017"], "final_goal_ids": ["G011"], "outcome": "represented",
  "reason": "因果（噪音→错过）与负面评价保留在 inferred 目标及其推断说明中。"},
 {"check_id": "S3", "evidence_candidates": [
     {"source_id": "DOC017:T019", "quote": "Okay, so one is the role like, I'll see if the role is really interesting. And I'm suitable for that role second is the payment. And then comes the location. And of course the company reputation."}],
  "candidate_ids": ["C013"], "final_goal_ids": [], "outcome": "excluded",
  "reason": "个人决策顺序，未要求系统实现排序或权重；排除理由为“非系统要求”，不是“出现少”。"},
 {"check_id": "S4", "evidence_candidates": [
     {"source_id": "DOC017:T059", "quote": "So that if the if there is giving me a huge list of jobs I'll get confused. What to apply for."}],
  "candidate_ids": ["C030"], "final_goal_ids": [], "outcome": "excluded",
  "reason": "仅为大列表带来的困惑，未提出列表规模、排序或筛选要求；避免把抱怨直接升级为需求。"},
 {"check_id": "S5", "evidence_candidates": [
     {"source_id": "DOC017:T013", "quote": "they kind of add a lot big message, and then they ask us whether they are interested, whether we are interested, and then they send us the link. So that is like a lot of process. And there's a lot of waiting time over there itself."},
     {"source_id": "DOC017:T015", "quote": "it's not helpful in terms of like, what is it? When it's when I want to do my up when I do want. When I want to do my application quickly right."},
     {"source_id": "DOC017:T017", "quote": "But in other ways it kind of helps me, because I kind of connect with the person some referral for the job."}],
  "candidate_ids": ["C010", "C011", "C012"], "final_goal_ids": [], "outcome": "excluded",
  "reason": "帖子渠道的利弊评价，无独立期望结果；内推价值被保留在记录中，避免因无关被静默删除。"},
 {"check_id": "S6", "evidence_candidates": [
     {"source_id": "DOC017:T075", "quote": "I just note down what the job id or whatever in a separate Doc, or something right? Maybe use notion, etc, right? And then maybe track in the later days of the week."}],
  "candidate_ids": ["C041"], "final_goal_ids": [], "outcome": "excluded",
  "reason": "现状做法，不是期望；G022 的意图依据来自 T077/T079，未用现状冒充要求。"},
 {"check_id": "S7", "evidence_candidates": [
     {"source_id": "DOC017:T099", "quote": "okay, if it's kind of matching with my criteria. One is that. And if the skill sets okay, if there is a quick, apply button right? Then it will be like, great yeah."}],
  "candidate_ids": ["C054"], "final_goal_ids": ["G030", "G002"], "outcome": "represented",
  "reason": "复合句按两个可独立满足的结果拆分，拆分映射与理由记录在 entries。"},
 {"check_id": "S8", "evidence_candidates": [
     {"source_id": "DOC017:T093", "quote": "when it comes for writing applications, I think I kind of still feel that Eas are uncertain, right? They are not reliable."},
     {"source_id": "DOC017:T095", "quote": "So, of course, if it is like verified by us, then it's good. But yeah, but it shouldn't be automatic."}],
  "candidate_ids": ["C052", "C053"], "final_goal_ids": ["G025"], "outcome": "represented",
  "reason": "识别与代写的分工、以及“可核验但不得自动”的条件均进入目标，未把 AI 代写写成禁止或放行。"},
 {"check_id": "S9", "evidence_candidates": [
     {"source_id": "DOC017:T007", "quote": "And yeah, job notifications would also be great unless it's like too complicated. And it's like filling all my notification tab in my mobile yeah."}],
  "candidate_ids": ["C005"], "final_goal_ids": ["G005"], "outcome": "represented",
  "reason": "unless 让步条件完整保留为可接受上限，未反转为“禁止移动通知”。"},
 {"check_id": "S10", "evidence_candidates": [
     {"source_id": "DOC017:T047", "quote": "Of course, the company's Hr right. Whoever is using this feature to actually like get the perfect candidate for the role."},
     {"source_id": "DOC017:T049", "quote": "And of course, even the job agency said."}],
  "candidate_ids": ["C025", "C026", "C027"], "final_goal_ids": [], "outcome": "excluded",
  "reason": "其他受益方属背景，受访者未对其提出目标；不把第三方受益写成系统要求。"},
]

spec = {
 "document_id": "DOC017",
 "raw_candidates": raw,
 "goals": goals,
 "review_questions": [
   {"candidate_ids": ["G005"], "question": "移动通知的限制是硬性上限还是偏好？原文只说“除非太复杂/占满通知栏”，未给阈值。", "reason": "影响渠道取舍与是否允许移动通知并行存在。"},
   {"candidate_ids": ["G007", "G030"], "question": "邮件内快速申请与站内列表的快速申请，是否应视为同一能力的两处入口，还是一个要求？", "reason": "两处分属不同渠道，若产品只做一个，需确认优先级。"},
   {"candidate_ids": ["G003"], "question": "“即时”的判定时延，以及“是否积极求职”由用户设置还是系统推断，原文都未说明。", "reason": "直接影响通知频率实现。"}
 ],
 "limitations": [
   "转写稿含口语重复与疑似识别错误（T021 'what text they are using'、T065 'Sean and Chris'、T093 'Eas'、T099 'list cars'），按上下文分别理解为技术栈、AI、卡片；未改写原文。",
   "单次隔离生成会话，未做独立语义评审与人工确认；questions 中的取舍仍待确认。",
   "访谈仅覆盖求职者一侧，未涉及雇主/HR 侧需求、性能与规模等非功能约束。",
   "未使用外部资料、历史目标或参考答案。"
 ],
 "ledger": {
   "model": "unknown", "temperature": "unknown", "budget": "1 initial pass + <=2 repair rounds",
   "usage": "unknown",
   "skill_revision": "a5952d426b1624a3fcb2ce2829e1ae1ceb15e19dc3309d9571f3bc6b465deb6f",
   "prompt_revision": "task-prompt-v1",
   "planned_passes": 1,
   "stop_reason": "完成 1 次基础逐窗提取与 1 次全篇校正，56 个窗口全部处理；剩余未决项属原文未给信息，无新证据可解，停止问题循环。",
   "passes": passes,
   "full_context_review": {"status": "completed",
     "reason": "回看全部 114 轮：校正 T003/T033/T099 的重复相关性表述与问答范围（问句在 T066、T100 等），T005 的条件频率（积极/不积极），T007 的渠道让步（邮件优先、移动通知有条件），T073 的让步（减少手工但保留按岗位定制），T093–T095 的 AI 分工（识别可用、代写须人工核验且不得自动），T025–T027 的因果（噪音→错过）；确认 T017/T047–T051/T087/T109 仅为比较、受益方或顾虑背景，不另立目标。"},
   "entries": entries,
   "source_checks": source_checks
 },
 "decisions": {
   "relations": [
     {"relation_id": "R1", "source_id": "G012", "target_id": "G011", "type": "contribution",
      "status": "supported", "conditions": ["通知内容按相关性过滤"], "assumptions": [],
      "rationale": "受访者把错过重要岗位直接归因于“通知几乎推送所有岗位且不准确”，因此只推送相关岗位有助于减少被淹没而漏看的岗位；这不保证不漏，故不写成精化。",
      "evidence_ids": [],
      "evidence_quotes": [ev("DOC017:T025", "I think that time the portal they kind of spam lot of notification, I mean, the notification system was not that accurate? And it was sending almost like what? All the jobs right? So few of the jobs were not relevant to me.")]},
     {"relation_id": "R2", "source_id": "G017", "target_id": "G012", "type": "contribution",
      "status": "supported", "conditions": ["被标记的岗位仍由同一匹配来源推荐"], "assumptions": [],
      "rationale": "受访者把“拉黑/标记不感兴趣”与“希望它不再出现”连说，标记反馈有助于后续只推相关岗位。",
      "evidence_ids": [],
      "evidence_quotes": [ev("DOC017:T057", "So I just like, sometimes I kind of blacklist those jobs. And yeah, I just remove those from. I just say that I'm uninterested. and I hope that it doesn't come.")]},
     {"relation_id": "R3", "source_id": "G016", "target_id": "G002", "type": "contribution",
      "status": "supported", "conditions": [], "assumptions": [],
      "rationale": "关键词定制被明确说成是为了“得到相关结果”，而相关性的判定基准是技能集，故关键词有助于收到技能匹配的更新；不宣称关键词足以覆盖全部匹配。",
      "evidence_ids": [],
      "evidence_quotes": [ev("DOC017:T041", "Also customizing few keywords for the job search to kind of get me the relevant result right?")]},
     {"relation_id": "R4", "source_id": "G015", "target_id": "G002", "type": "contribution",
      "status": "supported", "conditions": ["档案中的角色、经历与技能是最新的"], "assumptions": [],
      "rationale": "列表按档案（角色、经历、技能、项目）预先筛选，正是为了让更新贴合本人技能与背景，支持技能匹配的更新。",
      "evidence_ids": [],
      "evidence_quotes": [ev("DOC017:T039", "I kinda assume that it's already set right when it provides me the job list. and I don't need to add any more filters, right?")]},
     {"relation_id": "R5", "source_id": "G020", "target_id": "G019", "type": "contribution",
      "status": "supported", "conditions": ["申请在公司站内页面中完成"], "assumptions": [],
      "rationale": "站内嵌入门户后仍需填表，资料自动转移可让该路径真正省时；原文把两者作为并列期望（And also），有帮助但不构成充分条件。",
      "evidence_ids": [],
      "evidence_quotes": [ev("DOC017:T067", "And also, I would also prefer that all the details from my job portal is already like transferred to those reviews or Company's website. So that would be really great feature.")]}
   ],
   "groups": [
     {"group_id": "GR1", "parent_id": "G011", "child_ids": ["G003", "G012", "G018"],
      "kind": "and", "status": "proposed", "completeness": "partial",
      "rationale": "及时（G003）、相关（G012）、时效（G018）三者同时成立时，可以解释受访者不再因噪音错过岗位；但 G003 明确允许非积极求职时按周接收，该分支本身承认可能错过短期岗位，因此不能声称整组充分，保留为待确认精化。",
      "assumptions": ["通知噪音与过期岗位是错过岗位的主要原因（依据 T025–T027、T071）", "岗位信息在平台内可被及时获取"],
      "evidence_ids": [],
      "evidence_quotes": [
        ev("DOC017:T005", "So it would be great if I receive at the instant. The job is like posted in the platform, or if I'm not looking actively, then it's okay to receive once in a week, right."),
        ev("DOC017:T027", "And with that I kind of missed few of the important jobs.")],
      "relation_ids": ["R1"],
      "checks": [
        {"kind": "normal", "origin": "analysis_assumption",
         "scenario": "用户处于积极求职状态，一个与技能匹配的新岗位当天发布：G003 立即通知、G012 只推送相关岗位、G018 只展示近期岗位同时生效。",
         "outcome": "supports",
         "rationale": "三种机制共同覆盖“及时、相关、时效”，可解释该场景下不再错过。"},
        {"kind": "exception", "origin": "analysis_assumption",
         "scenario": "用户处于非积极求职状态并接受每周摘要，某岗位在两次摘要之间开放又很快关闭。",
         "outcome": "counterexample",
         "rationale": "G003 允许延后一周，因此整组在该分支无法保证不错过，完整性只能记 partial。"}]}
   ],
   "questions": [
     {"target_type": "model", "target_id": "DOC017-goal-model", "message": "邮件与移动通知的关系未定：是邮件为主、移动通知仅在不超过通知栏容量时补充，还是两者同权？"},
     {"target_type": "goal", "target_id": "G003", "message": "“即时”的目标时延，以及“是否积极求职”由用户手动设置还是系统推断，原文未说明。"},
     {"target_type": "goal", "target_id": "G018", "message": "“太旧”的阈值在原文有六个月与一年两种口语说法，是否需要统一为单一门槛？"},
     {"target_type": "group", "target_id": "GR1", "message": "非积极求职（每周摘要）分支下无法避免错过短期开放岗位，是否应把该分支排除在“避免错过”的适用范围之外？"},
     {"target_type": "relation", "target_id": "R5", "message": "G020→G019 的依据是同一答句中的并列偏好，资料自动转移是否应视为站内申请可用的必要前提而非仅帮助？"}
   ],
   "reassessments": []
 }
}

# integrity checks
goal_ids = [g["candidate_id"] for g in goals]
assert len(goal_ids) == len(set(goal_ids))
cand_ids = [c["candidate_id"] for c in raw]
assert len(cand_ids) == len(set(cand_ids))
covered = {}
for e in entries:
    covered[e["candidate_id"]] = e
assert set(cand_ids) == set(covered), set(cand_ids) ^ set(covered)
assert len(entries) == len(cand_ids)
mapped = set()
for e in entries:
    for g in e["final_goal_ids"]:
        assert g in goal_ids, g
        mapped.add(g)
    if e["disposition"] == "exclude":
        assert e["final_goal_ids"] == []
    else:
        assert e["final_goal_ids"]
assert mapped == set(goal_ids), set(goal_ids) - mapped
for g in goals:
    assert g["judgment"]["unsupported_parts"] == []
    if g["origin"] == "inferred":
        assert g["inference"] and g["inference"]["basis_candidate_ids"]
for r in spec["decisions"]["relations"]:
    assert r["source_id"] in goal_ids and r["target_id"] in goal_ids
for q in spec["decisions"]["questions"]:
    assert q["target_id"] in (["DOC017-goal-model"] + goal_ids + ["GR1"] + [r["relation_id"] for r in spec["decisions"]["relations"]])
for q in spec["review_questions"]:
    assert all(c in goal_ids for c in q["candidate_ids"])

out = os.path.join(TASK, "spec.json")
json.dump(spec, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("goals", len(goals), "cands", len(raw), "entries", len(entries), "relations", len(spec["decisions"]["relations"]), "groups", len(spec["decisions"]["groups"]))
print("wrote", out)
