"""Reproduce Git CRLF delivery drift; restore Git bytes, never alter expectations."""
import hashlib
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[1]


def test_force_checkout_restores_exact_git_bytes_after_autocrlf_conversion(tmp_path):
    def git(*args):return subprocess.check_output(['git',*args],cwd=tmp_path,stderr=subprocess.DEVNULL)
    git('init','-q');git('config','core.autocrlf','true')
    raw='{"label":"정확한 원본"}\nsecond line\n'.encode('utf-8')
    file=tmp_path/'identity.json';file.write_bytes(raw);git('add','identity.json')
    git('-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-qm','fixture')
    git('checkout-index','--all','--force')
    assert file.read_bytes()!=raw and b'\r\n' in file.read_bytes()
    git('-c','core.autocrlf=false','-c','core.eol=lf','checkout-index','--all','--force')
    assert hashlib.sha256(file.read_bytes()).digest()==hashlib.sha256(raw).digest()
    assert file.read_bytes()==git('show','HEAD:identity.json')


def test_windows_preflight_restores_delivery_before_checks_and_always_keeps_failure_evidence():
    source=(ROOT/'.github/workflows/pc-one-click-windows-fallback.yml').read_text(encoding='utf-8')
    assert source.index('checkout-index --all --force')<source.index('- name: Validate PC Work control plane')
    assert 'BEFORE_EXACT_CHECKOUT.json' in source and 'AFTER_EXACT_CHECKOUT.json' in source
    assert 'if: always()' in source.split('- name: Upload fallback preflight evidence',1)[1]
