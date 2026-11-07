# -*- coding: utf-8 -*-
"""Assemble explicitly authored data; quote positioning, hashes and frozen CLIs only.
No keyword classification, model API calls, or generated semantic labels.
"""
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'output1/revised'
SKILLS = ROOT / 'output1/_run/skill-snapshots/revised/skills'
INPUTS = ROOT / 'output1/_inputs'
DATA = Path(__file__).with_name('authored-data-DOC010-v2.json')
TRACE = SKILLS / 'goal-extraction/scripts/trace_candidates.py'
KAOS = SKILLS / 'goal-model-building/scripts/kaos_model.py'
RENDER = SKILLS / 'goal-extraction/scripts/render_review.py'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
os.environ['PYTHONUTF8'] = '1'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def read(p):
    return json.loads(p.read_bytes().decode('utf-8-sig'))

def write(p, data):
    with p.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')

def text(p, content):
    with p.open('x', encoding='utf-8', newline='\n') as f:
        f.write(content)

loaded = []
for skill, references in {
    'goal-extraction': ['input-processing','goal-boundaries','output-contract','evidence-rules','semantic-judgments','tracing-contract'],
    'goal-model-building': ['modeling-rules','output-contract','tools'],
    'model-review': ['tools','output-contract','semantic-review'],
}.items():
    loaded.append(SKILLS / skill / 'SKILL.md')
    loaded.extend(SKILLS / skill / 'references' / (n+'.md') for n in references)
# Runtime dependencies actually consumed by the frozen CLI.
loaded += [TRACE, KAOS, RENDER, SKILLS/'goal-extraction/scripts/simple_candidates.py']
loaded += [SKILLS/'goal-model-building/assets'/n for n in ['simple-viewer.html','simple-viewer.css','simple-core.js','simple-viewer.js']]

for doc, authored in read(DATA).items():
    dest = OUT/doc/'v2'
    dest.mkdir(parents=True, exist_ok=False)
    srcdir = INPUTS/doc
    source = (srcdir/'source.txt').read_bytes().decode('utf-8')
    data = read(srcdir/'source-input.json')
    assert hashlib.sha256(source.encode('utf-8')).hexdigest() == data['document_hash']
    assert data['document_id'] == doc
    smap = {s['source_id']: s for s in data['segments']}
    for seg in smap.values():
        start,end = seg['original_locator']['start_char'],seg['original_locator']['end_char']
        assert source[start:end] == seg['text'], seg['source_id']
    for name in ('source.txt','source-input.json','source-original.json'):
        shutil.copyfile(srcdir/name, dest/name)
    def evidence(turn):
        seg = smap[f'{doc}:T{turn:03d}']
        return dict(source_id=seg['source_id'],quote=seg['text'],
                    role='context' if seg['speaker']=='Interviewer' else 'basis',
                    start_char=seg['original_locator']['start_char'],end_char=seg['original_locator']['end_char'])
    data.update(schema_version='goalforge-extraction-3',status='completed',candidates=[],
                review_questions=[dict(candidate_ids=q['ids'],question=q['text'],reason=q['reason']) for q in authored['questions']],
                limitations=['只分析本次提供的完整文字访谈；未核对录音，也不声称穷尽产品需求。',
                             'native_text 表示接收的是原生文字，不表示转写曾获人工确认；口语残句和编码异常按原文保留。',
                             '提取、支持判断、精化与自检由同一生成代理完成；独立语义审查和形式证明未运行，人工采纳待定。',
                             '当前契约没有独立障碍、偏好或贡献关系层；相关语境以目标条件、原文及问题传递，不能宣称完整结构化关系分析。'])
    for g in authored['goals']:
        inf = None if g['origin']=='explicit' else dict(basis_candidate_ids=[],reason=g['rationale'],assumptions=g.get('assumptions',[]))
        data['candidates'].append(dict(candidate_id=g['id'],statement=g['statement'],origin=g['origin'],actor='受访者（Stakeholder）',
                                       context=g['context'],evidence_candidates=[evidence(t) for t in g['turns']],inference=inf,review_status='pending'))
    write(dest/'extraction.json',data)
    log=[]
    def run(*args):
        command=[sys.executable,'-B',*[str(a) for a in args]]
        result=subprocess.run(command,cwd=ROOT,text=True,encoding='utf-8',capture_output=True)
        log.append(dict(at_utc=datetime.now(timezone.utc).isoformat(),argv=command,exit_code=result.returncode,stdout=result.stdout,stderr=result.stderr))
        write(dest/f'command-{len(log):02d}.json',log[-1])
        if result.returncode:
            raise RuntimeError(result.stderr or result.stdout)
    run(TRACE,dest/'extraction.json','--judgment-template',dest/'judgments-template.json')
    j=read(dest/'judgments-template.json')
    for g in authored['goals']:
        j['judgments'][g['id']]=dict(target_statement=g['statement'],label=g['label'],rationale=g['rationale'],
                                    supported_parts=[g['statement']],unsupported_parts=[],assumptions=g.get('assumptions',[]),
                                    reasoning_steps=[g['rationale']])
    write(dest/'judgments.json',j)
    run(TRACE,dest/'extraction.json',dest/'tracing','--source',dest/'source.txt','--judgments',dest/'judgments.json','--review-md')
    shutil.copyfile(dest/'tracing/tracing.json',dest/'tracing.json')
    run(RENDER,dest/'extraction.json',dest/'goal-candidates.md')
    run(KAOS,'template',dest/'extraction.json',dest/'judgments.json',dest/'kaos-decisions-template.json')
    decisions=read(dest/'kaos-decisions-template.json')
    for group in authored['groups']:
        decisions['groups'].append(dict(group_id=group['id'],parent_id=group['parent'],child_ids=group['children'],kind='and',
                                       status=group['status'],completeness=group['completeness'],rationale=group['rationale'],
                                       assumptions=group['assumptions'],evidence_ids=[],evidence_quotes=[evidence(t) for t in group['turns']]))
        decisions['questions'].append(dict(target_type='group',target_id=group['id'],message=group['question']))
    write(dest/'kaos-decisions.json',decisions)
    run(KAOS,'assemble',dest/'extraction.json',dest/'judgments.json',dest/'source.txt',dest/'kaos-decisions.json',dest/'assembled')
    run(KAOS,'inspect',dest/'assembled/model-input.json',dest/'inspection.json')
    run(KAOS,'finalize',dest/'assembled/model-input.json',dest/'inspection.json',dest/'delivery','--svg')
    report=read(dest/'inspection.json')
    lines=[f'# {doc} 生成方自检', '',
           '执行者：本分支生成代理 /root/pilot_revised。同一代理完成提取、核验、精化与本次自检；这不是独立语义审查。',
           f"可见资料：{srcdir/'source.txt'}、同目录 source-input.json、source-original.json；全文 T000—T{len(data['segments'])-1:03d} 已读。只使用 revised 冻结三项正式技能及必要引用。",
           '外部参考答案、其他分支结果和旧报告未读取。模型精确标识、采样设置和 token 预算：unknown。', '',
           '## 全部目标回查', '', '| 目标 | 来源/支持 | 已核对的完整语义与依据 |', '|---|---|---|']
    for g in authored['goals']:
        lines.append(f"| {g['id']} | {g['origin']} / {g['label']} | {g['rationale']} 适用条件：{'；'.join(g['context'])} |")
    lines+=['','## 全部精化组回查','','| 组 | 端点 | 结论 | 理由与边界 |','|---|---|---|---|']
    for g in authored['groups']:
        lines.append(f"| {g['id']} | {g['parent']} ← {','.join(g['children'])} | {g['status']} / {g['completeness']} | {g['rationale']} {'；'.join(g['assumptions'])} |")
    lines+=['','## 场景、边界与未建关系','']+[f'- {x}' for x in authored['review_notes']]
    lines+=['','上述构造场景均标为分析假设，不是新增访谈事实；未执行穷尽场景检验或形式证明。','',
            '## 未决问题与停止条件','']
    lines += [f"- {'、'.join(q['ids'])}：{q['text']}（未解决：{q['reason']}）" for q in authored['questions']]
    lines += [f"- {g['id']}：{g['question']}（未解决；已写入模型问题）" for g in authored['groups']]
    lines += ['','以上缺口没有新材料可解，停止同一问题循环，保留待审状态；未删除疑点或替受访者采纳。', '',
              '## 工程结果与证据层次','', '实际 inspect 报告如下（机械复制，非手填）：','', '```json',json.dumps(report,ensure_ascii=False,indent=2),'```','',
              '工程检查核验附件、偏移、判断绑定和结构。作者自检覆盖全部目标与全部候选组；独立审查 not_run，形式证明 not_run，人工决定 pending。HTML 由冻结工具输出；未进行浏览器交互或截图验证。','']
    text(dest/'author-review.md','\n'.join(lines))
    provenance=dict(branch='revised',document_id=doc,version='v2',author='/root/pilot_revised',
                    model_identifier='unknown',sampling='unknown',token_budget='unknown',
                    started_scope='Provided three source inputs only; no baseline or reference answers',
                    authored_data=dict(path=str(DATA),sha256=sha(DATA)),assembly_helper=dict(path=str(Path(__file__)),sha256=sha(Path(__file__))),
                    loaded_skill_files=[dict(path=str(p),sha256=sha(p)) for p in loaded],
                    sources=[dict(path=str(srcdir/n),sha256=sha(srcdir/n)) for n in ('source.txt','source-input.json','source-original.json')],
                    commands=log,semantics='All statements, labels, rationales, groups and scenarios explicitly authored in authored-data.json; helper only assembles and validates.',
                    inspection=report,goals=len(authored['goals']),groups=len(authored['groups']),
                    supported_complete_groups=sum(g['status']=='supported' and g['completeness']=='complete' for g in authored['groups']))
    write(dest/'run-record.json',provenance)
    text(dest/'run-notes.md',f"# {doc} 运行说明\n\n全部加载路径、SHA-256、实际命令、返回值和输出见 run-record.json；每一步独立回执为 command-01.json 等。\n\n1. 阅读完整原文和三项冻结技能及必要引用。\n2. 在 authored-data.json 逐项人工编制语义结果，未用关键词规则产生标签。\n3. 复用 source-input，逐段断言原文切片与偏移一致并核对全文哈希。\n4. 实际执行冻结脚本生成空 judgments 模板，填入本次判断，执行 trace。\n5. 实际生成 KAOS 空包，填入本次整组判断，assemble → inspect → finalize。\n6. 生成覆盖全部目标和组的 author-review，保留未决问题。\n\n精确模型、采样参数、预算：unknown。所有人审 pending；同一代理自检不构成独立审查。未使用外部语义答案。没有进行现场 UI 或导出按钮验证。\n")
    # Additional evidence lives alongside the frozen package, not silently added to its manifest.
    previous=OUT/doc/'v1'
    prior=read(previous/'extraction.json')
    old_by={g['candidate_id']:g for g in prior['candidates']}
    changed=[]
    for current in data['candidates']:
        old=old_by[current['candidate_id']]
        if current!=old:
            changed.append(current['candidate_id'])
            assert current['candidate_id']=='G08'
            expected=copy.deepcopy(old)
            expected['statement']='下雨时更频繁地收到雨情变化、开始或停止的更新通知。'
            assert current==expected
    assert changed==['G08']
    assert sha(previous/'source.txt')==sha(dest/'source.txt')
    prior_decisions=read(previous/'kaos-decisions.json')
    assert prior_decisions['groups']==decisions['groups']
    assert prior_decisions['questions']==decisions['questions']
    revision=dict(schema_version='pilot-author-revision-record-1',document_id=doc,
                  revision_kind='assistant_semantic_review_wording_correction',human_feedback=False,human_acceptance='pending',
                  previous_artifact_version='v1',current_artifact_version='v2',
                  previous_model=dict(path=str(previous/'delivery/goal-model.json'),sha256=sha(previous/'delivery/goal-model.json')),
                  current_model=dict(path=str(dest/'delivery/goal-model.json'),sha256=sha(dest/'delivery/goal-model.json')),
                  tool_model_version=report['model']['version'],tool_model_parent=None,
                  tool_limitation='Frozen CLI only increments model version through actual human feedback. No feedback was fabricated: v2 is the external author artifact revision; internal model version remains its generated v1 and parent=null.',
                  changed_goal_ids=changed,affected_group_ids=['F02'],
                  id_mapping=[dict(previous=g['candidate_id'],current=g['candidate_id'],changed=g['candidate_id']=='G08') for g in data['candidates']],
                  reason='雨势可能误读为雨强；收窄为一般雨情，保留是否降雨、开始或停止的状态更新含义。',
                  semantic_review_scope='G08: T049/T063 plus T039–T071 context; F02: whole-group sufficiency and delayed-update hypothetical counterexample. All 12 unchanged goals and F01/F03 reviewed against unchanged source and retained reasons.',
                  mechanical_reverification='All 13 goals, full-text quote positions, all 3 groups, attachment hashes and complete reassembly/inspect/finalize executed anew through frozen scripts.',
                  source_unchanged=True,unchanged_goals_exactly_equal=True,groups_exactly_equal=True,
                  previous_extraction_sha256=sha(previous/'extraction.json'),current_extraction_sha256=sha(dest/'extraction.json'))
    write(dest/'revision-record.json',revision)
    text(dest/'revision-notes.md',"# DOC010 v1 → v2 局部作者修订\n\n仅 G08 将‘雨势变化’改为‘雨情变化’；ID不变。原文 T049/T063 及 T039—T071 已回查。开始或停止指是否降雨的变化，不是雨强测量。F02重新整组审查，延迟数据的分析假设反例仍存在，继续 proposed/partial。其余目标、条件、证据和全部组内容经核对不变。\n\n全13目标重新生成语义模板和判断绑定，实际执行 trace、KAOS template、assemble、inspect、finalize；并非只补写哈希。完整回执在 run-record.json 和 command-*.json。\n\n这是助手语义评审驱动的措辞修订，不是用户反馈；未调用 feedback，未伪造人工采纳。冻结工具仅支持用真实人工反馈递增内部模型版本，所以本目录的作者产物版本为 v2，内部模型保持工具实际生成的 version=v1、parent=null。前后版本与全量ID映射绑定见 revision-record.json；v1完整保留。\n")

    artifact_list=[dict(path=str(p.relative_to(dest)),sha256=sha(p)) for p in sorted(dest.rglob('*')) if p.is_file()]
    write(dest/'freeze-manifest.json',dict(schema_version='pilot-author-freeze-1',document_id=doc,version='v2',frozen_at_utc=datetime.now(timezone.utc).isoformat(),files=artifact_list))
    print(json.dumps(dict(document=doc,goals=len(authored['goals']),groups=len(authored['groups']),inspection=report),ensure_ascii=False))
