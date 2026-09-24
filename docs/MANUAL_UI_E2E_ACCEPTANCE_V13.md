# MINDLE MEDIA AI v13 — 수동 UI E2E 검수

상태: **PENDING_HUMAN_APPROVAL**

자동 검증은 완료되었지만, 이 문서는 신작가님의 실제 승인 UI 검수 전까지 Final Closeout 및 상용 해제를 금지합니다.

## 고정 조건

- 승인 UI의 디자인·레이아웃·명칭·패널 위치: 변경 없음 (`UI_SSOT_CHANGED: NO`)
- CPU only / GPU 미사용 / Production·main 변경 없음
- 실행 기준 private HF cache revision: `9202e5744a191fa77562b0c0ffe6af8053f8e3d9`

## 검수 순서

1. 사진 편집에서 실제 사진을 업로드하고 객체 선택을 실행합니다. 실제 SAM mask/overlay가 중앙 Preview에 반영되는지 확인합니다.
2. 같은 사진에서 4× upscale을 실행합니다. 실제 결과가 Preview에 표시되고 원본보다 4배 해상도인지 확인합니다.
3. 영상 편집에서 실제 영상을 업로드하고 tracking을 실행합니다. tracking overlay가 Preview/Timeline에 반영되는지 확인합니다.
4. 실제 한국어 음성 파일을 입력하고 STT를 실행합니다. 생성 텍스트가 고정 문자열이 아닌 실제 음성 내용인지 확인합니다.
5. 사진·영상 프로젝트 각각을 저장하고 내보냅니다. 생성 파일을 열어 결과가 유지되는지 확인합니다.

## 승인 기록

다섯 항목 모두 실제 화면에서 확인된 경우에만 다음 문구를 회신합니다.

> v13 수동 UI E2E 검수 승인: PHOTO segmentation / VIDEO tracking / 4× upscale / Korean STT / Preview·저장·내보내기 모두 PASS

이 승인 전 상태: `RELEASE_CANDIDATE_PASS: NO`, `COMMERCIAL_RELEASE_BLOCKED: YES`, `MINDLE_MEDIA_AI_FINAL_CLOSEOUT: NOT_DECLARED`.
