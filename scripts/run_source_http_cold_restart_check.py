"""Real Linux source HTTP process restart/export probe. No models or EXE claims."""
import base64
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from urllib.request import Request,urlopen
import zipfile
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]


def main():
    with tempfile.TemporaryDirectory() as td:
        work=Path(td);data=work/'data';log=(work/'server.log').open('ab')
        env=dict(os.environ,PYTHONPATH=str(ROOT/'src'),HF_HUB_OFFLINE='1')
        env.pop('MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT',None)
        def start():
            p=subprocess.Popen([sys.executable,'-m','media_ai.product_server','--root',str(ROOT),'--data-dir',str(data),'--port','0'],cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=log,text=True)
            url=p.stdout.readline().strip()
            if not url.startswith('http://127.0.0.1:'):
                p.terminate();p.wait(timeout=5);raise RuntimeError('source server failed to start')
            return p,url
        def call(url,path,payload=None,raw=False):
            req=Request(url+path,data=None if payload is None else json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
            with urlopen(req,timeout=30) as r:content=r.read()
            return content if raw else json.loads(content)
        p=None
        try:
            p,base=start();pid1=p.pid
            buf=io.BytesIO();Image.new('RGB',(90,160),(190,80,30)).save(buf,'PNG')
            photo=call(base,'/api/photo-edits',{'content_base64':base64.b64encode(buf.getvalue()).decode(),'command':'source restart fixture','options':{'temperature':20}})
            video=work/'source.mp4'
            subprocess.run(['ffmpeg','-y','-f','lavfi','-i','testsrc2=size=160x90:rate=10:duration=1','-f','lavfi','-i','sine=frequency=440:duration=1','-c:v','libx264','-pix_fmt','yuv420p','-c:a','aac','-shortest',str(video)],check=True,capture_output=True)
            edited=call(base,'/api/video-edits',{'filename':'source.mp4','content_base64':base64.b64encode(video.read_bytes()).decode(),'options':{'brightness':18}})
            saved=call(base,'/api/projects/save',{'job_ids':[photo['job_id'],edited['job_id']]})
            p.terminate();p.wait(timeout=5);p.stdout.close();p=None
            try:call(base,'/api/runtime-identity')
            except OSError:old_endpoint_closed=True
            else:raise AssertionError('old process endpoint still responds')
            p,base2=start();pid2=p.pid
            assert pid1!=pid2
            reopened=call(base2,'/api/projects/latest')['project']
            assert reopened['project_id']==saved['project_id']
            expected={j['job_id']:j['primary_output']['sha256'] for j in (photo,edited)}
            for job in reopened['jobs']:
                content=call(base2,job['preview_url'],raw=True)
                assert hashlib.sha256(content).hexdigest()==expected[job['job_id']]
            exported=call(base2,'/api/projects/'+saved['project_id']+'/export',{})
            archive=call(base2,exported['download_url'],raw=True)
            assert hashlib.sha256(archive).hexdigest()==exported['export']['sha256']
            with zipfile.ZipFile(io.BytesIO(archive)) as z:
                assert z.testzip() is None
                for job in reopened['jobs']:
                    content=z.read('jobs/'+job['job_id']+'/'+Path(job['primary_output']['path']).name)
                    assert hashlib.sha256(content).hexdigest()==expected[job['job_id']]
                members=z.namelist()
            result={'status':'PASS_LINUX_SOURCE_HTTP_COLD_RESTART_PHOTO_VIDEO_EXPORT',
                    'first_pid':pid1,'second_pid':pid2,'old_endpoint_closed':old_endpoint_closed,
                    'project_id':saved['project_id'],'job_output_sha256':expected,'export_sha256':hashlib.sha256(archive).hexdigest(),
                    'zip_crc':'PASS','members':members,'model_inference':False,
                    'scope':'GENERATED_FIXTURES_LINUX_SOURCE_HTTP_ONLY','windows_exe_pass':False,
                    'owner_pc_pass':False,'full_product_pass':False}
            out=ROOT/'outputs/r9-source-regression';out.mkdir(parents=True,exist_ok=True)
            (out/'SOURCE_HTTP_COLD_RESTART.json').write_text(json.dumps(result,indent=2)+'\n')
            print(json.dumps(result))
        finally:
            if p is not None:
                p.terminate();p.wait(timeout=5);p.stdout.close()
            log.close()


if __name__=='__main__':main()
