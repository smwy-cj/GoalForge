"""Minimal synthetic package reproduction. Does not access any real generation branch.
Run with python -B; output files are preserved under this script's directory.
"""
import sys, json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT/'tests'))
from test_kaos_model import fixture,k
from trace_candidates import judgment_template

base=Path(__file__).resolve().parent
results=[]
for index,token in enumerate(['__CORE__','__UI__'],1):
    data,source,j,dec=fixture()
    data['limitations'].append('Literal marker: '+token)
    current=judgment_template(data,k.encode(data));current['judgments']=j['judgments'];j=current
    dec['input_binding']={'extraction_sha256':k.digest(k.encode(data)),'judgments_sha256':k.digest(k.encode(j))}
    raws=[k.encode(data),k.encode(j),source,k.encode(dec)]
    work=base/('case-'+str(index));work.mkdir(exist_ok=False)
    model=k.build(*raws)
    for name,raw in zip(['extraction.json','judgments.json','source.txt','kaos-decisions.json'],raws):
        p=work/'attachments'/name;p.parent.mkdir(exist_ok=True);p.write_bytes(raw)
        model['input_artifacts'].append({'path':'attachments/'+name,'sha256':k.digest(raw)})
    (work/'model-input.json').write_bytes(k.encode(model))
    report=k.inspect(model,work)
    (work/'inspection.json').write_bytes(k.encode(report))
    k.package(model,work,work/'delivery',report)
    page=(work/'delivery/goal-model.html').read_text('utf-8')
    payload=re.search(r'<script id="payload" type="application/json">(.*?)</script>',page,re.S).group(1)
    result={'marker':token,'inspection':report['structure'],'finalize':'completed','delivery':str((work/'delivery/goal-model.html').relative_to(base))}
    try:
        json.loads(payload);result['html_payload']='valid'
    except json.JSONDecodeError as error:
        result.update(html_payload='invalid',exception=str(error))
    results.append(result)
receipt={'defect':'package replaces template placeholders inside already injected JSON payload',
         'code':'skills/goal-model-building/scripts/kaos_model.py:607-609',
         'impact':'Browser startup JSON.parse fails despite passed inspection and completed package; target review/export UI does not initialize.',
         'results':results}
with (base/'placeholder-collision-result.json').open('x',encoding='utf-8',newline='\n') as f:
    json.dump(receipt,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps(receipt,ensure_ascii=False,indent=2))
