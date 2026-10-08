"""Continue from immutable real PHOTO/tracking PASS; never rerun frozen models."""
from __future__ import annotations
import hashlib
import json
import os
import shutil
import subprocess
import threading
import time
import zipfile
from pathlib import Path
from urllib.parse import urljoin

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from media_ai.browser_preview import digest, probe
from media_ai.product_server import create_server
from media_ai.marketing_shortform_client import MarketingShortformClient, MarketingShortformClientError

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT/'product_e2e_evidence'
DATA = WORK/'product_data'
OUT = ROOT/'docs/evidence/media-ai-product-e2e-full-pass-20261008'
FROZEN = ROOT/'frozen_product_checkpoint'
EPOCH = 'MEDIA-AI-20261008-PRODUCT-E2E-VIDEO-PREVIEW-TO-FULL-PASS-R1'
EXPECTED = {
 'segment':'c5e56328a45d29724f437473a1c634b62255d2a81976317b7d28992e2e59a84f',
 'upscale':'a6dcc897c81f9cb581f8317a626e5f3e11eae5601cecb11fef7f1a8c5d0498f8',
 'tracking':'41a9c54966fe89a636873839402fdc3d2530fbb80e8eb2c3559f0fc815acbe69',
}
GATES = {}

def write(name, value):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def file_info(path):
    path=Path(path)
    return {'path':str(path),'bytes':path.stat().st_size,'sha256':digest(path)}

def rebase(value):
    if isinstance(value,dict): return {k:rebase(v) for k,v in value.items()}
    if isinstance(value,list): return [rebase(v) for v in value]
    if isinstance(value,str) and '/product_e2e_evidence/product_data/' in value:
        relative=value.split('/product_e2e_evidence/product_data/',1)[1]
        target=(DATA/relative).resolve()
        if DATA.resolve() not in target.parents: raise ValueError('checkpoint path traversal')
        return str(target)
    return value

def checkpoint():
    DATA.mkdir(parents=True,exist_ok=True)
    shutil.copytree(FROZEN/'product_data',DATA,dirs_exist_ok=True)
    jobs={}
    for path in sorted((DATA/'jobs').glob('*/JOB_EVIDENCE.json')):
        record=rebase(json.loads(path.read_text(encoding='utf-8')))
        operation=record.get('operation')
        if operation not in EXPECTED: continue
        if operation in jobs: raise RuntimeError('ambiguous frozen checkpoint')
        if record['status']!='TESTED_PASS' or record['primary_output']['sha256']!=EXPECTED[operation]:
            raise RuntimeError('immutable checkpoint identity mismatch')
        for item in [record['input'],record['primary_output'],*record['outputs']]:
            if digest(Path(item['path']))!=item['sha256']: raise RuntimeError('checkpoint media hash mismatch')
        jobs[operation]=record
    if set(jobs)!=set(EXPECTED): raise RuntimeError('frozen real model checkpoint unavailable')
    if jobs['upscale']['input']['sha256']!=jobs['segment']['primary_output']['sha256']:
        raise RuntimeError('frozen segment/upscale continuity mismatch')
    write('VIDEO_TRACKING_ARTIFACTS_MANIFEST.json',{
        'source_run':37735046818,'artifact_id':11531386885,'models_rerun':False,
        'frozen_original_records':jobs,'original_tracking_probe':probe(Path(jobs['tracking']['primary_output']['path']))})
    return jobs

def browser():
    download=WORK/'downloads';download.mkdir(parents=True,exist_ok=True)
    options=Options()
    for arg in ('--headless=new','--no-sandbox','--disable-dev-shm-usage','--autoplay-policy=no-user-gesture-required'):
        options.add_argument(arg)
    options.set_capability('goog:loggingPrefs',{'browser':'ALL'})
    options.add_experimental_option('prefs',{'download.default_directory':str(download),'download.prompt_for_download':False})
    driver=webdriver.Chrome(options=options);driver.set_window_size(1600,1100)
    return driver

def media_state(driver):
    return driver.execute_script('''const host=document.querySelector('[data-preview="video"]');
      const v=host.querySelector('video'); if(!v) return null;
      return {jobId:host.dataset.jobId,operation:host.dataset.operation,
        currentSrc:v.currentSrc,readyState:v.readyState,networkState:v.networkState,
        videoWidth:v.videoWidth,videoHeight:v.videoHeight,duration:Number.isFinite(v.duration)?v.duration:null,
        currentTime:v.currentTime,paused:v.paused,
        MediaError:{code:v.error?.code||null,message:v.error?.message||null},
        canPlayType:{mp4v:v.canPlayType('video/mp4; codecs="mp4v.20.9"'),
          h264:v.canPlayType('video/mp4; codecs="avc1.42E01E"'),mp4:v.canPlayType('video/mp4')}};''')

def photo_ready(driver, job_id):
    return driver.execute_script('''const h=document.querySelector('[data-preview="photo"]');const i=h.querySelector('img');
      return h.dataset.jobId===arguments[0] && i && i.complete && i.naturalWidth>0;''',job_id)

def diagnose(driver,base_url,tracking):
    deadline=time.monotonic()+20
    state=None
    while time.monotonic()<deadline:
        state=media_state(driver)
        if state and state['jobId']==tracking['job_id'] and (state['MediaError']['code'] or state['readyState']>=2):break
        time.sleep(.2)
    if not state or state['jobId']!=tracking['job_id']:raise RuntimeError('exact tracking element not restored')
    response=requests.get(urljoin(base_url,state['currentSrc']),timeout=30)
    value={'browser':state,'http':{'status':response.status_code,'Content-Type':response.headers.get('Content-Type'),
        'sha256':hashlib.sha256(response.content).hexdigest()},
        'browser_console':driver.get_log('browser'),
        'ffprobe':probe(Path(tracking['primary_output']['path'])),
        'captured_before_codec_repair':True,'source_run':37735046818}
    write('VIDEO_BROWSER_DIAGNOSTICS.json',value)
    driver.find_element(By.CSS_SELECTOR,'[data-preview="video"]').screenshot(str(OUT/'VIDEO_BEFORE.png'))
    return value

def decode(driver,tracking,play=False):
    def ready(_):
        state=media_state(driver)
        if state and state['jobId']==tracking['job_id'] and state['operation']=='tracking':
            if state['MediaError']['code']:raise RuntimeError('MediaError '+str(state['MediaError']))
            if state['readyState']>=2 and state['videoWidth']>0 and state['videoHeight']>0:return state
        return False
    state=WebDriverWait(driver,30).until(ready)
    if play:
        driver.find_element(By.CSS_SELECTOR,'[data-video-play]').click()
        WebDriverWait(driver,15).until(lambda _:media_state(driver)['currentTime']>.1 and not media_state(driver)['paused'])
        state=media_state(driver)
        driver.find_element(By.CSS_SELECTOR,'[data-video-play]').click()
    return state

def start_server(token,jobs=None):
    server=create_server(ROOT,DATA,token,0)
    if jobs:
        server.service.records.update({r['job_id']:r for r in jobs.values()})
        server.service.save_project({'job_ids':[jobs[k]['job_id'] for k in ('segment','upscale','tracking')]})
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    return server,thread,f'http://127.0.0.1:{server.server_port}'

def stop(server,thread):
    server.shutdown();thread.join(timeout=30);server.server_close()

def external_dependencies(base_url):
    client=MarketingShortformClient.from_env()
    token_present=bool(os.environ.get('MARKETING_SHORTFORM_BRIDGE_TOKEN','').strip())
    missing=[]
    if not token_present:missing.append('MARKETING_SHORTFORM_BRIDGE_TOKEN for the actual Marketing provider')
    try:
        health=requests.get(client.base_url+'/v1/shortform/health',timeout=client.timeout_seconds)
        provider={'health_http_status':health.status_code,'reachable':True}
        if health.status_code!=200:missing.append('Marketing provider health HTTP 200')
    except requests.RequestException:
        provider={'reachable':False};missing.append('actual Marketing runtime at '+client.base_url)
    if missing:
        result={'status':'BLOCKED_EXTERNAL_SHORTFORM_INTEGRATION','missing_dependencies':missing,
                'provider_base_url':client.base_url,'token_present':token_present,'provider':provider,
                'marketing_http_contract':'NOT_REACHED','approved_avora_asset':'NOT_REACHED',
                'shortform_preview':'NOT_REACHED','representative_approval':'NOT_REACHED','mp4_export':'NOT_REACHED',
                'mock_used':False,'auto_publish':False,'ad_spend':False}
        write('SHORTFORM_INTEGRATION_RESULT.json',result)
        return result
    # Actual integration credentials/assets must be resolved; no synthetic approvals.
    try:
        raw=client.approved_contract()
    except MarketingShortformClientError as error:
        result={'status':'BLOCKED_EXTERNAL_SHORTFORM_INTEGRATION','missing_dependencies':[str(error)],'mock_used':False}
        write('SHORTFORM_INTEGRATION_RESULT.json',result);return result
    raise RuntimeError('Real Marketing contract retrieved; full live shortform renderer verification remains required')

def receipt(status,error=None):
    for name in ('VIDEO_BROWSER_DIAGNOSTICS.json','VIDEO_TRACKING_ARTIFACTS_MANIFEST.json',
                 'H264_PREVIEW_PROBE.json','VIDEO_BROWSER_DECODE_RESULT.json','KOREAN_STT_RESULT.json',
                 'SAVE_REOPEN_RESULT.json','EXPORT_RESULT.json','SHORTFORM_INTEGRATION_RESULT.json'):
        if not (OUT/name).exists():write(name,{'status':'NOT_REACHED','blocked_by':status})
    write('EVIDENCE.json',{'status':status,'epoch':EPOCH,'source_commit':os.environ.get('GITHUB_SHA'),
        'github_run':os.environ.get('GITHUB_RUN_ID'),'gates':GATES,'error':error,
        'PHOTO_MODELS_RERUN':False,'UI_SSOT_CHANGED':'NO','main_changed':False,
        'employee_package_rebuilt':False,'pr23':'HOLD / DO NOT MERGE',
        'full_product_pass':status=='PASS_MINDLE_MEDIA_AI_FULL_PRODUCT_E2E_RUNTIME_VERIFIED'})
    write('PRODUCT_E2E_RUN_RECEIPT.json',{'status':status,'epoch':EPOCH,
          'run_id':os.environ.get('GITHUB_RUN_ID'),'source_commit':os.environ.get('GITHUB_SHA'),'gates':GATES})

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    subprocess.run(['python','scripts/validate_pc_work_control_plane.py'],cwd=ROOT,check=True)
    token=os.environ.get('HF_TOKEN','')
    if not token:raise RuntimeError('verified model vault credential unavailable')
    jobs=checkpoint();GATES['PHOTO']='FROZEN_PASS_REUSED_WITH_HASH_VERIFICATION'
    server,thread,base=start_server(token,jobs)
    driver=None;phase='FAIL_VIDEO_BROWSER_PREVIEW'
    try:
        driver=browser();driver.get(base)
        WebDriverWait(driver,30).until(lambda _:photo_ready(driver,jobs['upscale']['job_id']))
        diagnosis=diagnose(driver,base,jobs['tracking']);GATES['VIDEO_BROWSER_DIAGNOSTICS']=diagnosis
        response=requests.post(base+'/api/jobs/'+jobs['tracking']['job_id']+'/preview',json={},timeout=60)
        response.raise_for_status();tracking=response.json()
        write('H264_PREVIEW_PROBE.json',tracking['preview_derivative'])
        driver.execute_script("document.dispatchEvent(new CustomEvent('mindle:video-result',{detail:arguments[0]}));",tracking)
        state=decode(driver,tracking,play=True)
        media_response=requests.get(urljoin(base,state['currentSrc']),timeout=30)
        if media_response.status_code!=200 or hashlib.sha256(media_response.content).hexdigest()!=tracking['preview_output']['sha256']:
            raise RuntimeError('actual browser preview HTTP identity mismatch')
        GATES['VIDEO_BROWSER_DECODE']='PASS'
        write('VIDEO_BROWSER_DECODE_RESULT.json',{'status':'PASS','browser':state,'actual_playback':True,
              'http_status':media_response.status_code,'preview_sha256':tracking['preview_output']['sha256']})
        driver.find_element(By.CSS_SELECTOR,'[data-preview="video"]').screenshot(str(OUT/'VIDEO_AFTER.png'))
        (OUT/'VIDEO_AFTER_DOM.html').write_text(driver.page_source,encoding='utf-8')
        phase='FAIL_KOREAN_STT_UI_E2E'
        video=driver.find_element(By.CSS_SELECTOR,'[data-editor="video"]')
        audio=FROZEN/'inputs/fleurs_ko_kr_test_row0.wav'
        if digest(audio)!='e6bc095e55046de927d7c937f036f96ebb506570648ad9ae7c6576febfc4746a':
            raise RuntimeError('immutable Korean audio checkpoint SHA mismatch')
        video.find_element(By.CSS_SELECTOR,'[data-primary-input="video"]').send_keys(str(audio))
        video.find_element(By.CSS_SELECTOR,'[data-command="video"]').send_keys('한국어 음성을 실제 텍스트로 변환해줘',Keys.ENTER)
        def transcript_ready(_):
            message=video.find_element(By.CSS_SELECTOR,'[data-command-error]')
            if message.get_attribute('data-result')=='error':raise RuntimeError(message.text)
            result=next((r for r in server.service.records.values() if r.get('operation')=='transcribe' and r.get('status')=='TESTED_PASS'),None)
            if not result or result['runtime_result']['text'] not in message.text:return False
            if media_state(driver)['jobId']!=tracking['job_id']:raise RuntimeError('STT replaced VIDEO tracking preview')
            return result
        stt=WebDriverWait(driver,300).until(transcript_ready)
        GATES['KOREAN_STT']='PASS'
        write('KOREAN_STT_RESULT.json',{'status':'PASS','backend_job':stt,'ui_transcript_visible':True,'tracking_preserved':True,'input':file_info(audio)})
        phase='FAIL_SAVE_REOPEN_E2E'
        photo=driver.find_element(By.CSS_SELECTOR,'[data-editor="photo"]')
        photo.find_element(By.CSS_SELECTOR,'[data-action="save"]').click()
        WebDriverWait(driver,30).until(lambda _:photo.get_attribute('data-project-status')=='saved')
        saved=server.service.latest_project();project_id=saved['project_id']
        before=file_info(DATA/'projects'/f'{project_id}.json')
        driver.quit();driver=None;stop(server,thread);server=None
        server,thread,base=start_server(token)
        driver=browser();driver.get(base)
        WebDriverWait(driver,30).until(lambda _:photo_ready(driver,jobs['upscale']['job_id']))
        decode(driver,tracking)
        WebDriverWait(driver,30).until(lambda _:stt['runtime_result']['text'] in driver.find_element(By.CSS_SELECTOR,'[data-editor="video"] [data-command-error]').text)
        reopened=server.service.latest_project()
        if reopened!=saved or digest(DATA/'projects'/f'{project_id}.json')!=before['sha256']:
            raise RuntimeError('saved project identity changed after full server/browser close')
        for record in reopened['jobs']:
            for item in record['outputs']:
                if digest(Path(item['path']))!=item['sha256']:raise RuntimeError('reopened output hash mismatch')
        GATES['SAVE_CLOSE_REOPEN']='PASS'
        write('SAVE_REOPEN_RESULT.json',{'status':'PASS','fully_closed_browser_and_server':True,'project_id':project_id,
            'saved_project':before,'restored_job_ids':reopened['job_ids'],'all_output_hashes_verified':True,
            'photo_upscale_restored':True,'tracking_restored':True,'stt_visible_after_reopen':True})
        driver.save_screenshot(str(OUT/'REOPENED_UI.png'))
        phase='FAIL_EXPORT_E2E'
        photo=driver.find_element(By.CSS_SELECTOR,'[data-editor="photo"]')
        photo.find_element(By.CSS_SELECTOR,'[data-action="export"]').click()
        WebDriverWait(driver,30).until(lambda _:photo.get_attribute('data-export-status')=='exported')
        exported=DATA/'projects'/f'{project_id}_export.zip'
        with zipfile.ZipFile(exported) as archive:
            if archive.testzip() is not None:raise RuntimeError('export ZIP CRC failure')
            if len(archive.namelist())!=len(set(archive.namelist())):raise RuntimeError('duplicate output entries')
            exported_project=json.loads(archive.read('project.json'))
            for record in exported_project['jobs']:
                for item in record['outputs']:
                    name=f"jobs/{record['job_id']}/{Path(item['path']).name}"
                    if hashlib.sha256(archive.read(name)).hexdigest()!=item['sha256']:raise RuntimeError('exported member hash mismatch')
            members=archive.namelist()
        if photo.get_attribute('data-export-sha256')!=digest(exported):raise RuntimeError('UI export SHA mismatch')
        downloaded=WORK/'downloads'/exported.name
        WebDriverWait(driver,30).until(lambda _:downloaded.is_file() and digest(downloaded)==digest(exported))
        GATES['EXPORT']='PASS'
        write('EXPORT_RESULT.json',{'status':'PASS','export':file_info(exported),'zip_crc':'PASS','members':members,'ui_export_sha_matches':True,'browser_download':file_info(downloaded)})
        phase='FULL_PRODUCT_E2E_PASS_FORBIDDEN'
        external=external_dependencies(base);GATES['SHORTFORM']=external
        if external['status']=='BLOCKED_EXTERNAL_SHORTFORM_INTEGRATION':
            receipt('BLOCKED_EXTERNAL_SHORTFORM_INTEGRATION');raise SystemExit(3)
        raise RuntimeError('full product PASS requires actual approved shortform MP4 evidence')
    except Exception as error:
        if driver:
            write('FAILURE_BROWSER_STATE.json',{'phase':phase,'browser':media_state(driver),'console':driver.get_log('browser')})
            driver.save_screenshot(str(OUT/'FAILED_UI.png'))
            (OUT/'FAILED_DOM.html').write_text(driver.page_source,encoding='utf-8')
        receipt(phase,str(error));raise
    finally:
        if driver:driver.quit()
        if server:stop(server,thread)

if __name__=='__main__':main()
