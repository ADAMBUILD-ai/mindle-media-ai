#!/usr/bin/env python3
"""Validate the active General/PC handoff without promoting historical PASS scopes."""
from __future__ import annotations
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
LEGACY_EPOCH = 'MEDIA-AI-20261008-GENERAL-WORK-FINAL-SELF-AUDIT-R1'
PC_EPOCH = 'MEDIA-AI-20261008-PC-WORK-ONE-CLICK-RUNTIME-PACKAGE-R1'
RECOVERY_EPOCH = 'MEDIA-AI-20261013-OWNER-RUNTIME-RECOVERY-R1'
R3_EPOCH = 'MEDIA-AI-20261024-WINDOWS-AI-SUCCESSOR-R3'
PASS = 'PASS_MINDLE_MEDIA_AI_GENERAL_WORK_FINAL_SELF_AUDIT_READY_FOR_PC_WORK'


def require(value, message):
    if not value:
        raise ValueError(message)


def validate(root=ROOT):
    current = (root/'CURRENT_GENERAL_WORK_DIRECTIVE.md').read_text(encoding='utf-8')
    def read(name):
        return json.loads((root/name).read_text(encoding='utf-8'))
    lock = read('CURRENT_GENERAL_WORK_CONTROL_PLANE_LOCK.json')
    state = read('CURRENT_GENERAL_WORK_STATE.json')
    worker = read('CURRENT_WORKER_COORDINATION_LOCK.json')
    epoch = state.get('control_plane_epoch')
    if epoch in {RECOVERY_EPOCH, R3_EPOCH}:
        require(worker.get('active_control_plane_epoch') == epoch, 'worker epoch mismatch')
        expected_status=state.get('current_work',{}).get('general_status','ACTIVE_OWNER_RUNTIME_RECOVERY')
        require(expected_status in {'ACTIVE_OWNER_RUNTIME_RECOVERY','R2_GENERAL_PREPARATION_COMPLETE','R2_SOURCE_REVALIDATION_REQUIRED'}, 'unknown General status')
        require(state.get('status') == lock.get('status') == expected_status, 'recovery status mismatch')
        require(lock.get('control_plane_epoch') == lock.get('epoch') == epoch and lock.get('active') is True, 'General lock epoch mismatch')
        require(epoch in current and state.get('product_changes_allowed') is True, 'current General directive mismatch')
        for value in (state, lock):
            require(value.get('owner_pc_runtime_pass') is False and value.get('final_product_pass') is False, 'unsupported General final PASS')
        for invariant in ('main_merge_forbidden', 'force_push_forbidden', 'pr23_hold_do_not_merge', 'approved_visual_frozen'):
            require(lock.get('invariants', {}).get(invariant) is True, 'General invariant missing: '+invariant)
        if epoch == R3_EPOCH:
            # Keep the independent PC validator authoritative for source, delivery,
            # phase, consumed authorization, four state files and R3 byte readback.
            require(state.get('phase') == 'WINDOWS_AI_SUCCESSOR_R3_REMOTE_VERIFIED_OWNER_PC_PENDING', 'unaccepted R3 phase')
            for value in (state, lock):
                require(value.get('package_build_allowed') is False, 'R3 repeat build forbidden')
                for field in ('active_directive', 'evidence_contract'):
                    require(value.get(field) == state.get(field) and value.get(field) in current, 'General '+field+' mismatch')
            check = subprocess.run([sys.executable, str(root/'scripts/validate_pc_work_control_plane.py')],
                                   capture_output=True, text=True, timeout=30)
            require(check.returncode == 0, 'PC handoff validation failed: '+(check.stderr or check.stdout).strip())
            current_work=state.get('current_work')
            if current_work:
                return 'CURRENT_WORK='+current_work['work_id']+'\nGENERAL_STATUS='+expected_status+'\nPC_STATUS='+current_work['pc_status']+'\nHISTORICAL_GENERAL_WORK_R3_REMOTE_VERIFIED_OWNER_PC_PENDING\nOWNER_PC_PASS=false; FULL_PRODUCT_PASS=false; PACKAGE_BUILD_ALLOWED=false'
            return 'GENERAL_WORK_R3_REMOTE_VERIFIED_OWNER_PC_PENDING\nOWNER_PC_PASS=false; FULL_PRODUCT_PASS=false; PACKAGE_BUILD_ALLOWED=false'
        return 'GENERAL_WORK_OWNER_RUNTIME_RECOVERY_ACTIVE'

    require(lock.get('epoch') == epoch == LEGACY_EPOCH, 'General Work epoch mismatch')
    require(lock.get('status') == state.get('status') == 'COMPLETE_HANDOFF_TO_PC_WORK', 'General Work handoff must be complete')
    require(lock.get('final_result') == state.get('final_result') == PASS, 'General Work final PASS missing')
    require(lock.get('final_head') == '9f0bdaf7b8c3c9f7c8ea7df5b132dceb4199ddbb', 'General Work final HEAD mismatch')
    require(state.get('pc_work_allowed') is True, 'PC Work must be unblocked')
    require(worker.get('active_control_plane_epoch') == PC_EPOCH, 'PC Work must be the active worker epoch')
    for token in (PASS, '9f0bdaf7b8c3c9f7c8ea7df5b132dceb4199ddbb', PC_EPOCH):
        require(token in current, 'CURRENT missing '+repr(token))
    return 'GENERAL_WORK_COMPLETE_HANDOFF_TO_PC_WORK\nGENERAL_EPOCH='+LEGACY_EPOCH+'\nPC_EPOCH='+PC_EPOCH


def main():
    try:
        print(validate())
        return 0
    except (ValueError, KeyError, OSError, subprocess.SubprocessError) as error:
        print('GENERAL_WORK_HANDOFF_MISMATCH_BLOCKED: '+str(error), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
