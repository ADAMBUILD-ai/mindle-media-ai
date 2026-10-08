# MINDLE MEDIA AI General Work 최종 전수점검 지시서 v1.0

기준일: 2026-10-08  
Epoch: MEDIA-AI-20261008-GENERAL-WORK-FINAL-FULL-AUDIT-R1

## 1. 목적

오늘까지 General Work에서 개발·수정한 MINDLE MEDIA AI 전체를 대상으로 “끝났다고 생각했지만 빠진 기능”을 잡아내는 최종 전수점검을 수행한다.

이번 단계는 패키징 단계가 아니다. PC Work로 넘기기 전에 코드, UI 연결, Runtime, 저장/재열기, Export까지 실제 동작이 끊기지 않았는지 검수하고, 누락·불완전 항목이 발견되면 General Work에서 직접 보완한 뒤 재검증한다.

## 2. 기준 원칙

- 문서 존재만으로 PASS 금지
- 코드 존재만으로 PASS 금지
- 테스트 함수 존재만으로 PASS 금지
- UI 버튼 존재만으로 PASS 금지
- 실제 Runtime Evidence가 있어야 PASS
- Evidence 없는 PASS 금지
- Mock / Placeholder / TODO / FIXME / 임시 Fallback / Dead button / 연결 안 된 route를 전부 탐지
- 하나라도 PARTIAL / FAIL / NOT_IMPLEMENTED가 있으면 PC Work 인계 금지
- 외부 Marketing / AVORA 연동은 이번 General Work 완료 조건에서 분리하고 BLOCKED_EXTERNAL로만 기록
- main 변경 금지
- PR #23은 HOLD / DO NOT MERGE 유지
- PC Work 패키징 금지

## 3. 최신 UI SSOT 기준

검수 기준 UI는 이전 UI가 아니라 2026-10-08 최종 승인본이다.

### PHOTO
- 가로형 Preview가 기본
- VIDEO와 전체 높이·폭·그리드 정렬
- 보정 기능은 Preview 하단 중심
- 세로 사진은 동일 Preview 안에서 원본 비율 유지 + Auto Fit + 중앙 정렬
- 좌우 여백은 다크 네이비 또는 약한 Blur 처리
- 강제 Stretch / 강제 Crop 금지

### VIDEO
- 승인된 기존 구조 유지
- Preview / Timeline / Track / Subtitle / Effect / Audio / AI 편집 흐름 유지

### 공통
- 상단 제품명: MINDLE MEDIA AI
- Dark Navy
- VIDEO: Blue / Cyan
- PHOTO: Purple / Magenta
- 전체 재디자인 금지

## 4. 전수점검 범위

### A. 코드 인벤토리
다음 전체를 스캔한다.
- src / app / ui / frontend / backend / api / services / models / scripts / tests
- route / endpoint / command / event handler / IPC / websocket / worker
- config / env / model runner / ffmpeg / persistence / export
- launcher 관련 코드가 있으면 존재만 확인하고 이번 단계에서 패키징하지 않는다

확인 항목:
- 미사용 코드
- 끊긴 import
- 죽은 route
- UI에서 호출되지 않는 기능
- UI는 있으나 backend handler가 없는 기능
- backend는 있으나 UI에서 접근 불가한 기능
- Mock 데이터 의존
- TODO / FIXME / HACK / placeholder
- 임시 timeout 우회
- silent exception
- 실패를 PASS로 오인하는 완료 판정

### B. PHOTO 기능
최소 다음을 실제 Runtime으로 재확인한다.
- 사진 불러오기
- 가로 사진 Preview
- 세로 사진 Auto Fit
- 원본 비율 유지
- 밝기
- 대비
- 하이라이트
- 그림자
- 채도
- 색온도
- 선명도
- 크롭 / 회전
- AI 보정
- 배경 제거
- 색감 보정
- 스타일 변환
- 인물 보정
- 분할
- 4× 업스케일
- 업스케일 결과 Preview
- 고해상도 결과 저장
- 유사 이미지 검색 / 참고 이미지 진입점이 설계에 포함된 경우 실제 연결 여부

기존 PHOTO 분할·4× 실모델 PASS는 무의미하게 재연산하지 말고, 변경 영향이 없으면 기존 Evidence를 재사용하되 연결 회귀만 확인한다.

### C. VIDEO 기능
- 영상 불러오기
- 실제 브라우저 Preview
- H.264 / yuv420p / faststart Preview 경로
- Timeline
- 영상 Track
- Audio Track
- Subtitle Track
- Effect Track
- 자르기 / 분할
- 속도
- 필터 / 색보정
- 자막
- 오디오 편집
- 장면 전환
- AI 효과
- 하이라이트 추출
- 숏폼 변환 내부 기능
- 한국어 STT
- STT 결과 UI 표시

브라우저 Preview는 MediaError.code / readyState / videoWidth / currentSrc를 필요 시 기록한다.

### D. AI 대화 편집
자연어 명령이 실제 handler와 Runtime까지 전달되는지 확인한다.

대표 명령:
- “30초 숏폼으로 만들어줘”
- “자동으로 자막 넣어줘”
- “배경음악을 잔잔하게 바꿔줘”
- “이 사진을 따뜻하게 보정해줘”
- “배경을 제거해줘”
- “분할해줘”

명령이 UI에만 표시되고 실제 실행으로 전달되지 않는 항목은 FAIL이다.

### E. 저장 / 재열기 / 상태 복원
- Save
- 완전 종료
- Reopen
- 편집 상태 복원
- 연결된 미디어 경로 복원
- STT / 자막 / 편집 값 복원
- 오류 발생 시 손상된 상태로 PASS 처리하지 않는지 확인

### F. Export
- PHOTO 결과 Export
- VIDEO 결과 Export
- 다운로드 또는 저장 완료
- SHA-256 확인
- ZIP 또는 패키지 산출물이 있으면 CRC 확인
- 브라우저에서 실제 열리는 결과인지 확인
- 임시 경로에만 생성되고 사용자 결과가 없는 경우 FAIL

### G. 오류·예외 처리
대표적으로:
- 파일 없음
- 지원하지 않는 확장자
- 손상 미디어
- 모델 조회 실패
- 네트워크 없음
- 디스크 공간 부족
- 포트 충돌
- 브라우저 decode 실패
- 모델 실행 실패
- Export 실패
- Save 실패

오류가 발생했는데 성공 UI가 뜨는 경우 FAIL이다.

## 5. 외부 연동 분리

다음은 이번 General Work FULL PASS 조건에서 제외한다.
- Marketing 실제 HTTP
- MARKETING_SHORTFORM_BASE_URL
- MARKETING_SHORTFORM_BRIDGE_TOKEN
- AVORA 승인 자산
- 외부 9:16 광고 숏폼 대표 승인
- 외부 광고 MP4 delivery

이들은 반드시 BLOCKED_EXTERNAL_SHORTFORM_INTEGRATION으로 분리 기록한다.

외부 연동 미완료를 이유로 미디어 AI 자체 General Work PASS를 막지 않는다.
반대로 외부 연동을 핑계로 미디어 AI 내부 누락을 BLOCKED_EXTERNAL로 분류하면 안 된다.

## 6. 판정 체계

각 항목은 다음 중 하나로만 판정한다.

- PASS
- PARTIAL
- FAIL
- NOT_IMPLEMENTED
- BLOCKED_EXTERNAL

PASS에는 반드시 다음 Evidence가 있어야 한다.
- 실행 경로
- 입력
- 실제 출력
- 로그 또는 테스트 결과
- 관련 코드 경로
- 필요 시 산출물 SHA-256
- 변경 커밋

## 7. 수정 규칙

PARTIAL / FAIL / NOT_IMPLEMENTED 발견 시:
1. 원인 기록
2. General Work에서 최소 범위 수정
3. 관련 회귀 테스트
4. 실제 Runtime 재실행
5. Evidence 갱신
6. PASS로 바뀔 때까지 반복

금지:
- 단순 timeout 증가만으로 해결
- 실패를 skip 처리하여 PASS
- mock 결과로 대체
- 코드 주석만 수정하고 해결 선언
- UI 재디자인
- main 병합
- PR #23 병합
- 패키징으로 문제 은폐

## 8. 최종 종료 조건

아래 조건을 모두 만족해야 General Work를 종료한다.

- 내부 제품 항목에 PARTIAL 없음
- 내부 제품 항목에 FAIL 없음
- 내부 제품 항목에 NOT_IMPLEMENTED 없음
- BLOCKED_EXTERNAL은 외부 Marketing / AVORA 범위에만 존재
- 최신 승인 UI와 실제 기능 연결 일치
- PHOTO / VIDEO / AI 대화 편집 / STT / Save-Reopen / Export 실제 Runtime PASS
- 기본 CI PASS
- Evidence Contract 충족
- 최종 검수보고서 저장
- 원격 readback 확인

최종 PASS 문자열:

PASS_MINDLE_MEDIA_AI_GENERAL_WORK_FULL_AUDIT_RUNTIME_VERIFIED

## 9. PC Work 인계 조건

General Work PASS 후에만 PC Work로 넘긴다.

PC Work의 다음 범위:
1. 최종 승인 UI 적용 상태 확인
2. 복잡한 직원용 설치 패키지 제작 금지
3. 원클릭 구동 패키지 제작
4. 더블클릭 1회 → 필요한 로컬 서비스 자동 시작
5. 준비 완료 후 기본 브라우저 자동 오픈
6. 중복 실행 방지
7. 직원에게 개발 콘솔 노출 금지
8. 실제 직원 PC에서 실행 검증
9. 최종 종료 선언

설치형 패키지는 향후 별도 단계로 보류한다.
