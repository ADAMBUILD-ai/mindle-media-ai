# 실제 자산·승인 일괄 접수표

작업 ID: `MEDIA-AI-CORE-E2E-R2-20261025`

아래 항목을 한 번에 제출한다. 값을 모르면 비워 두며 추정값을 쓰지 않는다. 파일은 이 폴더 아래 `assets/`에 두고 `INPUT_MANIFEST.json`에는 이 폴더 기준 상대 경로를 적는다.

| 항목 | 제출 내용 | 담당 | 형식 | 자동 검사 |
|---|---|---|---|---|
| 실제 영상 1~12개 | 원본 파일, 장면 라벨, 사용 구간 | 자산 제공자/대표 | MP4/MOV 등 실제 촬영본 | SHA·bytes·해상도·길이·영상 스트림·합계 30초 이상 |
| 영상 권리 | 출처/소유자, 허용 범위, 확인 근거 | 대표/권리 확인자 | 각 clip의 `source_or_owner`, `license_or_permission`, `rights_status=CONFIRMED` | 누락 시 차단; 최종 법적 확인은 사람 |
| BGM | 실제 음악과 제품 사용 조건 | 대표/권리 확인자 | WAV/MP3/M4A/FLAC/OGG, 1~32MB | SHA·bytes·길이·오디오 스트림·권리 필드 |
| 한국어 원고 | 변경 없이 읽을 확정 원문 전체 | 대표 | UTF-8 문자열, 따옴표 자체는 제외 | 빈 원고 차단; 계획의 원문 일치 검사 |
| 음량 | 나레이션/원본음/BGM | 대표 | 배율: 나레이션·원본 0~2, BGM 0~1 | 범위·유한 숫자·계획값 일치 |
| 장문 정책 | 음성이 길 때 처리 | 대표 | `reject` 또는 명시 승인된 `extend_video` | 다른 값 차단; 30초 최종 Gate는 실제 길이 별도 확인 |
| Windows 7B 격리 채택 | 모델 배치·실행기·메모리 범위 | 모델 책임자/대표 | 승인 ID와 허용 경로 | 승인 전 설치·교체·실행 금지 |
| 후보 제작 | 최신 소스 포함 Windows 후보 | 빌드 승인자 | Build Gate 승인 ID | 현재 false이므로 제작 금지 |

접수 검사:

```powershell
$env:PYTHONPATH='src'
python -m media_ai.e2e_intake docs/handoff/media-ai-core-e2e-r2-20261025/INPUT_MANIFEST.json --output docs/handoff/media-ai-core-e2e-r2-20261025/INTAKE_RESULT.json
```

exit 0과 `PASS_INTAKE_TECHNICAL_ONLY`가 모두 필요하다. 판정은 `INTAKE_RESULT.json`만 권위가 있으며 `ASSET_INTAKE.json`은 과거 재고·누락 기록이다.
