# General 소스 실행·PC 인계 절차

현재 Build Gate=false, PR #23 Draft/HOLD. 실행기는 제품의 기존 HTTP API를 사용하며 EXE 제작·모델 다운로드·설치 교체를 하지 않는다. 최종 소스 SHA는 RESULT_KO.md/실행 승인본의 값을 사용한다.

## 1. 입력 검증 (실행 프로세스 없음)

```powershell
$env:PYTHONPATH = "src"
python -m media_ai.e2e_intake docs/handoff/media-ai-core-e2e-r2-20261025/INPUT_MANIFEST.json --output evidence-r2/INTAKE_RESULT.json --status-output docs/handoff/media-ai-core-e2e-r2-20261025/ASSET_INTAKE.json
```

빈 입력·해시 변경·권리 근거 누락·길이 부족 시 exit 2, BLOCKED_ASSET_INTAKE다. 출력 상태 문서의 SHA가 원본과 다르면 재생성한다. 현재 빈 접수표를 실행하면 차단되는 것이 정상이다.

## 2. 대상 PC 읽기 전용 사실 수집

```powershell
python scripts/collect_media_pc_readiness.py --engine-config "[실제 확인할 runtime-engines.json 경로]" --disk-path "[격리 작업 드라이브의 기존 경로]" --output evidence-r2/PC_READINESS.json
```

가중치·실행기 파일 해시를 읽고 RAM/디스크를 기록한다. 설치·변경·채택은 하지 않는다. `is_windows_target=true`인 실제 대상 PC 기록을 받아야 한다. Windows 7B/runtime 검증은 모델 채택 요청 JSON의 미확인 항목을 이 결과 및 격리 평가로 채운다.

## 3. 입력/엔진 사전검사

```powershell
python -m media_ai.source_e2e --manifest docs/handoff/media-ai-core-e2e-r2-20261025/INPUT_MANIFEST.json --engine-config "[고정된 별도 엔진 설정 JSON]" --output "[새 사전검사 디렉터리]"
```

출력 폴더는 새 경로여야 한다. 과거 출력 재사용 금지. relative engine 경로는 설정 JSON 디렉터리 기준으로 해석한다. 모델 2분할·실행기·runtime·context·Supertonic identity를 확인하고, 추론 전 준비 상태까지만 기록한다. 1.5B/eSpeak/일반 필터로 대체하지 않는다.

## 4. General 소스 환경 실제 E2E

실제 자료를 인수하고 고정한 엔진 구성이 있는 환경에서만 실행한다. 기존 소스 환경이며 새 Windows 패키지 제작이 아니다.

```powershell
python -m media_ai.source_e2e --manifest docs/handoff/media-ai-core-e2e-r2-20261025/INPUT_MANIFEST.json --engine-config "[고정 엔진 JSON]" --source-sha "[동결 코드 HEAD 전체 SHA]" --execute --output "[새 실제 실행 증거 디렉터리]"
```

Windows에서는 별도로 승인받은 `--windows-approval "[승인 JSON]"`을 추가한다. approved=true만으로 통과하지 않고 소스/Manifest/설정 SHA와 ISOLATED_SOURCE_ONLY 범위를 대조한다. 승인 없이 템플릿을 true로 바꾸지 않는다. Linux General 평가에는 Windows 승인 파일을 요구하지 않는다.

실행 경로:

1. Manifest와 실제 파일 재검사
2. pinned 7B와 Supertonic 사전검사
3. `/api/media/import`, 제한 구간이 있으면 `/api/video-edits`
4. `/api/architecture-agent/plan` → `/api/architecture-agent/productions`
5. `/api/workflows/plan`으로 정확한 원고·음량·정책의 새 Qwen 계획
6. `/api/workflows`에서 Supertonic 1회·BGM/원음 단일 믹스
7. 30초·16:9·H264/AAC·전체 영상/오디오 디코딩 검사
8. `/api/projects/{id}`로 저장 결과 확인
9. nonce/PID/instance에 결속한 `/api/runtime/shutdown` → 소유 자식 프로세스의 정상 종료 확인
10. 같은 isolated data로 새 프로세스 시작 → 새 PID/instance 확인 → Reopen
11. `/api/projects/{id}/export` 다운로드 → ZIP SHA/CRC·내부 Manifest 모든 파일 SHA/bytes·저장 작업 정보 검사

명시 수치·원고를 바꾼 계획은 거부한다. 30초 초과 결과는 고정 30초 PASS가 아니다. 실패 시 전체 receipt는 FAILED/BLOCKED이며 뒤 단계는 NOT_EXECUTED로 남는다. 부분 성공 조립물·기존 프로젝트는 지우지 않는다. 취소는 새 격리 작업의 ID만 사용하고 타인 프로세스/기존 제품은 종료하지 않는다.

`PASS_SOURCE_TECHNICAL_ONLY`도 전체 제품 PASS가 아니다. 원본 분석은 수치 측정이고 사용자 label은 제공자 설명이다. 건축 의미 이해·신규 장면 생성·미학/스토리 품질을 입증하지 않는다.

## 5. 출력과 PC 최종 검수 경계

- RUN_RECEIPT.json: 최초 차단/실패·단계 상태·소스/입력 identity
- INTAKE_RESULT.json / ASSET_INTAKE.json: 동일 원본 SHA의 접수 결과
- ENGINE_IDENTITY.json / SOURCE_RUNTIME_IDENTITY.json: 엔진·소스·UI fingerprint
- ACTUAL_SCENE_PLAN.json / ACTUAL_ASSEMBLY.json / ACTUAL_AUDIO_PLAN.json / ACTUAL_AUDIO_WORKFLOW.json
- isolated-product-data/architecture-agent 및 workflows 아래 실제 prompt/response·실패 원문·MP4·음성·프로젝트
- FIRST_SOURCE_SERVER.log / COLD_SOURCE_SERVER.log, AFTER_COLD_RESTART_EXPORT.zip

소스 실행기는 Python 제품 서버의 기술 검증이다. 최종 Windows EXE/브라우저 화면/재생/청취 인수를 대신하지 않는다. 신규 후보 승인 뒤에는 그 후보의 공식 lifecycle·정확한 패키지 identity와 최신 동결 소스를 확인하고 사람 검수를 별도 수행한다. 신규 후보가 아직 없으므로 이 문서에서 오래된 R3 명령이나 임의 EXE 경로를 제시하지 않는다.

General 준비 완료와 실제 실무 결과 완료를 별도 Gate로 기록한다. 원격 CI·Linux 소스·Windows 후보·대표 인수의 수치를 합산하지 않는다.

## SHA 적용 기준

검증 코드는 `903f892a5dcd79166cc2ffbaa70ddaabf293aaaa`다. 실행할 때 --source-sha는 실제 checkout의 Git HEAD와 같아야 하며 src/UI가 수정된 상태이면 차단한다. 후속 문서 전용 HEAD를 사용하면 차이와 실제 동결 SHA를 먼저 기록한다. 이전 SHA의 CI를 새 HEAD 전체 성공으로 바꾸지 않는다. Windows 후보는 실제 PACKAGE_MANIFEST.build_commit과 승인 파일의 source_sha가 같아야 한다.
