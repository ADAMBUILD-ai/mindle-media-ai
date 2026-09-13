"""Pinned Whisper Turbo technical weight-load and generation smoke."""
import hashlib
import json
import os
import time
import wave
from pathlib import Path

import numpy as np
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor

os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
ROOT = Path(__file__).parent / "artifacts" / "whisper_turbo"
REPO_ID = "openai/whisper-large-v3-turbo"
REVISION = "41f01f3fe87f28c78e2fbf8b568835947dd65ed9"
SAMPLE_RATE = 16000


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    audio_path, transcript_path = ROOT / "silent_10s_16khz.wav", ROOT / "transcript.json"
    audio = np.zeros(SAMPLE_RATE * 10, dtype=np.int16)
    with wave.open(str(audio_path), "wb") as out:
        out.setnchannels(1); out.setsampwidth(2); out.setframerate(SAMPLE_RATE); out.writeframes(audio.tobytes())
    processor = AutoProcessor.from_pretrained(REPO_ID, revision=REVISION)
    model = AutoModelForSpeechSeq2Seq.from_pretrained(REPO_ID, revision=REVISION).eval()
    inputs = processor(audio.astype(np.float32) / 32768.0, sampling_rate=SAMPLE_RATE, return_tensors="pt")
    started = time.perf_counter()
    with torch.no_grad():
        tokens = model.generate(inputs.input_features, language="ko", task="transcribe", max_new_tokens=8)
    duration_ms = round((time.perf_counter() - started) * 1000, 2)
    text = processor.batch_decode(tokens, skip_special_tokens=True)[0]
    transcript_path.write_text(json.dumps({"language": "ko", "task": "transcribe", "text": text}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    evidence = {
        "status": "TECHNICAL_SMOKE_PASS", "repo_id": REPO_ID, "revision": REVISION,
        "runtime": {"torch": torch.__version__, "transformers": __import__("transformers").__version__, "provider": "CPU"},
        "duration_ms": duration_ms, "audio_sha256": sha256(audio_path), "transcript_sha256": sha256(transcript_path),
        "language_request": "ko", "fixture": "10-second silent WAV for model-load and generation only",
        "quality_gate": "VERIFY_REQUIRED: no Korean speech content, accuracy or timestamps are assessed by this smoke."
    }
    (ROOT / "result.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(evidence, ensure_ascii=False, indent=2))


if __name__ == "__main__": main()
