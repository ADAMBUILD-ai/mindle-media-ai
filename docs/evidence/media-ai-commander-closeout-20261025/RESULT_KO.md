# MINDLE MEDIA AI 사령관 코어 점검·보강 결과

기준일: 2026-10-25 KST. 검토 기준 소스: `9cc6e93042a5e8d814a1693eca3151f81bbacee4`.

## 판정

**SOURCE_REGRESSION_PASS / CURRENT_SOURCE_MODEL_INFERENCE_NOT_EXECUTED / WINDOWS_CANDIDATE_REVALIDATION_REQUIRED**

제품에는 로컬 Qwen 추론, Supertonic 신경망 음성, FFmpeg 편집·합성·저장 경로가 구현돼 있다. 기존 R3의 실제 원격 Windows 기록도 있다. 따라서 전체를 단순 화면 껍데기로 단정하지 않는다. 다만 과거 엔진 성공과 최신 소스 제품 인수를 동일시하지 않는다. 기존 R3는 오늘의 보강 기능을 포함하지 않는다.

## 점검 범위와 결과

| 기능·경계 | 확인한 근거 | 현재 판정 |
|---|---|---|
| 한국어 자연어 → Qwen 구조화 계획 | workflow_planner, 수치·범위 계약, R3 실제 추론 기록 | 기존 R3 한정 실제 실행 PASS / 최신 소스 재추론 필요 |
| 건축 영상 장면 순서·길이·기존 클립 조립 | architecture_agent, architectural_video_pipeline, 실제 FFmpeg 회귀 | 소스·조립 회귀 PASS / 최신 Windows 연속 실행 필요 |
| 한국어 신경망 음성 → 최종 MP4 | workflow_worker, 큐, 기존 R3 Supertonic 기록 | 기존 R3 실제 실행 PASS / 최신 모델 실행·사람 청취 필요 |
| 원고·수치·음량·영상 연장 통제 | 생성형 계획 검증 함수 및 거부 시나리오 | 소스 계약 PASS |
| 영속 작업·취소·실패·저장·복원 | durable_workflows와 전체 Python 회귀 | Linux 소스 회귀 PASS / Windows 인수 별도 |
| 제품 상태 API → 상단 AI 상태 표시 | 실제 HTTP·파일 변경 시험, UI 계약 | 소스 PASS / Windows 화면 시각 인수 별도 |
| SAM 사진 분할·연속 추적, Whisper STT, 4× 확대 | 어댑터·제품 경로와 성공 산출물 검사 | 이번 모델 추론 NOT_EXECUTED; 전체 기능 PASS로 승격 금지 |
| 의미 이해에 의한 새로운 장면 생성, Wan/LTX/ComfyUI 텍스트→신규 영상 | 제품 limitations 및 기존 파이프라인 경계 | NOT_IMPLEMENTED |
| 승인 UI 시각 일치·사무실 PC·실제 청취 | 기존 인수 미완료 기록 | PENDING |
| OpenAI·외부 공급자 | 로컬 구성, 키 연결 없음 | NOT_CONNECTED |

전체 저장소 Python 회귀를 실행했다. 모든 모듈의 모든 기능이나 보안·성능·실사용 품질을 전수 입증했다는 의미는 아니다.

## 수정한 실제 결함

1. 서로 다른 작업의 Qwen·음성·MP4 기록을 합쳐 `AI_RUNTIME_ACTUAL_CHAIN_VERIFIED`로 승격하던 결함을 차단했다. 한 성공 workflow 안에서 계획 응답, 생성 음성, 최종 MP4, 음성 job 연결과 실제 믹스 입력 바이트가 연결돼야 한다.
   - 현재 chain 승격은 마지막 결과가 해당 음성을 직접 합성한 MP4인 경우에 한정한다. 그 뒤 추가 편집된 MP4나 다른 workflow 간 승계는 자동 승격하지 않으며 별도 연결 증거가 필요하다.
2. 단순 가져오기 MP4를 AI 생성 MP4 증거로 집계하지 않는다.
3. 제품 데이터 경계 안에서 실제 파일의 존재·bytes·SHA-256을 검사한다. 원본 계획 응답·WAV·MP4가 삭제되거나 바뀌면 PASS를 유지하지 않는다. 파일 시스템 identity가 바뀌면 해시 캐시를 재검증한다.
4. eSpeak 같은 포먼트 TTS 설정을 신경망 한국어 TTS 준비 상태로 오인하지 않도록 구분했다.
5. 모델이 지정 원고의 일부만 복사해도 통과하던 부분 문자열 검사를 전체 따옴표 원고 일치 검사로 바꿨다. 원고는 하나, 합성·믹스는 각각 한 번이다. 여러 원고·불명확한 원고는 명확히 지정하도록 요청한다.
6. 요청 없는 나레이션·원본 음량 변경과 영상 연장을 차단한다. 명시한 백분율과 연장 정책은 정확히 대조한다. 자연어 음량 문법은 `나레이션 음량 80%`, `원본 소리 음량 20%`처럼 명시한다.
7. 일반 계획기의 응답·진단 원문도 UTF-8 bytes로 저장한다. Windows의 LF→CRLF 변환으로 raw_response_sha256이 달라질 수 있는 저장 경로를 제거했다. Windows 네이티브 재검증은 아직 필요하다.
8. 검증된 음량·영상 길이 값을 한국어 제품 표시와 연결했다. 레이아웃·색·숏폼 영역은 재설계하지 않았다.
9. README의 10월 6일 복구 전용 표기를 현재 상태와 검증 문서 색인으로 정리했다. 실행 권한은 기존 machine lock을 따른다.
10. 이미 자연어 계획기로 이관된 `속도 2배`를 수동 경로로 기대하던 오래된 UI 회귀 계약을 현 기능에 맞게 수정했다.

## 실행 검증

- 전체 Python: **280 PASS / 6 SKIP**. SKIP은 PASS에 포함하지 않는다.
- 전체 UI JavaScript: **30 PASS / 0 FAIL**.
- 실제 FFmpeg: 테스트 입력 영상·톤 WAV를 합성하고 H.264/AAC 스트림, 실제 출력 파일, 큐 봉인 후 음성 해시 연결을 확인했다.
- 실제 HTTP: 제품 상태 API가 올바른 데이터 디렉터리를 검사하고, PASS 후 파일 변경 시 상태를 낮추는지 확인했다.
- Python compileall, JavaScript 구문, git diff 공백 검사: PASS.
- 이 회차에서 Qwen·Supertonic 모델은 실행하지 않았다. 시험용 모델 응답과 추론 영수증을 주입한 계약 시험을 실제 AI 추론 증거로 계산하지 않는다. FFmpeg 시험 음성은 합성 톤이며 신경망 음성이 아니다.

## 기존 R3의 실제 근거와 한계

GitHub 원격 run `40079944004`를 읽어 `completed / success`, source `9f5d304ce825ad622bcd64df6ad3c8f154dfd3b6`를 재확인했다.

- 실행: https://github.com/ADAMBUILD-ai/mindle-media-ai/actions/runs/40079944004
- 기존 원문: `docs/evidence/windows-ai-successor-20261024-r3/ACTUAL_GENERATIVE_PLAN.json`, `ACTUAL_NEURAL_VOICE.json`, `ACTUAL_ARCHITECTURE_AGENT.json`, `BROWSER_MEDIA.json`, `BROWSER_REOPEN.json`.
- 해당 실행의 성공은 그 후보와 시험 범위에만 적용한다.
- 이번의 파일 재검증·원고 보존·음량 계약·Windows 응답 저장 수정은 기존 R3의 검증 결과로 대체하지 않는다.

## 다음 실물 인수 Gate

1. 승인된 후속 후보가 이 수정의 정확한 소스·UI fingerprint·payload 해시를 포함하는지 확인한다. 기존 R3를 최신 후보로 표기하지 않는다.
2. 실제 Qwen으로 새 명령을 추론한다. 예: 기존 영상들로 30초 16:9 건축 홍보영상을 구성하고 `"리조트에서 만나는 새로운 휴식"` 나레이션과 명시한 BGM을 합성한다. 이는 기존 자료의 조립 목표이며 신규 장면 생성 검증이 아니다.
3. 요청 원고·수치·음량·연장 정책, Qwen 원문 바이트 해시, Supertonic 새 WAV, 최종 MP4 영상·오디오 스트림, 동일 workflow 음성 연결을 검사한다.
4. 요청하지 않은 원고 축약·음량·연장, BGM 누락, 입력 파일 변경, 실행 취소·실패를 거부하고 기존 프로젝트를 보존하는지 검사한다.
5. 종료→콜드 재시작→프로젝트 재열기→내보내기 후 실제 재생·탐색·사람 청취·승인 화면 대조를 수행한다.
6. SAM·Whisper·업스케일은 각각 새 파일의 실제 모델 추론과 산출물 Evidence를 별도로 확인한다.

Build Gate=false를 유지했다. 새 EXE·ZIP 후보 제작, 모델 도입·설치, 사무실 PC 변경, PR #23 병합, main 병합, 직원 최종 배포, 전체 제품 PASS를 수행하지 않았다. 별도 빌드 승인 이후에만 후속 Windows 후보를 제작할 수 있다. 구매·OpenAI 키 연결은 이번 작업 범위가 아니다.
