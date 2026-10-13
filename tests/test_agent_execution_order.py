import base64
from unittest.mock import patch
from pathlib import Path
import pytest
from PIL import Image
from media_ai.product_runtime import ProductJobService

def test_rejected_handoff_cannot_invoke_adapter_and_failure_survives_restart(tmp_path):
    source=tmp_path/'source.png';Image.new('RGB',(100,60)).save(source)
    service=ProductJobService(tmp_path/'data','')
    calls=[]
    class Adapter:
        weight=source
        def segment_photo(self,*args):calls.append('inference');raise AssertionError('must not run')
        def close(self):calls.append('close')
    with patch.object(service.vault,'sam',return_value=(Adapter(),{})),patch.object(service,'_handoff',side_effect=RuntimeError('gate rejection')):
        with pytest.raises(RuntimeError,match='gate rejection'):
            service.execute({'lane':'photo','operation':'segment','command':'분할','filename':'source.png','content_base64':base64.b64encode(source.read_bytes()).decode()})
    assert calls==['close']
    failed=next(iter(service.records.values()))
    assert failed['status']=='FAILED' and failed['state']=='failed'
    assert failed['state_history']==['queued','validating','failed']
    assert ProductJobService(tmp_path/'data','').records[failed['job_id']]==failed

def test_right_person_instruction_has_spatial_precedence(tmp_path):
    source=tmp_path/'source.png';Image.new('RGB',(100,60)).save(source)
    assert ProductJobService._photo_target_point('오른쪽 인물을 분리해줘',source)==(74,32)
    assert ProductJobService._photo_target_point('왼쪽 인물을 분리해줘',source)==(26,32)
