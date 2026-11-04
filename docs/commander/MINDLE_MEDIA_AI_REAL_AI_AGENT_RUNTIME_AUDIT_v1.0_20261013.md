# MINDLE MEDIA AI — 실제 AI 에이전트 작동 감사

기준: 2026-10-13, 원격 HEAD `733e1bf1a47236d9b83000974cf4d10845e0264f`.

판정: **REWORK_AGENT_RUNTIME_CONTROL_AND_SEMANTIC_BINDING_REQUIRED**.

실제 모델 추론은 존재합니다. 그러나 현재 제품은 **고정된 UI 명령 규칙·로컬 영상/픽셀 분석·3종 모델 실행기**를 조합합니다. 자연어 의미를 이해해 작업을 계획·분담·판단·재시도하는 생성형 AI 에이전트는 활성 제품 경로에 연결돼 있지 않습니다. 기존 `TESTED_PASS`를 전체 에이전트·편집 품질 PASS로 해석할 수 없습니다.

## 실제로 호출되는 AI

| 기능 | 실제 실행기 | 확인한 실행 증거 | 범위·한계 |
|---|---|---|---|
| PHOTO 분할/배경 제거 | SAM 2.1, PyTorch CPU | 기존 Windows Job `54338f7e-14ad-4673-a792-a6533d8a3a6f`, mask·overlay 해시, 실제 추론 4584.36ms | 언어가 대상을 찾는 모델이 아니라 좌표를 입력받는 분할 모델. 배경 제거는 이 mask로 RGBA를 만드는 별도 픽셀 처리 |
| PHOTO 4× | Intel SISR 1032, OpenVINO CPU | Job `217c102e-8e84-4465-bdd1-9539113f1366`, 실제 추론 약1391ms, 4× 출력 해시 | 함수 이름 `realesrgan()`과 달리 실제 adopted 모델은 Intel. 원본/출력 크기·해시 검증은 있으나 사람이 보는 품질까지 입증하지 않음 |
| VIDEO 추적 | SAM 2.1 이미지 분할기 | Job `448ea83d-6254-49e0-8a58-e0c0d20a5d67`, source frames **0/41/83/124**, 4개 실제 mask 결과 | 전체 프레임 temporal tracking이 아님. 이전 mask 중심을 다음 표본의 점으로 넣는 방식. 출력은 4개 overlay 프레임을 2fps로 인코딩 |
| 한국어 STT | Whisper-small, PyTorch CPU | Job `89c8a299-9d8f-45d6-899a-8877f378f416`, 12.48초 입력, 실제 추론4167.82ms, 한국어 문장·출력 해시 | `reference=null`, `word_error_rate=null`. 한글 포함·비어 있지 않음 PASS이며 실제 받아쓰기 정확도 PASS는 아님 |

위 네 Job은 **Windows runner 실행 38121146106 / 소스 8b28e712bf8e77052ca7efcc3459f7779597dc5a**의 과거 증거입니다. 아티팩트 11695148490을 내려받아 CRC·SHA-256를 확인했습니다. immutable revision·가중치 bytes/hash·adapter·입출력·elapsed·상태 기록을 `MODEL_EXECUTION_MATRIX.json`에 보존했습니다. 현재 사무실 PC에서 모델 파일을 찾고 실행했다는 증거가 아닙니다. PHOTO 기존 PASS를 재작업하거나 모델 추론을 재실행하지 않았습니다.

## AI로 보이지만 모델 에이전트가 아닌 처리

- VIDEO 자동 편집: 최근 수정된 OpenCV 장면 측정 + FFmpeg 편집. 생성형 판단 아님.
- PHOTO 자동 보정: 실제 픽셀 분포 분석 + canvas/Pillow. 생성형 판단 아님.
- AI 효과/스타일: FFmpeg vignette·픽셀 색상 변환. 생성 모델 아님.
- AI 대화 편집: 브라우저 정규식이 동작을 고름. `planner.py`도 고정 옵션을 Step 목록으로 바꾸는 함수이며 현재 browser → ProductJobService 경로에서 호출되지 않음.
- 유사 이미지: 첨부 이미지 RGB histogram 순위. 외부 웹 검색·embedding 검색 아님.
- Marketing: HTTP 연결 코드가 있지만 packaged/deferred 모드는503. 실제 마케팅 에이전트가 현재 호출됐다는 증거 없음. AVORA 연동도 DEFERRED_EXTERNAL.
- OpenAI `whisper-small`이라는 모델명이 OpenAI API 연결을 뜻하지 않음. 로컬 가중치를 실행하며 OpenAI API 호출은0회.

## 실제 실행 순서의 결함

현재 `ProductJobService.execute`는 입력 저장 → vault/adapter 준비 → **실제 모델 추론** → handoff/registry/intake → readiness → preflight → dispatch → running → 출력 검증 → 로컬 callback 수락 순서입니다. 게이트가 추론 전에 실행을 승인하는 구조가 아닙니다.

안전한 주입 adapter로 코드 순서만 재현했습니다. callback/handoff를 거부해도 먼저 adapter 호출이 발생했습니다. 실패 record는 `status=FAILED`, `state=queued`였습니다. 이 검사는 모델 추론 증거가 아니며 새 실제 모델 호출은0회입니다. 재현 스크립트와 결과를 함께 보존합니다.

과거 STT는 실제 추론4167.82ms인데 orchestration `started_at`과 `finished_at`은 같습니다. SAM 분할4584.36ms도 두 시간이 같습니다. 모델 자체 elapsed는 존재하지만, Job lifecycle timestamp는 모델 실행 시간을 포괄하지 못합니다. 실제 실행 상태 감시·실패/재시도 판단에 이 lifecycle 기록을 그대로 사용할 수 없습니다.

`execute_isolated`는 별도 CPU subprocess로 모델을 실행하고, 성공 결과만 parent에 반환합니다. 제품 HTTP는 동기 요청과 mutation lock을 쓰며, 별도의 활성 다중 에이전트 task queue·실시간 Job polling API에 연결돼 있지 않습니다. 실패 worker의 Job identity·state가 부모의 `/api/evidence`에 제대로 연결되지 않을 수 있습니다.

## 대상·참고자료·품질의 결함

1. **오른쪽 인물 오선택**: `_photo_target_point`는 “왼쪽 또는 인물”을 먼저 확인합니다. 100×60 사진에 “오른쪽 인물을 분리해줘”를 넣으면 오른쪽74가 아니라 **왼쪽26**이 나옵니다. 고정 좌표 규칙이고 인물 의미 탐지가 아닙니다.
2. **참고 이미지 미전달**: UI 첨부 references는 model Job body로 전달되지 않습니다. `file.datasetReference` 조건은 있으나 실제 할당 경로가 없고, ProductJobService의 MediaJob 생성도 reference_files를 넣지 않습니다. 참고 이미지를 이해해 편집했다는 주장은 불가합니다.
3. **추적 품질 미검증**: 실제 tracking receipt의 두 인접 표본 IoU는 약 **0.0233 / 0.0247**입니다. 이동·장면 변화로 낮을 수 있으므로 이 숫자만으로 실패를 확정하지 않습니다. 다만 연속 동일 객체 유지·전체 프레임 coverage를 통과시킨 별도 기준이 없어 production tracking PASS도 불가합니다.
4. **품질 게이트의 한계**: PIL/OpenCV parseability·비어 있지 않음·hash·4× 크기·mask가 전체흰색/검정이 아님을 주로 검증합니다. 의도한 대상·자연어 충실도·영상 의미·STT 정답률 검증과는 다릅니다.
5. **내부 callback**: Model Scout callback은 같은 ProductJobService 함수가 만들어 같은 함수에서 수락합니다. 실제 외부 에이전트 송수신을 증명하지 않습니다. `_handoff`의 issue_id도 PR-10으로 고정돼 있어 현재PR23 원요청과의 추적성을 바로잡아야 합니다.

## 필요한 수정 순서

**P0**: 입력/모델/registry 검증을 추론 앞으로 이동 → 실제 RUNNING 시작 → 실제 종료/실패 기록 → 부모 worker 결과·Job identity 연결 → 실패 재시도 가능성 검증. 기존 immutable 모델과 승인 UI는 보존합니다.

**P1**: 명시적 오른쪽/왼쪽 처리 오류 수정 → 실제 참고자료 전달·해시 결합 → 실행 성공과 업무 품질 PASS 분리 → 영상 전체 구간의 실제 tracking 경로/검수 기준 → 생성형 계획·의미 분석 agent 연결. OpenAI 실연결은 대표가 정한 승인·키 Gate에서만 수행합니다.

**P2**: 내부 receipt와 외부 agent callback 구분 → 실제 원요청·프로젝트·PR lineage → task 상태 조회·중단·재시도·재시작 후 상태 회복 경로 검수.

현재 제품 전체/사무실 PC PASS는 **false**입니다. 이번 감사에서 제품 소스·UI·모델 adapter·기존 PASS 증거는 바꾸지 않았고, PR23 **HOLD / DO NOT MERGE**, main 병합 없음입니다.

검수자료: `docs/evidence/media-ai-agent-runtime-audit-20261013/`의 EVIDENCE, MODEL_EXECUTION_MATRIX, GAP_REGISTER, CONTROL_FLOW_PROBE, SOURCE_READBACK, REMOTE_READBACK.
