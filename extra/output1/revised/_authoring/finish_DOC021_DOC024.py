import json
from pathlib import Path

ROOT = Path('output1/revised/_authoring')

# Resume the permitted unfinished draft only after full source rereading.
# Its save call is deliberately not executed; semantic amendments below are authored here.
draft = (ROOT / 'write_DOC021.py').read_text(encoding='utf-8-sig')
ns = {}
exec(draft.rsplit('\nsave(', 1)[0], ns)
g, f, q, r = (ns[x] for x in ('g', 'f', 'q', 'r'))
g[2]['statement'] = '按预算、面积或卧室数筛选房源，有特定工作或学校时通常选择附近地区'
g[2]['support']['supported_parts'] = [g[2]['statement']]
g[4]['statement'] = '希望房源信息保持最新，并能看到最后更新时间'
g[4]['support']['supported_parts'] = [g[4]['statement']]
g[4]['support']['rationale'] = 'T059/067/069分别明确更新时间可见和信息仍最新的诉求；未把这些线索加强为信息真实性已经得到保证。'
g[6]['statement'] = '可以考虑像电商选择现有选项一样，直接选择已列规格的感兴趣房源，减少尚未确定需求时的精确填写'
g[6]['support']['supported_parts'] = [g[6]['statement']]
g[6]['support']['rationale'] = 'T025为Maybe式建议，T023说明需求灵活、只想选现有选项的情境；保留建议强度及选定方式，不推为直接购买。'
g[8]['statement'] = '希望仍可用地图画定搜索区域，更灵活地包含邻近合适房源'
g[8]['support']['supported_parts'] = [g[8]['statement']]
g[17]['statement'] = '希望通过更透明的信息和流程，更安心、有信任地继续参与选房过程'
g[17]['support']['supported_parts'] = [g[17]['statement']]
g[17]['support']['rationale'] = 'T021明确说明透明带来更信任与参与意愿，并以might保留效果不确定；当前目标表达主观希望而非客观真实性保证。'
r += '''\n## 本次续作回查与明确修正\n
本次执行者完整重读冻结原文T000—T076（先0—39，再40—76；后半在首次整段读取中已覆盖），没有依据草稿标签替代核验。以上逐目标记录对当前18个目标逐项核对，两个精化候选亦整组重判。草稿未曾成功组装，无已交付模型被改写。本次将G03的“需要时”还原为特定工作/学校情境下的“通常”；G05收窄为新鲜度与更新时间可见，不宣称真实性保证；G07恢复Maybe建议和电商选项方式；G09明确已有能力的维持意图；G18恢复希望与主观感受。其余目标的语气、例外及证据经回读保留。origin与support分别判断：18项意图均为受访者明确表达或明确赞赏用途下的维持意图；当前整句独立核验为direct，并非从origin自动填值。\n
复核问题REV21-01（G05/G18/F01，未解决）：更新时间、评价与照片规则只能提供信任线索，不能担保内容真实；已收窄目标且F01保留partial。REV21-02（G06/G17，未解决）：实际回复或许很快，未知的是流程与预期，具体时限pending。REV21-03（G08/G13，未解决）：最少共享字段及双方确认细节pending。REV21-04（G15，未解决）：未知宠物政策如何核实pending。REV21-05（F02，未解决）：发现、筛选、比较和沟通不充分保证入住，保持候选。\n
来源事实未外部核验；执行者为当前续作生成助手；精确模型标识、采样参数、推理/令牌预算均unknown。作者自检非独立审查，人审pending。\n'''
ns['save']('DOC021', g, f, q, r, ns.get('model_questions', None) or [
    {'target_type':'group','target_id':'DOC021-F01','message':'可信线索不能保证真实且原文保留might；整组部分贡献。'},
    {'target_type':'group','target_id':'DOC021-F02','message':'找房研究与沟通没有覆盖实际入住全部条件，保持部分候选。'}])

helpers = {}
exec((ROOT / 'batch1_helpers.py').read_text(encoding='utf-8-sig'), helpers)
helpers['DOC'] = 'DOC024'
goal, question, save = (helpers[x] for x in ('goal', 'question', 'save'))
g = [
    goal(1, 'direct', '没有可用答疑时间时，也能随时获得清楚解释，理解课上不懂的基础术语、例子和逻辑', 9,
         "there's no available office hours today, and you have to wait till tomorrow, or even next week to answer those questions.",
         '本人明确随时询问并理解基础内容的用途；未推广为复杂问题始终可靠。',
         ['主要用于学习及自己的项目；认为基础解释较好、高层问题较弱属于本人经验。'],
         extra=[(9, 'And you can ask it like at any time.')]),
    goal(2, 'direct', '项目启动时获得自己未想到的不同视角和创意，以在开始实施前完善想法', 15,
         'it can provide me with some ideas, so I can refine my ideas before I start.',
         '启动阶段的创意用途与不同角度意图明确；不强迫在项目中段持续使用。',
         ['中段项目复杂、提供上下文负担大且可能遗漏，因此本人不太喜欢那时使用。'],
         extra=[(9, "giving me more perspective perspectives from the other fuse like the ones I I can't really sort of by my own.")]),
    goal(3, 'direct', '在项目启动时获得实施概要和重要要点，更清楚如何推进项目', 15,
         'often it can give me an outline about what you should do. And what are the points that are important?',
         '同一回答明确概要与关键点帮助理解实施；未要求完整可执行计划或保证项目成功。'),
    goal(4, 'direct', '需要把新产品可视化时生成图像，并按自己的要求继续修改完善', 11,
         'I will use chat gpt, to generate the image for me, and I will ask Chatgpt to refine it later, based on my requirements.',
         '具体可视化与按要求迭代明确；末尾说不常用不否定这一条件性用途。',
         ['大多数回答是文字；T033明确图像生成并不常用，主要还是解释与逻辑推理。']),
    goal(5, 'direct', '用书籍或论文核验基础术语解释，并对计算问题自行计算后核对答案', 13,
         'You can get some reference from the books or papers online, and then you can check if that\'s correct,',
         '受访者明确两种核验方式及重要性；并不表示已逐题执行或能验证所有复杂问题。',
         ['高级问题有时很难辨认错误，须谨慎；此为本人核验建议，不是外部正确性验证完成记录。'],
         extra=[(13, 'I think you should calculate those by yourself and then check if the result it provides you is correct.')]),
    goal(6, 'direct', '组织提问语言表达问题和上下文，必要时附图像或文档，帮助模型理解所问内容', 17,
         'I will try to organize my language to make chat, gpt, understand what I\'m saying, to understand.',
         '明确表达目的及辅助材料方式；不把努力表达升级成模型保证完整理解。',
         ['纯文字有时难说明全部；模型误解可能给出不符合预期的答案。'],
         extra=[(17, 'sometimes I will use images and documents to help Chatgpt understand my questions better.')]),
    goal(7, 'direct', '回看保存的历史问答和逻辑，以复习已学的术语与推理', 21,
         'you can just click the history and see like what Chat Gpt told you before, and see its logic.',
         '频繁使用历史并明确复习用途，支持维持此能力；未假定历史一定正确。',
         extra=[(21, 'for you to review the the things you\'ve learned.')]),
    goal(8, 'direct', '希望解释和推理的逻辑更准确，并在需要时使用自己认为推理更好的高级模型', 25,
         'it will take more time to think and analyze the logic, but the answer will be more accurate than than the lower lower Level models.',
         '结合T026—027对重视逻辑的确认和T029本人需要高级推理的描述，意图明确；模型优劣仅是受访者信念，标题保留“认为”。',
         ['本人报告购买会员获得高级模型；较长思考与更准确之间的因果和具体型号能力未外部核验。'],
         extra=[(29, 'you really need the High level model to analyze it and reasoning about it like, more logically.')]),
    goal(9, 'direct', '需要深入了解问题时，能向高级模型提出更多后续问题，减少额度用尽后被迫等待', 29,
         'not unlimited, but, like you, you can ask more, follow up questions to the higher level model.',
         '保留本人从unlimited纠正为more的最终含义；没有无限额度或确切次数承诺。',
         ['普通用户用尽后需等明天或数日是访谈经验；不视为当前实际套餐政策。']),
    goal(10, 'inferred', '减少生成长时间卡住和重试造成的等待及可用问答次数浪费', 31,
         "if you regenerate it, it will use the limit of your of your like of your chance talking to it. So that's kind of waste, and it's a waste of time,",
         '本人未直接提出具体修复，但明确把卡住、重试及次数消耗评价为浪费，正面支持减少此损失的意图推断。',
         origin='inferred', reason='从明确不满意的时间与次数损失推断希望减少这些损失，不指定实现方式。',
         assumptions=['受访者把反复等待和消耗称为浪费，意味着希望改善而非接受为必要体验。']),
    goal(11, 'inferred', '对依赖该工具及时完成任务的用户，减少服务宕机带来的任务中断', 31,
         'some people like rely on it to submit their work like, or to like trying to do something in a timely manner.',
         '宕机及恐慌被受访者列为技术问题，支持连续使用意图的有限推断；原文说some people，未冒充本人任务事实。',
         ['主体为受访者所描述、依赖工具及时完成任务的用户；没有零宕机或可用率指标。'],
         origin='inferred', reason='从及时任务受宕机影响且被列为技术问题，推断这些用户希望减少中断。',
         assumptions=['依赖服务及时交付的人通常希望可在需要时使用，材料未明确给出可用率承诺。'])
]
g[-1]['actor'] = '依赖工具及时完成任务的用户（受访者描述）'
q = [
    question([1,5,8], '对于难以自行验证的高层问题，应如何判断答案是否足够可靠？', '本人明确复杂问题难辨错误，当前基础核验方式并不充分覆盖。'),
    question([9,10], '可接受的追问额度、等待时长与失败重试的计次方式是什么？', '只表达更多次数与减少浪费，没有具体阈值。'),
    question([11], '哪些及时任务需要何种连续服务或替代处理？', '为受访者描述的其他用户推断，适用任务和可用率未知。')
]
r = '''# DOC024 生成方语义自检

实际范围：完整读取T000—T035共36轮，包括所有提问、反问、自我修正和末尾说明；原文英文引文保留，未核听录音，未核实OpenAI产品事实。当前续作生成助手负责提取、支持判断、组候选考虑和自检，同一执行者不构成独立语义审查。

逐目标核验（11/11）：G01为无office hours时随时理解基础概念/例子的明确用途，未声称高级问题可靠；G02保留启动阶段不同视角与完善想法，中段不愿使用的原因放条件；G03实施概要/关键点单列，不能保证项目实现；G04条件性产品可视化与迭代，T033“不常用”作为例外；G05保留书籍论文与独立计算两种选定核验方式及高层题难辨错误；G06表达与图文附件为帮助理解的尝试，非保证；G07频繁历史回看及学习用途支持维持；G08本人确认重视逻辑，高级模型比较保持“认为”，不声称客观最新型号能力；G09明确采用T029自我修正后的“更多”，不沿用前句无限；G10由浪费时间及额度的负面评价推断减少损失，origin=inferred和support=inferred分别由意图来源与当前整句正面依据判断；G11从宕机影响他人及时任务推断连续服务，主体未错误改成本人，范围与假设显式保留。G01—09 origin=explicit及direct分别经上下文检验；无从字段自动转换标签。

精化考虑与结论：本篇无成立或候选精化组。G02创意与G03概要同在启动阶段，但概要并不足以产生未想到的视角，二者为不同结果；图像G04也仅偶尔使用，不能强作共同必要子目标。G05、G06可能帮助G01/G08，却不能保证理解或答案逻辑正确。G09、G10、G11有关使用连续性和资源，但没有受访者明确上位总体意图与共同充分条件，不补根或拼成AND。故groups=[]，不是未评估关系。

正常场景（分析假设）：课后不懂基础术语且无答疑，附课堂文档提问，查看解释再用论文核对，日后回看历史；G01/05/06/07相容，是否真正理解尚未测量。项目启动（分析假设）：先获取思路与概要，必要时生成产品图并修改，G02/03/04不被强制为每次同时执行。异常场景（分析假设）：复杂项目上下文遗漏但答案流畅，G06不保证G08，维持谨慎与核验缺口。异常场景（分析假设）：生成卡住后重试继续耗次直至额度用尽，G09“更多”仍不能保证不受限，G10为独立改善目标。异常场景（分析假设）：截止前宕机，材料不确定替代方案或恢复时间，G11仍推断并待审。

稳定问题与状态：REV24-01（G01/G05/G08，未解决）复杂答案可靠性标准及核验途径不足；REV24-02（G09/G10，未解决）额度、耗时、失败计次阈值未知；REV24-03（G11，未解决）受访者描述的他人任务范围与连续性需求待确认。关键问题同时进入review_questions/model_questions。现有契约无完整障碍/偏好关联层，卡住、上下文遗失和高层题错误风险用条件与问题承接。

遗漏风险：T019模型选择是能力介绍，已有G08解释本人重视逻辑的用途，未把型号列表都变成强制需求；T023付费是现状和策略，不推导降价目标；T032采访者说“依赖过多”未获明确单独认领，不建立戒除依赖目标。没有凭采访者评价补目标。来源事实未外部核验，人审pending；独立语义审查与形式证明not_run；精确模型/采样/预算unknown。工程inspect以实际脚本结果为准。
'''
save('DOC024', g, [], q, r, [
    {'target_type':'goal','target_id':'DOC024-G08','message':'高级模型逻辑优劣为受访者信念；复杂问题正确性与采纳标准待确认。'},
    {'target_type':'goal','target_id':'DOC024-G11','message':'主体为受访者所描述用户；连续性意图为有限推断，适用任务及指标待确认。'}])
