"""Fail-closed CUDA SAM 2.1 video-memory tracking with durable evidence."""
import json
import os
import subprocess
import time
from pathlib import Path

import cv2
import numpy as np

from .verified_model_adapters import sha256_file


class ContinuousSamTracking:
    """Track only a source-reference-selected subject; never use CPU or a centre prompt."""

    adapter_id = "mindle.sam21.video.memory.cuda"
    adapter_version = "2.0.1"
    runtime_backend = "transformers-sam2-video-pytorch-cuda"
    device_requirement = "cuda"
    cut_threshold = 0.45
    reference_threshold = 0.75

    def __init__(self, snapshot, identity):
        import torch
        from transformers import Sam2ImageProcessorFast, Sam2VideoConfig, Sam2VideoModel, Sam2VideoProcessor, Sam2VideoVideoProcessor
        if not torch.cuda.is_available():
            raise RuntimeError("TRACKING_RUNTIME_BLOCKED: CUDA PyTorch runtime is required; CPU tracking is forbidden")
        self.identity = identity
        self.weight = identity.verify_snapshot(Path(snapshot), {"config.json", "model.safetensors", "preprocessor_config.json", "processor_config.json"})
        self.torch, self.device = torch, "cuda:0"
        properties = torch.cuda.get_device_properties(0)
        self.runtime_identity = {"device": self.device, "gpu_name": properties.name, "vram_total_bytes": int(properties.total_memory), "cuda_runtime": str(torch.version.cuda), "torch_version": str(torch.__version__), "cuda_available": True}
        config = Sam2VideoConfig.from_pretrained(snapshot, local_files_only=True)
        config.image_size = config.prompt_encoder_config.image_size = config.vision_config.image_size = 512
        config.vision_config.backbone_feature_sizes = [(128, 128), (64, 64), (32, 32)]
        config.memory_attention_rope_feat_sizes = [32, 32]
        self.model, loading = Sam2VideoModel.from_pretrained(snapshot, config=config, local_files_only=True, trust_remote_code=False, output_loading_info=True)
        if loading.get("missing_keys") or loading.get("mismatched_keys"):
            raise RuntimeError("Pinned checkpoint does not contain the complete video memory engine")
        # A video session is deliberately created in fp16 to fit the pinned
        # SAM 2.1 engine into the approved CUDA envelope.  The model and every
        # frame tensor must use that exact dtype.  Leaving the loaded checkpoint
        # in fp32 lets a half frame reach an fp32 Conv2d bias, which fails only
        # after a real job has started (rather than at the runtime gate).
        self.inference_dtype = torch.float16
        self.model = self.model.to(device=self.device, dtype=self.inference_dtype).eval()
        if not next(self.model.parameters()).is_cuda:
            raise RuntimeError("TRACKING_RUNTIME_BLOCKED: SAM model was not placed on CUDA")
        self.processor = Sam2VideoProcessor(
            image_processor=Sam2ImageProcessorFast.from_pretrained(snapshot, local_files_only=True, size={"height": 512, "width": 512}),
            video_processor=Sam2VideoVideoProcessor(size={"height": 512, "width": 512}), target_size=512)

    @staticmethod
    def _validate_point(point, width, height):
        if (not isinstance(point, (tuple, list)) or len(point) != 2 or any(type(value) not in (int, float) for value in point) or not 0 <= point[0] < width or not 0 <= point[1] < height):
            raise RuntimeError("TRACKING_TARGET_REFERENCE_REQUIRED: source-matched target reference is required")
        return round(point[0]), round(point[1])

    def _reference_point(self, frame, template):
        if template is None or template.shape[0] > frame.shape[0] or template.shape[1] > frame.shape[1] or template.std() < 2:
            raise RuntimeError("TRACKING_TARGET_REFERENCE_INVALID: target reference must be a distinguishable source-frame crop")
        scores = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
        _, score, _, location = cv2.minMaxLoc(scores)
        if score < self.reference_threshold:
            raise RuntimeError("TRACKING_CUT_TARGET_REFERENCE_MISMATCH: target was not found after scene cut")
        return (location[0] + template.shape[1] // 2, location[1] + template.shape[0] // 2), float(score)

    @staticmethod
    def _scene_distance(previous, current):
        def histogram(frame):
            sample = cv2.resize(frame, (160, 90))
            value = cv2.calcHist([sample], [0, 1, 2], None, [8, 8, 8], [0, 256] * 3)
            return cv2.normalize(value, value)
        return float(cv2.compareHist(histogram(previous), histogram(current), cv2.HISTCMP_BHATTACHARYYA))

    def _new_session(self, frame, point, session_id, start_frame, score, reason):
        inputs = self.processor(images=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), device=self.device, return_tensors="pt")
        session = self.processor.init_video_session(inference_device=self.device, dtype=self.inference_dtype)
        self.processor.add_inputs_to_inference_session(inference_session=session, frame_idx=0, obj_ids=1, input_points=[[[[point[0], point[1]]]]], input_labels=[[[1]]], original_size=inputs.original_sizes[0])
        return session, inputs, {"session_id": session_id, "start_frame": start_frame, "target_point": list(point), "reference_match_score": score, "restart_reason": reason}

    def track_video(self, source, directory, command="", target_point=None, target_reference=None):
        del command
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        masks_dir, log_path = directory / "masks", directory / "FRAME_TRACKING_LOG.jsonl"
        masks_dir.mkdir()
        capture = cv2.VideoCapture(str(source))
        fps = capture.get(cv2.CAP_PROP_FPS)
        if not capture.isOpened() or fps <= 0:
            raise RuntimeError("영상 원본을 읽을 수 없습니다.")
        width, height = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        ok, first_frame = capture.read()
        if not ok:
            capture.release()
            raise RuntimeError("영상의 첫 프레임을 읽을 수 없습니다.")
        point = self._validate_point(target_point, width, height)
        template = cv2.imread(str(target_reference)) if target_reference else None
        matched_point, first_score = self._reference_point(first_frame, template)
        if max(abs(matched_point[0] - point[0]), abs(matched_point[1] - point[1])) > 2:
            capture.release()
            raise RuntimeError("TRACKING_TARGET_REFERENCE_MISMATCH: reference and initial target point differ")
        raw = directory / "tracking_frames.mp4"
        writer = cv2.VideoWriter(str(raw), cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))
        if not writer.isOpened():
            capture.release()
            raise RuntimeError("영상 출력기를 열 수 없습니다.")
        started, rows, sessions, ious = time.perf_counter(), [], [], []
        previous_frame, previous_mask = None, None
        session_id, session_frame = 0, 0
        session, initial_inputs, session_info = self._new_session(first_frame, point, 0, 0, first_score, "initial")
        sessions.append(session_info)

        def process(frame, frame_index, distance, restarted):
            nonlocal session_frame, previous_mask
            frame_inputs = initial_inputs if session_frame == 0 else self.processor(images=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), device=self.device, return_tensors="pt")
            frame_tensor = frame_inputs.pixel_values[0].to(device=self.device, dtype=self.inference_dtype)
            if frame_tensor.dtype != self.inference_dtype:
                raise RuntimeError("TRACKING_RUNTIME_BLOCKED: SAM frame dtype does not match the CUDA model dtype")
            result = self.model(inference_session=session, frame=frame_tensor)
            mask = self.processor.post_process_masks([result.pred_masks], original_sizes=frame_inputs.original_sizes, binarize=False)[0].squeeze().detach().float().cpu().numpy() > 0
            if mask.shape != (height, width):
                raise RuntimeError("영상 mask 비율이 원본과 다릅니다.")
            mask_path = masks_dir / f"frame_{frame_index:06d}.png"
            if not cv2.imwrite(str(mask_path), mask.astype(np.uint8) * 255):
                raise RuntimeError("추적 마스크를 저장하지 못했습니다.")
            overlay = frame.copy()
            overlay[mask] = (0.55 * frame[mask] + 0.45 * np.array([32, 32, 255])).astype(np.uint8)
            writer.write(overlay)
            iou = None
            if previous_mask is not None:
                union = np.logical_or(previous_mask, mask).sum()
                iou = float(np.logical_and(previous_mask, mask).sum() / union) if union else 1.0
                ious.append(iou)
            row = {"frame_index": frame_index, "session_id": session_id, "session_frame_index": session_frame, "foreground_fraction": float(mask.mean()), "consecutive_mask_iou": iou, "scene_distance": distance, "session_restarted": restarted, "mask": {"path": str(mask_path), "sha256": sha256_file(mask_path), "bytes": mask_path.stat().st_size}}
            rows.append(row)
            with log_path.open("a", encoding="utf-8") as stream:
                stream.write(json.dumps(row, ensure_ascii=False) + "\n")
            previous_mask = mask
            session_frame += 1

        try:
            with self.torch.inference_mode():
                process(first_frame, 0, None, False)
                previous_frame, frame_index = first_frame, 1
                while True:
                    ok, frame = capture.read()
                    if not ok:
                        break
                    distance = self._scene_distance(previous_frame, frame)
                    restarted = False
                    if distance >= self.cut_threshold:
                        cut_point, score = self._reference_point(frame, template)
                        session_id += 1
                        session_frame, previous_mask = 0, None
                        session, initial_inputs, session_info = self._new_session(frame, cut_point, session_id, frame_index, score, "scene_cut")
                        sessions.append(session_info)
                        restarted = True
                    process(frame, frame_index, distance, restarted)
                    previous_frame, frame_index = frame, frame_index + 1
        finally:
            capture.release()
            writer.release()
        if not rows or not any(row["foreground_fraction"] > 0 for row in rows):
            raise RuntimeError("추적 대상 결과가 없습니다.")
        package = os.environ.get("MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT")
        ffmpeg = str(Path(package) / "tools/ffmpeg/ffmpeg.exe") if package else "ffmpeg"
        encoder = "h264_mf" if package and os.name == "nt" else "libx264"
        output = directory / "track_1_overlays.mp4"
        completed = subprocess.run([ffmpeg, "-y", "-i", str(raw), "-i", str(source), "-map", "0:v:0", "-map", "1:a?", "-c:v", encoder, "-pix_fmt", "yuv420p", "-c:a", "aac", "-movflags", "+faststart", str(output)], check=True, capture_output=True, text=True)
        manifest = directory / "tracking.json"
        manifest.write_text(json.dumps({"engine": "SAM2_VIDEO_MEMORY", "tracking_mode": "continuous_video_memory_per_scene", "fps": fps, "width": width, "height": height, "tracked_frames": len(rows), "target_reference": {"sha256": sha256_file(Path(target_reference)), "threshold": self.reference_threshold}, "scene_cut_policy": {"detector": "BGR_histogram_bhattacharyya", "threshold": self.cut_threshold}, "sessions": sessions, "average_consecutive_mask_iou": float(np.mean(ious)) if ious else None, "runtime_identity": self.runtime_identity, "ffmpeg_stderr": completed.stderr[-4000:]}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return {"status": "TESTED_PASS", "tracking_mode": "continuous_video_memory_per_scene", "sampled_frames": len(rows), "tracked_frames": len(rows), "fps": fps, "elapsed_ms": (time.perf_counter() - started) * 1000, "task_quality": "NOT_BENCHMARKED", "sessions": sessions, "average_consecutive_mask_iou": float(np.mean(ious)) if ious else None, "runtime_identity": self.runtime_identity, "outputs": [{"path": str(output), "sha256": sha256_file(output), "bytes": output.stat().st_size}, {"path": str(manifest), "sha256": sha256_file(manifest), "bytes": manifest.stat().st_size}, {"path": str(log_path), "sha256": sha256_file(log_path), "bytes": log_path.stat().st_size}]}

    def close(self):
        self.model = None
