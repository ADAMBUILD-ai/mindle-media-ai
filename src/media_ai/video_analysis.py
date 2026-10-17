"""Measured scene selection, without a generative-AI or model-inference claim."""
from __future__ import annotations
import math
import cv2


def analyze_video(source, requested_seconds=30):
    requested_seconds = float(requested_seconds)
    if not math.isfinite(requested_seconds) or requested_seconds <= 0:
        raise ValueError('자동 편집 길이는 양수여야 합니다.')
    capture = cv2.VideoCapture(str(source))
    try:
        fps = capture.get(cv2.CAP_PROP_FPS)
        frames = capture.get(cv2.CAP_PROP_FRAME_COUNT)
        if not capture.isOpened() or not math.isfinite(fps) or fps <= 0 or frames <= 0:
            raise ValueError('자동 편집할 영상 프레임을 읽을 수 없습니다.')
        duration = frames / fps
        interval = max(1.0, duration / 300)
        samples, previous = [], None
        second = 0.0
        while second < duration:
            capture.set(cv2.CAP_PROP_POS_MSEC, second * 1000)
            ok, frame = capture.read()
            if ok:
                gray = cv2.cvtColor(cv2.resize(frame, (160, 90)), cv2.COLOR_BGR2GRAY)
                exposure = float(gray.mean())
                sharpness = float(cv2.Laplacian(gray, cv2.CV_64F).var())
                motion = float(cv2.absdiff(gray, previous).mean()) if previous is not None else 0.0
                # Near-black/white frames cannot dominate by a single flashing transition.
                usable = 12 <= exposure <= 243
                score = min(motion, 40) + min(sharpness / 50, 10) if usable else 0.0
                samples.append({'second': round(second, 3), 'motion': round(motion, 4),
                                'exposure': round(exposure, 4), 'sharpness': round(sharpness, 4),
                                'score': round(score, 4), 'usable': usable})
                previous = gray
            second += interval
        if not samples:
            raise ValueError('자동 편집 분석에 성공한 영상 프레임이 없습니다.')
        length = min(requested_seconds, duration)
        # Score the whole output window, rather than centering on one noisy peak.
        starts = sorted({0.0, max(0.0, duration-length)} | {max(0.0, min(duration-length, s['second']-length/2)) for s in samples})
        windows = []
        for start in starts:
            selected = [s for s in samples if start <= s['second'] < start+length]
            score = sum(s['score'] for s in selected)/len(selected) if selected else -1
            windows.append((score, -start, start))
        start = max(windows)[2]
        return {'method': 'measured_scene_window_v1', 'model_inference': False,
                'semantic_understanding': False, 'source_duration': duration,
                'requested_duration': requested_seconds, 'start': start, 'duration': length,
                'sample_count': len(samples), 'samples': samples,
                'reason': 'Motion, exposure and sharpness measured from decoded source frames; highest mean window score.'}
    finally:
        capture.release()
