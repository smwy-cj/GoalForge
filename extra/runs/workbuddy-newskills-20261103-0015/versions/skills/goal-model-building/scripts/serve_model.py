"""Loopback-only preview with verified, non-overwriting export receipts.

No upload to external services and no model changes. Every save is an explicit
page action, authenticated by a per-process token and exact same-origin check.
"""
import argparse
import html
import json
import secrets
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

import kaos_model as k


def save_export(model, root, body):
    require = k.require
    require(isinstance(body, dict), 'Invalid save request')
    kind, content = body.get('kind'), body.get('content')
    require(isinstance(content, str) and len(content.encode('utf-8')) <= 8*1024*1024, 'Invalid export size')
    if kind in {'feedback', 'draft'}:
        packet=json.loads(content)
        k.validate_feedback(packet,model,kind=='feedback')
        require(packet['status'] == ('submitted' if kind=='feedback' else 'draft'), 'Feedback export status mismatch')
        stem,ext='review-feedback' if kind=='feedback' else 'review-feedback-draft','json'
    elif kind=='feedback-md':
        # Human-readable derived text can be saved, but is not importable proof.
        require(content.startswith('# 审核意见\n'), 'Invalid opinion summary')
        stem,ext='review-feedback','md'
    elif kind=='model-json':
        require(k.object_hash(json.loads(content)) == k.object_hash(model), 'Different model export')
        stem,ext='goal-model','json'
    elif kind=='model-md':
        require(content == k.markdown(model), 'Different model text')
        stem,ext='goal-model','md'
    elif kind=='model-svg':
        require(content == k.svg(model), 'Different model diagram')
        stem,ext='goal-model','svg'
    elif kind=='relations-svg':
        require(model['schema_version'] == k.SCHEMA2 and content == k.relations_svg(model), 'Different relation diagram')
        stem,ext='goal-relations','svg'
    else:
        raise ValueError('Unsupported export kind')
    directory=(Path(root)/'exports').resolve()
    require(directory.parent == Path(root).resolve(), 'Unsafe export directory')
    directory.mkdir(exist_ok=True)
    name=stem+'-'+secrets.token_hex(6)+'.'+ext
    target=directory/name
    raw=content.encode('utf-8')
    with target.open('xb') as handle:
        handle.write(raw)
    require(k.digest(target.read_bytes()) == k.digest(raw), 'Written export verification failed')
    return dict(path=str(target),relative_path='exports/'+name,sha256=k.digest(raw),bytes=len(raw))


def make_server(root, port=0):
    root=Path(root).resolve()
    model=k.load(root/'goal-model.json')
    k.inspect(model,root)
    token=secrets.token_urlsafe(32)
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self,*a,**kw):super().__init__(*a,directory=str(root),**kw)
        def log_message(self,*a):pass
        def origin(self):return 'http://127.0.0.1:'+str(self.server.server_port)
        def valid_host(self):return self.headers.get('Host')=='127.0.0.1:'+str(self.server.server_port)
        def reply(self,status,value):
            raw=k.encode(value)
            self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Content-Length',str(len(raw)));self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(raw)
        def do_GET(self):
            if not self.valid_host():self.send_error(403);return
            path=unquote(urlsplit(self.path).path)
            target=(root/path.lstrip('/')).resolve()
            if root not in target.parents and target!=root:self.send_error(403);return
            if path in {'/','/goal-model.html'}:
                page=(root/'goal-model.html').read_text(encoding='utf-8')
                config=json.dumps(dict(endpoint='/__goalforge_save',token=token),ensure_ascii=True).replace('<','\\u003c')
                page=page.replace('<script id="payload"', '<script id="local-save-config" type="application/json">'+config+'</script><script id="payload"',1)
                raw=page.encode('utf-8');self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(raw)));self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(raw)
            elif target.is_dir():self.send_error(404)
            else:super().do_GET()
        def do_POST(self):
            if (not self.valid_host() or self.path!='/__goalforge_save' or self.headers.get('Origin')!=self.origin()
                or not secrets.compare_digest(self.headers.get('X-GoalForge-Token',''),token)):
                self.reply(403,dict(error='This save must be initiated by the current local preview'));return
            try:
                k.require(self.headers.get('Content-Type','').startswith('application/json'), 'JSON required')
                size=int(self.headers.get('Content-Length','0'))
                k.require(0<size<=10*1024*1024,'Invalid request size')
                k.require(k.binding(k.load(root/'goal-model.json'))==k.binding(model),'Model changed; reopen the preview')
                result=save_export(model,root,json.loads(self.rfile.read(size).decode('utf-8')))
                self.reply(200,result)
            except (ValueError,KeyError,TypeError,OSError) as error:
                self.reply(400,dict(error=str(error)))
    server=ThreadingHTTPServer(('127.0.0.1',port),Handler)
    return server


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('delivery',type=Path);parser.add_argument('--port',type=int,default=8772)
    args=parser.parse_args();server=make_server(args.delivery,args.port)
    print('Local review: http://127.0.0.1:'+str(server.server_port)+'/goal-model.html',flush=True)
    print('Verified exports are saved under '+str(args.delivery.resolve()/'exports'),flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()


if __name__=='__main__':main()
