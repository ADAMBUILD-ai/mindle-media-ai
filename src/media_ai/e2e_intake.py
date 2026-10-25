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
    def require(condition,message):
        if not condition:errors.append(message)
    require(manifest.get('duration_seconds')==30,'30-second delivery required')
    require(manifest.get('aspect')=='16:9','16:9 delivery required')
    require(isinstance(manifest.get('narration_script'),str) and bool(manifest['narration_script'].strip()),'exact Korean narration script missing')
    require(manifest.get('voice_length_policy') in {'reject','extend_video'},'explicit voice length policy missing')
    volumes=manifest.get('volumes',{})
    for role in ('narration','original','bgm'):
        number=volumes.get(role)
        require(type(number) in (int,float) and math.isfinite(number) and 0<=number<=2,f'explicit {role} volume required (0..2)')
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
        candidate=item.get('path')
        if not isinstance(candidate,str) or not candidate.strip():errors.append(f'{label}: local path missing');continue
        path=(base/candidate).resolve()
        if not path.is_file():errors.append(f'{label}: local file missing');continue
        digest=hashlib.sha256(path.read_bytes()).hexdigest()
        require(digest==item.get('sha256'),f'{label}: SHA-256 mismatch')
        require(type(item.get('bytes')) is int and path.stat().st_size==item['bytes'],f'{label}: byte size mismatch')
        try:
            info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],text=True,timeout=30))
            streams=info.get('streams',[]);stream=next(x for x in streams if x.get('codec_type')==role)
            duration=float(info['format']['duration'])
            require(math.isfinite(duration) and duration>0,f'{label}: invalid duration')
            require(type(item.get('duration_seconds')) in (int,float) and abs(duration-item['duration_seconds'])<=.05,f'{label}: declared duration mismatch')
            if role=='video':
                require(item.get('width')==stream.get('width') and item.get('height')==stream.get('height'),f'{label}: resolution mismatch')
            verified.append({'role':role,'label':label,'path':str(path),'sha256':digest,'bytes':path.stat().st_size,'duration_seconds':duration,'codec':stream.get('codec_name')})
        except (OSError,subprocess.SubprocessError,StopIteration,ValueError,KeyError) as error:
            errors.append(f'{label}: media probe failed ({type(error).__name__})')
    require(sum(min(30,x['duration_seconds']) for x in verified if x['role']=='video')>=30,'source coverage below 30 seconds')
    return {'status':'BLOCKED_ASSET_INTAKE' if errors else 'PASS_INTAKE_TECHNICAL_ONLY',
            'errors':errors,'verified_assets':verified,'rights_review':'DECLARATIONS_ONLY_REQUIRES_OWNER_CONFIRMATION',
            'scene_labels':'USER_SUPPLIED_NOT_MODEL_VISION','human_visual_review':'NOT_EXECUTED',
            'human_audio_review':'NOT_EXECUTED','full_product_pass':False}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('manifest');parser.add_argument('--output',required=True)
    args=parser.parse_args();path=Path(args.manifest).resolve()
    manifest=json.loads(path.read_text(encoding='utf-8'))
    result=validate_intake(manifest,path.parent)
    result['manifest_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
    output=Path(args.output);output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(result['status'])
    raise SystemExit(2 if result['errors'] else 0)


if __name__=='__main__':main()
