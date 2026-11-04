# AI 작업·음성·MP4 구현 인계 — 2026-10-18

구현 소스:4bc645f4026ea8d0f1af4bfb09d614ac1166de58. 원본 지시 기준21f7d12. 증거:docs/evidence/media-ai-workflow-runtime-20261018/RESULT_KO.md.

General 구현:영속 큐·작업ID/해시·중복방지·own worker 취소·bounded retry·봉인결과·중단복구·실제 eSpeak 한국어음성·음량 재합성·BGM/자막/MP4·저장/소스서버재시작/복원/Export.

완료 범위는 실제 소스 HTTP/브라우저/FFmpeg/eSpeak와 명시된 시험에 한정한다. 범용 생성형 모델실행,신경망TTS음질/사람청취,실제모델중간취소,Windows native분기·EXE 인수,승인UI전체일치 미완료.

Windows 인계 조건:기존Build Gate=false 유지.새유효승인으로 source/EXE/manifest/ZIP SHA를고정한후보가필요하다.c37은새수정미포함.검증된Windows eSpeak실행파일/DLL/espeak-ng-data와RUNTIME_ENGINES.json의상대경로/실행파일SHA/음성데이터treeSHA를후보제작단계에서고정한다.직원은더블클릭하며수동환경설정/키입력을요구하지않는다.새공급자/API키접속없음.

Windows 수행:후보identity확인→실제계획/상태/취소/재시도→한국어음성생성/음량재합성/재생→원본/나레이션/BGM/자막합성→Save/project_id→제품정상종료/PID소멸/endpoint불응답→EXE재실행/새PID→자료/작업이력Reopen→Export/manifestSHA/CRC/MP4codec→설치플레이어표시/탐색/실제소리청취→승인UI비교.원본·게시파일SHA가작업전후유지되는지특히검사한다.원시중간파일변경의쓰기주체추가진단은남아있다.

제출:단계별PASS/PARTIAL/FAIL/BLOCKED,source/candidateidentity,시각/PID/instance,원본응답·로그·화면·voice/MP4/ZIPsha,사람청취확인,정확한잔여항목.

PR23HOLD/main병합·forcepush금지/PHOTO분할4x보존/승인UI재설계금지/MarketingAVORA DEFERRED/직원최종패키지재생성금지/전체PASS금지.
