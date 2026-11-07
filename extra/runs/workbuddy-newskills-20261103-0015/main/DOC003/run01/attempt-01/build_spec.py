import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
src = json.loads((BASE / "source/DOC003.json").read_text(encoding="utf-8"))
texts = {t["source_id"]: t["text"] for t in src["turns"]}

def Q(sid, start, end=None):
    s = texts[sid]
    i = s.find(start)
    assert i >= 0, ("start not found", sid, start)
    if end is None:
        q = start
    else:
        j = s.find(end, i)
        assert j >= 0, ("end not found", sid, end)
        q = s[i:j + len(end)]
    assert s.count(q) == 1, ("ambiguous quote", sid, q)
    return q

def E(sid, start, end=None, role="basis"):
    return {"source_id": sid, "quote": Q(sid, start, end), "role": role}

# ---------------- goals ----------------
goals = []

goals.append(dict(
    candidate_id="G001", actor="Stakeholder", origin="explicit",
    statement="Find a flight itinerary whose timing fits my travel plans - matching onward transport and the schedules of people I am meeting, and ideally letting me sleep at night.",
    context=["timing is judged against onward transport, hotel needs and people I am meeting",
             "if the booking is urgent and no other itinerary exists, I accept an itinerary that does not fit",
             "a better-fitting option is weighed against its price difference"],
    inference=None,
    evidence=[E("DOC003:T129", "It should give me a good itinerary in terms of times", "match my situations."),
              E("DOC003:T119", "is it matching up with the schedules of the other modes of transport", "Is it matching up with their schedules."),
              E("DOC003:T083", "so that I would be able to make sure that I get home that night", "I don't miss my train")],
    judgment=dict(label="direct",
                  rationale="受访者把“好行程”明确限定为时间合适、与其处境（衔接其他交通、与要见的人日程一致）匹配，并表示宁可要夜间睡眠而不坐红眼；陈奈-加尔各答例子给出错过末班车的具体条件。",
                  supported_parts=["行程时间需匹配其他交通/会面日程", "夜间睡眠为偏好强度", "紧急且无替代时接受不匹配的行程"],
                  unsupported_parts=[], assumptions=[], reasoning_steps=[])))

goals.append(dict(
    candidate_id="G002", actor="Stakeholder", origin="explicit",
    statement="Find a good deal on the flight - primarily a low price, with seating and other benefits taken into account.",
    context=["seating and other benefits are secondary considerations"],
    inference=None,
    evidence=[E("DOC003:T025", "my primary focus is to like get a really good deal", "booking my flights."),
              E("DOC003:T115", "finding a good price that works for me"),
              E("DOC003:T009", "find what's like the best alternative in terms of price and seating and other benefits")],
    judgment=dict(label="direct",
                  rationale="多处明确把“拿到好价格/好交易”列为主要目标，并称会反复查看以确保最优；早期也提到按价格、座位与其他权益比较备选。",
                  supported_parts=["好价格为主", "座位与其他权益为次要比较项"], unsupported_parts=[],
                  assumptions=[], reasoning_steps=[])))

goals.append(dict(
    candidate_id="G003", actor="Stakeholder", origin="explicit",
    statement="Compare different booking websites for the chosen itinerary to find the provider that offers the best price and overall deal.",
    context=["comparison includes final cost, discounts and provider rating",
             "if no provider deal is better, I book wherever the best coupon applies"],
    inference=None,
    evidence=[E("DOC003:T115", "I would also use it to compare different booking websites", "best possible combination of options."),
              E("DOC003:T077", "I often visit multiple providers from this page"),
              E("DOC003:T103", "they allow me to find the best price for that itinerary.", "comparing all of the different booking options.")],
    judgment=dict(label="direct",
                  rationale="受访者把“比较不同预订网站、选出最优组合”列为使用该应用的三项主要目标之一，并描述会逐个打开提供方页面比较价格、评分与折扣。",
                  supported_parts=["比较多个预订提供方", "以价格与整体交易为比较标准"], unsupported_parts=[],
                  assumptions=[], reasoning_steps=[])))

goals.append(dict(
    candidate_id="G004", actor="Stakeholder", origin="explicit",
    statement="Search across many airport, city and country pairs and date ranges in a single search rather than one pair at a time (for example, about 11,760 combinations of airports, dates and cabin classes).",
    context=["search by country or region so that many airports are looked up together"],
    inference=None,
    evidence=[E("DOC003:T065", "I would rather search with a series of different airports.", "More airports looked up at the same time."),
              E("DOC003:T099", "So I'd like to search for all possible airports", "top 5 or 6 most popular airports in India."),
              E("DOC003:T095", "you want to do around 500 searches at the same time")],
    judgment=dict(label="direct",
                  rationale="明确说更愿意一次搜索一系列机场、用国家或地区让多个机场同时被查询，并给出 20×6×49×2≈11,760 的组合规模作为期望的检索范围。",
                  supported_parts=["多机场/多城市/多国家组合一次检索", "日期范围与舱位维度", "示例规模11,760"], unsupported_parts=[],
                  assumptions=[], reasoning_steps=[])))

goals.append(dict(
    candidate_id="G005", actor="Stakeholder", origin="explicit",
    statement="Complete flight research much faster, with substantially less time and mental effort per search.",
    context=["long-term switching: even a couple of minutes saved per search matters because they add up; a one-off saving may not be worth switching"],
    inference=None,
    evidence=[E("DOC003:T149", "If I was able to do research at a much quicker pace.", "while spending less time at it."),
              E("DOC003:T137", "I have to invest a lot of time into finding.", "What's the ideal option?"),
              E("DOC003:T147", "being familiar with the user interface and being able to quickly key in things", "just saves you time.")],
    judgment=dict(label="direct",
                  rationale="明确说若能以快得多的速度、同时看更多组合且更准确地研究、花更少时间，就会投入换平台；并把研究耗时列为最大障碍。",
                  supported_parts=["更快完成研究", "减少时间与心力", "长期使用即使每次只省几分钟也值得"], unsupported_parts=[],
                  assumptions=[], reasoning_steps=[])))

goals.append(dict(
    candidate_id="G006", actor="Stakeholder", origin="inferred",
    statement="Get all the information needed for a booking in one place instead of visiting 10 to 12 different sites.",
    context=["research otherwise spans several aggregators and booking providers"],
    inference=dict(basis_candidate_ids=["G005"],
                   reason="受访者把“信息不在同一处、至少要访问10–12个站点”列为两大障碍之一，并与研究耗时相连；由此推断他希望有一处集中的信息视图。",
                   assumptions=["该抱怨被理解为希望减少跨站访问，而不仅是陈述现状"]),
    evidence=[E("DOC003:T137", "I don't get to have all of my information at one pace", "at a mostly at a minimum."),
              E("DOC003:T047", "All of the research takes place on Skyscann directly.", role="context")],
    judgment=dict(label="inferred",
                  rationale="原文只有抱怨（信息分散、需访问10–12个站点），没有直接提出“集中在一处”的要求；结合其把该点列为障碍，推断出信息集中目标。",
                  supported_parts=["信息分散导致跨站访问"], unsupported_parts=[],
                  assumptions=["抱怨被解读为希望信息集中，而非仅描述现状"],
                  reasoning_steps=["识别障碍句", "将障碍的目标状态表述为信息集中"])))

goals.append(dict(
    candidate_id="G007", actor="Stakeholder", origin="explicit",
    statement="Stay anonymous while searching flights - not logging in and blocking cookies - so that I am not tracked or quoted higher prices.",
    context=["exception: award/points bookings require logging into the airline site, outside this browsing activity"],
    inference=None,
    evidence=[E("DOC003:T053", "I generally am very privacy conscious.", "as anonymized as possible."),
              E("DOC003:T053", "they might increase the flight prices for you"),
              E("DOC003:T089", "I go through an incognito window route. and I block all the cookies.")],
    judgment=dict(label="direct",
                  rationale="明确说自己注重隐私、避免登录并尽量匿名，理由是可能被跟踪或因频繁搜索而被提价；并描述使用无痕窗口和屏蔽 cookie。",
                  supported_parts=["不登录/匿名搜索", "屏蔽cookie", "避免被跟踪与差别定价"], unsupported_parts=[],
                  assumptions=[], reasoning_steps=[])))

goals.append(dict(
    candidate_id="G008", actor="Stakeholder", origin="explicit",
    statement="Receive price-drop alerts for several candidate routes so I can book as soon as one of them falls within reach.",
    context=["used only once, on Google Flights, for a trip that had to be made",
             "doubt that accurate alert rules are feasible because fares and plans change quickly"],
    inference=None,
    evidence=[E("DOC003:T087", "I needed a reminder on a few different routes", "I I book it"),
              E("DOC003:T085", "there could be better alert options to just let me know when flight prices drop down.", role="context")],
    judgment=dict(label="direct",
                  rationale="明确说“可以有更好的提醒选项”并在一次必须成行的行程中为多条路线设置降价提醒；同时保留其对规则可行性的怀疑作为限定，强度为弱建议。",
                  supported_parts=["多路线降价提醒", "降价即订的触发意图"], unsupported_parts=[],
                  assumptions=[], reasoning_steps=[])))

goals.append(dict(
    candidate_id="G009", actor="Stakeholder", origin="explicit",
    statement="Show whether a fare is above or below the typical price for that market, especially where I am unfamiliar with local prices.",
    context=["needed only until I become familiar with the market"],
    inference=None,
    evidence=[E("DOC003:T109", "I can use Google flights for it because it tells me if the price is above, below, or lower than the Median."),
              E("DOC003:T111", "it would help out for the times when I'm not familiar with the specific market."),
              E("DOC003:T111", "it's nice to have.")],
    judgment=dict(label="direct",
                  rationale="明确说在陌生市场会用 Google Flights 的中位数比较判断价格高低，并回答在 Skyscanner 上显示该比较“会有帮助”“是锦上添花”；强度弱且随熟悉度消失。",
                  supported_parts=["显示相对市场中位数的价格位置", "仅在不熟悉市场时需要"], unsupported_parts=[],
                  assumptions=[], reasoning_steps=[])))

goals.append(dict(
    candidate_id="G010", actor="Stakeholder", origin="explicit",
    statement="Keep at least 1.5 times (preferably 2 times) the minimum connection time at any stopover.",
    context=["unless visa constraints make a stopover unacceptable"],
    inference=None,
    evidence=[E("DOC003:T123", "I generally don't care very much about it as long as the I am at least 1.5 x the Mct"),
              E("DOC003:T123", "I generally tend to at least go for 1.5 x or 2 x of that for a stopover.")],
    judgment=dict(label="direct",
                  rationale="明确说不介意经停数量，只要换乘时间至少为 IATA 最低衔接时间（MCT）的1.5倍，通常按1.5–2倍安排；签证问题为例外。",
                  supported_parts=["最低1.5倍MCT", "通常取2倍", "签证为例外"], unsupported_parts=[],
                  assumptions=[], reasoning_steps=[])))

goals.append(dict(
    candidate_id="G011", actor="Stakeholder", origin="explicit",
    statement="Avoid itineraries with long idle waits or excessive total travel time.",
    context=["applies to practical trips; on leisure trips I may deliberately choose longer, stop-heavy routes"],
    inference=None,
    evidence=[E("DOC003:T031", "So I try to plan out my travel, such that things fall into place", "doing nothing."),
              E("DOC003:T073", "the cheapest section ends up being filled with a lot of stuff that's like 40, 50, 60")],
    judgment=dict(label="direct",
                  rationale="明确说规划行程要避免在城市里空等约20小时，并说国际搜索时会避开40–60小时的超长廉价行程；其“喜欢绕行观光”的偏好属另一情境，已在条件中区分。",
                  supported_parts=["避免长时间空等", "避免过长总旅行时间"], unsupported_parts=[],
                  assumptions=[], reasoning_steps=[])))

goals.append(dict(
    candidate_id="G012", actor="Stakeholder", origin="explicit",
    statement="Book flights on behalf of family and friends as well as myself, using leftover points or gift vouchers where possible.",
    context=["about 80% of bookings are for myself and 20% for other people"],
    inference=None,
    evidence=[E("DOC003:T017", "I absolutely use it for friends and family", "family more so than friends."),
              E("DOC003:T017", "if I've got like extra points, or like gift vouchers left over", "help friends book their own flights"),
              E("DOC003:T017", "it's like 80 20 like myself to everybody else.")],
    judgment=dict(label="direct",
                  rationale="明确报告长期为父母、姐妹、伴侣和朋友订票，并会用剩余积分或礼券帮朋友；约80/20的自我/他人比例。属现状实践，不是变更请求，故在理由中标注。",
                  supported_parts=["为亲友订票", "使用剩余积分/礼券"], unsupported_parts=[],
                  assumptions=[], reasoning_steps=[])))

goals.append(dict(
    candidate_id="G013", actor="Stakeholder", origin="inferred",
    statement="Continue from the aggregator to the chosen provider's checkout with the itinerary and my details already filled in, leaving only confirmation and payment.",
    context=["the aggregator itself does not complete bookings"],
    inference=dict(basis_candidate_ids=["G003"],
                   reason="受访者描述选定提供方后会被直接带到已填好行程与个人信息的页面，并称剩下“只是确认信息和付款”；由此推断他希望这一交接保留已填信息。",
                   assumptions=["把描述性的流程说明理解为对现状的认可与维持意图"]),
    evidence=[E("DOC003:T047", "Skyscanner directly takes me to the exact booking page", "making the final payment."),
              E("DOC003:T135", "the flight details will already be filled in", "which flight I'm taking.")],
    judgment=dict(label="inferred",
                  rationale="原文是对现有跳转流程的描述和价值判断（“就像确认信息和付款”），没有直接提出要求；由描述推断出对无缝交接的目标。",
                  supported_parts=["跳转到提供方结账页", "行程与信息已预填"], unsupported_parts=[],
                  assumptions=["描述性认可被视为维持意图"], reasoning_steps=["识别流程描述", "将价值评价转写为预期结果"])))

goals.append(dict(
    candidate_id="G014", actor="Stakeholder", origin="explicit",
    statement="See detailed connection and timing information - layovers, local times, arrival day and total duration - so I can judge whether an itinerary works.",
    context=[],
    inference=None,
    evidence=[E("DOC003:T077", "I make sure all the flight details like I said.", "they work for my schedule."),
              E("DOC003:T075", "this is the time I take off.", "How many hours am I gonna have to wait in the Istanbul airport?")],
    judgment=dict(label="direct",
                  rationale="明确说会大量使用行程详情，逐项确认衔接与时间是否适合自己；并描述需要中转等待时长、当地时间和到达日等信息。",
                  supported_parts=["中转等待与当地时间", "到达日与总时长", "用于判断行程是否可行"], unsupported_parts=[],
                  assumptions=[], reasoning_steps=[])))

goals.append(dict(
    candidate_id="G015", actor="Stakeholder", origin="explicit",
    statement="See the lounge access my cards and passes give me at the connecting airport inside the flight search, if it can be kept accurate.",
    context=["about 30 cards with different lounge entitlements",
             "existing third-party trackers do not update reliably; otherwise I use the issuer's own site"],
    inference=None,
    evidence=[E("DOC003:T125", "it would be very nice if I could, input there would be a website", "That would be wonderful."),
              E("DOC003:T125", "I prefer going to the source of the truth for the lounge access", role="context"),
              E("DOC003:T123", "will the lounge at that airport be open at that point of time?", role="context")],
    judgment=dict(label="direct",
                  rationale="对“在搜索中显示休息室信息”回答“Sure”，并称若能持续更新并整合会“非常棒”；但同一轮明确说第三方更新不可靠、宁愿以发卡行源头为准，故目标带准确性条件、强度弱。",
                  supported_parts=["在航班搜索中看到可用休息室", "以持续准确更新为条件", "否则以发卡行为准"], unsupported_parts=[],
                  assumptions=[], reasoning_steps=[])))

# ---------------- raw candidates ----------------
cands = []

def C(cid, stmt, mod, wins, ev, origin, disp, gids, reason, ctx=None):
    cands.append(dict(candidate_id=cid, statement=stmt, actor="Stakeholder", modality=mod,
                      context=ctx or [], origin=origin, evidence=ev,
                      disposition=disp, final_goal_ids=gids, reason=reason))

C("C001", "Plan travel itineraries by looking at several different travel websites.", "descriptive ('I take a look')", [], 
  [E("DOC003:T007", "Yes. So to plan out different itineraries. I take a look at different traveling related websites")],
  "explicit", "merge", ["G006"], "多站点查阅行程是现状；其暴露的信息分散问题由G006承接。")
C("C002", "Find the best travel alternative in terms of price, seating and other benefits.", "descriptive ('I explored')", [],
  [E("DOC003:T009", "I explored various different options to find what's like the best alternative", "in terms of price and seating and other benefits")],
  "explicit", "merge", ["G002"], "价格/座位/权益的综合比较并入G002（好交易、主要看价格）；座位与权益作为次要比较项保留在G002正文。")
C("C003", "Find good itineraries and book early to get a better price.", "explicit ('looking for')", [],
  [E("DOC003:T009", "looking for good itineraries to plan to book things early so that I can get it at a better price.")],
  "explicit", "split", ["G001", "G002"], "同句含两个可独立满足的结果：好行程（G001）与更好价格（G002）；“提前订”是其订票时机策略，见C004。")
C("C004", "Book international trips at least one to 1.5 months ahead, ideally a couple of months, to get a better deal.", "preference ('Ideally... Mostly I try to aim')", [],
  [E("DOC003:T015", "Ideally, I like to do it at least a couple of months before."),
   E("DOC003:T015", "Mostly I try to aim for at least one to 1.5 months out", "better price at a better deal.")],
  "explicit", "exclude", [], "个人订票时机习惯，服务于更好价格；结果已由G002承接，不单列为平台能力目标。")
C("C005", "Book flights for family and friends, using leftover points or gift vouchers to help them save money.", "explicit ('I absolutely use it')", [],
  [E("DOC003:T017", "I absolutely use it for friends and family", "family more so than friends."),
   E("DOC003:T017", "if I've got like extra points, or like gift vouchers left over", "help friends book their own flights")],
  "explicit", "keep", ["G012"], "亲友订票与用剩余积分/礼券帮其省钱，是完整的独立使用目标，保留为G012。")
C("C006", "Maximize time in the air and take stop-heavy routes to visit cities and lounges.", "preference ('I try to maximize')", [],
  [E("DOC003:T019", "I try to maximize my time in the air.")],
  "explicit", "exclude", [], "个人旅行偏好（喜欢经停观光），非对应用的要求；与G011的实用行程时长规避分属不同情境。")
C("C007", "Get a really good deal on every flight booked.", "explicit ('my primary focus')", [],
  [E("DOC003:T025", "my primary focus is to like get a really good deal", "booking my flights.")],
  "explicit", "keep", ["G002"], "“拿到好价”是其明确的优先目标，保留为G002。")
C("C008", "Check dozens of websites to make sure the best deal is found.", "explicit ('I check like dozens')", [],
  [E("DOC003:T025", "I check like dozens of different websites to just make sure I'm having the best deal possible.")],
  "explicit", "merge", ["G003"], "“查几十个网站确保最优价”是跨站比价行为，归G003。")
C("C009", "Find good deals for the winter break trip.", "uncertain ('I'm still looking')", [],
  [E("DOC003:T029", "I'm still looking for some good deals.")],
  "explicit", "exclude", [], "具体假期出行计划，无平台能力要求。")
C("C010", "Start research with three or four aggregators, using country pairs, nearby airports and flexible dates.", "descriptive ('generally my process')", [],
  [E("DOC003:T031", "generally my process starts with an aggregator. I generally have 3 to 4 aggregators that I take a look at."),
   E("DOC003:T031", "I generally do country to country pairs, or like a relative area of the destination")],
  "explicit", "merge", ["G004"], "多聚合器与国别/区域、邻近机场的起始检索方式，服务于扩大组合覆盖，归G004。")
C("C011", "Plan the trip so flight times connect with hotels and other transport and avoid staying 20 hours in a city doing nothing.", "explicit ('I try to plan out')", [],
  [E("DOC003:T031", "So I try to plan out my travel, such that things fall into place", "doing nothing.")],
  "explicit", "keep", ["G011"], "避免在城市长时间空等是明确的规避目标，保留为G011。")
C("C012", "Narrow options in the order: price first, then dates, then times and overall logistics.", "descriptive ('my 1st priority')", [],
  [E("DOC003:T031", "So my 1st priority starts with getting the price down", "finally onto like time and overall logistics.")],
  "explicit", "exclude", [], "检索优先级/顺序描述；价格与行程结果分别由G002、G001承接，不构成独立结果。")
C("C013", "Check provider costs, coupons, upgrade options and terminal/logistics information before booking.", "explicit ('I'll check out')", [],
  [E("DOC003:T031", "I'll check out what sort of coupon options I have upgrade options I have."),
   E("DOC003:T031", "I'll just make sure all the terminal, all the logistics. Information is correct.")],
  "explicit", "merge", ["G003"], "提供方费用、优惠与物流核对属比价/确认步骤，归G003；物流信息核对亦服务G006的信息集中。")
C("C014", "Sometimes check providers directly, outside the aggregator, to get a better discount.", "explicit ('sometimes')", [],
  [E("DOC003:T031", "I also sometimes check out providers directly without going through an aggregator. Sometimes you can get a better discount that way.")],
  "explicit", "merge", ["G003"], "直接查提供方以获得更优折扣，是跨提供方比价的一部分，归G003。")
C("C015", "Complete checkout by entering passenger details and declaration forms and paying by credit card.", "explicit ('I just fill out')", [],
  [E("DOC003:T031", "I just fill out my information.", "And I just pay the amount through my credit card website.")],
  "explicit", "exclude", [], "最终填表与支付属提供方网站上的常规结账步骤，平台不承担（T045/T133），无独立平台目标。")
C("C016", "Experience the discovery of finding good deals and apply tricks learned from FlyerTalk to beat airline pricing.", "preference ('I really like that')", [],
  [E("DOC003:T033", "there's a definite dopamine hit to like finding a good deal."),
   E("DOC003:T033", "There's a lot of different tricks that you end up getting to know about.")],
  "explicit", "exclude", [], "对“发现好价”的个人享受与技巧偏好，非平台目标；作为与G005（省时）的张力记入问题。")
C("C017", "Be handed to the chosen provider's booking page with the itinerary and personal details already filled in.", "descriptive ('directly takes me')", [],
  [E("DOC003:T047", "Skyscanner directly takes me to the exact booking page", "making the final payment."),
   E("DOC003:T135", "the flight details will already be filled in", "which flight I'm taking.")],
  "explicit", "keep", ["G013"], "预填行程与信息的交接触点独立且被明确描述为剩余“确认与支付”，保留为G013（推断维持意图）。")
C("C018", "Stay anonymous while searching by not logging in, so as not to be tracked or charged higher prices.", "strong preference ('very privacy conscious')", [],
  [E("DOC003:T053", "I generally am very privacy conscious.", "as anonymized as possible."),
   E("DOC003:T053", "they might increase the flight prices for you")],
  "explicit", "keep", ["G007"], "匿名搜索与避免差别定价是明确、稳定的目标，保留为G007。")
C("C019", "For award bookings, log into the airline loyalty site to see and book award seats.", "explicit ('I'd log on')", [],
  [E("DOC003:T057", "So if I have to make a points or an award booking, I'd log on to the airline that I have a loyalty account with")],
  "explicit", "exclude", [], "积分/奖励票须在航司站点操作，明确不在本活动（现金票浏览）范围内。")
C("C020", "Search a whole country or region as origin or destination so many airports are looked up at once.", "explicit ('I generally put in')", [],
  [E("DOC003:T065", "I generally put in a country or a region that gives me way.", "More airports looked up at the same time.")],
  "explicit", "merge", ["G004"], "按国家/区域一次查多个机场，是G004多组合检索的具体方式。")
C("C021", "Set a hard limit on the number of hours spent in the air.", "explicit ('If I also have')", [],
  [E("DOC003:T069", "If I also have a hard limit on the number of hours I want to spend in the sky.")],
  "explicit", "merge", ["G011"], "对空中时长的硬限制服务于避免过长行程，归G011。")
C("C022", "Adjust departure and arrival time windows when the flight connects to something else.", "explicit ('If I'm connecting')", [],
  [E("DOC003:T069", "So if I'm connecting to something, then I can put the like, change the departure and the arrival time", "I want it to be.")],
  "explicit", "merge", ["G001"], "按衔接调整时间窗，是判断行程是否适合日程的具体方式，归G001。")
C("C023", "Use the 'best' tab for international trips to avoid 40-60 hour cheap options, and the cheapest tab for domestic trips.", "explicit ('that's what I refer to')", [],
  [E("DOC003:T073", "So that's what I refer to when I'm booking international, when I'm booking domestic, it's mostly going through the cheapest tab.")],
  "explicit", "split", ["G002", "G011"], "同句含价格标签选择（G002）与规避40–60小时长行程（G011）两个独立结果。")
C("C024", "See detailed connection information such as layover duration, local times, arrival day and total duration.", "explicit ('I use both extensively')", [],
  [E("DOC003:T077", "I use both of these very extensively."),
   E("DOC003:T075", "this is the time I take off.", "How many hours am I gonna have to wait in the Istanbul airport?")],
  "explicit", "keep", ["G014"], "中转与时间详情是独立的信息需求，保留为G014。")
C("C025", "Make sure all flight details, connections and times are right and work for my schedule.", "explicit ('I make sure')", [],
  [E("DOC003:T077", "I make sure all the flight details like I said.", "they work for my schedule.")],
  "explicit", "keep", ["G001"], "核对衔接与时间是否适合自身日程，是“好行程”目标的核心表述，保留为G001。")
C("C026", "Compare providers on price, rating and discounts for the same itinerary.", "explicit ('I look at...')", [],
  [E("DOC003:T077", "I look at the price. I take a look at the rating, and I often visit multiple providers from this page.")],
  "explicit", "merge", ["G003"], "按价格、评分与折扣比较提供方，归G003。")
C("C027", "Re-run all options when an itinerary does not meet expectations, and accept the only option when the booking is urgent.", "explicit ('I try to just rerun')", [],
  [E("DOC003:T081", "I try to just rerun through all of my options. Make sure I'm not missing something."),
   E("DOC003:T081", "if that is the only option I have, so be it.")],
  "explicit", "merge", ["G001"], "不匹配时重跑是补救步骤；“紧急/唯一选择时接受”作为G001的例外条件保留。")
C("C028", "Prefer an itinerary that lands early enough to catch the last onward train, if the price difference is acceptable.", "conditional preference", [],
  [E("DOC003:T083", "If I had a better option available", "Then I would go for that option."),
   E("DOC003:T083", "it again depends on the price differential.")],
  "explicit", "merge", ["G001"], "以赶上末班车为条件的行程选择，是G001“衔接其他交通”的具体例证；价格权衡写入context。")
C("C029", "Have better alert options that tell me when flight prices drop.", "weak suggestion ('there could be better')", [],
  [E("DOC003:T085", "there could be better alert options to just let me know when flight prices drop down.")],
  "explicit", "merge", ["G008"], "降价提醒建议，归G008；其可行性怀疑作为context保留。")
C("C030", "Set price alerts on several routes and book when any one of them drops.", "explicit past use", [],
  [E("DOC003:T087", "I needed a reminder on a few different routes", "I I book it")],
  "explicit", "keep", ["G008"], "多路线降价提醒的实际使用，保留为G008。")
C("C031", "Browse in incognito and block cookies so personal data is not shared with another party.", "explicit ('I go through')", [],
  [E("DOC003:T089", "I go through an incognito window route. and I block all the cookies.")],
  "explicit", "merge", ["G007"], "无痕与屏蔽cookie是匿名目标的具体方式，归G007。")
C("C032", "Avoid logging in even if the data policy changes, unless the source code can be inspected.", "strong ('probably never')", [],
  [E("DOC003:T093", "I would probably never log in. It would be a very specific scenario that I really need to do this.")],
  "explicit", "merge", ["G007"], "对登录的强拒绝及其例外，归G007并保留强度。")
C("C033", "Run the hundreds of combination searches needed for a trip at the same time.", "explicit obstacle", [],
  [E("DOC003:T095", "The research aspect is the biggest obstacle, because you want to do around 500 searches at the same time", "you want to do around 500 searches at the same time")],
  "explicit", "keep", ["G004"], "“同时跑数百个组合搜索”是明确的检索目标/障碍，保留为G004。")
C("C034", "Keep research within 10-15 minutes when possible, rather than a couple of hours spread over days.", "descriptive baseline", [],
  [E("DOC003:T097", "If things are working out my way, maybe it will just be 10 to 15", "distributed over several days as well.")],
  "explicit", "merge", ["G005"], "现状耗时作为G005（更快研究）的改善基线。")
C("C035", "Search roughly 11,760 combinations of airports, dates and cabin classes.", "explicit illustration", [],
  [E("DOC003:T099", "So that works out to be 11,760 different combinations of flights")],
  "explicit", "merge", ["G004"], "11,760组合是G004规模的示例说明。")
C("C036", "Use flexible date ranges and 'everywhere' destination search like other aggregators offer.", "descriptive comparison ('more convenient')", [],
  [E("DOC003:T101", "it allows me to take a date range of plus minus 3 days on both the sites"),
   E("DOC003:T101", "Google flights does it differently. It allows you to search everywhere.")],
  "explicit", "merge", ["G004"], "灵活日期范围与“任意目的地”检索是扩大组合覆盖的方式，归G004。")
C("C037", "Use aggregators for flexibility in finding the right itinerary.", "explicit ('they allow me')", [],
  [E("DOC003:T103", "They allow me to have more flexibility in terms of finding the right itinerary.")],
  "explicit", "merge", ["G004"], "聚合器的检索灵活性服务于扩大组合覆盖与找对行程，归G004。")
C("C038", "Find the best price for a chosen itinerary by comparing all booking options.", "explicit ('they allow me')", [],
  [E("DOC003:T103", "they allow me to find the best price for that itinerary.", "comparing all of the different booking options.")],
  "explicit", "keep", ["G003"], "对既定行程比较全部预订选项以取得最优价，保留为G003。")
C("C039", "Get the aggregator's protection and coupons when they work in my favour, otherwise book wherever the deal is better.", "conditional", [],
  [E("DOC003:T103", "they also provide a certain level of protection, and they also provide their own set of coupons.")],
  "explicit", "merge", ["G003"], "保护与优惠券纳入提供方比较，归G003。")
C("C040", "Default to Skyscanner because I know its interface, and switch to other aggregators when results are not good.", "preference/actual practice", [],
  [E("DOC003:T105", "skyscanner was the 1st in the game, and that's the one I've been using for many years."),
   E("DOC003:T105", "when I'm not getting the best results. That's when I go to Google flights, or to kayak")],
  "explicit", "merge", ["G005"], "熟悉界面带来的时间优势归G005；工具选择习惯不另立目标。")
C("C041", "Achieve 'best results' as a combination of itinerary logistics, price and flexibility.", "definition ('for me')", [],
  [E("DOC003:T107", "Best results for me is a combination of the logistics in terms of the itinerary that I want the price and the flexibility."),
   E("DOC003:T107", "mostly focusing on the 1st 2.")],
  "explicit", "split", ["G001", "G002"], "“best results”由行程物流与价格构成，分别归G001、G002；flexibility未定义，未单独立目标（记入问题）。")
C("C042", "Know whether a price is above or below the median for an unfamiliar market.", "explicit use", [],
  [E("DOC003:T109", "I can use Google flights for it because it tells me if the price is above, below, or lower than the Median.")],
  "explicit", "keep", ["G009"], "中位数比较支持价格判断，保留为G009。")
C("C043", "Show the market price comparison on Skyscanner for unfamiliar markets.", "weak ('nice to have')", [],
  [E("DOC003:T111", "it would help out for the times when I'm not familiar with the specific market."),
   E("DOC003:T111", "it's nice to have.")],
  "explicit", "merge", ["G009"], "在Skyscanner显示市场比较，与G009同一结果（弱偏好）。")
C("C044", "Research to find a good itinerary and a good price that work for me.", "explicit top goal", [],
  [E("DOC003:T115", "The 1st perspective is finding, doing research, and I would do that in terms of finding a good itinerary and finding a good price that works for me.")],
  "explicit", "split", ["G001", "G002"], "同句含好行程与好价格两个可独立满足的结果，分别归G001、G002。")
C("C045", "Compare different booking websites to find the best combination of options.", "explicit top goal", [],
  [E("DOC003:T115", "I would also use it to compare different booking websites, just to figure out which one is giving me the best possible combination of options.")],
  "explicit", "merge", ["G003"], "与G003同义，合并保留一个目标。")
C("C046", "Match the itinerary to onward transport schedules, people's schedules and a time of day that allows sleep.", "explicit examples ('a way to do it')", [],
  [E("DOC003:T119", "is it matching up with the schedules of the other modes of transport", "Is it matching up with their schedules."),
   E("DOC003:T119", "I would rather get my night's sleep.")],
  "explicit", "merge", ["G001"], "好行程的判断维度（交通/会面/睡眠）是其具体化，归G001。")
C("C047", "Allow at least 1.5x, preferably 2x, the minimum connection time at a stopover.", "explicit ('I generally tend to')", [],
  [E("DOC003:T123", "I generally don't care very much about it as long as the I am at least 1.5 x the Mct"),
   E("DOC003:T123", "I generally tend to at least go for 1.5 x or 2 x of that for a stopover.")],
  "explicit", "keep", ["G010"], "带明确倍数阈值的换乘约束，保留为G010。")
C("C048", "See whether the lounge at the connecting airport is open at that time.", "explicit personal factor", [],
  [E("DOC003:T123", "will the lounge at that airport be open at that point of time?")],
  "explicit", "merge", ["G015"], "休息室开放时间是休息室信息目标的具体内容，归G015。")
C("C049", "Have up-to-date lounge entitlement information integrated with the flight search.", "weak ('would be wonderful')", [],
  [E("DOC003:T125", "it would be very nice if I could, input there would be a website", "That would be wonderful."),
   E("DOC003:T125", "I prefer going to the source of the truth for the lounge access")],
  "explicit", "keep", ["G015"], "休息室权益信息与搜索整合的愿望，保留为G015（带准确性与源头偏好条件）。")
C("C050", "See good itineraries matching my situation, ideal prices, available city/date/time combinations and booking partners with discounts.", "explicit re-summary", [],
  [E("DOC003:T129", "It should give me a good itinerary in terms of times", "match my situations."),
   E("DOC003:T129", "It should show me what the ideal prices are", "available to me that work best for me."),
   E("DOC003:T129", "it should provide me a set of booking partners that potentially have discounts.")],
  "explicit", "split", ["G001", "G002", "G004", "G003"], "一句总结四个可独立满足的结果：行程匹配、理想价格、组合可得性、提供方优惠；分别归四目标。")
C("C051", "Narrow options with filters and compare itineraries and booking partners before paying.", "explicit process summary", [],
  [E("DOC003:T131", "I would narrow them down based on my filters and different combinations."),
   E("DOC003:T131", "I would then check out what is the best booking partner for these?")],
  "explicit", "merge", ["G003"], "收窄与比较流程中，比较/确定提供方部分归G003；行程筛选由G001承接。")
C("C052", "Have a one-click platform that takes all my parameters and finds the best option.", "complaint-derived", [],
  [E("DOC003:T137", "There's no one click platform where I can just give it all of my parameters, and it will find the best option for me.")],
  "inferred", "merge", ["G005"], "把“没有一键平台”的抱怨作为省时目标的依据；不把抱怨取反后另立自动化选优目标。")
C("C053", "Have all booking information in one place instead of visiting 10-12 sites.", "complaint", [],
  [E("DOC003:T137", "I don't get to have all of my information at one pace", "at a mostly at a minimum.")],
  "explicit", "keep", ["G006"], "信息分散的障碍句，保留为G006（推断目标）。")
C("C054", "Operate the site quickly because I know its interface and where each option is.", "descriptive", [],
  [E("DOC003:T143", "I'm familiar with all the nooks and crannies of the website."),
   E("DOC003:T143", "I'm generally aware of how to do that in a quick manner")],
  "explicit", "merge", ["G005"], "界面熟悉带来的速度优势归G005。")
C("C055", "Save time and mental load across dozens of searches.", "explicit ('just saves you time')", [],
  [E("DOC003:T147", "Because the mental load makes you take more time."),
   E("DOC003:T147", "when you are having to do dozens and dozens of searches")],
  "explicit", "keep", ["G005"], "省时与降低心力是明确目标，保留为G005。")
C("C056", "Switch to a platform that lets me research more quickly, with more combinations and more accuracy for less time.", "conditional ('I would definitely')", [],
  [E("DOC003:T149", "If I was able to do research at a much quicker pace.", "while spending less time at it.")],
  "explicit", "split", ["G004", "G005"], "同句含“同时看更多组合”（G004）与“更快/更省时”（G005）两个独立结果。")
C("C057", "Switch for long-term use even if it saves only a couple of minutes per search.", "conditional long-term", [],
  [E("DOC003:T155", "If I'm doing it long term I would definitely do it, even if it's saving me just a couple of minutes, because they add up.")],
  "explicit", "merge", ["G005"], "长期累积的省时阈值，作为G005的context保留。")
C("C058", "Book about 80% of flights for myself and 20% for other people.", "descriptive ratio", [],
  [E("DOC003:T017", "it's like 80 20 like myself to everybody else.")],
  "explicit", "merge", ["G012"], "自我/他人订票比例是G012的情境量化。")
C("C059", "Check timings against hotel needs and other modes of transport so the trip falls into place.", "explicit", [],
  [E("DOC003:T031", "I look around the timings that are available. how that would factor it into whether I have to book a hotel. How does that connect with other modes of transport?")],
  "explicit", "merge", ["G001"], "时间与酒店/其他交通的衔接是G001的组成。")
C("C060", "Drop the price benchmark feature once I know the market.", "conditional negation", [],
  [E("DOC003:T111", "once I become more familiar with the prices I would I would be able to. I won't really need that feature.")],
  "explicit", "merge", ["G009"], "熟悉市场后不再需要基准，作为G009的适用条件保留。")
C("C061", "Research over days or weeks depending on how much time I have.", "descriptive", [],
  [E("DOC003:T027", "When I have got a little bit more time, though, I try to look out for like a better deal sometimes that's over weeks, sometimes it's just over days.")],
  "explicit", "merge", ["G008"], "跨天/跨周检索节奏支持价格提醒的使用情境，归G008。")
C("C062", "See little scope for improving prediction of the ideal booking time.", "belief/negative", [],
  [E("DOC003:T085", "So I don't see much scope for improvement here. No.")],
  "explicit", "exclude", [], "对改进空间的悲观判断，属信念/否定，不构成目标；写入G008的context。")
C("C063", "Do research on the aggregator and leave only the final booking to the provider website.", "descriptive", [],
  [E("DOC003:T045", "I do all of my research and planning on this website and other aggregators. And but the final booking is made on one of the booking providers website")],
  "explicit", "merge", ["G013"], "研究在聚合器、最终预订在提供方的分工，是G013交接目标的情境。")
C("C064", "Mostly use the cheapest or best tabs rather than filters.", "descriptive", [],
  [E("DOC003:T069", "So mostly I just switch over to the cheapest or the best tabs.")],
  "explicit", "merge", ["G002"], "主要看最便宜/最佳标签，支持价格优先，归G002。")
C("C065", "Trust a company with personal data only if I can inspect how it is handled.", "strong belief", [],
  [E("DOC003:T093", "Unless I see the source code myself. I don't believe any company", "my default sense is to not trust somebody.")],
  "explicit", "merge", ["G007"], "信任是隐私与匿名使用的理由，归G007。")

# ---------------- relations ----------------
relations = [
    dict(relation_id="R1", source_id="G004", target_id="G005", type="operationalization", status="supported",
         conditions=["platform can execute the full combination set in an acceptable time"],
         assumptions=["一次覆盖大量组合能减少逐对搜索的往返次数"],
         rationale="受访者把“同一时间跑数百个组合搜索”当作缩短研究时间的实现方式；不声称单靠它就能让研究显著变快。",
         evidence_ids=[], evidence_quotes=[dict(source_id="DOC003:T095", quote=Q("DOC003:T095", "you want to do around 500 searches at the same time"), role="basis")]),
    dict(relation_id="R2", source_id="G006", target_id="G005", type="contribution", status="supported",
         conditions=[], assumptions=["集中信息减少的跨站切换不会被新的核对成本抵消"],
         rationale="把信息集中到一处可直接减少其在10–12个站点间来回核对的时间，从而帮助实现更快的检索。",
         evidence_ids=[], evidence_quotes=[dict(source_id="DOC003:T137", quote=Q("DOC003:T137", "I end up having to visit at least 10 to 12 different sites at a mostly at a minimum."), role="basis")]),
    dict(relation_id="R3", source_id="G003", target_id="G002", type="contribution", status="supported",
         conditions=[], assumptions=["各提供方报价差异不会小到可忽略"],
         rationale="比较多个预订网站能暴露同一行程的不同最终价与折扣，有助于拿到更好价格，但不保证最低价。",
         evidence_ids=[], evidence_quotes=[dict(source_id="DOC003:T103", quote=Q("DOC003:T103", "they allow me to find the best price for that itinerary.", "comparing all of the different booking options."), role="basis")]),
    dict(relation_id="R4", source_id="G008", target_id="G002", type="contribution", status="supported",
         conditions=["an alert fires before the fare rises again"],
         assumptions=["票价下跌窗口足够长，能完成预订"],
         rationale="多路线降价提醒让他在票价下探时及时下单，有助于取得更好价格；不保证价格一定下降。",
         evidence_ids=[], evidence_quotes=[dict(source_id="DOC003:T087", quote=Q("DOC003:T087", "if any one of them goes down in price. I I book it"), role="basis")]),
    dict(relation_id="R5", source_id="G009", target_id="G002", type="contribution", status="supported",
         conditions=["the market benchmark is available for that route"],
         assumptions=["中位数能代表该市场的常见价位"],
         rationale="价格相对市场中位数的判断帮助他识别当前报价是否偏高，从而支持拿到好价格；仅是判断辅助。",
         evidence_ids=[], evidence_quotes=[dict(source_id="DOC003:T111", quote=Q("DOC003:T111", "it would help out for the times when I'm not familiar with the specific market."), role="basis")]),
    dict(relation_id="R6", source_id="G010", target_id="G001", type="specialization", status="supported",
         conditions=["the itinerary includes at least one stopover"],
         assumptions=["MCT数据可得且按机场定义"],
         rationale="“换乘至少留1.5倍MCT”是“行程时间适合我”的一般目标在经停情境下的具体化；不声称覆盖无经停或签证受限的情形。",
         evidence_ids=[], evidence_quotes=[dict(source_id="DOC003:T123", quote=Q("DOC003:T123", "I generally tend to at least go for 1.5 x or 2 x of that for a stopover."), role="basis")]),
    dict(relation_id="R7", source_id="G011", target_id="G001", type="contribution", status="supported",
         conditions=[], assumptions=["空等与过长总时长确实会让行程不适合其日程"],
         rationale="避免长时间空等/过长总时长，有助于得到时间上真正可用的行程；不构成充分条件。",
         evidence_ids=[], evidence_quotes=[dict(source_id="DOC003:T073", quote=Q("DOC003:T073", "the cheapest section ends up being filled with a lot of stuff that's like 40, 50, 60"), role="basis")]),
    dict(relation_id="R8", source_id="G014", target_id="G001", type="contribution", status="supported",
         conditions=[], assumptions=["展示的衔接信息准确"],
         rationale="中转等待、当地时间与到达日等详情让他能判断行程是否与日程相符，从而帮助找到合适行程。",
         evidence_ids=[], evidence_quotes=[dict(source_id="DOC003:T077", quote=Q("DOC003:T077", "All the connections and all the times are right for me, and they work for my schedule."), role="basis")]),
    dict(relation_id="R9", source_id="G007", target_id="G002", type="contribution", status="supported",
         conditions=[], assumptions=["差别定价的判断来自其自述担心，未经验证"],
         rationale="他认为保持匿名可避免因被跟踪搜索而被提价，因此匿名有助于守住价格；该机制是受访者陈述的信念。",
         evidence_ids=[], evidence_quotes=[dict(source_id="DOC003:T053", quote=Q("DOC003:T053", "they might increase the flight prices for you"), role="basis")]),
]

# ---------------- groups ----------------
groups = [
    dict(group_id="GR1", parent_id="G005", child_ids=["G004", "G006"], kind="and", status="proposed", completeness="partial",
         rationale="一次覆盖大量组合与把信息集中到一处，分别压缩“逐对搜索”和“跨站核对”的时间，是让研究更快的最直接手段；但原文没有声称两者合起来足以让研究显著变快，也未覆盖其提到的“更准确”。",
         assumptions=["平台能在可接受时间内执行上万组合搜索", "信息集中后无需再逐站复核"],
         evidence_ids=[], evidence_quotes=[dict(source_id="DOC003:T137", quote=Q("DOC003:T137", "I end up having to visit at least 10 to 12 different sites at a mostly at a minimum."), role="basis")],
         relation_ids=["R1", "R2"],
         checks=[dict(kind="normal", origin="analysis_assumption",
                      scenario="一个有明确机场与日期范围的国际行程：一次搜索覆盖全部组合，并在同一处看到各提供方报价，检索用时明显下降。",
                      outcome="supports", rationale="两个子目标各自消除一类往返成本，正常情形下叠加后确实缩短检索。"),
                 dict(kind="exception", origin="analysis_assumption",
                      scenario="票价逐日波动需要隔几天回访，或用户不熟悉新界面：即使组合与信息集中，研究仍需多轮并带有学习成本。",
                      outcome="counterexample", rationale="该情形下两项目标并未覆盖回访与学习成本，无法声称整组足以实现显著更快。")]),
]

# ---------------- ledger ----------------
entries = []
for c in cands:
    entries.append(dict(candidate_id=c["candidate_id"], disposition=c["disposition"],
                        final_goal_ids=c["final_goal_ids"], reason=c["reason"]))

source_checks = [
    dict(check_id="S1", candidate_ids=["C003"], final_goal_ids=["G001", "G002"], outcome="represented",
         evidence_candidates=[E("DOC003:T009", "looking for good itineraries to plan to book things early so that I can get it at a better price.")],
         reason="好行程与更好价格分别由G001/G002承接；提前订票作为个人策略不单列（见S2）。"),
    dict(check_id="S2", candidate_ids=["C004"], final_goal_ids=[], outcome="excluded",
         evidence_candidates=[E("DOC003:T015", "Mostly I try to aim for at least one to 1.5 months out", "better price at a better deal.")],
         reason="订票时机属个人习惯，结果是更好价格（G002），不构成平台能力目标。"),
    dict(check_id="S3", candidate_ids=["C006"], final_goal_ids=[], outcome="excluded",
         evidence_candidates=[E("DOC003:T019", "I try to maximize my time in the air.")],
         reason="喜欢绕行/经停属个人旅行偏好，不是对应用的要求；与G011的实用行程规避分情境。"),
    dict(check_id="S4", candidate_ids=["C005"], final_goal_ids=["G012"], outcome="represented",
         evidence_candidates=[E("DOC003:T017", "I absolutely use it for friends and family", "family more so than friends.")],
         reason="为亲友订票是稳定的实际使用目标，由G012承接。"),
    dict(check_id="S5", candidate_ids=["C059"], final_goal_ids=["G001"], outcome="represented",
         evidence_candidates=[E("DOC003:T031", "how that would factor it into whether I have to book a hotel. How does that connect with other modes of transport?")],
         reason="时间与酒店/其他交通的衔接由G001承接。"),
    dict(check_id="S6", candidate_ids=["C018"], final_goal_ids=["G007"], outcome="represented",
         evidence_candidates=[E("DOC003:T053", "I avoid logging in, and I try to keep myself as anonymized as possible.")],
         reason="匿名/不登录的明确目标由G007承接。"),
    dict(check_id="S7", candidate_ids=["C028"], final_goal_ids=["G001"], outcome="represented",
         evidence_candidates=[E("DOC003:T083", "so that I would be able to make sure that I get home that night", "I don't miss my train")],
         reason="以衔接末班车为条件的行程选择由G001承接，价格权衡写入context。"),
    dict(check_id="S8", candidate_ids=["C033"], final_goal_ids=["G004"], outcome="represented",
         evidence_candidates=[E("DOC003:T095", "The research aspect is the biggest obstacle, because you want to do around 500 searches at the same time")],
         reason="数百组合同时检索由G004承接。"),
    dict(check_id="S9", candidate_ids=["C041"], final_goal_ids=["G001", "G002"], outcome="uncertain",
         evidence_candidates=[E("DOC003:T107", "Best results for me is a combination of the logistics in terms of the itinerary that I want the price and the flexibility.")],
         reason="物流与价格分别由G001/G002承接；“flexibility”未被定义，未单独立目标，作为未决项保留。"),
    dict(check_id="S10", candidate_ids=["C044", "C045"], final_goal_ids=["G001", "G002", "G003"], outcome="represented",
         evidence_candidates=[E("DOC003:T115", "finding a good itinerary and finding a good price that works for me.")],
         reason="他自述的三项主要目标分别由G001、G002、G003承接。"),
    dict(check_id="S11", candidate_ids=["C049"], final_goal_ids=["G015"], outcome="represented",
         evidence_candidates=[E("DOC003:T125", "That would be wonderful.")],
         reason="休息室信息整合的弱愿望由G015承接，准确性与源头偏好写入context。"),
    dict(check_id="S12", candidate_ids=["C052", "C053"], final_goal_ids=["G005", "G006"], outcome="represented",
         evidence_candidates=[E("DOC003:T137", "There's no one click platform where I can just give it all of my parameters, and it will find the best option for me.")],
         reason="“没有一键平台”支持省时目标G005，信息分散支持G006；未把一键自动化另立目标。"),
    dict(check_id="S13", candidate_ids=["C056"], final_goal_ids=["G004", "G005"], outcome="represented",
         evidence_candidates=[E("DOC003:T149", "look for much, much more combinations. At the same time, if I was able to more accurately research for things while spending less time at it.")],
         reason="更多组合由G004承接，更快/更省时由G005承接；“更准确”未单立目标。"),
    dict(check_id="S14", candidate_ids=["C019"], final_goal_ids=[], outcome="excluded",
         evidence_candidates=[E("DOC003:T057", "So if I have to make a points or an award booking, I'd log on to the airline that I have a loyalty account with")],
         reason="积分票操作明确在航司站点进行，不在本活动范围内。"),
    dict(check_id="S15", candidate_ids=["C029"], final_goal_ids=["G008"], outcome="uncertain",
         evidence_candidates=[E("DOC003:T085", "there could be better alert options to just let me know when flight prices drop down.")],
         reason="降价提醒需求存在，但受访者同时怀疑规则可行性；G008保留弱强度与怀疑条件。"),
    dict(check_id="S16", candidate_ids=["C051"], final_goal_ids=["G003"], outcome="represented",
         evidence_candidates=[E("DOC003:T131", "I would then check out what is the best booking partner for these?")],
         reason="确定最佳预订伙伴的流程由G003承接。"),
]

# window IDs
windows = json.loads((BASE / "work/source-windows.json").read_text(encoding="utf-8"))["windows"]
win_results = [dict(window_id=w["window_id"], status="processed", reason="") for w in windows]

spec = dict(
    document_id="DOC003",
    raw_candidates=[{k: v for k, v in c.items() if k not in ("disposition", "final_goal_ids", "reason")} | {"pass_id": "P1"}
                    for c in cands],
    goals=goals,
    review_questions=[
        dict(candidate_ids=["G006"], question="“把所有信息集中在一处”是指单个聚合器内，还是聚合器与预订提供方的统一视图？", reason="原文只说访问10–12个站点，未界定集中范围。"),
        dict(candidate_ids=["G015"], question="休息室信息集成与“以发卡行源头为准”的偏好冲突时，哪个优先？", reason="同一轮既说集成会“非常棒”，又说第三方更新不可靠、宁愿查发卡行。"),
        dict(candidate_ids=["G005"], question="“快得多/更省时”没有量化阈值，可接受的时长或节省比例是多少？", reason="受访者明确说该问题很主观、取决于当时忙闲。"),
        dict(candidate_ids=["G004"], question="11,760个组合是示例规模还是硬性上限？", reason="该数字由20×6×49×2推算，是说明性例子。"),
    ],
    limitations=[
        "访谈为口语转写，含识别噪声（如“Â”与不换行空格）与拼写变体；引文按原文逐字符保留，不据此改写语义。",
        "多处偏好以条件式（would/could）或“nice to have”表述，未给出量化阈值。",
        "活动范围限定为现金票的浏览、比价与预订；积分/奖励票不在范围。",
        "未执行独立语义评审、形式证明或人工确认。",
    ],
    ledger=dict(
        model="unknown", temperature="unknown", budget="1 initial pass + <=2 repair rounds", usage="unknown",
        skill_revision="a5952d426b1624a3fcb2ce2829e1ae1ceb15e19dc3309d9571f3bc6b465deb6f",
        prompt_revision="task-prompt-v1", planned_passes=1,
        stop_reason="完成一次逐窗捕获（81窗）与全篇校正；预算内未追加重复采样，未决项保留为问题。",
        passes=[dict(pass_id="P1", kind="initial", context="isolated", status="completed", window_results=win_results)],
        full_context_review=dict(status="completed",
                                 reason="回读全部163轮，核对指代（如“both of these”“these”）、条件继承（匿名例外、紧急订票例外、签证例外、熟悉市场后不再需要基准）、让步（红眼/绕行偏好）与相反证据（喜欢长航程 vs 规避过长行程；休息室集成 vs 源头优先）。"),
        entries=entries, source_checks=source_checks),
    decisions=dict(
        relations=relations, groups=groups,
        questions=[
            dict(target_type="group", target_id="GR1", message="G004+G006 是否足以让研究显著更快？原文只有感受性时长（10–15分钟到数小时），没有阈值，且“更准确”未被覆盖。"),
            dict(target_type="goal", target_id="G013", message="预填信息交接是明确要求，还是仅描述现有流程？维持意图需确认。"),
            dict(target_type="goal", target_id="G006", message="“一处”的范围未界定：单个聚合器、聚合器+提供方，还是含休息室等外部信息？"),
            dict(target_type="model", target_id="DOC003-goal-model", message="T107 的“flexibility”未被定义；是否需要独立目标或仅作为条件？"),
            dict(target_type="relation", target_id="R9", message="匿名避免涨价的贡献联系基于受访者担心（might），未经证实；是否保留为supported？"),
        ],
        reassessments=[]),
)

(BASE / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("candidates", len(spec["raw_candidates"]), "goals", len(goals), "entries", len(entries),
      "relations", len(relations), "groups", len(groups), "checks", len(source_checks), "windows", len(win_results))
