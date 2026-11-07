# -*- coding: utf-8 -*-
"""Generate spec.json for DOC004 run02 attempt-02. Validates every quote against source."""
import json
import sys
from pathlib import Path

HERE = Path("D:/Desktop/summer_pro/GoalForge/GoalForge/extra/runs/workbuddy-newskills-20261103-0015/main/DOC004/run02/attempt-02")
SKILLS = Path("D:/Desktop/summer_pro/GoalForge/GoalForge/extra/runs/workbuddy-newskills-20261103-0015/versions/skills")
sys.path.insert(0, str(SKILLS / "goal-extraction" / "scripts"))
from prepare_source import prepare, build_windows, digest, encode  # noqa: E402

SRC = json.loads((HERE / "source" / "DOC004.json").read_text(encoding="utf-8"))
TEXT = {t["source_id"]: t["text"] for t in SRC["turns"]}
MANIFEST_SHA = "a5952d426b1624a3fcb2ce2829e1ae1ceb15e19dc3309d9571f3bc6b465deb6f"

# ---- exact quotes (copy verbatim from source text) ----
Q = {
 "q1": ("DOC004:T005", "the main reason I use the app is to do sell payments to like a few of my friends. Basically split split costs and all of that."),
 "q2": ("DOC004:T005", "So normally, when I have. Let's say a lot of funds in my checking account, so I normally transfer it over to my savings, so I can get even that little bit of interest I normally get."),
 "q3": ("DOC004:T005", "So any grocery stores, or like any outlets. So I use apple pay there. So which directly connects to chase itself. And then, does the payment from there."),
 "q4": ("DOC004:T007", "So Zelle is basically like a way to instantaneously transfer small amounts of money between, let's say, 2 different accounts just based on their phone number."),
 "q4b": ("DOC004:T007", "And to, let's say, do quick payments to, let's say friends or family."),
 "q5": ("DOC004:T015", "I would say the ui is really good on. Honestly. Obviously, I don't mean that it's like amazing or anything, but it's like very functional and very useful, and the ui looks good compared to other bank applications."),
 "q6": ("DOC004:T015", "So it's a good thing that I can like. Just look at all of my spends on like in like a quick glance, and don't really have to go to like multiple screens to check all of that"),
 "q7": ("DOC004:T015", "They also have a very small list of all the transactions, like all the recent transactions. So again, that's also good. Also because I don't have to like, you know, click on another link, or like another button, and then I'll check out this. So it's pretty convenient."),
 "q8": ("DOC004:T015", "So everything is presented to me in in sort of like this dashboard when I sign in. So it shows me all my bank accounts."),
 "q9": ("DOC004:T017", "Honestly. It's perfect the way it is. I think it handles everything that an a banking application should handle"),
 "q10": ("DOC004:T017", "Obviously there might be some con country specific features, but I'm not including that in this, because it doesn't obviously matter in this context."),
 "q11": ("DOC004:T017", "the pays up is much better because they also have like this plan and track feature where you can like track like, you can basically set monetary goals. And then track how you're doing that."),
 "q12": ("DOC004:T019", "And I believe, like my funds are pretty safe with the bank. because, like every time I do a transaction. I get a notification on my phone saying that this much amount of money has been spent, and then I can also contest it, which is great."),
 "q13": ("DOC004:T019", "They had this whole 2 factor thing authentication thing set up like from the get go. So that was good. So that way. That's like an additional layer of security."),
 "q14": ("DOC004:T019", "although, might not have like a very good idea of how well, they've implemented like the security infrastructure"),
 "q15": ("DOC004:T021", "they have this plan and track feature where it basically keeps track of how much money I'm spending every month and how much money I'm actually getting"),
 "q16": ("DOC004:T021", "So it lets me set a goal and then tells me how much exactly I'm supposed to be earning, and are spending every month to make sure I hit that goal by a specified timeframe which is good, because, like obviously helps me keep on track and not really spend a lot"),
 "q17": ("DOC004:T021", "But apart from that, I don't really think it gives me like a breakdown of how much I'm spending and where. So I I think that it would be great to see something like that. So I believe it's pretty easy to like categorize what we are spending on. And then I think it would be like a very valuable insight. For the users."),
 "q18": ("DOC004:T021", "although I'm not really sure if they let's say, track, what kind of expenses I do."),
 "q19": ("DOC004:T023", "But apart from that, it doesn't have any other sort of indicator to show that I've let's say, spend it on groceries or on fuel, or something like that."),
 "q20": ("DOC004:T023", "it just categorizes how I spend it. Like it says, if it's card Zelle or yeah, if it's like another fee or something like that, or if it's like an account transfer."),
 "q21": ("DOC004:T025", "Lets me basically set different kind of parameters that I want in the card, or like change, how much like, what's the Max limit per day, and all of that? So that is pretty straightforward. And then like very easy to access."),
 "q21b": ("DOC004:T025", "I can. I can do that in the in the app, I believe."),
 "q22": ("DOC004:T028", "I will make it a very specific goal. Let's try and restrict your online spend limit to. let's say, a hundred dollars per transaction."),
 "q23": ("DOC004:T035", "So yeah, I don't think I don't think they really have like a specific option where I can, like, you know. change my change the limits on the card per se, yeah."),
 "q24": ("DOC004:T035", "Yeah, so obviously, it's not very intuitive. I would really like it to be a bit more better."),
 "q25": ("DOC004:T037", "So I would like to see that feature, and it's honestly upset that they haven't added it to this, considering it's such a huge bank."),
 "q26": ("DOC004:T037", "That's obviously something I'd really like to have."),
 "q27": ("DOC004:T037", "the only reason I'm I haven't used it yet is because most of my funds are in my savings account, which is not tied to my debit card anyway. So even if let's say that limit really matters to me, I can't really go above it, because most of my funds are in savings, anyway."),
 "q28": ("DOC004:T037", "But obviously like at 1 point in time, I would like to use it at some point, because I remember using it for my previous credit and debit cards."),
 "q29": ("DOC004:T041", "I don't think Zelle is I don't think we can sell on of the web app."),
 "q29b": ("DOC004:T041", "So I'll have to know the I have to know the what do you say? The account number to basically transfer this to someone."),
 "q30": ("DOC004:T045", "Yeah, obviously, I would like to see them implement Zelle on on the web app because I think it. It'll just be more convenient, so that I don't have to like reach. Reach my phone every time."),
 "q31": ("DOC004:T045", "it's super intuitive, and then it makes sure that you don't send the wrong amount, or like to the wrong person. So that is great, and then it lets you schedule properly. It also lets you repeat the transactions is a great, so you don't have to come and keep on doing it again and again."),
 "q32": ("DOC004:T045", "My only my only concern is that it does not have cell."),
 "q33": ("DOC004:T053", "but I don't see like a way to like text or like chat with a with a bank manager like someone in the bank, like on through text through the website."),
 "q34": ("DOC004:T055", "Normally. I am very used to having a chat based interface when it comes to support, because it lets I don't know. It's just more relaxing. It's not really it doesn't. It's not really anxiety inducing as much as the call."),
 "q35": ("DOC004:T055", "So and I can like multitask while texting like, let's say, the bank representative. So that would be a great option."),
 "q36": ("DOC004:T055", "But obviously, I believe there are like a few limitations as to why they can't add it."),
 "q37": ("DOC004:T055", "But that obviously, that'd be a great feature like either. Let's say, through an AI bot."),
 "q38": ("DOC004:T055", "But for, let's say, people who who don't exactly know how to get around the website. It'd be great to just like text the AI bot. And then, like, get responses and all of that. So that would be great, too."),
 "q39": ("DOC004:T059", "Okay. So I definitely don't feel better of the website. But I still stand by my statement that it is a very good ui."),
 "q40": ("DOC004:T059", "I I think I had to click like 7 or 8 times to even get to locking or unlocking my debit card, which is. which is honestly kind of bad design."),
 "q41": ("DOC004:T059", "But honestly, I understand that because I don't think people use that as often."),
 "q42": ("DOC004:T059", "But although I think, like some of the more important features should be more accessible."),
 "q43": ("DOC004:T059", "So that way for doing like all these main functions, it's really good. So it's really accessible."),
 "q44": ("DOC004:T061", "but they also have, like a team of advisors, or like you can have a 1 to one with an advisor which is a really good features. Be really good feature, because if you're not, if you don't know where to start investing, you can like talk to someone."),
 "q45": ("DOC004:T061", "And instead of like losing a lot of money, you know, you could talk to someone who actually knows what they're doing, and then, get started with the training, which I think is a really good option."),
 "q_task_transfer": ("DOC004:T040", "Let's just say, like you, you have to transfer like $1, just for the purpose of this assignment."),
 "q_task_agent": ("DOC004:T050", "You only have access to their website right now. I would like you to be able to get in touch with an agent."),
}

# ---- quote validation (must be exact substring of the referenced turn) ----
def verify_quotes():
    bad = []
    ambiguous = []
    for key, (sid, quote) in Q.items():
        if sid not in TEXT:
            bad.append((key, sid, "unknown source_id"))
            continue
        hits = TEXT[sid].count(quote)
        if quote not in TEXT[sid]:
            bad.append((key, sid, "NOT an exact substring"))
        elif hits > 1:
            ambiguous.append((key, sid, hits))
    if bad:
        print("QUOTE VALIDATION FAILED:")
        for key, sid, why in bad:
            print(" ", key, sid, why)
            print("   quote:", repr(Q[key][1][:120]))
        raise SystemExit(1)
    print("quote validation: all", len(Q), "quotes are exact substrings")
    if ambiguous:
        print("ambiguous quotes (resolved by harness offsets):")
        for key, sid, hits in ambiguous:
            print(" ", key, sid, hits, "hits")
    else:
        print("no ambiguous quotes")


def ev(*keys, role="basis"):
    return [{"source_id": Q[k][0], "quote": Q[k][1], "role": role} for k in keys]


# ---- raw candidates ----
raw = []
def RC(cid, statement, *qkeys, actor="Stakeholder", modality="statement", origin="explicit", context=None):
    raw.append({"candidate_id": cid, "statement": statement, "actor": actor,
                "modality": modality, "context": context or [], "origin": origin,
                "pass_id": "P1", "evidence": ev(*qkeys)})

RC("C001", "Use the app mainly to make small 'sell' payments to friends to split costs, to transfer surplus checking funds to savings to earn interest, and to pay at grocery stores/outlets with Apple Pay connected to Chase.", "q1", "q2", "q3", modality="habitual use ('normally' / 'main reason')")
RC("C002", "Zelle is a way to instantaneously transfer small amounts of money between two accounts based on phone number; it is super easy to use and is used for quick payments to friends or family.", "q4", "q4b", modality="definition + 'super easy to use'")
RC("C003", "The website UI is very good/functional/useful and similar to the mobile app; everything is laid out on a dashboard showing all accounts, balances, deposits and withdrawals; it is good to see all spends at a quick glance without multiple screens; there is also a convenient small list of recent transactions without extra clicks.", "q5", "q8", "q6", "q7", modality="positive evaluation ('a good thing' / 'pretty convenient')")
RC("C004", "It's perfect the way it is; it handles everything a banking application should handle; any country-specific features are not included in this comparison because they do not matter in this context.", "q9", "q10", modality="general satisfaction / concession")
RC("C005", "The plan and track feature lets you set monetary goals and track how you are doing, which makes the app much better.", "q11", modality="positive evaluation ('much better')")
RC("C006", "I feel my funds are pretty safe with the bank; two-factor authentication is an additional layer of security; every transaction triggers a phone notification that can also be contested; although I might not have a very good idea of how well the security infrastructure is implemented.", "q12", "q13", "q14", modality="belief / evaluation + concession")
RC("C007", "The plan and track feature keeps track of monthly spending and income, lets me set a goal and tells me how much to earn/spend each month to make sure I hit that goal by a specified timeframe, which is good because it helps me keep on track and not really spend a lot.", "q15", "q16", modality="positive evaluation ('which is good')")
RC("C008", "It would be great to see a breakdown of how much I am spending and where; I believe it is pretty easy to categorize what we are spending on and that it would be a very valuable insight for the users; I am not really sure if they track what kind of expenses I do.", "q17", "q18", modality="soft suggestion ('I think' / 'I believe' / 'it would be great')")
RC("C009", "The transaction view just categorizes how I spend by transaction type (card, Zelle, another fee, account transfer) but has no other indicator to show that I spent it on groceries or on fuel.", "q19", "q20", modality="observation of current capability")
RC("C010", "In the app I believe I can set different card parameters or change what the Max limit per day is; that is pretty straightforward and very easy to access.", "q21b", "q21", modality="belief ('I believe') about an existing app capability")
RC("C011", "Let's try and restrict your online spend limit to a hundred dollars per transaction on the website.", "q22", actor="Interviewer", modality="interviewer task / specific value")
RC("C012", "The website only lets me lock/unlock the card, replace a card or get a new PIN; I don't think there is a specific option to change the limits on the card; it is not very intuitive and I would really like it to be a bit better.", "q23", "q24", modality="complaint + improvement wish")
RC("C013", "That is something I would really like to have on the website and I would like to see that feature; I am honestly upset they haven't added it to such a huge bank. The only reason I haven't used it yet is that most of my funds are in a savings account not tied to my debit card, so the limit would not currently bind, but I would like to use it at some point, having used it on previous credit and debit cards.", "q26", "q25", "q27", "q28", modality="strong desire ('really like' / 'would like to see') + condition/exception")
RC("C014", "I don't think we can Zelle on the web app; to transfer to someone I would have to know their account number.", "q29", "q29b", modality="observation of a gap")
RC("C015", "I would like to see them implement Zelle on the web app because it would be more convenient so I don't have to reach for my phone every time; apart from that account transfer is great, super intuitive, makes sure you don't send the wrong amount or to the wrong person, lets you schedule properly and repeat transactions so you don't keep doing it again and again; my only concern is that it does not have Zelle; except that it's really good and seamless.", "q30", "q31", "q32", modality="desire + positive evaluation + 'only concern'")
RC("C016", "On the website I don't see a way to text or chat with a bank manager through the website; we can call them or set up a meeting.", "q33", modality="observation of a missing channel")
RC("C017", "I am very used to a chat based interface for support; it is more relaxing and less anxiety inducing than a call and lets me multitask while texting a bank representative; that would be a great option / a great feature, e.g. through an AI bot; for people who don't exactly know how to get around the website it would be great to just text the AI bot and get responses; I believe there are a few limitations as to why they can't add it.", "q34", "q35", "q36", "q37", "q38", modality="preference / soft suggestion + belief about feasibility")
RC("C018", "I definitely don't feel better of the website, but I still stand by it being a very good UI; for the main daily functions (transferring money, checking transactions) it is really good and really accessible; some niche features like locking/unlocking the debit card needed 7 or 8 clicks, which is honestly kind of bad design, though I understand because people don't use them as often; some of the more important features should be more accessible.", "q39", "q43", "q40", "q41", "q42", modality="evaluation + complaint + concession + improvement wish")
RC("C019", "The investment feature (trading account, one-to-one advisor, believed partnership with J.P. Morgan) is a really good feature; if you don't know where to start investing you can talk to someone instead of losing a lot of money and get started with trading, which I think is a really good option.", "q44", "q45", modality="positive evaluation + belief")
RC("C020", "Let's say you have to transfer like $1, just for the purpose of this assignment.", "q_task_transfer", actor="Interviewer", modality="interviewer task / specific value")
RC("C021", "You only have access to their website right now. I would like you to be able to get in touch with an agent.", "q_task_agent", actor="Interviewer", modality="interviewer task framing")

# ---- goals (one goal = one core action) ----
goals = []
def G(gid, statement, ctx, qkeys, label, rationale, supported, unsupported=None,
      assumptions=None, steps=None, origin="explicit", inference=None):
    goals.append({"candidate_id": gid, "statement": statement, "actor": "Stakeholder",
                  "context": ctx, "origin": origin, "inference": inference,
                  "evidence": ev(*qkeys),
                  "judgment": {"label": label, "rationale": rationale,
                               "supported_parts": supported, "unsupported_parts": unsupported or [],
                               "assumptions": assumptions or [], "reasoning_steps": steps or []}})

G("G001", "Use the app to make quick small payments (called 'sell' payments, i.e. Zelle) to a few friends to split costs.",
  ["主要用途（'the main reason I use the app'）", "转写中 'sell'/'cell' 为 Zelle 的 ASR 拼写，按 T006/T007 的定义校正", "对象：几个朋友（T007 补充亲友）；小额、即时、凭手机号", "主体为受访者本人"],
  ["q1", "q4b"], "direct",
  "受访者明确说使用 app 的主要原因是向朋友发 Zelle 付款以分摊费用，主体、动作、对象与目的在 T005 直接出现；T007 的定义补充'小额/即时/凭手机号/面向亲友'的方式。位置与语义逐项一致。",
  ["使用 app 向朋友发起小额付款以分摊费用"])

G("G002", "Transfer surplus funds from the checking account to the savings account when the checking account has a lot of funds, in order to earn the small amount of interest.",
  ["条件：'when I have ... a lot of funds in my checking account'", "强度：习惯性（'normally'）", "预期结果：'get even that little bit of interest'", "账户为本人名下的 checking 与 savings"],
  ["q2"], "direct",
  "T005 直接陈述当支票账户资金较多时把资金转到储蓄账户以获取利息；条件、动作、结果、强度均可逐项核对。",
  ["条件触发的本人账户间转账以获取利息"])

G("G003", "Use Apple Pay, which is connected directly to Chase, to pay at grocery stores and other outlets.",
  ["方式：Apple Pay 且'directly connects to chase itself'", "场景：grocery stores / any outlets", "习惯性用途"],
  ["q3"], "direct",
  "T005 明确说在杂货店等门店使用 Apple Pay、且该方式直接连到 Chase 完成付款；主体/对象/方式一致。",
  ["用直连 Chase 的 Apple Pay 在门店付款"])

G("G004", "Have the website provide a categorized data analysis of where money is spent (e.g. groceries or fuel) as a valuable insight for users.",
  ["软建议强度：'I think it would be great'、'I believe'", "受访者不确定现有系统是否已按消费类别跟踪（'I'm not really sure if they ... track, what kind of expenses I do'）", "T023：现有交易列表只按交易类型（card/Zelle/another fee/account transfer）分类，不按消费地点/类别", "'data analysis'/'expense categories' 的措辞来自采访者 T020", "'valuable insight for the users' 为受访者的推广性评价"],
  ["q17", "q18", "q19"], "insufficient",
  "受访者表达了'想看到花费多少与去向的分解'这一愿望，但把它表述为'面向用户的数据分析/有价值洞察'时证据不足：'data analysis / expense categories'措辞来自采访者提问，'valuable insight for the users'是推广性评价，且受访者自述不确定系统是否已按消费类别跟踪；T023 表明系统已按交易类型分类、只是未按消费类别。据实保留为 insufficient，不升级。",
  ["希望看到花费多少与去向的分解（T021）", "现有分类仅按交易类型、缺少 groceries/fuel 等消费类别指示（T023）"],
  ["'按消费类别的数据分析'是否为其本人需求表述（该措辞来自采访者 T020）", "'面向用户的有价值洞察'这一推广性收益", "系统是否已按消费类别跟踪（受访者明确表示不确定）"],
  ["把 'a breakdown of how much I'm spending and where' 理解为按消费类别的分解"],
  ["逐项核对主体/范围/条件/强度/方式与来源版本", "区分采访者措辞与受访者措辞", "识别相反证据：现有按交易类型分类"])

G("G005", "Be able to set and change spending limits on the debit card through the website.",
  ["强诉求：'something I'd really like to have'、'I would like to see that feature'、'honestly upset that they haven't added it'", "仅针对网站端：T025 显示移动 app 可设置卡片参数/每日上限（且带 'I believe'），T035 确认网站端缺少专门选项", "条件/例外：多数资金在未绑定借记卡的储蓄账户，故该限额当前不会触发；但'希望将来某时使用'，且曾在以前的信用卡/借记卡上用过", "T028 的'每笔 100 美元'为采访者任务数值，不作为本目标内容"],
  ["q26", "q25", "q27", "q28", "q23"], "direct",
  "T037 明确表达想在网站拥有该限额功能并希望看到它被加入；T035 确认网站无专门选项。条件与例外（资金在储蓄账户、未来使用、曾用过）逐项保留在 context，未把任务数值写入目标。",
  ["在网站端拥有设置/修改借记卡限额的功能"])

G("G006", "Have Zelle implemented on the web app so the user does not have to reach for the phone every time.",
  ["诉求：'I would like to see them implement Zelle on the web app'", "理由：更方便、'so that I don't have to reach my phone every time'", "'My only concern is that it does not have Zelle'（T045）", "T041：'I don't think we can ... sell [Zelle] on of the web app'，向他人转账需知道对方账号", "背景：受访者平时用移动 app，本次首次使用网站（T012/T013）"],
  ["q30", "q32", "q29"], "direct",
  "T045 直接表达希望在 web app 实现 Zelle 及其理由，T041 与 T045 的'only concern'确认网站端缺 Zelle；主体/对象/理由一致。",
  ["在 web app 上实现 Zelle 以免每次去拿手机"])

G("G007", "Have a chat/text-based support interface (chatting with a bank representative, or an AI bot) available on the website.",
  ["偏好/建议强度：'would be a great option'、'that'd be a great feature'，非强制", "理由：比电话更放松、'not really anxiety inducing'、可一边发消息一边处理其他事", "明确选定的方式之一：'through an AI bot'；尤其面向'people who don't exactly know how to get around the website'，可直接问 AI bot 并得到回复", "信念/让步：'I believe there are a few limitations as to why they can't add it'", "T053：网站现有替代方式为预约会议、发消息、找网点、打电话，无文字/聊天通道"],
  ["q34", "q35", "q36", "q37", "q38", "q33"], "inferred",
  "受访者以偏好/习惯（'I am very used to having a chat based interface'、'would be a great option/feature'）表达对网站聊天支持的期望，需由偏好与 T053 的'缺少聊天通道'缺口推断为一项产品诉求；方式与受益人群在原文明确选定并保留于 context。",
  ["偏好聊天式支持及其放松/可多任务处理的理由", "网站目前无文字/聊天联系银行的通道", "AI 机器人方式及面向不熟悉网站者的条件"],
  assumptions=["受访者的个人偏好可视为对网站功能的有依据诉求", "'a few limitations'为信念性可行性顾虑，不否定诉求本身"],
  steps=["由'used to / would be a great'的偏好与 T053 的缺口推断诉求", "核对方式、条件、强度与来源版本", "不把偏好升级为强制要求"],
  origin="inferred",
  inference={"basis_candidate_ids": [],
             "reason": "由 T055 对聊天式支持的偏好、T053 网站缺少文字/聊天通道的缺口，推断出'在网站提供聊天支持'这一产品诉求；推断直接依据原文，而非由其他目标派生。",
             "assumptions": ["个人使用习惯与'would be a great option'可视为对网站功能的有依据诉求"]})

G("G008", "Make the more important (niche) features, such as locking/unlocking the debit card, more accessible with fewer clicks on the website.",
  ["诉求：'some of the more important features should be more accessible'", "例证：为锁定/解锁借记卡'had to click like 7 or 8 times ... kind of bad design'", "让步/条件：'I understand that because I don't think people use that as often'", "总体：'I definitely don't feel better of the website'但'still stand by ... a very good ui'；主要功能（转账、查交易）'really good / accessible'", "T035 另提'it's not very intuitive. I would really like it to be a bit more better'"],
  ["q42", "q40", "q41", "q39", "q24"], "direct",
  "T059 直接陈述'一些更重要/小众功能应更易访问'，并以 7-8 次点击为例；让步（不常用、理解）与总体评价张力保留在 context。",
  ["让更重要/小众功能更易访问、减少点击"])

G("G009", "Be able to view all bank accounts, balances, deposits, withdrawals and recent transactions at a quick glance on the dashboard without going to multiple screens or extra clicks.",
  ["维持/避免型意图：'it's a good thing that I can ... look at all of my spends ... in a quick glance'、'don't really have to go to like multiple screens'", "T015：登录后的 dashboard 展示所有账户、各账户余额、存款与取款；下方还有近期交易小列表，'pretty convenient'、无需再点链接/按钮", "条件：在网站 dashboard 上（受访者首次使用网站）", "张力：这是对已实现能力的正面评价，brief 4.3 提示'已实现能力不自动成为要求'，但维持/避免型意图应保留"],
  ["q8", "q6", "q7"], "inferred",
  "该目标由对现有 dashboard 的正面评价推断为'维持一览能力、避免多屏/多次点击'的意图：原文以'it's a good thing'/'that's also good'/'pretty convenient'表达价值，并明确'don't really have to go to multiple screens'，属有正面依据支撑的维持/避免型意图；因原文是对已实现能力的评价而非新增要求，按 inferred 保留并在 context 标注该张力，不升级为强制诉求。",
  ["登录后 dashboard 集中展示所有账户/余额/存取款与近期交易", "可一眼查看所有花费、无需多屏或额外点击"],
  assumptions=["对已实现能力的正面评价可视为希望维持的状态"],
  steps=["由 T015 的正面评价与'无需多屏/额外点击'推断维持/避免型意图", "核对展示内容、条件与来源版本", "不把正面评价升级为新增强制要求"],
  origin="inferred",
  inference={"basis_candidate_ids": [],
             "reason": "由 T015 对登录后 dashboard 一览能力、近期交易列表及'无需多屏/额外点击'的正面评价，推断出维持该能力、避免多屏与额外点击的意图；推断直接依据原文，而非由其他目标派生。",
             "assumptions": ["对已实现能力的正面评价（'a good thing'/'pretty convenient'）可视为希望维持的状态"]})

# ---- ledger entries (exactly one per raw candidate) ----
entries = [
 {"candidate_id": "C001", "disposition": "split", "final_goal_ids": ["G001", "G002", "G003"], "reason": "T005 一句含三个独立动作/意图（Zelle 分摊、转储蓄赚利息、Apple Pay 付款），各有独立依据，拆成三个一目标一核心动作。"},
 {"candidate_id": "C002", "disposition": "exclude", "final_goal_ids": [], "reason": "Zelle 的定义与'好用'评价（T007），是对既有能力的说明，非达到/维持/避免类意图，不作为目标。"},
 {"candidate_id": "C003", "disposition": "keep", "final_goal_ids": ["G009"], "reason": "T015 复合评价的核心为维持'dashboard 一览、无需多屏/额外点击'，归入 G009；其余 UI 评价部分作为该目标证据保留。"},
 {"candidate_id": "C004", "disposition": "exclude", "final_goal_ids": [], "reason": "'It's perfect the way it is'（T017）为总体满意与让步，非可执行诉求；country-specific 让步亦排除。"},
 {"candidate_id": "C005", "disposition": "exclude", "final_goal_ids": [], "reason": "对另一应用（pays up）现成 plan and track 功能的比较性评价（T017），非本系统的新诉求。"},
 {"candidate_id": "C006", "disposition": "exclude", "final_goal_ids": [], "reason": "资金安全、2FA、通知与'安全实现程度未知'（T019）均为信念/评价与让步，非意图。"},
 {"candidate_id": "C007", "disposition": "exclude", "final_goal_ids": [], "reason": "对既有 plan and track 功能'which is good'的正面评价（T021），已实现能力不自动成为要求。"},
 {"candidate_id": "C008", "disposition": "keep", "final_goal_ids": ["G004"], "reason": "T021 的'想看到花费多少与去向的分解'是候选诉求，对应 G004；因措辞与能力不确定，保留为 insufficient，不升级。"},
 {"candidate_id": "C009", "disposition": "merge", "final_goal_ids": ["G004"], "reason": "T023 对现有按交易类型分类、缺少消费类别指示的观察，是 G004 的缺口/相反证据，合并进该目标作依据。"},
 {"candidate_id": "C010", "disposition": "merge", "final_goal_ids": ["G005"], "reason": "T025 关于移动 app 可设卡片参数/每日上限（带 'I believe'）是 G005 的范围对照，合并进该目标。"},
 {"candidate_id": "C011", "disposition": "exclude", "final_goal_ids": [], "reason": "T028 的'每笔 100 美元'为采访者任务设定数值，不是受访者稳定目标。"},
 {"candidate_id": "C012", "disposition": "merge", "final_goal_ids": ["G005"], "reason": "T035 网站缺少改限额选项、'not very intuitive'，是 G005 的缺口证据，合并进该目标。"},
 {"candidate_id": "C013", "disposition": "keep", "final_goal_ids": ["G005"], "reason": "T037 明确'想在网站拥有该限额功能'并带条件/例外，是 G005 的主要诉求来路。"},
 {"candidate_id": "C014", "disposition": "merge", "final_goal_ids": ["G006"], "reason": "T041 '网站不能 Zelle、转账需知道对方账号'是 G006 的缺口证据，合并进该目标。"},
 {"candidate_id": "C015", "disposition": "keep", "final_goal_ids": ["G006"], "reason": "T045 '希望在 web app 实现 Zelle 以免每次拿手机'是 G006 的主要诉求来路；转账功能好评部分作为证据保留。"},
 {"candidate_id": "C016", "disposition": "merge", "final_goal_ids": ["G007"], "reason": "T053 网站无文字/聊天联系银行的通道，是 G007 的缺口证据，合并进该目标。"},
 {"candidate_id": "C017", "disposition": "keep", "final_goal_ids": ["G007"], "reason": "T055 对聊天式支持的偏好、AI bot 方式与受益人群、可行性让步，是 G007 的主要诉求来路。"},
 {"candidate_id": "C018", "disposition": "keep", "final_goal_ids": ["G008"], "reason": "T059 '更重要功能应更易访问'及 7-8 次点击例证是 G008 的诉求来路；总体评价与让步保留在 context。"},
 {"candidate_id": "C019", "disposition": "exclude", "final_goal_ids": [], "reason": "T061 对既有投资/顾问功能的正面评价，未表达新增或改变诉求，已实现能力不自动成为要求。"},
 {"candidate_id": "C020", "disposition": "exclude", "final_goal_ids": [], "reason": "T040 '$1 转账'为采访者任务设定数值，不是受访者目标。"},
 {"candidate_id": "C021", "disposition": "exclude", "final_goal_ids": [], "reason": "T050 '仅限网站、请联系 agent'为采访者任务框架，不是受访者意图本身；其引发的讨论已由 G007 承接。"},
]

# ---- source checks (only important re-checked spans) ----
def SC(cid, qkeys, cids, gids, outcome, reason):
    return {"check_id": cid,
            "evidence_candidates": [{"source_id": Q[k][0], "quote": Q[k][1]} for k in qkeys],
            "candidate_ids": cids, "final_goal_ids": gids, "outcome": outcome, "reason": reason}

source_checks = [
 SC("S1", ["q1"], ["C001"], ["G001"], "represented", "回查 T005 主要用途原句，确认 G001 的 Zelle 分摊费用意图及主体/对象。"),
 SC("S2", ["q30", "q32"], ["C015"], ["G006"], "represented", "回查 T045 'implement Zelle on the web app'与'only concern'，确认 G006 诉求与理由。"),
 SC("S3", ["q17", "q18"], ["C008"], ["G004"], "represented", "回查 T021 'breakdown of how much I'm spending and where'与'not really sure'的能力不确定，确认 G004 保留 insufficient。"),
 SC("S4", ["q19", "q20"], ["C009"], ["G004"], "represented", "回查 T023 现有按交易类型分类、缺少 groceries/fuel 指示，作为 G004 的缺口/相反证据。"),
 SC("S5", ["q27"], ["C013"], ["G005"], "represented", "回查 T037 资金在储蓄账户、限额当前不触发的例外，确认 G005 保留条件/例外。"),
 SC("S6", ["q38"], ["C017"], ["G007"], "represented", "回查 T055 AI bot 方式与面向不熟悉网站者的条件，确认 G007 保留选定方式。"),
 SC("S7", ["q9"], ["C004"], [], "excluded", "回查 T017 'It's perfect the way it is'，确认其为总体满意/让步、非可执行诉求，C004 排除。"),
 SC("S8", ["q11"], ["C005"], [], "excluded", "回查 T017 对另一应用 plan and track 的评价，确认非本系统诉求，C005 排除。"),
 SC("S9", ["q22"], ["C011"], [], "excluded", "回查 T028 每笔 100 美元，确认是采访者任务数值，C011 排除。"),
 SC("S10", ["q44", "q45"], ["C019"], [], "excluded", "回查 T061 投资/顾问功能好评，确认无新增诉求，C019 排除。"),
]

# ---- review questions / limitations ----
review_questions = [
 {"candidate_ids": ["G004"], "question": "按消费类别的花费分解是否应作为受访者本人目标，还是仅为对采访者措辞的附和？",
  "reason": "'data analysis / expense categories'来自采访者 T020，受访者用'I think it would be great'且自述不确定现有跟踪能力。"},
 {"candidate_ids": ["G007"], "question": "聊天/文字支持是否应升格为强要求？",
  "reason": "原文仅为偏好强度（'would be a great option/feature'），并含'a few limitations as to why they can't add it'的让步。"},
 {"candidate_ids": ["G009"], "question": "对已实现 dashboard 的正面评价是否构成独立维持型目标？",
  "reason": "brief 4.3 提示已实现能力不自动成为要求，但维持/避免型意图应保留，二者存在张力。"},
 {"candidate_ids": [], "question": "是否遗漏了原文中其他达到/维持/避免类意图？",
  "reason": "逐窗捕获与全篇校正后仍需整体复核是否压薄或漏提；受访者多处表达'perfect the way it is'。"},
]

limitations = [
 "仅依据任务目录内 source/DOC004.json 的访谈转写与冻结技能，未联网、未参考任何历史目标/关系/评分或其他任务目录。",
 "原文为 ASR 转写，含口语重复、断句与 'sell'/'cell'（Zelle）等拼写噪声；引文逐字符取自原文，未做规范化或改写。",
 "Read 工具曾把 T043 截断，已改用脚本读取完整 67 轮文本核对；本次以完整原文为准。",
 "覆盖记录、支持标签、联系与精化组为生成方编制与自检，未进行独立语义评审或形式化证明。",
 "采访者任务数值（T028 每笔 100 美元、T040 的 $1 转账）视为任务设定，未写成受访者固定业务目标。",
 "G004 保留为 insufficient，其 blocking issue 属如实保留，不代表已解决。",
]

# ---- windows / passes ----
canonical, prepared = prepare(HERE / "source" / "DOC004.json")
windows_obj = build_windows(prepared, canonical, 4, 2, digest(encode(prepared)))
window_ids = [w["window_id"] for w in windows_obj["windows"]]
window_results = [
 {"window_id": w["window_id"], "status": "processed",
  "reason": "按 4/2 逐窗捕获本窗 " + "、".join(s.split(":", 1)[1] for s in w["source_ids"]) + " 的意图，未预先压缩；候选来路见 raw_candidates 与 entries。"}
 for w in windows_obj["windows"]]

passes = [{"pass_id": "P1", "kind": "initial", "context": "isolated", "status": "completed",
           "window_results": window_results}]

# ---- decisions ----
questions = [
 {"target_type": "goal", "target_id": "G004",
  "message": "按消费类别的数据分析/有价值的洞察措辞来自采访者，需确认是否为受访者本人需求；受访者亦自述不确定系统是否已按消费类别跟踪。"},
 {"target_type": "goal", "target_id": "G007",
  "message": "网站聊天支持由偏好与建议强度推断，且受访者自述存在可行性限制，需确认是作为正式要求还是仅保留为偏好。"},
 {"target_type": "goal", "target_id": "G009",
  "message": "该目标由对现有 dashboard 的正面评价推断为维持/避免型意图，需确认已实现能力的正面评价是否应保留为独立目标。"},
 {"target_type": "model", "target_id": "DOC004-goal-model",
  "message": "本次未建立任何独立联系或 AND 精化组，需复核是否存在被遗漏、且两端均有依据的 contribution/operationalization 联系或可声称共同满足的精化组。"},
]

decisions = {"relations": [], "groups": [], "questions": questions, "reassessments": []}

# ---- assemble spec ----
spec = {
 "schema_version": "goalforge-extraction-3",
 "document_id": "DOC004",
 "status": "completed",
 "omissions": [],
 "raw_candidates": raw,
 "goals": goals,
 "review_questions": review_questions,
 "limitations": limitations,
 "ledger": {
   "model": "unknown", "temperature": "unknown", "budget": "1 initial pass + <=2 repair rounds",
   "usage": "unknown", "skill_revision": MANIFEST_SHA, "prompt_revision": "task-prompt-v1",
   "planned_passes": 1,
   "stop_reason": "已完成 67 轮逐窗（4/2）捕获、全篇校正与一目标一核心动作整理；不存在可声称共同满足的 AND 精化组，亦无两端均有依据的独立联系，故 relations/groups 为空；G004 保留为 insufficient，停止。",
   "passes": passes,
   "full_context_review": {
     "status": "completed",
     "reason": "回看全部 67 轮：校正 'sell/cell'→Zelle 的指代、plan and track 与按消费类别分析的区分、T025（移动 app）与 T035/T037（网站）的范围差异、T037 的条件/例外、T055 的让步、T059 的评价张力，以及 T023 的相反证据（现有按交易类型分类）。"},
   "entries": entries,
   "source_checks": source_checks,
 },
 "decisions": decisions,
}

# ---- local structural pre-flight ----
def preflight():
    rids = [c["candidate_id"] for c in raw]
    gids = [g["candidate_id"] for g in goals]
    assert len(rids) == len(set(rids)), "duplicate raw id"
    assert len(gids) == len(set(gids)), "duplicate goal id"
    eids = [e["candidate_id"] for e in entries]
    assert set(eids) == set(rids), "entries must cover every raw candidate"
    from collections import Counter
    tcount = Counter(g for e in entries for g in e["final_goal_ids"])
    for e in entries:
        d, t = e["disposition"], e["final_goal_ids"]
        assert d in {"keep", "merge", "split", "exclude", "uncertain", "pending"}
        assert set(t) <= set(gids), "unknown final goal " + e["candidate_id"]
        if d == "pending":
            assert not t
        else:
            assert e["reason"].strip()
            if d in {"keep", "merge"}:
                assert len(t) == 1, e["candidate_id"]
            if d == "merge":
                assert tcount[t[0]] >= 2, e["candidate_id"] + " merge needs >=2 sources"
            if d == "split":
                assert len(t) >= 2, e["candidate_id"]
            if d == "exclude":
                assert not t, e["candidate_id"]
    for g in gids:
        assert tcount[g] >= 1, "goal without provenance: " + g
    for g in goals:
        lab = g["judgment"]["label"]
        assert lab in {"direct", "inferred", "insufficient", "contradicted"}
        if lab in {"direct", "inferred"}:
            assert g["judgment"]["unsupported_parts"] == [], g["candidate_id"] + " direct/inferred has unsupported_parts"
        if g["origin"] == "inferred":
            assert g["inference"] and g["inference"]["reason"].strip(), g["candidate_id"]
            assert set(g["inference"]["basis_candidate_ids"]) <= set(gids)
        else:
            assert g["inference"] is None, g["candidate_id"] + " explicit origin must have inference=None"
    for c in source_checks:
        assert set(c["candidate_ids"]) <= set(rids)
        assert set(c["final_goal_ids"]) <= set(gids)
        assert c["outcome"] in {"represented", "excluded", "uncertain"}
        if c["outcome"] == "represented":
            assert c["final_goal_ids"]
        if c["outcome"] == "excluded":
            assert not c["final_goal_ids"]
        if c["candidate_ids"] and c["final_goal_ids"]:
            mapped = {g for cid in c["candidate_ids"] for g in next(e for e in entries if e["candidate_id"] == cid)["final_goal_ids"]}
            assert set(c["final_goal_ids"]) <= mapped, c["check_id"] + " contradicts dispositions"
    for q in questions:
        assert q["target_type"] in {"goal", "group", "relation", "model"}
        if q["target_type"] == "goal":
            assert q["target_id"] in gids
        elif q["target_type"] == "model":
            assert q["target_id"] == "DOC004-goal-model"
        assert q["message"].strip()
    for q in review_questions:
        assert set(q["candidate_ids"]) <= set(gids)
    assert len(window_results) == 33, "window count"
    print("preflight: structure OK | raw=%d goals=%d entries=%d checks=%d windows=%d" %
          (len(raw), len(goals), len(entries), len(source_checks), len(window_results)))
    from collections import Counter as C2
    print("dispositions:", dict(C2(e["disposition"] for e in entries)))
    print("support labels:", dict(C2(g["judgment"]["label"] for g in goals)))


if __name__ == "__main__":
    verify_quotes()
    preflight()
    out = HERE / "spec.json"
    out.write_text(json.dumps(spec, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print("wrote", out, "bytes:", out.stat().st_size)
