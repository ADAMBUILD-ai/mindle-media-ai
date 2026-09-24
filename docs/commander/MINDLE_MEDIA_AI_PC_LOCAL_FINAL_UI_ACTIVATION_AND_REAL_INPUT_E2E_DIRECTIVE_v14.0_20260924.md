# MINDLE MEDIA AI — PC LOCAL FINAL UI ACTIVATION & REAL INPUT E2E DIRECTIVE v14.0
Date: 2026-09-24
Status: EXECUTE
Branch: work/media-direct-acquisition-20260919

## 1. 목적
v13 FINAL CLOSEOUT 기준선과 승인 UI/SSOT를 훼손하지 않고, PC 로컬 환경에서 실제 기능 활성화 상태와 실사용 품질을 최종 검수한다. 새 기능 개발이나 UI 재디자인이 목적이 아니다.

## 2. 고정 기준선
- MINDLE_MEDIA_AI_FINAL_CLOSEOUT: PASS
- RELEASE_CANDIDATE_PASS: PASS
- COMMERCIAL_RELEASE_BLOCKED: NO
- UI_SSOT_CHANGED: NO
- v13 final commit baseline: ab121cced16f6ebe35271a434f9a78d4d8cbbb9c
- 기존 모델/License/Runtime/Product E2E Evidence는 immutable baseline으로 보존한다.
- 기존 승인 UI 디자인, 레이아웃, 색상, 2단 구조를 임의 변경하지 않는다.

## 3. UI/UX 최종 검수
실제 사용성만 검수하고 다음 3종으로 분류한다.
A. 반드시 추가/수정해야 하는 기능
B. 선택적 개선 기능
C. 불필요·중복되어 삭제 또는 숨김 가능한 기능

필수 확인:
- 처음 사용하는 사용자도 주요 작업 흐름을 이해할 수 있는가
- 자연어 입력과 참고 이미지 + 버튼 동선
- 실제 파일 업로드와 실행 상태 표시
- 원본/결과 Preview 및 비교
- Undo/Redo
- AI 1차 처리 후 사람 최종 리터치 흐름
- 프로젝트 저장
- 결과 내보내기
- 오류 발생 시 앱 종료 없이 복구 가능한가

시각 SSOT 변경이 필요한 경우 임의 변경 금지. COMMANDER_REVIEW_REQUIRED로 올린다.

## 4. PC 로컬 실제 E2E
실제 로컬 파일로 아래를 각각 검증한다.
1. PHOTO segmentation
2. VIDEO tracking
3. 4x upscale
4. Korean STT

각 기능 공통 검증 경로:
REAL INPUT -> UI ACTION -> BACKEND/ADAPTER -> REAL MODEL RUNTIME -> REAL OUTPUT -> PREVIEW -> PROJECT SAVE -> EXPORT

Mock, placeholder, synthetic-only 결과로 PASS 선언 금지.

## 5. 품질 검수
단순 실행 성공만 보지 않는다.
- segmentation 경계 품질
- video tracking의 프레임 간 객체 유지/안정성
- 4x upscale의 디테일, artifact, 과도한 sharpening 여부
- Korean STT의 실제 한국어 문장 정확도
- Preview와 export 결과의 동일성
- AI 1차 결과가 사람의 최종 리터치 시작점으로 실사용 가능한 수준인지 기록한다.

## 6. 실패 처리
한 번 실패했다고 종료하지 않는다.
Evidence -> 원인 -> 허용된 수정 -> 재실행 순으로 계속한다.
기존 PASS 기준선을 덮어쓰지 않는다.
실제 입력 또는 로컬 장치가 필요한 경우 BLOCKED_INPUT 또는 PC_MANUAL_GATE로 정확히 표시한다.

## 7. 보호 규칙
- UI_SSOT_CHANGED:NO 유지
- main merge 금지
- Production deploy 금지
- force push 금지
- 승인 없는 GPU/유료 compute 금지
- Secret/token 출력 금지
- 기존 Private HF immutable revision 및 Evidence 변경 금지

## 8. 완료 Evidence
반드시 생성/보존:
- UI_FINAL_REVIEW 결과
- 실제 입력 파일 identity/hash
- 기능별 실제 output identity/hash
- Preview 확인 결과
- 프로젝트 저장 결과
- Export 결과
- 로컬 Runtime/Adapter 정보
- PASS/REWORK/BLOCKED 판정
- 변경 파일 목록
- Commit SHA
- PR/Actions 상태

## 9. 완료 Gate
다음이 모두 확인될 때만 PC_LOCAL_FINAL_E2E_PASS:
- PHOTO segmentation PASS
- VIDEO tracking PASS
- 4x upscale PASS
- Korean STT PASS
- Preview PASS
- Project Save PASS
- Export PASS
- UI usability final review PASS
- UI_SSOT_CHANGED:NO
- 기존 v13 Closeout baseline 보존

## 10. 운영 규칙
검수 완료 즉시 기다리지 말고 다음 단계 지시서를 자동 작성하여 docs/commander/에 저장하고, Commit SHA와 함께 사령관에게 보고한다. Evidence 없는 PASS 금지.
