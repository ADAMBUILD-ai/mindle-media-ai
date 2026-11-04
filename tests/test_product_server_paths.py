"""Real HTTP delivery for relative and Windows short-form data roots."""
import ctypes
import os
from pathlib import Path
import threading
from urllib.error import HTTPError
from urllib.request import Request,urlopen
import pytest
from media_ai.product_server import create_server


def serve_check(root,data_root,range_header=None):
    server=create_server(root,data_root,'',0)
    media=server.data_dir/'test.bin';media.write_bytes(b'abcdefgh')
    worker=threading.Thread(target=server.serve_forever,daemon=True);worker.start()
    try:
        request=Request(f'http://127.0.0.1:{server.server_port}/files/test.bin',headers={} if range_header is None else {'Range':range_header})
        with urlopen(request,timeout=5) as response:
            assert response.read()==(b'abcdefgh' if range_header is None else b'abcd')
            assert response.status==(200 if range_header is None else 206)
        assert server.data_dir==Path(data_root).resolve()
    finally:
        server.shutdown();server.server_close();worker.join(timeout=5)


@pytest.mark.parametrize('range_header',[None,'bytes=0-3'])
def test_relative_data_root_delivers_saved_bytes(tmp_path,monkeypatch,range_header):
    monkeypatch.delenv('MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT',raising=False)
    root=Path(__file__).resolve().parents[1]
    monkeypatch.chdir(tmp_path)
    serve_check(root,Path('data'),range_header)


@pytest.mark.skipif(os.name!='nt',reason='native Windows 8.3 path support required')
def test_windows_short_data_root_delivers_same_file(tmp_path,monkeypatch):
    monkeypatch.delenv('MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT',raising=False)
    data=tmp_path/'Long Media Data Folder';data.mkdir()
    api=ctypes.windll.kernel32.GetShortPathNameW
    api.argtypes=[ctypes.c_wchar_p,ctypes.c_wchar_p,ctypes.c_uint32]
    api.restype=ctypes.c_uint32
    buffer=ctypes.create_unicode_buffer(32768)
    size=api(str(data),buffer,len(buffer))
    assert 0<size<len(buffer)
    serve_check(Path(__file__).resolve().parents[1],Path(buffer.value),'bytes=0-3')


def test_outside_data_root_remains_unavailable(tmp_path,monkeypatch):
    monkeypatch.delenv('MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT',raising=False)
    server=create_server(Path(__file__).resolve().parents[1],tmp_path/'data','',0)
    (tmp_path/'outside.bin').write_bytes(b'outside')
    worker=threading.Thread(target=server.serve_forever,daemon=True);worker.start()
    try:
        with pytest.raises(HTTPError) as error:urlopen(f'http://127.0.0.1:{server.server_port}/files/../outside.bin',timeout=5)
        assert error.value.code==404
    finally:
        server.shutdown();server.server_close();worker.join(timeout=5)
