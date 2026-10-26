# R2 중단 원인 수정·관제 복구 결과

판정: **관제·검사 복구 완료 / 제품 PARTIAL / 실제 30초 E2E BLOCKED**.

검증 소스: `d98db8cd61268b766563b6c426e3c55375570312`. 이 보고서는 그 소스의 증거를 추가하며 제품 런타임을 변경하지 않는다.

## 확인한 원인과 수정

1. 기존 General/PC 관제에 R3 ACTIVE/READY 표시와 현재 R2 자료 차단이 혼재했다. 실제 Manifest와 검증 소스에서 계산한 단일 상태를 만들고 state/lock 5개를 결속했다. 과거 R3 epoch·후보 identity·소진된 승인은 보존했다. 상태 위조·미갱신·소스 변경은 거부한다.
2. 새 Windows 검사는 실제 시작 후 관제 검사에서 실패했다. 예산 차단이 아니다. Windows checkout의 CRLF 변환으로 고정 증거·Manifest·소스 바이트가 달라졌다. 최초 수정의 checkout-index도 충분하지 않아 실패했으며 성공으로 인수하지 않았다.
3. 최종 수정은 일회용 Actions runner에서 Git 원본 archive를 만들고 ls-tree blob 해시와 대조한 뒤 원본 바이트를 인수한다. 기대 해시는 변경하지 않는다. 사용자 로컬에서 CLI 실행은 거부한다. Windows 증거에서 88개 파일 중 69개 바이트 변경을 복원했고, 고정 런타임/UI 59개가 일치했다.
4. R2 상태 변경이 기존 패키지 금지를 우회하지 않도록 3개 패키지 workflow의 Gate를 보강했다. General 입력 준비와 Windows 별도 승인 조건을 구분했다.

## 실제 새 실행 결과

| 검사 | 실행 | 결과 |
|---|---|---|
| Windows 관제·재배포 사전검사·소스 compile | [40199152130](https://github.com/ADAMBUILD-ai/mindle-media-ai/actions/runs/40199152130) | SUCCESS |
| Python·실제 브라우저 회귀 | [40199152150](https://github.com/ADAMBUILD-ai/mindle-media-ai/actions/runs/40199152150) | 402 PASS / 5 SKIP, 브라우저 41 PASS |
| Canonical 관제 | [40199157084](https://github.com/ADAMBUILD-ai/mindle-media-ai/actions/runs/40199157084) | SUCCESS |
| 로컬 Python / UI 계약 | LOCAL_PYTHON.log / LOCAL_UI.log | 401 PASS / 6 SKIP, UI 31 PASS |

실패 기록: `b7a74e7a` / Run `40197924012`, `1d75b914` / Run `40198446453`. 두 실행 모두 모델 실행 전 실제 관제 검사 실패다. 두 번째 시도의 원본 바이트 회귀도 실패해 최종 수정으로 교체했다. 과거 실패를 일괄 재실행하지 않았다.

엔진 입력이 변경되지 않아 `CHECK_SELECTION.json`이 인수한 `93a5e80a` / Run `40186056871` / Job `121147027021`의 성공을 원래 범위로 재사용했다. 이번 브라우저 회귀는 새 모델 추론이 아니다. Windows hosted 사전검사는 대표 PC 실행·청취 증거가 아니다.

Windows OpenVINO `40199157022`, remote package `40199157023`, one-click `40199152132`의 Gate는 성공했고 패키지 작업은 SKIPPED다. 새 Windows EXE·설치 모델 교체는 없다.

## 현재 상태와 다음 실행

- General: `R2_GENERAL_PREPARATION_COMPLETE`.
- PC: `R2_BLOCKED_ASSET_INTAKE`.
- 실제 입력: 건축·리조트 영상과 사용 권한, 음악과 사용 조건, 한국어 확정 원고, 나레이션·원본음·BGM 음량, 장문 정책이 미접수다.
- 실제 30초 제작·새 추론·대표 PC 콜드 재시작·Reopen·Export·화면/청취 인수는 이번 변경에서 실행하지 않았다.
- PC 프로세스 현재 상태는 `NOT_OBSERVED`다. 실행 중이라고 주장하지 않는다.

제출 위치와 단일 접수표: [SUBMISSION_FORM_KO.md](../../handoff/media-ai-core-e2e-r2-20261025/SUBMISSION_FORM_KO.md). 원본 Manifest: [INPUT_MANIFEST.json](../../handoff/media-ai-core-e2e-r2-20261025/INPUT_MANIFEST.json).

접수 후 `python scripts/media_work_status.py --refresh` → General/PC validator → [General 실행 절차](../../handoff/media-ai-core-e2e-r2-20261025/EXECUTION_KO.md)의 모델 identity 사전검사 및 제품 API 실행 순으로 진행한다. 입력 준비만으로 제작 허가나 완료를 부여하지 않는다. Linux General 평가에는 Windows 승인을 요구하지 않는다. Windows는 [채택·승인 요청표](../../handoff/media-ai-core-e2e-r2-20261025/INTAKE_AND_APPROVAL_KO.md)의 범위를 확인한 뒤 [PC 절차](../../handoff/media-ai-core-e2e-r2-20261025/PC_EXECUTION_KO.md)를 따른다.

Build Gate=false, PR #23 Draft/HOLD·미병합 유지. 전체 제품 PASS·대표 인수는 부여하지 않는다. main 병합·배포·예산 변경은 하지 않았다.

기계 판정·변경 22개 파일·원격 Artifact SHA는 [SOURCE_VALIDATION.json](SOURCE_VALIDATION.json), 파일별 증거 해시는 `EVIDENCE_FILES.json`에 있다. 원격 Artifact 3개는 다운로드 후 SHA-256 및 ZIP CRC를 확인했다.
