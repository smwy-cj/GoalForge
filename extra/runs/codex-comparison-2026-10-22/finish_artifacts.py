"""Create the executed companion notebook and a safe inline source receipt."""
import contextlib
import io
import json
from pathlib import Path

RUN=Path(__file__).resolve().parent
cells=[{'cell_type':'markdown','metadata':{},'source':[
 '# GoalForge 比对审计记录\n',
 '本笔记本读取本轮保存的结果并复算计数。原始核验及语义判断保存在同目录脚本和记录中。\n',
 '语义判断来自 Codex，不构成人工 Gold。工作目录为本笔记本目录或项目根目录。']}]
blocks=[
 "from pathlib import Path\nimport json\nrun_dir = Path.cwd()\nif not (run_dir / 'metrics.json').exists():\n    run_dir = run_dir / 'runs/codex-comparison-2026-10-22'\nmetrics = json.loads((run_dir / 'metrics.json').read_text(encoding='utf-8'))\nprint(json.dumps(metrics['counts'], ensure_ascii=False, indent=2))",
 "alignments = [json.loads(line) for line in (run_dir / 'goal-alignment.jsonl').read_text(encoding='utf-8').splitlines()]\nfrom collections import Counter\nprint(dict(Counter(row['correspondence'] for row in alignments)))\nprint('Reasonable inference originally labeled explicit:', metrics['reasonable_inference_labeled_explicit_in_original'])\nprint('Paper-only goals pending full-source adjudication:', metrics['paper_only_source_not_assessed'])",
 "for split in ['calibration', 'consensus_evaluation', 'single_rater_evaluation']:\n    result = metrics['relation_benchmark'][split]\n    print(split, 'total=', result['n'], 'resolved=', result['resolved'], 'correct=', result['correct'], 'abstained=', result['abstained'])\nprint('Validation:', json.loads((run_dir / 'validation.json').read_text(encoding='utf-8'))['passed'])",
]
namespace={}
for index,code in enumerate(blocks,1):
    captured=io.StringIO()
    with contextlib.redirect_stdout(captured):exec(compile(code,'audit-trail.ipynb','exec'),namespace)
    cells.append({'cell_type':'code','metadata':{},'execution_count':index,'source':code.splitlines(keepends=True),
                  'outputs':[{'output_type':'stream','name':'stdout','text':captured.getvalue().splitlines(keepends=True)}]})
notebook={'cells':cells,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},
                                  'language_info':{'name':'python'}},'nbformat':4,'nbformat_minor':5}
(RUN/'audit-trail.ipynb').write_text(json.dumps(notebook,ensure_ascii=False,indent=2),encoding='utf-8')

receipt={'schemaVersion':1,'items':[
 {'id':'comparison-coverage','title':'本轮比对范围','queries':[{'id':'frozen-counts','source':{
  'label':'GoalForge 首轮比对','files':[{'label':'metrics.json'},{'label':'validation.json'}],
  'metricDefinitions':[{'label':'比对范围','definition':'本轮对34篇产物中的398个本地目标建立语义候选对应，并对2263个本地关系对进行结构对应。'}],
  'caveats':['候选对应包含范围差异和部分重叠，不能当作准确率。']},
  'columns':[{'field':'metric','label':'项目'},{'field':'count','label':'数量'}],
  'rows':[{'metric':'访谈','count':34},{'metric':'本地目标','count':398},{'metric':'本地关系对','count':2263}]}]},
 {'id':'semantic-findings','title':'目标与精化的具体问题','queries':[{'id':'source-rechecks','source':{
  'label':'逐文档自动评审','files':[{'label':'DOC023.json'},{'label':'DOC013.json'},{'label':'source-based-relation-reviews.json'}],
  'caveats':['这些判断由Codex结合原文作出，不是独立人工标注。']},
  'summary':'DOC023出现200字符与200字的单位差异；DOC013增加了缺少源文支持的文件大小无限制；DOC010的降雨持续更新不足以实现极端天气告警。'}]},
 {'id':'remaining-scope','title':'结论的适用范围','queries':[{'id':'scope-limits','source':{
  'label':'评审覆盖记录','files':[{'label':'paper-goal-correspondence.jsonl'},{'label':'metrics.json'}],
  'caveats':['321个论文单方目标尚待完整源文裁决，未计为本地遗漏。','当前无法据此证明总体优于原论文。']},
  'summary':'全部本地目标已有首轮对应，论文单方目标的全文支持裁决尚未全部完成。'}]},
]}
(RUN/'reviewed-sources.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8')
summary=RUN/'summary.md'
summary.write_text(summary.read_text(encoding='utf-8').replace('REFINE\u200bS','REFINES'),encoding='utf-8')
print('Notebook executed; source receipt input saved.')
