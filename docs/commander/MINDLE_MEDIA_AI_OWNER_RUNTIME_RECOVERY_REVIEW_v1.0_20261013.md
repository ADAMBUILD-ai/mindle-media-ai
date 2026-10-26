# MINDLE MEDIA AI — 실제 Runtime 복구 1차 검수

2026-10-13 · 개발 총괄의 직접 수정 및 실제 실행 증거

현재 상태는 `ACTIVE_OWNER_RUNTIME_RECOVERY`입니다. 전체 제품 완료·사무실 PC 실사용 PASS는 **false**입니다. 10월 8일의 General Work PASS와 기존 Windows ZIP은 이번 수정본의 배포·실사용 증거가 아닙니다.

## 실제 수정

1. **영상 AI 자동 편집의 잘못된 연결**: 고정된 “대상을 추적해줘” 명령을 제거했습니다. 실제 영상 프레임을 디코딩해 움직임·노출·선명도를 측정하고, 평균 점수가 높은 구간을 골라 FFmpeg로 편집합니다. 선택 시작점·길이·표본 수·측정값이 Job에 기록되고 저장·재열기·Export에 보존됩니다. 의미 이해·생성형 AI·모델 추론으로 주장하지 않습니다.
2. **사진 AI 보정의 고정값**: 밝기 분포의 10/50/90 백분위수와 RGB 분포로 보정값을 산출합니다. 실제 픽셀을 변경해 PNG로 저장합니다. 기존 7개 보정 항목과 비율·세로 사진 중앙 배치를 유지합니다. 모델 추론은 아닙니다.
3. **샘플 MEDIA 목록**: 정적인 가짜 파일명 대신 실제 원본 Job을 `/api/assets`에서 읽어 표시합니다. 클릭·키보드로 실제 원본을 선택할 수 있고 재시작 후에도 유지됩니다. 원본을 다시 선택한 상태가 저장 후 재열기에서 되돌아가던 순서 문제도 수정했습니다. 파일명에 내부 UUID를 노출하지 않습니다.
4. **모델 누락으로 기본 앱까지 종료되는 경로**: 시작 시 모델 파일 검증 오류를 readiness에 기록하고 기본 사진 기능은 유지합니다. AI Job은 검증을 다시 통과해야 실행되며, 파일 부재·불일치는 계속 차단합니다. 누락 상태를 AI 준비 완료로 표시하지 않습니다. `/api/runtime-readiness`를 추가했습니다.
5. **검증·패키지 게이트**: General Work를 대표의 명시적 지시에 따라 재개했습니다. Canonical CI에 실제 FFmpeg·한글 글꼴을 설치했습니다. 구형 패키지 workflow도 General Work 재개발 보류를 읽도록 수정했습니다.

UI HTML·CSS·브랜드/데모 자산과 기존 모델 adapter 26개 경로는 시작 HEAD 대비 동일 blob입니다. 레이아웃·색상을 재설계하지 않았습니다. 라이브 Marketing/AVORA·OpenAI 호출은 하지 않았습니다.

## 새 실제 실행

- 검증된 소스: `1493cb5e6886dc2b6c35252fff246ad6eb48ebe9`
- 실제 Chrome: https://github.com/ADAMBUILD-ai/mindle-media-ai/actions/runs/38414861948
- Canonical: https://github.com/ADAMBUILD-ai/mindle-media-ai/actions/runs/38414872423
- Python **83 PASS**, UI **2 PASS**, 브라우저 **10개 PASS**. pip check·컴파일·General 활성 Control Plane 검증 PASS.
- 실제 브라우저에서 원본 Import, MEDIA 원본 표시, 자동 영상 분석 편집, H.264 재생, 사진 자동 측정 보정, 세로 사진 픽셀 보정, 원본 재선택, 완전 서버/브라우저 종료·재시작, 목록·선택 결과·프로젝트 동일성, Export 다운로드를 검증했습니다.
- MediaError.code·readyState·videoWidth·currentSrc·currentTime을 실제 기록했습니다. 300초 Timeout을 늘리는 방식은 사용하지 않았습니다.
- 아티팩트 `11823561702`, ZIP SHA-256 `719e94c63e472b9f1e7658bf8782f173dacd30b4e566b662afb83cd02541cdc8`. 내려받은 아티팩트 CRC, Export CRC와 미디어 **7개 SHA-256**를 별도로 대조했습니다. 실제 화면도 육안 확인했습니다.
- 로컬은 **82 PASS / 한글 글꼴 부재 1 SKIP**입니다. Hosted CI에는 한글 글꼴을 설치해 **83 PASS**입니다.

## 실패·부수 실행 기록

초기 Canonical 실행 `38413580061`은 새 실제 영상 시험에 필요한 FFmpeg가 설치돼 있지 않아 실패했습니다. 시험을 건너뛰어 통과시키지 않고 의존성을 설치해 최종 Canonical PASS를 확보했습니다. 실패 로그를 보존합니다.

초기 PR 동기화에서 기존 패키지 workflow `38413580030`, `38413579985`가 PC state의 `package_build_allowed=true`만 읽고 자동 시작됐습니다. 제공된 GitHub 도구에는 실행 취소 기능이 없어 취소하지 못했습니다. 이를 새 수정본 배포나 fresh PHOTO inference로 간주하지 않습니다. 게이트 수정 이후 최종 실행 `38414872480`, `38414872884`의 실제 package job은 **SKIPPED**입니다. 이번에 수정된 Windows 배포 ZIP은 만들지 않았습니다.

## 기존 Windows 모델 증거 대조

기존 Windows 실행 `38121146106`의 검수 아티팩트 `11695148490`도 새 다운로드 없이 모델 추론을 재실행하지 않고 내려받아 CRC·SHA를 확인했습니다. 모델 Job·immutable revision·출력 해시가 기록돼 있고, 패키지 소스는 **8b28e712bf8e77052ca7efcc3459f7779597dc5a**입니다. 현재 수정된 소스와 대표 PC의 실행을 증명하지 않습니다.

특히 기존 `basic_photo`는 options에 brightness=10이 기록됐지만 **출력 SHA가 photo_import 출력과 동일**합니다. 이 기존 HTTP 시험만으로 실제 브라우저 밝기 보정이 동작했다고 인정할 수 없습니다. 이번에는 실제 브라우저 컨트롤을 눌러 보정한 결과를 저장·재열기·Export까지 검증했습니다. `HISTORICAL_WINDOWS_MODEL_READBACK.json`과 원본 receipt를 보존했습니다.

## 계속 남은 실제 작업

- 자연어 편집은 규칙 기반이며 생성형 계획·영상 의미 분석 에이전트는 미연결입니다. OpenAI는 승인된 키 연결 단계에서만 연결합니다. 로컬 분석 PASS를 생성형 AI PASS로 올리지 않습니다.
- PHOTO 배경 제거·4×, VIDEO 추적, 한국어 STT의 기존 모델 증거는 보존했습니다. 이번 브라우저 시험에서 새 모델 추론은 **0회**입니다. 현 수정 패키지의 모델 Runtime·대표 PC 실사용은 별도 실제 증거가 필요합니다.
- Timeline은 상태 표시이며 다중 클립·멀티트랙 편집기로 완성됐다는 주장을 하지 않습니다. 유사 이미지도 첨부 참고 이미지 색감 순위이고 외부 검색이 아닙니다.
- Marketing HTTP·승인 AVORA·광고 최종 출력은 **DEFERRED_EXTERNAL**입니다.
- 수정본 Windows 재빌드·원클릭 배포·대표의 실제 자료로 실행 검증은 **미완료**입니다. 기존 ZIP을 새 수정본으로 전달하지 않습니다.

다음 실행 순서는 생성형 계획/AI Runtime 연결의 실제 조건 확인 → 현재 모델 Runtime과 사무실 사용 경로의 실패 증거 확보 → 필요한 복구 → 수정본 Windows 검증·배포 → 실제 사용자 파일 편집·저장·재열기·출력입니다. PR #23은 계속 **HOLD / DO NOT MERGE**, main 병합·force push 없음.

상세 기능 연결·미완료 목록: `docs/evidence/media-ai-runtime-recovery-20261013/FUNCTION_BINDING_AUDIT.json`.
실제 실행과 다운로드 검증: 같은 폴더의 `RUNTIME_RECEIPT.json`, `EVIDENCE.json`, `INDEPENDENT_DOWNLOAD_VERIFICATION.json`, `ACTIONS_RUN.log`, `CANONICAL_BASELINE.log`.
