# -*- coding: utf-8 -*-
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

root = Path('output1/revised')
docs = ['DOC021', 'DOC024', 'DOC034', 'DOC036']
expected = {'DOC021':(18,2), 'DOC024':(11,0), 'DOC034':(14,2), 'DOC036':(17,1)}

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

required = [
    'source.txt', 'extraction.json', 'judgments.json', 'tracing/tracing.json',
    'kaos-decisions.json', 'assembled/model-input.json', 'inspection.json',
    'goal-candidates.md', 'authoring.json', 'author-review.md', 'run-record.json',
    'delivery/goal-model.html', 'delivery/goal-model.json', 'delivery/goal-model.md',
    'delivery/manifest.json', 'delivery/attachments/extraction.json',
    'delivery/attachments/judgments.json', 'delivery/attachments/source.txt',
    'delivery/attachments/kaos-decisions.json', 'delivery/attachments/inspection.json'
]
rows = []
for doc in docs:
    base = root / doc / 'v1'
    assert all((base/name).is_file() for name in required)
    model = read(base/'delivery/goal-model.json')
    check = read(base/'inspection.json')
    record = read(base/'run-record.json')
    extraction = read(base/'extraction.json')
    tracing = read(base/'tracing/tracing.json')
    manifest = read(base/'delivery/manifest.json')
    author = read(root/'_authoring'/f'{doc}.json')
    assert (len(model['goals']), len(model['refinement_groups'])) == expected[doc]
    assert check['structure'] == 'passed'
    assert all(command['exit_code'] == 0 for command in record['commands'])
    assert len(record['commands']) == 7
    assert digest(base/'source.txt') == digest(Path('output1/_inputs')/doc/'source.txt') == extraction['document_hash']
    assert digest(base/'authoring.json') == digest(root/'_authoring'/f'{doc}.json')
    assert (base/'author-review.md').read_text(encoding='utf-8') == author['author_review']
    for entry in manifest['files']:
        assert digest(base/'delivery'/entry['path']) == entry['sha256']
    quotes = [ev for trace in tracing['traces'] for ev in trace['submitted_evidence']]
    assert all(ev['location_status'] == 'exact' and ev['source_version_status'] == 'verified' for ev in quotes)
    labels = Counter(trace['support']['label'] for trace in tracing['traces'])
    blocked = [issue for issue in model['issues'] if issue.get('blocking')]
    if doc == 'DOC036':
        assert [issue['target_id'] for issue in blocked] == ['DOC036-G17']
        assert check['readiness'] == 'blocked'
    else:
        assert blocked == [] and check['readiness'] == 'reviewable'
    assert all(g['status']=='proposed' and g['completeness']=='partial' for g in model['refinement_groups'])
    rows.append({
        'document_id':doc, 'latest_revision':'v1', 'package_status':'complete',
        'latest_directory':base.resolve().as_posix(),
        'html':(base/'delivery/goal-model.html').resolve().as_posix(),
        'model_json':(base/'delivery/goal-model.json').resolve().as_posix(),
        'summary_md':(base/'delivery/goal-model.md').resolve().as_posix(),
        'author_review':(base/'author-review.md').resolve().as_posix(),
        'goals':len(model['goals']), 'groups':len(model['refinement_groups']),
        'supported_complete_groups':sum(g['status']=='supported' and g['completeness']=='complete' for g in model['refinement_groups']),
        'support_labels':dict(labels), 'structure':check['structure'], 'readiness':check['readiness'],
        'independent_semantic':check['independent_semantic'], 'formal_proof':check['formal_proof'], 'human':check['human'],
        'blocking_issues':blocked, 'successful_commands':len(record['commands']),
        'required_files_verified':len(required), 'manifest_files_hash_verified':len(manifest['files']),
        'submitted_quotes_exact_and_source_version_verified':len(quotes),
        'author_review_matches_current_authoring':True,
        'canonical_source_matches_frozen_input':True
    })

report = {
    'schema_version':'goalforge-remaining-completion-1',
    'completed_at_utc':datetime.now(timezone.utc).isoformat(),
    'scope':docs, 'executor':'current continuation agent /root/finish_remaining',
    'executor_role':'model-authored semantic extraction, verification, modeling and author self-review; deterministic frozen tools for assembly/inspection/finalization',
    'exact_model_identifier':'unknown', 'sampling_parameters':'unknown', 'reasoning_budget':'unknown', 'token_budget':'unknown',
    'inputs_used':['output1/_inputs/<DOC>/source.txt and source-input.json',
                   'output1/_run/skill-snapshots/revised/skills/{goal-extraction,goal-model-building,model-review}',
                   'output1/_run/authoring-contract.md and build_artifacts.py',
                   'permitted unfinished DOC021 author draft and formatting helper'],
    'prohibited_answer_sources_used':False,
    'source_claims_externally_verified':False,
    'all_sources_fully_read':True,
    'turn_ranges':{'DOC021':'T000-T076','DOC024':'T000-T035','DOC034':'T000-T026','DOC036':'T000-T076'},
    'totals':{'documents':4,'goals':60,'groups':5,'supported_complete_groups':0,'successful_assembly_pipeline_commands':28},
    'documents':rows,
    'unresolved_note':'DOC036-G17匿名发帖由采访者并列归纳与简短肯定形成，当前支持不足。工具将整包readiness汇总为blocked，但阻断仅关联该候选；其他16目标仍direct。全部人审pending。',
    'relationship_note':'5组均经整体与正常/异常分析假设自检后保留proposed/partial，不绘为成立精化；没有为了数量补根。',
    'prior_complete_deliveries_overwritten':False,
    'failure_log':(root/'_authoring/finish-first-attempt-failure.json').resolve().as_posix(),
    'failure_note':'首次作者脚本调用发生编码错误，未创建交付目录；保留日志后显式UTF-8解码编译成功。四篇中性组装全部首次v1成功；无补哈希或伪造人审。',
    'validation_scope':'Mandatory file presence, delivery manifest hashes, unchanged canonical inputs, current author review equality, all submitted evidence exact/full-source-version verified, actual seven-command pipeline exit codes and inspection status. Does not prove semantic correctness, full requirements coverage, independent review or formal refinement.'
}
json_path = root/'remaining-completion.json'
md_path = root/'remaining-completion.md'
assert not json_path.exists() and not md_path.exists()
with json_path.open('x', encoding='utf-8', newline='\n') as out:
    json.dump(report, out, ensure_ascii=False, indent=2)
    out.write('\n')

lines = ['# 四篇续作完成记录', '',
         'DOC021、DOC024、DOC034、DOC036完整交付包均已生成，未改输入、冻结技能或其他已完整交付。共60目标、5个proposed/partial候选组，0个成立精化组。目标与组无数量配额；引文保留英文，目标及说明为中文。', '',
         '| 文档 | 目标 | 组 | 结构检查 | readiness | 最新HTML | 作者自检 |',
         '|---|---:|---:|---|---|---|---|']
for row in rows:
    lines.append(f"| {row['document_id']} | {row['goals']} | {row['groups']} | {row['structure']} | {row['readiness']} | [v1]({row['html']}) | [自检]({row['author_review']}) |")
lines += ['',
    'DOC036的blocked仅由G17“希望能够匿名发帖”支持不足触发：T071/072把匿名浏览、匿名发帖和恶意账号并列后得到简短肯定，无法确认独立发帖意图。该候选保留pending，不作为成立精化前提；其余16目标direct。其他三篇readiness=reviewable。全部human=pending、independent_semantic=not_run、formal_proof=not_run。', '',
    '本次完整读取轮次：DOC021 T000—T076、DOC024 T000—T035、DOC034 T000—T026、DOC036 T000—T076。DOC021续用未完成草稿前已独立完整回查，恢复“通常”“可以考虑”等语气，并收窄更新时间与真实性边界。DOC024保留“无限→更多”自纠和逻辑可靠性信念；DOC034保留招聘/营销成本不同语境及自动化建议；DOC036保留评论线索不等于安全、可疑交易先货后款与普通先付款并存。', '',
    '每包含extraction、judgments、tracing、KAOS decisions、assembled model、inspection、delivery HTML/JSON/MD、实际附件、7条命令回执、作者自检与run-record。28条流水线命令均实际成功；重新逐文件核对交付manifest的32个文件哈希、80项必需文件存在、源文与冻结输入一致、作者自检与当前作者JSON一致，以及全部提交引文精确定位和源版本核验。具体计数见JSON逐篇记录。结构和哈希检查不证明语义或精化充分性。', '',
    '执行者：当前续作生成助手 /root/finish_remaining。语义提取、核验、建模、自检由同一执行者完成；中性脚本仅定位、绑定、组装与检查。精确模型标识、采样参数、推理预算和令牌预算均unknown。未使用baseline、其他文档答案、旧output、研究裁决/参考模型、development_reference或upstream_reference。来源事实未外部核验。', '',
    f"首次作者脚本调用的编码失败保存在[失败记录]({report['failure_log']})，当时未创建交付目录；显式UTF-8解码编译后完成。四篇v1实际组装没有失败目录；没有补哈希、伪造人审或覆盖既有完整包。", '',
    f"[机器完成记录]({json_path.resolve().as_posix()})"
]
with md_path.open('x', encoding='utf-8', newline='\n') as out:
    out.write('\n'.join(lines)+'\n')
print(json.dumps({'documents':len(rows),'goals':60,'groups':5,'completion':str(json_path),'manifest_files_verified':sum(row['manifest_files_hash_verified'] for row in rows),'quotes_exact_verified':sum(row['submitted_quotes_exact_and_source_version_verified'] for row in rows)}, ensure_ascii=False))
