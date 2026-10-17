"""Real loopback HTTP with no models; owner stop never kills another PID."""
import json
import os
from pathlib import Path
import threading
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import pytest
from media_ai.product_server import create_server

@pytest.fixture
def live(tmp_path, monkeypatch):
    monkeypatch.delenv('MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT', raising=False)
    server = create_server(Path(__file__).resolve().parents[1], tmp_path / 'data', '', 0)
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    yield server, worker, f'http://127.0.0.1:{server.server_port}'
    if worker.is_alive():
        server.shutdown()
    server.server_close()
    worker.join(timeout=5)

def call(base, route, body=None, headers=None):
    headers = dict(headers or {})
    if body is not None:
        headers['Content-Type'] = 'application/json'
    req = Request(base + route, data=None if body is None else json.dumps(body).encode(), headers=headers)
    with urlopen(req, timeout=5) as response:
        return response.status, json.load(response), response.headers

def control(base):
    _, info, _ = call(base, '/api/runtime/control')
    body = {k: info[k] for k in ('server_pid', 'server_instance_id')}
    return body, {'X-Mindle-Control': info['control_nonce']}

def test_runtime_identity_reports_own_pid_and_per_instance_identity(live):
    server, _, base = live
    _, value, headers = call(base, '/api/runtime-identity')
    assert value['server_pid'] == os.getpid()
    assert value['server_instance_id'] == server.instance_id
    assert value['server_command'] and value['server_started_at']
    assert 'control_nonce' not in value
    assert 'no-store' in headers['Cache-Control']

@pytest.mark.parametrize('headers', [{'Origin': 'https://foreign.example'},
    {'Host': 'foreign.example'}, {'Sec-Fetch-Site': 'cross-site'}])
def test_foreign_browser_cannot_acquire_owner_control(live, headers):
    _, _, base = live
    with pytest.raises(HTTPError) as error:
        call(base, '/api/runtime/control', headers=headers)
    assert error.value.code == 403

def test_missing_nonce_wrong_identity_and_busy_work_do_not_stop(live):
    server, worker, base = live
    body, headers = control(base)
    for payload, auth, code in [(body, {}, 403),
        (body, {**headers, 'Origin': 'https://foreign.example'}, 403),
        ({**body, 'server_instance_id': 'old-instance'}, headers, 409),
        ({**body, 'server_pid': -1}, headers, 409), ([], headers, 400)]:
        with pytest.raises(HTTPError) as error:
            call(base, '/api/runtime/shutdown', payload, auth)
        assert error.value.code == code
        assert worker.is_alive() and not server.stopping
    assert server.begin_request()
    try:
        with pytest.raises(HTTPError) as error:
            call(base, '/api/runtime/shutdown', body, headers)
        assert error.value.code == 409
    finally:
        server.end_request()
    assert not server.stopping

def test_confirmed_owner_stop_returns_and_new_requests_are_refused(live):
    server, worker, base = live
    body, headers = control(base)
    status, value, _ = call(base, '/api/runtime/shutdown', body, headers)
    assert status == 202 and value['server_instance_id'] == server.instance_id
    worker.join(timeout=5)
    assert not worker.is_alive()
    assert not server.begin_request()
    assert server.active_requests == 0


@pytest.mark.parametrize('operation', ['save', 'edit', 'download'])
def test_owner_stop_does_not_interrupt_real_inflight_requests(live, monkeypatch, operation):
    """Pause a real request at the I/O boundary, never add a product bypass."""
    from concurrent.futures import ThreadPoolExecutor
    from io import BytesIO
    import base64
    from PIL import Image
    from media_ai.product_server import Handler
    server, worker, base = live
    body, headers = control(base)
    entered, release = threading.Event(), threading.Event()
    def gate(action):
        def delayed(*args, **kwargs):
            entered.set()
            assert release.wait(3), 'test must release the held request'
            return action(*args, **kwargs)
        return delayed
    if operation == 'save':
        seed = BytesIO(); Image.new('RGB', (4, 3), 'blue').save(seed, 'PNG')
        job = server.service.store_photo_edit({'filename': 'seed.png',
            'content_base64': base64.b64encode(seed.getvalue()).decode(), 'options': {}})
        monkeypatch.setattr(server.service, 'save_project', gate(server.service.save_project))
        request = lambda: call(base, '/api/projects/save', {'project_id': None, 'job_ids': [job['job_id']]})
    elif operation == 'edit':
        image = BytesIO(); Image.new('RGB', (4, 3), 'blue').save(image, 'PNG')
        monkeypatch.setattr(server.service, 'store_photo_edit', gate(server.service.store_photo_edit))
        request = lambda: call(base, '/api/photo-edits', {'filename': 'edit.png',
            'content_base64': base64.b64encode(image.getvalue()).decode(), 'options': {}})
    else:
        path = server.data_dir / 'download.bin'; path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b'unchanged actual download')
        monkeypatch.setattr(Handler, '_file', gate(Handler._file))
        def request():
            with urlopen(base + '/files/download.bin', timeout=5) as response:
                return response.status, response.read(), response.headers
    with ThreadPoolExecutor(max_workers=1) as pool:
        pending = pool.submit(request)
        try:
            assert entered.wait(3)
            with pytest.raises(HTTPError) as error:
                call(base, '/api/runtime/shutdown', body, headers)
            assert error.value.code == 409
            assert worker.is_alive() and not server.stopping
            assert not pending.done()
        finally:
            release.set()
        status, result, _ = pending.result(timeout=5)
        assert status == (200 if operation == 'download' else 201)
        if operation == 'download': assert result == b'unchanged actual download'
    # A rejected stop must leave the runtime accepting subsequent work.
    assert call(base, '/api/runtime-identity')[0] == 200
