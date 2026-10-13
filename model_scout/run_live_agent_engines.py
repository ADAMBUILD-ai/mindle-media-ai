"""Real adopted CPU engines through the repaired product service, no fake adapters."""
import base64
import hashlib
import json
import os
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
    service=ProductJobService(ROOT/'live_agent_engine_data',os.environ.get('HF_TOKEN',''))
    receipt={'source_commit':os.environ['GITHUB_SHA'],'status':'RUNNING','real_model_calls':0,'jobs':[],'full_product_pass':False}
    try:
        for operation in ('segment','upscale','tracking','transcribe'):
            previous=records[operation];source=frozen/'inputs'/Path(previous['input']['path']).name
            assert hashlib.sha256(source.read_bytes()).hexdigest()==previous['input']['sha256']
            request={'lane':previous['lane'],'operation':operation,'command':previous['command'],
                     'filename':source.name,'content_base64':base64.b64encode(source.read_bytes()).decode()}
            result=service.execute_isolated(request)
            assert result['status']=='TESTED_PASS'
            assert result['execution_started_at']<result['execution_finished_at']
            assert result['state_history']==['queued','validating','preflight_ready','dispatched','running','output_validating','succeeded']
            receipt['real_model_calls']+=1;receipt['jobs'].append(result)
            (OUT/'LIVE_ENGINE_RECEIPT.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
        saved=service.save_project({'job_ids':[j['job_id'] for j in receipt['jobs']]})
        reopened=ProductJobService(ROOT/'live_agent_engine_data',os.environ.get('HF_TOKEN',''))
        assert reopened.latest_project()['project_id']==saved['project_id']
        receipt['export']=reopened.export_project(saved['project_id'])
        receipt['status']='PASS_ADOPTED_CPU_ENGINE_EXECUTION_AND_PERSISTENCE'
    except Exception as error:
        receipt.update(status='FAILED',error=repr(error));raise
    finally:
        (OUT/'LIVE_ENGINE_RECEIPT.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
