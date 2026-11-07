# -*- coding: utf-8 -*-
"""Build spec.json with character-exact quotes pulled from the assigned source."""
import json
from pathlib import Path

A = Path(__file__).resolve().parent
DOC = json.loads((A / "source/DOC026.json").read_text(encoding="utf-8"))
TEXT = {t["source_id"]: t["text"] for t in DOC["turns"]}


def span(sid, start, end):
    t = TEXT[sid]
    i = t.find(start)
    if i < 0:
        raise ValueError(f"start not found in {sid}: {start!r}")
    j = t.find(end, i)
    if j < 0:
        raise ValueError(f"end not found in {sid}: {end!r}")
    quote = t[i:j + len(end)]
    if t.count(quote) != 1:
        raise ValueError(f"quote not unique in {sid} ({t.count(quote)}): {quote!r}")
    return {"source_id": sid, "quote": quote, "role": "basis"}


def ev(sid, start, end, role="basis"):
    d = span(sid, start, end)
    d["role"] = role
    return d


def T(sid, start, end, role="basis"):
    return ev(sid, start, end, role)


# ---------------- evidence snippets ----------------
E = {
    "main_goal": T("DOC026:T005", "For me, the main goal", "one place to another."),
    "time_price": T("DOC026:T007", "When I've chosen to look for a ride", "in deciding whether or not to take ride."),
    "no_drive": T("DOC026:T007", "It's usually like whether or not I'm able to drive there",
                  "which kind of depends on again the price and duration.", "context"),
    "walk": T("DOC026:T007", "So if it's going to take like an hour and a half", "even if it's kind of far away."),
    "cheapest": T("DOC026:T011", "I usually just go for The cheapest one", "unless if i'm going with more people"),
    "map": T("DOC026:T011", "I can also see a map with a couple different Ubers around", "if there are other drivers near me."),
    "wait": T("DOC026:T011", "if the price was too high", "then I can choose to wait"),
    "now_later": T("DOC026:T011", "I can also book it uh for now or later", "I rarely book something in the future."),
    "autocomplete": T("DOC026:T011", "a couple of different options pop up as I'm typing it", "before I necessarily finish typing it."),
    "promo": T("DOC026:T011", "telling me that there's a flash promo deal", "automatically applied."),
    "booking_fail": T("DOC026:T013", "sometimes when I click okay and try to book that driver", "can't find a driver."),
    "no_cancel": T("DOC026:T013", "I usually try not to cancel a ride", "rating of the passenger as well."),
    "charge_unknown": T("DOC026:T013", "I also don't remember if you get a a potential charge for that.",
                        "potential charge for that."),
    "start_to_cancel": T("DOC026:T015", "I kind of wish that I don't want to just start a ride to cancel it.",
                         "start a ride to cancel it."),
    "rent_work": T("DOC026:T019", "Most of the time when I book or when I'm traveling for work", "I would probably prefer to rent a car."),
    "work_time": T("DOC026:T019", "on the times where I have needed to to use a rideshare for work", "because my work is going to cover it."),
    "rent_duration": T("DOC026:T021", "But for the most part, I would choose to rent a car depending on the duration.",
                       "than to do a ride share every time I want to go someplace."),
    "bus": T("DOC026:T021", "So I usually do take a bus for my like planned route.", "My work gives me a free bus pass, basically."),
    "no_bus_unfamiliar": T("DOC026:T021", "Because I don't want to take a bus in a place I'm not familiar with", "not familiar with"),
    "uber_over_bus": T("DOC026:T021", "there are a lot of there are a lot of places", "I would probably prefer And Uber in that case."),
    "eats": T("DOC026:T025", "I have used it.", "so I've stopped using it."),
    "eats_bad": T("DOC026:T029", "It was a mixture of a bad estimate", "extraordinarily poor."),
    "human": T("DOC026:T031", "I found it very difficult because I wanted to talk to a person", "talk to a person"),
    "resolve": T("DOC026:T031", "if you actually want to actually resolve an issue", "you're probably going to need more than what they're like"),
    "single_dest": T("DOC026:T037", "Most of the time, if I'm going to use Uber", "versus going to multiple ones."),
    "quick_stop": T("DOC026:T037", "I always feel weird if I'm going to do that", "I try to make it as quick as possible"),
    "contact_helpful": T("DOC026:T039", "I actually find that very helpful.", "GPS just isn't great in that location."),
    "call_helpful": T("DOC026:T039", "So calling or calling usually calling on their way", "is usually really helpful"),
    "notify_helpful": T("DOC026:T039", "in the circumstance where I'm doing a multi-stop", "is also helpful"),
    "heads_up": T("DOC026:T041", "I think most of the time when I do want to change it", "instead of doing it on the app."),
    "pickup_easy_only": T("DOC026:T041", "But now I think it's only really easy", "from the start"),
    "pickup_hard": T("DOC026:T041", "when you have it be your location", "without actually booking a ride."),
    "fare": T("DOC026:T045", "I will go back And look at how much the ride was", "as a receipt to get reimbursed."),
    "rate_tip": T("DOC026:T045", "they give you the option to rate the driver", "option to tip the driver too"),
    "not_look": T("DOC026:T045", "But I don't really... look back at it for the location or the duration usually.",
                  "location or the duration usually."),
}

ST = "Stakeholder"


def c(cid, statement, modality, origin, evidence, context=None):
    return {"candidate_id": cid, "statement": statement, "actor": ST, "modality": modality,
            "context": context or [], "origin": origin, "pass_id": "P1", "evidence": evidence}


raw = [
    c("C001", "Use Uber mainly to get transportation from one place to another.", "stated main goal", "explicit", [E["main_goal"]]),
    c("C002", "Decide whether to take a ride by weighing how long the trip takes and what it costs.",
      "usual decision rule", "explicit", [E["time_price"], E["no_drive"]],
      ["Only when unable or unwilling to drive, or when no better transport option exists"]),
    c("C003", "Walk instead of taking a ride when the ride would take about an hour and a half.",
      "stated fallback rule", "explicit", [E["walk"]], ["Even if the destination is far away"]),
    c("C004", "Choose the cheapest ride option, except when traveling with more people.",
      "usual preference", "explicit", [E["cheapest"]]),
    c("C005", "See nearby drivers on a map to know whether drivers are available near me.",
      "valued feature", "explicit", [E["map"]]),
    c("C006", "Wait before booking when the price is too high.", "stated option", "explicit", [E["wait"]]),
    c("C007", "Book a driver shown as nearby without a long scheduling wait or a 'can't find a driver' ending.",
      "reported problem", "inferred", [E["booking_fail"]]),
    c("C008", "Avoid canceling rides in order to protect my passenger rating.", "stated intention", "explicit", [E["no_cancel"]]),
    c("C009", "Rent a car for work travel or vacations when walkability, driving needs and duration make it worthwhile.",
      "stated preference", "explicit", [E["rent_work"], E["rent_duration"]],
      ["Preferred over rideshare when traveling for work or on vacation"]),
    c("C010", "Care less about price and more about time on work rideshare trips, because the employer covers the cost.",
      "stated priority", "explicit", [E["work_time"]]),
    c("C011", "Take the bus for planned routes, including work trips covered by a free bus pass.",
      "usual practice", "explicit", [E["bus"]]),
    c("C012", "Avoid taking a bus in an area I am not familiar with.", "stated limit", "explicit", [E["no_bus_unfamiliar"]]),
    c("C013", "Take Uber instead of the bus when the bus trip would be long, require walking, or involve multiple transfers.",
      "stated preference", "explicit", [E["uber_over_bus"]]),
    c("C014", "Avoid using Uber Eats after a bad customer-service experience.", "stated decision", "explicit", [E["eats"], E["eats_bad"]]),
    c("C015", "Reach a human customer-support agent when I need an issue resolved.", "reported unmet need", "inferred",
      [E["human"], E["resolve"]]),
    c("C016", "Prefer a single destination over a multi-stop trip when using Uber.", "stated preference", "explicit", [E["single_dest"]]),
    c("C017", "Keep multi-stop trips as quick as possible, avoiding long in-between stops.", "stated effort", "explicit", [E["quick_stop"]]),
    c("C018", "Call or message the driver in the app when the pickup point is hard to find or the area is busy.",
      "stated practice", "explicit", [E["contact_helpful"], E["call_helpful"]],
      ["House numbers hard to see, poor GPS, no place to pull over, many people around"]),
    c("C019", "Let the driver know in the app when a multi-stop trip is taking longer than expected.",
      "hypothetical endorsement", "explicit", [E["notify_helpful"]]),
    c("C020", "Give the driver a heads-up directly instead of changing the pickup location in the app.",
      "preferred workaround", "explicit", [E["heads_up"]], ["When the pickup point needs to change"]),
    c("C021", "Adjust the pickup location in the app easily even when it was set from the current location.",
      "hedged complaint", "inferred", [E["pickup_easy_only"], E["pickup_hard"]]),
    c("C022", "Check the ride fare after the trip to split the charge with friends or use it as a receipt for reimbursement.",
      "usual practice", "explicit", [E["fare"]]),
    c("C023", "Book a ride for now rather than scheduling one for later.", "usage habit", "explicit", [E["now_later"]]),
    c("C024", "Pick an address suggestion while typing instead of finishing the full address.", "praised feature", "explicit", [E["autocomplete"]]),
    c("C025", "Have a flash promo automatically applied to the fare.", "observed feature", "explicit", [E["promo"]]),
    c("C026", "Rate and tip the driver after the ride.", "described routine", "explicit", [E["rate_tip"]]),
    c("C027", "Know whether a cancellation carries a charge.", "uncertain knowledge", "unknown", [E["charge_unknown"]]),
    c("C028", "Cancel a ride without first starting the ride just to cancel it.", "garbled wish", "unknown", [E["start_to_cancel"]]),
    c("C029", "Not review the ride's location or duration after the trip.", "described non-use", "explicit", [E["not_look"]]),
    c("C030", "Get an accurate time estimate for Uber Eats orders.", "reported complaint", "inferred", [E["eats_bad"]]),
]

goals = [
    {"candidate_id": "G001", "statement": "Use Uber mainly to get from one place to another.",
     "actor": ST, "context": [], "origin": "explicit", "inference": None, "evidence": [E["main_goal"]],
     "judgment": {"label": "direct", "rationale": "受访者直述使用 Uber 的主要目的是从此地到彼地，主体、范围与语气一致。",
                  "supported_parts": ["主体为受访者本人", "目的为完成地点间交通", "明确称为主要目标"],
                  "unsupported_parts": [], "assumptions": [], "reasoning_steps": []}},
    {"candidate_id": "G002", "statement": "Decide whether to take a ride by weighing the trip's duration and price.",
     "actor": ST, "context": ["Only when I cannot or do not want to drive there, or when no better transport option exists"],
     "origin": "explicit", "inference": None, "evidence": [E["time_price"], E["no_drive"]],
     "judgment": {"label": "direct", "rationale": "原句明确以时间与价格作为是否乘车的判断依据，并给出可自驾或其他交通方式的前提。",
                  "supported_parts": ["判断依据为时间与价格", "适用前提为不自驾且无更好方式"], "unsupported_parts": [],
                  "assumptions": [], "reasoning_steps": []}},
    {"candidate_id": "G003", "statement": "Walk to the destination instead of taking a ride when the ride would take about an hour and a half.",
     "actor": ST, "context": ["Even if the destination is far away"], "origin": "explicit", "inference": None,
     "evidence": [E["walk"]],
     "judgment": {"label": "direct", "rationale": "原句给出约一个半小时的样例阈值并明确表示宁可步行，含‘即使很远’的让步。",
                  "supported_parts": ["以约一个半小时为触发样例", "结果为改为步行", "保留即使很远的让步"],
                  "unsupported_parts": [], "assumptions": [], "reasoning_steps": []}},
    {"candidate_id": "G004", "statement": "Choose the cheapest ride option, except when traveling with more people.",
     "actor": ST, "context": ["Except when traveling with more people"], "origin": "explicit", "inference": None,
     "evidence": [E["cheapest"]],
     "judgment": {"label": "direct", "rationale": "原句明确‘通常选最便宜’，并以与他人同行作为例外，未把偏好升级为强制。",
                  "supported_parts": ["通常选最便宜", "多人同行时例外"], "unsupported_parts": [], "assumptions": [],
                  "reasoning_steps": []}},
    {"candidate_id": "G005", "statement": "See nearby drivers on the map so I know whether drivers are available near me.",
     "actor": ST, "context": [], "origin": "explicit", "inference": None, "evidence": [E["map"]],
     "judgment": {"label": "direct", "rationale": "原句说明地图上可见附近车辆，并给出‘知道附近是否有司机’的用途。",
                  "supported_parts": ["对象为地图上的附近司机", "目的为了解附近可用性"], "unsupported_parts": [],
                  "assumptions": [], "reasoning_steps": []}},
    {"candidate_id": "G006", "statement": "Wait before booking when the price is too high.",
     "actor": ST, "context": [], "origin": "explicit", "inference": None, "evidence": [E["wait"]],
     "judgment": {"label": "direct", "rationale": "原句明确若价格过高可选择等待，条件与行动均直接表述。",
                  "supported_parts": ["条件为价格过高", "行动为等待而非立即出发"], "unsupported_parts": [],
                  "assumptions": [], "reasoning_steps": []}},
    {"candidate_id": "G007", "statement": "Avoid long booking waits and 'can't find a driver' failures after the app shows a driver nearby.",
     "actor": ST, "context": [], "origin": "inferred",
     "inference": {"basis_candidate_ids": ["G005"], "reason": "受访者依赖地图上‘附近有司机’的信息，并报告该信息有时无法转化为成功匹配，由此推断其希望避免此失败结果。",
                   "assumptions": ["受访者希望附近可用性能够兑现为可完成的预订", "匹配失败被其视为问题而非可接受结果"]},
     "evidence": [E["booking_fail"]],
     "judgment": {"label": "inferred", "rationale": "原文直接描述长时间等待与‘找不到司机’的失败，但未直接说出改进要求；结合其使用附近司机可见性的目标推断避免该结果的意图。",
                  "supported_parts": ["失败情境为应用显示附近有司机", "失败表现为长时间调度与找不到司机"],
                  "unsupported_parts": [], "assumptions": ["希望可用性兑现为成功预订"], "reasoning_steps": ["由抱怨的失败状态推断其期望的相反结果"]}},
    {"candidate_id": "G008", "statement": "Avoid canceling rides in order to protect my passenger rating.",
     "actor": ST, "context": [], "origin": "explicit", "inference": None, "evidence": [E["no_cancel"]],
     "judgment": {"label": "direct", "rationale": "原句明确‘尽量不取消’，并说明原因是担心影响乘客评分；评分受损是其信念，目标本身为明确避免意图。",
                  "supported_parts": ["避免取消", "理由为保护乘客评分"], "unsupported_parts": [], "assumptions": [],
                  "reasoning_steps": []}},
    {"candidate_id": "G009", "statement": "Rent a car for work travel or vacations when walkability, driving needs and trip duration make it worthwhile.",
     "actor": ST, "context": ["Preferred over rideshare when traveling for work or on vacation"], "origin": "explicit",
     "inference": None, "evidence": [E["rent_work"], E["rent_duration"]],
     "judgment": {"label": "direct", "rationale": "两处原句均明确偏好租车，并给出步行便利度、用车量与行程时长等条件；一周假期为例，不另立固定场景目标。",
                  "supported_parts": ["偏好租车", "条件含步行便利度、用车量与时长", "涵盖工作出行与度假"], "unsupported_parts": [],
                  "assumptions": [], "reasoning_steps": []}},
    {"candidate_id": "G010", "statement": "Prioritize arrival time over price on work rideshare trips because my employer covers the cost.",
     "actor": ST, "context": ["Employer reimburses the trip"], "origin": "explicit", "inference": None,
     "evidence": [E["work_time"]],
     "judgment": {"label": "direct", "rationale": "原句明确工作出行时更在意时间而非价格，并说明费用由工作承担。",
                  "supported_parts": ["情境为工作出行", "时间优先于价格", "理由是费用由雇主承担"], "unsupported_parts": [],
                  "assumptions": [], "reasoning_steps": []}},
    {"candidate_id": "G011", "statement": "Take the bus for planned routes, including work trips covered by a free bus pass.",
     "actor": ST, "context": ["Work provides a free bus pass"], "origin": "explicit", "inference": None,
     "evidence": [E["bus"]],
     "judgment": {"label": "direct", "rationale": "原句说明通常对既定路线乘公交，工作场景因免费公交卡不必考虑费用。",
                  "supported_parts": ["对象为既定路线的公交", "工作场景有免费公交卡"], "unsupported_parts": [],
                  "assumptions": [], "reasoning_steps": []}},
    {"candidate_id": "G012", "statement": "Avoid taking a bus in an area I am not familiar with.",
     "actor": ST, "context": [], "origin": "explicit", "inference": None, "evidence": [E["no_bus_unfamiliar"]],
     "judgment": {"label": "direct", "rationale": "原句直接表述不愿在不熟悉的地方乘公交，为明确的避免型意图。",
                  "supported_parts": ["避免对象为公交", "条件为不熟悉该地区"], "unsupported_parts": [], "assumptions": [],
                  "reasoning_steps": []}},
    {"candidate_id": "G013", "statement": "Take Uber instead of the bus when the bus trip would be long, require walking, or involve multiple transfers.",
     "actor": ST, "context": [], "origin": "explicit", "inference": None, "evidence": [E["uber_over_bus"]],
     "judgment": {"label": "direct", "rationale": "原句列出公交耗时长、需步行、需换乘等复杂情形，并明确此时更倾向 Uber。",
                  "supported_parts": ["替代对象为公交", "触发条件含耗时长、步行、换乘", "结果为选 Uber"], "unsupported_parts": [],
                  "assumptions": [], "reasoning_steps": []}},
    {"candidate_id": "G014", "statement": "Avoid using Uber Eats after a bad customer-service experience.",
     "actor": ST, "context": [], "origin": "explicit", "inference": None, "evidence": [E["eats"], E["eats_bad"]],
     "judgment": {"label": "direct", "rationale": "原句说明有过糟糕体验并已停止使用，附加说明含时间预估差与客服极差两部分。",
                  "supported_parts": ["避免使用 Uber Eats", "原因含糟糕体验与客服问题"], "unsupported_parts": [],
                  "assumptions": [], "reasoning_steps": []}},
    {"candidate_id": "G015", "statement": "Reach a human customer-support agent when I need an issue resolved.",
     "actor": ST, "context": ["Rather than relying on automated or chatbot responses for issue resolution"],
     "origin": "inferred",
     "inference": {"basis_candidate_ids": ["G014"], "reason": "Uber Eats 的不良客服体验中，受访者明确想与真人对话并怀疑面对的是聊天机器人，由此推断其在需要解决问题时希望触达人工客服。",
                   "assumptions": ["该诉求不限于 Uber Eats 单一事件", "受访者仍会在需要时寻求客服"]},
     "evidence": [E["human"], E["resolve"]],
     "judgment": {"label": "inferred", "rationale": "原文直接说出‘想和人说话’及自动回复不足以解决问题，但未把‘触达人工’表述为一般目标；据该诉求推断。",
                  "supported_parts": ["需要与人对话", "自动/聊天机器人回复不足以解决实际问题"], "unsupported_parts": [],
                  "assumptions": ["适用于需要解决实际问题的客服场景"], "reasoning_steps": ["由单次体验中的明确诉求推断一般化目标"]}},
    {"candidate_id": "G016", "statement": "Prefer a single destination over a multi-stop trip when using Uber.",
     "actor": ST, "context": [], "origin": "explicit", "inference": None, "evidence": [E["single_dest"]],
     "judgment": {"label": "direct", "rationale": "原句明确‘多数情况下更愿意只去一个地点’，未否认偶尔使用多站点。",
                  "supported_parts": ["偏好单目的地", "对多站点为相对偏好而非禁止"], "unsupported_parts": [], "assumptions": [],
                  "reasoning_steps": []}},
    {"candidate_id": "G017", "statement": "Keep multi-stop trips as quick as possible, avoiding long in-between stops.",
     "actor": ST, "context": [], "origin": "explicit", "inference": None, "evidence": [E["quick_stop"]],
     "judgment": {"label": "direct", "rationale": "原句说明中间停靠耗时过长会感到不适，并明确尽量加快。",
                  "supported_parts": ["避免中间停靠耗时过长", "尽量让多站点行程快"], "unsupported_parts": [], "assumptions": [],
                  "reasoning_steps": []}},
    {"candidate_id": "G018", "statement": "Call or message the driver in the app when the pickup point is hard to find or the area is busy.",
     "actor": ST, "context": ["House numbers hard to see, poor GPS, no place to pull over, many people around"],
     "origin": "explicit", "inference": None, "evidence": [E["contact_helpful"], E["call_helpful"]],
     "judgment": {"label": "direct", "rationale": "原句说明用过应用内联系并认为很有帮助，给出难找地点与繁忙地点两类情境。",
                  "supported_parts": ["方式为应用内通话或消息", "情境含地点难找与区域繁忙", "评价为有帮助"], "unsupported_parts": [],
                  "assumptions": [], "reasoning_steps": []}},
    {"candidate_id": "G019", "statement": "Let the driver know in the app when a multi-stop trip is taking longer than expected.",
     "actor": ST, "context": ["Multi-stop trip"], "origin": "explicit", "inference": None, "evidence": [E["notify_helpful"]],
     "judgment": {"label": "direct", "rationale": "原句在该情境下评价提前告知司机有帮助；受访者同时说明自己未必这样做过，故只支持‘有帮助的做法’而非既有习惯。",
                  "supported_parts": ["情境为多站点且自己耗时较长", "方式为告知司机", "评价为有帮助"], "unsupported_parts": [],
                  "assumptions": ["该评价为假设性认可，不等于已执行"], "reasoning_steps": []}},
    {"candidate_id": "G020", "statement": "Give the driver a heads-up directly instead of changing the pickup location in the app.",
     "actor": ST, "context": ["When the pickup point needs to change"], "origin": "explicit", "inference": None,
     "evidence": [E["heads_up"]],
     "judgment": {"label": "direct", "rationale": "原句明确多数情况下直接告知司机，而不是在应用内修改；访谈者复述‘直接联系是首选’后受访者确认。",
                  "supported_parts": ["方式为直接告知司机", "与应用内修改形成取舍"], "unsupported_parts": [], "assumptions": [],
                  "reasoning_steps": []}},
    {"candidate_id": "G021", "statement": "Adjust the pickup location in the app easily even when it was set from the current location.",
     "actor": ST, "context": [], "origin": "inferred",
     "inference": {"basis_candidate_ids": ["G020"], "reason": "受访者因应用内改上车点不便而改用直接告知司机，由此推断其希望在使用当前位置时也能容易地改上车点。",
                   "assumptions": ["改用告知司机是对应用内不便的替代", "受访者对版本变化的记忆基本准确"]},
     "evidence": [E["pickup_easy_only"], E["pickup_hard"]],
     "judgment": {"label": "inferred", "rationale": "原文说改上车点如今只在未使用当前位置时容易，用当前位置时很难且需先下单；未直接提出改进要求，据其绕行做法推断。",
                  "supported_parts": ["使用当前位置时改上车点更难", "受访者因此改用告知司机"], "unsupported_parts": [],
                  "assumptions": ["记忆有保留但方向明确"], "reasoning_steps": ["由困难描述与替代做法推断期望的易用性"]}},
    {"candidate_id": "G022", "statement": "Check the ride fare after the trip to split the charge with friends or submit it as a receipt for reimbursement.",
     "actor": ST, "context": [], "origin": "explicit", "inference": None, "evidence": [E["fare"]],
     "judgment": {"label": "direct", "rationale": "原句明确回看车费，并给出与朋友分摊、工作报销两种用途。",
                  "supported_parts": ["对象为行程费用", "用途含分摊与报销凭证"], "unsupported_parts": [], "assumptions": [],
                  "reasoning_steps": []}},
]

review_questions = [
    {"candidate_ids": ["G007"], "question": "把‘显示附近有司机却长时间匹配或最终找不到司机’整理为需要避免的目标，是否超出了单次问题描述？",
     "reason": "原文只描述问题与猜测（应用夸大或司机拒单），未直接提出改进要求。"},
    {"candidate_ids": ["G019"], "question": "‘多站点迟到时告知司机’是受访者评价为有帮助、但自述未必做过的做法，是否应保留为软目标？",
     "reason": "该句为假设情境下的评价，不是已执行的惯例。"},
    {"candidate_ids": ["G021"], "question": "受访者称使用当前位置时改上车点较难，但语气有保留（I think、记不清版本变化），是否需要向本人确认？",
     "reason": "该目标是据抱怨与绕行做法推断，且依赖其对应用版本的记忆。"},
]

limitations = [
    "原文为访谈转写，含口语重复、断句与转写噪声（如T007、T011、T013、T041），个别语句只能按上下文理解。",
    "受访者多处对记忆不确定（取消是否收费、改上车点是否变更、客服是否为聊天机器人），相关判断保留其保留语气。",
    "未提供音频，无法核对语气、停顿与说话人识别；说话者仅依据转写标注。",
    "T015‘start a ride to cancel it’措辞含糊，无法确定其确切诉求，未据此建立目标。",
]

windows = [f"DOC026:W{i:04d}" for i in range(1, 24)]
pass1 = {"pass_id": "P1", "kind": "initial", "context": "isolated", "status": "completed",
         "window_results": [{"window_id": w, "status": "processed", "reason": ""} for w in windows]}

entries = []
for item in raw:
    cid = item["candidate_id"]
    gid = "G" + cid[1:]
    if cid in {"C023", "C024", "C025", "C026", "C027", "C029", "C030"}:
        entries.append({"candidate_id": cid, "disposition": "exclude", "final_goal_ids": [], "reason": ""})
    elif cid == "C028":
        entries.append({"candidate_id": cid, "disposition": "uncertain", "final_goal_ids": [], "reason": ""})
    else:
        entries.append({"candidate_id": cid, "disposition": "keep", "final_goal_ids": [gid], "reason": ""})

reasons = {
    "C023": "仅描述‘通常现在叫车、很少预约’的使用习惯，未表达要达成或维持的结果。",
    "C024": "对地址联想功能的赞许，属于现有体验评价，未提出要达到的独立结果。",
    "C025": "描述促销自动应用的观察，未表达目标；不因出现具体机制另建业务目标。",
    "C026": "评价与打赏是乘车后的常规动作，未表达需要被满足的结果。",
    "C027": "只是记不清取消是否收费，属于知识不确定，不构成目标。",
    "C028": "转写语义含糊，无法确定是希望取消无需先开始行程，还是仅不愿取消；不升级为目标。",
    "C029": "说明通常不回看位置或时长，仅描述不使用的功能，未表达避免意图。",
    "C030": "Uber Eats 时间预估差是糟糕体验的组成部分，已在‘避免使用 Uber Eats’中承接，不另立目标。",
}
for e in entries:
    if not e["reason"]:
        e["reason"] = "与最终目标的核心动作、主体与条件一致，保留原句中的条件与限定。"

source_checks = [
    {"check_id": "S1", "evidence_candidates": [E["main_goal"]], "candidate_ids": ["C001"], "final_goal_ids": ["G001"],
     "outcome": "represented", "reason": "主要目的原句直接映射到交通目标。"},
    {"check_id": "S2", "evidence_candidates": [E["time_price"], E["no_drive"], E["walk"]], "candidate_ids": ["C002", "C003"],
     "final_goal_ids": ["G002", "G003"], "outcome": "represented", "reason": "时间/价格判断与步行替代分别保留，前提与让步进入目标。"},
    {"check_id": "S3", "evidence_candidates": [E["cheapest"], E["map"], E["wait"]], "candidate_ids": ["C004", "C005", "C006"],
     "final_goal_ids": ["G004", "G005", "G006"], "outcome": "represented", "reason": "订车流程中的三个独立取舍分别建立目标。"},
    {"check_id": "S4", "evidence_candidates": [E["booking_fail"], E["no_cancel"]], "candidate_ids": ["C007", "C008"],
     "final_goal_ids": ["G007", "G008"], "outcome": "represented", "reason": "匹配失败转为避免型目标，取消顾虑单列，未混为同一目标。"},
    {"check_id": "S5", "evidence_candidates": [E["rent_work"], E["rent_duration"], E["work_time"]], "candidate_ids": ["C009", "C010"],
     "final_goal_ids": ["G009", "G010"], "outcome": "represented", "reason": "租车偏好与工作出行时间优先分别承接，条件保留。"},
    {"check_id": "S6", "evidence_candidates": [E["bus"], E["no_bus_unfamiliar"], E["uber_over_bus"]], "candidate_ids": ["C011", "C012", "C013"],
     "final_goal_ids": ["G011", "G012", "G013"], "outcome": "represented", "reason": "公交常规使用、陌生地区回避与复杂路线改叫车分为三项。"},
    {"check_id": "S7", "evidence_candidates": [E["eats"], E["eats_bad"]], "candidate_ids": ["C014"], "final_goal_ids": ["G014"],
     "outcome": "represented", "reason": "停止使用 Uber Eats 的明确决定保留，糟糕体验作为理由。"},
    {"check_id": "S8", "evidence_candidates": [E["human"], E["resolve"]], "candidate_ids": ["C015"], "final_goal_ids": ["G015"],
     "outcome": "represented", "reason": "想与真人对话的诉求推断为人工客服目标，未当作已实现的现状。"},
    {"check_id": "S9", "evidence_candidates": [E["single_dest"], E["quick_stop"]], "candidate_ids": ["C016", "C017"],
     "final_goal_ids": ["G016", "G017"], "outcome": "represented", "reason": "单目的地偏好与多站点加速是两个不同结果，未合并。"},
    {"check_id": "S10", "evidence_candidates": [E["contact_helpful"], E["call_helpful"], E["notify_helpful"]],
     "candidate_ids": ["C018", "C019"], "final_goal_ids": ["G018", "G019"], "outcome": "represented",
     "reason": "两类联系司机的情境分别保留，假设性评价在判断理由中标明。"},
    {"check_id": "S11", "evidence_candidates": [E["heads_up"], E["pickup_easy_only"], E["pickup_hard"]],
     "candidate_ids": ["C020", "C021"], "final_goal_ids": ["G020", "G021"], "outcome": "represented",
     "reason": "已选定的替代方式单独保留，易用性诉求据其推断，未把方式并入目标。"},
    {"check_id": "S12", "evidence_candidates": [E["fare"]], "candidate_ids": ["C022"], "final_goal_ids": ["G022"],
     "outcome": "represented", "reason": "回看车费的两个用途均保留。"},
    {"check_id": "S13", "evidence_candidates": [E["now_later"], E["autocomplete"], E["promo"]],
     "candidate_ids": ["C023", "C024", "C025"], "final_goal_ids": [], "outcome": "excluded",
     "reason": "使用习惯、对现有功能的赞许与促销观察，均无独立结果意图。"},
    {"check_id": "S14", "evidence_candidates": [E["charge_unknown"]], "candidate_ids": ["C027"], "final_goal_ids": [],
     "outcome": "excluded", "reason": "仅表示记不清是否收费，属于不确定知识。"},
    {"check_id": "S15", "evidence_candidates": [E["start_to_cancel"]], "candidate_ids": ["C028"], "final_goal_ids": [],
     "outcome": "uncertain", "reason": "转写含糊，无法确定确切诉求，保持待确认。"},
    {"check_id": "S16", "evidence_candidates": [E["rate_tip"], E["not_look"]], "candidate_ids": ["C026", "C029"],
     "final_goal_ids": [], "outcome": "excluded", "reason": "分别描述常规动作与不使用某信息，未表达目标。"},
    {"check_id": "S17", "evidence_candidates": [E["eats_bad"]], "candidate_ids": ["C030"], "final_goal_ids": [],
     "outcome": "excluded", "reason": "时间预估问题已归入避免使用 Uber Eats 的理由，不另造目标。"},
]

ledger = {
    "model": "unknown", "temperature": "unknown", "budget": "1 initial pass + <=2 repair rounds",
    "usage": "unknown", "skill_revision": "a5952d426b1624a3fcb2ce2829e1ae1ceb15e19dc3309d9571f3bc6b465deb6f",
    "prompt_revision": "task-prompt-v1", "planned_passes": 1,
    "stop_reason": "完成一次整篇读取与23个窗口处理，并回查关键原句；无新增有据意图，按预算停止。",
    "passes": [pass1],
    "full_context_review": {
        "status": "completed",
        "reason": "回看全部48轮：核对T007时间/价格条件与步行替代、T011‘除非多人’限定与等待选项、T013司机显示与匹配失败的对答范围、T015取消措辞、T019工作出行价格/时间反转、T021公交与租车条件、T031人工客服诉求、T041改上车点的保留语气、T045乘车后查看费用的目的；并确认采访者提问未获回应处（T017、T023、T028）不当作涉众目标。"},
    "entries": entries,
    "source_checks": source_checks,
}

decisions = {
    "relations": [
        {"relation_id": "R1", "source_id": "G010", "target_id": "G002", "type": "specialization",
         "status": "supported", "conditions": ["工作出行且费用由雇主承担"], "assumptions": [],
         "rationale": "工作出行是‘按时间与价格决定是否乘车’的具体情境；该情境下价格由雇主承担、时间权重上升，属于同一判断在特定条件下的具体化，而非另立一般目标。",
         "evidence_ids": [], "evidence_quotes": [E["work_time"]]},
        {"relation_id": "R2", "source_id": "G006", "target_id": "G002", "type": "operationalization",
         "status": "supported", "conditions": ["当前报价过高且行程可以延后"], "assumptions": [],
         "rationale": "价格过高时选择等待，是落实‘按时间与价格决定是否乘车’的具体策略，服务同一取舍目的，不声称等待总能使价格下降。",
         "evidence_ids": [], "evidence_quotes": [E["wait"]]},
    ],
    "groups": [],
    "questions": [
        {"target_type": "goal", "target_id": "G007",
         "message": "‘显示附近有司机却长时间匹配或最终找不到司机’是否应作为需改进的目标？原文只描述问题与猜测，没有明确改进要求。"},
        {"target_type": "goal", "target_id": "G019",
         "message": "多站点迟到时告知司机，是受访者评价为有帮助但自述未必做过的做法；是否保留为软目标而非既有习惯？"},
        {"target_type": "goal", "target_id": "G021",
         "message": "使用当前位置时改上车点较难，依据的是有保留的记忆与绕行做法；是否需要向受访者确认具体版本与操作路径？"},
        {"target_type": "model", "target_id": "DOC026-goal-model",
         "message": "本次为单一样本访谈，个人偏好（如最便宜选项、单目的地）是否可视为产品层面的通用需求？"},
    ],
    "reassessments": [],
}

spec = {
    "document_id": "DOC026",
    "raw_candidates": raw,
    "goals": goals,
    "review_questions": review_questions,
    "limitations": limitations,
    "ledger": ledger,
    "decisions": decisions,
}

(A / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("ok", len(raw), len(goals), len(decisions["relations"]))
