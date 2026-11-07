import json
from pathlib import Path
ROOT=Path('output1/revised/_authoring')
LIMITS=['仅处理指定已转写访谈全文；未核听录音，未验证受访者关于产品、价格、组织或技术的事实陈述。','提供材料范围内完成，不代表业务需求穷尽；源索引 native_text 仅表示所提供文本格式，不构成人工核听证明。','语义提取、核验和模型自检由同一生成助手完成；独立语义审查与形式证明未执行，人工决定 pending。','精确模型ID、采样参数和预算未知；继承当前模型配置。现有契约无独立障碍/偏好关系层，相关限制保留在条件、依据和问题中。']
def goal(n,support_label,statement,turn,quote,rationale,context=None,origin='explicit',reason=None,assumptions=None,extra=None):
    doc=DOC
    inf=None if origin=='explicit' else {'basis_candidate_ids':[],'reason':reason,'assumptions':assumptions or []}
    ev=[{'source_id':f'{doc}:T{turn:03d}','quote':quote}]
    for t,q in extra or []:ev.append({'source_id':f'{doc}:T{t:03d}','quote':q,'role':'context'})
    return {'candidate_id':f'{doc}-G{n:02d}','statement':statement,'origin':origin,'actor':'受访者','context':context or [],'inference':inf,'evidence':ev,'support':{'label':support_label,'rationale':rationale,'supported_parts':[statement],'unsupported_parts':[],'assumptions':assumptions or [],'reasoning_steps':[reason or rationale]}}
def group(n,parent,children,turn,quote,rationale,assumptions=None,status='proposed',completeness='partial'):
    return {'group_id':f'{DOC}-F{n:02d}','parent_id':f'{DOC}-G{parent:02d}','child_ids':[f'{DOC}-G{x:02d}' for x in children],'kind':'and','status':status,'completeness':completeness,'rationale':rationale,'assumptions':assumptions or [],'evidence':[{'source_id':f'{DOC}:T{turn:03d}','quote':quote}]}
def question(ids,q,reason):return {'candidate_ids':[f'{DOC}-G{x:02d}' for x in ids],'question':q,'reason':reason}
def save(doc,goals,groups,questions,review,model_questions=None):
    d={'document_id':doc,'status':'completed','limitations':LIMITS,'goals':goals,'groups':groups,'review_questions':questions,'model_questions':model_questions or [],'author_review':review}
    p=ROOT/f'{doc}.json'
    if p.exists():raise FileExistsError(p)
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
