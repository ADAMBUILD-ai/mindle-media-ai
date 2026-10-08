"""CPU H.264 derivatives; retain model outputs and their immutable identity."""
from __future__ import annotations
import hashlib
import json
import os
import subprocess
from pathlib import Path

def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for part in iter(lambda: f.read(1024 * 1024), b''): h.update(part)
    return h.hexdigest()

def tools() -> tuple[str, str]:
    package = os.environ.get('MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT', '').strip()
    directory = Path(package) / 'tools/ffmpeg'
    return (str(directory/'ffmpeg.exe'), str(directory/'ffprobe.exe')) if package else ('ffmpeg','ffprobe')

def probe(path: Path) -> dict:
    _, ffprobe = tools()
    result = subprocess.run([ffprobe,'-v','error','-show_entries',
        'stream=codec_name,codec_tag_string,pix_fmt,width,height,duration:format=duration',
        '-of','json',str(path)], check=True, capture_output=True, text=True, timeout=30)
    return json.loads(result.stdout)

def faststart(path: Path) -> bool:
    boxes = []; size = path.stat().st_size
    with path.open('rb') as f:
        while f.tell() < size:
            header = f.read(8)
            if len(header) != 8: return False
            length = int.from_bytes(header[:4],'big'); kind = header[4:].decode('ascii',errors='replace')
            if length == 1:
                length = int.from_bytes(f.read(8),'big'); header_size = 16
            else: header_size = 8
            if length == 0: length = size - (f.tell()-header_size)
            if length < header_size: return False
            boxes.append(kind); f.seek(length-header_size,1)
    return 'moov' in boxes and 'mdat' in boxes and boxes.index('moov') < boxes.index('mdat')

def create_preview(source: Path, expected_sha256: str, destination: Path) -> dict:
    source, destination = Path(source), Path(destination)
    if source.resolve() == destination.resolve(): raise ValueError('original model output must be preserved')
    if digest(source) != expected_sha256: raise ValueError('original tracking SHA-256 mismatch')
    ffmpeg, _ = tools()
    version = subprocess.run([ffmpeg,'-version'],check=True,capture_output=True,text=True,timeout=30).stdout.splitlines()[0]
    encoders = subprocess.run([ffmpeg,'-hide_banner','-encoders'],check=True,capture_output=True,text=True,timeout=30).stdout
    if 'libx264' not in encoders: raise RuntimeError('verified H.264 encoder libx264 unavailable; no codec fallback')
    destination.parent.mkdir(parents=True,exist_ok=True)
    command = [ffmpeg,'-y','-i',str(source),'-map','0:v:0','-map','0:a?',
               '-vf','scale=trunc(iw/2)*2:trunc(ih/2)*2','-c:v','libx264',
               '-preset','veryfast','-pix_fmt','yuv420p','-c:a','aac',
               '-movflags','+faststart',str(destination)]
    subprocess.run(command,check=True,capture_output=True,timeout=600)
    info = probe(destination)
    video = next((s for s in info['streams'] if s.get('codec_name')=='h264'),None)
    if not video or video.get('pix_fmt') != 'yuv420p' or not faststart(destination):
        raise RuntimeError('H.264/yuv420p/faststart preview validation failed')
    if digest(source) != expected_sha256: raise RuntimeError('original tracking output changed')
    return {'status':'H264_PREVIEW_CREATED','model_output_preserved':True,
            'ffmpeg_version':version,'encoder':'libx264','command':command,
            'input':{'path':str(source),'sha256':expected_sha256},
            'output':{'path':str(destination),'file_name':destination.name,'bytes':destination.stat().st_size,'sha256':digest(destination)},
            'ffprobe':info,'faststart':True,'gpu_used':False,'paid_compute':False}
