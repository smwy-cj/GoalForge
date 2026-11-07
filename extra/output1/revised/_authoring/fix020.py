import json
from pathlib import Path
p=Path('output1/revised/_authoring/DOC020.json');d=json.loads(p.read_text(encoding='utf-8'))
d['goals'][8]['evidence'][0]['quote']="It would probably be better if there's an function of editing the email instead of sending a new one."
d['author_review']+='\n修订记录：v1组装前T029引文句首it应为It，未精确绑定，保留原输入及失败日志。v2依据完整上下文改为真实连续原文，G09表述和整句支持重核不变；所有组重新核验后完整运行，不虚构人类feedback。\n'
Path('output1/revised/_authoring/DOC020-v2.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
Path('output1/revised/_authoring/DOC020-v1-failure.json').write_text(json.dumps({'attempt':'v1','phase':'evidence binding before output directory creation','error':'DOC020:T029 quote not exact due initial it/It case','preserved_input':'DOC020.json','next_revision':'v2','reason':'Correct quotation and re-evaluate G09 against full context; semantic statement unchanged'},ensure_ascii=False,indent=2),encoding='utf-8')
