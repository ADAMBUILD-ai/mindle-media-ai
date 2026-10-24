# MINDLE MEDIA AI 다중 건축 장면 조립·영속 상태 3차 결과

- 기준일: 2026-10-24
- 원격 선행 커밋: `4d143bff378bab40746ca5251532c9978e37629c`
- 판정: **PARTIAL — 기존 영상 다중 장면 조립·상태 영속·중단 복구 PASS / Blender·Wan 장면 실생성 미실행**
- Build Gate: `false` 유지
- PR #23: `HOLD / DO NOT MERGE` 유지

## 구현 결과

1. 최대 12개의 기존 영상 장면을 계획 순서로 실제 결합한다.
2. 장면마다 원본 SHA-256을 실행 직전과 종료 뒤 확인한다.
3. 서로 다른 원본 비율을 지정 출력 크기에 비율 유지·중앙 padding으로 맞춘다.
4. 각 장면은 24fps로 정규화하며 계획 길이만큼 자르거나 마지막 프레임을 연장한다.
5. 원본 오디오가 있는 장면은 48kHz stereo로 정규화한다.
6. 오디오가 없는 장면에는 같은 길이의 silence를 공급해 영상·음성 concat 순서를 유지한다.
7. 최종 출력은 H.264/yuv420p/AAC/faststart이며 계획 길이 합과 실제 길이를 대조한다.
8. 출력 경로가 원본과 같거나 소유 작업 root 밖이면 실행하지 않는다.

## 영속 작업 상태

- 요청키와 전체 계획 fingerprint를 SQLite에 영속 저장한다.
- 동일 요청 재전송은 같은 production ID를 반환한다.
- 같은 요청키에 다른 계획을 보내면 거절한다.
- `QUEUED → RUNNING → SUCCEEDED`와 취소·차단·실패·중단 상태를 구분한다.
- 서버가 재시작되면 `RUNNING` 또는 `CANCEL_REQUESTED`를 `INTERRUPTED`로 복구한다.
- 중단된 작업을 성공으로 승격하지 않는다.
- `RUNNING` 상태에서만 완료할 수 있고 결과 MP4 경로·크기·SHA-256이 영수증과 모두 같아야 한다.

## 실제 다중 장면 실행

두 장면을 실제 생성해 결합했다.

| 순서 | 입력 | 비율 | 오디오 | 계획 길이 |
|---:|---|---|---|---:|
| 1 | 파란색 도착 장면 | 16:9 | 330Hz 음원 있음 | 0.5초 |
| 2 | 빨간색 빌라 장면 | 9:16 | 없음, silence 생성 | 0.5초 |

실제 결과:

- 장면 순서: `arrival → villa`
- 최종 비율: 16:9, 320×180
- 길이: 1.000초
- 영상: H.264/yuv420p
- 오디오: AAC/48kHz/stereo
- faststart: PASS
- 상태: `QUEUED → RUNNING → SUCCEEDED`
- MP4 크기: 15,606 bytes
- MP4 SHA-256: `835f5190912bc1c03a558486a898a555120f79276c97adcd1a6a8a693d2e8894`
- 250ms 프레임 평균 BGR: `[254.0, 0.0, 0.0]`, 첫 파란 장면 확인
- 750ms 프레임 평균 BGR: `[0.0125, 0.0, 79.06875]`, 두 번째 빨간 장면 확인

## 회귀와 자산 해시

- 전체 Python: `216 passed, 6 skipped`
- Node: `1 passed`
- 신규 건축 파이프라인: `6 passed`
- Python compile 및 `git diff --check`: PASS
- `architectural_video_pipeline.py`: `c8d061871ea3f32b58a4ae40facad13b525201140269b8d2d9ace102efb9247d`
- `test_architectural_video_pipeline.py`: `4b22030c41c46c010049108916bc7e5943386ec83235d0bab39e6a64a8dd2c5f`
- `smoke_architecture_scene_assembly.py`: `6eefcf028591e002391f5d5a13a2fa11d461a3258b23f2410c8a3bb27ecf58eb`
- `SCENE_ASSEMBLY_RECEIPT.json`: `c1e7b2cbfc764e921858640e9df7a3ec02707c2a9f226d83d90390dcc47ea948`
- `FFPROBE.json`: `ee516449d617f9c34c4d34bfa6a2cea101220d113b7e88bfa5bb4cd0321f1953`

## 판정 제한

이번 증거는 MEDIA 소유 FFmpeg 조립 코어와 영속 상태 계약의 실제 실행이다.
건축 원본 품질, Blender 렌더, Wan 모델 추론, 한국어 나레이션 청취, 실제 UI
Preview, Save/Reopen 또는 Windows EXE 인수를 의미하지 않는다.

다음 개발 단계는 이 영속 계획에 Blender driver와 격리 ComfyUI prompt ID를
각각 작업 단계로 연결하고, 생성 완료 파일을 같은 원본 해시·장면 순서 계약으로
FFmpeg 조립에 넘기는 것이다. 외부 엔진이 준비되기 전에는 계속 `BLOCKED_ASSET`이다.
