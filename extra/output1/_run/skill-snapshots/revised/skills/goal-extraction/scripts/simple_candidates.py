"""Minimal goal-only extraction contract; preserve native evidence and old renderers."""
import copy

SCHEMA = 'goalforge-extraction-3'


def legacy_shape(data):
    """Validation adapter only. Never stamp this transformed object as a judgment input."""
    result = copy.deepcopy(data)
    result['schema_version'] = 'goalforge-extraction-draft-2'
    for goal in result['candidates']:
        if any(k in goal for k in ('category', 'subtype', 'classification_reason')):
            raise ValueError('Goal-only extraction has no category/subtype/classification_reason')
        goal.update(category='goal', subtype='unspecified', classification_reason='')
    return result


def validate(data):
    from render_review import validate as validate_old
    if data.get('schema_version') != SCHEMA:
        raise ValueError('Unsupported goal-only schema')
    validate_old(legacy_shape(data))
    return {s['source_id']: s for s in data['segments']}


def render(data):
    from render_review import safe
    validate(data)
    lines = ['# 目标清单', '', '请核对目标是否符合原意；需要时在统一意见区说明。', '']
    lines += ['材料：' + '、'.join(safe(m['file_name']) for m in data['materials']), '']
    if data['status'] != 'completed':
        lines += ['处理范围不完整，请注意下列限制。', '']
    for i, g in enumerate(data['candidates'], 1):
        lines += [f'{i}. {safe(g["statement"])}' + ('（根据原文推断，需确认）' if g['origin'] == 'inferred' else '')]
        if g['context']:
            lines += ['   条件：' + safe('；'.join(g['context']))]
    if not data['candidates']:
        lines += ['本次可读材料中未提取到目标。']
    questions = [q['question'] for q in data['review_questions']]
    limits = data['limitations'] + data['coverage']['omissions'] + data['conversion']['issues']
    if questions or limits:
        lines += ['', '## 需要留意', ''] + ['- ' + safe(x) for x in questions + limits]
    lines += ['', '原文依据保存在机器结果和来源附件中，可让助手按目标编号展开。', '', '## 我的意见', '', '']
    return '\n'.join(lines)
