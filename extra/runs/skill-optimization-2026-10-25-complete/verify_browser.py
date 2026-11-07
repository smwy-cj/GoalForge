"""Exercise real packaged v1/v2 pages in an installed headless browser.

Synthetic author judgments are for UI/contract validation only.
"""
import html
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUN = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT/'tests'))
from test_kaos_relations import fixture
from test_kaos_model import fixture as legacy_fixture, k


def create_demo(version):
    output = RUN/'browser'/('v'+str(version))
    if (output/'delivery/goal-model.json').exists():
        k.inspect(k.load(output/'delivery/goal-model.json'),output/'delivery')
        return output
    data, source, judgments, decisions = fixture() if version == 2 else legacy_fixture()
    if version == 2:
        for identifier, kind, status in [('R2','operationalization','proposed'),('R3','specialization','rejected'),('R4','precedes','proposed')]:
            r = dict(decisions['relations'][0], relation_id=identifier, type=kind, status=status)
            r['rationale'] = '合成UI测试：验证类型、状态及审核显示，不作为真实关系准确率。'
            decisions['relations'].append(r)
    raw = [k.encode(data), k.encode(judgments), source, k.encode(decisions)]
    model = k.build(*raw)
    base = k.fresh(output/'assembled')
    for name, content in zip(['extraction.json','judgments.json','source.txt','kaos-decisions.json'],raw):
        target = base/'attachments'/name; target.parent.mkdir(parents=True,exist_ok=True); target.write_bytes(content)
        model['input_artifacts'].append(dict(path='attachments/'+name,sha256=k.digest(content)))
    (base/'model-input.json').write_bytes(k.encode(model))
    k.package(model,base,output/'delivery',with_svg=True)
    return output


HARNESS = r"""
<script>
(async()=>{
const el=id=>document.getElementById(id),checks=[];
const assert=(condition,name)=>{if(!condition)throw new Error(name);checks.push(name);};
try{
 const p=JSON.parse(el('payload').textContent),v2=p.model.schema_version==='goalforge-kaos-2';
 assert(document.querySelectorAll('#dagCanvas [data-goal]').length===p.model.goals.length,'all goals rendered once');
 assert(document.querySelectorAll('#dagCanvas [data-relation]').length===0,'auxiliary relations excluded from established DAG');
 if(v2){
  assert(!el('relationsView').hidden,'v2 relation view offered');el('relationsView').click();
  assert(!el('relationsPanel').hidden&&el('dagCanvas').hidden,'relation view separate from DAG');
  assert(document.querySelectorAll('.relationCard').length===4,'all four relation records displayed');
  assert(document.querySelector('.relationCard.proposed')&&document.querySelector('.relationCard.rejected'),'proposed and rejected states visible');
  document.querySelector('[data-relation-id="R1"] > button').click();
  assert(el('detail').textContent.includes('不代表充分精化'),'relation detail distinguishes sufficiency');
  el('detail').querySelector('input[value="modify"]').click();el('opinion').value='合成测试：请核对联系范围';el('opinion').dispatchEvent(new Event('input'));
  el('exportFeedback').click();assert(el('saveFile').disabled,'unfinished relation form blocks submission');el('closeExport').click();
  el('detail').querySelector('form').requestSubmit();el('exportFeedback').click();
  const packet=JSON.parse(el('exportText').value);
  assert(packet.schema_version==='goalforge-simple-feedback-2'&&packet.status==='submitted','v2 feedback schema and submission');
  assert(packet.entries.length===1&&packet.entries[0].target_type==='relation'&&packet.entries[0].target_id==='R1','relation opinion not goal/group opinion');
  assert(!el('saveFile').disabled,'saved opinion can export');el('closeExport').click();
  el('modelFiles').click();el('exportType').value='relations-svg';el('exportType').dispatchEvent(new Event('change'));
  assert(el('exportText').value===p.relations_svg,'relation SVG export matches frozen payload');el('closeExport').click();
  el('importButton').click();
  const old={...packet,schema_version:'goalforge-simple-feedback-1'},dt=new DataTransfer();dt.items.add(new File([JSON.stringify(old)],'old.json',{type:'application/json'}));el('importFile').files=dt.files;await el('importFile').onchange();
  assert(el('confirmImport').disabled,'v1 feedback rejected for v2 model');el('closeImport').click();
  el('relationsView').click();
 }else{
  assert(el('relationsView').hidden,'legacy v1 does not offer relation view');el('reviewFirst').click();
  el('detail').querySelector('input[value="accept"]').click();el('detail').querySelector('form').requestSubmit();el('exportFeedback').click();
  assert(JSON.parse(el('exportText').value).schema_version==='goalforge-simple-feedback-1','legacy feedback stays v1');el('closeExport').click();
 }
 assert(!(window.uiErrors||[]).length,'no browser JavaScript errors');
 const result=document.createElement('pre');result.id='ui-test-result';result.textContent=JSON.stringify({status:'passed',checks,errors:window.uiErrors||[]});document.body.appendChild(result);
}catch(e){const result=document.createElement('pre');result.id='ui-test-result';result.textContent=JSON.stringify({status:'failed',checks,error:e.message,errors:window.uiErrors||[]});document.body.appendChild(result);}
})();
</script>
"""


def main():
    browsers = [Path('C:/Program Files/Google/Chrome/Application/chrome.exe'),Path('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe')]
    browser = next((p for p in browsers if p.exists()),None)
    if browser is None: raise RuntimeError('No installed browser; browser verification not run')
    reports=[]
    for version in (1,2):
        output=create_demo(version)
        attempts = output/'attempts'; attempts.mkdir(exist_ok=True)
        attempt = attempts/str(len(list(attempts.iterdir()))+1).zfill(3); attempt.mkdir()
        page=(output/'delivery/goal-model.html').read_text(encoding='utf-8')
        page=page.replace('<script id="payload"','<script>window.uiErrors=[];window.addEventListener("error",e=>window.uiErrors.push(e.message));</script><script id="payload"',1)
        page=page.replace('</body>',HARNESS+'</body>')
        test_page=attempt/'ui-check.html';test_page.write_text(page,encoding='utf-8')
        with tempfile.TemporaryDirectory(prefix='goalforge-browser-') as profile:
            command=[str(browser),'--headless=new','--disable-gpu','--no-first-run','--no-default-browser-check',
                     '--allow-file-access-from-files','--user-data-dir='+profile,'--virtual-time-budget=4000',
                     '--window-size=1500,1100','--screenshot='+str(attempt/'screenshot.png'),'--dump-dom',test_page.as_uri()]
            result=subprocess.run(command,capture_output=True,timeout=60)
            (attempt/'browser-stderr.log').write_bytes(result.stderr)
            (attempt/'dom.html').write_bytes(result.stdout)
            match=re.search(r'<pre id="ui-test-result">(.*?)</pre>',result.stdout.decode('utf-8',errors='replace'),re.S)
            if not match: raise RuntimeError('Browser did not produce a UI result: '+str(attempt/'browser-stderr.log'))
            report=json.loads(html.unescape(match.group(1)));report.update(version=version,browser=str(browser),exit_code=result.returncode)
            report['attempt_path'] = str(attempt.relative_to(RUN))
            (attempt/'result.json').write_bytes(k.encode(report));reports.append(report)
            if report['status']!='passed': raise RuntimeError(str(report))
    (RUN/'browser-verification.json').write_bytes(k.encode(dict(status='passed',runs=reports)))
    print(json.dumps(dict(status='passed',checks=sum(len(r['checks']) for r in reports)),ensure_ascii=False))


if __name__=='__main__':main()
