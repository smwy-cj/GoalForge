'use strict';
const model = JSON.parse(document.getElementById('model-data').textContent);
const $ = id => document.getElementById(id);
const svg = $('canvas').querySelector('svg');
svg.setAttribute('role', 'group');
const goals = new Map(model.goals.map(g => [g.goal_id, g]));
const evidence = new Map(model.evidence_index.map(e => [e.evidence_id, e]));
const decisions = new Map(model.pair_decisions.map(p => [p.pair_id, p]));
const shortId = id => '目标 ' + String(model.goals.findIndex(g => g.goal_id === id) + 1).padStart(2, '0');
const labels = {explicit:'显式目标',inferred:'推断目标',design_extension:'设计扩展',pending:'待人工审核',accepted:'已人工采纳',partial:'部分审核',rejected:'未采纳',unchecked:'待审核草案',blocked:'存在阻断问题',reviewable:'可供审核',not_run:'尚未执行',passed:'通过',failed:'未通过',direct:'直接支持',insufficient:'支持不足',contradicted:'存在反证',needs_retrace:'需重新追溯',related:'相关',refinement:'精化',none:'未建立关系',uncertain:'不确定',equivalent:'等价待归并',needs_review:'需要人工检查',reviewed_no_findings:'已审查，未发现问题',reviewed_with_findings:'已审查，存在问题'};
const label = value => labels[value] || value || '未记录';
const ends = edge => edge.type === 'refinement' ? [edge.parent_id, edge.child_id] : [edge.a, edge.b];
const state = {selected:null, decision:null, mode:'all', focus:false, display:matchMedia('(max-width:760px)').matches?'cards':'graph'};
const nodeElements = new Map([...svg.querySelectorAll('[data-node]')].map(n => [n.dataset.node,n]));
let visibleIds = new Set(goals.keys()), view = [0,130,1140,Number(svg.dataset.height)-130], fitWidth = 1140, animation = null, drag = null;
const reducedMotion = matchMedia('(prefers-reduced-motion:reduce)');
const smallScreen = matchMedia('(max-width:760px)');
let displayWasChosen = false;

function element(tag, text, cls) {const node=document.createElement(tag);if(text!==undefined)node.textContent=text;if(cls)node.className=cls;return node;}
function add(parent, tag, text, cls) {const node=element(tag,text,cls);parent.appendChild(node);return node;}
function button(parent, text, action, cls) {const node=add(parent,'button',text,cls);node.addEventListener('click',action);return node;}
function section(parent, title) {const node=add(parent,'section',undefined,'detail-section');add(node,'h3',title);return node;}
function pill(parent,text,cls='') {add(parent,'span',text,'pill '+cls);}
function switchPanel(name) {
  for(const id of ['detail','issues','relations']) {
    $(id+'Panel').hidden = id !== name;
    $(id+'Tab').setAttribute('aria-selected',String(id===name));
  }
  document.querySelector('.inspector').scrollTop=0;
}
// All displayed text is inserted with textContent. Source material never becomes markup.
function locationText(e) {
  const loc=e.original_locator||{}, parts=[];
  if(loc.page!==undefined)parts.push('第 '+loc.page+' 页');
  if(loc.slide!==undefined)parts.push('第 '+loc.slide+' 张幻灯片');
  if(loc.paragraph!==undefined)parts.push('第 '+loc.paragraph+' 段');
  if(loc.line_start!==undefined)parts.push('第 '+loc.line_start+(loc.line_end!==loc.line_start&&loc.line_end!==undefined?'—'+loc.line_end:'')+' 行');
  if(loc.time_start_ms!==undefined)parts.push((loc.time_start_ms/1000).toFixed(1)+'—'+(loc.time_end_ms/1000).toFixed(1)+' 秒');
  if(loc.turn!==undefined)parts.push('访谈轮次 T'+String(loc.turn).padStart(3,'0'));
  return parts.join(' · ') || e.source_id || '原件位置尚未确定';
}
function showEvidence(parent, ids) {
  const box=section(parent,'原文依据');
  if(!ids.length){add(box,'p','尚未提供可核对的原文。');return;}
  add(box,'p','以下保留资料的原始语言，供你对照目标表述。');
  for(const id of ids) {
    const e=evidence.get(id);if(!e)continue;
    const card=add(box,'div',undefined,'quote-card');
    add(card,'div',locationText(e),'quote-label');
    add(card,'div',e.quote,'quote');
    const statuses={native_text:'原生文字',ocr_unverified:'文字识别稿，未经人工核对',transcript_unverified:'录音转写稿，未经人工核对',human_verified:'人工核对过的文字'};
    const status=e.location_status==='exact'?'引文位置已核对':'引文位置待核对';
    add(card,'div',status+' · '+(statuses[e.recognition_status]||'识别状态未记录'),'quote-meta');
    button(card,'审核这段证据',()=>openReview('evidence',id),'text-button');
  }
}
function showOverview() {
  const box=$('detail');box.replaceChildren();
  add(box,'p','READING GUIDE','detail-kicker');
  add(box,'h3','先选一个你关心的目标','detail-title');
  add(box,'p','图中的每张卡片都是一个期望结果。点击后，可以查看它来自哪段原文、是否包含推断，以及与哪些目标有关。','muted');
  button(box,'开始逐项查看',()=>{if(model.goals[0])selectGoal(model.goals[0].goal_id);});
  const intro=section(box,'建议先看什么？');
  button(intro,'先看 '+model.goals.filter(g=>g.origin==='inferred').length+' 个推断目标',()=>filterOrigin('inferred'),'connection-button');
  button(intro,'查看 '+model.issues.length+' 项待确认事项',()=>switchPanel('issues'),'connection-button');
  const meaning=section(box,'关系怎么理解？');
  add(meaning,'p','精化：一个目标是另一个目标有依据的范围或情境具体化。');
  add(meaning,'p','相关：两个目标存在联系，但不能因此认定上下级关系。');
  updateStepper();
}
function renderGoal(id) {
  const g=goals.get(id),box=$('detail');box.replaceChildren();
  add(box,'p',shortId(id)+' · '+id,'detail-kicker');
  add(box,'h3',g.statement,'detail-title');
  const badges=add(box,'div',undefined,'pills');
  pill(badges,label(g.origin),g.origin);pill(badges,label(g.review_status),'pending');
  button(box,'审核这个目标',()=>openReview('goal',id),'primary');
  const status=section(box,'这个目标有多少依据？');
  add(status,'p',({direct:'直接支持',inferred:'推断支持'}[g.trace_status]||label(g.trace_status))+'。'+(g.origin==='inferred'?'它由原资料推断而来，请特别留意下面的假设。':'它保留了资料中的明确表达，仍需对照情境审核。'));
  showEvidence(box,g.evidence_ids);
  if(g.context.length){const context=section(box,'适用情境');for(const item of g.context)add(context,'p',item);}
  const assumptions=(model.assumptions||[]).filter(a=>g.source_candidate_ids.includes(a.candidate_id));
  for(const a of assumptions){const inf=add(box,'div',undefined,'inference-box');add(inf,'strong','这部分包含推断');add(inf,'p',a.reason);for(const assumption of a.assumptions||[])add(inf,'p','需要确认：'+assumption);}
  const links=section(box,'与哪些目标有联系？');
  const pairs=model.pair_decisions.filter(p=>(p.a===id||p.b===id)&&['related','refinement','equivalent','uncertain'].includes(p.label));
  if(!pairs.length)add(links,'p','当前资料未建立可采用的目标联系。这不代表现实中绝无关系。');
  for(const p of pairs){const other=p.a===id?p.b:p.a;const b=button(links,'',()=>showDecision(p.pair_id),'connection-button');add(b,'span',goals.get(other).statement);add(b,'small',label(p.label)+' · 查看判断依据');}
  updateStepper();
}
function selectGoal(id, options={}) {
  if(!goals.has(id))return;
  if(options.reveal){clearFilterValues();state.focus=false;}
  state.selected=id;state.decision=null;renderGoal(id);switchPanel('detail');applyFilters(false);
  if(options.focus){state.focus=true;$('neighbors').setAttribute('aria-pressed','true');applyFilters(true);}
  else if(state.display==='graph'){const b=nodeElements.get(id).getBBox();if(b.x<view[0]||b.y<view[1]||b.x+b.width>view[0]+view[2]||b.y+b.height>view[1]+view[3])animateView([b.x+b.width/2-view[2]/2,b.y+b.height/2-view[3]/2,view[2],view[3]]);}
  if(matchMedia('(max-width:760px)').matches)document.querySelector('.inspector').scrollIntoView({behavior:reducedMotion.matches?'instant':'smooth',block:'start'});
}
function showDecision(id) {
  const p=decisions.get(id);if(!p)return;
  state.decision=id;state.selected=null;state.focus=false;state.mode='all';updateModeButtons();clearFilterValues();
  const box=$('detail');box.replaceChildren();
  add(box,'p','RELATION · '+p.pair_id,'detail-kicker');
  add(box,'h3','这两个目标'+({related:'存在关联',refinement:'构成精化',uncertain:'关系尚不确定',none:'尚未建立关系',equivalent:'可能等价'}[p.label]||'的关系'),'detail-title');
  const badges=add(box,'div',undefined,'pills');pill(badges,label(p.label),p.label==='uncertain'?'inferred':'');pill(badges,'待人工审核','pending');
  button(box,'审核这项关系',()=>openReview('relation',id),'primary');
  const nodes=section(box,'涉及的目标');
  for(const target of [p.a,p.b])button(nodes,goals.get(target).statement,()=>selectGoal(target,{reveal:true}),'connection-button');
  if(p.parent_id)add(nodes,'p','方向：'+shortId(p.parent_id)+' → '+shortId(p.child_id));
  const why=section(box,'为什么这样判断？');add(why,'p',p.rationale);
  if(p.label==='uncertain'||p.label==='none')add(why,'p',p.label==='uncertain'?'依据尚不足，暂不把这项判断绘制成确定连线。':'这里只表示当前资料未建立可采用关系。');
  if(p.conditions?.length){const conditions=section(box,'关系成立的条件');for(const c of p.conditions)add(conditions,'p',c);}
  showEvidence(box,p.evidence_ids||[]);switchPanel('detail');applyFilters(false);updateStepper();if(state.display==='graph')fit(true,new Set([p.a,p.b]));
}
function renderIssues() {
  const box=$('issues');box.replaceChildren();
  if(!model.issues.length)add(box,'p','没有另列待确认事项，但模型仍需按其审核状态使用。','panel-empty');
  for(const [i,issue] of model.issues.entries()) {
    const b=button(box,'',()=>{
      const ids=issue.target_ids||[];
      const pair=ids.length===2?model.pair_decisions.find(p=>new Set([p.a,p.b]).size===2&&ids.includes(p.a)&&ids.includes(p.b)):null;
      if(pair)showDecision(pair.pair_id);else if(ids[0])selectGoal(ids[0],{reveal:true,focus:true});
    },'issue-button');
    add(b,'small',String(i+1).padStart(2,'0')+' · '+(issue.code==='uncertain_relation'?'关系需要确认':'需要核对'));
    add(b,'span',issue.reason||issue.code);
    const names=(issue.target_ids||[]).filter(id=>goals.has(id)).map(shortId);if(names.length)add(b,'small',names.join(' / ')+' · 点击查看');
  }
}
function renderDecisions() {
  const box=$('decisions'),filter=$('relationFilter').value;box.replaceChildren();
  const found=model.pair_decisions.filter(p=>filter==='all'||p.label===filter);
  if(!found.length)add(box,'p','当前模型没有这类关系判断。','panel-empty');
  for(const p of found){const b=button(box,'',()=>showDecision(p.pair_id),'decision-button');add(b,'small',label(p.label)+' · '+shortId(p.a)+' / '+shortId(p.b));add(b,'span',goals.get(p.a).statement+' / '+goals.get(p.b).statement);}
}
function renderCards() {
  const cards=$('cards');cards.replaceChildren();
  for(const g of model.goals.filter(g=>visibleIds.has(g.goal_id))) {
    const b=button(cards,'',()=>selectGoal(g.goal_id),'goal-card '+g.origin+(state.selected===g.goal_id?' selected':''));
    b.setAttribute('aria-label',g.statement);
    const top=add(b,'div',undefined,'pills');pill(top,shortId(g.goal_id));pill(top,label(g.origin),g.origin);
    add(b,'strong',g.statement);add(b,'small',g.evidence_ids.length+' 段原文依据 · '+label(g.review_status));
  }
  if(!visibleIds.size){const box=add(cards,'div',undefined,'panel-empty');add(box,'p','没有匹配的目标。');button(box,'清除筛选',reset);}
}
function edgeAllowed(e){return state.mode==='all'||e.type===state.mode;}
function applyFilters(refit=true) {
  const query=$('search').value.trim().toLowerCase(),origin=$('origin').value;
  const nearby=new Set(state.selected?[state.selected]:[]);
  if(state.selected)for(const edge of model.edges.filter(edgeAllowed)){const [a,b]=ends(edge);if(a===state.selected||b===state.selected){nearby.add(a);nearby.add(b);}}
  visibleIds=new Set(model.goals.filter(g=>(!query||(g.goal_id+' '+shortId(g.goal_id)+' '+g.statement).toLowerCase().includes(query))&&(origin==='all'||g.origin===origin)&&(!$('pending').checked||!reviewEntry('goal',g.goal_id))&&(!state.focus||!state.selected||nearby.has(g.goal_id))).map(g=>g.goal_id));
  const activePair=state.decision?decisions.get(state.decision):null;
  for(const [id,node] of nodeElements){node.classList.toggle('hidden',!visibleIds.has(id));node.classList.toggle('selected',state.selected===id||!!activePair&&[activePair.a,activePair.b].includes(id));node.classList.toggle('dimmed',activePair?![activePair.a,activePair.b].includes(id):!!state.selected&&!state.focus&&!nearby.has(id));}
  let edgeCount=0;
  for(const node of svg.querySelectorAll('[data-edge]')){const edge=model.edges.find(e=>e.edge_id===node.dataset.edge),[a,b]=ends(edge);const show=visibleIds.has(a)&&visibleIds.has(b)&&edgeAllowed(edge);node.classList.toggle('hidden',!show);node.classList.toggle('focused-edge',state.selected===a||state.selected===b);node.classList.toggle('selected-edge',state.decision===edge.decision_id);node.classList.toggle('dimmed',activePair?state.decision!==edge.decision_id:!!state.selected&&!state.focus&&state.selected!==a&&state.selected!==b);if(show)edgeCount++;}
  $('counter').textContent='当前显示 '+visibleIds.size+' / '+model.goals.length+' 个目标 · '+edgeCount+' 条关系';
  $('emptyState').hidden=visibleIds.size>0;
  const refinement=model.edges.filter(e=>e.type==='refinement').length;
  $('graphNotice').textContent=state.focus&&!state.selected?'先选择一个目标，再聚焦它的相邻目标。':state.mode==='refinement'&&!refinement?'当前没有可采用的精化关系，保留所有目标；可切换“全景关系”查看已有联系。':state.mode==='related'?'相关仅表示存在联系，不表示上下级关系。':state.mode==='all'&&!refinement?'这份模型目前以相关联系为主，尚未建立精化层级。':'点击卡片查看原文，点击连线查看关系依据。';
  $('neighbors').setAttribute('aria-pressed',String(state.focus));
  renderCards();updateStepper();
  if(refit&&state.display==='graph'&&visibleIds.size)fit();
}
function clearFilterValues(){$('search').value='';$('origin').value='all';$('pending').checked=false;}
function reset(){clearFilterValues();state.selected=null;state.decision=null;state.focus=false;state.mode='all';updateModeButtons();showOverview();switchPanel('detail');applyFilters();}
function filterOrigin(origin){clearFilterValues();$('origin').value=origin;state.focus=false;state.selected=null;state.decision=null;applyFilters();const first=model.goals.find(g=>visibleIds.has(g.goal_id));if(first)selectGoal(first.goal_id);else showOverview();}
function updateStepper(){const ids=[...visibleIds],index=ids.indexOf(state.selected);$('position').textContent=index>=0?(index+1)+' / '+ids.length:'逐项目标浏览';$('previous').disabled=ids.length===0||index<=0;$('next').disabled=ids.length===0||index===ids.length-1;}
function move(offset){const ids=[...visibleIds];let index=ids.indexOf(state.selected);if(index<0)index=-1;const id=ids[Math.max(0,Math.min(ids.length-1,index+offset))];if(id)selectGoal(id);}
function updateModeButtons(){for(const b of document.querySelectorAll('[data-mode]'))b.setAttribute('aria-pressed',String(b.dataset.mode===state.mode));}
function setDisplay(display,manual=false){if(manual)displayWasChosen=true;state.display=display;$('canvas').hidden=display!=='graph';$('cards').hidden=display!=='cards';$('graphView').setAttribute('aria-pressed',String(display==='graph'));$('cardsView').setAttribute('aria-pressed',String(display==='cards'));$('mobileBack').textContent=display==='cards'?'返回目标清单':'返回目标图';if(display==='graph')fit(false);}
function paint(){svg.setAttribute('viewBox',view.join(' '));$('zoomValue').textContent=Math.round(fitWidth/view[2]*100)+'%';}
function animateView(target,animate=true){if(animation)cancelAnimationFrame(animation);if(!animate||reducedMotion.matches){view=target;paint();return;}const before=[...view],start=performance.now();function frame(now){const t=Math.min(1,(now-start)/230),ease=1-Math.pow(1-t,3);view=target.map((n,i)=>before[i]+(n-before[i])*ease);paint();if(t<1)animation=requestAnimationFrame(frame);else animation=null;}animation=requestAnimationFrame(frame);}
function fit(animate=true,ids=visibleIds){if(!ids.size||state.display!=='graph')return;const bounds=[...nodeElements].filter(([id])=>ids.has(id)).map(([,n])=>n.getBBox());if(!bounds.length)return;const x=Math.min(...bounds.map(b=>b.x))-42,y=Math.min(...bounds.map(b=>b.y))-42,w=Math.max(...bounds.map(b=>b.x+b.width))-x+42,h=Math.max(...bounds.map(b=>b.y+b.height))-y+72;const width=Math.max(w,470),height=Math.max(h,230);fitWidth=width;animateView([x-(width-w)/2,y-(height-h)/2,width,height],animate);}
function zoom(factor){const width=view[2]*factor,height=view[3]*factor;if(width<160||width>16000)return;animateView([view[0]+(view[2]-width)/2,view[1]+(view[3]-height)/2,width,height]);}

for(const [id,node] of nodeElements){const g=goals.get(id);const first=node.querySelector('text');if(first)first.textContent=shortId(id)+' · '+({explicit:'显式',inferred:'推断',design_extension:'设计扩展'}[g.origin]||'来源待确认');node.addEventListener('click',()=>selectGoal(id));node.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();selectGoal(id);}});}
for(const node of svg.querySelectorAll('[data-edge]')){const edge=model.edges.find(e=>e.edge_id===node.dataset.edge);const p=decisions.get(edge.decision_id);node.setAttribute('aria-label',label(p.label)+'：'+goals.get(p.a).statement+' / '+goals.get(p.b).statement);node.addEventListener('click',()=>showDecision(p.pair_id));node.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();showDecision(p.pair_id);}});}
for(const id of ['detail','issues','relations'])$(id+'Tab').addEventListener('click',()=>switchPanel(id));
for(const [index,id] of ['detail','issues','relations'].entries())$(id+'Tab').addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key==='ArrowLeft'){e.preventDefault();const ids=['detail','issues','relations'],next=ids[(index+(e.key==='ArrowRight'?1:2))%3];switchPanel(next);$(next+'Tab').focus();}});
$('previous').onclick=()=>move(-1);$('next').onclick=()=>move(1);$('relationFilter').onchange=renderDecisions;
$('metricAll').onclick=reset;$('metricExplicit').onclick=()=>filterOrigin('explicit');$('metricInferred').onclick=()=>filterOrigin('inferred');$('metricIssues').onclick=()=>switchPanel('issues');
$('graphView').onclick=()=>setDisplay('graph',true);$('cardsView').onclick=()=>setDisplay('cards',true);
$('mobileBack').onclick=()=>document.querySelector('.explorer').scrollIntoView({behavior:reducedMotion.matches?'instant':'smooth',block:'start'});
for(const b of document.querySelectorAll('[data-mode]'))b.addEventListener('click',()=>{state.mode=b.dataset.mode;updateModeButtons();applyFilters();});
$('neighbors').onclick=()=>{state.focus=!state.focus;applyFilters();};$('reset').onclick=reset;$('emptyReset').onclick=reset;
$('search').addEventListener('input',()=>{state.focus=false;applyFilters();if(state.selected&&!visibleIds.has(state.selected)){state.selected=null;state.decision=null;showOverview();applyFilters(false);}});
for(const id of ['origin','pending'])$(id).addEventListener('change',()=>{state.focus=false;applyFilters();if(state.selected&&!visibleIds.has(state.selected)){state.selected=null;showOverview();applyFilters(false);}});
$('zoomIn').onclick=()=>zoom(.8);$('zoomOut').onclick=()=>zoom(1.25);$('fit').onclick=()=>fit();
$('help').onclick=()=>$('helpDialog').showModal();$('closeHelp').onclick=()=>$('helpDialog').close();
function focusWorkspace(active){document.body.classList.toggle('workspace-focused',active);$('focusWorkspace').textContent=active?'退出专注':'专注阅读';$('focusWorkspace').setAttribute('aria-pressed',String(active));window.scrollTo({top:0,behavior:'instant'});requestAnimationFrame(()=>fit(false));}
$('focusWorkspace').onclick=()=>focusWorkspace(!document.body.classList.contains('workspace-focused'));
document.querySelector('.brand').addEventListener('click',e=>{e.preventDefault();reset();});
document.addEventListener('keydown',e=>{if(e.key==='/'&&!['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName)&&!document.querySelector('dialog[open]')){e.preventDefault();$('search').focus();}if(e.key==='Escape'&&!document.querySelector('dialog[open]')&&document.body.classList.contains('workspace-focused'))focusWorkspace(false);});
svg.addEventListener('wheel',e=>{e.preventDefault();zoom(e.deltaY>0?1.12:.89);},{passive:false});
svg.addEventListener('pointerdown',e=>{if(e.target.closest('[data-node],[data-edge]'))return;if(animation)cancelAnimationFrame(animation);drag={x:e.clientX,y:e.clientY,view:[...view]};svg.setPointerCapture(e.pointerId);svg.style.cursor='grabbing';});
svg.addEventListener('pointermove',e=>{if(!drag)return;const ratio=Math.max(drag.view[2]/svg.clientWidth,drag.view[3]/svg.clientHeight);view=[drag.view[0]-(e.clientX-drag.x)*ratio,drag.view[1]-(e.clientY-drag.y)*ratio,drag.view[2],drag.view[3]];paint();});
for(const name of ['pointerup','pointercancel','lostpointercapture'])svg.addEventListener(name,()=>{drag=null;svg.style.cursor='';});
window.addEventListener('resize',()=>fit(false));
smallScreen.addEventListener('change',event=>{if(!displayWasChosen)setDisplay(event.matches?'cards':'graph');});

const docIds=model.document_scope?.document_ids||[];
$('documentName').textContent=(docIds.join(' / ')||model.model_id)+' · 目标模型';
$('subtitle').textContent='从 '+model.goals.length+' 个目标出发，查看它们之间的联系，并回到原文确认每一项判断。';
$('version').textContent=model.version;$('readiness').textContent=label(model.delivery.readiness);
if(model.delivery.readiness==='blocked'){$('noteTitle').textContent='模型存在需要处理的问题';$('noteBody').textContent='可以继续浏览，但请先核对待确认事项，再决定如何采用。';}
if(model.review.status==='accepted'){$('noteTitle').textContent='当前版本已有明确人工认可';$('noteBody').textContent='认可范围与反馈文件见版本记录；人工认可不等于独立语义审查通过。';}else if(model.review.status==='partial'){$('noteTitle').textContent='当前版本已记录部分人工意见';$('noteBody').textContent='单项认可不代表完整模型已获采纳。可以继续填写审核意见。';}
$('goalCount').textContent=model.goals.length;$('explicitCount').textContent=model.goals.filter(g=>g.origin==='explicit').length;$('inferredCount').textContent=model.goals.filter(g=>g.origin==='inferred').length;$('issueCount').textContent=model.issues.length;$('issueBadge').textContent=model.issues.length;
$('modelCaption').textContent=model.edges.filter(e=>e.type==='refinement').length+' 条精化 · '+model.edges.filter(e=>e.type==='related').length+' 条相关 · '+model.pair_decisions.filter(p=>p.label==='uncertain').length+' 对关系待确认';
for(const text of ['模型：'+model.model_id+' · '+model.version,'结构检查：'+label(model.validation.structure_status),'语义审查：'+label(model.validation.semantic_status),'人工审核：'+label(model.review.status),...(model.delivery.limitations||[]),'内容标识：'+model.content_sha256])add($('provenance'),'p',text);
renderIssues();renderDecisions();showOverview();applyFilters(false);setDisplay(state.display);
