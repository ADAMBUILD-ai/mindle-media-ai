"""MEDIA-owned Blender background renderer; executed by Blender, not normal Python."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys

import bpy


def _sha(path):
    digest = sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", required=True)
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args(sys.argv[sys.argv.index("--") + 1:])
    request = json.loads(Path(args.request).read_text(encoding="utf-8"))
    if request.get("schema_version") != 1:
        raise ValueError("unsupported request schema")
    current_file = Path(bpy.data.filepath)
    if _sha(current_file) != request["blend_file_sha256"]:
        raise ValueError("opened .blend identity differs from request")
    camera = bpy.data.objects.get(request["camera"])
    if camera is None or camera.type != "CAMERA":
        raise ValueError("requested existing camera is unavailable")
    owned_root = Path(request["owned_job_root"]).resolve()
    output_dir = Path(request["output_dir"]).resolve()
    receipt_path = Path(args.receipt).resolve()
    if not output_dir.is_relative_to(owned_root) or not receipt_path.is_relative_to(owned_root):
        raise ValueError("job output escaped the owned root")
    frame_start = int(request["frame_start"])
    frame_end = int(request["frame_end"])
    fps = int(request["fps"])
    width = int(request["width"])
    height = int(request["height"])
    if not (1 <= frame_start <= frame_end <= 1_000_000):
        raise ValueError("invalid frame range")
    if not (1 <= fps <= 120 and 64 <= width <= 8192 and 64 <= height <= 8192):
        raise ValueError("invalid render settings")
    output_dir.mkdir(parents=True, exist_ok=True)
    scene = bpy.context.scene
    scene.camera = camera
    scene.frame_start = frame_start
    scene.frame_end = frame_end
    scene.render.fps = fps
    scene.render.resolution_x = width
    scene.render.resolution_y = height
    scene.render.filepath = str(output_dir / "frame_")
    bpy.ops.render.render(animation=True)
    files = sorted(p for p in output_dir.iterdir() if p.is_file())
    receipt = {"schema_version": 1, "camera": camera.name, "frames": [{"name": p.name, "size_bytes": p.stat().st_size, "sha256": _sha(p)} for p in files]}
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
