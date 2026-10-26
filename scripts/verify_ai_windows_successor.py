"""Independent readback of the single Windows AI successor candidate."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import zipfile

from build_ai_windows_successor import NAME, record, sha, write

producer = Path("producer-delivery")
evidence_source = Path("producer-evidence")
output = Path("verified-delivery")
evidence = Path("readback-r3")
output.mkdir(exist_ok=True)
evidence.mkdir(exist_ok=True)

delivery = json.loads(next(evidence_source.rglob("SUCCESSOR_DELIVERY.json")).read_text(encoding="utf-8-sig"))
acceptance = json.loads(next(evidence_source.rglob("ACCEPTANCE.json")).read_text(encoding="utf-8-sig"))
assert acceptance["status"] == "REMOTE_WINDOWS_EXE_QWEN_SUPERTONIC_MEASURED_ARCHITECTURE_RESTART_EXPORT_PASS"
starter = next(producer.rglob("MINDLE_MEDIA_AI_START_20261024_R3.zip"))
assert starter.stat().st_size == delivery["installer"]["bytes"] and sha(starter) == delivery["installer"]["sha256"]
shutil.copy2(starter, output / starter.name)
archive = output / delivery["name"]
with archive.open("wb") as target:
    for item in delivery["parts"]:
        part = next(producer.rglob(Path(item["path"]).name))
        assert part.stat().st_size == item["bytes"] and sha(part) == item["sha256"]
        with part.open("rb") as source:
            shutil.copyfileobj(source, target, 1024 * 1024)
assert archive.stat().st_size == delivery["bytes"] and sha(archive) == delivery["sha256"]
with zipfile.ZipFile(archive) as bundle:
    assert bundle.testzip() is None
    names = bundle.namelist()
    assert len(names) == len(set(names))
    prefix = NAME + "/_payload/"
    manifest_bytes = bundle.read(prefix + "PACKAGE_MANIFEST.json")
    assert hashlib.sha256(manifest_bytes).hexdigest() == delivery["manifest_sha256"]
    manifest = json.loads(manifest_bytes)
    assert manifest["build_commit"] == delivery["source"] == acceptance["source"]
    assert hashlib.sha256(bundle.read(NAME + "/MINDLE_MEDIA_AI_RUN.exe")).hexdigest() == delivery["exe_sha256"]
    for item in manifest["files"]:
        digest=hashlib.sha256();length=0
        with bundle.open(prefix + item["path"]) as source:
            while body:=source.read(1024*1024):digest.update(body);length+=len(body)
        assert length == item["bytes"] and digest.hexdigest() == item["sha256"], item["path"]
    assert not any("/__pycache__/" in name or name.endswith(".pyc") for name in names)

parts = []
with archive.open("rb") as source:
    index = 0
    while body := source.read(500 * 1024 * 1024):
        path = output / (archive.name + f".part-{index:02d}")
        path.write_bytes(body)
        parts.append(record(output, path))
        index += 1
write(evidence / "FINAL_DELIVERY.json", {
    **delivery,
    "parts": parts,
    "independent_all_payload_hashes": "PASS",
    "independent_zip_crc": "PASS",
    "actual_qwen": True,
    "actual_supertonic": True,
    "actual_measured_architecture_agent": True,
    "office_pc_acceptance": False,
    "human_hearing": False,
    "full_product_pass": False,
})
print("SUCCESSOR_INDEPENDENT_READBACK_PASS", delivery["sha256"], len(parts), flush=True)
