# MINDLE MEDIA AI 외부 숏폼 연동 마감 검수 — 2026-10-08

결과: **BLOCKED_EXTERNAL_SHORTFORM_INTEGRATION**.

새 지시서와 Evidence Contract 전체를 확인하고 새 Epoch 전용 실행을 수행했습니다. 기존 기본 제품 PASS를 반복 실행하지 않았습니다.

- Epoch: MEDIA-AI-20261008-SHORTFORM-EXTERNAL-INTEGRATION-CLOSEOUT-R1
- Canonical branch: feature/ad-shortform-bridge-p0-20260926
- 제공 HEAD: 4b1f38f4035884c717a2efddf2fa5f66cf54cb01
- 실행 소스: 144abf748fda7630304ebec6a338c4d7e7c9095b
- [실제 Actions 실행 37744311046](https://github.com/ADAMBUILD-ai/mindle-media-ai/actions/runs/37744311046)
- Artifact 11534494818 / ZIP SHA-256: `3857b9c4b8056d3c311a3b9fbe34c6d1f280e1b75b627ff2a40f9868b00c7fd8`
- 다운로드한 아티팩트의 SHA 및 전체 ZIP CRC 확인 PASS.
- 기록 시각: 2026-10-08 07:35:13 UTC / 16:35:13 KST.

## 실제 확인 결과

| 단계 | 결과 | 실행 증거 |
|---|---|---|
| 새 Control Plane | PASS | CONTROL_PLANE.log |
| 공급자 URL 설정 | BLOCKED | 실제 runner 환경에서 MARKETING_SHORTFORM_BASE_URL 빈 값 |
| 실제 공급자 health/네트워크 | NOT_REACHED | URL 미설정으로 network_attempted=false |
| bridge token 제공 | BLOCKED | 실제 runner 환경에서 token_present=false |
| Marketing 실제 HTTP·인증·Contract | NOT_REACHED | request_sent=false; authentication_tested=false |
| 승인 AVORA 자산 | NOT_REACHED | 실제 HTTP 계약 이전 중단 |
| 9:16 실제 브라우저 Preview | NOT_REACHED | 외부 의존성 차단 |
| 대표 승인 전 Export 차단·승인 action | NOT_REACHED | 승인 조작/자동 승인 없음 |
| 승인 광고 MP4 Export | NOT_REACHED | ffprobe·MP4 해시 검증 수행 없음 |
| 기존 기본 제품 | FROZEN PASS 유지 | 원본 실행 37738880868의 PHOTO·VIDEO·STT·재열기·기본 Export 재사용 |

공급자 판정 코드는 BLOCKED_MARKETING_PROVIDER_UNREACHABLE이고 세부 이유는 **MARKETING_SHORTFORM_BASE_URL_MISSING**입니다. 이번 실행에서 연결 실패를 관찰한 것은 아닙니다. 주소가 없어 네트워크 요청 자체를 수행하지 않았습니다. token의 환경 제공 여부만 확인했으며 인증 성공/실패는 검증하지 않았습니다. token 누락은 BLOCKED_MARKETING_BRIDGE_TOKEN_MISSING에 해당하는 추가 의존성입니다.

Actions 결론은 failure입니다. 실행 스크립트가 명시적인 외부 의존성 차단을 알리는 exit 3으로 종료했습니다. 이 실행을 전체 제품 성공으로 재표기하지 않습니다.

## 변경 범위와 검증

`.github/workflows/product-e2e.yml`에 활성 Epoch를 읽는 실행 분기를 추가했습니다. 기존 기본 제품 E2E는 이전 제품 Epoch에서만 허용하고, 새 Epoch에서는 외부 환경 확인 전용 Job으로 진행합니다. `model_scout/run_shortform_external_closeout.py`는 기본 localhost 주소를 대입하지 않고 실제 repository variable/Actions secret의 환경 제공 여부를 확인합니다. 설정이 있다면 지정 health 경로로 실제 요청을 시도하며, 비밀값은 Evidence에 기록하지 않습니다.

이번 실제 실행에서 active-epoch Job은 SUCCESS, external-shortform-closeout Job은 BLOCKED에 따른 failure, 기존 Approved UI to perpetual-use CPU models Job은 **SKIPPED**입니다. 모델 획득·PHOTO·VIDEO·STT·Save/Reopen·기본 Export를 다시 실행하지 않았습니다.

Canonical baseline 37744310808은 SUCCESS입니다. 제품 runner의 기존 Python 66 PASS / UI 2 PASS는 frozen Evidence에서 재사용했습니다. 이번 환경 검사 실행에서 66개 테스트를 새로 수행했다고 주장하지 않습니다. 제품 runtime·UI·확정 HTML/CSS는 수정하지 않았으므로 기본 제품 smoke도 재실행하지 않았습니다. 새 스크립트 Python compile 검사 및 실제 새 Epoch validator는 PASS입니다.

패키지 잠금은 유지됐고 실행 37744310925의 package Job, 37744310814의 Windows runtime package Job이 모두 **SKIPPED**입니다. 직원 배포 패키지를 재생성하지 않았습니다. main은 `797da297f588780ad2d608deea3b5af8f05af450`, PR #23은 draft/open·미병합·HOLD / DO NOT MERGE를 유지했습니다. 새 Control Plane 4종·validator·지시서·Contract 및 역사 Evidence를 변경/삭제하지 않았습니다.

## 보안 설정과 정확한 재개 조건

연동 소유자가 GitHub repository/environment에 다음 값을 제공해야 합니다.

1. Repository variable `MARKETING_SHORTFORM_BASE_URL`: 실제 E2E runner에서 접근 가능한 Marketing 공급자 URL.
2. Actions secret `MARKETING_SHORTFORM_BRIDGE_TOKEN`: 실제 공급자가 인정하는 bridge token.
3. 공급자 health/Contract 경로·method의 확정 정보. 현재 client에는 POST /v1/shortform/contracts와 GET /v1/shortform/e2e/approved-contract가 인코딩돼 있습니다.
4. 실제 승인 AVORA 자산의 ID·origin·SHA·승인 provenance.
5. 실제 대표 승인 경로와 승인 전 Export 차단을 시험할 상태.

현재 연결된 GitHub API 도구에는 repository variables/Actions secrets를 관리하는 administration 기능이 없으며, 실제 공급자의 token 값도 제공되지 않았습니다. 이름이 같은 secret을 가정하거나 다른 서비스 token을 재사용하지 않았습니다. token은 채팅·문서·로그로 전달하지 않고 Actions secret에 설정해야 합니다. 기존 [연동 의존성 요청서](MINDLE_MEDIA_AI_MARKETING_SHORTFORM_INTEGRATION_DEPENDENCY_REQUEST_v1.0_20261008.md)를 그대로 적용합니다.

localhost를 사용할 경우 같은 runner/job/service 네트워크에 **실제** Marketing 프로세스가 먼저 실행돼야 합니다. mock 서버나 과거 응답을 띄우지 않았습니다.

이 회차의 변경은 환경·Epoch 실행 경로와 증거 기록입니다. 실제 HTTP Contract·자산·9:16 renderer·승인·MP4 검증이 구현/수행됐다는 판정은 내리지 않습니다. 연결 입력이 제공되면 실제 응답을 기준으로 필요한 제품 연동 수정과 후속 검증을 계속해야 합니다. 모든 외부 Gate의 실제 증거 이전에 PASS_MINDLE_MEDIA_AI_FULL_PRODUCT_E2E_RUNTIME_VERIFIED, 직원 패키지 재생성, main 병합은 허용되지 않습니다.
