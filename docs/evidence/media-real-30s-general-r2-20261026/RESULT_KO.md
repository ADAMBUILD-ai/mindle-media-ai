# MEDIA General Work R2 — 실제 제작 인수 검수 결함 수정

작업 ID: MEDIA-REAL-30S-EXECUTION-R2-20261026  
기준 소스: 1aa25b2e1935e485a75542c218b8ad10d23696fe  
판정: GENERAL_ACCEPTANCE_GATE_FIX_VERIFIED / 실제 30초 제작 BLOCKED_ASSET_INTAKE

## 확인하고 수정한 결함

기존 source_e2e 검수에서 영상 스트림 1초·오디오 30초·컨테이너 30초인 실제 MP4가 PASS_TECHNICAL_ONLY로 통과했다. 전체 디코딩 성공만으로 스트림 길이 불일치를 발견할 수 없었다.

영상·오디오 각각의 유한한 start_time과 duration을 필수 검사한다. 각 시작 시각·길이·종료 시각을 30초 고정 인수의 0.15초 허용 오차로 검사하고, 두 종료 시각의 차이도 검사한다. 타이밍 누락·NaN·무한대·늦은 시작·한쪽만 짧은 출력은 차단한다. PASS 반환에 두 스트림의 실제 타임라인을 남긴다. 이 검사는 지각적 립싱크나 음성 자연스러움 검사를 대체하지 않는다.

기존 콜드 재시작 뒤 Reopen 검사는 출력 SHA 위주여서 저장된 원고·음량·workspace 등의 변경을 놓칠 수 있었다. 저장 당시와 재열기 프로젝트 전체를 비교하고 HTTP 전송용 URL 세 필드만 제외한다. 원본 입력·출력·참조 파일의 SHA와 bytes를 모두 재검사한다. Export의 기존 내부 SHA 검사는 유지한다.

## 실제 실행한 검증

- Linux General 환경에서 집중 pytest 실제 시작·종료, exit 0: **57 PASS / 0 SKIP**.
- source_e2e: 29개. 실제 FFmpeg 스트림 길이 오류 주입과 정상 30초 계약, 실제 제품 child PID 종료·재시작·Reopen·Export 포함.
- 상태 권위 및 접수 회귀: 나머지 28개. 추가 미검증 변경은 계속 차단.
- Python 4개 파일 구문 검사와 git diff --check: PASS.
- 모델 실행·실제 작품 제작·사람의 시청 및 청취: NOT_EXECUTED.
- 사용한 색상·무음 파일은 결함 주입용이며 실무 입력으로 등록하거나 인수하지 않았다.

## 소스 권위와 변경 제한

기존 foundation 및 R2 SOURCE_VALIDATION 원문은 고치지 않았다. 상태 검사기는 기존 59개 경로 중 source_e2e.py의 검토한 변경 해시 한 개만 명시적으로 덧붙인다. 기존 해시를 base_sha256으로 대조하고 추가 변조 차단 회귀를 통과했다. 다른 runtime과 UI의 기대 해시·확정 UI fingerprint는 유지한다.

CURRENT_*의 변경은 새 상태 스냅샷 결속뿐이다. R3 epoch·소비한 승인·Build Gate·최종 인수값은 변경하지 않는다. 이는 새 모델 추론이나 Windows 인수가 아니다.

기존 446 PASS / 5 SKIP은 해당 원래 소스의 결과로 보존한다. 이번 수정 경로에는 새 57개 집중 회귀를 적용하며, 예전 전체 PASS를 최신 전체 PASS로 표시하지 않는다. CI 일괄 재실행·새 workflow·접수 ZIP 재생성·EXE 제작·설치 모델 교체는 하지 않았다.

## 다음 실행

PC Work는 기존 OPERATOR_INPUT.json에 실제 영상·사용 구간·권리·BGM·확정 원고·세 음량·장문 정책을 채우고 입력이 달라진 뒤에만 기존 도구로 새 RETURN_03을 생성한다. 그 파일과 원본 접근 위치는 아직 General에 도착하지 않았다. 경로 문자열만으로 Linux General에서 Windows 원본에 접근할 수 없다.

실제 입력 수신 후 최신 정확한 checkout SHA·Manifest SHA·실제 엔진 identity를 새로 결속한다. 이전 General 보고서의 3710194 소스 동결은 역사적 기록이다. 이번 수정 소스를 사용하는 실행에 그 SHA를 혼용하지 않는다. Windows 7B 승인·실행기 확보는 실제 입력 접수와 별도 조건이다.

Build Gate=false, PR #23 Draft/HOLD, main 미병합·미배포 유지.
