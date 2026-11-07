"""Build spec.json for DOC019 attempt-01 (author-side semantic content)."""

import json
from pathlib import Path

A = Path(__file__).resolve().parent
DOC = json.loads((A / "source/DOC019.json").read_text(encoding="utf-8"))
TURNS = {t["source_id"]: t["text"] for t in DOC["turns"]}

SKILL_REV = "a5952d426b1624a3fcb2ce2829e1ae1ceb15e19dc3309d9571f3bc6b465deb6f"
WINDOW_COUNT = 32


def ev(sid, quote, role="basis"):
    text = TURNS[sid]
    n = text.count(quote)
    if n != 1:
        raise SystemExit(f"quote hits={n} in {sid}: {quote[:70]}")
    return {"source_id": sid, "quote": quote, "role": role}


def cand(cid, statement, actor, modality, context, origin, evidence, pass_id="P1"):
    return {"candidate_id": cid, "statement": statement, "actor": actor,
            "modality": modality, "context": context, "origin": origin,
            "pass_id": pass_id, "evidence": evidence}


raw = [
    cand("C001", "Understand the stakeholder's experience with investment and trading apps so the product team can design a better overall experience.",
         "Interviewer", "interview framing (explicit purpose statement)", ["研究访谈开场"],
         "explicit", [ev("DOC019:T003", "The goal here is to kind of understand your experience with these apps, and particularly in terms of what you use them for, what works well and what we could improve.")]),
    cand("C002", "Reports having used Kite, Binance and WazirX for stock and crypto exchanges.",
         "Stakeholder", "factual report", ["过往使用经历"], "explicit",
         [ev("DOC019:T004", "So I have used 0 the kite I have used binance and I have used an app called Moodrex")]),
    cand("C003", "Reports using no stock-trading app at present because he is in the US, and using Binance for crypto.",
         "Stakeholder", "factual report", ["当前居住地美国"], "explicit",
         [ev("DOC019:T008", "So for presently I for Stock exchanges, I'm not really using anything, because I'm in the Us.")]),
    cand("C004", "Came to understand finance through Zerodha's own academy web interface before starting to trade.",
         "Stakeholder", "factual report", ["入门学习路径"], "explicit",
         [ev("DOC019:T012", "Dha has their own sort of academy in which they have kind of a they have a web interface")]),
    cand("C005", "Be able to perform a trade in the least amount of time with the least amount of effort through a seamless exchange interface.",
         "Stakeholder", "stated preference (reason for choosing Binance)", ["比较 Binance 与其他加密应用时"], "explicit",
         [ev("DOC019:T016", "still be able to perform a trade in the least amount of time with the least amount of effort")]),
    cand("C006", "Have an easy way to integrate one's own bank account with a trading app.",
         "Stakeholder", "stated preference (reason Binance was chosen over WazirX)", ["比较加密应用时"], "explicit",
         [ev("DOC019:T016", "it was very tough to integrate your own bank account with Wazirex's account")]),
    cand("C007", "Coinbase should have gone deeper into Indian crypto regulations in order to tap the Indian market.",
         "Stakeholder", "speculation/advice about a vendor's market strategy", ["印度市场，当时代"], "explicit",
         [ev("DOC019:T018", "if Coinbase would have, you know, gotten deeper into the regulations that are present for.")]),
    cand("C008", "Have a seamless interface to integrate bank accounts and a payment interface to convert crypto into cash and cash into crypto.",
         "Stakeholder", "counterfactual wish ('would have been helpful')", ["印度市场，当时代", "谈 Coinbase 可改进之处"], "explicit",
         [ev("DOC019:T018", "if they had a seamless interface to integrate our bank accounts with coinbase at that point of time, or even some kind of a payment interface to get my cryptocurrencies into cash or cash to cryptocurrency conversions")]),
    cand("C009", "Be able to get cash from the bank into the cryptocurrency one wants to invest in.",
         "Stakeholder", "reported inability (obstacle)", ["印度市场，当时代", "Coinbase"], "inferred",
         [ev("DOC019:T018", "I was not able to get my cash from my bank to oh. a coin that I wanted to invest in.")]),
    cand("C010", "Track daily how holdings and the market have moved, and realign investments every fortnight or month.",
         "Stakeholder", "reported habit", ["在印度交易时期"], "explicit",
         [ev("DOC019:T020", "Every day I I used to keep a track of whatever I have invested whatever, how the market has moved.")]),
    cand("C011", "Stay averse to crypto trading because of volatility and scam coins, and invest only in blue-chip coins.",
         "Stakeholder", "reported personal risk stance", ["加密货币 vs 印度股票"], "explicit",
         [ev("DOC019:T020", "I have been averse to doing cryptocurrency trades compared to stock stock trades")]),
    cand("C012", "Decide to hold, add or exit based on 3-month (small cap) and 6-month (large cap) performance and on having maximized profit.",
         "Stakeholder", "reported decision method", ["个人交易方法"], "explicit",
         [ev("DOC019:T022", "I see how they have performed in the past 3 months")]),
    cand("C013", "Use the app for long-term financial planning and save money for retirement.",
         "Stakeholder", "explicit primary goal", ["首要目标"], "explicit",
         [ev("DOC019:T024", "so my, my primary goal is financial planning long term financial planning. I want to be I want to be able to save up money for the future whenever I retire.")]),
    cand("C014", "Become more financially literate in the process, including understanding how markets work.",
         "Stakeholder", "explicit secondary goal", ["次要目标"], "explicit",
         [ev("DOC019:T024", "Then there are some secondary goals to this one is becoming more financially literate in the process, trying to understand how markets work")]),
    cand("C015", "Understand new algorithms that can be used to generate profits.",
         "Stakeholder", "explicit secondary goal", ["次要目标"], "explicit",
         [ev("DOC019:T024", "trying to understand new algorithms that can be used to gardener profits")]),
    cand("C016", "Become algorithmically literate in finance, which can help in getting jobs.",
         "Stakeholder", "explicit tertiary goal", ["第三目标"], "explicit",
         [ev("DOC019:T024", "and another tertiary goal can be becoming algorithmically literate in terms of finance that can help me in getting jobs")]),
    cand("C017", "Have a seamless integration with the bank account at the start of onboarding, described as the deciding factor for using an app.",
         "Stakeholder", "explicit ideal-experience requirement", ["开户最初阶段"], "explicit",
         [ev("DOC019:T028", "an ideal experience generally involves having a seamless integration with the bank account initially"),
          ev("DOC019:T028", "that has been the deciding factor of using or not using an app")]),
    cand("C018", "Understand how a particular stock is moving at that point of time and be able to make a trade instantly.",
         "Stakeholder", "explicit ideal-experience requirement ('trades easily')", ["理想交易体验"], "explicit",
         [ev("DOC019:T028", "When I say trades easily, it means that I'm able to understand how the how a particular stock is moving at that point of time, and I'm able to make a trade instantly")]),
    cand("C019", "Be able to set up rules for trading.",
         "Stakeholder", "explicit ideal-experience requirement", ["理想交易体验"], "explicit",
         [ev("DOC019:T028", "or I'm able to set up rules of for trading")]),
    cand("C020", "Have a separate interface for financial news to understand what happened in the market that can affect different stocks.",
         "Stakeholder", "explicit ideal-experience requirement ('I would like to have')", ["理想交易体验"], "explicit",
         [ev("DOC019:T028", "I would like to have a separate interface to get in financial news and understand what all things have happened in the market that can affect the different stocks.")]),
    cand("C021", "Have news headlines marked as positive or negative for a particular stock or crypto, with its logo, as Coinbase does.",
         "Stakeholder", "reference example of a liked feature", ["Coinbase 现有实现"], "explicit",
         [ev("DOC019:T038", "for each headline they mentioned whether this particular headline is positive news for some particular stock")]),
    cand("C022", "Use a portfolio dashboard that gives one-page insight into everything that happened during the day.",
         "Stakeholder", "reported reliance and liking", ["Zerodha 常用功能"], "explicit",
         [ev("DOC019:T036", "So the most frequently used tool that I use is the portfolio dashboard."),
          ev("DOC019:T036", "Here it gives me like in in one page it gives me an insight into everything that has happened in the happened in the day.")]),
    cand("C023", "Keep a watchlist of interesting stocks, though it is not used much.",
         "Stakeholder", "mild preference, explicitly low use", ["Zerodha 功能"], "explicit",
         [ev("DOC019:T036", "I also like the watchlist feature. I I don't use it a lot")]),
    cand("C024", "Rely on news from newspapers, online articles and YouTube for about 99% of investment information.",
         "Stakeholder", "reported information habit", ["投资信息来源"], "explicit",
         [ev("DOC019:T040", "it's generally like 99% of it is news.")]),
    cand("C025", "Get more guidance on advanced algorithms once already using the app.",
         "Stakeholder", "soft request ('would be good for me')", ["已进入应用之后", "'I am not sure of this' 指对当时 Academy 内容的记忆不确定"], "explicit",
         [ev("DOC019:T044", "It would be, I think, good for me if I have some more guidance on advanced algorithms.")]),
    cand("C026", "Have a comprehensive academy on futures and options trading rather than a running mention.",
         "Stakeholder", "soft request ('would be good addition')", ["Academy 课程范围", "不确定现在是否已补充"], "explicit",
         [ev("DOC019:T044", "also, I think they didn't have a very comprehensive Academy on futures and Options trading")]),
    cand("C027", "Had to do a lot of research himself to understand the algorithms companies use.",
         "Stakeholder", "reported obstacle", ["想学算法时"], "explicit",
         [ev("DOC019:T044", "So I had to do a lot of research at the point of time to understand different algorithms that companies use.")]),
    cand("C028", "Have the option of investing in mutual funds in addition to stocks.",
         "Stakeholder", "proposal with feasibility doubt ('I'm not sure how feasible it is')", ["共同基金 vs 个股", "预期更安全、可投更多、更信任"], "explicit",
         [ev("DOC019:T046", "if they also had an option of investing in mutual funds and mutual funds apart from just stocks")]),
    cand("C029", "The complex part of the app is onboarding, specifically the bank account part.",
         "Stakeholder", "reported pain point", ["开户流程"], "explicit",
         [ev("DOC019:T052", "The only com the complex part is onboarding. And that I have already mentioned the bank account part of it.")]),
    cand("C030", "Make onboarding as easy as possible.",
         "Stakeholder", "explicit wish ('I would like it to be as easier as possible for me')", ["开户流程", "即便最易用的应用也仍显复杂"], "explicit",
         [ev("DOC019:T054", "even Zerota being the easiest, it was much complex like it was very complex, even though it was the easiest, so I would like it to be as easier as possible for me")]),
    cand("C031", "Add a voice feature (voice-based orders or voice-based summarization) to reduce the pain of going into the app to check.",
         "Stakeholder", "explicit request with feasibility doubt ('if it is possible')", ["语音下单与语音摘要为替代形式"], "explicit",
         [ev("DOC019:T058", "but an addition of a voicing feature would be very good."),
          ev("DOC019:T058", "Because I think that would help me reduce the pain of going into the app all the time to check it whatever I want to ask.")]),
    cand("C032", "Is unlikely (1-2 of 5) to switch to a new app because setting up the system takes time.",
         "Stakeholder", "self-reported switching likelihood", ["迁移成本"], "explicit",
         [ev("DOC019:T060", "I already have a system set up in front of me, and setting up the system is is like a time taking task in this scenario")]),
    cand("C033", "Opens the stock app once a day at the end of the day to check what the day was like.",
         "Stakeholder", "reported habit", ["日常使用频率"], "explicit",
         [ev("DOC019:T030", "So for stock exchanges it is once a day, because every day at the end of the day I would just check.")]),
]

goals = []


def goal(gid, statement, context, evidence, rationale, supported, origin="explicit", inference=None):
    goals.append({
        "candidate_id": gid, "statement": statement, "actor": "Stakeholder",
        "context": context, "origin": origin, "inference": inference, "evidence": evidence,
        "judgment": {"label": "direct", "rationale": rationale,
                     "supported_parts": supported, "unsupported_parts": [],
                     "assumptions": [], "reasoning_steps": []}})


goal("G001", "Plan finances long term and save money for retirement.",
     ["首要目标（primary goal）"],
     [ev("DOC019:T024", "so my, my primary goal is financial planning long term financial planning. I want to be I want to be able to save up money for the future whenever I retire.")],
     "T024 原句明确把长期财务规划、为退休存钱称为首要目标；主体、对象与时间范围一致。",
     ["长期财务规划为首要目标", "为退休存钱"])

goal("G002", "Become more financially literate while investing, including understanding how markets work.",
     ["次要目标（secondary goal）"],
     [ev("DOC019:T024", "Then there are some secondary goals to this one is becoming more financially literate in the process, trying to understand how markets work")],
     "T024 原句把'变得更懂金融、理解市场如何运作'列为次要目标；未附加掌握程度或证书等阈值。",
     ["提升金融素养", "理解市场如何运作"])

goal("G003", "Understand new algorithms that can be used to generate profits.",
     ["次要目标（secondary goal）", "转写稿 'gardener profits' 应按 generate profits 理解"],
     [ev("DOC019:T024", "trying to understand new algorithms that can be used to gardener profits")],
     "T024 原句明确列出'理解可用于产生利润的新算法'；'gardener' 为转写错误，不改变语义。",
     ["了解可用于获利的新算法"])

goal("G004", "Become algorithmically literate in finance to help in getting jobs.",
     ["第三目标（tertiary goal）"],
     [ev("DOC019:T024", "and another tertiary goal can be becoming algorithmically literate in terms of finance that can help me in getting jobs")],
     "T024 原句明确把'在金融方面具备算法素养、有助于找工作'列为第三目标；目标含自述用途，未推断额外职业要求。",
     ["金融算法素养", "用于求职"])

goal("G005", "Integrate the user's own bank account seamlessly at the start of onboarding.",
     ["银行账户绑定发生在开户最初阶段", "受访者称其为是否使用某应用的决定因素"],
     [ev("DOC019:T028", "an ideal experience generally involves having a seamless integration with the bank account initially"),
      ev("DOC019:T016", "it was very tough to integrate your own bank account with Wazirex's account")],
     "T028 明确说理想体验首先是无缝绑定银行账户，并称其为决定用不用该应用的因素；T016 以 WazirX 难以绑定账户为反例。'seamless' 为原文用词，未加时延指标。",
     ["开户时无缝绑定自有银行账户", "绑定体验影响是否继续使用"])

goal("G006", "Convert cash from the bank into the desired cryptocurrency and back into cash inside the app.",
     ["当时在印度使用 Coinbase", "法币与加密资产双向转换"],
     [ev("DOC019:T018", "if they had a seamless interface to integrate our bank accounts with coinbase at that point of time, or even some kind of a payment interface to get my cryptocurrencies into cash or cash to cryptocurrency conversions"),
      ev("DOC019:T018", "I was not able to get my cash from my bank to oh. a coin that I wanted to invest in.")],
     "T018 明确提出希望有支付接口完成加密资产与现金的双向转换，并说明当时无法把银行的钱换成本想投资的币；这是与银行绑定并列的另一项资金通路需求。",
     ["法币换入加密资产", "加密资产换回现金", "在应用内完成"])

goal("G007", "Be able to set up rules for trading.",
     ["理想交易体验的一部分"],
     [ev("DOC019:T028", "or I'm able to set up rules of for trading")],
     "T028 原句把'能设置交易规则'列为理想体验的一部分；原文未说明规则类型、触发条件或自动化程度，未补造。",
     ["可设置交易规则"])

goal("G008", "Have a separate interface for financial news that shows what has happened in the market and how it can affect individual stocks.",
     ["参照 Coinbase：每条标题标注对具体股票/币种的正负面并配图标", "新闻是受访者主要信息来源"],
     [ev("DOC019:T028", "I would like to have a separate interface to get in financial news and understand what all things have happened in the market that can affect the different stocks."),
      ev("DOC019:T038", "for each headline they mentioned whether this particular headline is positive news for some particular stock")],
     "T028 明确要求单独的财经新闻界面，用于了解影响个股的市场事件；T038 给出 Coinbase 标题正负面标注的参照；T040 佐证新闻是其主要信息来源。界面'separate' 为原文用词。",
     ["独立财经新闻界面", "说明市场事件对个股的影响", "标题级正负面标注为参照实现"])

goal("G009", "See how a particular stock is moving at that moment.",
     ["'trades easily' 的第一项含义"],
     [ev("DOC019:T028", "I'm able to understand how the how a particular stock is moving at that point of time")],
     "T028 把'理解某只股票当时的走势'作为交易顺畅的第一项含义；'at that point of time' 保留为即时性要求，未加刷新频率阈值。",
     ["查看个股当下走势"])

goal("G010", "Place a trade instantly with the least amount of time and effort.",
     ["'trades easily' 的第二项含义", "受访者以最少时间和最少精力评价 Binance"],
     [ev("DOC019:T028", "I'm able to make a trade instantly"),
      ev("DOC019:T016", "still be able to perform a trade in the least amount of time with the least amount of effort")],
     "T028 明确要求能即时下单；T016 补充以最少时间和精力完成交易。'instantly' 与'least effort' 均为原文表述，未量化。",
     ["即时下单", "以最少时间和精力完成交易"])

goal("G011", "Keep a single-page portfolio dashboard that summarizes the day's gains and losses.",
     ["受访者每天使用该视图", "被称为最喜欢的功能之一"],
     [ev("DOC019:T036", "So the most frequently used tool that I use is the portfolio dashboard."),
      ev("DOC019:T036", "Here it gives me like in in one page it gives me an insight into everything that has happened in the happened in the day."),
      ev("DOC019:T030", "So for stock exchanges it is once a day, because every day at the end of the day I would just check.")],
     "T036 明确说组合仪表盘是最常用工具、一页给出当日发生的一切（涨跌），并称其为喜欢的功能；T030 佐证每天收盘后查看。此为依赖与偏好型目标，'keep' 不引入新指标。",
     ["单页组合仪表盘", "汇总当日涨跌", "作为每日查看的主视图"])

goal("G012", "Provide more guidance on advanced trading algorithms once the user is already using the app.",
     ["用户已进入应用并开始使用之后", "'I am not sure of this' 指对当时 Academy 内容的记忆不确定"],
     [ev("DOC019:T044", "It would be, I think, good for me if I have some more guidance on advanced algorithms."),
      ev("DOC019:T044", "So I had to do a lot of research at the point of time to understand different algorithms that companies use.")],
     "T044 明确说在已使用应用后获得更多高级算法指引会更好，并以当时只能自己大量检索为对照；语气为'would be good'，未升级为必须。",
     ["已上手后提供高级算法指引", "覆盖当时需自行检索的缺口"])

goal("G013", "Provide comprehensive academy coverage of futures and options trading.",
     ["Academy 课程范围", "受访者不确定现在是否已经补充（'I don't know if they have done it now'）"],
     [ev("DOC019:T044", "also, I think they didn't have a very comprehensive Academy on futures and Options trading")],
     "T044 明确指出 Academy 对期货与期权交易覆盖不全面（仅一带而过），希望更完整；对现状是否已改不确定，故只保留课程范围要求。",
     ["期货与期权课程覆盖更完整"])

goal("G014", "Offer mutual fund investing in addition to individual stocks.",
     ["可行性未知（'I'm not sure how feasible it is'）", "预期更安全、可投入更大金额、信任度更高"],
     [ev("DOC019:T046", "if they also had an option of investing in mutual funds and mutual funds apart from just stocks")],
     "T046 明确提出希望除个股外还有共同基金选项，并给出更安全、可投更多、更信任的理由；同时表示可行性未知，故目标保留愿望而不声称已承诺实现。",
     ["在个股之外提供共同基金", "作为更安全、可投更多的渠道"])

goal("G015", "Make onboarding as easy as possible.",
     ["开户流程", "即便最易用的应用也仍显得复杂"],
     [ev("DOC019:T054", "even Zerota being the easiest, it was much complex like it was very complex, even though it was the easiest, so I would like it to be as easier as possible for me"),
      ev("DOC019:T052", "The only com the complex part is onboarding. And that I have already mentioned the bank account part of it.")],
     "T054 明确说希望开户尽可能简单；T052 指出应用复杂之处就在开户，具体是银行账户环节。'as easy as possible' 为原文强度，未加步骤数或时限。",
     ["开户尽可能简单", "复杂点集中在银行账户环节"])

goal("G016", "Add voice-based orders or voice-based summarization so the user does not have to open the app repeatedly to check or ask.",
     ["'if it is possible' 表示可行性未定", "语音下单与语音摘要为两种替代形式（or）"],
     [ev("DOC019:T058", "but an addition of a voicing feature would be very good. I'm not sure. So voice based orders, if it is possible. or voice based summarization."),
      ev("DOC019:T058", "Because I think that would help me reduce the pain of going into the app all the time to check it whatever I want to ask.")],
     "T058 在'只改一件事'的追问下明确选择增加语音功能，说明目的是减少反复打开应用查看或询问的麻烦；两种形式由'or'连接，按替代保留，未要求同时具备。",
     ["语音下单或语音摘要", "减少反复打开应用", "保留可行性不确定"])

relations = [
    {"relation_id": "R1", "source_id": "G005", "target_id": "G015", "type": "specialization",
     "status": "supported", "conditions": ["银行账户绑定属于开户流程的初始环节"],
     "assumptions": [], "rationale": "G005 是开户最初环节的具体目标，G015 是开户整体尽可能简单的目标；T052 明确说复杂点就在开户的银行账户部分，T054 要求整个开户尽可能简单，故具体环节指向一般目标。",
     "evidence_ids": [],
     "evidence_quotes": [ev("DOC019:T052", "The only com the complex part is onboarding. And that I have already mentioned the bank account part of it."),
                         ev("DOC019:T054", "so I would like it to be as easier as possible for me")]},
    {"relation_id": "R2", "source_id": "G006", "target_id": "G010", "type": "contribution",
     "status": "supported", "conditions": ["资金需先能进入交易账户"],
     "assumptions": [], "rationale": "T018 说明无法把银行的钱换成本想投资的币，连第一步投资都做不到；法币通路对即时下单是有帮助的前提，但不保证下单本身的体验。",
     "evidence_ids": [],
     "evidence_quotes": [ev("DOC019:T018", "I was not able to get my cash from my bank to oh. a coin that I wanted to invest in.")]},
    {"relation_id": "R3", "source_id": "G012", "target_id": "G003", "type": "operationalization",
     "status": "supported", "conditions": [], "assumptions": [],
     "rationale": "T044 把'更多高级算法指引'作为获得算法理解的途径，T024 的目标是理解可用于获利的新算法；在应用内提供指引服务于该学习目的，但不保证学懂全部算法。",
     "evidence_ids": [],
     "evidence_quotes": [ev("DOC019:T044", "It would be, I think, good for me if I have some more guidance on advanced algorithms.")]},
    {"relation_id": "R4", "source_id": "G013", "target_id": "G002", "type": "operationalization",
     "status": "supported", "conditions": [], "assumptions": [],
     "rationale": "T044 的期货与期权课程属于 Academy 学习内容，服务于 T024 的金融素养目标；课程只是素养的一个来源，不覆盖全部素养要求。",
     "evidence_ids": [],
     "evidence_quotes": [ev("DOC019:T044", "they didn't have a very comprehensive Academy on futures and Options trading")]},
    {"relation_id": "R5", "source_id": "G005", "target_id": "G006", "type": "contribution",
     "status": "proposed", "conditions": [], "assumptions": ["银行账户绑定是法币出入金的技术前提"],
     "rationale": "T018 把'绑定银行账户的顺畅接口'与'法币与加密资产转换的支付接口'并列提出，绑定账户可能帮助资金转换；但原文未说明两者机制上的依赖，故标 proposed。",
     "evidence_ids": [],
     "evidence_quotes": [ev("DOC019:T018", "if they had a seamless interface to integrate our bank accounts with coinbase at that point of time")]},
]

decisions = {
    "relations": relations,
    "groups": [],
    "questions": [
        {"target_type": "model", "target_id": "DOC019-goal-model",
         "message": "精化组判断已逐对执行但未建立任何 AND 组：检查了 (G002,G003,G012,G013) 的学习类组合、(G005) 对 G015、(G006) 对 G010、(G011) 对 G009 等候选，没有一组能声称'共同满足足以实现父目标'——课程与指引不足以保证素养与算法理解，单一银行绑定环节不等于顺畅开户，资金通路不等于即时下单，日度仪表盘也不等于实时走势；单子目标组会退化为同一目标，故 groups 为空。"},
        {"target_type": "goal", "target_id": "G011",
         "message": "组合仪表盘只有'最常用、喜欢'的表述，没有明确的维持或改进要求；是否应作为偏好型目标保留，还是仅作背景？"},
        {"target_type": "goal", "target_id": "G016",
         "message": "语音下单与语音摘要按原文'or'读作替代形式；若产品需要两者分别成立，应拆为两个目标，当前未拆。"},
        {"target_type": "relation", "target_id": "R5",
         "message": "银行账户绑定与法币出入金转换的依赖关系原文未明说，当前标 proposed；需确认绑定是否为转换的必要前提。"},
    ],
    "reassessments": [],
}

entries = []
for c in raw:
    cid = c["candidate_id"]
    entries.append({"candidate_id": cid, "disposition": "keep", "final_goal_ids": [], "reason": ""})

MAPPING = {
    "C001": ("exclude", [], "采访者的研究目的与泛化期望，主体为 Interviewer，未表达涉众目标或具体结果，不作为目标。"),
    "C002": ("exclude", [], "过往使用应用的背景事实，无期望状态。"),
    "C003": ("exclude", [], "当前使用现状与居住地限制，属背景事实；已写入限制说明。"),
    "C004": ("exclude", [], "过去通过 Academy 入门的学习经历；教育类要求由 C025、C026 承接，本项仅背景。"),
    "C005": ("merge", ["G010"], "与'即时下单'同义（交易省时省力），合并入 G010 并保留最少时间/精力的表述。"),
    "C006": ("merge", ["G005"], "以 WazirX 绑定困难说明银行账户集成需求，合并入 G005。"),
    "C007": ("exclude", [], "对 Coinbase 在印度市场策略的建议，属第三方商业判断，非受访者对应用的结果意图。"),
    "C008": ("split", ["G005", "G006"], "同一句含两项独立结果：银行账户绑定接口（G005）与法币/加密资产转换支付接口（G006），分别保留并共享'印度市场、当时'情境。"),
    "C009": ("merge", ["G006"], "无法把银行的钱换成本想投资的币，是 G006 资金通路的直接障碍与依据。"),
    "C010": ("exclude", [], "既有交易习惯（每日跟踪、双周调仓）的描述，未提出对应用的要求；日常查看由 G011 承接。"),
    "C011": ("exclude", [], "个人风险偏好与只买蓝筹币的做法，未表达对产品的要求；不作为目标或约束强加给应用。"),
    "C012": ("exclude", [], "个人选股与止盈方法，属决策习惯描述，未转化为产品要求，未编造指标。"),
    "C013": ("keep", ["G001"], "首要目标原句，完整保留长期规划与退休储蓄。"),
    "C014": ("keep", ["G002"], "次要目标原句，保留金融素养与理解市场运作。"),
    "C015": ("keep", ["G003"], "次要目标原句，保留对可获利新算法的理解。"),
    "C016": ("keep", ["G004"], "第三目标原句，保留算法素养与求职用途。"),
    "C017": ("keep", ["G005"], "理想体验中银行账户无缝绑定的主依据，保留'决定是否使用'的强度。"),
    "C018": ("split", ["G009", "G010"], "原句以'交易顺畅'统摄两项可独立满足的结果：理解个股当下走势（G009）与即时下单（G010），分别保留。"),
    "C019": ("keep", ["G007"], "理想体验中的交易规则设置，单独成目标，未补造规则类型。"),
    "C020": ("keep", ["G008"], "独立财经新闻界面的明确要求。"),
    "C021": ("merge", ["G008"], "Coinbase 标题正负面标注是新闻界面的参照实现，合并入 G008 的 context，未升级为强制方式。"),
    "C022": ("keep", ["G011"], "组合仪表盘为最常用且喜欢的功能，保留为偏好/依赖型目标。"),
    "C023": ("exclude", [], "仅表示喜欢但明确'用得不多'，没有维持或改变的结果意图；不把偏好改写为要求。"),
    "C024": ("merge", ["G008"], "新闻为主要信息来源，佐证 G008 的必要性，合并入该目标。"),
    "C025": ("keep", ["G012"], "高级算法指引的明确请求，保留'soft'语气与'已上手后'条件。"),
    "C026": ("keep", ["G013"], "期货与期权课程覆盖不足的改进要求，单独成目标。"),
    "C027": ("merge", ["G012"], "当时只能自行检索算法，是 G012 的障碍依据，合并入该目标。"),
    "C028": ("keep", ["G014"], "共同基金选项的提议，保留可行性不确定。"),
    "C029": ("merge", ["G015"], "指出复杂点在开户的银行账户环节，合并入 G015 作为范围限定。"),
    "C030": ("keep", ["G015"], "开户尽可能简单的明确愿望，保留原文强度。"),
    "C031": ("keep", ["G016"], "语音功能的明确请求，保留两种替代形式与可行性不确定。"),
    "C032": ("exclude", [], "对切换到新应用意愿的自评（1-2/5）与迁移成本，属行为倾向，非产品目标。"),
    "C033": ("merge", ["G011"], "每天收盘后查看的习惯，佐证 G011 的使用场景，合并入该目标。"),
}

for e in entries:
    d, gids, reason = MAPPING[e["candidate_id"]]
    e["disposition"] = d
    e["final_goal_ids"] = gids
    e["reason"] = reason

source_checks = [
    {"check_id": "S1", "evidence_candidates": [ev("DOC019:T003", "The goal here is to kind of understand your experience with these apps")],
     "candidate_ids": ["C001"], "final_goal_ids": [], "outcome": "excluded",
     "reason": "回查开场：这是采访者的研究目的，不是受访者的目标；不因访谈主题相关而建根目标。"},
    {"check_id": "S2", "evidence_candidates": [ev("DOC019:T024", "so my, my primary goal is financial planning long term financial planning.")],
     "candidate_ids": ["C013", "C014", "C015", "C016"], "final_goal_ids": ["G001", "G002", "G003", "G004"],
     "outcome": "represented", "reason": "回查三层目标陈述：首要/次要/第三目标各有独立意图，分别保留为四个目标，未压缩为一条。"},
    {"check_id": "S3", "evidence_candidates": [ev("DOC019:T028", "When I say trades easily, it means that I'm able to understand how the how a particular stock is moving at that point of time, and I'm able to make a trade instantly")],
     "candidate_ids": ["C018"], "final_goal_ids": ["G009", "G010"],
     "outcome": "represented", "reason": "回查理想体验段：'交易顺畅'含两项可独立满足的能力，拆为实时走势与即时下单，未合并成一句空泛目标。"},
    {"check_id": "S4", "evidence_candidates": [ev("DOC019:T018", "I was not able to get my cash from my bank to oh. a coin that I wanted to invest in.")],
     "candidate_ids": ["C008", "C009"], "final_goal_ids": ["G005", "G006"],
     "outcome": "represented", "reason": "回查 Coinbase 反事实段：银行绑定与法币转换是两项需求，且以无法把银行的钱换成币为障碍依据。"},
    {"check_id": "S5", "evidence_candidates": [ev("DOC019:T038", "for each headline they mentioned whether this particular headline is positive news for some particular stock")],
     "candidate_ids": ["C021"], "final_goal_ids": ["G008"],
     "outcome": "represented", "reason": "回查新闻参照：Coinbase 的正负面标注作为实现参照写入 G008 的 context，未把示例固化为唯一方式。"},
    {"check_id": "S6", "evidence_candidates": [ev("DOC019:T044", "It would be, I think, good for me if I have some more guidance on advanced algorithms.")],
     "candidate_ids": ["C025", "C026", "C027"], "final_goal_ids": ["G012", "G013"],
     "outcome": "represented", "reason": "回查改进建议段：高级算法指引与期货期权课程是两项独立内容，分别成目标；自行检索作为障碍依据。"},
    {"check_id": "S7", "evidence_candidates": [ev("DOC019:T052", "The only com the complex part is onboarding. And that I have already mentioned the bank account part of it.")],
     "candidate_ids": ["C029", "C030"], "final_goal_ids": ["G015"],
     "outcome": "represented", "reason": "回查复杂度问答：受访者明确否认交易步骤冗余，复杂度集中在开户；据此把范围限定在开户，不造无关目标。"},
    {"check_id": "S8", "evidence_candidates": [ev("DOC019:T058", "but an addition of a voicing feature would be very good.")],
     "candidate_ids": ["C031"], "final_goal_ids": ["G016"],
     "outcome": "represented", "reason": "回查'只改一件事'：语音功能为明确选择，两种形式按替代保留，未升级为两项必须。"},
    {"check_id": "S9", "evidence_candidates": [ev("DOC019:T060", "I already have a system set up in front of me, and setting up the system is is like a time taking task in this scenario")],
     "candidate_ids": ["C032"], "final_goal_ids": [], "outcome": "excluded",
     "reason": "回查切换意愿：这是对自身行为的估计与迁移成本，不是对产品结果的要求；未据此造'降低迁移成本'目标。"},
    {"check_id": "S10", "evidence_candidates": [ev("DOC019:T022", "I see how they have performed in the past 3 months")],
     "candidate_ids": ["C012"], "final_goal_ids": [], "outcome": "excluded",
     "reason": "回查决策方法：3/6 个月表现与止盈属受访者个人策略，原文未要求应用提供该指标，未编造阈值。"},
    {"check_id": "S11", "evidence_candidates": [ev("DOC019:T036", "I also like the watchlist feature. I I don't use it a lot")],
     "candidate_ids": ["C023"], "final_goal_ids": [], "outcome": "excluded",
     "reason": "回查功能偏好：自选列表仅表喜欢且明确少用，无维持或改进意图；与 G011 的常用仪表盘区别在于依赖程度，避免偏好升级为要求。"},
]

passes = [{
    "pass_id": "P1", "kind": "initial", "context": "isolated", "status": "completed",
    "window_results": [{"window_id": f"DOC019:W{i:04d}", "status": "processed", "reason": ""}
                       for i in range(1, WINDOW_COUNT + 1)],
}]

spec = {
    "document_id": "DOC019",
    "status": "completed",
    "omissions": [],
    "raw_candidates": raw,
    "goals": goals,
    "review_questions": [
        {"candidate_ids": ["G011"], "question": "组合仪表盘只有'最常用、喜欢'的表述，没有明确的维持或改进要求；应作为偏好型目标保留，还是仅作背景？",
         "reason": "原文对其评价为正面但未提出改变，涉及偏好是否升级为要求。"},
        {"candidate_ids": ["G016"], "question": "语音下单与语音摘要是否应拆成两个目标？",
         "reason": "原文用'or'连接，按替代读作一条；若产品需两者分别成立，则粒度不同。"},
        {"candidate_ids": ["G014"], "question": "共同基金选项在'可行性未知'下是否仍作为目标保留？",
         "reason": "受访者明确表示不确定是否可行，但愿望本身清楚；当前保留愿望、不声称承诺。"},
    ],
    "limitations": [
        "转写稿存在识别/拼写问题（'0 Dha' 指 Zerodha、'Moodrex'/'Wazirex' 指 WazirX、'gardener profits' 应为 generate profits、'â‚¹' 为编码异常），按上下文解读，未改动引文。",
        "受访者当前在美国，无法进行印度股票交易；部分描述针对过去在印度的使用时期，相关目标已按该情境记录。",
        "访谈未给出数量阈值、性能指标或优先级权重，未编造。",
        "单一受访者、单一场景，不声称覆盖全部用户需求。",
    ],
    "ledger": {
        "model": "unknown", "temperature": "unknown", "budget": "1 initial pass + <=2 repair rounds",
        "usage": "unknown", "skill_revision": SKILL_REV, "prompt_revision": "task-prompt-v1",
        "planned_passes": 1,
        "stop_reason": "完成一次全篇读取、32 个窗口逐窗捕获、全篇校正与建模判断；无新的有据意图可补，按预算停止。",
        "passes": passes,
        "full_context_review": {
            "status": "completed",
            "reason": "回查全部 65 轮：核对指代（'0 Dha'=Zerodha、'that app'、'they' 指应用方）、条件继承（印度使用时期、已上手后、可行性未知）、让步（'I am not sure'、'if it is possible'）、例外（交易步骤不复杂而开户复杂）与相反证据（T050 称下单流程不复杂，故不建简化下单目标），并跨窗连接 T012 学习经历→T044 课程要求、T016/T018 银行绑定→T028 开户体验、T030 日查看→T036 仪表盘、T038/T040 新闻→T028 新闻界面。"},
        "entries": entries,
        "source_checks": source_checks,
    },
    "decisions": decisions,
}

(A / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
print("candidates", len(raw), "goals", len(goals), "relations", len(relations))
