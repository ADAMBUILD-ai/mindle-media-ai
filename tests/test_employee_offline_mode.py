from pathlib import Path
from unittest.mock import patch

import pytest
from media_ai.product_runtime import ProductModelVault
from media_ai.product_server import ProductHttpServer


def test_local_mode_never_constructs_hf_client_and_blocks_acquisition(tmp_path, monkeypatch):
    monkeypatch.setenv('MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT', str(tmp_path / 'package'))
    with patch('media_ai.product_runtime.HfApi', side_effect=AssertionError('network client forbidden')):
        vault = ProductModelVault(tmp_path / 'data', '')
    assert vault.api is None
    for call in (lambda: vault._download_files('sam21', {}), vault._alternatives,
                 lambda: vault._alternative_files('revision', 'folder', [])):
        with pytest.raises(RuntimeError, match='disabled'): call()
    with pytest.raises(RuntimeError, match='unavailable'): vault.verify_local_models()


def test_local_snapshot_rejects_corruption(tmp_path, monkeypatch):
    monkeypatch.setenv('MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT', str(tmp_path))
    snapshot = tmp_path / 'models/sam21'; snapshot.mkdir(parents=True)
    (snapshot / 'config.json').write_text('wrong')
    vault = ProductModelVault(tmp_path / 'data', '')
    with pytest.raises(RuntimeError, match='mismatch'):
        vault._local_snapshot('sam21', {'config.json': (5, '0' * 64)})


def test_package_identity_requires_no_git(tmp_path, monkeypatch):
    import json
    monkeypatch.setenv('MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT', str(tmp_path))
    (tmp_path / 'PACKAGE_MANIFEST.json').write_text(json.dumps({'package_version': '1.0', 'build_commit': 'a' * 40,
                        'ui_fingerprint': 'b' * 64, 'model_manifest_hash': 'c' * 64}))
    server = object.__new__(ProductHttpServer); server.data_dir = tmp_path / 'data'; server.root = tmp_path / 'app'
    with patch('media_ai.product_server.subprocess.check_output', side_effect=AssertionError('git forbidden')):
        identity = server.runtime_identity()
    assert identity['runtime_mode'] == 'LOCAL_OFFLINE_PACKAGE'
    assert identity['distribution'] == 'EMPLOYEE_WIN_X64'
    assert identity['install_root'] == str(tmp_path)


def test_saved_jobs_survive_new_service_for_export_and_resave(tmp_path, monkeypatch):
    from media_ai.product_runtime import ProductJobService
    monkeypatch.delenv('MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT', raising=False)
    with patch('media_ai.product_runtime.ProductModelVault'):
        first = ProductJobService(tmp_path, '')
        output = tmp_path / 'jobs/result.txt'; output.write_text('actual saved output')
        first.records['job1'] = {'job_id': 'job1', 'status': 'TESTED_PASS', 'outputs': [{'path': str(output)}]}
        saved = first.save_project({'job_ids': ['job1']})
        second = ProductJobService(tmp_path, '')
        assert second.latest_project()['project_id'] == saved['project_id']
        assert second.records['job1']['status'] == 'TESTED_PASS'
        assert second.export_project(saved['project_id'])['status'] == 'EXPORTED'
        assert second.save_project({'project_id': saved['project_id'], 'job_ids': ['job1']})['status'] == 'SAVED'


def test_development_identity_keeps_fingerprints_when_git_is_unavailable(tmp_path, monkeypatch):
    import subprocess
    monkeypatch.delenv('MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT', raising=False)
    files = ('ui/index.html', 'ui/approved_visual.css', 'ui/interaction.css',
             'ui/interaction.js', 'ui/product_integration.js',
             'ui/assets/brand/MINDLE_MEDIA_AI_APP_ICON.ico')
    for relative in files:
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b'fixture')
    server = object.__new__(ProductHttpServer)
    server.root = tmp_path
    with patch('media_ai.product_server.subprocess.check_output',
               side_effect=subprocess.CalledProcessError(128, 'git')):
        identity = server.runtime_identity()
    assert identity['head'] is None and identity['branch'] is None
    assert identity['git_identity_status'] == 'UNAVAILABLE'
    assert len(identity['file_hashes']) == len(files)
    assert len(identity['workspace_ui_fingerprint']) == 64
