# MEDIA LTX 소스 어댑터 R2 — 실제 연결 코드와 인수 경계

2026-10-26 KST. `MEDIA-LTX-SOURCE-ADAPTER-R2-20261026`.

## 이번에 만든 것

`external_assets/media-production/ltx_remote_adapter.py`는 LTX Desktop v1.3.1 고정 Remote API로 실제 HTTP 요청을 보내는 독립 소스 어댑터다. 이미지 업로드 → 생성 등록 → 작업 조회·취소 → MP4 회수·전체 디코딩 검사 → 기존 ProductJobService.import_media를 통한 불러오기를 구현했다. 설치·다운로드·서버 기동·다른 작업 취소·cloud fallback 기능은 없다.

제품 core/UI와 registry enabled 값은 그대로다. 새로운 화면 버튼이나 설치본 기능으로 활성화하지 않았다. LTX 모델 추론·건축 품질을 확인하기 전 제품에서 신규 영상 생성 완료로 표시하지 않는다.

## 실패 보호

- source revision은 LTX Desktop `8ffed888f3a9afdfbf137fa6193bf1cdc1cd657b`만 받는다.
- 승인 원점은 명시적인 loopback HTTP 주소다. 시스템 proxy·redirect·외부 output URL을 거부한다. LAN 엔진·원격 host는 이 버전 범위 밖이다.
- 실행 승인·라이선스 검토·오프라인 검토·application/runtime/model/settings/FFmpeg/FFprobe 로컬 파일 SHA·bytes가 필요하다. 승인 템플릿은 false·빈 값이다.
- 실제 settings.json에서 로컬 텍스트 인코더, 자동 프롬프트 변경 금지, local Assistant, standard budget을 읽어 검사한다. API 키가 있으면 차단한다. 설정 파일 일치는 실행 프로세스·네트워크 무전송의 독립 증명이 아니다.
- 모델 specs API에서 설치된 local 모델·활성 offering·승인한 해상도/fps/길이 조합을 대조한다. API-only 제공을 로컬 실행으로 대체하지 않는다.
- 생성 POST 전에 요청을 SQLite WAL에 기록한다. 응답 유실·프로세스 중단은 SUBMISSION_UNKNOWN으로 보존하고 동일 요청을 다시 POST하지 않는다. 오래된 lock은 자동 삭제하지 않고 담당자가 실제 프로세스·서버 작업을 대조해야 한다.
- 응답의 모델·원고·길이·비율·fps·seed·해상도·입력 asset ID가 바뀌면 차단한다. Remote 응답이 노출하지 않는 cameraMotion/negativePrompt는 확인 불가로 남긴다. 이번 버전은 neutral camera만 전송한다.
- 생성 성공 응답은 PROVIDER_SUCCEEDED_UNVERIFIED다. 실제 MP4의 바이트·해상도·길이·fps·전체 디코딩을 확인한 후에만 COLLECTED_TECHNICAL_ONLY다. 540p 같은 tier명에서 실제 pixel 크기를 임의 계산하지 않고 승인 구성의 exact dimensions와 비교한다.
- 취소 요청과 취소 완료를 구분한다. 만료된 서명 URL은 asset metadata를 다시 읽는 collect로 회수할 수 있지만 생성 요청은 반복하지 않는다.
- product import에도 선행 intent를 기록한다. 중단된 import는 IMPORT_REVIEW_REQUIRED로 남긴다. 이미 만든 project나 유효 중간 파일은 삭제하지 않는다.
- 생성 receipt를 reference_artifacts로 연결해 Save/Reopen/Export에 함께 넣는다. import의 model_inference=false를 유지하고 생성 원천 기록을 별도 보존한다. Bearer·서명 URL은 로그에서 제거한다.

## 실행 준비

1. 기존 실제 제작 단일 접수표의 자산·권리·원고·음량·장문 정책을 채운다. 신규 장면 평가에는 권리 확인된 건축 렌더 이미지와 생성 지시를 별도로 정한다.
2. 설치·모델 배치가 필요하면 그 범위만 별도 승인받는다. 앱 코드와 가중치 약관을 따로 검토한다. 이 문서는 승인이 아니다.
3. `ltx_source_config.template.json`을 별도 작업 폴더로 복사한다. application/runtime/model 전체 구성 파일/settings/ffmpeg/ffprobe 각각의 절대 경로·bytes·SHA를 등록한다. 모든 분할 가중치와 실행에 필요한 파일 목록은 모델 담당자가 동결한다. 이 어댑터는 목록이 완전한지 모델 내부를 해석하지 않으며 확인된 파일만 검사한다.
4. `allowed_params`에는 prompt, model, resolution, duration, fps, aspectRatio, seed를 모두 명시한다. 이 버전은 16:9·24fps·중립 카메라·LTX local fast offering만 평가한다. `output_dimensions`에는 해당 params의 canonical SHA-256을 key로 `[width,height]`를 넣는다. 고정 backend의 pixel 규격을 확인해 작성하며 추정값을 넣지 않는다.
5. 허용된 엔진과 pairing을 승인 범위에서 준비하고 device session은 `MINDLE_LTX_DEVICE_SESSION` 환경변수에만 둔다. command line·저장소·receipt에 키를 쓰지 않는다. 설치·pairing·엔진 시작은 실행기가 하지 않는다.

```powershell
python scripts/run_ltx_source_evaluation.py --config <승인구성.json> --root <새작업폴더> --action preflight
python scripts/run_ltx_source_evaluation.py --config <승인구성.json> --root <새작업폴더> --action submit --request <요청.json> --execute
python scripts/run_ltx_source_evaluation.py --config <승인구성.json> --root <새작업폴더> --action poll --request-id <UUID> --execute
python scripts/run_ltx_source_evaluation.py --config <승인구성.json> --root <새작업폴더> --action collect --request-id <UUID> --execute
python scripts/run_ltx_source_evaluation.py --config <승인구성.json> --root <새작업폴더> --action import --request-id <UUID> --product-root <격리MEDIA폴더> --execute
```

요청 JSON 필드: request_id(UUID), image_path, image_sha256, command(한국어 원지시), params(승인 값 그대로). `status`는 로컬 기록 조회다. `cancel --execute`는 해당 어댑터가 등록한 작업 ID에만 적용한다. 승인이나 runtime identity가 바뀌면 같은 요청을 재사용하지 않는다. 공급자 작업 ID를 모르는 SUBMISSION_UNKNOWN은 자동 복구하지 않으며 서버 queue의 원요청을 담당자가 대조한다.

## 시험과 미완료

로컬 HTTP 시험 서버는 공식 DTO 구조의 응답을 제공할 뿐 AI가 아니다. FFmpeg로 만든 5초 파란색 시험 영상을 실무 자산으로 등록하지 않았다. 시험에서는 이 영상을 회수·디코딩·제품 import·저장하고, 서로 다른 실제 Python 프로세스에서 재열기·Export를 확인했다. ZIP 내부 생성 receipt와 파일 해시도 대조했다.

아직 필요한 것: 실제 LTX 실행기·전체 가중치 identity, 실제 GPU/메모리 검수, 실행 프로세스와 로컬 파일의 연결 증명, 외부 전송 관측, 새 모델 추론 원문·실행 기록, 건물/창호/재료 유지와 카메라 품질, 30초 음성·BGM 통합, 대표 PC 화면·청취 인수다.

따라서 모델 추론 검증=false, 전체 제품 PASS=false를 유지한다. Build Gate=false / PR #23 Draft/HOLD / main 미병합 / 새 EXE·설치 모델 교체 없음.

근거: [LTX 고정 입력 schema](https://github.com/Lightricks/LTX-Desktop/blob/8ffed888f3a9afdfbf137fa6193bf1cdc1cd657b/backend/api_types.py), [고정 settings schema](https://github.com/Lightricks/LTX-Desktop/blob/8ffed888f3a9afdfbf137fa6193bf1cdc1cd657b/backend/state/app_settings.py), [고정 Remote 문서](https://github.com/Lightricks/LTX-Desktop/blob/8ffed888f3a9afdfbf137fa6193bf1cdc1cd657b/docs/remote-lan.md).
