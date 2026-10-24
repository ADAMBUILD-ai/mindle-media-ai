# R3 사무실 PC 인수 키트 결과

## 판정

`READY_NOT_EXECUTED_ON_OWNER_PC`

기존 R3 후보를 그대로 사용하는 더블클릭 인수 실행기를 구현했다. 새 후보를 만들거나 모델을 다시 내려받지 않는다.

## 고정 후보

| 항목 | 값 |
|---|---|
| 후보 | `MINDLE_MEDIA_AI_PC_TEST_20261024_R3` |
| 소스 | `9f5d304ce825ad622bcd64df6ad3c8f154dfd3b6` |
| ZIP SHA-256 | `e6e05a2b74f806095a6afce13e3af46ddc586870917908250426f215cff1bbe1` |
| EXE SHA-256 | `701654240d8f2795957f78f7d1cc9d7fd23d3195f49a0d39ede1d8b8a3a915a5` |
| manifest SHA-256 | `ec2b82e15eba653a977ce9ddfcf1fb0b697d2bd701c8a7e65aa37f51b68652ca` |
| runtime ID | `9f5d304ce825-0f8cc3c5d320-ai-r3` |
| manifest 파일 | 19,341 |

## 구현 범위

- `scripts/START_R3_OWNER_PC_ACCEPTANCE.cmd`: 더블클릭 진입점
- `scripts/accept_r3_on_owner_pc.ps1`: identity·전체 payload·runtime·저장/재시작/복원·MP4·사람 판정 증거 수집
- `tests/test_owner_pc_r3_acceptance_kit.py`: exact candidate와 안전한 소유 서버 종료 계약 회귀
- `docs/handoff/MINDLE_MEDIA_AI_R3_OWNER_PC_ACCEPTANCE_KIT_20261024.zip`: 위 두 실행 파일과 한국어 안내를 묶은 단일 다운로드 파일. SHA-256 `9c058c27669f9ea2141903f477b9dac8c201f2e7501fc5944b1379b9f55fdda8`, ZIP CRC PASS

실행기는 일반 프로세스 강제 종료를 쓰지 않는다. 제품의 `/api/runtime/control`에서 받은 PID·server instance·control nonce를 `/api/runtime/shutdown`에 제출하고 endpoint가 실제 닫힌 뒤 같은 EXE를 다시 실행한다.

## 기존 실증과의 관계

원격 Windows 실행 `40079944004`에서 실제 Qwen 2.5 1.5B 계획, Supertonic 3 한국어 신경망 TTS, 건축 영상 agent, Chrome MP4 재생, 서버 완전 종료·새 PID·프로젝트 복원·Export는 PASS했다. 이번 키트는 그 결과를 사무실 PC 인수로 확대하기 위한 도구다.

R3 이후의 UI 시각 보강 소스 커밋 `e5638b46323559bc6710d89d439c9d7854e21ca5`는 R3 패키지에 포함되지 않는다. 따라서 사무실 PC 인수 결과와 최신 UI 소스 결과를 혼합하지 않는다.

## 아직 실제로 남은 항목

1. 사무실 PC에서 이 키트를 실제 실행해 생성한 원본 폴더와 ZIP 회수
2. 설치 Windows 플레이어의 영상 표시·재생·탐색 확인
3. 사람이 실제 한국어 나레이션과 오디오를 들은 결과
4. 1536×1024·100% 기준 승인 UI 픽셀 최종 판정

이 네 항목이 없으므로 전체 제품 PASS 문자열은 발행하지 않는다. Build Gate=false와 PR #23 HOLD / DO NOT MERGE를 유지한다.
