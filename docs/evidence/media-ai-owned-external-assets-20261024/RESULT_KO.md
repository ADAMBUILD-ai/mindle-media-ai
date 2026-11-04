# MINDLE MEDIA AI 외부 제작 엔진 자산화 1차 결과

- 기준일: 2026-10-24
- 기준 소스: `9f1a8686baf111b80c923250ca35b26b3100d32c`
- 판정: **PARTIAL — 소유 어댑터·정책·검증기 PASS, 외부 런타임/모델 실증 미실행**
- Build Gate: `false` 유지
- PR #23: `HOLD / DO NOT MERGE` 유지

## 이번에 제품 자산으로 만든 범위

1. Blender 고정 카메라 렌더 드라이버를 저장소 자산으로 추가했다.
   사용자 자연어를 Python이나 shell로 평가하지 않으며, 기존 `.blend`, 기존
   카메라명, 제한된 프레임·FPS·해상도만 구조화 JSON으로 전달한다. 결과
   프레임은 크기와 SHA-256을 영수증에 기록한다.
2. ComfyUI/Wan 어댑터 경계를 추가했다. 명시적 loopback 주소, 해시가 맞는
   API workflow, allowlist에 등록된 node/input만 허용한다. 공유 프로세스의
   전역 `/interrupt`는 차단하고 MEDIA가 격리 소유한 프로세스와 prompt만
   취소할 수 있다. 출력 경로 이탈도 거부한다.
3. Blender, FFmpeg, ComfyUI, Wan 2.2 TI2V-5B, LTX Desktop의 상태·출처·
   revision gate·라이선스·활성 여부를 단일 registry로 고정했다.
4. 대상 PC에서 같은 검사를 반복할 수 있는 read-only validator를 추가했다.
   프로그램 존재 확인은 Runtime E2E 성공으로 확대하지 않는다.

## 판정표

| 자산 | 현재 판정 | 활성 | 다음 실증 |
|---|---|---:|---|
| MEDIA Blender driver | SOURCE 계약·SHA 검증 PASS | 아니오 | Windows Blender에서 승인 `.blend` 카메라 렌더 |
| Blender runtime | 물질화 전 | 아니오 | 버전·설치 경로·EXE SHA·GPU 렌더 |
| FFmpeg | 기존 제품 Runtime 경로 유지, 이번 Linux identity probe PASS | 예 | 후속 Windows 후보의 정확한 바이너리/빌드 설정 재기록 |
| ComfyUI | API 안전 경계 단위검증 PASS, 설치 미실행 | 아니오 | 격리 프로세스·공식 API workflow 실기동 |
| Wan 2.2 TI2V-5B | 출처·라이선스 후보 등록, weight 없음 | 아니오 | 12 GB GPU에서 짧은 I2V/T2V와 VRAM·시간·품질 측정 |
| LTX Desktop | 하드웨어 보류 | 아니오 | 24 GB 이상 권장 GPU 환경이 확보된 뒤 재평가 |

## 검증 결과

- 신규 경계 테스트: `7 passed`
- 전체 Python 회귀: `210 passed, 6 skipped`
- Node 회귀: `1 passed`
- `git diff --check`: PASS
- Python bytecode compile: PASS
- 현재 환경 FFmpeg: exit 0, `6.1.1-3ubuntu5`, executable SHA-256
  `ed16af623947494a72e284b6eb8ff225f2da22b38b5d5069c2fd4b4ba3384e41`

주요 저장소 자산 SHA-256:

- `ASSET_REGISTRY.json`: `5b9bf0efb3eb9e6ddab3cab61edb814713de0007eb61c7fe0a63b9d27f4e092c`
- Blender driver: `f4df254e3f054c650b1ea12f849183d7ca4c048f350432f79bbbf9608472c5b3`
- `external_media_assets.py`: `b00d85f404b8b35b1c6f0eda134381d36ee12eda0d8d8e9ff0c66614428b3191`
- validator: `b28fba1cbb6cea9e4a5ea0363dc5f57d6e919bc9f8dce05baa51b2febb75f05c`

## 외부 사실 확인과 적용 제한

- Blender 공식 문서는 background mode에서 `--python` 스크립트 실행을
  지원한다. 제품은 이 기능을 임의 스크립트 실행이 아니라 소유 driver로
  제한했다: <https://docs.blender.org/api/current/info_tips_and_tricks.html>
- Wan 2.2 공식 저장소는 TI2V-5B의 720p/24fps와 Apache-2.0 공개를 설명한다.
  이 설명은 RTX 3060 12 GB에서의 제품 실증을 대체하지 않는다:
  <https://github.com/Wan-Video/Wan2.2>
- LTX Desktop 공식 문서는 Windows local generation에 24 GB 이상 VRAM을
  권장한다. 보고된 12 GB GPU에서는 이번 단계에서 보류했다:
  <https://github.com/Lightricks/LTX-Desktop>
- FFmpeg 재배포 라이선스는 실제 Windows 패키지의 build configuration에
  따라 다시 고정한다: <https://ffmpeg.org/legal.html>

## 미완료와 다음 실행 순서

1. 실제 사무실 PC의 GPU driver, VRAM, RAM, 여유 디스크를 read-only로 다시 측정한다.
2. Blender의 승인 버전·정확한 EXE SHA를 고정하고 기존 건축 `.blend` 한 건을 렌더한다.
3. ComfyUI를 전용 loopback port로 격리 실행하고 공식 Wan API workflow를 export해 SHA를 고정한다.
4. 모델 weight revision·파일 SHA·라이선스를 고정한 뒤 2~4초 저해상도 smoke를 먼저 실행한다.
5. 통과한 출력만 FFmpeg의 H.264/yuv420p/faststart 합성으로 연결하고 Save/Reopen/Export를 검증한다.

이번 변경은 외부 엔진을 안전하게 소유 자산으로 받아들이는 실행 경계다.
Blender·ComfyUI·Wan 실제 실행, 생성 영상 품질, Windows 패키지 포함 여부는
아직 PASS가 아니며 UI에 성공 기능으로 노출하지 않는다.
