import json
from pathlib import Path
p=Path('output1/revised/_authoring/DOC011.json'); d=json.loads(p.read_text(encoding='utf-8'))
d['goals'][0]['evidence'][1]['quote']='We had a very difficult time finding work session like creating work sessions to collaborate with each other in person.'
d['author_review']+='\n修订记录：v1组装前引文绑定失败（T101句首we应为原文We，大小写不匹配）。保留原作者输入；v2仅按全文重核纠正为真实连续子串，G01含义和支持范围重核不变，全部组再次检查。没有伪造人工反馈。\n'
Path('output1/revised/_authoring/DOC011-v2.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
Path('output1/revised/_authoring/DOC011-v1-failure.json').write_text(json.dumps({'attempt':'v1','phase':'evidence binding before output directory creation','error':'DOC011:T101 quote not exact due initial we/We case','preserved_input':'DOC011.json','next_revision':'v2','reason':'Correct source quotation after full-context recheck; semantic statement unchanged'},ensure_ascii=False,indent=2),encoding='utf-8')
