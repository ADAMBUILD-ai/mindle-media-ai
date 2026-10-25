# MEDIA-AI-CORE-E2E-R1-20261025 — 동결 전 인수 준비

현재 상태: **BLOCKED_ASSET_INTAKE / PC 실행 NOT_EXECUTED**. 새 Windows 후보 제작, 설치 모델 교체, 배포 승인이 아니다. Build Gate=false, PR #23 Draft/HOLD 유지.

## 소스와 실행 경계

- 지시 인수 HEAD: 410ba721eac23e118a4b4ff7938dd44501118591.
- 보강 코드: 19d9cd562735e32b460d4b08278fd2bea9faa7a9.
- 건축 계획의 모델 길이를 자동 배분하던 경로를 제거했다. 지시 길이 불일치는 거부하며 prompt/response/REJECTED 원문을 보존한다.
- 제출 시 입력 SHA, 요청 원문 SHA, 실제 모델 응답, 조립 계획을 다시 대조한다. 과거 계획에 새 요청 결속 정보가 없으면 새 계획을 생성해야 한다.
- 격리 Linux 7B 자동 편집 평가와 실제 건축 30초·Supertonic 연속 제작 인수는 별개다. 아래 자료가 들어오기 전 작품 제작 완료를 주장하지 않는다.

## 실제 자료 인수

`INPUT_MANIFEST.json`의 clips에 실제 촬영 영상 1~12건을 등록한다. 각 영상은 path, sha256, bytes, duration_seconds, width, height, label, origin=real_capture, rights_status=CONFIRMED, source_or_owner, license_or_permission이 필요하다. label은 제공자 설명이며 모델 영상 이해 증거가 아니다.

모든 자료의 합산 사용 가능 길이는 최소 30초여야 한다. 별도 bgm 항목에는 오디오 파일·해시·크기·길이·출처·사용 조건·트랙 라벨을 등록한다. narration_script와 narration/original/bgm 음량(0..2)을 대표 지시에 따라 기입한다. 상대 경로는 Manifest 디렉터리 기준이다. 자동 다운로드·가짜 해시·권한 추정은 하지 않는다.

```bash
PYTHONPATH=src python -m media_ai.e2e_intake \
  docs/handoff/media-ai-core-e2e-r1-20261025/INPUT_MANIFEST.json \
  --output docs/handoff/media-ai-core-e2e-r1-20261025/INTAKE_RESULT.json
```

미등록/변조 시 exit 2와 BLOCKED_ASSET_INTAKE. 통과해도 PASS_INTAKE_TECHNICAL_ONLY이며 권한 선언 확인·작품/청취 검수는 사람이 수행한다. 현재 공개 Wikimedia 사진 5건은 소유자 실무 영상/BGM/원고 인수를 충족하지 않는다.

## 실행 요청 형식

아래는 작성 형식이며 미확정 수치나 원고를 임의 채워 실행하지 않는다.

> 선택한 기존 자료 모두로 30초 16:9 건축 홍보 영상을 구성해 주세요. 나레이션 원고는 "[확정 원고]". 나레이션 음량 [확정]%·원본 소리 음량 [확정]%·BGM 음량 [확정]%. 음성이 30초를 넘으면 실패로 종료하고 중간 영상과 기존 프로젝트를 보존하세요.

30초 고정 인수의 기본 길이 정책은 `reject`다. `extend_video`는 별도 명시 지시가 있을 때만 사용하며, 30초 초과 결과를 30초 고정 인수 PASS로 처리하지 않는다. `trim`은 현재 지원하지 않는다. 명시 원고는 정확히 한 쌍의 따옴표로 구분한다.

## General 완료 전 PC 착수 조건

1. 실제 입력 Manifest 기술 검사와 권한 확인.
2. 동결 소스에서 실제 Qwen 장면 계획 → FFmpeg 조립 → 실제 Supertonic 한국어 합성 → 단일 BGM/원본 소리 믹스.
3. 입력·모델 전체 분할 SHA·실행기·runtime·context·prompt/response·출력 해시 결속.
4. 실제 30초·16:9·H264/AAC, 디코딩/재생, 원고·음량 보존, 오류/취소 시 전체 완료 금지.
5. 저장·프로세스 종료·재시작·재열기·Export 검증. 단순 객체 재생성과 실제 프로세스 재시작은 별도 기록.
6. 장면·구도·스토리·자막 화면 검수와 한국어 음성 청취 기록.
7. 이후 최신 소스를 포함하는 Windows 후보 제작/모델 채택 승인. 기존 R3 EXE는 대체 증거가 아니다.

미지원 의미 기반 신규 장면 생성은 NOT_IMPLEMENTED, 실행하지 않은 경로는 NOT_EXECUTED. Hosted/Linux 통과를 Windows/대표 인수 완료로 승격하지 않는다. 과거 실패 일괄 재실행·main 병합·배포·예산 변경 금지.
