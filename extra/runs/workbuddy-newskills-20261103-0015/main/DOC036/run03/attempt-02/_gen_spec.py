# -*- coding: utf-8 -*-
"""生成 spec.json（语义内容由本次会话编制），并逐字校验证据引文。"""
import json
from pathlib import Path

src = json.load(open('source/DOC036.json', encoding='utf-8'))
TXT = {t['source_id']: t['text'] for t in src['turns']}
SHA = 'a5952d426b1624a3fcb2ce2829e1ae1ceb15e19dc3309d9571f3bc6b465deb6f'

def ev(sid, quote, role='basis'):
    return {'source_id': sid, 'quote': quote, 'role': role}

def evs(items):
    return [ev(s, q) for s, q in items]

# ---------------- raw candidates ----------------
# (id, statement, [(source_id, quote)], origin)
RAW = [
 ("C001","Use Instagram mainly to shop on special occasions like Valentine's Day, e.g. to get a specific gift (a cake) for my girlfriend",
  [("DOC036:T010","So I use Instagram mainly to shop on days like Valentine's Day, for example."),
   ("DOC036:T010","So I would go on Instagram to get my my girlfriend, maybe a cake from a really good spot")],"explicit"),
 ("C002","Spot cake-vendor accounts (mostly cakes, because girlfriend likes cakes) and order really good cakes from there",
  [("DOC036:T010","So I try to spot like you know, accounts that I've mostly like cakes"),
   ("DOC036:T010","And and I and I order from there.")],"explicit"),
 ("C003","See the shop's contact and reach out via landline or WhatsApp to purchase (main way I purchase on Instagram)",
  [("DOC036:T010","because then I would go and see the the contact of the shop, and then I would use that now to reach out to them")],"explicit"),
 ("C004","For clothing/dresses: view a vendor's showcased designs online, then go to an actual market and ask for those same designs",
  [("DOC036:T010","I would I could go to an account of a vendor who, you know, is who is showcasing this plot, and, you know, see the designs they have in store."),
   ("DOC036:T010","I'll go to an actual market and ask for those.")],"explicit"),
 ("C005","Shops in Rwanda can have a business account on Instagram to post products (cakes to dresses to drawers)",
  [("DOC036:T010","if you have a shop, you can actually more or less have it as a business account on Instagram, where you post like the products you make.")],"explicit"),
 ("C006","Those have been the 2 primary use cases of me using Instagram",
  [("DOC036:T010","So those have been the 2 primary use cases of of me using like, Instagram, yeah.")],"explicit"),
 ("C007","Enter the name of what I want to look for (e.g. cakes) in the search bar",
  [("DOC036:T012","and there you can now enter the name of of what you want to look for. So in my case, I would be like cakes.")],"explicit"),
 ("C008","Search returns cake vendors in the area I am in (e.g. cakes in the Us) - I found that really useful",
  [("DOC036:T012","it will search for like cake vendors in the area you are in right.")],"explicit"),
 ("C009","If I don't immediately see what I want, add the location name (e.g. cakes in Rwanda / cake sellers in ...) to the search",
  [("DOC036:T012","and if I don't see immediately what I'm looking for, I'll just add maybe the name of the location.")],"explicit"),
 ("C010","Search results show vendor accounts, not products",
  [("DOC036:T014","It. It shows me it would show me the accounts.")],"explicit"),
 ("C011","Even after seeing a product, I still need to get in touch with the vendor to have it sent (unlike Amazon's swipe-card-and-delivered flow)",
  [("DOC036:T014","you need to still get in touch with the vendor right? to get the the product sent to you.")],"explicit"),
 ("C012","I'm sure it's definitely good that way, especially in my side of the world",
  [("DOC036:T014","I'm sure it's definitely good that way, especially like my side of the world")],"explicit"),
 ("C013","A malicious account asks you to send money first; then you don't get the product, you lose the money, and you can't track the account",
  [("DOC036:T014","they will tell you to send the money. and when you send that money you will not get the product delivered to you right"),
   ("DOC036:T014","and you've lost the money, and there is no way you can track who has this account")],"explicit"),
 ("C014","I didn't lose my money because I understood you have to deliver before I pay you",
  [("DOC036:T014","I didn't lose my money, because maybe I was very wise to understand that. You know you have to deliver before I pay you.")],"explicit"),
 ("C015","See the vendor's phone number and contact info in the account bio and reach out (WhatsApp or normal call)",
  [("DOC036:T016","And then in the account, bio, that that is where I would see, like, maybe their phone number and their and and their contact information.")],"explicit"),
 ("C016","Response time for a very active account is quick / low latency",
  [("DOC036:T016","Usually the response time. If it's a if it's a very active account, is not that it's it's actually quick. There is low latency.")],"explicit"),
 ("C017","You can also reach out via in-app Instagram chat and they will get back to you",
  [("DOC036:T016","You can. You can do a Instagram chat to that number, and then they will get back to you right")],"explicit"),
 ("C018","I would always prefer to reach out to the number they've specified, because communication is quicker (and I don't expect them always online)",
  [("DOC036:T016","I would. I would always prefer to, you know, reach out to the number they've specified, because that way the communication is quicker.")],"explicit"),
 ("C019","Yeah, they are, yeah. (confirm malicious accounts are an obstacle)",
  [("DOC036:T018","Yeah, they are, yeah.")],"explicit"),
 ("C020","Sometimes I go with a very open mind, with no particular product in mind",
  [("DOC036:T022","I think there are some times when I go with a very open mind. I don't have a particular product in mind.")],"explicit"),
 ("C021","Shuffle through a bunch of images and products and might pick something I did not imagine I'd pick",
  [("DOC036:T022","and I might end up picking something that you know I not imagine I'll pick")],"explicit"),
 ("C022","It's a good way to see what's available and choose in the moment, giving flexibility (as opposed to buying something planned)",
  [("DOC036:T022","So that gives you some kind of flexibility in your choices.")],"explicit"),
 ("C023","I like seeing a bunch of products with different varieties from one vendor (a really good thing)",
  [("DOC036:T022","The fact that I can see like a bunch of products from one vendor with different varieties.")],"explicit"),
 ("C024","I do not like that I have to sign in to use the app; I would have loved to use it without signing in (it takes time)",
  [("DOC036:T024","so I would have loved to use the application without signing in right, but I but each time I have to use it I have to sign it.")],"explicit"),
 ("C025","Sometimes I don't want someone to know I'm online; I just want to search, get it, and get out",
  [("DOC036:T024","Sometimes I don't want someone to know online. I just want to go and search for what I'm searching for. I get it. And I'm and I'm out of it right?")],"explicit"),
 ("C026","Search results are saved in a dropdown so after a month I can pick a vendor I used in the past and don't have to always search for vendors (a good feature)",
  [("DOC036:T024","It's gonna save my search results right in a dropdown."),
   ("DOC036:T024","I can just pick one I used in the past.")],"explicit"),
 ("C027","Vendor page has bio, highlights (events with products), and a gallery of images with comments and likes",
  [("DOC036:T024","The good with the gallery is that when you go to the gallery you have people commenting, and you also have likes.")],"explicit"),
 ("C028","Gallery engagement (likes/comments) shows people use/love/recommend the products - an important feature",
  [("DOC036:T024","Because if you see engagement, then you'd actually know that actually, people are using this site.")],"explicit"),
 ("C029","I used the gallery to spot that the other account was malicious: old products should have more likes; uniform ~1 like / 0 comments means everything was uploaded at once",
  [("DOC036:T024","I that helped me to spot that you know."),
   ("DOC036:T024","But then, if you are seeing just one like and maybe 0 comments")],"explicit"),
 ("C030","After perusing, comments can say maybe this is what I might need for my girlfriend / whoever I'm buying for",
  [("DOC036:T024","and the comments can say, Oh, yeah, maybe this is what you know I might need for for my girlfriend")],"explicit"),
 ("C031","I could search for a person by name (e.g. John Mc)",
  [("DOC036:T026","Yes, definitely I could search for.")],"explicit"),
 ("C032","It's a good way to connect with people and share photos of yourself and what you are doing",
  [("DOC036:T026","it's a good way to connect with people to share, you know, photos of yourself")],"explicit"),
 ("C033","I tend to be careful about posting about my life/stuff on social media, because it could come back to hurt/hunt you in the future",
  [("DOC036:T026","I tend to be careful with that aspect of you know, posting about your life and your stuff on social media."),
   ("DOC036:T026","Because, it's it's just it could come back, you know, to hurt you or hunt you in the future.")],"explicit"),
 ("C034","I make sure I have a private account (currently private) so only very close friends see my posts and see I'm online",
  [("DOC036:T026","then I make sure I have a private account, because my account currently is private."),
   ("DOC036:T026","and if I'm online, I would expect that just my very close friends would see I'm online.")],"explicit"),
 ("C035","It helps weed away the evils of people preying on your life on social media",
  [("DOC036:T026","So it kind of helps to weed away the the the evils of you know, people preying on your life and on social media and all of that stuff.")],"explicit"),
 ("C036","It's a good way to connect, but it has downsides if you're very open/outlandish about your life, which I find unnecessary",
  [("DOC036:T026","which which I just find to be unnecessary.")],"explicit"),
 ("C037","Yes, it does. (confirm the app has a social component)",
  [("DOC036:T028","Yes, it does.")],"explicit"),
 ("C038","I would follow someone on Instagram to connect more with them (like Facebook)",
  [("DOC036:T030","I would go to follow you on Instagram.")],"explicit"),
 ("C039","If I lose your phone number/contact/email, we're still friends on Instagram so I can always reconnect via the app (I travel and keep changing numbers)",
  [("DOC036:T030","if any time in in this life. I lose your phone number or your immediate contact or your email address."),
   ("DOC036:T030","I can always, you know, reconnect with you by getting in touch with you, using using the application.")],"explicit"),
 ("C040","I like to dress in a particular way / dress cool",
  [("DOC036:T032","So for me, I like to dress in a particular way")],"explicit"),
 ("C041","Seeing something someone wears that looks good can play a role in me acquiring it at the market - an enabler in purchasing particular products, consciously or unconsciously",
  [("DOC036:T032","it will kind of play a role in me, actually acquiring it"),
   ("DOC036:T032","I would say an enabler in you purchasing particular product. whether you, whether it is consciously or unconsciously, it has that effect.")],"explicit"),
 ("C042","That's one reason I try to stay away from it a lot; I don't know what else it could make me do unconsciously; I stay away when I have no use for it and only use it when I have a need",
  [("DOC036:T032","that is one of the reasons why I try to stay away from it a lot"),
   ("DOC036:T032","it could make me do unconsciously, unconsciously."),
   ("DOC036:T032","So I try to stay away from it when I'm when I'm not having any use for it, and only use it when I have, you know, a need for it.")],"explicit"),
 ("C043","Infinite scroll keeps updating content as you scroll; wanting to catch up with people is addictive and very time-consuming",
  [("DOC036:T034","it has an infinity school where it just keeps on updating content as you scroll down"),
   ("DOC036:T034","those things make it kind of addictive and very time consuming.")],"explicit"),
 ("C044","Following a user can be mutual (become friends); following a celebrity is one-way; you can also follow groups/hashtags and see their content",
  [("DOC036:T036","if I follow you. you can follow me back, and we become friends"),
   ("DOC036:T036","you could also more or less follow like groups or hashtags.")],"explicit"),
 ("C045","Following star people for advice and lessons about life I find irrelevant",
  [("DOC036:T036","for the advice and lessons about life, which again, I find to be irrelevant.")],"explicit"),
 ("C046","Yeah. And that's true. (confirm following a person shows their info in an infinite scroll)",
  [("DOC036:T038","Yeah. And that's true.")],"explicit"),
 ("C047","I haven't really used Instagram groups; Facebook has a group feature and since Facebook runs Instagram it's imperative they brought those features too (belief)",
  [("DOC036:T044","I haven't really used groups."),
   ("DOC036:T044","It. It's it's kind of imperative that they brought those features as well to Instagram.")],"explicit"),
 ("C048","Subscribing to a hashtag (more or less like a group) shows posts with that hashtag in your feed - but it's not the same as Facebook groups",
  [("DOC036:T044","but I know their hashtags whereby if you subscribe to a hashtag which is more or less like a group."),
   ("DOC036:T044","It's gonna show up on your in your feed, right?"),
   ("DOC036:T044","But it's not the same way.")],"explicit"),
 ("C049","The main one is that I have to log in before I can view or do anything with the app; I wish it was not the case / I would have hoped I could do things without logging in (even just viewing a vendor's profile) - this is the main obstacle",
  [("DOC036:T052","I have to log in before I can view or do anything with the app. I wish it was not the case"),
   ("DOC036:T052","even if it's to view the profile of the vendor. it's a bit disturbing."),
   ("DOC036:T052","I would have hoped that. You know I could do things without needing to log in")],"explicit"),
 ("C050","I log out / delete the app / delete web history so that I don't use it very often and only access it when I need something",
  [("DOC036:T052","so that I don't use it very often."),
   ("DOC036:T052","I just I just kinda lock out myself and then delete the application on my phone."),
   ("DOC036:T052","and I only access it when I need something."),
   ("DOC036:T052","how I try to manage the use of the application.")],"explicit"),
 ("C051","As a workaround, around Valentine's I start looking a few days ahead and stay logged in during that period, then log out after I've gotten what I want",
  [("DOC036:T052","During Valentine's I would start looking at stuff like few days towards that time")],"explicit"),
 ("C052","Interviewer: one aspect is trying to limit your use; another is you would appreciate anonymous browsing without signing in while still using the app - Stakeholder: Exactly. Yeah.",
  [("DOC036:T053","Another one sounds like you would really appreciate some type of anonymous browsing where you don't actually have to sign in. But you can still use the app."),
   ("DOC036:T054","Exactly. Yeah.")],"explicit"),
 ("C053","When in a new place (having moved countries), Instagram's vendor accounts/bios quickly show where vendors are, their location, phone number and products - very helpful for someone in a place for a short time",
  [("DOC036:T056","You don't really know, like the vendors there, you don't know what they have to offer."),
   ("DOC036:T056","would quickly, you know, help you to see where vendors are, cause their bios. You also have their location. which number to call which products they have."),
   ("DOC036:T056","That is very, very helpful information."),
   ("DOC036:T056","And for someone like me, who is probably in a place for a very short time, right?")],"explicit"),
 ("C054","I would not really say I choose Instagram over something else; I use it just out of convenience",
  [("DOC036:T056","It's just out of convenience that I I use it.")],"explicit"),
 ("C055","Get the phone number from the bio, then WhatsApp/direct call to ask the cost of the product",
  [("DOC036:T058","once I see your bio information, I get your phone number."),
   ("DOC036:T058","I would say, I saw this product and this product can I know the cost of it?")],"explicit"),
 ("C056","They should put the price of products on the business pages (they currently only show the products, not prices)",
  [("DOC036:T058","they should put on the website on. I'm sorry on the pages, the business."),
   ("DOC036:T058","They don't put the price of the products.")],"explicit"),
 ("C057","But if they did, people might not ask about the products, so vendors wouldn't get the pricing feedback they need",
  [("DOC036:T058","But I I would imagine that if they did that, then maybe people would not ask about the products, and so they will not get the feedback they need on pricing.")],"explicit"),
 ("C058","After learning the price, ask for the payment number, make the payment, confirm the delivery address, then wait",
  [("DOC036:T058","I would go ahead to ask for the phone number I can use for the payment."),
   ("DOC036:T058","I would confirm my address where the whatever I'm buying, you know, should be delivered to.")],"explicit"),
 ("C059","When the product comes / is about to be dispatched, they call me to say they're about to reach / at my home and I should pick it up",
  [("DOC036:T058","They'll give me a phone call."),
   ("DOC036:T058","I should come pick it up")],"explicit"),
 ("C060","Interviewer summary: travel a lot, shop locally for specific items, IG finds stores in immediate location, search by occasion, platform accounts for selling",
  [("DOC036:T059","So it sounds like you travel around a lot."),
   ("DOC036:T059","you are also able to sell things on Instagram.")],"explicit"),
 ("C061","Interviewer summary: social interactions influence/inspire purchases; a ranking/like system signals reputable/safe; browsing platform",
  [("DOC036:T061","It provides social media interactions which also feed into help, influence and inspire some of your purchases"),
   ("DOC036:T061","as well as providing some type of ranking system for the some of the things that you're looking at you.")],"explicit"),
 ("C062","Correction: the 'ranking' feature doesn't really run",
  [("DOC036:T062","the the feature for the ranking. It's really it it doesn't. It doesn't really run.")],"explicit"),
 ("C063","For a reputable business, older products should have more likes/engagement than newly uploaded ones; uniform engagement across all products is fishy (malicious account baiting people to pay)",
  [("DOC036:T062","the amount of likes you would have if you are actually a reputable business is going to be reasonable, right?"),
   ("DOC036:T062","The the products you uploaded 6 months ago would probably have more likes and more engagement than the 2 products you just uploaded today."),
   ("DOC036:T062","It. It is fishy. It looks like it's a malicious site or a malicious account")],"explicit"),
 ("C064","This (social engineering) helps me know which accounts are good to buy from and which not; it saved me money with one account",
  [("DOC036:T062","It just helps me to know which accounts are probably good and which ones are not good I should buy from, and I should not buy from."),
   ("DOC036:T062","And it saved me some money actually with, there was one account.")],"explicit"),
 ("C065","Yeah, definitely. (confirm people can endorse/like a product to say it's good)",
  [("DOC036:T064","Yeah, definitely.")],"explicit"),
 ("C066","It's a pizza. (unclear transcription)",
  [("DOC036:T066","It's a pizza.")],"unknown"),
 ("C067","Confirm frustration with being made to sign in",
  [("DOC036:T069","On the counterpoint. It sounds like some things that you are frustrated with are the ability to that makes you sign in."),
   ("DOC036:T070","Yeah, it's.")],"explicit"),
 ("C068","Interviewer proposes feature request: anonymous browsing or anonymous posting; notes malicious accounts",
  [("DOC036:T071","being able to do anonymous browsing or anonymous posting.")],"explicit"),
 ("C069","Yeah. Yes. (general confirmation of interviewer's feature-request summary)",
  [("DOC036:T072","Yeah. Yes.")],"explicit"),
 ("C070","I think you did ... you covered everything (confirm interviewer's recap)",
  [("DOC036:T074","I think you did. It was a good interview, and you did a great job. I think you covered everything.")],"explicit"),
]

raw_candidates = []
for cid, stmt, quotes, origin in RAW:
    raw_candidates.append({
        'candidate_id': cid, 'statement': stmt, 'actor': 'Stakeholder',
        'modality': 'unknown', 'context': [], 'origin': origin, 'pass_id': 'P1',
        'evidence': evs(quotes),
    })

# ---------------- goals ----------------
def G(gid, stmt, quotes, context, origin, label, rationale, inference=None,
      supported_parts=None, unsupported_parts=None, assumptions=None, reasoning_steps=None):
    return {
        'candidate_id': gid, 'statement': stmt, 'actor': 'Stakeholder',
        'context': context, 'origin': origin, 'inference': inference,
        'evidence': evs(quotes),
        'judgment': {
            'label': label, 'rationale': rationale,
            'supported_parts': supported_parts or [],
            'unsupported_parts': unsupported_parts or [],
            'assumptions': assumptions or [],
            'reasoning_steps': reasoning_steps or [],
        },
    }

goals = [
 G('G001',
   "Buy a specific planned gift (e.g. a really good cake for my girlfriend) on Instagram, mainly on special occasions such as Valentine's Day",
   [("DOC036:T010","So I use Instagram mainly to shop on days like Valentine's Day, for example."),
    ("DOC036:T010","So I would go on Instagram to get my my girlfriend, maybe a cake from a really good spot")],
   ["主要在情人节等特殊场合购物（mainly / for example）","女友很喜欢吃蛋糕，因此专门找蛋糕账号"],
   'explicit','direct',
   "T010 涉众明确说明主要在情人节等特殊场合用 Instagram 购物，并给女友买蛋糕等特定礼物；主体（涉众）、对象（蛋糕/礼物）、情境（特殊场合）与强度（mainly）一致。C002 找蛋糕账号下单与之同义，合并承接，不另建重复节点。"),
 G('G002',
   "Find what I'm looking for (e.g. cakes / cake vendors) using the search bar, entering the name of what I want and adding the location if I don't see it immediately",
   [("DOC036:T012","and there you can now enter the name of of what you want to look for. So in my case, I would be like cakes."),
    ("DOC036:T012","and if I don't see immediately what I'm looking for, I'll just add maybe the name of the location.")],
   ["若未立即看到想要的，就加地点名（如 'cakes in Rwanda'、'cake sellers in ...'）再搜"],
   'explicit','direct',
   "T012 涉众描述用右上方搜索栏输入想找的名称（cakes），并在找不到时加地点名再搜；这是同一查找动作的核心动作加局部条件，按'一个动作的多个限定'保留为一个目标，不机械拆成两项。搜索会返回所在地区供应商（C008）为系统现状/正面评价，作为背景而非独立要求。"),
 G('G003',
   "Get the vendor's phone number / contact info from its account bio and reach out by WhatsApp or a normal call to place the order",
   [("DOC036:T010","because then I would go and see the the contact of the shop, and then I would use that now to reach out to them"),
    ("DOC036:T016","And then in the account, bio, that that is where I would see, like, maybe their phone number and their and and their contact information.")],
   ["若是商业账户即可联系；商家会告知可用 WhatsApp 还是普通电话","也可用站内 Instagram chat（涉众较少用，见 G004 偏好）"],
   'explicit','direct',
   "T010 与 T016 明确描述从账户 bio 看电话/联系方式，再通过电话或 WhatsApp 联系下单，是涉众 'the main way in which I purchase stuff on Instagram' 的独立动作；主体、对象、方式一致。"),
 G('G004',
   "Prefer to reach out to the number the vendor specified rather than via in-app Instagram chat, because communication is quicker",
   [("DOC036:T016","I would. I would always prefer to, you know, reach out to the number they've specified, because that way the communication is quicker.")],
   ["强度：always prefer（明确偏好，不升级为强制 must）","理由：沟通更快，且 'I don't expect them to always be online'"],
   'explicit','direct',
   "T016 'I would always prefer to ... reach out to the number they've specified' 是明确表达的偏好，对象（商家指定号码）、方向（相对站内 chat）、理由（更快）齐全。按目标边界保留 prefer 强度，不升级为强制，也不把偏好变成全体默认。"),
 G('G005',
   "For clothing/dresses, view a vendor's showcased designs on their account, then go to an actual market and ask for those same designs",
   [("DOC036:T010","I would I could go to an account of a vendor who, you know, is who is showcasing this plot, and, you know, see the designs they have in store."),
    ("DOC036:T010","I'll go to an actual market and ask for those.")],
   ["这是涉众所述两种主要用例之一","原文 'purchase address' / 'showcasing this plot' 为口语转写，语义指服装/设计，识别风险记入 limitations"],
   'explicit','direct',
   "T010 明确说明看商家展示的设计（see the designs they have in store）后去实体市场求购同款（go to an actual market and ask for those），是独立用例。个别触发词为转写噪声，但核心语义由上述两句支撑；不静默改写原文，识别风险另记 limitations 与问题。"),
 G('G006',
   "Browse images and products with an open mind (no particular product in mind) and pick something unplanned, choosing in the moment",
   [("DOC036:T022","I think there are some times when I go with a very open mind. I don't have a particular product in mind."),
    ("DOC036:T022","and I might end up picking something that you know I not imagine I'll pick")],
   ["与'先有明确计划再购买'相对，提供选择灵活性","可看到单一商家多种不同花色的产品（涉众称 a really good thing，作为背景）"],
   'explicit','direct',
   "T022 涉众明确描述有时无特定商品、开放心态浏览大量图片/产品并挑到未预想的商品；C020/C022 的情境与价值并入本目标。状态/选择类意图按边界保留，不因缺动作句式删除。"),
 G('G007',
   "When in a new place, quickly find local vendors and see their location, phone number and products via their account bios",
   [("DOC036:T056","You don't really know, like the vendors there, you don't know what they have to offer."),
    ("DOC036:T056","would quickly, you know, help you to see where vendors are, cause their bios. You also have their location. which number to call which products they have."),
    ("DOC036:T056","That is very, very helpful information."),
    ("DOC036:T056","And for someone like me, who is probably in a place for a very short time, right?")],
   ["涉众经常跨国搬迁、在每个地方停留时间短","涉众明确说 'I would not really say I choose it ... It's just out of convenience'，故本目标为依据使用动机的推断，非明确需求句式"],
   'inferred','inferred',
   "T056 是对'使用 Instagram 的初始动机'的回答：到新地方不认识供应商，IG 通过商家 bio 快速给出位置/电话/产品，且对短暂停留者 'very, very helpful'。由此正面推断涉众希望在新地方快速找到本地供应商信息；'just out of convenience' 仅说明非主动挑选平台，不否定该查找目的。origin 与 label 同为 inferred，理由与假设已写明。",
   inference={'basis_candidate_ids':['G002'],
              'reason':"由 T056 的使用动机/价值（不认识当地供应商、bio 快速提供位置电话产品、对短暂停留者很有帮助）推断涉众想达成'快速找到本地供应商信息'这一结果；G002 用搜索栏查找是同一查找意图在目标集合中的来路。",
              'assumptions':["涉众把'快速看到当地供应商信息'视为自己使用 Instagram 想要达成的结果","'just out of convenience' 仅说明非主动选择平台，不否定上述查找目的"]}),
 G('G008',
   "Be able to use / view the app (including just viewing a vendor's profile) without signing in, and browse without anyone knowing I'm online",
   [("DOC036:T024","so I would have loved to use the application without signing in right, but I but each time I have to use it I have to sign it."),
    ("DOC036:T024","Sometimes I don't want someone to know online. I just want to go and search for what I'm searching for. I get it. And I'm and I'm out of it right?"),
    ("DOC036:T052","I have to log in before I can view or do anything with the app. I wish it was not the case"),
    ("DOC036:T052","even if it's to view the profile of the vendor. it's a bit disturbing."),
    ("DOC036:T052","I would have hoped that. You know I could do things without needing to log in"),
    ("DOC036:T053","Another one sounds like you would really appreciate some type of anonymous browsing where you don't actually have to sign in. But you can still use the app."),
    ("DOC036:T054","Exactly. Yeah.")],
   ["强度：would have loved / wish / hoped（愿望、偏好，不升级为强制）","涉众称这是主要障碍（this is the main obstacle）；未登录连商家资料都看不了令人不快","有时不想让别人知道自己在线，只想快速搜索后退出","采访者归纳为 anonymous browsing，涉众 T054 'Exactly' 确认"],
   'explicit','direct',
   "T024 与 T052 多次明确表达'希望免登录即可使用/查看（含仅查看商家资料）'及'不想被人知道在线'，T053 采访者归纳为 anonymous browsing、T054 'Exactly. Yeah.' 确认。跨窗指代与确认已回查。不升级为强制；'anonymous posting'（T071）为采访者引入、涉众仅泛泛确认，未纳入本目标，另记问题。"),
 G('G009',
   "Limit my use of the app - log out, delete the app / web history, and access it only when I have a specific need",
   [("DOC036:T052","so that I don't use it very often."),
    ("DOC036:T052","I just I just kinda lock out myself and then delete the application on my phone."),
    ("DOC036:T052","and I only access it when I need something."),
    ("DOC036:T052","how I try to manage the use of the application."),
    ("DOC036:T032","So I try to stay away from it when I'm when I'm not having any use for it, and only use it when I have, you know, a need for it.")],
   ["维持/避免型：只在有需要时用、不常使用","方式：登出、删除手机应用或网页历史，使自己不容易访问","应对方式：情人节等特殊时期提前几天开始看并保持登录，过后登出（T052）"],
   'explicit','direct',
   "T052 'so that I don't use it very often' / 'only access it when I need something' / 'how I try to manage the use' 与 T032 'stay away ... only use it when I have a need' 为明确自我约束意图；登出/删除为明确选定方式，随目标保留。C042 同义并入，C051 应对方式并入 context，不另建重复节点。"),
 G('G010',
   "Avoid being unconsciously influenced by social/clothing content into buying things I did not plan",
   [("DOC036:T032","that is one of the reasons why I try to stay away from it a lot"),
    ("DOC036:T032","it could make me do unconsciously, unconsciously."),
    ("DOC036:T032","I don't know the other things that it could affect me.")],
   ["涉众称看到别人穿着好看会'促成购买'（an enabler in you purchasing particular product），并据此尽量远离","涉众明确表示不确定内容还可能影响自己什么（I don't know the other things）","强度：try to stay away（自我约束倾向，非绝对禁止）"],
   'explicit','direct',
   "T032 'that is one of the reasons why I try to stay away from it a lot' 明确把避免无意识影响作为远离的动机，是 avoid 型目标。其中'影响'属涉众顾虑/信念，不当已验证事实；影响范围自述不确定（I don't know ...），写入 context 并另记问题。与 G009（限制使用频率）为不同结果、各自有独立依据，故拆分而非合并。"),
 G('G011',
   "Avoid losing money to malicious vendor accounts that ask for payment upfront and never deliver the product",
   [("DOC036:T014","they will tell you to send the money. and when you send that money you will not get the product delivered to you right"),
    ("DOC036:T014","and you've lost the money, and there is no way you can track who has this account"),
    ("DOC036:T062","And it saved me some money actually with, there was one account.")],
   ["涉众曾遇到恶意账户（卖花和蛋糕的账户），但自己没有损失","恶意账户要求先付款、不发货、且无法追查账户持有者"],
   'explicit','direct',
   "T014 描述恶意账户'先收款、不发货、丢钱、无法追查'的具体损失情境，涉众以 'I didn't lose my money' 及 T062 'it saved me some money' 表明主动避免该结果，是明确 avoid 目标。抱怨/单次经历不自动推广为全部账户都恶意。"),
 G('G012',
   "Ensure the product is delivered before I pay the vendor (to avoid being scammed)",
   [("DOC036:T014","I didn't lose my money, because maybe I was very wise to understand that. You know you have to deliver before I pay you.")],
   ["涉众明确选定的付款规则（you have to deliver before I pay you）","因此涉众在那次恶意账户事件中未损失钱"],
   'explicit','direct',
   "T014 'you have to deliver before I pay you' 是涉众明确选定的、带 have to 强度的付款规则，且'没丢钱'被归因于它。它是 G011 的实现方式，但有独立结果意图与明确强度，按'一目标一核心动作'单独保留为方式目标，用于承接选定方式，不藏在解释里。"),
 G('G013',
   "Use a vendor gallery's likes and comments (engagement) to judge whether the account is reputable or malicious - older products should have more engagement; uniform engagement across all products is suspicious",
   [("DOC036:T024","The good with the gallery is that when you go to the gallery you have people commenting, and you also have likes."),
    ("DOC036:T024","I that helped me to spot that you know."),
    ("DOC036:T024","But then, if you are seeing just one like and maybe 0 comments"),
    ("DOC036:T062","The the products you uploaded 6 months ago would probably have more likes and more engagement than the 2 products you just uploaded today."),
    ("DOC036:T062","It. It is fishy. It looks like it's a malicious site or a malicious account"),
    ("DOC036:T062","It just helps me to know which accounts are probably good and which ones are not good I should buy from, and I should not buy from.")],
   ["判断逻辑：老产品应比新上传产品有更多点赞/评论；若所有产品点赞/评论数相近则可疑（一次性上传后离开）","涉众称这只是 social engineering；T062 明确纠正：'排名'功能其实并未真正运行","这是涉众避免被骗的判断方式，saved me some money"],
   'explicit','direct',
   "T024 'helped me to spot ... malicious account' 与 T062 'It just helps me to know which accounts ... I should buy from' 明确说明画廊点赞/评论被用来判断账户可信/恶意；C029/C063/C064 的判断逻辑与用途并入。采访者 T061 所称 ranking system 被 T062 否定，本目标不据该总结建立。"),
 G('G014',
   "Keep my account private so that only very close friends can see my posts and see when I'm online",
   [("DOC036:T026","then I make sure I have a private account, because my account currently is private."),
    ("DOC036:T026","and if I'm online, I would expect that just my very close friends would see I'm online."),
    ("DOC036:T026","So only very close friends of me. You know I use friends to me, and I can see my post.")],
   ["账户目前已是私密（现状 + 维持意图 make sure / expect）","动机：避免公众看到自己发布的内容、避免被人盯上"],
   'explicit','direct',
   "T026 'I make sure I have a private account' 与 'I would expect that just my very close friends would see I'm online' 是对现有私密状态的明确维持意图（make sure / expect），按边界'已实现能力不自动成为要求，但有维持意图则为有效目标'保留。"),
 G('G015',
   "Be careful about posting about my life and my stuff on social media, and avoid people preying on my life",
   [("DOC036:T026","I tend to be careful with that aspect of you know, posting about your life and your stuff on social media."),
    ("DOC036:T026","So it kind of helps to weed away the the the evils of you know, people preying on your life and on social media and all of that stuff."),
    ("DOC036:T026","Because, it's it's just it could come back, you know, to hurt you or hunt you in the future.")],
   ["强度：tend to be careful（谨慎倾向，非绝对禁止）","动机含信念：相关内容将来可能反噬（could come back to hurt/hunt you），不当已验证事实"],
   'explicit','direct',
   "T026 'I tend to be careful with ... posting about your life' 与 'weed away the evils of ... people preying on your life' 是明确的谨慎/避免意图；'could come back to hurt you' 是涉众信念，作为动机保留、不当事实。C035 预期结果并入本目标；私密账户（G014）为其实现方式，单独建目标以便承接联系。"),
 G('G016',
   "Stay connected with people on Instagram so that if I lose their phone number / contact / email, I can still reconnect with them via the app",
   [("DOC036:T030","if any time in in this life. I lose your phone number or your immediate contact or your email address."),
    ("DOC036:T030","I can always, you know, reconnect with you by getting in touch with you, using using the application."),
    ("DOC036:T030","I would go to follow you on Instagram.")],
   ["涉众经常跨国搬迁、更换手机号（I keep changing my phone numbers）","通过关注/成为好友实现（it's like Facebook）"],
   'explicit','direct',
   "T030 明确说明关注对方后即使丢失电话/即时联系方式/邮箱，仍可通过 Instagram 重连，且因自己常换号'is a really good benefit for me'；主体、结果、情境一致。社交组件虽被采访者列为可单独成题，但涉众确实表达了该目标，故保留。"),
 G('G017',
   "Have vendors put the price of products on their business pages (so I would not need to ask for the cost)",
   [("DOC036:T058","they should put on the website on. I'm sorry on the pages, the business."),
    ("DOC036:T058","They don't put the price of the products."),
    ("DOC036:T058","But I I would imagine that if they did that, then maybe people would not ask about the products, and so they will not get the feedback they need on pricing.")],
   ["涉众随即自我让步：若标价，人们就不再询价、商家得不到所需定价反馈","该提议与让步形成混合冲突，支持不足，保留 insufficient 不升级"],
   'explicit','insufficient',
   "T058 涉众先说 'they should put ... the price'（提议页面标价），随即用 'But I I would imagine that if they did that ... they will not get the feedback they need on pricing' 给出相反理由（标价会减少询价、商家失去定价反馈）。同一条件下明确让步且无有效支持可裁决，按证据口径混合冲突无法决定时为 insufficient 并提出人工问题；不为凑数升级为 direct。",
   supported_parts=["涉众提及商家页面目前不标价格、自己需电话询价（现状/事实）"],
   unsupported_parts=["商家应标价这一要求是否被涉众最终认可（其后自我让步）","若认可，该要求针对商家还是平台、强度如何"],
   reasoning_steps=["T058 先以 'should put' 提议在商家页面标价","紧接 'But I would imagine that if they did that...' 给出反方后果（询价减少、商家失去定价反馈）","按 evidence-rules 混合冲突无法决定时为 insufficient 并提出人工问题"]),
]

# ---------------- review_questions ----------------
review_questions = [
 {"candidate_ids":["G017"],"question":"涉众是否最终希望商家在页面标注产品价格？","reason":"T058 先提议应标价，随即自我让步（标价会减少询价、商家失去定价反馈），混合冲突无法确定，judgment 如实保留 insufficient，不升级。"},
 {"candidate_ids":["G008"],"question":"采访者 T071 提到的 'anonymous posting'（匿名发帖）是否应作为独立目标？","reason":"涉众此前只表达匿名浏览/不被人知道在线（T024）且账户私密（T026），T072 仅泛泛 'Yeah. Yes.' 确认，无独立依据，未升级，保留待确认。"},
 {"candidate_ids":["G010"],"question":"社交/服装内容对涉众购买行为的无意识影响具体范围是什么？","reason":"涉众 T032 明确说 'I don't know the other things that it could affect me'，影响范围为自述不确定，信念不当事实。"},
 {"candidate_ids":["G005"],"question":"T010 'purchase address' / 'showcasing this plot' 是否为 'a dress' / 服装设计的转写误差？","reason":"原文为口语转写，个别词不清；核心语义由 'see the designs they have in store' 与 'go to an actual market and ask for those' 支撑，识别风险记入 limitations。"},
 {"candidate_ids":["G007"],"question":"G007 为依据使用动机的推断目标，是否应保留？","reason":"T056 涉众强调 'I would not really say I choose it ... just out of convenience'，故标 inferred 并写明假设；请人工确认该查找目的是否需保留为目标。"},
 {"candidate_ids":[],"question":"采访者 T061 所称 'ranking system / 声誉排名' 是否应提取为目标？","reason":"涉众 T062 明确纠正 'It doesn't really run'，故不据采访者总结提取，作为整体问题保留。"},
 {"candidate_ids":[],"question":"T034 'addictive and very time consuming' 是否隐含'避免沉迷/减少耗时'的避免目标？","reason":"仅为对现有功能的抱怨/观察，涉众未明确表达改进或避免意图；按目标边界抱怨不自动证明障碍，未提取目标。"},
 {"candidate_ids":[],"question":"T014 'you need to still get in touch with the vendor' 是否意味着涉众希望改为直接下单？","reason":"涉众同句称该方式 'definitely good that way'，为相反证据；未提取'去掉手动联系'目标。"},
]

limitations = [
 "本次仅读取任务目录 source/DOC036.json（77 轮）与冻结技能只读目录；未联网、未读取参考答案/其他 attempt/数据集/全过程记录。",
 "原文为英文口语访谈转写，含大量不完整句、重复、犹豫与转写噪声（如 T010 'purchase address'、T047 '30Â min'、T066 'It's a pizza.'）；个别词不清处按上下文判断，保留识别风险，不静默润色原文。",
 "采访者多处总结（T059/T061/T069/T071）由涉众以 'Yeah'/'Exactly'/'Yeah. Yes.'/'covered everything' 泛泛确认，未逐项重新陈述；其中 'ranking system' 被 T062 明确否定，已据此校正，不逐项升级为涉众目标。",
 "全篇校正与关系/精化组判断均为同一生成会话的编制判断（生成方自检），非独立语义评审；独立语义审查 not_run、形式证明 not_run、人工接受 pending。",
 "ledger 的 model / temperature / usage 不可获得，如实记 unknown。",
]

# ---------------- ledger ----------------
ENTRIES = {
 'C001':('keep',['G001'],"整理为 G001：明确说明主要在特殊场合用 IG 购物买特定礼物；保留 mainly / for example 情境与蛋糕例子。"),
 'C002':('merge',['G001'],"与 C001 同义（都是为女友买好蛋糕），合并；'找蛋糕账号'作为方式并入 G001 语境，不另建重复节点。"),
 'C003':('keep',['G003'],"独立动作：看店铺联系方式并电话/WhatsApp 联系下单，有独立意图依据，整理为 G003。"),
 'C004':('keep',['G005'],"独立用例：看服装设计后到实体市场求购同款，整理为 G005；保留转写噪声说明。"),
 'C005':('exclude',[],"现状背景：卢旺达商家在 Instagram 开商业账户展示商品（cakes to dresses），非涉众意图。"),
 'C006':('exclude',[],"涉众对两种主要用例的元总结，非独立目标；已由 G001/G005 承接。"),
 'C007':('keep',['G002'],"用搜索栏输入名称查找想要的，整理为 G002 核心动作。"),
 'C008':('exclude',[],"对现有能力（搜索按地区返回供应商）的正面评价 'I found that really useful'，按边界已实现能力不自动成为要求；仅作 G002 背景，不单独建目标。"),
 'C009':('merge',['G002'],"找不到时加地点名再搜，是 G002 搜索动作的局部条件/选定方式，随 G002 保留。"),
 'C010':('exclude',[],"现状：搜索结果显示供应商账户而非商品（T014），非涉众意图。"),
 'C011':('exclude',[],"现状流程：看到商品后仍需联系商家才能发货（对比 Amazon），非改善要求；涉众 T014 反称该方式 'definitely good'（见相反证据登记）。"),
 'C012':('exclude',[],"涉众评价'必须联系商家'在他那边 definitely good，是重要相反证据；不据此提取'去掉手动联系'目标，登记于 source_checks 与 questions。"),
 'C013':('keep',['G011'],"恶意账户先收款不发货、无法追查，是 G011 避免目标的障碍情境依据。"),
 'C014':('keep',['G012'],"'先交货再付款'是涉众明确选定的避免损失方式（have to），整理为独立方式目标 G012。"),
 'C015':('merge',['G003'],"从 bio 看电话/联系方式并联系，与 C003 同义，合并到 G003。"),
 'C016':('exclude',[],"现状评价：活跃账户响应快/低延迟，非目标。"),
 'C017':('exclude',[],"替代方式：站内 Instagram chat 可联系商家，涉众未选为主方式；作为 G004 中被比较的替代对象保留，不单独建目标。"),
 'C018':('keep',['G004'],"明确偏好（always prefer）拨打商家指定号码，整理为 G004；保留 prefer 强度不升级。"),
 'C019':('exclude',[],"涉众 T018 'Yeah, they are, yeah.' 对采访者'恶意账户是障碍'的简短确认，非独立意图；相关目标已由 G011 承接。"),
 'C020':('merge',['G006'],"开放心态、无特定商品，是 G006 的情境条件，并入。"),
 'C021':('keep',['G006'],"浏览大量图片/产品、可能挑到未预想商品，整理为 G006 核心动作。"),
 'C022':('merge',['G006'],"当场选择、灵活性是 G006 的预期结果/价值，并入 G006。"),
 'C023':('exclude',[],"对'看到单一商家多种产品'的正面评价 'a really good thing'，现状/偏好，不自动成为目标；G006 context 作为背景提及。"),
 'C024':('keep',['G008'],"明确愿望：免登录使用应用（would have loved / wish），整理为 G008。"),
 'C025':('merge',['G008'],"不想被人知道在线、快速搜索后退出，是 G008 匿名浏览的伴随意图，并入。"),
 'C026':('exclude',[],"现状功能：搜索结果保存在下拉、可复用过去供应商（a good feature），已实现能力不自动成为要求；'不必每次重搜'作为背景在 questions 说明，不建目标。"),
 'C027':('exclude',[],"现状浏览流程：页面含 bio/highlights/gallery，非目标。"),
 'C028':('exclude',[],"对画廊互动（点赞/评论显示有人使用/喜爱/推荐）的正面评价，现状；判断用途由 G013 承接。"),
 'C029':('merge',['G013'],"用点赞/评论识别恶意账户（老产品应有更多赞、全 1 赞 0 评论可疑），并入 G013 判断逻辑。"),
 'C030':('exclude',[],"看评论帮助决定给女友买什么，是画廊功能的用途/评价，现状，不单独建目标。"),
 'C031':('exclude',[],"现状：可按人名搜索找人，非本次购物意图目标。"),
 'C032':('exclude',[],"现状/价值：用 IG 与人连接、分享照片，社交组件背景；保持联系/重连由 G016 承接。"),
 'C033':('keep',['G015'],"谨慎发布个人生活（tend to be careful），整理为 G015；保留信念成分（可能反噬）于 context。"),
 'C034':('keep',['G014'],"维持私密账户（make sure / expect），整理为 G014。"),
 'C035':('merge',['G015'],"避免被人盯上/weed away the evils，是 G015 的预期结果，并入。"),
 'C036':('exclude',[],"对过度公开生活的负面评价（find it unnecessary），偏好/评价，不单独建目标。"),
 'C037':('exclude',[],"T028 'Yes, it does.' 确认有社交组件，简短确认，非目标。"),
 'C038':('merge',['G016'],"关注人以保持联系，是 G016 的实现方式，并入。"),
 'C039':('keep',['G016'],"丢失电话/邮箱后仍可通过应用重连，整理为 G016 核心结果。"),
 'C040':('exclude',[],"偏好/背景：喜欢穿得酷，非目标；与 G010 的服装影响相关，作背景。"),
 'C041':('exclude',[],"观察/信念：看到别人穿着好看会促成自己购买（enabler），现状观察非目标；G010 的动机背景，questions 保留。"),
 'C042':('split',['G009','G010'],"该复合候选含两个独立结果：远离/只在需要时用（→G009，与 C050 同义）与避免被社交/服装内容无意识影响（→G010，'that is one of the reasons ... it could make me do unconsciously'）；按一目标一核心动作拆分，分别核验。"),
 'C043':('exclude',[],"抱怨/观察：无限滚动与追动态让人上瘾、耗时，非明确改进或避免意图；按边界抱怨不自动证明障碍，questions 保留。"),
 'C044':('exclude',[],"现状功能：关注用户/群组/标签/名人及信息流，非目标。"),
 'C045':('exclude',[],"偏好/评价：觉得关注明星看人生建议 irrelevant，非目标。"),
 'C046':('exclude',[],"T038 'Yeah. And that's true.' 确认 follow → infinite scroll，简短确认，非目标。"),
 'C047':('exclude',[],"现状 + 信念：没用过 IG 群组，认为 Facebook 有群组所以 IG 必然也有（imperative）。信念不当事实，非目标。"),
 'C048':('exclude',[],"现状/限定：订阅标签≈群组、带标签帖子进 feed，且'和 Facebook 群组不一样'，非目标。"),
 'C049':('merge',['G008'],"再次明确愿望：免登录即可查看/使用（含查看商家资料），wish/hoped，与 C024 同义合并到 G008；这是主要障碍。"),
 'C050':('keep',['G009'],"明确维持/避免：登出、删应用/历史、只在需要时用（manage the use），整理为 G009 核心动作。"),
 'C051':('merge',['G009'],"情人节期间保持登录、过后登出的应对方式，并入 G009 的方式说明。"),
 'C052':('split',['G008','G009'],"采访者 T053 把诉求拆为两方面：匿名浏览（→G008）与限制使用（→G009），涉众 T054 'Exactly. Yeah.' 同时确认；按两方面分别映射，分别核验。"),
 'C053':('keep',['G007'],"使用动机/价值：到新地方通过 bio 快速看到供应商位置/电话/产品，整理为 G007（inferred）。"),
 'C054':('merge',['G007'],"'不是主动选择、只是图方便'的让步，并入 G007 的推断假设/context，不单独建目标。"),
 'C055':('exclude',[],"现状下单流程：从 bio 拿电话→电话/WhatsApp 询价，非目标；相关能力由 G003 承接。"),
 'C056':('uncertain',['G017'],"提议商家在页面标价（should put），是 G017 的来路；但伴随 C057 让步，支持不足，处置 uncertain 并映射到 insufficient 目标 G017。"),
 'C057':('merge',['G017'],"随即自我让步（标价会减少询价、商家失去定价反馈），是 G017 判 insufficient 的相反证据，并入。"),
 'C058':('exclude',[],"现状下单流程：询价→要支付号码→付款→确认地址→等待，非目标。"),
 'C059':('exclude',[],"现状交付流程：到货/发货前商家来电、到 home 取货，非目标。"),
 'C060':('exclude',[],"采访者 T059 总结（旅行/本地购物/搜索/可卖东西的平台账户），仅经涉众泛泛确认，不逐项升级为涉众目标；相关点已由 G001/G002/G007 等承接。"),
 'C061':('exclude',[],"采访者 T061 总结（社交影响购买、ranking/点赞系统、浏览平台）；其中 'ranking system' 被 T062 明确否定（见校正），不据总结提取目标。"),
 'C062':('exclude',[],"重要相反证据：涉众 T062 纠正 'the ranking ... doesn't really run'；登记于 source_checks 与 questions，不建'排名系统'目标。"),
 'C063':('merge',['G013'],"信誉商家老产品应有更多点赞/互动、全店互动量相近则可疑，是 G013 的判断逻辑，并入。"),
 'C064':('merge',['G013'],"判断账户帮助决定该从哪家买/不该买、并省过钱，是 G013 的用途/结果，并入（同时支撑 R2 贡献关系）。"),
 'C065':('exclude',[],"T064 'Yeah, definitely.' 确认点赞/背书，简短确认，非目标。"),
 'C066':('exclude',[],"T066 'It's a pizza.' 为转写噪声，无法判断语义，不提取；记入 limitations。"),
 'C067':('exclude',[],"T069/T070 确认对必须登录的不满，简短确认，已由 G008 承接。"),
 'C068':('exclude',[],"采访者 T071 提出 feature request（anonymous browsing or anonymous posting）及恶意账户，涉众未逐项重新陈述；'anonymous posting' 无依据不升级（见 questions）。"),
 'C069':('exclude',[],"T072 'Yeah. Yes.' 对采访者 feature-request 总结的泛泛确认，非独立目标。"),
 'C070':('exclude',[],"T074 确认采访者 'covered everything'，元确认，非目标。"),
}

windows = ["DOC036:W%04d" % i for i in range(1, 39)]

ledger = {
 'model':'unknown','temperature':'unknown','budget':'1 initial pass + <=2 repair rounds (within attempt-02)',
 'usage':'unknown','skill_revision':SHA,'prompt_revision':'task-prompt-v1',
 'planned_passes':1,
 'stop_reason':"已完成全部 38 窗口逐窗捕获、全篇指代/条件/让步/相反证据校正、最终目标整理，以及四类独立联系与 AND 精化组的逐条判断（含'已检查但无依据'记录）；无新增有据候选或可解决的新证据，停止该循环。",
 'passes':[{
   'pass_id':'P1','kind':'initial','context':'isolated','status':'completed',
   'window_results':[{'window_id':w,'status':'processed','reason':''} for w in windows],
 }],
 'full_context_review':{
   'status':'completed',
   'reason':"回查全部 77 轮源片段：核对跨窗指代（T026 'it' 指私密账户安排、T024 'the other account' 指 T014 恶意账户、T062 纠正 T061 的 ranking system）、问答范围（采访者 T011/T019/T053/T071 的总结与涉众 T054/T072/T074 的泛泛确认）、条件继承（T012 加地点名的局部条件、T052 情人节应对方式）、让步与例外（T058 标价提议后的自我让步、T014 'definitely good that way' 相反证据、T044 'not the same thing'）、以及被排除项与不确定项；跨窗证据可引用多个窗口，补查未新增候选，故不另起 P2。",
 },
 'entries':[{'candidate_id':cid,'disposition':d,'final_goal_ids':g,'reason':r}
            for cid,(d,g,r) in ENTRIES.items()],
 'source_checks':[],
}

def chk(cid, quotes, cands, gids, outcome, reason):
    ledger['source_checks'].append({
        'check_id':cid,
        'evidence_candidates':evs(quotes),
        'candidate_ids':cands,'final_goal_ids':gids,
        'outcome':outcome,'reason':reason,
    })

chk('S1',[("DOC036:T010","So I use Instagram mainly to shop on days like Valentine's Day, for example."),
          ("DOC036:T010","because then I would go and see the the contact of the shop, and then I would use that now to reach out to them"),
          ("DOC036:T010","I'll go to an actual market and ask for those.")],
    ['C001','C002','C003','C004'],['G001','G003','G005'],'represented',
    "T010 超长复合段拆分：特殊场合买礼物→G001（C002 同义并入）、看联系方式联系下单→G003、服装设计去市场→G005；C005 现状、C006 元总结排除。")
chk('S2',[("DOC036:T012","and there you can now enter the name of of what you want to look for. So in my case, I would be like cakes."),
          ("DOC036:T012","and if I don't see immediately what I'm looking for, I'll just add maybe the name of the location.")],
    ['C007','C009'],['G002'],'represented',
    "搜索栏输入名称→G002 核心动作，加地点名为局部条件并入；C008 按地区返回供应商为现状/正面评价，排除，仅作背景。")
chk('S3',[("DOC036:T014","they will tell you to send the money. and when you send that money you will not get the product delivered to you right"),
          ("DOC036:T014","I didn't lose my money, because maybe I was very wise to understand that. You know you have to deliver before I pay you.")],
    ['C013','C014'],['G011','G012'],'represented',
    "恶意账户损失情境→G011，先交货再付款→G012；两者分别核验，不把复合候选的一次判断复制给全部拆分项。")
chk('S4',[("DOC036:T016","I would. I would always prefer to, you know, reach out to the number they've specified, because that way the communication is quicker.")],
    ['C018'],['G004'],'represented',
    "always prefer 拨指定号码→G004（保留偏好强度）；站内 chat 为被比较的替代方式，排除。")
chk('S5',[("DOC036:T022","I think there are some times when I go with a very open mind. I don't have a particular product in mind."),
          ("DOC036:T022","and I might end up picking something that you know I not imagine I'll pick")],
    ['C020','C021','C022'],['G006'],'represented',
    "开放心态浏览/当场挑选→G006；灵活性价值并入、单一商家多花色为正面评价排除（作背景）。")
chk('S6',[("DOC036:T024","so I would have loved to use the application without signing in right, but I but each time I have to use it I have to sign it."),
          ("DOC036:T024","I that helped me to spot that you know."),
          ("DOC036:T024","It's gonna save my search results right in a dropdown.")],
    ['C024','C025','C029'],['G008','G013'],'represented',
    "免登录/不被人知道在线→G008；画廊互动识别恶意账户→G013（C029/C063/C064 并入）；下拉保存、bio/highlights、看评论选礼物等为现状/评价，排除。")
chk('S7',[("DOC036:T026","then I make sure I have a private account, because my account currently is private."),
          ("DOC036:T026","I tend to be careful with that aspect of you know, posting about your life and your stuff on social media."),
          ("DOC036:T026","So it kind of helps to weed away the the the evils of you know, people preying on your life and on social media and all of that stuff.")],
    ['C033','C034','C035'],['G014','G015'],'represented',
    "私密账户维持→G014、谨慎发布/避免被盯上→G015；'it' 经回查指私密账户安排，是 R3 关系依据；过度公开的评价排除。")
chk('S8',[("DOC036:T030","if any time in in this life. I lose your phone number or your immediate contact or your email address."),
          ("DOC036:T030","I can always, you know, reconnect with you by getting in touch with you, using using the application.")],
    ['C038','C039'],['G016'],'represented',
    "丢失联系方式后仍可经应用重连→G016；关注为并入的实现方式。")
chk('S9',[("DOC036:T032","that is one of the reasons why I try to stay away from it a lot"),
          ("DOC036:T032","I would say an enabler in you purchasing particular product. whether you, whether it is consciously or unconsciously, it has that effect.")],
    ['C042'],['G009','G010'],'represented',
    "避免无意识影响→G010、远离/只在需要时用→G009（C042 并入）；'促成购买'为观察/信念排除，影响范围不确定记入问题。")
chk('S10',[("DOC036:T034","those things make it kind of addictive and very time consuming.")],
    ['C043'],[],'excluded',
    "无限滚动/追动态'上瘾耗时'为抱怨/观察，非明确改进或避免意图；按边界抱怨不自动证明障碍，是否隐含避免目标记入 questions。")
chk('S11',[("DOC036:T044","I haven't really used groups."),
           ("DOC036:T044","But it's not the same way.")],
    ['C047','C048'],[],'excluded',
    "没用过 IG 群组、'imperative that they brought those features' 为信念，不当事实；标签订阅≈群组且'和 Facebook 不一样'为现状/限定，均非目标。")
chk('S12',[("DOC036:T052","I have to log in before I can view or do anything with the app. I wish it was not the case"),
           ("DOC036:T052","and I only access it when I need something."),
           ("DOC036:T053","Another one sounds like you would really appreciate some type of anonymous browsing where you don't actually have to sign in. But you can still use the app."),
           ("DOC036:T054","Exactly. Yeah.")],
    ['C049','C050','C051','C052'],['G008','G009'],'represented',
    "免登录愿望再次确认→G008（C024 同义合并）、限制使用→G009；T053/T054 把两方面拆开并确认，C052 按 split 映射 G008+G009；应对方式并入 G009。")
chk('S13',[("DOC036:T056","would quickly, you know, help you to see where vendors are, cause their bios. You also have their location. which number to call which products they have."),
           ("DOC036:T056","It's just out of convenience that I I use it.")],
    ['C053','C054'],['G007'],'represented',
    "到新地方快速找本地供应商信息→G007（依使用动机推断，inferred）；'just out of convenience' 让步并入推断假设，不单独建目标。")
chk('S14',[("DOC036:T058","they should put on the website on. I'm sorry on the pages, the business."),
           ("DOC036:T058","But I I would imagine that if they did that, then maybe people would not ask about the products, and so they will not get the feedback they need on pricing.")],
    ['C056','C057'],['G017'],'uncertain',
    "标价提议与紧随的自我让步形成混合冲突，无法裁决；G017 判 insufficient，处置 uncertain，写入 review_questions。")
chk('S15',[("DOC036:T061","as well as providing some type of ranking system for the some of the things that you're looking at you."),
           ("DOC036:T062","the the feature for the ranking. It's really it it doesn't. It doesn't really run.")],
    ['C060','C061','C062'],[],'excluded',
    "采访者总结的 'ranking system' 被涉众 T062 明确否定；不据采访者总结提取'排名/声誉系统'目标，也不据此建立联系。采访者总结仅经泛泛确认，不逐项升级。")
chk('S16',[("DOC036:T071","being able to do anonymous browsing or anonymous posting."),
           ("DOC036:T072","Yeah. Yes.")],
    ['C068','C069'],[],'uncertain',
    "'anonymous posting' 为采访者引入、涉众仅泛泛确认，此前只表达匿名浏览/不被人知道在线；无独立依据不升级，保留不确定并写入 questions。")
chk('S17',[("DOC036:T014","I'm sure it's definitely good that way, especially like my side of the world"),
           ("DOC036:T015","you yourself have to manually contact this vendor.")],
    ['C011','C012'],[],'excluded',
    "重要相反证据：采访者把'必须手动联系商家'归为障碍，但涉众称该方式 'definitely good that way'；不提取'去掉手动联系/像 Amazon 直接下单'的改善目标。")
chk('S18',[("DOC036:T066","It's a pizza.")],
    ['C066'],[],'excluded',
    "T066 'It's a pizza.' 为转写噪声，语义无法判断，不提取目标；记入 limitations。")

# ---------------- decisions ----------------
relations = [
 {'relation_id':'R1','source_id':'G012','target_id':'G011','type':'operationalization',
  'status':'supported','conditions':["在 Instagram 购物、需向商家付款的情境下"],'assumptions':[],
  'rationale':"T014 涉众明确把'没丢钱'归因于坚持先交货再付款（'I didn't lose my money, because ... you have to deliver before I pay you'）；G012 是 G011（避免被恶意账户骗钱）的选定实现方式。仅为方式→目的，不声称该方式单独充分，也不把操作先后当精化。两端目标均为 direct。",
  'evidence_ids':[],
  'evidence_quotes':evs([("DOC036:T014","I didn't lose my money, because maybe I was very wise to understand that. You know you have to deliver before I pay you.")])},
 {'relation_id':'R2','source_id':'G013','target_id':'G011','type':'contribution',
  'status':'supported','conditions':["通过商家画廊的点赞/评论可判断账户可信时"],'assumptions':[],
  'rationale':"T062 'It just helps me to know which accounts ... I should buy from, and I should not buy from' 且 'it saved me some money actually'，T024 也说画廊互动 'helped me to spot ... malicious account'；G013 对 G011（避免被恶意账户骗钱）有帮助但未证明充分，按 contribution 而非精化。两端目标均为 direct。",
  'evidence_ids':[],
  'evidence_quotes':evs([("DOC036:T062","It just helps me to know which accounts are probably good and which ones are not good I should buy from, and I should not buy from."),
                         ("DOC036:T062","And it saved me some money actually with, there was one account.")])},
 {'relation_id':'R3','source_id':'G014','target_id':'G015','type':'operationalization',
  'status':'supported','conditions':["在自己的账户上发布内容/在线状态的情境下"],'assumptions':[],
  'rationale':"T026 'So it kind of helps to weed away ... people preying on your life' 中的 'it' 经全篇回查指代前文的私密账户安排（make sure I have a private account / only very close friends see my posts and online status）；G014 是 G015（谨慎发布、避免被人盯上）的选定方式。仅为方式→目的，不声称单独充分。两端目标均为 direct。",
  'evidence_ids':[],
  'evidence_quotes':evs([("DOC036:T026","So it kind of helps to weed away the the the evils of you know, people preying on your life and on social media and all of that stuff.")])},
]

questions = [
 {'target_type':'model','target_id':'DOC036-goal-model','message':"【specialization 已检查但无依据】逐窗核对全部目标对，未提取出成对的'一般目标 / 具体情境目标'关系：G001/G005/G006 为并列的不同购物用例而非一般-具体；G007 为新地方情境但无对应一般父目标。不为凑层级造泛化根，故不建 specialization 联系。"},
 {'target_type':'model','target_id':'DOC036-goal-model','message':"【operationalization 已检查但无依据】除 R1(G012→G011)、R3(G014→G015) 外，其余'方式→目的'候选（T012 找不到时加地点名再搜、T052 情人节期间保持登录、T058 电话询价等）均为同一目标内的操作步骤或现有流程，未形成独立目标端点；按联系发现规则不把操作先后/步骤当联系，故不建。"},
 {'target_type':'model','target_id':'DOC036-goal-model','message':"【contribution 已检查但无依据】除 R2(G013→G011) 外，'搜索结果下拉可复用过去供应商'、'搜索按地区返回供应商'、'社交内容促成购买(T032)' 等均为现状能力/正面评价或观察，缺独立目标端点或仅同主题相关；相关/相似不构成贡献联系，故不建。"},
 {'target_type':'model','target_id':'DOC036-goal-model','message':"【precedes 已检查但无依据】回查 T010/T024/T058 的流程顺序（搜索→看联系方式→联系→询价→付款→确认地址→等待→取货），'then/once' 均为涉众现有操作流程的步骤顺序，不是两个目标结果之间的先后声明；按规则不将操作先后当作 precedes 联系，故不建。"},
 {'target_type':'model','target_id':'DOC036-goal-model','message':"【AND 精化组 已检查但无依据】检查 G011 是否由 {G012 先交货再付款, G013 画廊判断} 共同满足足以实现：两者是避免被骗的两种方式/帮助，原文未声称二者共同充分（仍有其他诈骗手法与其他判断方式），不能声称'共同满足足以实现父目标'；故不建 supported+complete 组，也不为凑边扩写目标。"},
 {'target_type':'model','target_id':'DOC036-goal-model','message':"【AND 精化组 已检查但无依据】检查 G015 是否由 {G014 私密账户} 或其他组合精化：单子目标不构成 AND 组，且原文无共同充分性声明；G008/G009/G010 等为独立愿望/维持目标，彼此无'共同满足足以实现'的父子关系；故不建组。"},
 {'target_type':'model','target_id':'DOC036-goal-model','message':"【AND 精化组 场景检查 已检查但无依据】supported+complete 组需至少一条 normal 与一条 exception 场景、全部 outcome=supports、所有端点支持有效、所有依赖联系 supported；原文仅提供单次事件（T014 恶意账户一次经历、T062 省过一次钱），不足以证明任一组的共同充分性。无任何成立组，groups 为空是判断结果而非跳过判断。"},
 {'target_type':'goal','target_id':'G017','message':"【待确认】G017（商家页面应标价）为 insufficient：T058 涉众先提议 'should put'，随即自我让步'若标价则人们不再询价、商家失去定价反馈'。请人工判断涉众最终是否希望标价，以及该要求针对商家还是平台。"},
 {'target_type':'model','target_id':'DOC036-goal-model','message':"【相反证据/校正 已检查】采访者 T061 总结的 'ranking / 排名系统' 被涉众 T062 明确纠正为 'It doesn't really run'；不据采访者总结提取'排名/声誉系统'目标，也不据此建立联系。采访者 T059/T061 总结仅经涉众泛泛确认（T072/T074），不逐项升级为涉众目标。"},
 {'target_type':'model','target_id':'DOC036-goal-model','message':"【范围不确定 已检查】T071 采访者提出 'anonymous browsing or anonymous posting'，涉众 T072 仅泛泛 'Yeah. Yes.'；涉众此前只表达匿名浏览/不被人知道在线（T024）且账户私密（T026），未表达匿名发帖。'匿名发帖'无独立依据，不升级为目标；保留不确定。"},
 {'target_type':'model','target_id':'DOC036-goal-model','message':"【相反证据 已检查】T014 涉众称'必须联系商家'这种方式 'I'm sure it's definitely good that way, especially like my side of the world'，未要求改为像 Amazon 那样直接刷卡下单；不提取'去掉手动联系/直接下单'的改善目标。"},
 {'target_type':'model','target_id':'DOC036-goal-model','message':"【排除项 已检查】T034 无限滚动/追动态 'addictive and very time consuming'、T036 关注名人 'irrelevant'、T044 群组/标签 'not the same thing' 等为抱怨、偏好评价或现状描述，按目标边界不自动成为要求或障碍，未提取目标；其可能关联的'避免耗时/避免沉迷'仅作问题保留，无明确意图依据不建节点。"},
]

decisions = {'relations':relations,'groups':[],'questions':questions,'reassessments':[]}

spec = {
 'document_id':'DOC036',
 'raw_candidates':raw_candidates,
 'goals':goals,
 'review_questions':review_questions,
 'limitations':limitations,
 'ledger':ledger,
 'decisions':decisions,
}

# ---------------- 逐字校验 ----------------
errors = []
def check_quotes(items, where):
    for item in items:
        sid = item.get('source_id')
        q = item.get('quote')
        if sid not in TXT:
            errors.append('%s: 未知 source_id %s' % (where, sid)); continue
        if q not in TXT[sid]:
            errors.append('%s: 引文不匹配 %s : %r' % (where, sid, q))

for c in raw_candidates:
    check_quotes(c['evidence'], c['candidate_id'])
for g in goals:
    check_quotes(g['evidence'], g['candidate_id'])
for sc in ledger['source_checks']:
    check_quotes(sc['evidence_candidates'], sc['check_id'])
for r in relations:
    check_quotes(r['evidence_quotes'], r['relation_id'])

# 结构自检
ids = [c['candidate_id'] for c in raw_candidates]
assert len(ids) == len(set(ids)), 'raw candidate id 重复'
gids = [g['candidate_id'] for g in goals]
assert len(gids) == len(set(gids)), 'goal id 重复'
for cid,(d,gl,r) in ENTRIES.items():
    assert cid in ids, 'entries 引用未知候选 %s' % cid
    for x in gl:
        assert x in gids, 'entries 引用未知目标 %s' % x
for cid in ids:
    assert cid in ENTRIES, '候选缺 entries: %s' % cid
for g in goals:
    assert any(g['candidate_id'] in gl for d,gl,r in ENTRIES.values()), '目标缺来路: %s' % g['candidate_id']
    if g['judgment']['label'] in ('direct','inferred'):
        assert g['judgment']['unsupported_parts'] == [], 'direct/inferred 的 unsupported_parts 必须为空: %s' % g['candidate_id']
for q in questions:
    assert q['target_id'] in gids or q['target_id']=='DOC036-goal-model', 'question target_id 无效: %s' % q['target_id']
assert len(ledger['passes'][0]['window_results']) == 38, '窗口覆盖数不足'

if errors:
    print('=== 引文校验失败 %d 项 ===' % len(errors))
    for e in errors:
        print(e)
else:
    print('引文逐字校验: 全部通过')

Path('spec.json').write_text(json.dumps(spec, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('已写 spec.json: raw=%d goals=%d relations=%d groups=%d questions=%d source_checks=%d' %
      (len(raw_candidates), len(goals), len(relations), len(decisions['groups']), len(questions), len(ledger['source_checks'])))
