"""Serialize authored semantics and execute installed skill tools, retaining every attempt.
No semantic extraction is done by this script: judgments live in semantic-specs.py
and the separately preserved full-context corrections file.
"""
import copy, hashlib, json, os, pathlib, runpy, subprocess, sys, time
from datetime import datetime, timezone

ROOT=pathlib.Path(__file__).resolve().parent
PROJECT=pathlib.Path.cwd().resolve()
DOC_ORDER=['DOC003','DOC010','DOC013','DOC020','DOC023','DOC031','DOC028','DOC036']
EX=PROJECT/'skills/goal-extraction/scripts'
KAOS=PROJECT/'skills/goal-model-building/scripts/kaos_model.py'
LOG=ROOT/'operation-logs'
LOG.mkdir(exist_ok=True)

def now(): return datetime.now(timezone.utc).isoformat()
def digest(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def read(p): return json.loads(pathlib.Path(p).read_text(encoding='utf-8-sig'))
def put(p,obj):
    p=pathlib.Path(p)
    with p.open('x',encoding='utf-8',newline='\n') as f:
        json.dump(obj,f,ensure_ascii=False,indent=2,allow_nan=False)
        f.write('\n')
def md(p,s):
    with pathlib.Path(p).open('x',encoding='utf-8',newline='\n') as f: f.write(s)
def run(args,label):
    stamp=now(); start=time.monotonic()
    env=os.environ.copy(); env['PYTHONUTF8']='1'; env['PYTHONIOENCODING']='utf-8'
    cp=subprocess.run([sys.executable]+[str(a) for a in args],cwd=PROJECT,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace')
    idx=len(list(LOG.glob('*.json')))+1
    put(LOG/f'{idx:03d}-{label}.json',{'started_at':stamp,'elapsed_seconds':round(time.monotonic()-start,4),
        'argv':[sys.executable]+[str(a) for a in args],'cwd':str(PROJECT),'returncode':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr})
    print(label,cp.returncode,flush=True)
    if cp.returncode:
        print(cp.stdout,cp.stderr,flush=True)
        raise RuntimeError(f'{label} failed; retained inputs and actual log; no overwrite or automatic semantic repair')
    return cp

def evidence(source,turn,role='basis'):
    sid=f"{source['document_id']}:T{turn:03d}"
    seg=next(s for s in source['segments'] if s['source_id']==sid)
    return {'source_id':sid,'quote':seg['text'],'role':role,
        'start_char':seg['original_locator']['start_char'],'end_char':seg['original_locator']['end_char']}

def loadspec(corrected=False):
    s=runpy.run_path(str(ROOT/'semantic-specs.py'))['DOCS']
    if corrected: runpy.run_path(str(ROOT/'semantic-corrections.py'))['apply'](s)
    return s

def loaded_skills():
    paths=[]
    references={
      'goal-extraction':['input-processing','extraction-strategy','goal-boundaries','coverage-contract','output-contract','evidence-rules','semantic-judgments','tracing-contract'],
      'goal-model-building':['relation-discovery','modeling-rules','output-contract','tools'],
      'model-review':['tools','output-contract','semantic-review']}
    for skill,refs in references.items():
        paths.append(PROJECT/f'skills/{skill}/SKILL.md')
        paths.extend(PROJECT/f'skills/{skill}/references/{r}.md' for r in refs)
    # Actual entry points and local imported implementation. No tests or data examples.
    paths.extend(EX/n for n in ['prepare_source.py','check_coverage.py','trace_candidates.py','simple_candidates.py','render_review.py'])
    paths.append(KAOS)
    result=[{'path':str(p),'relative_path':p.relative_to(PROJECT).as_posix(),'sha256':digest(p)} for p in paths]
    return result

def capture():
    specs=loadspec()
    put(ROOT/'execution-start.json',{'started_at':now(),'resume_note':'Recovered retained source preparation and semantic compilation after interruption; no restart or baseline selection.',
        'agent_role':'candidate-repeat','actual_model':'unknown','temperature':'unknown','budget':'unknown','usage_tokens':'unknown','cost':'unknown',
        'scope':'Eight named source JSON/TXT files and only the three named installed skills; output limited to this directory.',
        'context':'Source-only generation context isolated from answers and other branch outputs; all passes within this agent share context. Context isolation does not establish statistical independence.',
        'source_preparation_receipt':'Before interruption the actual prepare_source.py command for all eight documents returned exit code 0; generated files retained.',
        'external_llm_api':False,'dependencies_installed':False,'subagents_spawned':False,'skill_files':loaded_skills()})
    for d in DOC_ORDER:
        p=ROOT/d; src=read(p/'source-input.json'); windows=read(p/'source-windows.json')
        run([EX/'check_coverage.py','capture-template','--source-input',p/'source-input.json','--source',p/'source.txt','--windows',p/'source-windows.json','--output',p/'raw-candidates-template.json'],d+'-capture-template')
        raw=read(p/'raw-candidates-template.json'); cids={}
        for t,item in sorted(specs[d]['captures'].items()):
            ev=evidence(src,t); cid=f'C{len(raw["candidates"])+1:03d}'; cids[str(t)]=cid
            wid=next(w['window_id'] for w in windows['windows'] if ev['source_id'] in w['source_ids'])
            raw['candidates'].append({'candidate_id':cid,'statement':ev['quote'],'actor':next(s['speaker'] for s in src['segments'] if s['source_id']==ev['source_id']),
                'modality':'原句保留其习惯、偏好、建议、条件及不确定性；候选资格尚未裁定。','context':[],
                'origin':'unknown','pass_id':'P1-local-capture','window_ids':[wid],'evidence_candidates':[ev]})
        put(p/'raw-candidates.json',raw)
        put(p/'capture-turn-index.json',cids)
    print('Raw candidates frozen. Next stage uses preserved full-context semantic corrections.',flush=True)

def build():
    specs=loadspec(corrected=True)
    changes=[
      {'document_id':'DOC010','change':'将极端天气推迟活动与不外出两个独立结果拆开；原始引文候选保留。'},
      {'document_id':'DOC028','change':'移动应用易用性与运行流畅度分别核验；不按多个形容词机械拆字段。'},
      {'document_id':'DOC020','change':'删除不属于候选精化组内部端点的依赖声明R008；原联系本身仍保留。'},
      {'document_id':'DOC036','change':'新地方商家信息对检索为贡献而非同一动作的具体化；混合附和的匿名发帖含义留待确认。'}]
    put(ROOT/'author-corrections.json',{'stage':'full-context author self-review before first extraction','human_feedback':'not_received','changes':changes,
        'original_semantic_compilation':{'path':'semantic-specs.py','sha256':digest(ROOT/'semantic-specs.py')},
        'correction_program':{'path':'semantic-corrections.py','sha256':digest(ROOT/'semantic-corrections.py')}})
    skillmanifest=loaded_skills()
    skillhash=hashlib.sha256(json.dumps(skillmanifest,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
    for d in DOC_ORDER:
        p=ROOT/d; authored=specs[d]; src=read(p/'source-input.json'); windows=read(p/'source-windows.json'); raw=read(p/'raw-candidates.json'); cids=read(p/'capture-turn-index.json')
        # Stable IDs follow the preserved initial compilation; newly split goals append.
        ids={k:f'G{i:03d}' for i,k in enumerate(authored['goals'],1)}
        put(p/'goal-id-map.json',ids)
        extraction=copy.deepcopy(src)
        extraction.update(schema_version='goalforge-extraction-3',status='completed',
            coverage={'scope':'provided_material','source_ids':[s['source_id'] for s in src['segments']],'omissions':[]},
            candidates=[],review_questions=[],limitations=[
              '本次读取提供的原始转写JSON与标准全文；未核对录音，不修正原文口误或未经证实的技术/商业事实。',
              '局部捕获、全文校正、支持判断及语义自检由同一助手在共享上下文完成；不是独立评审、形式证明或人工采纳。',
              '未预设目标、联系或精化组数量；未建立成立精化不等于已排除所有可能精化。',
              'extraction-ledger与覆盖报告单独审计；当前模型组装工具不消费该附件。'])
        for k,a in authored['goals'].items():
            inferred=a['origin']=='inferred'
            extraction['candidates'].append({'candidate_id':ids[k],'statement':a['statement'],'origin':a['origin'],'actor':'Stakeholder',
                'context':a['context'],'evidence_candidates':[evidence(src,a['turn'])]+[evidence(src,t,'context') for t in a['extra']],
                'inference':{'basis_candidate_ids':[],'reason':a['rationale'],'assumptions':['该处描述的困难或可选改善表达了受访者所期待的相应结果；不推断唯一实现。']} if inferred else None,
                'review_status':'pending'})
        if d=='DOC013':
            extraction['review_questions'].append({'candidate_ids':[ids['restrict'],ids['prohibit']],'question':'哪些观众与内容需要限制、哪些内容禁止任何发布，原文没有给出完整判据。','reason':'不据显式语言例子擅自定义法规、年龄或内容规则。'})
        if d=='DOC020':
            extraction['review_questions'].append({'candidate_ids':[ids['protocol']],'question':'自定义类别标识如何在双方客户端互通仍未明确。','reason':'原文自身称可能不实际；不把设想视为已定协议。'})
        if d=='DOC036':
            extraction['review_questions'].append({'candidate_ids':[],'question':'混合复述后的yes是否还意指匿名发帖尚不清楚；目前仅提取明确的匿名浏览。','reason':'T071包含匿名浏览、匿名发帖及恶意账户多个成分，T072无法区分。'})
        put(p/'extraction.json',extraction)
        run([EX/'check_coverage.py','template','--source-input',p/'source-input.json','--source',p/'source.txt','--windows',p/'source-windows.json','--candidates',p/'raw-candidates.json','--extraction',p/'extraction.json','--output',p/'extraction-ledger-template.json'],d+'-ledger-template')
        ledger=read(p/'extraction-ledger-template.json')
        ledger['run'].update(model='unknown',temperature='unknown',budget='unknown',usage={'tokens':'unknown','cost':'unknown'},skill_revision=skillhash,
            prompt_revision='candidate-repeat source-only task; exact hidden/system model settings unknown',planned_passes=2,
            stop_reason='完成一次局部捕获、一次全文条件/例外与拆合校正及当前支持核验；无外部新证据，不对相同未决语义重复循环。',
            passes=[{'pass_id':pid,'kind':kind,'context':'shared','status':'completed',
              'window_results':[{'window_id':w['window_id'],'status':'processed','reason':reason} for w in windows['windows']]}
              for pid,kind,reason in [('P1-local-capture','initial','按重叠轮次范围捕获重要意图/含混候选；该窗未必有候选。'),
                ('P2-full-context','full_context','全文回查指代、问答、条件、例外和独立核心结果；同一上下文，不是新增独立采样。')]])
        ledger['full_context_review']={'status':'completed','source_ids':[s['source_id'] for s in src['segments']],
            'reason':'已完整读取全部原轮次；回查主要目的、通常策略、可让步偏好、背景事实、跨轮条件和相反例子。按独立意图拆合并逐项编制支持理由。'}
        entries=[]; checks=[]; seen=set()
        for t,a in sorted(authored['captures'].items()):
            gids=[ids[k] for k in a['keys']]; cid=cids[str(t)]
            uncertain=a.get('uncertain',False)
            disposition='uncertain' if uncertain else 'exclude' if not gids else 'split' if len(gids)>1 else 'merge' if gids[0] in seen else 'keep'
            entries.append({'candidate_id':cid,'disposition':disposition,'final_goal_ids':gids,'reason':a['reason']})
            checks.append({'check_id':f'SC{len(checks)+1:03d}','evidence_candidates':[evidence(src,t)],'candidate_ids':[cid],
                'final_goal_ids':gids,'outcome':'uncertain' if uncertain else 'represented' if gids else 'excluded','reason':a['reason']})
            seen.update(gids)
        ledger['entries']=entries; ledger['source_checks']=checks
        ledger['limitations']=['处理完所有窗口与去向记录不证明语义穷尽；检查器的semantic_completeness固定为not_assessed。',
          '重叠窗口共享同一完整转写与作者上下文；本分支未读答案或其他运行结果，但隔离不代表统计独立。']
        put(p/'extraction-ledger.json',ledger)
        run([EX/'check_coverage.py','check','--source-input',p/'source-input.json','--source',p/'source.txt','--windows',p/'source-windows.json','--candidates',p/'raw-candidates.json','--extraction',p/'extraction.json','--ledger',p/'extraction-ledger.json','--output',p/'coverage-check.json'],d+'-coverage')
        run([EX/'trace_candidates.py',p/'extraction.json','--judgment-template',p/'judgments-template.json'],d+'-judgment-template')
        js=read(p/'judgments-template.json')
        for k,a in authored['goals'].items():
            js['judgments'][ids[k]].update(label='inferred' if a['origin']=='inferred' else 'direct',rationale=a['rationale'],
                supported_parts=[a['statement']],unsupported_parts=[],assumptions=extraction['candidates'][list(ids).index(k)]['inference']['assumptions'] if a['origin']=='inferred' else [],
                reasoning_steps=['回查该轮及所列后续说明，核对主体、情境、强度与选定方式；'+a['rationale']])
        put(p/'judgments.json',js)
        run([EX/'trace_candidates.py',p/'extraction.json',p/'tracing','--source',p/'source.txt','--judgments',p/'judgments.json','--review-md'],d+'-trace')
        run([KAOS,'template',p/'extraction.json',p/'judgments.json',p/'decisions-template.json'],d+'-decisions-template')
        decisions=read(p/'decisions-template.json')
        for i,r in enumerate(authored['relations'],1):
            decisions['relations'].append({'relation_id':f'R{i:03d}','source_id':ids[r['a']],'target_id':ids[r['b']],
                'type':r['type'],'status':r['status'],'conditions':r['conditions'],'assumptions':r['assumptions'],
                'rationale':r['rationale'],'evidence_ids':[],'evidence_quotes':[evidence(src,r['turn'])]})
        for i,a in enumerate(authored['groups'],1):
            gid=f'FG{i:03d}'
            decisions['groups'].append({'group_id':gid,'parent_id':ids[a['parent']],'child_ids':[ids[k] for k in a['children']],
                'kind':'and','status':'supported' if a['supported'] else 'proposed','completeness':'complete' if a['supported'] else 'partial',
                'rationale':a['rationale'],'assumptions':['场景仅为作者概念层检查，不是形式化充分性证明。'],
                'evidence_ids':[],'evidence_quotes':[evidence(src,a['turn'])],
                'relation_ids':[f'R{r+1:03d}' for r in a['refs']],
                'checks':[{'kind':'normal','origin':'analysis_assumption','scenario':a['normal'],'outcome':'supports','rationale':'在所述条件下可解释这些子目标如何服务父目标；不扩大到所有场景。'},
                    {'kind':'exception','origin':'analysis_assumption','scenario':a['exception'],'outcome':'supports' if a['supported'] else 'counterexample',
                     'rationale':'未解决的充分性缺口保留候选；不补造根、额外前提目标或完整性。'}]})
            if not a['supported']:
                decisions['questions'].append({'target_type':'group','target_id':gid,'message':a['rationale']+' 异常场景：'+a['exception']})
        put(p/'decisions.json',decisions)
        # All four types considered. No fixed number of edges, groups, or roots is imposed.
        put(p/'relation-discovery.json',{'document_id':d,'scope':'同一问答、目的/方法、条件和跨轮指代；未穷举全部目标对。',
            'types':[{'type':typ,'relation_ids':[r['relation_id'] for r in decisions['relations'] if r['type']==typ],
               'result':'保存实际有依据的联系及明确候选/否定；未列目标对为未评估，不补写无关系。'}
               for typ in ['specialization','operationalization','contribution','precedes']],
            'relations_file':'decisions.json','refinements':'只有整组充分才可成立；本次有反例/完整性未知者均保留proposed/partial。'})
        lines=['# 生成方语义自检', '', '执行者为当前生成助手；与提取/核验共享上下文。独立语义审查 not_run，形式证明 not_run，人工审核 pending。',
            '', '已完整核对本次全部目标、候选处置、全部联系与精化组。程序检查仅验证记录/文件一致性，不证明意图穷尽。', '', '## 目标与粒度', '']
        for k,a in authored['goals'].items():
            lines.append(f"- {ids[k]}：{a['statement']} 核对：{a['rationale']}"+(' 条件：'+'；'.join(a['context']) if a['context'] else ''))
        lines+=['','## 联系与精化场景','']
        for r in decisions['relations']:
            lines.append(f"- {r['relation_id']} {r['source_id']} → {r['target_id']} / {r['type']} / {r['status']}：{r['rationale']}")
        for a in decisions['groups']:
            lines.append(f"- {a['group_id']}：{a['rationale']} 正常场景：{a['checks'][0]['scenario']} 异常/反例：{a['checks'][1]['scenario']} 状态 {a['status']}/{a['completeness']}。")
        lines+=['','## 覆盖与未决','']+[f"- T{t:03d}：{a['reason']}" for t,a in sorted(authored['captures'].items()) if not a['keys'] or a.get('uncertain')]
        lines+=['','未确认的匿名发帖、协议细节、内容限制边界等只在相关文档问题中保留；没有真实用户反馈，不生成认可记录。','']
        md(p/'semantic-review.md','\n'.join(lines))
        run([KAOS,'assemble',p/'extraction.json',p/'judgments.json',p/'source.txt',p/'decisions.json',p/'assembled'],d+'-assemble')
        run([KAOS,'inspect',p/'assembled/model-input.json',p/'inspection.json'],d+'-inspect')
        run([KAOS,'finalize',p/'assembled/model-input.json',p/'inspection.json',p/'delivery','--svg'],d+'-finalize')
    finish()

def finish():
    summaries=[]
    for d in DOC_ORDER:
        p=ROOT/d; m=read(p/'delivery/goal-model.json'); cov=read(p/'coverage-check.json'); ins=read(p/'inspection.json')
        from collections import Counter
        summaries.append({'document_id':d,'goals':len(m['goals']),'raw_candidates':cov['counts']['raw_candidates'],
            'support':dict(Counter(g['support']['label'] for g in m['goals'])),
            'relations':len(m['relations']),'relation_status':dict(Counter(r['status'] for r in m['relations'])),
            'relation_types':dict(Counter(r['type'] for r in m['relations'])),
            'groups':len(m['refinement_groups']),'supported_complete_groups':sum(g['status']=='supported' and g['completeness']=='complete' for g in m['refinement_groups']),
            'coverage_structure':cov['structure'],'coverage_workflow':cov['workflow'],'semantic_completeness':cov['semantic_completeness'],
            'uncertain_candidate_ids':cov['uncertain_candidate_ids'],'model_inspection':ins,
            'source_txt_sha256':digest(p/'source.txt'),'source_json_sha256':digest(PROJECT/f'datasets/processed/goalforge-v1/source/{d}.json')})
    logs=[read(p) for p in sorted(LOG.glob('*.json'))]
    start=read(ROOT/'execution-start.json')
    execution={**start,'completed_at':now(),'status':'completed','documents':DOC_ORDER,'summary':summaries,
        'operations':{'completed_tool_commands':len(logs),'failed_tool_commands':sum(x['returncode']!=0 for x in logs),
          'failure_policy':'All actual failed commands and their unchanged inputs are retained; no best-of selection.',
          'tool_log_directory':'operation-logs'},
        'source_read_scope':'All eight full standard transcripts and source JSON source-only projections; long terminal truncation repaired by reading omitted source ranges before semantic compilation.',
        'semantic_authoring':'Current assistant compiled every selected goal, candidate disposition, support rationale, relation and normal/exception scenario; scripts serialize those judgments and validate actual artifacts, not keyword extraction.',
        'review_layers':{'author_self_review':'completed','independent_semantic':'not_run','formal_proof':'not_run','human':'pending'},
        'limitations':['Exact model/temperature/budget/token/cost unknown.','Context isolation from answers and other branches does not establish statistical independence.',
          'No P/R/F1, no human approval fabricated, no dependency installation, no external model API, no subagents.']}
    put(ROOT/'execution.json',execution)
    put(ROOT/'document-summary.json',summaries)
    table=['# 第二次隔离前向运行','',
      '仅依据八篇源文与本次三技能编制。目标支持和语义复核为生成方自检；独立评审/形式证明未执行，人工待审。隔离不等于统计独立。','',
      '|文档|原始候选|目标|联系|候选组|成立组|覆盖|模型检查|','|---|---:|---:|---:|---:|---:|---|---|']
    for s in summaries:
        table.append(f"|{s['document_id']}|{s['raw_candidates']}|{s['goals']}|{s['relations']}|{s['groups']}|{s['supported_complete_groups']}|{s['coverage_structure']}/{s['coverage_workflow']}|{s['model_inspection'].get('structure')}|")
    table+=['','全部候选精化组的充分性缺口/反例均保留，没有强造完整组或根。DOC036的混合附和含义留为不确定候选；各篇其他条件和提议见目标及语义自检。','',
      '交付路径及每个文件的SHA256见 delivery-index.json；每篇delivery包含HTML、JSON、MD、两个独立SVG及必要附件。覆盖附件独立保存在每篇目录。','']
    md(ROOT/'README.md','\n'.join(table))
    files=[]
    for p in sorted(ROOT.rglob('*')):
        if p.is_file() and p.name!='delivery-index.json' and '__pycache__' not in p.parts:
            files.append({'relative_path':p.relative_to(ROOT).as_posix(),'sha256':digest(p),'bytes':p.stat().st_size,
                'role':'delivery' if 'delivery' in p.relative_to(ROOT).parts else 'audit_or_execution'})
    put(ROOT/'delivery-index.json',{'schema_version':'candidate-repeat-delivery-index-1','created_at':now(),
        'hash_scope':'Every retained task output file except this self-index; no recursive self-hash. Paths relative to candidate-repeat.',
        'document_deliveries':{d:[f['relative_path'] for f in files if f['relative_path'].startswith(d+'/delivery/')] for d in DOC_ORDER},'files':files})
    print(json.dumps([{k:v for k,v in s.items() if k not in ['model_inspection','source_txt_sha256','source_json_sha256']} for s in summaries],ensure_ascii=False),flush=True)

if __name__=='__main__':
    if len(sys.argv)!=2 or sys.argv[1] not in ['capture','build','finish']: raise SystemExit('capture | build | finish')
    {'capture':capture,'build':build,'finish':finish}[sys.argv[1]]()
