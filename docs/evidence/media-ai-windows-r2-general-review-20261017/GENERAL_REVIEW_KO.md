# Windows R2 원본 독립 검수·잔여 소스 수정

2026-10-17 KST. 인계 `bfd08648213f79c980c6e749a990222c955645b5`.
수정 `30203975e8fe8e6e3ee15dc1450a2486aa5e90e9`.

## 수용한 실제 성과

원격의 전달 객체109개를 General에서 별도 내려받아 크기/SHA를 확인했다.
ZIP3개를 조립해 원본 SHA/CRC가 일치했고, 원본 manifest92개 파일도 전부 일치했다.
그중 c37 Export의129개 파일은 ZIP 안에서 다시 크기/SHA를 확인했다.
이 확인은 Windows 작업자의 readback 보고를 복사한 것이 아니라 실제 bytes를 수령한 독립 검사다.

Chrome6개 시나리오 JSON 모두 PASS, 실제 Chrome155.0.8059.80, source ef56f956을 확인했다.
실행된 product_integration.js/workspace_shell.js는 LF/CRLF 차이를 제외하면 해당 수정 소스와 같다.
기존6개 검사는 재실행하지 않고 원본 실행 증거로 수용했다.

c37의 실제 Explorer 기동·identity·복제 프로젝트 Save/Reopen/Export와 PotPlayer 표시/진행/앞뒤 탐색 증거도 수용한다.
이는 서버 완전 종료·새 PID 재실행, 최신 수정 포함 EXE, 실제 청취 PASS가 아니다.
실제 청취는 Owner 응답대로 미확인이다.

## deploy.lock 원인 구분

CLI 원본은 one_click_bootstrap.py line60의 파일 열기 Errno13이다.
실행 context는 AppContainer/low-integrity이며 사용자 경로 ACL FullControl/readOnly=false와 구별해야 한다.
Explorer 후속 원본은 line68의 byte-lock 획득 실패→line73의 준비 작업 충돌 안내다.
R9 원본 예외도 같은 DeployLock byte-lock timeout 코드 경로임을 확인했다.
잠금 소유자는 미확인이므로 stale lock·ACL 결함·모델 실패로 단정하지 않는다.
bootstrap·ACL·환경변수·lock은 변경하지 않았다.

## 수정1 — 자료 목록으로 인한 패널 확장

원본 Windows 측정은 패널 bottom1142/viewport1024였다.
실제 소스 서버와 Linux Chromium138에 자료 밀집 fixture를 적용해 확장을 재현했다.
asset-grid에 높이 상한과 내부 스크롤이 없어 항목 수에 따라 grid row가 계속 커졌다.
interaction.css에서 목록만 max-block-size16rem/overflow-y:auto로 제한했다.
마지막 자료도 스크롤로 접근되며 삭제/누락하지 않는다. VIDEO 미디어의 intrinsic sizing도 기존 contain/center 프레임 안으로 제한했다.

같은 Noto 한글 폰트·1536×1024 조건에서 panel bottom1086→885, PHOTO 입력 bottom970→769로 줄었다.
1920×1080에서도 두 패널이 viewport 안에 들어왔다.
1366×768은 패널 bottom920.72로 전체가 동시에 보이지 않지만 정상 페이지 스크롤로 입력·자료에 접근된다.
이 낮은 높이 결과를 전체 화면 동시 표시 PASS로 과장하지 않는다.
세 viewport에서 마지막 자료의 실제 box가 스크롤 영역 안으로 들어오는지 확인했다.
Windows Malgun과 다른 Linux 폰트이므로 정확한 최종 UI 승인이나 사무실 PC 재검수 완료를 주장하지 않는다.
approved_visual.css·HTML·두 controller·모델·가중치는 보존했다.

## 수정2 — 서버 자체 PID·안전한 정상 종료

기존 제품 identity에는 서버 PID/인스턴스가 없고 정상 종료 API도 없었다.
따라서 CIM 가시성 제한을 제품 자체 정보로 보완할 수 없었다.
서버가 자신의 PID·명령행·시작 시각·고유 인스턴스를 identity에 제공하도록 보완했다.
정상 종료는 loopback/Host/Origin 검사, 메모리 내 인스턴스 capability, 일치하는 PID/instance를 요구한다.
진행 중 HTTP 작업/다운로드가 있으면409로 거절하고, 종료 중 신규 요청도 거절한다.
유효한 종료는 serve_forever→server_close로 닫으며 다른 프로세스를 종료하지 않는다.
capability는 공개 identity·로그·증거에 포함하지 않는다.

실제 소스 subprocess 두 번을 띄워 반환 PID와 실제 자식 PID를 대조했다.
첫 정상 종료 exit0·endpoint 미응답→새 PID/instance→동일 프로젝트·첨부 해시 복원→Export5개 manifest 파일 CRC/SHA→두 번째 정상 종료 exit0를 확인했다.
이 검사는 생성 이미지·무음 WAV fixture이며 모델 추론은0회다. Windows EXE 검증은 아니다.
현재 c37에 새 API가 없으므로 기존 payload를 수정하거나 같은 요청을 반복하지 않는다.

## 검증과 남은 범위

- 영향 Python46 PASS / Windows 전용2 SKIP.
- Node10 PASS.
- 실제 Linux Chromium3 viewport 밀집 자료 검사.
- 실제 source HTTP subprocess 정상 종료·재기동·복원·Export PASS.
- 신규 모델 추론·OpenAI 연결·추가 Windows 빌드0회.

후속 승인 후보에는 84cf580 전환 수정과 이번3020397의 CSS·server·launcher 정리를 함께 포함해야 한다.
현재 Build Gate=false이므로 새 후보를 만들지 않았다. 기존 c37 인수를 최신 소스 인수로 바꾸지 않는다.

남은 것은 후속 승인 후보의 실제 Windows cold restart/자료 밀집 UI 검수, 실제 청취,272MB 과거 R9 ZIP 원본 수령이다.
R9 TXT/CSV/PNG/예외는 수령했으나 대형ZIP은 index/hash만 제공돼 전체 원본 인수 완료가 아니다.
Marketing/AVORA는 DEFERRED_EXTERNAL, PR23 HOLD / DO NOT MERGE, main/force push 없음.
전체 제품 최종 PASS를 발급하지 않는다.
