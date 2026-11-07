# -*- coding: utf-8 -*-
"""Build spec.json for DOC034 run03 attempt-01 with char-exact quote verification."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
SRC = json.loads((BASE / "source/DOC034.json").read_text(encoding="utf-8"))
TEXT = {t["source_id"]: t["text"] for t in SRC["turns"]}
WINDOWS = json.loads((BASE / "preview/source-windows.json").read_text(encoding="utf-8"))

TRACE = []


def sp(sid, start, end):
    """Exact substring from start marker through end marker (inclusive)."""
    full = sid if sid.startswith("DOC034:") else "DOC034:" + sid
    t = TEXT[full]
    i = t.find(start)
    assert i >= 0, (full, start)
    j = t.find(end, i)
    assert j >= 0, (full, end)
    q = t[i:j + len(end)]
    TRACE.append((full, q, t.count(q)))
    return q


def ev(sid, quote, role="basis"):
    full = sid if sid.startswith("DOC034:") else "DOC034:" + sid
    return {"source_id": full, "quote": quote, "role": role}


# --- quotes -------------------------------------------------------------
q_net = sp("T003", "networking just connecting with other colleagues", "see what they're up to")
q_mkt = sp("T003", "We do a lot of marketing especially in my field.", "So we focus a lot on marketing.")
q_rec = sp("T003", "We do a lot of recruiting as well through Linkedin.", "compared to some of the other competitors.")
q_lara = sp("T015", "for example, recruiting like the Laravel community", "posting something on Linkedin.")
q_job = sp("T003", "And then even looking for jobs for myself.", "always keeps you motivated.")
q_evt = sp("T003", "I drink from the fire hose of emails", "being put on the community.")
q_cred = sp("T005", "It's mostly to just signal to like my other to my clients", "a bit of credibility.")
q_verify = sp("T005", "It's more of just a you know, another resource", "when I meet in person.")
q_profdev = sp("T005", "So for my own professional development. I can't say", "that much of a role.")
q_cost = sp("T007", "I mean, they do charge you an arm and a leg.", "cost is definitely a consideration there.")
q_tools = sp("T007", "some of the tools that they have to like post", "pretty targeted.")
q_boost = sp("T007", "They have like recommendations.", "all of your different marketing metrics.")
q_learn = sp("T007", "If you want to do kind of a quick, deep dive", "some of those other resources.")
q_post = sp("T009", "So let's say, I'm at a conference.", "post something about it.")
q_toggle = sp("T009", "I can toggle between one or both", "I would choose myself.")
q_sched = sp("T009", "it doesn't really make sense, you know, in the evening", "boost in some of the impressions.")
q_engage = sp("T009", "So once I've posted it", "eventually win some business.")
q_research = sp("T011", "maybe I'll search for their name", "I'll add them.")
q_nocold = sp("T011", "I don't often kind of reach out", "cold call or cold.")
q_freq = sp("T013", "let's call it 4 out of 5 days", "in some way, shape or form.")
q_ads = sp("T017", "sometimes the amount of ads", "there's a lot of irrelevant stuff there.")
q_clutter = sp("T017", "And then certain parts of the interface.", "don't necessarily care for it.")
q_core = sp("T019", "I mean its core hasn't evolved much", "hasn't changed a great deal.")
q_ai = sp("T019", "there's some new like AI tools", "pretty new and interesting.")
q_auto = sp("T021", "Probably the biggest would just be", "that's always a pain")
q_design = sp("T023", "Design is at a premium", "the whole marketing funnel.")
q_interv = sp("T024", "Yes, yes, that would be a really good feature to add", "cut cuts down the time.")
q_def = sp("T001", "So Linkedin is, I mean, in my view", "live in the business world.")

S = "Stakeholder"

raw = [
    dict(candidate_id="C001", statement="Connect with colleagues and former classmates on LinkedIn to see what they are up to.",
         actor=S, modality="present habitual practice ('some of the things that I do')", context=[], origin="explicit",
         pass_id="P1", evidence=[ev("T003", q_net)]),
    dict(candidate_id="C002", statement="Do a lot of marketing on LinkedIn because the exposure is far better than Google Ads, Facebook or other channels in the stakeholder's field.",
         actor=S, modality="explicit present practice with comparison", context=["in the stakeholder's field"], origin="explicit",
         pass_id="P1", evidence=[ev("T003", q_mkt)]),
    dict(candidate_id="C003", statement="Recruit through LinkedIn to source many people at a fairly low cost compared with competitors.",
         actor=S, modality="explicit present practice", context=[], origin="explicit",
         pass_id="P1", evidence=[ev("T003", q_rec)]),
    dict(candidate_id="C004", statement="Look for jobs for himself on LinkedIn and check what salary ranges are out there from time to time.",
         actor=S, modality="hedged ('sometimes it's nice to kind of poke around')", context=[], origin="explicit",
         pass_id="P1", evidence=[ev("T003", q_job)]),
    dict(candidate_id="C005", statement="Check community events posted on LinkedIn when he has the availability and bandwidth.",
         actor=S, modality="conditional ('when I have the availability ... can have the bandwidth')", context=["emails arrive in a firehose, so he cannot otherwise keep up"], origin="explicit",
         pass_id="P1", evidence=[ev("T003", q_evt)]),
    dict(candidate_id="C006", statement="Signal to clients that he exists, with credentials and degrees, so the profile lends credibility.",
         actor=S, modality="explicit purpose statement ('mostly to just signal')", context=[], origin="explicit",
         pass_id="P1", evidence=[ev("T005", q_cred)]),
    dict(candidate_id="C007", statement="Keep LinkedIn as a place where people can verify he is who he says he is and not a scammer, including a matching photo.",
         actor=S, modality="explicit ('another resource for people to check in')", context=[], origin="explicit",
         pass_id="P1", evidence=[ev("T005", q_verify)]),
    dict(candidate_id="C008", statement="LinkedIn contributes to his overall professional development.",
         actor=S, modality="denied ('I can't say it's actually played that much of a role')", context=[], origin="inferred",
         pass_id="P1", evidence=[ev("T005", q_profdev)]),
    dict(candidate_id="C009", statement="Marketing resources are good but LinkedIn charges a lot, so cost is a consideration.",
         actor=S, modality="evaluative comment on pricing ('cost is definitely a consideration')", context=[], origin="explicit",
         pass_id="P1", evidence=[ev("T007", q_cost)]),
    dict(candidate_id="C010", statement="Use LinkedIn's easy, user-friendly posting tools so that broad-based marketing can be targeted.",
         actor=S, modality="positive evaluation of feature usefulness ('very, very easy and user friendly')", context=[], origin="inferred",
         pass_id="P1", evidence=[ev("T007", q_tools)]),
    dict(candidate_id="C011", statement="Pay to have posts recommended more, and keep track of impressions and marketing metrics.",
         actor=S, modality="second-person capability description ('you can pay', 'you can kind of keep track')", context=[], origin="explicit",
         pass_id="P1", evidence=[ev("T007", q_boost)]),
    dict(candidate_id="C012", statement="Use the acquired e-learning platform (Lynda/LinkedIn Learning) for a quick deep dive into a technology stack or marketing practice, because its quality exceeds YouTube.",
         actor=S, modality="past positive evaluation ('I did like', 'one of the better places to go')", context=[], origin="explicit",
         pass_id="P1", evidence=[ev("T007", q_learn)]),
    dict(candidate_id="C013", statement="Post something about what is happening at a conference as a marketing/awareness post.",
         actor=S, modality="typical practice ('Typically what we'll do')", context=["when something interesting is happening at a conference"], origin="explicit",
         pass_id="P1", evidence=[ev("T009", q_post)]),
    dict(candidate_id="C014", statement="Schedule the post for 9 AM the next morning when people first show up at the office instead of posting in the evening, to get more impressions.",
         actor=S, modality="explicit intention ('So I'm going to be posted at ... 9 Am. Tomorrow')", context=[], origin="explicit",
         pass_id="P1", evidence=[ev("T009", q_sched)]),
    dict(candidate_id="C015", statement="Get interactions once the post is on the feed and hopefully eventually win some business.",
         actor=S, modality="expected then hedged hope ('hopefully, eventually')", context=[], origin="explicit",
         pass_id="P1", evidence=[ev("T009", q_engage)]),
    dict(candidate_id="C016", statement="Research a prospect's profile and background for common threads before adding them; do not do cold calls or cold adds.",
         actor=S, modality="conditional practice plus explicit negative ('I don't reach out too much as kind of cold call or cold')", context=[], origin="explicit",
         pass_id="P1", evidence=[ev("T011", q_research), ev("T011", q_nocold)]),
    dict(candidate_id="C017", statement="Use LinkedIn about 4 out of 5 days a week in some way, shape or form.",
         actor=S, modality="factual frequency report", context=[], origin="explicit",
         pass_id="P1", evidence=[ev("T013", q_freq)]),
    dict(candidate_id="C018", statement="For recruiting in the small Laravel community, posting on Lara Jobs yields better candidates than posting on LinkedIn.",
         actor=S, modality="comparative factual report", context=["niche Laravel community"], origin="explicit",
         pass_id="P1", evidence=[ev("T015", q_lara)]),
    dict(candidate_id="C019", statement="The amount of ads and targeted content plus the cluttered interface cloud the feed with irrelevant noise; he does not care for it.",
         actor=S, modality="frustration report ('would probably be the biggest frustration')", context=["when he is on LinkedIn with a mission, e.g. to post something"], origin="explicit",
         pass_id="P1", evidence=[ev("T017", q_ads), ev("T017", q_clutter)]),
    dict(candidate_id="C020", statement="LinkedIn's core has not evolved much; it has focused on more targeted marketing tools and acquired the e-learning platform.",
         actor=S, modality="observation about platform evolution", context=[], origin="explicit",
         pass_id="P1", evidence=[ev("T019", q_core)]),
    dict(candidate_id="C021", statement="New AI tools that help develop content for posts are new and interesting.",
         actor=S, modality="interest observation ('pretty new and interesting')", context=[], origin="explicit",
         pass_id="P1", evidence=[ev("T019", q_ai)]),
    dict(candidate_id="C022", statement="Have LinkedIn provide support for content development, with more of it automated, so that a smaller marketing team is needed.",
         actor=S, modality="suggestion ('would be great to have more of that kind of automated')", context=[], origin="explicit",
         pass_id="P1", evidence=[ev("T021", q_auto)]),
    dict(candidate_id="C023", statement="Be able to post professional-looking content without being reviewed six times or going through the whole marketing funnel.",
         actor=S, modality="suggestion ('it'd be great to be able to')", context=["design is at a premium and takes a while"], origin="explicit",
         pass_id="P1", evidence=[ev("T023", q_design)]),
    dict(candidate_id="C024", statement="Adding a feature that cuts down the time would be a really good feature to add.",
         actor="Interviewer", modality="interviewer endorsement", context=[], origin="explicit",
         pass_id="P1", evidence=[ev("T024", q_interv)]),
    dict(candidate_id="C025", statement="LinkedIn is mostly a professional networking platform that lets professionals connect and live in the business world.",
         actor=S, modality="general description of the platform", context=[], origin="explicit",
         pass_id="P1", evidence=[ev("T001", q_def)]),
]

goals = [
    dict(candidate_id="G001", statement="Connect with colleagues and former classmates on LinkedIn to see what they are up to.",
         actor=S, context=[], origin="explicit", inference=None,
         evidence=[ev("T003", q_net)],
         judgment=dict(label="direct", rationale="原句明确列出在 LinkedIn 上做的事包括 networking、连接同事与过去同学并查看其近况，主体、对象与目的一致。",
                       supported_parts=["连接同事与同学的动作", "查看对方近况的目的"], unsupported_parts=[], assumptions=[], reasoning_steps=[])),
    dict(candidate_id="G002", statement="Run marketing on LinkedIn to obtain exposure that is far better than Google Ads, Facebook or other channels in the stakeholder's field.",
         actor=S, context=["in the stakeholder's field, where LinkedIn exposure is judged better than other channels"], origin="explicit", inference=None,
         evidence=[ev("T003", q_mkt)],
         judgment=dict(label="direct", rationale="原文明确说‘We do a lot of marketing’并把 LinkedIn 的曝光与 Google ads、Facebook 等渠道作比较，认定前者更好；主体、渠道与结果均保留。",
                       supported_parts=["以 LinkedIn 做营销", "曝光优于其他渠道的判断"], unsupported_parts=[], assumptions=[], reasoning_steps=[])),
    dict(candidate_id="G003", statement="Recruit through LinkedIn to source many candidates at a cost that is fairly low compared with competitors.",
         actor=S, context=["exception: in the small Laravel community, posting on Lara Jobs yields better candidates than LinkedIn"],
         origin="explicit", inference=None,
         evidence=[ev("T003", q_rec), ev("T015", q_lara, "context")],
         judgment=dict(label="direct", rationale="原句明确说通过 LinkedIn 大量招聘、来源广且相对竞争者成本低；T015 的 Laravel/Lara Jobs 例外已作为条件保留，不改变一般招聘目标。",
                       supported_parts=["通过 LinkedIn 招聘", "候选人来源广", "相对低成本"], unsupported_parts=[], assumptions=[], reasoning_steps=[])),
    dict(candidate_id="G004", statement="Browse job openings for himself on LinkedIn and check salary ranges from time to time.",
         actor=S, context=["occasionally, when he feels like poking around"], origin="explicit", inference=None,
         evidence=[ev("T003", q_job)],
         judgment=dict(label="direct", rationale="原句‘looking for jobs for myself ... see what some of the salary ranges’表达查看外部机会与薪资范围的意愿，保留‘sometimes / nice to’的弱强度。",
                       supported_parts=["为自己看工作机会", "了解薪资范围"], unsupported_parts=[], assumptions=[], reasoning_steps=[])),
    dict(candidate_id="G005", statement="Check community events posted on LinkedIn when he has the availability and bandwidth, since email alone makes it impossible to keep up.",
         actor=S, context=["only when he has availability/bandwidth", "emails arrive in a firehose, so he cannot keep up otherwise"], origin="explicit", inference=None,
         evidence=[ev("T003", q_evt)],
         judgment=dict(label="direct", rationale="原句说明在有空闲与带宽时会上 LinkedIn 查看社区活动，并给出邮件太多无法兼顾的理由；条件与理由均保留。",
                       supported_parts=["查看社区活动", "以带宽为条件", "邮件过多的理由"], unsupported_parts=[], assumptions=[], reasoning_steps=[])),
    dict(candidate_id="G006", statement="Maintain a credible LinkedIn profile with credentials, degrees and a photo matching his real appearance, so that clients can confirm he is genuine and not a scammer.",
         actor=S, context=["for clients and people who receive his emails"], origin="explicit", inference=None,
         evidence=[ev("T005", q_cred), ev("T005", q_verify)],
         judgment=dict(label="direct", rationale="原句明确把资料页当作向客户示意身份与资历、供人核验其非诈骗的资源，属维持型目标；照片与本人一致等细节保留。",
                       supported_parts=["向客户传递可信度", "供人核验身份", "照片与本人一致"], unsupported_parts=[], assumptions=[], reasoning_steps=[])),
    dict(candidate_id="G007", statement="Use LinkedIn's easy, user-friendly posting tools, including paid recommendations, to put broad-based marketing in front of a targeted audience.",
         actor=S, context=["he already runs marketing on LinkedIn"], origin="inferred",
         inference=dict(basis_candidate_ids=["G002"], reason="受访者已明确在 LinkedIn 上大量做营销（G002），并评价发帖与推荐工具‘very easy and user friendly’、可‘pretty targeted’；由此推断其选择这些工具作为投放方式，而非仅作泛泛评价。",
                        assumptions=["易用与可定向是该受访者持续使用这些工具的实际理由"]),
         evidence=[ev("T007", q_tools)],
         judgment=dict(label="inferred", rationale="原文只陈述工具易用、适合广泛而有针对性的营销，未直接说‘我要用这些工具’；结合其持续营销的正向依据可推断方式选择，故记 inferred。",
                       supported_parts=["工具易用", "营销可广泛且定向"], unsupported_parts=[], assumptions=["易用是其选用理由"],
                       reasoning_steps=["G002 已支持持续营销", "原文正面评价发帖与推荐工具", "推断以其作为实现方式"])),
    dict(candidate_id="G009", statement="Prefer LinkedIn Learning for quick deep dives into a technology stack or a marketing practice, because its quality exceeds YouTube and similar resources.",
         actor=S, context=["when he wants a quick deep dive"], origin="explicit", inference=None,
         evidence=[ev("T007", q_learn)],
         judgment=dict(label="direct", rationale="原句‘I did like ... one of the better places to go ... quality would definitely exceed ... YouTube’直接表达对 e-learning 内容的偏好及质量理由；属偏好型目标，未升级为强制。",
                       supported_parts=["用于快速深入了解技术栈或营销做法", "质量优于 YouTube 的偏好理由"], unsupported_parts=[], assumptions=[], reasoning_steps=[])),
    dict(candidate_id="G010", statement="Publish marketing or awareness posts about events such as conferences, as the company and/or personal profile, with images, videos or other visual additions.",
         actor=S, context=["typically when something interesting happens at a conference", "may post as the company profile, his personal profile, or both"], origin="explicit", inference=None,
         evidence=[ev("T009", q_post), ev("T009", q_toggle, "context")],
         judgment=dict(label="direct", rationale="原文以‘Typically what we'll do is ... post something about it’描述会议现场发营销/曝光帖的固定做法，并说明公司/个人主页切换与图片视频等做法；方式与情境保留。",
                       supported_parts=["发布营销/曝光帖", "会议情境", "公司或个人主页身份"], unsupported_parts=[], assumptions=[], reasoning_steps=[])),
    dict(candidate_id="G011", statement="Schedule posts for about 9 AM the next morning when people first arrive at the office, instead of posting in the evening, to get more impressions.",
         actor=S, context=["posting in the evening is judged to get fewer impressions"], origin="explicit", inference=None,
         evidence=[ev("T009", q_sched)],
         judgment=dict(label="direct", rationale="原文明确说要改为次日上午 9 点定时发布、晚上发布曝光更少；时间、理由与预期结果一致。",
                       supported_parts=["上午 9 点定时", "避开晚间", "以获得更多曝光"], unsupported_parts=[], assumptions=[], reasoning_steps=[])),
    dict(candidate_id="G012", statement="Gain interactions once a post is on the feed and, hopefully, eventually win some business.",
         actor=S, context=["outcome is hoped for, not guaranteed"], origin="explicit", inference=None,
         evidence=[ev("T009", q_engage)],
         judgment=dict(label="direct", rationale="原句说发布后会开始获得互动，并‘hopefully, eventually win some business’；保留希望强度，未写成承诺或指标。",
                       supported_parts=["获得互动", "希望最终带来业务"], unsupported_parts=[], assumptions=[], reasoning_steps=[])),
    dict(candidate_id="G013", statement="Before connecting with a new prospect, search the person's profile and review the background for common threads, and avoid cold calls or cold connection requests.",
         actor=S, context=["usually only connects with people he knows", "example prospect: a C-level person at a company he wants to sell to"], origin="explicit", inference=None,
         evidence=[ev("T011", q_research), ev("T011", q_nocold)],
         judgment=dict(label="direct", rationale="原文明确说明只联系认识的人、不做 cold call/cold add；对目标公司的 C-level 会先搜索资料、看背景找共同点再决定是否添加。动作、对象与否定均保留。",
                       supported_parts=["先搜索并查看背景", "寻找共同点", "不做 cold add"], unsupported_parts=[], assumptions=[], reasoning_steps=[])),
    dict(candidate_id="G014", statement="Have LinkedIn provide more automated support for content development so that a smaller marketing team is needed.",
         actor=S, context=["suggestion strength ('would be great')"], origin="explicit", inference=None,
         evidence=[ev("T021", q_auto)],
         judgment=dict(label="direct", rationale="原文在被问及希望增加或修改什么时明确回答内容开发支持、希望更多自动化，以减少对大型营销团队的需要；建议强度保留。",
                       supported_parts=["内容开发支持", "更多自动化", "减少营销团队规模"], unsupported_parts=[], assumptions=[], reasoning_steps=[])),
    dict(candidate_id="G015", statement="Be able to post professional-looking content without six rounds of review or going through the whole marketing-funnel approval process.",
         actor=S, context=["design is at a premium and always takes a while"], origin="explicit", inference=None,
         evidence=[ev("T023", q_design)],
         judgment=dict(label="direct", rationale="原文明确希望不必被评审 6 次、不必走完整营销漏斗就能发布专业外观的内容，并说明设计耗时是原因；强度与条件保留。",
                       supported_parts=["发布专业外观内容", "免去六轮评审与营销漏斗"], unsupported_parts=[], assumptions=[], reasoning_steps=[])),
]

# --- relations / groups / questions ------------------------------------
q_prec = "So once I've posted it, it goes out to the network and it's on the feed, so I'll start to kind of get some interactions."
assert TEXT["DOC034:T009"].count(q_prec) == 1
q_timing = q_sched
q_spec = sp("T009", "the task would probably be kind of posting, marketing information", "just for awareness")
q_group = sp("T009", "And then, when I'm done I can hit this post button", "schedule it for later")
for qq in (q_prec, q_timing, q_spec, q_group, q_tools, q_mkt):
    assert sum(t.count(qq) for t in TEXT.values()) >= 1

relations = [
    dict(relation_id="R1", source_id="G010", target_id="G012", type="precedes", status="supported",
         conditions=[], assumptions=[],
         rationale="先有发布并进入 feed 的结果，随后才会开始获得互动；原句用 once I've posted it ... I'll start to get interactions 明确先后。",
         evidence_ids=[], evidence_quotes=[ev("T009", q_prec)]),
    dict(relation_id="R2", source_id="G011", target_id="G012", type="contribution", status="supported",
         conditions=["posts are scheduled to the morning peak instead of the evening"], assumptions=["more impressions make interactions more likely"],
         rationale="上午 9 点定时被明确用于获得更多曝光，而曝光进入 feed 后才开始获得互动；定时对互动有正向帮助但原文未保证。",
         evidence_ids=[], evidence_quotes=[ev("T009", q_timing)]),
    dict(relation_id="R3", source_id="G010", target_id="G002", type="specialization", status="supported",
         conditions=["posting as company and/or personal profile"], assumptions=[],
         rationale="发布营销/曝光帖是受访者做营销的一般目标下的具体情境做法；T009 把该任务直接称为 marketing post，T003 说他们重点关注营销。",
         evidence_ids=[], evidence_quotes=[ev("T009", q_spec), ev("T003", sp("T003", "So we focus a lot on marketing.", "So we focus a lot on marketing."))]),
    dict(relation_id="R4", source_id="G007", target_id="G002", type="operationalization", status="supported",
         conditions=[], assumptions=["tool ease and targeting are the reasons the stakeholder keeps using them"],
         rationale="易用的发帖与推荐工具是受访者实现营销曝光的实现方式；原句说这些工具让 LinkedIn 成为适合广泛且定向营销的工具。",
         evidence_ids=[], evidence_quotes=[ev("T007", q_tools)]),
]

groups = [
    dict(group_id="GR1", parent_id="G012", child_ids=["G010", "G011"], kind="and", status="proposed", completeness="partial",
         rationale="发布内容并在早高峰定时，看起来共同构成获得互动的操作组合；但原文没有给出内容质量、受众规模与转化条件，不能声称整组已足以实现获得互动与业务。",
         assumptions=["把发布与定时视为同一流程中互补的两个子目标"],
         evidence_ids=[], evidence_quotes=[ev("T009", q_group)],
         relation_ids=["R1", "R2"],
         checks=[
             dict(kind="normal", origin="analysis_assumption",
                  scenario="受访者在会议现场写好一条营销帖，并定时到次日 9 点人群上线时发布。",
                  outcome="supports",
                  rationale="发布使内容进入 feed，定时提升曝光；两者共同构成获得互动的前置条件。"),
             dict(kind="exception", origin="analysis_assumption",
                  scenario="内容与目标受众无关、账号粉丝很少，或只发布而不回应评论时，即使按早高峰定时也未必获得互动或业务。",
                  outcome="counterexample",
                  rationale="原文未给出内容质量、受众规模与互动转化条件，且有其他目标（G014/G015）涉及内容制作，故整组不能成立为充分精化。"),
         ]),
]

questions = [
    dict(target_type="model", target_id="DOC034-goal-model",
         message="已检查 G014（内容开发自动化支持）与 G015（免多轮评审发布专业内容）之间是否存在实现方式或贡献联系：原文只并列提出两项期望，未说明自动化能减少评审轮次，故未建立联系。"),
    dict(target_type="model", target_id="DOC034-goal-model",
         message="已检查 G006（可信的专业资料页）是否有助于 G012（获得互动与业务）：原文只说明向客户传递可信度，未说明它带来互动或成交，故未建立联系。"),
    dict(target_type="model", target_id="DOC034-goal-model",
         message="已检查 G013（先查背景再加人）与 G001（与同事、同学联系）之间的联系：两者对象不同（陌生目标客户 vs 熟人），原文未说明前者服务于后者，故未建立联系。"),
    dict(target_type="model", target_id="DOC034-goal-model",
         message="已检查 G009（LinkedIn Learning 快速深入）与其他目标的联系：原文未说明它服务于营销、招聘或职业发展；且 T005 明确否认 LinkedIn 对职业发展起作用，故无联系依据。"),
    dict(target_type="goal", target_id="G010",
         message="受访者把广告与界面杂乱列为最大困扰（T017），但未提出明确的改动要求；是否应据此建立‘减少广告/无关内容干扰’的目标，待确认。"),
    dict(target_type="group", target_id="GR1",
         message="GR1 缺少内容质量、受众规模与互动转化条件的依据，也未把 G014/G015（专业内容制作）纳入为共同前提，尚不能成立。"),
]

review_questions = [
    dict(candidate_ids=["G014"], question="‘would be great to have more of that kind of automated’属建议强度，是否应视为必须需求？",
         reason="原文未说明采纳或优先级，只表达希望。"),
    dict(candidate_ids=["G012"], question="‘hopefully, eventually win some business’是期望而非承诺，业务结果是否应保留为目标？",
         reason="强度为希望，且没有时间或数量指标。"),
]

wids = [w["window_id"] for w in WINDOWS["windows"]]
passes = [
    dict(pass_id="P1", kind="initial", context="isolated", status="completed",
         window_results=[dict(window_id=w, status="processed", reason="") for w in wids]),
    dict(pass_id="P2", kind="full_context", context="isolated", status="completed",
         window_results=[dict(window_id=w, status="processed", reason="") for w in wids]),
]

entries = [
    ("C001", "keep", ["G001"], "同义保留：连接同事/同学并查看近况，动作与目的一致。"),
    ("C002", "keep", ["G002"], "同义保留：以 LinkedIn 做营销并认定曝光优于其他渠道。"),
    ("C003", "keep", ["G003"], "同义保留：大量招聘、来源广、成本较低。"),
    ("C004", "keep", ["G004"], "同义保留：为自己看工作与薪资范围，保留弱强度。"),
    ("C005", "keep", ["G005"], "同义保留：以带宽为条件查看社区活动。"),
    ("C006", "keep", ["G006"], "同义保留：向客户示意存在与资历。"),
    ("C007", "merge", ["G006"], "与 C006 为同一维持意图的另一表述（供人核验非诈骗），合并入 G006 并保留照片一致细节。"),
    ("C008", "exclude", [], "受访者明确否认 LinkedIn 对职业发展起作用，属相反证据，不建目标。"),
    ("C009", "exclude", [], "仅是对营销资源与定价的评价；价格只是选型考虑，未表达要达成或维持的成本状态，原文仍继续大量营销。"),
    ("C010", "keep", ["G007"], "整理为方式目标：以易用、可定向的发帖工具投放广泛营销。"),
    ("C011", "exclude", [], "‘you can pay / you can keep track’是第二人称的工具能力描述，未表明本人付费推广或跟踪指标，不建目标。"),
    ("C012", "keep", ["G009"], "同义保留：偏好 e-learning 做快速深入，质量优于 YouTube。"),
    ("C013", "keep", ["G010"], "同义保留：会议现场发布营销/曝光帖。"),
    ("C014", "keep", ["G011"], "同义保留：改到次日上午 9 点定时以增加曝光。"),
    ("C015", "keep", ["G012"], "同义保留：获得互动并希望带来业务；保留希望强度。"),
    ("C016", "keep", ["G013"], "同义保留：先查资料找共同点再加人，不做 cold add；条件与否定均保留。"),
    ("C017", "exclude", [], "使用频率陈述（4/5 天）是事实，不是要达到或维持的目标。"),
    ("C018", "merge", ["G003"], "招聘渠道对比；作为 G003 的例外条件并入（小众社区另有更优渠道），不另建目标。"),
    ("C019", "exclude", [], "广告与界面杂乱是障碍/抱怨，原文未提出明确改动要求；保留为 G010 的待确认问题，不升级为目标。"),
    ("C020", "exclude", [], "平台演进观察，不构成要求。"),
    ("C021", "merge", ["G014"], "对 AI 内容工具的兴趣与 G014 同向，作为背景并入，不单独建目标。"),
    ("C022", "keep", ["G014"], "同义保留：内容开发自动化支持，减少营销团队规模。"),
    ("C023", "keep", ["G015"], "同义保留：免六轮评审与营销漏斗发布专业内容。"),
    ("C024", "exclude", [], "采访者的赞同与评价，非受访者目标；采纳未知，不作为要求。"),
    ("C025", "exclude", [], "对平台的总体定义，属背景，不含个人意图。"),
]

source_checks = [
    ("S1", [ev("T003", q_mkt)], ["C002"], ["G002"], "represented", "回查营销句：主体、渠道比较与‘focus a lot on marketing’一致，已入 G002。"),
    ("S2", [ev("T005", q_profdev)], ["C008"], [], "excluded", "回查职业发展问答：受访者明确否认 LinkedIn 的作用，无目标可建。"),
    ("S3", [ev("T007", q_cost)], ["C009"], [], "excluded", "回查定价评论：只是成本考量，未条件化或改变营销行为。"),
    ("S4", [ev("T007", q_boost)], ["C011"], [], "excluded", "回查付费推荐与指标句：为第二人称能力描述，无本人采纳依据。"),
    ("S5", [ev("T015", q_lara)], ["C018"], ["G003"], "represented", "回查 Laravel 招聘渠道：作为 G003 的例外条件保留，未改变一般招聘目标。"),
    ("S6", [ev("T017", q_ads), ev("T017", q_clutter)], ["C019"], [], "excluded", "回查障碍段：抱怨成立但无改动请求，转为 G010 的待确认问题。"),
    ("S7", [ev("T005", q_verify)], ["C007"], ["G006"], "represented", "回查身份核验句：与 C006 合并入 G006。"),
    ("S8", [ev("T024", q_interv)], ["C024"], [], "excluded", "回查结尾：采访者评价，非受访者目标。"),
    ("S9", [ev("T009", q_sched)], ["C014"], ["G011"], "represented", "回查定时句：时间、晚间对比与曝光结果一致。"),
]

spec = dict(
    document_id="DOC034",
    raw_candidates=raw,
    goals=goals,
    review_questions=review_questions,
    limitations=[
        "原文为英文访谈转写，含口语重复与转写噪声（如‘I I.’‘our just too cluttered’）；引文按原文逐字符保留，未做清理。",
        "未获得受访者对目标清单的采纳、优先级或验收指标，全部目标保持待审。",
        "广告与界面杂乱是受访者所述最大困扰，但原文未提出明确改动要求，仅作为待确认问题保留。",
    ],
    ledger=dict(
        model="unknown", temperature="unknown", budget="1 initial pass + <=2 repair rounds",
        usage="unknown", skill_revision="a5952d426b1624a3fcb2ce2829e1ae1ceb15e19dc3309d9571f3bc6b465deb6f",
        prompt_revision="task-prompt-v1", planned_passes=2,
        stop_reason="完成一次全窗口初始提取与一次全篇校正；剩余未决项（广告干扰、建议强度、GR1 充分性）缺少新证据，按预算停止。",
        passes=passes,
        full_context_review=dict(status="completed",
            reason="27 轮全文通读两遍：逐窗捕获后回查指代（it/that 指向帖子、工具、资料页）、问答范围（T004 职业发展、T006 功能、T016 障碍、T020 改进）、条件继承（带宽、已知联系人、公司/个人主页）与例外（Laravel 招聘渠道），并核对 T005 对职业发展的相反证据。"),
        entries=[dict(candidate_id=c, disposition=d, final_goal_ids=g, reason=r) for c, d, g, r in entries],
        source_checks=[dict(check_id=i, evidence_candidates=e, candidate_ids=c, final_goal_ids=g, outcome=o, reason=r)
                       for i, e, c, g, o, r in source_checks],
    ),
    decisions=dict(relations=relations, groups=groups, questions=questions, reassessments=[]),
)

# --- verification -------------------------------------------------------
for sid, q, n in TRACE:
    assert q in TEXT[sid], (sid, q[:60])
    assert n >= 1
for rel in relations:
    for e in rel["evidence_quotes"]:
        n = TEXT[e["source_id"]].count(e["quote"])
        assert n == 1, ("relation quote not unique", rel["relation_id"], n)
for g in groups:
    for e in g["evidence_quotes"]:
        n = TEXT[e["source_id"]].count(e["quote"])
        assert n == 1, ("group quote not unique", g["group_id"], n)

ids = {g["candidate_id"] for g in goals}
for g in goals:
    if g["inference"]:
        assert set(g["inference"]["basis_candidate_ids"]) <= ids
for q in review_questions:
    assert set(q["candidate_ids"]) <= ids
for entry in spec["ledger"]["entries"]:
    assert set(entry["final_goal_ids"]) <= ids
    assert entry["final_goal_ids"] or entry["disposition"] == "exclude" or entry["disposition"] == "uncertain"

payload = json.dumps(spec, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
# close the numeric gap created by the dropped metrics goal: shift G009..G015 down by one
for old, new in (("G009", "G008"), ("G010", "G009"), ("G011", "G010"),
                 ("G012", "G011"), ("G013", "G012"), ("G014", "G013"), ("G015", "G014")):
    payload = payload.replace(old, new)
(BASE / "spec.json").write_text(payload, encoding="utf-8")
print("goals", len(goals), "raw", len(raw), "relations", len(relations), "groups", len(groups))
print("windows", len(wids))
for sid, q, n in TRACE:
    print(sid, n, q[:50].replace("\n", " "))
