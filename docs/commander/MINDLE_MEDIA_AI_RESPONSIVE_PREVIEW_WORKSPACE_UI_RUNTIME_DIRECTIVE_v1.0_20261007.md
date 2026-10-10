# MINDLE MEDIA AI — RESPONSIVE PREVIEW WORKSPACE UI RUNTIME DIRECTIVE v1.0

**Date:** 2026-10-07  
**Status:** QUEUED — NEXT UI WORK AFTER CURRENT EMPLOYEE PACKAGE R2 CLOSEOUT  
**Repository:** `ADAMBUILD-ai/mindle-media-ai`  
**Canonical Branch:** `feature/ad-shortform-bridge-p0-20260926`

---

## 0. EXECUTION ORDER / CONTROL PLANE

이 지시서는 현재 `CURRENT_PC_WORK_DIRECTIVE.md`의 Active 작업인 **EMPLOYEE PACKAGE FINAL CLOSEOUT R2**를 중단하거나 대체하지 않는다.

현재 R2가 Evidence와 사령관 검수로 종료된 뒤, 또는 사령관이 명시적으로 본 지시서를 Active로 전환했을 때 실행한다.

금지:
- 현재 R2 작업 중 임의 lane 전환
- main merge
- force push
- 새 repo 생성
- 임의 worktree 생성
- 승인되지 않은 UI 전면 재설계
- Evidence 없는 PASS

---

## 1. PURPOSE

2026-10-07 Owner UI 검토 기준을 실제 MINDLE MEDIA AI Runtime에 반영한다.

핵심 원칙은 다음 한 문장으로 고정한다.

> **사진·영상의 본래 비율은 유지하고, Preview 아래 남는 공간에 필요한 기능들을 내려 배치해서 화면 낭비와 하단 기능 잘림을 동시에 없앤다.**

목표는 화면을 억지로 꽉 채우는 것이 아니라 **실제 작업하기 편하고, 어떤 화면 크기에서도 필요한 기능에 접근 가능한 UI**를 만드는 것이다.

---

## 2. IMMUTABLE UI SSOT

기본 승인 UI:

`ui/assets/ssot/MINDLE_MEDIA_AI_APPROVED_FINAL_20260913.png`

기준 SHA-256:

`f27eeb5031d83d7015494bc1683a981488ac4806627dc91c21f1c8c523df2541`

Shortform Addendum:

`docs/ssot/MINDLE_MEDIA_AI_SHORTFORM_UI_SSOT_ADDENDUM_v1.0_20260926.md`

최종 UI 정의:

**F27E base + Shortform Addendum**

VIDEO action order는 유지한다.

`영상 불러오기 → AI 자동 편집 → 광고 숏폼 → 프로젝트 저장 → 내보내기`

`광고 숏폼` 버튼 삭제/누락은 불합격이다.

안정적인 workspace geometry 기준 commit:

`97900cc6c784e74b4224333fa2cc84d29c611f87`

과거 잘못된 clipping commit:

`2ab174e03dc786c53f38ba956dea95f8e1ccd5a7`

위 clipping 방식은 재도입하지 않는다.

---

## 3. OWNER-APPROVED UI DIRECTION

### 3.1 Preview는 원본 비율 우선

- VIDEO Preview는 영상 원본 aspect ratio를 유지한다.
- PHOTO Preview는 사진 원본 aspect ratio를 유지한다.
- 화면을 채우기 위해 미디어를 세로로 늘이거나 왜곡하지 않는다.
- Preview가 다른 기능을 화면 밖으로 밀어낼 정도로 과도하게 커지지 않게 한다.
- 필요한 경우 `object-fit`, aspect-ratio container, max-height, min/max sizing 등 적절한 반응형 규칙을 사용한다.

### 3.2 Preview 하단 유휴공간을 버리지 않는다

가로형 미디어 등으로 Preview 아래에 공간이 남으면, 그 영역을 단순 공백으로 방치하지 않는다.

기존 기능 중 작업 흐름상 적절한 것을 Preview 하단으로 재배치한다.

우선 검토 대상:
- VIDEO Timeline
- 실행 상태 / Job 상태
- 결과 확인
- 보조 편집 컨트롤
- 저장 / 내보내기 관련 보조 상태
- 현재 우측 또는 하단에 몰려 화면 밖으로 밀리는 기능

단, 기존 기능을 임의 삭제하거나 완전히 다른 UI 체계로 바꾸지 않는다.

### 3.3 상단 작업 / 하단 기능 구조

화면은 자연스럽게 다음 구조를 따른다.

**상단**
- 실제 VIDEO / PHOTO Preview
- 핵심 작업 진입
- 미디어 상태

**하단**
- 해당 미디어 편집 기능
- Timeline
- 실행 상태
- 결과 확인
- 저장 / 내보내기 등 후속 작업

하단은 남는 공간을 적극 활용하되 Preview를 침범하거나 원본 비율을 훼손하지 않는다.

---

## 4. VIDEO REQUIREMENTS

VIDEO 화면은 다음을 만족해야 한다.

1. 가로 영상(예: 16:9) 원본 비율 유지
2. 세로 영상(예: 9:16) 원본 비율 유지
3. 정사각 또는 기타 비율 영상도 왜곡 금지
4. Preview 아래 유휴공간 활용
5. Timeline 및 주요 편집 기능이 화면 밖으로 사라지지 않음
6. 창 높이가 줄어도 주요 기능 접근 가능
7. `광고 숏폼` 버튼 유지
8. 프로젝트 저장 / 내보내기 접근 가능
9. 현재 승인 UI의 다크 네이비 언어와 정렬 체계 유지

---

## 5. PHOTO REQUIREMENTS

PHOTO도 VIDEO와 동일한 원칙을 적용한다.

1. 가로 사진 원본 비율 유지
2. 세로 사진 원본 비율 유지
3. 정사각 사진 원본 비율 유지
4. Preview 아래 남는 공간을 편집 / 결과 / 작업 기능에 활용
5. 하단 기능이 화면 밖으로 잘리지 않음
6. PHOTO와 VIDEO의 전체 UI 언어와 정렬 기준 통일
7. Preview를 필요 이상으로 키우지 않음
8. 기존 승인 PHOTO 기능 삭제 금지

---

## 6. RESPONSIVE / CLIPPING RULE

다음 방식은 금지한다.

- 고정 높이만으로 전체 workspace를 강제
- `overflow:hidden`으로 기능을 잘라 숨김
- 낮은 해상도에서 버튼/Timeline/Save/Export가 사라지는 구조
- Preview 크기를 유지하기 위해 기능을 viewport 밖으로 밀어냄

필요한 경우:
- 내부 영역 독립 scroll
- min/max sizing
- flex/grid 재배치
- viewport-aware height
- breakpoint 기반 재배치

를 사용한다.

단, 스크롤을 추가했다는 이유만으로 PASS하지 않는다. 실제 주요 기능이 항상 접근 가능해야 한다.

---

## 7. LIVE UI vs SSOT CHECK

작업 전 반드시 현재 실제 Runtime UI와 승인 SSOT를 대조한다.

확인 항목:
- dark navy visual styling 실제 적용 여부
- VIDEO / PHOTO 구조
- Preview geometry
- Timeline 위치
- 자연어 명령 영역
- Reference Image
- 프로젝트 저장
- 내보내기
- 광고 숏폼
- 화면 높이 축소 시 clipping 여부

코드나 DOM에 요소가 존재한다는 이유만으로 PASS하지 않는다.

**실제 화면에서 보이고 사용할 수 있어야 한다.**

승인되지 않은 새로운 색상/폰트/버튼 스타일을 임의로 추가하지 않는다.

---

## 8. REQUIRED RUNTIME TEST MATRIX

최소 다음 화면 조건을 실제 Runtime에서 검증한다.

### Desktop
- 일반 데스크탑 화면
- maximized
- 창 높이 축소
- 창 폭 축소

### Laptop
- 일반 노트북 수준 viewport
- 낮은 화면 높이 조건

### VIDEO
- 16:9
- 9:16
- 1:1 또는 비표준 비율 1종

### PHOTO
- 가로 사진
- 세로 사진
- 1:1 사진

각 조건에서 다음을 확인한다.

- Preview 왜곡 없음
- 기능 clipping 없음
- 하단 기능 접근 가능
- Timeline 접근 가능
- Save 접근 가능
- Export 접근 가능
- 광고 숏폼 접근 가능
- 필요 scroll 정상 동작
- 화면 공간 낭비가 과도하지 않음

---

## 9. REGRESSION REQUIREMENTS

이번 UI 수정으로 기존 직원 패키지 기능을 깨뜨리면 불합격이다.

최소 회귀 확인:
- VIDEO import
- PHOTO import
- Preview
- 프로젝트 Save
- Reopen
- Export
- Korean STT
- SAM PHOTO segmentation
- SAM VIDEO tracking
- Intel 4× upscale
- 광고 숏폼 unavailable 시 graceful handling
- Desktop launch

기존 기능 전체를 다시 개발하지 말고, 이미 PASS Evidence가 유효하면 재사용할 수 있다.

다만 이번 UI 변경으로 영향을 받는 항목은 반드시 다시 실행 검증한다.

---

## 10. REQUIRED EVIDENCE

Evidence root:

`evidence/pc_remote/media-ai-responsive-preview-workspace-ui-runtime-v1-20261007/`

최소 산출물:

1. `BEFORE_VIDEO_FULL.png`
2. `AFTER_VIDEO_16x9_FULL.png`
3. `AFTER_VIDEO_9x16_FULL.png`
4. `AFTER_VIDEO_REDUCED_HEIGHT.png`
5. `AFTER_PHOTO_LANDSCAPE_FULL.png`
6. `AFTER_PHOTO_PORTRAIT_FULL.png`
7. `AFTER_PHOTO_SQUARE_FULL.png`
8. `AFTER_PHOTO_REDUCED_HEIGHT.png`
9. `FUNCTION_ACCESSIBILITY_CHECK.md`
10. `UI_SSOT_COMPARISON.md`
11. `RUNTIME_TEST_MATRIX.md`
12. `REGRESSION_RESULT.md`
13. `CHANGED_FILES.txt`
14. `MINDLE_MEDIA_AI_RESPONSIVE_PREVIEW_WORKSPACE_UI_RUNTIME_EVIDENCE_v1_0_20261007.json`

Machine Evidence JSON에는 최소 다음을 기록한다.

- branch
- starting commit
- final commit
- changed files
- runtime launch method
- runtime URL/host if applicable
- tested viewport sizes
- tested media aspect ratios
- VIDEO result
- PHOTO result
- clipping result
- accessibility result
- shortform button result
- save/export result
- regression result
- final status

---

## 11. PASS / FAIL RULE

### PASS 조건

다음이 모두 만족될 때만 PASS다.

- VIDEO 원본 비율 유지
- PHOTO 원본 비율 유지
- Preview 왜곡 없음
- Preview 하단 유휴공간을 작업 기능에 합리적으로 활용
- 낮은 화면 높이에서도 기능 소실 없음
- VIDEO / PHOTO 모두 정상
- Timeline 접근 가능
- 저장 / 내보내기 접근 가능
- 광고 숏폼 유지
- 승인 UI 디자인 언어 유지
- 기존 주요 기능 regression 없음
- 실제 Runtime screenshot Evidence 존재
- Machine Evidence 존재
- remote commit readback 완료

### FAIL / REWORK 조건

다음 중 하나라도 있으면 PASS 금지.

- `overflow:hidden` 등으로 하단 기능이 사라짐
- Preview가 왜곡됨
- Preview를 과도하게 키워 기능이 밀려남
- PHOTO 또는 VIDEO 한쪽만 검증
- 광고 숏폼 누락
- Save / Export 접근 불가
- 승인 UI와 무관한 재디자인
- 코드만 수정하고 실제 Runtime 화면 미검증
- Evidence 누락

---

## 12. FINAL STATUS STRING

모든 검증과 Remote Readback까지 완료된 경우에만 다음 상태로 종료한다.

`PASS_MINDLE_MEDIA_AI_RESPONSIVE_PREVIEW_WORKSPACE_RUNTIME_VERIFIED`

Evidence 없는 PASS는 금지한다.
