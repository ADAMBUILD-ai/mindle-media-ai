"""Actual browser recovery gate: import, analyze/edit, play, persist, restart, export."""
import base64
import hashlib
import json
import os
import subprocess
import threading
import time
import zipfile
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from media_ai.product_server import create_server

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/evidence/media-ai-runtime-recovery-20261013'
OUT.mkdir(parents=True,exist_ok=True)
DATA=ROOT/'runtime_recovery_data'
checks=[]
def record(name,detail):
    checks.append({'check':name,'status':'PASS','detail':detail})
def media_state(driver):
    return driver.execute_script("const v=document.querySelector('[data-preview=video] video');return v?{error:v.error?.code||null,readyState:v.readyState,videoWidth:v.videoWidth,currentSrc:v.currentSrc,currentTime:v.currentTime,paused:v.paused}:null")
def serve():
    server=create_server(ROOT,DATA,'',0)
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    return server,thread
def close(server,thread):
    server.shutdown();thread.join(5);server.server_close()

def main():
    source=OUT/'SOURCE.mp4'
    subprocess.run(['ffmpeg','-y','-f','lavfi','-i','testsrc2=size=160x90:rate=12','-t','5','-c:v','libx264','-pix_fmt','yuv420p',str(source)],check=True,capture_output=True)
    from PIL import Image
    photo=OUT/'SOURCE_PORTRAIT.png';Image.new('RGB',(120,240),(80,100,120)).save(photo)
    options=webdriver.ChromeOptions();options.add_argument('--headless=new');options.add_argument('--no-sandbox');options.add_argument('--disable-dev-shm-usage');options.add_argument('--window-size=1920,1080')
    options.add_experimental_option('prefs',{'download.default_directory':str(OUT.resolve()),'download.prompt_for_download':False})
    driver=webdriver.Chrome(options=options);server,thread=serve()
    receipt={'source_commit':os.environ.get('GITHUB_SHA'),'status':'REWORK_RUNTIME_RECOVERY_INCOMPLETE','owner_pc_runtime_pass':False,'generative_ai_connected':False,'fresh_model_inference':False}
    try:
        driver.get(f'http://127.0.0.1:{server.server_port}');wait=WebDriverWait(driver,90)
        wait.until(lambda d:d.execute_script('return window.mindleRestoreReady'))
        driver.find_element(By.CSS_SELECTOR,'[data-primary-input=video]').send_keys(str(source.resolve()))
        wait.until(lambda d:(media_state(d) or {}).get('readyState',0)>=2)
        record('actual_import_media_diagnostics',media_state(driver))
        wait.until(lambda d:len(d.find_elements(By.CSS_SELECTOR,'[data-editor=video] [data-asset-job-id]'))==1)
        assert driver.find_element(By.CSS_SELECTOR,'[data-asset-job-id]').text=='SOURCE.mp4'
        record('actual_media_library_contains_user_import',driver.find_element(By.CSS_SELECTOR,'[data-asset-job-id]').text)
        driver.find_element(By.CSS_SELECTOR,'[data-action=ai-auto-edit]').click()
        wait.until(lambda d: d.execute_script("return document.querySelector('[data-preview=video]').dataset.operation==='video_edit' && !window.mindleEditPending('video')"))
        jobs=driver.execute_async_script("fetch('/api/evidence').then(r=>r.json()).then(arguments[0])")['jobs']
        job=[j for j in jobs.values() if j['operation']=='video_edit'][-1]
        assert job['runtime_result']['analysis']['sample_count']>0 and job['runtime_result']['options']['auto_edit'] is True
        assert job['runtime_result']['model_inference'] is False and not any(j['operation']=='tracking' for j in jobs.values())
        record('auto_edit_actual_button_analysis_not_tracking',job)
        wait.until(lambda d:(media_state(d) or {}).get('readyState',0)>=2)
        driver.execute_async_script("document.querySelector('[data-preview=video] video').play().then(()=>arguments[0](true)).catch(e=>arguments[0](String(e)))")
        wait.until(lambda d:media_state(d)['currentTime']>.3)
        assert media_state(driver)['error'] is None
        record('actual_h264_playback',media_state(driver))
        driver.find_element(By.CSS_SELECTOR,'[data-primary-input=photo]').send_keys(str(photo.resolve()))
        wait.until(lambda d:d.execute_script("const i=document.querySelector('[data-preview=photo] img');return i?.complete&&i.naturalWidth===120&&!window.mindleEditPending('photo')"))
        driver.find_element(By.CSS_SELECTOR,'[data-editor=photo] [data-action=photo-auto]').click()
        wait.until(lambda d:d.execute_script("return document.querySelector('[data-preview=photo]').dataset.operation==='photo_edit'&&!window.mindleEditPending('photo')"))
        photo_jobs=driver.execute_async_script("fetch('/api/evidence').then(r=>r.json()).then(arguments[0])")['jobs']
        auto_photo=[j for j in photo_jobs.values() if j['operation']=='photo_edit'][-1]
        assert auto_photo['runtime_result']['options']['automaticAnalysis']['sample_pixels']>0
        assert auto_photo['runtime_result']['options']['automaticAnalysis']['model_inference'] is False
        record('actual_photo_auto_measured_pixels_not_preset',auto_photo)
        wait.until(lambda d:d.execute_script("const i=document.querySelector('[data-preview=photo] img');return i?.complete&&i.naturalWidth===120"))
        driver.execute_script("const i=document.querySelector('[data-photo-adjust=brightness]');i.value=20;i.dispatchEvent(new Event('input',{bubbles:true}))")
        driver.find_element(By.CSS_SELECTOR,'[data-photo-apply]').click()
        wait.until(lambda d:d.execute_script("return document.querySelector('[data-preview=photo]').dataset.operation==='photo_edit'&&!window.mindleEditPending('photo')"))
        wait.until(lambda d:d.execute_script("const i=document.querySelector('[data-preview=photo] img');return i?.complete&&i.naturalWidth===120&&i.naturalHeight===240"))
        record('actual_portrait_correction',driver.execute_script("const i=document.querySelector('[data-preview=photo] img');return {width:i.naturalWidth,height:i.naturalHeight}"))
        driver.find_element(By.CSS_SELECTOR,'[data-editor=photo] [data-asset-job-id]').click()
        wait.until(lambda d:d.execute_script("return document.querySelector('[data-preview=photo]').dataset.operation==='import'&&!window.mindleEditPending('photo')"))
        selected_photo=driver.execute_script("return document.querySelector('[data-preview=photo]').dataset.jobId")
        record('actual_original_selection_changes_current_result',{'job_id':selected_photo})
        def edited(selector,label):
            old=driver.execute_script("return document.querySelector('[data-preview=video]').dataset.jobId")
            driver.find_element(By.CSS_SELECTOR,selector).click()
            wait.until(lambda d:d.execute_script("return document.querySelector('[data-preview=video]').dataset.jobId!==arguments[0]&&!window.mindleEditPending('video')",old))
            wait.until(lambda d:(media_state(d) or {}).get('readyState',0)>=2)
            jobs=driver.execute_async_script("fetch('/api/evidence').then(r=>r.json()).then(arguments[0])")['jobs']
            identifier=driver.execute_script("return document.querySelector('[data-preview=video]').dataset.jobId")
            result=jobs[identifier];record(label,result);return result
        for key in ('rotate','rotate','fade','effect'):
            edited('[data-video-tool='+key+']','actual_video_'+key)
        for toggle in ('denoise','stabilize'):
            driver.find_element(By.CSS_SELECTOR,'[data-video-toggle='+toggle+']').click()
            edited('[data-video-apply]','actual_video_'+toggle)
            driver.find_element(By.CSS_SELECTOR,'[data-video-toggle='+toggle+']').click()
        driver.find_element(By.CSS_SELECTOR,'[data-video-tool=speed]').click()
        driver.execute_script("document.querySelector('[data-video-option=speed]').value=1.25")
        speed_job=edited('[data-video-apply]','actual_video_speed');assert speed_job['runtime_result']['options']['speed']==1.25
        driver.find_element(By.CSS_SELECTOR,'[data-video-tool=trim]').click()
        driver.execute_script("document.querySelector('[data-video-option=start]').value=.2;document.querySelector('[data-video-option=duration]').value=1.2")
        edited('[data-video-apply]','actual_video_trim')
        driver.find_element(By.CSS_SELECTOR,'[data-video-tool=subtitle]').click()
        driver.find_element(By.CSS_SELECTOR,'[data-video-subtitle]').send_keys('실제 한국어 자막')
        edited('[data-video-apply]','actual_video_manual_korean_subtitle')
        driver.find_element(By.CSS_SELECTOR,'[data-video-subtitle]').clear()
        driver.find_element(By.CSS_SELECTOR,'[data-video-tool=split]').click()
        driver.execute_script("document.querySelector('[data-video-option=start]').value=.6")
        split_job=edited('[data-video-apply]','actual_video_split');assert len(split_job['outputs'])==2
        edited('[data-video-tool=shortform]','actual_video_9x16_shortform')
        assert media_state(driver)['videoWidth']==360
        for key in ('contrast','highlights','shadows','saturation','temperature','sharpness'):
            old=driver.execute_script("return document.querySelector('[data-preview=photo]').dataset.jobId")
            driver.execute_script("const i=document.querySelector('[data-photo-adjust='+arguments[0]+']');i.value=15;i.dispatchEvent(new Event('input',{bubbles:true}))",key)
            driver.find_element(By.CSS_SELECTOR,'[data-photo-apply]').click()
            wait.until(lambda d:d.execute_script("return document.querySelector('[data-preview=photo]').dataset.jobId!==arguments[0]&&!window.mindleEditPending('photo')",old))
            wait.until(lambda d:d.execute_script("const i=document.querySelector('[data-preview=photo] img');return i?.complete&&i.naturalWidth>0"))
            record('actual_photo_correction_'+key,{'job_id':driver.execute_script("return document.querySelector('[data-preview=photo]').dataset.jobId")})
        for key in ('rotate','rotate','flip-h','flip-v'):
            old=driver.execute_script("return document.querySelector('[data-preview=photo]').dataset.jobId")
            driver.find_element(By.CSS_SELECTOR,'[data-photo-tool='+key+']').click()
            wait.until(lambda d:d.execute_script("return document.querySelector('[data-preview=photo]').dataset.jobId!==arguments[0]&&!window.mindleEditPending('photo')",old))
            wait.until(lambda d:d.execute_script("const i=document.querySelector('[data-preview=photo] img');return i?.complete&&i.naturalWidth>0"))
            record('actual_photo_'+key,{'job_id':driver.execute_script("return document.querySelector('[data-preview=photo]').dataset.jobId")})
        for key in ('color','style','portrait'):
            old=driver.execute_script("return document.querySelector('[data-preview=photo]').dataset.jobId")
            driver.find_element(By.CSS_SELECTOR,'[data-photo-tool='+key+']').click()
            wait.until(lambda d:d.execute_script("return document.querySelector('[data-preview=photo]').dataset.jobId!==arguments[0]&&!window.mindleEditPending('photo')",old))
            wait.until(lambda d:d.execute_script("const i=document.querySelector('[data-preview=photo] img');return i?.complete&&i.naturalWidth>0"))
            record('actual_photo_'+key,{'job_id':driver.execute_script("return document.querySelector('[data-preview=photo]').dataset.jobId")})
        driver.find_element(By.CSS_SELECTOR,'[data-reference-input=photo]').send_keys(str(photo.resolve()))
        driver.find_element(By.CSS_SELECTOR,'[data-photo-tool=similar]').click()
        wait.until(lambda d:'SOURCE_PORTRAIT' in d.find_element(By.CSS_SELECTOR,'[data-photo-status]').text)
        record('actual_reference_color_similarity',{'text':driver.find_element(By.CSS_SELECTOR,'[data-photo-status]').text})
        driver.find_element(By.CSS_SELECTOR,'[data-photo-tool=resize]').click()
        driver.execute_script("document.querySelector('[data-photo-resize]').value=60")
        old=driver.execute_script("return document.querySelector('[data-preview=photo]').dataset.jobId")
        driver.find_element(By.CSS_SELECTOR,'[data-photo-apply]').click()
        wait.until(lambda d:d.execute_script("return document.querySelector('[data-preview=photo]').dataset.jobId!==arguments[0]&&!window.mindleEditPending('photo')",old))
        wait.until(lambda d:d.execute_script("const i=document.querySelector('[data-preview=photo] img');return i?.complete&&i.naturalWidth===60&&i.naturalHeight===120"))
        record('actual_photo_resize_original_ratio',{'dimensions':[60,120]})
        music=OUT/'BGM.wav'
        subprocess.run(['ffmpeg','-y','-f','lavfi','-i','sine=frequency=220:sample_rate=16000','-t','2',str(music)],check=True,capture_output=True)
        old=driver.execute_script("return document.querySelector('[data-preview=video]').dataset.jobId")
        driver.find_element(By.CSS_SELECTOR,'[data-bgm-input]').send_keys(str(music.resolve()))
        wait.until(lambda d:d.execute_script("return document.querySelector('[data-preview=video]').dataset.jobId!==arguments[0]&&!window.mindleEditPending('video')",old))
        assert driver.execute_script("return document.querySelector('[data-bgm-input]').files.length")==0
        record('actual_bgm_added_selection_consumed_once',{'job_id':driver.execute_script("return document.querySelector('[data-preview=video]').dataset.jobId")})
        follow=edited('[data-video-tool=effect]','actual_bgm_followup_without_readding_music')
        assert follow['runtime_result']['options']['backgroundAlreadyMixed'] is True
        # Return to the original before save; prove chosen current result survives restart.
        driver.find_element(By.CSS_SELECTOR,'[data-editor=photo] [data-asset-job-id]').click()
        wait.until(lambda d:d.execute_script("return document.querySelector('[data-preview=photo]').dataset.operation==='import'&&!window.mindleEditPending('photo')"))
        driver.find_element(By.CSS_SELECTOR,'[data-editor=video] [data-action=save]').click()
        wait.until(lambda d:d.execute_script("return document.querySelector('[data-editor=video]').dataset.projectStatus==='saved'"))
        saved=driver.execute_async_script("fetch('/api/projects/latest').then(r=>r.json()).then(arguments[0])")['project']
        driver.save_screenshot(str(OUT/'ACTUAL_UI.png'))
        driver.quit();close(server,thread)
        server,thread=serve();driver=webdriver.Chrome(options=options)
        driver.get(f'http://127.0.0.1:{server.server_port}');wait=WebDriverWait(driver,90)
        wait.until(lambda d:d.execute_script("return window.mindleRestoreReady&&document.querySelector('[data-editor=video]').dataset.projectStatus==='reopened'"))
        reopened=driver.execute_async_script("fetch('/api/projects/latest').then(r=>r.json()).then(arguments[0])")['project']
        assert reopened==saved
        assert driver.execute_script("return document.querySelector('[data-preview=photo]').dataset.jobId")==selected_photo
        assert len(driver.find_elements(By.CSS_SELECTOR,'[data-asset-job-id]'))==2
        record('actual_asset_library_survives_restart',{'assets':2})
        record('full_server_browser_restart_identical_saved_analysis',{'project_id':saved['project_id'],'job_ids':saved['job_ids']})
        driver.find_element(By.CSS_SELECTOR,'[data-editor=video] [data-action=export]').click()
        wait.until(lambda d:d.execute_script("return document.querySelector('[data-editor=video]').dataset.exportStatus==='exported'"))
        deadline=time.monotonic()+30
        archives=[]
        while time.monotonic()<deadline:
            archives=list(OUT.glob('*_export.zip'))
            if archives:break
            time.sleep(.2)
        assert len(archives)==1
        with zipfile.ZipFile(archives[0]) as archive:
            assert archive.testzip() is None
            doc=json.loads(archive.read('project.json'))
            for j in doc['jobs']:
                for output in j['outputs']:
                    assert hashlib.sha256(archive.read('jobs/'+j['job_id']+'/'+Path(output['path']).name)).hexdigest()==output['sha256']
        record('actual_browser_download_export_crc_and_media_hashes',{'file':archives[0].name,'sha256':hashlib.sha256(archives[0].read_bytes()).hexdigest()})
        receipt['status']='PASS_RUNTIME_RECOVERY_SCENE_EDIT_BROWSER_GATE'
    except Exception as error:
        receipt['error']=repr(error)
        receipt['media_diagnostics']=media_state(driver)
        driver.save_screenshot(str(OUT/'FAILURE.png'))
        raise
    finally:
        receipt['checks']=checks
        (OUT/'RUNTIME_RECEIPT.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
        driver.quit();close(server,thread)
if __name__=='__main__':main()
