# 目标模型

版本：v1。人工待审。

- Find a flight itinerary whose timing fits my travel plans - matching onward transport and the schedules of people I am meeting, and ideally letting me sleep at night.
  适用条件：timing is judged against onward transport, hotel needs and people I am meeting；if the booking is urgent and no other itinerary exists, I accept an itinerary that does not fit；a better-fitting option is weighed against its price difference
- Find a good deal on the flight - primarily a low price, with seating and other benefits taken into account.
  适用条件：seating and other benefits are secondary considerations
- Compare different booking websites for the chosen itinerary to find the provider that offers the best price and overall deal.
  适用条件：comparison includes final cost, discounts and provider rating；if no provider deal is better, I book wherever the best coupon applies
- Search across many airport, city and country pairs and date ranges in a single search rather than one pair at a time (for example, about 11,760 combinations of airports, dates and cabin classes).
  适用条件：search by country or region so that many airports are looked up together
- Complete flight research much faster, with substantially less time and mental effort per search.
  适用条件：long-term switching: even a couple of minutes saved per search matters because they add up; a one-off saving may not be worth switching
- Get all the information needed for a booking in one place instead of visiting 10 to 12 different sites.
  适用条件：research otherwise spans several aggregators and booking providers
- Stay anonymous while searching flights - not logging in and blocking cookies - so that I am not tracked or quoted higher prices.
  适用条件：exception: award/points bookings require logging into the airline site, outside this browsing activity
- Receive price-drop alerts for several candidate routes so I can book as soon as one of them falls within reach.
  适用条件：used only once, on Google Flights, for a trip that had to be made；doubt that accurate alert rules are feasible because fares and plans change quickly
- Show whether a fare is above or below the typical price for that market, especially where I am unfamiliar with local prices.
  适用条件：needed only until I become familiar with the market
- Keep at least 1.5 times (preferably 2 times) the minimum connection time at any stopover.
  适用条件：unless visa constraints make a stopover unacceptable
- Avoid itineraries with long idle waits or excessive total travel time.
  适用条件：applies to practical trips; on leisure trips I may deliberately choose longer, stop-heavy routes
- Book flights on behalf of family and friends as well as myself, using leftover points or gift vouchers where possible.
  适用条件：about 80% of bookings are for myself and 20% for other people
- Continue from the aggregator to the chosen provider's checkout with the itinerary and my details already filled in, leaving only confirmation and payment.
  适用条件：the aggregator itself does not complete bookings
- See detailed connection and timing information - layovers, local times, arrival day and total duration - so I can judge whether an itinerary works.
- See the lounge access my cards and passes give me at the connecting airport inside the flight search, if it can be kept accurate.
  适用条件：about 30 cards with different lounge entitlements；existing third-party trackers do not update reliably; otherwise I use the issuer's own site

## 目标之间的联系

下列联系不表示充分精化；待确认及已否定记录保留各自状态。

- 有依据的联系：Search across many airport, city and country pairs and date ranges in a single search rather than one pair at a time (for example, about 11,760 combinations of airports, dates and cabin classes). —[实现方式]→ Complete flight research much faster, with substantially less time and mental effort per search.
  依据：受访者把“同一时间跑数百个组合搜索”当作缩短研究时间的实现方式；不声称单靠它就能让研究显著变快。
  条件／假设：platform can execute the full combination set in an acceptable time；一次覆盖大量组合能减少逐对搜索的往返次数
- 有依据的联系：Get all the information needed for a booking in one place instead of visiting 10 to 12 different sites. —[有助于]→ Complete flight research much faster, with substantially less time and mental effort per search.
  依据：把信息集中到一处可直接减少其在10–12个站点间来回核对的时间，从而帮助实现更快的检索。
  条件／假设：集中信息减少的跨站切换不会被新的核对成本抵消
- 有依据的联系：Compare different booking websites for the chosen itinerary to find the provider that offers the best price and overall deal. —[有助于]→ Find a good deal on the flight - primarily a low price, with seating and other benefits taken into account.
  依据：比较多个预订网站能暴露同一行程的不同最终价与折扣，有助于拿到更好价格，但不保证最低价。
  条件／假设：各提供方报价差异不会小到可忽略
- 有依据的联系：Receive price-drop alerts for several candidate routes so I can book as soon as one of them falls within reach. —[有助于]→ Find a good deal on the flight - primarily a low price, with seating and other benefits taken into account.
  依据：多路线降价提醒让他在票价下探时及时下单，有助于取得更好价格；不保证价格一定下降。
  条件／假设：an alert fires before the fare rises again；票价下跌窗口足够长，能完成预订
- 有依据的联系：Show whether a fare is above or below the typical price for that market, especially where I am unfamiliar with local prices. —[有助于]→ Find a good deal on the flight - primarily a low price, with seating and other benefits taken into account.
  依据：价格相对市场中位数的判断帮助他识别当前报价是否偏高，从而支持拿到好价格；仅是判断辅助。
  条件／假设：the market benchmark is available for that route；中位数能代表该市场的常见价位
- 有依据的联系：Keep at least 1.5 times (preferably 2 times) the minimum connection time at any stopover. —[范围具体化]→ Find a flight itinerary whose timing fits my travel plans - matching onward transport and the schedules of people I am meeting, and ideally letting me sleep at night.
  依据：“换乘至少留1.5倍MCT”是“行程时间适合我”的一般目标在经停情境下的具体化；不声称覆盖无经停或签证受限的情形。
  条件／假设：the itinerary includes at least one stopover；MCT数据可得且按机场定义
- 有依据的联系：Avoid itineraries with long idle waits or excessive total travel time. —[有助于]→ Find a flight itinerary whose timing fits my travel plans - matching onward transport and the schedules of people I am meeting, and ideally letting me sleep at night.
  依据：避免长时间空等/过长总时长，有助于得到时间上真正可用的行程；不构成充分条件。
  条件／假设：空等与过长总时长确实会让行程不适合其日程
- 有依据的联系：See detailed connection and timing information - layovers, local times, arrival day and total duration - so I can judge whether an itinerary works. —[有助于]→ Find a flight itinerary whose timing fits my travel plans - matching onward transport and the schedules of people I am meeting, and ideally letting me sleep at night.
  依据：中转等待、当地时间与到达日等详情让他能判断行程是否与日程相符，从而帮助找到合适行程。
  条件／假设：展示的衔接信息准确
- 有依据的联系：Stay anonymous while searching flights - not logging in and blocking cookies - so that I am not tracked or quoted higher prices. —[有助于]→ Find a good deal on the flight - primarily a low price, with seating and other benefits taken into account.
  依据：他认为保持匿名可避免因被跟踪搜索而被提价，因此匿名有助于守住价格；该机制是受访者陈述的信念。
  条件／假设：差别定价的判断来自其自述担心，未经验证

## 需要确认

- “把所有信息集中在一处”是指单个聚合器内，还是聚合器与预订提供方的统一视图？
- 休息室信息集成与“以发卡行源头为准”的偏好冲突时，哪个优先？
- “快得多/更省时”没有量化阈值，可接受的时长或节省比例是多少？
- 11,760个组合是示例规模还是硬性上限？
- G004+G006 是否足以让研究显著更快？原文只有感受性时长（10–15分钟到数小时），没有阈值，且“更准确”未被覆盖。
- 预填信息交接是明确要求，还是仅描述现有流程？维持意图需确认。
- “一处”的范围未界定：单个聚合器、聚合器+提供方，还是含休息室等外部信息？
- T107 的“flexibility”未被定义；是否需要独立目标或仅作为条件？
- 匿名避免涨价的贡献联系基于受访者担心（might），未经证实；是否保留为supported？
- 这组层级仍需确认，尚未作为成立的精化展示。
- 访谈为口语转写，含识别噪声（如“Â”与不换行空格）与拼写变体；引文按原文逐字符保留，不据此改写语义。
- 多处偏好以条件式（would/could）或“nice to have”表述，未给出量化阈值。
- 活动范围限定为现金票的浏览、比价与预订；积分/奖励票不在范围。
- 未执行独立语义评审、形式证明或人工确认。

原文与层级依据可在 HTML 中展开。结构检查不等于语义证明，意见导出后交回助手。
