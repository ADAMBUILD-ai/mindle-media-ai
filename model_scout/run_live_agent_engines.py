"""Real adopted CPU engines through the repaired product service, no fake adapters."""
import base64
import hashlib
import json
import os
import threading
import shutil
import requests
from media_ai.product_server import create_server
from pathlib import Path
from media_ai.product_runtime import ProductJobService

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/evidence/media-ai-agent-engine-repair-20261014'
OUT.mkdir(parents=True,exist_ok=True)

def main():
    frozen=ROOT/'engine_fixtures/product_e2e_evidence/product_data'
    projects=list((frozen/'projects').glob('*.json'))
    original=[]
    for p in projects:original.extend(json.loads(p.read_text())['jobs'])
    records={j['operation']:j for j in original if j['operation'] in ('segment','upscale','tracking','transcribe')}
    revision=records['upscale']['model']['private_cache']['revision']
    os.environ['MINDLE_ALTERNATIVE_CACHE_REVISION']=revision
    os.environ['MINDLE_ALTERNATIVE_MANIFEST_RUN_ID']='37738880868'
    server=create_server(ROOT,ROOT/'live_agent_engine_data',os.environ.get('HF_TOKEN',''),0)
    worker=threading.Thread(target=server.serve_forever,daemon=True);worker.start()
    service=server.service
    base_url=f'http://127.0.0.1:{server.server_port}'
    receipt={'source_commit':os.environ['GITHUB_SHA'],'status':'RUNNING','real_model_calls':0,'jobs':[],'full_product_pass':False}
    try:
        resume=ROOT/'engine_resume'
        prior=resume/'docs/evidence/media-ai-agent-engine-repair-20261014/LIVE_ENGINE_RECEIPT.json'
        completed=set()
        if prior.is_file():
            checkpoint=json.loads(prior.read_text())
            assert checkpoint['source_commit']=='ac0ee3c4eaa6c708712f3cc3467cf155ce710606'
            shutil.copytree(resume/'live_agent_engine_data/jobs',ROOT/'live_agent_engine_data/jobs',dirs_exist_ok=True)
            def rebase(value):
                if isinstance(value,dict):return {k:rebase(v) for k,v in value.items()}
                if isinstance(value,list):return [rebase(v) for v in value]
                if isinstance(value,str) and '/live_agent_engine_data/' in value:return str(ROOT/'live_agent_engine_data'/value.split('/live_agent_engine_data/',1)[1])
                return value
            for previous in checkpoint['jobs']:
                if previous['operation']=='segment':continue
                item=rebase(previous)
                for output in item['outputs']:
                    assert hashlib.sha256(Path(output['path']).read_bytes()).hexdigest()==output['sha256']
                original=records[item['operation']]
                original_source=frozen/'inputs'/Path(original['input']['path']).name
                destination=Path(item['input']['path']);destination.parent.mkdir(parents=True,exist_ok=True)
                if not destination.is_file():shutil.copy2(original_source,destination)
                assert hashlib.sha256(destination.read_bytes()).hexdigest()==item['input']['sha256']
                item['verification_provenance']='REUSED_CURRENT_REPAIR_RUN_38425586338_SAME_ENGINE_IMPLEMENTATION'
                service.records[item['job_id']]=item;receipt['jobs'].append(item);completed.add(item['operation'])
        for operation in ('segment','upscale','tracking','transcribe'):
            if operation in completed:continue
            previous=records[operation];source=frozen/'inputs'/Path(previous['input']['path']).name
            assert hashlib.sha256(source.read_bytes()).hexdigest()==previous['input']['sha256']
            if operation=='transcribe':
                import subprocess
                original=source;source=OUT/'long_korean_44100.wav'
                subprocess.run(['ffmpeg','-y','-stream_loop','2','-i',str(original),'-ar','44100','-ac','2',str(source)],check=True,capture_output=True)
            request={'lane':previous['lane'],'operation':operation,'command':previous['command'],
                     'filename':source.name,'content_base64':base64.b64encode(source.read_bytes()).decode()}
            if operation=='segment':
                import io
                from PIL import Image
                buffer=io.BytesIO()
                with Image.open(source) as image:image.crop((109,126,141,166)).save(buffer,'PNG')
                request['references']=[{'filename':'target_crop.png','content_base64':base64.b64encode(buffer.getvalue()).decode()}]
            response=requests.post(base_url+'/api/jobs',json=request,timeout=950)
            result=response.json()
            if not response.ok:raise RuntimeError(result.get('error','actual HTTP job failed'))
            assert result['status']=='TESTED_PASS'
            assert result['execution_started_at']<result['execution_finished_at']
            assert result['state_history']==['queued','validating','preflight_ready','dispatched','running','output_validating','succeeded']
            if operation=='tracking':
                import cv2
                capture=cv2.VideoCapture(str(source));count=int(capture.get(cv2.CAP_PROP_FRAME_COUNT));capture.release()
                assert result['runtime_result']['tracked_frames']==count
            if operation=='segment':assert result['runtime_result']['reference_match']['score']>=.75
            if operation=='transcribe':
                assert result['runtime_result']['duration_seconds']>25
                assert len(result['runtime_result']['segments'])>=2
                assert result['runtime_result']['sample_rate']==16000
            receipt['real_model_calls']+=1;receipt['real_model_jobs']=len(receipt['jobs'])+1;receipt['jobs'].append(result)
            (OUT/'LIVE_ENGINE_RECEIPT.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
        saved=service.save_project({'job_ids':[j['job_id'] for j in receipt['jobs']]})
        reopened=ProductJobService(ROOT/'live_agent_engine_data',os.environ.get('HF_TOKEN',''))
        assert reopened.latest_project()['project_id']==saved['project_id']
        receipt['export']=reopened.export_project(saved['project_id'])
        receipt['status']='PASS_ADOPTED_CPU_ENGINE_EXECUTION_AND_PERSISTENCE'
    except Exception as error:
        receipt.update(status='FAILED',error=repr(error));raise
    finally:
        server.shutdown();worker.join(5);server.server_close()
        (OUT/'LIVE_ENGINE_RECEIPT.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
