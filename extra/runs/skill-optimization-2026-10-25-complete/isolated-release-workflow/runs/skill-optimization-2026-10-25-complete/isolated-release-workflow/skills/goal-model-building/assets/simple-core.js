(function(root){
'use strict';
function empty(binding,model){return {schema_version:model?.schema_version==='goalforge-kaos-2'?'goalforge-simple-feedback-2':'goalforge-simple-feedback-1',model:binding,status:'draft',entries:[],form_drafts:{},note:''};}
function targets(model,kind){return kind==='goal'?model.goals.map(g=>g.goal_id):kind==='group'?model.refinement_groups.map(g=>g.group_id):kind==='relation'&&model.schema_version==='goalforge-kaos-2'?(model.relations||[]).map(r=>r.relation_id):kind==='model'?[model.model_id]:[];}
function validate(packet,model,binding,submit=false){
 const errors=[];
 const expected=model.schema_version==='goalforge-kaos-2'?'goalforge-simple-feedback-2':'goalforge-simple-feedback-1';
 if(!packet||packet.schema_version!==expected||!packet.model||['model_id','version','sha256'].some(k=>packet.model[k]!==binding[k]))return ['审核文件与当前模型版本不一致，当前草稿未改变。'];
 if(!['draft','submitted'].includes(packet.status)||typeof packet.note!=='string'||!Array.isArray(packet.entries)||!packet.form_drafts||typeof packet.form_drafts!=='object'||Array.isArray(packet.form_drafts))return ['审核文件结构无效。'];
 const seen=new Set();
 for(const e of packet.entries){if(!e||!targets(model,e.target_type).includes(e.target_id)){errors.push('意见指向了不存在的目标或层级。');continue;}const key=e.target_type+':'+e.target_id;if(seen.has(key))errors.push('同一项有重复意见。');seen.add(key);if(!['accept','modify','defer'].includes(e.decision)||typeof e.comment!=='string')errors.push('意见格式无效。');else if(e.decision!=='accept'&&!e.comment.trim())errors.push('请说明需要修改或暂不确定的原因。');}
 for(const [key,d] of Object.entries(packet.form_drafts)){if(!d||!targets(model,d.target_type).includes(d.target_id)||key!==d.target_type+':'+d.target_id||!['','accept','modify','defer'].includes(d.decision)||typeof d.comment!=='string')errors.push('未完成表单格式无效。');}
 if(submit&&Object.keys(packet.form_drafts).length)errors.push('有尚未保存的意见，请返回相应目标保存，或选择导出审核草稿。');
 if(submit&&!packet.entries.length&&!packet.note.trim())errors.push('还没有审核意见；可以先审核一项，或选择保存审核草稿。');
 return [...new Set(errors)];
}
function packet(feedback,submit){return {...JSON.parse(JSON.stringify(feedback)),status:submit?'submitted':'draft',exported_at:new Date().toISOString()};}
function summary(feedback,model){return {goals:feedback.entries.filter(e=>e.target_type==='goal').length,total:model.goals.length,groups:feedback.entries.filter(e=>e.target_type==='group').length,groupTotal:model.refinement_groups.length,relations:feedback.entries.filter(e=>e.target_type==='relation').length,relationTotal:(model.relations||[]).length,drafts:Object.keys(feedback.form_drafts).length};}
function markdown(feedback,model){const names={accept:'可以',modify:'需要修改',defer:'暂不确定'};const title=e=>e.target_type==='goal'?model.goals.find(g=>g.goal_id===e.target_id)?.statement:e.target_type==='group'?'目标层级 '+e.target_id:e.target_type==='relation'?'目标联系 '+e.target_id:'整体意见';return '# 审核意见\n\n模型：'+model.model_id+' · '+model.version+'\n状态：'+(feedback.status==='submitted'?'已提交意见包':'草稿')+'（不代表完整模型认可）\n\n'+feedback.entries.map(e=>'## '+title(e)+'\n\n'+names[e.decision]+'\n\n'+(e.comment||'')+'\n').join('\n')+'\n整体补充：'+feedback.note+'\n';}
const api={empty,validate,packet,summary,markdown};if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.SimpleReview=api;
})(typeof globalThis!=='undefined'?globalThis:this);
