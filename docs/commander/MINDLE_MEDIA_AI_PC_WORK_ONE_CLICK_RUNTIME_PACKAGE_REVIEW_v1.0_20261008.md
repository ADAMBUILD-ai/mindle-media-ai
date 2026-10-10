# MINDLE MEDIA AI PC Work 원클릭 구동 패키지 — 사전 점검

기준일: 2026-10-08

판정: `BLOCKED_RUNTIME_REDISTRIBUTION_OR_DEPENDENCY`

이번 작업의 목표는 `MINDLE_MEDIA_AI_RUN.exe` 더블클릭 한 번으로 내부 준비, 서버 실행, 상태 확인 및 승인 UI 자동 열기를 수행하는 원클릭 패키지입니다. 기존 수동 ZIP 해제/설치 방식은 정상 직원 경로에서 제외합니다. 아직 새 실행 파일을 제작하거나 Windows E2E PASS를 얻지 못했습니다.

## 확인한 기준

활성 원격 HEAD: `4c2f5da208717a48458f8369c56c6f0452c29c33`.
General Work 고정 기준: `9f0bdaf7b8c3c9f7c8ea7df5b132dceb4199ddbb`.
새 지시서·Evidence Contract·인계서를 전문 확인하고, CURRENT 지시서 → Control Plane lock → state → worker lock → validator 순으로 읽었습니다. 이후 동일 immutable HEAD에서 6개 제어 파일을 재확인했습니다. Epoch와 인계 PASS 필드는 일치합니다. 실제 로컬 validator는 실행되지 않았으므로 `PC_WORK_CONTROL_PLANE_PASS`를 주장하지 않습니다. General Work의 77/2/75 결과는 이전 기준 증거이며 새로운 PC Work 시험 결과가 아닙니다.

## 실제 진행을 막는 항목

PC 실행 도구가 `Failed to create unified exec process: helper_unknown_error: setup refresh had errors`를 반환했습니다. PowerShell 읽기 및 Get-Location 요청도 결과를 받지 못해 취소했습니다. 따라서 현재 Windows 파일/프로필·런타임을 재조사하거나 컴파일·빌드·더블클릭 E2E를 실행할 수 없습니다. 이 오류를 파일 쓰기 권한 거부나 자동 승인 심사의 거부로 바꾸어 설명하지 않습니다.

기존 R2 실측에서는 `msvcp140.dll`, `vcruntime140_threads.dll`, `msvcp140_atomic_wait.dll`이 System32에서 로드됐습니다. 소유자는 Visual Studio 재배포 권한을 아직 확인하지 못했다고 답했습니다. 새 지시서 4절의 재배포 근거 요구에 따라 해당 DLL/설치기를 임의 포함하지 않았습니다. Microsoft 공식 재배포 문서도 적용 라이선스 확인을 요구합니다. 기존 FFmpeg의 정적 의존성 전체 소스 제공 조건 역시 R2 증거에서 닫히지 않았습니다. 이것은 현재 새 패키지의 DLL inventory를 수행했다는 뜻이 아니며, 새 General Work 제품 PASS를 라이선스 마감으로 간주하지 않습니다.

근거: [Microsoft VC 파일 재배포](https://learn.microsoft.com/en-us/cpp/windows/redistributing-visual-cpp-files?view=msvc-170), [기존 R2 검증](MINDLE_MEDIA_AI_EMPLOYEE_PACKAGE_FINAL_CLOSEOUT_R2_REVIEW_v1.0_20261007.md).

## 저장한 작업과 다음 실행 조건

정확한 원클릭 구현 계획, 재배포 점검, 새 PC epoch의 미실행/부재 결과를 지정 Evidence 경로에 기록합니다. 모든 Windows 시나리오는 `NOT_RUN`, 새 artifact와 SHA-256은 null/NOT_AVAILABLE로 명시합니다. 이전 ZIP을 새 원클릭 실행 파일로 재명명하지 않습니다. 제품 코드·승인 UI·General Work 증거·main·PR #23은 변경하지 않습니다.

PC 실행환경 복구 후 실제 validator를 먼저 실행하고, 승인된 runtime/DLL/FFmpeg/font/model 폐쇄성을 확인해야 합니다. 이후에만 원클릭 런처를 구현·빌드하고 일반 직원 Windows 프로필에서 첫/두 번째 실행, 단일 서버, 실제 모델 기능, 저장/완전 종료/재실행/Export/데이터 보존을 검증합니다. 사용자에게 수동 설치/모델 다운로드/의존성 복구 명령을 정상 사용 절차로 제시하지 않습니다.

최종 성공 조건은 오직 `PASS_MINDLE_MEDIA_AI_ONE_CLICK_RUNTIME_WINDOWS_E2E`입니다. 현재 그 조건을 충족하지 못했습니다.
