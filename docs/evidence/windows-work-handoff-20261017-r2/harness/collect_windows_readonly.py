import ctypes as c,ctypes.wintypes as w,json,pathlib,os,datetime,subprocess,concurrent.futures,urllib.request,hashlib
out=pathlib.Path('outputs/WINDOWS_WORK_HANDOFF_20261017_R2');out.mkdir(exist_ok=False)
def write(n,v):(out/n).write_text(json.dumps(v,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
now=lambda:datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat()
k=c.WinDLL('kernel32',use_last_error=True);a=c.WinDLL('advapi32',use_last_error=True)
k.GetCurrentProcess.restype=w.HANDLE;k.CloseHandle.argtypes=[w.HANDLE]
a.OpenProcessToken.argtypes=[w.HANDLE,w.DWORD,c.POINTER(w.HANDLE)];a.GetTokenInformation.argtypes=[w.HANDLE,c.c_int,c.c_void_p,w.DWORD,c.POINTER(w.DWORD)]
a.ConvertSidToStringSidW.argtypes=[c.c_void_p,c.POINTER(w.LPWSTR)];k.LocalFree.argtypes=[c.c_void_p]
token=w.HANDLE();assert a.OpenProcessToken(k.GetCurrentProcess(),8,c.byref(token))
def ti(cls):
 n=w.DWORD();a.GetTokenInformation(token,cls,None,0,c.byref(n));buf=c.create_string_buffer(n.value)
 if not a.GetTokenInformation(token,cls,buf,n,c.byref(n)):return {'error':c.get_last_error()}
 return buf
def sid(ptr):
 s=w.LPWSTR()
 if not a.ConvertSidToStringSidW(ptr,c.byref(s)):return None
 value=s.value;k.LocalFree(s);return value
class SIDATTR(c.Structure):_fields_=[('Sid',c.c_void_p),('Attributes',w.DWORD)]
tok={}
for name,cls in [('is_appcontainer',29),('is_elevated',20),('elevation_type',18)]:
 v=ti(cls);tok[name]=v if isinstance(v,dict) else c.cast(v,c.POINTER(w.DWORD)).contents.value
for name,cls in [('user_sid',1),('integrity_sid',25),('appcontainer_sid',31)]:
 v=ti(cls);tok[name]=v if isinstance(v,dict) else sid(c.cast(v,c.POINTER(SIDATTR)).contents.Sid)
k.CloseHandle(token)
context={'at':now(),'tool':'Codex exec_command / PowerShell / bundled Python','user':os.environ.get('USERNAME'),'LOCALAPPDATA':os.environ.get('LOCALAPPDATA'),'USERPROFILE':os.environ.get('USERPROFILE'),'cwd':str(pathlib.Path.cwd()),'python':os.sys.executable,'token':tok,'historical_exe_env_override':'Previous launch script explicitly set LOCALAPPDATA=C:/Users/R/AppData/Local; not repeated in this collection.'};write('EXECUTION_CONTEXT.json',context)
parent=pathlib.Path('C:/Users/R/AppData/Local/MINDLE_MEDIA_AI');paths=[parent.parent,parent,parent/'deploy.lock',pathlib.Path('C:/Users/R/AppData/Local/MINDLE/MEDIA_AI_DATA/launch.lock')]
rows=[]
for p in paths:
 row={'path':str(p),'exists':p.exists()}
 try:
  s=p.lstat();row.update(kind='directory' if p.is_dir() else 'file' if p.is_file() else 'other',size=s.st_size,file_attributes=getattr(s,'st_file_attributes',None),readonly=bool(getattr(s,'st_file_attributes',0)&1),reparse=bool(getattr(s,'st_file_attributes',0)&1024),created_utc=datetime.datetime.fromtimestamp(s.st_ctime,datetime.timezone.utc).isoformat(),modified_utc=datetime.datetime.fromtimestamp(s.st_mtime,datetime.timezone.utc).isoformat())
  if p.is_file():row['sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
 except Exception as e:row['error']=repr(e)
 rows.append(row)
write('PATH_METADATA.json',rows)
# Built-in Restart Manager is used for query only. No shutdown/restart calls.
class UNIQUE(c.Structure):_fields_=[('pid',w.DWORD),('started',w.FILETIME)]
class INFO(c.Structure):_fields_=[('process',UNIQUE),('app',w.WCHAR*256),('service',w.WCHAR*64),('type',w.DWORD),('status',w.DWORD),('session',w.DWORD),('restartable',w.BOOL)]
rm=c.WinDLL('rstrtmgr',use_last_error=True);rm.RmStartSession.argtypes=[c.POINTER(w.DWORD),w.DWORD,w.LPWSTR];rm.RmRegisterResources.argtypes=[w.DWORD,w.UINT,c.POINTER(w.LPCWSTR),w.UINT,c.c_void_p,w.UINT,c.c_void_p];rm.RmGetList.argtypes=[w.DWORD,c.POINTER(w.UINT),c.POINTER(w.UINT),c.POINTER(INFO),c.POINTER(w.DWORD)]
handle=w.DWORD();key=c.create_unicode_buffer(33);r=rm.RmStartSession(c.byref(handle),0,key);result={'query_only':True,'start_result':r,'path':str(parent/'deploy.lock')}
if r==0:
 try:
  files=(w.LPCWSTR*1)(str(parent/'deploy.lock'));result['register_result']=rm.RmRegisterResources(handle,1,files,0,None,0,None)
  needed=w.UINT();count=w.UINT();reason=w.DWORD();code=rm.RmGetList(handle,c.byref(needed),c.byref(count),None,c.byref(reason));result.update(initial_get_result=code,needed=needed.value)
  if code==234:
   count=w.UINT(needed.value);arr=(INFO*count.value)();code=rm.RmGetList(handle,c.byref(needed),c.byref(count),arr,c.byref(reason));result.update(get_result=code,owners=[{'pid':x.process.pid,'app':x.app,'service':x.service,'type':x.type} for x in arr[:count.value]] if code==0 else None)
  elif code==0:result.update(get_result=0,owners=[])
 finally:rm.RmEndSession(handle)
write('RESTART_MANAGER_QUERY.json',result)
# Visible matching process paths only; no unrelated Chrome command lines.
class ENTRY(c.Structure):_fields_=[('size',w.DWORD),('usage',w.DWORD),('pid',w.DWORD),('heap',c.c_size_t),('module',w.DWORD),('threads',w.DWORD),('parent',w.DWORD),('priority',w.LONG),('flags',w.DWORD),('name',w.WCHAR*260)]
k.CreateToolhelp32Snapshot.argtypes=[w.DWORD,w.DWORD];k.CreateToolhelp32Snapshot.restype=w.HANDLE;k.Process32FirstW.argtypes=[w.HANDLE,c.POINTER(ENTRY)];k.Process32NextW.argtypes=[w.HANDLE,c.POINTER(ENTRY)];k.OpenProcess.argtypes=[w.DWORD,w.BOOL,w.DWORD];k.OpenProcess.restype=w.HANDLE;k.QueryFullProcessImageNameW.argtypes=[w.HANDLE,w.DWORD,w.LPWSTR,c.POINTER(w.DWORD)]
snap=k.CreateToolhelp32Snapshot(2,0);entry=ENTRY();entry.size=c.sizeof(entry);procs=[];seen=0
if snap and snap!=w.HANDLE(-1).value:
 ok=k.Process32FirstW(snap,c.byref(entry))
 while ok:
  seen+=1
  if entry.name.lower() in ['mindle_media_ai_run.exe','pythonw.exe','python.exe']:
   row={'pid':entry.pid,'parent_pid':entry.parent,'name':entry.name};ph=k.OpenProcess(0x1000,False,entry.pid)
   if ph:
    buf=c.create_unicode_buffer(32768);n=w.DWORD(len(buf));row['path']=buf.value if k.QueryFullProcessImageNameW(ph,0,buf,c.byref(n)) else None;k.CloseHandle(ph)
   else:row['path_access_error']=c.get_last_error()
   procs.append(row)
  ok=k.Process32NextW(snap,c.byref(entry))
 k.CloseHandle(snap)
write('VISIBLE_PROCESS_QUERY.json',{'visible_total':seen,'matching':procs,'command_line':'Collected independently via CIM if permitted','cannot_infer_global_absence_from_filtered_view':True})
def probe(port):
 try:
  with urllib.request.urlopen('http://127.0.0.1:%d/api/runtime-identity'%port,timeout=1) as r:return {'port':port,'status':r.status,'identity':json.load(r)}
 except Exception as e:return {'port':port,'error':repr(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:write('ENDPOINTS_READONLY.json',list(pool.map(probe,range(18768,18778))))
print(json.dumps({'token':tok,'restart_manager':result,'visible_processes':seen,'matching':len(procs)},ensure_ascii=True))
