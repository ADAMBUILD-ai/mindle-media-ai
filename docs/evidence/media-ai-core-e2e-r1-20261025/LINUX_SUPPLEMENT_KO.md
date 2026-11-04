# AI 코어 실무 인수 준비 결과 — MEDIA-AI-CORE-E2E-R1-20261025

**판정: 소스 보강과 격리 합성 입력 평가 완료. 실제 30초 건축 영상 통합 실행은 BLOCKED_ASSET_INTAKE. 전체 제품 인수 미완료.**

## 후속 Windows 보고서 인수

원격 HEAD `5a9d3b46985c7556be20d52b3b8fc932e23d2419`의 기존 `RESULT_KO.md`와 `ASSET_INTAKE.json`을 보존한다. 이 후속 커밋은 제품 코드/UI/모델 변경 없이 Windows CP949 읽기와 대소문자 비구분 파일시스템 테스트 fixture를 수정했다. Windows 집중 회귀 **66 PASS / 1 SKIP**은 해당 보고 범위로 인수한다. 같은 최신 HEAD의 두 수정 테스트 파일을 Linux에서 확인한 별도 집중 실행은 **68 PASS / 1 SKIP**이며 Windows 실측 수치와 합치지 않는다.

이 문서는 별도 Linux 격리 평가와 원격 CI 증거를 추가하며 **PARTIAL / 30초 실무 E2E BLOCKED** 판정을 유지한다.

## 소스와 보강

- 지시 인수 HEAD: `410ba721eac23e118a4b4ff7938dd44501118591` — 작업 시작 시 원격 동일 확인.
- 보강 코드: `19d9cd562735e32b460d4b08278fd2bea9faa7a9` — 변경 소스·검사 7개 파일 원격 readback 일치.
- 건축 Qwen 계획의 합계 길이가 요청과 달라도 비례 배분으로 수정하던 경로를 제거했다. 이제 모델의 길이 변경을 거부하고 prompt/response/REJECTED 기록을 보존한다. 코드가 모델의 잘못된 답을 대신 고치지 않는다.
- 제출 시 원래 요청 SHA·실제 응답 원문·현재 입력 SHA와 저장된 장면/비율을 재검증한다. 유효 응답의 해시만 남긴 채 조립 계획을 바꾸는 시도는 등록 전에 차단한다. 기존 계획은 새 요청 결속 정보가 필요하다.
- 자동 편집의 정상 노출을 과소/과다 노출로 악화시키는 출력도 완료 게시 전에 거부한다. 합성/실행 성공과 결과 품질을 분리한다.
- 실제 자료 인수기와 미등록 Manifest, PC 인계 조건을 준비했다. 이 인수기는 자료를 다운로드하거나 새 후보를 제작하지 않는다.

## 실제 Qwen 7B 격리 재추론

새로운 요청 5건으로 실제 고정 가중치·실행기를 실행하고 FFmpeg MP4, 기술 검사, 저장 후 service 객체 재생성·재열기·Export를 수행했다. Mock 응답을 사용하지 않았다.

| 합성 입력 (각 2초) | Qwen 밝기 판단 | 원본 평균 노출 | 실제 출력 평균 노출 | 결과 |
|---|---:|---:|---:|---|
| 어두움 | +8 | 31 | 54 | 노출 오차 49→26 |
| 밝음 | -4 | 223 | 210 | 노출 오차 47→34 |
| 정상 노출 | 0 | 128 | 128 | 유지 |
| 움직이는 testsrc2 | 0 | 105.72795 | 105.70260 | 정상 범위 유지 |
| 첫 프레임 고정 testsrc2 | 0 | 104.2987 | 104.3253 | 정상 범위 유지 |

5건 모두 기술 검수와 프로젝트 재열기·Export PASS. 프로젝트 Export ZIP 5개 CRC PASS. 이는 수치에 따른 노출 판단의 입력 민감성과 보존 동작 증거다. 움직임/정적 입력에서 동일 노출 유지가 적절하므로 억지로 다른 보정값을 요구하지 않았다. **긴 영상의 구간 선택, 건축 의미 이해, 스토리/미학/음성 품질, 프로세스 콜드 재시작은 이 시험으로 증명하지 않았다.**

각 폴더에 실제 prompt/response/계획/작업 기록/input.mp4/output.mp4/PROJECT_EXPORT.zip을 보존했다. `REAL_INFERENCE_RECEIPT.json`의 관측 Git HEAD는 커밋 전 HEAD 그대로 유지한다. `SOURCE_BINDING.json`에서 실행 시 기록한 런타임·UI 54개 파일의 SHA가 보강 코드와 모두 일치함을 확인한다. 신규 intake 모듈은 이 자동 편집 평가에서 호출하지 않았다.

## 모델 identity와 실행 조건

- 모델: Qwen/Qwen2.5-7B-Instruct-GGUF, Apache-2.0.
- revision: `bb5d59e06d9551d752d08b292a50eb208b07ab1f`.
- 분할 1 SHA: `dfce12e3862a5283ccfb88221b48480e58745165de856439950d0f22590580db`.
- 분할 2 SHA: `539cf93f78e887edea1c04e2d7d8cdaca9d01dae9c9025bcb8accbe29df3d72a`.
- 실행기 SHA: `7119bef261611b26f326f7c4da4dc3fdeb7bb28e2faf1ec392bda7b21215ef52`.
- runtime tree SHA: `2fe617a6b6e10211303ea1db242c54cb1eb8d92e2dcdf497ad93c5214846f5e3`.
- Linux CPU, 2 threads, context 4096, temperature 0. 두 가중치와 실행기/runtime은 추론 전 기존 검증 경로로 확인한다.
- `RESOURCE_SAMPLE.json`: 실행 중 관측 RSS 약 7.18 GiB, 해당 프로세스 관측 HWM 약 7.48 GiB. 전체 5회 최고치나 Windows 최소 메모리 요건은 아니다. Windows 성능·메모리 채택 시험은 별도다.
- 기존 설치본/기본 모델을 교체하지 않았다. 1.5B 자동 판단 실패 기록은 보존하며 이번 7B 결과로 덮지 않는다.

## 회귀와 실제 자료 인수

로컬 Python **337 PASS / 6 SKIP**, UI **31 PASS**, Python 구문 검사 PASS. 모델 길이 불일치 거부/원문 보존, 응답-계획 변조, 정상 노출 악화 거부, 입력 해시·권한 선언·길이·해상도·음량·BGM 누락 실패를 포함한다. Skip은 미실행이며 통과로 승격하지 않는다.

`docs/handoff/media-ai-core-e2e-r1-20261025/INPUT_MANIFEST.json`에는 실제 촬영 영상·BGM·확정 원고·음량이 등록되지 않았다. 실행한 인수기 결과는 **exit 2 / BLOCKED_ASSET_INTAKE**다. 기존 Wikimedia 건축 사진은 별도 소스 평가 자료이며 실제 소유자 영상 인수의 대체물이 아니다. 자료 부재를 이유로 합성 회색 MP4를 실무 30초 납품으로 바꾸지 않았다.

## Gate 판정

| Gate | 판정 | 범위/남은 조건 |
|---|---|---|
| 소스 identity | PASS | 원격 7개 파일 readback, 추론 런타임/UI SHA 결속 |
| 모델 identity | PASS | 격리 Linux 7B 2분할+실행기+runtime |
| 실제 추론 | PASS | 새 5건 원문과 해시; 실제 건축/음성 재추론은 별도 |
| 입력 결속 | PASS | 합성 5건; 실제 촬영 자료는 미인수 |
| 판단 적합성 | PARTIAL | 노출 반대 판단·정상 유지; 건축 의미/긴 구간 선택 미검증 |
| 지시 준수 | PARTIAL | 계약·실패 주입 회귀 통과, 실제 30초 원고/음량 E2E 미실행 |
| 실제 실행 | PARTIAL | Qwen→FFmpeg 5건; 신규 Supertonic 통합 실행 NOT_EXECUTED |
| 결과 검수 | PARTIAL | 5건 기술 검사; 건축 작품 재생/화면/청취 미실행 |
| 실패 보호 | PASS | 소스 회귀 범위; 최신 Windows 인수로 확대 금지 |
| 영속성 | PARTIAL | service 객체 재생성·재열기·Export; 프로세스 콜드 재시작 미실행 |
| 실제 자료 인수 | BLOCKED | 영상·사용 권한 확인·BGM·원고·음량 필요 |
| 실무 품질 | NOT_EXECUTED | 장면·구도·스토리·자막·한국어 음성 사람 검수 필요 |
| 대표 인수 | NOT_EXECUTED | 실제 최종 결과물 대기 |
| 신규 장면 생성 | NOT_IMPLEMENTED | Wan/LTX/Blender 실행 증거 없음 |
| Windows 최신 후보 | BLOCKED | Build Gate=false; 별도 승인 전 제작 금지 |

## 다음 실행에 필요한 자료

실제 촬영 영상 파일/경로와 장면 라벨, 출처·사용 권한 확인, 사용할 BGM과 조건, 확정 한국어 원고, 나레이션·원본·BGM 음량이 필요하다. Manifest 인수 뒤 동일 동결 소스에서 30초 16:9 연속 제작을 실행한다. 음성 초과는 기본 reject로 종료하고 중간 영상/기존 프로젝트를 보존한다. 인계 실행 명령과 PC 착수 조건은 `PC_HANDOFF_KO.md`에 기록했다.

Build Gate=false, PR #23 Draft/HOLD, 미병합 유지. main 병합·배포·예산 변경·새 Windows 후보 제작·설치 모델 교체 없음. 과거 실패 일괄 재실행 없음.

## 새 원격 회귀 증거

코드 `19d9cd562735e32b460d4b08278fd2bea9faa7a9`의 Run **40180334294 SUCCESS**를 확인했다. select-checks, actual-browser, adopted-real-engines가 모두 실제 시작 후 성공했다. 원격 Python **338 PASS / 5 SKIP**, 실제 브라우저 **41 PASS**. 해당 브라우저 receipt는 `fresh_model_inference=false`이며 위 로컬 Qwen 5건의 추론 증거와 구분한다. 제품 코드가 바뀌어 엔진 회귀는 재실행됐고, 과거 실패는 재실행하지 않았다.

브라우저 Artifact **12593523274** ZIP을 직접 내려받아 SHA-256 `81ee66232a3f63943f1e400f7462ec315a6b017489b70d329c0ba23babfddb68`, ZIP CRC, receipt source_commit을 검증했다. 상세 job/산출물/선택 근거는 `REMOTE_VALIDATION.json`, 브라우저 원본은 `REMOTE_RUNTIME_RECEIPT.json`, Python 로그는 `REMOTE_REGRESSION.log`다.

후속 `5a9d3b46` 변경은 문서 2개/테스트 2개이며 제품 실행 소스가 동일하다. 이전 CI 수치를 최신 HEAD 전체 CI 성공이라고 바꾸지 않고 원래 실행 SHA와 연결한다. 테스트 수정은 최신 HEAD 집중 회귀로 별도 확인했다. 새 문서 증거는 [skip ci]로 반영해 불필요한 빌드를 만들지 않는다. 패키지 workflow의 실제 제작 job들은 skipped였음을 별도 확인했다.
