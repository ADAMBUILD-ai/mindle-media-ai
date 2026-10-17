# Windows 인수 증거 인계 — 2026-10-17 R2

최종 판정: PARTIAL. 제품 전체 PASS 발행 금지. package_build_allowed=false / PR23 HOLD 유지.

## 원본 연결

Chrome 프로젝트 전환 6 PASS는 재실행하지 않았다. 실행 source ef56f956db5cdaf9e9dd455a5a8c065ce4f15a56, 수정 84cf58014eafa2aabd5eed763881424ab3a70c1f. 원본 ZIP·실행 스크립트·6개 결과·로그·화면·controller SHA는 CHROME_ORIGINAL_INDEX.json 및 chrome_original에 보존했다. Chrome 155.0.8059.80, 2026-10-17 14:36:42–14:37:15 KST. 새 c37 PC 실행과 별도 결과이다.

## deploy.lock 원인 분리

|항목|판정|실제 근거|
|---|---|---|
|경로/종류/읽기전용|확인/읽기전용 배제|owner AppData의 deploy.lock은 일반 1-byte 파일, readonly=false, reparse=false|
|단순 사용자 ACL 누락|배제|현재 사용자 R에 inherited FullControl. 이것만으로 AppContainer 유효 쓰기 허용을 증명하지 않음|
|도구 실행 문맥 차이|확인|CLI 토큰 AppContainer=1, low integrity. 실제 LOCALAPPDATA는 Packages sandbox AC. 과거 명령은 owner AppData를 명시 지정했고 open(a+b) line60 Errno13 발생|
|공유/잠금 소유자|미확인|RestartManager 시작 오류29, CIM 접근 불가, Toolhelp 제한된 프로세스만 보임. stale lock으로 판단하지 않음|
|정상 Explorer 실행|PASS c37 범위|owner AppData에 runtime 배포 완료, localhost18768 LOCAL_OFFLINE_PACKAGE c37 identity 응답, 브라우저 자동 창 표시|
|추가 실행 입력에 따른 중복 안내|확인|첫 기동 관측 전 추가 실행 입력이 발생. line68 byte-lock PermissionError→line73 준비 중 RuntimeError. 과거 line60 open 실패와 구분|

원본 traceback은 chrome_original 및 windows_diagnostics/NATIVE_EXE_EXCEPTION.json에 있다. lock/ACL/LOCALAPPDATA/제품 코드 변경, 관리자 우회, 프로세스 일괄 종료는 하지 않았다. 정상 Explorer 실행은 성공했으나 CLI context 원인을 제품 모델 오류로 합치지 않았다.

## 실제 c37 PC 결과

source c37c7819b1454996f3510f92184b1ef62faf3c78. 최신 프로젝트 전환 수정 미포함. manifest 7a31da30969b9e7901da8f109c467f281e2550171c15e9ddf3a8ddf215ab3377. EXE SHA256 24fe0ad565a5568b392b32040d7789cbd8abce7b60e8dade97666bbd1ec2888c.

복제 프로젝트 78a2aa14-15bb-4bf3-809d-8b27a85f11f9에서 기존 48 job 결과를 보존하고 실제 UI Save/Reopen/Export를 실행했다. 고비용 모델 재추론은 하지 않았다. 참고 사진2개와 음성 해시가 복원되었고 기존 프로젝트 해시는 불변이다. 첫 harness는 제품 Save 이후 content-addressed filename을 원본명으로 오인해 중단했고, 수정한 검수 스크립트는 이미 저장된 clone에서 이어갔다. 실패 로그도 보존했다.

C37_UI_EXPORT.zip 89,168,405 bytes / c1c4f0a34bf4e58530e70f7fd46bec463887884b7267647f3aa28a1a93aaa993. CRC 및 manifest 전 파일 크기/SHA 대조 PASS. 실제 Export MP4 284,879 bytes / c8fb412095b59d9970e836a662ee92874197d1f3fe88f7b4eb448cf4ec86543b. H.264/yuv420p + AAC. PotPlayer 영상 표시·시간 진행·앞뒤 seek PASS. 실제 청취는 확인자/시각 응답이 없어 BLOCKED이다.

## UI 및 잔여

1536×1024, zoom1/DPR1. VIDEO 좌측 PHOTO 우측, PHOTO stage 약400.5×225.3 가로형, 세로 원본480×960 object-fit:contain/center. 제목·사진7보정·광고숏폼·자연어 입력·우측 도구 확인. 기존48개 자료가 있는 화면에서 패널높이1064, 하단1142로 viewport를 넘는다. 전체 승인 UI 일치 PASS로 확대하지 않으며 GENERAL의 화면 검토가 필요하다. 옛 F27E로 되돌리지 않았다.

|범위|판정|재개 조건/담당|
|---|---|---|
|Chrome6 원본/해시/source|PASS|원격 인계 경로와 manifest 참조; 수령자의 독립 검증은 별도|
|c37 배포·서버·실제 Save/Reopen/Export|PASS 범위 제한|최신 전환 수정 포함 후보 아님|
|서버 완전 종료/새 PID/재실행 후 복원|BLOCKED|정확한 backend PID/명령행 및 허용된 정상 종료 수단 필요. CLI CIM 제한·TaskManager UI PID 미확보. 무차별 종료하지 않음|
|Windows 플레이어 표시/seek|PASS|실제 c37 UI Export 사용|
|사람의 실제 청취|BLOCKED|확인자와 청취 시각 필요|
|UI 전체 일치|PARTIAL|현재 화면의 세로 overflow 검토; Windows 임의 패치 없음|
|R9 원본|PARTIAL|TXT/CSV/PNG/과거 예외 복사. 272MB 기존 ZIP은 로컬 보존, 원격에는 해시/크기 index만 제공|
|Marketing/AVORA|DEFERRED_EXTERNAL|기존 상태 보존|

GENERAL 수정 검토: 실행 토큰 문맥별 deploy.lock 실패 안내와 정상 종료/PID 관측 가능 경로, 자료가 많은 화면의 높이. 소스 결함으로 단정하지 않음. 기존 payload/UI/모델/가중치/Control Plane은 수정하지 않았다. Windows 최종 인수·전체 제품 PASS는 미발행이다.
