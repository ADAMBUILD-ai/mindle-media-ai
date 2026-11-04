# MINDLE MEDIA AI 자연어 편집 도구 연결 결과

## 판정

`SOURCE_PASS / ACTUAL QWEN RUNTIME REVALIDATION REQUIRED / NEW WINDOWS CANDIDATE NOT BUILT`

## 구현

기존 FFmpeg 편집 엔진에 이미 있던 기능 중 다음 항목을 Qwen 생성형 계획과 영속 작업 큐에 연결했다.

- `N초부터 M초까지 자르기`: `start=N`, `duration=M-N`
- `속도 X배`: 0.5~2배
- `9:16` 또는 `16:9` 원본 비율 보존 패딩
- 페이드 전환
- 선택한 BGM 합성 및 음량. 명시하지 않으면 화면에 표시되는 기본값 35%

Qwen 출력은 실행 전에 사용자 문장과 다시 대조한다. 모델이 시작·종료 시간, 속도, 비율, 페이드 여부, BGM 음량을 바꾸거나 요청하지 않은 도구를 추가하면 실행하지 않는다. 구조화 단계와 영속 큐도 속도·시간·음량 범위를 다시 검사한다.

BGM 요청에 오디오 파일이 선택되지 않았으면 브라우저가 작업 제출 전에 구체적인 안내를 표시한다. 워커는 선택된 BGM의 SHA-256을 다시 확인한 뒤 attempt 전용 입력으로 복사한다.

## 검증

- 자연어 수치·도구 계약 6개 시나리오 PASS
- 기존 AI 코어 판정 4개 시나리오 PASS
- 기존 R3 사무실 인수 계약 3개 PASS
- UI 계약 3개 PASS
- Python 4개 모듈 구문 검사 PASS
- JavaScript 구문 검사 PASS

현재 실행 환경에는 R3 Qwen/Supertonic Windows runtime과 전체 Python 의존성이 없으므로 새 자연어 문장을 실제 Qwen에 입력한 재추론은 아직 수행하지 않았다. 이 변경은 소스 연결이며 기존 R3 EXE에는 포함되지 않는다. Build Gate=false, PR #23 HOLD / DO NOT MERGE, 전체 제품 PASS 금지를 유지한다.

숏폼 외부 연동, 임의 효과, 회전, 생성형 텍스트→영상은 이번 범위에 포함하지 않았으며 완료 기능으로 표시하지 않는다.
