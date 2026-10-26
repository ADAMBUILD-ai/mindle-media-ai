# 신규 장면 생성 어댑터 사전 조사 결과

기준일: 2026-10-26 KST. 판정: 공식 외부 제어 경로 확인 / MEDIA 통합·실제 생성 미실행.

LTX Desktop v1.3.1의 인증 Remote API에서 이미지 입력, 생성 등록·조회·취소, 결과 회수 경로를 확인했다. Remote 이미지 업로드로 Blender Depth/Canny 영상도 전달할 수 있다는 가정은 채택하지 않았다. 현재 MEDIA 생산 엔진 목록에는 LTX가 없고, Wan은 비활성 ComfyUI 기반 자산 경로다.

반환: [연결 규격](../../commander/GENERATION_ADAPTER_R1_KO.md), [소스 구조 검사](STATIC_AUDIT.json), [범위·고정 revision](SOURCE_VALIDATION.json).

Python AST로 공식 생성/asset route를 추출하고 필수 경로 5개, Wan CLI 옵션 6개, MEDIA LTX 엔진 부재를 확인했다. 이는 정적 조사이며 네트워크 API 실행·추론·품질 시험이 아니다. 가중치·라이선스·GPU 채택은 확정하지 않았다.

제품 코드·UI·설치본·기존 registry는 변경하지 않았다. 기존 원격 402 PASS/5 SKIP·브라우저 41 PASS는 해당 소스의 과거 증거로 유지하며 이번 조사를 새 추론 증거로 올리지 않는다. 불필요한 Actions 재실행은 하지 않았다.

실제 자료 30초 제작은 기존 단일 접수표의 영상·권리·BGM·원고·음량·장문 정책 접수가 필요하다. 신규 생성 실증은 승인된 설치/모델/입력에서 짧은 건축 장면 1개부터 시작하고 형태·카메라·실패 복구를 검증한 뒤 MEDIA 편집·재열기·Export로 이어간다.

Build Gate=false / PR #23 Draft/HOLD / 미병합 유지. 모델 다운로드·설치·유료 API·자료 업로드·새 EXE 제작 없음.
