"""Source-only real pinned Qwen proof. Requires an existing verified engine config.

Creates synthetic exposure counterfactuals, not architectural marketing footage.
No model download, package build, fixture inference or installation is performed.
"""
from __future__ import annotations
import argparse
import base64
import hashlib
import json
import shutil
import subprocess
import time
from pathlib import Path
from media_ai.product_runtime import ProductJobService, file_record
from media_ai.generative_auto_edit import make_auto_plan
from media_ai.durable_workflows import DurableWorkflows
from media_ai.ai_core_status import summarize_ai_core


def write(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--engine-config',required=True)
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    output=Path(args.output).resolve();output.mkdir(parents=True,exist_ok=False)
    config=json.loads(Path(args.engine_config).read_text())
    assert config['planner']['model_sha256']=='6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e'
    assert config['planner']['executable_sha256']=='7119bef261611b26f326f7c4da4dc3fdeb7bb28e2faf1ec392bda7b21215ef52'
    repo=Path(__file__).resolve().parents[1]
    files=sorted((repo/'src/media_ai').glob('*.py'))+sorted((repo/'ui').glob('*.js'))+[repo/'ui/index.html']
    receipt={'status':'RUNNING','source_commit':subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip(),
             'source_files':{str(p.relative_to(repo)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
             'model_downloaded_by_probe':False,'fixture_inference':False,'native_windows':False,
             'semantic_understanding':False,'architectural_promotion_quality':'NOT_TESTED','full_product_pass':False,'cases':[]}
    try:
        for name,color in [('dark','0x202020'),('bright','0xe0e0e0')]:
            folder=output/name;folder.mkdir()
            media=folder/'input.mp4'
            subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i',f'color=c={color}:s=160x90:r=12',
                            '-t','2','-c:v','libx264','-pix_fmt','yuv420p',str(media)],check=True)
            service=ProductJobService(folder/'data','')
            write(service.root/'runtime-engines.json',config)
            source=service.import_media({'kind':'video','filename':'input.mp4','content_base64':base64.b64encode(media.read_bytes()).decode()})
            queue=DurableWorkflows(service)
            try:
                plan=make_auto_plan(service,{'command':'자동 편집','input_job_id':source['job_id']})
                write(folder/'ACTUAL_QWEN_PLAN.json',plan)
                shutil.copyfile(service.root/'workflows/plans'/(plan['plan_id']+'.response.txt'),folder/'ACTUAL_QWEN_RESPONSE.txt')
                task=queue.submit({'request_id':'real-qwen-'+name,'input_job_id':source['job_id'],'plan_id':plan['plan_id'],'steps':plan['steps']})
                deadline=time.monotonic()+120
                while time.monotonic()<deadline:
                    task=queue.get(task['workflow_id'])
                    if task['state'] in {'SUCCEEDED','FAILED','CANCELLED','INTERRUPTED'}:break
                    time.sleep(.05)
                write(folder/'ACTUAL_WORKFLOW.json',task)
                assert task['state']=='SUCCEEDED',task.get('error',task['state'])
                status=summarize_ai_core({},[task],[],[],data_root=service.root)
                assert status['state']=='AI_EDIT_EXECUTION_VERIFIED'
                assert task['technical_quality']['status']=='PASS_TECHNICAL_ONLY'
                shutil.copyfile(task['result']['primary_output']['path'],folder/'output.mp4')
                reopened=ProductJobService(service.root,'')
                saved=reopened.latest_project()
                assert saved['project_id']==task['project_id']
                exported=reopened.export_project(task['project_id'])
                row={'case':name,'input':file_record(media),'output':file_record(folder/'output.mp4'),
                     'workflow_id':task['workflow_id'],'plan_id':plan['plan_id'],'decision':plan['decision'],
                     'actual_model_inference':True,'raw_response_sha256':plan['raw_response_sha256'],
                     'technical_quality':task['technical_quality'],'reopen_project':'PASS','export':exported,
                     'status':'PASS_ACTUAL_QWEN_FFMPEG_TECHNICAL_GATE'}
                receipt['cases'].append(row)
                print(name,'ACTUAL_QWEN_TO_MP4_PASS',json.dumps(plan['decision'],ensure_ascii=False),flush=True)
            finally:queue.close()
        # Same request, different measured input: reject a constant response/preset.
        dark,bright=[case['decision']['brightness'] for case in receipt['cases']]
        receipt['input_sensitivity']={'dark_brightness':dark,'bright_brightness':bright,
                                       'different_decisions':dark!=bright,'opposite_exposure_directions':dark>0 and bright<0}
        assert dark>0 and bright<0,'AI_INPUT_SENSITIVITY_FAILED'
        receipt['status']='PASS_ACTUAL_PINNED_QWEN_INPUT_SENSITIVE_AUTO_EDIT'
    except Exception as error:
        receipt['status']='FAIL_ACTUAL_QWEN_AUTO_EDIT';receipt['error']=repr(error)
        raise
    finally:write(output/'REAL_INFERENCE_RECEIPT.json',receipt)


if __name__=='__main__':main()
