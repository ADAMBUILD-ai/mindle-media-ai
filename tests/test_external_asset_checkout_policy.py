from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_hashed_blender_driver_is_checkout_stable_on_windows():
    attributes = (ROOT / ".gitattributes").read_text(encoding="utf-8").splitlines()
    assert (
        "external_assets/media-production/blender/media_ai_blender_camera_render.py text eol=lf"
        in attributes
    )
