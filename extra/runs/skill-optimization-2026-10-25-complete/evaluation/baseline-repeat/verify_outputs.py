import hashlib
import json
from pathlib import Path

out=Path(__file__).resolve().parent
root=out.parents[3]
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
index=read(out/'delivery-index.json')
execution=read(out/'execution.json')
checks=[]
for skill in execution['skill_files']:
    assert digest(root/skill['path'])==skill['sha256'], skill['path']
for doc in index['documents']:
    d=out/doc['document_id']
    for entry in doc['files'].values():
        assert digest(out/entry['path'])==entry['sha256'],entry['path']
    model=read(d/'delivery/goal-model.json')
    extraction=read(d/'extraction.json')
    source=(d/'source.txt').read_text(encoding='utf-8')
    assert hashlib.sha256(source.encode('utf-8')).hexdigest()==extraction['document_hash']
    for segment in extraction['segments']:
        loc=segment['original_locator']
        assert source[loc['start_char']:loc['end_char']]==segment['text']
    for c in extraction['candidates']:
        for e in c['evidence_candidates']:
            assert source[e['start_char']:e['end_char']]==e['quote']
    manifest=read(d/'delivery/manifest.json')
    for item in manifest['files']:
        assert digest(d/'delivery'/item['path'])==item['sha256']
    assert read(d/'inspection.json')['structure']=='passed'
    assert model['review']=={'status':'pending'}
    assert all(g['status']=='proposed' and g['completeness']=='partial' for g in model['refinement_groups'])
    lines=['# '+doc['document_id']+' 语义问题明细','','执行者：本轮同一助手。可见材料为本篇完整原文与本篇当前目标/组包。目标自检覆盖全部当前目标，组检查覆盖全部候选组。独立审查not_run；形式证明not_run；人工pending。','']
    for n,g in enumerate(model['refinement_groups'],1):
        evidence=[e['source_id'] for e in model['evidence_index'] if e['evidence_id'] in g['evidence_ids']]
        lines += ['## S'+str(n).zfill(3),'',
            '- 对象：'+g['group_id']+'；父目标'+g['parent_id']+'；子目标'+', '.join(g['child_ids']),
            '- 类别：精化问题；状态：未解决。',
            '- 依据：'+', '.join(evidence)+'；全文引文与偏移见decisions.json和交付evidence_index。',
            '- 判断：'+g['rationale'],
            '- 场景：'+'；'.join(g['assumptions']),
            '- 建议：在同一情境下确认完整满足条件后再重评整组；当前不作为成立精化。',
            '- 后续处置：原文不足以证明充分，未造新目标、人工答案或通过结论；无新增证据，停止此组循环并保留问题。','']
    lines += ['## 正确与边界记录','','所有当前目标均回查全文与逐项目标支持理由；目标来源explicit与inferred分别记录，现状能力仅在有用途或维持意图时保留。纯按钮操作、未经确认的采访者推测、受访者对平台内部实现的猜测不自动变成已验证需求。没有新的目标实质修订，没有人工反馈，不生成虚构反馈副本。','']
    p=d/'semantic-review-details.md'
    with p.open('x',encoding='utf-8',newline='\n') as f: f.write('\n'.join(lines))
    checks.append(dict(document_id=doc['document_id'],goals=doc['goals'],groups=doc['groups'],structure='passed',readiness=doc['readiness'],indexed_hashes='passed',manifest_hashes='passed',all_source_segment_slices='passed',all_evidence_slices='passed',review_details=dict(path=p.relative_to(out).as_posix(),sha256=digest(p))))
result=dict(status='passed',skill_hashes='unchanged',documents=checks,total_goals=sum(d['goals'] for d in checks),total_proposed_partial_groups=sum(d['groups'] for d in checks),supported_complete_groups=0,actual_commands=execution['command_count'],failures=execution['failures'],repairs=execution['repairs'],note='未进行P/R/F1计算；上下文隔离不等于统计独立；检查通过不证明语义或完整性。')
with (out/'verification.json').open('x',encoding='utf-8',newline='\n') as f: json.dump(result,f,ensure_ascii=False,indent=2)
print(json.dumps(result,ensure_ascii=False,indent=2))
