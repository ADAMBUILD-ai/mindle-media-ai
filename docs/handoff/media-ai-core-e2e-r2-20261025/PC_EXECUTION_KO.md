# PC Work 단일 실행 절차

작업 ID: `MEDIA-AI-CORE-E2E-R2-20261025`  
현재 상태: **착수 조건 미충족 / 실행 금지**

## 선행 Gate

아래 네 항목이 모두 충족된 뒤에만 실행한다.

1. `INTAKE_RESULT.json`이 `PASS_INTAKE_TECHNICAL_ONLY`이고 대표의 권리 확인이 별도로 완료됨.
2. General Work가 전달한 source SHA와 후보의 `/api/runtime-identity.build_commit`이 같음.
3. Windows 7B 격리 채택 승인 ID, 검증된 Windows 실행기 SHA, runtime tree SHA가 기록됨.
4. 최신 후보가 필요하면 별도의 Build Gate 승인 ID가 기록됨.

현재는 실제 영상·BGM·원고·음량이 없고 Windows 7B와 Build Gate도 승인되지 않았으므로 이 명령을 실행하지 않는다. 승인 후 `APPROVED_*` 자리만 승인 자료의 실제 값으로 바꾸어 한 줄로 실행한다.

```powershell
$env:PYTHONPATH='src'; python scripts/run_real_architecture_acceptance.py docs/handoff/media-ai-core-e2e-r2-20261025/INPUT_MANIFEST.json --evidence-root C:\MINDLE_EVIDENCE\MEDIA-AI-CORE-E2E-R2-PC-실행시각 --expected-source APPROVED_SOURCE_SHA --exe C:\APPROVED_CANDIDATE\MINDLE_MEDIA_AI_RUN.exe --task-timeout 900
```

이 실행기는 제품 HTTP API만 사용하며 순서는 접수 검사 → 후보 identity → 실제 영상 import → Qwen 계획 → 건축 영상 조립 → Supertonic 음성 및 단일 오디오 합성 → H.264/yuv420p/AAC/30초 검사 → 정상 종료 → 새 PID/instance 재실행 → Reopen → Export ZIP SHA/CRC이다. 기존 설치 모델을 바꾸거나 패키지를 만들지 않는다.

## 출구 조건

- exit 2: `BLOCKED_ASSET_INTAKE`. 서버·Qwen·FFmpeg·Supertonic·저장·Export는 실행하지 않는다.
- exit 1: 단계 실패. `RESULT.json`의 원문 오류와 성공한 중간 산출물을 보존한다.
- exit 0: 기술 E2E만 통과. `TECHNICAL_E2E_PASS_HUMAN_ACCEPTANCE_REQUIRED`이며 전체 제품 PASS가 아니다.

exit 0 뒤 별도로 같은 MP4 SHA를 대상으로 화면·구도·스토리·자막·재생/탐색과 한국어 음성 실제 청취를 사람이 기록해야 한다. 사람 검수 전 `human_visual`과 `human_hearing`은 `NOT_EXECUTED`로 유지한다.

증거는 `00_INTAKE_RESULT.json`, `02_RUNTIME_IDENTITY.json`, `03_ARCHITECTURE_PLAN.json`, `04_ARCHITECTURE_PRODUCTION.json`, `05_AUDIO_PLAN.json`, `06_AUDIO_WORKFLOW.json`, `07_FINAL_MEDIA.json`, `08_COLD_RELAUNCH.log`, `09_AFTER_RESTART_EXPORT.zip`, `RESULT.json`으로 연결된다.
