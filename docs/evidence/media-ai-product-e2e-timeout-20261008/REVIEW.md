# MINDLE MEDIA AI — 업스케일 E2E 실패 검수 및 수정

대상: Actions 37638260222 / Artifact 11491720522 / source 3615d1080a97d5102d1c90866a3db945b2a17d9c.

## 판정
PASS_TARGETED_REGRESSION_ONLY_FULL_PRODUCT_E2E_PENDING. PR #23 HOLD / DO NOT MERGE 유지. main/prod 변경 없음.

## 직접 증거
다운로드한 ZIP SHA-256: b45a2ee7163af6a4c85e9c5b31348015495234d496698cdb574b4388d1cf91fb — Actions 업로드 로그와 일치.
ZIP 9개 파일 중 JOB_EVIDENCE 2개: 원본 import TESTED_PASS 및 upscale FAILED. segment 결과나 SAM 추론 증거 없음.
업스케일 실패 문구: offline mode is enabled; HF_HUB_OFFLINE을 해제하라는 모델 저장소 조회 오류. 실패 state=queued. 모델 추론 자체의 오류로 볼 증거는 없다.

## 원인 구분
1. 모델 처리 경로: execute_isolated가 원격 모델 캐시 실행에도 직원 오프라인 패키지 전용 HF_HUB_OFFLINE/TRANSFORMERS_OFFLINE 및 네트워크 금지, 토큰 제거를 적용했다. child의 _alternatives() private revision 조회가 실패했다.
2. 작업 상태 조회: 이 경로는 비동기 job polling이 아니라 /api/jobs의 동기 HTTP 응답이다. polling 장애로 판정할 근거가 없다. UI가 실패를 표시해도 E2E는 읽지 않아 300초 Timeout으로 변환했다.
3. 명령/UI 연결: mindlePhotoCommand의 AI 전달 키워드에 분할이 빠져 테스트 명령을 소비했다. import가 actual-output으로 표시되고 E2E가 operation을 확인하지 않아 분할 완료로 잘못 읽었다. 이후 실패한 upscale에서는 새 job ID가 오지 않았다.

## 수정 범위
- src/media_ai/product_runtime.py: local package와 remote cache worker 환경을 분리. local package는 오프라인 및 네트워크 금지, 토큰 제거 유지. remote worker는 토큰을 프로세스 환경으로 전달하고 immutable cache 검증 경로 사용. 모델/라이선스/해시 검증은 유지.
- ui/photo_workspace.js: 분할 명령을 기존 모델 라우터로 전달.
- ui/product_integration.js: 미리보기 host에 보이지 않는 operation 식별값 추가. HTML/CSS/레이아웃 변경 없음.
- model_scout/run_product_e2e.py: import/segment/upscale/tracking을 구분하고 이미지 decode·영상 ready 상태 확인; 명시적 실패는 즉시 실패; 실패 DOM/스크린샷/API 증거 보존. 현재 확정 UI의 STT 영상 유지 동작을 검수. import 작업을 최종 모델 PASS 집합에서 제외하고 오래된 PR 번호 10 제거.

## 실행 검증과 한계
Python 6/6 PASS. 원격/로컬 worker 환경 분리를 실제 child process로 검사하되 모델 서비스는 stub 사용. wait_preview 테스트는 DOM/WebDriver test double 사용.
JS: 분할/배경 제거/업스케일 3개 명령의 모델 라우터 전달 PASS, 미지원 명령 처리 유지 PASS. DOM test double 사용.
Python compile 및 JS syntax PASS.
실제 가중치 추론, Selenium 전체 실기, Marketing HTTP·AVORA 자산·숏폼 Preview·MP4 실기는 이번 로컬 검증에서 수행하지 않았다. 해당 항목을 PASS로 승격하지 않는다.

## 후속 검수
수정 커밋에 대한 새로운 GitHub Actions 결과만 검수한다. 기존 실패 run 재실행은 이전 SHA를 다시 실행하므로 수정 검증이 아니다. segment/upscale/tracking/transcribe 각각 TESTED_PASS+입출력 해시 및 UI 실제 로드, save/export 결과가 모두 있어야 기본 제품 E2E PASS. 이 기본 E2E가 PASS여도 Marketing/AVORA/광고 숏폼 MP4 통합이나 clean Windows 배포 PASS를 대신하지 못한다.

## 최종 실기 재검수 — 2026-10-08

최종 판정: **PASS_PHOTO_UPSCALE_PREVIEW_FIX_FULL_E2E_FAIL_VIDEO_PREVIEW**.
수정 커밋: 0e541626b7e0b6e9b5990e3ba3ead791dc98dd61. 의존성 보완: 67eb55548ee9d36d8ee6b5791c3f5c8be5ea449f.

- 새 실기 run 37735046818 / Artifact 11531386885.
- 사진 segment와 upscale은 실제 모델 TESTED_PASS. wait_preview가 operation과 실제 image decode까지 확인한 뒤 영상 단계로 진행했다.
- 업스케일: 480×270 → 1920×1080, 실제 추론 약 292.7ms, output SHA-256 a6dcc897c81f9cb581f8317a626e5f3e11eae5601cecb11fef7f1a8c5d0498f8.
- 업스케일 입력 SHA가 segment의 photo_overlay.png 출력 SHA와 일치: c5e56328a45d29724f437473a1c634b62255d2a81976317b7d28992e2e59a84f. 연속 작업 연결 확인.
- 영상 tracking backend TESTED_PASS, HTTP API 201 및 preview GET 200. DOM에도 tracking operation과 정확한 job ID가 남았다. 그러나 browser readyState/videoWidth 조건이 통과하지 않아 전체 E2E FAIL.
- ffprobe: 결과 파일 codec=mpeg4, tag=mp4v, 512×292, yuv420p. 기존 adapter가 mp4v로 생성하는 사실과 부합한다. 브라우저 코덱 호환 문제가 유력하나 MediaError code를 기록하지 않았으므로 확정 원인으로 단정하지 않는다.
- STT·프로젝트 저장·내보내기는 이번 재검수에서 NOT_REACHED. Marketing HTTP·AVORA 자산·광고 숏폼 Preview·MP4 통합도 VERIFY_REQUIRED 유지.
- 기본 CI 37735401505 SUCCESS: Python 64 PASS / UI 2 PASS / Evidence 동기화·패키지 소스 검증 SUCCESS.

## 다음 수정 범위
사진 수정은 추가 대기시간 확대나 모델 교체 없이 유지한다. 별도 영상 결함은 브라우저 MediaError/readyState/videoWidth/currentSrc를 기록하고, tracking 출력의 원본/마스크/추적 JSON을 보존하면서 기존 FFmpeg 경로를 이용한 H.264(yuv420p, faststart) 미리보기 생성으로 좁혀 검증해야 한다. 브라우저 실제 decode 후 STT→save/export까지 재검수한다. 이 보고서는 영상 코덱 수정이나 전체 E2E PASS를 주장하지 않는다.

PR #23은 역사적 통합 경로이므로 HOLD / DO NOT MERGE 유지. main 변경·병합 없음.
