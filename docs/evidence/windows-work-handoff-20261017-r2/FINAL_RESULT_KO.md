# WINDOWS WORK 최종 인계 결과 — 2026-10-17

최종 판정 PARTIAL. 제품 코드·UI·모델·가중치·payload 변경 및 재빌드 없음. Build Gate=false, PR23 HOLD 유지. 전체 제품 PASS 미발행.

|항목|판정|결과|
|---|---|---|
|Chrome 6 PASS 원본|PASS 인계|ef56f956 실행 원본·source·두 controller SHA·6 JSON·통합 로그·화면·ZIP 제공. 재실행하지 않음|
|deploy.lock|원인 분리 PARTIAL|CLI AppContainer/low-integrity의 line60 open Errno13과 정상 Explorer 실행 이후 line68 byte-lock 충돌을 구분. 사용자 FullControl/readonly=false. 공유 소유자는 확인 불가; stale/ACL 결함 확정 금지|
|c37 EXE 실기동|PASS 범위 제한|Explorer 실행으로 실제 owner runtime 배포, LOCAL_OFFLINE_PACKAGE c37 identity 및 자동 브라우저 창 확인. 첫 기동 관측 전 추가 실행 입력으로 중복 준비 안내가 발생한 기록도 보존|
|자료 복원·Save·Export|PASS 범위 제한|복제 프로젝트78a2aa14-15bb-4bf3-809d-8b27a85f11f9. 기존48 job 보존, 참고사진2개/음성 해시 일치, 원래 프로젝트 해시 불변. UI Save/Reopen/Export, ZIP129파일 manifest SHA/크기·CRC 정상|
|서버 완전 종료·새 PID·재실행|BLOCKED|도구 CIM/프로세스 가시성 제한으로 정확한 backend PID/명령행·정상 종료 경로 미확보. netstat에 안 보여도 HTTP는 응답하므로 종료 PASS 아님. 서버는 실행 상태로 보존|
|설치 플레이어|표시/seek PASS, 청취 BLOCKED|실제 c37 UI Export MP4, PotPlayer engine1.7.22619.0. 영상/시간진행/4초앞탐색/1초뒤탐색 확인. 사용자가 명시적으로 ‘청취 미확인’ 응답. AAC 존재를 실제 청취로 대체하지 않음|
|UI|PARTIAL|1536×1024/zoom1. VIDEO좌 PHOTO우, PHOTO 가로 preview 및 세로contain/center, 7보정·광고숏폼·자연어·우측도구 존재. 기존자료 다수 상태 패널높이1064/하단1142로 viewport 초과. GENERAL 검토 필요, Windows 임의패치 없음|
|R9|PARTIAL|기존TXT/CSV/비교PNG/잠금예외 원본 인계. 272MB 과거ZIP은 로컬 보존·해시index만 원격 제공; 새 로그로 대체하지 않음|
|Marketing/AVORA|DEFERRED_EXTERNAL|변경 없음|

c37에는 최신 프로젝트 전환 수정84cf580이 포함되지 않는다. c37 실행 성공을 최신 수정 포함 후보의 인수 PASS로 확대하지 않는다. 완료된 모델 추론·입력8·버튼60 준비도 반복하지 않았다.

GENERAL 재개 조건: 정확한 제품 backend PID/명령행과 허용된 정상 종료 수단 확보 후 종료→endpoint 미응답→새 PID→동일 clone 복원 검수. 현재 자료가 많은 UI 높이는 첨부 실제 화면으로 검토. 코드 결함은 미확정이며, 필요 시 GENERAL이 수정/회귀/별도 유효 빌드 승인을 담당한다.

실행 도구의 Git 자격 증명 접근 거부0x5도 별도 보존했다. 관리자·ACL·잠금 삭제·환경변수 전환 우회 없이 연결된 GitHub 도구로 전달했다.

원본 인계 커밋: 0656eb7efd42b721d7e4586de9133fcd567c4dd2. 같은 원격에서 다시 fetch해113객체 바이트 해시, 원본 manifest92파일, 분할ZIP3개의 복원 SHA256/CRC를 확인했다. REMOTE_FULL_BYTE_READBACK.json 참조. GENERAL 담당자의 별도 독립 수령 확인은 아직 아님.

ZIP 복원: 이 디렉터리를 받은 뒤 기존 개발 검수 Python으로 REASSEMBLE_ZIPS.py 실행. 제품 설치나 빌드 작업이 아니며, 원본43MB Chrome ZIP·15MB source Export·89MB c37 Export를 동일 bytes로 복원한다. 파일 목록/크기/SHA256/분할 순서는 REMOTE_DELIVERY.json 및 TRANSFER_MANIFEST.json 참조.
