"""Current R2 eligibility, separate from the consumed R3 candidate authorization.

Reads real inputs and immutable runtime evidence; starts no process, inference,
workflow, installation or package build. Refresh never grants/revokes approval.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from media_ai.e2e_intake import intake_result

WORK_ID='MEDIA-AI-CORE-E2E-R2-20261025'
STATUS_FILE='CURRENT_MEDIA_WORK_STATUS.json'
DIRECTIVE='docs/commander/MINDLE_MEDIA_AI_R2_CURRENT_WORK_20261025.md'
MANIFEST='docs/handoff/media-ai-core-e2e-r2-20261025/INPUT_MANIFEST.json'
BASELINE='docs/evidence/media-ai-core-e2e-r2-20261025/SOURCE_VALIDATION.json'
BASELINE_SHA='2655b6e1d90c97859d0d4a4d2331002368f578e32192e62531d89e68ac6fbfc1'
FOUNDATION='docs/evidence/media-ai-core-e2e-r1-20261025/SOURCE_BINDING.json'
FOUNDATION_SHA='5a93616e83ff9cb935fdd9c85f30f4d9dffb49f20797ac544e9f379a5bced76e'
CODE='903f892a5dcd79166cc2ffbaa70ddaabf293aaaa'
# Reviewed source-acceptance tool delta only. Preserve immutable runtime/UI
# foundation evidence and reject every other changed byte as before.
ACCEPTANCE_TOOL_PATCH={
    'path':'src/media_ai/source_e2e.py',
    'base_sha256':'7f44953fa2b0549c9cae1b645a3e37cac941d6654b07cb6c462b01d96b671b08',
    'sha256':'59b8f13ed38ea85ad233b50b721754773e82c8029591eff03c89cbca1470bf58',
    'scope':'SOURCE_AND_WINDOWS_ACCEPTANCE_AND_MEDIA_PRODUCTION_PACKAGE_ONLY',
    'evidence':'docs/evidence/media-real-30s-general-r3-20261026/RESULT_KO.md',
}
CONTROLS=('CURRENT_GENERAL_WORK_STATE.json','CURRENT_GENERAL_WORK_CONTROL_PLANE_LOCK.json',
          'CURRENT_PC_WORK_STATE.json','CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json','CURRENT_WORKER_COORDINATION_LOCK.json')
SCOPE='HISTORICAL_R3_CANDIDATE_ONLY_SEE_CURRENT_WORK_FOR_R2'


def require(value,message):
    if not value:raise ValueError(message)


def read(root,name):return json.loads((root/name).read_text(encoding='utf-8'))
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def encoded(value):return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')


def runtime_baseline(root):
    if digest(root/BASELINE)!=BASELINE_SHA:
        return {'status':'BLOCKED_EVIDENCE_AUTHORITY_CHANGED','source':CODE,'changed_paths':[BASELINE]}
    if digest(root/FOUNDATION)!=FOUNDATION_SHA:
        return {'status':'BLOCKED_EVIDENCE_AUTHORITY_CHANGED','source':CODE,'changed_paths':[FOUNDATION]}
    receipt=read(root,BASELINE)
    require(receipt['frozen_code']==CODE,'R2_BASELINE_SOURCE_MISMATCH')
    paths=dict(read(root,FOUNDATION)['source_file_sha256'])
    paths.update({name:sha for name,sha in receipt['code_file_sha256'].items() if name.startswith('src/media_ai/')})
    paths.update(receipt['source_ui_identity']['file_hashes'])
    patch=ACCEPTANCE_TOOL_PATCH
    require(paths.get(patch['path'])==patch['base_sha256'],'ACCEPTANCE_TOOL_BASE_AUTHORITY_MISMATCH')
    paths[patch['path']]=patch['sha256']
    changed=[name for name,sha in paths.items() if not (root/name).is_file() or digest(root/name)!=sha]
    changed.extend(p.relative_to(root).as_posix() for p in (root/'src/media_ai').glob('*.py') if p.relative_to(root).as_posix() not in paths)
    return {'status':'BLOCKED_RUNTIME_SOURCE_CHANGED' if changed else 'PASS_EXACT_RUNTIME_UI_BYTES',
            'source':CODE,'file_count':len(paths),'changed_paths':changed,
            'acceptance_tool_patch':dict(patch),
            'workspace_ui_fingerprint':receipt['source_ui_identity']['workspace_ui_fingerprint']}


def derive(root=ROOT):
    root=Path(root);baseline=runtime_baseline(root);intake=intake_result(root/MANIFEST)
    source_ok=baseline['status']=='PASS_EXACT_RUNTIME_UI_BYTES';inputs_ok=not intake['errors']
    eligibility=('BLOCKED_SOURCE_REVALIDATION' if not source_ok else
                 'BLOCKED_ASSET_INTAKE' if not inputs_ok else 'ENGINE_PREFLIGHT_REQUIRED')
    return {'schema':'MINDLE_CURRENT_WORK_STATUS_V1','work_id':WORK_ID,'current_directive':DIRECTIVE,
            'runtime_baseline':baseline,
            'general_status':'R2_GENERAL_PREPARATION_COMPLETE' if source_ok else 'R2_SOURCE_REVALIDATION_REQUIRED',
            'pc_status':('R2_'+eligibility if not source_ok or not inputs_ok else 'R2_WINDOWS_ENGINE_AND_APPROVAL_PREFLIGHT_REQUIRED'),'production_eligibility':eligibility,
            'input_manifest':MANIFEST,'input_manifest_sha256':intake['manifest_sha256'],
            'intake_status':intake['status'],'input_errors':intake['errors'],
            'next_action':('REVALIDATE_CHANGED_RUNTIME_SOURCE' if not source_ok else
                'REGISTER_REAL_VIDEO_BGM_SCRIPT_VOLUMES_POLICY' if not inputs_ok else 'RUN_GENERAL_SOURCE_ENGINE_PREFLIGHT'),
            'source_lane':'ACTUAL_ASSET_INTAKE_REQUIRED' if not inputs_ok else 'ENGINE_IDENTITY_NOT_CHECKED_BY_THIS_STATUS_TOOL',
            'windows_lane':'WINDOWS_7B_AND_EXACT_CANDIDATE_APPROVAL_REQUIRED',
            'production_execution_allowed':False,'source_execution_started_by_this_check':False,
            'local_pc_process_status':'NOT_OBSERVED','background_execution_claimed':False,
            'package_build_allowed':False,'installed_model_replacement_allowed':False,
            'owner_acceptance':False,'full_product_pass':False,
            'historical_candidate_control':'R3 epoch/phase/identity remain consumed candidate evidence, not current R2 readiness'}


def reference(value):
    return {'work_id':WORK_ID,'status_file':STATUS_FILE,'snapshot_sha256':hashlib.sha256(encoded(value)).hexdigest(),
            'current_directive':DIRECTIVE,'general_status':value['general_status'],'pc_status':value['pc_status'],
            'production_eligibility':value['production_eligibility'],'runtime_baseline_source':CODE}


def closed_gates(root):
    values=[read(root,name) for name in CONTROLS]
    # Refuse inconsistent/open gates. Never "repair" them by setting false.
    for value in values[:4]:
        require(value.get('package_build_allowed') is False,'EXISTING_BUILD_GATE_NOT_CLOSED')
        require(value.get('owner_pc_runtime_pass') is False and value.get('final_product_pass') is False,'UNSUPPORTED_EXISTING_FINAL_PASS')
        old=value.get('owner_windows_ai_successor_20261024',{})
        require(old.get('authorization_consumed') is True and old.get('additional_package_builds_allowed') is False,'R3_CONSUMED_AUTHORIZATION_MISSING')
    return values


def write(path,value):
    temp=path.with_suffix(path.suffix+'.r2-status.tmp')
    temp.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');temp.replace(path)


def refresh(root=ROOT):
    root=Path(root);controls=closed_gates(root);value=derive(root);ref=reference(value)
    require((root/DIRECTIVE).is_file(),'CURRENT_R2_DIRECTIVE_MISSING')
    # A partial multi-file write is rejected by check(); rerunning refresh is safe.
    write(root/STATUS_FILE,value)
    for name,state in zip(CONTROLS,controls):
        state.setdefault('pre_r2_status',state['status'])
        state['historical_candidate_status_scope']=SCOPE
        state['current_work']=ref
        state['status']=(value['general_status'] if 'GENERAL_WORK' in name else
                         value['pc_status'] if 'PC_WORK' in name else 'R2_WAITING_INPUT_OR_PREFLIGHT')
        if name=='CURRENT_WORKER_COORDINATION_LOCK.json':
            state.setdefault('pre_r2_collision_status',state.get('collision_status'))
            state['collision_status']='ALIGNED_R2_STATUS_AND_CONSUMED_R3_CANDIDATE_EVIDENCE'
            state['worker_lanes']['general_work']['current_assignment']='R2 General source preparation verified; read CURRENT_MEDIA_WORK_STATUS.json; actual production is gated by real inputs and engine preflight.'
            state['worker_lanes']['pc_work_remote_windows']['current_assignment']='R3 is consumed historical evidence. R2 Windows 7B/candidate execution requires exact approval and real asset intake; no build authorization granted.'
        write(root/name,state)
    return check(root)


def check(root=ROOT):
    root=Path(root);controls=closed_gates(root)
    require(read(root,STATUS_FILE)==derive(root),'CURRENT_WORK_SNAPSHOT_STALE_OR_FORGED')
    value=read(root,STATUS_FILE);ref=reference(value)
    require((root/DIRECTIVE).is_file(),'CURRENT_R2_DIRECTIVE_MISSING')
    for name,state in zip(CONTROLS,controls):
        require(state.get('current_work')==ref,'CURRENT_WORK_REFERENCE_MISMATCH: '+name)
        require(state.get('historical_candidate_status_scope')==SCOPE,'R3_SCOPE_MISSING: '+name)
        expected=(value['general_status'] if 'GENERAL_WORK' in name else
                  value['pc_status'] if 'PC_WORK' in name else 'R2_WAITING_INPUT_OR_PREFLIGHT')
        require(state.get('status')==expected,'CURRENT_WORK_LANE_STATUS_MISMATCH: '+name)
    return value


def main():
    p=argparse.ArgumentParser();p.add_argument('--refresh',action='store_true');p.add_argument('--check',action='store_true')
    p.add_argument('--preflight',action='store_true',help='Read fresh eligibility only; never launch or approve')
    args=p.parse_args()
    try:
        value=refresh() if args.refresh else derive() if args.preflight else check()
        print(json.dumps(value,ensure_ascii=False,indent=2))
        # Status consistency PASS is distinct from permission to run production.
        return 2 if args.preflight and not value['production_execution_allowed'] else 0
    except (ValueError,KeyError,OSError) as error:
        print('CURRENT_MEDIA_WORK_STATUS_BLOCKED: '+str(error),file=sys.stderr);return 2


if __name__=='__main__':raise SystemExit(main())
