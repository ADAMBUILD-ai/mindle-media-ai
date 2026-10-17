# 최종 수정 통합 및 후보 인수 경계 — 2026-10-17 KST

최종 판정 PARTIAL. 소스 수정 및 독립 개발 검수는 마감했다. Build Gate=false이며 새 후보를 제작하지 않았다. 최신 수정 포함 후보가 정식 인계되지 않아 EXE 완전 재시작 인수는 BLOCKED이다. c37의 기존 성과를 승격하지 않는다.

## 고정 소스와 수정

통합 소스: `c1956f48abdba52c55a20932dadad16d56bd672a`. 기준 `7116244481c8159fadaf45f6a6fcc20dededa876`. `84cf58014eafa2aabd5eed763881424ab3a70c1f`, `30203975e8fe8e6e3ee15dc1450a2486aa5e90e9`, `7116244` 모두 실제 조상 커밋으로 확인했다. 작업 시작/게시 직전 원격 HEAD와 변경을 확인했다. 기존 로컬 증거 커밋과 사용자 자료는 보존했고 기존 source 체크아웃을 재사용했다.

실제 Chrome 155.0.8059.80, 격리한 실제 ProductHttpServer·실제 제품 HTML/CSS/JS로 다음 결함을 재현했다.

1. 영상·자막·효과가 있는 프로젝트 A에서 영상 없는 프로젝트 B를 Open하면 실제 video/audio 입력은 null이지만 이전 자막·효과·영상 길이·ruler·preview job metadata가 남았다.
2. A를 다시 연 뒤 New를 하면 미리보기는 비워져도 이전 영상 효과·트랙·projectStatus가 남았다.

원인은 복원 성공/New에서 미리보기 자식만 비우거나 일부 표시만 초기화한 것이다. `clearWorkspacePresentation`을 두 성공 경로에서 함께 사용해 track/clock/seek/ruler/preview metadata/project·export 표시를 초기화한다. 복원 의존 파일의 읽기가 모두 성공한 뒤에만 호출하므로 기존 7116244의 실패 시 작업 보존을 유지한다. `FIX.diff`에 정확한 변경을 제공한다. 제품 수정은 `ui/product_integration.js` 하나이며 승인 HTML/CSS·PHOTO 알고리즘·가중치·Timeout은 변경하지 않았다.

## 검증 결과와 실제 범위

|항목|판정|근거|
|---|---|---|
|신규 표시 초기화 회귀|PASS|Node 신규 2개 수정 전 FAIL → 후 PASS, 전체 Node16 PASS|
|실제 Chrome 영상 없는 Open / New|PASS|BEFORE_R3 실패 JSON/화면과 AFTER_R1 성공 JSON/화면|
|미리보기·참고·음성 HTTP 실패|PASS 범위 제한|검수 환경에서만503 주입. 기존 입력·미리보기·project ID 보존, Save·정상 재시도 확인. 제품 우회 코드 없음|
|정상 종료 vs 작업 진행|PASS 소스 HTTP|실제 HTTP Save·사진 편집·파일 전달을 검수 I/O 경계에서 지연. 종료409, 원작업은201/200 완료, 이후 요청 정상. 해당 제품 서버 프로세스의 EXE 재시작 증거는 아님|
|관련 Python|PASS|46개 통과. 초기 신규 Save fixture가 빈 job_ids로422를 받았고 유효한 실제 사진 job을 저장하도록 검수 fixture만 수정. 이전 실패 로그 보존|
|Export 서버·ZIP|PASS 소스 HTTP|실제 UI가 Save/Export201을 받았고 파일 GET200, 직접 HTTP 수신 ZIP CRC 정상. 각 ZIP 원본 포함|
|현재 브라우저 UI 다운로드|BLOCKED|Download.save_as canceled. 허용된 workspace downloads_path에서도 동일, 단순 TXT 대조 파일도 canceled. 제품 ZIP 결함으로 확정하지 않음. 서버 생성/전달과 브라우저 다운로드를 분리|
|밀집 자산 목록·도구 접근|PASS 범위 제한|1536×1024 및1536×720, zoom1. 기존 CSS에 목록 버튼을 추가한 검수 DOM으로 스크롤·편집·자연어·Save/Export 접근 확인. 실제60개 새 자산을 import한 검사는 아님|
|승인 UI 전체 시각 일치|PARTIAL|VIDEO 좌/PHOTO 우, 가로 PHOTO와 세로 contain/center 보존. 실제 화면을 제공하되 전체 이미지 픽셀 일치·소리·새 후보 인수 PASS로 확대하지 않음|

브라우저 시험은 커밋 전 `7116244 + FIX.diff` 작업 파일에서 수행했다. 이후 원격 통합 소스를 다시 fetch했고 시험 당시 모든 제품 UI 파일 SHA256이 불변 커밋 c1956f4와 동일함을 확인했다. SOURCE_INTEGRATION.json에 파일별 해시를 제공한다.

초기 BEFORE_R1은 검수 도구 다운로드 취소로 중단됐다. BEFORE_R2는 A/B 생성 사이 New 누락으로 같은 project ID를 사용한 검수 fixture 오류가 있어 제품 Open 결함의 증거로 사용하지 않는다. 유효한 별도 프로젝트 A/B의 BEFORE_R3만 수정 전 재현 근거로 채택했다. 원래 중간 결과들은 로컬에 그대로 보존했다.

## AI 기능 경계

`AI_SCOPE.json`에 현재 `/api/jobs → execute_isolated → ProductModelVault → 검증 adapter`와 기존 실제 엔진 receipt를 연결했다. SAM2.1 사진 분할·SAM2Video 연속 추적·Intel SISR1032 4×·Whisper-small 증거는 보존하며 새 추론은0회다.

자연어 기능은 고정 intent dispatcher와 로컬 장면 분석이다. 범용 생성형 계획기는 미구현·미연결이다. `job_queue.py`에는 메모리 큐·실행 전 취소·재시도 가능 판정 계약이 있으나 제품의 영속 큐·진행 작업 취소·자동 재시도 스케줄러가 연결됐다는 뜻이 아니다. TTS도 미구현이다. 이번 마감은 이 기능들을 새로 구현하는 승인이 아니며, 필요 시 Owner가 요구 범위·공급자·자격 증명 승인을 별도로 정해야 한다. OpenAI/신규 공급자 연결 없음. Marketing HTTP·AVORA·승인 광고 MP4는 DEFERRED_EXTERNAL.

## 다음 수행 주체와 진입 조건

- GENERAL/승인자: 별도 유효한 후보 빌드 승인 전에는 제작하지 않는다. 승인 시 c1956f4 및 세 선행 수정군을 포함하고 source·manifest·EXE·ZIP 크기/SHA를 독립 readback한다. c37 payload 및 직원 최종 패키지 재생성 금지.
- WINDOWS: 정식 후보 수령 후 SHA/identity 확인 → 자료가 있는 프로젝트 Save → PID/instance/명령행 → 정상 종료 → PID 소멸·endpoint 미응답 → EXE 더블클릭 → 새 PID/instance → 같은 프로젝트 복원 → Export. 브라우저 종료만으로 완전 재시작 PASS 금지.
- WINDOWS 브라우저 환경: TXT도 취소되는 현재 다운로드 조건을 진단하되 기존 다운로드 실패를 숨기거나 제품 검증을 약화하지 않는다.
- 사무실 확인자: 설치 플레이어의 실제 후보 Export 소리 청취와 확인자/시각 기록. 기존 PotPlayer 표시·탐색 PASS 및 사용자의 ‘청취 미확인’ 응답 보존.

R9 TXT·CSV·PNG·예외 원본 인수 성과는 보존한다. 과거272MB ZIP 원본 bytes는 General 미수령이며 기존 로컬 보존/해시index만 있다. deploy.lock 열기 권한 오류와 byte-lock 충돌을 계속 구분하며 lock 삭제·ACL 변경·관리자 우회 없음.

PR23 HOLD / DO NOT MERGE. main 병합·force push 금지. Build Gate=false. 전체 제품 최종 PASS 미발행.
