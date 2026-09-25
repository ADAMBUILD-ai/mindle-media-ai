# MINDLE MEDIA AI · 광고 숏폼 쌍방향 연계 SSOT v1.1

Date: 2026-09-26
Status: LOCKED / APPROVED DIRECTION

## 1. 최상위 원칙
- 광고 숏폼 전용 독립 앱을 신규 개발하지 않는다.
- 현재 승인·고정된 MINDLE MEDIA AI UI/SSOT를 재설계하지 않는다.
- 기존 영상 편집 영역에 `일반 영상 편집 | 광고 숏폼` 모드만 증분 추가한다.
- 영상 제작 엔진은 MINDLE MEDIA AI 한 곳으로 통합한다.
- 7형제는 콘텐츠 공급자, Marketing AI는 광고 기획자, MEDIA AI는 영상 제작자다.
- SHORTFORM BRIDGE는 별도 사용자 앱이 아니라 양 시스템의 공통 제작지시 Schema/API 계층이다.

## 2. 쌍방향 진입 구조
### Route A — Marketing AI 시작
MINDLE ADA 7형제 → Marketing AI(자료 수집/선정, 전략, Hook, 시나리오, 자막, 내레이션, 음악 지시, CTA) → SHORTFORM BRIDGE → MEDIA AI → Preview/수정/저장/Export

### Route B — MEDIA AI 시작
사용자가 MEDIA AI 광고 숏폼 모드에서 자연어 지시 → MEDIA AI가 Marketing AI에 광고 기획+자료 패키지 요청 → Marketing AI가 7형제 자료 확보 및 전체 시나리오 구성 → SHORTFORM BRIDGE → MEDIA AI가 실제 영상 구현 → Preview/수정/저장/Export

원칙: 진입점은 2개지만 내부 제작 파이프라인과 영상 엔진은 하나다.

## 3. 역할 고정
- ADAM / AVORA / AURA / ARCOS / AXIOM / ADRAW / ASPEC: 광고 원천 Asset 제공
- Marketing AI: 타깃/목적 분석, Asset 선정, 광고 전략, Hook, 대본, Scene 구성, 자막, 내레이션, BGM 지시, CTA
- SHORTFORM BRIDGE: product, target, campaign_goal, duration, platform, scene timeline, asset reference, subtitle, voiceover, music directive, CTA, brand outro 등을 표준 Schema로 전달
- MINDLE MEDIA AI: 실제 컷 편집, 9:16 구성, 자막/음성/BGM/전환, Preview, 자연어 수정, Timeline 미세조정, 프로젝트 저장, MP4 Export

## 4. UI 증분 규칙
현재 확정 UI의 레이아웃/컬러/패널 구조/자연어 입력/Preview/Timeline/저장/내보내기를 유지한다.
영상 편집 영역에 모드 선택만 추가한다:
`일반 영상 편집 | 광고 숏폼`
광고 숏폼 선택 시 기존 편집 UI를 재사용하고 Marketing AI 호출 및 SHORTFORM BRIDGE 수신 기능만 활성화한다.

## 5. 1차 개발 — 현재 MEDIA AI 최종 UI 활성화와 함께
1. 기존 PHOTO / 4× / VIDEO / STT / Preview / Save / Export UI 연결 및 최종 E2E를 우선 PASS로 고정한다.
2. 영상 편집 영역에 `광고 숏폼` 모드 진입부를 증분 추가한다.
3. 기존 자연어 입력창을 그대로 사용한다.
4. Marketing AI 호출용 인터페이스 자리와 SHORTFORM BRIDGE 수신 Hook을 만든다.
5. 기존 기능과 UI 회귀가 없어야 한다.

## 6. 2차 개발 — 기존 MEDIA AI 기준선 PASS 후 증분
1. Marketing AI ↔ MEDIA AI 쌍방향 호출 완성
2. 7형제 광고 Asset Resolver 연결
3. SHORTFORM BRIDGE Scene/Timeline Schema 구현
4. 15/30/60초 자동 Timeline
5. 9:16 자동 Reframe / Pan / Zoom
6. 자동 자막 / AI 내레이션 / BGM / Transition / MINDLE ADA Brand Outro
7. Preview 후 자연어 재편집 및 Timeline 미세조정
8. Shorts / Reels / TikTok 등 플랫폼 Preset 및 MP4 Export

## 7. 금지사항
- 숏폼 전용 독립 앱 신규 개발 금지
- 7형제 각각에 영상 편집기 중복 구현 금지
- Marketing AI 광고기획 로직을 MEDIA AI 내부에 복제 금지
- 승인된 MEDIA AI UI 전면 재설계 금지
- 기존 MEDIA AI 최종 PASS 전 대규모 숏폼 기능 병합 금지

## 8. 최종 사용자 경험
예: MEDIA AI에서 `ADAM을 건축사 대상으로 15초 광고 숏폼 만들어.` 입력
→ MEDIA AI가 Marketing AI 호출
→ Marketing AI가 ADAM 관련 자료와 광고 시나리오/자막/내레이션/BGM 지시/CTA 구성
→ SHORTFORM BRIDGE 전달
→ MEDIA AI 자동 제작
→ Preview
→ 자연어 수정/Timeline 미세조정
→ 저장/MP4 Export

## 9. 최종 구조
MINDLE ADA 7형제 ↔ Marketing AI ↔ SHORTFORM BRIDGE ↔ MINDLE MEDIA AI

진입은 Marketing AI 또는 MEDIA AI 양쪽에서 가능하며, 광고 기획 책임은 Marketing AI, 영상 구현 책임은 MEDIA AI로 고정한다.
