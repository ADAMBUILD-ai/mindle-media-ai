# MINDLE MEDIA AI 새 창 인수인계 Master — 2026-10-07
상태: HANDOFF_SNAPSHOT / 제품 최종 배포 NOT PASS
대상: ADAMBUILD-ai/mindle-media-ai
Canonical branch: feature/ad-shortform-bridge-p0-20260926
감사 기준 원격 commit: c2e53a35f8534840952de1925a64f14f251a343e
기준 commit 시각: 2026-10-07 08:43:54 KST
이 문서는 인수인계이며 새 실행 지시나 제어 epoch 변경이 아니다. 사용자 요청에 따라 문서 3종만 게시한다. Worker B의 제품 변경 금지와 Worker A의 독점 실행 역할을 유지한다.

## 1. 핵심 판정과 점검 범위
현재 실행 주기는 MEDIA-AI-20261007-EMPLOYEE-PACKAGE-FINAL-CLOSEOUT-R2.
직원용 Windows 완전체 오프라인 배포 최종 판정은 RUNTIME_DEPENDENCY_LEAK이며 EMPLOYEE_PACKAGE_CLEAN_WINDOWS_E2E_PASS가 아니다.
구성요소 시험 및 임시 프로필 복사 설치 UI 관찰은 통과 근거가 있으나 기본 Windows 프로필 설치·바탕화면 cold launch 2/2·설치본 한국어 STT/PHOTO SAM·최종 자체 완결성과 고지 감사는 미완료다.

이번 점검은 원격 고정 SHA의 CURRENT 4종, R2 directive/contract/validator, 이전 Package Review/Evidence와 상세 파일, ACL/rebind 기록, UI HTML/CSS/manifest, 설치/launcher, 원격 변경 목록과 실제 로컬 Git 상태, 후보 ZIP 해시를 대조한 인수인계 감사다. 새 Windows E2E를 실행한 결과가 아니다. 원 대화에서 제공된 첫 화면 사진은 이번 참조에서 회수되지 않았으므로 화면 여백은 사용자 관찰로 기록하고 원격 소스 구조만 대조했다. 전체 소스의 모든 기능이 이번 창에서 재검증됐다는 의미가 아니다.

## 2. 최신 authority와 불일치
항상 다음 파일이 최신 원격에서 동일한 R2 epoch를 가리키는지 먼저 확인한다.
- CURRENT_PC_WORK_DIRECTIVE.md
- CURRENT_PC_WORK_CONTROL_PLANE_LOCK.json
- CURRENT_PC_WORK_STATE.json
- CURRENT_WORKER_COORDINATION_LOCK.json
- scripts/validate_pc_work_control_plane.py
- docs/commander/MINDLE_MEDIA_AI_EMPLOYEE_PACKAGE_FINAL_CLOSEOUT_R2_DIRECTIVE_v1.0_20261007.md
- docs/commander/MINDLE_MEDIA_AI_EMPLOYEE_PACKAGE_FINAL_CLOSEOUT_R2_EVIDENCE_CONTRACT_v1.0_20261007.json

CURRENT 4종과 원격 validator 상수는 R2로 정합하다. 실행 재개 전 실제 로컬 validator 출력 CONTROL_PLANE_PASS가 필요하다. 이 창에서는 원격 내용 정합을 확인했으며 최신 로컬 validator 실행 PASS를 새로 주장하지 않는다.
README.md는 아직 10월 6일 CONTROL-PLANE-RECOVERY 및 제품/패키지 PAUSED라고 표시한다. R2 authority보다 오래됐으므로 README만 읽어 작업을 중단하거나 과거 recovery를 재실행하지 않는다.
CURRENT_PC_WORK_STATE의 current_local_observation.local_head=093d15f... 및 dirty_tracked v20.2.7 목록도 과거 관찰이다. 현재 로컬 상태를 대신하지 않는다.
R2 최종 Review/Evidence와 scripts/FINAL_EMPLOYEE_PACKAGE_HOST_GATE.ps1은 기준 원격 SHA에서 404였다. 지시가 존재한다는 사실을 완료 근거로 쓰지 않는다.

## 3. 실제 로컬 checkout — 손실 방지 필수
사용 중 확인된 repo:
C:\Users\PC\Documents\Codex\2026-09-30\referenced-chatgpt-conversation-this-is-an-2\work\mindle-media-ai
origin: https://github.com/ADAMBUILD-ai/mindle-media-ai.git
branch: feature/ad-shortform-bridge-p0-20260926
이번 읽기 당시 local HEAD: b39ca305839f7d9f2fe1cb8ae25c8212159b91be.
원격 c2e53a3는 이 HEAD보다 15 commits ahead / behind 0.
로컬 tracked 변경:
src/media_ai/product_runtime.py
src/media_ai/product_server.py
src/media_ai/verified_model_adapters.py
ui/interaction.js
ui/product_integration.js
untracked: dist/, 패키지 Review/Evidence/detail, 패키지 scripts 8종, tests/test_employee_offline_mode.py, work-data/, work/.
이는 원격 구현을 connector로 게시하면서 로컬 Git HEAD를 갱신하지 않았다는 이전 Evidence와 일치한다. 로컬 dirty를 새 미게시 작업이라고 단정하지도, 모두 원격과 같다고 단정하지도 않는다. 파일별 diff/hash로 비교한다.
9월 15일 다른 checkout은 HEAD 2a9b34a / v20.2.1이다. canonical 작업 시작점으로 쓰지 않는다.
이번 문서 작성은 checkout/reset/pull/제품 파일 수정 없이 진행했다.

## 4. 커밋과 Evidence 계보
- c2e53a35f8534840952de1925a64f14f251a343e: R2 validator 정렬, 감사 기준 최신 head.
- a70e7cfd88555f6a8ef11f49fbd25f511431598c: 최신 Package Review가 명시한 구현 commit; 분할 압축 해제 경로 수정.
- ac0e6909f55aaf73ebcf8dcf736c37ebfda74824: 초기 구현 원격 게시/readback, 로컬 HEAD 미갱신.
- 527444b19e61e29ee2e78a264418671a34013300: 이전 archive source commit.
- 46fc392a843473bacd13805dfd5174e3bf423342: 이전 6/6 progress readback; employee E2E NOT_PASS.
- 6010efd / 89199c6: 로컬 이력에서 확인한 rebind Evidence/Review 게시. 정확한 복구 판정은 아래 원격 파일로 확인한다.

현재 패키지 근거:
docs/commander/MINDLE_MEDIA_AI_EMPLOYEE_DISTRIBUTION_PACKAGE_REVIEW_v1.0_20261006.md
evidence/pc_remote/MINDLE_MEDIA_AI_EMPLOYEE_DISTRIBUTION_PACKAGE_EVIDENCE_v1_0_20261006.json
evidence/pc_remote/media-ai-employee-package-v1_0-20261006/

최종 R2 필수 출력(감사 기준 아직 Review/Evidence 없음):
docs/commander/MINDLE_MEDIA_AI_EMPLOYEE_PACKAGE_FINAL_CLOSEOUT_R2_REVIEW_v1.0_20261007.md
evidence/pc_remote/MINDLE_MEDIA_AI_EMPLOYEE_PACKAGE_FINAL_CLOSEOUT_R2_EVIDENCE_v1_0_20261007.json
evidence/pc_remote/media-ai-employee-package-final-closeout-r2-v1_0-20261007/

## 5. 직원 패키지 실사용 E2E 매트릭스
| 항목 | 현재 근거/판정 | 최종 남은 확인 |
|---|---|---|
| 소스 회귀 | 이전 실행 56 PASS, offline tests 4 | 관련 수정 부분만 재검증 |
| 임시 프로필 runtime import | PASS, user-site 차단 | clean 기본 프로필 자체 완결성 |
| Intel 4x CPU | 실제 구성요소 PASS, 복사 설치 UI 1920x1080 preview 관찰 | 최종 설치본 retest |
| 한국어 Whisper STT CPU | 실제 구성요소 PASS | 최종 설치 UI 한국어 STT |
| PHOTO SAM | 실제 구성요소 PASS | 최종 설치 UI segmentation |
| VIDEO SAM tracking | 구성요소 PASS, 설치 UI tracking/decoded preview 관찰 | 최종 설치본 retest |
| 저장/닫기/재열기 | 복사 설치 UI 프로젝트 복원 관찰 | 기본 프로필 및 desktop 재시작 복원 |
| ZIP 내보내기 | 설치 UI 관찰 | 최종 설치본 실제 산출물 검증 |
| Shortform 미지원 | 안내 후 기본 작업 지속 관찰 | 최종 offline 동작 재확인; 온라인 MP4 성공과 별개 |
| 제거/재설치 | 임시 프로필 PASS; 보존 17/17 hash match | 실제 기본 프로필 host gate |
| desktop cold launch | 2/2 미검증 | 2회 완전 종료·실행, 서버 1개 |
| 압축 해제/분할 | 21,182 files 및 5분할 재조립 기록 | 의존성 수정 후 최종 ZIP 재생성 |
| 런타임 누락/고지 | RUNTIME_DEPENDENCY_LEAK | VC handling 및 notice/license audit |

런타임 기록: Python 3.11.9, CPU PyTorch 2.14.0, Torchvision 0.29.0(+cpu), NumPy 2.2.6, OpenVINO 2025.1.0.
모델 Evidence는 Intel single-image-super-resolution-1032와 SAM facebook/sam2.1-hiera-base-plus의 pinned identity/revision/weight hash를 담는다. 임의 모델 대체나 전체 모델 재다운로드 금지.

## 6. 후보 패키지와 오래된 Evidence
최신 Review 후보:
1,388,859,811 bytes
SHA-256 d9afe1d284f5d8fb295955442f70b6c96f5a20a138575b21dfb13af92c5cafc8
로컬 사용자 전달본:
C:\Users\PC\Documents\Codex\2026-10-06\referenced-chatgpt-conversation-this-is-an-2\outputs\MINDLE_MEDIA_AI_EMPLOYEE_FULL_WIN_X64_v1.0.zip
이 파일은 후보이며 직원 배포 승인본이 아니다.

반면 aggregate Evidence의 FINAL_PACKAGE_ARCHIVE 및 split_manifest는 이전 1,388,859,709 bytes / e7d798cb1c19af03baf54d4653d05ad464502cdfa9c961ac0902bb836d0fdae1을 담고 있다. 서로 다른 후보 버전이므로 혼용 금지.
실제 원격 detail 점검:
PACKAGE_BUILD_MANIFEST=BLOCKED/zip_built false,
PACKAGE_SELF_CONTAINMENT_AUDIT=NOT_RUN,
DESKTOP_SHORTCUT/INSTALLER/SAVE_REOPEN/EXPORT/SHORTFORM=NOT_RUN,
SPLIT_PARTS_MANIFEST=NOT_BUILT,
PACKAGE_SHA256SUMS=NOT_BUILT,
CLEAN_WINDOWS_FUNCTION_AUDIT=전체 NOT_RUN.
UNINSTALL_REINSTALL_TEST만 PASS_TEMPORARY_PROFILE/17 files, 기본 프로필 false.
REMOTE_PUSH_VERIFY는 ac0e6909의 과거 구현 readback을 기록한다. 최신 배포 readback PASS가 아니다.
FFMPEG_IDENTITY는 6.1.1-essentials_build-www.gyan.dev / STAGED_NOT_INSTALLED.
NATIVE_RUNTIME_STAGING_AUDIT는 공식 서명 VC 14.51.36247.0, STAGED_NOT_BUNDLED, entitlement PENDING_USER_RESPONSE.
상위 Review 관찰과 detail placeholder 불일치는 실제 최종 run으로 정리해야 한다. placeholder를 결과 확인 없이 PASS로 바꾸지 않는다.

## 7. 남은 blocker와 처리 방식
1. 패키지-local msvcp140.dll, msvcp140_atomic_wait.dll, vcruntime140_threads.dll 누락. 개발 PC의 외부 VC runtime에 기대므로 완전체 offline 아님.
2. R2가 요구한 소유자 Visual Studio 재배포 권한 증빙 미확정. Microsoft 서명만으로 권리를 추정하지 않는다.
   A: entitlement 확인 시 공식 unmodified x64 VC Redistributable, signature/version/SHA/license 기록, runtime 감지 및 필요한 경우 설치.
   B: 미확정 시 공식 https://aka.ms/vc14/vc_redist.x64.exe online bootstrap fallback만, 서명 검증·사용자 prerequisite 설치 동의. 이 경로는 offline 완전체 PASS로 인정하지 않는다.
3. 실제 기본 프로필 설치·쓰기·Start Menu/Desktop·cold launch 2/2 미확인. sandbox write grant 미반환은 제품 결함으로 단정하지 않는다.
4. 최종 설치본 한국어 STT/PHOTO SAM 및 모든 기능 재검증.
5. self-containment, runtime/model/FFmpeg notice/license audit.
6. 마지막 수정 뒤 manifest/ZIP/300 MiB parts/reassembly hashes/Evidence/remote readback 갱신.

위 항목은 현행 R2 요구사항의 전달이며 이 창에서 법률 판정을 새로 내린 것이 아니다.

## 8. Recovery / ACL / canonical rebind 이력
기존 실패: helper_unknown_error: apply deny-read ACLs.
기록된 corrupt state:
C:\Users\PC\.codex\.sandbox\deny_read_acl_state.json
22 bytes all NUL / invalid JSON / CASE_A_EXACT_MALFORMED_22B_ALL_NUL.
ACL Review v1.1은 중립 probe C:\MINDLE_WORK_TEST\acl_probe.txt -> MINDLE_PC_WORK_ACL_PROBE_PASS를 확인한 HOST_SANDBOX_ACL_RECOVERY_PASS였다. 이때 canonical repo validation은 아직 pending이었고 full RECOVERY_PASS가 아니었다.
이후 canonical rebind v1.2 Review/Evidence는 remote/branch 확인, 외부 backup, origin 재연결, tracked clean, work-data 보존, CONTROL_PLANE_PASS -> LOCAL_CANONICAL_REBIND_PASS / RECOVERY_PASS를 기록한다.
근거:
docs/commander/MINDLE_MEDIA_AI_WINDOWS_SANDBOX_ACL_RECOVERY_REVIEW_v1.1_20261006.md
evidence/pc_remote/MINDLE_MEDIA_AI_WINDOWS_SANDBOX_ACL_RECOVERY_EVIDENCE_v1_1_20261006.json
docs/commander/MINDLE_MEDIA_AI_CANONICAL_LOCAL_REBIND_REVIEW_v1.2_20261006.md
evidence/pc_remote/MINDLE_MEDIA_AI_CANONICAL_LOCAL_REBIND_EVIDENCE_v1_2_20261006.json

실제 남아 있는 외부 backup:
C:\MINDLE_RECOVERY_BACKUP\media-ai-20261006-193149\
DIRTY_TRACKED_CHANGES.patch
mindle-media-ai-local.bundle
v20.2.7_EVIDENCE_LOCAL.json
v20.2.7_REVIEW_LOCAL.md
이번 읽기에서 파일 존재는 확인했다. bundle 내용 복원시험이나 hash 무결성은 이번 창에서 재실행하지 않았다.
복구 PASS는 10월 6일 checkpoint이며 지금의 dirty/15 commits behind를 해소했다는 뜻이 아니다. 손상 재발 증거 없이 sandbox state 삭제, ACL 광범위 초기화, recovery 재시작 금지.

## 9. Worker 역할 분리와 운영
CURRENT_WORKER_COORDINATION_LOCK: NO_ACTIVE_COLLISION.
Worker A: Windows employee package final-closeout executor. scripts, packaging/runtime fixes in src, package/host tests, 지정 R2 Review/Evidence/detail, dist, LICENSES만 담당. approved UI layout 변경 금지(필수 결함 behavior fix 예외).
Worker B: repository governance observer, R2 Evidence 게시 전 READ-ONLY. 코드·패키지·control plane 중복 편집 금지.
Commander: 최신 원격 Evidence 검증, PASS lane 유지, 필요한 다음 지시 통합, 사용자/UI 권위 조율. 이번 사용자의 명시 요청에 따른 인수인계 3종 게시만 수행하며 Worker B 제품 작업을 재활성화하지 않는다.
순환: DIRECTIVE -> WORK -> EVIDENCE -> COMMANDER REVIEW -> NEXT DIRECTIVE.
docs/commander와 evidence/pc_remote가 authoritative 저장 위치다. 다른 창에 메시지 보내기/새 worker chat 만들기는 이번 요청에 포함되지 않는다.

## 10. VIDEO 중앙 Preview 아래 여백 — 최소 변경 검토안
사용자 관찰: 첫 VIDEO 화면에서 미디어 고유 비율 때문에 Preview 아래 큰 빈 공간 발생. 아래/우측 기능 일부를 그 공간으로 옮겨 화면 효율을 높이는 방향 검토.
현재 소스: video-center에 Preview -> transport -> multi-track timeline. 우측에는 편집/효과/자막/오디오 tabs, 자르기/분할/회전/속도, 밝기/대비/채도, 흔들림 보정/노이즈 제거.
CSS는 video layout height 380px, preview flex 48%/min-height 190px, timeline flex 52%/min-height 165px, 우측 space-between. breakpoint 1400/1100 계열에서 다른 min-height. 고정 높이와 intrinsic media 크기의 불일치는 여백 원인 후보이나 screenshot/실측 없이 단일 원인 확정 금지.
승인 기준: ui/ssot_manifest.json, docs/01_UI_SSOT_FINAL.md, F27E 승인 이미지와 Shortform Addendum.
승인 이미지 SHA:
f27eeb5031d83d7015494bc1683a981488ac4806627dc91c21f1c8c523df2541

권장 최소 후보(검토안, 미구현):
- Preview 미디어 비율을 보존하고 실제 높이·container 높이·DPI를 측정한다. 늘리기/crop으로 빈 공간을 덮지 않는다.
- transport와 timeline 기능을 유지한 채, 잔여 공간에 우측의 기존 기본 편집 4버튼 그룹을 compact 1행으로 이동하는 한 가지 후보를 먼저 비교한다. 실제 공간이 부족하면 이동하지 않는다.
- 상단 영상 불러오기 -> AI 자동 편집 -> 광고 숏폼 -> 프로젝트 저장 -> 내보내기 순서, 왼쪽 자연어/reference, 우측 고급 설정, PHOTO 구성, 색/아이콘/브랜드를 보존한다.
- 기존 control DOM/data-action/event/state를 재사용한다. 복제 버튼·이벤트 중복·설정값 유실·keyboard 순서 단절 금지.
- layout 변경 전 기존 담당 Worker의 package 작업과 충돌하지 않게 Commander가 UI 별도 epoch/범위/회귀 근거를 명시한다. 현행 R2 ui_changes_allowed=false이므로 이번 인수인계만으로 UI 구현 권한을 재활성화하지 않는다.
검증: 실사용 installed Windows 화면 before/after, 16:9·9:16·4:3·무미디어, 1920x1080/1366x768와 실제 대표 DPI, 1400/1100 breakpoint, 가로/세로 overflow, 모든 기존 control·tracking·STT·Save/Reopen·Export·Shortform·PHOTO 회귀. 대표 확인 후 최종 layout 반영. 수치/배치는 실제 비교자료로 확정.
선행 UI/아이콘 승인 이력은 frozen 자료로 유지하며 이미 승인된 브랜드를 새로 만들지 않는다. 새 이동안은 사용자 검토 요청이지 최종 배치 승인 완료가 아니다.

## 11. 최종 PASS 조건
EMPLOYEE_PACKAGE_CLEAN_WINDOWS_E2E_PASS는 아래 전체 통과에만 사용:
- owner/license entitlement + 공식 runtime 처리 + native dependency closure.
- DEFAULT_PROFILE_HOST_GATE_PASS.
- 기본 %LOCALAPPDATA%\MINDLE\MEDIA_AI 설치 및 MEDIA_AI_DATA 데이터 경로, Start Menu/Desktop 생성.
- Desktop cold launch 2/2, 서버 정확히 1개, runtime identity LOCAL_OFFLINE_PACKAGE.
- installed-package VIDEO import/tracking/decoded preview, 한국어 STT, PHOTO import/SAM, Intel 4x.
- Save -> 완전 종료 -> Desktop reopen -> 프로젝트 복원 -> Export ZIP.
- Shortform unavailable graceful continuation.
- 제거 후 application 제거·data 보존, 재설치 후 보존 17개 hash 일치.
- Git/system Python/pip/HF token/repo/developer profile/external model cache 의존 없음.
- LICENSES/THIRD_PARTY_NOTICES.txt, MODEL_LICENSE_MANIFEST.json, RUNTIME_REDISTRIBUTION_MANIFEST.json 완성.
- 최종 ZIP 및 300 MiB 분할본 재생성, reconstruction hash 일치, extracted count/manifest/native import 확인.
- 모든 stale Evidence 갱신, canonical commit, 최종 원격 내용 readback, commit/ZIP/parts hash 보고.

결과 어휘:
license만 남음 -> OFFLINE_FULL_PACKAGE_LICENSE_GATE_BLOCKED
외부 VC 의존 -> RUNTIME_DEPENDENCY_LEAK
기본 프로필 gate 미실행 -> DEFAULT_PROFILE_HOST_GATE_PENDING
설치본 기능 실패 -> CLEAN_WINDOWS_TEST_FAILED
여러 blocker가 있으면 개별 목록도 함께 기록한다.

## 12. 절대 하지 말아야 할 작업
main/default merge, force push, 새 repo/branch/worktree, Production 배포, 무단 UI/브랜드 재설계, master SSOT 변경, 역사 Evidence 삭제, 개발/컴포넌트 시험을 installed clean E2E PASS로 승격, 임시 프로필을 기본 프로필로 표시, 변경 전 archive hash 재사용, 모델 임의 대체/불필요한 전체 재다운로드, GitHub 로그인 반복, credential/token 노출, worker 동시 제품 편집, work-data/사용자 데이터 삭제.
dirty checkout에 무조건 pull/reset/clean하지 않는다. 역사 rebind의 reset --hard 예외를 현재 동기화의 일반 허가로 사용하지 않는다. 외부 bundle/patch/데이터 hash 백업 및 원격과 비교 후 최소 동기화.
완료 lane을 처음부터 재실행하지 않는다. 마지막 수정에 영향을 받은 부분과 최종 설치 E2E만 재검증한다.

## 13. 다음 새 창 시작 순서
1. Pointer -> Bootstrap -> 이 Master를 읽고 원격 canonical 최신 SHA 확인. snapshot SHA보다 새 commit이면 CURRENT/Review/Evidence 재읽기.
2. 현재 Worker lane/진행 여부 확인. Worker A 제품 writer 1명 유지.
3. 실제 canonical repo branch/origin/HEAD/status 확인. dirty 및 untracked 외부 backup; 최신 로컬/원격 file diff/hash 대조. 오래된 9월 15일 clone 금지.
4. 손실 없는 동기화 후 CURRENT 4종 -> validator -> R2 directive/contract 읽기. CONTROL_PLANE_PASS 및 R2 epoch 확인.
5. 기존 Review/Evidence 및 실제 package/model/runtime/data 위치 검증. frozen PASS 재사용. placeholder/해시 충돌을 추적 목록으로 남김.
6. entitlement 확인과 기본 profile host gate 준비를 각각 진행. scripts/FINAL_EMPLOYEE_PACKAGE_HOST_GATE.ps1/.cmd를 R2 사양에 맞춰 작성·검증. 미실행을 PASS로 표기하지 않음.
7. VC closure -> 최종 package build -> 기본 Windows profile host E2E -> license/self-containment -> ZIP/parts/hash.
8. R2 exact Review/Evidence/detail 기록, commit/push/readback. 제품 최종 PASS는 전체 조건 만족 후만.
9. VIDEO 여백은 별도 최소 변경안의 실제 before/after 근거로 검토. R2와 혼합해 approved UI를 바꾸지 않음.

## 14. 자료 사용 및 갱신
이 Master + Bootstrap + Pointer는 같은 2026-10-07 snapshot 세트다. 문서 게시 commit은 Pointer의 publication receipt 설명과 사용자 최종 보고로 확인한다. 문서 자체에 자기 commit SHA를 넣는 순환 갱신을 하지 않는다.
원격 permalink 기본: https://github.com/ADAMBUILD-ai/mindle-media-ai/blob/c2e53a35f8534840952de1925a64f14f251a343e/
최신 작업 authority는 항상 canonical branch에서 재확인한다.
