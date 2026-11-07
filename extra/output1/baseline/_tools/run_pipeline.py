"""Assemble author-written decisions, locate verbatim evidence, run frozen tools.

No keyword classification or semantic label generation is performed here.
All goal wording, labels, groups, rationales and review notes come from the
current assistant's authored-content.json after reading complete transcripts.
"""
import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'output1/baseline'
SNAP = ROOT / 'output1/_run/skill-snapshots/baseline/skills'
TRACE = SNAP / 'goal-tracing/scripts/trace_candidates.py'
KAOS = SNAP / 'goal-model-building/scripts/kaos_model.py'
SPECS = json.loads((OUT / '_tools/authored-content.json').read_text(encoding='utf-8'))

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def dump(path, data):
    with path.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')

def read(path):
    return json.loads(path.read_bytes().decode('utf-8-sig'))

def run(args, log):
    command = [sys.executable] + [str(a) for a in args]
    started = datetime.now(timezone.utc).isoformat()
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONIOENCODING='utf-8')
    p = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, encoding='utf-8', errors='replace')
    log.append(dict(command=command, cwd=str(ROOT), started_utc=started,
                    exit_code=p.returncode, stdout=p.stdout, stderr=p.stderr))
    if p.returncode:
        raise RuntimeError(p.stdout + p.stderr)

for doc, spec in SPECS.items():
    target = OUT / doc / 'v1'
    target.mkdir(parents=True, exist_ok=False)
    inputs = ROOT / 'output1/_inputs' / doc
    src = (inputs / 'source.txt').read_bytes()
    canonical = src.decode('utf-8')
    original = read(inputs / 'source-original.json')
    data = read(inputs / 'source-input.json')
    assert sha(src) == data['document_hash'] == original['document_hash']
    assert data['document_id'] == doc
    segs = {s['source_id']: s for s in data['segments']}
    assert len(segs) == len(original['turns'])
    for turn in original['turns']:
        seg = segs[turn['source_id']]
        a, b = seg['original_locator']['start_char'], seg['original_locator']['end_char']
        assert canonical[a:b] == seg['text'] == turn['text']
    (target / 'source.txt').write_bytes(src)
    shutil.copyfile(inputs / 'source-input.json', target / 'source-input.json')
    shutil.copyfile(inputs / 'source-original.json', target / 'source-original.json')
    def quote(turn):
        s = segs[f'{doc}:T{turn:03d}']
        return dict(source_id=s['source_id'], quote=s['text'], role='basis',
                    start_char=s['original_locator']['start_char'], end_char=s['original_locator']['end_char'])
    data.update(schema_version='goalforge-extraction-3', status='completed', candidates=[],
                review_questions=[dict(candidate_ids=q['ids'], question=q['question'], reason=q['reason']) for q in spec['questions']],
                limitations=spec['limitations'])
    data['coverage'] = dict(scope='provided_material', source_ids=list(segs), omissions=[])
    for authored in spec['goals']:
        inference = None if authored['origin'] == 'explicit' else dict(basis_candidate_ids=[], reason=authored['rationale'], assumptions=authored['assumptions'])
        data['candidates'].append(dict(candidate_id=authored['id'], statement=authored['statement'],
            origin=authored['origin'], actor='受访者', context=authored['context'],
            evidence_candidates=[quote(t) for t in authored['turns']], inference=inference, review_status='pending'))
    dump(target / 'extraction.json', data)
    log = []
    try:
        run([TRACE, target / 'extraction.json', '--judgment-template', target / 'judgments-template.json'], log)
        judgments = read(target / 'judgments-template.json')
        for authored in spec['goals']:
            judgments['judgments'][authored['id']].update(label=authored['label'], rationale=authored['rationale'],
                supported_parts=[authored['statement']], unsupported_parts=[], assumptions=authored['assumptions'],
                reasoning_steps=[authored['review']])
        dump(target / 'judgments.json', judgments)
        run([TRACE, target / 'extraction.json', target / 'trace', '--source', target / 'source.txt', '--judgments', target / 'judgments.json'], log)
        shutil.copyfile(target / 'trace/tracing.json', target / 'tracing.json')
        run([KAOS, 'template', target / 'extraction.json', target / 'judgments.json', target / 'kaos-decisions-template.json'], log)
        decisions = read(target / 'kaos-decisions-template.json')
        for authored in spec['groups']:
            g = copy.deepcopy(authored)
            turns = g.pop('turns')
            g.update(evidence_ids=[], evidence_quotes=[quote(t) for t in turns])
            decisions['groups'].append(g)
            decisions['questions'].append(dict(target_type='group', target_id=g['group_id'],
                message='候选组尚未确认共同充分性：' + g['rationale']))
        dump(target / 'kaos-decisions.json', decisions)
        run([KAOS, 'assemble', target / 'extraction.json', target / 'judgments.json', target / 'source.txt', target / 'kaos-decisions.json', target / 'assembled'], log)
        run([KAOS, 'inspect', target / 'assembled/model-input.json', target / 'inspection.json'], log)
        run([KAOS, 'finalize', target / 'assembled/model-input.json', target / 'inspection.json', target / 'delivery', '--svg'], log)
    finally:
        dump(target / 'execution-log.json', log)

    report = read(target / 'inspection.json')
    review = ['# ' + doc + ' 生成方自检', '', '范围：' + spec['coverage'], '',
        '本文件是同一生成方基于本次全文所做自检，不能充当独立语义审查、形式证明或用户验收。', '',
        '## 全部目标逐项核对', '']
    for g in spec['goals']:
        review += [f"### {g['id']} {g['statement']}", '',
                   f"来源轮次：{', '.join('T%03d' % t for t in g['turns'])}；支持判断：{g['label']}。", '',
                   g['rationale'], '', '自检与边界：' + g['review'], '']
        if g['assumptions']:
            review += ['必要假设：' + '；'.join(g['assumptions']), '']
    review += ['## 全部候选精化组核对', '']
    for g in spec['groups']:
        review += [f"- {g['group_id']}：{g['parent_id']} ← {{{', '.join(g['child_ids'])}}}；{g['status']}/{g['completeness']}。{g['rationale']}"]
    review += ['', '上述组均不进入已成立精化图；多根和孤立节点有意保留。', '', '## 考虑后未建立的其他精化', '']
    review += ['- ' + x for x in spec['rejected']]
    review += ['', '## 未决问题', ''] + ['- ' + ', '.join(q['ids']) + '：' + q['question'] for q in spec['questions']]
    review += ['', '## 场景与验证边界', '',
        '本次没有新造用户使用场景；上述实际例子均来自对应访谈。关于组充分性不足的推理是作者分析，不能作为新增访谈事实。', '',
        '实际工程检查结果见 inspection.json；当前结构状态：' + str(report['structure']) + '；交付状态：' + str(report['readiness']) + '。', '',
        '独立语义审查、形式证明和人工决定状态以实际报告为准；本次未执行独立审查或形式证明，人工待审。', '',
        '没有执行浏览器交互或下载回执测试；本地交付文件由finalize实际写入，清单哈希另行核验。', '']
    (target / 'author-review.md').write_text('\n'.join(review), encoding='utf-8')
    manifest = read(target / 'delivery/manifest.json')
    for item in manifest['files']:
        assert sha((target / 'delivery' / item['path']).read_bytes()) == item['sha256']
    traces = read(target / 'tracing.json')['traces']
    assert all(e['location_status'] == 'exact' and e['verification_scope'] == 'full_text'
               for t in traces for e in t['submitted_evidence'])
    verification = dict(delivery_manifest_files=len(manifest['files']), manifest_hashes_match=True,
                        source_input_unchanged=sha(src) == sha((inputs / 'source.txt').read_bytes()),
                        full_text_exact_evidence=sum(len(t['submitted_evidence']) for t in traces),
                        goals=len(spec['goals']), candidate_groups=len(spec['groups']), supported_complete_groups=0,
                        note='本核验仅验证文件与定位，不新增语义结论。')
    dump(target / 'artifact-verification.json', verification)
    provenance = dict(branch='baseline', document_id=doc, created_utc=datetime.now(timezone.utc).isoformat(),
        skill_snapshot=str(SNAP), model='unknown', sampling='unknown', token_budget='unknown',
        authoring='当前助手完整阅读各访谈后手工编制语义内容；脚本只复制、定位、组装和验证。',
        source_preparation='复用提供的source-input；逐轮核对source-original与source.txt，没有重新规范化文本。',
        inputs=[dict(path=str(inputs / n), sha256=sha((inputs / n).read_bytes())) for n in ['source.txt','source-input.json','source-original.json']],
        snapshot_inventory=[dict(path=str(p), sha256=sha(p.read_bytes())) for p in sorted(SNAP.rglob('*')) if p.is_file() and '__pycache__' not in p.parts],
        authored_content=dict(path=str(OUT / '_tools/authored-content.json'), sha256=sha((OUT / '_tools/authored-content.json').read_bytes())),
        execution_log=str(target / 'execution-log.json'),
        restrictions=['未读取另一生成分支、项目当前skills、旧output、docs/13-16、runs报告或参考答案。',
                      '未修改输入或冻结技能；未采纳任何跨分支反馈。'],
        checks=verification)
    dump(target / 'run-record.json', provenance)
    (target / 'run-notes.md').write_text(
        '# ' + doc + ' baseline v1运行说明\n\n'
        '已加载冻结快照中的goal-extraction、goal-tracing、goal-model-building、model-review四项SKILL.md及接入、契约、证据、判断、精化和执行引用。具体路径及SHA-256见run-record.json。\n\n'
        '顺序：完整阅读访谈 → 手工目标与语义判断 → 冻结trace脚本生成空模板 → 填入本次判断 → 实际trace → 冻结kaos模板 → 填入候选组 → assemble → inspect → finalize --svg → 清单文件哈希和全文引文核验。命令、时间、退出码及原始输出见execution-log.json。\n\n'
        '源文三件套按提供版本复用并保留；源文与轮次逐一核对。脚本不以关键词生成目标、支持标签或精化结论。\n\n'
        '模型精确标识：unknown；采样参数：unknown；预算：unknown。未调用外部模型API。\n\n'
        'inspect是工程检查；作者自检为author-review.md，独立语义审查与形式证明均未执行，人工待审。没有浏览器交互测试。所有产物均在output1/baseline。\n', encoding='utf-8')
    print(doc + ': ' + json.dumps(dict(verification, structure=report['structure'], readiness=report['readiness']), ensure_ascii=False))
