"""Cross-file handoff checks and fault injection; never relax current build gates."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('general_validator', ROOT/'scripts/validate_general_work_control_plane.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


@pytest.fixture
def handoff(tmp_path):
    paths = [
        'CURRENT_GENERAL_WORK_DIRECTIVE.md', 'CURRENT_PC_WORK_DIRECTIVE.md',
        'CURRENT_GENERAL_WORK_STATE.json', 'CURRENT_GENERAL_WORK_CONTROL_PLANE_LOCK.json',
        'CURRENT_PC_WORK_STATE.json', 'CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json',
        'CURRENT_WORKER_COORDINATION_LOCK.json', 'scripts/validate_general_work_control_plane.py',
        'scripts/validate_pc_work_control_plane.py',
        'docs/commander/MINDLE_MEDIA_AI_WINDOWS_AI_SUCCESSOR_R3_DIRECTIVE_20261024.md',
        'docs/commander/MINDLE_MEDIA_AI_WINDOWS_AI_SUCCESSOR_R3_EVIDENCE_CONTRACT_20261024.json',
        'docs/evidence/windows-ai-successor-20261024-r3/ACCEPTANCE.json',
        'docs/evidence/windows-ai-successor-20261024-r3/FINAL_DELIVERY.json',
    ]
    paths += ['CURRENT_MEDIA_WORK_STATUS.json','scripts/media_work_status.py',
              'docs/commander/MINDLE_MEDIA_AI_R2_CURRENT_WORK_20261025.md',
              'docs/handoff/media-ai-core-e2e-r2-20261025/INPUT_MANIFEST.json',
              'docs/evidence/media-ai-core-e2e-r2-20261025/SOURCE_VALIDATION.json',
              'docs/evidence/media-ai-core-e2e-r1-20261025/SOURCE_BINDING.json']
    baseline=json.loads((ROOT/'docs/evidence/media-ai-core-e2e-r2-20261025/SOURCE_VALIDATION.json').read_text(encoding='utf-8'))
    foundation=json.loads((ROOT/'docs/evidence/media-ai-core-e2e-r1-20261025/SOURCE_BINDING.json').read_text(encoding='utf-8'))
    paths += list(foundation['source_file_sha256'])
    paths += [name for name in baseline['code_file_sha256'] if name.startswith('src/media_ai/')]
    paths += list(baseline['source_ui_identity']['file_hashes'])
    for name in set(paths):
        destination = tmp_path/name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT/name, destination)
    return tmp_path


def mutate(root, name, field, value):
    path = root/name
    data = json.loads(path.read_text())
    target = data
    for key in field.split('.')[:-1]:
        target = target[key]
    target[field.split('.')[-1]] = value
    path.write_text(json.dumps(data))


def test_current_r3_handoff_has_no_unsupported_final_pass(handoff):
    result = validator.validate(handoff)
    assert 'GENERAL_WORK_R3_REMOTE_VERIFIED_OWNER_PC_PENDING' in result
    assert 'FULL_PRODUCT_PASS=false' in result
    assert 'PACKAGE_BUILD_ALLOWED=false' in result


@pytest.mark.parametrize('name,field,value', [
    ('CURRENT_GENERAL_WORK_STATE.json', 'control_plane_epoch', 'UNKNOWN'),
    ('CURRENT_GENERAL_WORK_CONTROL_PLANE_LOCK.json', 'epoch', 'OLD'),
    ('CURRENT_GENERAL_WORK_CONTROL_PLANE_LOCK.json', 'status', 'COMPLETE_HANDOFF_TO_PC_WORK'),
    ('CURRENT_WORKER_COORDINATION_LOCK.json', 'active_control_plane_epoch', 'OLD'),
    ('CURRENT_PC_WORK_STATE.json', 'control_plane_epoch', 'OLD'),
    ('CURRENT_GENERAL_WORK_STATE.json', 'phase', 'WINDOWS_AI_SUCCESSOR_R3_SINGLE_ATTEMPT_AUTHORIZED'),
    ('CURRENT_GENERAL_WORK_CONTROL_PLANE_LOCK.json', 'package_build_allowed', True),
    ('CURRENT_GENERAL_WORK_STATE.json', 'owner_pc_runtime_pass', True),
    ('CURRENT_GENERAL_WORK_CONTROL_PLANE_LOCK.json', 'final_product_pass', True),
    ('CURRENT_GENERAL_WORK_CONTROL_PLANE_LOCK.json', 'invariants.pr23_hold_do_not_merge', False),
    ('CURRENT_PC_WORK_STATE.json', 'owner_windows_ai_successor_20261024.source', 'a'*40),
    ('CURRENT_PC_WORK_STATE.json', 'owner_windows_ai_successor_20261024.zip_sha256', 'a'*64),
    ('docs/evidence/windows-ai-successor-20261024-r3/FINAL_DELIVERY.json', 'independent_zip_crc', 'FAIL'),
    ('docs/commander/MINDLE_MEDIA_AI_WINDOWS_AI_SUCCESSOR_R3_EVIDENCE_CONTRACT_20261024.json', 'epoch', 'OLD'),
])
def test_mismatched_or_relaxed_handoff_is_still_rejected(handoff, name, field, value):
    mutate(handoff,name,field,value)
    with pytest.raises(ValueError):
        validator.validate(handoff)


def test_missing_r3_acceptance_is_rejected(handoff):
    (handoff/'docs/evidence/windows-ai-successor-20261024-r3/ACCEPTANCE.json').unlink()
    with pytest.raises(ValueError,match='PC handoff validation failed'):
        validator.validate(handoff)


def test_current_directive_must_name_the_active_contract(handoff):
    path = handoff/'CURRENT_GENERAL_WORK_DIRECTIVE.md'
    path.write_text(validator.R3_EPOCH)
    with pytest.raises(ValueError,match='directive mismatch'):
        validator.validate(handoff)


def test_cli_failure_prefix_and_exit_code_survive_python_optimization(handoff):
    mutate(handoff,'CURRENT_WORKER_COORDINATION_LOCK.json','active_control_plane_epoch','OLD')
    result = subprocess.run([sys.executable,'-O',str(handoff/'scripts/validate_general_work_control_plane.py')],capture_output=True,text=True)
    assert result.returncode == 2
    assert 'GENERAL_WORK_HANDOFF_MISMATCH_BLOCKED' in result.stderr
