# -*- coding: utf-8 -*-
"""Apply the explicitly requested wording correction; preserve all v1 files."""
from pathlib import Path
import json

here = Path(__file__).resolve().parent
data = json.loads((here/'authored-data.json').read_text(encoding='utf-8'))
doc = data['DOC010']
g = next(g for g in doc['goals'] if g['id']=='G08')
assert g['statement']=='下雨时更频繁地收到雨势变化、开始或停止的更新通知。'
g['statement']='下雨时更频繁地收到雨情变化、开始或停止的更新通知。'
doc['review_notes'].append('R07（v2 局部复核 G08/F02）：助手语义评审指出“雨势”可能被理解为雨强。回查 T049、T063 及 T039—T071 后改为一般“雨情”。开始或停止指是否降雨的状态变化，不要求雨强测量；T049 口语残句不作技术词解释。F02 的延迟数据反例仍成立，继续 proposed/partial。其他12项目标及 F01/F03 在源文、目标、条件、引文及原判断理由逐项一致性核对后沿用，未受到这一措辞收窄影响。')
with (here/'authored-data-DOC010-v2.json').open('x',encoding='utf-8') as f:
    json.dump({'DOC010':doc},f,ensure_ascii=False,indent=2)
    f.write('\n')
code=(here/'build.py').read_text(encoding='utf-8')
code=code.replace("with_name('authored-data.json')", "with_name('authored-data-DOC010-v2.json')")
code=code.replace("dest = OUT/doc/'v1'", "dest = OUT/doc/'v2'")
code=code.replace("version='v1'", "version='v2'")
marker="    artifact_list=[dict(path=str(p.relative_to(dest)),sha256=sha(p)) for p in sorted(dest.rglob('*')) if p.is_file()]"
addition='''    previous=OUT/doc/'v1'
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
    text(dest/'revision-notes.md',"# DOC010 v1 → v2 局部作者修订\\n\\n仅 G08 将‘雨势变化’改为‘雨情变化’；ID不变。原文 T049/T063 及 T039—T071 已回查。开始或停止指是否降雨的变化，不是雨强测量。F02重新整组审查，延迟数据的分析假设反例仍存在，继续 proposed/partial。其余目标、条件、证据和全部组内容经核对不变。\\n\\n全13目标重新生成语义模板和判断绑定，实际执行 trace、KAOS template、assemble、inspect、finalize；并非只补写哈希。完整回执在 run-record.json 和 command-*.json。\\n\\n这是助手语义评审驱动的措辞修订，不是用户反馈；未调用 feedback，未伪造人工采纳。冻结工具仅支持用真实人工反馈递增内部模型版本，所以本目录的作者产物版本为 v2，内部模型保持工具实际生成的 version=v1、parent=null。前后版本与全量ID映射绑定见 revision-record.json；v1完整保留。\\n")
'''
assert marker in code
code=code.replace(marker,addition+'\n'+marker)
with (here/'build-doc010-v2.py').open('x',encoding='utf-8') as f:
    f.write(code)
