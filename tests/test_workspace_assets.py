"""Pending workspace attachment persistence; generated fixtures, no model calls."""
import base64, hashlib, io, json, wave, zipfile
from pathlib import Path
import pytest
from PIL import Image
from media_ai.product_runtime import ProductJobService

def image_bytes(color):
    stream=io.BytesIO();Image.new('RGB',(24,40),color).save(stream,'PNG');return stream.getvalue()

@pytest.fixture
def workspace(tmp_path,monkeypatch):
    monkeypatch.delenv('MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT',raising=False)
    service=ProductJobService(tmp_path,'')
    photo=image_bytes((80,100,120))
    job=service.store_photo_edit({'content_base64':base64.b64encode(photo).decode()})
    audio=io.BytesIO()
    with wave.open(audio,'wb') as wav:
        wav.setparams((1,2,16000,0,'NONE','not compressed'));wav.writeframes(bytes(3200))
    def attachment(name,content,mime):
        return {'filename':name,'content_base64':base64.b64encode(content).decode(),'mime_type':mime}
    payload={'references':{
        'photo':[attachment('사진 참고.png',image_bytes((30,50,70)),'image/png')],
        'video':[attachment('영상 참고.png',image_bytes((70,50,30)),'image/png')]},
        'audio':attachment('한국어 입력.wav',audio.getvalue(),'audio/wav')}
    return service,job,payload

def save(service,job,payload,**kw):
    return service.save_project({'job_ids':[job['job_id']],'workspace':payload,**kw})

def test_pending_references_audio_survive_restart_and_export(workspace):
    service,job,payload=workspace;pid=save(service,job,payload)['project_id']
    restarted=ProductJobService(service.root,'');project=restarted.latest_project()
    assert project['project_id']==pid
    ws=project['workspace']
    assert ws['references']['photo'][0]['original_filename']=='사진 참고.png'
    assert ws['references']['video'][0]['original_filename']=='영상 참고.png'
    assert ws['audio']['original_filename']=='한국어 입력.wav'
    with zipfile.ZipFile(restarted.export_project(pid)['export']['path']) as archive:
        assert archive.testzip() is None
        files=json.loads(archive.read('BUNDLE_MANIFEST.json'))['files']
        assert {f['role'] for f in files}=={'input','output','workspace_reference','workspace_audio'}
        assert len(files)==5
        for item in files:
            content=archive.read(item['archive_path'])
            assert len(content)==item['bytes'] and hashlib.sha256(content).hexdigest()==item['sha256']

def test_same_attachments_reuse_content_files(workspace):
    service,job,payload=workspace;pid=save(service,job,payload)['project_id']
    before=sorted((service.projects/(pid+'_assets')).iterdir())
    save(service,job,payload,project_id=pid)
    assert before==sorted((service.projects/(pid+'_assets')).iterdir())

def test_legacy_save_preserves_workspace(workspace):
    service,job,payload=workspace;pid=save(service,job,payload)['project_id']
    previous=json.loads((service.projects/(pid+'.json')).read_text(encoding='utf-8'))['workspace']
    service.save_project({'project_id':pid,'job_ids':[job['job_id']]})
    assert service.latest_project()['workspace']==previous

def test_explicit_clear_does_not_restore_old_attachments(workspace):
    service,job,payload=workspace;pid=save(service,job,payload)['project_id']
    save(service,job,{},project_id=pid)
    assert service.latest_project()['workspace']['references']=={'photo':[],'video':[]}
    assert service.latest_project()['workspace']['audio'] is None
    with zipfile.ZipFile(service.export_project(pid)['export']['path']) as archive:
        assert not any(n.startswith('workspace/') for n in archive.namelist())

@pytest.mark.parametrize('invalid',['bad_image','bad_audio_extension','too_many','path_payload'])
def test_invalid_workspace_preserves_saved_project(workspace,invalid):
    service,job,payload=workspace;pid=save(service,job,payload)['project_id']
    path=service.projects/(pid+'.json');previous=path.read_bytes()
    if invalid=='bad_image':payload['references']['photo'][0]['content_base64']=base64.b64encode(b'not image').decode()
    if invalid=='bad_audio_extension':payload['audio']['filename']='not-audio.exe'
    if invalid=='too_many':payload['references']['video']*=6
    if invalid=='path_payload':payload['audio']={'filename':'sound.wav','path':'C:/unapproved.wav'}
    with pytest.raises((ValueError,OSError)):
        save(service,job,payload,project_id=pid)
    assert path.read_bytes()==previous

def test_changed_workspace_file_does_not_replace_valid_export(workspace):
    service,job,payload=workspace;pid=save(service,job,payload)['project_id']
    archive=Path(service.export_project(pid)['export']['path']);before=archive.read_bytes()
    Path(service.latest_project()['workspace']['audio']['path']).write_bytes(b'corrupt')
    with pytest.raises(ValueError,match='무결성'):
        service.export_project(pid)
    assert archive.read_bytes()==before
