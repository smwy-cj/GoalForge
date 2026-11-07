"""Summarize completed evidence-bound reviews; never stamp the core model reviewed."""
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]
PILOT = {'DOC010', 'DOC023', 'DOC031'}
FULL = {
    1: {'DOC003', 'DOC009', 'DOC012', 'DOC034'},
    2: {'DOC014', 'DOC022', 'DOC025'},
    3: {'DOC004', 'DOC015', 'DOC026', 'DOC033'},
}


def load(relative):
    return json.loads((OUT / relative).read_bytes().decode('utf-8-sig'))


def sha(relative):
    return hashlib.sha256((OUT / relative).read_bytes()).hexdigest()


def relative(path):
    return path.removeprefix('output1/') if hasattr(str, 'removeprefix') else (path[8:] if path.startswith('output1/') else path)


def save(path, data):
    (OUT / path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    index = load('_run/delivery-index.json')
    audit = load('_run/final-verification.json')
    assert audit['status'] == 'passed' and not audit['errors']
    selected = {r['document_id']: r for r in index['documents'] if r['arm'] == 'revised'}
    assert len(selected) == 34
    reviews = {n: load(f'review/expanded-batch{n}/review.json') for n in (1, 2, 3)}
    followups = {
        'DOC003': 'review/expanded-batch1/followup.json',
        'DOC025': 'review/expanded-batch2/followup-by-batch3.json',
        'DOC015': 'review/expanded-batch3/review.json',
        'DOC033': 'review/expanded-batch3/review.json',
    }
    docs, batches, findings = [], [], []
    for n, review in reviews.items():
        batch_docs = []
        for entry in review['documents']:
            doc = entry['document_id']
            record = selected[doc]
            model = load(record['json'])
            goal_ids = {g['goal_id'] for g in model['goals']}
            group_ids = {g['group_id'] for g in model['refinement_groups']}
            reviewed_goals = set(entry['reviewed_goal_ids'])
            reviewed_groups = set(entry['reviewed_group_ids'])
            assert reviewed_goals <= goal_ids, doc
            assert reviewed_groups == group_ids, (doc, reviewed_groups, group_ids)
            if doc in FULL[n]:
                assert reviewed_goals == goal_ids, doc
            before_path = relative(entry.get('model_path', entry.get('delivery_path', '')))
            assert before_path and sha(before_path) == entry['model_sha256'], doc
            final_sha = sha(record['json'])
            binding = 'same_actual_model_bytes'
            followup = None
            if final_sha != entry['model_sha256']:
                followup = followups[doc]
                # Followups retain explicit final byte hashes, affected-object checks and equality scope.
                assert final_sha in json.dumps(load(followup)), (doc, 'missing selected hash in independent followup')
                binding = 'initial_full_scope_plus_independent_affected_object_recheck_and_unchanged_object_comparison'
            result = dict(
                document_id=doc, batch=n, full_goal_review=doc in FULL[n],
                initial_model_path=before_path, initial_model_sha256=entry['model_sha256'],
                selected_model_path=record['json'], selected_model_sha256=final_sha,
                selected_binding=binding, independent_followup=followup,
                reviewed_goal_ids=sorted(reviewed_goals), reviewed_group_ids=sorted(reviewed_groups),
                unreviewed_goal_ids=sorted(goal_ids - reviewed_goals),
                total_goals=len(goal_ids), total_groups=len(group_ids),
            )
            docs.append(result)
            batch_docs.append(result)
        batches.append(dict(
            batch=n, report=f'review/expanded-batch{n}/report.md',
            review=f'review/expanded-batch{n}/review.json',
            review_sha256=sha(f'review/expanded-batch{n}/review.json'),
            documents=len(batch_docs), reviewed_goals=sum(len(d['reviewed_goal_ids']) for d in batch_docs),
            reviewed_groups=sum(len(d['reviewed_group_ids']) for d in batch_docs),
            full_goal_documents=sorted(FULL[n]),
            full_goal_count=sum(d['total_goals'] for d in batch_docs if d['full_goal_review']),
        ))
        for item in review['findings']:
            f = dict(item)
            f['original_report'] = f'review/expanded-batch{n}/review.json'
            if f['finding_id'] in {'ER-B1-001', 'ER-B2-001'}:
                f['initial_status'] = f['status']
                f['effective_status'] = 'resolved_in_separate_revision_independently_rechecked'
                f['effective_followup'] = followups['DOC003' if n == 1 else 'DOC025']
            else:
                f['effective_status'] = f['status']
            findings.append(f)
    assert {d['document_id'] for d in docs} == set(selected) - PILOT
    assert len(docs) == 31
    expanded_count = sum(len(d['reviewed_goal_ids']) for d in docs)
    expanded_groups = sum(len(d['reviewed_group_ids']) for d in docs)
    full_count = sum(d['total_goals'] for d in docs if d['full_goal_review'])
    pilot_review = load('review/pilot-review.json')
    for doc in PILOT:
        model = load(selected[doc]['json'])
        reviewed = {g['goal_id'] for g in pilot_review['goal_reviews'] if g['branch'] == 'revised' and g['document'] == doc}
        assert reviewed == {g['goal_id'] for g in model['goals']}, doc
        reviewed_groups = {g['group_id'] for g in pilot_review['group_reviews'] if g['branch'] == 'revised' and g['document'] == doc}
        assert reviewed_groups == {g['group_id'] for g in model['refinement_groups']}, doc
    # The frozen inspect tool binds canonical JSON; the revision ledger binds file bytes.
    pilot_final = load(selected['DOC010']['json'])
    canonical = json.dumps(pilot_final, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')
    assert hashlib.sha256(canonical).hexdigest() == load('review/pilot-v2-followup.json')['independent_inspection']['model']['sha256']
    assert sha(selected['DOC010']['json']) == load('revised/DOC010/v2/revision-record.json')['current_model']['sha256']
    revised_goals = sum(r['goals'] for r in selected.values())
    revised_groups = sum(r['groups'] for r in selected.values())
    active_groups = sum(r['active_groups'] for r in selected.values())
    pilot_goals = sum(selected[d]['goals'] for d in PILOT)
    pilot_groups = sum(selected[d]['groups'] for d in PILOT)
    assert expanded_groups + pilot_groups == revised_groups
    readiness = Counter(d['readiness'] for d in audit['deliveries'] if d['arm'] == 'revised')
    support = sum((Counter(r['support']) for r in selected.values()), Counter())
    totals = dict(
        revised_documents=34, revised_goals=revised_goals, revised_groups=revised_groups,
        supported_complete_groups=active_groups, proposed_partial_groups=revised_groups-active_groups,
        author_support_labels=dict(support), engineering_readiness=dict(readiness),
        expanded_documents=31, expanded_independently_reviewed_goals=expanded_count,
        expanded_independently_reviewed_groups=expanded_groups,
        expanded_full_goal_documents=sum(len(x) for x in FULL.values()), expanded_full_goal_count=full_count,
        revised_independently_reviewed_goals=expanded_count+pilot_goals,
        revised_independently_reviewed_groups=expanded_groups+pilot_groups,
        revised_full_goal_documents=sum(len(x) for x in FULL.values())+len(PILOT),
        revised_full_goal_count=full_count+pilot_goals,
        revised_goals_not_independently_reviewed=revised_goals-expanded_count-pilot_goals,
        confirmed_material_findings_in_expansion=1, open_confirmed_material_findings=0,
    )
    record = dict(
        record_type='consolidated_independent_context_review', completed_at_utc=datetime.now(timezone.utc).isoformat(),
        status='complete_with_one_local_unresolved_candidate', totals=totals, batches=batches,
        documents=docs, findings=findings,
        pilot=dict(report='review/pilot-comparison.md', review='review/pilot-review.json',
                   followup='review/pilot-v2-followup.json', baseline_goals=27, baseline_groups=7,
                   revised_goals=pilot_goals, revised_groups=pilot_groups,
                   DOC010_file_sha256=sha(selected['DOC010']['json']),
                   DOC010_inspect_canonical_json_sha256=hashlib.sha256(canonical).hexdigest(),
                   hash_note='File-byte hash and frozen-tool canonical-JSON hash have different definitions; both checked'),
        remaining_blockers=[dict(document_id='DOC036', goal_id='DOC036-G17',
            scope='anonymous-posting intention only; no dependent established group',
            resolution='genuine stakeholder clarification; no fabricated answer')],
        limits=[
            'Purposive review sample, not random; only three pilot documents have both skill arms.',
            'Separate model contexts, not human review, not fully blinded, not external validation or formal proof.',
            'Unknown exact model IDs, sampling controls, budgets and token costs; interrupted run may change models.',
            'Full source reading alone does not imply all output goals were independently reviewed.',
            'Counts and support labels are not accuracy, recall, causal effects or human acceptance.',
            'Core inspection independent_semantic/formal_proof remains not_run; this is an additional bound review layer.',
        ], human='pending', formal_proof='not_run',
    )
    save('review/expanded-review.json', record)
    lines = [
        '# 扩展处理独立复核汇总', '',
        '31篇扩展结果的计划复核已完成。初审确认的一项实质语义偏差（DOC015-G12）已另存修订，并由独立复核者确认修复；四项低严重度表达或证据呈现建议也已处理。当前未遗留已确认的实质语义偏差。DOC036-G17的匿名发帖意图仍待真实澄清，保留支持不足候选，不虚构答案。', '',
        '这是与生成方分离上下文的模型复核，人工审核仍pending，形式证明not_run。以下范围和数字只描述实际覆盖。', '',
        '## 覆盖与版本绑定', '',
        '| 批次 | 文档 | 全目标样本篇数 / 目标 | 独立检查的不同目标 | 全部精化组 | 原报告 |',
        '|---|---:|---:|---:|---:|---|',
    ]
    for row in batches:
        n = row['batch']
        lines.append(f"| {n} | {row['documents']} | {len(FULL[n])} / {row['full_goal_count']} | {row['reviewed_goals']} | {row['reviewed_groups']} | [批{n}报告](expanded-batch{n}/report.md) |")
    lines += [
        f'| 扩展合计 | 31 | 11 / {full_count} | {expanded_count} | {expanded_groups} | [逐对象记录](expanded-review.json) |', '',
        f'全目标样本为{ "、".join(sorted(set().union(*FULL.values()))) }。另外{expanded_count-full_count}个目标仅按精化端点或明确追加风险核查。DOC024无组且未抽中全目标复核，不计独立目标覆盖。读取过全文不等于审查过该篇全部目标。', '',
        f'加上三篇试运行，新版共{expanded_count+pilot_goals}个不同目标、全部{revised_groups}组有独立复核记录；14篇的{full_count+pilot_goals}目标属于全目标样本。尚有{revised_goals-expanded_count-pilot_goals}个目标未作独立逐目标复核，只能依赖生成方自检和工程检查，不宣称559目标全部已复核。', '',
        '初审与当前选择版本的路径、SHA-256、目标ID集合、未审ID集合和补查位置逐篇保存在[汇总JSON](expanded-review.json)。改版只重核受影响对象，并核验其余对象不变；不能把补查说成重做整篇独立语义审查。', '',
        '## 发现与最终处置', '',
        '| 编号 | 性质与原问题 | 当前处置 |', '|---|---|---|',
        '| ER-B3-001 | 中等、确证语义偏差：DOC015将内容分类与质量评价中的反馈/评分合并 | v3将G12收窄为质量判断；按内容分类保留在G02推荐上下文，独立重核解决 |',
        '| ER-B1-001 | 低严重度依据呈现缺口：DOC003-G14绑定片段缺少“心智负担”的直接出处，完整原文已有支持 | v2补T146上下文与T147连续回答，目标含义不变；[独立补查](expanded-batch1/followup.md)通过 |',
        '| ER-B2-001 | 低严重度理由越界：DOC025-F1父目标只含探索/申请，理由误含招聘回应 | v2删除回应理由与假设，组仍proposed/partial；[批3代补查](expanded-batch2/followup-by-batch3.md)确认 |',
        '| ER-B3-002 | 低严重度阈值表达歧义：DOC033“20分钟以上” | v2改为“超过20分钟”，独立重核解决 |',
        '| ER-B3-003 | 低严重度证据呈现缺口：DOC033-G17引文未覆盖超长广告烦恼 | 同一v2补T151/T155的连续依据及例外，独立重核解决 |',
        '| ER-B3-004 | DOC036-G17独立匿名发帖意图不明确 | 全77轮回查后继续insufficient/pending，局部待确认，不计已确认错误目标 |', '',
        '问题条目数不等于错误目标数。候选遗漏风险、正确边界案例、领域未知与确证偏差分别保留在原报告；未确认的覆盖风险没有被改写成真实漏提，也未为增加节点而强行补目标。', '',
        '批2补查遇到模型容量限制后，实际由批3独立复核者承接；[交接补查记录](expanded-batch2/followup-by-batch3.json)明确身份和有限范围，未冒充原复核者完成。', '',
        '## 精化与待确认边界', '',
        '扩展35组中仅DOC017的限定双条件合取与DOC027的限定直接读取场景被保留为supported/complete；连同试运行DOC023的同一人选资格合取，全量新版为3/44组。成立结论都依赖明示范围和假设，不保证完整理想门户、全部工作时间缩短或最终内推成功。其余41组继续proposed/partial；候选组存在本身不算错误成立精化，也不要求强造完整树。', '',
        'DOC036-G17不能从“免登录浏览”、私密发帖或采访者并列归纳后的简短同意中独立确认匿名发帖意图。核心readiness因此标blocked；真实缺口仅该候选，未否定其余16目标，也没有依赖该候选的成立组。需未来真实反馈单独澄清。', '',
        '## 解释限制', '',
        '11篇是目的抽样，其中DOC012和DOC015为风险追加样本；这不是随机、未知测试集或总体准确率估计。三篇修改前后比较使用已接触的开发案例；多数差异为拆分和显式化。模型标识、采样、预算和成本未知，执行中断及后续模型切换进一步限制归因。不能把559目标或3个成立组当成技能质量提升幅度。', '',
        '原文引文位置核验与语义支持不同。来源未重新核听录音，领域事实未作外部验证，HTML/SVG未做浏览器交互或视觉验收。核心inspection的independent_semantic/formal_proof保留not_run；本报告和各子报告是另存的额外复核层。所有人工状态仍pending。', '',
        '[返回结果目录](../README.md) · [处理总结](../处理总结.md) · [试运行对照](pilot-comparison.md)',
    ]
    (OUT / 'review/expanded-review.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    inventory = load('_run/source-inventory.json')
    summary = [
        '# 同源数据处理总结', '',
        '本轮已完成用户指定source目录中DOC003—DOC036共34篇资料的新技能处理，全部新内容保存在output1。先对三篇做修改前后同源试运行，复核达门槛后处理其余31篇；原始输入、历史输出、项目skills及两套技能快照均未因本轮处理被覆盖。', '',
        '## 交付内容', '',
        f'输入共{sum(r["turns"] for r in inventory)}轮、{sum(r["characters"] for r in inventory):,}字符。新版交付{revised_goals}个目标、{revised_groups}个精化组；其中{active_groups}组在限定范围/假设内为supported/complete，{revised_groups-active_groups}组仍为proposed/partial。每篇均提供HTML审核入口、Markdown、JSON，以及原文/提取/支持判断/建模决策附件和实际运行记录。', '',
        '| 入口 | 用途 |', '|---|---|',
        '| [结果目录](README.md) / [网页入口](index.html) | 逐篇查看当前选择的完整交付与状态 |',
        '| [三篇修改前后对照](review/pilot-comparison.md) | 原始冻结v1的语义对齐、依据与局部问题 |',
        '| [DOC010修订补查](review/pilot-v2-followup.md) | 原比较保留，当前选用v2的“雨情”措辞修订 |',
        '| [扩展独立复核汇总](review/expanded-review.md) | 复核覆盖、确证问题修复与未知项 |',
        '| [工程核验]( _run/final-verification.json) | 原始输入、技能及实际交付绑定检查 |'.replace(']( ', ']('),
        '| [版本记录](_run/revision-ledger.json) | 旧版保留、前后哈希与失败尝试记录 |', '',
        '生成方支持标签为direct 461、inferred 97、insufficient 1；这些是逐目标编制判断，不是独立准确率。33篇核心readiness为reviewable，DOC036因一个局部待确认候选为blocked；所有结果仍待人工采纳。', '',
        '## 三篇比较得到的结论', '',
        '| 文档 | 修改前目标 / 组 | 修改后目标 / 组 |', '|---|---:|---:|',
        '| DOC010 | 10 / 2 | 13 / 3 |', '| DOC023 | 8 / 3 | 13 / 4 |', '| DOC031 | 9 / 2 | 11 / 2 |', '| 合计 | 27 / 7 | 37 / 9 |', '',
        '两分支由互不读取对方结果的独立生成上下文处理同源资料；复核者先读原文，再读冻结结果。两版64目标及16组均已独立核查。新版更明确呈现偏好/建议语气、维持已有能力、推断依据及条件；多数目标数差异来自拆分或显式化，基线也保留主要意图和例外。未发现新版未处置的严重无依据强化或错误成立精化，允许扩展。', '',
        '原v1比较里的DOC010“雨势变化”存在非阻断歧义；当前v2收窄为雨情变化、开始或停止，并已独立补查。旧版分支与原v1比较完整保留，不为改善结论而改写。只有三篇做双分支比较，其余31篇只做新版处理，不能称34篇全部完成修改前后实验。', '',
        '## 独立复核与修订', '',
        f'扩展范围为11篇{full_count}目标全量独立复核，加{expanded_count-full_count}个组端点/风险目标，共{expanded_count}个不同目标及全部{expanded_groups}组。连同试运行，新版共{expanded_count+pilot_goals}目标有独立复核，全部{revised_groups}组已复核；其中14篇{full_count+pilot_goals}目标属于全目标样本，另{revised_goals-expanded_count-pilot_goals}目标未作独立逐目标复核。具体ID和版本绑定见[机器汇总](review/expanded-review.json)。', '',
        '扩展初审确证一项实质语义问题：DOC015将按内容分类与质量评价中的反馈/评分交叉合并；已在v3分清G02和G12的适用范围并独立重核。DOC003补心智负担直接出处、DOC025收窄精化理由、DOC033消歧时长阈值并补长广告依据，均另存版本后独立补查。没有为清除问题删除有依据意图或伪造用户反馈。', '',
        'DOC036-G17仍是唯一支持不足候选。完整77轮原文未找到独立明确的匿名发帖意图，保留待确认；免登录浏览、私密发帖和匿名发帖分别处理。当前源资料范围内的处理与计划复核已完成，实际采纳该候选需未来真实澄清。', '',
        '## 可核验性与限制', '',
        '最终工程核验真实检查34篇原始JSON/TXT、轮次到全文的投影、冻结技能与当前项目技能哈希、六份原试运行v1冻结包，以及37份当前选择交付（34新版、3基线）的清单、输入和实际模型绑定；结果passed且无工程错误。这不证明语义完备。运行配置、实际命令和失败记录保留在_run及各包中。', '',
        '外层v2/v3用于区分助手修订包；冻结工具的内部model.version仍可能为v1、parent=null。引用时以完整路径和SHA-256识别版本；未伪造人工反馈来递增内部版本。独立补查和未改对象比较另有绑定记录，原版不覆盖。', '',
        '精确模型标识、采样参数、预算、token消耗和成本未知，执行跨日且经历额度中断和后续模型切换。三篇是已接触开发案例，未随机重复；扩展是目的抽样复核，不计算准确率/召回率或因果提升幅度。独立模型上下文不等于外部人审；录音未核听，领域事实未外部验证，HTML/SVG未做浏览器视觉/交互验收，形式证明未运行。', '',
        '核心inspection的independent_semantic/formal_proof保持not_run；单独的模型语义复核报告提供额外依据。人工审核保持pending。', '',
        '实际来源：datasets/processed/goalforge-v1/source；处理日期：2026-10-23至2026-10-24（Asia/Shanghai）。',
    ]
    (OUT / '处理总结.md').write_text('\n'.join(summary) + '\n', encoding='utf-8')
    print(json.dumps(totals, ensure_ascii=False))


if __name__ == '__main__':
    main()
