# AI 작업 실행·한국어 음성·MP4 통합 — 2026-10-18

판정: PARTIAL_PRODUCT / PASS_BOUNDED_SOURCE_RUNTIME. 구현 소스 `4bc645f4026ea8d0f1af4bfb09d614ac1166de58`. 기준21f7d12. Windows EXE·전체 승인 UI·범용 생성형 모델 완료는 아니다.

## 실제 구현
- SQLite WAL/FULL 기반 영속 작업 큐,단일 owner 파일 잠금,프로젝트/단계/시도 ID,요청 fingerprint replay,진행 상태/오류/worker PID/입출력 해시를 연결했다.
- QUEUED/RUNNING/RETRY_WAIT/CANCEL_REQUESTED/SUCCEEDED/FAILED/CANCELLED/INTERRUPTED를 영속 저장한다. 서버 시작 시 기존 DB를 열어 미완료 실행을 INTERRUPTED로 복구한다. 성공으로 바꾸거나 중단 모델 추론을 자동 반복하지 않는다.
- 각 단계는 별도 Python 프로세스와 전용 attempt 폴더에서 실행한다. 취소는 그 worker의 POSIX process group 또는 Windows의 해당PID process tree만 대상으로 한다. parent 종료 감시도 있다. 다른 Python/Chrome을 일괄 종료하지 않는다. Windows 분기는 이번에 native 검증하지 않았다.
- 일시적 오류 분류에 한해 최대3회,1/2초 간격 자동 재시도. 재시도 대기 중 취소 가능. 입력/인증/모델/TTS 미준비 및 미지원 작업은 무한 재시도하지 않는다.
- 모든 단계와 파일/ZIP 검증 후에만 작업·프로젝트를 게시한다. 원래 저장본 충돌을 검사하고 중단된 commit은 기존 프로젝트의 정확한 바이트로 복구한다. 공개 결과는 인코더 원시 경로 대신 별도 해시 검증 사본으로 봉인한다. 정상 완료 전/게시 목록 밖의 workflow 파일은 HTTP403이다.
- 기존 자연어 입력/작업 이력에 순차 실행 상태,취소,완료 프로젝트 열기,나레이션 재생·원본 목록 제외·음량 재합성·길이 정책을 연결했다. 기존 PHOTO/VIDEO 구조를 재설계하지 않았다. 이미 소리가 합성된 영상에 중복 믹싱하지 않고 명시적으로 원본에서 다시 합성한다. 추가 BGM은 해당 실행 입력으로 선택한다.
- 로컬 eSpeak NG Korean(규칙 기반 formant 합성)을 연결했다. 신경망 TTS라고 표시하지 않는다. 실제 원고→WAV·원고 파일·엔진/음성데이터 해시·버전·샘플레이트·채널·길이를 저장한다.
- FFmpeg로 원본 소리/나레이션/BGM의 명시적 음량을 합성한다. 타임스탬프 정규화,유한 무음 패딩,peak limiter,음성 초과 시 reject 또는 명시적 마지막 프레임 연장 정책을 적용했다. H264/yuv420p/AAC/faststart를 확인한다. 원본/16:9/9:16은 구분한다.
- 한국어 STT→자막 적용 단계는 기존 verified Whisper 호출에 연결했다. 이번에 기존 Whisper/SAM/SISR 가중치를 재추론하지 않았다. STT 새 큐 통합의 실제 모델 실행은 미검증이다.
- Save/Cold Reopen/Export에 새 음성·원고·영상·참고와 작업 이력을 포함한다. 나레이션을 STT 입력이나 자막으로 오인해 복원하지 않도록 분리했다.

## 계획기의 정확한 상태
범용 생성형 추론은 BLOCKED_LOCAL_GENERATIVE_MODEL_ABSENT다. 허용된 작업만 받는 구조화 계획 계약과 로컬 llama-cli/GGUF adapter,모델/실행파일 SHA와 고정40자리 revision/라이선스 확인 경로는 구현했다. 설치된 GGUF/실행기/승인 모델 receipt가 없어 실제 생성형 실행은0회다. 모델 출력은 whitelist 검증 후 계획 receipt를 고정하고,변경된 계획은 실행하지 않는다. 임의 shell/경로/외부 API 키를 모델 출력에서 실행하지 않는다.

실제 통합 시험의 계획 출처는 STRUCTURED_USER_PLAN_NOT_GENERATIVE다. `계획 JSON:`과 인용한 원고의 명시적 나레이션 명령은 생성형 모델 추론으로 표시하지 않는다. 전자의 실제 브라우저 실행을 검증했고,나레이션 명령 template는 구현 범위이며 동일한 정도의 별도 브라우저 검수로 집계하지 않았다.

MODEL SCOUT main `54e1cdfea0714102820626a8a19d9a366b439a72`의 runtime-executors.json을 확인했다. huggingface-model은 distilbert 감정 분류 모델이며,stt-tts라는 이름의 기본 모델도 Whisper-tiny다. 이를 생성형 계획기/TTS 생성 엔진으로 사용하지 않았다. 다른 branch/PR의 구현이 이 main 또는 MEDIA에 채택됐다고 주장하지 않는다.

## 최종 실제 증거
- Python113 PASS / Windows native2 SKIP. Node16 PASS. General/PC Control Plane validator PASS. PC 검수기 PASS는 gate/문서 정합성이지 사무실 PC PASS가 아니다. Actions/CI를 실행하지 않았다.
- 실제 ProductHttpServer와 Linux Chromium138에서 실제 영상 import→영상 보정·한국어 자막→한국어 원고 TTS→합성→프로젝트 저장/복원·참고1개 보존→나레이션 재생 요소·이력 확인. 나레이션을 재생성하지 않고 동일 voice job ID로 음량0.5 재합성했다. 실제 영상 재생과 MediaError0/readyState/videoWidth/currentSrc를 기록했다.
- 별도 실제 BGM 입력+나레이션+원본 소리의3입력 합성 PASS. 다른 저장 프로젝트의 원본 JSON 바이트가 보존됨을 확인했다. 이 BGM은 생성한 sine fixture이며 실제 승인 광고 음악/자산으로 표시하지 않는다.
- 제품 정상 종료:PID1480·instance`001b7a09-3397-4723-a931-10dd13e88205`→exit0·endpoint불응답→새PID1958·instance`7bb8d3e0-6461-456a-88dd-8aee4f922fe4`→동일project_id/작업 이력·자료 복원→Export PASS. 두번째 서버도 정상 종료했다. 이는 소스 Python 프로세스이며 Windows EXE 증거가 아니다.
- 최종 WAV:22050Hz/mono/3.121초/137700bytes. 실제 eSpeak Korean 합성이다. 사람 청취·발음·자연스러움·고급 신경망 음질은 미검증이다.
- 최종 MP4:H264/yuv420p/AAC,moov가mdat앞,실제 브라우저 재생 확인. ZIP의15개 manifest 파일 크기/SHA256과 CRC PASS. ARTIFACTS.json의 원본 WAV/MP4/ZIP/화면을 함께 게시한다.
- 취소/재시도 시험은 실제 큐/HTTP/별도 OS 프로세스를 사용했으나 sleep worker·일시 오류는 검수 경계에서 주입했다. 실제 고비용 모델의 중간 취소/외부 서비스 장애 재시도,Windows process-tree 종료가 검증됐다는 뜻은 아니다. 중단 commit 복구도 명시적으로 구성한 상태 fixture 검증이며 시스템 전원 차단 증거가 아니다.

## 발견·수정 및 한계
1. 합성 중 비정상 DTS 반복으로 종료하지 않는 문제가 실제 통합 시험에서 재현됐다. 오디오 시점/샘플레이트를 정규화하고 유한 패딩으로 바꿨다. timeout을 늘리지 않았다. BEFORE_RUNTIME_STDOUT와 최종 FFmpeg 경로/결과를 보존했다.
2. 재합성 검수에서 원시 edited_video.mp4가48bytes로 바뀌는 현상을 관찰했다. 해당 쓰기 주체를 확정하지 못했다. 이를 근거 없이 제품/환경 한쪽의 확정 원인으로 표시하지 않는다. 별도 검수 실행을 겹치지 않는 단일 orchestrator로 통합하고,입력 사본·결과 봉인·HTTP 게시 whitelist·사후 해시 gate를 추가했다. 원시 attempt 파일을 바꿔도 게시 결과/Export를 보존하는 회귀가 PASS이며,최종 실제 전체 흐름도 PASS다. Windows에서도 원본·게시 파일 해시 보존을 반드시 재검수한다. 쓰기 주체에 대한 추가 진단은 남아 있다.
3. 기존 승인 UI 전체 일치 FAIL(배너 원화/Timeline·전체 높이 차이)은 이번 기능 연결로 해소됐다고 주장하지 않는다.

## 다음 단계
- General: 검증된 로컬 생성형 GGUF/llama-cli/모델카드·라이선스·40자리revision·파일SHA를 확보·검수해 실제 자연어 계획 추론을 별도 실행한다. 외부 키 연결은 하지 않았다. MODEL SCOUT 등록 이름만으로 완료하지 않는다.
- General: TTS 신경망 음질이 요구되면 검증할 모델과 해당 adapter/자원을 구체화한다. 현재 eSpeak는 실제 동작 가능한 로컬 음성 합성 경로이며 최종 음질 승인은 아니다.
- General: 승인 UI 차이 및 STT 큐 실제 모델 연결 검증·실제 모델 실행 중 취소를 남은 범위로 관리한다. 이미 끝난 분할/4× 추론은 반복하지 않는다.
- 후보 발행 담당: Build Gate=false. 유효한 새 승인 전 빌드하지 않는다. 현재 c37에는 이 소스가 없다. 이후 Windows engine/DLL/음성데이터/manifest와새 JS/Python이 포함된 후보 source/EXE/ZIP 해시 독립 검증이 필요하다. 설치 번들의 RUNTIME_ENGINES.json 상대경로를 자동 해석하므로 직원에게 config 수동 작성을 요구하지 않는다. 현재 Linux TTS 바이너리를 Windows용으로 재사용하지 않는다.
- Windows: 정식 후보 인계 후 EXE→작업/취소/재시도/음성→Save→완전 종료/PID소멸→EXE재실행/새PID→동일자료·이력복원→MP4/ZIP→설치플레이어/실제청취·최종UI. 실행 환경이 없는 이 창에서 사무실 PC 인수 완료를 발행하지 않는다.

PR23 HOLD / DO NOT MERGE. main/force push 금지. Build Gate=false. OpenAI 미연결. Marketing/AVORA/승인 광고 MP4 DEFERRED_EXTERNAL. 직원 최종 패키지 미생성. 전체 제품 최종 PASS 미발행.
