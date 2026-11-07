'use strict';
const $=id=>document.getElementById(id),payload=JSON.parse($('payload').textContent),model=payload.model,bound=payload.binding;
const goals=new Map(model.goals.map(g=>[g.goal_id,g])),groups=new Map(model.refinement_groups.map(g=>[g.group_id,g])),evidence=new Map(model.evidence_index.map(e=>[e.evidence_id,e]));
const relations=new Map((model.relations||[]).map(r=>[r.relation_id,r]));
const relationTypes={specialization:'范围具体化',operationalization:'实现方式',contribution:'有助于',precedes:'过程先后'},relationStates={supported:'有依据的联系',proposed:'待确认联系',rejected:'已否定联系'};
const key='goalforge-simple-feedback:'+bound.sha256;
let feedback=SimpleReview.empty(bound,model),storageProblem='',selected=null,pendingImport=null,exportSnapshot=null,busy=false,display='dag',dagScale=1;
try{const raw=localStorage.getItem(key);if(raw){const data=JSON.parse(raw);const errors=SimpleReview.validate(data,model,bound);if(errors.length)storageProblem='旧草稿未恢复：'+errors.join(' ');else feedback=data;}}catch(e){storageProblem='浏览器草稿无法保存，请及时导出或复制意见。';}
function add(parent,tag,text,cls){const el=document.createElement(tag);if(text!==undefined)el.textContent=text;if(cls)el.className=cls;parent.appendChild(el);return el;}
function button(parent,text,handler,cls){const el=add(parent,'button',text,cls);el.type='button';el.onclick=handler;return el;}
function persist(){feedback.status='draft';try{localStorage.setItem(key,JSON.stringify(feedback));storageProblem='';}catch(e){storageProblem='浏览器草稿未保存，请立即导出或复制。';}progress();}
function progress(){const s=SimpleReview.summary(feedback,model);$('progress').textContent=`目标已记录 ${s.goals}/${s.total} · 层级已记录 ${s.groups}/${s.groupTotal}${model.relations?' · 联系已记录 '+s.relations+'/'+s.relationTotal:''}`;$('saveStatus').textContent=storageProblem||`草稿保存在当前浏览器${s.drafts?'，有 '+s.drafts+' 项未完成意见':''}。导出后交回助手。`;}
function entry(kind,id){return feedback.entries.find(e=>e.target_type===kind&&e.target_id===id);}
function goalIssues(id){return model.issues.filter(i=>i.target_type==='goal'&&i.target_id===id);}
function isActive(group){return group.status==='supported'&&group.completeness==='complete';}
const byParent=new Map();for(const group of groups.values())if(isActive(group)){if(!byParent.has(group.parent_id))byParent.set(group.parent_id,[]);byParent.get(group.parent_id).push(group);}
function renderOutline(){
 $('outline').replaceChildren();const children=new Set([...byParent.values()].flat().flatMap(g=>g.child_ids)),seen=new Set(),query=$('search').value.trim();
 function node(id,parent,depth=0){
  const g=goals.get(id),card=add(parent,'article',undefined,'goal'+(selected?.kind==='goal'&&selected.id===id?' selected':''));card.dataset.goalId=id;
  button(card,g.statement,()=>openDetail('goal',id),'goalTitle');const meta=add(card,'div',undefined,'goalMeta');
  if(goalIssues(id).length||g.origin==='inferred')add(meta,'span','需确认','tag');
  const e=entry('goal',id);add(meta,'span',e?({accept:'已记录：可以',modify:'已记录：需修改',defer:'已记录：暂不确定'}[e.decision]):'点开查看依据并审核');
  if(seen.has(id)){add(card,'p','同一目标，也出现在其他层级；意见会同步。','muted shared');return;}seen.add(id);
  if(!query&&byParent.has(id)){
   const alternatives=byParent.get(id),details=add(card,'details');details.open=depth<1;add(details,'summary',`查看下一级目标${alternatives.length>1?'与替代方案':''}`);
   const nested=add(details,'div',undefined,'children');alternatives.forEach((group,i)=>{const section=add(nested,'section',undefined,'group');const head=add(section,'div',undefined,'groupHeader');add(head,'strong',alternatives.length>1?`方案 ${i+1}：任选一个完整方案；以下各项都需满足`:'以下各项都需满足');button(head,entry('group',group.group_id)?'查看层级意见':'审核这组层级',()=>openDetail('group',group.group_id));for(const child of group.child_ids)node(child,section,depth+1);});
  }
 }
 const roots=query?model.goals.filter(g=>g.statement.includes(query)).map(g=>g.goal_id):model.goals.filter(g=>!children.has(g.goal_id)).map(g=>g.goal_id);for(const id of roots)node(id,$('outline'));
 if(!roots.length)add($('outline'),'p',query?'没有匹配的目标，请更换关键词。':'本次可读资料中没有提取到目标。','notice');
 $('hierarchyHint').textContent=query?'搜索结果仅列匹配目标；清空搜索可恢复层级。':byParent.size?'展开查看具体目标，点击文字查看原文。共享目标会标明重复引用。':'当前资料尚未建立可靠的目标层级，以下目标独立列出。';
 document.querySelectorAll('.dag-node').forEach(n=>n.classList.toggle('selected',!!selected&&(n.dataset.goal===selected.id||n.dataset.group===selected.id)));
}
function drawDag(){
 $('dagCanvas').innerHTML=payload.svg;
 const graphic=$('dagCanvas').querySelector('svg');
 graphic.querySelectorAll('[data-goal],[data-group]').forEach(n=>{const kind=n.dataset.goal?'goal':'group',id=n.dataset.goal||n.dataset.group;n.onclick=()=>openDetail(kind,id);n.onkeydown=e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();openDetail(kind,id);}};});
 if(!byParent.size&&model.goals.length)$('dagLegend').textContent='当前尚未建立有依据的层级，各项目标独立展示。点击目标查看原文并审核。';
 fitDag();
}
function scaleDag(){const graphic=$('dagCanvas').querySelector('svg');if(!graphic)return;graphic.style.width=(Number(graphic.getAttribute('width'))*dagScale)+'px';graphic.style.height='auto';}
function fitDag(){const graphic=$('dagCanvas').querySelector('svg');if(!graphic)return;dagScale=Math.min(1,Math.max(.2,($('dagCanvas').clientWidth-8)/Number(graphic.getAttribute('width'))));scaleDag();}
function switchView(kind){display=kind;$('dagCanvas').hidden=$('dagTools').hidden=$('dagLegend').hidden=kind!=='dag';$('outline').hidden=$('hierarchyHint').hidden=kind!=='list';$('relationsPanel').hidden=kind!=='relations';$('searchBox').hidden=kind!=='list'||model.goals.length<12;$('relationsView').setAttribute('aria-pressed',String(kind==='relations'));$('dagView').setAttribute('aria-pressed',String(kind==='dag'));$('listView').setAttribute('aria-pressed',String(kind==='list'));if(kind==='dag')fitDag();}
function renderQuestions(){
 $('questions').replaceChildren();const seen=new Set();for(const i of model.issues){const q=i.target_type+':'+i.target_id+':'+i.message;if(seen.has(q))continue;seen.add(q);const b=button($('questions'),i.message,()=>openDetail(i.target_type,i.target_id),'question');add(b,'small','点开核对并给意见');}$('questionsSection').hidden=!seen.size;
}
function evidenceBlock(parent,refs){
 const items=refs.map(id=>evidence.get(id)).filter(Boolean);if(!items.length){add(parent,'p','当前未找到可查看的原文依据。','notice');return;}
 function show(p,e){add(p,'blockquote',e.quote);let location=Object.entries(e.original_locator||{}).filter(([k])=>!['start_char','end_char'].includes(k)).map(([k,v])=>({paragraph:'段落',page:'页码',slide:'幻灯片',turn:'轮次',line_start:'起始行',line_end:'结束行'}[k]||k)+' '+v).join(' · ');add(p,'small',location||e.source_id);if(!['native_text','human_verified'].includes(e.recognition_status))add(p,'p','这段依据来自识别稿，尚需核对原件。','notice');}
 show(parent,items[0]);if(items.length>1){const d=add(parent,'details');add(d,'summary',`其他 ${items.length-1} 段依据`);items.slice(1).forEach(e=>show(d,e));}
}
function openDetail(kind,id){
 selected={kind,id};$('emptyReader').hidden=true;$('detail').hidden=false;const panel=$('detail');panel.replaceChildren();
 button(panel,'返回目标模型',()=>{const target=$(display==='dag'?'dagCanvas':display==='relations'?'relationsPanel':'outline');target.scrollIntoView({block:'start'});target.querySelector('[role=button],button')?.focus();},'backOutline');
 let title,refs=[];
 if(kind==='goal'){
  const g=goals.get(id);title=g.statement;add(panel,'h2',title);if(g.conditions.length)add(panel,'p','适用条件：'+g.conditions.join('；'),'conditions');if(g.actor)add(panel,'p','目标主体：'+g.actor,'muted');
  if(g.origin==='inferred'){add(panel,'p','这项目标根据原文推断，请确认是否符合原意。','notice');if(g.inference){add(panel,'p',g.inference.reason);if(g.inference.assumptions?.length)add(panel,'p','推断条件：'+g.inference.assumptions.join('；'));}}
  refs=g.evidence_ids;
 }else if(kind==='group'){
  const g=groups.get(id);title='这组层级是否合理？';add(panel,'h2',title);add(panel,'p','上层目标：'+goals.get(g.parent_id).statement);add(panel,'strong','以下各项在说明的条件下共同满足上层目标：');const list=add(panel,'ul');g.child_ids.forEach(gid=>add(list,'li',goals.get(gid).statement));add(panel,'p',g.rationale);if(g.assumptions.length)add(panel,'p','适用条件：'+g.assumptions.join('；'),'conditions');if(!isActive(g))add(panel,'p','这是待确认的层级建议，未作为成立的精化展开。','notice');refs=g.evidence_ids;if(g.checks?.length){const checks=add(panel,'details');add(checks,'summary','正常与异常场景检查');for(const c of g.checks)add(checks,'p',(c.kind==='normal'?'正常场景':'异常场景')+' · '+(c.origin==='source'?'来自原文':'分析假设')+'：'+c.scenario+'；'+({supports:'在所述范围内支持',counterexample:'存在反例',unknown:'尚未确定'}[c.outcome])+'。'+c.rationale);}
 }else if(kind==='relation'){
  const r=relations.get(id);title=relationTypes[r.type];add(panel,'h2',title);add(panel,'p',relationStates[r.status],'notice');add(panel,'p','起点：'+goals.get(r.source_id).statement);add(panel,'p','终点：'+goals.get(r.target_id).statement);add(panel,'p',r.rationale);if(r.conditions.length)add(panel,'p','适用条件：'+r.conditions.join('；'));if(r.assumptions.length)add(panel,'p','分析假设：'+r.assumptions.join('；'));add(panel,'p','这项联系单独审核，不代表充分精化。','muted');refs=r.evidence_ids;
 }else{title='整体与遗漏意见';add(panel,'h2',title);add(panel,'p','请说明缺了什么、哪里不清楚，或需要回查哪段资料。');}
 const relevant=model.issues.filter(i=>i.target_type===kind&&i.target_id===id);for(const i of relevant)add(panel,'p',i.message,'notice');
 if(refs.length){add(panel,'h3','原文依据');evidenceBlock(panel,refs);}
 const form=add(panel,'form');const field=add(form,'fieldset',undefined,'choices');add(field,'legend',kind==='group'?'你对这组层级的判断':'你的判断');const draftKey=kind+':'+id,original=feedback.form_drafts[draftKey]||entry(kind,id)||{decision:'',comment:''};
 const radios=[];for(const [value,text] of [['accept','可以'],['modify','需要修改'],['defer','暂不确定']]){const label=add(field,'label'),input=add(label,'input');input.type='radio';input.name='decision';input.value=value;input.checked=original.decision===value;add(label,'span',text);radios.push(input);}
 const label=add(form,'label','意见或原因（需修改／暂不确定时填写）');label.htmlFor='opinion';const comment=add(form,'textarea');comment.id='opinion';comment.rows=3;comment.value=original.comment;comment.placeholder='用自己的话说明即可。';
 const message=add(form,'p','意见保存后仍需导出交回助手。','muted');message.setAttribute('role','status');
 function stage(){feedback.form_drafts[draftKey]={target_type:kind,target_id:id,decision:radios.find(r=>r.checked)?.value||'',comment:comment.value};persist();}
 radios.forEach(r=>r.onchange=stage);comment.oninput=stage;
 const actions=add(form,'div',undefined,'editorActions');const save=add(actions,'button','保存意见','primary');save.type='submit';
 button(actions,'撤回本项意见',()=>{feedback.entries=feedback.entries.filter(e=>e.target_type!==kind||e.target_id!==id);delete feedback.form_drafts[draftKey];persist();renderOutline();openDetail(kind,id);});
 form.onsubmit=e=>{e.preventDefault();const decision=radios.find(r=>r.checked)?.value;if(!decision||(decision!=='accept'&&!comment.value.trim())){message.textContent='请选择判断；需要修改或暂不确定时，请填写原因。';if(!decision)radios[0].focus();else comment.focus();return;}feedback.entries=feedback.entries.filter(e=>e.target_type!==kind||e.target_id!==id);feedback.entries.push({target_type:kind,target_id:id,decision,comment:comment.value});delete feedback.form_drafts[draftKey];persist();renderOutline();message.textContent='本项意见已记录。未审核内容保持待审，请导出后交回助手。';};
 renderOutline();$('reader').scrollIntoView({block:'nearest'});panel.querySelector('h2').tabIndex=-1;panel.querySelector('h2').focus({preventScroll:true});
}
function options(list){$('exportType').replaceChildren();list.forEach(([v,t])=>{const o=add($('exportType'),'option',t);o.value=v;});}
function openExport(mode='feedback'){
 options(mode==='model'?[['model-json','模型 JSON'],['model-md','简短说明 Markdown'],['model-svg','目标层级 SVG'],...(model.relations?[['relations-svg','目标联系 SVG']]:[])]:[['feedback','正式审核意见 JSON'],['draft','审核草稿 JSON'],['feedback-md','可读意见摘要 Markdown']]);
 $('exportType').value=mode==='draft'?'draft':mode==='model'?'model-json':'feedback';$('exportHeading').textContent=mode==='model'?'导出模型文件':'导出审核意见';prepareExport();$('exportDialog').showModal();
}
function prepareExport(){
 const type=$('exportType').value,packet=SimpleReview.packet(feedback,type==='feedback');let text,mime='application/json',extension='json',errors=[];
 if(type==='feedback'||type==='draft'){errors=SimpleReview.validate(packet,model,bound,type==='feedback');text=JSON.stringify(packet,null,2)+'\n';}
 else if(type==='feedback-md'){text=SimpleReview.markdown(SimpleReview.packet(feedback,false),model);mime='text/markdown';extension='md';}
 else if(type==='model-json')text=JSON.stringify(model,null,2)+'\n';
 else if(type==='model-md'){text=payload.markdown;mime='text/markdown';extension='md';}
 else{text=type==='relations-svg'?payload.relations_svg:payload.svg;mime='image/svg+xml';extension='svg';}
 const name=(type==='relations-svg'?'goal-relations':type.startsWith('model-')?'goal-model':type==='draft'?'review-feedback-draft':'review-feedback')+'-'+model.model_id.replace(/[^a-zA-Z0-9_-]/g,'_')+'-'+model.version.replace(/[^a-zA-Z0-9._-]/g,'_')+'-'+new Date().toISOString().replace(/[:.]/g,'-')+'.'+extension;
 exportSnapshot={text,mime,name,errors,kind:type};$('exportInfo').textContent=`${name} · ${new Blob([text]).size} 字节`;$('exportError').textContent=errors.join(' ');$('errorLinks').replaceChildren();
 if(errors.length)for(const draft of Object.values(feedback.form_drafts))button($('errorLinks'),'返回未完成意见',()=>{$('exportDialog').close();openDetail(draft.target_type,draft.target_id);});
 $('saveFile').disabled=$('copyFile').disabled=$('showContent').disabled=$('saveAs').disabled=!!errors.length;$('saveAs').hidden=typeof window.showSaveFilePicker!=='function';$('exportText').value=text;$('manualCopy').hidden=true;$('confirmSaved').hidden=true;$('exportStatus').textContent=errors.length?'可切换到“审核草稿 JSON”先保存进度。':'保存或复制后，请把审核意见交回助手。';
}
function showText(message){$('manualCopy').hidden=false;$('exportStatus').textContent=message;$('exportText').focus();$('exportText').select();}
$('saveFile').onclick=async()=>{
 if(busy||!exportSnapshot||exportSnapshot.errors.length)return;busy=true;$('saveFile').disabled=true;const snapshot=exportSnapshot;
 try{const configNode=$('local-save-config');if(configNode){const config=JSON.parse(configNode.textContent);const response=await fetch(config.endpoint,{method:'POST',headers:{'Content-Type':'application/json','X-GoalForge-Token':config.token},body:JSON.stringify({kind:snapshot.kind,content:snapshot.text}),credentials:'omit'});const receipt=await response.json();if(!response.ok)throw new Error(receipt.error||'本地保存失败');$('exportStatus').textContent='文件已实际保存：'+receipt.path+'（'+receipt.bytes+' 字节）。请将审核意见交回助手。';}
 else{const url=URL.createObjectURL(new Blob([snapshot.text],{type:snapshot.mime+';charset=utf-8'})),a=document.createElement('a');a.href=url;a.download=snapshot.name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),60000);$('exportStatus').textContent='已发起浏览器下载，请检查下载列表；未收到文件时可复制或查看文本。';$('confirmSaved').hidden=false;}}
 catch(e){showText(e.name==='AbortError'?'保存已取消，内容仍保留。你也可以复制或手动保存。':'保存未完成：'+e.message+'。请复制或手动保存完整内容。');}
 finally{busy=false;$('saveFile').disabled=false;}
};
$('saveAs').onclick=async()=>{if(busy||!exportSnapshot||exportSnapshot.errors.length)return;busy=true;$('saveAs').disabled=true;try{const handle=await window.showSaveFilePicker({suggestedName:exportSnapshot.name});const writable=await handle.createWritable();await writable.write(exportSnapshot.text);await writable.close();$('exportStatus').textContent='文件已写入所选位置。审核意见仍需交回助手。';}catch(e){showText(e.name==='AbortError'?'保存已取消，内容仍保留，可复制或手动保存。':'无法写入所选位置：'+e.message+'。请复制或手动保存。');}finally{busy=false;$('saveAs').disabled=false;}};
$('copyFile').onclick=async()=>{if(!exportSnapshot||exportSnapshot.errors.length)return;try{await navigator.clipboard.writeText(exportSnapshot.text);$('exportStatus').textContent='完整内容已复制，可直接粘贴给助手；这不代表模型已经修改。';}catch(e){showText('无法自动复制，请在下方全选并复制完整内容。');}};
$('showContent').onclick=()=>showText('下方是完整导出内容，可全选复制，或另存为 UTF-8 文件。');
$('confirmSaved').onclick=()=>{$('exportStatus').textContent='已记录你确认文件保存。请将审核意见交回助手。';$('confirmSaved').hidden=true;};
$('exportType').onchange=prepareExport;$('closeExport').onclick=()=>$('exportDialog').close();$('exportFeedback').onclick=()=>openExport();$('exportDraft').onclick=()=>openExport('draft');$('modelFiles').onclick=()=>openExport('model');
$('reviewFirst').onclick=()=>{const goal=model.goals.find(g=>!entry('goal',g.goal_id))||model.goals[0];if(goal)openDetail('goal',goal.goal_id);else openDetail('model',model.model_id);};
$('importButton').onclick=()=>{pendingImport=null;$('confirmImport').disabled=true;$('importFile').value='';$('importStatus').textContent='替换前建议先导出当前草稿。';$('importDialog').showModal();};$('closeImport').onclick=()=>$('importDialog').close();
$('importFile').onchange=async()=>{pendingImport=null;$('confirmImport').disabled=true;try{const file=$('importFile').files[0];if(!file)return;if(file.size>5*1024*1024)throw new Error('文件超过 5MB，请确认选择的是审核 JSON。');const data=JSON.parse(await file.text());const errors=SimpleReview.validate(data,model,bound,data.status==='submitted');if(errors.length)throw new Error(errors.join(' '));pendingImport=data;$('importStatus').textContent=`版本一致，包含 ${data.entries.length} 项意见；确认后替换当前草稿。`;$('confirmImport').disabled=false;}catch(e){$('importStatus').textContent=e.message+' 当前草稿保持不变。';}};
$('confirmImport').onclick=()=>{if(!pendingImport)return;feedback=JSON.parse(JSON.stringify(pendingImport));persist();$('overallNote').value=feedback.note;$('importDialog').close();renderOutline();if(selected)openDetail(selected.kind,selected.id);};
$('overallNote').value=feedback.note;$('overallNote').oninput=()=>{feedback.note=$('overallNote').value;persist();};$('search').oninput=renderOutline;$('searchBox').hidden=true;
$('relationsView').hidden=model.schema_version!=='goalforge-kaos-2';$('relationsView').onclick=()=>switchView('relations');
$('dagView').onclick=()=>switchView('dag');$('listView').onclick=()=>switchView('list');$('zoomIn').onclick=()=>{dagScale=Math.min(2.5,dagScale*1.25);scaleDag();};$('zoomOut').onclick=()=>{dagScale=Math.max(.2,dagScale/1.25);scaleDag();};$('fitDag').onclick=fitDag;
window.addEventListener('resize',()=>{if(display==='dag')fitDag();});
$('version').textContent=model.version;$('scope').textContent=`${model.scope.document_id} · ${model.goals.length} 个目标。原文依据保留在各项目标旁。`;
if(model.limitations.length||payload.report.readiness==='blocked'){$('limitations').hidden=false;$('limitations').textContent=(payload.report.readiness==='blocked'?'部分目标仍有依据问题，请优先核对。 ':'')+model.limitations.join(' ');}
const technical=$('technical');add(technical,'p',`模型 ${model.model_id} · ${model.version}。结构及原文版本已核验；独立语义审查与形式证明未执行，人工待审。`);add(technical,'p',`完整记录：${model.goals.length} 个目标、${model.refinement_groups.length} 个精化组、${model.evidence_index.length} 段依据。没有评估全部两两关系，也不把未评估当作无关系。`);
const records=add(technical,'ul');for(const group of model.refinement_groups)button(add(records,'li'),'查看层级记录 '+group.group_id,()=>openDetail('group',group.group_id));button(technical,'导出当前模型文件',()=>openExport('model'));
window.addEventListener('beforeunload',e=>{if(storageProblem&&(feedback.entries.length||Object.keys(feedback.form_drafts).length||feedback.note)){e.preventDefault();e.returnValue='';}});
function renderRelations(){
 $('relationsList').replaceChildren();for(const r of relations.values()){
  const card=add($('relationsList'),'article',undefined,'relationCard '+r.status);card.dataset.relationId=r.relation_id;
  add(card,'strong',relationStates[r.status]+' · '+relationTypes[r.type]);
  const endpoints=add(card,'p');button(endpoints,goals.get(r.source_id).statement,()=>openDetail('goal',r.source_id));add(endpoints,'span',' → ');button(endpoints,goals.get(r.target_id).statement,()=>openDetail('goal',r.target_id));
  add(card,'p',r.rationale);button(card,'查看依据与审核联系',()=>openDetail('relation',r.relation_id));
 }if(!relations.size)add($('relationsList'),'p','当前没有提交目标联系；不表示已排除所有可能联系。');
}
renderRelations();drawDag();renderOutline();renderQuestions();progress();
