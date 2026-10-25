# MINDLE MEDIA AI AI 코어 실무 E2E R1 결과

작업 ID: `MEDIA-AI-CORE-E2E-R1-20261025`  
기준 원격 HEAD: `410ba721eac23e118a4b4ff7938dd44501118591`  
검증 코드 기준: `79831e0cd21ed3bb5216437e34b4c28dcec4c054`  
최종 판정: **PARTIAL / 30초 실무 E2E BLOCKED**

## 이번에 직접 확인한 내용

- 원격 브랜치 HEAD가 인계값 `410ba721…`와 같음을 새로 fetch해 확인했다.
- 1.5B 자동 노출 판단 실패 원문과 7B Linux 합성 2건 제한 PASS를 보존했다. 이를 Windows 채택이나 건축 품질 PASS로 확대하지 않았다.
- 현재 Windows에 설치된 모델은 Qwen2.5-1.5B Q4_K_M이다. 모델 SHA는 `6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e`, 실행기 SHA는 `cfbe37629352def818bb1c917419d7433abfe53a77151d0154bf5e7d4858ff37`이다.
- Supertonic 설치 identity는 기존 `RUNTIME_ENGINES.json`과 일치한다. 다만 이번 30초 체인에서 새 합성과 사람 청취를 실행하지 않았으므로 기존 증거를 이번 E2E PASS로 재사용하지 않았다.
- 7B Windows 분할 가중치는 이 PC에서 발견되지 않았다. 설치본 교체와 신규 후보 제작은 Build Gate=false 때문에 실행하지 않았다.
- 권리·출처가 등록된 건축 사진 5장의 실제 bytes, SHA-256, 해상도를 다시 확인했다. 실제 건축·리조트 영상, 승인 음악, 확정 한국어 원고와 음량·길이 정책은 접수되지 않았다.
- 합성 회색 영상, 색상 영상, 테스트 톤, 임의 원고로 실무 인수를 대체하지 않았다.

## 새 회귀 결과와 수정

Windows에서 모델 runtime tree 정렬 테스트가 `A.txt`와 `a.txt`의 동시 생성을 가정해 실패했다. 기본 Windows 파일시스템에서는 두 이름이 충돌한다. 제품 해시 함수는 변경하지 않고, 충돌 없는 파일명으로 동일한 대소문자 정렬 계약을 검증하도록 테스트 fixture만 수정했다.

- 집중 계약 회귀: `64 PASS / 1 SKIP`
- 더 넓은 선별 실행에서 FFmpeg H.264 encoder가 없는 개발용 LGPL binary 때문에 미디어 fixture 생성 항목은 환경 실패로 분리했다. 제품 후보나 기존 성공 증거를 변경하지 않았다.
- UI, 모델 가중치, 제품 runtime, 패키지, Timeout은 변경하지 않았다.

## 30초 통합 실행 판정

`자연어 → Qwen 계획 → FFmpeg → Supertonic → BGM/원음 → 검수 → Save/Reopen/Export`는 이번 실행에서 완료하지 않았다.

차단 원인은 독립적이다.

1. `BLOCKED_ASSET_INTAKE`: 실제 영상, 승인 음악, 원고와 음량·장문 정책이 없다.
2. `BLOCKED_MODEL_ADOPTION`: 자동판단에 제한 PASS를 얻은 7B는 Linux 격리 후보뿐이며 Windows 설치·채택 승인이 없다.
3. `BLOCKED_BUILD_GATE`: Build Gate=false이므로 최신 소스와 7B를 포함한 Windows 후보를 만들 수 없다.
4. `BLOCKED_HUMAN_ACCEPTANCE`: 최종 건축 화면 품질과 한국어 음성 청취 대상 산출물이 없다.

중간 파일 생성이나 기존 1.5B/Supertonic 실행을 조합해 완료로 표시하지 않았다.

## Gate 표

| Gate | 판정 | 근거 |
|---|---|---|
| 소스 identity | PASS | 원격 HEAD `410ba721…`; 검증 코드 `79831e0…` |
| 모델 identity | PARTIAL | 기존 Windows 1.5B·Supertonic 확인, 7B Windows 없음 |
| 실제 추론 | NOT_EXECUTED | 새 실무 입력과 7B Windows 조합 미실행 |
| 입력 결속 | BLOCKED | 필수 영상·음악·원고 미접수 |
| 판단 적합성 | PARTIAL | 1.5B FAIL, 7B 합성 2건 제한 PASS 보존 |
| 지시 준수 | SOURCE PASS | 원고·수치·길이·음량 계약 회귀 보존 |
| 실제 실행 | BLOCKED | 자산·모델 채택·Build Gate |
| 결과 검수 | NOT_EXECUTED | 최종 30초 MP4 없음 |
| 실패 보호 | PASS | 대체 실행·완료 게시 안 함 |
| 영속성 | NOT_EXECUTED | 이번 최종 산출물이 없어 Save/Reopen/Export 미실행 |
| 실무 품질 | BLOCKED | 사람 검수 대상 없음 |
| 대표 인수 | BLOCKED | 선행 Gate 미충족 |

## 다음 진입 조건

General Work에는 권리 확인된 영상과 음악, 확정 원고·음량·장문 정책을 전달해야 한다. 모델 책임자는 7B Windows 채택 여부와 정확한 분할 가중치·runtime·메모리 조건을 승인해야 한다. 별도의 유효한 Build Gate가 열린 뒤에만 신규 Windows 후보를 제작한다. 그 후보에서 새 추론 원문, 30초 MP4, 기술 검사, 콜드 재시작, Reopen, Export, 화면·청취 사람 검수를 연속 수행한다.

PR #23 Draft/HOLD, main 병합 금지, Build Gate=false, 전체 제품 PASS 금지를 유지한다.
