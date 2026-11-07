"""Build, inspect, package and process feedback for the conceptual KAOS subset.

No model calls. Supplied judgments are evidence-bound authoring, not formal proof.
Legacy graph models keep their existing entrypoints and are never auto-converted.
"""
import argparse
import copy
import hashlib
import html
import json
import re
import sys
import unicodedata
from pathlib import Path

SKILLS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILLS / 'goal-tracing/scripts'))
sys.path.insert(0, str(SKILLS / 'goal-extraction/scripts'))
from trace_candidates import trace, locate
from simple_candidates import validate as validate_extraction

SCHEMA = 'goalforge-kaos-1'
FEEDBACK = 'goalforge-simple-feedback-1'


def encode(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8')


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def object_hash(value):
    return digest(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8'))


def binding(model):
    return dict(model_id=model['model_id'], version=model['version'], sha256=object_hash(model))


def load(path):
    return json.loads(Path(path).read_bytes().decode('utf-8-sig'))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def string_list(value):
    return isinstance(value, list) and all(isinstance(s, str) and s.strip() for s in value)


def ids(items, key):
    require(isinstance(items, list), 'Expected array: ' + key)
    result = {}
    for item in items:
        identifier = item.get(key)
        require(isinstance(identifier, str) and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.:-]{0,119}', identifier), 'Invalid ' + key)
        require(identifier not in result, 'Duplicate ' + key)
        result[identifier] = item
    return result


def decision_template(extraction_raw, judgments_raw):
    data = json.loads(extraction_raw.decode('utf-8-sig'))
    validate_extraction(data)
    return dict(schema_version='goalforge-kaos-decisions-1',
                input_binding=dict(extraction_sha256=digest(extraction_raw), judgments_sha256=digest(judgments_raw)),
                groups=[], questions=[])


def build(extraction_raw, judgments_raw, source_raw, decision_raw, previous=None, feedback=None):
    data = json.loads(extraction_raw.decode('utf-8-sig'))
    validate_extraction(data)
    source = source_raw.decode('utf-8')
    require(digest(source_raw) == data['document_hash'], 'Source hash mismatch')
    judgments = json.loads(judgments_raw.decode('utf-8-sig'))
    traced = trace(data, judgments, source, digest(extraction_raw))
    decisions = json.loads(decision_raw.decode('utf-8-sig'))
    require(decisions.get('schema_version') == 'goalforge-kaos-decisions-1', 'Unsupported KAOS judgment schema')
    require(decisions.get('input_binding') == dict(extraction_sha256=digest(extraction_raw), judgments_sha256=digest(judgments_raw)), 'Stale KAOS judgments')
    evidence, goals, issues = {}, [], []
    for c, t in zip(data['candidates'], traced['traces']):
        evidence_ids = []
        for e in t['submitted_evidence'] + t['located_evidence']:
            evidence[e['evidence_id']] = e
            evidence_ids.append(e['evidence_id'])
        require(c['candidate_id'] == t['target_id'], 'Trace target mismatch')
        goals.append(dict(goal_id=c['candidate_id'], statement=c['statement'], actor=c['actor'], conditions=c['context'],
                          origin=c['origin'], inference=c['inference'], support=t['support'], evidence_ids=list(dict.fromkeys(evidence_ids))))
        for item in t['issues']:
            issues.append(dict(target_type='goal', target_id=c['candidate_id'], message=item['reason'],
                               blocking=item['code'] in {'semantic_not_run', 'no_verified_basis', 'version_mismatch'}))
        if t['support']['label'] not in {'direct', 'inferred'}:
            issues.append(dict(target_type='goal', target_id=c['candidate_id'], message='原文尚不足以支持这项目标，或存在相反证据。', blocking=True))
    for q in data['review_questions']:
        for gid in q['candidate_ids'] or [data['document_id'] + '-goal-model']:
            issues.append(dict(target_type='goal' if q['candidate_ids'] else 'model', target_id=gid, message=q['question'], blocking=False))
    model = dict(schema_version=SCHEMA, model_id=data['document_id'] + '-goal-model', version='v1', parent=None,
                 scope=dict(document_id=data['document_id'], coverage=data['coverage']),
                 goals=goals, refinement_groups=copy.deepcopy(decisions['groups']), evidence_index=list(evidence.values()),
                 issues=issues, limitations=list(dict.fromkeys(data['limitations'] + data['coverage']['omissions'] + data['conversion']['issues'])),
                 input_artifacts=[], review=dict(status='pending'), changes=[])
    # The explanation of a relationship may occur outside the goal quotations.
    # Locate those actual passages too, instead of showing an unrelated goal quote.
    segments = {s['source_id']: s for s in data['segments']}
    counter = 0
    for group in model['refinement_groups']:
        for quote in group.pop('evidence_quotes', []):
            require(isinstance(quote, dict), 'Invalid refinement quotation')
            counter += 1
            found = locate(quote, segments.get(quote.get('source_id')), source, data['document_hash'], counter)
            require(found['location_status'] == 'exact' and found['verification_scope'] == 'full_text', 'Refinement quotation must match actual source')
            found['evidence_id'] = 'K' + str(counter).zfill(4)
            model['evidence_index'].append(found)
            group['evidence_ids'] = [found['evidence_id']] + group.get('evidence_ids', [])
    for q in decisions.get('questions', []):
        require(isinstance(q, dict) and q.get('target_type') in {'goal', 'group', 'model'} and isinstance(q.get('message'), str) and q['message'].strip(), 'Invalid modeling question')
        model['issues'].append(dict(target_type=q['target_type'], target_id=q['target_id'], message=q['message'], blocking=False))
    if data['status'] != 'completed':
        model['limitations'].append('资料处理不完整，请核对范围与缺失部分。')
    for g in model['refinement_groups']:
        if g.get('status') != 'supported' or g.get('completeness') != 'complete':
            model['issues'].append(dict(target_type='group', target_id=g.get('group_id'), message='这组层级仍需确认，尚未作为成立的精化展示。', blocking=False))
    if previous is not None:
        require(feedback is not None, 'Revision requires actual feedback bound to the previous model')
        validate_feedback(feedback, previous, submitted=True)
        require(previous['schema_version'] == SCHEMA, 'No automatic legacy KAOS conversion')
        require(model['model_id'] == previous['model_id'], 'Revision must retain the model identity')
        model['parent'] = binding(previous)
        model['version'] = previous['version'] + '.r1'
        model['changes'] = [dict(kind='rebuild_after_feedback', feedback_sha256=object_hash(feedback),
                                 before_goals=previous['goals'], before_groups=previous['refinement_groups'],
                                 removed_goal_ids=sorted(set(g['goal_id'] for g in previous['goals']) - set(g['goal_id'] for g in goals)))]
        # An omitted issue is not a resolution. Preserve every requested change
        # until the author explicitly accounts for it in this bound decision pack.
        dispositions = decisions.get('feedback_dispositions', [])
        require(isinstance(dispositions, list), 'Invalid feedback dispositions')
        targets = {(e['target_type'], e['target_id']): e for e in feedback['entries'] if e['decision'] != 'accept'}
        accounted = {}
        for item in dispositions:
            target = (item.get('target_type'), item.get('target_id'))
            require(target in targets and target not in accounted and item.get('status') in {'addressed', 'unresolved'}
                    and isinstance(item.get('reason'), str) and item['reason'].strip(), 'Invalid/unknown feedback disposition')
            accounted[target] = item
        model['changes'][0]['feedback_dispositions'] = dispositions
        for target, opinion in targets.items():
            if accounted.get(target, {}).get('status') != 'addressed':
                kind, identifier = target
                available = {g['goal_id'] for g in goals} if kind == 'goal' else {g['group_id'] for g in model['refinement_groups']} if kind == 'group' else {model['model_id']}
                if identifier not in available:
                    kind, identifier = 'model', model['model_id']
                model['issues'].append(dict(target_type=kind, target_id=identifier,
                                            message='前轮意见尚待处理：' + opinion['comment'], blocking=False))
        if feedback['note'].strip():
            model['issues'].append(dict(target_type='model', target_id=model['model_id'], message='前轮整体补充（请核对）：' + feedback['note'], blocking=False))
    check_structure(model)
    return model


def check_structure(model):
    require(model.get('schema_version') == SCHEMA, 'Use the correct versioned model tool')
    require(model.get('review') == {'status': 'pending'}, 'This builder cannot manufacture human acceptance')
    goals = ids(model['goals'], 'goal_id')
    groups = ids(model['refinement_groups'], 'group_id')
    evidence = ids(model['evidence_index'], 'evidence_id')
    require(not set(goals).intersection(groups), 'Goal and group IDs must be distinct')
    for g in goals.values():
        require(isinstance(g.get('statement'), str) and g['statement'].strip(), 'Goal statement required')
        require(g.get('origin') in {'explicit', 'inferred'}, 'Only evidence-grounded goals enter this subset')
        require(g.get('actor') is None or isinstance(g['actor'], str), 'Invalid responsibility')
        require(string_list(g.get('conditions')), 'Invalid goal conditions')
        require(g.get('evidence_ids') and set(g['evidence_ids']).issubset(evidence), 'Goal evidence required')
    graph = {gid: [] for gid in goals}
    seen = set()
    for group in groups.values():
        parent, children = group.get('parent_id'), group.get('child_ids')
        require(parent in goals and string_list(children) and children, 'Group parent/members required')
        require(len(children) == len(set(children)) and parent not in children and set(children).issubset(goals), 'Invalid group members')
        require(group.get('kind') == 'and', 'Each group is one sufficient AND alternative; multiple groups encode OR alternatives')
        require(group.get('status') in {'supported', 'proposed'} and group.get('completeness') in {'complete', 'partial'}, 'Invalid refinement status')
        require(isinstance(group.get('rationale'), str) and group['rationale'].strip(), 'Refinement rationale required')
        require(string_list(group.get('assumptions')) and string_list(group.get('evidence_ids')), 'Group assumptions/evidence required')
        require(group['evidence_ids'] and set(group['evidence_ids']).issubset(evidence), 'Unknown or absent group evidence')
        key = (parent, tuple(sorted(children)))
        require(key not in seen, 'Duplicate refinement alternative')
        seen.add(key)
        for gid in children:
            graph[parent].append(gid)
        if active(group):
            require(all(goals[gid]['support']['label'] in {'direct', 'inferred'} for gid in [parent] + children), 'Supported refinement has unsupported goals')
    colors = {}
    def visit(gid):
        require(colors.get(gid) != 1, 'Refinement cycle')
        if colors.get(gid) == 2:
            return
        colors[gid] = 1
        for child in graph[gid]:
            visit(child)
        colors[gid] = 2
    for gid in goals:
        visit(gid)
    for issue in model['issues']:
        require(issue.get('target_type') in {'goal', 'group', 'model'}, 'Invalid issue kind')
        allowed = goals if issue['target_type'] == 'goal' else groups if issue['target_type'] == 'group' else {model['model_id']: model}
        require(issue.get('target_id') in allowed and isinstance(issue.get('message'), str) and issue['message'].strip(), 'Unknown issue target')
    return goals, groups, evidence


def active(group):
    return group['status'] == 'supported' and group['completeness'] == 'complete'


def read_artifacts(model, base):
    result = {}
    base = Path(base).resolve()
    for a in model['input_artifacts']:
        name = a['path']
        target = (base / name).resolve()
        require(name.startswith('attachments/') and base in target.parents and name not in result, 'Unsafe or duplicate attachment')
        raw = target.read_bytes()
        require(digest(raw) == a['sha256'], 'Attachment hash mismatch: ' + name)
        result[name] = raw
    return result


def inspect(model, base):
    check_structure(model)
    files = read_artifacts(model, base)
    required = ['extraction.json', 'judgments.json', 'source.txt', 'kaos-decisions.json']
    require(all('attachments/' + k in files for k in required), 'Missing proof attachments')
    previous = json.loads(files['attachments/previous-model.json']) if model['parent'] else None
    feedback = json.loads(files['attachments/review-feedback.json']) if model['parent'] else None
    if previous is not None:
        require(binding(previous) == model['parent'], 'Previous model binding mismatch')
    rebuilt = build(*(files['attachments/' + k] for k in required), previous=previous, feedback=feedback)
    for key in ('schema_version', 'model_id', 'version', 'parent', 'scope', 'goals', 'refinement_groups', 'evidence_index', 'issues', 'limitations', 'review', 'changes'):
        require(model[key] == rebuilt[key], 'Model differs from actual source/judgments: ' + key)
    canonical = files['attachments/source.txt'].decode('utf-8')
    for e in model['evidence_index']:
        require(e['location_status'] == 'exact' and e['verification_scope'] == 'full_text' and e['source_version_status'] == 'verified', 'Unverified evidence location')
        require(type(e['start_char']) is int and type(e['end_char']) is int and 0 <= e['start_char'] < e['end_char'] <= len(canonical) and canonical[e['start_char']:e['end_char']] == e['quote'], 'Evidence quote mismatch')
    return dict(schema_version='goalforge-kaos-check-1', model=binding(model), structure='passed',
                independent_semantic='not_run', formal_proof='not_run', human='pending',
                readiness='blocked' if any(i['blocking'] for i in model['issues']) else 'reviewable',
                note='已核验结构、实际原文与版本绑定；精化充分性来自编制判断，未进行形式化证明。')


def validate_feedback(packet, model, submitted=False):
    require(packet.get('schema_version') == FEEDBACK and packet.get('model') == binding(model), 'Feedback model/version/hash mismatch')
    require(packet.get('status') in {'draft', 'submitted'} and (not submitted or packet['status'] == 'submitted'), 'Submitted feedback required')
    goals, groups, _ = check_structure(model)
    require(isinstance(packet.get('entries'), list) and isinstance(packet.get('form_drafts'), dict) and isinstance(packet.get('note'), str), 'Invalid feedback content')
    seen = set()
    for entry in packet['entries']:
        kind, target = entry.get('target_type'), entry.get('target_id')
        allowed = goals if kind == 'goal' else groups if kind == 'group' else {model['model_id']: model} if kind == 'model' else {}
        require(target in allowed and (kind, target) not in seen, 'Unknown/duplicate feedback target')
        seen.add((kind, target))
        require(entry.get('decision') in {'accept', 'modify', 'defer'} and isinstance(entry.get('comment'), str), 'Invalid decision')
        require(entry['decision'] == 'accept' or entry['comment'].strip(), 'Please explain the requested change/uncertainty')
    for key, draft in packet['form_drafts'].items():
        require(isinstance(draft, dict) and draft.get('target_type') in {'goal', 'group', 'model'}, 'Invalid draft')
        allowed = goals if draft['target_type'] == 'goal' else groups if draft['target_type'] == 'group' else {model['model_id']: model}
        require(draft.get('target_id') in allowed and key == draft['target_type'] + ':' + draft['target_id'], 'Unknown draft target')
        require(draft.get('decision') in {'', 'accept', 'modify', 'defer'} and isinstance(draft.get('comment'), str), 'Invalid unfinished form')
    if submitted:
        require(not packet['form_drafts'], 'Unfinished forms: save entries or export a draft')
        require(packet['entries'] or packet['note'].strip(), 'No review opinions to submit')


def process_feedback(model, packet):
    validate_feedback(packet, model, submitted=True)
    affected_goals = {e['target_id'] for e in packet['entries'] if e['target_type'] == 'goal' and e['decision'] != 'accept'}
    affected_groups = {e['target_id'] for e in packet['entries'] if e['target_type'] == 'group' and e['decision'] != 'accept'}
    affected_groups.update(g['group_id'] for g in model['refinement_groups'] if affected_goals.intersection([g['parent_id']] + g['child_ids']))
    return dict(schema_version='goalforge-kaos-revision-request-1', model=binding(model), feedback_sha256=object_hash(packet),
                affected_goal_ids=sorted(affected_goals), affected_group_ids=sorted(affected_groups),
                opinions=packet['entries'], note=packet['note'], status='awaiting_reassessment' if affected_goals or affected_groups or packet['note'].strip() else 'opinions_recorded',
                next_step='依据原文处理意见；新目标重新绑定判断，精化组重新评估；assemble --previous --feedback 生成待审副本。',
                human_acceptance='not_inferred')


def fresh(directory):
    directory = Path(directory)
    require(not directory.exists() or not any(directory.iterdir()), 'Use a fresh output directory; preserve comments and old versions')
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def markdown(model):
    goals = {g['goal_id']: g for g in model['goals']}
    groups = {}
    for g in model['refinement_groups']:
        if active(g):
            groups.setdefault(g['parent_id'], []).append(g)
    children = {c for items in groups.values() for g in items for c in g['child_ids']}
    lines = ['# 目标模型', '', f'版本：{model["version"]}。人工待审。', '']
    seen = set()
    def node(gid, indent=0):
        text = goals[gid]['statement'].replace('\n', ' ')
        lines.append('  ' * indent + '- ' + text + ('（同一目标的再次引用）' if gid in seen else ''))
        if gid in seen:
            return
        seen.add(gid)
        g = goals[gid]
        if g['conditions']:
            lines.append('  ' * (indent + 1) + '适用条件：' + '；'.join(g['conditions']))
        for index, group in enumerate(groups.get(gid, []), 1):
            title = f'方案 {index}（任选一个完整方案；方案内全部满足）' if len(groups[gid]) > 1 else '以下各项都需满足'
            lines.append('  ' * (indent + 1) + title)
            for child in group['child_ids']:
                node(child, indent + 2)
    for gid in goals:
        if gid not in children:
            node(gid)
    if not goals:
        lines.append('本次可读材料中未提取到目标。')
    if model['issues'] or model['limitations']:
        lines += ['', '## 需要确认', ''] + ['- ' + i['message'] for i in model['issues']] + ['- ' + s for s in model['limitations']]
    lines += ['', '原文与层级依据可在 HTML 中展开。结构检查不等于语义证明，意见导出后交回助手。', '']
    return '\n'.join(lines)


def diagram_rows(text, width=26):
    rows, row, units = [], '', 0
    for char in text:
        size = 2 if unicodedata.east_asian_width(char) in 'WF' else 1
        if char == '\n' or units + size > width:
            rows.append(row); row, units = '', 0
            if char == '\n':
                continue
        row += char; units += size
    if row:
        rows.append(row)
    return rows or ['']


def dag_layout(model):
    """One node per goal plus explicit sufficient-set junctions, top to bottom."""
    check_structure(model)
    nodes, edges, alternatives = {}, [], {}
    for goal in model['goals']:
        rows = diagram_rows(goal['statement'])
        visible = rows[:4]
        if len(rows) > 4:
            visible[-1] = visible[-1][:-1] + '…'
        nodes['goal:'+goal['goal_id']] = dict(kind='goal', id=goal['goal_id'], label=goal['statement'],
                                            lines=visible, width=234, height=max(76, 30+len(visible)*20))
    for group in model['refinement_groups']:
        if active(group):
            alternatives.setdefault(group['parent_id'], []).append(group)
    for parent, choices in alternatives.items():
        for index, group in enumerate(choices, 1):
            label = ('方案 '+str(index)+' · ' if len(choices)>1 else '') + ('共同满足' if len(group['child_ids'])>1 else '具体目标')
            node = 'group:'+group['group_id']
            nodes[node] = dict(kind='group',id=group['group_id'],label=label,lines=[label],width=174,height=42)
            edges.append(dict(start='goal:'+parent,end=node,group_id=group['group_id']))
            edges.extend(dict(start=node,end='goal:'+c,group_id=group['group_id']) for c in group['child_ids'])
    incoming = {key: [] for key in nodes}
    outgoing = {key: [] for key in nodes}
    for edge in edges:
        incoming[edge['end']].append(edge['start']);outgoing[edge['start']].append(edge['end'])
    degree={key:len(value) for key,value in incoming.items()}
    ready=[key for key in nodes if not degree[key]];ranks={key:0 for key in nodes};visited=[]
    while ready:
        key=ready.pop(0);visited.append(key)
        for child in outgoing[key]:
            ranks[child]=max(ranks[child],ranks[key]+1);degree[child]-=1
            if not degree[child]:ready.append(child)
    require(len(visited)==len(nodes),'Refinement cycle in diagram')
    layers={}
    for key in visited:layers.setdefault(ranks[key],[]).append(key)
    order={}
    for rank,layer in sorted(layers.items()):
        layer.sort(key=lambda key:sum(order[p] for p in incoming[key])/len(incoming[key]) if incoming[key] else list(nodes).index(key))
        order.update({key:i for i,key in enumerate(layer)})
    width=max([580]+[len(layer)*274+36 for layer in layers.values()]);y=38
    for rank,layer in sorted(layers.items()):
        layer_width=sum(nodes[key]['width'] for key in layer)+40*(len(layer)-1)
        x=(width-layer_width)/2
        for key in layer:
            nodes[key].update(x=x,y=y,rank=rank);x+=nodes[key]['width']+40
        y+=max(nodes[key]['height'] for key in layer)+62
    return dict(nodes=nodes,edges=edges,width=width,height=max(190,y+8))


def svg(model):
    layout=dag_layout(model);esc=lambda text:html.escape(str(text),quote=True)
    width,height=layout['width'],layout['height']
    result=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="group" aria-label="目标有向无环图：从上到下展开目标，不表示操作先后">',
            '<defs><marker id="dagArrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#799b8c"/></marker></defs>',
            '<style>text{font-family:system-ui,"Microsoft YaHei",sans-serif}.goal-node rect{fill:#fff;stroke:#719c8c;stroke-width:1.5}.group-node rect{fill:#edf5f0;stroke:#8aaf9e;stroke-width:1.2}.dag-node{cursor:pointer;outline:none}.dag-node:focus rect,.dag-node.selected rect{stroke:#176d58;stroke-width:3}.dag-edge{fill:none;stroke:#799b8c;stroke-width:1.6}.dag-node:hover rect{fill:#e9f4ed}</style>',
            '<rect width="100%" height="100%" fill="#f8fbf8"/>']
    if not layout['nodes']:
        result.append('<text x="30" y="75" font-size="18" fill="#62766d">本次资料没有可展示的目标</text>')
    for edge in layout['edges']:
        a,b=(layout['nodes'][edge[k]] for k in ('start','end'))
        x1,y1=a['x']+a['width']/2,a['y']+a['height'];x2,y2=b['x']+b['width']/2,b['y'];middle=(y1+y2)/2
        result.append(f'<path class="dag-edge" data-group-edge="{esc(edge["group_id"])}" d="M{x1} {y1} C{x1} {middle} {x2} {middle} {x2} {y2}" marker-end="url(#dagArrow)"/>')
    for node in layout['nodes'].values():
        kind,identifier=node['kind'],node['id'];x,y,w,h=(node[k] for k in ('x','y','width','height'))
        description=node['label'] if kind=='goal' else '审核这组层级：'+node['label']
        result.append(f'<g class="dag-node {kind}-node" data-{kind}="{esc(identifier)}" tabindex="0" role="button" aria-label="{esc(description)}"><title>{esc(description)}</title><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{12 if kind=="goal" else 21}"/>')
        top=y+(h-len(node['lines'])*20)/2+15
        for i,line in enumerate(node['lines']):
            result.append(f'<text x="{x+w/2}" y="{top+i*20}" text-anchor="middle" font-size="{15 if kind=="goal" else 13}" fill="#203d38">{esc(line)}</text>')
        result.append('</g>')
    return '\n'.join(result+['</svg>'])


def package(model, base, output, report=None, with_svg=False):
    actual = inspect(model, base)
    if report is not None:
        require(report == actual, 'Stale or forged inspection report')
    files = read_artifacts(model, base)
    assets = Path(__file__).resolve().parents[1] / 'assets'
    data = dict(model=model, binding=binding(model), report=actual, markdown=markdown(model), svg=svg(model))
    payload = json.dumps(data, ensure_ascii=False, allow_nan=False).replace('<', '\\u003c').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
    page = (assets / 'simple-viewer.html').read_text(encoding='utf-8')
    page = page.replace('__CSS__', (assets / 'simple-viewer.css').read_text(encoding='utf-8'))
    page = page.replace('__PAYLOAD__', payload)
    page = page.replace('__CORE__', (assets / 'simple-core.js').read_text(encoding='utf-8'))
    page = page.replace('__UI__', (assets / 'simple-viewer.js').read_text(encoding='utf-8'))
    files.update({'goal-model.json': encode(model), 'goal-model.md': data['markdown'].encode('utf-8'),
                  'goal-model.html': page.encode('utf-8'), 'attachments/inspection.json': encode(actual)})
    if with_svg:
        files['goal-model.svg'] = data['svg'].encode('utf-8')
    manifest = dict(schema_version='goalforge-kaos-delivery-1', model=binding(model), readiness=actual['readiness'], human='pending',
                    files=[dict(path=name, sha256=digest(raw)) for name, raw in files.items()])
    files['manifest.json'] = encode(manifest)
    out = fresh(output)
    for name, raw in files.items():
        target = out / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='mode', required=True)
    p = sub.add_parser('template')
    p.add_argument('extraction', type=Path); p.add_argument('judgments', type=Path); p.add_argument('output', type=Path)
    p = sub.add_parser('assemble')
    for name in ('extraction', 'judgments', 'source', 'decisions', 'output'):
        p.add_argument(name, type=Path)
    p.add_argument('--previous', type=Path); p.add_argument('--feedback', type=Path)
    p = sub.add_parser('inspect')
    p.add_argument('model', type=Path); p.add_argument('output', type=Path)
    p = sub.add_parser('finalize')
    p.add_argument('model', type=Path); p.add_argument('report', type=Path); p.add_argument('output', type=Path)
    p.add_argument('--svg', action='store_true')
    p = sub.add_parser('feedback')
    p.add_argument('model', type=Path); p.add_argument('feedback', type=Path); p.add_argument('output', type=Path)
    args = parser.parse_args()
    if args.mode == 'template':
        result = decision_template(args.extraction.read_bytes(), args.judgments.read_bytes())
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('xb') as handle:
            handle.write(encode(result))
    elif args.mode == 'assemble':
        require(bool(args.previous) == bool(args.feedback), 'Use --previous and --feedback together')
        raws = [getattr(args, k).read_bytes() for k in ('extraction', 'judgments', 'source', 'decisions')]
        previous = load(args.previous) if args.previous else None
        packet = load(args.feedback) if args.feedback else None
        if previous is not None:
            inspect(previous, args.previous.parent)
        result = build(*raws, previous=previous, feedback=packet)
        files = dict(zip(['extraction.json', 'judgments.json', 'source.txt', 'kaos-decisions.json'], raws))
        if previous is not None:
            files.update({'previous-model.json': encode(previous), 'review-feedback.json': encode(packet)})
        result['input_artifacts'] = [dict(path='attachments/' + name, sha256=digest(raw)) for name, raw in files.items()]
        out = fresh(args.output)
        for name, raw in files.items():
            target = out / 'attachments' / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
        (out / 'model-input.json').write_bytes(encode(result))
    elif args.mode == 'inspect':
        report = inspect(load(args.model), args.model.parent)
        with args.output.open('xb') as handle:
            handle.write(encode(report))
    elif args.mode == 'finalize':
        result = package(load(args.model), args.model.parent, args.output, load(args.report), args.svg)
        print(json.dumps(dict(readiness=result['readiness'], human=result['human'])))
    else:
        model, packet = load(args.model), load(args.feedback)
        inspect(model, args.model.parent)
        result = process_feedback(model, packet)
        out = fresh(args.output)
        (out / 'revision-request.json').write_bytes(encode(result))
        (out / 'review-feedback.json').write_bytes(encode(packet))
        (out / '修改说明.md').write_text('已记录审核意见。原模型未变；需重新判断后生成待审新版本。\n' + '\n'.join('- ' + (e['comment'] or '该项可以') for e in packet['entries']), encoding='utf-8')


if __name__ == '__main__':
    main()
