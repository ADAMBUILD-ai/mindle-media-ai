# 승인 PHOTO 구조 복원 — 2026-10-17

최종 PARTIAL. 원격 보고 b68b8fc와 최신 승인 이미지 원본을 직접 대조하고 PHOTO의 확인된 구조 차이부터 수정했다. 전체 승인 UI는 여전히 FAIL이며 후속 후보는 제작하지 않았다.

## 접수와 기준
- 기준 HEAD: b68b8fc737abac70175bd4c0abb6ae5ab64580fd. c1956f4 전환 표시 초기화 수정과 선행 수정은 보존한다.
- RESULT_KO.md / UI_IMAGE_COMPARISON_FINAL_KO.md 원문 접수 확인. 보고된 41개 증거·6개 ZIP은 이번 턴에 전부 다시 내려받아 독립 검증한 것으로 주장하지 않는다.
- 최신 APPROVED_REFERENCE.png 직접 열람: 2,021,140 bytes / SHA256 cfeed43d4864dfe4cc1505dbb37d1ac44871d51cd10907f27cb2abe3694ae339. 옛 F27E 상하 배치가 아니다.

## 실제 변경
1. PHOTO 우측 세로 도구를 미리보기 아래로 이동. 7개 보정 가로 배치, 세부 기능 아래 배치. 원래 도구와 data attribute 유지.
2. 좌측의 연결되지 않은 REFERENCE 예시 문구 제거. 기존 실제 참고 파일 추가 버튼·input·list를 별도 가로 Strip으로 이동.
3. 참고 렌더링과 제거 이벤트의 조회 범위를 editor로 확장해 command 카드 밖에서도 첨부·제거·복원이 동작한다. 실제 첨부 Blob URL 썸네일과 파일명을 표시한다. 예시 자산을 실제 파일로 위장하지 않는다.
4. PHOTO crop/resize hidden 속성을 기존 display:grid가 무시하는 것을 브라우저에서 확인. PHOTO에 한정해 hidden을 존중하도록 수정했다. crop 클릭 시 표시·초기화 시 숨김도 검증했다.

## 검증과 경계
- Node 제품 회귀 16 PASS. product_integration.js, photo_workspace.js, video_workspace.js는 기준에서 변경하지 않았다.
- 실제 Linux Chromium 138 / 1536x1024, 1366x1024: 수정 전 tools가 preview 우측인 것을 계측, 수정 후 preview 하단으로 이동 및 reference Strip 하단 배치 확인.
- PHOTO preview 폭 408→544px(1536), 353→489px(1366). VIDEO preview 폭 각각408/353px 그대로.
- 실제 파일 input의 첨부→이미지 표시→입력 focus 후 유지→제거→복원 이벤트, crop 열기/초기화, 7보정·광고 숏폼·Save/Export 버튼 존재 확인. fixture portrait480x960의 contain/center 확인. pageerror0.
- 검수는 실제 제품 HTML/CSS/JS를 정적 HTTP 서버에서 실행했다. /api/assets/latest는 검수 fixture 응답이며 실제 Save/Export/모델/API 통합 재실행은 아니다. Save/Export 존재 확인을 실행 PASS로 확대하지 않는다.
- 스크린샷 환경에는 한글 폰트와 demo 이미지가 없어 글꼴 대조/전체 시각 승인에 사용할 수 없다. BROWSER.json의 geometry와 첨부 이벤트 검증만 채택한다. Windows 최종 UI 비교는 남아 있다.
- 새 Python 제품 코드·모델·가중치 변경 없음, 추론0. 이전 Python46/실제 Chrome 경계 검증은 제출 보고의 기존 성과로 보존하고 이번 신규 실행으로 집계하지 않는다.

## 남은 마감
1. 헤더 카메라 배너·아이콘·탭 비율, Timeline thumbnail/waveform/clip, 전체 비율·AI 입력 강조는 아직 승인 원본과 차이가 있다. 전체 UI FAIL 유지. 작동하지 않는 clip 편집이나 임의 파형을 그려 완료로 표시하지 않는다. 헤더 원본 자산/실제 미디어 기반 Timeline 시각화와 기존 동작 연결을 후속 소스 작업으로 진행해야 한다.
2. 이번 PHOTO 구조 수정도 Windows Chrome 및 승인 원본 같은 viewport/zoom 대조와 전체 버튼·Save/Reopen/Export 영향을 인수해야 한다. Linux geometry PASS는 최종 승인 일치가 아니다.
3. 브라우저 다운로드 취소는 기존 TXT 대조에서도 발생한 환경 BLOCKED로 유지한다. 서버 생성/GET 성공과 분리한다.
4. Build Gate=false, 후보 미제작. 유효한 후속 승인과 UI 잔여 마감 후에만 후보 source/manifest/EXE/ZIP SHA 고정·독립 검증→사무실 PC 완전 종료/재실행/복원/Export→실제 소리 청취·최종 UI 인수.

PR23 HOLD / DO NOT MERGE, main/force push 금지, 직원 최종 패키지 재생성 금지. Marketing/AVORA DEFERRED_EXTERNAL. 전체 제품 최종 PASS 발행하지 않음.
