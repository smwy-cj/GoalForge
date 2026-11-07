"""Transport manually authored semantic decisions into the public skill contracts.
No keyword extraction, reference labels, external API, or generated semantic decisions.
"""
import json, pathlib, hashlib, subprocess, datetime, sys
BASE=pathlib.Path(__file__).resolve().parent
ROOT=pathlib.Path.cwd()
def read(p): return json.loads(pathlib.Path(p).read_text(encoding='utf-8'))
def write(p,x): pathlib.Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
SPECS={}
def spec(doc,text):
 rows=[]
 for line in text.strip().splitlines():
  parts=line.split('|')
  turn,key,statement,reason=parts[:4]
  rows.append(dict(turn=int(turn),key=key,statement=statement,rationale=reason,origin=parts[4] if len(parts)>4 else 'explicit'))
 SPECS[doc]=rows

spec('DOC003','''
7|plan|Plan flight itineraries using travel websites.|The respondent explicitly describes the purpose of consulting travel websites.
9|compare|Find the best available travel alternative considering price, seating and other benefits.|The stated exploration has this comparative result; no universal cheapest-only criterion is imposed.
9|deal|Obtain a good deal on flight bookings.|Better prices motivate early booking and exploration; later answers repeatedly confirm the intent.
15|early|Aim to book flights at least one to one-and-a-half months ahead for a better price, ideally a couple of months ahead.|This is an aspiration with acknowledged last-minute exceptions, not a compulsory lead time.
17|others|Book flights for friends and family as well as for oneself.|The stakeholder explains helping several named kinds of travellers; no software responsibility is assigned.
17|vouchers|Use spare points or gift vouchers to help others save on their flights.|This is a conditional strategy and intended saving, not an always-required payment method.
19|airtime|Prefer to maximize time in the air on personally enjoyable trips.|An explicitly chosen long flight and willingness to take stops support the personal preference; later intolerable durations limit it.
25|periodic|Compare flight deals across multiple websites at intervals before booking.|Repeated checks are an intentional means to seek a good deal; urgent bookings are an exception.
29|winter|Travel during the winter break, returning home if a good deal is found and otherwise choosing another destination.|The destination remains conditional and undecided; the travel intention is explicit.
31|city|Explore alternative city or country pairs, nearby airports and dates to find suitable options.|All are constraints on one search result, not separate compulsory journeys.
31|connect|Coordinate the flight itinerary with onward transport and lodging logistics to avoid long unproductive waits.|The respondent states the reason for checking timing and connections.
31|coupons|Check provider coupon and upgrade options before deciding where to book.|The stated investigation preserves both alternatives without promising a particular benefit.
31|details|Verify terminal and other journey logistics before booking.|The respondent says to make sure the logistics information is correct.
31|pay|Pay the selected booking through a credit card after finalizing the itinerary and provider.|A selected payment strategy in the described booking flow; it is not a requirement for every user.
47|handoff|Reach the selected provider's itinerary page with flight details already populated.|The direct handoff is used deliberately to confirm and pay, not to search again.
53|anonymous|Prefer to search revenue flights anonymously without logging in, except when a specific need forces login.|Privacy intent is explicit; points booking and later forced-login cases are exceptions.
53|tracking|Avoid disclosing personal data or being tracked while researching flights.|The motive is explicit; the belief that tracking may raise prices is not asserted as a verified fact.
55|award|Check availability of limited award seats by logging into the airline loyalty account when making a points booking.|A clear conditional aim; no assertion that Skyscanner supports award search is made.
57|awardbook|Book award flights directly with the airline account holding the points.|The respondent's chosen route is explicit, while third-party tools are described but not personally adopted.
65|country|Search combinations of airports using country or region inputs instead of only the nearest airport.|A clear preferred way of widening the search.
69|timefilter|Restrict departure and arrival times when connecting to another commitment.|The conditional use of time filters is explicit.
69|duration|Apply a reasonable flight-duration limit when a hard limit is needed, especially for international journeys.|The example rejects 55 hours without claiming a universal maximum.
73|balance|Prefer international flight options balancing price and time rather than extremely long cheapest itineraries.|The stated use of the best tab is situational, not acceptance of its algorithm's every criterion.
73|domestic|Compare the cheapest domestic options when the limited alternatives can be judged directly.|The domestic search preference differs from the international case.
77|schedule|Find an itinerary whose connections and times fit the traveller's actual plans.|This is the explicit test applied to flight details.
77|provider|Compare provider final prices, ratings and applicable discounts for a chosen itinerary.|The respondent actively visits several providers; quoted prices may occasionally change.
81|research|Recheck available alternatives when an itinerary is unsuitable, while accepting the only feasible urgent booking if necessary.|The exception is retained rather than turning preferences into absolute rejection rules.
83|train|Prefer a reasonably priced flight arriving early enough to catch the last onward train and get home that night.|The desired connection is explicit but can be sacrificed when the price difference is unaffordable.
87|alerts|Receive price-drop alerts for several acceptable routes when urgent travel becomes too expensive.|A specific exceptional use is explicit; it does not replace the usual anonymous search preference.
89|data|Avoid sharing data with an additional party when an already-logged-in trusted-as-needed alternative can supply alerts.|The choice is relative data minimization, not a statement that Google has perfect privacy.
95|parallel|Research many combinations of airports, dates, travellers and service classes at the same time.|The respondent explicitly wants parallel searches instead of repeated manual research.
99|matrix|Compare a broad combination of US and Indian airports, outbound and return date ranges and service classes, including a separate points search.|The 11760 calculation is illustrative, not a new fixed system capacity requirement.
103|price|Find the best booking price for the selected itinerary across booking options.|This distinct price objective is explicit, with discounts affecting the final choice.
107|flexibility|Include flexibility when evaluating flight options, while giving itinerary and price greater emphasis.|The stakeholder names three dimensions and prioritizes the first two.
111|market|Show price comparisons with typical market prices when the traveller is unfamiliar with that market.|This is explicitly helpful only while unfamiliar, and nice-to-have rather than necessary forever.
119|meeting|Match flight timing to the schedule of the person being visited when relevant.|The condition is explicit and must not apply to every journey.
119|sleep|Prefer a flight time allowing a night's sleep, while accepting red-eye flights.|The stated preference is defeasible and cannot become a red-eye prohibition.
123|mct|Prefer stopover time of at least about 1.5 to 2 times the airport minimum connection time to account for delays.|The stakeholder's usual safety margin is retained; stop count itself is not a priority unless visa issues apply.
123|lounge|Check whether desired airport lounges will be open during stopovers.|This is a distinct travel preference, not a requirement to minimize stops.
123|pass|Maintain global lounge access through Priority Pass.|A reported capability has an explicit continuing-maintenance intention.
125|loungeintegration|Ideally integrate an up-to-date record of the traveller's cards and lounge entitlements with Skyscanner.|The proposal is conditional on accurate updates; current third-party unreliability is retained.
127|loungesource|Check lounge access policies, opening times and disruptions using the relevant card or pass issuer's source.|This is the chosen reliable-information strategy, conditional on issuer and airport.
127|balanceaccess|For a limited-use lounge card, verify that airport access remains valid and unused allowance remains for the applicable period.|The respondent explicitly distinguishes limited from their own unlimited access.
129|partners|Obtain a set of booking partners potentially offering useful discounts or deals.|This requested output is explicit; actual savings are not guaranteed.
137|oneclick|Find the best suitable flight option from all personal parameters in one place with less manual research.|The obstacle explains a positively supported inferred improvement, not a guarantee of mathematically global optimality.|inferred
137|consolidate|Access the information needed for booking in one place instead of consulting at least ten to twelve sites.|The desired consolidation is inferred from the specific expressed obstacle.|inferred
147|speed|Reduce time and mental effort spent performing repeated flight research.|Familiarity saves repeated-search effort and later willingness to switch explicitly confirms the aim.
149|accurate|Research flight options more accurately while spending less time.|The respondent explicitly identifies a reason to adopt another platform, without a fixed time threshold.
155|longterm|Adopt a different research platform for even small recurring time savings over the long term.|This willingness does not apply automatically to a single use; learning cost and busyness matter.
''')
spec('DOC010','''
7|planning|Use weather information to plan everyday activities and trips.|The stakeholder explicitly identifies planning as the primary purpose.
7|clothing|Choose suitable clothing for the day's weather.|A separately satisfiable everyday decision is explicit.
7|outdoor|Plan outdoor activities according to expected weather.|The purpose is explicit, distinct from clothing and travel.
13|weather|Obtain useful weather information, initially via Siri and through the app if the assistant does not provide it.|This preserves fallback and does not require visiting a website when the app suffices.
13|carry|Choose what to carry when going out based on the weather.|A separate preparation decision is explicit.
17|trip|Check destination weather before planning a trip and buying outdoor-activity tickets.|The unfamiliar-location and pre-purchase context is explicit.
19|week|Check the whole week's forecast when planning a trip requiring activities and tickets.|Ordinary use is daily, so the weekly scope remains conditional.
21|tickets|Avoid buying amusement-park tickets for rainy or very cold conditions.|The expressed reason for checking the Chicago Six Flags forecast supports this avoidance goal.
25|exit|Check weather whenever leaving the apartment because conditions may change.|This is a personal checking intention rather than a forced app notification rate.
33|newplace|Become familiar with weather conditions when in a new place.|The stakeholder contrasts this with not needing checks after long residence.
35|extreme|Identify extreme weather such as thunderstorms and flooding.|These conditions are explicitly important for deciding whether to go out.
35|postpone|Postpone an event and avoid going out when extreme weather is forecast.|This combines the direct action and its immediate safety consequence, with the triggering condition retained.
39|alert|Receive app notifications or alerts for extreme weather.|Explicit expectation, not a requirement that all weather arrive by email or county SMS.
41|routine|Receive ordinary weather notifications three times a day, in the morning, afternoon and evening.|The chosen frequency fits the routine; rain updates are an explicit exception.
49|rain|Receive frequent notifications about ongoing rain and when it starts or stops.|Rain-specific exception to ordinary three-times-daily updates.
51|transport|Use timely weather information to decide whether to walk or take a bus.|The grocery example expresses this decision purpose.
51|realtime|Receive accurate, real-time weather updates to avoid being caught out by unexpected rain.|The wet-shopping experience and later explicit requests support the result; no perfect-forecast guarantee is invented.
57|ads|Use the weather service without annoying advertisements.|The preference is explicit and is later restated as no ads.
59|sync|Keep app and website weather information consistent and up to date.|The stale-rain example plus agreement about cross-platform consistency support the intended improvement.
63|hourly|Receive hourly updates when rain or other adverse conditions require closer monitoring.|This retains condition-specific frequency rather than applying hourly updates universally.
65|daily|Use daily forecasts comfortably for ordinary planning.|The respondent prefers ordinary daily forecasts, with three routine updates.
71|cross|Keep weather information consistent across all platforms.|An explicitly requested broader consistency goal, beyond the app/website example.
''')
spec('DOC013','''
4|choose|Allow viewers to choose videos to watch.|The described viewer role has a clear choice purpose.
4|share|Allow content creators to share content with the platform.|The streamer role is described through its intended result.
6|restrictview|Prevent viewers from seeing content unsuitable for them.|A tentative but explicit requirement; suitability rules and viewer classes remain unspecified.
6|restrictupload|Prevent streamers from sharing prohibited content with anybody.|Distinct upload-side restriction; explicit language is only an example, not an exhaustive legal rule.
12|textsearch|Find a specific kind of video using text search or filters.|Both are alternative ways to a single search result.
12|visual|Browse many video options visually using thumbnails and relevant descriptions or creator information.|A separately requested visual-discovery mode, not merely a text-search implementation step.
12|upload|Upload a video to the platform.|Explicit creator requirement.
12|stream|Start a live stream.|Explicit alternative creator result, separate from uploading an existing video.
12|describe|Add descriptive information to uploaded videos.|Title/description context is carried by the source and later workflow.
12|captions|Add a transcript or captions to videos.|A proposed creator capability, not an assertion of automatic perfect transcription.
12|edit|Edit videos with operations such as sound effects, trimming and cropping.|The core action is editing; examples constrain capability without inventing three compulsory separate edits.
14|vague|Obtain meaningful search results even from vague criteria.|The stakeholder explicitly wants this beyond exact search.
14|smooth|Receive a seamless buffered video stream without constant freezing.|A quality result is explicit; no invented latency threshold.
16|entertain|Use video content for entertainment.|Explicit purpose.
16|educate|Use video content for education.|Explicit purpose, separate from entertainment.
16|information|Gain needed information quickly through a search.|The stakeholder explicitly summarizes this purpose; book avoidance does not prohibit reading elsewhere.
18|format|Avoid format incompatibility when uploading an already-made video.|An inferred desired improvement from a stated potential technical obstacle; exact supported formats remain unknown.|inferred
18|length|Avoid restrictive video-length requirements during upload.|The stated obstacle supports the concern but no numeric limit is specified.|inferred
18|publish|Publish uploaded videos through a simple process.|The questions about waiting and publication identify a desired simplification, without proving publication can precede completion.|inferred
30|watchlist|Save videos to a watch list.|Tentative proposed viewer capability; not compulsory usage.
30|subscribe|Subscribe to creators or types of content.|The suggested viewer capability is explicit.
30|latest|Access the latest content from subscribed creators in one subscriptions area.|A distinct retrieval result with subscription as a condition.
40|controls|Make playback controls discoverable to unfamiliar viewers, including when hidden during full-screen playback.|The expressed discoverability obstacle positively supports the inferred improvement.|inferred
40|captionaccuracy|Improve automatic-caption accuracy for viewers, particularly those who do not speak English as a first language.|The speaker is uncertain about current accuracy; this is an inferred accessibility concern, not a verified defect.|inferred
40|colour|Consider colour adjustments for colourblind viewers.|The speaker explicitly proposes possible work while admitting not knowing current capabilities; tentative strength retained.
''')
spec('DOC020','''
9|recruit|Receive and respond to recruiter emails during job applications.|Current recruiting communication intent is explicit; later frequent checking confirms its importance.
9|school|Receive school notifications and communicate about school matters.|The primary-use explanation supports this separate communication purpose.
15|unread|Review unread emails to identify important messages.|The workflow is intentional triage, not a requirement to reread all mail forever.
15|mark|Mark important emails for attention.|A distinct triage action selected by the stakeholder.
15|delete|Delete unwanted or spam emails to keep the inbox clear.|This directly combines deletion with its stated organizing purpose.
15|read|Read important emails.|Explicit intended action after initial triage.
15|defer|Tag emails needing later action so the task can be completed when available.|Tagging is the chosen means; deferral is not omission of the task.
17|finished|Delete even important emails once their conversation has ended.|The condition differentiates this from discarding active important messages.
17|accounts|Separate important recruiting or school messages from deal mail using different email accounts.|The selected organization strategy is retained without making it the only solution for everyone.
19|draft|Use an AI assistant to compose an email from the sender's main points, then adjust the draft.|AI drafting is explicit; internal integration is separately requested later.
21|font|Adjust font size when preparing an email.|A selected composition capability, not a new automatic-style rule.
21|bold|Make important sentences bold before sending an email.|Explicit emphasis strategy.
21|send|Send the prepared email.|The direct result is explicit after composition and formatting.
23|cloud|Share multimedia through cloud links so recipients can view it on phones or laptops.|Preferred strategy when multimedia is sent; not a demand for embedded media or frequent attachments.
27|spam|Avoid missing important messages due to spam classification, even at the cost of receiving some spam.|The explicit tradeoff prevents a false goal of blocking all spam.
29|edit|Edit a sent email rather than sending a separate correction.|The proposed feature is explicit beyond the reported short undo window.
29|history|Let recipients view the current edited email and optionally inspect its editing history.|Distinct visibility result; both versions remain accessible by choice.
33|delivery|Reliably receive expected emails such as website-registration messages.|The stated delivery obstacle supports an inferred outcome; no transport cause is invented.|inferred
37|builtin|Compose a well-organized email from brief input using an assistant built into the email client.|A distinct explicit integration request, preserving the selected in-client mechanism.
37|attachment|Warn before sending when the text says an attachment is present but the file is missing.|The existing feature is explicitly valued and should be preserved, not discarded as mere fact.
41|summary|Use AI to extract the main points of received emails.|Explicit request confirmed as summarization.
45|keywords|Highlight important keywords or details so the reader does not overlook them.|The assessment example explains the separate highlighting outcome.
49|miss|Avoid missing messages from recruiting teams.|Frequent checking is expressly motivated by this avoidance result; checking count is not a service frequency requirement.
53|time|Reduce the time spent reading every email.|The stakeholder explicitly identifies the routine task to simplify.
55|digest|Consider periodic summaries of batches of received emails as one way to reduce reading effort.|The interviewer suggestion receives tentative acceptance as one possible solution, not a mandatory three-email schedule.
59|notify|Receive notifications for important messages if importance detection is sufficiently reliable.|The speaker declines full reliance if important messages may be missed; conditional strength retained.
71|forward|Forward email when coordinating work under a tight deadline.|A condition-specific existing feature the stakeholder calls important.
71|bulk|Send a message to the whole group using bulk addressing or BCC under a tight deadline.|The follow-up confirms reaching many people quickly; no privacy interpretation of BCC is invented.
87|search|Search emails as an essential daily capability.|The priority ranking supplies explicit continuing intent.
87|filter|Filter messages by tags, including through search.|The speaker considers this achievable through search, not an independent mandatory implementation.
87|schedule|Schedule emails for different sending times.|The requested ranking places this after searching; it does not make it obligatory or time-specific.
93|category|Explore shared, self-defined email categories or protocol identifiers so correspondents can communicate using matching categories.|An explicitly tentative future proposal, with recruiting as an example and practicality uncertain.
99|professional|Maintain professional communication with people inside or outside one's employer.|The future-use intent is explicit and broader than internal communication.
''')
spec('DOC023','''
3|count|Increase the number of profile connections.|An explicit primary goal; no target count is invented.
3|active|Show other people that the stakeholder is active on LinkedIn.|Explicit purpose for increasing the connection count.
3|referral|Obtain referrals from current employees for target-company internships or full-time jobs.|Explicit primary goal; current-employee condition clarified later.
3|resume|Increase the chance that recruiters see the resume.|The stakeholder states referrals help this, without guaranteeing review or employment.
7|search|Find people matching both the target company and the stakeholder's university background.|A conjunction on the same people, not two independent lists; current employment clarified by T009.
7|profile|Review potential contacts' profiles to judge whether their experience fits the need.|A purposeful screening action, distinct from search.
7|connect|Send connection invitations to suitable potential referrers.|The selected action follows relevant experience screening.
7|note|Attach a self-introduction and, when appropriate, a referral request to a connection invitation.|The referral message is sometimes included rather than compulsory in every note.
7|chat|Discuss referral details after the invitation is accepted.|Acceptance is a condition, not a separately guaranteed goal.
9|current|Choose current target-company employees who attended the same university for referral outreach.|One constrained selection goal; former employees and single-criterion matches are explicitly excluded in this context.
11|willing|Increase potential referrers' willingness to help by emphasizing the shared university background.|The belief about alumni helpfulness motivates the strategy but is not asserted as a verified universal fact.
13|precise|Obtain more precise people-search results matching the intended background.|Specific irrelevant-result obstacles support this inferred improvement.|inferred
15|access|Access as many relevant potential connections as needed, using Premium when worthwhile despite its cost.|The paid strategy is one option, not a mandatory subscription.
15|keywords|Modify search keywords to seek more precise potential-connection results when needed.|Removing keywords or becoming more specific are alternatives for the same search adjustment.
17|message|Convey the intended connection message without excessive effort shrinking it to the nonmember character limit.|A desired improvement inferred from the explicit communication obstacle; no unsupported new character limit is specified.|inferred
''')
spec('DOC031','''
1|communicate|Communicate with university peers, teaching assistants and professors.|The intended communication audience is explicit across early answers.
7|instant|Reach university members almost immediately.|The primary advantage is explicit instant communication.
7|lookup|Find university members by name or surname without first saving phone numbers or email addresses.|The selected lookup route is explicit; it is not a guarantee that any ambiguous surname uniquely identifies someone.
7|devices|Communicate using Slack on either the phone or laptop.|The cross-device use is explicitly valued rather than merely listed as available.
9|audience|Reach a wide audience immediately through channels.|The desired outcome and selected means are explicit.
9|history|Access channel information posted before joining the channel.|Explicitly valued history capability to preserve.
9|aware|Keep informed about shared subject information and university or program activities.|A purposeful information result, not a new requirement for all possible topics.
11|document|Share documents instantly with teammates while collaborating.|The action is explicitly central and is tied to instant communication in T013.
19|retrieve|Find specific past messages or files using keyword search.|The target is specific retrieval, not simply showing every matching item.
19|relevance|Reduce the difficulty of locating a desired message among excessive keyword-search results.|A supported inferred improvement from the precise retrieval obstacle.|inferred
21|call|Make audio or video calling easier to access with fewer navigation steps.|The improvement is explicitly requested and later repeated, especially for groups.
23|phone|Use a direct phone call as a quicker alternative when the other person's number is already known.|The condition and alternative strategy are explicit, not an instruction to abandon Slack.
27|email|Provide a quick handoff to a standard email app for formal communication with a teaching assistant or professor.|The selected external-app handoff is explicit; no automatic email sending is implied.
27|groupcall|Make the call feature more accessible in a group setting.|A context-specific further request, distinguishable from the general access improvement.
31|narrow|Improve navigation when the Slack browser window is narrowed alongside other open windows.|A personal multiwindow usage condition, not a claim the full-screen layout is unusable.
''')
spec('DOC028','''
3|information|Find information about a particular topic when needed.|The stakeholder names local Halloween information as an example.
3|browse|Read interesting posts from followed communities during free time.|The intentional leisure activity is retained despite the lack of a fixed external outcome.
3|technical|Obtain technical help or alternative inputs when stuck on a coding problem.|A distinct use case and desired result.
5|targeted|Obtain targeted answers to the particular problem being faced.|The primary reason for using Reddit is explicit.
5|experience|Learn from contextual personal experiences rather than only generalized search facts.|The preference is explicit; legitimacy is the user's belief, not a verified reliability guarantee.
7|google|Find relevant Reddit posts by searching Google with the question plus Reddit.|The chosen targeted-search route is retained.
9|solve|Solve a predefined problem through the Reddit interaction.|An explicit desired outcome when there is a predefined problem; no promise that any answer will solve it.
15|quick|Reach authentic answers to specific queries faster.|The speaker explicitly values saved time; authenticity is an aspiration, not verified for every post.
21|advice|Post questions in an appropriate community to obtain advice.|The stakeholder's actual posts are advice-seeking; other post genres are not imposed as personal goals.
21|comment|Interact with a post by adding a comment or replying in an existing thread.|Alternative comment placements serve one communication action.
27|mobile|Improve the mobile app's usability and responsiveness.|Explicit frustration and later request support this improvement, without claiming all platforms fail.
27|draft|Save unfinished mobile posts as drafts.|The missing mobile capability is contrasted with desktop; inferred desired repair.|inferred
27|threads|Make mobile comment threads easier to follow.|A specific usability improvement supported by the stated mobile tracking difficulty.|inferred
31|trends|Occasionally keep up with relevant community events or trends.|The limited purpose is explicit; news is generally preferred outside Reddit.
33|product|Research purchase decisions using balanced product experiences from people with relevant backgrounds.|The laptop example provides both intent and desired contextual comparison.
35|health|Learn about general health or beginner activity questions while avoiding reliance on Reddit for specific medical problems.|The speaker explicitly limits trust and does not recommend personal-diagnosis reliance.
43|card|Prefer card view for passive browsing.|A conditional display preference, not a universal mode.
43|compact|Prefer compact view when actively searching so multiple relevant results can be compared before opening one.|The active-search condition is distinct from passive card browsing.
45|ads|Prefer an advertisement-free experience.|An explicit preference even though existing ads are described as subtle.
47|premium|Consider paying for Premium to avoid advertisements when ad blocking is unavailable.|The condition explains why the current ad blocker makes payment unnecessary.
51|accurate|Maintain accurate search results that avoid wasting time finding specific information.|The positive evaluation includes a clear continuing value, supporting maintenance intent.|inferred
51|subreddit|Find the exact relevant subreddit using a generative AI tool.|The explicit proposed mechanism and result are retained, later repeated in T059.
59|specific|Post a particular question in a suitably specific community.|This strategy is explicit and distinguishable from merely finding the community.
61|better|Obtain better subject-relevant answers from knowledgeable community respondents.|A hoped-for result with acknowledged possible bad responses, not complete mitigation.
63|bestapp|Improve the official mobile app so it is a strong first-party option rather than lagging behind third-party wrappers.|The aspiration is explicit; no quantitative market-share target is invented.
''')
spec('DOC036','''
10|gift|Purchase suitable gifts such as cakes for a girlfriend on special occasions.|The use case is explicit and examples do not limit all purchases to cakes.
10|design|Inspect vendor clothing designs online before seeking those designs in a physical market.|The selected research-before-offline-shopping strategy is explicit.
12|vendor|Find nearby relevant vendors by searching product terms and adding location terms if necessary.|The location-suggestion mechanism is uncertain; the search intention is clear.
14|fraud|Avoid losing money to malicious vendor accounts that do not deliver purchases.|The specific near-scam experience supports this inferred avoidance goal; the speaker did not actually lose money.|inferred
14|beforepay|Require delivery before payment when a suspicious vendor would otherwise pose a risk.|A described personal precaution, not a universal payment rule across all later purchases.
16|contact|Prefer contacting vendors through the phone or WhatsApp number in their bio for quicker responses.|On-platform chat is possible; the preference is explicitly comparative.
22|browse|Browse a vendor's product images and varieties to choose a gift even without a predetermined item.|The open-minded selection goal is explicit.
24|anonymous|Browse and search Instagram without signing in.|An explicit request repeated and clearly confirmed later; anonymous posting remains ambiguous.
24|presence|Avoid revealing online presence while making a quick product search.|Distinct privacy purpose of anonymous access.
24|history|Reuse saved vendor search history to return to a previously found vendor without searching again.|The continuing feature is explicitly valued.
24|engagement|Examine comments and likes on product images to help assess vendors and purchases.|The chosen heuristic is valued; T062 corrects the interviewer so no guaranteed trust ranking is claimed.
26|privateposts|Restrict personal posts to close friends using a private account.|Explicit personal privacy strategy when posting.
26|privateonline|Limit visibility of online status to close friends.|A distinct explicit expectation, not a demand that nobody can ever see it.
26|harm|Avoid future harm or predation arising from public personal-life sharing.|The concern and protective purpose are explicit; no verified attack is invented.
30|reconnect|Reconnect with friends through Instagram if phone numbers or other immediate contact details are lost.|A condition-specific valued social benefit.
32|style|Choose clothing that fits the stakeholder's preferred cool style.|The personal taste motivates purchases but is not a requirement for other people.
32|limit|Limit Instagram use to times when there is a need, to reduce unwanted influence or overuse.|An explicit self-regulation goal; later logout and deletion are chosen strategies.
52|logout|Log out or remove easy access after a shopping period to manage use.|Selected means include deleting the phone app or browser traces; alternatives are not simultaneous requirements.
52|period|Remain logged in only through a planned shopping period when repeated login is inconvenient.|A conditional workaround, distinct from the preferred anonymous access.
56|local|Quickly learn local vendors' locations, contact details and offerings when staying in an unfamiliar place.|A clear convenience purpose, not a claim Instagram is always preferred to stores or other services.
58|price|Display product prices on business pages.|An explicit feature wish, despite speculation that sellers may withhold prices to solicit feedback.
58|askprice|Ask the vendor for a product's price when it is not displayed.|A selected step with a direct information purpose.
58|pay|Pay the vendor using the supplied payment contact after agreeing the price.|A current flow, not a claim payment before delivery is safe with suspicious accounts.
58|address|Provide the delivery address for the purchased product.|A separate intended outcome in ordering, conditional on delivery.
58|delivery|Receive the purchased product at the agreed delivery location.|The described wait and pickup embody a positively supported outcome.|inferred
62|assess|Use the pattern of engagement across products of different ages to judge whether a vendor seems legitimate.|The speaker clarifies this is a heuristic, not an automatic rating system or proof of safety.
''')

# Explicitly inspected boundary cases. These are candidate exclusions, not an assertion
# that every background sentence ought to become a candidate.
EXCLUSIONS={
 'DOC003':[(43,'Hotels and car hire are reported aggregator capabilities, not adopted goals in this flight-focused discussion.'),(67,'CO2, airline and stop filters are described as available; personal use or maintenance intent is not established for each.'),(71,'The best-tab algorithm description is not the respondent adopting all its ranking criteria.'),(85,'Better alerts are a hedged possibility with strong limitations; the actual limited alert goal is captured from T087.'),(101,'Capabilities of Kayak and Google Flights are comparison background; they are not all separate requested features.'),(133,'Skyscanner itself does not perform the final booking; do not invent an in-Skyscanner payment goal.')],
 'DOC010':[(31,'Residence history explains reduced checking in a familiar place; do not impose universal daily checks there.'),(55,'A guess about technology limitations does not specify a technical solution.')],
 'DOC013':[(10,'A guess that a large company hosts and controls content is architectural background, not an adopted deployment goal.'),(24,'Thumbnails, voice-search icons, ads and interface layout are largely narrated capabilities; no distinct intention supports every UI control as a goal.'),(28,'The 24-hour wait is a reported platform rule rather than a request to impose that rule.'),(32,'Premium pricing and family/student plans are reported product facts, without an expressed purchase or preservation intent.'),(38,'Playback toggles, timing and volume widgets are narrated options; do not automatically upgrade each to a stakeholder goal.')],
 'DOC020':[(33,'The respondent sends no confidential mail; do not infer that security is unimportant to every user or invent a privacy specification.'),(61,'Rare crashes are a positive current fact without a separate explicit reliability target.'),(79,'Historical uncertainty about pre-email communication is not a new-client requirement.')],
 'DOC023':[(13,'Search-result access limits are an obstacle; do not turn the existence of Premium into a compulsory subscription.'),(17,'200 characters is a reported limit, not the desired replacement limit.')],
 'DOC031':[(17,'Bold, italics and emojis are described capabilities during a file-sharing walkthrough, without independent intent for each.'),(25,'The stakeholder will continue Slack despite calling friction; this does not mean the improvement request disappears.')],
 'DOC028':[(11,'Anonymity is described as a platform selling point, without a personal demand to make identification impossible.'),(29,'Beliefs about bot fact checking and moderator effectiveness are not verified guarantees or a new universal moderation design.'),(37,'Observed community feeling in others is not evidence that this respondent seeks social bonding.'),(39,'Offline cached-feed capability is only described; a preservation or improvement intention is not established.'),(41,'Sort options are described; later conditional view preferences have separate explicit intent.'),(49,'Dark mode and legacy-site capabilities are background without an adopted demand for each.'),(53,'Browser notifications are described as nonintrusive, not requested for every possible activity.'),(55,'Confidence about backend protocols is a belief, not a verified privacy requirement or implementation.'),(67,'Messaging and trophies are add-on facts without an expressed goal for streaks or direct messaging.')],
 'DOC036':[(34,'The addictive scroll is an obstacle to limited use, not a desire for increased engagement.'),(36,'Following celebrities or hashtags is described, often dismissed as irrelevant, not an adopted goal.'),(44,'The speaker has not used Instagram groups and speculates by analogy with Facebook; do not invent group requirements.'),(59,'The interviewer mentions selling; the stakeholder gives no substantive adoption of a selling goal.'),(71,'Anonymous posting is bundled into an interviewer paraphrase and only weakly acknowledged; the clear repeated browsing request is retained and posting remains unconfirmed.')]
}

if __name__=='__main__':
 for doc,rows in SPECS.items():
  folder=BASE/doc
  write(folder/'manual-initial-spec.json',{'document_id':doc,'authorship':'current assistant semantic reading; program only transports authored decisions','rows':rows,'boundary_candidates':EXCLUSIONS[doc]})
 print('Saved manual initial captures for',len(SPECS),'documents')
