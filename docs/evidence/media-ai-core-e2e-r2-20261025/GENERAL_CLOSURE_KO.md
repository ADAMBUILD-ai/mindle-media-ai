# R2 General 준비 폐합·인수 보강 결과

작업 ID: `MEDIA-AI-CORE-E2E-R2-20261025` / 기준일: 2026-10-25

**판정: GENERAL_PREPARATION_COMPLETE / 전체 PARTIAL / 실제 30초 실무 E2E BLOCKED.**

## 소스 인수와 변경

- 최초 지시 HEAD: `fb7fc76898b2c134b40ae143f1d82596f99f82fa`.
- 병행 PC 준비 결과 `8b0b9bce` → `41469aa7c9ede9de95b333a56cc8f63e5a2f69c7`를 발견해 대조·인수했다. PC용 기존 실행기, BGM 상한 1, Windows 인수 단위시험의 mocked FFprobe 수정과 보고된 실제 PC 자원 snapshot을 보존했다.
- 코어 보강: `93a5e80ae214365043e91622920ce8e9f1ac0e9d`.
- 원본/미리보기 결속 보강: `f94b473d8e139a526f46cd3646ef4d018af257fb`.
- 최종 동결 코드: `903f892a5dcd79166cc2ffbaa70ddaabf293aaaa`.

기존 `RESULT_KO.md`는 PC 측 최초 준비 결과로 보존한다. 이 문서와 `SOURCE_VALIDATION.json`이 후속 보강·검증·승인 경계를 추가한다. 최신 코드에 포함되지 않은 기존 R3 EXE를 최신 완료 증거로 사용하지 않았다.

## 완료한 General 작업

1. 입력 원본은 R2 INPUT_MANIFEST, 실행 상태는 그 원본 SHA를 넣어 매번 다시 계산한 INTAKE_RESULT로 정리했다. ASSET_INTAKE도 같은 계산 결과의 파생 snapshot으로 연결했다. 원본 변경 시 과거 PASS 문서로 실행할 수 없다. R1과 이전 R2 BLOCKED_PROBE는 당시 이력이다.
2. 실제 영상 사용 구간·합산 길이·권리 근거 참조·원고·세 음량·장문 정책을 검사한다. BGM은 제품 상한인 0..1과 32MB/지원 확장자를 적용한다. 원본 소리 요구 시 실제 오디오 있는 입력이 필요하다. FFprobe JSON은 Windows CP949와 무관하게 UTF-8로 읽는다.
3. General 소스용 `python -m media_ai.source_e2e`와 승인 후보용 `scripts/run_real_architecture_acceptance.py`가 같은 제품 API와 공통 원고/음량/Export/입력 검사를 사용한다. 소스 실행을 후보 실행으로 바꾸거나 두 결과를 합치지 않는다.
4. 제품 import는 영상 미리보기를 재인코딩한다. 원본 SHA는 import의 input과 결속하고, 변환된 primary_output은 별도 SHA/bytes로 검증한다. 원본과 미리보기 바이트가 같아야 한다는 잘못된 조건을 제거했다. 제한 구간은 제품 FFmpeg 편집 API로 먼저 적용한다.
5. 일반 Qwen 계획도 원래 명령 SHA·실제 응답 SHA·실제 응답의 실행 단계와 저장된 계획을 제출 전에 대조한다. 건축 계획만 보호하던 범위를 나레이션/BGM 마감 계획까지 확장했다. 실행 계획이 유효해도 다른 답으로 바꾸면 등록을 거부한다.
6. 모델 시간 초과·프로세스 오류·JSON 해석 실패의 prompt·부분 응답·stderr·실패 유형을 보존한다. 호출 반환은 도메인 검증 통과를 뜻하지 않는 상태로 기록한다.
7. 소스 실행기는 새 격리 데이터와 소유한 실제 자식 서버만 사용한다. nonce/PID/instance 결속 종료, 이전 프로세스 정상 종료, 새 PID/instance, 재열기와 Export 내부 파일/작업 정보 검사를 수행한다. 승인 후보 실행기도 실제 Windows PID 종료, 설치 Manifest·모델 2분할·runtime·Supertonic 결속, 16:9·전체 영상/오디오 디코딩을 검사한다.
8. 소스 평가 승인과 제품 후보 승인 템플릿은 모두 false다. 후보 EXE와 패키지 Manifest, source/입력 SHA, Windows 7B 채택 승인이 결속되지 않으면 PC 후보를 호출하지 않는다. Build Gate를 대신 열지 않는다.

## 이번에 실제로 실행한 증거

### 새 실제 Qwen 계획·변조 거부

`ACTUAL_QWEN_BINDING_SMOKE.json`과 ACTUAL_QWEN prompt/response:

- 실행 소스 **93a5e80a**, 기존 고정 Linux 7B 2분할·실행기·runtime, context 4096, threads 2.
- 새 기술 명령 `밝기 3 높여 줘`에 실제 Qwen이 brightness=3 계획을 반환했다.
- 원래 계획은 결속 검사 통과, 저장된 밝기를 4로 바꾼 계획은 거부했다.
- 실제 소요 약 51.9초. 모델을 다운로드하거나 설치본/기본 모델을 바꾸지 않았다.
- **계획 경계의 실제 추론 검사다. 30초 영상·새 Supertonic·Windows 추론·건축 자동 판단 품질 증거가 아니다.** 이후 두 커밋은 실행/접수 도구 수정이며 이 실제 추론을 새 SHA에서 다시 실행했다고 쓰지 않는다.

### 실제 프로세스 재시작·Export 도구 검사

`LIFECYCLE_TOOLING_RECEIPT.json` / `LIFECYCLE_TOOLING_EXPORT.zip`:

- 실행 소스 **f94b473d**, Linux 격리 환경, 1초 합성 회귀 입력.
- 서버 PID **55 → 101**, instance도 변경됐고 이전 소유 프로세스의 정상 종료를 확인했다.
- 원본·재인코딩 미리보기의 분리 identity, 저장, Reopen, Export ZIP SHA/CRC 및 내부 파일 해시를 검증했다.
- **모델·TTS 추론과 30초 실무 인수는 실행하지 않았다.** service 객체 재생성으로 대신한 검사가 아니다. 현재 최종 소스의 전체 회귀에도 같은 실제 프로세스 시험이 포함된다.

### 실패 보호 직접 시험

`FAILURE_PROTECTION_RECEIPT.json` / `ACTUAL_FFMPEG_FAILURE.stderr.txt`, 실행 소스 **f94b473d**:

- 실제 WAV 길이가 영상보다 긴 경우 reject 확인.
- BGM 해시 변경 거부.
- 음성 해시 변경 거부.
- 잘못된 입력에 대한 실제 FFmpeg 비정상 종료 확인.
- 4건 모두 기존 프로젝트 bytes 보존, 새 완료 job 게시 0건.
- 테스트 톤·합성 영상은 **실패 보호 시험에만** 사용했다. 신경망 음성이나 실제 건축 자산으로 등록하지 않았다.

### 자료 부재 차단

빈 R2 입력으로 두 실행기의 차단 회귀를 수행했다. 소스 frozen probe는 `BLOCKED_REHEARSAL_FROZEN/RUN_RECEIPT.json`에 있다. 최초 Gate는 실제 자산 인수이며 서버·Qwen·조립·음성·믹스·저장·재시작·Export 단계는 NOT_EXECUTED다. 새 증거 디렉터리만 허용하므로 과거 출력 재사용으로 통과하지 않는다.

## 모델·PC 자원 인수

7B revision, 가중치 파일 2개의 이름·크기·SHA, context/threads, Linux 실행기/runtime identity와 Windows 요청 범위는 `WINDOWS_7B_ADOPTION_REQUEST.json`에 연결했다. Windows 선행 1.5B 실행기 identity는 참고로만 기록한다.

PC 측 `41469aa7`에서 보고한 RAM 총량 약 34.23GB·당시 가용 약 7.81GB·디스크 여유 약 423.12GB snapshot을 보존했다. General이 PC를 다시 측정한 결과는 아니다. R1 Linux 표본의 HWM은 8,035,344,384 bytes이며 Windows 최소 메모리나 현재 PC peak로 사용하지 않는다. 실제 실행 직전 읽기 전용 PC 사실 수집 및 승인된 7B의 Windows 메모리/성능 검증이 필요하다. 기존 1.5B와 Supertonic 보존·별도 디렉터리 평가/복구 방식을 명시했다.

## Gate 판정

| Gate | 상태 | 범위 |
|---|---|---|
| General 코드·검사·절차 준비 | PASS | 입력과 무관한 준비 및 로컬/원격 회귀; 아래 외부 Gate는 열지 않음 |
| 소스·변경분 인수 | PASS | fb7 → 병행 41469 → 93a5 → f94 → 903f 계보/파일 readback |
| 실제 자료 접수 | BLOCKED | 영상·권리 확인·BGM·확정 원고·음량·정책 미접수 |
| 모델 identity | PARTIAL | Linux 7B 고정; Windows 새 구성 채택/확보/실측 미완료 |
| 실제 새 Qwen 계획 | PASS | 93a5의 명시 수치 계획·변조 거부 1건; 작품 판단으로 확대 금지 |
| 건축 판단·창작 품질 | PARTIAL | 기존 합성 노출 5종만 인수; 실무 작품은 미검증 |
| 지시 준수·실패 보호 | PASS | 계약/실패 주입/실제 FFmpeg 오류 시험 범위 |
| 30초 실제 자료 체인 | BLOCKED | 실제 새 Qwen→Supertonic→30초 MP4 미실행 |
| 프로세스 재시작·Reopen·Export | PARTIAL | 합성 회귀의 실제 프로세스/내부 해시 검증; Windows 실무 결과 미실행 |
| Windows 최신 후보·UI | NOT_EXECUTED | 새 후보 없음; 기존 R3로 대체 안 함 |
| 화면·한국어 음성 사람 검수 | NOT_EXECUTED | 실무 최종 MP4 없음 |
| 신규 장면 생성 | NOT_IMPLEMENTED | Wan/LTX/Blender 실제 생성 연결 증거 없음 |
| 대표 인수 | BLOCKED | 선행 자료·모델·후보·실무 검수 필요 |
| 전체 제품 | PARTIAL | full_product_pass=false 유지 |

실제 Supertonic 생성/청취 실패와 Windows 7B 전체 메모리·성능을 이번 Linux 회귀만으로 PASS 처리하지 않는다. Skip과 환경 미실행은 그대로 남긴다.

## 전달 위치와 다음 진입

- 단일 자료/승인 접수표: `docs/handoff/media-ai-core-e2e-r2-20261025/INTAKE_AND_APPROVAL_KO.md`
- General 소스·읽기 전용 PC 사양 수집: `EXECUTION_KO.md`
- 승인 후보의 단일 PC 명령/출구 조건: `PC_EXECUTION_KO.md`
- 입력 원본: `INPUT_MANIFEST.json`, 상태: 같은 SHA의 INTAKE_RESULT/ASSET_INTAKE
- 모델 채택 검토: `WINDOWS_7B_ADOPTION_REQUEST.json`

자료가 들어오면 General 소스 E2E를 실행할 수 있다. Windows 소스 평가에는 Windows 7B 격리 승인, 새 제품 후보 제작에는 별도 Build Gate 승인이 필요하다. 준비된 템플릿을 승인으로 간주하지 않는다.

Build Gate=false, PR #23 Draft/HOLD, main 미병합, 배포/예산 변경/설치 모델 교체/새 Windows 후보 제작 없음.

## 최종 동결 소스 회귀·원격 인수

- 코드 **903f892a5dcd79166cc2ffbaa70ddaabf293aaaa**의 Run **40186880120 SUCCESS**. select-checks와 actual-browser가 실제 시작 후 성공했다.
- 로컬 전체 Python **378 PASS / 6 SKIP**, UI **31 PASS**. 원격 전체 Python **379 PASS / 5 SKIP**, 실제 브라우저 **41 PASS**. 환경별 skip을 합산하거나 Windows 실측으로 바꾸지 않았다. Python 구문/JSON 파싱/변경 공백 검사도 통과했다.
- 새 엔진 다운로드/반복 실행을 줄이기 위해, 실행 도구만 변경된 후속 소스에서는 엔진 입력과 workflow job body의 동일성을 확인했다. GitHub API로 검증한 **93a5e80a / Run 40186056871 / job 121147027021 SUCCESS**를 재사용했다. 최신 adopted-real-engines job은 의도된 skipped다. planner/runtime/UI/알 수 없는 입력 변경은 재사용을 무효화한다. CHECK_SELECTION.json에 선택 원본을 보존했다.
- 브라우저 Artifact **12595689748**: SHA-256 `26bf5f49eccdf782ae1c3f506f8dd3bc46d1bd9113d806d77ac0be9b1aec277e`, ZIP CRC, receipt source를 직접 확인했다. 브라우저 receipt의 fresh_model_inference는 false이며 위 실제 7B 계획 probe와 분리한다.
- 선택 Artifact **12595824769**: SHA-256 `91c3bd5388b750da468656bbba1bbb760fe4946bae909e4de288ccf8f0896eae`, ZIP CRC와 재사용 run/source/job을 확인했다.
- 변경 코드/검사/선택 workflow **14개 파일 원격 readback 일치**. SOURCE_VALIDATION.json에 코드 SHA·파일 SHA·UI fingerprint·run/job/artifact·실행 범위를 기록했다.
- Windows build/package job들은 실제로 skipped였다. 상위 workflow의 success를 새 후보 제작 성공으로 보고하지 않았다.
- 이전 f94b 원격 회귀는 F94B_REMOTE_* 이력으로 보존한다. 최종 소스의 실제 빈 입력 probe는 BLOCKED_FINAL_SOURCE/RUN_RECEIPT.json이며 여전히 30초 실무 실행은 차단된다.

후속 증거/문서 커밋은 [skip ci]로 반영하며 코드 903f의 실행 결과를 그 문서 HEAD에서 새로 실행했다고 표시하지 않는다.
