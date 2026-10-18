# 2026-10-18 로컬 AI 엔진·제품 통합 마감 결과

**최종 판정: PARTIAL. 검증한 Linux 소스 제품 흐름은 PASS. 승인 UI 최종 일치·최신 Windows EXE 인수는 완료되지 않았다.**

소스 커밋: `3a889d9af5e0e91b4efc8132eb86e11251f1ced5` (이전 `31380cea4b34d6f2edb4cccf55460bb799ad33b8`). 제품 UI·PHOTO 알고리즘·가중치는 변경하지 않았다. 변경은 생성형 계획 어댑터, 신경망 TTS 어댑터, 경계 회귀 테스트다.

| 항목 | 실제 결과와 범위 |
|---|---|
| 생성형 추론 | **PASS** — Qwen2.5-1.5B-Instruct Q4_K_M + llama.cpp 로컬 CPU 실제 추론. 분류기·고정 계획으로 대체하지 않았다. |
| 계획의 의미 일치 | **PASS, 한정 시나리오** — 복합 밝기 10→명시 원고→나레이션 합성, 대비 7, STT→자막 계획, 미리 제시하지 않은 대비 13·채도 9/밝기 -6. STT 계획 검증은 새 Whisper 추론 완료가 아니다. |
| 범위 밖 모델 응답 | **PASS 차단** — 파일 삭제 요청에 모델이 무관한 보정·음성 단계를 생성해도 요청 범위·원고 검사가 HTTP 422로 거절. 범용 추론 신뢰성 전체 PASS를 뜻하지 않는다. |
| 한국어 신경망 TTS | **PASS 생성·제품 연결** — Supertonic 3 / sherpa-onnx 1.13.8, 실제 한국어 PCM WAV. eSpeak 경로는 보존. |
| 음질·자연스러움·사람 청취 | **BLOCKED / NOT_VERIFIED** — 파형·디코딩·시간 진행으로 청취를 대체하지 않았다. |
| 브라우저·MP4·BGM | **PASS** — 실제 Chrome 자연어 입력→계획→순차 실행→음성·영상 미리보기, 음성 재생성 없는 음량 0.5 재합성, 별도 원본 소리+나레이션+BGM 합성. |
| 저장·완전 재시작·복원·Export | **PASS, 소스 서버** — 정상 소유 서버 종료·endpoint 미응답·새 PID/instance·프로젝트/작업 이력 복원, 새 브라우저 Reopen·음성 재생, ZIP 15개 파일 SHA/크기·CRC. Windows EXE 증거가 아니다. |
| 영상 출력 | **PASS** — H.264 / yuv420p / AAC 48kHz, 16:9 320×180 테스트 MP4, moov가 mdat 앞에 존재. 실제 미리보기 MediaError.code=0. 승인 광고 MP4와 구분한다. |
| 원시 중간 파일 쓰기 주체 | **미확정** — 과거 writer PID를 확보하지 못했다. 이번 단일 오케스트레이터 실행은 완료. 게시용 별도 봉인·해시 보호 회귀는 PASS. |
| 승인 UI 최종 일치 | **FAIL 유지** — 동일 1536×1024 / DPR 1에서 확인. 헤더 카메라 원본 아트, 도구 표현·전체 비율 차이가 남는다. 화면 내용 상태도 다르므로 높이 차이 원인을 하나로 단정하지 않는다. |
| 최신 Windows EXE 인수 | **BLOCKED** — 새 수정·Qwen·신경망 TTS를 담은 승인 후보가 없다. c37은 미포함. Build Gate=false 유지. |

## 확인한 수정 원인과 내용

1. 기존 llama-cli 호출은 대화형 배너/프롬프트를 출력했고 모델 응답의 단계가 누락됐다. 비대화형 `llama-completion`, Qwen ChatML, JSON 형식 제약, 제품 단계 계약, 요청에 없는 보정·STT·나레이션 및 창작 원고 거절을 연결했다. 실제 모델은 여전히 틀릴 수 있으므로 원문 응답·해시와 모델 identity를 저장한다. 검사기는 계획을 생성하는 분류기가 아니다.
2. 기존 TTS는 eSpeak 규칙 기반이었다. 해시로 고정한 Supertonic ONNX·voice 자산과 sherpa 라이브러리를 검증하고 실제 CPU 신경망 추론→PCM WAV→기존 영속 큐·합성·저장·복원으로 연결했다. 외부 API·키를 사용하지 않았다.
3. 소형 모델의 오답과 초기 통합 하네스의 HTTP 400/422 예상 불일치는 원본 기록으로 남겼다. 최종 R2는 전체 흐름 PASS다. 실패를 통과 증거로 재사용하지 않았다.

## 엔진 identity

- Qwen: `Qwen/Qwen2.5-1.5B-Instruct-GGUF`, revision `91cad51170dc346986eccefdc2dd33a9da36ead9`, 1,117,320,736 bytes, SHA256 `6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e`, Apache-2.0. 공식 LFS oid와 대조.
- llama.cpp: b11716 / 797de63b2, 공식 Linux archive SHA256 `8c08b19bee40d118b803d58fd8f6633ba311ce3c7f1f0138262e636f02aa11f0` 일치. 실행기·라이브러리 트리 해시도 고정.
- Supertonic 3: upstream revision `3cadd1ee6394adea1bd021217a0e650ede09a323`, k2-fsa 공식 변환 archive SHA256 `82fa96f91c4ef8abaae3a14a3f4153facf88bed821d1f7331cec2700f432c427` 일치. 모델 OpenRAIL-M, upstream 코드 MIT, sherpa-onnx Apache-2.0. 모델 라이선스를 코드 MIT로 대체 표시하지 않는다. 가중치는 저장소·직원 패키지에 배포하지 않았다.

## 실행 증거

- `RUNTIME.json`, `BROWSER.json`, `BROWSER_REOPEN.json`: 실제 서버·Chrome·큐·엔진·재시작·Export.
- `PLANNER_CASES.json`, `PLANNER_GENERALIZATION.json`, `runtime-plans/`, `runtime-raw-responses/`, `generalization-plans/`: 추론 원문·구조화 계획·identity.
- `MEDIA_PROBE.json`, `KOREAN_NARRATION.wav`, `NARRATED_EXPORT.mp4`, `PROJECT_EXPORT.zip`: 실제 출력.
- `PYTEST.txt`: **120 PASS / native Windows 2 SKIP**. `NODE.txt`: **16 PASS**. 두 Control Plane 검수기 exit 0은 문서 정합성이지 Windows 인수 PASS가 아니다.
- `BROWSER_COMPLETED.png`는 최초 Linux 폰트 부족으로 한글이 네모로 보인 캡처다. 이후 개발 브라우저 Fontconfig에 기존 Noto CJK를 연결한 `BROWSER_REOPEN_FONT_READY.png`, `UI_AUTORESTORED_1536.png`를 시각 대조에 사용했다. 제품 CSS·폰트 배포를 변경한 것이 아니다.
- 승인 원본: `docs/evidence/media-ai-final-integration-20261017/APPROVED_REFERENCE.png`, SHA256 `cfeed43d4864dfe4cc1505dbb37d1ac44871d51cd10907f27cb2abe3694ae339`. 현재 실측: 상단 높이 66px, 좌/우 카드 x=11/773·폭=752px, VIDEO preview 406×228.375, PHOTO preview 548×308.25. 사진 7보정·광고 숏폼 버튼은 유지됐다. 전체 일치로 판정하지 않는다.

## 남은 인수 조건

1. 승인 헤더 원본 자산과 최종 DOM/CSS 기준으로 남은 UI 차이를 복원·대조한다. 승인 화면을 잘라 붙여 제품처럼 보이게 하지 않는다.
2. 유효한 별도 Build Gate 승인 후 정확한 최신 소스와 Windows용 실행기·모델·의존성·라이선스를 포함한 개발 검증 후보가 필요하다. 이번 결과는 재빌드 승인이 아니다.
3. 그 후보의 실제 사무실 PC EXE 실행→소유 서버 완전 종료→새 PID 재실행→작업 이력·자료 Reopen→나레이션 포함 Export, Windows 플레이어 표시·탐색·사람의 소리 청취를 수행한다.
4. 과거 원시 파일 writer는 당시 PC PID·traceback·bootstrap/server 로그가 필요한 미확정 조사 항목이다. 확인 전 원인 확정이나 임의 잠금/권한 우회 금지.

PR #23 HOLD / DO NOT MERGE, main 병합·force push 금지, Build Gate=false, 직원 최종 패키지 재생성 금지, Marketing·AVORA DEFERRED_EXTERNAL을 유지한다. 전체 제품 최종 PASS 문자열은 발급하지 않았다.
