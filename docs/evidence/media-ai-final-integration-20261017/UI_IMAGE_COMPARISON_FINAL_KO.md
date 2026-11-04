# 최신 승인 이미지와 실제 Source Chrome 비교

최종 시각 판정: **FAIL_APPROVED_IMAGE_MATCH**. 이는 source 기능·전환 회귀 PASS와 별개다. RESULT_KO.md의 전체 UI PARTIAL을 이 직접 비교 결과로 구체화한다. 실제 후속 후보 EXE의 시각 인수는 여전히 미실행 BLOCKED다.

비교 기준은 사용자가 마지막으로 제공한 `마인들 미디어 AI 통합 편집 대시보드.png` 원본이다. 과거 F27E 상하 배치 이미지를 기준으로 삼지 않았다. 두 이미지1536×1024, 실제 Chrome zoom1/DPR1. 기준 이미지는 raster 원본이라 브라우저 zoom 값 자체가 없으며 1:1 pixels로 비교했다. COMPARE.html은 원본 두 장을 나란히 표시하는 정적 비교 문서다. 이미지 원본은 편집하지 않았다.

실제 화면은 AFTER_R1/BASELINE.png이며 밀집 목록을 위한 DOM fixture를 추가하기 전이다. Windows의 공식 Chrome155.0.8059.80와 실제 source 서버에서 촬영했다. 새 Windows 패키지 실행 화면으로 표시하지 않는다. 검사 파일 SHA는 c1956f4 소스와 일치한다.

|항목|판정|확인 내용|
|---|---|---|
|제목·좌우 영역·색상 계열|PASS 범위 제한|MINDLE MEDIA AI, VIDEO좌/PHOTO우, Navy·Cyan/Purple 유지|
|PHOTO 가로 preview·세로 Auto Fit|PASS 동작 범위|가로 stage, 원본480×960 contain/center. 승인본의 대형 preview 너비·면적까지 같다는 뜻은 아님|
|PHOTO 보정 도구 위치|FAIL|승인본은 가로 Preview 아래7보정/세부 기능, source는 우측 세로 도구 패널|
|PHOTO 참고 Strip|FAIL|승인본의 Preview 아래 가로 이미지 Strip과 source의 좌측 참조/하단 첨부 목록 구조가 다름|
|상단/패널 Header|FAIL|승인본의 큰 카메라 배너·아이콘·탭 비율과 source의 간략 header/작은 버튼 배치가 다름|
|Timeline 시각 구조|FAIL|승인본은 thumbnail/waveform/clip 표현, source는 읽기 전용 status track 행. 기존 기능을 시각 Timeline 완료로 승격하지 않음|
|AI 입력 존재|PASS 존재 범위|양쪽 실제 입력이 있으나 승인본과 크기·강조·간격은 동일하지 않음|
|전체 비율·크기·강조|FAIL|패널·사진 preview 면적·도구 버튼·참고영역 비율과 표현이 다름|

제품 기능이 동작하거나 source 회귀가 통과했어도 위 시각 구조는 PASS가 아니다. 이번 작업에서 승인 HTML/CSS를 임의 수정하거나 옛 상하 UI로 되돌리지 않았다. 새 레이아웃을 창작하지 않았다.

다음 수행 주체: GENERAL/Owner UI 기준 담당. 이 최신 승인 원본과 source 차이를 인수 결함으로 취급하고, 승인 구조 복원 범위에서 기존 버튼 연결·엔진·가중치를 보존해야 한다. 단순 source 회귀 통과만으로 시각 승인이나 Windows 최종 PASS를 발급하면 안 된다. Build Gate=false는 그대로이며 이후 후보 제작은 별도 유효 승인 후 가능하다.
