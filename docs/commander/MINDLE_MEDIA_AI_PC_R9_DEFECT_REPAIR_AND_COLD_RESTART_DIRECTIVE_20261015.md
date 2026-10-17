# PC R9 결함 수정 및 실제 완전 재시작 검수

기준: 2026-10-15 KST. Epoch MEDIA-AI-20261013-OWNER-RUNTIME-RECOVERY-R1 유지.

## 접수 상태
사용자가 제공한 PC R9 보고: 재생/탐색/오디오 디코딩, 사진 7개 보정 픽셀 변화, 브라우저 종료 후 프로젝트 복원, ZIP 다운로드/CRC PASS. 버튼60은 역할 기준59 PASS/1 FAIL. 클라우드 버튼 오연결, 세로 PHOTO 잘림, 승인 화면 구조 차이, 런처 준비 잠금 예외. 서버 완전 종료/EXE 재실행 및 Windows 플레이어 미완료.

보고 링크는 PC 상대경로이며 General 환경에서 원본 파일을 읽지 못했다. 따라서 위 결과는 USER_REPORTED로 접수하고, 원본 독립 검증 완료로 표시하지 않는다. 검수기 exit0은 증거 완전성 검사이며 Runtime PASS가 아니다.

## General에서 이번에 확인·수정한 것
ui/index.html의 클라우드 버튼이 data-shell=storage로 지정돼 있었고 workspace_shell.js가 /api/projects와 data_root를 표시했다. cloud 전용 경로를 만들고 외부 클라우드 미연결 상태를 명확히 표시하도록 수정했다. 실제 외부 서비스 연결을 추가한 것은 아니다. 클라우드는 DEFERRED이며 제품 기능 PASS로 승격하지 않는다.

Node 실행 경로 회귀3개 PASS: cloud는 로컬 API 미호출, settings storage는 기존 로컬 API 유지, 승인 라벨 및 분리된 routing 유지. CSS/레이아웃/색상/모델 수정 없음. 기존 배포 후보에 이 소스 수정이 들어갔다고 주장하지 않는다.

## PC Work 즉시 후속 작업
1. R9 원본을 보존한다. RESUMED_RESULT_KO.txt, RESUMED_BUTTON_60.csv, SSOT_VS_ACTUAL_CHROME.png 및 증거 ZIP의 실제 bytes/SHA256을 기록한다. 기존 전달 위치로 General이 읽을 수 있게 인계한다. 화면 비교에는 승인 원본 파일명/hash와 실제 후보 source/runtime/UI fingerprint를 함께 남긴다.
2. 수정되지 않은 기존 후보에서 독립적으로 가능한 Windows 플레이어 검수를 진행한다. Export MP4를 실제 설치 플레이어로 열고 앱 이름/버전, 화면, 재생 진행, 탐색, 실제 소리 청취 여부를 기록한다. 브라우저 오디오 디코딩 성공을 소리 청취 PASS로 대체하지 않는다.
3. Save 응답과 project_id 및 저장 결과 hash를 기록한다. 제품의 정상 종료 경로를 우선 사용한다. 해당 제품 process identity/PID를 확인한 뒤 그 제품에 한해 종료한다. 다른 Python/Chrome 프로세스를 일괄 종료하지 않는다.
4. 해당 제품 서버 process 종료 및 기존 runtime endpoint 미응답을 모두 확인한다. 단순 브라우저 종료는 cold restart가 아니다. EXE 더블클릭 → 신규 서버 PID/identity → 동일 프로젝트 재열기 → 결과/자막/오디오/참조 복원 → Export를 기록한다.
5. 잠금 예외가 다시 나오면 반복 더블클릭을 중단하고 exception 전문/traceback, bootstrap.log, server.log, 관련 PID·명령행·시각 및 launch.lock의 경로/파일 상태를 확보한다. lock 파일 삭제, 모든 프로세스 kill, 잠금 검증 우회는 하지 않는다. 실제 오류와 실패 지점을 확인한 후 General에서 수정한다.
6. 세로 PHOTO 잘림: 원본 dimensions, Preview host bounding box, image bounding box/naturalWidth/naturalHeight, computed width/height/max-height/object-fit/object-position/overflow, 브라우저 viewport/DPR/zoom 및 적용된 CSS URL을 기록한다. 원본 이미지 네 모서리가 보이는 비교 화면을 포함한다. CSS 추정 수정이나 전체 레이아웃 재설계는 하지 않는다.
7. 승인 UI 구조 차이는 승인본/실제본을 동일 viewport/zoom으로 맞춰 비교한다. 각 차이를 요소 selector, 기대값, 실제값, 화면 좌표로 목록화한다. 승인 원본과 패키지 UI 파일 hash 불일치인지, viewport/캐시/스타일 cascade인지, 실제 구조 회귀인지 구분한다.
8. 가능한 항목은 계속 검수한다. 잠금으로 cold restart가 막히면 그 항목만 FAIL/BLOCKED로 남기고 Windows 플레이어와 원본 증거 인계를 완료한다.

## 후속 후보 Gate
현재 package_build_allowed=false 유지. 이번 cloud 소스 수정 및 앞으로의 실제 UI/잠금 수정을 하나의 검수 가능한 변경으로 모으고 회귀검증 후 통제된 후속 후보 발행을 판단한다. 기존 후보 payload를 직접 덮어쓰지 않는다. PHOTO 분할/4x 알고리즘 재작업 금지. 확정 제목/배치/색상/7보정/광고숏폼 버튼 보존.

PR23 HOLD / DO NOT MERGE. main/force push 금지. OpenAI 연결 미승인, Marketing/AVORA DEFERRED 유지. owner_pc_runtime_pass=false 및 final_product_pass=false 유지. 최종 PASS 문자열 발급 금지.
