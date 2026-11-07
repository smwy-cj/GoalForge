/* Pure feedback contract. Also loaded by Node tests; never interprets source as code. */
(function(root,factory){if(typeof module==='object'&&module.exports)module.exports=factory();else root.ReviewFeedback=factory();})(globalThis,function(){
'use strict';
const clone=x=>JSON.parse(JSON.stringify(x));
const actions={goal:['accept','modify','exclude','merge','split','defer'],relation:['accept','modify','defer'],evidence:['sufficient','partial','insufficient','incorrect'],model:['comment','add_goal']};
const changed=e=>!['accept','sufficient','comment'].includes(e.decision);
function empty(binding){const now=new Date().toISOString();return {schema_version:'goalforge-review-feedback-1',feedback_id:'FB-'+(globalThis.crypto?.randomUUID?.()||Date.now().toString(36)+'-'+Math.random().toString(36).slice(2)),base_model:clone(binding),reviewer:{name:''},created_at:now,updated_at:now,status:'draft',entries:[],form_drafts:{},overall:{decision:'undecided',full_scope_ack:false,acknowledge_limits:false,comment:''}};}
function validateImpl(packet,model,binding,submission=false){
 const errors=[];const need=(ok,message)=>{if(!ok)errors.push(message);};
 if(!packet||typeof packet!=='object'||Array.isArray(packet))return ['审核文件必须是对象。'];
 need(packet.schema_version==='goalforge-review-feedback-1','审核文件格式不支持。');
 need(JSON.stringify(packet.base_model&&Object.keys(binding).map(k=>packet.base_model[k]))===JSON.stringify(Object.values(binding)),'审核文件对应的模型版本或内容不一致。');
 need(typeof packet.feedback_id==='string'&&packet.feedback_id.length>0,'缺少反馈编号。');
 need(packet.reviewer&&typeof packet.reviewer.name==='string','审核人信息格式错误。');
 need(['draft','submitted'].includes(packet.status),'审核文件状态错误。');
 need(typeof packet.created_at==='string'&&Number.isFinite(Date.parse(packet.created_at))&&typeof packet.updated_at==='string'&&Number.isFinite(Date.parse(packet.updated_at)),'审核时间格式错误。');
 if(!Array.isArray(packet.entries))return [...errors,'审核项目格式错误。'];
 const ids={goal:new Set(model.goals.map(g=>g.goal_id)),relation:new Set(model.pair_decisions.map(p=>p.pair_id)),evidence:new Set(model.evidence_index.map(e=>e.evidence_id)),model:new Set([model.model_id])};
 const entryIds=new Set(),targets=new Set(),claimed=new Set();
 for(const e of packet.entries){
  if(!e||typeof e!=='object'){errors.push('审核条目格式错误。');continue;}
  need(typeof e.entry_id==='string'&&e.entry_id&&!entryIds.has(e.entry_id),'审核条目编号缺失或重复。');entryIds.add(e.entry_id);
  if(!actions[e.target_type]||!ids[e.target_type].has(e.target_id)){errors.push('审核引用了未知对象。');continue;}
  const key=e.target_type+':'+e.target_id;need(e.target_type==='model'||!targets.has(key),'同一对象存在重复意见。');targets.add(key);
  need(actions[e.target_type].includes(e.decision),'审核选择不支持。');
  need(typeof e.reason==='string','审核理由格式错误。');need(typeof e.reviewed_at==='string'&&Number.isFinite(Date.parse(e.reviewed_at)),'条目审核时间格式错误。');
  const p=e.proposed; if(!p||typeof p!=='object'||Array.isArray(p)){errors.push('修改建议格式错误。');continue;}
  if(!['accept','sufficient'].includes(e.decision))need(Boolean(e.reason?.trim()),'修改、争议或暂不确定意见需要填写理由。');
  if(e.target_type==='goal'){
   let affected=[e.target_id];
   if(e.decision==='modify'||e.decision==='merge')need(typeof p.statement==='string'&&p.statement.trim(),'请填写建议目标表述。');
   if(e.decision==='merge'){need(Array.isArray(p.goal_ids)&&new Set(p.goal_ids).size>=2&&new Set(p.goal_ids).size===p.goal_ids.length&&p.goal_ids.includes(e.target_id)&&p.goal_ids.every(id=>ids.goal.has(id)),'合并需选择至少两个现有目标，包含当前目标。');affected=Array.isArray(p.goal_ids)?p.goal_ids:[];}
   if(e.decision==='split')need(Array.isArray(p.statements)&&p.statements.length>=2&&p.statements.every(s=>typeof s==='string'&&s.trim())&&new Set(p.statements).size===p.statements.length,'拆分需至少两个不同且完整的目标表述。');
   if(!['accept','defer'].includes(e.decision))for(const id of affected){need(!claimed.has(id),'目标修改方案互相冲突。');claimed.add(id);}
  }
  if(e.target_type==='relation'&&e.decision==='modify'){
   need(['refinement','related','equivalent','none','uncertain'].includes(p.label),'请选择有效关系类型。');
   need(Array.isArray(p.conditions)&&p.conditions.every(x=>typeof x==='string'),'关系条件格式错误。');need(typeof p.rationale==='string'&&p.rationale.trim(),'请填写关系判断依据。');
   const pair=model.pair_decisions.find(x=>x.pair_id===e.target_id);if(p.label==='refinement')need(new Set([p.parent_id,p.child_id]).size===2&&[p.parent_id,p.child_id].every(x=>[pair.a,pair.b].includes(x)),'精化方向必须使用当前两个目标。');
  }
  if(e.target_type==='model'&&e.decision==='add_goal'){need(typeof p.statement==='string'&&p.statement.trim(),'请填写新增目标表述。');need(['explicit','inferred'].includes(p.origin),'新增目标需注明显式或推断。');need(Array.isArray(p.evidence_ids)&&p.evidence_ids.length>0&&new Set(p.evidence_ids).size===p.evidence_ids.length&&p.evidence_ids.every(id=>ids.evidence.has(id)),'新增目标需选择已有原文依据；新材料请另行交接。');}
 }
 for(const e of packet.entries)if(e?.target_type==='goal'&&['accept','defer'].includes(e.decision))need(!claimed.has(e.target_id),'该目标的意见与合并或修改方案冲突。');
 const drafts=packet.form_drafts||{};need(drafts&&typeof drafts==='object'&&!Array.isArray(drafts),'未完成表单格式错误。');
 for(const [key,value] of Object.entries(drafts)){const [kind,...rest]=key.split(':');need(ids[kind]?.has(rest.join(':'))&&value&&typeof value==='object'&&!Array.isArray(value)&&Object.values(value).every(v=>typeof v==='string'||Array.isArray(v)&&v.every(x=>typeof x==='string')),'未完成表单引用或内容错误。');}
 const o=packet.overall; if(!o||typeof o!=='object')return [...errors,'整体审核决定缺失。'];
 need(['undecided','accept','request_changes'].includes(o.decision),'整体审核决定错误。');need(typeof o.comment==='string'&&typeof o.full_scope_ack==='boolean'&&typeof o.acknowledge_limits==='boolean','整体审核字段格式错误。');
 if(o.decision==='accept'){need(o.full_scope_ack&&o.acknowledge_limits,'整体认可前需要确认完整范围与检查限制。');need(!packet.entries.some(changed),'仍有修改、争议或暂不确定意见，不能整体认可。');need(model.delivery.readiness==='reviewable'||model.delivery.readiness==='accepted','模型存在阻断问题或尚未检查，不能整体认可。');}
 if(submission){need(Object.keys(drafts).length===0,'还有尚未记录的表单，请保存此项意见或放弃表单修改。');need(packet.status==='submitted','请通过“提交审核并导出”提交。');need(o.decision!=='undecided'||packet.entries.length>0,'请至少填写一项意见或明确整体决定。');}
 return [...new Set(errors)];
}
function validate(packet,model,binding,submission=false){try{return validateImpl(packet,model,binding,submission);}catch(error){return ['审核文件字段格式错误，当前草稿保持不变。'];}}
function upsert(packet,entry){const p=clone(packet);p.form_drafts??={};p.entries=p.entries.filter(e=>e.entry_id!==entry.entry_id&&(entry.target_type==='model'||e.target_type!==entry.target_type||e.target_id!==entry.target_id));p.entries.push(clone(entry));p.status='draft';p.updated_at=new Date().toISOString();if(changed(entry))p.overall.decision='request_changes';return p;}
function summary(packet,model){const count=t=>packet.entries.filter(e=>e.target_type===t).length;return {goals:count('goal'),relations:count('relation'),evidence:count('evidence'),total:model.goals.length+model.pair_decisions.length+model.evidence_index.length,reviewed:count('goal')+count('relation')+count('evidence'),changes:packet.entries.filter(changed).length};}
function markdown(p){const safe=x=>String(x??'').replaceAll('<','&lt;').replaceAll('>','&gt;');return ['# 人工审核意见','',`模型：${safe(p.base_model.model_id)} · ${safe(p.base_model.version)}`,`审核人（自填）：${safe(p.reviewer.name||'未填写')}`,`反馈状态：${p.status}`,`整体决定：${p.overall.decision}`,'','意见提交与模型修改应用是两个步骤。','',...p.entries.flatMap(e=>[`## ${safe(e.target_type)} · ${safe(e.target_id)}`,`选择：${safe(e.decision)}`,`理由：${safe(e.reason)}`,`建议：${safe(JSON.stringify(e.proposed))}`,'']),`整体意见：${safe(p.overall.comment)}`,''].join('\n');}
return {empty,validate,upsert,summary,markdown,changed};
});
