"""Source-reviewed local repair for ER-B3-001; preserve original author packages."""
import copy
import hashlib
import json
from pathlib import Path

OUT=Path(__file__).resolve().parents[1]


def load(p):
    return json.loads(p.read_bytes().decode('utf-8-sig'))


def main():
    original=OUT/'revised/DOC015/v2/authoring.json'
    authored=load(original)
    old=copy.deepcopy(authored)
    goals={g['candidate_id']:g for g in authored['goals']}
    source=load(OUT/'_inputs/DOC015/source-input.json')
    turn=next(s for s in source['segments'] if s['source_id']=='DOC015:T025')['text']
    quote='we also segregate this podcast based on most of its content. In terms of which category it belongs to which in turn helps the you know, giving the users what they actually need. In terms of suggestions.'
    assert turn.count(quote)==1
    g=goals['DOC015-G12']
    previous=g['statement']
    assert previous=='在内容分类与质量判断中考虑听众反馈和评分'
    g['statement']='在播客质量判断中考虑听众反馈和评分'
    g['context']=['在T024询问质量评估流程后，T025把用户反馈与评分列入该流程；具体审核权重未知。',
                  '内容分类按播客内容进行并用于辅助推荐，已作为G02的相关方式保留；没有证据说明反馈或评分用于决定内容类别。']
    g['support'].update(label='direct',rationale='T024的质量评估提问与T025的回答共同支持在质量判断中考虑听众反馈和评分；同轮的按内容分类用于推荐是另一项信息，不合并成评分决定分类。',
                        supported_parts=[g['statement']],unsupported_parts=[],assumptions=[],
                        reasoning_steps=['先用T024确定质量评估语境，再核对T025反馈/评分条目。','按内容分类与反馈评分在回答中分别描述，不推断两者有分类依据关系。'])
    g2=goals['DOC015-G02']
    g2['context'].append('受访者另述按播客内容归类以辅助推荐；没有说明用听众反馈或评分决定类别，也没有证明分类足以实现个性化推荐。')
    g2['evidence'].append(dict(source_id='DOC015:T025',quote=quote,role='context'))
    g2['support']['rationale']+=' T025按播客内容归类的说明仅作为辅助推荐的所述方式保留，不把反馈评分作为分类依据。'
    g2['support']['reasoning_steps'].append('分类按内容进行并服务建议，与质量评价中的听众反馈分开理解。')
    review=authored['author_review']
    old_g2=old['goals'][1]
    old_g12=old['goals'][11]
    for original_goal,new_goal in [(old_g2,g2),(old_g12,g)]:
        old_line=next(line for line in review.splitlines() if line.startswith('- '+original_goal['candidate_id']+'：'))
        new_line='- '+new_goal['candidate_id']+'：'+new_goal['statement']+'。origin='+new_goal['origin']+'；support='+new_goal['support']['label']+'。'+new_goal['support']['rationale']+' 条件：'+'；'.join(new_goal['context'])+'。'
        review=review.replace(old_line,new_line)
    authored['author_review']=('# DOC015 外层 v3：独立复核后的局部修订\n\n'
        '修订发现ER-B3-001：原G12把内容分类依据与质量反馈交叉合并。父代理回查T019–T029，收窄G12为质量评价中的反馈/评分，把按内容分类辅助推荐的方式转为G02上下文并增加真实引文。未新增目标，ID均保留，两候选组不依赖这两个目标且内容不变。\n\n'
        '本轮语义重核仅覆盖G02/G12及相关来源；其余29目标保留先前生成方自检与独立复核的既有记录，没有声称父代理重新语义评审全篇。全部31目标及2组由冻结脚本重新定位、绑定、组装和检查。新增G02证据会使后续E编号重新分配，属于本包定位编号变化，不代表其他目标语义变化。\n\n'
        '以下沿用初始生成方全篇自检，并更新受影响的两条记录；v2原件不改。人工状态仍pending，没有伪造feedback。\n\n'+review)
    target=OUT/'revised/_authoring/DOC015-v3.json'
    with target.open('xb') as f:f.write((json.dumps(authored,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
    record=dict(finding_id='ER-B3-001',document_id='DOC015',before_authoring=original.relative_to(OUT).as_posix(),
                before_authoring_sha256=hashlib.sha256(original.read_bytes()).hexdigest(),after_authoring=target.relative_to(OUT).as_posix(),
                semantic_changed_goal_ids=['DOC015-G02','DOC015-G12'],goals_added=[],goals_removed=[],groups_changed=[],
                source_review_turns=['DOC015:T%03d'%n for n in range(19,30)],source_unchanged=True,
                reason='Separate content-based categorization for recommendations from listener feedback/ratings in quality evaluation.',
                human_feedback=False,human_acceptance='pending',independent_recheck='pending')
    (OUT/'revised/_authoring/DOC015-v3-revision-record.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(target)


if __name__=='__main__':main()
