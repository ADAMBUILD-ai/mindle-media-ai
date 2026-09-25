"""Concrete CPU adapters backed only by a verified local model cache.

The adapters never resolve model identifiers over the network.  Callers must pass
an already materialized snapshot and the exact verified weight identity.
"""
from __future__ import annotations

import gc
import hashlib
import json
import re
import time
from dataclasses import dataclass
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


@dataclass(frozen=True)
class VerifiedModelIdentity:
    repo_id: str
    revision: str
    license: str
    weight_name: str
    weight_size_bytes: int
    weight_sha256: str

    def verify_snapshot(self, snapshot: Path, required: set[str]) -> Path:
        snapshot = Path(snapshot)
        if not snapshot.is_dir():
            raise ValueError(f"verified snapshot is unavailable: {snapshot}")
        missing = sorted(name for name in required if not (snapshot / name).is_file())
        if missing:
            raise ValueError(f"verified snapshot is incomplete: {', '.join(missing)}")
        weight = snapshot / self.weight_name
        if weight.stat().st_size != self.weight_size_bytes:
            raise ValueError("verified weight byte count changed")
        if sha256_file(weight) != self.weight_sha256:
            raise ValueError("verified weight SHA-256 changed")
        return weight


class Sam21VerifiedAdapter:
    adapter_id = "mindle.sam21.verified.cpu"
    adapter_version = "1.0.1"
    runtime_backend = "transformers-pytorch"
    device_requirement = "cpu"
    required = {
        "config.json",
        "model.safetensors",
        "preprocessor_config.json",
        "processor_config.json",
    }

    def __init__(self, snapshot: Path, identity: VerifiedModelIdentity) -> None:
        import torch
        from transformers import AutoModelForMaskGeneration, AutoProcessor

        self.snapshot = Path(snapshot)
        self.identity = identity
        self.weight = identity.verify_snapshot(self.snapshot, self.required)
        self.torch = torch
        self.processor = AutoProcessor.from_pretrained(
            self.snapshot, local_files_only=True, trust_remote_code=False
        )
        self.model = AutoModelForMaskGeneration.from_pretrained(
            self.snapshot,
            local_files_only=True,
            trust_remote_code=False,
            use_safetensors=True,
        ).to("cpu").eval()

    def _mask(self, image, point: tuple[int, int]):
        import numpy as np

        inputs = self.processor(
            images=image,
            input_points=[[[[int(point[0]), int(point[1])]]]],
            return_tensors="pt",
        )
        started = time.perf_counter()
        with self.torch.inference_mode():
            result = self.model(**inputs)
        scores = result.iou_scores[0, 0].detach().cpu()
        ranked = scores.argsort(descending=True).tolist()
        selected = int(ranked[0])
        binary = None
        for candidate in ranked:
            raw = result.pred_masks[0, 0, int(candidate)][None, None]
            mask = self.torch.nn.functional.interpolate(
                raw,
                size=(image.height, image.width),
                mode="bilinear",
                align_corners=False,
            )[0, 0]
            candidate_binary = (mask.detach().cpu().numpy() > 0).astype(np.uint8) * 255
            fraction = float((candidate_binary > 0).mean())
            binary = candidate_binary
            selected = int(candidate)
            if 0.001 < fraction < 0.999:
                break
        return binary, selected, round((time.perf_counter() - started) * 1000, 2)

    @staticmethod
    def _overlay(image, mask):
        import numpy as np
        from PIL import Image

        base = np.asarray(image.convert("RGB"), dtype=np.uint8).copy()
        selected = mask > 0
        base[selected] = (0.55 * base[selected] + 0.45 * np.array([255, 32, 32])).astype(np.uint8)
        return Image.fromarray(base)

    def segment_photo(self, input_path: Path, output_dir: Path, prompt_point: tuple[int, int] | None = None) -> dict:
        import numpy as np
        from PIL import Image

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        image = Image.open(input_path).convert("RGB")
        source_width, source_height = image.size
        image.thumbnail((640, 640))
        if prompt_point is None:
            point = (image.width // 2, image.height // 2)
        else:
            # The approved UI supplies the target in source-image coordinates.
            # Scale it only after the bounded SAM preprocessing resize.
            point = (
                min(image.width - 1, max(0, round(int(prompt_point[0]) * image.width / source_width))),
                min(image.height - 1, max(0, round(int(prompt_point[1]) * image.height / source_height))),
            )
        mask, selected, elapsed = self._mask(image, point)
        fraction = float((mask > 0).mean())
        if not 0.001 < fraction < 0.999:
            raise RuntimeError(f"SAM photo mask is degenerate: foreground_fraction={fraction}")
        mask_path = output_dir / "photo_mask.png"
        overlay_path = output_dir / "photo_overlay.png"
        Image.fromarray(mask).save(mask_path)
        self._overlay(image, mask).save(overlay_path)
        return {
            "status": "TESTED_PASS",
            "input_path": str(input_path),
            "input_sha256": sha256_file(input_path),
            "prompt_point": list(point),
            "selected_mask_index": selected,
            "foreground_fraction": fraction,
            "elapsed_ms": elapsed,
            "outputs": [
                {"path": str(mask_path), "sha256": sha256_file(mask_path), "bytes": mask_path.stat().st_size},
                {"path": str(overlay_path), "sha256": sha256_file(overlay_path), "bytes": overlay_path.stat().st_size},
            ],
        }

    def track_video(self, input_path: Path, output_dir: Path, sample_count: int = 4) -> dict:
        import cv2
        import numpy as np
        from PIL import Image

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        capture = cv2.VideoCapture(str(input_path))
        if not capture.isOpened():
            raise RuntimeError("SAM video input could not be decoded")
        total = max(int(capture.get(cv2.CAP_PROP_FRAME_COUNT)), sample_count)
        indexes = sorted({round(i * (total - 1) / (sample_count - 1)) for i in range(sample_count)})
        rows, overlays, previous_mask = [], [], None
        point = None
        for sample_no, frame_index in enumerate(indexes):
            capture.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
            ok, bgr = capture.read()
            if not ok:
                raise RuntimeError(f"SAM video frame {frame_index} could not be decoded")
            rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(rgb)
            image.thumbnail((512, 512))
            if point is None:
                point = (image.width // 2, image.height // 2)
            mask, selected, elapsed = self._mask(image, point)
            foreground = mask > 0
            fraction = float(foreground.mean())
            if not 0.001 < fraction < 0.999:
                raise RuntimeError(f"SAM tracking mask {sample_no} is degenerate: {fraction}")
            ys, xs = np.nonzero(foreground)
            centroid = (int(xs.mean()), int(ys.mean()))
            iou = None
            if previous_mask is not None:
                intersection = np.logical_and(previous_mask > 0, foreground).sum()
                union = np.logical_or(previous_mask > 0, foreground).sum()
                iou = float(intersection / union) if union else 0.0
            mask_path = output_dir / f"track_1_frame_{sample_no:02d}_mask.png"
            overlay_path = output_dir / f"track_1_frame_{sample_no:02d}_overlay.png"
            Image.fromarray(mask).save(mask_path)
            overlay = self._overlay(image, mask)
            overlay.save(overlay_path)
            overlays.append(np.asarray(overlay.convert("RGB")))
            rows.append({
                "track_id": 1,
                "source_frame_index": frame_index,
                "prompt_point": list(point),
                "centroid": list(centroid),
                "selected_mask_index": selected,
                "foreground_fraction": fraction,
                "iou_with_previous_sample": iou,
                "elapsed_ms": elapsed,
                "mask_path": str(mask_path),
                "mask_sha256": sha256_file(mask_path),
                "overlay_path": str(overlay_path),
                "overlay_sha256": sha256_file(overlay_path),
            })
            point, previous_mask = centroid, mask
        capture.release()
        video_path = output_dir / "track_1_overlays.mp4"
        height, width = overlays[0].shape[:2]
        writer = cv2.VideoWriter(str(video_path), cv2.VideoWriter_fourcc(*"mp4v"), 2.0, (width, height))
        if not writer.isOpened():
            raise RuntimeError("SAM tracking output video could not be opened")
        for frame in overlays:
            writer.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
        writer.release()
        if not video_path.is_file() or video_path.stat().st_size == 0:
            raise RuntimeError("SAM tracking output video is empty")
        manifest_path = output_dir / "tracking.json"
        manifest_path.write_text(json.dumps({"track_id": 1, "samples": rows}, indent=2) + "\n", encoding="utf-8")
        return {
            "status": "TESTED_PASS",
            "input_path": str(input_path),
            "input_sha256": sha256_file(input_path),
            "track_id": 1,
            "sampled_frames": len(rows),
            "samples": rows,
            "outputs": [
                {"path": str(video_path), "sha256": sha256_file(video_path), "bytes": video_path.stat().st_size},
                {"path": str(manifest_path), "sha256": sha256_file(manifest_path), "bytes": manifest_path.stat().st_size},
            ],
        }

    def close(self) -> None:
        del self.model
        del self.processor
        gc.collect()


class WhisperKoreanVerifiedAdapter:
    adapter_id = "mindle.whisper.ko.verified.cpu"
    adapter_version = "1.0.0"
    runtime_backend = "transformers-pytorch"
    device_requirement = "cpu"
    required = {
        "config.json",
        "generation_config.json",
        "model.safetensors",
        "preprocessor_config.json",
        "tokenizer.json",
        "tokenizer_config.json",
    }

    def __init__(self, snapshot: Path, identity: VerifiedModelIdentity) -> None:
        import torch
        from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor

        self.snapshot = Path(snapshot)
        self.identity = identity
        self.weight = identity.verify_snapshot(self.snapshot, self.required)
        self.torch = torch
        self.processor = AutoProcessor.from_pretrained(
            self.snapshot, local_files_only=True, trust_remote_code=False
        )
        self.model = AutoModelForSpeechSeq2Seq.from_pretrained(
            self.snapshot,
            local_files_only=True,
            trust_remote_code=False,
            use_safetensors=True,
        ).to("cpu").eval()

    def transcribe(self, input_path: Path, output_dir: Path, reference: str | None = None) -> dict:
        import soundfile as sf
        from jiwer import wer

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        audio, sample_rate = sf.read(str(input_path), dtype="float32")
        if getattr(audio, "ndim", 1) == 2:
            audio = audio.mean(axis=1)
        if sample_rate != 16000:
            raise RuntimeError(f"expected 16 kHz Korean input, got {sample_rate}")
        inputs = self.processor(audio, sampling_rate=sample_rate, return_tensors="pt")
        started = time.perf_counter()
        with self.torch.inference_mode():
            tokens = self.model.generate(
                inputs.input_features,
                language="ko",
                task="transcribe",
                max_new_tokens=128,
                do_sample=False,
            )
        elapsed = round((time.perf_counter() - started) * 1000, 2)
        text = self.processor.batch_decode(tokens, skip_special_tokens=True)[0].strip()
        error_rate = float(wer(reference, text)) if reference else None
        if not text or re.search(r"[가-힣]", text) is None or (error_rate is not None and error_rate > 0.75):
            raise RuntimeError(
                f"Korean STT quality gate failed: nonempty={bool(text)}, hangul={bool(re.search(r'[가-힣]', text))}, wer={error_rate}"
            )
        transcript_path = output_dir / "korean_transcript.json"
        transcript_path.write_text(
            json.dumps(
                {
                    "language": "ko",
                    "task": "transcribe",
                    "reference": reference,
                    "text": text,
                    "word_error_rate": error_rate,
                },
                ensure_ascii=False,
                indent=2,
            ) + "\n",
            encoding="utf-8",
        )
        return {
            "status": "TESTED_PASS",
            "input_path": str(input_path),
            "input_sha256": sha256_file(input_path),
            "sample_rate": sample_rate,
            "duration_seconds": len(audio) / sample_rate,
            "reference": reference,
            "text": text,
            "word_error_rate": error_rate,
            "elapsed_ms": elapsed,
            "outputs": [
                {"path": str(transcript_path), "sha256": sha256_file(transcript_path), "bytes": transcript_path.stat().st_size}
            ],
        }

    def close(self) -> None:
        del self.model
        del self.processor
        gc.collect()
