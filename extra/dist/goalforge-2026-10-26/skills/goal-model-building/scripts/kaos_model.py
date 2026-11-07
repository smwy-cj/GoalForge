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
sys.path.insert(0, str(SKILLS / 'goal-extraction/scripts'))
from trace_candidates import trace, locate
from simple_candidates import validate as validate_extraction

SCHEMA = 'goalforge-kaos-1'
FEEDBACK = 'goalforge-simple-feedback-1'
SCHEMA2 = 'goalforge-kaos-2'
FEEDBACK2 = 'goalforge-simple-feedback-2'
RELATION_TYPES = {'specialization': '范围具体化', 'operationalization': '实现方式',
                  'contribution': '有助于', 'precedes': '过程先后'}
RELATION_STATUS = {'supported': '有依据的联系', 'proposed': '待确认联系', 'rejected': '已否定联系'}


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


def decision_template(extraction_raw, judgments_raw, version=1):
    data = json.loads(extraction_raw.decode('utf-8-sig'))
    validate_extraction(data)
    require(version in {1, 2}, 'Unsupported decision version')
    result = dict(schema_version='goalforge-kaos-decisions-' + str(version),
                input_binding=dict(extraction_sha256=digest(extraction_raw), judgments_sha256=digest(judgments_raw)),
                groups=[], questions=[])
    if version == 2:
        result.update(relations=[], reassessments=[])
    return result


def build(extraction_raw, judgments_raw, source_raw, decision_raw, previous=None, feedback=None, migration=None):
    data = json.loads(extraction_raw.decode('utf-8-sig'))
    validate_extraction(data)
    source = source_raw.decode('utf-8')
    require(digest(source_raw) == data['document_hash'], 'Source hash mismatch')
    judgments = json.loads(judgments_raw.decode('utf-8-sig'))
    traced = trace(data, judgments, source, digest(extraction_raw))
    decisions = json.loads(decision_raw.decode('utf-8-sig'))
    require(decisions.get('schema_version') in {'goalforge-kaos-decisions-1', 'goalforge-kaos-decisions-2'}, 'Unsupported KAOS judgment schema')
    v2 = decisions['schema_version'] == 'goalforge-kaos-decisions-2'
    require(v2 or not any(k in decisions for k in ('relations', 'reassessments', 'migration_parent')), 'v1 cannot consume v2 judgments')
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
    model = dict(schema_version=SCHEMA2 if v2 else SCHEMA, model_id=data['document_id'] + '-goal-model', version='v1', parent=None,
                 scope=dict(document_id=data['document_id'], coverage=data['coverage']),
                 goals=goals, refinement_groups=copy.deepcopy(decisions['groups']), evidence_index=list(evidence.values()),
                 issues=issues, limitations=list(dict.fromkeys(data['limitations'] + data['coverage']['omissions'] + data['conversion']['issues'])),
                 input_artifacts=[], review=dict(status='pending'), changes=[])
    if v2:
        model['relations'] = copy.deepcopy(decisions['relations'])
        model['source_binding'] = dict(sha256=digest(source_raw))
    # The explanation of a relationship may occur outside the goal quotations.
    # Locate those actual passages too, instead of showing an unrelated goal quote.
    segments = {s['source_id']: s for s in data['segments']}
    counter = 0
    for group in model['refinement_groups'] + model.get('relations', []):
        for quote in group.pop('evidence_quotes', []):
            require(isinstance(quote, dict), 'Invalid refinement quotation')
            counter += 1
            found = locate(quote, segments.get(quote.get('source_id')), source, data['document_hash'], counter)
            require(found['location_status'] == 'exact' and found['verification_scope'] == 'full_text', 'Refinement quotation must match actual source')
            found['evidence_id'] = 'K' + str(counter).zfill(4)
            model['evidence_index'].append(found)
            group['evidence_ids'] = [found['evidence_id']] + group.get('evidence_ids', [])
    for q in decisions.get('questions', []):
        require(isinstance(q, dict) and q.get('target_type') in ({'goal', 'group', 'relation', 'model'} if v2 else {'goal', 'group', 'model'}) and isinstance(q.get('message'), str) and q['message'].strip(), 'Invalid modeling question')
        model['issues'].append(dict(target_type=q['target_type'], target_id=q['target_id'], message=q['message'], blocking=False))
    if data['status'] != 'completed':
        model['limitations'].append('资料处理不完整，请核对范围与缺失部分。')
    for g in model['refinement_groups']:
        if g.get('status') != 'supported' or g.get('completeness') != 'complete':
            model['issues'].append(dict(target_type='group', target_id=g.get('group_id'), message='这组层级仍需确认，尚未作为成立的精化展示。', blocking=False))
    for relation in model.get('relations', []):
        if relation.get('status') == 'proposed':
            model['issues'].append(dict(target_type='relation', target_id=relation.get('relation_id'), message='这项联系尚待确认，不表示充分精化。', blocking=False))
    require(not (migration is not None and previous is not None), 'Migration and feedback revision are separate operations')
    if migration is not None:
        check_structure(migration)
        require(v2 and migration['schema_version'] == SCHEMA, 'Explicit migration is v1 to v2 only')
        require(decisions.get('migration_parent') == binding(migration), 'Migration parent binding mismatch')
        require(model['model_id'] == migration['model_id'] and model['goals'] == migration['goals'], 'Migration must keep the verified goal set; revise goals separately')
        model['parent'] = binding(migration)
        model['version'] = migration['version'] + '.kaos2'
        model['changes'] = [dict(kind='explicit_v1_migration', before_goals=migration['goals'],
                                before_groups=migration['refinement_groups'], before_relations=[],
                                note='旧关系不推定新类型；当前精化及联系按新版判断重新核验。')]
        omitted = sorted(target_ids(migration, 'group') - target_ids(model, 'group'))
        model['changes'][0]['removed_group_ids'] = omitted
        if omitted:
            model['issues'].append(dict(target_type='model', target_id=model['model_id'],
                message='升级后尚未重新编制的旧精化组：' + '、'.join(omitted) + '；旧判断保留在迁移快照中，请核对。', blocking=False))
    else:
        require('migration_parent' not in decisions, 'Migration judgments require --migrate-from')
    if previous is not None:
        require(feedback is not None, 'Revision requires actual feedback bound to the previous model')
        validate_feedback(feedback, previous, submitted=True)
        require(previous['schema_version'] == model['schema_version'], 'No automatic schema conversion; use explicit migration')
        require(model['model_id'] == previous['model_id'], 'Revision must retain the model identity')
        model['parent'] = binding(previous)
        model['version'] = previous['version'] + '.r1'
        model['changes'] = [dict(kind='rebuild_after_feedback', feedback_sha256=object_hash(feedback),
                                 before_goals=previous['goals'], before_groups=previous['refinement_groups'],
                                 removed_goal_ids=sorted(set(g['goal_id'] for g in previous['goals']) - set(g['goal_id'] for g in goals)))]
        if v2:
            affected = revision_dependencies(previous, model, feedback)
            reassessed = ids(decisions.get('reassessments', []), 'assessment_id')
            accounted_assessments = set()
            for item in reassessed.values():
                key = (item.get('target_type'), item.get('target_id'))
                require(key in affected and key not in accounted_assessments and isinstance(item.get('reason'), str) and item['reason'].strip(), 'Invalid or duplicate reassessment')
                accounted_assessments.add(key)
            require(affected <= accounted_assessments, 'Changed goals/relations or feedback require explicit group/relation reassessments: ' + str(sorted(affected - accounted_assessments)))
            model['changes'][0].update(before_relations=previous['relations'], reassessments=list(reassessed.values()),
                removed_relation_ids=sorted({r['relation_id'] for r in previous['relations']} - {r['relation_id'] for r in model['relations']}),
                removed_group_ids=sorted({g['group_id'] for g in previous['refinement_groups']} - {g['group_id'] for g in model['refinement_groups']}))
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
                available = target_ids(model, kind)
                if identifier not in available:
                    kind, identifier = 'model', model['model_id']
                model['issues'].append(dict(target_type=kind, target_id=identifier,
                                            message='前轮意见尚待处理：' + opinion['comment'], blocking=False))
        if feedback['note'].strip():
            model['issues'].append(dict(target_type='model', target_id=model['model_id'], message='前轮整体补充（请核对）：' + feedback['note'], blocking=False))
    check_structure(model)
    return model


def target_ids(model, kind):
    return ({g['goal_id'] for g in model['goals']} if kind == 'goal' else
            {g['group_id'] for g in model['refinement_groups']} if kind == 'group' else
            {r['relation_id'] for r in model.get('relations', [])} if kind == 'relation' else
            {model['model_id']} if kind == 'model' else set())


def revision_dependencies(previous, model, feedback):
    def states(m):
        evidence = {e['evidence_id']: e for e in m['evidence_index']}
        return {g['goal_id']: dict(goal=g, evidence=[evidence[e] for e in g['evidence_ids']]) for g in m['goals']}
    old, new = states(previous), states(model)
    changed = {gid for gid in old if old[gid] != new.get(gid)}
    if previous['source_binding'] != model['source_binding']:
        changed.update(old)
    changed.update(e['target_id'] for e in feedback['entries'] if e['target_type'] == 'goal' and e['decision'] != 'accept')
    old_relations = {r['relation_id']: r for r in previous['relations']}
    new_relations = {r['relation_id']: r for r in model['relations']}
    def relation_state(m, r):
        evidence = {e['evidence_id']: e for e in m['evidence_index']}
        return dict(relation=r, evidence=[evidence[e] for e in r['evidence_ids']])
    relation_ids = {rid for rid, r in old_relations.items() if rid not in new_relations or
                    relation_state(previous, r) != relation_state(model, new_relations[rid]) or
                    changed.intersection([r['source_id'], r['target_id']])}
    relation_ids.update(r['relation_id'] for r in model['relations'] if changed.intersection([r['source_id'], r['target_id']]))
    relation_ids.update(e['target_id'] for e in feedback['entries'] if e['target_type'] == 'relation' and e['decision'] != 'accept')
    group_ids = {g['group_id'] for g in previous['refinement_groups'] + model['refinement_groups']
                 if changed.intersection([g['parent_id']] + g['child_ids']) or relation_ids.intersection(g.get('relation_ids', []))}
    group_ids.update(e['target_id'] for e in feedback['entries'] if e['target_type'] == 'group' and e['decision'] != 'accept')
    return ({('relation', rid) for rid in relation_ids if rid in new_relations} |
            {('group', gid) for gid in group_ids if gid in target_ids(model, 'group')})


def check_structure(model):
    require(model.get('schema_version') in {SCHEMA, SCHEMA2}, 'Use the correct versioned model tool')
    v2 = model['schema_version'] == SCHEMA2
    if v2:
        require(isinstance(model.get('source_binding'), dict) and isinstance(model['source_binding'].get('sha256'), str)
                and re.fullmatch(r'[a-f0-9]{64}', model['source_binding']['sha256']), 'v2 source binding required')
    require(v2 or 'relations' not in model, 'v1 cannot silently carry v2 relations')
    require(model.get('review') == {'status': 'pending'}, 'This builder cannot manufacture human acceptance')
    goals = ids(model['goals'], 'goal_id')
    groups = ids(model['refinement_groups'], 'group_id')
    evidence = ids(model['evidence_index'], 'evidence_id')
    relations = ids(model['relations'], 'relation_id') if v2 else {}
    require(not set(goals).intersection(groups), 'Goal and group IDs must be distinct')
    require(not (set(relations) & (set(goals) | set(groups))), 'Relation IDs must be distinct from goals/groups')
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
    if v2:
        validate_relations(relations, goals, evidence)
        for group in groups.values():
            refs = group.get('relation_ids', [])
            require(string_list(refs) and len(refs) == len(set(refs)) and set(refs) <= set(relations), 'Invalid group relation dependencies')
            members = {group['parent_id'], *group['child_ids']}
            require(all({relations[r]['source_id'], relations[r]['target_id']} <= members for r in refs), 'Group relation dependency endpoints outside group')
            checks = group.get('checks', [])
            require(isinstance(checks, list), 'Invalid scenario checks')
            for item in checks:
                require(item.get('kind') in {'normal', 'exception'} and item.get('origin') in {'source', 'analysis_assumption'}
                        and item.get('outcome') in {'supports', 'counterexample', 'unknown'}
                        and all(isinstance(item.get(k), str) and item[k].strip() for k in ('scenario', 'rationale')), 'Invalid scenario check')
                if item['origin'] == 'source':
                    require(item.get('evidence_ids') and set(item['evidence_ids']) <= set(evidence), 'Source scenario requires evidence')
            if active(group):
                require(all(relations[r]['status'] == 'supported' for r in refs), 'Unconfirmed relation cannot support an established refinement')
                require({c['kind'] for c in checks} == {'normal', 'exception'} and all(c['outcome'] == 'supports' for c in checks), 'Established refinement requires normal/exception checks without unresolved counterexamples')
    for issue in model['issues']:
        require(issue.get('target_type') in ({'goal', 'group', 'relation', 'model'} if v2 else {'goal', 'group', 'model'}), 'Invalid issue kind')
        allowed = target_ids(model, issue['target_type'])
        require(issue.get('target_id') in allowed and isinstance(issue.get('message'), str) and issue['message'].strip(), 'Unknown issue target')
    return goals, groups, evidence


def validate_relations(relations, goals, evidence):
    seen = set()
    graphs = {kind: {gid: [] for gid in goals} for kind in ('specialization', 'operationalization', 'precedes')}
    for r in relations.values():
        a, b, kind = r.get('source_id'), r.get('target_id'), r.get('type')
        require(a in goals and b in goals and a != b, 'Invalid relation endpoints')
        require(kind in RELATION_TYPES and r.get('status') in RELATION_STATUS, 'Invalid relation type/status')
        require(string_list(r.get('conditions')) and string_list(r.get('assumptions')), 'Relation conditions/assumptions required')
        require(isinstance(r.get('rationale'), str) and r['rationale'].strip(), 'Relation rationale required')
        refs = r.get('evidence_ids')
        require(string_list(refs) and refs and len(refs) == len(set(refs)) and set(refs) <= set(evidence), 'Relation evidence required')
        require(any(evidence[e]['location_status'] == 'exact' and evidence[e]['evidence_role'] == 'supporting' for e in refs), 'Relation requires located basis evidence')
        key = (kind, a, b, tuple(sorted(r['conditions'])))
        require(key not in seen, 'Duplicate typed relation')
        seen.add(key)
        if r['status'] == 'supported':
            require(all(goals[gid]['support']['label'] in {'direct', 'inferred'} for gid in (a, b)), 'Supported relation has unsupported goals')
        if kind in graphs and r['status'] != 'rejected':
            graphs[kind][a].append(b)
    for kind, graph in graphs.items():
        state = {}
        def visit(gid):
            require(state.get(gid) != 1, 'Typed relation cycle: ' + kind)
            if state.get(gid) == 2:
                return
            state[gid] = 1
            for child in graph[gid]:
                visit(child)
            state[gid] = 2
        for gid in graph:
            visit(gid)


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
    migrated = bool(model['parent'] and model['changes'] and model['changes'][0]['kind'] == 'explicit_v1_migration')
    previous = json.loads(files['attachments/previous-model.json']) if model['parent'] and not migrated else None
    migration = json.loads(files['attachments/migration-model.json']) if migrated else None
    feedback = json.loads(files['attachments/review-feedback.json']) if previous is not None else None
    if previous is not None:
        require(binding(previous) == model['parent'], 'Previous model binding mismatch')
    if migration is not None:
        require(binding(migration) == model['parent'], 'Migration model binding mismatch')
    rebuilt = build(*(files['attachments/' + k] for k in required), previous=previous, feedback=feedback, migration=migration)
    keys = ['schema_version', 'model_id', 'version', 'parent', 'scope', 'goals', 'refinement_groups', 'evidence_index', 'issues', 'limitations', 'review', 'changes']
    if model['schema_version'] == SCHEMA2:
        keys.extend(['relations', 'source_binding'])
    for key in keys:
        require(model[key] == rebuilt[key], 'Model differs from actual source/judgments: ' + key)
    canonical = files['attachments/source.txt'].decode('utf-8')
    for e in model['evidence_index']:
        require(e['location_status'] == 'exact' and e['verification_scope'] == 'full_text' and e['source_version_status'] == 'verified', 'Unverified evidence location')
        require(type(e['start_char']) is int and type(e['end_char']) is int and 0 <= e['start_char'] < e['end_char'] <= len(canonical) and canonical[e['start_char']:e['end_char']] == e['quote'], 'Evidence quote mismatch')
    return dict(schema_version='goalforge-kaos-check-2' if model['schema_version'] == SCHEMA2 else 'goalforge-kaos-check-1', model=binding(model), structure='passed',
                independent_semantic='not_run', formal_proof='not_run', human='pending',
                readiness='blocked' if any(i['blocking'] for i in model['issues']) else 'reviewable',
                note='已核验结构、实际原文与版本绑定；精化充分性来自编制判断，未进行形式化证明。')


def validate_feedback(packet, model, submitted=False):
    expected = FEEDBACK2 if model['schema_version'] == SCHEMA2 else FEEDBACK
    require(packet.get('schema_version') == expected and packet.get('model') == binding(model), 'Feedback model/version/hash mismatch')
    require(packet.get('status') in {'draft', 'submitted'} and (not submitted or packet['status'] == 'submitted'), 'Submitted feedback required')
    goals, groups, _ = check_structure(model)
    require(isinstance(packet.get('entries'), list) and isinstance(packet.get('form_drafts'), dict) and isinstance(packet.get('note'), str), 'Invalid feedback content')
    seen = set()
    for entry in packet['entries']:
        kind, target = entry.get('target_type'), entry.get('target_id')
        allowed = target_ids(model, kind)
        require(target in allowed and (kind, target) not in seen, 'Unknown/duplicate feedback target')
        seen.add((kind, target))
        require(entry.get('decision') in {'accept', 'modify', 'defer'} and isinstance(entry.get('comment'), str), 'Invalid decision')
        require(entry['decision'] == 'accept' or entry['comment'].strip(), 'Please explain the requested change/uncertainty')
    for key, draft in packet['form_drafts'].items():
        require(isinstance(draft, dict) and draft.get('target_type') in {'goal', 'group', 'relation', 'model'}, 'Invalid draft')
        allowed = target_ids(model, draft['target_type'])
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
    affected_relations = {e['target_id'] for e in packet['entries'] if e['target_type'] == 'relation' and e['decision'] != 'accept'}
    affected_relations.update(r['relation_id'] for r in model.get('relations', []) if affected_goals.intersection([r['source_id'], r['target_id']]))
    affected_groups.update(g['group_id'] for g in model['refinement_groups'] if affected_relations.intersection(g.get('relation_ids', [])))
    result = dict(schema_version='goalforge-kaos-revision-request-2' if model['schema_version'] == SCHEMA2 else 'goalforge-kaos-revision-request-1', model=binding(model), feedback_sha256=object_hash(packet),
                affected_goal_ids=sorted(affected_goals), affected_group_ids=sorted(affected_groups),
                opinions=packet['entries'], note=packet['note'], status='awaiting_reassessment' if affected_goals or affected_groups or affected_relations or packet['note'].strip() else 'opinions_recorded',
                next_step='依据原文处理意见；新目标重新绑定判断，精化组重新评估；assemble --previous --feedback 生成待审副本。',
                human_acceptance='not_inferred')
    if model['schema_version'] == SCHEMA2:
        result['affected_relation_ids'] = sorted(affected_relations)
    return result


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
    if model.get('relations'):
        lines += ['', '## 目标之间的联系', '', '下列联系不表示充分精化；待确认及已否定记录保留各自状态。', '']
        for r in model['relations']:
            lines += ['- ' + RELATION_STATUS[r['status']] + '：' + goals[r['source_id']]['statement'] +
                      ' —[' + RELATION_TYPES[r['type']] + ']→ ' + goals[r['target_id']]['statement'],
                      '  依据：' + r['rationale']]
            if r['conditions'] or r['assumptions']:
                lines.append('  条件／假设：' + '；'.join(r['conditions'] + r['assumptions']))
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


def relations_svg(model):
    """A separate labelled relation list; never overload established DAG arrows."""
    check_structure(model)
    goals = {g['goal_id']: g for g in model['goals']}
    rows, y = [], 90
    for r in model.get('relations', []):
        label = RELATION_STATUS[r['status']] + ' · ' + RELATION_TYPES[r['type']]
        lines = diagram_rows(goals[r['source_id']]['statement'] + ' → ' + goals[r['target_id']]['statement'], 90)
        height = 52 + 22 * len(lines)
        color = {'supported': '#296a75', 'proposed': '#8b6725', 'rejected': '#777777'}[r['status']]
        esc = lambda s: html.escape(str(s), quote=True)
        rows.append(f'<g data-relation="{esc(r["relation_id"])}" role="button" tabindex="0" aria-label="{esc(label)}"><rect x="20" y="{y}" width="780" height="{height}" rx="8" fill="#fafafa" stroke="{color}" stroke-dasharray="5 4"/><text x="36" y="{y+25}" fill="{color}">{esc(label)}</text>')
        for i, line in enumerate(lines):
            rows.append(f'<text x="36" y="{y+51+i*22}">{esc(line)}</text>')
        rows.append('</g>')
        y += height + 14
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="820" height="' + str(max(160, y)) +
            '" viewBox="0 0 820 ' + str(max(160, y)) + '" role="group" aria-label="目标联系，不表示充分精化">' +
            '<style>text{font:15px system-ui,sans-serif}</style><rect width="100%" height="100%" fill="white"/>' +
            '<text x="20" y="32">目标之间的联系</text><text x="20" y="60">独立于成立精化；箭头按联系类型解释，状态逐项标明。</text>' + ''.join(rows) + '</svg>')


def package(model, base, output, report=None, with_svg=False):
    actual = inspect(model, base)
    if report is not None:
        require(report == actual, 'Stale or forged inspection report')
    files = read_artifacts(model, base)
    assets = Path(__file__).resolve().parents[1] / 'assets'
    data = dict(model=model, binding=binding(model), report=actual, markdown=markdown(model), svg=svg(model))
    if model['schema_version'] == SCHEMA2:
        data['relations_svg'] = relations_svg(model)
    payload = json.dumps(data, ensure_ascii=False, allow_nan=False).replace('<', '\\u003c').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
    page = (assets / 'simple-viewer.html').read_text(encoding='utf-8')
    replacements = {'__CSS__': (assets / 'simple-viewer.css').read_text(encoding='utf-8'),
                    '__PAYLOAD__': payload,
                    '__CORE__': (assets / 'simple-core.js').read_text(encoding='utf-8'),
                    '__UI__': (assets / 'simple-viewer.js').read_text(encoding='utf-8')}
    require(all(page.count(token) == 1 for token in replacements), 'Unexpected viewer template placeholders')
    # Replace only tokens present in the original template. Inserted source text
    # and assets may legitimately contain the same literal strings.
    page = re.sub(r'__(?:CSS|PAYLOAD|CORE|UI)__', lambda match: replacements[match.group(0)], page)
    files.update({'goal-model.json': encode(model), 'goal-model.md': data['markdown'].encode('utf-8'),
                  'goal-model.html': page.encode('utf-8'), 'attachments/inspection.json': encode(actual)})
    if with_svg:
        files['goal-model.svg'] = data['svg'].encode('utf-8')
        if model['schema_version'] == SCHEMA2:
            files['goal-relations.svg'] = data['relations_svg'].encode('utf-8')
    manifest = dict(schema_version='goalforge-kaos-delivery-2' if model['schema_version'] == SCHEMA2 else 'goalforge-kaos-delivery-1', model=binding(model), readiness=actual['readiness'], human='pending',
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
    p.add_argument('--schema-version', type=int, choices=(1, 2), default=2)
    p = sub.add_parser('upgrade-template')
    p.add_argument('model', type=Path); p.add_argument('output', type=Path)
    p = sub.add_parser('assemble')
    for name in ('extraction', 'judgments', 'source', 'decisions', 'output'):
        p.add_argument(name, type=Path)
    p.add_argument('--previous', type=Path); p.add_argument('--feedback', type=Path)
    p.add_argument('--migrate-from', type=Path)
    p = sub.add_parser('inspect')
    p.add_argument('model', type=Path); p.add_argument('output', type=Path)
    p = sub.add_parser('finalize')
    p.add_argument('model', type=Path); p.add_argument('report', type=Path); p.add_argument('output', type=Path)
    p.add_argument('--svg', action='store_true')
    p = sub.add_parser('feedback')
    p.add_argument('model', type=Path); p.add_argument('feedback', type=Path); p.add_argument('output', type=Path)
    args = parser.parse_args()
    if args.mode == 'template':
        result = decision_template(args.extraction.read_bytes(), args.judgments.read_bytes(), args.schema_version)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('xb') as handle:
            handle.write(encode(result))
    elif args.mode == 'upgrade-template':
        model = load(args.model)
        inspect(model, args.model.parent)
        require(model['schema_version'] == SCHEMA, 'upgrade-template accepts v1 only')
        files = read_artifacts(model, args.model.parent)
        result = decision_template(files['attachments/extraction.json'], files['attachments/judgments.json'], 2)
        result['migration_parent'] = binding(model)
        # Empty groups and relations require authoring, not automatic promotion.
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('xb') as handle:
            handle.write(encode(result))
    elif args.mode == 'assemble':
        require(bool(args.previous) == bool(args.feedback), 'Use --previous and --feedback together')
        require(not (args.migrate_from and args.previous), 'Do not mix migration and feedback revision')
        raws = [getattr(args, k).read_bytes() for k in ('extraction', 'judgments', 'source', 'decisions')]
        previous = load(args.previous) if args.previous else None
        packet = load(args.feedback) if args.feedback else None
        if previous is not None:
            inspect(previous, args.previous.parent)
        migration = load(args.migrate_from) if args.migrate_from else None
        if migration is not None:
            inspect(migration, args.migrate_from.parent)
        result = build(*raws, previous=previous, feedback=packet, migration=migration)
        files = dict(zip(['extraction.json', 'judgments.json', 'source.txt', 'kaos-decisions.json'], raws))
        if previous is not None:
            files.update({'previous-model.json': encode(previous), 'review-feedback.json': encode(packet)})
        if migration is not None:
            files['migration-model.json'] = encode(migration)
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
