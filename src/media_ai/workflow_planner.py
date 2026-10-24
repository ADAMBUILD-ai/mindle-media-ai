"""Local-only generative adapter, with explicit plans kept distinct from inference."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import subprocess
import re
from uuid import uuid4
from .durable_workflows import validate_steps
from .planner_constraints import instruction_text, validate_edit_values, requested_edit_fields
from .workflow_worker import engines_config, tree_sha


def invoke_local_json_plan(root, prompt, schema, *, max_tokens=768, timeout=120):
    """Run the pinned local planner and return parsed JSON plus an identity receipt.

    This is the single product boundary for generative planning. Callers supply a
    constrained schema and must still validate the returned domain semantics.
    """
    settings=engines_config(root).get('planner',{})
    model=Path(settings.get('model_path',''));executable=Path(settings.get('executable',''))
    if not model.is_file() or not executable.is_file() or not settings.get('license') or not re.fullmatch(r'[0-9a-f]{40}',str(settings.get('revision',''))):
        raise ValueError('LOCAL_GENERATIVE_MODEL_UNAVAILABLE: 로컬 생성형 모델·고정 revision·라이선스·llama-cli가 필요합니다. 분류기를 생성형 계획기로 대체하지 않습니다.')
    for path,key in [(model,'model_sha256'),(executable,'executable_sha256')]:
        with path.open('rb') as stream:digest=hashlib.file_digest(stream,'sha256').hexdigest()
        if digest!=settings.get(key):raise ValueError('PLANNER_IDENTITY_MISMATCH')
    if settings.get('runtime_sha256') and tree_sha(executable.parent)!=settings['runtime_sha256']:
        raise ValueError('PLANNER_RUNTIME_IDENTITY_MISMATCH')
    output=subprocess.check_output([
        str(executable),'-m',str(model),'-p',prompt,'-n',str(max_tokens),
        '--no-display-prompt','--no-conversation','--simple-io','--temp','0','-t','2',
        '--json-schema',json.dumps(schema),
    ],text=True,encoding='utf-8',timeout=timeout)
    start=output.find('{')
    if start < 0:raise ValueError('PLANNER_INVALID_JSON: 생성형 계획이 JSON을 반환하지 않았습니다.')
    try:parsed,_=json.JSONDecoder().raw_decode(output[start:])
    except json.JSONDecodeError as error:raise ValueError('PLANNER_INVALID_JSON: 생성형 계획 JSON을 해석할 수 없습니다.') from error
    return parsed,output,settings


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

def validate_plan_scope(command,steps):
    """Reject model-invented actions; this gate never generates a plan."""
    text=instruction_text(command)
    if re.search(r'자막|받아쓰|stt|subtitle|transcrib|나레이션|내레이션|narration|tts',text) and re.search(r'지\s*마|말|않|금지|하지|없이|제외|빼고|do not|don.t|never|without',text):
        raise ValueError('PLANNER_AMBIGUOUS_NEGATION: 음성·자막 부정 지시를 실행하지 않습니다. 수행할 작업만 명시하세요.')
    fields={'brightness':('밝기','밝게','brightness'),'contrast':('대비','contrast'),'saturation':('채도','saturation')}
    narration=any(word in text for word in ('나레이션','내레이션','narration','tts'))
    subtitles=any(word in text for word in ('받아쓰','자막','stt','transcrib','subtitle'))
    for step in steps:
        op=step['operation']
        if op=='video_edit':
            options=step.get('options',{})
            if not options or any(not any(word in text for word in fields.get(key,())) for key in options):
                raise ValueError('PLANNER_SCOPE_MISMATCH: 요청하지 않은 영상 보정입니다.')
        if op in {'transcribe','apply_subtitles'} and not subtitles:
            raise ValueError('PLANNER_SCOPE_MISMATCH: 요청하지 않은 받아쓰기·자막입니다.')
        if op in {'narrate','mix_narration'} and not narration:
            raise ValueError('PLANNER_SCOPE_MISMATCH: 요청하지 않은 나레이션입니다.')
        if op=='narrate' and step['text'] not in command:
            raise ValueError('PLANNER_SCRIPT_NOT_IN_REQUEST: 명시한 원고만 합성할 수 있습니다.')
    # A valid subset is not a completed plan: reject silently dropped requests.
    actual_fields={key for step in steps if step['operation']=='video_edit' for key in step.get('options',{})}
    expected_fields=requested_edit_fields(command)
    operations={step['operation'] for step in steps}
    if not expected_fields.issubset(actual_fields):
        raise ValueError('PLANNER_INCOMPLETE_PLAN: 요청한 영상 보정이 누락됐습니다.')
    if narration and not {'narrate','mix_narration'}.issubset(operations):
        raise ValueError('PLANNER_INCOMPLETE_PLAN: 요청한 나레이션 생성·합성이 누락됐습니다.')
    if subtitles and 'transcribe' not in operations:
        raise ValueError('PLANNER_INCOMPLETE_PLAN: 요청한 받아쓰기가 누락됐습니다.')
    if any(word in text for word in ('자막','subtitle')) and 'apply_subtitles' not in operations:
        raise ValueError('PLANNER_INCOMPLETE_PLAN: 요청한 자막 적용이 누락됐습니다.')
    validate_edit_values(command,steps)
    return steps


def make_plan(root,request):
    if request.get('steps') is not None:
        return persist_plan(root,{'plan_source':'STRUCTURED_USER_PLAN_NOT_GENERATIVE','steps':validate_steps(request['steps'])},request)
    command=str(request.get('command','')).strip()
    if not command or len(command)>4000:raise ValueError('편집 지시는1~4000자입니다.')
    if re.search(r'속도|자르|회전|전환|효과|배경음악|숏폼|추적|삭제|제거',re.sub(r'["“][^"”]*["”]', '', command)):
        raise ValueError('PLANNER_UNSUPPORTED: 대화 계획기는 밝기·대비·채도·받아쓰기·자막·명시 원고 나레이션을 지원합니다. 그 밖의 편집은 해당 도구를 사용하세요.')
    # Completion mode prevents interactive banners/prompt echoes contaminating JSON.
    # The model still chooses the operations and values; the grammar only constrains
    # the product's allowlisted wire format, never substitutes an intent classifier.
    schema={'type':'object','properties':{'steps':{'type':'array','maxItems':8,'items':{'type':'object','properties':{
        'operation':{'enum':['video_edit','transcribe','apply_subtitles','narrate','mix_narration']},
        'options':{'type':'object','properties':{key:{'type':'number'} for key in ('brightness','contrast','saturation')},'additionalProperties':False},
        'text':{'type':'string'},'length_policy':{'enum':['reject','extend_video']}
    },'required':['operation'],'additionalProperties':False}},'error':{'type':'string'}},'required':['steps'],'additionalProperties':False}
    instructions=('You translate Korean video edit requests into JSON. Output {"steps":[...]} only. '
      'Allowed step shapes: {"operation":"video_edit","options":{"brightness":10}}, '
      '{"operation":"video_edit","options":{"contrast":7}}, '
      '{"operation":"video_edit","options":{"saturation":5}}, '
      '{"operation":"transcribe"}, {"operation":"apply_subtitles"}, '
      '{"operation":"narrate","text":"EXACT USER SCRIPT"}, '
      '{"operation":"mix_narration","length_policy":"reject"}. '
      'Choose ONLY the requested steps; numeric values above are examples, use actual user values. '
      '밝기=brightness, 대비=contrast, 채도=saturation. '
      'Edit values are signed relative correction points, not absolute settings or percentages. '
      'For an explicit magnitude 0 to 100 use positive for 높이기/increase and negative for 낮추기/decrease. '
      'Omit controls the user says to preserve; never repeat the same control. '
      'Ambiguous magnitudes, absolute settings, unsupported units or negated speech/subtitle requests: return an error. '
      'Speech to subtitles: transcribe THEN apply_subtitles. Narration: narrate THEN mix_narration. '
      'If video extension requested use length_policy extend_video. Never invent a narration script. '
      'Unsupported request: {"error":"unsupported request"}. Do not output paths, commands or network actions.')
    examples=[('대비를 4 높여 주세요.',{'steps':[{'operation':'video_edit','options':{'contrast':4}}]}),
        ('음성을 받아쓰고 자막을 적용해 주세요.',{'steps':[{'operation':'transcribe'},{'operation':'apply_subtitles'}]}),
        ('밝기를 3 높이고 "반갑습니다" 나레이션을 넣고 영상을 연장해 주세요.',{'steps':[{'operation':'video_edit','options':{'brightness':3}},{'operation':'narrate','text':'반갑습니다'},{'operation':'mix_narration','length_policy':'extend_video'}]}),
        ('파일을 삭제해 줘.',{'steps':[],'error':'unsupported request'})]
    prompt='<|im_start|>system\n'+instructions+'<|im_end|>\n'
    for question,answer in examples:prompt+='<|im_start|>user\n'+question+'<|im_end|>\n<|im_start|>assistant\n'+json.dumps(answer,ensure_ascii=False)+'<|im_end|>\n'
    prompt+='<|im_start|>user\n'+command+'<|im_end|>\n<|im_start|>assistant\n' 
    parsed,output,settings=invoke_local_json_plan(root,prompt,schema)
    diagnostic=Path(root)/'workflows/planner-responses';diagnostic.mkdir(parents=True,exist_ok=True)
    (diagnostic/(str(uuid4())+'.txt')).write_text(output,encoding='utf-8')
    if parsed.get('error'):raise ValueError('PLANNER_UNSUPPORTED: '+str(parsed['error']))
    steps=validate_steps(parsed['steps'])
    validate_plan_scope(command,steps)
    if any(s['operation']=='narrate' for s in steps) and not any(s['operation']=='mix_narration' for s in steps):
        raise ValueError('PLANNER_INCOMPLETE_NARRATION_PLAN: 음성 생성 후 합성 단계가 필요합니다.')
    value=persist_plan(root,{'plan_source':'LOCAL_GENERATIVE_INFERENCE','model_sha256':settings['model_sha256'],'revision':settings['revision'],'license':settings['license'],'executable_sha256':settings['executable_sha256'],'runtime_sha256':settings.get('runtime_sha256'),'model_id':settings.get('model_id'),'raw_response_sha256':hashlib.sha256(output.encode()).hexdigest(),'steps':steps,'validated_edit_values':validate_edit_values(command,steps)},request)
    (Path(root)/'workflows/plans'/(value['plan_id']+'.response.txt')).write_text(output,encoding='utf-8')
    return value
