# -*- coding: utf-8 -*-
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'output1/review'
def load(p): return json.loads(p.read_text(encoding='utf-8-sig'))

# These are the reviewer's source-grounded assessments, not author-review imports.
alignments = {
'DOC010': [
(['G1'], ['G01'], ['T007','T013'], '总体天气规划', '两者保留穿着、户外活动、旅行的用途；新版明确是不同情境，不是每次三者同时完成。旧版支持理由也有该限定。语义相当。'),
(['G2'], ['G02','G13'], ['T013','T014','T015','T025','T037'], '日常准备与便捷取得信息', 'G02承接穿戴携带物目的；新增G13从“信息够用便结束查询”和助手失败后用应用推断便利获取，有正面依据且标inferred。旧版G2已保存助手路径障碍，新增是将隐含结果显式化，不直接判旧版漏提。'),
(['G3'], ['G03'], ['T017','T019','T021'], '旅行、整周天气、购票前规划', '均保留旅行时整周、平日逐日的区别及买票前用途；游乐园只是例子，没有无条件禁止雨天旅行。'),
(['G4'], ['G04'], ['T031','T033'], '陌生地点熟悉天气', '均保留新地点与长期熟悉地点的差异，没有泛化地域属性或强制定位功能。'),
(['G5'], ['G05','G06'], ['T035','T037','T039'], '极端天气告警和避免外出', '旧版合并通知及延期/避免外出的用途，新版拆分信息与用户行为；两者均有来源。新版未授权应用自动取消活动，拆分不是旧版缺失。'),
(['G6'], ['G07'], ['T041','T043','T044','T045','T049','T065'], '常规通知频率偏好', '三次有明确确认；旧版早午晚“各一次”未保留时间分布的usually及偏好语气，存在轻度强化（PR-001）。新版约三次/更愿意并保留降雨例外，更忠实。'),
(['G7'], ['G08'], ['T049','T063','T066','T067'], '降雨时频繁通知', '两者都保留条件与频率未知。新版“雨势变化”可被理解为雨强，原文adding/going不清，记录PR-003局部歧义，未确认是新增雨强要求。旧版“降雨变化”更保守。'),
(['G8'], ['G09','G12'], ['T051','T054','T055','T057','T060','T061','T069','T071'], '实时更新与可靠性', '实时更新均有直接支持；新版G12将错报导致外出受阻的可靠性改善另列为inferred并排除零误差。旧版G8及问题已区分时效和准确性，但未单列改善结果；不因多一个节点确认旧版漏提。旧版技术限制归因语气见PR-002。'),
(['G9'], ['G11'], ['T057','T059','T060','T061','T071'], '跨平台天气一致', '均指天气信息而非界面一致，且未将一致等同正确。新版明确同步故障原因尚未核实。'),
(['G10'], ['G10'], ['T057','T071'], '无广告', '无广告是明确偏好且有受阻体验；两版均未加免费或特定商业模式，新版偏好语气更可见。旧版目标式表述本身不等于强制采纳。'),
],
'DOC023': [
(['G1'], ['G01'], ['T003'], '增加人脉数量', '均忠实保留数量目的，没有用采访者的“有意义连接”替代，也无数量指标。'),
(['G2'], ['G02'], ['T003'], '向他人展示活跃', '均保存目的与连接数这一选定展示方式；不声称他人必定认同活跃。'),
(['G3'], ['G03'], ['T003','T009','T011'], '目标公司在职员工内推', '均保留实习/全职及现任员工范围；未把3rd company当第三家公司约束，未把个人资格理解升级为所有公司政策。'),
(['G4'], ['G04'], ['T003'], '增加简历被看到的机会', '均保留有时有帮助的或然性，不保证招聘结果。来源是明确用途，direct可成立。'),
(['G5'], ['G05','G06','G07'], ['T007','T009','T011'], '在职与同校的筛选交集', '新版将复合筛选拆成父目标及两个条件，父限定具体求内推情境。两版均不选已离职者，同校帮助是信念而非保证。旧版“校友”与在读范围已有待确认问题，新版“本校就读背景”更包容；不以此确认旧版排除在读。'),
(['G6','G7'], ['G10','G11'], ['T009','T013','T015'], '足量可访问人选与匹配背景', '两版都区分访问数量限制与相关性，未保证购买会员解决匹配。旧版改善负担/扩大候选标inferred；新版G10/G11以T015明说访问尽可能多、改词找更匹配者标direct，有直接用途依据。不能仅以标签不同判错。'),
(['G8'], ['G08','G12'], ['T007','T017'], '附言表达与压缩负担', '新版将已有明确附言用途与从限制推断的改善拆开；旧版合并并标inferred，核心含义均受支持。两版均保留内推请求非必附，也没指定无限字数。'),
([], ['G09'], ['T007'], '接受连接后继续聊细节', '新版明确保留现有能力的使用目的和接受条件。旧版内推目标及F2提及对方接受这一依赖，未独立表达继续聊天的结果；这是可回查的覆盖风险，仍可能被广义内推过程覆盖，不确认漏提。'),
(['G7'], ['G13'], ['T015'], '昂贵会员与替代方式取舍', '旧版G7条件保留费用高及扩大可见范围，新版从因费用改词的行为推断减少昂贵依赖并保留仍可购买；推断有依据。不是要求免费，不把旧版未单列成本节点直接当遗漏。'),
],
'DOC031': [
(['G1'], ['G01'], ['T001','T005','T007','T025'], '校内即时沟通', '均限定大学对象；新版条件保留仍继续使用Slack，不推出一应用包办全部沟通。即时未量化，不自动等于每人立即回应。'),
(['G2'], ['G02','G03'], ['T007','T029','T031'], '免存联系方式找人及多设备', '旧版复合，新版拆分。赞赏、日常用途及推荐给新人提供维持意图依据，不因已实现而删掉。姓氏可查需结合sometimes和重名未知，条件已有约束；没有确认跨全网或唯一定位保证。'),
(['G3'], ['G04'], ['T009'], '频道触及广泛受众', '均保留频道方式和较广受众，立即是原文诉求，没有扩为保证全员已读。'),
(['G4'], ['G05','G06'], ['T009','T019'], '加入前历史和了解动态', '旧版复合目标direct，新版分历史维持inferred与了解动态direct。T009有明确赞赏和用途，两种来源判断都可辩护；新版更显式标维持推断，不因此判旧版虚构。两者均保留历史价值，没有因搜索拥挤删除历史。'),
(['G5'], ['G07'], ['T011','T013','T017','T029'], '协作时即时分享文档', '两版保留私信方式在条件中；没有把逐步附件操作、表情格式或any file升级为无限文件规格。'),
(['G6'], ['G08'], ['T018','T019'], '从大量结果找到所需消息', '均由明确检索任务与困难推断改善，有正面依据；未指定删除旧消息或唯一算法。'),
(['G7'], ['G09'], ['T021','T023','T025','T027'], '更易进入音视频/群组通话', '均正确保留功能已经存在、入口不便与有号码时可外拨等条件；未把不便升级为放弃Slack。'),
(['G8'], ['G10'], ['T027'], '正式沟通快捷跳转邮件应用', '两版完整保留正式沟通与外部标准邮件应用这一选定方式，不自动发、不仅限一个厂商。'),
(['G9'], ['G11'], ['T031'], '缩窄浏览器窗口导航', '两版保留多窗口窄浏览器条件和手机/大屏正面体验。新版显式保留could be considered建议语气；旧版仍能方便导航是合理期望表达，但建议状态可更清楚（PR-004），不是已确认承诺。'),
]}

findings = [
{'id':'PR-001','branch':'baseline','document':'DOC010','objects':['G6'],'category':'semantic_deviation','severity':'low','status':'confirmed_local_wording_strengthening','blocking_extension':False,'evidence':[{'source_id':'DOC010:T041','quote':"it's usually in the morning. in the afternoon, afternoon and in the evening."},{'source_id':'DOC010:T044','quote':'For notifications, and you change the frequency to thrice a day.'},{'source_id':'DOC010:T045','quote':'Yes, yes.'}],'judgment':'每日三次本身有确认，问题是把通常的早午晚分布写成每天各一次，并弱化个人偏好状态。降雨例外已保留，故是局部轻度强化而非无条件总上限错误。','suggestion':'改为受访者平常偏好一天约三次、通常分布在早晨下午晚上；保留已配置状态及降雨例外。','comparison':'revised G07已清楚表达约三次、更愿意及例外。'},
{'id':'PR-002','branch':'baseline','document':'DOC010','objects':['G8.conditions'],'category':'expression_insufficiency','severity':'low','status':'unresolved_attribution_wording','blocking_extension':False,'evidence':[{'source_id':'DOC010:T055','quote':"It's just like the technology is not there yet, I guess."}],'judgment':'“受访者承认技术对天气预测仍有限制”没有显式保留猜测语气；但仍归属于受访者，并未据此断定具体技术根因。不能据此计为严重信念事实化。','suggestion':'改成受访者猜测可能与预测技术限制有关，根因未核实。','comparison':'revised G09明确写猜测和非核实事实。'},
{'id':'PR-003','branch':'revised','document':'DOC010','objects':['G08','F02'],'category':'source_ambiguity_and_wording_risk','severity':'low','status':'unresolved_in_v1','blocking_extension':False,'evidence':[{'source_id':'DOC010:T049','quote':"when it's stopping, when it's adding like when it's going"},{'source_id':'DOC010:T063','quote':"when it's raining and not raining."}],'judgment':'v1“雨势变化”可被读成雨强变化，但原文能稳妥支持的是雨情开始、停止和变化，adding/going含义不清。尚不能确认作者意在新增强度指标，故不计确认语义错误；若按雨强义解释，direct整句支持不足。F02已为proposed/partial，并未由此形成错误成立精化。','suggestion':'另存版本将“雨势变化”收窄为“雨情变化”或“降雨状态变化”，保留开始/停止与不确定频率；同步重核支持与依赖F02。','comparison':'baseline G7用“降雨开始、停止及变化”更保守。'},
{'id':'PR-004','branch':'baseline','document':'DOC031','objects':['G9'],'category':'expression_insufficiency','severity':'low','status':'unresolved_suggestion_status','blocking_extension':False,'evidence':[{'source_id':'DOC031:T031','quote':'I feel like that is an area of improvement that could be considered.'}],'judgment':'目标及条件清楚表达缩窗改善方向，却未突出原文是可考虑的建议。目标式“仍能方便导航”可合理读为期望，且人工状态pending，不确认其已变成强制承诺。','suggestion':'在陈述或条件明确“可考虑改善”的建议状态，保持场景不变。','comparison':'revised G11已在陈述与条件保留建议语气。'}]

group_rows = [
('baseline','DOC010','F1','candidate_correct',['T007','T019','T035'],'G2/G3/G5涉及不同规划用途；普通户外活动并未穷尽，也无从信息到合适计划的充分规则。proposed/partial适当。'),
('baseline','DOC010','F2','candidate_correct',['T049','T051','T057','T071'],'频繁通知可仍旧过时，多平台可一致地错；降雨局部不覆盖所有实时更新。proposed/partial适当。'),
('revised','DOC010','F01','candidate_correct',['T007','T017','T019'],'穿戴及旅行是实例，不穷尽总体户外规划；未形成成立AND。'),
('revised','DOC010','F02','candidate_correct',['T049','T063','T069'],'下雨时频繁通知不保证实时或覆盖非降雨。候选状态正确；G08词义风险不使组升级成立。'),
('revised','DOC010','F03','candidate_correct',['T035','T039'],'收到告警不等于已读、决定延期并实际不外出；仍为贡献候选，未宣称充分。'),
('baseline','DOC023','F1','candidate_correct',['T003'],'连接数增加不必然让他人看见并认为活跃；候选适当。'),
('baseline','DOC023','F2','candidate_correct',['T007','T009','T011','T013','T017'],'找到匹配人、更多结果及充分附言仍依赖他人接受/愿意内推。没有误将寻找过程当保证。'),
('baseline','DOC023','F3','candidate_correct',['T003'],'sometimes helps不构成确定内推效果；候选适当。'),
('revised','DOC023','F01','supported_with_explicit_scope',['T007','T009','T011'],'G05只约束本例所选人脉同时满足在职与同校。G06核验同一所选人脉的在职属性，G07保留同校选择；在资料真实且当前、两者约束同一选择集合的解释下，两条件合取足够满足父筛选约束。无须对方愿意帮助或存在至少一个候选人，父目标本来不保证内推或候选存在。资料真实性是显式领域假设，未当已证事实；complete只限这两项资格。'),
('revised','DOC023','F02','candidate_correct',['T007','T009','T011'],'资格筛选、附言和接受后聊天不保证他人接受及内推。候选适当。'),
('revised','DOC023','F03','candidate_correct',['T003'],'数量与别人判断之间仍有可见性/理解条件，候选适当。'),
('revised','DOC023','F04','candidate_correct',['T003'],'有时帮助不能保证每次提高曝光；候选适当。'),
('baseline','DOC031','F1','candidate_correct',['T007','T009','T013','T025','T027'],'便利功能集合不保证即时通信达成，且不一定每次共同使用；候选适当。'),
('baseline','DOC031','F2','candidate_correct',['T009','T019'],'搜索更容易本身不赋予加入前历史访问，也不保证了解动态；候选适当。'),
('revised','DOC031','F01','candidate_correct',['T007','T009','T013'],'找人、多设备、频道和分享有帮助，但不是完整的即时沟通充分条件；候选适当。'),
('revised','DOC031','F02','candidate_correct',['T009','T019'],'能访问历史并不保证获知当前动态，需相关性与阅读等条件；候选适当。'),
]

models = {(b,d):load(ROOT/f'output1/{b}/{d}/v1/delivery/goal-model.json') for b in ('baseline','revised') for d in alignments}
goal_reviews=[]
for (b,d),m in models.items():
    for g in m['goals']:
        matches=[a for a in alignments[d] if g['goal_id'] in a[0 if b=='baseline' else 1]]
        assert matches,(b,d,g['goal_id'])
        related=[f['id'] for f in findings if f['branch']==b and f['document']==d and any(o.split('.')[0]==g['goal_id'] for o in f['objects'])]
        goal_reviews.append({'branch':b,'document':d,'goal_id':g['goal_id'],'statement':g['statement'],
          'source_turns':sorted(set(d+':'+t for a in matches for t in a[2])),
          'source_and_support_review':'reviewed_in_full_with_conditions_origin_inference_and_support',
          'conclusion':'qualified_by_findings' if related else 'supported_with_recorded_conditions',
          'finding_ids':related,'assessment':' '.join(a[4] for a in matches)})

groups=[]
for b,d,gid,result,turns,reason in group_rows:
    g=next(g for g in models[b,d]['refinement_groups'] if g['group_id']==gid)
    groups.append({'branch':b,'document':d,'group_id':gid,'parent_id':g['parent_id'],'child_ids':g['child_ids'],
                   'author_status':g['status'],'author_completeness':g['completeness'],'review_conclusion':result,
                   'source_turns':[d+':'+t for t in turns],'reason':reason,'formal_proof':'not_run'})
assert len(goal_reviews)==64 and len(groups)==16

coverage = [
{'document':'DOC010','candidate':'便捷获取足够天气信息/可靠性改善','baseline':'G2/G8及证据和问题已有路径、预测误差语境；未分别建便利性和可靠性目标','revised':'G13/G12为有依据推断','status':'richer_explicit_representation_not_confirmed_baseline_omission'},
{'document':'DOC023','candidate':'接受后聊天进一步细节','baseline':'无独立目标；G3内推目的、F2接受依赖及T007完整证据已保留','revised':'G09显式有条件保留','status':'candidate_coverage_risk_not_confirmed_omission'},
{'document':'DOC023','candidate':'减轻昂贵会员依赖','baseline':'G7条件保留成本取舍','revised':'G13从因成本转向改词推断改善','status':'richer_explicit_representation_not_confirmed_baseline_omission'},
{'document':'DOC031','candidate':'多设备、加入前历史、动态关注','baseline':'G2/G4复合覆盖','revised':'G02/G03、G05/G06分开表达','status':'covered_in_both_granularity_difference'},
{'document':'DOC031','candidate':'格式、表情、any file、步骤左右布局','baseline':'G5操作背景/证据','revised':'G07条件/证据','status':'no_confirmed_independent_result_intent_no_required_new_nodes'},
{'document':'DOC010/DOC023/DOC031','candidate':'第一阶段重要意图与例外总体回查','baseline':'主要意图均有目标或必要上下文承载；局部表达和候选风险另记','revised':'全部重要意图及例外有目标/条件/问题/证据承载','status':'no_confirmed_omissions_found_within_read_scope_not_exhaustiveness_proof'},
]
engineering=load(OUT/'engineering/projection-and-evidence-audit.json')
data={
 'record_type':'independent_context_pilot_review_local_record_not_core_schema',
 'review_date_local':'2026-10-24','reviewer':'/root/pilot_review','execution_model_exact_id':'unknown','execution_model_switch_status':'unknown',
 'independence':{'source_criteria_written_before_outputs':True,'generator_context_inherited':False,'external_human_review':False,'formal_proof':'not_run','author_review_files_read':False,'limitations':'独立上下文模型复核；与生成方共享模型体系。精确模型ID/采样参数/额度中断后的运行模型连续性未知。'},
 'scope':{'source_documents':{'DOC010':'T000-T077 (78)','DOC023':'T000-T018 (19)','DOC031':'T000-T032 (33)'},'baseline':{'goals':27,'groups':7,'supported_complete':0},'revised':{'goals':37,'groups':9,'supported_complete':1},'unreviewed_goals':[],'unreviewed_groups':[],
   'semantic_materials_read':['全部6份delivery/goal-model.json的goals含条件/origin/inference/support、issues、limitations及引用映射','全部6份kaos-decisions.json（全部组、依据和问题）','第一阶段完整source.txt/source-input.json及规则；第二阶段对争议轮次回读','本次_run/evaluation-protocol.md及model-review/references/tools.md'],
   'programmatic_materials_checked':['全部extraction候选到交付目标的投影','全部judgments到support的投影','全部决策组到交付组的投影','191处模型引文与全文/轮次精确对应','6份冻结source输入及assembled/delivery一致性'],
   'not_claimed_read_or_reviewed':['author-review.md未用于接受结论','模板和全部运行记录未逐一语义阅读','HTML/SVG未做浏览器视觉/交互测试','录音/原始JSON附件未重新核听或逐字比对','旧output、研究答案、development_reference、upstream_reference未读取']},
 'alignments':[{'document':d,'baseline_goal_ids':a[0],'revised_goal_ids':a[1],'source_turns':[d+':'+t for t in a[2]],'semantic_unit':a[3],'assessment':a[4]} for d, rows in alignments.items() for a in rows],
 'goal_reviews':goal_reviews,'group_reviews':groups,'findings':findings,'coverage_recheck':coverage,
 'engineering':{'inspect_reexecuted':6,'all_structure_passed':True,'exact_model_quotes_checked':191,'projection_or_quote_errors':[],'details':'engineering/projection-and-evidence-audit.json','original_inspections_changed':False,'core_independent_semantic_status':'not_run_unchanged'},
 'gate_v1':{'decision':'pass_with_nonblocking_findings','blocking_revised_severe_deviations':[],'semantic_basis':'新版没有尚未处置的严重无依据强化、信念事实化或错误成立精化。PR-003局部歧义可保守修订，不构成扩展阻断。无为消错删除已支持重要意图的证据。','required_before_expansion':[],'recommended_revision':['PR-003另存版本收窄雨势措辞并重核G08/F02'],'human_acceptance':'pending','formal_proof':'not_run'},
 'revision_followup':{'status':'awaiting_parent_notification','note':'父代理已通知拟另存revised DOC010 v2；本记录仍是v1冻结比较，不将未收到的修订计已解决。'},
 'interpretation_limits':['不以目标或问题条目数计算错误率/加权得分。','三篇为已接触开发案例，不能外推总体技能优劣或其余31篇正确率。','不是随机重复实验；生成上下文差异与采样不可控，不能把差异全归因技能修改。','原文精确定位不证明含义；本次模型语义复核不是外部验证或人工采纳。']
}
(OUT/'pilot-review.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')

lines=['# 三篇同源试运行：冻结 v1 独立语义比较','',
'结论：新版 v1 达到扩展门槛，带一项不阻断的局部措辞歧义 PR-003。没有发现新版尚未处置的严重无依据强化、信念升级为事实或错误成立精化。新版在偏好/建议语气、已有能力维持、部分推断结果与条件呈现上更清楚；多数差异是拆分或显式化，不能据节点数量宣称更高召回率。基线也保留了主要意图、例外及精化不确定性。',
'','## 复核身份、范围与证据层次','',
'复核者 `/root/pilot_review` 先独立阅读完整来源并保存 `pilot-source-criteria.md` / `criteria.json`，冻结后才读两分支结果。属于独立上下文模型复核，非外部人审、形式证明或采纳意见。精确执行模型标识及额度中断后模型是否切换为 unknown。未读生成方 author-review.md 来替代判断，未读历史输出或研究参考答案。',
'','| 文档 | 完整来源 | baseline目标/组 | revised目标/组 | 已成立组 |','|---|---|---:|---:|---|',
'| DOC010 | T000–T077，78轮 | 10 / 2 | 13 / 3 | 两版均0 |',
'| DOC023 | T000–T018，19轮 | 8 / 3 | 13 / 4 | 仅新版F01 |',
'| DOC031 | T000–T032，33轮 | 9 / 2 | 11 / 2 | 两版均0 |',
'| 合计 | 130轮 | 27 / 7 | 37 / 9 | 1 |','',
'全部64个目标的陈述、主体、条件、origin、inference、support及引用范围均已复核；全部16组先于逐目标检查。模型中的问题和限制也已读取。提取与支持判断原件用程序逐字段确认与模型投影一致，故不存在因只看交付而漏掉不同目标内容的情形。191处模型引文逐一匹配冻结全文和轮次。关键疑点重新阅读原问题、回答与后续例外。',
'','以各自技能快照重新执行6份 inspect，全为 passed，另存 `engineering/`；原 v1 inspection 保持不变，`independent_semantic=not_run`、`formal_proof=not_run`和人工pending不手填通过。本报告是额外独立上下文复核层。未做HTML/SVG视觉或交互验收，未核听录音，未逐一语义阅读模板和全部运行日志。','',
'## 逐语义单元对齐（覆盖全部目标）','',
'编号均带所在分支和文档解释，不按ID对应。一个旧目标可以对应多个新版目标；“-”代表无独立节点，不自动表示遗漏。下表连同机器记录的逐目标条目覆盖全部64个目标。']
for d,rows in alignments.items():
    lines += ['',f'### {d}','','| 语义单元 | baseline | revised | 原文轮次 | 独立判断 |','|---|---|---|---|---|']
    for bs,rs,ts,label,assessment in rows:
        lines.append('| '+' | '.join([label,', '.join(bs) or '—',', '.join(rs),', '.join(ts),assessment])+' |')
lines += ['','## 全部精化组审查','','所有未成立候选均有未解决充分性理由；这些候选的存在不计为错误成立精化。没有强行要求完整树。以下反例/条件分析是复核者的分析检验，不冒充新增访谈事实或穷尽证明。','','| 分支/文档/组 | 作者状态 | 复核结论及依据 |','|---|---|---|']
for g in groups:
    lines.append(f"| {g['branch']} / {g['document']} / {g['group_id']} | {g['author_status']} / {g['author_completeness']} | {g['reason']} 来源：{', '.join(g['source_turns'])}。 |")
lines += ['','新版DOC023 F01的关键边界：同一求内推场景、同一所选人脉集合，同时满足当前公司任职与本校背景。它仅分解筛选约束，不证明资料真实、不保证合适者存在、不要求获得内推成功。资料真实性/时效已列为假设；同校者更愿帮助在G07中明确作为受访者推测。因此当前 supported/complete 在限定范围内可接受。若后续将父目标扩为“找到合适内推人”或“得到内推”，必须重新评估，不能沿用此结论。',
'','## 具体发现及处置','','没有新版严重阻断项。以下低严重度条目不能相加称为“错误目标数”；其中只有PR-001是本次确认的局部措辞强化，其他为表达不足或歧义风险。']
for f in findings:
    lines += ['',f"### {f['id']} · {f['branch']} {f['document']} {', '.join(f['objects'])}",'',
      f"类别：{f['category']}；严重程度：{f['severity']}；状态：{f['status']}；不阻断扩展。",'',f['judgment'],'',
      '证据：'+'；'.join(e['source_id']+' “'+e['quote']+'”' for e in f['evidence'])+'。','',
      '具体建议：'+f['suggestion'],'','比较：'+f['comparison']]
lines += ['','## 候选覆盖缺口回查与正确边界','','未发现可在当前完整阅读范围内确认的新版意图遗漏。此结论不是穷尽性证明。以下专门区分真实缺项、已有综合覆盖与表达差异：']
for c in coverage: lines += ['',f"- **{c['document']}：{c['candidate']}**。baseline：{c['baseline']}。revised：{c['revised']}。判断：{c['status']}。"]
lines += ['','值得保留的正确/边界案例：',
'', '- DOC010 两版均保留普通日常、旅行整周、极端天气与降雨频繁通知的不同情境；三次通知没有被错误设成所有告警硬上限。无广告可成为偏好结果，不能因“更喜欢”删除。',
'- DOC023 数量展示与获得内推是不同目的；两版都未把“有意义连接”替换数量目标。同校意愿是信念，内推有时帮助曝光不是因果保证；新版G10/G11的direct有明确使用目的依据，并非必须机械降为inferred。',
'- DOC031 已实现能力仍可有维持价值：免存联系方式、多设备、历史访问和文档分享有赞赏/用途依据。新版将历史维持标inferred是保守来源记录，旧版复合direct也有明确正面语境，不能仅凭标签判错。',
'- 历史可见性与搜索负担并存不构成自动逻辑冲突；正式邮件跳转不能抽象成内建邮箱；缩窄浏览器困难不能泛化为手机不好用。两版均守住这些边界。',
'','## 扩展决定与限制','',
'冻结v1门槛为 **pass_with_nonblocking_findings**。工程绑定检查通过；新版没有严重无依据强化、信念事实化或错误成立精化；重要意图与例外没有为消除问题而删去。建议另存版本处理PR-003并重核相关支持与F02，不需要为通过而增加目标、删除候选或改核心检查状态。',
'','父代理已通知计划对DOC010另存v2，本报告暂不把尚未提供的修订算作已解决；收到完成通知后另附修订复核，原v1对照不覆盖。',
'','这些是三篇已接触开发案例的一次上下文隔离试运行，没有重复采样、随机分组或已知模型参数控制，不能把差异全部归因技能修改，也不能外推其他31篇的错误率。扩展结果应继续区分生成方自检、实际工程核验及独立语义复核范围。所有模型仍待真实人工审核。']
(OUT/'pilot-comparison.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
gate='''# Pilot 扩展门槛（冻结 v1）

**决定：pass_with_nonblocking_findings，可扩展。** 未发现新版尚未处置的严重无依据强化、信念事实化或错误成立精化。这个决定是独立上下文模型复核意见，不是外部人审、采纳或形式证明。

| 门槛 | 实际证据 | 判断 |
|---|---|---|
| 来源完整且可追溯 | 三篇130轮全文；191处模型引文匹配全文/轮次；两分支源副本一致 | 满足 |
| 工程检查绑定实际文件 | 各自快照重新执行6次inspect通过；提取、判断、组到交付的投影无差异 | 满足 |
| 全部目标与精化组复核 | baseline 27目标/7候选组；revised 37目标/9组，含1成立组；无未查对象 | 满足 |
| 无新版严重语义偏差 | 没有把条件偏好变无条件强制、个人信念变已证事实或候选关系变保证 | 当前范围未发现 |
| 已成立组正确限定 | revised DOC023 F01只分解同一人脉选择的在职及同校条件，带资料真实性假设，不保证内推 | 可接受 |
| 正确意图与例外保留 | 普通/降雨通知、旅行整周、内推或然性、历史访问价值、邮件跳转、窄窗条件均保留 | 满足 |

不阻断项：PR-003（revised DOC010 G08）“雨势变化”可能被读成雨强，原文转写不明确。建议另存版本收窄为雨情/降雨状态变化并同步重核G08及候选F02。该组原本proposed/partial，所以没有错误成立精化；不能将这一措辞歧义统计为已确认严重错误。父代理已计划另存v2，尚未收到完成通知时不记已解决。

基线的PR-001是轻度时间分布措辞强化；PR-002/PR-004是来源猜测、建议状态的表达不足。它们用于如实比较，不构成新版门槛阻断，也不能合成为任意错误率。目标数量37对27主要包含拆分与显式化，不是质量分数。

执行下一步：允许按已授权任务扩展其余31篇，同时保留每篇原文绑定、候选组状态和真实未决。若采用DOC010局部v2，先完成该版本的独立补查后再把PR-003标解决；不得覆盖冻结v1。不能把试运行结论标记成全部扩展篇独立审查已通过。

局限：精确模型ID及中断前后模型连续性unknown；模型体系共享，非外部评审；未核听录音、未做HTML/SVG交互视觉测试、未证明需求穷尽或形式可实现性。核心inspection的independent_semantic/formal_proof仍保持not_run，人工pending不变。详细证据见pilot-comparison.md、pilot-review.json与engineering/。
'''
(OUT/'pilot-gate.md').write_text(gate,encoding='utf-8')
print(json.dumps({'goal_reviews':len(goal_reviews),'group_reviews':len(groups),'alignment_units':sum(map(len,alignments.values())),'findings':len(findings),'gate':'pass_with_nonblocking_findings'},ensure_ascii=False))
