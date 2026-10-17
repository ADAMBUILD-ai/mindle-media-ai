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
