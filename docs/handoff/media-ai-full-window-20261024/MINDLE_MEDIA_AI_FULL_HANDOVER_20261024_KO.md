# MINDLE MEDIA AI — 이 창 전체 작업 인수인계

작성: 2026-10-24 KST / 용도: PC 창 연결 불안정 시 다음 General/PC Work 창에서 이어가기.

## 0. 다음 담당자가 먼저 읽을 결론

**현재 인수 대상은 TEST R2다. 제작·원격 Windows 실제 검증·전달은 완료됐다.**
실제 사무실 PC 인수·설치 플레이어/사람 청취·승인 UI 최종 대조는 완료되지 않았다.
과거 c37, 10월 18일 TEST R1, Linux 소스 실행, 현재 TEST R2를 섞지 않는다.
이 문서는 완료된 일을 다시 시작하라는 지시가 아니다. 새 패키지나 새 모델을 만들지 말고 남은 인수만 진행한다.

현재 창의 연결 장애는 사용자가 보고한 상태다. 제품 서버 오류 또는 TEST R2 실패로 판정할 새 PC 증거는 없다. 이 문서 작성으로 ChatGPT/Codex PC 창 연결이 복구됐다고 주장하지 않는다. 다음 창에서 기존 작업이 자동으로 이어지거나 PC 제어 권한이 자동으로 생긴다고도 보장하지 않는다.

### 현재 기준

| 항목 | 값 |
|---|---|
| 저장소 | ADAMBUILD-ai/mindle-media-ai |
| 작업 브랜치 | feature/ad-shortform-bridge-p0-20260926 |
| 인계 직전 확인 HEAD | cce3431c9a32687f0e3adc62f8ebefd5d944bd10 |
| 실제 TEST R2 제품 source | 2e5e9197d78c9b975686c1e419d2b68ce5f65226 |
| main 확인 HEAD | 797da297f588780ad2d608deea3b5af8f05af450 |
| PR #23 | OPEN / DRAFT / HOLD / DO NOT MERGE |
| PR 확인 수치 | 650 commits / 1,244 changed files — 이번 인계 시 재확인. 과거 646/1,213 수치를 현재로 재사용하지 말 것 |
| 현재 Epoch | MEDIA-AI-20261013-OWNER-RUNTIME-RECOVERY-R1 |
| 현재 phase | OWNER_WINDOWS_AI_CANDIDATE_READY_FOR_PC_ACCEPTANCE |
| 전역 Build Gate | package_build_allowed=false |
| 새 후보 제작 승인 | 대표의 “추가 후보 재작까지 진행한다.”로 후속 개발 후보 1건 제작 완료·승인 소비 |
| 전체 제품 PASS | 미발급 / owner_pc_runtime_pass=false / final_product_pass=false |

HEAD 구분: 2e5e…는 실행 검수한 제품 source다. b488…는 전달 문서/분할 readback, 38c7…는 동일 바이트 중간 전송, cce343…는 최종 증거/SSOT 인계다. 후속 문서 commit이 생겨도 기존 EXE의 source가 그 HEAD로 바뀌지 않는다.

## 1. 대표가 이 창에 요청한 일과 진행 원칙

1. GitHub Actions의 PHOTO 업스케일 preview 300초 timeout을 로그·아티팩트·소스와 대조해 원인을 구분하고 검증 가능한 수정 수행.
2. 제품 E2E → 외부 연동 마감 → General Work 전수 자체검수로 활성 지시서가 전환됨. 직원용 R2 Control Plane은 당시 작업에서 내려짐.
3. 영상 MediaError.code·readyState·videoWidth·currentSrc를 실제 기록하고 H.264/yuv420p/faststart preview를 검증. 단순 timeout 증가는 금지.
4. VIDEO/STT/Save/Close/Reopen/Export/Marketing/AVORA/9:16 광고/MP4를 구분하고 실제 증거만 PASS.
5. 버튼·죽은 기능·UI만 있고 runtime 없는 기능·중복 코드·저장/재열기/Export·개발환경 의존성·사진/영상 비율 전수 점검.
6. PC가 막혀도 독립적인 PHOTO/CSS·런처 lock·저장/복원 소스 수정과 회귀검증을 계속할 것. 도구/보고서만 만들고 끝내지 말 것.
7. AI 계획기·영속 큐·취소·제한 재시도·한국어 TTS·MP4를 실제 제품 흐름에 연결할 것. Windows Work에 제품 개발과 공급자 설정을 떠넘기지 말 것.
8. 기존 UI를 노트북/데스크톱에서 더블클릭 실행할 수 있는 후보 제작·전달. TEST R1 전달 후 실제 PC에서 다음 날 실행 실패가 발생해 소스 감사와 TEST R2 제작으로 이어짐.
9. 엔진이 어떤 모델인지, 실제 작동하는지, 제안공모 자료에 어떤 도움을 주는지 설명·정리할 것.
10. 현재 PC 창 연결 불안정 때문에 이 창의 자료·조사·작업·잔여를 다음 창에 빠짐없이 넘길 것.

대응 원칙: 불필요한 승인 질문·“진행하겠습니다”만으로 끝내기·상태 보고 반복 금지. 대표에게 개발자가 만든 과거 로그/ZIP 위치를 찾아 제출하라고 요구하지 않는다. 접근 가능한 워커가 수집한다. 실제 접근 불가능한 PC/사람 청취를 추정 PASS로 바꾸지 않는다. 한 항목이 막혀도 독립 항목은 이어간다. 새 범위 확대는 금지한다.

## 2. 현재 읽을 SSOT와 자료 우선순위

1. 현재 소유자 지시와 후보의 명시 승인 범위.
2. CURRENT_PC_WORK_DIRECTIVE.md / CURRENT_GENERAL_WORK_DIRECTIVE.md의 2026-10-24 TEST R2 머리말.
3. docs/commander/MINDLE_MEDIA_AI_PC_TEST_R2_ACCEPTANCE_20261024.md
4. docs/commander/MINDLE_MEDIA_AI_PC_TEST_R2_EVIDENCE_CONTRACT_20261024.json
5. docs/evidence/windows-ai-candidate-20261024-r1/FINAL_RESULT_KO.md, FINAL_DELIVERY.json, ACCEPTANCE.json, ASSEMBLY.json.
6. 원본 Actions 실행·고정 manifest/EXE/ZIP identity.
7. 과거 R9/TEST R1/LINUX 보고는 날짜와 source를 붙여 역사 증거로 사용.

Control Plane은 General/PC STATE 및 LOCK 4종과 CURRENT_WORKER_COORDINATION_LOCK.json이다. 이번 인계 ZIP의 SOURCE_SNAPSHOTS에 현재 원문을 보존했다. 현재 validator가 통과했다는 사실은 문서 정합성 확인이며 사무실 PC 제품 전체 PASS가 아니다.

### 인계 재검토에서 확인한 잔여 문서 불일치

cce343…의 최신 후보 source/hash/phase와 owner_windows_candidate_20261024는 TEST R2다. 그러나 아래 구형 필드가 일부 남아 있다. 이 필드를 근거로 재빌드하거나 c37을 최신으로 실행하지 않는다. **이 인계 작업은 이 불일치를 표시·보존했으며 제품/Control Plane 원본을 몰래 고치지 않았다.**

| 구형 잔여 필드/설명 | 현재 해석 |
|---|---|
| candidate_artifact_run=38845082039, candidate_evidence_artifact 및 candidate_delivery_part_artifacts의 120… ID | c37 과거 아티팩트. 최신은 candidate_delivery_artifact_run=39987617196와 FINAL_ARTIFACTS.json |
| candidate_contains_project_transition_fix=false | pending_source_repairs의 candidate_contains_fix=true/inclusion_source=2e5e… 및 최신 source와 충돌. 포함 여부와 새 후보에서 경계 6건을 재실행한 여부는 별개 |
| candidate_contains_runtime_owner_stop=false | 새 native ACCEPTANCE의 정상 종료·새 PID 실증과 충돌하는 과거 설명 |
| candidate_contains_dense_library_fix=false | 과거 포함 상태. 현재 source에 관련 수정이 있으나 새 후보의 밀집 UI 전용 시나리오를 새로 PASS로 확대하지 말 것 |
| candidate_contains_workflow_runtime=false, workflow_runtime.windows_native_verified=false | 과거 10/18 소스 보고. TEST R2 Qwen/TTS native 증거로 구분 |
| latest_source_requires_new_candidate=true | TEST R2 제작 전 설명. 추가 빌드 승인으로 해석 금지 |
| local_physical_acceptance_condition에 “Only this R9…” | TEST R2 계약·고정 해시가 최신 인수 기준 |
| local_helper_status=NORMAL_20261014 | 과거 사용자 보고. 현재 사용자는 PC 창 연결 불가를 보고함 |
| approved_ui_original_sha256=f27e… | 오래된 승인 이미지 값. 최신 좌 VIDEO/우 PHOTO 권위 정리와 cfeed… 비교 원본을 함께 확인 |

첫 후속 조치는 위 구형 필드를 역사 영역으로 명확히 구분하는 작은 문서 정합화까지 가능하다. 그것을 이유로 제품 코드를 바꾸거나 후보를 다시 만들지 않는다. 원본 snapshot은 보존한다.

## 3. TEST R2 정확한 identity — 가장 중요

- 제품 source: `2e5e9197d78c9b975686c1e419d2b68ce5f65226`
- Runtime ID: `2e5e9197d78c-473763a9ef2d-ai-r2`
- EXE SHA256: `701654240d8f2795957f78f7d1cc9d7fd23d3195f49a0d39ede1d8b8a3a915a5`
- PACKAGE_MANIFEST SHA256: `2c6c3345539473e77cab56b10105448d0c23b651875dca45e8d49217b781dc07`
- 최종 ZIP: `MINDLE_MEDIA_AI_PC_TEST_20261024_R1.zip`
- ZIP bytes: **3,166,947,613**
- ZIP SHA256: `c3cfda25e2f36f97024a57b586a20914be3b21a2b481f25e1652c8931ece3606`
- payload 파일 수: **19,333**
- 설치기: `MINDLE_MEDIA_AI_START_20261024_R1.zip`, **2,365 bytes**
- 설치기 SHA256: `747ddd1eb7aa1cef93f235af2128d9aeef68399e15c362a30260d36b1a4e9b44`
- 바로가기 표시: **MINDLE MEDIA AI TEST R2**. ZIP 파일명 날짜 뒤 R1과 바로가기 TEST R2는 모순이 아니라 해당 제작 라운드/후속 후보 표기다.

최초 producer ZIP b8f162…와 최종 c3cf…는 같지 않다. payload 밖 DELIVERY_ARTIFACT_SHA256.txt가 c37 값을 유지한 것을 정정했기 때문이다. 수정 전 문서가 ORIGINAL_EXTERIOR_CHECKSUM.txt에 보존됐다. EXE·manifest·모든 제품/모델 파일은 바뀌지 않았고 전체 SHA/CRC를 다시 검증했다. ZIP 해시 차이를 숨기거나 첫 ZIP을 최종으로 쓰지 않는다.

## 4. 이미 전달·보존된 파일 9개

설치 필수는 설치기 1개 + part-00~06 7개, 총 8개다. Runtime evidence ZIP은 검수자료다.
인계 시 보관된 파일 9개 모두를 파일 목록에서 다시 확인했다. 원본 증거 ZIP은 최신 version 1을 복구해 CRC를 확인했다. **3.17GB 제품을 다시 내려받거나 재생성하지 않았다.**

파일별 전체 SHA/bytes는 DOWNLOAD_FILE_MANIFEST.json과 SOURCE_SNAPSHOTS/docs/evidence/windows-ai-candidate-20261024-r1/FINAL_DELIVERY.json에 있다. PRIVATE_FILE_LOCATORS.json은 다음 창이 원래 파일을 복구하는 식별자이며 공개 GitHub에 올리지 않는다.

| 파일 | bytes | SHA256 |
|---|---:|---|
| MINDLE_MEDIA_AI_START_20261024_R1.zip | 2365 | `747ddd1eb7aa1cef93f235af2128d9aeef68399e15c362a30260d36b1a4e9b44` |
| MINDLE_MEDIA_AI_PC_TEST_20261024_R1.zip.part-00 | 524288000 | `0f2a3a438ae76fc857da79932fb025a2091b4af9df5cd2b336c168f2f1076c59` |
| MINDLE_MEDIA_AI_PC_TEST_20261024_R1.zip.part-01 | 524288000 | `a3e7cc7c2e171c5ccecc589c92ffdd98791095251289ae3920d204fc95b8f4b5` |
| MINDLE_MEDIA_AI_PC_TEST_20261024_R1.zip.part-02 | 524288000 | `f85a8219c0c769e0e2770f2d18966c12da76f878f99a328486c11622e37af0ad` |
| MINDLE_MEDIA_AI_PC_TEST_20261024_R1.zip.part-03 | 524288000 | `1961cb3b717cf7ad1793d7bd5bd92a5d69a4228eafb8dd806c60e341c87c1ad0` |
| MINDLE_MEDIA_AI_PC_TEST_20261024_R1.zip.part-04 | 524288000 | `a73dd9a639c7d3dec697b0c689a1c308c4a1ee18ec1a4d0f1a56c810d78f2992` |
| MINDLE_MEDIA_AI_PC_TEST_20261024_R1.zip.part-05 | 524288000 | `8ffd45e965cbdf9bcc9edc30440be0fa94f761739f078ae1c00194ff6c6b36f0` |
| MINDLE_MEDIA_AI_PC_TEST_20261024_R1.zip.part-06 | 21219613 | `1c525ec6209b16639156a35a32fd78e092b1a8897c79f245ce72bbe89b7aa169` |
| MINDLE_MEDIA_AI_RUNTIME_EVIDENCE_20261024_R1.zip | 1852889 | `14cf7e69c05a1239e2bc114adde4db08f8250bdad7b5f2e9d4c7f2d013a23d73` |

기존 파일은 파일명으로 검색해 사용하거나, PRIVATE_FILE_LOCATORS의 정확한 현재 식별자로 복구한다. 새 파일을 만들었다고 가장하거나 사용자에게 이미 전달된 8개를 이유 없이 다시 받게 하지 않는다. 대용량 파일은 파일 내용이 실제 필요한 시점에만 복구한다.

### 실행 경로

- 8개를 같은 폴더에 놓고 설치기 ZIP만 푼다. START_MINDLE_MEDIA_AI.cmd 더블클릭.
- 새 바로가기 TEST R2 사용. 20261018 TEST R1 또는 c37 바로가기를 혼용하지 않는다.
- 후보 설치: `%LOCALAPPDATA%\MINDLE\PC_TEST_INSTALLS\20261024_R1\MINDLE_MEDIA_AI_PC_TEST_20261024_R1`
- bootstrap 설치 runtime: `%LOCALAPPDATA%\MINDLE_MEDIA_AI\runtime\2e5e9197d78c-473763a9ef2d-ai-r2`
- 새 작업 데이터: `%LOCALAPPDATA%\MINDLE\MEDIA_AI_CANDIDATE_20261024_R1`
- 서버 로그: 위 새 데이터 폴더의 `logs\server.log`.
- 기존 TEST R1 데이터 `MEDIA_AI_CANDIDATE_20261018_R1` 및 c37 `MEDIA_AI_DATA`는 보존한다. 자동 이전은 하지 않았다. 이전 자료가 새 후보에 자동 표시된다고 약속하지 않는다.
- INSTALL_COMMAND는 part 결합→최종 ZIP SHA→System32 tar.exe 추출→EXE SHA→새 바로가기→실행이다. >2GB 파일 때문에 Expand-Archive로 바꾸지 않는다.

## 5. 실제 TEST R2 원격 검증

| 실행 | 역할 | 결과 |
|---|---|---|
| 39985471598 | Windows native EXE + 실제 Chrome/Qwen/Supertonic + 정상 서버 종료/새 PID/복원/UI Export | success |
| 39987617196 | 독립 원본 회수·모든 payload SHA·CRC·외부 checksum 문서 정정·분할 발행 | success |
| 39989419656 | 이미 검증된 동일 바이트의 작은 중간 전송, 제품 재빌드/추론 아님 | success |

실행 URL은 `https://github.com/ADAMBUILD-ai/mindle-media-ai/actions/runs/<번호>`.

- 실제 복합 지시: `밝기를 3 높이고 "반갑습니다" 나레이션을 넣고 영상을 연장해 주세요.`
- 사용자 입력→실제 Qwen 응답→허용 단계 검증→영속 큐→실제 Supertonic ONNX 음성→MP4→브라우저 재생.
- 이전 PID **4968** 정상 종료, endpoint 닫힘, 새 EXE/PID **7412** 및 새 instance.
- project_id `7f05e21e-72c1-4851-8dca-9417b7944fa9`.
- workflow_id `ee31eefa-db70-43f7-9acd-b93c6e33850e`.
- 같은 프로젝트·작업 이력·생성 나레이션 복원, 실제 Chrome UI Export 다운로드.
- 설치 runtime/배포 payload 파일 **19,333개** 실행 후 SHA 정상, 생성 `.pyc` **0개**.
- 한국어 WAV: **131,846 bytes / mono 44,100Hz / 1.4943537415초**.
- WAV SHA: `4134a7503b4c46878cbd0f090dbcd27042fce08f0fe56781bf81303d8baeeda3`.
- MP4: H.264/yuv420p + AAC, 영상 4.000초/음성 4.006초, moov가 mdat 앞의 faststart, 전체 FFmpeg 디코딩 exit 0.
- MP4 SHA: `043d0d2e9accd7fef171d02c506dc0c64abd272138df6343c2b72a2b27ec8755`.
- API Export SHA: `db053e2d59eb6ce7d62c20986133e4e496c4ef1a49f123e43e621e610ff76d15`.
- UI Export SHA: `f29db14aa2ea97ddd6faa2ca1855f106886a18b2e9f68753afe5a22814967d05`.
- API/UI ZIP 각각 manifest 11개 항목의 크기/SHA와 CRC 독립 확인.

**범위 한계:** EXE는 원격 runner에서 --no-browser로 서버를 기동하고 실제 Chrome을 별도로 제어했다. 물리 PC에서 사용자가 일반 더블클릭한 것과 동일한 증거로 확대하지 않는다. 새 시나리오는 영상/나레이션/작업 이력이다. 사진·참고 이미지 2개·입력 음성·Whisper/SAM 전부를 TEST R2에서 새로 실증한 것으로 바꾸지 않는다. 원격 영상은 검증용 4초 fixture이며 건축 홍보영상 품질 평가 결과가 아니다. 사람의 실제 청취/자연스러움은 미확인이다.

## 6. 사용자가 준 실행 장애 사진과 실제 결함

USER_INPUTS에 원본 사진 2장을 복구했다.
- image-1792644361820.jpg: 기존 TEST R1 바로가기/다운로드 폴더 및 대상 경로.
- image-1792644384621.jpg: `패키지 검증 실패: runtime/site-packages/PIL/__pycache__/ExifTags.cpython-311.pyc` 오류 창.

사용자는 “어제는 열렸는데 지금은 열리지 않는다”, “AI 프로그램인지 일반 프로그램인지 느껴지지 않는다”고 보고하고 전체 점검을 지시했다.

확인한 설계 결함: 실행 중 갱신 가능한 Python 캐시 .pyc를 manifest로 봉인했고 import가 다시 쓰면 다음 실행에서 해시가 달라져 차단될 수 있었다. 실제 별도 Python 프로세스에서 오래된 캐시→일반 import는 해시 변경, -B import는 해시 유지 현상을 재현했다. 오류는 모델 추론 이전의 검증 단계다. 물리 PC의 정확한 writer PID/수정 시각은 회수하지 못해 미확정이다.

수정 source 8b694818c3bd401194695e427ae410dc7c04cb72:
- bootstrap→Python / launcher→server / durable queue→worker 모두 -B.
- launcher 초기에 sys.dont_write_bytecode=True.
- 새 payload/manifest/ZIP에서 캐시 제외. SHA 검증과 lock은 유지.
- TEST R2는 최신 bootstrap EXE를 새로 컴파일. 기존 frozen EXE 재사용이 아님.

기존 R1 현장 캐시를 지우거나 현장 해시를 새 정상값으로 채택하는 우회 도구를 발행하지 않았다. 원본 후보와 사용자 자료를 보존했다. TEST R2가 원격 Windows에서 검증됐다는 사실을 “사용자 PC의 R1을 원격 수리 완료”로 표현하지 않는다.

이전 응답에서 사용자에게 진단 ZIP을 찾아 올리라고 요구한 일이 있었고, 사용자는 개발자/PC Work의 책임을 떠넘기지 말라고 지적했다. 다음 담당자는 이를 반복하지 않는다. 초기 진단 ZIP은 read-only 수집 도구였으며 실행 문제 수리 완료본이 아니었다.

## 7. AI 엔진과 실제 역할

| 엔진 | 채택/실행 | 실제 역할·제한 |
|---|---|---|
| 생성형 계획기 | Qwen2.5-1.5B-Instruct-GGUF + llama.cpp b11716 llama-completion | 자연어를 지원 편집 단계로 계획. 도구 실행 자체와 분리. 범용 에이전트/공모 제안서 전체 엔진 아님 |
| 영역 분할/추적 | Meta SAM 2.1, facebook/sam2.1-hiera-base-plus | 사진 대상 분리·배경 제거·영상 추적. 새 투시도/이미지 생성 아님 |
| 한국어 STT | OpenAI Whisper-small 로컬 가중치 | 음성 받아쓰기·자막. OpenAI API 키 연결과 무관 |
| 사진 업스케일 | Intel single-image-super-resolution-1032 | 기존 사진 확대/화질 개선. 치수·문자·도면 선의 정확 복원을 보장하지 않음 |
| 신경망 TTS | Supertone Supertonic 3 / sherpa-onnx 1.13.8 | 원고→한국어 실제 WAV. 신경망 ONNX 추론. 사람 청취·음질 인증은 별도 |
| 과거 대체 TTS | eSpeak NG | 규칙 기반 formant 합성. neural TTS로 표시하지 않음 |
| 영상 합성 | FFmpeg | 원본 소리·나레이션·BGM·자막 합성, H.264/AAC MP4. 생성형 모델 아님 |
| 자동 편집/하이라이트 | OpenCV 움직임·노출·선명도 분석 + FFmpeg | 통계/규칙 기반 장면 선택. 의미 이해·생성형 편집 완료 아님 |
| PHOTO AI 보정 | Canvas 픽셀 분위수·색온도 통계 | 일반 영상처리. 생성형 모델 추론 아님 |
| PHOTO 스타일/인물/유사도 | 흑백/따뜻한 필터·전체 부드럽게 보정·색상 히스토그램 | neural 스타일 전이/얼굴 복원/의미 임베딩 검색 아님 |

우리 개발 부분은 공개 모델 학습 자체가 아니라 제품 UI·작업 계획·검증·순차 실행·저장·복원·Export 연결 코드다. 실제 생성형 추론과 키워드 처리, 모의 시험을 구분한다.

### 모델 identity

- Qwen revision `91cad51170dc346986eccefdc2dd33a9da36ead9`, GGUF **1,117,320,736 bytes**, SHA `6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e`, Apache-2.0.
- Windows llama archive SHA `79b143075ab87fb5aff6f8f8ca80500a984f4120b5199fa9f9b70b284f17428e`.
- Supertonic upstream revision `3cadd1ee6394adea1bd021217a0e650ede09a323`, 변환 archive SHA `82fa96f91c4ef8abaae3a14a3f4153facf88bed821d1f7331cec2700f432c427`. 모델 OpenRAIL-M, upstream 코드 MIT, sherpa Apache-2.0. 모델 라이선스를 코드 라이선스로 바꾸지 않는다.
- SAM weight SHA `2012733a0de5d03efd1bba550a2847c4551be9ef2e0d497c83074df66189f780`, revision `b7320756a13354e7530a63935656d35b2f91a290`.
- Whisper weight SHA `1d7734884874f1a1513ed9aa760a4f8e97aaa02fd6d93a3a85d27b2ae9ca596b`, revision `973afd24965f72e36ca33b3055d56a652f456b4d`.

새 이미지/영상 텍스트 생성 모델은 이번 제품에 없다. 이미 있는 모델 파일이나 버튼을 이를 구현한 것처럼 표시하지 않는다. Qwen/Supertonic의 현재 원격 실제 실행 PASS를 나머지 엔진의 최신 사무실 PC 전체 PASS로 확대하지 않는다.

### AI가 체감되지 않았던 연결 결함과 수정

일반 VIDEO 자연어가 일부 키워드에서만 workflow로 들어갔고, 단순 나레이션은 정규식이 steps를 만들어 생성형 추론을 우회했다. 모델이 복합 요청 중 일부를 누락해도 성공할 수 있었다. 8b6948…에서 지원 자연어/미지원 요청의 plan API 도달, 주입 steps 제거, 누락 단계 거절, 광고 모드 우선 처리, 일반 처리 설명을 보완했다. 레이아웃/색상은 바꾸지 않았다. 현재 대화 계획 범위는 밝기·대비·채도·받아쓰기·자막·명시 원고 나레이션이다. 임의 셸/삭제/네트워크 명령으로 연결하지 않는다.

## 8. 실제 작업 실행 구조

- SQLite WAL/FULL 영속 큐, 프로젝트/계획/작업/단계 식별자, 입력·출력 hash, attempt/error 기록.
- QUEUED / RUNNING / RETRY_WAIT / CANCEL_REQUESTED / SUCCEEDED / FAILED / CANCELLED / INTERRUPTED.
- 서버 재시작 시 실행 중이던 작업을 성공으로 바꾸지 않는다. interrupted 판정 후 안전한 재개 조건을 확인한다.
- 중복 request/idempotency, 단계별 이전 결과 연결, 해당 작업의 프로세스/자식에 한정한 취소.
- 일시 오류에만 횟수 제한 retry. 입력 누락·지원 불가·인증 실패 무한 retry 금지.
- attempt-private 임시 파일과 게시 봉인 결과 분리. 취소/실패 미완성물을 정상 preview/MP4로 게시하지 않는다.
- 원고/음성 참조·음량·원본 오디오/BGM·길이 정책을 저장. 음성이 길면 reject/명시적 영상 연장 선택을 구분하고 조용히 자르지 않는다.
- 저장·복원·Export는 단계적 commit으로 마지막 정상 프로젝트를 보존한다.
- 이 구조는 제품이 시작될 때 돌아가는 실제 워커/큐다. 별도 상시 AI 팀이 무조건 알아서 개발을 진행하거나 새 키를 연결한 것처럼 표현하지 않는다.

원시 중간 파일의 과거 쓰기 주체는 여전히 미확정이다. 봉인·해시 보호 회귀 PASS와 writer PID 확정을 섞지 않는다. 독립 filesystem exec를 실제 장시간 미디어 쓰기 중에 무분별하게 병행하지 말고, 한 오케스트레이터에서 작업하고 해당 session만 poll한다.

## 9. 제안공모 활용 질문에 대한 정리

대표는 이 모델들을 건축 제안공모/제안서 작성에 쓸 수 있는지 물었다.
- SAM: 현장/참고 사진의 대상 분리·설명 이미지 보조.
- SISR: 작은 참고 사진 확대. 도면 치수/정밀 선/문자 정합성을 위한 복원 용도로 과장 금지.
- Whisper: 회의·현장 음성·설계 의도 구술을 텍스트로 옮기는 보조.
- TTS: 제안 발표/홍보영상 원고의 한국어 나레이션.
- Qwen의 현재 제품 경로: 제한된 미디어 편집 계획. 공모 지침 전체 이해·설계 생성·도면 해석·12페이지 제안서 전체 제작을 책임지는 엔진으로 검증한 것이 아님.

이 질문을 이유로 MEDIA가 AURA 제안서·AKI CAD·AVORA 모델링 업무까지 새로 떠맡지 않는다. 별도 대화의 Blender/FFmpeg/무료 로컬 영상 모델 어댑터 구상은 향후 검토 계획으로만 남기며, 현재 TEST R2 마감 작업으로 구현됐거나 실행 승인됐다고 간주하지 않는다.

## 10. 확정 UI와 대조 원본

- 제목 MINDLE MEDIA AI.
- 최신 방향: **VIDEO 좌측 / PHOTO 우측**. 기존 VIDEO 승인 구조 보존.
- PHOTO 가로 사진 기본, 사진/영상 원본 비율 유지.
- 세로 PHOTO Auto Fit + 중앙 배치/contain. 잘라 채우기로 대체 금지.
- 밝기·대비·하이라이트·그림자·채도·색온도·선명도 7개 보정 유지.
- 광고 숏폼 버튼·자연어 입력 두 곳·우측 편집 패널·Timeline·하단 가이드 보존.
- 색상·배치·헤더·타임라인 비율 임의 재설계 금지.
- 비교는 1536×1024, zoom100%, DPR1과 동일 콘텐츠 상태에서 수행. viewport/캐시/font/자산 상태와 실제 DOM/CSS 결함 구분.

승인 비교 원본: docs/evidence/media-ai-final-integration-20261017/APPROVED_REFERENCE.png.
SHA256 `cfeed43d4864dfe4cc1505dbb37d1ac44871d51cd10907f27cb2abe3694ae339`.
USER_INPUTS/APPROVED_REFERENCE_20261017.png로 복구하고 동일 SHA를 확인했다.
과거 f27e… 원본은 역사 자료이며 최신 가로 이중 패널 권위와 혼동하지 않는다.

과거 차이: PHOTO 보정/참고 Strip 위치, 헤더 카메라 아트, 도구 표현·전체 비율, Timeline/하단 및 많은 자산 상태 넘침. 일부 source 복구가 있었지만 전체 픽셀 승인 PASS는 없다. 승인 헤더 원본 자산 미확보 부분도 남는다. 검수 화면에 승인 이미지를 잘라 붙여 통과처럼 만들지 않는다. 10/18 Linux 한글 네모 캡처는 font 미설치 개발환경 문제였고 이후 font-ready 캡처로 비교했다. 제품 폰트 배포 변경과 혼동하지 않는다.

## 11. 주요 이력·수정·증거의 연결

| 시점/단계 | 보존할 사실 |
|---|---|
| 초기 10/7 실패 | run 37638260222 / artifact 11491720522 / model_scout/run_product_e2e.py browser_e2e wait_preview 300초 timeout. 당시 문제를 최신 TEST R2 또는 PC 연결 오류와 동일 원인으로 단정하지 않음 |
| 10/8 지시서 전환 | PRODUCT_E2E_VIDEO_PREVIEW_TO_FULL_PASS, SHORTFORM_EXTERNAL_INTEGRATION_CLOSEOUT, GENERAL_WORK_FINAL_SELF_AUDIT 지시서/계약. 원문 snapshot 포함 |
| 10/14 준비 | Ryzen7 5800X / RAM약32GB / RTX3060 12GB, 백업·CRC·입력8·버튼60 준비 사용자 보고. 당시 문서 날짜 충돌/Build Gate로 검수 BLOCKED. 현재 PC에서 재확인한 사양은 아님 |
| 10/15 R9 | 사용자가 실제 Chrome 재생·탐색·오디오, 사진7보정, 브라우저 재열기, ZIP/CRC, 버튼59PASS/1FAIL 보고. cloud 오연결·세로 PHOTO 잘림·UI차이·런처 lock 남음 |
| 10/16 독립 General | PHOTO/CSS, launcher lock, 저장/복원 source 수정·회귀를 PC 대기와 분리. 무조건 lock삭제/타임아웃 증가 금지 |
| c37 원격 Windows | ZIP SHA529176… / manifest19,236 검증, EXE. run38851276116 동일프로젝트/참고2/입력음성 복원/UI Export. 원격 runner이며 현장 인수 아님 |
| 10/17 프로젝트 경합 | 84cf580… 전환 Save응답 경합 수정. Windows Chrome source6 시나리오 PASS, c37 미포함. 302039… 소유PID/정상종료·밀집자산 보완 |
| 10/17 저장/미리보기 | 4e20d02… 참고·음성 저장, 7116244… 원자적 의존 복원, c1956f48… 이전 영상 잔류 제거. UI최종일치 미완료 |
| 10/17 물리 PC 보고 | bfd086… 인계. c37 EXE/Save/Reopen/Export, ZIP129파일 SHA·CRC, PotPlayer 표시/탐색 PASS. 사람 청취 미확인·완전종료 당시 BLOCKED. 113개 재회수/ZIP3개 확인은 과거 보고 범위 |
| 10/18 최초 워크플로 | 4bc645… 영속 큐/취소/retry/eSpeak. eSpeak를 neural로 부르지 않음 |
| 10/18 로컬 엔진 | 3a889d9… 실제 Qwen/Supertonic Linux·Chrome/MP4·완전재시작. 증거978f82… 당시120PASS/2SKIP·Node16. Windows EXE 아님 |
| 10/18 TEST R1 | sourcee00e6… ZIP715c… 3,177,192,286bytes / payload20,440 파일 정적SHA·CRC. c37 bootstrap 재사용. 당시native미실행. 사용자후속실행실패사진접수 |
| 10/22 감사/수정 | source8b6948… 캐시·AI 라우팅/누락계획 검사·설명 보완. Python167PASS/6SKIP, Node23PASS. source시험/fixture와 실제 모델 추론을 구분 |
| 10/24 TEST R2 | source2e5e… 새 bootstrap + nativeQwen/TTS/재시작/UIExport. 독립readback/동일바이트전송/전체파일전달 및cce343…SSOT 인계. 현재 기준 |

초기 cloud 수정38bed49, 진단도구0900f36, timeline21f7d121, PHOTO승인구조40de8cac 등의 기존 성과도 보존한다. commit 짧은 표기는 역사 설명용이며 실제 checkout은 고정된 full SHA/원격 readback을 사용한다. 자세한 원문은 SOURCE_SNAPSHOTS와 전체 저장소 TREE에 연결돼 있다.

## 12. R9 원본·PC 자료 경로 — 수신/검증을 구분

사용자 보고에 등장한 Windows 작업 root:
`C:/Users/R/Documents/Codex/2026-10-10/mindle-media-ai-ui-photo-video/`

- outputs/EVIDENCE_20261014_PREPARATION_R1/FINAL_SUMMARY_KO.txt
- outputs/MINDLE_MEDIA_AI_PC_PREPARATION_20261014.zip
- outputs/EVIDENCE_20261015_CANDIDATE_R9/RESUMED_RESULT_KO.txt
- outputs/EVIDENCE_20261015_CANDIDATE_R9/RESUMED_BUTTON_60.csv
- outputs/EVIDENCE_20261015_CANDIDATE_R9/SSOT_VS_ACTUAL_CHROME.png
- outputs/MINDLE_MEDIA_AI_PC_EXECUTION_20261015_R9.zip
- outputs/MINDLE_FINAL_ACCEPTANCE_20261017_R1/RESULT_KO.txt
- outputs/MINDLE_FINAL_ACCEPTANCE_20261017_R1/source_browser/FINAL_NORMAL_REOPEN_EXPORT.png
- outputs/MINDLE_FINAL_ACCEPTANCE_20261017_R1.zip
- outputs/FINAL_INTEGRATION_20261017_R1/delivery/RESULT_KO.md
- outputs/FINAL_INTEGRATION_20261017_R1/delivery/COMPARE.html
- outputs/FINAL_INTEGRATION_20261017_R1/delivery/UI_IMAGE_COMPARISON_FINAL_KO.md
- work/transition-browser-20261017/serve_source.py, browser_transitions.py, run_combined.py, collect_windows_readonly.py, prepare_windows_handoff.py, c37_save_export.py.

이 인계 작성 환경은 해당 C: 드라이브에 접근하지 못했다. 이 목록은 사용자 보고/저장소 문서의 경로이지 이번에 모든 원본 bytes를 회수했다는 뜻이 아니다. 당시 lock예외전문·bootstrap/server로그·작성PID 조사는 미완료로 남는다.
과거 원격 인계: docs/evidence/windows-work-handoff-20261017-r2/FINAL_RESULT_KO.md 및 docs/evidence/media-ai-windows-r2-general-review-20261017/ACCEPTED_CHROME_SIX.json/GENERAL_VERDICT.json. 현재 원본 snapshot으로 보존했다.

## 13. 남은 작업 — 우선순위와 완료 조건

### P0: 연결되는 실제 Windows PC에서 TEST R2 인수

1. 현재 PC Work 도구/브라우저/명령 실행 연결이 실제 가능한지 먼저 확인한다. 이 채팅창/에이전트 연결 실패와 제품 서버 장애를 분리한다. 연결 안 됐다고 제품을 삭제·재설치·재빌드하지 않는다.
2. TEST R2 고정4종(source/EXE/manifest/ZIP)과 runtime identity를 대조한다. old R1/c37을 대체 증거로 쓰지 않는다.
3. 새 후보 EXE 실행, 정확한 제품 PID/명령행/instance/endpoint를 기록한다. 사용자프로젝트/타앱은 건드리지 않는다.
4. 현재자료 또는 승인된보존입력으로 사진·영상·자막·나레이션·참고·입력음성 Save 응답/project_id 확보.
5. `/api/runtime/control`의 PID/instance/nonce 대조 후 정상 종료 우선. PID 종료+endpoint닫힘 모두 확인.
6. 새 EXE→새 PID/instance→동일 프로젝트와 참조 복원→실제 UI Export. 원본로그·hash·화면 수집.
7. 원래확정PHOTO 분할/4×를 고비용으로 이유 없이 재실행하지 않는다. 단순 source포함확인과 해당PC추론검수완료를 구분한다.

PC Work가 접근가능한환경에서직접수집한다. 대표에게 과거ZIP/로그를 찾아오라고넘기지않는다. 연결불가면 BLOCKED 근거와 정확히미실행한항목만남기고, 다음접근가능창으로동일고정후보를인계한다.

### P0: 설치 플레이어와 실제 청취

Export MP4를 설치된 Windows 플레이어로 열고 이름/버전, 표시, 시간진행, 앞뒤탐색, 실제음성청취를 각각기록한다. browserdecode/파형/무음테스트를 사람청취로대체하지않는다. 과거 PotPlayer 표시/탐색 PASS가 최신R2 전체인수는아니다.

### P1: 승인 UI 최종 대조

동일 viewport/zoom/DPR와 동일 콘텐츠상태에서 헤더·Timeline·전체비율·자연어2곳·우측패널·PHOTO세로 contain/중앙·7보정·숏폼·하단가이드 대조. 원본없는차이는승인일치로판정하지않는다. CSS/DOM/cache/패키지차이/폰트상태를구분한다. 근거확인전추정UI수정금지.

### P2: 역사 조사 및 문서 정합화

R9원본과 lock예외로그 확보후에만 당시원인을확정. 현재legacy SSOT필드의상태정리는문서범위로처리하고 source검증/실제Windows/물리PC판정을분리한다. Marketing/승인AVORA는기존DEFERRED_EXTERNAL; 새외부연동승인으로해석하지않는다.

## 14. 고정 금지·재개 조건

- PR23 HOLD/DO NOT MERGE. main병합/forcepush금지.
- Build Gate=false. TEST R2 제작승인은소비됨. 직원최종패키지/새후보임의재생성금지.
- PHOTO분할/4×알고리즘·가중치재작업금지. 백업·입력8·버튼60준비반복금지.
- 300초timeout만늘리기, lock삭제, 잠금검증제거, 현장변조해시채택금지.
- 다른Python/Chrome프로세스일괄종료금지. 소유PID확인후해당작업만제어.
- 승인UI임의재설계금지. 완료모델/출력/사용자자료보존.
- 승인없는OpenAI/외부API키연결금지.
- Marketing HTTP·승인AVORA·광고자산/승인광고MP4는DEFERRED_EXTERNAL.
- 전체제품실증전최종문자열 `PASS_MINDLE_MEDIA_AI_FULL_PRODUCT_E2E_RUNTIME_VERIFIED` **발급금지**. 이문서에문자열을인용한것은발급이아님.
- 현재PC에R2가설치됐는지/정상동작하는지추측금지.
- 새창에서완료된ACTIONS/모델추론/3GB조립을다시시작하지않는다. 이미전달된파일을재사용한다.

## 15. 다음 창에서 그대로 실행할 시작 지시

NEXT_WINDOW_START_KO.txt를 다음창에이문서/ZIP과함께전달한다. 최소실행순서는 다음과같다.

1. 이문서0~5·13~14장과 TEST R2 active directive/contract를읽는다.
2. 브랜치/최신HEAD만조회한다. 인계이후변경이있으면diff만확인하고 기존후보source2e5…를유지한다.
3. 실제PC접근가능여부를확인한다. 이인계가PC연결복구를보장하지않음을인정한다.
4. 접근되면 TEST R2 남은물리PC/플레이어/청취/UI검수만진행한다. 접근안되면BLOCKED를구체화하고문서정합화등독립업무만수행한다.
5. 항목별 PASS/FAIL/PARTIAL/BLOCKED/DEFERRED로원본증거와함께기록한다. blanket PASS금지.

## 16. 이번 인계 패키지 구성·검증·한계

- 이전체MD와 NEXT_WINDOW_START_KO.txt.
- HANDOVER_STATE.json: 현재identity·남은항목·금지사항.
- DOWNLOAD_FILE_MANIFEST.json: 기존9개전달파일목록/bytes/SHA(증거ZIP은최신version1현재크기포함).
- PRIVATE_FILE_LOCATORS.json: 기존파일/사용자사진복구용private 식별자. 공개저장소게시금지.
- SOURCE_SNAPSHOTS: 관련원문69개. cce343…의Gitblob와69/69일치확인. 코드·지시서·ControlPlane·판정·계약이포함됨.
- SNAPSHOT_MANIFEST.json: 원문69개각 SHA256/Gitblob/크기.
- REPOSITORY_TREE_AT_cce3431.json: 저장소전체1,624트리항목index. 필요한과거파일을다시찾을수있으며전체파일bytes를동봉했다는뜻은아님.
- USER_INPUTS: 사용자오류사진2개와승인UI원본PNG. 승인원본cfeed… SHA확인. 사용자바탕화면사진은공개GitHub에올리지않는다.
- recovered: 기존 TEST R2 설치기와최신원본Runtime Evidence ZIP. 후자는CRC PASS. 3GB제품분할본7개는기존저장파일로연결하고중복동봉하지않음.
- PACKAGE_MANIFEST.json: 이번인계ZIP의모든파일hash/bytes.

인계확인범위는이창의보이는요청/사용자보고·현재저장소원문·기존전달파일metadata·복구한사진/증거다. 접근불가능한PC의미수신로그, 보이지않는다른창전체대화, 미검증원본의존재/정상여부를완전히확인했다고주장하지않는다. 미확보/미실행은위에명시해다음창으로넘긴다. 다른프로젝트의이미지/지시서가메모리에보여도MEDIA첨부자료로임의편입하지않는다.
