"""Select disjoint, deterministic calibration/evaluation pairs; print no labels."""
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path
RUN=Path(__file__).resolve().parent
rows=list(csv.DictReader((RUN/'inputs/paper/study1/data1/comps_final.csv').open(encoding='utf-8-sig',newline='')))
norm=lambda s:s.strip().upper().replace(' ','_')
valid={'REFINES','REFINED_BY','NONE','EQUIV'}
groups=defaultdict(list)
for i,r in enumerate(rows): groups[(r['G1'],r['G2'])].append((i,r))
consensus,single=[],[]
for key,entries in groups.items():
    if len(entries)!=1 or (key[1],key[0]) in groups: continue
    i,r=entries[0]
    a,b=norm(r['rater1']),norm(r['rater2'])
    if b not in valid:continue
    item={'csv_row_index_zero_based':i,'A':key[0],'B':key[1],'reference':b}
    if a==b and a in valid:consensus.append(item)
    elif not a:single.append(item)
key=lambda x:hashlib.sha256(('goalforge-20261022|'+x['A']+'|'+x['B']).encode()).hexdigest()
consensus.sort(key=key);single.sort(key=key)
selected=[]
for name,items in [('calibration',consensus[:12]),('consensus_evaluation',consensus[12:36]),('single_rater_evaluation',single[:24])]:
    for i,item in enumerate(items):selected.append({'case_id':f'{name}-{i+1:02}', 'split':name,**item})
(RUN/'relation-benchmark-key.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2),encoding='utf-8')
public=[{k:v for k,v in x.items() if k not in ['reference','csv_row_index_zero_based']} for x in selected]
(RUN/'relation-benchmark-input.json').write_text(json.dumps(public,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps([x for x in public if x['split']=='calibration'],ensure_ascii=False,indent=2))
print('eligible consensus',len(consensus),'eligible single',len(single),'selected',len(selected))
