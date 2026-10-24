# MINDLE MEDIA AI — AI 실행 환경 및 기능 복구 실검수

2026-10-14 KST. PR #23 **HOLD / DO NOT MERGE**. main 병합 없음. 활성 Owner Runtime Recovery Epoch를 유지한다.

기존 감사에서 발견한 결함을 수정하고 실제 CPU 모델·HTTP·Chrome·FFmpeg·프로젝트 저장/재열기/Export를 실행했다. 환경 준비 여부만으로 PASS하지 않았다. 범위 판정은 **PASS_ADOPTED_CPU_ENGINE_EXECUTION_AND_PERSISTENCE** 및 **PASS_RUNTIME_RECOVERY_SCENE_EDIT_BROWSER_GATE**이다. 생성형 계획 에이전트, 외부 Marketing/AVORA, 교정된 Windows 패키지와 사무실 PC 승인을 전체 PASS에 포함하지 않는다.

## 실제 사용하는 엔진

| 기능 | 엔진 / Runtime | 실제 실행 확인 | 범위 |
|---|---|---|---|
| PHOTO 분할 | facebook/sam2.1-hiera-base-plus / PyTorch CPU | 참고 crop가 입력에 전달되고 실제 mask·overlay·참고파일 해시가 생성됨 | 동일 사진의 대상 crop template match. 일반 이미지 의미 이해나 언어 객체 탐지는 아님 |
| PHOTO 4× | Intel single-image-super-resolution-1032 / OpenVINO CPU | 실제 4× 결과 파일·해시·프로젝트 보존 | adopted 엔진은 Intel이며 함수 이름 realesrgan()은 실제 모델명을 뜻하지 않음 |
| VIDEO 추적 | 같은 pinned SAM 2.1 가중치 / Transformers Sam2VideoModel streaming memory | 원본 24fps의 125프레임 전체 처리. H.264/yuv420p/faststart와 원본 크기·길이 유지 | CPU512 입력 약207.8초. 실시간·추적 정확도 벤치마크 PASS는 아님 |
| 한국어 STT | openai/whisper-small / PyTorch CPU | 44.1kHz 스테레오 WAV → 16kHz 모노. 37.44초 599,040 samples 전부 처리. 25초+12.44초 두 구간 한국어 출력 | OpenAI API가 아닌 로컬 가중치. WER 정답률 미측정 |
| 구간 자막 / 편집 | FFmpeg / Pillow / OpenCV / canvas | 실제 37초 영상에 두 구간 한글 자막 렌더. 5초·30초 프레임 검수 | 구간 단위 자막이며 단어 단위 forced alignment는 아님 |

torch2.8.0 CPU, torchvision0.23.0, transformers4.57.3, openvino2025.3.0, soundfile0.13.1로 실제 CI를 수행했다. 모델 revision·weight bytes/SHA는 LIVE_ENGINE_RECEIPT에 있다. 공식 SAM2 Video 문서 및 pinned4.57.3 구현, Intel 두 입력/BGR/4× 규격, Whisper 다국어·긴 입력 chunking 문서를 대조했다. 최신 버전이라는 이유만으로 검증된 가중치나 dependency를 교체하지 않았다.

이번 복구 세션의 38422429712 실행에서 네 엔진 작업 모두 실제 HTTP 추론을 수행했다. 38425586338에서 긴 Whisper 입력을 다시 실제 추론했다. 최신 검수 실행은 SAM 참고 분할을 새로 실행하고, 동일 수정 구현의 upscale/tracking/long-STT 결과 세 개를 해시 확인 후 재사용한다. **최신 한 실행에서 네 모델을 모두 새로 호출했다고 주장하지 않는다.** 과거 10월11일 Windows 증거를 현재 모델 실행으로 재분류하지 않았다.

## 고친 제품 경로

모델 실행 앞에 intake·handoff·readiness·preflight·dispatch 게이트를 배치했다. 실제 시작/종료 시간을 기록하고 실패 worker의 Job을 부모와 재시작한 서비스에서 다시 조회한다. `/api/tasks/{request_id}`가 실행 단계, `/api/jobs/{job_id}`가 보존 Job을 반환한다. 거절된 게이트는 adapter를 호출하지 않는다. 모델 준비 실패는 실패로 기록하며 대체 가짜 추론으로 성공하지 않는다. 내부 Model Scout callback은 로컬 receipt로 분류하고 PR lineage를 PR23으로 수정했다.

명시적 오른쪽 대상의 좌우 반전 버그, 참고 파일 미전달·미저장, immutable 모델 manifest를 현재 Actions run id로 찾던404 오류를 수정했다. 별도 Sam2VideoModel로 전체 프레임 memory 추적을 연결했다. PHOTO Sam21VerifiedAdapter AST·기존 immutable PHOTO receipt·가중치는 보존했다. 기존 사진 분할 알고리즘을 교체하지 않았다.

WAV 입력 형식을 정상화하고 긴 STT를 모든 구간으로 처리한다. 토큰 상한을 decoder prefix를 포함해 수정했다. 자동 자막은 STT 구간 시간으로 영상에 표시한다. 별도 음성 입력이 영상 미리보기를 덮어쓰지 않으며, 저장된 STT 입력을 다시 읽을 수 있도록 연결했다. BGM은 한 번 적용한 파일을 다음 편집에서 중복 혼합하지 않는다. 참고 이미지를 프로젝트에 저장하고 재열기·Export에 포함한다.

VIDEO 자동 편집은 측정된 장면 분석, PHOTO 자동 보정은 실제 픽셀 분포 분석이다. 이들은 작동하지만 생성형 판단으로 표시하지 않는다. 동일한 단색 사진으로 slider 해시만 검사하지 않고 textured portrait의 7개 보정·회전·반전·스타일·crop·원본 비율 resize 결과를 확인했다.

## 실제 검증 및 보존

Python89개, UI 구조/동작2개 및 실제 Chrome40항목이 통과했다. Chrome 검사는 영상/사진 import, 별도 음성 import의 영상 유지, MediaError/readyState/videoWidth/currentSrc, 자동 편집, H264 재생, 편집 도구, 사진7보정, 참고 유사도, 9:16 비율, BGM 단일 적용, 저장·서버/브라우저 완전 재시작·동일 프로젝트·브라우저 Export CRC/해시를 포함한다. 모든 화면 버튼의 클릭이나 자연어 의미 품질을 이40개로 전수 PASS했다고 확대하지 않는다. 기능별 소스 연결과 실제 실행 여부는 FEATURE_ENGINE_MATRIX에 분리했다.

생성형 계획/의미 분석, durable 다중 에이전트 queue·자동 재시도·취소는 연결하지 않았다. 한국어 STT 정답률·semantic target·tracking accuracy도 독립 정답셋으로 측정하지 않았다. 로컬 callback 정상과 외부 agent 송수신 정상을 구별한다. 이 부분은 GAP_CLOSURE에 남긴다. OpenAI는 대표가 정한 유일한 승인 gate까지 **NOT_CONNECTED**이며 API 호출0회이다. 키 연결 승인 후 계획→실행→검수 경로를 실제 호출로 검증해야 한다.

Marketing HTTP·승인 AVORA 자산은 활성 Control Plane의 **DEFERRED_EXTERNAL**이다. 승인되지 않은 자산을 만들거나 실제 연동 완료로 바꾸지 않았다. Windows corrected package는 현재 package_build_allowed=false를 따른다. 구형 두 워크플로가 paused PC validator에서 실패한 기록을 남기고, 활성 Recovery hold를 job gate에 적용해 build 작업이 SKIPPED임을 확인했다. 기존 패키지는 새 교정본이 아니며 사무실 PC double-click 승인도 대신 PASS하지 않는다.

승인 UI HTML/CSS/SSOT의 원격 blob SHA를 감사 시작 HEAD와 실제 검증 HEAD에서 비교해 동일함을 확인했다. 타이틀·색상·배치·가로 PHOTO 기준·세로 AutoFit/중앙·일곱 보정·광고 숏폼 버튼을 재설계하지 않았다. 검사 영상/이미지는 아티팩트에 남긴다. 전체 제품 최종 PASS 문자열을 발행하지 않는다.

검수자료: `docs/evidence/media-ai-agent-engine-repair-20261014/`. EVIDENCE에는 최종 실행/아티팩트/소스 SHA와 보류 범위, PREVIOUS_ATTEMPTS에는 중간 실패 및 수정 실행을 남긴다. 최종 아티팩트 ZIP SHA·CRC, 모델 결과 해시, browser-ready codec/faststart/길이는 독립 readback으로 확인한다.
