import json
from build_spec_part1 import raw, goals, ev

ENTRIES = [
    ("C001", "keep", ["G001"], "直接陈述的主要用途，保留为支付需求目标。"),
    ("C002", "keep", ["G003"], "习惯性支票转储蓄以赚利息，保留为账户间转账目标。"),
    ("C003", "exclude", [], "仅描述 Apple Pay 线下使用现状，未对网页端提出改进或维持诉求。"),
    ("C004", "merge", ["G001"], "与 C001 同一支付方式，补充即时、小额、按手机号的特征，并入 G001。"),
    ("C005", "exclude", [], "对访谈任务的应允，属任务执行而非产品目标。"),
    ("C006", "keep", ["G004"], "同屏概览账户、余额、存取与近期交易，整理为单一仪表盘目标。"),
    ("C007", "exclude", [], "整体观感与布局评价，无可独立满足的结果或改动诉求。"),
    ("C008", "exclude", [], "总体满意表述，后续仍指出具体缺口，不构成新增目标。"),
    ("C009", "keep", ["G005"], "设定货币目标并跟踪进度，保留为 plan and track 目标。"),
    ("C010", "keep", ["G011"], "新设备首登两步验证，保留为安全维持目标。"),
    ("C011", "keep", ["G012"], "交易通知与申诉，保留为交易提醒闭环目标。"),
    ("C012", "exclude", [], "总体安全感受，具体机制已由 C010、C011 承接。"),
    ("C013", "keep", ["G006"], "明确希望看到支出分类明细，保留为分类目标。"),
    ("C014", "merge", ["G005"], "与 C009 同一功能的更详细描述，并入 G005。"),
    ("C015", "merge", ["G006"], "对分类缺口的现场核实，并入 G006 作为缺口依据。"),
    ("C016", "merge", ["G004"], "交易列表字段说明，并入 G004 的同屏概览。"),
    ("C017", "merge", ["G007"], "App 内可设卡片参数与每日上限，并入 G007 作为能力与渠道依据。"),
    ("C018", "exclude", [], "范围为采访者设定，涉众仅确认 App 内可设置参数，未自述为网页端目标。"),
    ("C019", "exclude", [], "采访者设定的百元限额任务，涉众仅同意执行；能力诉求见 C023。"),
    ("C020", "merge", ["G007"], "网页端找不到限额入口的观察，并入 G007 的缺口依据。"),
    ("C021", "keep", ["G008"], "卡片控制不直观、希望改进，保留为可达性目标。"),
    ("C022", "merge", ["G007"], "确认无修改限额选项，并入 G007。"),
    ("C023", "merge", ["G007"], "明确希望拥有该功能并抱怨缺失，并入 G007。"),
    ("C024", "exclude", [], "说明储蓄资金未绑定借记卡，属使用条件，不作为目标；已记入 G007 的 context。"),
    ("C025", "keep", ["G002"], "网页端无 Zelle 的缺口观察，保留为网页端 Zelle 目标依据。"),
    ("C026", "merge", ["G003"], "转账入口易达的正面评价，并入 G003。"),
    ("C027", "keep", ["G010"], "排程转账的日期、备注与重复设置，整理为排程目标。"),
    ("C028", "keep", ["G009"], "提交前确认步骤，保留为防错确认目标。"),
    ("C029", "merge", ["G003"], "实际执行的转账，并入 G003。"),
    ("C030", "merge", ["G002"], "希望网页端实现 Zelle 并给出便利理由，并入 G002。"),
    ("C031", "merge", ["G003"], "网页账户转账“super intuitive”的评价，并入 G003。"),
    ("C032", "merge", ["G009"], "确认步骤避免金额或对象出错，并入 G009。"),
    ("C033", "merge", ["G010"], "可排程与重复以免反复录入，并入 G010。"),
    ("C034", "keep", ["G013"], "网页端无文字聊天的缺口，保留为人工聊天目标依据。"),
    ("C035", "exclude", [], "仅记录帮助入口位置的观察，未提出入口位置诉求，后续诉求集中在聊天渠道。"),
    ("C036", "merge", ["G013"], "偏好聊天式支持及其理由，并入 G013。"),
    ("C037", "keep", ["G014"], "面向不熟悉网站用户的 AI 机器人对话，保留为独立目标。"),
    ("C038", "exclude", [], "对厂商限制的猜测，属信念背景，不构成目标或已证障碍。"),
    ("C039", "split", ["G003", "G004"], "同时涉及日常转账与查看交易两项结果，分别并入 G003 与 G004。"),
    ("C040", "keep", ["G008"], "锁卡需 7-8 次点击、重要功能应更易达，保留为可达性目标。"),
    ("C041", "keep", ["G015"], "一对一投资顾问的正面评价，保留为维持目标。"),
    ("C042", "exclude", [], "描述现有投资开户与交易功能，正面评价集中在顾问支持，不另立目标。"),
]

SOURCE_CHECKS = [
    ("S1", [("DOC004:T005", "the main reason I use the app is to do sell payments to like a few of my friends. Basically split split costs and all of that.")],
     ["C001"], ["G001"], "represented", "主要用途直接支持 Zelle 支付需求。"),
    ("S2", [("DOC004:T005", "so I normally transfer it over to my savings, so I can get even that little bit of interest I normally get.")],
     ["C002"], ["G003"], "represented", "习惯转账与赚息目的均保留在 G003。"),
    ("S3", [("DOC004:T015", "So it's a good thing that I can like. Just look at all of my spends on like in like a quick glance, and don't really have to go to like multiple screens to check all of that")],
     ["C006"], ["G004"], "represented", "一屏查看与免切屏的要求保留在 G004。"),
    ("S4", [("DOC004:T017", "Honestly. It's perfect the way it is.")],
     ["C008"], [], "excluded", "总体满意与后续具体缺口并存，按总体评价排除而非当目标。"),
    ("S5", [("DOC004:T019", "because, like every time I do a transaction. I get a notification on my phone saying that this much amount of money has been spent, and then I can also contest it, which is great.")],
     ["C011"], ["G012"], "represented", "通知与申诉作为同一闭环保留在 G012。"),
    ("S6", [("DOC004:T021", "But apart from that, I don't really think it gives me like a breakdown of how much I'm spending and where. So I I think that it would be great to see something like that.")],
     ["C013"], ["G006"], "represented", "分类支出诉求保留在 G006。"),
    ("S7", [("DOC004:T028", "Let's try and restrict your online spend limit to. let's say, a hundred dollars per transaction.")],
     ["C019"], [], "excluded", "采访者设定的任务，未成为涉众自述目标；限额诉求另由 T037 承接。"),
    ("S8", [("DOC004:T037", "So I would like to see that feature, and it's honestly upset that they haven't added it to this, considering it's such a huge bank.")],
     ["C023"], ["G007"], "represented", "明确的限额功能诉求保留在 G007。"),
    ("S9", [("DOC004:T041", "I don't think Zelle is I don't think we can sell on of the web app.")],
     ["C025"], ["G002"], "represented", "网页端无 Zelle 的缺口支持 G002。"),
    ("S10", [("DOC004:T045", "and then it lets you schedule properly. It also lets you repeat the transactions is a great, so you don't have to come and keep on doing it again and again.")],
     ["C033"], ["G010"], "represented", "排程与重复合并为一个排程目标，附加好处保留在 statement。"),
    ("S11", [("DOC004:T053", "I I don't even see anything on the footers for help. So that's interesting.")],
     ["C035"], [], "excluded", "仅记录发现路径，未提出入口位置诉求；相关诉求由 G013 承接。"),
    ("S12", [("DOC004:T055", "But for, let's say, people who who don't exactly know how to get around the website. It'd be great to just like text the AI bot. And then, like, get responses and all of that.")],
     ["C037"], ["G014"], "represented", "AI 机器人对话诉求保留为独立目标。"),
    ("S13", [("DOC004:T059", "I had to click. I I think I had to click like 7 or 8 times to even get to locking or unlocking my debit card, which is. which is honestly kind of bad design.")],
     ["C040"], ["G008"], "represented", "点击数问题与可达性诉求保留在 G008。"),
    ("S14", [("DOC004:T061", "you can have a 1 to one with an advisor which is a really good features. Be really good feature, because if you're not, if you don't know where to start investing, you can like talk to someone.")],
     ["C041"], ["G015"], "represented", "顾问支持的正面评价保留为维持目标。"),
]

all_windows = ["DOC004:W%04d" % i for i in range(1, 34)]

ledger = {
    "model": "unknown",
    "temperature": "unknown",
    "budget": "1 initial pass + <=2 repair rounds",
    "usage": "unknown",
    "skill_revision": "a5952d426b1624a3fcb2ce2829e1ae1ceb15e19dc3309d9571f3bc6b465deb6f",
    "prompt_revision": "task-prompt-v1",
    "planned_passes": 1,
    "stop_reason": "完成 67 轮全文逐窗捕获与全篇校正，剩余不确定项（目标归组、替代渠道）已转为问题，无新证据可继续推进。",
    "passes": [{"pass_id": "P1", "kind": "initial", "context": "isolated", "status": "completed",
                "window_results": [{"window_id": w, "status": "processed", "reason": ""} for w in all_windows]}],
    "full_context_review": {
        "status": "completed",
        "reason": "回查全部 67 轮：校正指代（cell/sell 指 Zelle；that feature 指卡片限额；they/their 指银行）；核对问答范围（T024 与 T028 为采访者设定，不计为涉众自述目标）；核对条件继承（T037 储蓄资金未绑定借记卡的限定记入 G007）；处理相反证据（T017“perfect the way it is”与后续具体缺口按总体评价与分项缺口分别处置）；核对 T042-T043 任务执行与 T045 复述，避免对同一愿望重复建点。"},
    "entries": [{"candidate_id": c, "disposition": d, "final_goal_ids": g, "reason": r} for c, d, g, r in ENTRIES],
    "source_checks": [{"check_id": s, "evidence_candidates": [{"source_id": sid, "quote": q} for sid, q in eqs],
                       "candidate_ids": cs, "final_goal_ids": gs, "outcome": o, "reason": r}
                      for s, eqs, cs, gs, o, r in SOURCE_CHECKS],
}

decisions = {
    "relations": [{
        "relation_id": "R1", "source_id": "G002", "target_id": "G001",
        "type": "operationalization", "status": "supported",
        "conditions": [], "assumptions": [],
        "rationale": "网页端提供 Zelle 是继续以手机号做小额即时转账的一种实现渠道，服务于既有的分摊费用用途；该渠道让用户不必取用手机，但不宣称它是唯一或充分方式。",
        "evidence_ids": [],
        "evidence_quotes": [ev("DOC004:T045", "I would like to see them implement Zelle on on the web app because I think it. It'll just be more convenient, so that I don't have to like reach. Reach my phone every time.")],
    }],
    "groups": [],
    "questions": [
        {"target_type": "goal", "target_id": "G007",
         "message": "限额应只作用于线上单笔消费，还是也覆盖其他卡类交易？原文只给出“online spend limit”与“Max limit per day”两种说法，未确认统一口径。"},
        {"target_type": "goal", "target_id": "G014",
         "message": "AI 机器人对话与 G013 的人工文字聊天，是“无需电话获得帮助”的两种替代方式，还是需要同时具备？原文以 either 引出，未确认取舍。"},
        {"target_type": "model", "target_id": "DOC004-goal-model",
         "message": "G004、G005、G009、G010、G011、G012、G015 均由对现状的正面评价推断为维持意图，受访者未明确要求保留；其强度按 inferred 记录，待确认。"},
    ],
    "reassessments": [],
}

spec = {
    "document_id": "DOC004",
    "raw_candidates": raw,
    "goals": goals,
    "review_questions": [
        {"candidate_ids": ["G007", "G008"],
         "question": "是否应把“设置单笔限额”与“重要卡片功能更易达”归入同一“卡片控制”上位目标？",
         "reason": "原文由采访者提出“control your debit card access”的框架，涉众仅确认可设置参数并希望限额与更少点击；自建上位目标可能属为凑层级造根，故未建组。"},
        {"candidate_ids": ["G013", "G014"],
         "question": "人工文字聊天与 AI 机器人是否属同一“无需电话获得帮助”目标的替代方式？",
         "reason": "原文以 either ... through an AI bot 引出两种渠道，但两者面向的人群与理由不同（少焦虑/可多任务 与 不熟悉网站），当前作为两个目标保留。"},
        {"candidate_ids": ["G001", "G002"],
         "question": "若手机 App 仍可完成 Zelle 转账，网页端 Zelle 是否仍是必需渠道？",
         "reason": "受访者的理由仅是“不必去拿手机”的便利性，未说明在何种情境下必须使用网页端。"},
    ],
    "limitations": [
        "原文为英文访谈自动转写，含识别噪声（如 sell/cell 指 Zelle、I dive、pays up），未核对音频或原始录音。",
        "未实测 Chase 网站或 App 的当前功能，功能缺口仅依据受访者叙述与其现场操作描述。",
        "未向受访者回问；维持型目标（G004、G005、G009、G010、G011、G012、G015）的需要强度与优先级未知。",
    ],
    "ledger": ledger,
    "decisions": decisions,
}

json.dump(spec, open("spec.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("candidates", len(raw), "goals", len(goals), "entries", len(ENTRIES))
print("checks", len(SOURCE_CHECKS))
