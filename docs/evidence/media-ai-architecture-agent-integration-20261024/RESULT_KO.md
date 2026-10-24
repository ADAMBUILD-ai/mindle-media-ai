# MINDLE MEDIA AI 건축 영상 생성형 에이전트 연결 결과

- 기준일: 2026-10-24
- 기준 원격 HEAD: `5b8746ce9887bddc785a4da632b69580f8b174c4`
- 판정: **SOURCE INTEGRATION PASS / NEW CANDIDATE NOT BUILT**
- PR #23: **HOLD / DO NOT MERGE**

## 해결한 단절

기존 로컬 Qwen 계획기는 밝기·대비·채도·자막·나레이션 작업만 계획했다. 별도로 만든 건축 영상 장면 조립, Blender 및 Wan 자산 계약은 AI 대화 입력과 연결되지 않았다.

이번 변경은 승인 UI의 배치와 색상을 바꾸지 않고 기존 VIDEO `AI 대화 편집` 입력에서 다음 제품 경로를 추가했다.

`자연어 건축 영상 요청 → 고정된 로컬 Qwen JSON 추론 → 서버가 보유한 영상 별칭만 선택 → 의미 계약 검증 → 영속 작업 → FFmpeg H.264/yuv420p/AAC/faststart 조립 → 프로젝트 저장·재열기`

## 구현 판정

| 항목 | 판정 | 근거 |
| --- | --- | --- |
| 생성형 실행 경계 공통화 | PASS | 편집 계획과 건축 계획이 같은 고정 모델·실행기·SHA·revision·license 검증 함수를 사용한다. |
| 자료 발명 방지 | PASS | 모델에는 `input-01` 형식 별칭만 전달하며 파일 경로·명령·네트워크 동작은 출력 스키마에 없다. |
| 요청 의미 검증 | PASS | 명시한 16:9/9:16/원본 비율, 전체 초, 모든 선택 영상 1회 사용, 원본 길이 초과를 실행 전에 검사한다. |
| 실제 MP4 조립 | PASS | 테스트에서 서로 다른 두 실제 MP4를 FFmpeg로 조립하고 출력 해시·코덱·픽셀 형식·AAC·faststart·장면 순서를 검증했다. |
| 중복 실행 차단 | PASS | 브라우저 request ID가 바뀌어도 같은 `plan_id`는 하나의 영속 production으로 재사용한다. |
| 취소 결과 비게시 | PASS | 실행 전·FFmpeg 실행 중·게시 직전 취소를 확인하고 미완성 출력을 삭제한다. |
| 프로젝트 자료 보존 | PASS | 영상 외 기존 PHOTO·음성 작업 ID를 유지한 채 결과 영상을 같은 프로젝트에 추가한다. 저장 실패 시 신규 기록·파일·프로젝트를 원복한다. |
| 브라우저 진입 | PASS | 기존 입력창에서 건축 홍보·장면 구성 요청만 전용 에이전트 API로 보내며 기존 편집 라우팅을 보존한다. |
| 실제 Qwen을 사용한 **새 경로** 추론 | **NOT RUN** | 현재 Linux 작업공간에 고정 GGUF와 llama 실행기가 없다. 단위/통합 검증의 모델 응답은 명시적 fixture이며 실제 모델 추론으로 세지 않는다. |
| Blender·Wan 실제 장면 생성 | **BLOCKED ASSET** | 자산 계약과 preflight만 있으며 Windows runtime·가중치·GPU 실증이 아직 없다. |
| TEST R2 포함 | **NO** | 기존 TEST R2는 그대로 재사용하며 이번 소스 변경을 포함한 재빌드는 승인되지 않았다. |

## 회귀 결과

- Python 전체: `229 passed, 6 skipped`
- Node 전체: 모든 UI 테스트 PASS
- 건축 에이전트 집중 검증: 생성형 계약 오류 5종 차단, 실제 두 장면 조립·영속 저장 PASS
- TEST R2 재사용 Gate: `REUSE_TEST_R2`
- Control Plane Build Gate: `false`
- GitHub Actions workflow 변경: 없음

## 후보와 다음 실제 검증

사무실 PC 인수는 기존 TEST R2 후보를 계속 사용한다. 작업 창 연결 문제만으로 재빌드하지 않는다. 이번 개발분을 Windows 후보에 넣으려면 변경 파일과 기존 후보로 해결할 수 없는 이유를 제출하고, 새 승인 ID·정확한 부모 SHA·단일 attempt·4개 Build Gate를 별도로 열어야 한다.

새 후보가 승인된 뒤에만 실제 Windows에서 다음을 확인한다.

1. Qwen이 두 개 이상의 실제 건축 영상을 순서·길이·비율 계획으로 반환하는지 확인한다.
2. 표시된 계획과 실행 결과의 장면 순서·총 길이가 같은지 확인한다.
3. 취소 중 FFmpeg 프로세스와 미완성 출력이 정리되는지 확인한다.
4. Save → 소유 서버 종료 → 새 PID → Reopen → Export → 설치 플레이어 재생·탐색·청취를 확인한다.

전체 제품 PASS 문자열은 발급하지 않는다.
