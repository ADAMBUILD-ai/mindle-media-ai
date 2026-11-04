# MINDLE MEDIA AI Windows AI 실행 공간 R3 결과

- 판정: **REMOTE WINDOWS DEVELOPMENT CANDIDATE PASS / OFFICE PC PENDING**
- 소스: `9f5d304ce825ad622bcd64df6ad3c8f154dfd3b6`
- 실행: https://github.com/ADAMBUILD-ai/mindle-media-ai/actions/runs/40079944004
- 검증 후보: `MINDLE_MEDIA_AI_PC_TEST_20261024_R3.zip`
- ZIP SHA-256: `e6e05a2b74f806095a6afce13e3af46ddc586870917908250426f215cff1bbe1`

## 실제 통과

- Qwen2.5-1.5B GGUF를 llama.cpp로 실제 실행해 한국어 복합 명령을 구조화된 계획으로 변환했다.
- 요청의 밝기 `3`, 한국어 나레이션, 영상 길이 연장을 검증한 뒤 순차 실행했다.
- sherpa-onnx / Supertonic 3가 한국어 WAV를 실제 신경망 추론으로 생성했다.
- Qwen 건축 영상 계획기가 두 입력을 배치하고, 명시된 전체 2초와 16:9 계약을 실행 가드레일로 맞췄다. 보정 전 모델 합계 4초와 적용 합계 2초를 영수증에 기록했다.
- 디코딩한 실제 프레임의 노출·움직임·선명도 측정값으로 각 장면 시작 구간을 선택했다.
- FFmpeg가 H.264/yuv420p/AAC/faststart, 1280×720, 2초 MP4를 생성했다.
- Chrome에서 `MediaError=0`, `readyState=4`, 실제 재생 진행을 확인했다.
- 서버 PID 1280 종료와 endpoint 닫힘 후 PID 7868로 재실행했다.
- 일반 프로젝트와 건축 프로젝트, Qwen 작업 이력, Supertonic 음성 참조를 복원하고 API 및 UI Export를 완료했다.
- 실행 후 payload 19,341개 파일의 해시가 유지됐고, 별도 Ubuntu readback에서 전체 payload hash와 ZIP CRC를 통과했다.

## 실행 공간의 의미

Qwen·llama.cpp·Supertonic은 외부 오픈소스 엔진/모델이다. 이번 후보는 이 바이트를 검증된 TEST R2에서 그대로 재사용하고, MINDLE이 소유한 계획 계약, 수치 가드레일, 영속 큐, 실제 프레임 측정, 영상 합성, 저장·복원, UI와 증거 체계를 하나의 로컬 제품 실행 공간으로 연결한다.

## 남은 실제 인수

- 사무실 PC 더블클릭 설치·실행
- 사람이 듣는 한국어 발음·자연스러움과 실제 소리 확인
- 승인 화면과 동일 viewport의 픽셀 수준 대조

이 세 항목은 원격 Windows 결과로 대체하지 않았다. PR #23은 HOLD / DO NOT MERGE이고, main 병합·직원 최종 배포·전체 제품 PASS는 발행하지 않는다.
