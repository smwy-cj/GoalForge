from pathlib import Path
p=Path('output1/revised/_authoring/write_DOC009.py'); s=p.read_text(encoding='utf-8-sig')
labels={1:'direct',2:'direct',3:'direct',4:'direct',5:'direct',6:'direct',7:'direct',8:'direct',9:'inferred',10:'direct',11:'inferred',12:'direct',13:'direct',14:'direct',15:'inferred',16:'direct',17:'direct'}
for n,label in labels.items(): s=s.replace(f'goal({n},',f"goal({n},'{label}',")
p.write_text(s,encoding='utf-8'); exec(s)
