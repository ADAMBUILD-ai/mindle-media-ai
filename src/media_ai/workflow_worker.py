"""One private workflow attempt. No output is published by this process."""
from __future__ import annotations
import base64
import errno
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import wave
from uuid import uuid4
from .product_runtime import ProductJobService, file_record, h264_encoder_args


def tree_sha(root):
    return hashlib.sha256('\n'.join(f'{p.relative_to(root).as_posix()}:{hashlib.sha256(p.read_bytes()).hexdigest()}' for p in sorted(root.rglob('*')) if p.is_file()).encode()).hexdigest()

def engines_config(root):
    path=Path(root)/'runtime-engines.json';bundled=False
    if not path.is_file():
        package=os.environ.get('MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT','').strip()
        if not package:return {}
        path=Path(package)/'RUNTIME_ENGINES.json';bundled=True
    if not path.is_file():return {}
    config=json.loads(path.read_text(encoding='utf-8'))
    for kind in ('tts','planner'):
        for field in ('executable','data_path','model_path'):
            value=config.get(kind,{}).get(field)
            if not value:continue
            resolved=(path.parent/Path(value)).resolve()
            if bundled and path.parent.resolve() not in resolved.parents and resolved!=path.parent.resolve():raise ValueError('BUNDLED_ENGINE_PATH_OUTSIDE_PACKAGE')
            config[kind][field]=str(resolved)
    return config

def narrate(service,text,config):
    settings=config.get('tts',{})
    executable=Path(settings.get('executable',''))
    data=Path(settings.get('data_path',''))
    if settings.get('engine')!='espeak-ng' or not executable.is_file() or not (data/'espeak-ng-data').is_dir():raise ValueError('TTS_ENGINE_UNAVAILABLE: 검증된 로컬 한국어 TTS가 필요합니다.')
    if file_record(executable)['sha256']!=settings.get('executable_sha256') or tree_sha(data/'espeak-ng-data')!=settings.get('data_sha256'):raise ValueError('TTS_ENGINE_IDENTITY_MISMATCH')
    version=subprocess.check_output([str(executable),'--path='+str(data),'--version'],text=True,timeout=10).strip()
    voices=subprocess.check_output([str(executable),'--path='+str(data),'--voices=ko'],text=True,timeout=10)
    if ' ko ' not in voices:raise ValueError('TTS_KOREAN_VOICE_UNAVAILABLE')
    identifier=str(uuid4());folder=service.jobs/identifier;folder.mkdir();script=folder/'narration.txt';script.write_text(text,encoding='utf-8');output=folder/'narration.wav'
    subprocess.run([str(executable),'--path='+str(data),'-v','ko','-s','165','-w',str(output),'-f',str(script)],check=True,capture_output=True,timeout=120)
    with wave.open(str(output),'rb') as audio:
        duration=audio.getnframes()/audio.getframerate();metadata={'sample_rate':audio.getframerate(),'channels':audio.getnchannels(),'duration_seconds':duration}
        if duration<=0 or audio.getsampwidth()!=2:raise ValueError('TTS_OUTPUT_INVALID')
    record={'status':'TESTED_PASS','job_id':identifier,'lane':'korean_audio','operation':'narration','command':'한국어 나레이션 생성',
        'primary_output':file_record(output),'input':file_record(script),'outputs':[file_record(output),file_record(script)],
        'runtime_result':{'engine':'eSpeak NG','engine_version':version,'engine_license':'GPL-3.0-or-later','engine_sha256':settings['executable_sha256'],'voice_data_sha256':settings['data_sha256'],
          'model_inference':False,'synthesis':'local formant synthesis, not neural TTS','text':text,'voice':'ko',**metadata,'human_hearing':'NOT_VERIFIED','naturalness':'NOT_BENCHMARKED'}}
    return record

def probe(path):
    package=os.environ.get('MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT')
    exe=str(Path(package)/'tools/ffmpeg/ffprobe.exe') if package else 'ffprobe'
    return json.loads(subprocess.check_output([exe,'-v','error','-show_streams','-show_format','-of','json',str(path)],timeout=30))

def mix_narration(service,video,voice,step,background=None):
    if video.get('runtime_result',{}).get('options',{}).get('narration_job_id'):raise ValueError('이미 나레이션이 합성된 영상입니다. 원본 영상을 선택해 중복 믹싱을 피하세요.')
    source=Path(video.get('preview_output',video['primary_output'])['path']);audio=Path(voice['primary_output']['path'])
    if file_record(source)['sha256']!=video.get('preview_output',video['primary_output'])['sha256'] or file_record(audio)['sha256']!=voice['primary_output']['sha256']:raise ValueError('WORKFLOW_INPUT_HASH_MISMATCH')
    if background and file_record(Path(background['path']))['sha256']!=background['sha256']:raise ValueError('BGM_INPUT_HASH_MISMATCH')
    # FFmpeg receives attempt-private copies, never the saved project's media paths.
    original_source,original_voice=source,audio
    source=service._store_input('mix_video.mp4',base64.b64encode(source.read_bytes()).decode())
    audio=service._store_input('mix_voice.wav',base64.b64encode(audio.read_bytes()).decode())
    if background:
        copied=service._store_input('mix_background'+Path(background['path']).suffix,base64.b64encode(Path(background['path']).read_bytes()).decode());background=file_record(copied)
    source_info,voice_info=probe(source),probe(audio)
    original_duration=float(source_info['format']['duration']);voice_duration=float(voice_info['format']['duration'])
    policy=step.get('length_policy','reject')
    if voice_duration>original_duration+.05 and policy=='reject':raise ValueError('NARRATION_LONGER_THAN_VIDEO: 음성을 줄이거나 영상 연장 정책을 선택하세요.')
    target=max(original_duration,voice_duration) if policy=='extend_video' else original_duration
    identifier=str(uuid4());folder=service.jobs/identifier;folder.mkdir();output=folder/'narrated_video.mp4'
    package=os.environ.get('MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT');exe=str(Path(package)/'tools/ffmpeg/ffmpeg.exe') if package else 'ffmpeg'
    command=[exe,'-y','-i',str(source),'-i',str(audio)]
    video_filter='scale=trunc(iw/2)*2:trunc(ih/2)*2,setsar=1'
    if target>original_duration:video_filter+=f',tpad=stop_mode=clone:stop_duration={target-original_duration}'
    filters=[f'[0:v]{video_filter},setpts=PTS-STARTPTS[video]',f"[1:a]aresample=48000,asetpts=N/SR/TB,volume={float(step.get('volume',1))}[voice]"]
    inputs=['[voice]']
    if any(s['codec_type']=='audio' for s in source_info['streams']):
        filters.append(f"[0:a]aresample=48000,asetpts=N/SR/TB,volume={float(step.get('original_volume',1))}[original]");inputs.append('[original]')
    if background:
        command+=['-stream_loop','-1','-i',str(background['path'])];filters.append(f"[2:a]aresample=48000,asetpts=N/SR/TB,volume={float(step.get('background_volume',.2))}[background]");inputs.append('[background]')
    filters.append(''.join(inputs)+f'amix=inputs={len(inputs)}:duration=longest:normalize=0,alimiter=limit=0.95:level=0:latency=1,apad=whole_dur={target},atrim=duration={target},asetpts=N/SR/TB[audio]')
    command+=['-filter_complex',';'.join(filters),'-map','[video]','-map','[audio]',*h264_encoder_args(package),'-c:a','aac','-t',str(target),'-movflags','+faststart',str(output)]
    subprocess.run(command,check=True,capture_output=True,timeout=600)
    if file_record(original_source)['sha256']!=video.get('preview_output',video['primary_output'])['sha256'] or file_record(original_voice)['sha256']!=voice['primary_output']['sha256']:raise ValueError('WORKFLOW_ORIGINAL_CHANGED_DURING_MIX')
    info=probe(output);v=next(s for s in info['streams'] if s['codec_type']=='video');a=next(s for s in info['streams'] if s['codec_type']=='audio')
    if v['codec_name']!='h264' or v.get('pix_fmt')!='yuv420p' or a['codec_name']!='aac':raise ValueError('MP4_CODEC_VALIDATION_FAILED')
    outputs=[file_record(output),file_record(audio)]+([background] if background else [])
    return {'status':'TESTED_PASS','job_id':identifier,'lane':'video','operation':'video_edit','command':'나레이션·원본 오디오·BGM 합성','input':file_record(source),
        'primary_output':file_record(output),'outputs':outputs,'runtime_result':{'engine':'FFmpeg','model_inference':False,'options':video.get('runtime_result',{}).get('options',{})|{'narrationVolume':float(step.get('volume',1)),'originalVolume':float(step.get('original_volume',1)),'lengthPolicy':policy,'narration_job_id':voice['job_id'],'backgroundVolume':float(step.get('background_volume',.2)) if background else None,'originalAudioIncluded':any(s['codec_type']=='audio' for s in source_info['streams']) and float(step.get('original_volume',1))>0},
        'duration_seconds':float(info['format']['duration']),'video_codec':v['codec_name'],'pixel_format':v['pix_fmt'],'audio_codec':a['codec_name'],'human_hearing':'NOT_VERIFIED'}}

def execute(request):
    service=ProductJobService(Path(request['root']),os.environ.get('HF_TOKEN',''))
    step=request['step'];records=request['records'];video=next((r for r in reversed(records) if r['lane']=='video'),request['input_record'])
    artifact=video.get('preview_output',video['primary_output']);path=Path(artifact['path']);content=path.read_bytes()
    if hashlib.sha256(content).hexdigest()!=artifact['sha256']:raise ValueError('WORKFLOW_INPUT_HASH_MISMATCH')
    payload={'filename':path.name,'content_base64':base64.b64encode(content).decode(),'options':step.get('options',{}),'command':'순차 작업'}
    if step['operation']=='video_edit':
        result=service.edit_video(payload)
        if video.get('runtime_result',{}).get('options',{}).get('narration_job_id'):result['runtime_result']['options']['narration_job_id']=video['runtime_result']['options']['narration_job_id']
        return result
    if step['operation']=='transcribe':return service.execute_isolated({**payload,'lane':'korean_audio','operation':'transcribe','request_id':str(uuid4())})
    if step['operation']=='apply_subtitles':
        transcript=next(r for r in reversed(records) if r['operation']=='transcribe')
        payload['options']={**step.get('options',{}),'subtitle':transcript['runtime_result']['text'],'subtitleSegments':transcript['runtime_result'].get('segments',[])}
        return service.edit_video(payload)
    if step['operation']=='narrate':
        result=narrate(service,step['text'],request.get('engines',{}));result['runtime_result']['base_video_job_id']=video['job_id'];return result
    if step['operation']=='mix_narration':
        voice=next(r for r in reversed(records+request.get('base_records',[])) if r['job_id']==step['voice_job_id']) if step.get('voice_job_id') else next(r for r in reversed(records) if r['operation']=='narration')
        return mix_narration(service,video,voice,step,request.get('background'))
    raise ValueError('Unsupported step')

def supervise_parent(parent_pid):
    import threading,time,signal
    def watch():
        if os.name=='nt':
            import ctypes
            kernel=ctypes.WinDLL('kernel32',use_last_error=True)
            kernel.OpenProcess.restype=ctypes.c_void_p
            handle=kernel.OpenProcess(0x00100000,False,parent_pid)
            if not handle:return
            while kernel.WaitForSingleObject(ctypes.c_void_p(handle),200)==258:pass
            subprocess.run(['taskkill','/PID',str(os.getpid()),'/T','/F'],capture_output=True)
        else:
            while os.getppid()==parent_pid:time.sleep(.2)
            os.killpg(os.getpgrp(),signal.SIGTERM)
    threading.Thread(target=watch,daemon=True).start()

if __name__=='__main__':
    path=Path(sys.argv[1]);request=json.loads(path.read_text(encoding='utf-8'));output=path.parent/'response.json'
    supervise_parent(request['parent_pid'])
    try:
        record=execute(request);output.write_text(json.dumps({'record':record},ensure_ascii=False),encoding='utf-8')
    except Exception as error:
        retryable=isinstance(error,(TimeoutError,ConnectionError)) or isinstance(error,OSError) and error.errno in {errno.EAGAIN,errno.EBUSY,errno.ETIMEDOUT}
        output.write_text(json.dumps({'error':str(error),'retryable':retryable,'error_type':type(error).__name__},ensure_ascii=False),encoding='utf-8');sys.exit(1)
