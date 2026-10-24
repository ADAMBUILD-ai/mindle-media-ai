import json,os,time,subprocess,urllib.request,pathlib,datetime,concurrent.futures
out=pathlib.Path('outputs/C37_OFFICE_20261017_R1');out.mkdir(exist_ok=False)
exe=pathlib.Path('work/c37-PC-20261017/MINDLE_MEDIA_AI_ONE_CLICK_WIN_X64_v1.0/MINDLE_MEDIA_AI_RUN.exe').resolve()
env=dict(os.environ);env['LOCALAPPDATA']='C:/Users/R/AppData/Local';env.pop('PYTHONPATH',None);env.pop('MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT',None)
process=subprocess.Popen([str(exe)],cwd=exe.parent,env=env)
receipt={'started_at':datetime.datetime.now().astimezone().isoformat(),'exe':str(exe),'launcher_pid':process.pid,'trigger':'COMMAND_EXECUTION_OF_EXACT_EXE_NOT_NATIVE_DOUBLE_CLICK','source':'c37c7819b1454996f3510f92184b1ef62faf3c78','contains_transition_fix':False}
(out/'LAUNCH.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8');print('EXE_LAUNCHED',process.pid,flush=True)
def probe(port):
 try:
  with urllib.request.urlopen('http://127.0.0.1:%s/api/runtime-identity'%port,timeout=.7) as r:return port,json.load(r)
 except Exception:return None
for attempt in range(45):
 with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:found=[v for v in pool.map(probe,range(18768,18778)) if v]
 for port,identity in found:
  if identity.get('build_commit')==receipt['source']:
   receipt.update(status='PASS_EXE_SERVER_RUNTIME_IDENTITY',port=port,identity=identity,observed_at=datetime.datetime.now().astimezone().isoformat());(out/'LAUNCH.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8');print('EXE_SERVER_READY',port,flush=True);raise SystemExit(0)
 time.sleep(2)
receipt.update(status='BLOCKED_NO_C37_ENDPOINT_OBSERVED',launcher_exit_code=process.poll());(out/'LAUNCH.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8');print(receipt['status'],flush=True)
