# MINDLE MEDIA AI R3 사무실 PC 최종 인수 지시서

기준일: 2026-10-24
대상 후보: `MINDLE_MEDIA_AI_PC_TEST_20261024_R3`
후보 소스: `9f5d304ce825ad622bcd64df6ad3c8f154dfd3b6`

## 목적

이미 원격 Windows에서 검증한 R3 후보를 다시 만들지 않고 실제 사무실 PC에서 인수한다. 패키지 identity, 제품 서버 완전 종료와 새 PID 재실행, 프로젝트 복원, MP4 재생·탐색·사람 청취를 하나의 증거 묶음으로 수집한다.

## 실행

`docs/handoff/MINDLE_MEDIA_AI_R3_OWNER_PC_ACCEPTANCE_KIT_20261025.zip`을 압축 해제하고 R3가 설치된 PC에서 `START_R3_OWNER_PC_ACCEPTANCE.cmd`를 두 번 클릭한다. 실행기는 새 입력을 생성한 뒤 Qwen 계획, Supertonic 한국어 신경망 음성, FFmpeg MP4를 실제로 새로 만든다. 이 단계가 실패하면 창이 열려도 인수를 중단한다. 이어서 사진·영상·자막·나레이션·참고 이미지가 포함된 프로젝트를 저장하고 Export한다. Windows 플레이어에서 자동으로 열린 MP4를 재생하고 앞뒤 탐색하며 실제 소리를 듣는다. 서버 재실행 뒤 동일 프로젝트를 Reopen하고 다시 Export한다.

실행기는 다음 항목을 자동 검증한다.

- R3 EXE SHA-256, manifest SHA-256, manifest 19,341개 파일 전체
- 정확한 설치 runtime root와 runtime manifest identity
- 새 4초 입력에 대한 Qwen 실제 생성형 계획과 요청 수치·원고 보존
- Supertonic 실제 신경망 한국어 음성 생성과 FFmpeg 영상·오디오 MP4 생성
- 저장 프로젝트·workflow·architecture production 상태
- MP4 SHA-256과 ffprobe 스트림 정보
- 소유 서버 control nonce를 사용한 정상 종료와 endpoint 닫힘
- 새 PID·새 server instance 재실행과 동일 project ID 복원

결과는 바탕 화면의 `MINDLE_MEDIA_AI_R3_ACCEPTANCE_날짜_시각` 폴더와 같은 이름의 ZIP에 남긴다.

## 판정 제한

- 질문에는 실제 관찰 사실만 `Y`로 답한다.
- `approved_ui_pixel_match`와 `full_product_pass`는 이 도구가 자동 승인하지 않는다.
- R3 이후 UI 소스 보강은 이 후보에 포함되지 않았다.
- PR #23은 HOLD / DO NOT MERGE를 유지한다.
- 실패 시 다른 Python·Chrome 프로세스를 일괄 종료하거나 lock 파일을 삭제하지 않는다.
- 현재 Build Gate=false를 유지하며 이 인수를 이유로 새 패키지를 만들지 않는다.
