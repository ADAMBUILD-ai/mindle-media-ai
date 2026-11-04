# General Work 반환 — 실제 30초 제작 R1

작업 ID: MEDIA-REAL-30S-EXECUTION-R1-20261026. 담당: 이 창의 General Work.

판정: **소스·기존 증거·인계 범위 대조 완료 / 실제 입력 미인수로 제작 BLOCKED**.

## 이번에 확인한 사실

- 원격 HEAD: `3710194effb33862fecf89097ccde8e4ef4c6b7a`, PR #23 Draft·미병합.
- 성공 검사 소스 `1606e67fae51ae889c88e63b05991ca948ada773` 이후 변경은 docs 아래 증거/접수 ZIP 16개다. 코드 변경은 없다. Run 40250290046의 446 PASS/5 SKIP·UI 계약 2 PASS를 그 범위로 재사용했다.
- 현재 R2 원본은 clips=[]·bgm=null·원고/정책/음량=null이다. 실제 자료를 인수한 Manifest가 아니다. 템플릿 SHA를 실제 제작 입력 SHA로 동결하지 않았다.
- 기존 접수 ZIP은 12,671 bytes, SHA-256 `06de65235e01ab992eef0c5f7b2ed6af455123fed4385ff1e7ec4f30586d6bde`인 기존 실물을 그대로 사용한다. 다시 제작하거나 CI를 재실행하지 않았다.
- 기존 source_e2e의 실제 제품 API·7B 두 분할·Supertonic identity·원고/음량/길이·프로세스 재시작·Export 검사 경로를 대조했다. Windows 승인과 EXE Build Gate는 별도다. Linux identity를 Windows runtime으로 쓰지 않는다.

## PC Work의 현재 착수 범위

**자료 확인·접수와 기존 엔진의 읽기 전용 사실 수집만 진행한다.** 새 모델 설치·기본 모델 교체·실제 제작·EXE 제작·대표 인수 완료 판정은 아직 시작하지 않는다.

PC는 기존 [단일 진입 지시서](../../handoff/media-production-closeout-r3-20261026/START_HERE_KO.md)와 [검증된 접수 ZIP](../../handoff/media-production-closeout-r3-20261026/SOURCE_INTAKE_TOOL_ONLY.zip)을 사용한다. 이번 작업에서 새 접수표·새 ZIP·새 시험을 만들지 않는다. 영상·사용 구간·권리·BGM·확정 원고·음량·장문 정책을 OPERATOR_INPUT.json 한 곳에 적고 새 RETURN 폴더로 접수한다.

반환할 것은 INPUT_MANIFEST.json, PREPARATION_RECEIPT.json, INTAKE_RESULT.json과 원본에 실제로 접근할 수 있는 위치다. 엔진 설정 파일이 이미 있다면 기존 collect_media_pc_readiness.py의 읽기 전용 결과도 함께 반환한다. 과거 PC 메모리/설치 상태를 최신 측정값으로 보고하지 않는다. 관련 없는 폴더/NAS 전체 탐색은 하지 않는다.

## General이 반환 후 수행할 일

받은 원본에 접근 가능한 환경에서 파일 SHA·권리 선언·사용 구간·조건을 대조한다. 그때 실제 Manifest SHA와 엔진 구성 SHA를 실행 소스에 결속한다. 소스 평가 기준은 위 reviewed HEAD로 고정하되 실제 checkout HEAD도 일치해야 한다. 다른 HEAD를 쓰면 코드 변경분을 대조하고 새 기준을 기록한다.

인수가 충족되면 기존 소스 E2E 실행기를 사용한다. 별도 시험 전용 영상 처리로 제품 제작을 대신하지 않는다. Qwen 장면 계획 → FFmpeg 조립 → Qwen 음향 계획 → Supertonic → BGM/원음 믹스 → 기술 검사 → 실제 프로세스 재시작/Reopen/Export로 연결한다. 시청·청취는 별도 사람 검수다.

**General 평가·Windows 7B 격리 평가·신규 EXE 제작은 서로 다른 단계다.** 기존 자료 30초 편집에 LTX 설치를 선행 조건으로 추가하지 않는다. Build Gate=false와 PR Draft/HOLD를 유지한다.

실제 Manifest를 아직 받지 않았으므로 영상 제작과 모델 추론은 NOT_EXECUTED다. PC가 실행 중이라고 주장하지 않는다. 기계 반환: GENERAL_WORK_RETURN.json.
