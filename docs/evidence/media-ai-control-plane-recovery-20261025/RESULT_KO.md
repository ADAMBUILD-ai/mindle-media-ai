# MEDIA — 필요한 회귀만 선택한 General Work 인수 검증 복구

판정: **PASS_TARGETED_CONTROL_PLANE_AND_ACTUAL_BROWSER_RECOVERY**

- 실패 기준: `08c5b1b449411f0ffa4e533aa98758bb5b1c65f0`
- 수정·실제 검증 소스: `beb6c8d3afdf1a144d4f7cc218f545d601d439d3`
- 복구 실행: https://github.com/ADAMBUILD-ai/mindle-media-ai/actions/runs/40172265928
- 최종 상태: `completed / success`

## 원인 구분

기존 run `40169533879`는 설치와 FFmpeg 사전검사를 완료한 뒤 `GENERAL_WORK_HANDOFF_MISMATCH_BLOCKED: General Work epoch mismatch`, exit 2로 종료됐다. 예산·작업 미시작 문제가 아니다.

General 검증기는 10월 8일 최종 인계와 10월 13일 복구 세대만 처리했다. 실제 General·PC state/lock과 worker는 10월 24일 R3 원격 검증 완료·사무실 PC 대기 세대에 정렬돼 있었으며, 독립 PC 검증기는 그 계약을 이미 검증하고 있었다. General 검사 경로만 과거 계약으로 되돌아간 것이 원인이다.

## 수정 내용과 보호

- state/lock의 세대값을 과거 값으로 되돌리지 않았다.
- 현재 General directive의 최상단에 활성 R3 세대, 계약 경로, 소진된 제작 승인과 현재 Gate=false를 명시했다. 역사 단락은 보존했다.
- General 검증기가 현재 epoch, 상태, phase, 활성 지시·계약, worker, 승인 UI·병합금지 불변조건을 대조한다.
- 이어서 기존 독립 PC 검증기를 그대로 실행해 4개 state/lock, R3 계약 epoch, 기존 실제 실행·전달 증거의 source/run/ZIP/manifest 및 독립 해시·CRC를 확인한다.
- 과거 R3의 원격 PASS를 사무실 PC·청취·전체 제품 PASS로 올리지 않는다. 소진한 Build Gate는 false다.
- 세대·계약·원본 SHA·ZIP·상태·불변조건의 불일치와 승인 범위 확대를 주입한 실패 시험을 유지한다. Python `-O`에서도 거부한다.
- 제품 `src`와 UI는 이번 수정에서 바뀌지 않았다. 브라우저 하네스 변경은 출력 경로 분리뿐이다.

## 선택 실행 및 기존 성공 인수

기존 `40169533879 / job 121097388617 adopted-real-engines`는 실제 성공했다. API에서 해당 성공 source와 job을 재확인했고, 고정 기준 `08c5b1b4` 이후 변경이 제어면·인수 문서·검사·출력 경로에만 한정되고 엔진 job 본문과 제품 입력이 그대로임을 확인했다.

새 실행의 선택 영수증은 `engine_inputs_unchanged=true`, `run_engines=false`다. 따라서 엔진 작업은 다시 실행하지 않고 `SKIPPED`로 남겼다. 이 인수는 과거 성공 작업의 한정된 범위이며 새 모델 추론 주장이 아니다. runtime/UI/의존성 또는 엔진 job 단계가 바뀌면 자동 재사용하지 않는다.

기존 source의 다른 성공 검사도 보존했다. 과거 실패 run을 일괄 재실행하지 않았다. 새 커밋 때문에 자동으로 생성된 패키지 workflow들은 Gate 검사와 실제 package job을 구분하며, Build Gate=false 때문에 package job은 SKIPPED다.

## 실제 새 실행 증거

| 단계 | 결과 |
|---|---|
| select-checks `121105426235` | PASS — 고정 성공 source·job·입력 대조 |
| actual-browser `121105505140` | 실제 시작 후 최종 SUCCESS |
| General Work 검증 | `GENERAL_WORK_R3_REMOTE_VERIFIED_OWNER_PC_PENDING` |
| 전체 Python 회귀 | **306 PASS / 5 SKIP / 0 FAIL** |
| 지정 UI 회귀·compileall·pip check | PASS |
| 실제 Chrome·FFmpeg 회귀 | **40개 PASS** |
| adopted-real-engines | SKIPPED — 위 고정 성공 결과 재사용 |

40개 브라우저 검사에는 실제 입력·H.264 재생, 측정 기반 자동 편집·사진 보정, 회전·페이드·속도·자르기·한국어 자막·분할·9:16, 사진 7보정·크롭·크기, BGM 1회 합성·후속 중복 방지, 선택한 자료 보존, 서버/브라우저 재시작 후 동일 프로젝트 복원, 내보낸 ZIP CRC·미디어 SHA가 포함된다.

## 산출물 독립 인수

- 새 회귀 Artifact: `12591121023`, SHA-256 `782f7a9ded6811120e3d56f32e2ff1218f6e074298cc92d17382fcf75acfe43b`
- 선택 Artifact: `12590158403`, SHA-256 `c36506e94bc30f4403a6392f3e7c9711e33689f9a9376c45fbcd26b4e96f4331`
- 두 ZIP 다운로드 후 SHA-256·CRC 확인 PASS.
- 새 영수증 `source_commit`은 수정 소스 `beb6c8d3...`와 일치한다. 40개 check가 모두 PASS임을 확인했다.
- workflow 출력은 새 `runtime_recovery_evidence/`에 저장한다. checkout의 역사적 결과 파일을 새 실행 결과로 업로드하지 않는다.
- 원본 영수증: `REMOTE_BROWSER_RUNTIME_RECEIPT.json`; 실제 회귀 로그: `REMOTE_REGRESSION.log`; 제어면 로그: `REMOTE_GENERAL_WORK_GATE.log`; 재사용 결정: `REMOTE_CHECK_SELECTION.json`.

## 남은 Gate

이 복구는 Linux 원격 실제 브라우저·제어면 회귀이며 최신 Windows 후보 제작이나 사무실 PC 인수가 아니다. `fresh_model_inference=false`, 사무실 PC·사람 청취·전체 제품 PASS=false를 유지한다. 기존 R3 후보를 이번 새 코드가 포함된 설치본으로 표시하지 않는다.

PR #23 Draft/HOLD 유지. main 병합·배포·추가 예산 변경·새 Windows 후보 제작을 하지 않았다. 증거만 추가하는 후속 커밋은 `[skip ci]`로 기록해 같은 검사를 다시 실행하지 않는다.
