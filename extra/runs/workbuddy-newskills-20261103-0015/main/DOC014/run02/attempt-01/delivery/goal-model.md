# 目标模型

版本：v1。人工待审。

- Check the next day's temperature before going out in order to decide whether to wear a thick or a light coat.
  适用条件：Daily routine；Checking the day before going out
- Skip cycling and take the bus instead when the weather is very cold.
  适用条件：Very cold weather
- Check the rain forecast and make sure to carry an umbrella when rain is forecast.
  适用条件：Rain is forecast
- When first opening the app, look at the temperature and at tomorrow's chance of rain before anything else.
  适用条件：When first opening the app
- Check the next day's hour-by-hour forecast, focused on the temperature and precipitation chance around the morning time before classes when actually going out.
  适用条件：Morning before classes；Using the hourly view
- Be warned by the app about severe weather events affecting his own city, so he notices them.
  适用条件：Severe weather event in his own city
- On receiving a typhoon alert, open the notification and check the severity and all the details provided.
  适用条件：A typhoon alert has been received
- Read the recommendations from local authorities or the government meteorological organization to decide whether to evacuate, seek shelter, stay inside, or just carry an umbrella and raincoat.
  适用条件：Warning includes official recommendations
- Adjust the day's plans based on the severity and the information given in the warning.
  适用条件：After reading the warning details
- Start checking the weather as soon as a trip is decided, using historical data or future/monthly forecasts to get a good estimate of the expected weather.
  适用条件：Trip decided, often a couple of weeks ahead
- Check cloud coverage when planning a trip and reconsider or cancel if it will be overcast, for example a beach vacation or an astronomical event trip.
  适用条件：Trip purpose depends on clear sky
- Defer the final go/no-go decision on a trip until about two or three days before, when the forecast is more accurate, and then decide based on the final forecast.
  适用条件：Close to the trip date
- Plan to screenshot temperature readings below zero and share them on social media.
  适用条件：Temperature reading below 0；Not done yet; planned soon
- Prefer a plain black or plain white background over the current dull blue colour scheme.
  适用条件：UI colour scheme
- Avoid pages crowded with four or five ads, including video ads, so the weather can still be checked quickly without distraction.
  适用条件：Main page and scrolling between tabs
- Make the layout more compact so related information sits closer together and is easier to read.
  适用条件：Switching from one tab to the next
- Consider paying for the ad-free/premium tier only if daily use exceeds 20-30 minutes or the radar section improves substantially; at current usage it is not required.
  适用条件：Ad-free tier costs 9.99 a year；Current use about 30-120 seconds in the morning
- Improve the radar section into a much more detailed, intuitive multi-parameter map (snow coverage, precipitation) with animated visuals.
  适用条件：Existing radar section compared with a startup he knows and with windy.com
- View temperatures in Celsius rather than the Fahrenheit default.
  适用条件：US default is Fahrenheit
- Keep weather.com notifications off, consistent with a general preference for no notifications.
  适用条件：Desktop browser version
- Prefer that location data stay in the local browser cache and be clearable, rather than be stored and be able to identify his city in a leak.
  适用条件：Rarely logs in；Location still shown without login
- Have very local weather data for specific non-city places such as hiking trails, a hotel in the middle of nowhere, or a mountain climbing route.
  适用条件：Destination is not a city

## 目标之间的联系

下列联系不表示充分精化；待确认及已否定记录保留各自状态。

- 有依据的联系：On receiving a typhoon alert, open the notification and check the severity and all the details provided. —[有助于]→ Adjust the day's plans based on the severity and the information given in the warning.
  依据：原句说调整当天安排取决于严重程度与所给信息，因此查看严重程度与详情有助于做出调整。
  条件／假设：收到并查看严重天气警报
- 有依据的联系：Read the recommendations from local authorities or the government meteorological organization to decide whether to evacuate, seek shelter, stay inside, or just carry an umbrella and raincoat. —[有助于]→ Adjust the day's plans based on the severity and the information given in the warning.
  依据：读官方建议是为了判断撤离/避难/仅带雨具，进而决定当天怎么调整，属帮助关系而非充分实现。
  条件／假设：警报附带官方建议
- 有依据的联系：Start checking the weather as soon as a trip is decided, using historical data or future/monthly forecasts to get a good estimate of the expected weather. —[过程先后]→ Defer the final go/no-go decision on a trip until about two or three days before, when the forecast is more accurate, and then decide based on the final forecast.
  依据：原文明确“几周前先看”→随日期接近预报更准→临期才有最终判断，先后的结果顺序清楚；先后不等于因果或精化。
  条件／假设：同一次出行规划
- 有依据的联系：Improve the radar section into a much more detailed, intuitive multi-parameter map (snow coverage, precipitation) with animated visuals. —[有助于]→ Consider paying for the ad-free/premium tier only if daily use exceeds 20-30 minutes or the radar section improves substantially; at current usage it is not required.
  依据：原句说若雷达做好他可能为享受雷达区而购买，即雷达改进有助于其付费决策；不表示一定购买。
  条件／假设：雷达改进达到其期待

## 需要确认

- 隐私相关目标是推断而非明确请求，是否应作为产品需求保留？
- 日常查温度/降雨被拆成四条目标，是否存在同义重复？
- 日常查温度/降雨被拆成四条目标，是否存在同义重复？
- 日常查温度/降雨被拆成四条目标，是否存在同义重复？
- 日常查温度/降雨被拆成四条目标，是否存在同义重复？
- 广告干扰与布局紧凑是否应合并为一个“快速查看”改善目标？
- 广告干扰与布局紧凑是否应合并为一个“快速查看”改善目标？
- 把“用量条件”与“雷达条件”合并为同一付费决策是否损失区分？
- 已检查精化组候选：父 G009“调整当天安排”，子 G007“查严重程度与详情”+ G008“读官方建议”。两者是决策输入，源文未说二者共同足以完成调整（还需形成决定并执行，且未给严重程度阈值），故不建组，保留 proposed 缺口说明。
- 已检查精化组候选：父 G012“临期最终决定”，子 G010“提前查预报”+ G011“查云量”。G010 与 G012 是先后关系（见 R3），G011 触发的是重新考虑而非最终决定；源文没有“旅行天气规划”这一上层目标，补父目标会造根，故不建组。
- 已检查日常簇 G001/G003/G004/G005 能否归入共同父目标：源文只给出具体决策（外套、雨伞、首看项、出门时段），未表达更高层目的；若设“日常出行准备”父目标属分析者补造，故不建组。
- 已检查 G015（避免广告干扰快速查看）与 G016（布局紧凑便于阅读）的 AND 组：二者结果部分重叠，但源文只把“快速查看”作为受广告影响的体验，未表述为可由两者共同满足的目标，且布局建议是 maybe 级建议；故不建组。
- 隐私目标由“缓存可清除所以不担心被存储”与“登录后泄露会怕”推断，不是明确请求；是否作为产品需求保留待确认。
- 把“用量超过 20-30 分钟才考虑付费”与“雷达做好才考虑买”合并为同一付费决策，是否掩盖了两个不同触发条件？
- “很冷时可能改坐公交”用 might 表达，是稳定偏好还是偶发选择？目标已保留条件但强度仍待确认。
- “本市严重天气会注意到”是对假设情境（佛州天气事件）的预期，而非已发生行为；作为目标保留是否合适待确认。
- 原文为英文访谈自动转写，含识别噪声（如 '2030Â min'、'10 week weekend monthly radar tab'、'tap/tab' 混用），涉及数值处按上下文保守表述，未据此编造阈值。
- 受访者多次以 guess/pretty sure/not 100% sure 表达对数据来源、缓存与 guide 的推测；这些内容未作为目标事实使用。
- 采访者提出的应用内分享（T028）未获受访者确认，未建目标。
- 本轮仅使用 source/DOC014.json 全文与冻结技能，未参考任何历史目标、关系或评分。

原文与层级依据可在 HTML 中展开。结构检查不等于语义证明，意见导出后交回助手。
