"""Start real product processes and browser together; no model inference/mocks."""
import base64,hashlib,json,os,subprocess,sys,time,zipfile,wave
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from PIL import Image

REPO=Path(os.environ.get('WORKFLOW_REPO_ROOT',Path.cwd())).resolve()
sys.path.insert(0,str(REPO/'src'))
from media_ai.workflow_worker import tree_sha
OUT=REPO/'docs/evidence/media-ai-workflow-runtime-20261018'
DATA=Path(os.environ.get('WORKFLOW_DATA_DIR',str(REPO/'work-data/workflow-runtime-verification')));DATA.mkdir(parents=True,exist_ok=True)
if (DATA/'workflows/queue.sqlite3').exists():raise RuntimeError('fresh evidence data required')
BASE=REPO.parent;env=dict(os.environ);env['PYTHONPATH']=str(REPO/'src')
lib=BASE/'tts-runtime/root/usr/lib/x86_64-linux-gnu';exe=BASE/'tts-runtime/root/usr/bin/espeak-ng';env['LD_LIBRARY_PATH']=str(lib);env['MINDLE_SUBTITLE_FONT']=str(BASE/'test-fonts/NotoSansCJKkr-Regular.otf');env.pop('MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT',None);env.pop('HF_TOKEN',None)
settings={'tts':{'engine':'espeak-ng','executable':str(exe),'executable_sha256':hashlib.sha256(exe.read_bytes()).hexdigest(),'data_path':str(lib),'data_sha256':tree_sha(lib/'espeak-ng-data')}}
(DATA/'runtime-engines.json').write_text(json.dumps(settings))
subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','testsrc2=s=320x180:r=12','-f','lavfi','-i','sine=frequency=220:sample_rate=22050','-t','4','-c:v','libx264','-pix_fmt','yuv420p','-c:a','aac','-movflags','+faststart','-y',str(OUT/'input.mp4')],check=True)
Image.new('RGB',(36,60),'blue').save(OUT/'reference.png')
processes=[]
def start():
 command=[sys.executable,'-u','-m','media_ai.product_server','--root',str(REPO),'--data-dir',str(DATA),'--port','0']
 if os.environ.get('WORKFLOW_STRACE'):command=['strace','-ff','-tt','-e','trace=openat,truncate,ftruncate,rename,unlink','-o',str(DATA/'file-trace'),*command]
 process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=(OUT/f'server-{len(processes)+1}.log').open('wb'),text=True,env=env)
 processes.append(process);url=process.stdout.readline().strip();assert url.startswith('http://127.0.0.1:'),url
 return process,url

def call(url,path,body=None,headers=None):
 data=json.dumps(body,ensure_ascii=False).encode() if body is not None else None
 request=Request(url+path,data=data,headers={'Content-Type':'application/json',**(headers or {})})
 with urlopen(request,timeout=30) as r:return r.status,json.load(r)

def stop(process,url):
 _,identity=call(url,'/api/runtime-identity');_,control=call(url,'/api/runtime/control')
 status,_=call(url,'/api/runtime/shutdown',{'server_pid':control['server_pid'],'server_instance_id':control['server_instance_id']},{'X-Mindle-Control':control['control_nonce']});assert status==202
 process.wait(timeout=10);assert process.returncode==0
 try:call(url,'/api/runtime-identity');raise AssertionError('endpoint remains alive')
 except OSError:pass
 return {'pid':identity['server_pid'],'instance':identity['server_instance_id'],'exit':0,'endpoint_unavailable':True}

try:
 first,url=start();_,capabilities=call(url,'/api/workflows/capabilities');assert capabilities['generative_planner']=='LOCAL_GENERATIVE_MODEL_UNAVAILABLE'
 browser_env={**env,'WORKFLOW_TEST_URL':url,'WORKFLOW_TEST_EVIDENCE':str(OUT),'WORKFLOW_REPO_ROOT':str(REPO),'WORKFLOW_CHROMIUM':str(BASE/'browser-runtime/extracted/chromium'),'WORKFLOW_CHROMIUM_LIB':str(BASE/'browser-runtime/extracted/lib')}
 subprocess.run(['node',str(OUT/'browser_workflow.cjs')],env=browser_env,check=True,timeout=90)
 browser=json.loads((OUT/'BROWSER.json').read_text());pid=browser['projectId'];_,project=call(url,'/api/projects/'+pid);_,tasks=call(url,'/api/workflows');task=next(t for t in tasks['workflows'] if t['project_id']==pid);assert task['state']=='SUCCEEDED'
 narrator=next(j for j in project['project']['jobs'] if j['operation']=='narration');wav=Path(narrator['primary_output']['path'])
 with wave.open(str(wav),'rb') as audio:voice={'channels':audio.getnchannels(),'sample_rate':audio.getframerate(),'frames':audio.getnframes(),'seconds':audio.getnframes()/audio.getframerate(),'sha256':hashlib.sha256(wav.read_bytes()).hexdigest(),'bytes':wav.stat().st_size}
 assert any(wav.read_bytes()[44:]);record=task['result'];video=Path(record['primary_output']['path']);mp4sha=hashlib.sha256(video.read_bytes()).hexdigest();assert video.read_bytes().find(b'moov')<video.read_bytes().find(b'mdat')
 # Independent local BGM + narration mix, preserving the first saved project's exact bytes.
 first_project_path=DATA/'projects'/(pid+'.json');first_project_bytes=first_project_path.read_bytes()
 bgm=OUT/'background.wav'
 subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','sine=frequency=660:sample_rate=22050','-t','1','-y',str(bgm)],check=True)
 source=next(j for j in project['project']['jobs'] if j['operation']=='import' and j['lane']=='video')
 _,bgm_task=call(url,'/api/workflows',{'request_id':'bgm-integration','input_job_id':source['job_id'],'steps':[{'operation':'narrate','text':'한국어 음성과 배경음악을 함께 확인합니다.'},{'operation':'mix_narration','length_policy':'extend_video','original_volume':.2}], 'background':{'filename':'background.wav','content_base64':base64.b64encode(bgm.read_bytes()).decode()}})
 deadline=time.monotonic()+30
 while time.monotonic()<deadline:
  _,bgm_result=call(url,'/api/workflows/'+bgm_task['workflow_id'])
  if bgm_result['state'] in {'SUCCEEDED','FAILED'}:break
  time.sleep(.1)
 assert bgm_result['state']=='SUCCEEDED',bgm_result
 assert first_project_path.read_bytes()==first_project_bytes
 _,all_tasks=call(url,'/api/workflows');(OUT/'ALL_TASKS.json').write_text(json.dumps(all_tasks,ensure_ascii=False,indent=2))
 (OUT/'BGM_TASK.json').write_text(json.dumps(bgm_result,ensure_ascii=False,indent=2))
 before=stop(first,url);second,url2=start();_,identity2=call(url2,'/api/runtime-identity');assert identity2['server_pid']!=before['pid'];assert identity2['server_instance_id']!=before['instance']
 _,reopened=call(url2,'/api/projects/'+pid);assert len(reopened['project']['jobs'])==len(project['project']['jobs']);_,history=call(url2,'/api/workflows');assert history['workflows'][0]['state']=='SUCCEEDED'
 _,export=call(url2,'/api/projects/'+pid+'/export',{});archive_path=Path(export['export']['path'])
 checks=[]
 with zipfile.ZipFile(archive_path) as archive:
  assert archive.testzip() is None
  manifest=json.loads(archive.read('BUNDLE_MANIFEST.json'))
  for item in manifest['files']:
   content=archive.read(item['archive_path']);assert len(content)==item['bytes'];assert hashlib.sha256(content).hexdigest()==item['sha256'];checks.append(item)
 assert any(item['sha256']==mp4sha for item in checks);assert any(item['sha256']==voice['sha256'] for item in checks);assert any(item['role']=='workspace_reference' for item in checks)
 after=stop(second,url2)
 receipt={'status':'PASS_SOURCE_PRODUCT_RUNTIME_NOT_WINDOWS','plan_source':'STRUCTURED_USER_PLAN_NOT_GENERATIVE','generative_inference':'BLOCKED_LOCAL_MODEL_ABSENT','workflow_id':task['workflow_id'],'project_id':pid,'attempts':task['attempts'],'voice':voice,'engine':narrator['runtime_result'],'mp4':record['primary_output'],'mix':record['runtime_result'],'first_stop':before,'second_stop':after,'export':{'sha256':hashlib.sha256(archive_path.read_bytes()).hexdigest(),'bytes':archive_path.stat().st_size,'crc':'PASS','files':checks},'human_hearing':'NOT_VERIFIED','windows_exe':'NOT_EXECUTED','marketing_avora':'DEFERRED_EXTERNAL'}
 (OUT/'RUNTIME.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2))
 (OUT/'TASK.json').write_text(json.dumps(task,ensure_ascii=False,indent=2))
 import shutil
 shutil.copyfile(wav,OUT/'KOREAN_NARRATION.wav');shutil.copyfile(video,OUT/'NARRATED_EXPORT.mp4');shutil.copyfile(archive_path,OUT/'PROJECT_EXPORT.zip')
 print('PASS real product browser -> TTS -> MP4 -> save -> own process shutdown -> new PID -> reopen -> export/CRC/hashes')
finally:
 for process in processes:
  if process.poll() is None:process.terminate();process.wait(timeout=10)
