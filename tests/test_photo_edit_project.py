import base64
import io
import json
import zipfile
from unittest.mock import patch

from PIL import Image
from media_ai.product_runtime import ProductJobService


def test_pixel_edit_survives_service_restart_and_export(tmp_path, monkeypatch):
    monkeypatch.delenv('MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT', raising=False)
    pixels = io.BytesIO()
    Image.new('RGB', (9, 16), (190, 80, 30)).save(pixels, format='PNG')
    with patch('media_ai.product_runtime.ProductModelVault'):
        service = ProductJobService(tmp_path, '')
        job = service.store_photo_edit({'content_base64': base64.b64encode(pixels.getvalue()).decode(),
                                        'command': '따뜻하게 보정', 'options': {'temperature': 20}})
        assert job['runtime_result']['result_size'] == [9, 16]
        assert job['runtime_result']['model_inference'] is False
        saved = service.save_project({'job_ids': [job['job_id']]})
        reopened = ProductJobService(tmp_path, '')
        assert reopened.latest_project()['jobs'][0]['primary_output']['sha256'] == job['primary_output']['sha256']
        exported = reopened.export_project(saved['project_id'])
    with zipfile.ZipFile(exported['export']['path']) as archive:
        assert archive.testzip() is None
        assert json.loads(archive.read('project.json'))['jobs'][0]['operation'] == 'photo_edit'
        with Image.open(io.BytesIO(archive.read(f"jobs/{job['job_id']}/edited_photo.png"))) as output:
            assert output.size == (9, 16)
            assert output.getpixel((4, 8)) == (190, 80, 30)
