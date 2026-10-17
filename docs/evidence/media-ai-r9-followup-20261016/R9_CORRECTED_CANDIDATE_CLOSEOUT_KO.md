# R9 수정 후보 Windows 실기동·전달 파일 마감
기준일: 2026-10-16 KST

## 결과
개발 검수용 수정 후보 빌드·원격 Windows 실기동·독립 전달 ZIP 검증을 완료했다.
판정: PASS_R9_CORRECTED_WINDOWS_CANDIDATE_REPAIRS_LOCAL_ACCEPTANCE_PENDING.
실제 사용 PC/Windows 플레이어/승인 화면 원본 대조는 별도 잔여 항목이다. 전체 제품 PASS는 발급하지 않았다.

## 후보 identity
{
  "source": "fef692312ae8d8e3070c97e013dacdd31a043172",
  "producer_run": 38822776656,
  "readback_run": 38824641294,
  "readback_artifact": 12014421906,
  "zip": "MINDLE_MEDIA_AI_ONE_CLICK_WIN_X64_v1.0.zip",
  "zip_bytes": 1913892012,
  "parts": 5,
  "zip_sha256": "79b8fc38a5dade14a5974b132f265ba52476058f574b9d6c1795aa000aed7fe6",
  "payload_manifest_sha256": "3facd08b16aeae044af39755c2d0d9638af4fe3fa0fec317b2dbc0bd863f2c17",
  "launcher_sha256": "dd3f485a13a869acac87c3094381c9b97f872e461044af685e768afe9cadbe5a",
  "runtime_id": "fef692312ae8-1261762e58ca",
  "ui_fingerprint": "1261762e58cacdc2fee1c7a01819b91551fe258c1abaffe6d0978b9e8490467e",
  "manifest_files_verified": 19236
}

Producer: https://github.com/ADAMBUILD-ai/mindle-media-ai/actions/runs/38822776656
Readback: https://github.com/ADAMBUILD-ai/mindle-media-ai/actions/runs/38824641294

## 반영된 수정
cloud 전용 안내/로컬 storage 분리, PHOTO 직접 이미지 contain/center,
런처 lock 획득 실패·준비 실패·unlock 실패의 핸들 정리,
Export 임시 ZIP/CRC/원자 교체, 기록된 입력·참조의 bundle/hash 보존,
relative/Windows 8.3 경로의 canonical root 처리가 실제 payload에 포함됐다.
수정 소스 6개와 승인 CSS를 독립적으로 추출·대조했다.
Windows checkout의 CRLF/LF 차이는 원본 내용과 별도로 기록했다.

## 실제 검수
- Windows pytest 116 PASS / 1 SKIP. SKIP은 /usr/share/fonts CJK fixture를 찾는 Linux 경로 기반 검사다.
- Node UI 5 PASS: cloud 3, interaction/SSOT 2.
- 패키지 내부 Python import: torch2.8.0+cpu, transformers4.57.3, OpenCV4.12.0, OpenVINO2025.3.0.
- 실제 EXE materialize·첫 실행·두 번째 실행 PASS. 서버 PID5220을 재사용하고 중복 서버0.
- 공식 Chrome155.0.8059.40 영상 실제 재생: MediaError=null, readyState4, videoWidth320, currentTime0→1.54611.
- PHOTO 보정 적용/영상 편집 PASS. 세로90×160: stage408×229.5/image406×227.5, contain, 50% 50%, 잘림 없음.
- 대상 패키지 서버 PID5220 종료·프로세스 소멸·endpoint 미응답 후 EXE 재실행→PID1780.
- project_id 9200506f-96a8-482a-8612-1cf0b60a4fdb의 사진/영상/보정3작업 복원·Export PASS.
- 해당 Export ZIP SHA 751a30205435d17efa44892363c5760a3161384d4edc63218d1107a384d41042: 독립 CRC 및 입력/출력8파일 해시/크기 PASS.
- 실제 생성된 편집 MP4: H.264/yuv420p/AAC, moov<mdat faststart PASS.
- 전달 ZIP 전체 SHA/CRC와 manifest19236파일 SHA/크기 PASS. manifest 밖의 생성 __pycache__/*.pyc1099개는 별도 해시 기록했다. 다른 미기록 소스/실행 바이너리는 허용하지 않았다.
- PHOTO 분할/4× 및 기존 모델 추론을 재실행하지 않았다. 고정 검증 payload를 재사용했고 신규 추론 PASS로 표시하지 않았다.

## 보존 및 실패 이력
첫 run38821443702는 제품 실행/브라우저/cold restart를 통과했지만, 잠금 테스트의 source.read_text()가 Windows cp1252를 사용해 6FAIL/110PASS/1SKIP였다.
UTF-8 명시와 회귀검증 선행으로 수정한 최종 producer가116PASS/1SKIP를 통과했다. 첫 증거 artifact12014036542는 보존했다.
첫 독립 readback38824390609는 재현용 CSS 복사본의 추가 마지막 줄바꿈1개를 기준으로 삼아 실패했다.
저장소 원본 blob3e1334c14b84fcbd5845a7a7a693c3f6bfe5a5da로 기준을 바로잡고 38824641294에서 PASS했다. 후보 ZIP 재빌드는 하지 않았다.
과거 재현용 복사본 SHA712cfaa…는 Git 원본 바이트 hash가 아니다. 원본 LF 내용 SHA는 2e6c7f992c8ab412e0d70af433fa2cc1e3e625304cf4051ba37de4d7814e7757, Windows 배포 파일 SHA는 23695715beb425b35580f2c56dc7e657e3a3538d714a8183f532f77a56b1ebc0다.
승인 CSS Git blob은 기준 HEAD8552793과 동일하다. 승인 원본 이미지와의 전체 화면 일치를 의미하지 않는다.
모든 역사 증거와 구 후보는 보존했다.

## 남은 항목
| 항목 | 판정 |
|---|---|
| 수정 반영 검수용 후보 빌드/원격 EXE/브라우저/전달 ZIP | PASS |
| R9 원본 report/CSV/승인 비교PNG/ZIP의 원본 바이트와 해시 | BLOCKED: 실제 사용 PC 자료 미확보 |
| 승인 화면 원본을 사용한 전체 UI 대조 | BLOCKED: 원본/동일 viewport 검수 필요 |
| 실제 R9 lock 예외와 수정의 인과 일치 | BLOCKED: 예외 전문·로그 미확보 |
| 실제 사용 PC EXE/서버 완전 종료·재실행·동일 프로젝트·자료 항목별 복원/Export | BLOCKED: 해당 PC 접근 필요 |
| 설치 Windows 플레이어 재생/탐색/실제 소리 청취 | BLOCKED: 해당 PC 실검수 필요 |
| Marketing HTTP/승인 AVORA | DEFERRED |
| OpenAI 연결 | NOT_APPROVED_NOT_CONNECTED |

브라우저 재생을 Windows 플레이어/청취 PASS로 확대하지 않는다.
사진/영상/보정3작업의 cold restart를 자막/참조까지 전체 복원한 것으로 확대하지 않는다.
R9 사용자 보고와 이번 원격 runner 증거는 서로 다른 출처다.

## 다음 작업
PC Work는 docs/commander/MINDLE_MEDIA_AI_PC_R9_CORRECTED_CANDIDATE_ACCEPTANCE_20261016.md에 따라 남은 항목만 수행한다.
입력8/버튼60 준비·백업·PHOTO 모델 검수를 반복하지 않는다.
build gate=false로 닫았다. 직원 최종 패키지는 발행하지 않았다.
PR23 HOLD / DO NOT MERGE, main 병합/force push 금지, 확정 UI 임의 재설계 금지를 유지한다.
owner_pc_runtime_pass=false; final_product_pass=false.
