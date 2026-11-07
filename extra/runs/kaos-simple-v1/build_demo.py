"""Controlled developer example, not user approval or semantic accuracy evaluation."""
import json
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'tests'))
from test_kaos_model import fixture
import kaos_model as k

BASE = Path(__file__).resolve().parent
commands=[]
def run(*args):
    result=subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,text=True,capture_output=True,encoding='utf-8')
    commands.append(dict(arguments=list(map(str,args)),returncode=result.returncode,stdout=result.stdout,stderr=result.stderr))
    if result.returncode:
        raise RuntimeError(result.stderr)


def main():
    global BASE
    parser=argparse.ArgumentParser()
    parser.add_argument('--run-name')
    args=parser.parse_args()
    if args.run_name:
        if not args.run_name.replace('-','').isalnum():raise ValueError('Use a simple run name')
        BASE=BASE/args.run_name
        BASE.mkdir(exist_ok=False)
    inputs=BASE/'inputs'
    inputs.mkdir(exist_ok=True)
    data,source,judgments,decisions=fixture()
    for name,value in [('extraction.json',data),('judgments.json',judgments),('kaos-decisions.json',decisions)]:
        p=inputs/name
        if p.exists():raise ValueError('Preserve earlier demo: '+str(p))
        p.write_bytes(k.encode(value))
    (inputs/'source.md').write_bytes(source)
    tool=ROOT/'skills/goal-model-building/scripts/kaos_model.py'
    run(ROOT/'skills/goal-extraction/scripts/render_review.py',inputs/'extraction.json',BASE/'目标清单.md')
    run(ROOT/'skills/goal-tracing/scripts/trace_candidates.py',inputs/'extraction.json',BASE/'tracing','--source',inputs/'source.md','--judgments',inputs/'judgments.json')
    run(tool,'assemble',inputs/'extraction.json',inputs/'judgments.json',inputs/'source.md',inputs/'kaos-decisions.json',BASE/'assembled')
    run(tool,'inspect',BASE/'assembled/model-input.json',BASE/'inspection.json')
    run(tool,'finalize',BASE/'assembled/model-input.json',BASE/'inspection.json',BASE/'delivery')
    model=k.load(BASE/'delivery/goal-model.json')
    simulated=dict(schema_version=k.FEEDBACK,model=k.binding(model),status='submitted',form_drafts={},note='工程模拟反馈，不是用户意见或人工认可。',
                   entries=[dict(target_type='group',target_id='F2',decision='modify',comment='工程模拟：请更清楚地解释为什么邮件送达可以满足上层目标。')])
    (inputs/'simulated-feedback.json').write_bytes(k.encode(simulated))
    run(tool,'feedback',BASE/'delivery/goal-model.json',inputs/'simulated-feedback.json',BASE/'feedback-simulation')
    decisions['groups'][1]['rationale']='本材料明确允许邮件或短信任一种渠道完成送达；因此邮件回执送达是一套单成员的完整替代方案。仅适用于本材料约定的有效回执。'
    decisions['feedback_dispositions']=[dict(target_type='group',target_id='F2',status='addressed',reason='依据原文渠道说明重评，已补充该方案足以满足送达目标的解释；仍需人工审核。')]
    (inputs/'reassessed-kaos-decisions.json').write_bytes(k.encode(decisions))
    run(tool,'assemble',inputs/'extraction.json',inputs/'judgments.json',inputs/'source.md',inputs/'reassessed-kaos-decisions.json',BASE/'revised',
        '--previous',BASE/'delivery/goal-model.json','--feedback',inputs/'simulated-feedback.json')
    run(tool,'inspect',BASE/'revised/model-input.json',BASE/'revised-inspection.json')
    run(tool,'finalize',BASE/'revised/model-input.json',BASE/'revised-inspection.json',BASE/'delivery-revised')
    (BASE/'commands.json').write_bytes(k.encode(commands))
    (BASE/'verification.json').write_bytes(k.encode(dict(kind='controlled_engineering_example',cli_calls=len(commands),source='synthetic',human='pending',model_api_calls=0,
             original_version=model['version'],revised_version=k.load(BASE/'delivery-revised/goal-model.json')['version'],
             initial_report=k.load(BASE/'inspection.json'),revised_report=k.load(BASE/'revised-inspection.json'))))
    print('Completed controlled demo and feedback revision: '+str(len(commands))+' CLI calls')


if __name__=='__main__':main()
