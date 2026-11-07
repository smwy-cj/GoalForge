"""Full-context author self-review before the first extraction/support package.
The initial semantic-specs.py remains intact. These are not human feedback.
"""
def apply(DOCS):
    DOCS['DOC010']['goals']['postpone']['statement']='遇到极端天气时推迟整个活动。'
    DOCS['DOC010']['goals']['postpone']['rationale']='推迟活动与不外出可分别满足，因此分开保留。'
    DOCS['DOC010']['goals']['stayhome']={
        'turn':35,'statement':'遇到雷暴、洪水等极端天气时不外出。',
        'rationale':'原文另有don’t go out at all的独立避免意图，不把普通降雨扩大为禁足。',
        'origin':'explicit','context':[],'extra':[]}
    DOCS['DOC010']['captures'][35]['keys'].append('stayhome')
    DOCS['DOC028']['goals']['mobile']['statement']='改善 Reddit 官方 Android 等移动应用的易用性。'
    DOCS['DOC028']['goals']['mobile']['rationale']='T063明确希望改善官方移动应用；T027说明操作不直观。运行速度另项保留。'
    DOCS['DOC028']['goals']['mobileperformance']={
        'turn':27,'statement':'改善 Android 版 Reddit 的运行流畅程度。',
        'rationale':'慢而沉重是受访者具体移动端挫折，正面支持减少运行阻滞的推断；没有编造性能阈值。',
        'origin':'inferred','context':['这是本人Android手机上的体验，未验证所有手机。'],'extra':[]}
    DOCS['DOC028']['captures'][27]['keys'].append('mobileperformance')
    DOCS['DOC020']['groups'][0]['refs']=[4]
    DOCS['DOC020']['groups'][0]['rationale']+=' R008为父目标对招聘目标的贡献，非本组内部依赖，不列入relation_ids。'
    DOCS['DOC036']['relations'][10]['type']='contribution'
    DOCS['DOC036']['relations'][10]['rationale']='新地点的商家位置、联系方式和产品信息有助查找合适商家；二者不是同一核心动作的特定化。'
    DOCS['DOC036']['captures'][72]['uncertain']=True
    DOCS['DOC036']['notes'].append('T072混合复述附和不能确定匿名发帖意图，留为待确认候选；当前只有匿名浏览目标。')
