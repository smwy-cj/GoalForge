import hashlib
import json
from pathlib import Path

b=Path(__file__).resolve().parents[1]
old=b/'revised/DOC015/v2/delivery/goal-model.json'
new=b/'revised/DOC015/v3/delivery/goal-model.json'
a=json.loads(old.read_text(encoding='utf-8'))
z=json.loads(new.read_text(encoding='utf-8'))


def normalized(model):
    ev={e['evidence_id']:e for e in model['evidence_index']}
    result={}
    for g in model['goals']:
        d={k:v for k,v in g.items() if k!='evidence_ids'}
        d['quoted_source']=[{k:v for k,v in ev[eid].items() if k!='evidence_id'} for eid in g['evidence_ids']]
        result[g['goal_id']]=d
    return result


x,y=normalized(a),normalized(z)
changed=[i for i in x if x[i]!=y[i]]
assert changed==['DOC015-G02','DOC015-G12'],changed
assert a['refinement_groups']==z['refinement_groups']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((b/'revised/_authoring/DOC015-v3-revision-record.json').read_text(encoding='utf-8'))
r.update(before_model_path=old.relative_to(b).as_posix(),before_model_sha256=sha(old),
         after_model_path=new.relative_to(b).as_posix(),after_model_sha256=sha(new),
         unchanged_semantic_goal_count=29,groups_exactly_equal=True,
         internal_model_version=z['version'],internal_parent=z['parent'],
         evidence_numbering='E IDs regenerated after added context quote; source/quote semantics compared independent of IDs')
(b/'revised/DOC015/v3/revision-record.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(b/'revised/DOC015/v3/revision-notes.md').write_text(
    '# DOC015 外层 v3 修订\n\nER-B3-001：G12收窄为质量评价中的听众反馈和评分。按内容分类辅助推荐的独立方式转入G02上下文，新增真实原文引文；没有新增/删除目标。其他29项目标语义、原文引文与2个候选组保持不变。\n\n'
    '本包实际重跑冻结脚本，structure passed、readiness reviewable；独立补查待完成。外层v3与工具内部version=v1、parent=null分别记录；未伪造人工反馈，人工仍pending。新增上下文证据引起E编号重新分配，不能仅凭编号比较语义。详见revision-record.json。\n',encoding='utf-8')
print('DOC015 revision ledger saved; only G02/G12 source semantics changed.')
