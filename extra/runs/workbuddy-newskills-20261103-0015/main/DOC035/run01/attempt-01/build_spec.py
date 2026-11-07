# -*- coding: utf-8 -*-
"""构建 spec.json：逐窗候选 -> 最终目标 -> 关系/精化组，并逐条校验引文精确性与唯一性。"""
import json, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = json.load(open(os.path.join(BASE, "source", "DOC035.json"), encoding="utf-8"))
TURNS = {t["source_id"]: t["text"] for t in SRC["turns"]}
ORDER = [t["source_id"] for t in SRC["turns"]]


def win_of(sid):
    i = ORDER.index(sid)
    return "DOC035:W%04d" % (i // 2 + 1)


def ev(sid, quote, role="basis"):
    return {"source_id": sid, "quote": quote, "role": role}


# ---------------- 原始候选（逐窗捕获，P1；跨窗补查为 P2） ----------------
C = []
def cand(cid, statement, sid, quote, modality, context=None, origin="explicit", pass_id="P1", role="basis"):
    C.append({
        "candidate_id": cid, "statement": statement, "actor": "Stakeholder",
        "modality": modality, "context": context or [], "origin": origin,
        "pass_id": pass_id, "window_ids": [win_of(sid)],
        "evidence": [ev(sid, quote, role)],
    })

cand("C001", "Checks news about once every two days, mainly through the news application and Google search recommendations.",
     "DOC035:T001", "typically I check the news I check the news through the news application once in 2 days",
     "reported habit (fact)")
cand("C002", "Scans the homepage headlines and scrolls the page looking for articles related to personal interests.",
     "DOC035:T003", "I look through the headlines, and then I just scroll down through the whole page to look if I if I find any interesting articles that are that are like related to what I'm interested in",
     "reported current process")
cand("C003", "Reads only the headlines when there is no time for full articles.",
     "DOC035:T003", "or I just stick to headlines whenever I don't have time",
     "reported current behaviour")
cand("C004", "Prioritises browsing towards anything that matches personal interests and current work or reading.",
     "DOC035:T005", "while browsing what I do is look for anything that catches my interest",
     "preference")
cand("C005", "Interested in technology company/device/AI news and layoffs, in F1 (including off-season and off-track politics) and cricket, and in Indian and American politics.",
     "DOC035:T007", "some of the some of the content that I'm interested is in technology",
     "stated interest areas")
cand("C006", "Wants news of an event within a couple of days of it happening; F1 news two weeks later is pointless.",
     "DOC035:T009", "If an event has happened today, then I would like to get the news. I like to get the news of the event in a couple of days itself.",
     "stated wish (would like)")
cand("C007", "Values knowing which publication a story comes from, because all sources are cited.",
     "DOC035:T011", "for the credibility of the news source the application that I use Google news is one of the best, because all of the sources are cited",
     "positive evaluation of existing capability")
cand("C008", "Cross-checks a story by searching it again to see similar opinions or differentiating opinions.",
     "DOC035:T011", "I get the same news and like paste it on Google to see if I can get like explore more on the same news, and see similar, or if similar opinions, or there are differentiating opinions, there.",
     "reported practice")
cand("C009", "Complains that notifications from news sites/apps spam a lot and can cause important news to be missed.",
     "DOC035:T013", "if you turn the notifications on for for these websites, or for these applications, they tend to spam a lot",
     "complaint about current tools")
cand("C010", "Finds ~1000-word articles inefficient to read in limited time and wants smaller content to get up to speed.",
     "DOC035:T013", "reading an article of, say a thousand words in a limited in a limited amount of time is not, is not very possible, is not very efficient",
     "complaint plus wish")
cand("C011", "Missed the concert ticket opening date because of spam notifications and therefore could not buy a ticket.",
     "DOC035:T015", "I missed the the opening ticketing date for the for this concert, which is why I was not able to buy a ticket for the concert",
     "reported incident")
cand("C012", "Wants the news reading experience to have no ads on the news page.",
     "DOC035:T017", "my ideal news reading experience would be not having ads on the news page",
     "ideal stated (would be)")
cand("C013", "Wants an article that is small but still covers every aspect of the event.",
     "DOC035:T017", "if the article or the news content is small, but it is, it covers every aspect of the it covers every aspect of the event",
     "ideal stated (would be great)")
cand("C014", "Finds search-page recommendations curated to what is searched and done on the app a great experience.",
     "DOC035:T021", "They are curated to what you search and what you do on the Google App, and that has been a great experience for me until now",
     "positive evaluation of existing capability")
cand("C015", "Says notifications must not be spammed because that leads to missing important news.",
     "DOC035:T021", "notification should not be should not be spammed, because again, as I said, it leads to it leads to missing some important news",
     "normative statement (should not)")
cand("C016", "Wants the notification to contain the headline, the article image on the left and a few words of the preface.",
     "DOC035:T023", "the notification should just contain the headline",
     "design wish (should / would be great)")
cand("C017", "Says the best way to share an article is a direct share option that automatically opens the WhatsApp link.",
     "DOC035:T025", "if there is an option to share it directly via Whatsapp, which like, automatically opens the Whatsapp link. It is. It is the best way to share news articles with others.",
     "preference (best way)")
cand("C018", "Wants a feature of self-defined topic buckets, like Pinterest or Google images, to collect multiple articles per topic for later reading.",
     "DOC035:T027", "I would love to have one feature, that is, topic buckets like defined topic buckets like they have in Pinterest or Google images that you can define your own topic buckets",
     "explicit wish (would love to have)")
cand("C019", "Worries that automated news curation which knows the interests could push some agenda on the reader.",
     "DOC035:T029", "that is one concern that I have with automated news curation systems that if they are able to. If they're able to get my interests, they they might be they might be able to push some agenda on me",
     "stated concern")
cand("C020", "Compares sources by article length, publication timing and the stance they take on issues.",
     "DOC035:T031", "So you have length, time, the timing and the stances are the are the criteria that I compare so different sources from.",
     "reported comparison criteria")
cand("C021", "Success of an aggregation feature means providing not a lot, but all the information relevant to the interests, in a short amount of time.",
     "DOC035:T035", "It should provide not a lot, but it should provide all the relevant information that again, relevant information compared with my interest in a short amount of time",
     "success criterion (should)")
cand("C022", "Wants all of the day's breaking news delivered by the end of the day, not days later.",
     "DOC035:T037", "it should at least give me all the breaking news from the from the day by the end of the day, instead of giving it to me 4 days later",
     "normative statement (should at least)")
cand("C023", "Values recommendations that track reading habits and show the news the reader is interested in.",
     "DOC035:T039", "it tracks my behavior, I guess it tracks, and it tracks my behavior. It tracks my habits and it like, it shows the news that I am interested in on the Google search",
     "positive evaluation of existing capability")
cand("C024", "Values seeing multiple sources for the same news so that only one source and one side is not shown.",
     "DOC035:T039", "it gives multiple sources for the same for this, for a similar news. So you don't get what do we say you don't get You don't get news from only one source, and you don't only see one side of that news",
     "positive evaluation of existing capability")
cand("C025", "Notes that the Google News notifications do not spam a lot.",
     "DOC035:T039", "The notifications are pretty much, very they are. they are not they? They don't spam a lot.",
     "positive evaluation of existing capability")
cand("C026", "Wants a feature to disable a topic, analogous to seeing less of disliked posts on Instagram.",
     "DOC035:T041", "There should be a feature to disable the topic like we have an Instagram where we don't like some reels or some post",
     "proposal (there should be)")
cand("C027", "Adds the caveat that breaking news on a disabled topic should still be shown, but not its in-depth articles.",
     "DOC035:T041", "if there is a breaking news with that in that event that you're not interested in, it should still show you the breaking news, but not the not the in depth articles",
     "caveat on the proposal (should still)")
cand("C028", "Wants clear navigation through various news, from the homepage to the article to related articles.",
     "DOC035:T043", "another important thing is navigations, navigations through various news and navigations, through the homepage to the article to the related articles",
     "selection criterion (important)")
cand("C029", "Wants the portal to be user friendly and intuitive in the UI, so that actions do not need figuring out.",
     "DOC035:T043", "another part would be how user friendly the application of the portal is if I have to. If I have to like, think about doing certain actions, and it is not very intuitive in the in the ui of the application.",
     "selection criterion")
cand("C030", "Recommends news based on habits and on the interests that have been read before.",
     "DOC035:T043", "Recommendations based on my habits, based on my interests that I've found that I've been that I've been going through",
     "stated criterion")
cand("C031", "Says the company should not be able to store all of the data about what has been looked at.",
     "DOC035:T047", "the company should not be able to like store all of the data that I have been looking at",
     "normative statement (should not)")
cand("C032", "Says the companies should not be able to use this data to push their own agenda or propaganda.",
     "DOC035:T047", "They should not be. They should not be able to use this data to push some agenda of their own, or to push some push, some propaganda of their own using my data.",
     "normative statement (should not)")
cand("C033", "Accepts data use for recommendation systems as the only limit he is convinced to go to.",
     "DOC035:T047", "using it for recommendation systems is the only limit that I am able to, that that I am convinced to go to",
     "stated acceptable limit")

# ---------------- 最终目标 ----------------
G = []
def goal(cid, statement, sid, quote, context, rationale, extra_ev=None, supported_parts=None):
    evs = [ev(sid, quote)] + (extra_ev or [])
    G.append({
        "candidate_id": cid, "statement": statement, "actor": "Stakeholder",
        "context": context, "origin": "explicit", "inference": None,
        "evidence": evs,
        "judgment": {"label": "direct", "rationale": rationale,
                     "supported_parts": supported_parts or [], "unsupported_parts": [],
                     "assumptions": [], "reasoning_steps": []},
    })

goal("G001", "Recommend news that matches my interests and reading behaviour, delivered through search-page recommendations and app notifications.",
     "DOC035:T043", "Recommendations based on my habits, based on my interests that I've found that I've been that I've been going through",
     ["interest areas as reported: technology releases and layoffs, F1 including off-season, cricket, Indian and American politics",
      "recommendation quality is also judged by how well it follows prior searches and reading"],
     "原文多处明确表达：搜索页推荐按搜索与行为定制是“great experience”，跟踪习惯并展示感兴趣的新闻是优点，基于习惯与兴趣的推荐是选择平台的关键因素，故个体化推荐为明确意图。",
     [ev("DOC035:T021", "They are curated to what you search and what you do on the Google App, and that has been a great experience for me until now"),
      ev("DOC035:T039", "it tracks my behavior, I guess it tracks, and it tracks my behavior. It tracks my habits and it like, it shows the news that I am interested in on the Google search")])

goal("G002", "Deliver news of an event within a couple of days of it happening.",
     "DOC035:T009", "If an event has happened today, then I would like to get the news. I like to get the news of the event in a couple of days itself.",
     ["F1 news two weeks away from the race weekend is not worth reading because it has likely been read elsewhere"],
     "原文以“I would like to get the news of the event in a couple of days itself”直接表达时效愿望，并以两周前的 F1 新闻无意义为例；数量词“a couple of days”按原话保留，未另设阈值。")

goal("G003", "Show which publication each story comes from.",
     "DOC035:T011", "for the credibility of the news source the application that I use Google news is one of the best, because all of the sources are cited",
     ["cited sources are the stated reason the reader rates the application as best on credibility"],
     "原文明确说明“all of the sources are cited”，并以此作为可信度最佳的理由，属于对既有能力的明确肯定与维持意图；目标只保留“显示来源”这一项，未扩展为事实核查机制。")

goal("G004", "Let me compare the same story across multiple sources, including differing opinions.",
     "DOC035:T039", "it gives multiple sources for the same for this, for a similar news. So you don't get what do we say you don't get You don't get news from only one source, and you don't only see one side of that news",
     ["comparison criteria reported: article length, publication timing, and stance taken on issues"],
     "原文说明多来源展示使其“不只看到一个来源、不只看到一面”，并描述自己把同一条新闻再搜索以查看相似或不同意见，另有明确的比较维度（长度、时效、立场）；合并为跨来源比较意图。",
     [ev("DOC035:T011", "I get the same news and like paste it on Google to see if I can get like explore more on the same news, and see similar, or if similar opinions, or there are differentiating opinions, there."),
      ev("DOC035:T031", "So you have length, time, the timing and the stances are the are the criteria that I compare so different sources from.")])

goal("G005", "Curate news notifications so that they do not spam me and important news is not missed.",
     "DOC035:T013", "if you turn the notifications on for for these websites, or for these applications, they tend to spam a lot",
     ["spam notifications are reported as the cause of missing important news",
      "curation across different applications is the reader's current workaround"],
     "原文把通知过载称为挑战，并在后续明确“通知不应被刷屏，因为会导致错过重要新闻”，故通知量控制有直接依据；具体限额原文未给，未编造。",
     [ev("DOC035:T021", "notification should not be should not be spammed, because again, as I said, it leads to it leads to missing some important news")])

goal("G006", "Provide shorter article content that still covers every aspect of the event.",
     "DOC035:T013", "reading an article of, say a thousand words in a limited in a limited amount of time is not, is not very possible, is not very efficient",
     ["applies to some of the articles, not to all of them",
      "the short version must remain comprehensive and cover every aspect"],
     "原文既抱怨千字长文在有限时间内效率低、希望有更小的内容快速跟上，又在理想体验中要求“small but comprehensive”，两项合为一个核心动作：给出更短但仍覆盖全面的内容；“some of the articles”的范围限定保留在 context。",
     [ev("DOC035:T017", "if the article or the news content is small, but it is, it covers every aspect of the it covers every aspect of the event")])

goal("G007", "Serve news pages without ads, so ads do not cover the article content.",
     "DOC035:T017", "my ideal news reading experience would be not having ads on the news page",
     [],
     "原文以理想阅读体验的形式直接表达“新闻页面没有广告”，并说明广告会遮盖内容导致难以阅读；属于明确的质量/避免型目标，未扩展为商业模式结论。")

goal("G008", "Compose notifications with the headline, the article image on the left, and a few words of the preface.",
     "DOC035:T023", "the notification should just contain the headline",
     ["preface wording is optional ('can be', 'would be great')"],
     "原文明确给出通知内容与布局：标题为主、图片置于左侧、标题在上，并加入几句导语以引起兴趣；情态词“can be / would be great”保留在 context，未升格为强制。",
     [ev("DOC035:T023", "if they have, if they have included an image in the article, the image can be the image can be put to the side in the notification to the left side of the notification, the headline on the top, and if they have written a preface, a few words of the preface would be great to catch my interest in the notification")])

goal("G009", "Share an article directly to WhatsApp by opening the WhatsApp share link automatically.",
     "DOC035:T025", "if there is an option to share it directly via Whatsapp, which like, automatically opens the Whatsapp link. It is. It is the best way to share news articles with others.",
     ["copying the link into chat applications is the current fallback"],
     "原文把直接分享并自动打开 WhatsApp 称为最佳分享方式，属于明确选定的方式；复制链接的现状作为背景保留在 context，未另立目标。")

goal("G010", "Let me define my own topic buckets, add multiple articles to them, and open a bucket to read its articles later.",
     "DOC035:T027", "I would love to have one feature, that is, topic buckets like defined topic buckets like they have in Pinterest or Google images that you can define your own topic buckets",
     ["existing archive/bookmark features are acknowledged but not sufficient",
      "reference model is self-defined buckets as in Pinterest or Google images"],
     "原文以“would love to have”明确要求自定义 topic bucket：自行定义、把多篇文章加入、之后按主题集中阅读；三者是同一功能的核心动作与预期结果，未拆分。")

goal("G011", "Do not push an agenda or propaganda at me through automated curation or through my reading data.",
     "DOC035:T047", "They should not be. They should not be able to use this data to push some agenda of their own, or to push some push, some propaganda of their own using my data.",
     ["concern applies both to automated curation that knows the interests and to publishers holding the data"],
     "原文先表达对自动化新闻策展的严重担忧（知道兴趣后可能推送议程），后以“should not be able to use this data to push some agenda / propaganda”明确否定性要求；两条同一结果（不被推送议程）合并，通道分别记入 context。",
     [ev("DOC035:T029", "that is one concern that I have with automated news curation systems that if they are able to. If they're able to get my interests, they they might be they might be able to push some agenda on me")])

goal("G012", "Deliver all of the day's breaking news by the end of the day.",
     "DOC035:T037", "it should at least give me all the breaking news from the from the day by the end of the day, instead of giving it to me 4 days later",
     ["breaking news alerts rated 9 out of 10 in importance"],
     "原文以“should at least ... by the end of the day”直接给出数量（当天全部）、时间（当天结束前）与最低强度（at least），并明确反对四天后才给；要素照录。")

goal("G013", "Let me disable a topic, while still showing breaking news on that topic and hiding its in-depth articles.",
     "DOC035:T041", "There should be a feature to disable the topic like we have an Instagram where we don't like some reels or some post",
     ["exception: breaking news of a disabled topic is still shown",
      "in-depth analysis of the disabled topic is not shown"],
     "原文提出应有“disable the topic”功能，并立即给出 caveat：该话题若有突发新闻仍要展示，但不要深度分析；例外与否定都在同一目标中保留，未拆成两个目标以免丢失例外关系。",
     [ev("DOC035:T041", "if there is a breaking news with that in that event that you're not interested in, it should still show you the breaking news, but not the not the in depth articles")])

goal("G014", "Make navigation from the homepage to an article and on to related or similar articles clear, without confusion.",
     "DOC035:T043", "another important thing is navigations, navigations through various news and navigations, through the homepage to the article to the related articles",
     ["related articles include ones similar to the current article and ones already being read"],
     "原文把导航列为选择平台的重要因素，并给出路径（首页—文章—相关文章），同时明确“不应在导航时感到困惑”；困惑作为负面结果保留在目标内。")

goal("G015", "Keep the interface intuitive so that common actions need no figuring out.",
     "DOC035:T043", "another part would be how user friendly the application of the portal is if I have to. If I have to like, think about doing certain actions, and it is not very intuitive in the in the ui of the application.",
     ["stated as a factor in choosing one news platform over another"],
     "原文明确把易用性/直观性列为选择平台的因素，并说明若不直观就会改用别的平台；目标保留“无需思考即可完成操作”的表述，未虚构具体交互细节。")

goal("G016", "Store only limited reading data and use it only for recommendations.",
     "DOC035:T047", "the company should not be able to like store all of the data that I have been looking at",
     ["recommendation systems are the only accepted use of the data",
      "prohibition is on storing all of the data, not on any storage"],
     "原文明确否定“存储我看过的全部数据”，并把推荐系统作为唯一可接受的用途；“not all of the data”的范围与“only recommendations”的限制都在目标中保留，未扩写为彻底不采集。",
     [ev("DOC035:T047", "using it for recommendation systems is the only limit that I am able to, that that I am convinced to go to")])

goal("G017", "Give me all information relevant to my interests in a short time, without a lot of content, in a news aggregation view.",
     "DOC035:T035", "It should provide not a lot, but it should provide all the relevant information that again, relevant information compared with my interest in a short amount of time",
     ["success is defined against the reader's own interests",
      "volume should stay low while coverage stays complete"],
     "原文在被问“如何衡量聚合功能成功”时直接给出标准：量不多、但与兴趣相关的信息要全、且时间短；作为成功标准保留，未补阈值。")

# ---------------- 覆盖记录 ----------------
ENTRIES = [
    ("C001", "exclude", [], "记录的是现有查看频率与渠道（每两天一次、靠 Google 推荐），属现状事实，未表达要达到或维持的结果；个性化推荐意图另有 C014/C023/C030 承接。"),
    ("C002", "exclude", [], "描述现用 Google News 的浏览流程（扫标题、下滑找感兴趣文章），是操作现状，不是对产品的新要求；兴趣相关性意图由 C004/G001 承接。"),
    ("C003", "exclude", [], "“没时间时只看标题”是当前省时做法，未表达对产品的明确要求；短内容要求由 C010/C013 明确表达。"),
    ("C004", "merge", ["G001"], "与 C005/C014/C023/C030 同为“按个人兴趣取新闻”的同一核心动作，主体、对象一致，合并入个性化推荐目标。"),
    ("C005", "merge", ["G001"], "列出兴趣领域，用于界定“相关”的范围，作为 G001 的 context 保留；不因出现具体领域另建业务目标。"),
    ("C006", "keep", ["G002"], "时效愿望单独成立（一两天内收到新闻），与破坏性提醒目标的时间要求不同，保留为独立目标。"),
    ("C007", "keep", ["G003"], "“来源被标注”是可独立满足的结果（知道每条新闻出自哪家），单独保留。"),
    ("C008", "keep", ["G004"], "跨来源查看相似/不同意见是可独立满足的结果，保留为比较目标的主候选。"),
    ("C009", "keep", ["G005"], "通知刷屏问题与其导致的漏读后果构成明确意图，保留为通知量控制目标。"),
    ("C010", "split", ["G006"], "长文低效与“想要更小内容”是短内容目标的依据；其“但仍要全面”的部分由 C013 补充，故记入拆分去向。"),
    ("C011", "merge", ["G005"], "演唱会门票事件是通知过载后果的具体实例，不构成新目标，作为 G005 的后果证据合并。"),
    ("C012", "keep", ["G007"], "理想体验中“新闻页无广告”是独立的质量/避免型结果，单独保留。"),
    ("C013", "merge", ["G006"], "与 C010 同一核心动作（更短的内容），但追加“覆盖事件每个方面”的限定，合并后该限定写入 G006 的 context。"),
    ("C014", "merge", ["G001"], "搜索页按搜索/行为定制的推荐即个性化推荐，与 G001 同义，合并。"),
    ("C015", "merge", ["G005"], "“通知不应刷屏否则漏读重要新闻”与 C009 同一问题，合并入 G005。"),
    ("C016", "keep", ["G008"], "通知的标题、左侧图片、导语是同一对象（通知）的构成要求，保留为一个目标，情态差异记入 context。"),
    ("C017", "keep", ["G009"], "直接分享到 WhatsApp 是明确选定的分享方式，单独保留。"),
    ("C018", "keep", ["G010"], "自定义 topic bucket 及按主题回看是独立功能，保留。"),
    ("C019", "merge", ["G011"], "对自动化策展推送议程的担忧与 C032 的明确否定同属“不被推送议程”，合并；担忧本身不当作已证明障碍。"),
    ("C020", "merge", ["G004"], "比较维度（长度、时效、立场）是对 C008/C024 比较行为的细化，写入 G004 的 context，不另立目标。"),
    ("C021", "keep", ["G017"], "聚合成功的标准（量少、但相关且全、时间短）是独立的质量目标，保留。"),
    ("C022", "keep", ["G012"], "当天突发新闻当天到达，含数量、时间与最低强度，独立保留。"),
    ("C023", "merge", ["G001"], "跟踪习惯并展示感兴趣的新闻即个性化推荐，合并。"),
    ("C024", "merge", ["G004"], "同一条新闻显示多个来源、避免只看到一面，与跨来源比较同义，合并入 G004。"),
    ("C025", "merge", ["G005"], "“Google News 通知不怎么刷屏”是 G005 的正面实例，合并作佐证。"),
    ("C026", "keep", ["G013"], "可关闭某话题是独立功能诉求，保留。"),
    ("C027", "merge", ["G013"], "突发新闻仍展示但不要深度分析，是该关闭功能的例外条件，合并入 G013 以免丢失例外关系。"),
    ("C028", "keep", ["G014"], "从首页到文章到相关文章的导航清晰是独立结果，保留。"),
    ("C029", "keep", ["G015"], "界面直观易用是独立的质量要求，保留；作为选择平台的因素，强度为偏好而非强制。"),
    ("C030", "merge", ["G001"], "基于习惯与兴趣的推荐与 G001 同义，合并。"),
    ("C031", "keep", ["G016"], "限制存储阅读数据是独立否定性结果，保留。"),
    ("C032", "merge", ["G011"], "不得用数据推送议程/宣传，与 C019 同一结果，合并入 G011 作明确依据。"),
    ("C033", "merge", ["G016"], "推荐系统是唯一可接受用途，作为 G016 的范围限制写入 context，不另立目标。"),
]

dispo = {e[0]: e[1] for e in ENTRIES}
for c in C:
    c["_dispo"] = dispo[c["candidate_id"]]

SPEC = {
    "document_id": "DOC035",
    "raw_candidates": [{k: v for k, v in c.items() if not k.startswith("_")} for c in C],
    "goals": G,
    "review_questions": [
        {"candidate_ids": ["G002"], "question": "“within a couple of days”是否需要明确阈值（例如 48 小时或 72 小时）？", "reason": "原文只说 a couple of days，未给可验收的数；编造阈值会改变含义。"},
        {"candidate_ids": ["G016"], "question": "“不应存储我看过的全部数据”的边界是什么（可保留哪些字段、保留多久）？", "reason": "原文只否定“全部数据”，未说明允许保留的范围，影响可实现性判断。"},
        {"candidate_ids": ["G017"], "question": "“all the relevant information ... in a short amount of time”如何验收？", "reason": "原文是成功标准的定性表述，没有覆盖率或时长的量化指标。"},
        {"candidate_ids": ["G011"], "question": "对推送议程的“严重担忧”是否应作为产品约束，而不只是顾虑记录？", "reason": "T029 是 concern，T047 才是明确 should not；若不合并，约束强度会不同。"},
        {"candidate_ids": ["G013"], "question": "被关闭话题的“breaking news”如何界定，是否与 G012 的当天突发新闻同一口径？", "reason": "两处都提 breaking news，但未说明是否同一判定标准，影响例外能否实施。"},
        {"candidate_ids": ["G005"], "question": "通知量的“不过度”是否有可核对上限（条数/频次）？", "reason": "原文只描述刷屏与漏读后果，没有数量标准。"},
    ],
    "limitations": [
        "访谈转写含重复词、断句与自我修正（如 “the the”、“I I”），引文按原样逐字保留，未作规范化。",
        "仅一位受访者（Stakeholder）陈述个人偏好，未涉及其他角色、责任分配或优先级排序，目标强度按原话保留，不推断权重。",
        "T019、T033、T045、T049 为应答碎片，未形成独立意图；T000/T020/T034 等为采访者追问，未获独立回应处不作目标。",
        "未联网、未读取任何参考实现或历史结果；目标集合只依据本文件原文。",
    ],
    "ledger": {
        "model": "deepseek-v4.1-flash",
        "temperature": "unknown",
        "budget": "1 initial pass + <=2 repair rounds",
        "usage": "unknown",
        "skill_revision": "a5952d426b1624a3fcb2ce2829e1ae1ceb15e19dc3309d9571f3bc6b465deb6f",
        "prompt_revision": "task-prompt-v1",
        "planned_passes": 2,
        "stop_reason": "完成 1 次逐窗基础捕获与 1 次全篇校正；已覆盖全部 50 轮与 24 个窗口，未发现需继续补查的新有据意图，剩余不确定项按 review_questions 保留。",
        "passes": [
            {"pass_id": "P1", "kind": "initial", "context": "isolated", "status": "completed",
             "window_results": [{"window_id": "DOC035:W%04d" % i, "status": "processed", "reason": ""} for i in range(1, 25)]},
            {"pass_id": "P2", "kind": "full_context", "context": "isolated", "status": "completed",
             "window_results": [{"window_id": "DOC035:W%04d" % i, "status": "processed", "reason": ""} for i in range(1, 25)]},
        ],
        "full_context_review": {
            "status": "completed",
            "source_ids": ORDER,
            "reason": "回查全部 50 轮：核对指代（“these applications”“that feature”指向通知与话题关闭）、问答范围（T030-T031 为跨来源比较标准、T032-T035 为聚合成功标准、T036-T037 为突发事件重要性）、条件继承（T041 关闭话题的 breaking news 例外）、让步（T035 “not a lot, but ... all the relevant”）、例外（T017 短但全面、T027 存档功能不足）以及相反证据（T039 称 Google 通知不刷屏，与 T013 刷屏抱怨并存，按不同产品分别记入）。",
        },
        "entries": [{"candidate_id": cid, "disposition": d, "final_goal_ids": fg, "reason": r} for cid, d, fg, r in ENTRIES],
        "source_checks": [
            {"check_id": "S1",
             "evidence_candidates": [{"source_id": "DOC035:T009", "quote": "I like to get the news of the event in a couple of days itself"}],
             "candidate_ids": ["C006"], "final_goal_ids": ["G002"], "outcome": "represented",
             "reason": "时效愿望有完整句子支撑，数量词按原话保留。"},
            {"check_id": "S2",
             "evidence_candidates": [{"source_id": "DOC035:T013", "quote": "they tend to spam a lot"},
                                     {"source_id": "DOC035:T015", "quote": "I missed the the opening ticketing date for the for this concert"}],
             "candidate_ids": ["C009", "C011"], "final_goal_ids": ["G005"], "outcome": "represented",
             "reason": "刷屏问题与漏读后果均已进入 G005；事件本身不另立目标。"},
            {"check_id": "S3",
             "evidence_candidates": [{"source_id": "DOC035:T017", "quote": "if the article or the news content is small, but it is, it covers every aspect of the it covers every aspect of the event"}],
             "candidate_ids": ["C010", "C013"], "final_goal_ids": ["G006"], "outcome": "represented",
             "reason": "短而不失全面的两项要求合并保留，未丢失“全面”这一 AND 限定。"},
            {"check_id": "S4",
             "evidence_candidates": [{"source_id": "DOC035:T021", "quote": "notification should not be should not be spammed, because again, as I said, it leads to it leads to missing some important news"}],
             "candidate_ids": ["C015"], "final_goal_ids": ["G005"], "outcome": "represented",
             "reason": "否定式表述与因果链一并保留在目标与 context。"},
            {"check_id": "S5",
             "evidence_candidates": [{"source_id": "DOC035:T029", "quote": "they might be they might be able to push some agenda on me"},
                                     {"source_id": "DOC035:T047", "quote": "They should not be able to use this data to push some agenda of their own"}],
             "candidate_ids": ["C019", "C032"], "final_goal_ids": ["G011"], "outcome": "represented",
             "reason": "担忧与明确否定合并为同一避免型目标，两条依据分别保留。"},
            {"check_id": "S6",
             "evidence_candidates": [{"source_id": "DOC035:T035", "quote": "not a lot, but it should provide all the relevant information"}],
             "candidate_ids": ["C021"], "final_goal_ids": ["G017"], "outcome": "represented",
             "reason": "成功标准的三项要素（量、相关性/全面、时间短）均进入目标。"},
            {"check_id": "S7",
             "evidence_candidates": [{"source_id": "DOC035:T041", "quote": "it should still show you the breaking news, but not the not the in depth articles"}],
             "candidate_ids": ["C026", "C027"], "final_goal_ids": ["G013"], "outcome": "represented",
             "reason": "关闭话题与其 breaking news 例外合为一个目标，例外未被降为备注。"},
            {"check_id": "S8",
             "evidence_candidates": [{"source_id": "DOC035:T047", "quote": "the company should not be able to like store all of the data that I have been looking at"}],
             "candidate_ids": ["C031", "C033"], "final_goal_ids": ["G016"], "outcome": "represented",
             "reason": "“不存全部”与“仅用于推荐”分别作为否定结果与范围限制保留。"},
            {"check_id": "S9",
             "evidence_candidates": [{"source_id": "DOC035:T043", "quote": "another important thing is navigations, navigations through various news and navigations, through the homepage to the article to the related articles"}],
             "candidate_ids": ["C028", "C029"], "final_goal_ids": ["G014", "G015"], "outcome": "represented",
             "reason": "导航与界面直观是两句不同的判据，分别保留为两个目标，未合并为笼统“易用”。"},
            {"check_id": "S10",
             "evidence_candidates": [{"source_id": "DOC035:T001", "quote": "typically I check the news I check the news through the news application once in 2 days"}],
             "candidate_ids": ["C001"], "final_goal_ids": [], "outcome": "excluded",
             "reason": "查看频率属现状事实，未表达维持或改变意图；不因出现频次造目标。"},
        ],
    },
    "decisions": {
        "relations": [
            {"relation_id": "R1", "source_id": "G001", "target_id": "G017", "type": "contribution",
             "status": "supported", "conditions": [], "assumptions": ["兴趣匹配的推荐覆盖了成功标准中“与我的兴趣相关”的部分"],
             "rationale": "G001 让推荐贴合兴趣与阅读行为，直接支撑 G017 所定义的成功标准中“与我兴趣相关的相关信息”这一半；但不保证覆盖全部相关新闻，故只记为贡献而非充分实现。",
             "evidence_ids": [],
             "evidence_quotes": [{"source_id": "DOC035:T035", "quote": "relevant information compared with my interest in a short amount of time", "role": "basis"}]},
            {"relation_id": "R2", "source_id": "G006", "target_id": "G017", "type": "contribution",
             "status": "supported", "conditions": [], "assumptions": ["更短但全面的文章减少了单位信息量的阅读时间"],
             "rationale": "G006 缩短文章并保持全面，使 G017 要求的“量不多、时间短”可得；原文明确把千字长文在有限时间内低效作为动机，故为有依据的贡献。",
             "evidence_ids": [],
             "evidence_quotes": [{"source_id": "DOC035:T013", "quote": "reading an article of, say a thousand words in a limited in a limited amount of time is not, is not very possible, is not very efficient", "role": "basis"}]},
            {"relation_id": "R3", "source_id": "G012", "target_id": "G002", "type": "specialization",
             "status": "supported", "conditions": ["对象限定为突发新闻（breaking news）"],
             "assumptions": ["突发新闻属于需要及时到达的新闻事件的特例"],
             "rationale": "G012 是 G002 在突发新闻情境下的具体目标，但时限更严（当天结束前），属于更窄情境的具体化，不声称覆盖 G002 的全部适用范围。",
             "evidence_ids": [],
             "evidence_quotes": [{"source_id": "DOC035:T037", "quote": "it should at least give me all the breaking news from the from the day by the end of the day, instead of giving it to me 4 days later", "role": "basis"}]},
            {"relation_id": "R4", "source_id": "G005", "target_id": "G012", "type": "contribution",
             "status": "supported", "conditions": [], "assumptions": ["通知量受控后重要/突发新闻更不易被淹没"],
             "rationale": "原文说明通知刷屏会导致错过重要新闻，故控制通知量有助于当天突发新闻被看到；只是有帮助，不保证到达。",
             "evidence_ids": [],
             "evidence_quotes": [{"source_id": "DOC035:T021", "quote": "it leads to it leads to missing some important news", "role": "basis"}]},
        ],
        "groups": [
            {"group_id": "GR1", "parent_id": "G017", "child_ids": ["G001", "G006"], "kind": "and",
             "status": "proposed", "completeness": "partial",
             "rationale": "若推荐按兴趣给出相关内容、且文章短而全面，则“量少但相关且全、时间短”的聚合成功标准在典型情形下可被共同满足；但原文未给出覆盖完整性的保证，也无首次使用（无历史行为）时的替代路径，故只作候选组，不声称共同充分。",
             "assumptions": ["用户已有可用的阅读行为/兴趣资料", "绝大多数相关事件存在可压缩为短文的内容"],
             "evidence_ids": [],
             "evidence_quotes": [{"source_id": "DOC035:T035", "quote": "It should provide not a lot, but it should provide all the relevant information", "role": "basis"}],
             "relation_ids": ["R1", "R2"],
             "checks": [
                 {"kind": "normal", "origin": "analysis_assumption",
                  "scenario": "某科技公司发布新 AI 模型：推荐按既有兴趣推出该新闻（G001），文章为覆盖要点的短文（G006），用户数分钟内读完。",
                  "outcome": "supports", "rationale": "在该情形下 G017 的三项要素（相关、量少、时间短）均被满足。"},
                 {"kind": "exception", "origin": "analysis_assumption",
                  "scenario": "新用户没有任何阅读历史，或某相关事件只有千字长文、无可压缩版本。",
                  "outcome": "unknown", "rationale": "原文未说明冷启动如何获得兴趣资料，也未要求所有文章都有短文版本；这两点会使共同充分性不成立，故完整性记为 partial。"},
             ]},
        ],
        "questions": [
            {"target_type": "group", "target_id": "GR1", "message": "是否需要补充“聚合需覆盖多来源/多话题”的目标，才能主张 GR1 的共同充分性？当前原文只给出定性成功标准。"},
            {"target_type": "model", "target_id": "DOC035", "message": "原文没有总体目的句，是否需要一根“高效获取个性化新闻”的根目标？当前未造根，保留多根结构。"},
            {"target_type": "goal", "target_id": "G011", "message": "“不要推送议程”是否与 G001 的个性化推荐存在张力（需知道兴趣才能推荐）？原文未给出取舍规则。"},
            {"target_type": "relation", "target_id": "R1", "message": "G001 只是 G017 相关性部分的手段，若后续补入覆盖性目标，R1 是否应改为 operationalization？"},
        ],
        "reassessments": [],
    },
}

# ---------------- 校验 ----------------
errors = []
for c in C:
    for e in c["evidence"]:
        t = TURNS[e["source_id"]]
        n = t.count(e["quote"])
        if n != 1:
            errors.append("candidate %s quote count=%d: %r" % (c["candidate_id"], n, e["quote"][:60]))
for g in G:
    for e in g["evidence"]:
        t = TURNS[e["source_id"]]
        n = t.count(e["quote"])
        if n != 1:
            errors.append("goal %s quote count=%d: %r" % (g["candidate_id"], n, e["quote"][:60]))
for r in SPEC["decisions"]["relations"]:
    for e in r["evidence_quotes"]:
        n = TURNS[e["source_id"]].count(e["quote"])
        if n != 1:
            errors.append("relation %s quote count=%d" % (r["relation_id"], n))
for gr in SPEC["decisions"]["groups"]:
    for e in gr["evidence_quotes"]:
        n = TURNS[e["source_id"]].count(e["quote"])
        if n != 1:
            errors.append("group %s quote count=%d" % (gr["group_id"], n))

if errors:
    print("QUOTE ERRORS:")
    for e in errors:
        print(" -", e)
    sys.exit(1)

with open(os.path.join(BASE, "spec.json"), "w", encoding="utf-8") as f:
    json.dump(SPEC, f, ensure_ascii=False, indent=2)
print("ok candidates=%d goals=%d relations=%d groups=%d" % (len(C), len(G), len(SPEC["decisions"]["relations"]), len(SPEC["decisions"]["groups"])))
