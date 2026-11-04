"""Reproduce Git CRLF delivery drift; restore Git bytes, never alter expectations."""
import hashlib
import importlib.util
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[1]


def test_force_checkout_restores_exact_git_bytes_after_autocrlf_conversion(tmp_path):
    def git(*args):return subprocess.check_output(['git',*args],cwd=tmp_path,stderr=subprocess.DEVNULL)
    git('init','-q');git('config','core.autocrlf','true')
    raw='{"label":"정확한 원본"}\nsecond line\n'.encode('utf-8')
    file=tmp_path/'identity.json';file.write_bytes(raw);git('add','identity.json')
    git('-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-qm','fixture')
    file.unlink();git('checkout-index','--all','--force')
    assert file.read_bytes()!=raw and b'\r\n' in file.read_bytes()
    spec=importlib.util.spec_from_file_location('restore_exact',ROOT/'scripts/restore_exact_status_source.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    receipt=module.restore(tmp_path,paths=('identity.json',))
    assert receipt['status']=='PASS_EXACT_GIT_SOURCE_BYTES'
    assert receipt['expected_hashes_modified'] is False
    assert receipt['files'][0]['changed_working_bytes'] is True
    assert hashlib.sha256(file.read_bytes()).digest()==hashlib.sha256(raw).digest()
    assert file.read_bytes()==git('show','HEAD:identity.json')


def test_windows_preflight_restores_delivery_before_checks_and_always_keeps_failure_evidence():
    source=(ROOT/'.github/workflows/pc-one-click-windows-fallback.yml').read_text(encoding='utf-8')
    assert source.index('restore_exact_status_source.py')<source.index('- name: Validate PC Work control plane')
    assert 'BEFORE_EXACT_CHECKOUT.json' in source and 'AFTER_EXACT_CHECKOUT.json' in source
    assert 'if: always()' in source.split('- name: Upload fallback preflight evidence',1)[1]


def test_exact_restore_cli_refuses_a_users_local_workspace(tmp_path):
    import os,sys
    result=subprocess.run([sys.executable,str(ROOT/'scripts/restore_exact_status_source.py'),'--output',str(tmp_path/'receipt.json')],
                          env={key:value for key,value in os.environ.items() if key!='GITHUB_ACTIONS'},capture_output=True,text=True)
    assert result.returncode!=0 and 'REFUSE_LOCAL_OVERWRITE' in result.stderr
    assert not (tmp_path/'receipt.json').exists()
