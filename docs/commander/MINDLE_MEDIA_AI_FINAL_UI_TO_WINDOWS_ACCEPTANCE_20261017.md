# MINDLE MEDIA AI 최종 UI → Windows 인수 작업

발행2026-10-17 KST. General Work는 같은 커밋의 UI/Timeline 구현·증거를 인계한다. Windows Work는 최신 후보 승인/identity 확인 전에 c37를 최신 수정 후보로 취급하지 않는다.

1. General: 승인 카메라 배너 독립 원화 자산을 확인하고,Timeline 상태행·높이 및 전체 패널/하단 가이드 비율 차이를 마감한다. 최신 승인 원본 SHA는 RESULT_KO.md에 고정됐다. 승인 screenshot을 잘라 runtime 화면으로 대체하거나 가짜 waveform/clip을 추가하지 않는다.
2. General: 실제 미디어 Timeline,PHOTO 보정/참고,자연어 입력,모든 기존 load/save/export/shortform hook 회귀와 같은 viewport/zoom 비교 후 source 고정. UI 전체 FAIL이 해소되지 않으면 이를 명시한다.
3. 기존 Build Gate=false. 별도 유효한 후속 후보 빌드 승인 없이 제작하지 않는다. 이전1회 승인은 소비됨. 직원 최종 패키지 재생성 금지.
4. 승인된 후보: 모든84cf/302/711/c195/40de+이번 수정을 포함한 source/manifest/EXE/ZIP bytes/SHA 고정과 독립 readback. timeline_preview.js의 실제 포함·fingerprint를 확인한다. c37 원본은 보존한다.
5. 실제 사무실 Windows: EXE→Runtime PID/instance/명령행→자료있는프로젝트Save응답/project_id→제품 정상종료→PID소멸/endpoint미응답→EXE더블클릭→새PID/instance→동일projectReopen→사진/영상/자막/음성/참고 복원hash→Export파일/ZIP CRC/manifesthash.
6. 실제 설치 Windows플레이어 이름/버전·MP4hash·표시·시간진행·앞뒤탐색·청취를 각각기록. 기존PotPlayer시각PASS 보존,청취미확인 승격금지.
7. 실제 Chrome3화면:MediaError.code/readyState/videoWidth/currentSrc,Timeline realframe/waveform/seek/New/Opencleanup,PHOTO portrait fit/7corrections/referenceattachments,Save/Reopen/Export. TXT도취소된다운로드 환경은 별도진단하며 서버ZIP성공과 브라우저다운로드를분리.
8. lock삭제/ACL/관리자우회/프로세스일괄종료/Timeout증가금지. 독립가능항목계속진행. PR23HOLD/main병합금지/전체PASS금지.

제출:정확한candidateidentity,항목별PASS/PARTIAL/FAIL/BLOCKED,실행시각,원본로그/화면/응답/hash,남은UI차이와실제청취판정. Linux나원격runner결과를사무실실증으로확대하지않는다.
