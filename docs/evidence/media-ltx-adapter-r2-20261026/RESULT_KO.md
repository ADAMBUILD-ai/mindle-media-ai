# MEDIA LTX 연결 코드 R2 결과

2026-10-26 KST. 판정: **독립 소스 어댑터 구현·계약시험 PASS / 실제 LTX 모델·30초 실무 E2E 미완료**.

문서 조사 다음 단계로 실제 HTTP 이미지 업로드·생성 등록·조회·취소·결과 회수 코드를 구현했다. 저장된 요청과 응답을 대조하고, 실제 FFprobe·FFmpeg 전체 디코딩 후 기존 제품 import를 호출한다. 생성 원천 receipt는 제품의 reference_artifacts로 연결해 프로젝트 Save/Reopen/Export에 보존한다.

## 검증

- 새 어댑터 계약시험: 31 PASS.
- 전체 로컬 Python: 432 PASS / 6 SKIP.
- 코어/UI 59개 파일 원본 bytes 일치. General/PC 관제 PASS, Build Gate=false 유지.
- 승인 없는 기본 구성: BLOCKED_EXECUTION_APPROVAL, exit 2. 외부 실행 없음.
- 실제 loopback HTTP 통신과 FFmpeg 합성 5초 fixture로 import·저장 후 별도 Python 프로세스에서 재열기·Export·ZIP CRC·내부 SHA 검증.
- 최신 소스 `b1aea66941277f20323f3a0116bbf60499eff365`의 [원격 Canonical Run 40248381507](https://github.com/ADAMBUILD-ai/mindle-media-ai/actions/runs/40248381507): SUCCESS, Python 433 PASS / 5 SKIP, UI 계약 2 PASS. 새 브라우저 E2E나 모델 추론 시험은 아니다.
- [Windows 사전검사 Run 40248377862](https://github.com/ADAMBUILD-ai/mindle-media-ai/actions/runs/40248377862): SUCCESS. 범위는 기존 관제·소스 compile이며 신규 어댑터의 Windows 실실행은 아니다. [패키지 Gate Run 40248377865](https://github.com/ADAMBUILD-ai/mindle-media-ai/actions/runs/40248377865): Gate SUCCESS / build-and-e2e SKIPPED.
- Python 구문·JSON 파싱·git diff --check·pip check PASS. 과거 실패 재실행 없음.

새 시험은 응답 유실 후 중복 POST 금지, 재시작 후 동일 요청 인수, 원고·길이·비율·모델·seed·fps·해상도 불일치, 취소 요청/완료 구분, 인증 만료, 입력/엔진 파일 변경, 외부 URL/redirect 거부, 만료·부분·손상 결과, cloud API 설정 차단, API-only 모델 거부, 동시 요청 lock과 config 결속을 검사한다.

## 완료 표현 제한

시험 서버는 LTX가 아니며 파란색 MP4는 FFmpeg 시험 fixture다. 이를 실무 영상·건축 생성 성공으로 쓰지 않았다. 새 모델 추론이나 대표 PC 인수를 실행했다고 보고하지 않는다. 원격 succeeded는 PROVIDER_SUCCEEDED_UNVERIFIED이며, 파일 검사 후에도 COLLECTED_TECHNICAL_ONLY다. model_inference_verified=false와 full_product_pass=false를 유지한다.

기존 제품 코어·확정 UI·설치본·registry enabled는 변경하지 않았다. 새 EXE·모델 설치·유료 API·main 병합·배포·예산 변경 없음. PR #23 Draft/HOLD 유지.

## 다음 실행 조건

[실행 절차·구성 계약](../../commander/MEDIA_LTX_SOURCE_ADAPTER_R2_KO.md)을 따른다. 실제 LTX 설치본·전체 가중치·실행 프로세스 identity와 GPU 조건을 인수하고, 승인된 건축 렌더에서 새 장면 1개를 추론해야 한다. 건물·창호·재료·카메라 사람 검수와 외부 전송 관측이 필요하다. 현재 API가 증명하지 못하는 loaded-runtime identity는 독립 실행 증거로 보강해야 한다.

기존 실제 자료 30초 영상은 [단일 접수표](../../handoff/media-ai-core-e2e-r2-20261025/INTAKE_AND_APPROVAL_KO.md)의 영상·권리·음악·원고·음량·장문 정책 접수가 필요하다. 설치/모델 배치/새 Windows 후보가 필요한 단계는 각각의 기존 승인 제한을 유지한다.

소스와 검사 해시: SOURCE_VALIDATION.json. 실제 두 프로세스 기록: SYNTHETIC_PROCESS_LIFECYCLE.json. Export 내부 목록: SYNTHETIC_EXPORT_MANIFEST.json. 이 증거는 소스 연결 계약을 검증하며 AI 모델 실행을 대신하지 않는다.
