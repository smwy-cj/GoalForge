import json
from pathlib import Path
p=Path(__file__).resolve().parent
notes={
'DOC014':'生成方末轮自检发现G12把明确的摄氏度偏好与仅被描述的切换能力合在一起。v2收窄为个人摄氏度显示偏好，保留切换为现状方式，重新编制支持说明并重建全部绑定/检查。无人工feedback，v1原件保留。',
'DOC028':'生成方末轮自检纠正自检说明中的定位笔误G39为T039；目标、证据及精化判断逐项回核后未改变。v2重新执行全部绑定、组装与检查，未仅补写哈希。无人工feedback，v1保留。',
'DOC035':'生成方末轮自检将G9明确写为理想情况下页面不显示广告，避免标题仅被读成不遮挡/不打扰而弱化原文无广告意图；重判整句支持并重建全部产物。无人工feedback，v1保留。'
}
for doc,note in notes.items():
    a=json.loads((p/f'{doc}.json').read_text(encoding='utf-8'))
    if doc=='DOC014':
        g=next(g for g in a['goals'] if g['candidate_id']=='DOC014-G12')
        g['statement']='天气温度显示更偏好摄氏度。'
        g['context']=['本人单位偏好；当前通过顶部单位切换达到该设置，不要求默认影响其他人。']
        g['support']['rationale']='本人直接说明prefer Celsius；整句只保留该个人偏好，已有切换能力作为现状方式承接，不把能力描述升级为另一明确维持要求。'
        g['support']['supported_parts']=[g['statement']]
        g['support']['reasoning_steps']=[g['support']['rationale']]
        a['author_review']=a['author_review'].replace('明确偏好摄氏并已使用单位设置；保留既有切换的个人维持意图。','本人直接说明prefer Celsius；当前只保留个人显示偏好，切换方式作为现状，不增添独立维持要求。').replace('保留G12/G14明确已有设置的维持意图','保留G12明确单位偏好与G14明确通知关闭维持意图')
    elif doc=='DOC028':
        a['author_review']=a['author_review'].replace('G39离线缓存','T039离线缓存')
    else:
        g=next(g for g in a['goals'] if g['candidate_id']=='DOC035-G09')
        g['statement']='理想情况下，新闻阅读页面不显示广告。'
        g['context']=['这是本人描述的理想体验；源文既反对遮挡内容的广告，也进一步明确希望新闻页面无广告。']
        g['support']['rationale']='本人直接说ideal news reading experience would be not having ads on the news page；当前表述忠实保留理想无广告意图，没有弱化为仅不遮挡。'
        g['support']['supported_parts']=[g['statement']]
        g['support']['reasoning_steps']=[g['support']['rationale']]
        a['author_review']=a['author_review'].replace('本人先说遮挡问题后明确ideal not having ads on news page，保留无广告理想强度。',g['support']['rationale'])
    a['author_review']+='\n## v2作者主动修订\n\n'+note+'\n所有其余目标及候选组已按同一源文重新回核，判断未改变；没有把作者修订伪装为人工意见。\n'
    a['limitations'].append('目录v2为作者主动修订快照；冻结组装器建立全新待审模型，嵌入模型版本仍为其初始v1，未伪造父模型或feedback。')
    (p/f'{doc}-v2.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (p/f'{doc}-v2-revision-note.md').write_text(note+'\n',encoding='utf-8')
