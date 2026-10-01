# MINDLE MEDIA AI

## Two Track Work Package

The non-destructive Work Track A handoff is in `docs/00_README_FIRST.md` through `docs/09_PC_REMOTE_FINAL_CHECKLIST.md`. The approved visual UI is intentionally not redrawn in this repository because its source and approved screenshot are absent; only the state contract is implemented in `src/media_ai/ui_contract.py`.

Model Scout를 제외한 P0 실행 코어입니다. 자연어 요청을 PHOTO 또는 VIDEO로 라우팅하고, 비동기 Job으로 처리하며, 원본과 결과 및 실행 로그를 분리 보관합니다.

## 실행

```bash
python -m pytest
python -m media_ai.cli photo --input sample.jpg --output out.jpg --brightness 1.05
```

VIDEO 명령은 시스템의 `ffmpeg`를 사용하여 지정 구간 자르기와 16:9, 9:16, 1:1 리프레임의 첫 E2E를 제공합니다.
