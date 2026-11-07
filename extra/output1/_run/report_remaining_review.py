"""Publish the verified coverage and stable finding records as readable reports."""
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]
ROUND = OUT / 'review/remaining-20261025'


def load(path):
    return json.loads(Path(path).read_bytes().decode('utf-8-sig'))


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def text_cell(value):
    if isinstance(value, list):
        value = '；'.join(map(str, value))
    return str(value or '—').replace('|', '／').replace('\n', ' ')


def status_text(status):
    if status == 'resolved_in_separate_revision_independently_rechecked':
        return '已修订并独立补查'
    if 'unconfirmed' in status or 'not_confirmed' in status:
        return '未确证风险，保留观察'
    if 'appropriately_unresolved' in status:
        return '待真实澄清'
    if status == 'unresolved_information':
        return '资料未给出，继续保留未知'
    if status == 'no_confirmed_omission':
        return '已核查，未确认遗漏'
    if status == 'not_counted':
        return '表征限制，未计遗漏'
    return status


def main():
    coverage = load(ROUND / 'coverage.json')
    assert coverage['status'] == 'passed' and not coverage['remaining_unreviewed_goal_ids']
    reports = {i: load(ROUND / f'batch{i}/review.json') for i in (1, 2, 3)}
    repair_file = ROUND / 'repairs.json'
    repairs = load(repair_file)['repairs'] if repair_file.exists() else []
    resolutions = {fid: r for r in repairs for fid in r['finding_ids']}
    findings = []
    for number, report in reports.items():
        native = list(report['findings'])
        seen = {f.get('finding_id', f.get('id')) for f in native}
        for risk in report.get('candidate_omission_risks', []):
            identifier = risk.get('finding_id', risk.get('id', risk.get('risk_id')))
            assert identifier, (number, 'risk needs stable ID')
            if identifier not in seen:
                native.append(dict(risk, finding_id=identifier, category='候选遗漏风险'))
                seen.add(identifier)
        for original in native:
            f = dict(original)
            f.setdefault('finding_id', f.get('id'))
            f['source_report'] = f'batch{number}/review.json'
            f['initial_status'] = original['status']
            if f['finding_id'] in resolutions:
                f['effective_status'] = 'resolved_in_separate_revision_independently_rechecked'
                f['resolution'] = resolutions[f['finding_id']]
            else:
                f['effective_status'] = original['status']
            findings.append(f)
    material = [f for f in findings if f.get('counts_as_confirmed_semantic_error', False)]
    opened = [f for f in material if f['effective_status'] != 'resolved_in_separate_revision_independently_rechecked']
    assert not opened, 'Confirmed material findings require a repair or an explicitly documented unresolved closure before reporting complete.'
    selected = [r for r in load(OUT / '_run/delivery-index.json')['documents'] if r['arm'] == 'revised']
    current_support = sum((Counter(r['support']) for r in selected), Counter())
    blocking = []
    for r in selected:
        model = load(OUT / r['json'])
        for issue in model['issues']:
            if issue['blocking']:
                blocking.append(dict(document_id=r['document_id'], model_path=r['json'], issue=issue))
    summary = dict(round_id='remaining-20261025', completed_at_utc=datetime.now(timezone.utc).isoformat(),
                   status='complete_with_local_unresolved_candidates' if blocking else 'complete',
                   coverage=coverage, findings=findings, newly_confirmed_material_findings=len(material),
                   open_confirmed_material_findings=len(opened), repairs=repairs, current_author_support_labels=dict(current_support),
                   remaining_local_blockers=blocking, human='pending', formal_proof='not_run',
                   exact_model='unknown', sampling_parameters='unknown', budget='unknown',
                   note='All selected goal IDs have independent model-context semantic review coverage, not proof of correctness/completeness or human acceptance. Original 3-document before/after comparison remains unchanged.')
    save(ROUND / 'summary.json', summary)
    lines = [
        '# 剩余目标独立复核结果', '', '日期：2026-10-25。', '',
        f'此前未审的243个目标已全部补齐独立复核。连同原有316个，新版34篇当前交付的{coverage["total_selected_goals"]}个目标均有独立上下文模型复核记录，全部{coverage["total_selected_groups"]}个精化组沿用已绑定的既有复核；发生变化的对象另行补查。', '',
        f'本轮新确认实质语义问题{len(material)}项；当前未解决的确证实质问题{len(opened)}项。问题条目不等于错误目标数，候选遗漏、表达改进和资料未知分别记录。', '',
        '## 复核范围', '', '| 批次 | 篇数 | 新增逐目标复核 | 详细记录 |', '|---|---:|---:|---|',
    ]
    for number, report in reports.items():
        lines.append(f'| {number} | {len(report["documents"])} | {sum(len(d["reviewed_goal_ids"]) for d in report["documents"])} | [批{number}报告](batch{number}/report.md) |')
    lines += [
        '| 合计 | 20 | 243 | [完整目标ID及版本绑定](coverage.json) |', '',
        '各篇先完整读取来源问答，保存来源检查点，再逐项核对目标陈述、主体、条件、强度、选定方式、来源/推断、支持判断和绑定引文，并回查后续例外。未读取作者自检作为接受依据，也未读取历史裁决或研究参考答案。新代理只接收各自规则、来源和目标包。', '',
        '## 本轮发现及处置', '',
    ]
    if findings:
        lines += ['| 编号 | 对象 | 性质 | 具体判断 | 最终状态 |', '|---|---|---|---|---|']
        for f in findings:
            brief = {
                'RR1-CR01': '偶尔收听播客是否纳入本次歌曲用例，范围仍待确认。',
                'RR1-CR02': '离线缓存主要是能力现状，尚未确认独立的维持或扩展意图。',
                'RR2-001': '情境推荐实例已写入判断理由，现补入T043连续原文作为绑定证据。',
                'RR2-C01': '看解后隔时重做同题，是否由现有回顾目标承接仍待确认。',
                'RR3-001': '章节剩余时间与章节进度的独立或合并表达范围仍待确认。',
            }.get(f['finding_id'], f.get('specific_unsupported_part', f.get('reason')))
            objects = f.get('goal_ids', f.get('target_ids', [])) or f.get('document_id')
            category = '证据呈现改善' if f.get('category') == 'expression_insufficiency' else f.get('category')
            lines.append('| ' + ' | '.join(text_cell(v) for v in [f['finding_id'], objects,
                category, brief, status_text(f['effective_status'])]) + ' |')
    else:
        lines.append('声明范围内未确认新增问题；逐目标理由、正确边界及资料限制仍保留于三个批次报告中。')
    lines += ['', '## 当前待确认内容', '']
    if blocking:
        for entry in blocking:
            issue = entry['issue']
            detail = '匿名发帖的独立意图尚不明确，支持不足。' if issue['target_id'] == 'DOC036-G17' else issue['message']
            lines.append('- ' + entry['document_id'] + ' / ' + issue['target_id'] + '：' + detail)
        lines.append('')
    lines += [
        'DOC036-G17的独立匿名发帖意图仍需真实澄清。此前已读完该篇77轮并确认支持不足；本轮不会以重复检查或替受访者回答消除该未知。局部候选不影响其他已有依据目标的保留，人工采纳仍pending。', '',
        '## 结果入口与记录边界', '',
        '- [当前模型目录](../../README.md)：每篇当前选择版本。',
        '- [统一问题清单](统一问题清单.md)：合并前期与本轮发现，区分已解决、待确认和历史基线记录。',
        '- [本轮机器汇总](summary.json)与[逐目标覆盖绑定](coverage.json)。',
        '- [DOC029补证版模型](../../revised/DOC029/v2/delivery/goal-model.html)及[独立补查](batch2/followup.md)：目标含义不变，仅补情境实例原文，其他15目标和唯一组不变。',
        '- [本轮开始前版本选择](prior-state/_run/delivery-index.json)：保留首次处理时的目录和统计口径；prior-state是原始字节存档，路径仍相对于output1。', '',
        '现有规则和技能快照未修改。若出现新的修订包，原件、修订原因、真实源文与独立补查一并保留；内部模型版本可能仍为v1，实际以外层路径和SHA-256区分。核心inspection独立语义/形式证明字段不手填通过，本轮语义复核是单独记录层。', '',
        '全目标覆盖不等于所有可能意图都已穷尽，也不等于人工认可、产品事实外部验证或形式证明。模型标识、采样参数和预算未知；本轮不能扩大三篇修改前后比较的结论，不能据数量推断准确率或skills提升幅度。',
    ]
    (ROUND / '复核总结.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    # Preserve native reports. Normalize only the additional cross-round index.
    unified = []
    pilot = load(OUT / 'review/pilot-review.json')
    for f in pilot['findings']:
        row = dict(f)
        row.update(finding_id=f['id'], round='pilot', scope=f['branch'], source_report='review/pilot-review.json')
        row['effective_status'] = 'resolved_in_separate_revision_independently_rechecked' if f['id'] == 'PR-003' else f['status']
        if f['branch'] == 'baseline':
            row['current_delivery_relevance'] = 'Historical comparator preserved; not an unresolved revised-delivery defect'
        unified.append(row)
    for f in load(ROUND / 'prior-state/review/expanded-review.json')['findings']:
        row = dict(f)
        row.update(round='initial_expanded_review', scope='revised')
        unified.append(row)
    for f in load(OUT / 'review/expanded-batch3/review.json').get('candidate_omission_risks', []):
        row = dict(f)
        row.update(finding_id=f['id'], round='initial_expanded_review', scope='revised',
                   category='候选遗漏风险/边界回查', effective_status=f['status'],
                   reason=f['description'], source_report='review/expanded-batch3/review.json')
        unified.append(row)
    for f in findings:
        row = dict(f)
        row.update(round='remaining-20261025', scope='revised')
        unified.append(row)
    save(ROUND / 'unified-findings.json', dict(findings=unified,
        new_round_correct_boundaries={str(n): r.get('correct_boundaries', []) for n, r in reports.items()},
        note='Native IDs/statuses preserved. Includes correct boundaries and unknowns; do not treat item count as error count.',
        prior_material_fixed=['ER-B3-001'], current_material_ids=[f['finding_id'] for f in material]))
    issue_lines = ['# 统一问题清单', '',
        '合并试运行、首次扩展复核与本轮补审。原报告不覆盖；本清单提供当前处置索引。正确边界案例与合理未决组不是错误，历史基线问题也不作为当前新版缺陷。', '',
        '## 新版需关注的发现', '', '| 编号 | 阶段 | 对象 | 问题或风险 | 当前状态 |', '|---|---|---|---|---|']
    for f in unified:
        if f['scope'] != 'revised':
            continue
        category = text_cell(f.get('category'))
        if f.get('severity') == 'none':
            continue
        objects = f.get('goal_ids', f.get('object_ids', f.get('target_ids', f.get('targets', f.get('objects', []))))) or f.get('document_id', [])
        detail = f.get('specific_unsupported_part') or f.get('reason') or f.get('reasoning') or f.get('judgment')
        stage = {'pilot':'三篇试运行','initial_expanded_review':'首次扩展复核','remaining-20261025':'本轮补审'}[f['round']]
        issue_lines.append('| ' + ' | '.join(text_cell(v) for v in [f['finding_id'], stage, objects, detail, status_text(f.get('effective_status', f['status']))]) + ' |')
    issue_lines += ['', '## 历史基线与正确边界', '',
        'PR-001、PR-002、PR-004属于修改前基线，按比较设计保留原样；不修写对照组来改善比较。原文支持、推断有据的现有能力维持、软偏好、避免型目标及候选精化的正确边界，详见[完整机器清单](unified-findings.json)和各批报告。', '',
        '## 对下一轮skills调整的意义', '',
        '先按具体案例判断执行偏差与规则缺口。已有规则明确要求整句支持、分开处理相邻语义成分、保留语气及必要引文；个别生成结果违反规则不能直接证明规则本身有缺陷。重复类型可转为后续检查项或开发回归材料，再用新增样本验证，不将带答案的DOC案例放进生成参考包。', '',
        '[返回本轮总结](复核总结.md) · [当前结果目录](../../README.md)',
    ]
    (ROUND / '统一问题清单.md').write_text('\n'.join(issue_lines) + '\n', encoding='utf-8')
    (ROUND / 'README.md').write_text(
        '# 剩余目标独立复核（2026-10-25）\n\n'
        '本轮243个目标已补齐；所有新版目标现有独立模型上下文复核记录，人工仍待审。\n\n'
        '- [复核总结](复核总结.md)\n- [统一问题清单](统一问题清单.md)\n- [覆盖及版本绑定](coverage.json)\n'
        '- [本轮计划](plan.json)\n- [当前模型目录](../../README.md)\n', encoding='utf-8')
    print(json.dumps(dict(newly_reviewed_goals=243, selected_goals=coverage['total_selected_goals'],
                         new_findings=len(findings), new_material_findings=len(material), unresolved_local_issues=len(blocking)), ensure_ascii=False))


if __name__ == '__main__':
    main()
