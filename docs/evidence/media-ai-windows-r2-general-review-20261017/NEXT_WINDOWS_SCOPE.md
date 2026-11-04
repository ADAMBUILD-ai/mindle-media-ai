# 후속 Windows Work 범위와 시작 조건

현재는 기존 c37 서버를 보존한다. 완료된 Chrome6개·모델·PotPlayer 표시/탐색을 반복하지 않는다.
이번 General 수정은 c37에 없으며 Build Gate=false다. c37에 파일을 덮어쓰거나 미지원 control API를 반복 호출하지 않는다.

## General에서 완료

- 원본109전달객체/92원본파일/ZIP3개/c37 Export129파일의 독립 해시·CRC 확인.
- 기존 Chrome6 source PASS 수용 및 실행 controller 원본 대응.
- 밀집 자료 내부 스크롤 최소 CSS 수정·실제 Linux browser3 viewport 검증.
- 서버 자체 PID/명령행/instance와 확인된 정상 종료 경로 보완.
- source subprocess 정상 종료→새 PID→동일 프로젝트·첨부 복원→Export 검증.
- 영향 Python46 PASS/Windows2 SKIP, Node10 PASS.

## Windows 실행을 재개할 조건

대표의 유효한 후속 후보 빌드 승인과 exact 후보 전달이 먼저 필요하다.
새 후보에는 전환84cf580과 밀집 UI·owner lifecycle3020397이 함께 포함돼야 한다.
제작·manifest·ZIP·EXE readback은 General/승인된 build 담당이 완료한 뒤 전달한다.
Windows가 소스 수정·패키지 내부 교체·임의 재빌드로 준비를 대신하지 않는다.

## 새 후보 수령 후 한 세션 검수

1. candidate source/manifest/ZIP/EXE SHA와 보존 자료 경로를 확인한다.
2. 기존 자료는 복제 검수 프로젝트로 사용하며 원본 hash를 보존한다.
3. EXE 실행 후 runtime identity의 server_pid/server_instance_id/server_command/build_commit/manifest/data_root가 대상 후보와 일치하는지 확인한다.
4. 사진·영상·자막·음성·참고자료 Save와 project_id를 기록한다. 처리 중 작업·Export 다운로드가 끝날 때까지 기다린다.
5. 앱의 정상 owner-stop 경로로 해당 instance만 종료한다. token은 메모리에서만 사용하고 로그/화면/증거에 남기지 않는다. busy409는 중단 지시가 아니라 진행 작업 보존이며 강제 종료로 우회하지 않는다.
6. 해당 PID 소멸과 endpoint 미응답을 모두 확인한다. 새 PID를 확인할 수 없으면 API 성공 응답만으로 cold restart PASS하지 않는다.
7. EXE 재실행→새 PID/instance→동일 project_id→기존 실제 자료 복원→UI Export를 확인한다.
8. 새 Export ZIP/MP4의 해시·CRC 및 설치 플레이어의 영상/진행/탐색을 확인한다. 실제 청취는 사람이 확인한 사실이 있을 때만 기록한다.
9. 자료가 많은 1536×1024와 낮은 높이 화면에서 마지막 자료 내부 스크롤, 두 자연어 입력, Save/Export/숏폼, 사진 원본 비율·세로 contain/center를 확인한다. 낮은 높이에서 페이지 스크롤이 필요한 결과를 모든 기능 동시 표시 PASS로 과장하지 않는다.
10. 272MB 과거 R9 ZIP은 기존 로컬 원본을 보존하고 실제 전달 가능한 승인 경로가 있으면 bytes를 인계한다. index hash만으로 원본 수령 완료라 하지 않는다.

PR23 HOLD / DO NOT MERGE. main/force push/OpenAI 연결/Marketing·AVORA 실연동/직원 최종 패키지/근거 없는 전체 PASS 금지.
