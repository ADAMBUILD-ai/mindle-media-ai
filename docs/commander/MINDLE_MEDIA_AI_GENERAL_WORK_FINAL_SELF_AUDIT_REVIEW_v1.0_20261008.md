# MINDLE MEDIA AI General Work 최종 전수 자체검수

**PASS_MINDLE_MEDIA_AI_GENERAL_WORK_FINAL_SELF_AUDIT_READY_FOR_PC_WORK**

활성 Epoch: `MEDIA-AI-20261008-GENERAL-WORK-FINAL-SELF-AUDIT-R1`.
기준 HEAD `985f3a7b464e53318a0f50b8655640ceb336d36b`에서 전수 검수와 확인된 결함 수정을 진행했다.
최종 Runtime 검증 소스는 `92897f4ff943d30d788416dbb10324f3df2b9427`이다.

이 PASS는 **활성 기본 제품 기능과 지시서가 허용한 미구현 기능의 명시적 비활성화**에 대한 General Work 완료 판정이다. 이미지 생성·되돌리기·템플릿 등이 구현됐다는 뜻이 아니다. Marketing/AVORA 실제 광고 제작과 Windows 직원용 Runtime 배포 PASS도 아니다.

## 실제 실행과 독립 확인

- [최종 브라우저 Runtime 실행 37752630381](https://github.com/ADAMBUILD-ai/mindle-media-ai/actions/runs/37752630381): **SUCCESS**. 실제 Chrome 검수 75건 PASS.
- [검수 아티팩트 11538633312](https://github.com/ADAMBUILD-ai/mindle-media-ai/actions/runs/37752630381/artifacts/11538633312): 36,550,491 bytes, ZIP SHA-256 `1809640a89cac062e6f7a56e79005a640581c9e4784640e2ec3bc2d7099c0ff8`. 직접 다운로드 후 CRC 검사 PASS.
- Python **77 PASS**, UI **2 PASS**, `pip check`, 컴파일, General Work validator PASS. PC Work validator는 의도된 `PC_WORK_PAUSED_WAITING_GENERAL_WORK_PASS`를 반환했다.
- [Canonical baseline 37752630409](https://github.com/ADAMBUILD-ai/mindle-media-ai/actions/runs/37752630409): SUCCESS. FFmpeg/CJK 글꼴이 설치된 제품 검수 runner의 77 PASS를 Runtime 회귀 기준으로 사용한다.
- 이전 PHOTO/VIDEO 모델 실행, 외부 마감 실행, 두 패키지 작업은 **SKIPPED**. 새 모델 취득·PHOTO 추론 재실행·직원 패키지 생성 없음.

CI 성공 여부만으로 PASS하지 않았다. 실제 버튼과 입력, PNG 픽셀 변화, MP4 디코드와 재생/탐색, 새 브라우저·새 서버에서의 복원, 다운로드한 ZIP의 모든 결과 해시를 검증했다. 원본 Runtime 판정은 `RAW_RUNTIME_EVIDENCE.json`에 보존하고, 전수 인벤토리·독립 다운로드 검사·readback을 `EVIDENCE.json`에 연결했다.

## 확인된 결함 20건과 처리

18건은 코드 수정으로 닫았고, 2건은 지시서의 명시적 비활성/미구현 분류 규칙으로 닫았다. `GAP_REGISTER.json`에는 원인, 수정 경로, 대상 테스트 및 실제 Runtime 항목을 개별 연결했다.

| 결함 묶음 | 수정 결과 | 실제 확인 |
|---|---|---|
| 저장 실패 후 이전 프로젝트 Export, 알 수 없는 Job 누락, 비원자적 저장 | 저장 실패 시 Export 중단, Job/UUID 검증, 임시 파일+원자적 교체 | 수정 편집과 frozen 모델 Job 저장·완전 종료·재열기, 실패 시 Export 요청 없음 |
| Export에서 누락/변조된 파일 무시 | 누락/해시 불일치 명시적 실패 | 실제 UI 다운로드 2종 CRC와 모든 미디어 SHA 확인, 누락/변조 대상 테스트 |
| 잘못된 입력으로 이전 File/Preview 교체, 같은 파일 재선택 무반응 | 실패 시 이전 입력 유지, 입력 선택값 정리 후 같은 파일 재가져오기 | corrupt PNG 오류 후 이전 사진 유지, 같은 영상 반복 import와 도구 실행 |
| 결과 이벤트와 File 상태 갱신 경쟁, 진행 중 저장, 중복 클릭/HTTP 요청 | 결과 수신을 await, 진행 상태 저장 차단, 동일 성공 요청 재생/충돌 거부 | 실제 이중 클릭이 Job 1개만 생성, 진행 중 저장 차단, 실제 HTTP replay/422 |
| 연결 없는 메뉴와 command chips | 실제 프로젝트·Job·저장소 조회와 새 프로젝트/기존 프로젝트 열기, 편집 입력 연결 | 실제 메뉴·dialog·선택 프로젝트 복원·스타일/톤/길이/비율/전송 실행 |
| 미구현 버튼과 가짜 enabled 선언 | 11개 버튼 명시적 disabled, before-after/batch 미구현 표시, timeline은 실제 상태 표시+transport seek | 실제 DOM 94개 control 인벤토리, 기존 표시/배치/색상 보존 |
| 지원하지 않는 VIDEO 명령이 추적으로 전달, 실패 전 입력 소실/이전 문장 재등장 | 지원 명령 검증, 실패/재시도용 입력 유지, DOM-상태 동기화 | unsupported 명령 오류·입력 보존, 실제 PHOTO/VIDEO 명령 편집 |
| 기본 시작의 HF token 의존 | 기본 편집은 token 없이 시작, 모델 미준비는 즉시 명시적 실패 | 새 실제 서버/Chrome 시작, 추적/STT/업스케일 버튼의 실제 HTTP dispatch와 오류 표면 |
| Linux 한국어 자막의 Windows 글꼴 고정 | 설치된 CJK 글꼴 선택; 없으면 명시적 실패 | 실제 한글 자막을 MP4에 렌더링하고 Chrome 디코드·화면 확인 |
| legacy 클립 합치기의 literal `\\n`, 작은따옴표 경로, 16:9 강제/codec 설정 누락 | 실제 줄바꿈·경로 escaping, 기본 원본 비율, H264/yuv420p/faststart | 공백·한국어·작은따옴표 파일명 대상 FFmpeg 테스트와 실제 8초 합치기 |
| 배경 제거가 빨간 SAM overlay를 반환 | verified SAM mask를 원본 사진의 alpha로 적용하는 별도 derivative | 실제 기존 버튼으로 RGBA 생성, alpha `(0,255)`, 원본 480×270 유지, original mask/overlay 해시 유지, 저장/Export |
| VIDEO 탐색 실패 | HTTP `Accept-Ranges`/206/Content-Range 및 잘못된 범위 416 | Chrome currentTime/seekable, 실제 range 응답, 재생/일시정지/탐색 |
| 참고 이미지 Blob URL 누수 | 제거/거부된 첨부 URL revoke | 실제 첨부·색감 유사도 정렬·제거와 회귀 테스트 |
| 후속 VIDEO 편집 후 BGM 상태 표시 누락 | 선택 BGM 재사용 시 기본 음량을 명시적으로 저장 | 실제 BGM output은 유지되고 Audio Track은 “추가한 배경음악” 표시; 저장·재열기 |

초기 실패 실행도 숨기지 않는다. `37749458686`은 유사 이미지의 비동기 decode 완료를 기다리지 않은 검수 도구 오류, `37750027825`는 실제 seek 실패, `37750501514`는 같은 파일 재import 무반응, `37751080466`은 command 상태 동기화 실패였다. Timeout을 늘려 해결하지 않았다. `PREVIOUS_ATTEMPTS.json`에서 소스/아티팩트/해시와 원인을 구분한다.

## 기능별 PASS 범위

`FEATURE_INVENTORY.json` 및 `FEATURE_INVENTORY.md`에 **115개 항목**을 UI 위치·소스·API·의존성·입출력·저장·오류·증거와 함께 기록했다. 분류는 PASS 92, PARTIAL 1, NOT_IMPLEMENTED 16, DEFERRED_EXTERNAL 6, FAIL 0이며 UNKNOWN은 0이다. PARTIAL 1개는 이 작업에서 실행하지 않는 향후 PC Work Windows 런처/업데이트/종료 범위다.

- PHOTO 가로/세로 import, 원본 비율·중앙 Auto Fit, 보정 7종의 **실제 픽셀 변화**, crop/resize/rotate/flip, 자동 보정·색감·흑백 스타일·전체 사진 부드럽게 보정, 첨부 이미지 **색감 histogram** 유사도 경로 PASS. 인물 보정은 얼굴 전용 모델 추론을 주장하지 않는다.
- VIDEO 재생/일시정지/시작/끝/음소거/seek/fullscreen과 crop/분할/회전/속도/전환/효과/하이라이트/9:16 변환/기본 보정/노이즈·흔들림/한글 자막/BGM 및 후속 편집 PASS. 효과는 FFmpeg vignette, 하이라이트는 frame-difference heuristic이며 LLM 기획이나 별도 AI 효과 모델 추론 PASS가 아니다. 원본 음량 옵션은 실제 FFmpeg 경로에 연결됐으며 이번 검수는 기본 1값을 사용했다; 별도 loudness 품질 벤치마크를 주장하지 않는다.
- 새 프로젝트/프로젝트 목록·선택 열기/실제 Job 내역/저장소·도움말, 진행 중 저장 차단, Save/full close/Reopen, 실제 UI Export·다운로드·무결성 PASS.
- 제목 **MINDLE MEDIA AI**, 기존 VIDEO 구조, PHOTO 가로 기본·세로 중앙 여백, navy/VIDEO blue-cyan/PHOTO purple-magenta, 광고 숏폼 entry 보존. 기존 CSS·브랜드/승인 이미지·Control Plane은 원격 blob 기준 동일하다. `APPROVED_UI_HEADER.png`, `PORTRAIT_AUTO_FIT.png`, DOM 및 readback 참조.

### Frozen 모델 PASS 재사용

PHOTO 분할/4× 및 tracking/Whisper inference 원본은 소스/미디어 해시를 검증해 재사용했다. SAM·Intel SISR·Whisper adapter와 확정 출력 원본은 변경하지 않았다. 이번 실행에서는 실제 browser decode/play, 재열기/저장/Export 및 변경된 UI dispatch를 재확인했다. 모델 미준비 오류 시험을 새 inference PASS로 세지 않았다.

| 항목 | 확정 SHA-256 / 범위 |
|---|---|
| PHOTO segmentation 원본 overlay | `c5e56328a45d29724f437473a1c634b62255d2a81976317b7d28992e2e59a84f` |
| PHOTO 4× 출력 1920×1080 | `a6dcc897c81f9cb581f8317a626e5f3e11eae5601cecb11fef7f1a8c5d0498f8` |
| tracking 원본 mp4v | `41a9c54966fe89a636873839402fdc3d2530fbb80e8eb2c3559f0fc815acbe69` |
| 실제 재생 H264 derivative | `451e9c9dd51a9e3f01412873b8293a9a0d60af542f7a971dd09529fc8de5ad4e` |
| 새 투명 배경 derivative | `0866e968c0bc9c82ef0fd789562d3e8edfbaaf89a88476dae870afb657b8173a` |

한국어 STT의 실제 inference/문장/복원은 기존 `37738880868`의 verified receipt를 재사용한다. WER/reference 품질 벤치마크는 측정하지 않았다. 새 한글 자막 MP4와 BGM 후속 편집 MP4는 실제 이번 실행 출력으로 저장했다.

### 실제 Export

| 실제 UI 다운로드 | 크기 | SHA-256 | 확인 |
|---|---:|---|---|
| 수정된 PHOTO/VIDEO 전체 작업 ZIP | 6,317,540 | `c0dbb827e44b13af9673020c3e9dc7ae7a369b4e4b71368160d04254e553545a` | full restart 뒤 UI download, ZIP CRC와 모든 media hash PASS |
| PHOTO/VIDEO/STT frozen 작업+새 RGBA derivative ZIP | 3,067,373 | `40255d8cde6da26e1c4e6743dc73b50d6f809ea7ef8fe6b0d0d94e849ceb49bb` | UI download, ZIP CRC와 모든 media hash PASS |

전체 입력·Job·프로젝트·MP4·다운로드 ZIP은 최종 Actions artifact에 보관된다. 핵심 실제 화면·새 RGBA·한글 자막/BGM MP4는 이 Evidence 폴더에도 보존했다.

## 미구현/보류를 PASS로 바꾸지 않은 항목

설정/계정/템플릿, 이미지 생성, 사진 이동/undo/redo, VIDEO 참고 이미지 기반 편집, native 최소화/종료는 **NOT_IMPLEMENTED·disabled**다. before-after/batch, editable keyframe/clip context/range-delete/multitrack은 활성 구현을 주장하는 선언을 제거했다. 기존 timeline은 실제 결과/자막/효과/오디오 **상태 표시**, transport는 실제 seek를 제공한다. 정적 demo 파일 그림은 실제 입력 자산으로 세지 않았다.

Marketing HTTP, 승인 AVORA 자산, 외부 광고 9:16 Preview, 대표 승인, 승인 광고 MP4는 **DEFERRED_EXTERNAL**. 기존 광고 숏폼 버튼/코드는 보존하고 unavailable 상태에서 기본 편집이 계속 작동함을 확인했다. 실제 광고 연동 PASS를 주장하지 않는다.

Windows 설치/업데이트/one-click 런처, native 종료와 재시작, Windows FFmpeg 경로/폰트, bundled runtime 의존성 검증은 **PC Work 다음 단계**다. General Work에서는 패키지를 생성하거나 기존 복잡한 직원 설치 계획을 실행하지 않았다. 시스템 Python/Git/pip를 직원에게 요구하지 않는 최종 Windows 패키지가 완성됐다고 주장하지 않는다.

HTTP idempotency는 실행 중인 동일 서버의 동일 request_id/payload replay 범위다. 실패 요청은 재시도 가능하며, 서버 재시작 뒤 HTTP retry key를 영구 복원하는 것은 구현하지 않았다. 저장된 프로젝트/Job/미디어 복원은 별도로 실제 검증했다.

## 인계와 보호 상태

main `797da297f588780ad2d608deea3b5af8f05af450` 유지. PR #23 open/draft/unmerged, **HOLD / DO NOT MERGE** 유지. force push·main merge·새 저장소/branch/worktree 없음. 기존 확정 Evidence 삭제 없음.

General Work 결과는 인계 가능하다. **PC Work Control Plane은 계속 PAUSED**이며, commander가 다음 `ONE_CLICK_RUNTIME_PACKAGE` 작업을 별도로 활성화해야 한다. 이 보고서는 PC Work의 자동 실행 허가나 외부 연동 최종 PASS가 아니다.

필수 산출물 9종과 전체 control/함수 인벤토리·실제 Runtime receipt·회귀 원본 로그·다운로드 독립 검증·원격 readback은 `docs/evidence/media-ai-general-work-final-self-audit-20261008/`에 있다.
