# MINDLE MEDIA AI 마무리 재점검·수정 결과

2026-10-17 KST. 기준 HEAD `0d6c2a664296050ff35294e5d0cf70cd7c948177`.
새 수정 `84cf58014eafa2aabd5eed763881424ab3a70c1f`.

판정: **소스 결함 수정·인계 기준 정리 완료, 새 수정의 실제 브라우저/후보 검증 및 실제 PC 인수는 미완료**.
준비만 하고 종료하지 않았다. 이번에 production JS를 실행해 두 경합을 재현하고 코드를 수정했으며, 실제 실패→통과 회귀 로그를 보존했다.

## 1. 기존 완료 결과는 보존했다

- c37 후속 Windows 후보 제작, 독립 ZIP CRC·19,236 manifest 파일 및 핵심 source readback PASS.
- 실행 38851276116의 실제 EXE: PID3624 종료/기존 endpoint 미응답→EXE 재실행 PID1488→같은 프로젝트→참고2개·입력음성의 이름/크기/SHA 복원 PASS.
- UI Export 3,737 bytes, 6개 manifest 파일 CRC/크기/SHA 확인 PASS.
- 기존 PHOTO 분할·Intel4×, SAM video memory tracking, Whisper-small 추론·자막 및 보정/편집 증거는 10월14일 복구 보고와 연결했다. 새 모델 추론은0회다.
- 사무실 PC/설치 플레이어 PASS로 확대하지 않았다. 백업·입력8·버튼60 준비나 완료 고비용 모델 작업을 반복하지 않았다.

## 2. 새로 확인하고 고친 제품 결함

`ui/product_integration.js`에는 편집을 저장하는 guard는 있었지만 프로젝트 New/Open에는 같은 guard가 없었다.
편집이 진행 중이어도 New가 현재 File/job/project 상태를 지웠다.
또한 Save 응답 대기 중 New를 실행하면 이전 Save 응답이 새 작업 상태에 과거 project ID를 다시 넣을 수 있었다.
이 상태에서 다음 Save가 과거 프로젝트를 대상으로 실행될 수 있다.

수정은 편집·Save·Reopen·Export 동안 프로젝트 전환을 거절하고, 작업이 끝나면 guard를 해제하는 범위다.
거절된 중복 Save/Export는 다른 작업의 guard를 풀지 않는다.
프로젝트 열기 실패/거절 때 shell dialog를 닫지 않도록 반환값도 연결했다.
레이아웃·색상·새 버튼·모델·backend 알고리즘은 바꾸지 않았다.

실제 production controller를 Node VM에서 실행한 원본2사례는 **2 FAIL**로 재현됐다.
수정 후 전환/중복/복원/Export 경합 **5 PASS**, 전체 Node **10 PASS**.
영향 Python **30 PASS / 1 SKIP**. SKIP은 실제 Windows 잠금 전용 항목이다.
문법 및 PC/General Control Plane validator도 PASS다.
DOM/network 경계는 fixture다. 이 검사를 실제 브라우저 화면·모델·Windows 동작 PASS로 부풀리지 않는다.

신규 소스의 실제 브라우저 검증을 위해 Chromium 확보를 시도했으나 다운로드가 완전한 ZIP이 아니어서 중단했다.
브라우저 검증·화면 캡처는 수행하지 않았다. 이 다운로드 실패를 제품 오류나 사무실 PC 도우미 장애로 판정하지 않는다.
현재 c37 후보에는 새 전환 수정이 없다. payload를 덮어쓰거나 추가 빌드를 하지 않았다.

## 3. 앞선 UI 판정은 최신 Owner 기준으로 바로잡았다

F27E PNG 자체가 상하 배치이고 실제 후보가 좌우 배치라는 비교 사실은 맞다.
그러나 10월10일 Owner가 VIDEO 좌측·PHOTO 우측 가로2분할을 최종 기준으로 지정한 직접 기록이 있다.
10월7일 구현 보고도 좌우 구조 보존을 기록했다.
따라서 F27E와 다르다는 사실만으로 최신 승인 위반 FAIL을 유지하거나 상하로 복원하면 안 된다.

`docs/01_UI_SSOT_FINAL.md`, 현 인계 문서·계약·상태에 이 우선순위를 명시했다.
역사 원본·비교 JSON·과거 보고는 삭제하지 않았다.
HTML/CSS·PHOTO/VIDEO workspace·모델 adapter의 원격 원본과 현재 해시가 같음을 확인했다.
현재 좌우 배치 지시와 일치한다는 판정과 정확한 최종 화면 승인/모든 viewport PASS는 분리했다.

## 4. AI 에이전트와 엔진의 정확한 완료 범위

실제 채택 엔진은 SAM2.1/PyTorch, Intel SISR/OpenVINO, Whisper-small 로컬 실행기다.
10월13일 감사의 실행 순서·참고 전달·전체프레임 추적·실패 상태 문제는 10월14일 수정/실행 증거와 대조했다.
과거 지적을 그대로 현재 FAIL로 반복하지 않는다.
OpenCV/FFmpeg/canvas 보정·고정 명령 분기 역시 실제 처리이지만 생성형 의미 계획과는 다르다.
생성형 planner, durable 다중 에이전트 queue·자동 재시도·취소는 미연결이다.
STT는 실제 한글 결과가 있어도 WER 정답률 미측정이다. 음성 입력/BGM/STT가 TTS 나레이션 생성 완료를 뜻하지 않는다.
OpenAI 키 연결 없이 이를 임의 provider나 새 모델로 활성화하지 않았다.
기능별 상태는 `FUNCTION_CLOSEOUT_MATRIX.json`에 기록했다.

## 5. 남은 실제 인수 항목

| 항목 | 상태 | 남은 실증 |
|---|---|---|
| 새 전환 수정 | PARTIAL | source 회귀 PASS; 실제 브라우저 및 후속 승인 후보에 반영·검증 |
| 사무실 PC cold restart | BLOCKED | 해당 PC의 EXE→서버 완전 종료→새 PID→자료 복원→Export |
| 설치 Windows 플레이어 | BLOCKED | 플레이어 이름/버전·재생·탐색·영상·실제 청취 |
| 정확한 최종 UI 화면 | PARTIAL | 최신 좌우 기준으로 실제 PC viewport/zoom·입력/우측 패널·미디어 fit 확인 |
| R9 원본·잠금 예외 | BLOCKED | 원본 TXT/CSV/PNG/ZIP·예외 전문·bootstrap/server log·크기/SHA/시각 |
| Marketing/AVORA | DEFERRED_EXTERNAL | 기존 보류 범위를 유지 |

현재 환경은 Linux이며 사무실 PC native 실행 표면이 연결되지 않았다.
R9 정확 파일명은 최신 저장소 tree와 Library에서 확보하지 못했다. 무관한 검색 결과는 증거로 쓰지 않았다.
이는 사무실 PC 자체/도우미 고장이나 원본 파일 전체 부재의 증명이 아니다.

실패 메일 제목만으로 후보 전체 FAIL을 판단하지 않았다.
최신 preflight 실패 38851275995는 제품이 아니라 예전 Control Plane의 unknown phase였고, 현재 동일 validator는 PASS다.
첫 추가 EXE 검수의 PID 식별 오류와 이후 실제 성공 실행도 구분해 보존했다.

## 6. 다음 작업을 끊지 않도록 정리했다

긴 실행 지시서: `docs/commander/MINDLE_MEDIA_AI_FINAL_CLOSEOUT_EXECUTION_20261017.md`.
순서는 A 신규 소스 브라우저/승인 후보 검증 → B 실제 PC 실기동 → C Windows 플레이어/청취 → D UI·R9 원본/로그 인수다.
각 묶음을 실제 결과까지 끝내고 실패한 독립 항목만 남긴다. 끝난 준비/모델 작업은 재시작하지 않는다.

Build Gate=false, PR23 HOLD/미병합, main 병합/force push 없음.
OpenAI 연결 없음. 직원 최종 패키지·추가 후보 제작 없음.
owner_pc_runtime_pass=false, final_product_pass=false. 전체 제품 최종 PASS 문자열을 발급하지 않는다.
