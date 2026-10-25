# MINDLE MEDIA AI 현재 작업 — R2 / 2026-10-25

현재 작업의 원본은 `CURRENT_MEDIA_WORK_STATUS.json`이며, 그 상태는 원본 Manifest와 고정된 검증 소스의 실제 파일에서 다시 계산한다. General 준비 완료와 실제 제작의 실행 가능 여부는 별개다.

- R2 검증 코드: `903f892a5dcd79166cc2ffbaa70ddaabf293aaaa`.
- 검증 증거: `docs/evidence/media-ai-core-e2e-r2-20261025/SOURCE_VALIDATION.json`.
- 현재 입력: `docs/handoff/media-ai-core-e2e-r2-20261025/INPUT_MANIFEST.json`.
- 다음 작업: 실제 영상·BGM·원고·음량·장문 정책을 접수하고 제품 엔진 사전검사를 수행한다.
- 실행 절차/단일 요청표: `docs/handoff/media-ai-core-e2e-r2-20261025/EXECUTION_KO.md`, `INTAKE_AND_APPROVAL_KO.md`, `PC_EXECUTION_KO.md`.

기존 state/lock의 R3 epoch·phase·후보 source·해시·소진된 승인은 과거 후보 보호용 기록으로 보존한다. current_work와 최상위 status가 현재 R2 작업을 가리킨다. 과거 R3의 READY, ACTIVE, Build Gate=true 문구를 R2 실행 권한으로 사용하지 않는다.

```powershell
python scripts/media_work_status.py --check
python scripts/media_work_status.py --preflight
```

check의 exit 0은 관제 표시가 실제 자료/소스와 일치한다는 뜻이다. preflight는 제작 실행 권한을 발급하지 않으며 미실행/차단 상태에서 exit 2다. 입력을 갱신한 뒤:

```powershell
python scripts/media_work_status.py --refresh
python scripts/validate_general_work_control_plane.py
python scripts/validate_pc_work_control_plane.py
```

refresh는 원본 자료와 소스 해시에서 상태를 다시 계산한다. 기존 Build Gate가 열려 있거나 과거 승인이 소진되지 않은 불일치는 덮어쓰지 않고 거부한다. 이 명령은 Qwen/TTS/FFmpeg/서버·PC worker·Actions를 시작하지 않는다. 상태만 바꿔서 완료 또는 승인 상태를 만들 수 없다.

실제 입력이 준비되면 상태는 ENGINE_PREFLIGHT_REQUIRED로 바뀐다. 그때 General 소스 실행기로 모델 identity·정확한 소스를 확인한다. Linux General 소스 평가에 Windows 채택·빌드 승인을 요구하지 않는다. Windows 경로는 별도 승인 범위를 확인한다. 이 상태 문서가 통합 실행기의 검사를 대체하지 않는다.

Build Gate=false / PR #23 Draft/HOLD / main 병합·배포·예산 변경·설치 모델 교체 금지 유지. 실제 PC 프로세스는 관제 파일만으로 확인했다고 보고하지 않는다. background_execution_claimed=false, full_product_pass=false.

검증된 소스/증거는 바이트 기준이다. checkout의 줄바꿈 변환이나 파일 누락도 변경으로 표시한다. 기대 해시를 바꾸거나 자동 보정해 통과시키지 말고 동결 소스의 정확한 bytes를 인수하거나 변경분을 재검증한다.
