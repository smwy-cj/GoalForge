# -*- coding: utf-8 -*-
"""Assemble spec.json from authored candidate/goal/relation decisions."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from quotes import Q, A  # noqa: E402

WIN = [w["window_id"] for w in json.loads((A / "authoring/wintmp/source-windows.json").read_text(encoding="utf-8"))["windows"]]

# (candidate_id, statement, actor, modality, context, origin, [quote keys], disposition, [final goal ids], note)
C = [
    ("C001", "Find a new place to live when moving to a new neighborhood or to a new country.", "House hunter", "need (explicit)", ["relocation to a new neighborhood or country"], "explicit", ["relocate"], "keep", ["G001"], "原句明确：搬家需要找新住处"),
    ("C002", "Search on the Internet and use house-hunting web apps to find the place.", "House hunter", "usually (habit)", ["relocation"], "explicit", ["relocate"], "merge", ["G001"], "网搜/web app 是 G001 的选定方式，并入同一目标"),
    ("C003", "Choose the neighborhood or place in which to look for a house before searching.", "House hunter", "usually (habit)", [], "explicit", ["choose_area"], "keep", ["G002"], "先选街区再按关键词搜索，独立动作"),
    ("C004", "Search by area keywords in order to find the relevant local listing websites.", "House hunter", "usually (habit)", ["target area may be in another country"], "explicit", ["keywords"], "merge", ["G003"], "关键词搜索是识别当地网站的手段"),
    ("C005", "Know which listing websites are the most popular or most used in that area.", "House hunter", "want (explicit)", ["especially another country"], "explicit", ["popular_sites"], "keep", ["G003"], "明确想了解当地最常用网站"),
    ("C006", "Find neighborhoods where listings that fit my budget and requirements are clustered.", "House hunter", "sometimes (one of many ways)", [], "explicit", ["clustered"], "keep", ["G004"], "按预算/条件聚集选街区，选址方式的具体化"),
    ("C007", "Ask people who live in that country for recommendations on places.", "House hunter", "one of many ways", ["target country"], "explicit", ["ask_locals"], "keep", ["G005"], "询问当地人是独立信息来源"),
    ("C008", "Pick a neighborhood close to my job or college when I have one.", "House hunter", "usually", ["specific job or college"], "explicit", ["near_job"], "keep", ["G006"], "靠近工作/学校的独立选法"),
    ("C009", "Search listings by size of the place or bedroom count, with a budget limit.", "House hunter", "will (stated practice)", [], "explicit", ["size_budget"], "keep", ["G007"], "面积/卧室数+预算的搜索条件"),
    ("C010", "Filter the many options down using less important criteria such as amenities or extra features.", "House hunter", "can (stated practice)", ["after the first search returns many options"], "explicit", ["secondary"], "keep", ["G008"], "次要条件二次筛选，独立动作"),
    ("C011", "Contact the people offering the shortlisted places.", "House hunter", "will (stated practice)", ["after filtering to several options"], "explicit", ["contact"], "keep", ["G009"], "联系房东；预期结果是缩小选项"),
    ("C012", "Use how fast providers reply and how complete their information is to narrow my choices.", "House hunter", "sometimes (criterion)", ["communication stage"], "explicit", ["reply_speed"], "merge", ["G009"], "回复速度/信息完整度是联系的判断结果"),
    ("C013", "Research the place by its name, Google Maps location, website, URL or phone number when I get no reply.", "House hunter", "might (reported practice)", ["provider does not respond through the app"], "explicit", ["research_name"], "merge", ["G010"], "查明名称/地图/网址是找替代联系渠道的前提"),
    ("C014", "Communicate with the provider through other methods such as email or phone.", "House hunter", "will (stated practice)", ["no reply through the app"], "explicit", ["other_methods"], "keep", ["G010"], "改用邮件/电话联系，核心动作"),
    ("C015", "Non-response means the management is not good.", "House hunter", "belief", ["provider does not reply"], "explicit", ["bad_sign"], "exclude", [], "对管理方的判断，不是期望结果"),
    ("C016", "Use the listing platforms only as a way to discover places.", "House hunter", "mainly (reported practice)", [], "explicit", ["discover_only"], "merge", ["G011"], "站内只用于发现房源，属同一约束的一半"),
    ("C017", "Proceed with a different type of communication outside these apps.", "House hunter", "usually (reported practice)", ["in-app messaging distrusted"], "explicit", ["outside_apps"], "keep", ["G011"], "明确平时在站外沟通"),
    ("C018", "Know when the listing information was last updated.", "House hunter", "complaint / missing information", [], "explicit", ["last_upd_complaint"], "keep", ["G012"], "明确想要最后更新时间"),
    ("C019", "Not be left with a long form whose submission outcome is unknown.", "House hunter", "dislike", [], "explicit", ["long_form"], "merge", ["G014"], "长表单且不知提交去向，属同一表单负担"),
    ("C020", "Be able to communicate in a short way instead of through a long form.", "House hunter", "want (explicit)", [], "explicit", ["short_comm"], "keep", ["G014"], "希望能简短沟通"),
    ("C021", "See a timeline of the next steps and what to expect if the request fails.", "House hunter", "want (explicit)", ["after sending a request"], "explicit", ["timeline"], "keep", ["G013"], "时间线与下一步预期"),
    ("C022", "Feel more trust and enthusiasm to go through the process.", "House hunter", "effect description", ["information visibility"], "explicit", ["trust_enthusiasm"], "exclude", [], "信任/热情是 G012/G013 的效果，无独立动作"),
    ("C023", "Not have to fill all form fields (first/last name, email, mobile, move end date, beds, baths, custom message).", "House hunter", "dislike (explicit)", ["all fields are required"], "explicit", ["required_fields"], "merge", ["G014"], "列举当前必填字段，是同一负担的具体内容"),
    ("C024", "Just communicate to know more or to get specific information without writing a custom message.", "House hunter", "sometimes (want)", [], "explicit", ["just_communicate"], "merge", ["G014"], "只想沟通了解信息，支撑最小信息联系"),
    ("C025", "Skip the website's request process and just take the information.", "House hunter", "observed behaviour", ["form feels overwhelming"], "explicit", ["skip_request"], "exclude", [], "描述自己跳过站内请求的行为，不是目标"),
    ("C026", "See the few matching units listed with their specifications and add the chosen one to a shortlist, e-commerce style.", "House hunter", "want (explicit)", ["only a few units match"], "explicit", ["three_units"], "keep", ["G016"], "列出规格+加入清单的明确愿望"),
    ("C027", "Know the expected response time and what happens next after choosing an option.", "House hunter", "want (explicit)", ["after proceeding with an option"], "explicit", ["what_next"], "merge", ["G013"], "预计回复时间属同一下一步可见性"),
    ("C028", "Have visibility and deterministic steps so that engaging in the process feels safe.", "House hunter", "want (explicit)", [], "explicit", ["deterministic"], "merge", ["G013"], "deterministic steps 即下一步可见性"),
    ("C029", "Share my information only after both parties confirm availability and interest.", "House hunter", "think (preference)", ["after confirmation"], "explicit", ["after_confirm", "not_before"], "keep", ["G015"], "确认后再提供信息"),
    ("C030", "Visit site, log in, use the search bar with filters, view details, then pick a path.", "House hunter", "process recap", [], "explicit", ["two_ways"], "exclude", [], "流程复述，无新意图；登录反对另由 C034/C042 承接"),
    ("C031", "Take the location from the map and find the provider through other websites such as Google Maps.", "House hunter", "alternative path", [], "explicit", ["map_route"], "merge", ["G010"], "站外联系路径的复述"),
    ("C032", "Draw a circle on the map and search inside that area.", "House hunter", "like (explicit)", ["neighborhood name too narrow"], "explicit", ["draw_tool"], "keep", ["G019"], "画圈选区，明确喜欢的功能"),
    ("C033", "See reviews from people so that places feel more trusted.", "House hunter", "like (explicit)", [], "explicit", ["reviews"], "keep", ["G020"], "评论带来信任"),
    ("C034", "Not be required to register in the website to use it.", "House hunter", "dislike (explicit)", [], "explicit", ["register_research"], "keep", ["G022"], "反对为使用网站而注册"),
    ("C035", "Avoid multiple unknown buttons whose outcome I cannot tell.", "House hunter", "dislike (explicit)", [], "explicit", ["unknown_buttons"], "keep", ["G021"], "未知按钮导致跳过网站"),
    ("C036", "Find where the favourites button saves things.", "House hunter", "complaint (missing feedback)", [], "explicit", ["favorites_lost"], "keep", ["G018"], "找不到收藏位置"),
    ("C037", "Avoid the Request-a-tour form that must be filled for a viewing.", "House hunter", "dislike", ["interested in a property"], "explicit", ["tour_form"], "merge", ["G014"], "看房请求也走同一长表单"),
    ("C038", "Not be required to register just to do research.", "House hunter", "dislike (explicit)", [], "explicit", ["register_research"], "merge", ["G022"], "仅为搜索就要注册"),
    ("C039", "Collect three or four liked options on a single page to compare their main features.", "House hunter", "wish (explicit)", ["3-4 liked options"], "explicit", ["compare_page"], "keep", ["G017"], "希望一页对比 3-4 个选项"),
    ("C040", "Know where the favourites button stores the saved items.", "House hunter", "complaint", [], "explicit", ["fav_weird"], "merge", ["G018"], "收藏存到哪里不清楚，同一问题"),
    ("C041", "Have the saved options on the nav bar or the first level of the menu.", "House hunter", "should (expectation)", [], "explicit", ["nav_bar"], "merge", ["G018"], "指定收藏应在导航/一级菜单"),
    ("C042", "Have registration/login be optional rather than required.", "House hunter", "should not be required", ["no account needed to communicate"], "explicit", ["optional_register"], "merge", ["G022"], "注册应为可选"),
    ("C043", "Start searching and see the whole functionality directly.", "House hunter", "preference", ["instead of logging in"], "explicit", ["start_search"], "merge", ["G022"], "直接开始搜索即免登录"),
    ("C044", "Search the information I want without steps I do not believe are beneficial.", "House hunter", "preference", [], "explicit", ["no_steps"], "merge", ["G022"], "省去无益步骤=免登录的便利"),
    ("C045", "Filter by price range, beds and baths, home type, move-in date, pets or utilities.", "House hunter", "can (beneficial)", [], "explicit", ["filter_main", "filter_extra"], "keep", ["G023"], "列出可用筛选维度"),
    ("C046", "Use the drawing functionality after specifying the location.", "House hunter", "can (stated practice)", [], "explicit", ["draw_tool"], "merge", ["G019"], "地图画圈功能再次提及"),
    ("C047", "Keep the filters optional, without forcing every field to be filled.", "House hunter", "like (explicit)", [], "explicit", ["filter_optional"], "merge", ["G023"], "筛选可选是同一要求"),
    ("C048", "Also see listings whose owner did not specify an attribute when I filter by it.", "House hunter", "fear + wish", ["filter applied"], "explicit", ["lose_options", "include_unspecified"], "keep", ["G024"], "担心过滤掉未标注的房源"),
    ("C049", "Have the option to see only the listings that already confirmed the attribute.", "House hunter", "option (explicit)", ["filter applied"], "explicit", ["include_unspecified"], "merge", ["G024"], "只看已确认，是同一开关的另一状态"),
    ("C050", "Have a checkbox to include the options that did not determine the attribute.", "House hunter", "suggestion (maybe)", ["pet policy dropdown"], "explicit", ["checkbox"], "merge", ["G024"], "复选框机制"),
    ("C051", "When the checkbox is on see both allowed and unspecified, when off see only specified.", "House hunter", "behaviour of the proposed control", [], "explicit", ["both_states"], "merge", ["G024"], "复选框两态行为"),
    ("C052", "Get an overview of the price ranges and available options in a new country.", "House hunter", "want (explicit)", ["moving to another country"], "explicit", ["overview", "overview2"], "keep", ["G025"], "了解价格区间与可选房源"),
    ("C053", "Have the site require owners to photograph listings in a standard format (sunlight, specific angles).", "House hunter", "suggestion (maybe)", ["for more trust"], "explicit", ["photo_rules"], "keep", ["G026"], "照片格式规则的建议"),
    ("C054", "See when the information was last updated.", "House hunter", "would really love", [], "explicit", ["last_upd_wish"], "merge", ["G012"], "再次要求最后更新时间"),
    ("C055", "Details page is sufficient apart from the last-updated information.", "House hunter", "assessment", [], "explicit", ["sufficient_except"], "merge", ["G012"], "细节页仅缺更新时间"),
    ("C056", "Be assured that the listing information is up to date.", "House hunter", "want (explicit)", [], "explicit", ["up_to_date"], "merge", ["G012"], "希望确认信息是最新的"),
    ("C057", "Have a feature that helps me compare several options.", "House hunter", "wish (explicit)", [], "explicit", ["compare_wish"], "merge", ["G017"], "再次提出对比功能"),
    ("C058", "Communicate with the property owners through these websites when the process is clear and fast.", "House hunter", "conditional wish", ["process clear and fast"], "explicit", ["clear_fast"], "keep", ["G027"], "条件性希望在站内与房东沟通"),
    ("C059", "Have all the housing communication in a single place.", "House hunter", "would be great", ["process clear and fast"], "explicit", ["single_place"], "merge", ["G027"], "所有沟通集中在一处"),
    ("C060", "Decide on a home within a week or at most a month.", "House hunter", "sometimes (time window)", [], "explicit", ["week_window"], "exclude", [], "决策时间窗是背景约束，已写入 G027 条件"),
    ("C061", "Give the user insight into how the communication process will proceed.", "House hunter", "suggestion (maybe)", ["UI change"], "explicit", ["ui_insight"], "merge", ["G013"], "让用户了解沟通流程=下一步可见性"),
    ("C062", "Trust the feature more and never try something else.", "House hunter", "effect description", ["process transparency"], "explicit", ["stay_inside"], "exclude", [], "信任后不换渠道是效果描述"),
    ("C063", "Keep the communication on the website instead of moving to another channel.", "House hunter", "effect + wish", ["process transparency"], "explicit", ["stay_inside"], "merge", ["G027"], "把沟通留在网站内"),
]

raw_candidates = []
entries = []
for cid, stmt, actor, modality, ctx, origin, keys, disp, gids, note in C:
    raw_candidates.append({
        "candidate_id": cid, "statement": stmt, "actor": actor, "modality": modality,
        "context": ctx, "origin": origin, "pass_id": "P1",
        "evidence": [Q[k] for k in keys]})
    entries.append({"candidate_id": cid, "disposition": disp, "final_goal_ids": gids, "reason": note})

# (goal_id, statement, context, origin, [quote keys], label, rationale, inference)
G = [
    ("G001", "Find a new place to live when moving to a new neighborhood or country, by searching on the internet with house-hunting web apps.",
     ["moving to a new neighborhood or a new country"], "explicit", ["relocate"], "direct",
     "原句明确以搬家为由需要找新住处，并说明用网络与 web app 的方式；主体、情境、目的与选定方式一致，强度为通常做法。", None),
    ("G002", "Choose the neighborhood or area to search in before starting a house search.",
     [], "explicit", ["choose_area"], "direct",
     "原句先选街区/地点再按关键词搜索，动作与先后顺序明确，未附加例外或强度弱化。", None),
    ("G003", "Identify the listing websites that are most popular or most used in the target area, especially when the area is in another country.",
     ["especially when the target area is in another country"], "explicit", ["popular_sites", "keywords"], "direct",
     "原句明确想了解当地最常用网站，并说明关键词搜索是达成手段；popular/most used 为原话强度，未夸大。", None),
    ("G004", "Find neighborhoods where listings that fit my budget and requirements are clustered.",
     [], "explicit", ["clustered"], "direct",
     "原句把“预算与要求相符的房源聚集在某街区”作为选街区的一种方式；主体、对象与条件一致。", None),
    ("G005", "Get recommendations on places from people who live in the target country.",
     ["the target country is not where I live"], "explicit", ["ask_locals"], "direct",
     "原句把询问当地居住者的推荐作为选街区方式之一，意图明确；未声称对方必然给建议。", None),
    ("G006", "Pick a neighborhood close to my job or college when I have one.",
     ["when I have a specific job or study at a specific college"], "explicit", ["near_job"], "direct",
     "原句以“如果有特定工作或就读学校”为条件，说明通常会选靠近该区域的街区；保留 usually 的可让步强度。", None),
    ("G007", "Search listings by size or bedroom count within a budget limit.",
     [], "explicit", ["size_budget"], "direct",
     "原句明确按面积/卧室数并带预算上限搜索；条件与方式一致，未附加阈值。", None),
    ("G008", "Filter the retrieved options down by secondary criteria such as amenities, extra features, or how good the place looks.",
     ["after the first search returns many options"], "explicit", ["secondary"], "direct",
     "原句在得到许多选项后用 amenities、额外特征、外观等“不太重要”的条件继续筛选；动作独立且有依据。", None),
    ("G009", "Contact the providers of the shortlisted places and narrow the options by how fast and how completely they respond.",
     ["after filtering down to several options"], "explicit", ["contact", "reply_speed"], "direct",
     "原句明确筛选后进入沟通，并以回复速度、信息完整度影响选择；联系为核心动作，缩小选项为预期结果。", None),
    ("G010", "Reach a provider who does not answer through the app by finding the place's name, location or website and contacting them by email or phone.",
     ["the provider does not respond through the app"], "explicit", ["research_name", "other_methods"], "direct",
     "受访者明确在站内无回应时改用邮件/电话，并说明先查明名称、地图位置或网址；触发条件（无回应）保留。", None),
    ("G011", "Keep the conversation with providers outside the listing apps, using the apps only to discover places.",
     ["based on reported practice and distrust of in-app messaging"], "explicit", ["outside_apps", "discover_only"], "direct",
     "原句直接陈述其稳定做法（平台只用于发现房源、沟通都在站外）并说明不信任站内沟通；目标按维持现状表述，未扩大为“永不使用站内沟通”，若读作纯过去行为则应降为 insufficient。",
     None),
    ("G012", "See when the listing information was last updated.",
     [], "explicit", ["last_upd_wish", "last_upd_complaint"], "direct",
     "多处原句明确提出想看最后更新时间，并说明用于判断信息是否过期；强度为强烈愿望（would really love），未编造精度要求。", None),
    ("G013", "See a timeline of the next steps and what to expect after sending a request, including what happens if it fails.",
     ["after a request is sent"], "explicit", ["timeline", "what_next"], "direct",
     "原句要求看到下一步时间线以及失败时会怎样，另一处要求知道对方何时回复、接下来是什么；条件与内容一致。", None),
    ("G014", "Contact a provider with minimal information instead of filling a long form in which every field is required.",
     ["current form requires first name, last name, email, mobile, move end date, beds, baths and a custom message"], "explicit", ["just_communicate", "required_fields"], "direct",
     "原句说明所有字段必填、只想简短沟通不想写自定义消息，并因此跳过站内请求；期望是低信息量即可联系，未扩展到其他渠道。", None),
    ("G015", "Share my personal information only after both sides have confirmed availability and interest.",
     ["before confirmation it is not necessary to give all the information"], "explicit", ["after_confirm", "not_before"], "direct",
     "原句明确信息可在双方确认可租且本人有意愿之后再提供，并称此前无必要提供全部信息；条件与主体一致。", None),
    ("G016", "See the few matching units listed with their specifications and add the chosen one to a shortlist, e-commerce style.",
     ["when only a few units match the specifications"], "explicit", ["three_units"], "direct",
     "原句以“若有三套符合规格的房源”为例，要求列出规格并提供类似加入购物车的操作；示例情境保留为条件，未固化数量。", None),
    ("G017", "Compare three or four shortlisted options on a single page by their main features.",
     ["three or four options I like"], "explicit", ["compare_page", "compare_wish"], "direct",
     "原句明确想收藏 3-4 个选项并在同一页面同时看主要特征，另一处再次提出对比功能；数量与对象一致。", None),
    ("G018", "Find my saved options from the nav bar or the first level of the menu.",
     [], "explicit", ["nav_bar", "favorites_lost"], "direct",
     "原句明确收藏入口应在导航栏或菜单第一层，并说明现在找不到收藏位置；位置要求为原话，未自行指定具体控件。", None),
    ("G019", "Search inside an area drawn on the map instead of only by neighborhood name.",
     ["when searching by neighborhood name is too narrow"], "explicit", ["draw_tool", "draw_flex"], "direct",
     "原句明确喜欢地图画圈选区，并说明比按街区名搜索更灵活；属对已提供功能的偏好性要求，理由为原文。", None),
    ("G020", "See reviews from people who lived in the place so that listings feel more trusted.",
     [], "explicit", ["reviews"], "direct",
     "原句明确喜欢评论功能，并说明评论让房源更可信、信息更集中；因果关系为受访者自述。", None),
    ("G021", "Avoid extra unknown buttons and steps whose outcome I cannot tell when searching on a site.",
     [], "explicit", ["unknown_buttons", "skip_site"], "direct",
     "原句明确不喜欢不知道会导向何处的按钮与冗长未知流程，并因此离开网站；属避免型意图，未扩大到所有按钮。", None),
    ("G022", "Search and use the full functionality without registering, with an account optional.",
     [], "explicit", ["optional_register", "start_search"], "direct",
     "原句明确注册/登录应为可选而非必需，并希望直接开始搜索看到全部功能；强度为 should not be required。", None),
    ("G023", "Filter listings by price range, beds and baths, home type, move-in date, pets or utilities, without being forced to fill every filter.",
     ["filters stay optional"], "explicit", ["filter_main", "filter_extra", "filter_optional"], "direct",
     "原句列举价格、卧室/卫浴、房型、入住日期、宠物、水电等筛选，并明确喜欢筛选可选、不强制填满；维度与强度保留。", None),
    ("G024", "Also see, when a filter is applied, the listings whose owner did not specify that attribute.",
     ["a filter on an attribute such as pet policy is applied"], "explicit", ["include_unspecified", "checkbox"], "direct",
     "原句明确希望有选项把未标注该属性的房源一并纳入，并可选择只看已确认；担心漏掉合适房源为依据。", None),
    ("G025", "Get an overview of the price ranges and available options in an area I do not know yet.",
     ["moving to another country"], "explicit", ["overview", "overview2"], "direct",
     "原句说明需要知道有哪些选项与价格区间，并称网站聚合信息能给出概览；目的明确，未编造指标精度。", None),
    ("G026", "Have the site require owners to photograph listings in a standard format (sunlight, specific angles) so that pictures are more trustworthy.",
     ["stated as a suggestion (maybe), not a firm requirement"], "explicit", ["photo_rules"], "direct",
     "原句以 maybe 提出网站应规定照片格式（光线、角度）以增加信任；保留建议强度，未升级为强制要求。", None),
    ("G027", "Keep all housing communication on the listing platform when the process is clear and fast.",
     ["only if the process is clear and fast", "decision window is about a week, at most a month"], "explicit", ["single_place", "clear_fast"], "direct",
     "原句以“流程清晰且快速”为条件，表示愿意在站内与房东沟通并把全部沟通集中在一处；条件保留，未去掉条件。", None),
]

goals = []
for gid, stmt, ctx, origin, keys, label, rationale, inference in G:
    goals.append({
        "candidate_id": gid, "statement": stmt, "actor": "House hunter", "context": ctx,
        "origin": origin, "inference": inference,
        "evidence": [Q[k] for k in keys],
        "judgment": {"label": label, "rationale": rationale, "supported_parts": [],
                     "unsupported_parts": [], "assumptions": [], "reasoning_steps": []}})

# relations
R = [
    ("R1", "G006", "G002", "specialization", "supported",
     ["原文把“靠近工作或学校”作为选街区的一种具体情境"],
     ["受访者的工作/学校位置在搜索时已知"],
     "G006 是 G002 在“已有明确工作或就读地点”情境下的具体化，方向为具体→一般。",
     ["near_job"]),
    ("R2", "G004", "G002", "specialization", "supported",
     ["“按预算与要求聚集”的街区是选街区的一种具体判据"],
     ["房源列表能反映街区层面的分布"],
     "G004 给出选择街区的一种具体判据（预算与要求相符的房源聚集），属于 G002 的具体情境。",
     ["clustered"]),
    ("R3", "G005", "G002", "specialization", "supported",
     ["询问当地人是选街区的具体做法，适用于跨国搬家"],
     ["可获得当地居住者的推荐"],
     "G005 是 G002 在“目标国家有熟人/当地人可问”情境下的具体化。",
     ["ask_locals"]),
    ("R4", "G009", "G010", "precedes", "supported",
     ["站内联系后未获回复才转站外"],
     ["站内消息渠道确实无回应"],
     "先发生的是站内联系（G009），无回应之后才改用邮件/电话（G010），顺序由问答直接给出；顺序不等于因果。",
     ["no_response_q", "other_methods"]),
    ("R5", "G019", "G002", "operationalization", "supported",
     ["画圈选区用于在地图上界定要搜索的区域"],
     ["地图数据能支持区域内检索"],
     "G019 是确定搜索区域的一种实现方式，服务于 G002 的选区目的；原文说明它比按街区名更灵活。",
     ["draw_flex"]),
    ("R6", "G013", "G027", "contribution", "supported",
     ["用户先看到下一步与预计回复，才愿意留在站内沟通"],
     ["时间线信息与实际流程一致"],
     "G013 提供沟通流程的可见性，直接支持留在站内完成沟通（G027）；原文称这会让用户更信任该功能、不再另找渠道。",
     ["stay_inside", "ui_insight"]),
    ("R7", "G014", "G027", "contribution", "supported",
     ["表单过重与流程不明会把人推向站外"],
     ["平台确实能承载轻量沟通"],
     "G014 降低联系门槛，削弱“流程不清→转站外”的动因，因而有助于 G027；方向为帮助项→受助项。",
     ["vague_button"]),
    ("R8", "G024", "G023", "contribution", "supported",
     ["按属性筛选会漏掉未标注的房源"],
     ["未标注不等于不具备该属性"],
     "G024 让筛选结果不因信息缺失而漏项，提升筛选（G023）的可用性；属帮助关系，不构成充分实现。",
     ["lose_options"]),
    ("R9", "G023", "G025", "contribution", "supported",
     ["筛选与聚合共同给出价格区间与选项概览"],
     ["房源数量足以形成区间感知"],
     "筛选条件帮助把大量房源收敛成可比较的价格区间与选项概览（G025）；原文把 filters 与网站聚合并列为概览来源。",
     ["overview2"]),
]

relations = []
for rid, src, tgt, typ, status, cond, assum, why, keys in R:
    relations.append({"relation_id": rid, "source_id": src, "target_id": tgt, "type": typ,
                      "status": status, "conditions": cond, "assumptions": assum,
                      "rationale": why, "evidence_ids": [],
                      "evidence_quotes": [Q[k] for k in keys]})

groups = [{
    "group_id": "GR1", "parent_id": "G027", "child_ids": ["G013", "G014"], "kind": "and",
    "status": "proposed", "completeness": "partial",
    "rationale": "G013（下一步时间线）与 G014（最小信息联系）分别对应原文对“流程不清”和“表单过重”的抱怨，两者共同解释了为何愿意把沟通留在站内；但房东是否在平台回复不受这两项控制，故只作为待确认的部分精化。",
    "assumptions": ["房东愿意在平台内回复", "时间线信息与实际处理流程一致", "两项同时具备时用户才不再转站外"],
    "evidence_ids": [], "relation_ids": ["R6", "R7"],
    "evidence_quotes": [Q["single_place"], Q["stay_inside"]],
    "checks": [
        {"kind": "normal", "origin": "analysis_assumption",
         "scenario": "用户提交站内请求时能看到下一步时间线与预计回复，且只需少量信息即可发起；房东在平台内正常回复。",
         "outcome": "supports",
         "rationale": "该场景同时消除原文抱怨的信息不透明与表单过重，用户没有明显理由再转到站外渠道。"},
        {"kind": "exception", "origin": "analysis_assumption",
         "scenario": "房东并不活跃于平台、不回复站内消息（原文 T017 称有人只发布信息、不持续使用网站）。",
         "outcome": "counterexample",
         "rationale": "即使界面透明、表单轻量，房东不回复时沟通仍会转到站外，说明该组不足以单独满足父目标 G027，故保留 proposed/partial。"},
    ]}]

questions = [
    {"target_type": "model", "target_id": "DOC021-goal-model",
     "message": "精化组判断（已执行）：G004、G005、G006 被原文描述为选街区的多种方式（“there are many ways”），属 OR 替代而非共同满足，因此未建 AND 组；是否需要以多个 OR 方案表达，请确认。"},
    {"target_type": "model", "target_id": "DOC021-goal-model",
     "message": "精化组判断（已执行）：曾评估以 G002（选址）、G007（按面积/预算搜索）、G008（次要条件筛选）共同满足 G001，但组内缺少联系房东与核验真实性，无法声称共同充分，故未建组。"},
    {"target_type": "model", "target_id": "DOC021-goal-model",
     "message": "GR1 的异常场景（房东不活跃、不在平台回复）未解决：该组至多改善站内沟通体验，不能保证沟通留在平台；请确认是否接受 partial 结论。"},
    {"target_type": "model", "target_id": "DOC021-goal-model",
     "message": "G011（现状：站外沟通）与 G027（条件性：站内单平台沟通）适用条件不同，未判为冲突；若流程变清晰后是否放弃站外渠道，原文未说明。"},
]

review_questions = [
    {"candidate_ids": ["G011"], "question": "“继续在站外沟通”是由现状与不信任推断的维持意图，是否应作为稳定偏好保留？",
     "reason": "原文陈述的是平常做法，未直接说“以后也要这样”。"},
    {"candidate_ids": ["G026"], "question": "照片格式规则只是以 maybe 提出的建议，是否应作为对平台的要求保留？",
     "reason": "语气为建议而非要求，强度已保留在 context 中。"},
    {"candidate_ids": ["G027"], "question": "“流程清晰且快速”没有可核对的时限或状态标准，是否需要补充定义？",
     "reason": "原文只给出条件性表述，未给阈值，不能自行编造。"},
]

checks = [
    ("S1", ["relocate"], ["C001", "C002"], ["G001"], "represented", "搬家找房的原句；网搜作为选定方式并入同一目标。"),
    ("S2", ["keywords", "popular_sites"], ["C004", "C005"], ["G003"], "represented", "关键词搜索与了解当地常用网站两处并读，确认为同一目的与手段。"),
    ("S3", ["clustered", "ask_locals", "near_job"], ["C006", "C007", "C008"], ["G004", "G005", "G006"], "represented", "选街区的三种方式分别建目标，未合并为单一目标。"),
    ("S4", ["no_response_q", "other_methods", "bad_sign"], ["C013", "C014", "C015"], ["G010"], "represented", "无回应后的替代联系保留；对管理方的判断（C015）排除。"),
    ("S5", ["discover_only", "outside_apps"], ["C016", "C017"], ["G011"], "represented", "站内只发现、沟通在站外的现状，推断为维持意图。"),
    ("S6", ["long_form", "required_fields", "skip_request"], ["C019", "C023", "C025"], ["G014"], "represented", "表单负担并入 G014；由此产生的跳过行为（C025）不作为目标。"),
    ("S7", ["unknown_buttons", "skip_site"], ["C035"], ["G021"], "represented", "未知按钮与跳过网站的因果，保留为避免型目标。"),
    ("S8", ["lose_options", "include_unspecified", "both_states"], ["C048", "C049", "C051"], ["G024"], "represented", "担心漏项与复选框两态，合并为一个筛选补充目标。"),
    ("S9", ["two_ways"], ["C030"], [], "excluded", "流程复述无新意图，登录与表单问题已分别由 C034/C023 承接。"),
    ("S10", ["trust_enthusiasm"], ["C022"], [], "excluded", "信任与热情是可见性目标的效果描述，不另立目标。"),
    ("S11", ["week_window"], ["C060"], [], "excluded", "决策时间窗作为 G027 的背景条件，不单独成目标。"),
    ("S12", ["stay_inside"], ["C062"], [], "excluded", "“不再换渠道”是效果描述，相关期望已由 G013/G027 承接。"),
]

source_checks = []
for cid, keys, cands, gids, outcome, reason in checks:
    source_checks.append({"check_id": cid, "evidence_candidates": [Q[k] for k in keys],
                          "candidate_ids": cands, "final_goal_ids": gids,
                          "outcome": outcome, "reason": reason})

passes = [
    {"pass_id": "P1", "kind": "initial", "context": "isolated", "status": "completed",
     "window_results": [{"window_id": w, "status": "processed", "reason": ""} for w in WIN]},
    {"pass_id": "P2", "kind": "full_context", "context": "isolated", "status": "completed",
     "window_results": [{"window_id": w, "status": "processed", "reason": ""} for w in WIN]},
]

spec = {
    "document_id": "DOC021",
    "raw_candidates": raw_candidates,
    "goals": goals,
    "review_questions": review_questions,
    "limitations": [
        "原文为英文访谈转写，含口语重复、自我更正与数字写法（如 1st）；引文按转写原样保留。",
        "受访者未回答或未展开的问题（如平台改后的接受度、房东侧行为）未作补全。",
    ],
    "ledger": {
        "model": "unknown", "temperature": "unknown",
        "budget": "1 initial pass + 1 full-context pass + <=2 repair rounds",
        "usage": "unknown",
        "skill_revision": "a5952d426b1624a3fcb2ce2829e1ae1ceb15e19dc3309d9571f3bc6b465deb6f",
        "prompt_revision": "task-prompt-v1",
        "planned_passes": 2,
        "stop_reason": "完成一次逐窗捕获与一次全篇校正；补查未再产生有据的新意图，保留未决问题后停止。",
        "passes": passes,
        "full_context_review": {
            "status": "completed",
            "reason": "回查全部 77 轮：校正指代（the other ways 指选街区方式）、条件继承（T027 的 before that step）、例外（未标注属性的房源、房东不活跃）与相反证据（T017 站外沟通 vs T071 条件性站内单平台）；窗口仅作定位，语义以整段问答裁决。"},
        "entries": entries,
        "source_checks": source_checks,
    },
    "decisions": {"relations": relations, "groups": groups, "questions": questions, "reassessments": []},
}

(A / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
print("goals", len(goals), "candidates", len(raw_candidates), "relations", len(relations), "groups", len(groups))
print("entries", len(entries), "windows", len(WIN))
