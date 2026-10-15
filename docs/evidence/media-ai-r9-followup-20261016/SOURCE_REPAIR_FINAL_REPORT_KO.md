# R9 독립 소스 수정 및 실행 검증 결과

기준일: 2026-10-16 KST
판정: PASS_SOURCE_REPAIRS_AND_SCOPED_RUNTIME_REGRESSION
수정 commit: d3c88ea13af7f924dfbcba6f22c691a91b73d8da
최종 검증 source: c37d0658c7f9cf596708a420698a9e90f6475ca0
실행: https://github.com/ADAMBUILD-ai/mindle-media-ai/actions/runs/38790535399
실제 화면/측정값/HTTP receipt artifact: https://github.com/ADAMBUILD-ai/mindle-media-ai/actions/runs/38790535399/artifacts/12000451176

## 1. PHOTO 잘림: 실제 재현 후 수정

원본 제품 HTML과 approved_visual.css/interaction.css를 공식 Chrome에서 사용했다. 모델·제품 서버 없이 합성 가로1600×900, 세로900×1600, 정사각1000×1000 이미지를 viewport1280/1536에서 검사했다. 외부 스크립트와 이미지 자산은 제외했다. 따라서 이 검사는 전체 제품/UI 승인 검수가 아니라 source CSS geometry 검증이다.

두 화면 폭 모두 세로·정사각 사진이 잘렸다: 원본6조합 중4FAIL. object-fit:contain이 있어도 이미지 요소 자체의 높이가 Preview 영역을 넘었다. 1280 세로 사례: host310×174.375, image308×512. 1536 세로 사례: host408×229.5, image406×512. grid 안의 replaced-element intrinsic 크기와 percentage 높이 계산이 이미지 박스를 영역보다 크게 만들었고 부모 overflow:hidden이 이를 잘랐다.

PHOTO의 직계 img만 absolute/inset0으로 기존 stage에 고정하고 width/height100%, min-size0, contain/center를 지정했다. VIDEO, 바깥 패널, 제목, 색상, 배치, 모델 코드 변경 없음. 초기 제안 비교와 실제 반영 CSS를 별도로 실행했고, 최종 실제 source CSS 6/6 PASS. stage의 위치·크기는 각 원본 조합과 동일하고 이미지 내용이 영역 안에 들어왔다.

초기 비교 run38789620357, 실제 source CSS 비교 run38790237971 및 최종38790535399. 최종 측정값은 SHIPPED_PHOTO_GEOMETRY_MATRIX.json.

## 2. 런처 잠금 자원 정리: 확인된 코드 결함 수정

원본 source의 잠금 획득/대기 구간은 try/finally 바깥에 있어 timeout 예외 시 파일 핸들이 닫히지 않았다. 원본 코드 구간을 추출한 fault injection으로 실제 미종료 핸들을 재현했다. 기존 해제 구간은 unlock 실패 시 close가 실행되지 않으며 원래 startup 예외도 가릴 수 있었다.

launch_request_lock context manager로 획득 전부터 정리 범위를 감쌌다. 획득 성공 시에만 unlock하고, unlock 실패에도 close하며, 이미 발생한 준비 실패는 보존하고 추가 해제 오류를 note로 연결한다. 잠금 파일 삭제·잠금 제거·90초 대기 증가 없음.

fault injection6 PASS: 첫/반복 실행, 경합 후 획득, timeout, 준비 실패, 준비+unlock 이중 실패, 단독 unlock 실패. 원격 실제 Windows msvcrt3 PASS: 다른 프로세스와 배타성, 준비 실패 후 재획득, 반복 실행 후 재획득. 이 증거는 source helper의 실제 Windows 잠금 검증이며 패키지 EXE나 사무실 PC 검증이 아니다. R9 예외 전문이 없으므로 이 코드 결함이 R9 예외와 동일 원인이라고 확정하지 않는다.

## 3. Export 중단 시 이전 정상 ZIP 훼손: 재현 후 수정

원본 export_project는 최종 파일을 바로 w 모드로 열었다. 기존 정상 Export가 있는 상태에서 다음 출력 쓰기에 OSError를 주입하자 이전 ZIP bytes가 바뀌는 결함을 재현했다.

새 ZIP은 고유 임시 파일로 만들고 전체 CRC 검증 후 os.replace로 교체한다. 실패 시 임시 파일만 정리해 기존 Export를 보존한다. 검사 후 사라진 결과 파일을 조용히 건너뛰던 분기도 제거해 누락을 성공으로 처리하지 않는다.

쓰기 중단·출력 누락 회귀2 PASS. 기존 저장 및 영상 편집/재열기7 PASS와 잠금6을 합쳐 local/remote 모두15 PASS. 모델 추론 없음.

## 4. 실제 HTTP 서버 cold restart

로컬과 원격 Linux에서 실제 별도 서버 프로세스를 실행했다. 합성 사진 보정과 합성 영상 편집을 HTTP 요청으로 저장한 뒤 서버를 종료하고 기존 endpoint 미응답을 확인했다. 동일 data root로 신규 서버를 실행해 project_id와 사진/영상 결과 SHA256이 일치하는지 확인하고 Export ZIP 다운로드/전체 CRC/포함 결과 SHA256을 검사했다.

최종 원격 PID4092→4147, old_endpoint_closed=true. 사진/영상2개 출력 복원 및 ZIP 검증 PASS. REMOTE_SOURCE_HTTP_COLD_RESTART.json에 실제 job/project/hash 기록. 이는 Linux source HTTP 검증이며 Windows EXE 및 한국어 STT/참조 복원의 신규 실증이 아니다.

## 5. 실행 이력과 보존

첫 실제 source CSS 비교 job에서 geometry 자체는 통과했으나 별도 영상 회귀가 runner의 FFmpeg 부재로 실패했다(run38790237971,14PASS/1FAIL). 이를 숨기지 않고 workflow에 FFmpeg 의존성을 추가했다. 최종run38790535399의 Linux/Windows job 모두SUCCESS,15회귀/3native/6geometry 및 HTTP cold restart PASS.

로컬 Node interaction/SSOT/cloud 검증5 PASS. approved_visual.css SHA256은 712cfaa77fe0b3936c48a65a3d0a781397d9014afa0b5e6fffdb938f3d46a488로 보존됐다. 현재 source UI와 R9 승인 비교 PNG의 완전 일치는 원본이 없어 미검증이다.

## 6. 남은 PC 항목과 후보 발행 판단

- R9 원본 보고/CSV/승인비교PNG/ZIP bytes 독립 인수 및 검증.
- 사무실 Windows의 기존 EXE 완전 종료/재실행 및 동일 프로젝트 복원.
- 실제 Windows 플레이어 재생·탐색·소리 청취.
- R9 잠금 예외 전문과 이번 source 결함의 인과 대조.
- 승인 화면 원본과 같은 viewport의 구조 전체 대조.

후속 개발 검수 후보는 필요하다. 기존 후보0e4e12a/run38497304486에는 cloud 수정, PHOTO 크기 수정, 런처 정리, atomic Export가 포함되지 않았다. 네 수정을 묶은 후보의 manifest/ZIP SHA를 새로 고정한 후 영향 항목과 저장/재열기/Export를 PC에서 검수해야 한다. 현재 package_build_allowed=false를 유지했으며 빌드/배포/직원 최종 패키지 재생성은 실행하지 않았다.

PR23 OPEN DRAFT HOLD / DO NOT MERGE. main797da297f588780ad2d608deea3b5af8f05af450 유지 확인. force push 없음. PHOTO adapter/가중치/과거 PASS 증거 변경 없음. OpenAI 미승인, Marketing/AVORA DEFERRED 유지. owner_pc_runtime_pass=false, final_product_pass=false. 최종 전체 PASS 문자열 발급 없음.
