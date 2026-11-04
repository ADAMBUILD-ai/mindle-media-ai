# MINDLE MEDIA AI 건축 영상 생산 파이프라인 2차 결과

- 기준일: 2026-10-24
- 원격 선행 커밋: `dee6eec6839585bc4746ada3c7969294c08ea872`
- 판정: **PARTIAL — 생산 계획·차단 Gate·FFmpeg MP4 실실행 PASS / Blender·Wan Runtime 미실행**
- Build Gate: `false` 유지
- PR #23: `HOLD / DO NOT MERGE` 유지

## 구현 범위

1. 건축 영상 생산 계획은 프로젝트 ID, 출력 비율, 1~12개 순차 장면,
   최종 MP4 경로를 고정한다.
2. 각 장면은 `existing_clip`, `blender`, `wan22` 중 하나의 엔진, 원본 경로,
   원본 SHA-256, 0.25~30초 길이와 필요한 카메라 또는 prompt를 기록한다.
3. 원본이 바뀌거나 출력이 작업 root 밖으로 나가면 `BLOCKED_INPUT`이다.
4. Blender/ComfyUI/Wan의 registry 항목이 비활성 상태이면 `BLOCKED_ASSET`이다.
   설치되지 않은 엔진을 FFmpeg 성공으로 대체하지 않는다.
5. FFmpeg delivery adapter는 FFmpeg·FFprobe 실행 파일 SHA-256과 작업 root를
   다시 확인하고 shell 없이 고정 인자로 H.264/yuv420p/AAC/faststart MP4를 만든다.
6. 변환 전후 원본 SHA-256을 비교해 실행 중 입력 변경을 탐지한다.

## 실제 실행 증거

현재 Linux 환경의 FFmpeg로 320×180, 24fps 영상과 440Hz 음원을 1초 동안
실제로 생성한 뒤 MEDIA delivery adapter를 통과시켰다.

| 검사항목 | 실제 결과 |
|---|---|
| FFmpeg 실행 | PASS |
| 영상 | H.264 / yuv420p |
| 오디오 | AAC / 48kHz / stereo |
| 길이 | 1.000초 |
| faststart | PASS, `moov` offset 36 / `mdat` offset 2085 |
| 출력 크기 | 83,531 bytes |
| 출력 SHA-256 | `147e7bfd43b13f807553c8575ea97a198cb6d045bd34c4cde42fec6cfcd9db0c` |
| 모델 추론 | 실행하지 않음 |
| 사람 청취 | 실행하지 않음 |

## 자산 SHA-256

- `architectural_video_pipeline.py`: `bb8a799b73d30768577d81f34e7741b1907a4b4a32fb4c6eca53be748831a141`
- `test_architectural_video_pipeline.py`: `de8afcdaa9573eba8e6ab8923d35d6ad785d270704d3233ca807c4cc522ca37e`
- `smoke_external_media_delivery.py`: `5c6e458e959ab7da05ca06a285d026c9f347b09430db0c46cfc45ab1be2191da`
- `FFMPEG_DELIVERY_RECEIPT.json`: `5eda20c3b3e1bcd747676330de0eaba6adbea52c7b9c4ddc975850b1398f4cd1`
- `FFPROBE.json`: `6c24cc30f6dc0eeb1bfd3ff4739bd846c36d1d07c5af004bfd0868bc3bdc4b7a`
- `SMOKE_DELIVERY.mp4`: `147e7bfd43b13f807553c8575ea97a198cb6d045bd34c4cde42fec6cfcd9db0c`

## 회귀 검증

- 전체 Python: `213 passed, 6 skipped`
- Node: `1 passed`
- 신규 생산 파이프라인: `3 passed`
- Python compile 및 `git diff --check`: PASS

## 판정 제한

이번 PASS는 실제 FFmpeg 영상·오디오 인코딩과 기술 규격에 한정한다. 실제
건축 이미지, Blender 렌더, Wan 생성, 자연어 장면 기획, 나레이션·BGM·자막
혼합, Windows 플레이어 청취 또는 사용자 품질 승인을 의미하지 않는다.

다음 단계는 대상 PC의 정확한 실행 파일을 registry에 물질화하고 Blender
고정 카메라 1장면을 먼저 렌더하는 것이다. 그 다음 격리 ComfyUI와 공식 Wan
API workflow를 고정해 동일 계획의 Wan 장면 하나를 생성하고, 두 장면을 기존
MEDIA Save/Reopen/Export 흐름에 넣는다.
