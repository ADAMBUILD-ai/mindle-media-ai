"""Local-only generative adapter, with explicit plans kept distinct from inference."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import subprocess
import re
from uuid import uuid4
from .durable_workflows import validate_steps
from .workflow_worker import engines_config


def capabilities(root):
    config=engines_config(root)
    planner=config.get('planner',{});tts=config.get('tts',{})
    return {'generative_planner':'CONFIGURED_NOT_INFERENCE_VERIFIED' if planner else 'LOCAL_GENERATIVE_MODEL_UNAVAILABLE',
            'generative_required_resources':'pinned local instruct GGUF + model-card/license + sha256 + llama-cli with JSON plan output; no provider API key used',
            'tts':'CONFIGURED_NOT_SYNTHESIS_VERIFIED' if tts else 'TTS_ENGINE_UNAVAILABLE',
            'durable_queue':True,'running_cancel':True,'bounded_retry':True,'external_provider_connected':False}

def persist_plan(root,value,request):
    folder=Path(root)/'workflows/plans';folder.mkdir(parents=True,exist_ok=True)
    value={**value,'plan_id':str(uuid4()),'command_sha256':hashlib.sha256(str(request.get('command','')).encode()).hexdigest()}
    (folder/(value['plan_id']+'.json')).write_text(json.dumps(value,ensure_ascii=False),encoding='utf-8')
    return value

def make_plan(root,request):
    if request.get('steps') is not None:
        return persist_plan(root,{'plan_source':'STRUCTURED_USER_PLAN_NOT_GENERATIVE','steps':validate_steps(request['steps'])},request)
    command=str(request.get('command','')).strip()
    if not command or len(command)>4000:raise ValueError('편집 지시는1~4000자입니다.')
    settings=engines_config(root).get('planner',{})
    model=Path(settings.get('model_path',''));executable=Path(settings.get('executable',''))
    if not model.is_file() or not executable.is_file() or not settings.get('license') or not re.fullmatch(r'[0-9a-f]{40}',str(settings.get('revision',''))):
        raise ValueError('LOCAL_GENERATIVE_MODEL_UNAVAILABLE: 로컬 생성형 모델·고정 revision·라이선스·llama-cli가 필요합니다. 분류기를 생성형 계획기로 대체하지 않습니다.')
    for path,key in [(model,'model_sha256'),(executable,'executable_sha256')]:
        with path.open('rb') as stream:digest=hashlib.file_digest(stream,'sha256').hexdigest()
        if digest!=settings.get(key):raise ValueError('PLANNER_IDENTITY_MISMATCH')
    prompt='Return ONLY JSON {"steps":[...]}. Allowed operations: video_edit(options brightness/contrast/saturation/subtitle), transcribe, apply_subtitles, narrate(text), mix_narration(length_policy reject or extend_video). No file paths, code, shell or network. Korean editing request: '+command
    output=subprocess.check_output([str(executable),'-m',str(model),'-p',prompt,'-n','1024','--no-display-prompt'],text=True,timeout=120)
    start=output.find('{');end=output.rfind('}')
    parsed=json.loads(output[start:end+1]);steps=validate_steps(parsed['steps'])
    return persist_plan(root,{'plan_source':'LOCAL_GENERATIVE_INFERENCE','model_sha256':settings['model_sha256'],'revision':settings['revision'],'license':settings['license'],'steps':steps},request)
