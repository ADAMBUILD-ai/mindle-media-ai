# MINDLE MEDIA AI TEST R2 재사용 우선·재빌드 Gate 결과

- 기준일: 2026-10-24 KST
- 판정: **TEST R2 REUSE REQUIRED / REBUILD GATE CLOSED**
- 대상 PR: #23 `HOLD / DO NOT MERGE`

## 확인한 현재 후보

| 식별 항목 | 고정값 |
|---|---|
| 제품 source | `2e5e9197d78c9b975686c1e419d2b68ce5f65226` |
| 생산 run | `39985471598` |
| 독립 readback run | `39987617196` |
| 동일 바이트 transport run | `39989419656` |
| EXE SHA-256 | `701654240d8f2795957f78f7d1cc9d7fd23d3195f49a0d39ede1d8b8a3a915a5` |
| payload manifest SHA-256 | `2c6c3345539473e77cab56b10105448d0c23b651875dca45e8d49217b781dc07` |
| 최종 ZIP SHA-256 | `c3cfda25e2f36f97024a57b586a20914be3b21a2b481f25e1652c8931ece3606` |
| ZIP 크기 | `3,166,947,613 bytes` |
| Runtime ID | `2e5e9197d78c-473763a9ef2d-ai-r2` |
| 설치기 SHA-256 | `747ddd1eb7aa1cef93f235af2128d9aeef68399e15c362a30260d36b1a4e9b44` |

정책, TEST R2 Evidence Contract, FINAL_DELIVERY, 네 Control Plane의 중첩된
후보 identity를 교차 대조했다. source·producer/readback/transport run·EXE·
manifest·ZIP·Runtime ID가 일치했다.

## 재사용 판정

- 네 Control Plane 모두 `package_build_allowed=false`다.
- 기존 승인 ID `MEDIA-AI-20261024-OWNER-WINDOWS-AI-CANDIDATE-R1`의 허용
  attempt는 1회이며 생산 run `39985471598`로 소비됐다.
- 작업 창·원격제어 연결 문제, 문서 변경, 동일 후보 재다운로드, 사무실 PC
  인수 재시도는 재빌드 사유가 아니다.
- 현재 소스 HEAD가 후보 source보다 새롭다는 사실만으로 TEST R2 사무실 PC
  인수 후보를 교체하지 않는다. 새 기능을 Windows 후보에 포함하려면 별도
  미소진 승인이 필요하다.

## 세 실행의 목적 보존

1. 생산 run은 승인된 1회 Windows 후보를 만들고 실제 원격 Windows에서 실행했다.
2. readback run은 생산된 파일을 독립적으로 다시 받아 해시와 CRC를 확인했다.
3. transport run은 확인된 동일 바이트를 전송 단위로 분할하고 복원했다.

readback과 transport는 새 EXE·패키지를 만든 중복 빌드가 아니다. 세 단계 중
하나를 삭제하거나 다른 단계의 성공으로 대체하지 않았다.

## 적용한 보호

- CI workflow 세 파일은 수정하지 않았다.
- 세 workflow의 기존 SHA-256을 정책에 고정해 근거 없는 변경을 탐지한다.
- 재빌드 요청은 새 승인 ID, 부모 SHA, 단일 attempt, 변경 파일, 파일별 TEST R2
  불충분 사유, 네 Build Gate=true가 모두 있어야 계약 완성으로 판정한다.
- 연결 장애를 사유로 구성한 재빌드 요청은 실제로
  `REBUILD_REJECTED_GATE_FALSE`로 거절했다.
- 기존 모델·설치본·사용자 프로젝트·증빙을 변경하거나 삭제하지 않았다.

## 회귀와 자산 해시

- 전체 Python: `221 passed, 6 skipped`
- Node: `1 passed`
- TEST R2 재사용 Gate: `5 passed`
- Python compile 및 `git diff --check`: PASS
- 정책: `8928982d49547fd4b7a7520e11042c82a22b234c78732b8a4f77bd44388ae6e4`
- validator core: `a044a1f08480132725a04057ad97befa307884b1049925df7c425df91a8b77c6`
- validator CLI: `e802727584386ebaa9c9cb3d75f59a398d30dbf866e57ea5f1e3f1c4d922ea9c`
- tests: `3d485d9abb81a4bdea08a12865708382106770e989a08d1bf1f5ac66e1248aa3`
- 재사용 영수증: `23a1dbfa7a9e80f6c71612a20586768b6a746e859b41987ce9af7f82436fd609`
- 연결 장애 재빌드 거절: `a2fc3bf32edd106ee52238ddd839e7525ab29483eb9d59113d35ddc46151bdf2`

## 정확한 후속

사무실 PC에서는 기존 TEST R2를 사용해 EXE 실행, 소유 서버 정상 종료,
endpoint 닫힘, 새 PID 재실행, 사진·영상·자막·나레이션·참고·입력 음성 복원,
Export와 설치 플레이어 실제 청취를 진행한다. 작업 창 연결 실패는 별도 운영
장애로 기록하며 패키지를 다시 만들지 않는다.

현재 신규 Blender/Wan 자산화 소스는 TEST R2에 포함되지 않는다. 해당 기능을
Windows 후보로 만들 필요가 생기면 변경 파일과 TEST R2로 해결할 수 없는 이유를
먼저 제출하고 별도 Build Gate 승인을 받아야 한다.
