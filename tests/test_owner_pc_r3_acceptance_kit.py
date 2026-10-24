from pathlib import Path
import hashlib
import zipfile


ROOT=Path(__file__).resolve().parents[1]


def test_r3_owner_pc_acceptance_is_exact_candidate_and_targeted_shutdown():
    source=(ROOT/'scripts/accept_r3_on_owner_pc.ps1').read_text(encoding='utf-8')
    assert '9f5d304ce825-0f8cc3c5d320-ai-r3' in source
    assert '701654240d8f2795957f78f7d1cc9d7fd23d3195f49a0d39ede1d8b8a3a915a5' in source
    assert 'ec2b82e15eba653a977ce9ddfcf1fb0b697d2bd701c8a7e65aa37f51b68652ca' in source
    assert '/api/runtime/shutdown' in source and 'X-Mindle-Control' in source
    assert 'MINDLE\\runtime\\$ExpectedRuntime' in source
    assert 'package_manifest_sha256 -eq $ExpectedManifest' in source
    assert 'Stop-Process' not in source and 'taskkill' not in source
    assert 'Find-Mp4' in source and 'ffprobe.exe' in source
    assert '04_REOPEN_EXPORT.json' in source
    assert 'PASS_ALL_ENTRIES_READ' in source
    assert 'ZipFile]::OpenRead' in source
    assert "approved_ui_pixel_match = $false" in source
    assert "full_product_pass = $false" in source


def test_r3_owner_pc_acceptance_has_double_click_entrypoint():
    command=(ROOT/'scripts/START_R3_OWNER_PC_ACCEPTANCE.cmd').read_text(encoding='utf-8')
    assert 'accept_r3_on_owner_pc.ps1' in command
    assert '-ExecutionPolicy Bypass' in command


def test_r3_owner_pc_acceptance_download_bundle_is_exact_and_complete():
    bundle=ROOT/'docs/handoff/MINDLE_MEDIA_AI_R3_OWNER_PC_ACCEPTANCE_KIT_20261024.zip'
    assert hashlib.sha256(bundle.read_bytes()).hexdigest()=='9c058c27669f9ea2141903f477b9dac8c201f2e7501fc5944b1379b9f55fdda8'
    with zipfile.ZipFile(bundle) as archive:
        assert archive.testzip() is None
        assert set(archive.namelist())=={'START_R3_OWNER_PC_ACCEPTANCE.cmd','accept_r3_on_owner_pc.ps1','README_KO.txt'}
        assert archive.read('START_R3_OWNER_PC_ACCEPTANCE.cmd')==(ROOT/'scripts/START_R3_OWNER_PC_ACCEPTANCE.cmd').read_bytes()
        assert archive.read('accept_r3_on_owner_pc.ps1')==(ROOT/'scripts/accept_r3_on_owner_pc.ps1').read_bytes()
