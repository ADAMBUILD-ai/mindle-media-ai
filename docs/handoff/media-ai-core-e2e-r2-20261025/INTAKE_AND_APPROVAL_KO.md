# R2 단일 자료·승인 접수표

작업 ID: MEDIA-AI-CORE-E2E-R2-20261025. 현재 실제 30초 실무 E2E는 BLOCKED다.

## 자료의 권위와 갱신

이 디렉터리의 `INPUT_MANIFEST.json`만 실행 입력의 원본이다. `ASSET_INTAKE.json`은 인수기가 같은 Manifest SHA를 넣어 생성하는 파생 상태다. 인수기 실행 시 `INTAKE_RESULT.json`과 같은 결과를 기록한다. 원본 수정 뒤 과거 ASSET_INTAKE 상태를 재사용하지 않는다. 실제 실행기는 상태 문서를 신뢰해 우회하지 않고 원본 파일과 Manifest를 다시 검사한다.

R1의 ASSET_INTAKE와 RESULT는 당시 사실을 보존한 이력이다. 현재 접수 상태를 수동으로 동기화하거나 PASS로 바꾸지 않는다. 새 자료 접수는 이 R2 원본에만 한다.

## 한 번에 제출할 항목

| 항목 | 담당 | 제출 위치/형식 | 검사와 다음 동작 |
|---|---|---|---|
| 실제 촬영 영상 1~12개 | 대표/자료 담당 | 회사 로컬 또는 NAS 원본 경로와 clips 배열 | SHA/bytes/해상도/길이/선택 구간 검사 후 제품 import |
| 장면 설명·사용 구간 | 자료 담당 | 각 clip의 label, usable_start_seconds, usable_end_seconds | 사용자 설명으로 기록; 영상 의미 인식 증거 아님. 제품 FFmpeg 편집 API로 구간 제한 후 장면 계획 |
| 영상 사용 권한 | 대표/자료 담당 | source_or_owner, license_or_permission, rights_status=CONFIRMED, rights_evidence | 허락 문서/계약/라이선스 확인 근거 경로·링크. 인수기는 선언·참조 존재만 검사; 권리 확인은 담당자 책임 |
| 음악과 사용 조건 | 대표/자료 담당 | bgm 객체와 실제 오디오 파일 | 지원 형식 WAV/MP3/M4A/FLAC/OGG, 32MB 이하. 동일 권리 필드와 SHA·길이 검사 |
| 한국어 확정 원고 | 대표 | narration_script 전체 | 1~3000자. 현 제품 명령 구분자와 충돌하는 큰따옴표는 사전 편집 확정 필요. 자동 변경 금지 |
| 음량 3개 | 대표 | volumes.narration/original/bgm | 나레이션·원본 0~2, BGM 0~1. 예: 0.8=80%. 미접수 값 자동 지정 금지 |
| 장문 정책 | 대표 | voice_length_policy=reject 또는 extend_video | 30초 고정 인수는 reject 권장 절차. extend_video가 명시돼도 30초 초과 결과는 고정 30초 PASS 아님 |
| Windows 7B 평가 승인 | 대표/모델 담당 | WINDOWS_SOURCE_APPROVAL.template.json에서 별도 승인본 생성 | 승인한 source SHA·Manifest SHA·engine config SHA 일치 때만 Windows 소스 격리 실행 |
| 대상 PC 실제 사양 | PC 담당, 읽기 전용 | collect_media_pc_readiness.py 결과 JSON | 가용 RAM·디스크·실제 엔진 파일 해시 확인. Linux 관측값 대입 금지 |
| 신규 Windows 후보 제작 | 대표/빌드 담당 | 별도의 정확한 Build Gate 승인 | 현재 false 유지. 소스 평가 승인으로 빌드/배포/설치 교체를 승인한 것으로 해석 금지 |

영상 clip 필수 필드:

`path, sha256, bytes, duration_seconds, width, height, label, origin=real_capture, rights_status=CONFIRMED, source_or_owner, license_or_permission, rights_evidence`

사용 구간을 제한하면 `usable_start_seconds`, `usable_end_seconds`를 함께 기입한다. 생략 시 파일 전체가 허용 구간이다. 각 사용 구간에서 최대 30초까지 합산한 길이가 총 30초 이상이어야 한다. 원본 음량을 0보다 크게 요구하면 실제 원본 오디오가 있는 영상이 적어도 하나 필요하다.

BGM 필수 필드는 영상 공통 필드 중 `width, height, origin, usable_*`를 제외한다. path는 이 Manifest 디렉터리를 기준으로 해석하며 로컬/NAS의 절대 경로도 허용한다. 테스트용 색상 영상·테스트 톤·임의 원고를 실무 자료로 등록하지 않는다.

## 승인 요청 범위

1. **자료·편집 의도 접수:** 위 7개 입력 항목을 확정한다. General 소스 평가에는 새 Windows 빌드 승인이 필요하지 않다.
2. **Windows 모델 평가:** 기존 1.5B와 Supertonic을 보존한 별도 경로에서 승인한 7B 구성으로 소스 평가한다. 모델 다운로드/배치가 필요하면 그 범위도 명시 승인해야 한다. 실행기는 다운로드나 설치를 하지 않는다.
3. **제품 후보 제작:** 새 EXE가 필요할 때 별도 Build Gate를 열고 최신 동결 소스를 포함한다. 이 시점에만 승인 후보의 공식 lifecycle/UI 검수 절차를 적용한다. 기존 R3로 최신 기능 완료를 주장하지 않는다.

현재 템플릿의 approved=false와 빈 입력을 유지했다. 요청서를 만드는 작업이 대표 승인 자체는 아니다.
