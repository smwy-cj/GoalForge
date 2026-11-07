# 目标模型

版本：v1。人工待审。

- Search many origin, destination, date and cabin combinations at the same time to find the best option.
  适用条件：单次检索接口通常只允许有限机场数与日期范围
- Stay logged out and anonymous while searching for flights on the aggregator.
  适用条件：里程/积分票（award booking）为例外，须登录航空公司账户
- Keep his personal data from being collected or shared by the flight search and booking sites.
  适用条件：看不到平台源码即默认不信任其数据承诺
- Be alerted when fares on the specific routes he is watching drop, so that he can book at the lower price.
  适用条件：仅在必须赶到某地、票价波动剧烈的行程中使用过
- Book one to one-and-a-half months before departure to obtain a better fare.
  适用条件：理想情况是提前数月；临时出行会被压缩到出发前 1-2 周
- Search by country or region instead of a single airport so that many airports are covered in one query.
  适用条件：首屏会按 IP 自动填入最近机场，他主动改成国家/区域
- Restrict search results to his preferred departure and arrival windows and to a maximum number of hours in the air.
  适用条件：主要在需要衔接其他交通或长途国际行程时使用
- Rule out itineraries with 40 to 60 hours of total travel even when they are the cheapest listed.
  适用条件：国际行程中最低价列表常被超长行程占满
- Allow at least 1.5 to 2 times the airport's minimum connection time at each connection.
  适用条件：有签证限制时不适用
- Check whether the lounge at the connection airport is open at the connection time.
  适用条件：他持有 Priority Pass 并希望走访各地休息室
- Have his card-based lounge entitlements kept up to date in one place and shown alongside the flight search.
  适用条件：仅在信息能可靠更新时才有价值；否则他改查发卡方或机场的源头信息
- Show whether a fare is above or below the median for markets he is unfamiliar with.
  适用条件：属于 nice to have；熟悉该市场后不再需要
- Cut the time spent researching flights while covering more combinations.
  适用条件：愿意为更快检索承担更换平台的学习成本；长期使用时每次节省几分钟也值得
- Log in to the airline loyalty account to check award-seat availability and book a points ticket.
  适用条件：仅限里程/积分票；该场景不使用聚合器
- Take routings with extra stops and lounge visits when he travels for pleasure and is not pressed for time.
  适用条件：独自或非家人同行的度假行程；时间不紧张
- Keep using the aggregator interface he already knows so that each search takes less time.
  适用条件：切换平台的成本估计为每次多 30 秒到 1 分钟；结果不好时才换用 Google Flights、Kayak 等
- Find the best flight option for a planned cash booking through research on aggregators.
  适用条件：现金票（revenue booking）；里程票走航空公司渠道
  以下各项都需满足
    - Find a flight itinerary whose departure, arrival and connection times fit his onward transport, hotel needs and the schedules of the people he is meeting.
      适用条件：到达时间须能衔接后续交通（如末班火车）；时间紧迫且无更优替代时接受现有选项；票价差过大时可接受时间较不理想的选项
    - Find the best available fare for the itinerary he has chosen.
      适用条件：以现金支付的 revenue booking 为前提；判断价格好坏依赖对区域与枢纽的熟悉度
    - Compare the booking providers offered for a shortlisted itinerary and choose the one with the lowest final price and best terms.
      适用条件：最终出票与支付在供应商网站完成，聚合器只做导流
- Prefer flight times that let him sleep at night over red-eye departures.
  适用条件：可说'不介意'红眼，但更想睡整觉

## 目标之间的联系

下列联系不表示充分精化；待确认及已否定记录保留各自状态。

- 有依据的联系：Book one to one-and-a-half months before departure to obtain a better fare. —[有助于]→ Find the best available fare for the itinerary he has chosen.
  依据：提前订票的目的就是拿到更低票价，属有帮助但非充分。
- 有依据的联系：Search many origin, destination, date and cabin combinations at the same time to find the best option. —[有助于]→ Find the best available fare for the itinerary he has chosen.
  依据：并行铺开大量组合是为确认拿到的是最优报价。
- 有依据的联系：Compare the booking providers offered for a shortlisted itinerary and choose the one with the lowest final price and best terms. —[有助于]→ Find the best available fare for the itinerary he has chosen.
  依据：逐家供应商比价才能得到最低的最终实付价。
- 有依据的联系：Stay logged out and anonymous while searching for flights on the aggregator. —[实现方式]→ Keep his personal data from being collected or shared by the flight search and booking sites.
  依据：不登录、匿名是他用来减少数据被收集与追踪的具体方式。
- 有依据的联系：Be alerted when fares on the specific routes he is watching drop, so that he can book at the lower price. —[有助于]→ Find the best available fare for the itinerary he has chosen.
  依据：降价提醒用于在价格下探时立即下单，帮助拿到低价。
- 有依据的联系：Search by country or region instead of a single airport so that many airports are covered in one query. —[实现方式]→ Search many origin, destination, date and cabin combinations at the same time to find the best option.
  依据：以国家/区域为输入是一次查询覆盖多机场的手段。
- 有依据的联系：Restrict search results to his preferred departure and arrival windows and to a maximum number of hours in the air. —[有助于]→ Find a flight itinerary whose departure, arrival and connection times fit his onward transport, hotel needs and the schedules of the people he is meeting.
  依据：用时段与总时长上限把结果收敛到可接受的时间范围。
  条件／假设：需要衔接其他交通或长途国际行程
- 有依据的联系：Rule out itineraries with 40 to 60 hours of total travel even when they are the cheapest listed. —[有助于]→ Find a flight itinerary whose departure, arrival and connection times fit his onward transport, hotel needs and the schedules of the people he is meeting.
  依据：剔除 40-60 小时行程使结果符合他对行程时长的要求。
- 有依据的联系：Allow at least 1.5 to 2 times the airport's minimum connection time at each connection. —[有助于]→ Find a flight itinerary whose departure, arrival and connection times fit his onward transport, hotel needs and the schedules of the people he is meeting.
  依据：MCT 缓冲保证中转衔接可行，是行程可用的条件之一。
- 有依据的联系：Check whether the lounge at the connection airport is open at the connection time. —[有助于]→ Take routings with extra stops and lounge visits when he travels for pleasure and is not pressed for time.
  依据：确认休息室开放时间是为了在行程中真的用上休息室。
- 待确认联系：Have his card-based lounge entitlements kept up to date in one place and shown alongside the flight search. —[有助于]→ Check whether the lounge at the connection airport is open at the connection time.
  依据：原文只说整合'会很好'，且他更信任发卡方源头信息，未直接断言该帮助，故标 proposed。
  条件／假设：权益信息须可靠更新；把权益集中一处可帮助判断能否进入休息室
- 有依据的联系：Show whether a fare is above or below the median for markets he is unfamiliar with. —[有助于]→ Find the best available fare for the itinerary he has chosen.
  依据：中位价对比帮助他判断报价是偏高还是偏低。
  条件／假设：仅在没经验的市场
- 有依据的联系：Keep using the aggregator interface he already knows so that each search takes less time. —[有助于]→ Cut the time spent researching flights while covering more combinations.
  依据：熟悉界面直接减少每次检索的操作时间。
- 有依据的联系：Find a flight itinerary whose departure, arrival and connection times fit his onward transport, hotel needs and the schedules of the people he is meeting. —[有助于]→ Find the best flight option for a planned cash booking through research on aggregators.
  依据：找到可用行程是聚合器研究的第一项产出。
- 有依据的联系：Find the best available fare for the itinerary he has chosen. —[有助于]→ Find the best flight option for a planned cash booking through research on aggregators.
  依据：确认理想价格是研究的第二项产出。
- 有依据的联系：Compare the booking providers offered for a shortlisted itinerary and choose the one with the lowest final price and best terms. —[有助于]→ Find the best flight option for a planned cash booking through research on aggregators.
  依据：比较预订网站是受访者列出的第三项目标，服务于找到最优预订方案。
- 有依据的联系：Find a flight itinerary whose departure, arrival and connection times fit his onward transport, hotel needs and the schedules of the people he is meeting. —[过程先后]→ Compare the booking providers offered for a shortlisted itinerary and choose the one with the lowest final price and best terms.
  依据：先定下候选中转行程，再进入供应商页面比价选伙伴；只表示先后，不表示因果或精化。

## 需要确认

- 休息室权益聚合是否应作为需求保留？他同时说第三方更新不准、宁愿查发卡方源头。
- 以 G020 作为三目标之上的一般目标是否符合他的本意，还是他并不认为自己有第四层目的？
- 偏好增加中转与排除 40-60 小时行程是否需要在同一行程上同时成立？
- 偏好增加中转与排除 40-60 小时行程是否需要在同一行程上同时成立？
- 中位价对比只是 nice to have，是否应进入需求集合而非仅记录为期望？
- 里程票流程（须登录航司）是否属于本应用范围？采访者限定在浏览航班的聚合器场景。
- 已检查但未建立联系：G011（排除 40-60 小时行程）与 G018（偏好增加中转、最大化空中时间）分属最低价列表与度假体验两种情境，原文没有把两者放在同一约束下的句子，未建边，也未判为冲突。
- 已检查但未建立联系：G017（里程票须登录航司）与 G005（匿名检索）在原文是例外关系（T053 'unless I'm booking with points'），已写成 G005 的 context，不构成贡献或精化边。
- 已检查但未建立联系：G006（数据不被共享）与 G002/G003（比价）在原文没有相互影响的表述；G006 只与 G005 有实现方式联系，未额外连边。
- 已评估但未成立的第二个精化组：G008/G004/G007/G003 对 G002 只有帮助，票价由航空公司控制，原文未声称这些动作共同足以保证最优价，故不建组。
- 休息室权益聚合的愿望与'更信任发卡方源头信息'并存，是否保留为需求待确认。
- 组内三项在紧急出行只剩一条行程时会退化为单一选项，是否仍视为满足父目标，需人工确认。
- G014 对 G013 的帮助未被原文直接断言，保持 proposed，待确认是否应否定。
- 这项联系尚待确认，不表示充分精化。
- 原文为英文访谈转写，含转写与编码噪声（如 'Â h'、Skyscanner/Sky Scanner/Skyscan 混写），引文一律逐字符取自原文，未做拼写修正。
- T031 单轮超过 2000 字符，初次阅读视图被截断显示，已用完整原文重新核对后再引用。
- 受访者对'好价格''好行程'明确表示无法给出客观标准，模型未添加任何阈值。

原文与层级依据可在 HTML 中展开。结构检查不等于语义证明，意见导出后交回助手。
