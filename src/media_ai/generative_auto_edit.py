"""Measured input -> pinned local inference -> bounded edit -> technical output gate.

Frame measurements are not semantic vision. No classifier or preset substitutes
for an unavailable generative model, and technical quality is not artistic approval.
"""
from __future__ import annotations
import hashlib
import json
import math
import re
from pathlib import Path
from uuid import uuid4
from .video_analysis import analyze_video

KIND = 'MEASURED_GENERATIVE_AUTO_EDIT'


def _decision(parsed, analysis):
    if not isinstance(parsed, dict) or set(parsed) != {'start','brightness','contrast','saturation','reason'}:
        raise ValueError('AI_AUTO_INVALID_DECISION')
    if not isinstance(parsed['reason'], str) or not 1 <= len(parsed['reason'].strip()) <= 500:
        raise ValueError('AI_AUTO_REASON_REQUIRED')
    length = analysis['duration']
    last = max(0.0, analysis['source_duration']-length)
    candidates = sorted({0.0, round(last,3), *[round(min(last, s['second']),3) for s in analysis['samples']]})
    for key in ('start','brightness','contrast','saturation'):
        if type(parsed[key]) not in (int,float) or not math.isfinite(parsed[key]):
            raise ValueError('AI_AUTO_NONFINITE_DECISION')
    if not any(abs(parsed['start']-value) < .0001 for value in candidates):
        raise ValueError('AI_AUTO_UNMEASURED_RANGE')
    if any(abs(parsed[key]) > 12 for key in ('brightness','contrast','saturation')):
        raise ValueError('AI_AUTO_EXCESSIVE_CORRECTION')
    selected=[item for item in analysis['samples'] if parsed['start'] <= item['second'] < parsed['start']+length]
    exposure=sum(item['exposure'] for item in selected)/len(selected) if selected else None
    if exposure is None or (exposure < 80 and parsed['brightness'] <= 0) or (exposure > 176 and parsed['brightness'] >= 0):
        raise ValueError('AI_AUTO_IGNORED_EXPOSURE: 측정한 과소·과다 노출을 무시한 판단입니다.')
    return {key:parsed[key] for key in ('start','brightness','contrast','saturation')} | {'duration':length}


def _source(service, identifier):
    from .product_runtime import file_record
    record = service.records.get(identifier)
    if not record or record.get('status') != 'TESTED_PASS' or record.get('lane') != 'video':
        raise ValueError('AI_AUTO_VIDEO_INPUT_REQUIRED')
    artifact = record.get('preview_output',record['primary_output'])
    path = Path(artifact['path']).resolve()
    if service.root.resolve() not in path.parents:
        raise ValueError('AI_AUTO_INPUT_OUTSIDE_PRODUCT')
    actual = file_record(path)
    if actual['sha256'] != artifact.get('sha256') or actual['bytes'] != artifact.get('bytes'):
        raise ValueError('AI_AUTO_INPUT_IDENTITY_MISMATCH')
    return record, actual


def make_auto_plan(service, request):
    from .workflow_planner import invoke_local_json_plan, persist_plan
    from .durable_workflows import validate_steps
    if not re.fullmatch(r'(?:AI\s*)?자동\s*편집(?:해\s*줘|해\s*주세요|해)?[.!]?',str(request.get('command','')).strip(),re.I):
        raise ValueError('AI_AUTO_EXPLICIT_INTENT_REQUIRED')
    record, artifact = _source(service,request.get('input_job_id'))
    # This API has one narrow intent. Compound explicit requests use the regular
    # model planner, where exact user numbers/scripts are independently checked.
    if set(request)-{'input_job_id','command'}:
        raise ValueError('AI_AUTO_UNSUPPORTED_REQUEST_FIELD')
    analysis = analyze_video(Path(artifact['path']),30)
    if analysis['duration'] < .25:
        raise ValueError('AI_AUTO_SOURCE_TOO_SHORT')
    schema = {'type':'object','properties':{
        **{key:{'type':'number'} for key in ('start','brightness','contrast','saturation')},
        'reason':{'type':'string'}},'required':['start','brightness','contrast','saturation','reason'], 'additionalProperties':False}
    mean_exposure=sum(s['exposure'] for s in analysis['samples'])/len(analysis['samples'])
    last=max(0.0,analysis['source_duration']-analysis['duration'])
    starts=sorted({0.0,round(last,3),*[round(min(last,s['second']),3) for s in analysis['samples']]})
    if len(starts)>12:starts=[starts[round(i*(len(starts)-1)/11)] for i in range(12)]
    windows=[]
    for start in starts:
        samples=[s for s in analysis['samples'] if start <= s['second'] < start+analysis['duration']]
        windows.append({'start':start,'mean_exposure':sum(s['exposure'] for s in samples)/len(samples),'mean_motion':sum(s['motion'] for s in samples)/len(samples),'mean_sharpness':sum(s['sharpness'] for s in samples)/len(samples)})
    observation={'mean_exposure_0_to_255':mean_exposure,'acceptable_exposure_band':[80,176],
                 'source_duration':analysis['source_duration'],'output_duration':analysis['duration'],'candidate_starts':starts}
    examples=[({'mean_exposure_0_to_255':60,'candidate_starts':[0]}, {'start':0,'brightness':6,'contrast':0,'saturation':0,'reason':'평균 노출 60이 낮아 밝기를 보정합니다.'}),
              ({'mean_exposure_0_to_255':196,'candidate_starts':[0]}, {'start':0,'brightness':-4,'contrast':0,'saturation':0,'reason':'평균 노출 196이 높아 밝기를 낮춥니다.'}),
              ({'mean_exposure_0_to_255':120,'candidate_starts':[0]}, {'start':0,'brightness':0,'contrast':0,'saturation':0,'reason':'평균 노출 120이 범위 안에 있어 유지합니다.'})]
    demonstrations=''.join('<|im_start|>user\nOBSERVATION='+json.dumps(question)+'<|im_end|>\n<|im_start|>assistant\n'+json.dumps(answer,ensure_ascii=False)+'<|im_end|>\n' for question,answer in examples)
    prompt = ('<|im_start|>system\nYou are a local video edit decision maker. '
              'Use the supplied measured exposure, motion and sharpness to select a source window and conservative color corrections. '
              'Return start, brightness, contrast, saturation, reason as JSON only. '
              'Choose start from sampled second values clamped to source_duration-duration, or zero or that final boundary. '
              'Corrections are signed relative points in [-12,12]; zero preserves the control. '
              'Zero motion or zero sharpness does NOT mean exposure is correct. '
              'If measured exposure is below 80, brightness MUST be positive. Above 176, brightness MUST be negative. '
              'Choose the magnitude yourself from 1 to 12 points; the validator rejects an ignored or reversed exposure correction. '
              'For exposure within [80,176], choose conservative corrections or preserve controls. '
              'Explain using the actual measured exposure number; write the reason in Korean. '
              'Do not invent scene objects, architecture types or semantic vision. Explain your decision from numeric measurements only. '
              'Do not add narration, external resources, camera moves or new scenes. '
              '<|im_end|>\n'+demonstrations+'<|im_start|>user\nOBSERVATION='+json.dumps(observation)+'\nMEASUREMENTS='+json.dumps(windows)+
              '\nREQUEST=Make the actual decision for OBSERVATION and MEASUREMENTS above. Use their measured exposure value, not an example. Return the edit JSON now.<|im_end|>\n<|im_start|>assistant\n')
    parsed, raw, settings = invoke_local_json_plan(service.root,prompt,schema,max_tokens=768,timeout=120)
    audit=service.root/'workflows/auto-decision-audit'/str(uuid4());audit.mkdir(parents=True)
    (audit/'response.txt').write_bytes(raw.encode('utf-8'))
    audit_value={'status':'PENDING_VALIDATION','input_sha256':artifact['sha256'],'model_sha256':settings['model_sha256'],'raw_response_sha256':hashlib.sha256(raw.encode('utf-8')).hexdigest(),'decision':parsed}
    try:
        options = _decision(parsed,analysis)
    except ValueError as error:
        audit_value.update(status='REJECTED',error=str(error))
        (audit/'DECISION.json').write_text(json.dumps(audit_value,ensure_ascii=False,indent=2),encoding='utf-8')
        raise
    audit_value['status']='ACCEPTED_DECISION_NOT_EXECUTION'
    (audit/'DECISION.json').write_text(json.dumps(audit_value,ensure_ascii=False,indent=2),encoding='utf-8')
    _record, after = _source(service,record['job_id'])
    if after['sha256'] != artifact['sha256']:
        raise ValueError('AI_AUTO_INPUT_CHANGED_DURING_INFERENCE')
    steps = validate_steps([{'operation':'video_edit','options':options}])
    plan = persist_plan(service.root,{'task_kind':KIND,'plan_source':'LOCAL_GENERATIVE_INFERENCE',
        'input_job_id':record['job_id'],'input_sha256':artifact['sha256'],'input_artifact':artifact,
        'analysis':analysis,'decision':parsed,'steps':steps,'validated_edit_values':options,
        'model_id':settings.get('model_id'),'model_sha256':settings['model_sha256'],
        'additional_model_sha256':[part['sha256'] for part in settings.get('additional_model_files',[])],
        'context_size':settings.get('context_size'),
        'revision':settings['revision'],'license':settings['license'],'executable_sha256':settings['executable_sha256'],
        'runtime_sha256':settings.get('runtime_sha256'),'raw_response_sha256':hashlib.sha256(raw.encode('utf-8')).hexdigest(),
        'semantic_understanding':False,'output_quality':'REQUIRED_BEFORE_PUBLICATION'},request)
    (service.root/'workflows/plans'/(plan['plan_id']+'.response.txt')).write_bytes(raw.encode('utf-8'))
    return plan


def validate_auto_binding(root, plan, source, actual):
    if plan.get('task_kind') != KIND:
        return
    if source['job_id'] != plan.get('input_job_id') or actual['sha256'] != plan.get('input_sha256'):
        raise ValueError('AI_AUTO_PLAN_INPUT_MISMATCH')
    raw = (Path(root)/'workflows/plans'/(plan['plan_id']+'.response.txt')).read_bytes()
    if hashlib.sha256(raw).hexdigest() != plan.get('raw_response_sha256'):
        raise ValueError('AI_AUTO_INFERENCE_RESPONSE_CHANGED')
    start = raw.find(b'{')
    if start < 0:
        raise ValueError('AI_AUTO_INVALID_INFERENCE_RESPONSE')
    parsed,_ = json.JSONDecoder().raw_decode(raw[start:].decode('utf-8'))
    options = _decision(parsed,plan['analysis'])
    if parsed != plan.get('decision') or len(plan['steps']) != 1 or plan['steps'][0]['options'] != options:
        raise ValueError('AI_AUTO_DECISION_EXECUTION_MISMATCH')


def assess_auto_output(plan, result):
    from .workflow_worker import probe
    output = result['primary_output']
    info = probe(Path(output['path']))
    video = next((s for s in info['streams'] if s['codec_type']=='video'),{})
    expected = plan['steps'][0]['options']['duration']
    duration = float(info['format']['duration'])
    if video.get('codec_name') != 'h264' or abs(duration-expected) > max(.15, expected*.02):
        raise ValueError('AI_AUTO_OUTPUT_STREAM_OR_DURATION_FAILED')
    measured = analyze_video(Path(output['path']),expected)
    samples = measured['samples']
    usable = sum(s['usable'] for s in samples)/len(samples)
    if usable < .5:
        raise ValueError('AI_AUTO_OUTPUT_QUALITY_REJECTED: 과반 프레임의 노출이 검수 범위를 벗어났습니다. 원본은 보존합니다.')
    options=plan['steps'][0]['options']
    originals=[s for s in plan['analysis']['samples'] if options['start'] <= s['second'] < options['start']+expected]
    before=sum(s['exposure'] for s in originals)/len(originals)
    after=sum(s['exposure'] for s in samples)/len(samples)
    distance=lambda value:max(80-value,0,value-176)
    if distance(before)>0 and distance(after)>=distance(before)-1:
        raise ValueError('AI_AUTO_OUTPUT_DID_NOT_IMPROVE_EXPOSURE')
    return {'status':'PASS_TECHNICAL_ONLY','output_sha256':output['sha256'],'duration_seconds':duration,
            'video_codec':video['codec_name'],'source_window_exposure':before,'output_exposure':after,'exposure_error_before':distance(before),'exposure_error_after':distance(after),'usable_frame_ratio':usable,'sample_count':len(samples),
            'semantic_quality':'NOT_EVALUATED','human_visual_approval':'REQUIRED','full_product_pass':False}
