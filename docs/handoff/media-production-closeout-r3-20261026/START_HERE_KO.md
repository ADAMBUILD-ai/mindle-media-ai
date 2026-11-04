# MEDIA 실무 제작 마무리 — 단일 진입 지시서

작업: MEDIA-PRODUCTION-CLOSEOUT-R3-20261026. 기준일: 2026-10-26 KST.

## 현재 정확한 판정

기존 AI 편집 코어와 LTX 연결 코드는 있다. 실제 자료로 완성한 30초 영상은 아직 없다. LTX 모델 실증·대표 PC 시청/청취도 미완료다. 이 문서나 접수 도구를 제품 완료 또는 새 실행 승인으로 사용하지 않는다.

## 1. 한 파일만 채운다 — 대표/자료 담당

같은 폴더의 OPERATOR_INPUT.template.json을 별도 작업 폴더에 OPERATOR_INPUT.json으로 복사하고 다음을 채운다. 원고·음량·장문 정책은 빈 값에서 자동 지정하지 않는다.

- clips: 실제 촬영 영상 1~12개. 각 항목에 path, label, origin=real_capture, source_or_owner, license_or_permission, rights_evidence, rights_status=CONFIRMED. 필요하면 usable_start_seconds/usable_end_seconds.
- bgm: 음악 파일의 path, label, source_or_owner, license_or_permission, rights_evidence, rights_status=CONFIRMED.
- narration_script: 그대로 읽을 확정 한국어 원문.
- volumes: narration/original은 0~2, bgm은 0~1. 예시 배율을 승인값으로 자동 넣지 않는다.
- voice_length_policy: reject 또는 extend_video. 30초를 넘긴 결과는 고정 30초 인수 PASS가 아니다.

SHA·bytes·해상도·길이는 사람이 계산하지 않아도 된다. 접수 도구가 실제 파일에서 측정한다. 상대 경로는 OPERATOR_INPUT.json의 폴더 기준이며 회사 PC/NAS의 절대 경로도 허용한다. 자료를 중앙 서버로 업로드하거나 원본을 이동할 필요가 없다.

## 2. 읽기 전용 접수 — PC Work/자료 담당

Python 3.11 이상과 기존 승인된 FFprobe가 PATH에 있는 환경에서, 최신 동결 소스 또는 별도 SOURCE_INTAKE_TOOL_ONLY.zip을 사용한다. ZIP은 EXE·설치본·모델이 없는 접수용 소스이며 Windows 제품 후보가 아니다. 도구는 FFprobe를 설치하거나 다른 실행기로 대체하지 않는다.

```powershell
python scripts/prepare_media_production_intake.py --request "<OPERATOR_INPUT.json 전체 경로>" --out "<아직 존재하지 않는 새 접수 폴더>"
```

반환 파일: OPERATOR_INPUT_SNAPSHOT.json, INPUT_MANIFEST.json, INTAKE_RESULT.json, ASSET_INTAKE.json, PREPARATION_RECEIPT.json. 원본 영상·음악·기존 프로젝트는 수정하지 않는다. 기존 출력 폴더 재사용은 거부한다. 사용자가 미리 기입한 SHA·길이·크기·해상도가 틀려도 도구가 정답으로 바꾸지 않는다.

exit 2면 PREPARATION_RECEIPT.errors에 적힌 누락만 보완하고 새 폴더로 다시 접수한다. 이는 기술 검사 재실행이 아니라 실제 입력 접수다. exit 0도 기술적 접수일 뿐 권리의 법적 확인·모델 실행 승인·작품 품질 승인이 아니다.

## 3. General Work 인수

담당자가 접수 폴더와 원본 경로에 접근 가능한 환경에서 INPUT_MANIFEST.json과 PREPARATION_RECEIPT.json을 반환한다. 경로 문자열만 전달하고 General이 그 PC/NAS를 실제로 읽었다고 가정하지 않는다. 실제 파일을 가진 환경의 검사 결과를 소스 SHA·Manifest SHA와 결속한다.

접수된 새 INPUT_MANIFEST.json만 해당 실행의 원본으로 사용한다. 기존 R2 빈 Manifest를 동시에 수정하거나 과거 ASSET_INTAKE를 PASS로 올리지 않는다. 실행기에 --manifest로 새 원본의 정확한 경로를 지정한다.

## 4. 엔진·실행 범위 — General/PC Work

먼저 기존 자료로 30초 한 편을 완성한다. 신규 장면 생성 모델 설치를 이 경로의 불필요한 선행 조건으로 만들지 않는다. 다만 Qwen 자동 판단은 검증한 7B 구성과 실제 Supertonic을 요구하며 실패한 1.5B로 대체하지 않는다.

- Linux General: 고정 7B/Supertonic identity를 확인하고 기존 [소스 E2E 실행 절차](../media-ai-core-e2e-r2-20261025/EXECUTION_KO.md)를 따른다. Windows 빌드 승인은 Linux 소스 평가의 선행 조건이 아니다.
- Windows 소스: 별도 [Windows 7B 채택 요청](../media-ai-core-e2e-r2-20261025/WINDOWS_7B_ADOPTION_REQUEST.json)과 정확한 소스·Manifest·엔진 구성에 결속한 승인 범위를 확인한다. 기존 설치 모델은 보존한다.
- LTX 신규 장면: [독립 어댑터 R2 절차](../../commander/MEDIA_LTX_SOURCE_ADAPTER_R2_KO.md)를 별도 수행한다. 시험 서버 성공을 실제 LTX 추론으로 올리지 않는다.
- 신규 EXE: 현재 Build Gate=false다. 필요할 때 정확한 후보 제작 승인을 별도로 받는다. 기존 R3 EXE가 최신 기능을 포함한다고 가정하지 않는다.

## 5. 완성 출구

실제 Qwen 장면 계획 → 30초 조립 → 새 Qwen 음향 계획 → Supertonic 한국어 합성 → BGM/원본음 단일 믹스 → 영상·오디오 전체 디코딩 → 저장 → 실제 프로세스 종료·재시작 → Reopen → Export 내부 SHA·CRC → 화면·한국어 음성 사람 검수 순으로 완료한다. 단계 실패 시 기존 유효 파일을 보존하고 뒤 단계는 NOT_EXECUTED로 남긴다.

현재 반환 판정은 General 접수·인계 준비 완료 / 실물 30초 제작 BLOCKED다. 필요한 자료는 1번의 단일 파일에 모은다. Windows 엔진·후보 승인은 해당 실행 경로에서만 별도 판정한다.

Build Gate=false / PR #23 Draft/HOLD / main 병합·배포·추가 예산 변경 금지 유지.
