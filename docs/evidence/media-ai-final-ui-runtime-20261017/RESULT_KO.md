# 헤더·Timeline·전체 비율 최종 대조 및 Windows 인수 경계

기준: 2026-10-17 KST / parent 40de8cac09a8546e9a56121061c0d016f1515cb1.
최종 판정 PARTIAL. 승인 구조 복원과 실제 미디어 Timeline 소스 검증을 수행했지만, 전체 승인 이미지 일치 및 Windows 최종 인수는 완료하지 않았다.

## 승인 기준과 변경
최신 APPROVED_REFERENCE.png(1536x1024, SHA256 cfeed43d4864dfe4cc1505dbb37d1ac44871d51cd10907f27cb2abe3694ae339)를 기준으로 대조했다. 옛 F27E 상하 배치로 되돌리지 않았다.

- 상단 제목/탭 크기, 상단66px, 양쪽 패널의 시작 위치/너비, VIDEO/PHOTO 배너 제목과 재생/사진 SVG 아이콘을 복원했다. 불러오기 버튼과 원래 입력은 각 MEDIA 영역으로, 나머지 원래 기능 버튼은 해당 편집 도구 영역으로 이동했다. 기존 data hook과 처리기를 보존했다.
- VIDEO의 MEDIA / 중앙 Preview+Timeline / 우측 편집 도구 구조를 승인 원본에 가깝게 조정했다. PHOTO 아래7보정·실제 참고 Strip과 원본 비율/중앙 배치는 보존했다. 자연어 입력의 종전 collapsed18rem 제한을 풀어 전체 폭으로 표시한다.
- Timeline은 현재 video.src에서 실제 decoded 프레임6개를 canvas에 추출한다. 각 썸네일은 해당 실제 시점으로 이동한다. 오디오는 실제 decodeAudioData 결과의 peak를 그린다. 이미지나 파형을 임의 채우지 않는다. 자막·효과는 현재 결과 options에서 표시한다. 원래 상태 Track은 별도로 유지한다. 이는 읽기 전용 결과 시각화+탐색이며 드래그 clip 편집 기능은 아니다.
- 새 결과/New/성공 Reopen 시 이전 샘플링·fetch·AudioContext를 정리하고 Timeline을 제거한다. 실패 Reopen에서 기존 작업을 보존하는 선행 수정은 유지한다. 120초 초과/32MB 초과 오디오는 파형 미생성으로 명시한다. 모델/가중치/AI 처리 Timeout은 변경하지 않았다.
- 새 timeline_preview.js를 개발 identity와 두 패키지 빌더 fingerprint 목록에 포함했다. 빌더는 실행하지 않았다.

## 실제 검증
- Node 전체16 PASS, 새 JS syntax PASS.
- 실제 Linux Chromium138:1536x1024 /1366x768 /1920x1080 세 화면에서 실제 H264/yuv420p/faststart+AAC 생성 fixture를 재생,6프레임 추출,실제 AAC 파형 디코드,썸네일 위치 탐색,New 후 이전 Timeline 제거 PASS. 무음 트랙이 아니라 오디오 트랙 자체가 없는 MP4에서는 파형 미표시 PASS.
- MediaError.code=0, readyState/videoWidth/currentSrc/duration을 BROWSER.json에 실제 기록했다. videoWidth320/duration6초. 실제 청취는 검증하지 않았다.
- 초반 탐색 시험은 검수 정적 서버의 Range 미지원으로 seekable[0,0] /currentTime0에 머물렀다. 제품 서버를 수정하거나 대기시간을 늘리지 않고 검수 서버에 정상206 Range 전달을 구현하자 같은 탐색 시험이 통과했다. 이것을 제품 탐색 결함으로 판정하지 않았다.
- 1536 화면: 패널 시작 y66,좌측x11/우측x773,각너비752px. 영상Preview406px/사진Preview548px. 양쪽 자연어 입력669px. PHOTO 보정은 Preview 아래,참고Strip은 보정 아래다. 낮은768높이에서는 페이지 스크롤이 필요하며 입력으로 실제 scrollIntoView 가능함을 검증했다. 모든 기능이 한 화면에 들어온다고 주장하지 않는다.
- 제품 JS를 정적 HTTP 서버에서 실행했고 assets/latest API는 fixture 응답이다. 실제 모델·서버Save/Reopen/Export·Windows/EXE를 이번 시험에 실행한 것으로 주장하지 않는다. 기존 c195/711/302 실증은 보존한다.
- source fingerprint의 실제 메서드를 추출해 timeline 바이트 변경 시 fingerprint가 달라짐을 검증했다. 패키지 빌더2종은 AST/목록 포함 검증만 했다. Python 전체 회귀/Windows 패키지 빌드 PASS로 확대하지 않는다.
- 검수 환경에 Noto CJK를 로컬 주입해 한글을 표시했다. Windows Malgun과 동일 렌더링이라고 주장하지 않으며 폰트는 제품에 새로 배포하지 않았다.

## 승인 이미지 최종 대조
|항목|판정|범위|
|---|---|---|
|제목·VIDEO좌/PHOTO우·상단66·패널 시작/너비|PASS 구조 범위|실제 geometry 기록,픽셀 전체일치 아님|
|PHOTO 아래7보정·참고Strip·원본비율|PASS 소스 구조|기존 연결 보존,Windows 회귀 필요|
|Timeline 실제 프레임·실제 파형·탐색|PASS fixture browser|가짜 미디어 없음,clip 드래그 편집 없음|
|승인 카메라 배너 원화·정확한 아이콘 표현|미완료|독립 카메라 배너 원본 자산을 확보하지 못했다. 승인 screenshot을 잘라 UI 배경으로 사용하지 않았다. 현재는 gradient/SVG 구조이며 동일 원화 아님|
|Timeline 전체 시각 배치·행 높이·상태 Track|PARTIAL|실제 시각화 추가됐지만 승인 원본과 상태행 구성/높이 차이 남음|
|전체 패널 높이·하단 가이드 비율|FAIL 전체일치|1536 화면 패널 하단 약928px. 승인 이미지의 약814px와 차이. 임의로 기능을 숨겨 맞추지 않았다|
|최종 UI 전체 일치|FAIL|구조 개선을 최종 시각 승인으로 승격하지 않음|

## Windows 진행 결과
이 대화 환경은 Linux이며 사용 가능한 도구에서 사무실 Windows 프로세스/EXE 제어 경로를 확인하지 못했다. 클라우드 브라우저를 사무실 Windows로 취급하지 않았다. 원격 CURRENT General/PC lock은 package_build_allowed=false이며 기존 1회 빌드 소비가 명시돼 있다. 이번 요청을 UI 정리·인수 진행 지시로 기록하되,그것만으로 기존1회 빌드 횟수를 재사용하지 않았다. 후보 재제작/Windows 실행0회. c37에는 새 수정들이 없다.

Windows 인수 지시와 증거 계약을 같은 커밋의 docs/commander/MINDLE_MEDIA_AI_FINAL_UI_TO_WINDOWS_ACCEPTANCE_20261017.md 및 JSON에 고정했다. 최종 시각 차이 마감과 유효한 후속 후보 제작 조건을 충족한 뒤, 별도 Windows Work가 동일 source/hash의 후보를 받아 정상 종료→새PID→자료복원→Export→플레이어/청취를 수행해야 한다.

PR23 HOLD / DO NOT MERGE. main/force push 금지. 직원 최종 패키지 재생성 없음. Marketing/AVORA DEFERRED_EXTERNAL. 전체 제품 PASS 발행하지 않음.
