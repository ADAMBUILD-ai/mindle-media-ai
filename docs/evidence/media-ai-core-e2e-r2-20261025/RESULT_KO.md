# MINDLE MEDIA AI 코어 E2E R2 결과

작업 ID: `MEDIA-AI-CORE-E2E-R2-20261025`  
기준 부모 HEAD: `fb7fc76898b2c134b40ae143f1d82596f99f82fa`  
판정: **GENERAL_PREPARATION_COMPLETE / 30초 실무 E2E BLOCKED**

## 완료한 General Work

- 과거 재고 문서 `ASSET_INTAKE.json`과 실행 선언 `INPUT_MANIFEST.json`을 분리했다. 실행 가능 여부의 권위 판정은 새로 계산되는 `INTAKE_RESULT.json` 하나뿐이다.
- 영상·BGM의 bytes/SHA/스트림/길이/해상도와 권리 선언, 확정 원고, 음량, 장문 정책을 한 번에 받는 접수표를 만들었다.
- 제품의 동일 HTTP API를 사용해 실제 import → Qwen 계획 → FFmpeg 조립 → Supertonic 및 단일 합성 → 기술 검사 → 정상 종료/콜드 재실행 → Reopen → Export를 잇는 실행기를 추가했다.
- 접수 실패 시 서버나 모델을 호출하지 않고 exit 2와 최초 차단 Gate를 기록한다. 실제 차단 probe로 Qwen·FFmpeg·Supertonic·저장·재시작·Reopen·Export가 미실행임을 확인했다.
- 제품 계획기의 BGM 허용 범위와 접수 검사 범위를 `0..1`로 일치시켰다. 나레이션과 원본음은 `0..2`를 유지했다.
- 콜드 재시작 증거 없이 기술 PASS가 나오지 않도록 승인 EXE와 source SHA를 필수 입력으로 고정했다.
- Windows 7B는 설치하지 않고 모델 분할 identity, Linux 전용 실행 identity, 실제 PC 자원 snapshot, 기존 1.5B/Supertonic 보존법, 승인 요청 범위를 문서화했다.

## 기존 증거 재사용 범위

- 코어 `19d9cd56` Run `40180334294`: Python 338 PASS / 5 SKIP, 브라우저 41 PASS.
- Windows 집중 회귀 66 PASS / 1 SKIP.
- Linux 7B 합성 5종의 실제 추론·MP4·재열기·Export.
- Qwen 1.5B 자동판단 실패 원문.

이는 각 실행 SHA와 환경에 한해서만 유지한다. 새 실제 건축 자산, Windows 7B, 30초 실무 작품, 프로세스 콜드 재시작 또는 사람 품질 인수의 증거로 승격하지 않았다.

## 이번 검사

- 신규 접수/차단/EXE Gate 회귀: 12 PASS.
- 실제 빈 접수 probe: exit 2, `BLOCKED_ASSET_INTAKE`.
- 더 넓은 기존 테스트는 현재 개발 Python에 선언 의존성 `huggingface_hub`가 없어 수집되지 않았다. 이 환경 문제를 제품 PASS/FAIL로 계산하지 않았고 기존 원격 회귀를 다른 SHA의 성공으로 재표현하지 않았다.

## 실제 자료 상태

실제 건축·리조트 촬영 영상, 승인된 BGM, 확정 한국어 원고, 세 음량 값이 접수되지 않았다. 따라서 `INPUT_MANIFEST.json`은 의도적으로 비어 있고 `INTAKE_RESULT.json`은 `BLOCKED_ASSET_INTAKE`다. 공개 사진·합성 영상·테스트 톤·임의 원고로 대체하지 않았다.

## Windows 7B 채택 상태

모델은 `Qwen/Qwen2.5-7B-Instruct-GGUF`, revision `bb5d59e06d9551d752d08b292a50eb208b07ab1f`, Apache-2.0이다. 두 분할 가중치의 bytes/SHA는 `WINDOWS_7B_ADOPTION_REQUEST.json`에 고정했다. Linux 실행기와 runtime 해시는 Windows identity로 재사용하지 않았다. Windows 실행기·runtime SHA와 peak memory는 미확인이다. 기존 Windows 1.5B와 Supertonic은 보존하며 설치·기본값 변경은 하지 않았다.

## Gate 판정

| Gate | 판정 | 근거 |
|---|---|---|
| General 준비 | PASS | 접수표·검사기·제품 API 실행기·PC 절차·7B 요청서 |
| 소스 identity | PASS | 부모 `fb7fc768…`와 이번 변경을 별도 고정 |
| 실제 자산 접수 | BLOCKED | 영상·BGM·원고·음량 미접수 |
| 입력 결속 | NOT_EXECUTED | 유효 Manifest 없음 |
| Windows 7B identity | PARTIAL | 모델 가중치 고정, Windows 실행기/runtime 미확인 |
| 실제 새 추론 | NOT_EXECUTED | 자산·채택 승인 미충족 |
| Qwen 판단 적합성 | PARTIAL | Linux 합성 제한 PASS만 보존 |
| FFmpeg/Supertonic 통합 | NOT_EXECUTED | 실제 입력 차단 뒤 실행 금지 확인 |
| 실패 보호 | PASS | 빈 접수에서 변이·완료 게시 없음 |
| 콜드 재시작/Reopen/Export | NOT_EXECUTED | 승인 후보와 실제 결과 없음 |
| 사람 화면·음성 인수 | BLOCKED | 최종 MP4 없음 |
| Build Gate | BLOCKED | false 유지 |
| 전체 제품 | BLOCKED | 선행 Gate 미충족 |

## 대표 단일 요청표

| 필요한 자료/결정 | 담당 | 제출 위치/형식 | 충족 검사 |
|---|---|---|---|
| 실제 영상·라벨·구간·권리 근거 | 대표/자산 제공자 | R2 handoff의 `assets/`와 Manifest clip 항목 | intake exit 0 + 대표 권리 확인 |
| 실제 BGM·제품 사용 조건 | 대표/권리 확인자 | `assets/`와 Manifest bgm 항목 | SHA/bytes/오디오/권리 검사 |
| 확정 한국어 원고 | 대표 | Manifest UTF-8 원문 | 빈 값 금지, 계획 원문 결속 |
| 나레이션·원본음·BGM 음량 | 대표 | 각각 숫자; 0..2, 0..2, 0..1 | intake 및 계획값 일치 |
| 30초 초과 음성 정책 | 대표 | `reject` 또는 승인된 `extend_video` | 최종 30초 Gate와 함께 검사 |
| Windows 7B 격리 평가 승인 | 모델 책임자/대표 | 승인 ID·경로·Windows 실행기/runtime identity | 요청서의 미확인 필드 해소 |
| 최신 Windows 후보 제작 승인 | 빌드 승인자 | 별도 Build Gate 승인 ID | 현재 false 해제 전 제작 금지 |

PC Work는 위 항목을 모두 충족한 뒤 `PC_EXECUTION_KO.md`의 단일 명령으로 시작한다. PR #23 Draft/HOLD, main 미병합, Build Gate=false, UI 보존, 전체 제품 PASS 금지를 유지한다.
