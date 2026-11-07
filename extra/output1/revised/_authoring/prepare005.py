from pathlib import Path
p=Path('output1/revised/_authoring/batch1_helpers.py')
s=p.read_text(encoding='utf-8-sig').replace('def goal(n,statement,turn,quote,rationale,','def goal(n,support_label,statement,turn,quote,rationale,').replace("'label':'direct' if origin=='explicit' else 'inferred'","'label':support_label")
p.write_text(s,encoding='utf-8')
p=Path('output1/revised/_authoring/write_DOC005.py')
s=p.read_text(encoding='utf-8-sig')
labels={1:'direct',2:'direct',3:'direct',4:'direct',5:'direct',6:'direct',7:'direct',8:'direct',9:'direct',10:'direct',11:'direct',12:'direct',13:'inferred'}
for n,label in labels.items():s=s.replace(f'goal({n},',f"goal({n},'{label}',")
p.write_text(s,encoding='utf-8')
exec(s)
