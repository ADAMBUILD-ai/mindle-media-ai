# MINDLE MEDIA AI 광고 숏폼 P0 연동 구현 검수자료

Date: 2026-09-26
SSOT: MINDLE MEDIA AI · 광고 숏폼 쌍방향 연계 SSOT v1.1
Base: work/v28-1-remote-runtime-package-20260924

## 구현 범위
- 기존 VIDEO 헤더에 광고 숏폼 모드 진입 버튼 증분 추가
- 기존 자연어 입력창 재사용
- MEDIA AI → Marketing AI 요청 Hook
- Marketing AI → SHORTFORM BRIDGE Contract v1 Reader
- Scene/Timeline, 9:16, 승인 Asset 참조 검증
- 대표 승인 전 Export fail-closed
- 기존 일반 영상/사진 편집 경로 유지

## 경계
- 독립 앱 신규 개발 없음
- Marketing AI 기획 로직 복제 없음
- 승인된 MEDIA AI 레이아웃 재설계 없음
- 자동 게시/광고비 집행 없음

## 검증 상태
- Contract Reader 단위테스트: PASS (5/5)
- UI 기존 assertion harness + Shortform mode: PASS
- 전체 Python 회귀: VERIFY_REQUIRED (전체 저장소 실행환경 미구성)
- 실제 Marketing AI HTTP 연결: VERIFY_REQUIRED
- 실제 AVORA Asset/Preview/MP4: VERIFY_REQUIRED


## 실행 증거
- `PYTHONPATH=src python -m pytest -q tests/test_shortform_bridge.py` → 5 passed
- `node ui/interaction.test.js` → exit 0
- 기존 UI 테스트 파일 전체 보존 후 Shortform assertion만 증분 추가
