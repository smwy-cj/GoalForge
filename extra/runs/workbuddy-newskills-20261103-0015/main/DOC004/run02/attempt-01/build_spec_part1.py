import json, sys, unicodedata

SRC = "source/DOC004.json"
doc = json.load(open(SRC, encoding="utf-8"))
turns = {t["source_id"]: t["text"] for t in doc["turns"]}


def ev(sid, quote, role="basis"):
    assert quote in turns[sid], "MISSING in %s: %r" % (sid, quote)
    return {"source_id": sid, "quote": quote, "role": role}


def cand(cid, statement, actor, modality, context, origin, evidence):
    return {"candidate_id": cid, "statement": statement, "actor": actor,
            "modality": modality, "context": context, "origin": origin,
            "pass_id": "P1", "evidence": evidence}


def goal(gid, statement, context, origin, evidence, label, rationale, supported):
    return {"candidate_id": gid, "statement": statement, "actor": "Stakeholder",
            "context": context, "origin": origin, "inference": None,
            "evidence": evidence,
            "judgment": {"label": label, "rationale": rationale,
                         "supported_parts": supported, "unsupported_parts": [],
                         "assumptions": [], "reasoning_steps": []}}


raw = []
raw.append(cand("C001",
    "Uses the mobile app mainly to send Zelle payments to a few friends and split shared costs.",
    "Stakeholder", "reported habit", [], "explicit",
    [ev("DOC004:T005", "the main reason I use the app is to do sell payments to like a few of my friends. Basically split split costs and all of that.")]))
raw.append(cand("C002",
    "Normally moves surplus checking funds to the savings account so the balance earns interest.",
    "Stakeholder", "reported habit", ["Separate savings and checking accounts at the same bank"], "explicit",
    [ev("DOC004:T005", "so I normally transfer it over to my savings, so I can get even that little bit of interest I normally get.")]))
raw.append(cand("C003",
    "Uses Apple Pay linked to Chase at grocery stores and other outlets.",
    "Stakeholder", "reported habit", [], "explicit",
    [ev("DOC004:T005", "So I use apple pay, and then using that any like target or something.")]))
raw.append(cand("C004",
    "Zelle transfers small amounts instantly between accounts by phone number, so quick payments to friends or family are easy.",
    "Stakeholder", "feature description", [], "explicit",
    [ev("DOC004:T007", "So Zelle is basically like a way to instantaneously transfer small amounts of money between, let's say, 2 different accounts just based on their phone number.")]))
raw.append(cand("C005",
    "Agrees to perform a small Zelle payment during the interview.",
    "Stakeholder", "agreement with interviewer request", [], "explicit",
    [ev("DOC004:T009", "Of course. Yeah, I can. I can do that. That's not a problem.")]))
raw.append(cand("C006",
    "Dashboard shows all accounts, their balances, deposits and withdrawals, and a short recent-transactions list, so spending can be seen at a glance without multiple screens.",
    "Stakeholder", "positive description of current state", [], "explicit",
    [ev("DOC004:T015", "So everything is presented to me in in sort of like this dashboard when I sign in."),
     ev("DOC004:T015", "So it's a good thing that I can like. Just look at all of my spends on like in like a quick glance, and don't really have to go to like multiple screens to check all of that"),
     ev("DOC004:T015", "They also have a very small list of all the transactions, like all the recent transactions. So again, that's also good.")]))
raw.append(cand("C007",
    "Website UI is similar to the mobile app, properly laid out, good and functional.",
    "Stakeholder", "aesthetic evaluation", [], "explicit",
    [ev("DOC004:T015", "the overall ui of the website is very similar to the mobile app itself.")]))
raw.append(cand("C008",
    "The website is perfect as it is and handles everything a banking application should handle.",
    "Stakeholder", "overall satisfaction", [], "explicit",
    [ev("DOC004:T017", "Honestly. It's perfect the way it is.")]))
raw.append(cand("C009",
    "Plan and track feature lets the user set monetary goals and track progress against them.",
    "Stakeholder", "feature praise", [], "explicit",
    [ev("DOC004:T017", "they also have like this plan and track feature where you can like track like, you can basically set monetary goals. And then track how you're doing that.")]))
raw.append(cand("C010",
    "Two-factor authentication is required when signing in for the first time from a new laptop.",
    "Stakeholder", "feature praise", ["First sign-in from an unfamiliar device"], "explicit",
    [ev("DOC004:T019", "So it. They had this whole 2 factor thing authentication thing set up like from the get go. So that was good.")]))
raw.append(cand("C011",
    "A notification is sent to the phone for every transaction and the user can contest it.",
    "Stakeholder", "feature praise", [], "explicit",
    [ev("DOC004:T019", "because, like every time I do a transaction. I get a notification on my phone saying that this much amount of money has been spent, and then I can also contest it, which is great.")]))
raw.append(cand("C012",
    "Feels funds are safe and customer-facing security is good.",
    "Stakeholder", "general trust statement", [], "explicit",
    [ev("DOC004:T019", "I would say it's really secure, because, like, while I was signing in.")]))
raw.append(cand("C013",
    "Would like a breakdown of how much is spent and where, by expense category.",
    "Stakeholder", "explicit wish", [], "explicit",
    [ev("DOC004:T021", "But apart from that, I don't really think it gives me like a breakdown of how much I'm spending and where. So I I think that it would be great to see something like that."),
     ev("DOC004:T021", "So I believe it's pretty easy to like categorize what we are spending on. And then I think it would be like a very valuable insight.")]))
raw.append(cand("C014",
    "Plan and track keeps track of monthly spending and income and states how much to earn and spend to hit a goal by a timeframe.",
    "Stakeholder", "feature praise", [], "explicit",
    [ev("DOC004:T021", "So it lets me set a goal and then tells me how much exactly I'm supposed to be earning, and are spending every month to make sure I hit that goal by a specified timeframe which is good")]))
raw.append(cand("C015",
    "Transactions are only categorized by type (card, Zelle, fee, account transfer); there is no indicator for groceries or fuel.",
    "Stakeholder", "observation of gap", [], "explicit",
    [ev("DOC004:T023", "But apart from that, it doesn't have any other sort of indicator to show that I've let's say, spend it on groceries or on fuel, or something like that.")]))
raw.append(cand("C016",
    "The transaction list shows how much was spent, where, at what time, and the balance at that point.",
    "Stakeholder", "feature description", [], "explicit",
    [ev("DOC004:T023", "So as I scroll down I just see what how much is spent, and where. and at what time? And what is the balance at that point in time?")]))
raw.append(cand("C017",
    "Debit card settings in the app let the user set card parameters and the maximum limit per day, and are easy to access.",
    "Stakeholder", "feature description", [], "explicit",
    [ev("DOC004:T025", "Lets me basically set different kind of parameters that I want in the card, or like change, how much like, what's the Max limit per day, and all of that?"),
     ev("DOC004:T025", "So that is pretty straightforward. And then like very easy to access.")]))
raw.append(cand("C018",
    "Uses the bank's service to control debit card access, for example blocking certain kinds of transactions or setting a transaction limit.",
    "Stakeholder", "confirmation of capability", [], "explicit",
    [ev("DOC004:T024", "if you ever use the bank's service to control your debit card access, like, maybe let's say, blocking certain kinds of transactions or setting a transaction limit"),
     ev("DOC004:T025", "Great. Yeah, of course. So I can. I can do that in the in the app, I believe.")]))
raw.append(cand("C019",
    "Asked to restrict the online spend limit to one hundred dollars per transaction.",
    "Stakeholder", "interviewer-assigned task, accepted", [], "explicit",
    [ev("DOC004:T028", "Let's try and restrict your online spend limit to. let's say, a hundred dollars per transaction."),
     ev("DOC004:T029", "Yeah, yeah, of course, of course I can. I can do that.")]))
raw.append(cand("C020",
    "Does not see a separate column to set transaction limits on the website.",
    "Stakeholder", "observation of gap", [], "explicit",
    [ev("DOC004:T033", "but I don't see like a separate column to like set limits my transaction")]))
raw.append(cand("C021",
    "Card controls are not very intuitive and should be better.",
    "Stakeholder", "criticism with improvement wish", [], "explicit",
    [ev("DOC004:T035", "Yeah, so obviously, it's not very intuitive. I would really like it to be a bit more better. though.")]))
raw.append(cand("C022",
    "No specific option to change card limits; the site only offers lock and unlock, replace card, and a new PIN.",
    "Stakeholder", "observation of gap", [], "explicit",
    [ev("DOC004:T035", "So yeah, I don't think I don't think they really have like a specific option where I can, like, you know. change my change the limits on the card per se, yeah.")]))
raw.append(cand("C023",
    "Would really like to have the card limit feature and is upset that a bank this size has not added it.",
    "Stakeholder", "explicit wish", [], "explicit",
    [ev("DOC004:T037", "So I would like to see that feature, and it's honestly upset that they haven't added it to this, considering it's such a huge bank.")]))
raw.append(cand("C024",
    "Most funds sit in the savings account, which is not tied to the debit card, so a card limit would not bind today.",
    "Stakeholder", "reason for not needing the feature yet", [], "explicit",
    [ev("DOC004:T037", "most of my funds are in my savings account, which is not tied to my debit card anyway.")]))
raw.append(cand("C025",
    "Zelle is not available on the web app; transferring to another person requires knowing their account number.",
    "Stakeholder", "observation of gap", [], "explicit",
    [ev("DOC004:T041", "I don't think Zelle is I don't think we can sell on of the web app.")]))
raw.append(cand("C026",
    "Transfer entry points on the dashboard are super accessible.",
    "Stakeholder", "feature praise", [], "explicit",
    [ev("DOC004:T041", "So there are columns that says, transfer money on each of the accounts, so I could click on either of them.")]))
raw.append(cand("C027",
    "Scheduled transfer lets the user choose from and to accounts, amount, transfer date and a note.",
    "Stakeholder", "feature description during task", [], "explicit",
    [ev("DOC004:T043", "And there's also notice self. So just to keep note of what this transfer exactly is, for there's also an option for setup, repeated transfers.")]))
raw.append(cand("C028",
    "Before submitting, the site asks the user to confirm that everything looks okay.",
    "Stakeholder", "feature praise during task", [], "explicit",
    [ev("DOC004:T043", "So then it tells me it asks me if everything looks okay. So just to confirm which is a great detail.")]))
raw.append(cand("C029",
    "Schedules a one-dollar transfer from checking to savings for the current day.",
    "Stakeholder", "task execution", [], "explicit",
    [ev("DOC004:T043", "So it's scheduled to transfer of one dollars to my savings account now.")]))
raw.append(cand("C030",
    "Wants Zelle implemented on the web app for convenience, without reaching for the phone.",
    "Stakeholder", "explicit wish", [], "explicit",
    [ev("DOC004:T045", "I would like to see them implement Zelle on on the web app because I think it. It'll just be more convenient, so that I don't have to like reach. Reach my phone every time.")]))
raw.append(cand("C031",
    "Account transfer on the web app is great and super intuitive.",
    "Stakeholder", "feature praise", [], "explicit",
    [ev("DOC004:T045", "if you just wanna do an account transfer. Then it's great, because, like, it's super intuitive")]))
raw.append(cand("C032",
    "The transfer flow makes sure the wrong amount or the wrong person is not used.",
    "Stakeholder", "feature praise", [], "explicit",
    [ev("DOC004:T045", "and then it makes sure that you don't send the wrong amount, or like to the wrong person.")]))
raw.append(cand("C033",
    "Transfer can be scheduled and repeated, so it does not have to be redone again and again.",
    "Stakeholder", "feature praise", [], "explicit",
    [ev("DOC004:T045", "and then it lets you schedule properly. It also lets you repeat the transactions is a great, so you don't have to come and keep on doing it again and again.")]))
raw.append(cand("C034",
    "No way to text or chat with a bank person on the website; the options are calling or scheduling a meeting.",
    "Stakeholder", "observation of gap", [], "explicit",
    [ev("DOC004:T053", "but I don't see like a way to like text or like chat with a with a bank manager like someone in the bank, like on through text through the website.")]))
raw.append(cand("C035",
    "No help entry is visible on the dashboard or footers; help and support is reached through the hamburger menu.",
    "Stakeholder", "observation of gap", [], "explicit",
    [ev("DOC004:T053", "I I don't even see anything on the footers for help. So that's interesting.")]))
raw.append(cand("C036",
    "Prefers a chat-based support interface: more relaxing, less anxiety-inducing than a call, and allows multitasking.",
    "Stakeholder", "stated preference", [], "explicit",
    [ev("DOC004:T055", "Normally. I am very used to having a chat based interface when it comes to support, because it lets I don't know. It's just more relaxing."),
     ev("DOC004:T055", "It's not really it doesn't. It's not really anxiety inducing as much as the call."),
     ev("DOC004:T055", "So and I can like multitask while texting like, let's say, the bank representative. So that would be a great option.")]))
raw.append(cand("C037",
    "An AI bot that users who do not know their way around the website can text for answers would be great.",
    "Stakeholder", "explicit wish", [], "explicit",
    [ev("DOC004:T055", "But for, let's say, people who who don't exactly know how to get around the website. It'd be great to just like text the AI bot. And then, like, get responses and all of that.")]))
raw.append(cand("C038",
    "Believes there are limitations that explain why chat support has not been added.",
    "Stakeholder", "belief about constraints", [], "explicit",
    [ev("DOC004:T055", "But obviously, I believe there are like a few limitations as to why they can't add it.")]))
raw.append(cand("C039",
    "Main daily functions such as transferring money and checking transactions are really good and accessible.",
    "Stakeholder", "overall evaluation", [], "explicit",
    [ev("DOC004:T059", "most of the actions that I was doing I would be doing on a daily basis, which includes like transferring money and checking my transactions and all of that.")]))
raw.append(cand("C040",
    "Locking or unlocking the debit card took seven or eight clicks; important features should be more accessible.",
    "Stakeholder", "criticism with improvement wish", [], "explicit",
    [ev("DOC004:T059", "I had to click. I I think I had to click like 7 or 8 times to even get to locking or unlocking my debit card, which is. which is honestly kind of bad design."),
     ev("DOC004:T059", "But although I think, like some of the more important features should be more accessible.")]))
raw.append(cand("C041",
    "One-to-one access to an investment advisor is a really good feature for people who do not know where to start investing.",
    "Stakeholder", "feature praise", ["User is new to investing"], "explicit",
    [ev("DOC004:T061", "you can have a 1 to one with an advisor which is a really good features. Be really good feature, because if you're not, if you don't know where to start investing, you can like talk to someone.")]))
raw.append(cand("C042",
    "The J.P. Morgan partnership lets users open a trading account and trade directly.",
    "Stakeholder", "feature description", [], "explicit",
    [ev("DOC004:T061", "So I believe they've they had. They're partnered with Jp. Morgan. So they let you open and like open a trading account, and then trade directly")]))

goals = []
goals.append(goal("G001",
    "Send instant Zelle payments of small amounts to friends and family by phone number, so shared costs can be split quickly.",
    ["Payments are small and between people who already know each other's phone number"],
    "explicit",
    [ev("DOC004:T005", "the main reason I use the app is to do sell payments to like a few of my friends. Basically split split costs and all of that."),
     ev("DOC004:T007", "So Zelle is basically like a way to instantaneously transfer small amounts of money between, let's say, 2 different accounts just based on their phone number.")],
    "direct",
    "受访者直接说明使用 App 的主要目的就是向朋友做 Zelle 小额转账以分摊费用，并说明该方式按手机号即时、小额；主体、对象与用途一致。",
    ["主要用途：向朋友 Zelle 转账并分摊费用", "小额、即时、按手机号发起", "对象为朋友或家人"]))
goals.append(goal("G002",
    "Offer Zelle payments on the website so small payments to friends can be sent from a laptop without reaching for the phone.",
    [],
    "explicit",
    [ev("DOC004:T045", "I would like to see them implement Zelle on on the web app because I think it. It'll just be more convenient, so that I don't have to like reach. Reach my phone every time."),
     ev("DOC004:T041", "I don't think Zelle is I don't think we can sell on of the web app.")],
    "direct",
    "T045 明确表达希望网页端实现 Zelle，理由是不必每次都去拿手机；T041 说明当前网页端没有 Zelle。诉求、渠道与理由均与表述一致。",
    ["希望在网页端提供 Zelle", "理由是更方便、无需拿手机", "当前网页端缺少该功能"]))
goals.append(goal("G003",
    "Transfer surplus funds from the checking account to the savings account on the website so the balance earns interest.",
    ["The user holds a checking and a savings account at the same bank"],
    "explicit",
    [ev("DOC004:T005", "so I normally transfer it over to my savings, so I can get even that little bit of interest I normally get."),
     ev("DOC004:T045", "if you just wanna do an account transfer. Then it's great, because, like, it's super intuitive")],
    "direct",
    "T005 说明习惯把闲置资金转入储蓄以赚取利息；T045 正面评价网页版账户转账“super intuitive ... great”。行为、对象与目的均有直接依据。",
    ["在自有账户间转账（支票→储蓄）", "目的是赚取利息", "网页端账户转账被正面评价"]))
goals.append(goal("G004",
    "Keep all accounts, their balances, deposits and withdrawals, and the latest transactions visible together on the dashboard so spending can be checked at a glance without opening several screens.",
    [],
    "inferred",
    [ev("DOC004:T015", "So everything is presented to me in in sort of like this dashboard when I sign in."),
     ev("DOC004:T015", "So it's a good thing that I can like. Just look at all of my spends on like in like a quick glance, and don't really have to go to like multiple screens to check all of that"),
     ev("DOC004:T015", "They also have a very small list of all the transactions, like all the recent transactions. So again, that's also good.")],
    "inferred",
    "受访者描述仪表盘同时呈现账户、余额、存取与近期交易，并明确“不必切多个屏”“不必再点链接”是优点。原文未提出改动要求，属对现状的正面评价，故按维持意图推断。",
    ["账户、余额、存取与近期交易同屏呈现", "一屏即可查看支出，无需切换多屏"]))
goals.append(goal("G005",
    "Keep the plan-and-track view that lets the user set a monetary goal and shows the monthly earning and spending needed to reach it by a chosen timeframe.",
    [],
    "inferred",
    [ev("DOC004:T021", "So it lets me set a goal and then tells me how much exactly I'm supposed to be earning, and are spending every month to make sure I hit that goal by a specified timeframe which is good"),
     ev("DOC004:T017", "they also have like this plan and track feature where you can like track like, you can basically set monetary goals. And then track how you're doing that.")],
    "inferred",
    "T021 描述 plan and track 可设定货币目标并给出每月应收支额度，且评价“which is good ... helps me keep on track”；T017 亦称该功能使手机端更好。属正面评价的维持意图，原文未要求改动。",
    ["可设定货币目标与期限", "给出每月应赚取/支出的额度", "正面评价其帮助控制支出"]))
goals.append(goal("G006",
    "Break down spending by expense category, such as groceries or fuel, so users can see where their money goes.",
    [],
    "explicit",
    [ev("DOC004:T021", "But apart from that, I don't really think it gives me like a breakdown of how much I'm spending and where. So I I think that it would be great to see something like that."),
     ev("DOC004:T023", "But apart from that, it doesn't have any other sort of indicator to show that I've let's say, spend it on groceries or on fuel, or something like that.")],
    "direct",
    "T021 明确提出希望看到按类别分解的支出，T023 指出当前只按交易类型分类、缺少 grocery 或 fuel 标识。诉求与缺口均直接对应。",
    ["希望看到支出分类明细", "当前只有交易类型分类", "示例类别为 grocery 与 fuel"]))
goals.append(goal("G007",
    "Let the user set a per-transaction spending limit on the debit card from the website.",
    ["Limit applies to the debit card linked to the checking account",
     "Most funds sit in the savings account, which is not tied to the debit card, so the limit would rarely bind today"],
    "explicit",
    [ev("DOC004:T037", "So I would like to see that feature, and it's honestly upset that they haven't added it to this, considering it's such a huge bank."),
     ev("DOC004:T035", "So yeah, I don't think I don't think they really have like a specific option where I can, like, you know. change my change the limits on the card per se, yeah."),
     ev("DOC004:T025", "Lets me basically set different kind of parameters that I want in the card, or like change, how much like, what's the Max limit per day, and all of that?")],
    "direct",
    "T037 明确希望拥有该功能并抱怨缺失，T035 指出没有修改卡片限额的入口，T025 说明 App 内可设卡片参数与每日上限。诉求、对象与渠道（网页端）一致，储蓄账户条件已记入 context。",
    ["希望能在网页端设置卡片限额", "当前网页端找不到限额入口", "App 内可设每日上限"]))
goals.append(goal("G008",
    "Make important debit card features such as locking or unlocking the card more accessible on the website, so they do not take seven or eight clicks to reach.",
    [],
    "explicit",
    [ev("DOC004:T059", "I had to click. I I think I had to click like 7 or 8 times to even get to locking or unlocking my debit card, which is. which is honestly kind of bad design."),
     ev("DOC004:T059", "But although I think, like some of the more important features should be more accessible."),
     ev("DOC004:T035", "Yeah, so obviously, it's not very intuitive. I would really like it to be a bit more better. though.")],
    "direct",
    "T035 称卡片控制“not very intuitive，希望更好”，T059 具体指出锁卡需七到八次点击且“重要功能应更易达”。诉求、对象与量化问题均有直接依据。",
    ["卡片控制不直观，希望改进", "锁卡需 7 至 8 次点击", "重要功能应更易达"]))
goals.append(goal("G009",
    "Keep the review-and-confirm step before a transfer is submitted, so the wrong amount or the wrong recipient is not sent.",
    [],
    "inferred",
    [ev("DOC004:T043", "So then it tells me it asks me if everything looks okay. So just to confirm which is a great detail."),
     ev("DOC004:T045", "and then it makes sure that you don't send the wrong amount, or like to the wrong person.")],
    "inferred",
    "两处均正面评价确认步骤（“a great detail”“makes sure that you don't send the wrong amount ...”），并给出防错目的。原文未提出改动，按维持意图推断。",
    ["提交前确认金额与对象", "目的为避免金额或对象出错"]))
goals.append(goal("G010",
    "Let the user schedule a transfer for a chosen date and set it to repeat so recurring payments do not have to be entered again each time.",
    [],
    "inferred",
    [ev("DOC004:T045", "and then it lets you schedule properly. It also lets you repeat the transactions is a great, so you don't have to come and keep on doing it again and again."),
     ev("DOC004:T043", "there's also an option for setup, repeated transfers. That's that I'm assuming is for like stuff like rent or utilities.")],
    "inferred",
    "T045 称赞可正常排程、可重复且“不用一遍遍来做”；T043 记录了日期、备注与重复设置的操作。原文为正面描述而非新要求，按维持意图推断；日期与频率属同一排程动作的限定，未拆成多目标。",
    ["可按选定日期排程转账", "可设置重复转账", "目的为免除反复手工录入"]))
goals.append(goal("G011",
    "Keep two-factor authentication when the user signs in from a new device, as an extra layer of security.",
    ["Sign-in from a device or browser not used before"],
    "inferred",
    [ev("DOC004:T019", "So it. They had this whole 2 factor thing authentication thing set up like from the get go. So that was good.")],
    "inferred",
    "受访者描述首次在笔记本登录即触发两步验证，并评价这是“additional layer of security”“that was good”。属正面评价的维持意图，条件（新设备首登）已记入 context。",
    ["新设备首次登录触发两步验证", "被视为额外的安全层"])"))
goals.append(goal("G012",
    "Notify the user on their phone of every transaction and let them contest it, so unauthorized spending can be caught.",
    [],
    "inferred",
    [ev("DOC004:T019", "because, like every time I do a transaction. I get a notification on my phone saying that this much amount of money has been spent, and then I can also contest it, which is great.")],
    "inferred",
    "原句描述每笔交易都有手机通知且可申诉，并评价“which is great”，目的是资金安全。通知与申诉被视为同一交易提醒闭环的两个环节，未拆分；属维持意图推断。",
    ["每笔交易发送手机通知", "可就交易提出申诉", "目的为发现未授权支出"]))
goals.append(goal("G013",
    "Offer text chat with a bank representative on the website, so support is less anxiety-inducing than a call and can be handled while doing something else.",
    [],
    "explicit",
    [ev("DOC004:T055", "So and I can like multitask while texting like, let's say, the bank representative. So that would be a great option."),
     ev("DOC004:T055", "It's not really it doesn't. It's not really anxiety inducing as much as the call."),
     ev("DOC004:T053", "but I don't see like a way to like text or like chat with a with a bank manager like someone in the bank, like on through text through the website.")],
    "direct",
    "T055 明确说聊天式支持“would be a great option”，并给出少焦虑、可多任务的理由；T053 指出网页端没有文字聊天入口。诉求与理由均有直接依据。",
    ["希望网页端提供与银行人员文字聊天", "理由是比电话少焦虑、可多任务", "当前只有电话或预约"])"))
goals.append(goal("G014",
    "Offer an AI-bot text channel for users who do not know their way around the website, so they can get answers by text.",
    [],
    "explicit",
    [ev("DOC004:T055", "But for, let's say, people who who don't exactly know how to get around the website. It'd be great to just like text the AI bot. And then, like, get responses and all of that.")],
    "direct",
    "原句明确对不熟悉网站的用户“text the AI bot ... would be great”，并说明可获得回应。对象、渠道与目的与表述一致；与人工聊天是否属同一目标的替代方式留作问题。",
    ["面向不熟悉网站的用户", "以 AI 机器人文字对话获取回应", "属提议强度（would be great）"]))
goals.append(goal("G015",
    "Keep one-to-one access to an investment advisor, so a beginner can talk to someone before investing instead of losing money while learning.",
    ["The user is new to investing"],
    "inferred",
    [ev("DOC004:T061", "you can have a 1 to one with an advisor which is a really good features. Be really good feature, because if you're not, if you don't know where to start investing, you can like talk to someone."),
     ev("DOC004:T061", "And instead of like losing a lot of money, you know, you could talk to someone who actually knows what they're doing")],
    "inferred",
    "受访者称一对一顾问“a really good feature”，理由是初学者可先咨询以避免亏钱。原文未表明本人要使用，也无改动要求，按对现状的正面评价推断为维持意图。",
    ["提供一对一投资顾问", "理由是初学者可先咨询、避免亏钱", "与交易账户开立同属投资功能"]))
