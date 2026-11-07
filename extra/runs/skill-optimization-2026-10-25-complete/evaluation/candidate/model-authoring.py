import sys,pathlib,json
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from authoring import BASE, ROOT, SPECS, read,write,sha
from importlib.util import spec_from_file_location,module_from_spec
module_spec=spec_from_file_location('records',BASE/'build-records.py');records=module_from_spec(module_spec);module_spec.loader.exec_module(records)
records.COMMANDS=read(BASE/'pipeline-execution.json')
R={}
def relations(doc,text):
 R[doc]=[line.split('|') for line in text.strip().splitlines()]

relations('DOC003','''
early|deal|operationalization|15|Booking further ahead is a chosen attempt to obtain better prices; the respondent reports recent last-minute exceptions.
vouchers|others|operationalization|17|Spare vouchers or points are a stated way to help book other people's flights.
periodic|deal|operationalization|25|Repeated cross-site comparisons are explicitly used to seek a good deal, without guaranteeing the lowest obtainable price.
country|city|operationalization|65|Country or regional inputs are the selected way to search many origin and destination airports.
timefilter|connect|operationalization|69|The respondent applies time filters when matching another connection.
balance|compare|specialization|73|The international scenario narrows the general evaluation of price and other travel benefits.
domestic|compare|specialization|73|The domestic scenario uses a cheaper-options preference within the more general alternative evaluation.
provider|price|operationalization|77|Comparing providers, discounts and final costs serves the best price objective.
research|compare|operationalization|81|Rechecking alternatives when details are unsuitable serves finding a workable option.
train|connect|specialization|83|Catching the last train is a concrete instance of onward-transport coordination, subject to affordability.
alerts|deal|contribution|87|Price-drop reminders help urgent price-sensitive travel but cannot force a low fare to appear.
anonymous|tracking|operationalization|53|Anonymous use is the stakeholder's chosen data-protection strategy; the claimed pricing effect is only a belief.
data|tracking|specialization|89|Avoiding an additional party's data collection is a more specific privacy case.
matrix|parallel|specialization|99|The US-to-India airport/date/class matrix is a concrete example of broad parallel research, not a universal fixed capacity.
market|price|contribution|111|Market-price context helps judge unfamiliar prices but does not itself produce or select the best fare.
meeting|schedule|specialization|119|Matching a host's schedule is a concrete itinerary suitability criterion when visiting someone.
sleep|schedule|contribution|119|Sleep-friendly timing helps suitability but red-eye flights remain acceptable.
mct|connect|contribution|123|A larger connection-time buffer helps manage delay risk but cannot guarantee onward travel.
loungeintegration|lounge|contribution|125|Accurate integrated entitlements could help check lounge opportunities, conditional on reliable updates.
loungesource|lounge|operationalization|127|The issuer's lounge information is the chosen source for checking policies and opening times.
parallel|speed|contribution|95|Simultaneous combination searches reduce repeated manual research effort under the described obstacle.
consolidate|speed|contribution|137|Having booking information in one place can reduce visits to many sites; it does not guarantee accurate optimal research.
handoff|pay|precedes|47|The described flow reaches the provider page before confirming details and making payment.
details|pay|precedes|31|Checking logistics is described before deciding and paying, without claiming that checking alone enables a complete booking.
''')
relations('DOC010','''
clothing|planning|specialization|7|Choosing clothes is one explicit concrete use of general weather-informed planning.
outdoor|planning|specialization|7|Outdoor-activity planning is one explicit part of the broader stated planning purpose.
trip|planning|operationalization|17|Destination weather checking is an explicitly selected means to support the trip-planning use of weather.
week|trip|operationalization|19|A whole-week forecast is the selected information scope when planning activity tickets for a trip.
weather|clothing|contribution|13|Obtaining weather helps decide clothing, but the information alone does not complete the decision.
weather|carry|contribution|13|Weather information informs what to carry on a day out.
extreme|postpone|precedes|35|The respondent first sees extreme weather and then postpones the event.
alert|extreme|operationalization|39|Extreme-weather notifications are an expected means of learning about those conditions.
rain|realtime|specialization|49|Frequent rain status updates are a specific case of the wider real-time update request.
realtime|transport|contribution|51|Timely updates inform the walk-versus-bus choice but do not guarantee an accurate weather forecast.
hourly|realtime|operationalization|63|Closer hourly monitoring is a selected update approach during adverse weather, rather than the default routine frequency.
sync|cross|specialization|59|App/website consistency is a concrete pair within the broader all-platform consistency request.
daily|planning|contribution|65|Daily forecasts are valued for routine planning, with trip and extreme-weather exceptions.
''')
relations('DOC013','''
textsearch|choose|operationalization|12|Text or filter search is an explicitly requested means to locate a video to choose.
visual|choose|operationalization|12|Visual thumbnail browsing is a separately requested means to choose among videos.
upload|share|operationalization|12|Uploading an existing video is one stated way creators share content.
stream|share|operationalization|12|Live streaming is another stated way creators share content.
vague|textsearch|specialization|14|Vague-criteria search is a narrower case of the search capability, adding a meaningful-result expectation.
textsearch|information|contribution|16|Quick searching helps obtain needed information, but finding an irrelevant video would not fulfill the information purpose.
educate|information|contribution|16|Educational viewing can provide information but is not claimed as the only or sufficient path to every information need.
format|upload|contribution|18|Removing format incompatibility helps upload but does not ensure transfer or publication succeeds.
length|upload|contribution|18|Avoiding length barriers can help upload; transport and format barriers may remain.
subscribe|latest|precedes|30|The described latest-content area depends on the user's prior subscription to creators.
''')
relations('DOC020','''
mark|unread|contribution|15|Marking important messages helps triage but follows and does not itself perform the unread-message review.
unread|read|precedes|15|The respondent first glances over unread mail, then reads important messages in detail.
defer|reply|precedes|15|When a reply cannot be done now, tagging records it before later completion.
accounts|miss|contribution|17|Separate accounts help isolate important recruiting or school mail, without ensuring delivery or attention.
draft|adjust|precedes|19|The described AI composition happens before the sender adjusts the output.
adjust|send|precedes|21|The sender adjusts content or formatting before sending.
font|send|precedes|21|Font formatting is a described pre-send step, not a sufficient cause of sending.
bold|send|precedes|21|Important sentences are made bold before the described send.
spam|miss|contribution|27|Avoiding erroneous spam placement helps avoid missed recruiting messages; missing mail can have other causes.
builtin|draft|operationalization|37|A built-in assistant is explicitly proposed as a means to compose from short main-point input.
summary|time|contribution|53|Summarization is explicitly suggested to reduce the time spent reading every message.
keywords|read|contribution|47|Highlighting overlooked details supports careful reading but does not ensure understanding of the entire message.
digest|time|operationalization|55|Periodic batch summaries are tentatively accepted as one way to reduce reading effort.
notify|miss|contribution|59|Reliable important-message alerts could reduce missed mail, with the acknowledged failure condition if detection misses an item.
search|filter|operationalization|87|The respondent says tag filtering can be done through searching; searching is the proposed means to obtain the filtered messages.
''')
relations('DOC023','''
count|active|contribution|3|Increasing connection count is intended to signal activity but a static count need not prove present activity.
referral|resume|contribution|3|A referral is said to help recruiter visibility; it is not a guarantee that recruiters inspect the resume.
search|referral|operationalization|7|Searching by company and school is an outreach strategy serving referral requests.
profile|connect|precedes|7|The respondent checks experience before inviting a matching person.
connect|chat|precedes|7|Referral-detail chat occurs after inviting and only if the invitation is accepted.
note|referral|contribution|7|An introduction and optional referral request can help outreach, without guaranteeing a response.
current|search|specialization|9|Current employees with the university background narrow the earlier company-and-school search whose results may include former employees.
willing|referral|contribution|11|Increased willingness may help gain a referral, based on a stated personal belief about alumni.
keywords|precise|operationalization|15|Keyword revision is the explicit alternative strategy to improve relevance.
access|referral|contribution|15|More accessible potential contacts may help find a referrer; high access alone is not enough.
message|note|contribution|17|A message not excessively constrained by the character cap would support the intended introduction/request.
''')
relations('DOC031','''
instant|communicate|specialization|7|The instant-result requirement narrows the broader university-communication purpose.
lookup|instant|operationalization|7|Name lookup without saved contact data is explicitly valued as a way to reach people immediately.
devices|communicate|operationalization|7|Phone or laptop access provides the described routes to communication, not a guarantee of recipient response.
audience|instant|specialization|9|Immediate channel outreach is a wide-audience case of instant university communication.
history|aware|contribution|9|Earlier channel information helps understand shared subjects or campus activity, but history alone need not cover current events.
document|instant|operationalization|13|The stakeholder explicitly relates instant teammate document sharing to the instant-communication goal.
relevance|retrieve|contribution|19|Reducing excessive search results can help find the desired past message.
phone|instant|operationalization|23|A known person's direct phone number is an alternative quicker route in the described circumstance.
email|communicate|operationalization|27|A quick handoff to email serves formal university communication while leaving the final send to the email app.
groupcall|call|specialization|27|Group call access is an especially requested case of the general call-access improvement.
narrow|communicate|contribution|31|Improved narrow-window navigation can ease communication during side-by-side work.
''')
relations('DOC028','''
technical|targeted|specialization|3|Stuck coding problems are a concrete class of targeted questions.
experience|targeted|contribution|5|Relevant personal experience can produce contextual answers, but the respondent's reliability belief is not proof.
google|targeted|operationalization|7|A Google question plus Reddit query is the chosen route to relevant Reddit posts.
targeted|solve|contribution|9|Targeted answers may solve a predefined problem, but incorrect or incomplete answers remain possible.
advice|targeted|operationalization|21|Asking a question in a community is a described way to obtain advice on a problem.
draft|mobile|contribution|27|Saving unfinished posts would address one specific mobile usability problem, leaving other UI issues.
threads|mobile|contribution|27|Clearer thread presentation addresses another mobile usability problem but not general slowness.
product|targeted|specialization|33|Purchase research is a concrete problem context seeking relevant personal experiences.
health|information|specialization|35|General-health learning is a specific information use, excluding reliance for specific medical problems.
card|browse|operationalization|43|Card view is explicitly preferred when passively browsing interesting posts.
compact|targeted|operationalization|43|Compact view is preferred for comparing relevant results during active searching.
premium|ads|operationalization|47|When ad blocking is unavailable, a Premium subscription is a contemplated ad-free route.
accurate|quick|contribution|51|Accurate results are valued because they reduce time spent finding information.
subreddit|specific|precedes|59|The proposed tool finds the right community before the person posts a question there.
specific|better|contribution|61|A specific community is expected to improve answer relevance, with explicitly acknowledged bad responses still possible.
subreddit|better|operationalization|59|The proposed generative AI community finder serves the hoped-for improvement in answers, without guaranteeing quality.
bestapp|mobile|contribution|63|A stronger official app is expected to improve the stated mobile experience, without a fixed market-share target.
''')
relations('DOC036','''
vendor|gift|operationalization|12|Searching nearby relevant vendors is a selected route to sourcing the intended gift.
beforepay|fraud|operationalization|14|Delivery before payment is the personal precaution used against a suspicious seller, not a guarantee against every fraud.
contact|gift|contribution|16|Quicker vendor contact helps the shopping goal but does not ensure stock, payment or delivery.
browse|gift|operationalization|22|Browsing varieties is a valued alternative for choosing a gift without a predetermined item.
anonymous|presence|operationalization|24|Browsing without signing in is explicitly desired to avoid revealing a quick search visit.
history|vendor|operationalization|24|Reusing a saved vendor result is an alternate way to return to a vendor without repeating the search.
engagement|fraud|contribution|24|Examining comments and likes helps spot suspicious accounts, but the speaker's heuristic does not prove safety.
privateposts|harm|operationalization|26|A private account restricting posts to close friends is the chosen protective strategy.
privateonline|harm|contribution|26|Limiting online-status visibility is expected to reduce public exposure.
logout|limit|operationalization|52|Logging out and removing easy access is a stated means of limiting use after a shopping period.
period|limit|operationalization|52|Keeping login only through an intended shopping period is a workaround serving bounded use.
local|gift|contribution|56|Learning local vendor information helps source purchases during short stays without making Instagram universally preferred.
askprice|pay|precedes|58|The described purchase flow establishes the price before the buyer pays.
pay|address|precedes|58|In the ordinary described flow payment precedes confirmation of the delivery address; suspicious-seller precautions are a distinct case.
address|delivery|contribution|58|An agreed address helps delivery but cannot ensure an honest vendor sends the product.
assess|fraud|operationalization|62|Comparing engagement across product ages is the stakeholder's specific legitimacy heuristic, not an automatic ranking or conclusive fraud test.
''')

# Whole-group candidate assessments were authored after the independent relation pass.
# All retained groups have concrete insufficiency findings, not invented completion.
GROUPS={
 'DOC003':[
 ('schedule',['connect','meeting','sleep','mct'],119,'Timing and connection checks are plausible itinerary-fit criteria, but they are expressly examples and depend on visa, cost and the actual journey.','A trip with matching host and train schedules, sufficient stopover buffer and acceptable sleep is more likely to fit the plans.','A visa restriction, cancellation or unacceptable price can leave an itinerary unsuitable even when these timing criteria hold.','counterexample'),
 ('deal',['periodic','early','provider','alerts'],25,'These strategies can improve deal finding but cannot jointly ensure a good fare; early booking and alerts are situational alternatives, not a compulsory AND plan.','When comparable fares exist and booking time is flexible, repeated comparisons can reveal a suitable deal.','A fare surge or lack of seats leaves no good deal despite all research; urgent travel may preclude early booking.','counterexample'),
 ('speed',['parallel','consolidate'],137,'Parallel searches and consolidated information address stated effort but are not proven sufficient for all research time or mental effort.','A broad matrix with accurate consolidated details can reduce repetitive visits and search entry.','Slow or stale consolidated results can require manual checking and negate the expected saving.','unknown')],
 'DOC010':[
 ('planning',['clothing','outdoor','trip'],7,'The three explicit planning uses are examples of the broad primary purpose; satisfying them does not establish completeness for every daily decision.','For a day needing only clothing, an activity and a trip decision, weather-informed decisions support planning.','A new decision such as travel mode, or a changing forecast after planning, is not covered by those three results.','counterexample'),
 ('cross',['sync'],71,'App/website synchronization is a specific pair, not demonstrated coverage of every platform.','If the deployment has exactly the app and website, synchronized current data supports consistency.','A voice assistant or another platform may still display stale information while the app and website agree.','counterexample')],
 'DOC013':[
 ('share',['upload','stream'],12,'Upload and live stream are described content-sharing methods, but they are alternatives and their completion does not ensure successful permitted publication.','A valid uploaded video or authorized live stream can make content available for sharing.','An upload can finish but remain unpublished or be prohibited; streaming can be unavailable under the reported wait.','counterexample'),
 ('upload',['format','length'],18,'Format compatibility and length concerns identify possible obstacles but do not ensure successful file transfer.','A compatible acceptable-length file removes two potential upload barriers.','Network failure or missing authorization can still prevent upload.','counterexample')],
 'DOC020':[
 ('miss',['spam','notify','accounts'],59,'Conservative spam handling, reliable alerts and separated accounts can help; the speaker expressly declines reliance when AI can miss importance.','Correct classification and notification of a delivered recruiting message helps the person notice it.','A registration or recruiting email may not arrive at all, or importance detection may miss it, despite those arrangements.','counterexample'),
 ('time',['summary','keywords','digest'],53,'Summaries, highlighting and a tentative batch digest may reduce reading effort but accuracy and completeness are unproven.','An accurate concise summary with salient details can save reading time.','An omitted assessment restriction forces rereading or leads to wasted work; a batch summary may omit a message.','counterexample')],
 'DOC023':[
 ('referral',['search','profile','connect','note','chat'],7,'The outreach workflow is not a sufficient referral plan because the other person may decline or be unable to refer.','A suitable current employee accepts and discusses a relevant opening after outreach.','The person can accept and chat yet decline to refer, or the opening may close.','counterexample')],
 'DOC031':[
 ('instant',['lookup','document','audience','call'],7,'The described features support different communication situations; they are neither universally required together nor sufficient for prompt recipient interaction.','An available university user can be found and sent an immediate message or document.','A recipient may be offline, a channel may be inappropriate, or a call can remain unanswered despite accessible controls.','counterexample')],
 'DOC028':[
 ('better',['subreddit','specific','experience'],61,'Relevant community placement and personal experiences increase value but the source explicitly acknowledges bad responses.','A knowledgeable respondent in the specific community gives a relevant experience-based answer.','The community can provide a bad or unanswered response even after correct placement.','counterexample'),
 ('mobile',['draft','threads'],27,'Two concrete fixes do not cover the stated sluggishness and broader unintuitive mobile interface.','Draft saving and clearer threads remove those two usability frustrations.','The app can remain slow and difficult to navigate after both fixes.','counterexample')],
 'DOC036':[
 ('fraud',['assess','engagement','beforepay'],62,'Engagement heuristics and a payment precaution are risk mitigations, not a complete guarantee against malicious sellers.','A crude malicious account with uniformly low engagement may be recognized, and refusing advance payment avoids that particular loss.','A malicious vendor can imitate engagement or offer a different scam despite those checks.','counterexample'),
 ('gift',['vendor','browse','contact','pay','address'],58,'The shopping steps can support purchase but cannot jointly guarantee a suitable gift arrives; the interview expressly mentions malicious vendors.','A real vendor with a suitable item accepts the order and delivers to the agreed location.','A dishonest vendor can accept payment and an address without delivering, or the selected item may be unsuitable.','counterexample')]
}

def build(doc):
 f=BASE/doc; a=read(f/'final-author-spec.json');keys=a['key_to_goal_id'];rows=a['rows'];bykey={r['key']:r for r in rows}
 records.run(['skills/goal-model-building/scripts/kaos_model.py','template',f/'extraction.json',f/'judgments.json',f/'decisions.json'])
 d=read(f/'decisions.json');write(f/'decisions-template.json',d)
 d['relations']=[];d['groups']=[];d['questions']=[]
 relkeys=[]
 for source,target,kind,turn,reason in R[doc]:
  rid=f'R{len(d["relations"])+1:03}'
  d['relations'].append(dict(relation_id=rid,source_id=keys[source],target_id=keys[target],type=kind,status='supported',conditions=['Only in the source-described scenario; endpoint conditions and defeasible preferences remain applicable.'],assumptions=[],rationale=reason,evidence_ids=[],evidence_quotes=[records.ev(doc,int(turn))]))
  relkeys.append((rid,source,target,kind))
 for parent,children,turn,reason,normal,exception,outcome in GROUPS[doc]:
  gid=f'F{len(d["groups"])+1:03}'; end={parent,*children}
  used=[rid for rid,s,t,k in relkeys if s in end and t in end]
  d['groups'].append(dict(group_id=gid,parent_id=keys[parent],child_ids=[keys[c] for c in children],kind='and',status='proposed',completeness='partial',rationale=reason,assumptions=['Candidate sufficiency assessment only; no complete domain model or formal guarantee is available.'],evidence_ids=[],evidence_quotes=[records.ev(doc,turn)],relation_ids=used,checks=[dict(kind='normal',origin='analysis_assumption',scenario=normal,outcome='supports',rationale='This limited constructed scenario explains why the candidate is plausible; it does not establish general sufficiency.'),dict(kind='exception',origin='analysis_assumption',scenario=exception,outcome=outcome,rationale='The unresolved exception prevents supported/complete status; no extra goal is invented to patch the hierarchy.')]))
  d['questions'].append(dict(target_type='group',target_id=gid,message='Joint sufficiency is unconfirmed: '+reason))
 for q in read(f/'extraction.json')['review_questions']:
  d['questions'].append(dict(target_type='model',target_id=doc+'-goal-model',message=q['question']+' '+q['reason']))
 write(f/'decisions.json',d)
 # Explicit coverage of all four relation meanings, including types with no clear
 # candidate. Unassessed pairs are not represented as rejected records.
 audit={'document_id':doc,'authorship':'same generating assistant; not independent semantic review','relation_pass':{'specialization':'Checked narrower scenarios against broader extracted goals.','operationalization':'Checked stated ways and purposes, preserving optional and conditional adoption.','contribution':'Checked helpful results without treating them as guarantees.','precedes':'Checked only source-described ordering; no causal or refinement entailment assumed.'},'relation_count':len(d['relations']),'group_count':len(d['groups']),'groups_supported_complete':0,'scope':'All authored relation candidates and refinement groups; not an exhaustive all-pairs assessment.','issues':[],'independent_semantic':'not_run','formal_proof':'not_run','human':'pending'}
 if doc=='DOC036':audit['issues'].append({'id':'SR-DOC036-001','target':'model','category':'candidate omission risk','status':'unresolved','reason':'Anonymous posting is not confidently separable from the bundled interviewer paraphrase; browsing is clearly represented.','suggestion':'Seek separate stakeholder confirmation if posting matters.'})
 audit['boundary_cases']=[{'source_id':f'{doc}:T{turn:03}','category':'source/inference or goal-qualification boundary','judgment':reason,'status':'retained as documented exclusion'} for turn,reason in __import__('authoring').EXCLUSIONS[doc]]
 audit['group_findings']=[{'id':f'SR-{doc}-G{i+1:03}','target':g['group_id'],'category':'refinement sufficiency','evidence':g['evidence_quotes'],'basis':g['rationale'],'suggestion':'Keep proposed/partial; do not draw as established refinement.','status':'unresolved','disposition_reason':'No new source evidence establishes sufficiency.'} for i,g in enumerate(d['groups'])]
 write(f/'author-semantic-review.json',audit)
 (f/'author-semantic-review.md').write_text('# Generating-assistant semantic self-check\n\nAll goals were checked against their complete respondent meaning, questions, conditions and exceptions. All four relation types were considered before assessing whole refinement groups. The retained groups have unresolved sufficiency gaps and remain proposed/partial. The constructed normal and exception cases are analysis assumptions, not source facts.\n\nThis record is not independent semantic review, formal proof or human approval. The scope of relation discovery was contextual candidates, not every possible pair. Coverage checks do not prove semantic completeness.\n\n'+ '\n'.join('- '+g['group_id']+': '+g['rationale'] for g in d['groups'])+'\n',encoding='utf-8')
 records.run(['skills/goal-model-building/scripts/kaos_model.py','assemble',f/'extraction.json',f/'judgments.json',f/'source.txt',f/'decisions.json',f/'assembled'])
 records.run(['skills/goal-model-building/scripts/kaos_model.py','inspect',f/'assembled/model-input.json',f/'inspection.json'])
 records.run(['skills/goal-model-building/scripts/kaos_model.py','finalize',f/'assembled/model-input.json',f/'inspection.json',f/'delivery','--svg'])
 print(doc, len(rows),len(d['relations']),len(d['groups']))

if __name__=='__main__':
 for doc in SPECS:build(doc)
