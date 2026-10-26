# MEDIA 신규 장면 생성 연결 규격 R1

기준일: 2026-10-26 KST. 작업 ID: MEDIA-GENERATION-CONTRACT-R1-20261026.

## 판정과 범위

공식 고정 소스의 외부 제어 경로 조사 완료. MEDIA 어댑터 구현·실제 생성·Windows 설치·실무 품질 검증은 미완료다. 조사 결과를 생성 기능 PASS로 표시하지 않는다. 기존 자료 30초 제작의 입력 접수는 병행하며 신규 모델 조사로 대체하지 않는다.

MEDIA 조사 HEAD: `fb445c3ea98f6d9ea4c0bfd6fbffa3be3d5dd471`. LTX Desktop v1.3.1: `8ffed888f3a9afdfbf137fa6193bf1cdc1cd657b`. Wan2.2: `1ea34ff48f87168174e12956e200b1d908b1c5ff`. 모델 가중치 revision/SHA·설치본·대상 GPU 실제 사양은 이번 조사로 확정하지 않는다.

## 확인된 실제 경로

| 대상 | 확인 | MEDIA 결정 |
|---|---|---|
| LTX Desktop | Remote :41955, Bearer 인증·단일 사용 pairing·공유 생성 queue | 화면 좌표 자동화보다 이 API 경로를 우선 검증한다. 공개 안정 SDK 보장으로 확대하지 않는다. |
| 이미지→영상 | POST /api/assets/upload → POST /api/generations/image-to-video | 첫 범위는 권리 확인된 건축 렌더 이미지 1개·짧은 장면 1개다. |
| 조회·취소 | GET /api/generations/{generation_id}, POST /api/generations/{generation_id}/cancel | MEDIA 작업 ID와 공급자 작업 ID를 영속 연결한다. |
| 결과 회수 | 생성 응답 outputs의 asset ID, GET /api/assets/{asset_id}, 서명 bytes_url | 로컬 작업 폴더로 복사 후 SHA·스트림·길이·디코딩 검사한다. |
| Blender 가이드 영상 | Remote 업로드는 이미지 전용; 영상·음악 업로드 미지원 | Depth/Canny 영상 파일을 이 업로드 API로 보낼 수 있다고 가정하지 않는다. 별도 수동 인수 또는 CLI/지원 API 확인 전 BLOCKED_UNSUPPORTED_INPUT. |
| LTX Python pipeline | 공식 문서는 코드 통합에 Python pipeline을 안내 | Desktop Assistant와 별도 어댑터 ID·엔진 identity로 관리한다. |
| Wan CLI | generate.py의 task/image/prompt/save_file/frame_num/base_seed 옵션 존재 | CLI 후보일 뿐 MEDIA 현재 Wan 경로와 동일하지 않다. 현재 경로는 ComfyUI workflow 승인·고정을 요구한다. |

Remote의 입력 DTO는 params, inputs, contract_version으로 구성되고 extra 필드를 금지한다. 구현 전 고정 api_types.py 및 /api/generate/models-specs에서 실제 모델·해상도·fps·길이 조합을 대조한다. 지원하지 않는 값을 조용히 바꾸지 않는다. 원본 prompt와 전송 prompt·요청 JSON·반환 spec을 모두 보존한다.

## 현재 MEDIA 코드의 차이

architectural_video_pipeline.py의 ENGINE_ASSETS에는 existing_clip, blender, wan22만 있다. LTX 엔진이 없다. FFmpeg 조립 함수는 existing_clip만 받는다. registry의 LTX는 enabled=false다. 따라서 LTX 결과가 MEDIA로 자동 편입된다고 보고할 근거가 없다.

현재 LTX registry의 24GB 기준 보류 설명은 1.3.1의 소형 설정 발표와 함께 재평가할 사항이다. 그러나 9GB라는 숫자만으로 기존 문서의 RTX 3060 12GB를 지원한다고 결론내리지 않는다. FP8 지원 조건·실제 VRAM/RAM·설정·runtime·라이선스를 검증하기 전 활성화하지 않는다. registry와 모델 설치본은 변경하지 않았다.

## 구현할 어댑터 계약

1. preflight: 정확한 앱 source/실행기/모델 전체 파일 identity, 사용권 검토, 승인 범위, 대상 GPU/메모리, API 명세를 확인한다. 외부 파일/모델 자동 다운로드 금지.
2. submit: MEDIA job ID·입력 SHA·한국어 원지시·검증된 생성 prompt·seed·요청 설정의 해시를 원장에 먼저 저장한다. 생성 POST 응답이 끊기면 재전송하지 말고 SUBMISSION_UNKNOWN으로 중단하고 서버 작업을 대조한다. 중복 생성 방지가 입증되기 전 무조건 재시도 금지.
3. poll: 고정 엔진 작업 ID만 조회한다. API의 실제 상태 enum을 버전별로 인수하며 알 수 없는 상태는 실패/미확인으로 유지한다. queue 등록을 추론 완료로 올리지 않는다.
4. cancel: 자신이 제출한 작업에만 취소 요청한다. 취소 요청·서버 취소 확인을 구분하고 확인 전 CANCELLED로 확정하지 않는다. 공유 queue 정리·다른 작업 취소·모델 삭제 기능은 호출하지 않는다.
5. collect: output asset ID와 만료 가능한 bytes_url을 사용한다. URL 호스트/경로를 승인 엔진으로 제한하고 redirect·만료·빈 파일·부분 파일을 검사한다. Bearer·pairing grant·서명 URL은 로그/receipt에서 제거한다.
6. validate: 임시 파일을 전체 디코딩·FFprobe·입력/작업 결속 검사한 뒤 확정 경로에 게시한다. 과거 파일 존재·API 성공·실행 exit 0만으로 PASS 금지.
7. import: 생성 receipt를 보존한 채 검증 MP4를 기존 제품 import/편집 API로 인수한다. 변환 후 FFmpeg receipt의 model_inference=false가 생성 이력을 지우거나, 반대로 FFmpeg 성공이 생성 성공을 대신하지 않도록 원천 receipt를 별도 연결한다.

계약 필드: request_id, media_job_id, provider_job_id, adapter_id, app_revision, executable_sha256, runtime_manifest_sha256, model_manifest_sha256, input_sha256s, original_command_sha256, submitted_spec_sha256, returned_spec_sha256, timestamps, terminal_state, output_sha256, technical_review, human_review. missing identity는 null 및 BLOCKED로 남긴다.

## 오프라인·승인 조건

Assistant의 Gemini/local 선택은 prompt enhancement·text encoder 설정과 별개다. Assistant만 local로 바꾸고 오프라인이라고 판정하지 않는다. 각 공급자 설정, 자동 향상, 모델 다운로드, analytics/update, 실제 네트워크 전송을 별도로 확인한다. LTX 문서의 기본 Gemini 선택을 묵인하지 않는다. 앱 라이선스와 모델 가중치 약관은 별도다. 이번 작업에서 모델 약관 수락·키 입력·네트워크 pairing·설치·GPU 실행은 하지 않았다.

## 첫 실증 출구 조건

| 단계 | 증거/통과 조건 |
|---|---|
| 입력 | 권리 확인된 동일 건축 렌더 원본과 SHA, 창호·층수·재료·카메라 지시 확정 |
| 실행 | 격리 모델/실행기 승인, 새 job의 실제 추론 시작·종료·메모리·시간·실패 원문 |
| 형태 | 동일 건물·창호·층수·외장재 유지 여부를 대표/검수자가 대조; 왜곡은 품질 FAIL |
| 실패 주입 | 세션 만료, 생성 POST 응답 유실, queue 중단, 취소, 앱 재시작, 결과 URL 만료·부분 파일·해시 변경에서 완료 게시 차단 |
| MEDIA 인수 | 생성 클립 import → 기존 장면과 편집 → Supertonic 한국어 음성·BGM 합성 → 30초 MP4 기술 검사 |
| 영속성/사람 검수 | 실제 프로세스 종료·재시작 → Reopen → Export → 화면·한국어 음성 청취 기록 |

단일 생성 길이와 완성 영상 길이는 구분한다. Wan의 frame_num 격자·생성 fps와 MEDIA 24fps 편집을 대조하고, 1280×704를 정확한 16:9로 표기하지 않는다. 최종 비율·패딩/크롭 정책을 사전에 확정하며 건축 구도를 임의로 자르지 않는다.

## 권위 있는 근거

- [LTX 고정 Remote 문서](https://github.com/Lightricks/LTX-Desktop/blob/8ffed888f3a9afdfbf137fa6193bf1cdc1cd657b/docs/remote-lan.md)
- [LTX 생성 route](https://github.com/Lightricks/LTX-Desktop/blob/8ffed888f3a9afdfbf137fa6193bf1cdc1cd657b/backend/remote/generations.py)
- [LTX 입력 schema](https://github.com/Lightricks/LTX-Desktop/blob/8ffed888f3a9afdfbf137fa6193bf1cdc1cd657b/backend/api_types.py)
- [LTX Assistant](https://github.com/Lightricks/LTX-Desktop/blob/8ffed888f3a9afdfbf137fa6193bf1cdc1cd657b/docs/desktop-assistant.md)
- [LTX 공식 Python pipeline 안내](https://docs.ltx.io/open-source-model/getting-started/quick-start) — 가변 문서이며 Desktop v1.3.1 계약과 혼용 금지.
- [Wan 고정 CLI](https://github.com/Wan-Video/Wan2.2/blob/1ea34ff48f87168174e12956e200b1d908b1c5ff/generate.py)
- [실제 제작 자료 단일 접수표](../handoff/media-ai-core-e2e-r2-20261025/INTAKE_AND_APPROVAL_KO.md)

검사 원본: ../evidence/media-generation-contract-r1-20261026/STATIC_AUDIT.json. 이는 AST·소스 구조 확인이며 HTTP 통신 시험·모델 실행 시험이 아니다. Build Gate=false / PR #23 Draft/HOLD / 미병합 유지.
