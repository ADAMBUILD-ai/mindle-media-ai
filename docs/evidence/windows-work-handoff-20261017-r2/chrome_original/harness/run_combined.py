import sys,os,threading,json,urllib.request,runpy
from pathlib import Path
folder=Path(__file__).resolve().parent;repo=folder/'source'
sys.path.insert(0,str(repo/'src'));sys.path.append(str(folder.parent/'site-packages'))
sys.path.append(str(folder.parent/'browser-control-probe/venv/Lib/site-packages'))
from media_ai.product_server import create_server
evidence=Path('outputs/TRANSITION_BROWSER_20261017_R6').resolve();evidence.mkdir(exist_ok=False)
server=create_server(repo,evidence/'data','',18768);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
os.environ['MINDLE_ACCEPTANCE_EVIDENCE']=str(evidence);os.environ['MINDLE_ACCEPTANCE_URL']='http://127.0.0.1:18768'
(evidence/'SERVER.json').write_text(json.dumps({'pid':os.getpid(),'identity':server.runtime_identity(),'scope':'SOURCE_NOT_CANDIDATE'},indent=2),encoding='utf-8')
try:
 with urllib.request.urlopen('http://127.0.0.1:18768/api/runtime-identity',timeout=5) as response:print('SELF_HTTP',response.status,flush=True)
 runpy.run_path(str(folder/'browser_transitions.py'),run_name='__main__')
finally:
 server.shutdown();server.server_close();thread.join(timeout=5)
 (evidence/'SERVER_REQUEST_LOG.json').write_text(json.dumps(server.requests,indent=2),encoding='utf-8')




