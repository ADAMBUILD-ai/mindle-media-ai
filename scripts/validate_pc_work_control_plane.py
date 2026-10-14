#!/usr/bin/env python3
import json,pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
def require(value,message):
    if not value:raise SystemExit('PC_WORK_CONTROL_PLANE_MISMATCH_BLOCKED: '+message)
def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))
p=read('CURRENT_PC_WORK_STATE.json');l=read('CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json');g=read('CURRENT_GENERAL_WORK_STATE.json');gl=read('CURRENT_GENERAL_WORK_CONTROL_PLANE_LOCK.json');w=read('CURRENT_WORKER_COORDINATION_LOCK.json')
epoch='MEDIA-AI-20261013-OWNER-RUNTIME-RECOVERY-R1'
require(p.get('control_plane_epoch')==l.get('epoch')==g.get('control_plane_epoch')==gl.get('epoch')==w.get('active_control_plane_epoch')==epoch,'epoch mismatch')
require(p.get('active_directive')==l.get('active_directive')=='docs/commander/MINDLE_MEDIA_AI_WINDOWS_CANDIDATE_BUILD_AND_PC_ACCEPTANCE_DIRECTIVE_v1.0_20261014.md','directive mismatch')
require(p.get('evidence_contract')==l.get('evidence_contract')=='docs/commander/MINDLE_MEDIA_AI_WINDOWS_CANDIDATE_BUILD_AND_PC_ACCEPTANCE_EVIDENCE_CONTRACT_v1.0_20261014.json','contract mismatch')
require((ROOT/p['active_directive']).is_file() and (ROOT/p['evidence_contract']).is_file(),'missing active files')
require(json.loads((ROOT/p['evidence_contract']).read_text())['epoch']==epoch,'evidence contract epoch mismatch')
require(p.get('package_build_allowed') is True and g.get('package_build_allowed') is True,'build gate not released')
require(g.get('phase')=='VERIFIED_CORE_WINDOWS_CANDIDATE_BUILD' and g.get('package_workflow')=='.github/workflows/pc-one-click-windows-build-e2e.yml','candidate scope mismatch')
require(p.get('verified_core_source')==g.get('verified_core_source')=='92a281f8c5eee70e4e23d14949f2f2c9b728da82' and p.get('verified_core_run')==g.get('verified_core_run')==38433228957,'verified core mismatch')
for s in (p,g):
    require(s.get('owner_pc_runtime_pass') is False and s.get('final_product_pass') is False and s.get('openai_connected') is False,'unsupported final PASS')
require(p.get('employee_manual_install_steps_allowed') is False and p.get('external_marketing_avora_status')=='DEFERRED_EXTERNAL','scope mismatch')
require(w.get('pr23_hold_do_not_merge') is True and w.get('merge_main_forbidden') is True and w.get('force_push_forbidden') is True,'invariant mismatch')
for inv in ('main_merge_forbidden','force_push_forbidden','pr23_hold_do_not_merge','approved_ui_preserved'):
    require(l['invariants'].get(inv) is True,inv)
require(epoch in (ROOT/'CURRENT_PC_WORK_DIRECTIVE.md').read_text(),'current directive epoch missing')
print('PC_WORK_CORRECTED_WINDOWS_CANDIDATE_GATE_PASS')
print('LOCAL_READINESS=USER_REPORTED_NORMAL; LOCAL_PRODUCT_PASS=false; FINAL_PRODUCT_PASS=false')
