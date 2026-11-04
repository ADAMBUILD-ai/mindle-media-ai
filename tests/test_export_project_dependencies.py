"""Dependency bundle tests use generated fixtures, never model inference."""
import base64
import hashlib
import io
import json
from pathlib import Path
import zipfile
from unittest.mock import patch
import pytest
from PIL import Image
from media_ai.product_runtime import ProductJobService,file_record


def saved_fixture(tmp_path,monkeypatch):
    monkeypatch.delenv('MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT',raising=False)
    service=ProductJobService(tmp_path,'')
    pixels=io.BytesIO();Image.new('RGB',(90,160),(100,50,20)).save(pixels,'PNG')
    job=service.store_photo_edit({'content_base64':base64.b64encode(pixels.getvalue()).decode()})
    ref=service.jobs/job['job_id']/'references/portrait.png';ref.parent.mkdir()
    Image.new('RGB',(10,10),(20,50,100)).save(ref)
    job['reference_artifacts']=[file_record(ref)|{'original_filename':'portrait.png'}]
    saved=service.save_project({'job_ids':[job['job_id']]})
    return service,job,saved['project_id']


def test_input_and_reference_bytes_included_after_service_restart(tmp_path,monkeypatch):
    service,job,pid=saved_fixture(tmp_path,monkeypatch)
    reopened=ProductJobService(tmp_path,'')
    assert reopened.latest_project()['jobs'][0]['reference_artifacts']==job['reference_artifacts']
    exported=reopened.export_project(pid)
    with zipfile.ZipFile(exported['export']['path']) as z:
        manifest=json.loads(z.read('BUNDLE_MANIFEST.json'))
        assert manifest['project_id']==pid
        assert {f['role'] for f in manifest['files']}=={'input','reference','output'}
        assert len(manifest['files'])==3
        for entry in manifest['files']:
            content=z.read(entry['archive_path'])
            assert hashlib.sha256(content).hexdigest()==entry['sha256']
            assert len(content)==entry['bytes']
        saved=json.loads(z.read('project.json'))
        assert saved['jobs'][0]['reference_artifacts']==job['reference_artifacts']
        assert z.testzip() is None


@pytest.mark.parametrize('role',['input','reference'])
def test_changed_dependency_does_not_replace_previous_export(tmp_path,monkeypatch,role):
    service,job,pid=saved_fixture(tmp_path,monkeypatch)
    export=Path(service.export_project(pid)['export']['path']);before=export.read_bytes()
    artifact=job['input'] if role=='input' else job['reference_artifacts'][0]
    Path(artifact['path']).write_bytes(b'changed')
    with pytest.raises(ValueError,match='무결성'):service.export_project(pid)
    assert export.read_bytes()==before


def test_reference_changed_during_zip_write_is_detected(tmp_path,monkeypatch):
    service,job,pid=saved_fixture(tmp_path,monkeypatch)
    export=Path(service.export_project(pid)['export']['path']);before=export.read_bytes()
    reference=Path(job['reference_artifacts'][0]['path'])
    original=zipfile.ZipFile.write
    def replace_before_write(self,filename,*args,**kwargs):
        if Path(filename)==reference:reference.write_bytes(b'changed after preflight')
        return original(self,filename,*args,**kwargs)
    with patch.object(zipfile.ZipFile,'write',replace_before_write):
        with pytest.raises(ValueError,match='내보내는 중 파일이 변경'):service.export_project(pid)
    assert export.read_bytes()==before
    assert not list(service.projects.glob('*.tmp'))
