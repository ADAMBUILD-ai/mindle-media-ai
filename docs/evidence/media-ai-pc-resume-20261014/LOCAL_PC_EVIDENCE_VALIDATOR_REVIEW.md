# 사무실 PC 신규 증거 접수 검수기 — 2026-10-15 KST

현재 후보는 변경하지 않는다. source `0e4e12a9e4c758f202c6ebb5085df5a542bb6314`, producer run `38497304486`를 유지한다. PR23 HOLD / DO NOT MERGE, build gate CLOSED, main 병합 금지.

## 실행
PC Work에서 신규 실행 증거를 receipt.json과 같은 폴더 아래 보관한 후 실행한다.

```text
python scripts/validate_local_pc_acceptance.py EVIDENCE_DIR/receipt.json
```
이 도구는 개발 검수 전용이다. 직원용 제품 설치에 Python을 요구하지 않으며 기존 후보를 재빌드하지 않는다.

## Receipt 구조
`scope=OFFICE_PC_NEW_EXECUTION`, `source_sha`, `zip_sha256`, `runtime_id`는 현재 후보와 일치해야 한다. `execution_id`, `started_at`, `finished_at`, `browser_version`을 기록한다. `full_product_pass=false`를 유지한다.

각 파일 근거는 `{path: 상대경로, sha256: 실제 해시, bytes: 실제 크기}` 객체다. `runtime_identity`, `environment`, `approved_ui_screenshot`에 실제 파일을 연결한다.

- `inputs`: 준비한 8개 입력 각각의 `id`, `file`, `result` 파일 근거.
- `buttons`: 60개 각각의 `id`, `selector`, `disposition`, `reason`, `evidence`. disposition은 active/disabled/status-only/unsupported. active의 `result`는 실제 PASS/FAIL/BLOCKED.
- `model_jobs`: segment/upscale/track/transcribe 각각의 실제 `execution_id`, `request_id`, `job_id`, `receipt`, `output`. 현재 실행의 호출만 사용한다.
- `media`: 실제 `MediaError_code`, `readyState`, `videoWidth`, `currentSrc`, `before_time`, `after_time`, `evidence`를 연결한다. 실패 값도 원본대로 기록한다.
- `lifecycle`: `single_instance`, `save`, `cold_close`, `reopen`, `export_zip`, `export_mp4`, `play_seek_audio` 각각의 실제 파일 근거.

## 판정 한계
누락은 EVIDENCE_INCOMPLETE(exit 1). 파일/해시/후보 identity/필수 항목이 갖춰지면 EVIDENCE_COMPLETE_REQUIRES_RUNTIME_REVIEW(exit 0). 완전한 FAIL 기록도 접수할 수 있다. exit 0은 기능 성공이나 office PC PASS를 뜻하지 않는다.

이는 제출 내용의 정합성 검사이며 실행 사실 인증, 픽셀 품질, 한국어 STT 정확도, 재생 성공, 60개 기능 성공을 자동 인증하지 않는다. 원본 receipt/log와 실제 output의 별도 검토가 필요하다. owner_pc_pass 및 full_product_pass를 이 도구가 승격하지 않는다.

## 실제 검증
2026-10-15 KST General runtime: 경계 테스트 6개 PASS. 누락된 입력/버튼, 이전 후보, 다른 실행의 job, 파일 변조, 절대경로/상위경로/symlink 탈출, 최종 PASS 오표기를 거부했다. 합성 파일은 테스트 전용으로 실제 PC 증거에 포함하지 않았다.

새 PC 실행 증거는 이 시점 원격 HEAD/Actions/PR23 댓글 조회에서 발견되지 않았다. 기존 Windows/Linux PASS를 사무실 PC PASS로 재사용하지 않는다. UI/모델/패키지 bytes 변경 없음. OpenAI 연결 및 Marketing/AVORA는 기존 Gate 유지.
