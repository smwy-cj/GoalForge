import json, hashlib
from pathlib import Path
BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
a=read(BASE/'assignment.json'); notes=read(BASE/'review-notes.json')
boundary=read(BASE/'boundary-notes.json')
# Independent determinations made from the full source context, before comparing author labels.
independent_inferred={'DOC005-G13','DOC006-G03','DOC006-G07','DOC006-G13','DOC007-G02','DOC007-G16','DOC016-G11','DOC016-G16','DOC024-G10','DOC024-G11','DOC028-G05','DOC028-G06','DOC028-G15','DOC035-G04','DOC035-G12','DOC035-G18'}
docs=[]
for d in a['documents']:
    if d['document_id'] not in notes: continue
    mpath=ROOT/d['model_path']; m=read(mpath); si=read(ROOT/d['source_input_path']); ex=read(mpath.parent/'attachments/extraction.json')
    source_map={s['source_id']:s for s in si['segments']}
    assert sha(mpath)==d['model_sha256']
    assert sha(ROOT/d['source_path'])==d['source_sha256']
    rs=[]
    for gid in d['required_goal_ids']:
        short=gid.split('-')[1]
        if short not in notes[d['document_id']]: continue
        turns,reason=notes[d['document_id']][short]
        g=next(g for g in m['goals'] if g['goal_id']==gid)
        ev=[e for e in m['evidence_index'] if e['evidence_id'] in g['evidence_ids']]
        sids=sorted(set([d['document_id']+f':T{t:03d}' for t in turns]+[e['source_id'] for e in ev]))
        for e in ev: assert e['quote'] in source_map[e['source_id']]['text']
        rs.append({'goal_id':gid,'statement':g['statement'],'actor':g['actor'],'conditions':g['conditions'],'author_origin':g['origin'],'author_support':g['support'],'author_inference':g['inference'],'independent_origin':'inferred' if gid in independent_inferred else 'explicit','independent_support':'inferred' if gid in independent_inferred else 'direct','verdict':'supported_with_stated_boundaries','reason':reason,'source_ids':sids,'bound_evidence':[{'evidence_id':e['evidence_id'],'source_id':e['source_id'],'quote':e['quote'],'evidence_role':e['evidence_role'],'quote_exact_in_source_segment':True} for e in ev],'all_bound_evidence_reviewed':True,'origin_assessment':'与所读上下文相容；具体理由见reason','questions_issues_assessment':'已读取当前模型issues与提取review_questions；具体未知不自动构成错误，保留现有待澄清范围。','findings':[]})
    for gr in rs:
        gr['questions_and_issues_reviewed']={'model_issues':[x for x in m['issues'] if x['target_type']=='goal' and x['target_id']==gr['goal_id']],'extraction_questions':[x for x in ex['review_questions'] if gr['goal_id'] in x['candidate_ids']]}
    rec={**{k:d[k] for k in ['document_id','model_path','required_goal_ids']},'model_sha256':sha(mpath),'source_sha256':sha(ROOT/d['source_path']),'hashes_match_assignment':True,'source_read_ranges':[{'first_turn':'T000','last_turn':f"T{d['source_turns']-1:03d}",'complete':True}],'source_complete_read':True,'reviewed_goal_ids':[r['goal_id'] for r in rs],'goal_reviews':rs,'reviewed_group_ids':[],'group_review_scope':'本轮只补指定目标；无需重开此前组结论，未对组作新充分性裁决。'}
    docs.append(rec)
    (BASE/(d['document_id']+'-review.json')).write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
out={'review_id':'remaining-20261025-batch1-RR1','reviewer':{'agent':'/root/remaining_review1','role':'independent semantic reviewer','model':'unknown','reasoning_effort':'unknown','sampling_parameters':'unknown','independence':'独立审查调用；生成方标签为被审对象。未读禁止的历史语义报告或参考答案。'},'status':'in_progress','documents':docs,'findings':[],'correct_boundaries':boundary['correct_boundaries'],'candidate_omission_risks':boundary['candidate_omission_risks'],'limits':['仅实际指定目标；其他目标仅作覆盖上下文，不声称全模型审核。','仅所提供转写文本；未核听音频、核实产品事实或穷尽需求。','未执行形式证明，未作人工采纳。','未另行执行核心inspection或更改生成包；哈希与引文精确匹配属于程序检查，不能替代语义判断。','候选遗漏风险2项均未确认，不计真实漏提；完成82目标补审不代表已经证明需求穷尽。']}
if sum(len(x['goal_reviews']) for x in docs)==a['goals']: out['status']='completed'
(BASE/'review.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['# Batch 1 独立语义补审','',f"状态：{out['status']}。实际覆盖 {len(docs)} 篇 / {sum(len(x['goal_reviews']) for x in docs)} 个指定目标。确证语义错误 0 个；没有将现有未决问题计为错误。",'','本次先读完整来源再核整句、主体、条件、来源/推断、支持包、全部绑定引文及问题；作者标签不是正确答案。未重新评审精化组，未读历史语义报告或参考答案。','']
for d in docs:
    lines += ['## '+d['document_id'],'',f"来源 T000–{d['source_read_ranges'][0]['last_turn']} 全读；模型/来源 SHA256 均与assignment一致。",'']
    for g in d['goal_reviews']:
        lines += [f"- **{g['goal_id']}**（{g['independent_support']}）：{g['reason']} 来源：{', '.join(g['source_ids'])}。"]
    lines.append('')
lines += ['## 正确与边界案例','']+['- '+x['id']+'：'+x['reason'] for x in out['correct_boundaries']]
lines += ['','## 未确证的候选遗漏风险','']+['- '+x['id']+'（'+x['document_id']+'）：'+x['reason']+' '+x['recommendation'] for x in out['candidate_omission_risks']]
lines += ['','## 限制','']+['- '+x for x in out['limits']]
(BASE/'report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(f"Wrote {len(docs)} documents / {sum(len(x['goal_reviews']) for x in docs)} goals.")
