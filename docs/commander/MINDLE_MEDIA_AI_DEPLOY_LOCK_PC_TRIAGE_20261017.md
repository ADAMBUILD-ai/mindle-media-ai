# PC Work — deploy.lock 원인 분리·Chrome 원본 인수
2026-10-17 KST. PR23 HOLD / DO NOT MERGE. 추가 Build Gate=false.

Chrome 전환 6개 시나리오 PASS 보고를 접수했다. 완료 검사를 반복하지 않는다. General은 원본 bytes/hash/source identity를 받기 전 독립 실증 PASS로 승격하지 않는다.

## 이번 PC 작업 범위
1. 기존 RESULT_KO.txt·시나리오 JSON/로그·FINAL_NORMAL_REOPEN_EXPORT.png·증거 ZIP의 실제 크기/SHA256/실행 시각과 사용한 product_integration.js/workspace_shell.js SHA 및 source HEAD를 인계한다. Chrome 버전·실제 사용 서버 root/identity도 기록한다. 보고서 경로만으로 원본 확인 완료라 하지 않는다.
2. 기존 실패 exception/traceback 전문, errno/winerror, 정확한 deploy.lock 경로, 원본 실행 명령·시각·작업 사용자/실행 context를 확보한다. 수집을 위해 EXE를 반복 실행하지 않는다.
3. 해당 경로와 부모 디렉터리의 존재/종류/ReadOnly 속성/소유자/ACL을 읽기 전용으로 확인한다. 실제 LOCALAPPDATA와 경로가 같은 사용자 것인지 확인한다. 잠금 파일이 있다는 이유만으로 stale lock으로 판정하지 않는다.
4. 실행 중인 해당 제품 프로세스의 PID/명령행과 이미 설치된 진단 수단에서 확인 가능한 handle 정보를 읽기 전용으로 기록한다. 다른 Python/Chrome 프로세스를 종료하지 않는다. 새 handle 도구 설치나 관리자 권한이 필요한 수단으로 확대하지 않는다.
5. ACL 접근 거부, 다른 프로세스 공유/잠금 충돌, 읽기 전용 속성, 다른 사용자 경로, 실행 도구의 쓰기 제한을 증거로 구분한다. errno=13만으로 구분 완료라 하지 않는다.
6. lock 삭제·ACL 소유권 강제 변경·권한 일괄 부여·관리자 실행 우회·LOCALAPPDATA 임의 전환·payload 교체·잠금 검증 제거·Timeout 연장 금지.
7. 같은 사용자에게 이미 허용된 정상 실행 경로가 확인되고 원인을 분리했을 때만 기존 후보를 제한적으로 재실행한다. 원래 데이터 경로를 유지하고 해당 제품만 취급한다. 성공하면 서버 완전 종료→재실행→복원→Export 및 설치 플레이어 검수를 이어간다. 실행정책/자동승인 거부라면 우회하지 않고 정확한 거부를 반환한다.
8. source launcher 결함이 확인되면 PC에서 임의 패치하지 말고 재현 근거를 General에 인계한다. General이 최소 수정·회귀·원격 readback을 수행한다. 추가 후보 제작은 별도 유효 Gate 전에는 하지 않는다.

## 판정
Chrome source PASS 보고, 원본 독립 확인, c37 EXE 실행 실패, source 수정 미포함을 각각 분리한다. deploy.lock 오류는 모델 실패/기존 launch.lock 예외로 합치지 않는다. Windows cold restart/플레이어/청취는 실제 수행 전 BLOCKED다. 전체 PASS 발행 금지.

제출: 원본 파일 인계와 hash, 실패 전문, 경로/ACL/소유자/실행 context, 제품 PID, 원인별 배제 근거, 허용 경로 재실행 여부와 후속 실기 결과. 한 항목이 막혀도 나머지 읽기 전용 증거 인수를 계속한다.
