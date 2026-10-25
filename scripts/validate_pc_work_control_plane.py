#!/usr/bin/env python3
import json,pathlib,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
def require(value,message):
    if not value:raise SystemExit('PC_WORK_CONTROL_PLANE_MISMATCH_BLOCKED: '+message)
def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))
p=read('CURRENT_PC_WORK_STATE.json');l=read('CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json');g=read('CURRENT_GENERAL_WORK_STATE.json');gl=read('CURRENT_GENERAL_WORK_CONTROL_PLANE_LOCK.json');w=read('CURRENT_WORKER_COORDINATION_LOCK.json')
epoch='MEDIA-AI-20261024-WINDOWS-AI-SUCCESSOR-R3'
require(p.get('control_plane_epoch')==l.get('epoch')==g.get('control_plane_epoch')==gl.get('epoch')==w.get('active_control_plane_epoch')==epoch,'epoch mismatch')
r2=p.get('active_directive')=='docs/commander/MINDLE_MEDIA_AI_PC_TEST_R2_ACCEPTANCE_20261024.md'
r9=p.get('active_directive')=='docs/commander/MINDLE_MEDIA_AI_PC_R9_CORRECTED_CANDIDATE_ACCEPTANCE_20261016.md'
successor=p.get('active_directive')=='docs/commander/MINDLE_MEDIA_AI_WINDOWS_AI_SUCCESSOR_R3_DIRECTIVE_20261024.md'
expected_directive='docs/commander/MINDLE_MEDIA_AI_PC_R9_CORRECTED_CANDIDATE_ACCEPTANCE_20261016.md' if r9 else 'docs/commander/MINDLE_MEDIA_AI_WINDOWS_CANDIDATE_BUILD_AND_PC_ACCEPTANCE_DIRECTIVE_v1.0_20261014.md'
expected_contract='docs/commander/MINDLE_MEDIA_AI_PC_R9_CORRECTED_CANDIDATE_EVIDENCE_CONTRACT_20261016.json' if r9 else 'docs/commander/MINDLE_MEDIA_AI_WINDOWS_CANDIDATE_BUILD_AND_PC_ACCEPTANCE_EVIDENCE_CONTRACT_v1.0_20261014.json'
if r2:
    expected_directive='docs/commander/MINDLE_MEDIA_AI_PC_TEST_R2_ACCEPTANCE_20261024.md'
    expected_contract='docs/commander/MINDLE_MEDIA_AI_PC_TEST_R2_EVIDENCE_CONTRACT_20261024.json'
if successor:
    expected_directive='docs/commander/MINDLE_MEDIA_AI_WINDOWS_AI_SUCCESSOR_R3_DIRECTIVE_20261024.md'
    expected_contract='docs/commander/MINDLE_MEDIA_AI_WINDOWS_AI_SUCCESSOR_R3_EVIDENCE_CONTRACT_20261024.json'
require(p.get('active_directive')==l.get('active_directive')==expected_directive,'directive mismatch')
require(p.get('evidence_contract')==l.get('evidence_contract')==expected_contract,'contract mismatch')
require((ROOT/p['active_directive']).is_file() and (ROOT/p['evidence_contract']).is_file(),'missing active files')
require(json.loads((ROOT/p['evidence_contract']).read_text(encoding='utf-8'))['epoch']==epoch,'contract epoch mismatch')
phase=g.get('phase')
require(phase==p.get('phase')==gl.get('phase')==l.get('phase'),'phase mismatch')
if phase in {'WINDOWS_AI_SUCCESSOR_R3_SINGLE_ATTEMPT_AUTHORIZED','WINDOWS_AI_SUCCESSOR_R3_CROSSPLATFORM_FIX_SINGLE_ATTEMPT_AUTHORIZED'}:
    require(successor,'R3 successor directive missing')
    authorization=read('docs/commander/WINDOWS_AI_SUCCESSOR_20261024_AUTHORIZATION.json')
    require(authorization['attempts_allowed']==1 and authorization['package_build_allowed'] is True,'R3 authorization invalid')
    for state in (p,l,g,gl):
        owner=state.get('owner_windows_ai_successor_20261024',{})
        require(state.get('package_build_allowed') is True,'R3 build gate not released')
        require(owner.get('authorization')==authorization['id'] and owner.get('authorized_parent')==authorization['authorized_parent'],'R3 authorization mismatch')
        require(owner.get('engine_bytes')=='REUSE_VERIFIED_NO_DOWNLOAD_NO_REBUILD','R3 engine reuse contract missing')
elif phase=='WINDOWS_AI_SUCCESSOR_R3_REMOTE_VERIFIED_OWNER_PC_PENDING':
    require(successor,'R3 successor directive missing')
    accepted=read('docs/evidence/windows-ai-successor-20261024-r3/ACCEPTANCE.json')
    final=read('docs/evidence/windows-ai-successor-20261024-r3/FINAL_DELIVERY.json')
    require(accepted['status']=='REMOTE_WINDOWS_EXE_QWEN_SUPERTONIC_MEASURED_ARCHITECTURE_RESTART_EXPORT_PASS','R3 native acceptance missing')
    require(final['source']==accepted['source'] and final['actual_qwen'] is True and final['actual_supertonic'] is True and final['actual_measured_architecture_agent'] is True,'R3 engine evidence missing')
    require(final['independent_all_payload_hashes']=='PASS' and final['independent_zip_crc']=='PASS','R3 independent readback missing')
    for state in (p,l,g,gl):
        owner=state.get('owner_windows_ai_successor_20261024',{})
        require(state.get('package_build_allowed') is False,'R3 repeat build forbidden')
        require(owner.get('source')==final['source'] and owner.get('run')==40079944004,'R3 source/run mismatch')
        require(owner.get('zip_sha256')==final['sha256'] and owner.get('manifest_sha256')==final['manifest_sha256'],'R3 delivery identity mismatch')
        require(owner.get('office_pc_acceptance') is False and owner.get('human_hearing') is False and owner.get('full_product_pass') is False,'R3 unsupported scope expansion')
elif phase=='OWNER_WINDOWS_AI_CANDIDATE_READY_FOR_PC_ACCEPTANCE':
    require(r2,'TEST R2 directive missing')
    contract=read(p['evidence_contract'])
    accepted=read('docs/evidence/windows-ai-candidate-20261024-r1/ACCEPTANCE.json')
    final=read('docs/evidence/windows-ai-candidate-20261024-r1/FINAL_DELIVERY.json')
    require(accepted['status']=='REMOTE_WINDOWS_EXE_CHROME_QWEN_NEURAL_TTS_RESTART_EXPORT_PASS','native acceptance missing')
    mapping={'candidate_source':'source','candidate_run':'producer_run','candidate_readback_run':'readback_run','candidate_zip_sha256':'zip_sha256','candidate_payload_manifest_sha256':'manifest_sha256','candidate_launcher_sha256':'exe_sha256','candidate_runtime_id':'runtime_id'}
    for state in (p,l,g,gl):
        require(state.get('package_build_allowed') is False,'repeat build forbidden')
        for key,value in mapping.items():require(state.get(key)==contract[value], 'TEST R2 identity mismatch: '+key)
    require(final['sha256']==contract['zip_sha256'] and final['source']==contract['source']==accepted['source'],'final delivery mismatch')
    require(final['product_payload_changed'] is False and final['post_update_all_payload_hashes']=='PASS' and final['zip_crc']=='PASS','readback incomplete')
    require(accepted['office_pc_acceptance'] is False and accepted['human_hearing'] is False and accepted['full_product_pass'] is False,'unsupported native scope expansion')
    require(p.get('local_physical_acceptance_allowed') is True and p.get('package_status')=='AI_CANDIDATE_NATIVE_VERIFIED_DELIVERABLE_OWNER_PC_PENDING','TEST R2 handoff missing')
elif phase in {'R9_CORRECTED_CANDIDATE_BUILD_IN_PROGRESS','R9_CORRECTED_CANDIDATE_REVIEW_REQUIRED','R9_CORRECTED_CANDIDATE_READY_FOR_PC_ACCEPTANCE'}:
    for state in (p,l,g,gl):
        require(state.get('package_build_allowed') is False,'R9 one-attempt build gate must be closed')
        require(state.get('candidate_attempt_run')==p.get('candidate_attempt_run') and state.get('candidate_attempt_source')==p.get('candidate_attempt_source'),'R9 attempt identity mismatch')
    require(p.get('candidate_attempt_run') and p.get('candidate_attempt_source'),'R9 attempt missing')
    if phase=='R9_CORRECTED_CANDIDATE_READY_FOR_PC_ACCEPTANCE':
        for state in (p,l,g,gl):
            require(state.get('candidate_source')==p.get('candidate_source')==p.get('candidate_attempt_source'),'R9 source identity mismatch')
            require(state.get('candidate_run')==p.get('candidate_run')==p.get('candidate_attempt_run'),'R9 producer mismatch')
            for key in ('candidate_zip_sha256','candidate_payload_manifest_sha256','candidate_launcher_sha256','candidate_readback_run','candidate_runtime_id'):
                require(state.get(key)==p.get(key) and state.get(key),'R9 readback identity mismatch: '+key)
        require(p.get('local_physical_acceptance_allowed') is True and p.get('package_status')=='R9_CORRECTED_CANDIDATE_VERIFIED_AND_DELIVERABLE','R9 local acceptance release missing')
elif phase=='VERIFIED_WINDOWS_CANDIDATE_READY_FOR_PC_ACCEPTANCE':
    for state in (p,l,g,gl):
        require(state.get('package_build_allowed') is False,'repeat build gate must be closed')
        require(state.get('candidate_source')=='0e4e12a9e4c758f202c6ebb5085df5a542bb6314' and state.get('candidate_run')==38497304486,'candidate source/run mismatch')
        require(state.get('candidate_zip_sha256')=='8d844a686fdd2f8630b97384cf8d224fbb4195061819a5a79f4576097aeaf527' and state.get('candidate_readback_run')==38499220659,'candidate byte readback mismatch')
    require(p.get('local_physical_acceptance_allowed') is True and p.get('package_status')=='CORRECTED_CANDIDATE_VERIFIED_AND_DELIVERABLE','local acceptance release missing')
else:
    require(phase=='VERIFIED_CORE_WINDOWS_CANDIDATE_BUILD','unknown phase')
    require(p.get('package_build_allowed') is True and g.get('package_build_allowed') is True,'build gate not released')
require(p.get('verified_core_source')==g.get('verified_core_source') and p.get('verified_core_run')==g.get('verified_core_run'),'core mismatch')
for state in (p,l,g,gl):
    require(state.get('owner_pc_runtime_pass') is False and state.get('final_product_pass') is False and state.get('openai_connected') is False,'unsupported final PASS')
require(p.get('employee_manual_install_steps_allowed') is False and p.get('external_marketing_avora_status')=='DEFERRED_EXTERNAL','scope mismatch')
require(w.get('pr23_hold_do_not_merge') is True and w.get('merge_main_forbidden') is True and w.get('force_push_forbidden') is True,'invariant mismatch')
for inv in ('main_merge_forbidden','force_push_forbidden','pr23_hold_do_not_merge','approved_ui_preserved'):
    require(l['invariants'].get(inv) is True,inv)
require(epoch in (ROOT/'CURRENT_PC_WORK_DIRECTIVE.md').read_text(encoding='utf-8'),'current epoch missing')
if (ROOT/'CURRENT_MEDIA_WORK_STATUS.json').exists() or any('current_work' in value for value in (p,l,g,gl,w)):
    result=subprocess.run([sys.executable,str(ROOT/'scripts/media_work_status.py'),'--check'],capture_output=True,text=True,encoding='utf-8',timeout=30)
    require(result.returncode==0,'current R2 work status failed: '+(result.stderr or result.stdout).strip())
    print('CURRENT_R2_STATUS_VALIDATED; HISTORICAL_R3_IDENTITY_PRESERVED; NO_NEW_EXECUTION_AUTHORIZATION')
print('PC_WORK_CORRECTED_CANDIDATE_READY_FOR_LOCAL_ACCEPTANCE_PASS' if phase.endswith('PC_ACCEPTANCE') else 'PC_WORK_CORRECTED_WINDOWS_CANDIDATE_GATE_PASS')
print('OWNER_PC_PASS=false; FULL_PRODUCT_PASS=false; OPENAI_CONNECTED=false')

