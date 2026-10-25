"""Read-only preflight for the owner's real 30-second architecture acceptance inputs.

Declared rights/labels are intake records, not automatic legal or semantic proof.
Never downloads assets, replaces models, builds a package, or invents missing input.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess


def validate_intake(manifest: dict, base: Path) -> dict:
    errors=[];verified=[]
    if not isinstance(manifest,dict):manifest={}
    def require(condition,message):
        if not condition:errors.append(message)
    require(manifest.get('duration_seconds')==30,'30-second delivery required')
    require(manifest.get('aspect')=='16:9','16:9 delivery required')
    require(isinstance(manifest.get('narration_script'),str) and 1<=len(manifest['narration_script'].strip())<=3000 and not any(c in manifest['narration_script'] for c in ('"','“','”')),'exact Korean narration script missing or incompatible with quoted product command')
    require(manifest.get('voice_length_policy') in {'reject','extend_video'},'explicit voice length policy missing')
    volumes=manifest.get('volumes',{})
    if not isinstance(volumes,dict):volumes={}
    for role in ('narration','original','bgm'):
        number=volumes.get(role)
        upper=1 if role=='bgm' else 2
        require(type(number) in (int,float) and math.isfinite(number) and 0<=number<=upper,f'explicit {role} volume required (0..{upper})')
    clips=manifest.get('clips',[])
    require(isinstance(clips,list) and 1<=len(clips)<=12,'1..12 real video clips required')
    bgm=manifest.get('bgm')
    require(isinstance(bgm,dict),'BGM and its permission record required')
    rows=[('video',x) for x in clips] if isinstance(clips,list) else []
    if isinstance(bgm,dict):rows.append(('audio',bgm))
    for role,item in rows:
        if not isinstance(item,dict):errors.append(f'invalid {role} entry');continue
        label=str(item.get('label',''))
        require(bool(label.strip()),f'{role}: supplied scene/track label missing')
        require(item.get('rights_status')=='CONFIRMED' and bool(item.get('source_or_owner')) and bool(item.get('license_or_permission')),f'{label}: provenance/permission missing')
        if role=='video':require(item.get('origin')=='real_capture',f'{label}: real capture declaration missing')
        if manifest.get('require_rights_evidence'):
            require(isinstance(item.get('rights_evidence'),str) and bool(item['rights_evidence'].strip()),f'{label}: rights evidence reference missing')
        candidate=item.get('path')
        if not isinstance(candidate,str) or not candidate.strip():errors.append(f'{label}: local path missing');continue
        path=(base/candidate).resolve()
        if not path.is_file():errors.append(f'{label}: local file missing');continue
        if role=='audio':
            require(0<path.stat().st_size<=32*1024*1024 and path.suffix.lower() in {'.wav','.mp3','.m4a','.flac','.ogg'},f'{label}: product BGM format/32MB limit')
        with path.open('rb') as stream:digest=hashlib.file_digest(stream,'sha256').hexdigest()
        require(digest==item.get('sha256'),f'{label}: SHA-256 mismatch')
        require(type(item.get('bytes')) is int and path.stat().st_size==item['bytes'],f'{label}: byte size mismatch')
        try:
            info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],text=True,timeout=30))
            streams=info.get('streams',[]);stream=next(x for x in streams if x.get('codec_type')==role)
            duration=float(info['format']['duration'])
            require(math.isfinite(duration) and duration>0,f'{label}: invalid duration')
            require(type(item.get('duration_seconds')) in (int,float) and abs(duration-item['duration_seconds'])<=.05,f'{label}: declared duration mismatch')
            start,end=0.0,duration
            if role=='video':
                require(item.get('width')==stream.get('width') and item.get('height')==stream.get('height'),f'{label}: resolution mismatch')
                start=item.get('usable_start_seconds',0);end=item.get('usable_end_seconds',duration)
                valid=all(type(x) in (int,float) and math.isfinite(x) for x in (start,end)) and 0<=start<end<=duration+.01
                require(valid and end-start>=.25,f'{label}: invalid usable source range')
                if not valid:start=end=0.0
            verified.append({'role':role,'label':label,'path':str(path),'sha256':digest,'bytes':path.stat().st_size,'duration_seconds':duration,'codec':stream.get('codec_name'),'usable_start_seconds':start,'usable_end_seconds':end,'has_original_audio':any(x.get('codec_type')=='audio' for x in streams)})
        except (OSError,subprocess.SubprocessError,StopIteration,ValueError,KeyError) as error:
            errors.append(f'{label}: media probe failed ({type(error).__name__})')
    require(sum(min(30,x['usable_end_seconds']-x['usable_start_seconds']) for x in verified if x['role']=='video')>=30,'source coverage below 30 seconds')
    if type(volumes.get('original')) in (int,float) and volumes['original']>0:
        require(any(x['role']=='video' and x['has_original_audio'] for x in verified),'original volume requested but no clip has original audio')
    return {'status':'BLOCKED_ASSET_INTAKE' if errors else 'PASS_INTAKE_TECHNICAL_ONLY',
            'errors':errors,'verified_assets':verified,'rights_review':'DECLARATIONS_ONLY_REQUIRES_OWNER_CONFIRMATION',
            'scene_labels':'USER_SUPPLIED_NOT_MODEL_VISION','human_visual_review':'NOT_EXECUTED',
            'human_audio_review':'NOT_EXECUTED','full_product_pass':False}


def intake_result(path):
    path=Path(path).resolve();raw=path.read_bytes()
    result=validate_intake(json.loads(raw.decode('utf-8-sig')),path.parent)
    result.update(manifest_path=str(path),manifest_sha256=hashlib.sha256(raw).hexdigest(),
                  authoritative_input='INPUT_MANIFEST',historical_intake_reports_are_not_authority=True)
    return result


def write_result(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    pending=path.with_suffix(path.suffix+'.tmp')
    pending.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');pending.replace(path)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('manifest');parser.add_argument('--output',required=True)
    parser.add_argument('--status-output',help='Derived ASSET_INTAKE snapshot; never an independent approval')
    args=parser.parse_args();result=intake_result(args.manifest)
    write_result(args.output,result)
    if args.status_output:write_result(args.status_output,result)
    print(result['status'])
    raise SystemExit(2 if result['errors'] else 0)


if __name__=='__main__':main()
