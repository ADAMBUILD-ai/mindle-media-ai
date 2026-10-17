# MINDLE MEDIA AI — 최종 마감 연속 실행 지시서

기준일: 2026-10-17 KST. 기존 Epoch `MEDIA-AI-20261013-OWNER-RUNTIME-RECOVERY-R1` 유지.
목적: 이전 성과와 현재 소스를 연결해 남은 결함만 마감한다. 준비 보고·수집 도구 추가만으로 종료하지 않는다.

## 1. 고정 기준

- canonical branch `feature/ad-shortform-bridge-p0-20260926`만 사용한다.
- PR23 HOLD / DO NOT MERGE, main 병합·force push 금지.
- Build Gate=false. 승인된 후속 후보 1회 제작은 소진됐다. 추가 자동 제작·직원 최종 패키지 생성 금지.
- PHOTO 분할·4× 알고리즘/가중치와 완료 고비용 추론을 반복하지 않는다.
- 10월10일 Owner 기준인 VIDEO 좌측·PHOTO 우측, PHOTO 가로 기준, 세로 Auto Fit·중앙·원본 비율을 유지한다.
- 제목·7보정·자연어 입력·광고 숏폼·우측 편집 패널·색상·배치를 임의 재설계하지 않는다.
- OpenAI 키 연결 미승인. Marketing HTTP·승인 AVORA·외부 광고 Preview/Export는 DEFERRED_EXTERNAL.

## 2. 현재 확정 후보와 성과

후보 source `c37c7819b1454996f3510f92184b1ef62faf3c78`.
Producer 38845082039, 독립 readback 38846038527, 추가 실제 EXE 38851276116.
ZIP SHA256 `5291760966d87089259de4d1030879fdf0a1a878d7b9f1fd12f7918f36656b30`.
Manifest `7a31da30969b9e7901da8f109c467f281e2550171c15e9ddf3a8ddf215ab3377`.
EXE `24fe0ad565a5568b392b32040d7789cbd8abce7b60e8dade97666bbd1ec2888c`.
Runtime `c37c7819b145-cfb26b181119`.

ZIP CRC/19,236 manifest 파일, 저장 수정 포함, 실제 원격 Windows EXE의 서버 종료→새 PID→동일 프로젝트→참고2/음성 해시 복원→UI Export PASS를 보존한다.
이 결과를 실제 사무실 PC·설치 플레이어·청취·전체 제품 PASS로 확대하지 않는다.
백업·입력8·버튼60 준비와 기존 모델 검수는 다시 시작하지 않는다.

## 3. 이번에 완료한 General Work

프로젝트 전환 경합을 실제 production JS controller로 재현했다.
편집 중 New가 파일 상태를 비우고, Save 대기 중 New 후 이전 응답이 project ID를 재부착할 수 있었다.
편집·저장·복원·Export 동안 전환을 거절하고, 소유한 작업만 guard를 해제하도록 수정했다.
실패/거절된 프로젝트 열기에서는 dialog를 닫지 않는다.
구현 source `84cf58014eafa2aabd5eed763881424ab3a70c1f`.

새 controller 회귀5개, 전체 Node10 PASS. 영향 Python30 PASS/Windows 전용1 SKIP.
이는 실제 production JS를 실행한 DOM/network fixture 검사다. 실제 Chrome·Windows 실행 증거로 바꾸지 않는다.
소스 HTML/CSS·PHOTO/VIDEO 편집 구현·모델 adapter는 변경하지 않았다.
이 수정은 c37 후보에 미포함이다. 기존 payload 덮어쓰기·JS 파일 수동 교체 금지.

## 4. 후속 실행 — 큰 작업 단위로 끝내기

### A. 신규 전환 수정 브라우저 검증 및 후보 반영

접근 가능한 실제 브라우저에서 지연된 편집·Save·Reopen·Export 중 New/Open을 조작한다.
현재 자료·project_id가 유지되고 중복 HTTP가 생기지 않으며 완료 후 정상 전환되는지 확인한다.
새 프로젝트 첫 Save가 이전 project_id를 보내지 않아야 한다.
정상 Save/Reopen/Export, 실패 후 재시도, cloud/local 분리 회귀를 확인한다.
별도 후보 제작 승인이 실제 활성 gate에 기록되기 전에는 제작하지 않는다.
승인 후에는 source/ZIP/manifest/EXE를 새 identity로 고정하고 독립 readback한다.
이전 c37 증거를 새 후보 실행 증거로 재분류하지 않는다.

### B. 실제 사무실 PC 한 세션 실기동

기존 도우미와 설치 환경을 사용한다. 다른 제품/개인 자료·다른 Python/Chrome은 종료하지 않는다.
후보 identity를 확인하고 복제 검수 프로젝트로 Save 응답·project_id·PID·명령행·시간을 기록한다.
정상 종료 경로 우선으로 해당 제품 서버를 종료한다. PID 소멸과 endpoint 미응답을 모두 기록한다.
EXE 더블클릭→새 PID→동일 프로젝트 Reopen→사진·영상·자막·음성·참고 복원을 항목별 확인한다.
실제 UI Export로 ZIP/MP4를 받고 크기·SHA·CRC·manifest 파일을 확인한다.
한 실패가 발생해도 독립 항목은 계속하며 입력·오류·로그를 보존한다.

### C. Windows 플레이어와 실제 청취

같은 세션 Export MP4를 설치 플레이어로 직접 연다.
플레이어 이름/버전·재생 시간 진행·탐색·영상 표시를 기록한다.
실제 스피커/이어폰 소리 청취는 사람이 들은 사실과 시각을 기록한다.
무음 WAV·ffprobe·브라우저 decode는 청취 증거가 아니다.

### D. UI·R9 원본·잠금 로그를 한 번에 인수

최신 Owner 좌우 배치를 기준으로 실제 viewport/zoom·자연어 입력·우측 패널·PHOTO contain/center를 대조한다.
F27E 역사 원본과의 상하/좌우 차이는 사실로 보존하되 이를 최신 좌우 승인 위반으로 단정하지 않는다.
미디어 원본 크기/box·computed object-fit/object-position/overflow·적용 CSS 경로를 기록한다.
R9 TXT/CSV/PNG/ZIP, 승인 원본, bootstrap/server log, 예외 전문·launch.lock 상태를 원본 크기/SHA/시각과 연결한다.
R9 실제 예외 로그 없이 새 runner 로그나 모의 잠금 테스트로 R9 원인을 확정하지 않는다.
lock 삭제·잠금 검증 제거·Timeout 연장·다른 프로세스 일괄 종료 금지.

## 5. AI/엔진 완료 범위

SAM PHOTO·Intel SISR·SAM video memory tracking·Whisper-small 실제 추론 증거는 10월14일 엔진 복구 보고와 receipt에 있다.
고정 명령 dispatch·OpenCV/Pillow/FFmpeg 처리와 생성형 의미 계획을 구별한다.
생성형 planner, durable 다중 에이전트 queue·자동 재시도·취소는 활성화 완료로 처리하지 않는다.
품질 정답셋/WER/추적 정확도는 실행 파일 생성 PASS와 별개다.
OpenAI 연결·외부 연동 승인 전 이를 우회해 새로운 provider/키/모델로 바꾸지 않는다.

## 6. 최종 제출과 종료 기준

제출: 수정 diff/commit, 회귀 로그, 후보별 identity, 실제 PC cold restart/Export, 플레이어·청취, 최신 UI 비교, R9 원본/예외 로그, 정확한 잔여표.
각 항목 PASS / PARTIAL / FAIL / BLOCKED / DEFERRED_EXTERNAL. 과거 증거·신규 실행·source fixture를 분리한다.
검수기 exit0은 증거 조건 충족이며 전체 제품 실행 PASS가 아니다.
실제 전체 제품 실증 전 `PASS_MINDLE_MEDIA_AI_FULL_PRODUCT_E2E_RUNTIME_VERIFIED` 발급 금지.
상세 현재 결과: `docs/evidence/media-ai-final-closeout-20261017/FINAL_REVIEW_KO.md`.
