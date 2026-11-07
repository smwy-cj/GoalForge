"""Package Codex-authored judgments; this script does not classify goals automatically."""
import hashlib
import json
from collections import Counter
from pathlib import Path

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[1]
PACKETS = ROOT / 'runs/codex-comparison-2026-10-22/packets'

# id, verdict, source turns additionally reviewed, explanation, recommended treatment.
CASES = [
    ('DOC003-G003', 'representation_gap', [123],
     '1.5×/2×是受访者为安全留出的个人缓冲。当前上下文保留了这一点，目标可以成立；不能把1.5倍误作IATA规定，严格性与可配置性尚未明确。',
     '保留个人中转安全目标；将缓冲标为涉众自设约束/策略，严格性待确认。IATA相关事实在本轮仅作为受访者说法，未外部核实。'),
    ('DOC003-G005', 'semantic_strengthening', [73, 119],
     '受访者明确可以接受红眼航班，只是更希望保证睡眠。标题“避开红眼”比该可让步偏好更强，且与自身context相抵触；40–60小时过长行程是另一项权衡，不宜混成统一禁用条件。',
     '拆为控制行程耗时/保障休息的质量目标与偏好：其他条件合适时优先非红眼，红眼仍可接受。不得自动作为排除所有红眼航班的筛选约束。'),
    ('DOC003-G008', 'representation_gap', [15],
     '提前订票是获得较好价格的个人策略和理想计划，原文也承认实际经常提前1–2周订。作为涉众策略可保留，不能自动成为系统强制提前期。',
     '分开记录较好价格这一结果与提前订票这一策略；保留理想/实际差异，不增加强制日期规则。'),
    ('DOC007-G001', 'valid', [22, 56],
     '节省忙碌周采购时间是目标，自提优于配送是有费用、距离条件的履约偏好，当前context保存了这个区别。',
     '保留目标和条件；后续需要方案比较时再结构化自提/配送的条件偏好。'),
    ('DOC007-G008', 'valid', [46, 50],
     '推荐信息流是弱强度的明确建议，当前context已经保留仅在零食等探索情境成立及would kind of be interesting的语气。与常规补货不探索并不矛盾。',
     '保留待确认提议与情境，不升级为所有类目必备功能。'),
    ('DOC008-G007', 'source_modality', [71, 73, 75, 77],
     '原句报告通话随机断连及等待恢复。稳定通话是合理的Maintain目标候选，但从故障陈述到规范性目标的推断没有在explicit/direct标签中体现。不能据此证明故障根因。',
     '保留断连这一障碍候选，关联连续通话目标；若无另外的明确要求，将目标记为inferred并写出推理和假设。'),
    ('DOC014-G008', 'representation_gap', [35],
     '原文明确偏好黑色或白色界面，足以支持外观改善目标候选。偏好进入目标列表本身不构成错误，但黑/白是备选方案，不能要求同时满足，也未承诺必须改色。',
     '保留外观偏好及黑/白备选，不标成必选方案或无依据功能需求。'),
    ('DOC014-G010', 'semantic_strengthening', [55, 57],
     '原文说本人在PC上偏好关闭通知并已自行关闭，没有规定产品初始默认值。标题增加“默认”引入了设置状态/产品行为含义。',
     '改为本人在电脑上倾向不接收通知，需要时自主打开；产品默认状态保持未决，不由个人习惯直接推出。'),
    ('DOC014-G012', 'semantic_strengthening', [61],
     '原文多次明确本地缓存只是猜测，并表达登录后泄露城市的条件性担忧。输出把猜测变成只存本地/不留存的明确方案目标，explicit/direct不足以支持整句。隐私意图有依据，本地唯一存储架构未被确认。',
     '保留防止未授权披露位置的隐私目标候选、泄露风险和登录条件；缓存位置记为未证实信念，本地存储仅作为待评估方案。'),
    ('DOC015-G001', 'valid', [17],
     '个性化推荐是目标，最高优先级是附加排序；两者可以同时成立。',
     '保留目标，另表达推荐>无障碍>社区>创作者工具的排序，不把较低优先级等同可删除。'),
    ('DOC015-G002', 'valid', [17],
     '无障碍能力是目标，其第二优先级是相对排序，不能因此降为非目标。',
     '保留无障碍目标和排序；是否强制履行不能仅由排名判断。'),
    ('DOC015-G003', 'valid', [17],
     '社区参与是目标，第三优先级是目标间偏好，现有文本保留了含义。',
     '保留社区目标及相对排序，不将排序当精化或冲突关系。'),
    ('DOC015-G004', 'valid', [17],
     '创作者工具是平台目标，第四优先级本身不意味着可选或无需求价值。',
     '保留目标及排序；如需mandatory/optional应另取证。'),
    ('DOC017-G004', 'representation_gap', [19],
     '主体内容是投递决策中各评价标准的优先顺序。文本忠实，但将其仅作普通目标节点，后续难以区分决策偏好和希望达到的结果。',
     '表示为选择合适职位目标下的评价标准排序：角色匹配度>薪资>地点>公司声誉；不增加任何具体阈值。'),
    ('DOC020-G011', 'valid', [25, 27],
     '重要邮件不误入垃圾箱是Avoid目标，不是因为含否定词就变成障碍。误分类是障碍候选，宁可多收垃圾也不漏重要邮件是取舍偏好，当前context已经保留。',
     '保留目标；如扩展模型，可将误分类链接到该目标，并表达降低重要邮件漏判优先于减少垃圾邮件。'),
    ('DOC020-G015', 'valid', [59],
     '可靠性达到足够程度后才愿依赖提醒，是有条件的目标/接受态度。当前标题保留了条件，没有给出不存在的准确率阈值。',
     '保留条件和待确认的可靠程度，不擅自添加百分比指标。'),
    ('DOC023-G008', 'valid', [11, 13, 15],
     '原文不仅陈述困难，也说明所寻找的人群和希望得到更精确背景结果。不能机械地因出现抱怨就把整项目标判错或强制改成inferred。精度改善是有依据的目标。',
     '保留目标；将不相关结果作为障碍候选。对“精确命中”的可检验标准保留未决。'),
    ('DOC023-G009', 'boundary', [13, 15],
     '访问更多潜在联系人有明确目的依据，付费也被接受为解决办法。“不被免费账号上限卡住”可描述受阻处境，但不能据此推成永久免费无限访问。当前文本尚未明确作此承诺，不能直接判幻觉。',
     '保留足够候选覆盖目标，分开免费上限障碍、购买会员/调整关键词策略及费用权衡。'),
    ('DOC026-G003', 'representation_gap', [11],
     '最便宜车型是通常选择，多人出行是明确例外。当前含义忠实，属于情境性方案偏好，不是普遍最低价硬要求。',
     '保留条件偏好与人数约束；必要时置于完成适当出行这一目标的方案选择层。'),
    ('DOC026-G007', 'source_modality', [13],
     '受访者认为取消可能损害乘客评分并因此尽量不取消。输出context将“I think”强化成“他知道”，目标又标explicit/direct。可推断维护评分的关切，但取消影响评分的实际规则及取消免责诉求均未得到证实。',
     '区分维护评分的推断目标、对取消后果的未证实信念及少取消策略；不得把信念提升为平台业务规则或已确认免责要求。'),
    ('DOC026-G008', 'representation_gap', [19],
     '公司报销时愿多花20美元少等20分钟是情境性取舍，当前文本保留了关键条件，本身没有改错。缺少结构化偏好不能直接算语义错误。',
     '表达公司报销情境下等待时间优先于车费；该示例不能外推为任何情况下每分钟价值1美元。'),
    ('DOC027-G007', 'valid', [13],
     '原文明确不希望频繁宕机，同时接受偶发中断。标题和context忠实，属于可用性质量目标，不能因涉及坏事件就归为纯障碍。',
     '保留目标和容忍度；频繁/偶发阈值待确认，不能改为零宕机。'),
    ('DOC027-G009', 'source_modality', [47, 49],
     '原句描述信息流停止加载、回顶刷新及可能漏帖的困难。连续加载目标推断合理，但explicit/direct没有表达从症状推导维护目标的步骤。',
     '保留停止加载障碍候选、连续浏览目标候选与回顶刷新策略，目标推断注明依据。'),
    ('DOC028-G013', 'source_modality', [39],
     '原句描述现有缓存能力及离线限制，并未明确要求新增或保证离线阅读。现有能力可以支持Maintain目标候选，但需要意图依据，不能仅凭能力事实标为explicit/direct。',
     '将已缓存帖子可读记录为现状，离线读帖维持目标作为待确认推断；保留无法刷新/发帖限制，不扩为完整离线功能。'),
    ('DOC031-G007', 'source_modality', [19],
     '原文的直接表达是历史信息多导致难定位消息，查找特定消息的目的也明确。更精准搜索是合理抽象，整句直接支持的强度仍需说明；“不必筛大量历史消息”不是用户明确批准的唯一解决方案。',
     '保留定位所需消息的目标和结果过多障碍候选；精准检索这一补救质量目标记推断或补充明确支持，不能自行要求删除历史消息。'),
    ('DOC031-G010', 'boundary', [31],
     '受访者除了抱怨小窗口难导航，还明确称这是可考虑改善的方面。目标有效。不能仅因目标采用正向表达就断言必须从explicit改inferred，但“可考虑”的承诺强度应保留。',
     '保留小窗口易导航目标候选，标明改善提议/待确认；不升级为已承诺的强制需求。'),
    ('DOC005-C002', 'valid', [19, 21, 23],
     'K-pop/R&B等是内容口味和背景；没有直接推出“平台只应提供这两类音乐”的依据。保留为偏好且不凭空制造专属功能目标是合理的。',
     '保留个人口味背景。若用于推荐目标，作为条件/偏好证据使用，不推成排他内容约束。'),
    ('DOC005-C004', 'valid', [31],
     'Spotify缺某些混音导致转用YouTube，是内容可得性限制/障碍候选。保留它且不直接要求Spotify收录全部混音是合理的；正式障碍仍需标出相对于哪个目标。',
     '关联找到并听到特定混音的涉众目的，区分跨平台策略与单平台全曲库方案。'),
    ('DOC005-C009', 'under_extraction_candidate', [47, 63, 65, 67, 69],
     '对Spotify的方案偏好是正确的一面；访谈同时讨论过去想做但做不到的社交活动和如今可用的共享能力。仅以“未表达具体结果”挡住后续目标推断，可能遗漏共同听歌/分享的维持目标候选。G017的相似听众推荐并不等同共同听歌。',
     '保留Spotify优于Apple的方案偏好，同时提出共同听歌/分享播放列表的维持目标候选，注明推断和历史障碍已缓解；不强制新增指定功能。'),
    ('DOC005-C013', 'under_extraction_candidate', [63, 65, 67],
     '喜欢睡眠定时器确实是方案偏好，但停止播放条件和入睡场景也支持目标候选。现有功能并不自动失去目标资格。当前仅保留诊断、拒绝推断额外目标过于保守，仍需确认其期望而非直接判为强制需求。',
     '候选目标为入睡使用音乐时，能按选定时间或曲终条件停止播放；与25/30分钟等选项偏好分开，明确inferred/pending。'),
    ('DOC005-C019', 'under_extraction_candidate', [104, 105],
     '回答的问题明确询问缺少哪些功能产品就不完整；受访者说没有环境音便不完整，并列为最重要功能。仅作体验偏好弱化了维持环境音可用这一意图。G001仅粗略覆盖背景声音，未明确环境音能力与质量。',
     '补充环境音可用/满足收听目的的维持目标候选或补充G001范围；保留重要性偏好，不把“已具备”作为排除理由。'),
]

LABELS = {
    'semantic_strengthening': '表述被改强或增加方案约束',
    'source_modality': '来源模态/显式与推断的边界偏差',
    'representation_gap': '含义基本忠实，建模角色需明确',
    'valid': '本次未发现该方面语义偏差',
    'boundary': '边界案例，保留目标并限制解释',
    'under_extraction_candidate': '过度过滤导致目标候选遗漏风险',
}


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    records, input_paths, ambiguities = [], set(), []
    all_models = sorted((ROOT / 'output').glob('DOC*/final/goal-model.json'))
    field_counts, diag_counts, diag_documents = Counter(), Counter(), []
    for path in all_models:
        model = read(path)
        input_paths.add(path)
        for goal in model['goals']:
            field_counts.update(goal.keys())
        if model.get('diagnostics'):
            diag_documents.append(path.parts[-3])
            diag_counts.update(d['category'] for d in model['diagnostics'])
    for item_id, verdict, turn_ids, explanation, treatment in CASES:
        doc = item_id[:6]
        model_path = ROOT / f'output/{doc}/final/goal-model.json'
        source_path = ROOT / f'datasets/processed/goalforge-v1/source/{doc}.json'
        text_path = source_path.with_suffix('.txt')
        packet_path = PACKETS / f'{doc}.json'
        input_paths.update([model_path, source_path, text_path, packet_path])
        model, source, packet = read(model_path), read(source_path), read(packet_path)
        assert source['turns'] == packet['source'], doc
        is_goal = '-G' in item_id
        if is_goal:
            original = next(g for g in model['goals'] if g['goal_id'] == item_id)
            enriched = next(g for g in packet['local_goals'] if g['goal_id'] == item_id)
            assert original == {k: v for k, v in enriched.items() if k != 'quotes'}, item_id
            evidence = enriched['quotes']
        else:
            original = next(d for d in model['diagnostics'] if d['candidate_id'] == item_id)
            evidence = original['evidence_candidates']
        canonical = text_path.read_text(encoding='utf-8')
        mapped = []
        relevant_turn_ids = set(turn_ids)
        for e in evidence:
            matches = []
            for t in source['turns']:
                start = 0
                while True:
                    at = t['text'].find(e['quote'], start)
                    if at < 0:
                        break
                    a = t['start_char'] + at
                    b = a + len(e['quote'])
                    assert canonical[a:b] == e['quote'], (item_id, e)
                    matches.append({'source_id': t['source_id'], 'start_char': a, 'end_char': b})
                    relevant_turn_ids.add(int(t['turn']))
                    start = at + 1
            assert matches, (item_id, e)
            if len(matches) != 1:
                ambiguities.append({'item_id': item_id, 'quote': e['quote'], 'matches': matches})
            mapped.append({'submitted_evidence': e, 'canonical_matches': matches})
        turns = [t for t in source['turns'] if int(t['turn']) in relevant_turn_ids]
        assert set(turn_ids).issubset({int(t['turn']) for t in turns}), item_id
        records.append({
            'item_id': item_id, 'document_id': doc,
            'item_kind': 'goal' if is_goal else 'diagnostic',
            'original': original, 'verdict': verdict, 'verdict_zh': LABELS[verdict],
            'rationale': explanation, 'recommended_treatment': treatment,
            'source_scope': 'Attached evidence plus listed source turns; not a new full-document adjudication.',
            'source_turns': turns, 'mapped_evidence': mapped,
        })
    for rel in ['第10章.模型驱动方法.ppt', 'runs/planning-2026-10-22/ppt-slides.json',
                'skills/goal-extraction/SKILL.md', 'skills/goal-tracing/references/evidence-rules.md']:
        input_paths.add(ROOT / rel)
    manifest = [{'path': p.relative_to(ROOT).as_posix(), 'sha256': sha(p)}
                for p in sorted(input_paths)]
    counts = Counter(r['verdict'] for r in records)
    result = {
        'date': '2026-10-23',
        'reviewer': 'Codex; context-aware authored semantic review, not independent human ground truth',
        'scope': {
            'schema_scan_documents': len(all_models), 'schema_scan_goals': field_counts['goal_id'],
            'targeted_documents': len({r['document_id'] for r in records}),
            'targeted_goals': sum(r['item_kind'] == 'goal' for r in records),
            'targeted_diagnostics': sum(r['item_kind'] == 'diagnostic' for r in records),
            'sampling': 'Purposive boundary/risk cases plus positive controls, not a random sample or all-goal reclassification.',
        },
        'goal_field_counts': dict(field_counts),
        'diagnostic_documents': diag_documents, 'diagnostic_category_counts': dict(diag_counts),
        'targeted_verdict_counts': dict(counts), 'verdict_labels': LABELS,
        'literature': [
            {'title': 'Assessing requirements-related risks through probabilistic goals and obstacles',
             'authors': 'Antoine Cailliau; Axel van Lamsweerde', 'year': 2013,
             'url': 'https://webperso.info.ucl.ac.be/~avl/files/rej13.pdf',
             'reviewed_sections': ['2.1 Goal-oriented system modeling', '2.2 Obstacle analysis']},
            {'title': 'Specifying and Reasoning about Contextual Preferences in the Goal-oriented Requirements Modelling',
             'authors': 'Botangen et al.', 'year': 2018,
             'url': 'https://arxiv.org/abs/1905.06437',
             'reviewed_sections': ['Introduction', '2.1 Overview of Goal Modelling', '3.2 Contextual Preference Specification']},
        ],
        'ppt_scope': 'Native-text extraction, slides 9–18 and classification slide 12; no claim of diagram/layout inspection.',
        'cases': records,
    }
    write(RUN / 'review.json', result)
    write(RUN / 'input-manifest.json', {'inputs': manifest})
    md = ['# 目标、障碍与偏好：逐例证据附录', '',
          '日期：2026-10-23。Codex自动语义复核。目标性选例，不能外推整批错误率。', '',
          '源文轮次采用canonical的T编号；原输出S编号是另一套定位标识，不能直接当作T编号。', '']
    for r in records:
        md += [f"## {r['item_id']}：{r['verdict_zh']}", '',
               f"原输出：{r['original']['statement']}", '',
               f"判断：{r['rationale']}", '',
               f"建议：{r['recommended_treatment']}", '',
               '核对原文（完整所列轮次，包含附带证据定位到的轮次）：', '']
        for t in r['source_turns']:
            md += [f"**{t['source_id']} / {t['speaker']}**", '', '> ' + t['text'].replace('\n', '\n> '), '']
    (RUN / 'case-evidence.md').write_text('\n'.join(md), encoding='utf-8')
    validation = {
        'status': 'passed', 'record_count': len(records),
        'unique_ids': len({r['item_id'] for r in records}),
        'mapped_evidence_count': sum(len(r['mapped_evidence']) for r in records),
        'non_unique_quote_matches': ambiguities,
        'input_files_hashed': len(manifest),
        'checks': ['Canonical sources agree with prior packets', 'Each original item agrees with actual output',
                   'Every evidence quote located in canonical source and exact character slice verified',
                   'All explicitly requested source turns exist', 'IDs unique',
                   'All hashed inputs remain unchanged after packaging'],
        'semantic_limit': 'Packaging checks verify traceability, not the truth of authored semantic judgments.',
    }
    assert validation['unique_ids'] == len(records)
    for item in manifest:
        assert sha(ROOT / item['path']) == item['sha256'], item['path']
    write(RUN / 'validation.json', validation)
    print(json.dumps({'scope': result['scope'], 'verdict_counts': dict(counts), 'validation': validation}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
