"""Build a local navigation index from actual completed delivery files."""
import html
import json
from collections import Counter
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads(path.read_bytes().decode('utf-8-sig'))


def main():
    config = load(OUT/'_run/run-config.json')
    inventory = load(OUT/'_run/source-inventory.json')
    records = []
    for item in inventory:
        doc = item['document_id']
        for arm in ('baseline', 'revised'):
            choices = []
            base = OUT/arm/doc
            if base.exists():
                for path in base.rglob('goal-model.json'):
                    if 'attachments' in path.parts or not path.with_suffix('.html').exists():
                        continue
                    model = load(path)
                    if model.get('scope', {}).get('document_id') != doc:
                        continue
                    choices.append(path)
            if not choices:
                continue
            path = max(choices, key=lambda p:p.stat().st_mtime_ns)
            model = load(path)
            record = dict(document_id=doc, arm=arm, goals=len(model['goals']),
                          groups=len(model['refinement_groups']),
                          active_groups=sum(g['status']=='supported' and g['completeness']=='complete' for g in model['refinement_groups']),
                          support=dict(Counter(g['support']['label'] for g in model['goals'])),
                          issues=len(model['issues']), blocking_issues=sum(bool(i['blocking']) for i in model['issues']),
                          human=model['review']['status'], json=path.relative_to(OUT).as_posix(),
                          html=path.with_suffix('.html').relative_to(OUT).as_posix(),
                          markdown=path.with_suffix('.md').relative_to(OUT).as_posix(),
                          other_deliveries=[p.relative_to(OUT).as_posix() for p in choices if p!=path])
            records.append(record)
    selected = {(r['arm'],r['document_id']):r for r in records}
    summary = dict(prepared=len(inventory), baseline_delivered=sum(r['arm']=='baseline' for r in records),
                   revised_delivered=sum(r['arm']=='revised' for r in records),
                   selection='latest modification time among complete delivery JSON+HTML pairs; earlier versions retained',
                   documents=records)
    (OUT/'_run/delivery-index.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    blocked=[r for r in records if r['arm']=='revised' and r['blocking_issues']]
    md=['# 同源资料处理结果', '', f"已核验 {len(inventory)} 篇输入；修改后已交付 {summary['revised_delivered']} 篇，修改前比较分支已交付 {summary['baseline_delivered']} 篇。", '',
        '生成结果保持待人工审核。目标数、精化组数不是质量分数；工程通过与独立上下文复核分别报告。', '',
        '## 总结与记录', '',
        '- [运行口径](_run/evaluation-protocol.md)',
        '- [源文清单](_run/source-inventory.json)',
        '- [运行配置及技能快照](_run/run-config.json)', '']
    followup_summary=OUT/'review/remaining-20261025/summary.json'
    if followup_summary.exists():
        followup=load(followup_summary)
        md += ['', f'2026-10-25补审已完成：新版{followup["coverage"]["total_selected_goals"]}个目标及全部精化组均有独立模型上下文复核记录，人工仍待审。',
               '- [最新复核总结](review/remaining-20261025/复核总结.md)',
               '- [统一问题清单](review/remaining-20261025/统一问题清单.md)',
               '下列初次处理总结及原比较报告保留2026-10-24当时的范围和版本记录。', '']
    for name in ['处理总结.md','review/pilot-comparison.md','review/pilot-source-criteria.md','review/pilot-gate.md','review/pilot-v2-followup.md','review/expanded-review.md']:
        if (OUT/name).exists():
            md.append(f'- [{Path(name).stem}]({name})')
    if (OUT/'review/pilot-v2-followup.md').exists():
        md += ['', '试运行原始比较保留冻结 v1；DOC010 的“雨情”局部修订见 v2 补查。下列入口选择各篇最新完整交付；外层修订版本与工具内部模型版本的限制见补查说明。']
    if blocked:
        md += ['', '待确认：'+ '、'.join(r['document_id'] for r in blocked)+' 含支持不足候选。DOC036-G17 的匿名发帖意图需真实澄清；该局部未决项保留，不升级为已确认要求。']
    md += ['', '## 修改后结果', '', '| 文档 | 目标 | 精化组（成立/全部） | 当前状态 | 审核入口 | 机器结果 |', '|---|---:|---:|---|---|---|']
    for item in inventory:
        doc=item['document_id']; r=selected.get(('revised',doc))
        if r:
            state='局部候选待确认' if r['blocking_issues'] else '可进入人工审核'
            md.append(f"| {doc} | {r['goals']} | {r['active_groups']}/{r['groups']} | {state} | [打开模型]({r['html']}) · [文字版]({r['markdown']}) | [JSON]({r['json']}) |")
        else:
            md.append(f'| {doc} | — | — | 输入已准备，尚未交付 | — | — |')
    md += ['', '## 修改前比较分支', '', '| 文档 | 目标 | 精化组（成立/全部） | 结果 |', '|---|---:|---:|---|']
    for doc in config['pilot_documents']:
        r=selected.get(('baseline',doc))
        if r:
            md.append(f"| {doc} | {r['goals']} | {r['active_groups']}/{r['groups']} | [打开模型]({r['html']}) · [JSON]({r['json']}) |")
        else:
            md.append(f'| {doc} | — | — | 尚未交付 |')
    (OUT/'README.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
    cards=[]
    for item in inventory:
        doc=item['document_id']; r=selected.get(('revised',doc))
        if r:
            state='局部候选待确认' if r['blocking_issues'] else '待人工审核'
            cards.append(f'<article><h2>{doc}</h2><p>{r["goals"]} 项目标 · {r["active_groups"]} 组成立精化 · {state}</p><a href="{html.escape(r["html"],quote=True)}">打开目标模型</a> <a href="{html.escape(r["markdown"],quote=True)}">文字版</a></article>')
        else:
            cards.append(f'<article><h2>{doc}</h2><p>输入已核验，尚未交付</p></article>')
    page='<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>GoalForge 同源处理结果</title><style>body{font:16px/1.6 system-ui,sans-serif;background:#f5f6fa;color:#172334;margin:0;padding:32px;max-width:1100px;margin:auto}h1{font-size:28px}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}article{background:white;padding:20px;border:1px solid #dce2eb;border-radius:12px}h2{margin:0;font-size:20px}a{color:#1755a3;margin-right:12px}p{color:#4e5f73}</style><h1>同源资料处理结果</h1><p>修改后已交付 '+str(summary['revised_delivered'])+' / '+str(len(inventory))+' 篇。所有目标与层级保持待审核；数量不代表质量。</p><p><a href="README.md">完整目录与比较记录</a></p><main>'+''.join(cards)+'</main></html>'
    if followup_summary.exists():
        page=page.replace('<main>', '<p><a href="review/remaining-20261025/复核总结.md">最新复核总结</a><a href="review/remaining-20261025/统一问题清单.md">统一问题清单</a></p><main>')
    (OUT/'index.html').write_text(page,encoding='utf-8')
    print(json.dumps({k:summary[k] for k in ('prepared','baseline_delivered','revised_delivered')},ensure_ascii=False))


if __name__=='__main__':
    main()
