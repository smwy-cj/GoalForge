import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
COMMON=['来源为已处理英文访谈文本，已完整读取提供文本；未核听录音，未核验产品事实。','coverage为provided_material，不声称覆盖未提供材料或穷尽需求。','障碍、偏好、信念及方式约束由条件、推断、引文和问题承接；当前契约无独立辅助关系层。','本次语义核验与作者自检由同一助手完成；独立语义审查、形式证明未运行，人工审核pending。','继承当前模型配置；精确模型ID、采样参数和预算unknown。']
def make(doc, rows, overview, relations, scenes, questions=(), groups=()):
    src=json.loads((ROOT/'_inputs'/doc/'source-input.json').read_text(encoding='utf-8-sig'))
    seg={s['source_id']:s['text'] for s in src['segments']}
    goals=[]
    # Each row contains model-authored semantic decisions. This formatter only expands explicitly selected source turns.
    for num,statement,origin,label,turns,context,rationale,assumptions in rows:
        gid=f'{doc}-G{num:02d}'
        ev=[{'source_id':f'{doc}:T{t:03d}','quote':seg[f'{doc}:T{t:03d}']} for t in turns]
        goals.append(dict(candidate_id=gid,statement=statement,origin=origin,actor='受访者',context=context,inference=None if origin=='explicit' else dict(basis_candidate_ids=[],reason=rationale,assumptions=assumptions),evidence=ev,support=dict(label=label,rationale=rationale,supported_parts=[statement] if label in ('direct','inferred') else [],unsupported_parts=[],assumptions=assumptions,reasoning_steps=[rationale])))
    rq=[dict(candidate_ids=[f'{doc}-G{n:02d}' for n in ids],question=q,reason=why) for ids,q,why in questions]
    mq=[dict(target_type='goal' if ids else 'model',target_id=f'{doc}-G{ids[0]:02d}' if ids else f'{doc}-goal-model',message=q+' '+why) for ids,q,why in questions]
    gs=[]
    for g in groups:
        g=dict(g)
        g['parent_id']=f"{doc}-G{g['parent_id']:02d}"
        g['child_ids']=[f'{doc}-G{n:02d}' for n in g['child_ids']]
        g['evidence']=[{'source_id':f'{doc}:T{t:03d}','quote':seg[f'{doc}:T{t:03d}']} for t in g['evidence']]
        gs.append(g)
        if g['status']=='proposed' or g['completeness']=='partial':
            mq.append(dict(target_type='group',target_id=g['group_id'],message='候选组尚未证明共同充分性：'+g['rationale']))
    audit='\n'.join(f"- {g['candidate_id']}：{g['support']['label']}；{g['support']['rationale']} 条件：{'；'.join(g['context']) or '无额外限定'}。保留pending。" for g in goals)
    review=f'# {doc} 生成方语义自检\n\n## 覆盖与执行者\n\n完整读取此文所有问题、回答、后续说明和例外，使用本次冻结修改后三项技能。{overview}\n\n本记录是生成方自检，不是独立评审；实际工程结果见inspection.json。产品描述仅为受访者报告；未核听录音。\n\n## 逐目标核验\n\n{audit}\n\n## 精化及覆盖风险\n\n{relations}\n\n## 正常与异常场景\n\n{scenes}\n\n## 未决与阶段边界\n\n'+('\n'.join('- '+q+' 原因：'+why for ids,q,why in questions) or '没有必须在本次材料内继续循环的问题；目标标准和最终采纳仍需人工审核。')+'\n\n独立语义审查、形式化证明not_run；人工审核pending。所构造场景均为分析假设，不表示访谈事实或穷尽验证。精确模型ID、采样参数、预算unknown；继承当前模型配置。\n'
    obj=dict(document_id=doc,status='completed',limitations=COMMON,goals=goals,review_questions=rq,groups=gs,model_questions=mq,author_review=review)
    p=ROOT/'revised'/'_authoring'/f'{doc}.json'
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(p)
