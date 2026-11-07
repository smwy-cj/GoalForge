# -*- coding: utf-8 -*-
import json,hashlib,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
def loadp(p):return json.loads(p.read_text(encoding='utf-8-sig'))
assignment=loadp(OUT/'assignment.json')
notes=loadp(OUT/'notes.json')
logp=OUT/'consumed-files.json'
log=loadp(logp) if logp.exists() else {}
def read(p):
    p=ROOT/p
    b=p.read_bytes()
    log[p.relative_to(ROOT).as_posix()]={'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
    return b.decode('utf-8-sig'),hashlib.sha256(b).hexdigest()
def obj(p):
    s,h=read(p)
    return json.loads(s),h
def evidence(d,s,turns):
    by={x['source_id']:x for x in s['segments']}
    return [{'source_id':f'{d}:T{t:03d}','speaker':by[f'{d}:T{t:03d}']['speaker'],'quote':by[f'{d}:T{t:03d}']['text']} for t in turns]
ranges={'DOC008':[[0,97]],'DOC013':[[0,49]],'DOC020':[[0,52],[53,103]],'DOC027':[[0,53],[54,110]],'DOC029':[[0,27],[28,55]],'DOC030':[[0,22],[23,45]],'DOC032':[[0,42],[43,83]]}
question_assessments={
    'DOC008-G07':'限制陌生请求的方式未选定；T061–T065只支持担忧与改善方向，因此保留待问，不补全拒绝、验证或黑名单规则。',
    'DOC008-G08':'T063/T065明确未亲历且不知道入侵机制，账号安全范围的问题应保留；不能据此确定漏洞或防护措施。',
    'DOC008-G10':'T089比较其他应用分开菜单，但没有明确选定拆分；应保留具体布局待确认，改善拥挤/发现性的目标仍成立。',
    'DOC013-G10':'格式、长度和发布等待在T018是可能障碍；兼容边界及等待期望待问，不能把疑问改成无长度限制或即时发布。',
    'DOC013-G11':'T006只分部分观众不适宜和全体不可分享两类，未给观众/内容政策边界；保留问题且不宣称合规。',
    'DOC013-G12':'完全禁止分享针对哪些内容未定，explicit language也只是例子；保留政策边界问题，不扩展为全部粗口封禁。',
    'DOC013-G14':'字幕准确性是T040的不确定顾虑，实际问题与改善标准待验证；不填准确率或已确认错误。',
    'DOC013-G15':'T040明确不知道颜色调整能力，保留能力核验和偏好待问；不能将考虑改善当作已证实缺少色盲支持。',
    'DOC020-G09':'发送后编辑愿望明确，但生效客户端、时间窗和历史呈现未给；保留问题而不削成仅撤销窗口。',
    'DOC020-G14':'周期汇总仅是一种方案；T059担心遗漏重要信息，识别可靠性和原文/人工回查方式尚无答案，保留局部问题。',
    'DOC020-G19':'共享类别ID只是未来设想，未说明协调、冲突和不支持客户端处理；应继续待问，不能据8000例子制定协议。',
    'DOC027-G05':'位置是否实际妨碍印度消息和用户如何选择区域均未知；T009的跨地域意图可保留，算法机制仍只是假设。',
    'DOC027-G07':'保留至本人删/归档是明确愿望；政策删除、治理及其他可用性例外未讨论，问题应保留，不能默认为无例外产品承诺。',
    'DOC027-G16':'T103跳过后停播的偏好明确，但停止周期和同类判定未给；两条冰箱广告仅是示例，保留问题不编全局上限。',
    'DOC029-G08':'约一个月窗口已选定；渠道、频率和已开始观看后处理仍待问，不能凭窗口自行补推送策略。',
    'DOC029-G12':'T035给悬停这一可能交互，预览控制和代表片段选择未定；保留待问，不将方案变默认强制自动播放。',
    'DOC029-G15':'T041未描述具体bug，弱改善意图可保留；具体优先修什么仍未知，不能用泛称补造可执行缺陷。',
    'DOC030-G13':'T027只确认修正后等待很烦；可接受间隔和频率保护权衡未给，问题正确保留，不推无限提交。',
    'DOC030-G14':'相同代码跨年反馈波动的原因、公平/稳定评估基准未知；保留问题，不把投诉变成测量必错结论。',
    'DOC030-G16':'用户贡献测试的方式明确，但审核、去重及预期结果质量控制未讨论；保留这些实现问题，不从允许贡献推无审查采纳。',
    'DOC030-G17':'T031明确平台推荐有别于本人目标，推荐所针对经验和统计口径尚无依据；保留待问，不用个人20–30分钟当平台统一标准。',
    'DOC032-G08':'T055的25MB记忆不清，所需文件大小/类型和可接受绕行步骤未定；问题应保留，不据此改产品上限。'
}
documents=[]
sources={}
for d in assignment['documents']:
    did=d['document_id']
    source,sh=read(d['source_path']); s,sih=obj(d['source_input_path']); sources[did]=s
    m,mh=obj(d['model_path']); base=Path(d['model_path']).parent
    ex,eh=obj(base/'attachments/extraction.json')
    judgments,jh=obj(base/'attachments/judgments.json')
    decisions,kh=obj(base/'attachments/kaos-decisions.json')
    manifest,manh=obj(base/'manifest.json')
    attachment_source,ash=read(base/'attachments/source.txt')
    assert mh==d['model_sha256'],(did,'model hash mismatch')
    assert sh==d['source_sha256']==s['document_hash']==ash,(did,'source hash mismatch')
    assert source==attachment_source
    assert len(s['segments'])==d['source_turns']
    # Only supplied canonical text is checked; no product facts or original recordings are assumed.
    for seg in s['segments']:
        line=next(x for x in source.splitlines() if x.startswith('['+seg['source_id'].split(':')[1]+'] '))
        assert line.split(': ',1)[1]==seg['text']
    assert {x['path']:x['sha256'] for x in manifest['files']}['goal-model.json']==mh
    attachments={'attachments/extraction.json':eh,'attachments/judgments.json':jh,'attachments/source.txt':ash,'attachments/kaos-decisions.json':kh}
    assert all(next(x['sha256'] for x in manifest['files'] if x['path']==p)==h for p,h in attachments.items())
    assert all(next(x['sha256'] for x in m['input_artifacts'] if x['path']==p)==h for p,h in attachments.items())
    assert decisions['input_binding']['extraction_sha256']==eh
    assert decisions['input_binding']['judgments_sha256']==jh
    exby={x['candidate_id']:x for x in ex['candidates']}
    mb={x['goal_id']:x for x in m['goals']}
    jby=judgments['judgments']
    reviews=[]
    for gid in d['required_goal_ids']:
        n=notes[did][str(int(gid.split('-G')[1]))]
        label,turns,reason=n
        g=mb[gid]; c=exby[gid]; j=jby[gid]
        assert g['statement']==c['statement']==j['target_statement']
        assert g['actor']==c['actor'] and g['conditions']==c['context'] and g['origin']==c['origin'] and g['inference']==c['inference']
        for k,v in g['support'].items():assert j[k]==v,(gid,k)
        bound=[e for e in m['evidence_index'] if e['evidence_id'] in g['evidence_ids']]
        assert len(bound)==len(g['evidence_ids'])
        sb={x['source_id']:x for x in s['segments']}
        for e in bound:
            assert e['quote'] in sb[e['source_id']]['text']
            assert source[e['start_char']:e['end_char']]==e['quote']
        reqqs=[q for q in ex.get('review_questions',[]) if gid in q.get('candidate_ids',[])]
        issues=[i for i in m.get('issues',[]) if i.get('target_id')==gid]
        reviews.append({
            'goal_id':gid,'statement':g['statement'],'actor':g['actor'],'conditions':g['conditions'],
            'origin':g['origin'],'inference':g['inference'],'author_support':g['support'],
            'independent_support_label':label,'independent_verdict':'supported','reason':reason,
            'author_label_agreement':label==g['support']['label'],
            'source_ids':[f'{did}:T{t:03d}' for t in turns],
            'source_evidence':evidence(did,s,turns),'all_bound_evidence':bound,
            'questions_reviewed':reqqs,'issues_reviewed':issues,
            'questions_assessment':question_assessments.get(gid,'本目标没有绑定待问条目；具体边界见独立理由。'),
            'counts_as_confirmed_semantic_error':False,'local_blocking_scope':[]
        })
    assert len(reviews)==len(d['required_goal_ids'])==len(notes[did])
    assert set(r['goal_id'] for r in reviews)==set(d['required_goal_ids'])
    documents.append({
        'document_id':did,'model_path':d['model_path'],'model_sha256':mh,'source_path':d['source_path'],'source_sha256':sh,
        'source_input_path':d['source_input_path'],'source_input_sha256':sih,'assignment_hashes_match':True,
        'source_read_ranges':[{'start_source_id':f'{did}:T{a:03d}','end_source_id':f'{did}:T{b:03d}','inclusive':True} for a,b in ranges[did]],
        'source_turns':len(s['segments']),'source_complete_read':True,'source_read_before_model':True,
        'reviewed_goal_ids':[r['goal_id'] for r in reviews],'required_goal_ids':d['required_goal_ids'],'goal_reviews':reviews,
        'reviewed_group_ids':[],
        'group_scope_note':'精化组为此前轮次范围；本轮读取包中组/问题仅作上下文，不声称重新审结该组或未指定目标。',
        'package_binding_checks':{'source_projection_matches':True,'bound_quotes_exact_against_canonical_source':True,'goal_extraction_judgment_fields_match':True,'attachments_match_model_and_manifest':True},
        'status':'completed'
    })
for p in [
    '_run/skill-snapshots/revised/skills/model-review/SKILL.md',
    '_run/skill-snapshots/revised/skills/model-review/references/semantic-review.md',
    '_run/skill-snapshots/revised/skills/goal-extraction/references/goal-boundaries.md',
    '_run/skill-snapshots/revised/skills/goal-extraction/references/evidence-rules.md',
    '_run/skill-snapshots/revised/skills/goal-model-building/references/modeling-rules.md',
    'review/remaining-20261025/batch2/assignment.json'
]:read(p)
finding={
    'finding_id':'RR2-001','category':'expression_insufficiency','severity':'low','goal_ids':['DOC029-G02'],
    'model_path':'revised/DOC029/v1/delivery/goal-model.json',
    'source_evidence':evidence('DOC029',sources['DOC029'],[13,15,43]),
    'reason':'G02的整句由完整来源直接支持。现有绑定E0002/T013与E0003/T015只展示兴趣和当天心情，情境价值的T043在作者理由中提及但尚未绑定为证据；这是证据呈现可改善，不是该子项没有原文依据。',
    'recommendation':'可补T043一段连续原文为context/basis证据，保留现有目标、direct标签和组；另存版本并重绑字节。',
    'status':'open_at_initial_v1_review','counts_as_confirmed_semantic_error':False,'local_blocking_scope':[]
}
boundary_ids={
    'DOC008':[3,4,8,9,10], 'DOC013':[7,8,10,14,15,16],
    'DOC020':[7,9,11,14,17,18,19], 'DOC027':[5,6,7,8,9,11,13,15,16],
    'DOC029':[2,3,6,8,12,14,16], 'DOC030':[4,5,8,9,10,13,14,17,18,19,20],
    'DOC032':[1,2,4,5,6,7,8]
}
boundaries=[]
for did,ns in boundary_ids.items():
    for n in ns:
        label,ts,reason=notes[did][str(n)]
        boundaries.append({'goal_ids':[f'{did}-G{n:02d}'],'reason':reason,'source_ids':[f'{did}:T{t:03d}' for t in ts],'disposition':'retain_current_semantics'})
omission={
    'risk_id':'RR2-C01','document_id':'DOC030','status':'unconfirmed_candidate_only',
    'source_evidence':evidence('DOC030',sources['DOC030'],[17]),
    'candidate_intent':'看解并练习后，隔一段时间重做同一道题，以确认没有遗忘。',
    'existing_coverage_checked':['DOC030-G05','DOC030-G08','DOC030-G20'],
    'existing_goal_statement_scope':'已查看该模型全部20个现有statement核对覆盖；只有assignment的18项目标进行了完整语义审查。',
    'reason':'T017明确强调回到同一道题防遗忘。G05覆盖看解理解，G08覆盖少量简单/中等题回顾，G20覆盖选题，可能由G08承担，但对看解后同一难题的隔时重做尚未明确。',
    'recommendation':'先确认G08是否有意承接这一具体回顾方式，可考虑补条件；未确认前不新增节点。',
    'counts_as_confirmed_semantic_error':False,'counts_as_confirmed_omission':False,'local_blocking_scope':[]
}
result={
    'review_id':'remaining-20261025-batch2','reviewer':{'agent':'/root/remaining_review2','role':'独立来源先读语义复核者','model':'unknown','model_settings':{'exact_model_id':'unknown','sampling_parameters':'unknown','reasoning_budget':'unknown'}},
    'status':'completed_with_nonsemantic_improvement_and_unconfirmed_coverage_risk',
    'independence':{'read_author_review':False,'read_prior_semantic_reviews':False,'read_reference_answers':False,'read_other_batches':False,'author_support_role':'被审对象，不作为正确答案','source_first_checkpoints':'source-baseline.md'},
    'documents':documents,'findings':[finding],'correct_boundaries':boundaries,'candidate_omission_risks':[omission],
    'coverage':{'documents':len(documents),'required_goals':sum(len(d['required_goal_ids']) for d in documents),'reviewed_goals':sum(len(d['goal_reviews']) for d in documents),'reviewed_groups':0,'source_turns':sum(d['source_turns'] for d in documents),'confirmed_semantic_error_findings':0,'distinct_confirmed_error_goals':0,'nonsemantic_improvement_findings':1,'unconfirmed_omission_risks':1},
    'evidence_layers':{'byte_binding_checks':'run_for_listed_files_only','author_self_assessment':'reviewed_as_object','independent_semantic_review':'completed_for_90_required_goal_ids','formal_proof':'not_run','human_review':'not_run','human_adoption':'pending'},
    'limits':['只覆盖本assignment指定90目标，不声称把该7篇所有112个目标都完整复核。','完整阅读提供的549轮标准来源；未核听录音、未验证产品实际功能、法规、市场或算法事实。','没有新增节点、修改生成包、来源、技能或核心inspection。','组记录可读作上下文，本轮没有重新审结精化组。','未知事实、实现可行性及用户取舍仍按具体目标保留，不构成整篇blocked。','全量补审并不等于人工审核、形式证明或真实采纳。','DOC008最初source-input重复文本输出有截断；实际source.txt全98轮完整可见，后续程序逐段比对source-input映射与全文一致。']
}
assert result['coverage']['reviewed_goals']==assignment['goals']==90
assert result['coverage']['source_turns']==sum(x['source_turns'] for x in assignment['documents'])
(OUT/'review.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
logp.write_text(json.dumps(log,ensure_ascii=False,indent=2),encoding='utf-8')
lines=['# Batch 2 独立语义补审','',
    '已完成7篇提供来源的全部549轮阅读，逐项审查assignment指定90个目标。确认实质语义错误0项；证据呈现改善1项；候选遗漏风险1项尚未确证。未改生成包。','',
    '本轮先完整来源后当前目标语义，再查看作者origin/inference/support及问题。作者字段只是被审对象。精化组仅作上下文，本轮不声称重新审结。逐目标完整字段、全部绑定引文、实际回查问答及实测哈希详见review.json。','',
    '|资料|实际来源轮次|目标覆盖|模型SHA256|','|---|---|---:|---|']
for d in documents:lines.append(f"|{d['document_id']}|T000–T{d['source_turns']-1:03d}|{len(d['goal_reviews'])}/{len(d['required_goal_ids'])}|{d['model_sha256']}|")
lines+=['','## RR2-001：证据呈现可改善，非语义错误','',finding['reason'],'',finding['recommendation'],
    '', '初审状态：v1中尚未补绑定；本轮整句判direct，未判insufficient。父代理可另存修订版后再做局部复查。',
    '', '## RR2-C01：未确认的回顾方式覆盖风险','',omission['reason'],'',omission['recommendation'],
    '', '## 逐目标结论','']
for d in documents:
    lines+=['### '+d['document_id'],'']
    for r in d['goal_reviews']:
        lines += [f"- **{r['goal_id']}（{r['independent_support_label']}）** {r['statement']}  ",f"  {r['reason']} 回查："+'、'.join(r['source_ids'])+'。']
    lines.append('')
lines+=['## 范围与限制','']+[f'- {x}' for x in result['limits']]
(OUT/'report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps(result['coverage'],ensure_ascii=False))
print('all_required_ids_exactly_once=true; all_assignment_hashes_match=true; all_bound_quotes_exact=true')
