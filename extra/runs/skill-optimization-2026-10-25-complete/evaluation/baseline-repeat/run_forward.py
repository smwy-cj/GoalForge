"""Package manually authored semantic extraction; frozen tools perform actual checks.
No keyword extraction and no model API. Reads only the designated frozen skills and eight raw sources.
"""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
SKILLS = ROOT / 'runs/skill-optimization-2026-10-25-phase1/before/skills'
SOURCE = ROOT / 'datasets/processed/goalforge-v1/source'
DOCS = ['DOC003','DOC010','DOC013','DOC020','DOC023','DOC031','DOC028','DOC036']
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
sys.dont_write_bytecode = True
sys.path.insert(0, str(SKILLS / 'goal-extraction/scripts'))
from trace_candidates import judgment_template

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as f:
        f.write((json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)+'\n').encode('utf-8'))

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

log = []
def command(name, *args):
    cmd = [sys.executable, str(SKILLS / name), *map(str,args)]
    result = subprocess.run(cmd, cwd=ROOT, env=os.environ, capture_output=True, text=True, encoding='utf-8', errors='replace')
    row = dict(command=cmd, returncode=result.returncode, stdout=result.stdout, stderr=result.stderr,
               timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat())
    log.append(row)
    write(OUT / 'command-log' / (str(len(log)).zfill(3)+'.json'), row)
    if result.returncode:
        raise RuntimeError('Frozen command failed; full attempt retained: '+json.dumps(row,ensure_ascii=False))

authoring = read(OUT/'authoring-data.json')
plans = read(OUT/'model-plan.json')
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
skill_files=[]
for name in ['goal-extraction','goal-model-building','model-review']:
    for f in sorted((SKILLS/name).rglob('*')):
        if f.is_file() and '__pycache__' not in f.parts:
            skill_files.append(dict(path=f.relative_to(ROOT).as_posix(),sha256=sha(f.read_bytes())))
execution = dict(schema_version='goalforge-isolated-forward-execution-1', run='baseline-repeat', started_at=started,
    task='冻结三项技能对DOC003/DOC010/DOC013/DOC020/DOC023/DOC031/DOC028/DOC036逐篇前向提取、核验、组判断及待审交付',
    skill_root=SKILLS.relative_to(ROOT).as_posix(), skill_files=skill_files,
    model='unknown',temperature='unknown',token_budget='unknown',actual_tokens='unknown',cost='unknown',
    author='同一助手从本轮八篇原文直接编制目标、支持理由和组判断；本地程序只组织、定位和核验',
    isolation=dict(allowed_sources=[(SOURCE/(d+suffix)).relative_to(ROOT).as_posix() for d in DOCS for suffix in ['.json','.txt']],
        forbidden_read=['论文目标','output','output1','当前skills','tests','比较报告','之前运行','另一分支结果'],
        external_model_api=False,installed_dependencies=False,subagents=False,
        note='本运行上下文隔离不等于统计独立；同一助手作者自检不等于独立语义评审。'),
    full_source_read=dict.fromkeys(DOCS,True), independent_semantic='not_run',formal_proof='not_run',human='pending')
write(OUT/'execution-start.json',execution)
index=[]
supplement={('DOC020',16):[47],('DOC020',20):[73,75],('DOC028',13):[47],('DOC036',7):[52,54],('DOC036',15):[32,52],('DOC003',30):[151,155]}
for doc in DOCS:
    d=OUT/doc
    command('goal-extraction/scripts/prepare_source.py',SOURCE/(doc+'.json'),d,'--canonical-text',SOURCE/(doc+'.txt'))
    source_record=read(SOURCE/(doc+'.json'))
    turns={int(t['turn']):t for t in source_record['turns']}
    source=(d/'source.txt').read_text(encoding='utf-8')
    data=read(d/'source-input.json')
    data.update(schema_version='goalforge-extraction-3',status='completed',candidates=[],review_questions=[],
        limitations=['范围仅为本次提供的完整访谈；未证明业务需求穷尽。','目标资格、支持判断与精化判断由同一助手连续自检，未执行独立语义审查。','现有契约未单独表示障碍、偏好和辅助关系；关键条件保存在目标及引用中，不能声称完整结构化传递。'])
    for n,row in enumerate(authoring[doc],1):
        turn,statement,rationale=row[:3]
        origin=row[3] if len(row)>3 else 'explicit'
        context=row[4] if len(row)>4 else []
        evidence=[]
        for ti in [turn]+supplement.get((doc,n),[]):
            t=turns[ti]
            assert source[t['start_char']:t['end_char']]==t['text']
            evidence.append(dict(source_id=t['source_id'],quote=t['text'],role='basis' if ti==turn else 'context',start_char=t['start_char'],end_char=t['end_char']))
        data['candidates'].append(dict(candidate_id='G'+str(n).zfill(3),statement=statement,origin=origin,
            actor='受访者' if doc!='DOC013' else None,context=context,evidence_candidates=evidence,
            inference=None if origin=='explicit' else dict(basis_candidate_ids=[],reason=rationale,assumptions=['将受访者所述具体使用障碍或有价值能力理解为其相应改善或维持意图，未推定其他用户也相同。']),review_status='pending'))
    write(d/'extraction.json',data)
    judgments=judgment_template(data,(d/'extraction.json').read_bytes())
    write(d/'judgments-template.json',judgments)
    for n,row in enumerate(authoring[doc],1):
        c=data['candidates'][n-1]
        j=judgments['judgments'][c['candidate_id']]
        j.update(label='inferred' if c['origin']=='inferred' else 'direct',rationale=row[2],supported_parts=[c['statement']],unsupported_parts=[],
            assumptions=c['inference']['assumptions'] if c['inference'] else [],
            reasoning_steps=['回读该轮及完整会话，按个人用途、建议强度及上下文判断；没有将采访者未确认提议视作承诺。'])
    write(d/'judgments.json',judgments)
    command('goal-extraction/scripts/trace_candidates.py',d/'extraction.json',d/'tracing','--source',d/'source.txt','--judgments',d/'judgments.json','--review-md')
    command('goal-model-building/scripts/kaos_model.py','template',d/'extraction.json',d/'judgments.json',d/'decisions-template.json')
    decisions=read(d/'decisions-template.json')
    for k,(parent,children,ti,reason,scenario) in enumerate(plans[doc],1):
        t=turns[ti]
        gid='F'+str(k).zfill(3)
        decisions['groups'].append(dict(group_id=gid,parent_id='G'+str(parent).zfill(3),child_ids=['G'+str(c).zfill(3) for c in children],kind='and',status='proposed',completeness='partial',rationale=reason,assumptions=[scenario],evidence_ids=[],evidence_quotes=[dict(source_id=t['source_id'],quote=t['text'],role='basis',start_char=t['start_char'],end_char=t['end_char'])]))
        decisions['questions'].append(dict(target_type='group',target_id=gid,message='整组充分性尚未由原文确立；'+scenario))
    write(d/'decisions.json',decisions)
    command('goal-model-building/scripts/kaos_model.py','assemble',d/'extraction.json',d/'judgments.json',d/'source.txt',d/'decisions.json',d/'assembled')
    command('goal-model-building/scripts/kaos_model.py','inspect',d/'assembled/model-input.json',d/'inspection.json')
    command('goal-model-building/scripts/kaos_model.py','finalize',d/'assembled/model-input.json',d/'inspection.json',d/'delivery')
    report=read(d/'inspection.json')
    model=read(d/'delivery/goal-model.json')
    manifest=read(d/'delivery/manifest.json')
    for entry in manifest['files']:
        assert sha((d/'delivery'/entry['path']).read_bytes())==entry['sha256']
    review=['# '+doc+' 作者语义自检','', '实际逐轮阅读整篇访谈，逐项目标核对主体、语气、否定、条件与来源。没有调用外部LLM。','',
        '当前目标共 '+str(len(data['candidates']))+' 项；精化候选 '+str(len(decisions['groups']))+' 组，均未证明完整充分，因此保持 proposed/partial，不绘成已成立层级。','',
        '正常场景：按各目标引用所述的正常用途，目标与原文的个人任务或期望对应。以下异常检查均为分析假设，非访谈事实，也不是形式证明。','']
    for g in decisions['groups']:
        review.extend(['- '+g['group_id']+'：'+g['rationale']+' '+g['assumptions'][0]])
    review.extend(['','边界处置：排除将纯界面逐按钮讲解自动变成必须需求；已实现且明确有用途或维持意图的能力仍保留。建议与个人偏好未自动变为产品承诺；无新原文可证明充分性，停止组循环并保留待审。','',
        '检查层次：工程检查由冻结 inspect 实际执行；生成方语义自检覆盖全部当前目标与全部候选组。未另作独立语义审查，未执行形式化证明，未收到真实人工意见，human=pending。','',
        '未决：候选组存在未证充分性；目标表达保留原文的个人情境，没有统一可量化验收标准。检查通过不证明提取穷尽。'])
    with (d/'semantic-review.md').open('x',encoding='utf-8',newline='\n') as f:
        f.write('\n'.join(review)+'\n')
    files={}
    for name in ['source.txt','extraction.json','judgments.json','decisions.json','inspection.json','semantic-review.md','delivery/goal-model.json','delivery/goal-model.html','delivery/goal-model.md','delivery/manifest.json']:
        f=d/name
        files[name]=dict(path=f.relative_to(OUT).as_posix(),sha256=sha(f.read_bytes()))
    index.append(dict(document_id=doc,goals=len(model['goals']),groups=len(model['refinement_groups']),supported_complete_groups=sum(g['status']=='supported' and g['completeness']=='complete' for g in model['refinement_groups']),readiness=report['readiness'],structure=report['structure'],human='pending',files=files))
    print(doc, len(model['goals']),len(model['refinement_groups']),report['readiness'],flush=True)
execution.update(completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='completed',command_count=len(log),failures=[r for r in log if r['returncode']],repairs=[],semantic_revision='本轮未修改候选或判断，所有生成与检查使用同一冻结字节版本。')
write(OUT/'execution.json',execution)
write(OUT/'delivery-index.json',dict(schema_version='goalforge-isolated-delivery-index-1',documents=index,note='相对路径基于baseline-repeat；SHA256为实际字节；上下文隔离不等于统计独立。'))
