# MEDIA General Work R3 — PC 인계 전 폐합

작업 ID: `MEDIA-REAL-30S-GENERAL-CLOSEOUT-R3-20261026`  
실행 소스: `8e50446144d83d804ecb8a072f93b63bc117876d`  
판정: **GENERAL_WORK_COMPLETE / PC_WORK_NOT_ELIGIBLE / 실제 30초 제작 BLOCKED_ASSET_INTAKE**

## General Work에서 폐합한 항목

General 소스 실행기와 Windows 후보 실행기의 기술 인수 규칙을 하나로 맞췄다.

1. MP4 컨테이너 길이만 30초여도 통과하지 않는다. 영상과 오디오 스트림 각각의 시작 시각, 길이, 종료 시각을 검사하고 두 종료 시각 차이도 검사한다.
2. 저장 후 실제 프로세스 재시작·Reopen에서 최종 출력 SHA만 비교하지 않는다. 원고, 음량, workspace, 원본 입력, 출력, 참조 산출물까지 저장 당시와 대조한다. HTTP 표시 URL만 비교에서 제외한다.
3. PC 후보 인수기도 위 두 검사 함수를 사용한다. PC와 General의 결과 기준이 달라지지 않는다.
4. 기존 성공 엔진 작업 재사용 선택기를 실제 변경 112개 경로로 대조했다. 엔진 workflow 본문은 같고 모든 변경은 인수 도구·문서·증거·비엔진 LTX 어댑터 범위다. `run_engines=false`로 판정했다. 과거 엔진 평가를 다시 실행하지 않는다.

## 검증 결과

- 전체 Python: **462 PASS / 6 SKIP**
- General 집중 회귀: **64 PASS**
- UI 계약: **2 PASS**
- Python 구문, 증거 동기화, 소스 패키지 트리 완결성, diff 공백 검사: PASS
- 실제 모델 추론, 실제 건축·리조트 자료 조립, Supertonic 음성, 30초 MP4, 사람 시청·청취: 실행하지 않음

동일한 1초 영상·30초 오디오 오류 MP4를 결함 주입으로 재현해 이전 검수가 통과하던 사실을 확인했고, 새 검수에서 차단되는 회귀를 추가했다. 이 시험 파일은 실제 제작 입력이나 작품으로 등록하지 않았다.

## PC Work 인계 조건

PC Work는 지금 시작하지 않는다. 현재 `OPERATOR_INPUT.json` SHA-256은 `58bc76fd27f0051ec49920b227658371ba15c4c3292d088f9add745f2bc28e06`이고 모든 실무 입력값이 null이다.

실제 영상, 사용 구간, 권리 근거, BGM 권리, 확정 한국어 원고, 나레이션·원본음·BGM 음량, 장문 정책이 모두 확정되어 입력 SHA가 바뀐 뒤에만 기존 접수 도구를 한 번 실행한다. 그때 `INPUT_MANIFEST.json`, `PREPARATION_RECEIPT.json`, `INTAKE_RESULT.json`, 원본 접근 위치를 General Work에 반환한다.

General Work는 수신 자료를 다시 결속한 뒤에만 Windows 7B 실행기·runtime identity와 승인 범위를 확인한다. 그 다음에만 PC Work가 실제 Qwen 계획 → FFmpeg 조립 → Supertonic → 단일 합성 → 저장 → 실제 재시작 → Reopen → Export → 시청·청취로 들어간다.

Build Gate=false, PR #23 Draft/HOLD, main 병합·배포·새 EXE 제작·설치 모델 교체 금지는 유지한다.
