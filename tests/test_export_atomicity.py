import base64
import io
from pathlib import Path
from unittest.mock import patch
import zipfile
import pytest
from PIL import Image
from media_ai.product_runtime import ProductJobService


def project(tmp_path,monkeypatch):
    monkeypatch.delenv('MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT',raising=False)
    buf=io.BytesIO();Image.new('RGB',(9,16),(100,80,60)).save(buf,'PNG')
    with patch('media_ai.product_runtime.ProductModelVault'):
        service=ProductJobService(tmp_path,'')
        job=service.store_photo_edit({'content_base64':base64.b64encode(buf.getvalue()).decode()})
        saved=service.save_project({'job_ids':[job['job_id']]})
    return service,job,saved['project_id']


def test_interrupted_export_preserves_previous_download(tmp_path,monkeypatch):
    service,job,pid=project(tmp_path,monkeypatch)
    first=service.export_project(pid)
    archive=Path(first['export']['path']);before=archive.read_bytes()
    original=zipfile.ZipFile.write
    def fail_on_output(self,filename,*args,**kwargs):
        if str(filename)==job['primary_output']['path']:raise OSError('injected disk/write failure')
        return original(self,filename,*args,**kwargs)
    with patch.object(zipfile.ZipFile,'write',fail_on_output):
        with pytest.raises(OSError,match='injected'):service.export_project(pid)
    assert archive.read_bytes()==before
    assert not list(service.projects.glob('*.tmp'))
    with zipfile.ZipFile(archive) as z:assert z.testzip() is None
    assert service.export_project(pid)['status']=='EXPORTED'


def test_missing_output_rejected_without_replacing_export(tmp_path,monkeypatch):
    service,job,pid=project(tmp_path,monkeypatch)
    first=service.export_project(pid);archive=Path(first['export']['path']);before=archive.read_bytes()
    Path(job['primary_output']['path']).unlink()
    with pytest.raises(ValueError,match='누락'):service.export_project(pid)
    assert archive.read_bytes()==before
