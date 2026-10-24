# 전체 기능 재검수 및 복원 실패 수정 — 2026-10-17

판정: PARTIAL. 기존 24 기능군을 최신 소스·기존 실행 증거와 대조했다. 이번에 60버튼·고비용 모델 전체를 다시 실행한 것은 아니다.

## 새로 재현·수정한 결함
프로젝트 Open이 현재 project_id/job_ids/입력/미리보기를 먼저 교체했다. 이후 참고·음성 요청이 실패하면 false를 반환하면서 이전 작업을 잃고 부분 복원된 프로젝트를 Save할 수 있었다. 미리보기 HTTP 실패는 아예 무시됐다.

복원에 필요한 미리보기·참고·음성을 모두 먼저 읽고 성공 후 활성 상태를 교체한다. 실패하면 기존 입력 객체·미리보기·project_id·job_ids가 보존된다. 복원 파일명도 원본 input이 아닌 실제 preview/primary output의 이름을 사용한다.

기존 소스에 새 회귀 테스트를 적용하면 세 실패 경로 모두 FAIL(BEFORE_NODE.txt). 수정 후 세 실패 경로와 정상 복원·출력 파일명 및 기존 전환 보호 모두 PASS(AFTER_NODE.txt). 이는 Node VM에서 제품 컨트롤러를 실행한 검증이며 실제 Chrome/EXE 신규 검증으로 확대하지 않는다.

## 검증
- Node 전체: 14 PASS.
- 모델 재추론 없는 Python 기능·오프라인 identity·저장·Export·작업상태·런처·종료·UI/외부 브리지 회귀: 92 PASS / 2 native Windows SKIP.
- 넓힌 테스트에서 __init__을 생략한 offline identity fixture 2개가 새 lifecycle 필드 부재로 실패했다. identity fingerprint 단위 테스트가 기존 _runtime_identity를 직접 검사하도록 갱신했다. 실제 lifecycle identity는 별도 실제 HTTP 테스트가 계속 검증한다. 제품 runtime 필드를 숨기거나 기본값으로 우회하지 않았다.
- 승인 HTML/CSS, PHOTO 분할/4× 및 가중치 변경 없음. 새 모델 추론 0회.

## 전체 검수에서 남은 범위와 실행 순서
1. Build Gate는 false 유지. 다음 후보가 허용될 때 84cf 전환, 3020397 밀집 자산/정상 종료, 이번 복원 실패 수정을 함께 포함하고 source/manifest/ZIP SHA 고정 후 독립 검증한다. c37에 포함됐다고 주장하지 않는다.
2. 해당 후보 실제 사무실 PC에서 identity/PID 확인 → Save → 정상 제품 서버 종료/endpoint 불응답 → EXE 재실행/새 PID → 동일 프로젝트 Reopen/참고/음성/자막 → Export.
3. PotPlayer 영상·탐색 PASS는 보존하되 실제 소리 청취는 미확인으로 유지한다. 밀집 자산·낮은 높이 화면과 최종 승인 UI 전체 일치는 별도 확인한다.
4. R9 TXT/CSV/PNG/예외 원본은 접수 검증 완료. 272MB 이전 R9 ZIP 원본 바이트는 미접수. deploy.lock CLI 열기 권한 오류와 native byte-lock 충돌은 구분하며 소유자는 미확정이다.
5. AI 엔진의 기존 실제 추론 증거는 보존한다. 현재 자연어 기능은 고정 intent dispatcher이며 범용 생성형 계획기·영속 큐/취소/자동재시도·TTS는 미구현이다. 승인 없는 공급자·키 연결로 임의 활성화하지 않는다. Marketing HTTP/AVORA/승인 광고 MP4는 DEFERRED_EXTERNAL 유지.

PR23 HOLD / DO NOT MERGE. main/force push/직원 최종 패키지 재생성 금지. 전체 최종 PASS 발행하지 않음.
