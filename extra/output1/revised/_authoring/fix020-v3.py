import json
from pathlib import Path
d=json.loads(Path('output1/revised/_authoring/DOC020-v2.json').read_text(encoding='utf-8'))
d['goals'][8]['evidence'][1]['quote']='They could see the new email and old email, but they will see the new one. And if they want, they could see the editing history.'
d['author_review']+='\nv2在同轮另一引文句首they/They未匹配，亦未建立模型目录；v3保留v1/v2输入并更正该引文，逐项全文证据检查无其他不唯一/未命中；G09与F01语义再次核验不变。\n'
Path('output1/revised/_authoring/DOC020-v3.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
Path('output1/revised/_authoring/DOC020-v2-failure.json').write_text(json.dumps({'attempt':'v2','phase':'evidence binding before output directory creation','error':'DOC020:T029 context quote they/They case','preserved_input':'DOC020-v2.json','next_revision':'v3','reason':'Correct continuous context quotation; G09 rechecked, no semantic change'},ensure_ascii=False,indent=2),encoding='utf-8')
