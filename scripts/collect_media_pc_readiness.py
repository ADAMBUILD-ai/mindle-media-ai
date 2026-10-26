"""Read-only target-machine facts. No install, model selection, or readiness claim."""
from __future__ import annotations
import argparse
import ctypes
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil


def sha(path):
    with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()


def collect(config_path=None,disk_path=None):
    result={'status':'READ_ONLY_FACTS_COLLECTED','platform':platform.platform(),'python':platform.python_version(),
            'machine':platform.machine(),'is_windows_target':os.name=='nt','cpu_count':os.cpu_count(),
            'windows_model_adoption':'NOT_APPROVED_BY_THIS_PROBE','full_product_pass':False,
            'available_memory_bytes':None,'installed_models_changed':False,'package_build':False}
    if os.name=='nt':
        class Memory(ctypes.Structure):
            _fields_=[('length',ctypes.c_ulong),('load',ctypes.c_ulong),*[(key,ctypes.c_ulonglong) for key in ('total_phys','avail_phys','total_page','avail_page','total_virtual','avail_virtual','extended')]]
        memory=Memory();memory.length=ctypes.sizeof(memory)
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memory)):
            result.update(total_memory_bytes=memory.total_phys,available_memory_bytes=memory.avail_phys)
    elif Path('/proc/meminfo').exists():
        values={line.split(':')[0]:int(line.split()[1])*1024 for line in Path('/proc/meminfo').read_text(encoding='utf-8').splitlines() if line.startswith(('MemTotal:','MemAvailable:'))}
        result.update(total_memory_bytes=values.get('MemTotal'),available_memory_bytes=values.get('MemAvailable'))
    target=Path(disk_path or Path.cwd()).resolve();usage=shutil.disk_usage(target)
    result['disk']={'path':str(target),'total_bytes':usage.total,'free_bytes':usage.free}
    if config_path:
        path=Path(config_path).resolve();result['config_path']=str(path)
        try:
            config=json.loads(path.read_text(encoding='utf-8-sig'));result['config_sha256']=sha(path);result['engine_files']=[]
            for kind in ('planner','tts'):
                value=config.get(kind,{})
                for key in ('model_path','executable'):
                    if value.get(key):
                        item=(path.parent/value[key]).resolve()
                        result['engine_files'].append({'kind':kind,'field':key,'path':str(item),'exists':item.is_file(),
                            'bytes':item.stat().st_size if item.is_file() else None,'sha256':sha(item) if item.is_file() else None})
                for part in value.get('additional_model_files',[]):
                    item=(path.parent/part['path']).resolve()
                    result['engine_files'].append({'kind':kind,'field':'additional_model_files','path':str(item),'exists':item.is_file(),
                        'bytes':item.stat().st_size if item.is_file() else None,'sha256':sha(item) if item.is_file() else None})
            result['declared_engine_settings']=config
        except (OSError,ValueError) as error:result['config_error']=str(error)
    return result


def main():
    p=argparse.ArgumentParser();p.add_argument('--engine-config');p.add_argument('--disk-path');p.add_argument('--output',required=True)
    a=p.parse_args();value=collect(a.engine_config,a.disk_path);out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(value['status'])


if __name__=='__main__':main()
