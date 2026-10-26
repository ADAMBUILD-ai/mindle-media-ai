# MEDIA 마무리 인계 R3 결과

2026-10-26 KST. **접수 도구·전달 실물 검증 완료 / 전체 제품 PARTIAL / 실제 30초 제작 BLOCKED**.

## 실제로 마무리한 범위

1. 파일 경로·권리·원고·음량·장문 정책을 한 OPERATOR_INPUT.json으로 접수한다. 새 도구가 파일 SHA-256·bytes·해상도·길이를 측정하고 기존 media_ai.e2e_intake로 검사한다.
2. 사용자 선언의 잘못된 해시·수치·출력 비율을 자동으로 고치지 않는다. 누락은 누락으로 남긴다. null 장면 설명을 문자열 'None'으로 받아들이지 않는다. 원본 입력 스냅샷을 보존한다.
3. 새 출력 폴더만 허용하며 기존 자료·프로젝트·승인·기본 모델을 바꾸지 않는다. 이 도구는 제작·모델·서버를 시작하지 않는다.
4. 설치·모델·EXE가 없는 SOURCE_INTAKE_TOOL_ONLY.zip을 제작하고, 별도 폴더에 풀어 실제 일반 Python 프로세스로 실행했다. Python 외 추가 패키지 설치 없이 import/차단 결과를 확인했다. 이 ZIP은 Windows 제품 후보가 아니다.
5. 단일 START_HERE_KO.md에 자료 담당·General·PC의 절차와 출구 조건을 연결했다. PC가 자료 위치와 해시를 다시 조사할 필요를 줄였다.

## 검증과 소스

- 검증 소스: `1606e67fae51ae889c88e63b05991ca948ada773`.
- 신규 접수 계약시험: 13 PASS. 앞선 LTX 계약과 함께 실행한 검사: 43 PASS(접수 12개 시점). 이후 추가한 null 설명 회귀를 포함한 최종 전체 검사는 아래 원격 결과로 확인했다.
- [Canonical Run 40250290046](https://github.com/ADAMBUILD-ai/mindle-media-ai/actions/runs/40250290046), Job 121340477284: **446 PASS / 5 SKIP**, UI 계약 2 PASS, SUCCESS.
- [Windows 사전검사 40250285456](https://github.com/ADAMBUILD-ai/mindle-media-ai/actions/runs/40250285456): SUCCESS. 기존 관제/compile의 hosted 검사이며 대표 PC 실행 증거가 아니다.
- package/one-click/OpenVINO Gate는 성공했고 실제 패키지 작업은 SKIPPED다. 과거 실패 일괄 재실행 없음.
- 코어·UI 59개 bytes 일치 유지. 설치 모델·기존 패키지·UI 변경 없음.

## 전달할 실물

[SOURCE_INTAKE_TOOL_ONLY.zip](../../handoff/media-production-closeout-r3-20261026/SOURCE_INTAKE_TOOL_ONLY.zip)

- Bytes: 12,671
- SHA-256: `06de65235e01ab992eef0c5f7b2ed6af455123fed4385ff1e7ec4f30586d6bde`
- 내부 파일 10개·ZIP CRC·내부 SHA 전부 PASS.
- 단독 실행: exit 2 / BLOCKED_ASSET_INTAKE. 빈 자료를 완료로 게시하지 않는 정상 차단이다.
- 실행 확인: SOURCE_KIT_VERIFICATION.json.
- [단일 진입 지시서](../../handoff/media-production-closeout-r3-20261026/START_HERE_KO.md).

## 실제로 남은 일 — 한 번에 반환

| 담당 | 필요한 반환 | 충족 후 동작 |
|---|---|---|
| 대표/자료 담당 | ZIP의 OPERATOR_INPUT.json에 실제 영상·BGM 경로와 권리 근거·한국어 확정 원고·음량·장문 정책 | 같은 PC/NAS 접근 환경에서 접수 도구 실행 |
| PC/자료 담당 | 새 RETURN 폴더의 INPUT_MANIFEST.json·PREPARATION_RECEIPT.json·INTAKE_RESULT.json과 실제 원본 접근 위치 | General이 해당 원본 SHA와 고정 엔진을 결속 |
| 엔진 담당 | 7B 두 분할·실행기/runtime·Supertonic identity와 실제 대상 사양 | 기존 source_e2e의 사전검사 후 승인 범위 내 실제 제작 |
| 대표/검수자 | 실행 경로에 필요한 Windows 격리 승인, 최종 화면·한국어 음성 검수 | 기술 검사와 분리한 최종 인수 |

기존 자료 편집에는 LTX 설치를 선행 조건으로 강제하지 않는다. LTX는 신규 장면 생성의 별도 평가 경로다. Linux 소스 평가에 Windows 빌드 승인을 요구하지 않는다. Windows 신규 후보가 필요하면 그때 별도 Build Gate 승인을 받는다.

현재 컨테이너에서는 nvidia-smi/장치가 관측되지 않았다. 이는 대표 PC의 GPU 판정이 아니다. GPU_OBSERVATION.json과 GENERAL_HOST_FACTS.json은 General 환경 관측이다. 대표 PC를 직접 검사하거나 모델을 새로 추론했다고 보고하지 않는다.

현재 빈 접수 도구 실행 결과는 CURRENT_INTAKE 아래에 보존했다. 이 측정용 Manifest가 기존 제품의 R2 원본을 덮어쓰지는 않는다. 실제 새 실행은 접수 후 동결한 새 Manifest 경로를 명시해야 한다.

Build Gate=false / PR #23 Draft/HOLD / main 미병합 / 배포·예산 변경 없음. 파일 생성·CI 성공·접수 ZIP 검증을 실제 30초 작품 완성으로 올리지 않는다.
