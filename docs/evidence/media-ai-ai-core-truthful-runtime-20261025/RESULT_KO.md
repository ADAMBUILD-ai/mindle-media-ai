# MINDLE MEDIA AI 코어 실작동 보강 결과

## 판정

`SOURCE_PASS / R3 OWNER-PC FRESH AI GATE READY / NEW WINDOWS CANDIDATE NOT BUILT`

## 확인한 공백

R3는 원격 Windows에서 Qwen 2.5 1.5B, Supertonic 3, FFmpeg를 실제 실행한 후보이지만 제품 화면은 엔진 준비와 실제 추론 완료를 명확히 구분해 보여주지 않았다. 기존 사무실 PC 인수 도구도 저장 프로젝트 복원 확인 비중이 커서, 새 실행에서 AI가 실제로 한 번도 일하지 않아도 사용자가 단순 편집 화면을 먼저 볼 수 있었다.

## 보강

- `/api/ai-core/status`가 모델 구성과 실제 완료 증거를 분리한다.
- Qwen/건축 계획 실제 추론, Supertonic 신경망 음성, MP4 결과가 모두 확인돼야 `AI_RUNTIME_ACTUAL_CHAIN_VERIFIED`를 반환한다.
- UI 상단에 Qwen·한국어 신경망 음성·AI 작업 MP4 상태를 항상 표시한다.
- 엔진 미연결 상태는 `shell_only=true`로 노출하며 제품 PASS로 표시하지 않는다.
- 텍스트→영상 생성 모델과 의미 영상 생성은 현재 미구현이라고 계속 명시한다.
- 사무실 인수 도구가 새 입력으로 Qwen 계획→Supertonic 음성→FFmpeg MP4를 매번 실제 실행한다. 기존 결과 재사용으로 통과하지 않는다.

## 검증

- AI 코어 판정 3개 시나리오 PASS
- UI AI 상태 계약 2개 Node 테스트 PASS
- Python 구문 검사 PASS
- 인수 ZIP CRC PASS

현재 환경에는 Windows와 R3 3GB runtime이 없으므로 2026-10-25 보강 인수 도구 자체의 사무실 PC 실행 결과는 아직 없다. 검증된 R3 후보를 재빌드하지 않았고 Build Gate=false를 유지한다. 최신 UI·상태 API 소스도 R3 ZIP에는 포함되지 않는다.

PR #23은 HOLD / DO NOT MERGE이며 전체 제품 PASS 문자열은 발행하지 않는다.

## 추가 전수 보강

- SAM 2.1 사진 분할·영상 추적, Whisper 한국어 STT, Intel 4× 업스케일도 각각 `TESTED_PASS` 실행 기록이 있어야 화면에서 실제 추론 PASS로 표시한다.
- 모델 파일 확인만으로 위 기능을 PASS 처리하지 않는다.
- 새 상태 스크립트를 개발 실행 identity의 UI fingerprint 대상에 포함했다.
- 현 소스 검증은 AI 코어 판정 4개 시나리오, 사무실 인수 계약 3개, UI 계약 2개, Python 구문, JSON, ZIP CRC를 통과했다.

기계 판정 원본은 `SOURCE_VALIDATION.json`에 기록했다. 실제 텍스트→영상 생성(Wan/LTX/ComfyUI)과 의미 기반 신규 장면 생성은 여전히 별도 개발 범위이며 현재 제품의 완료 기능으로 표시하지 않는다.
