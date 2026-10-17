# R9 후속 작업 — General 실행 결과, 2026-10-16 KST

조회 source HEAD: 38bed49a46d46788f53f664a0f41c28b47466530. 원격 SSOT의 package_build_allowed=false 확인. 기존 후보 source/run/SHA 유지. R9 원본은 현재 원격 tree에서 찾지 못했으며 PC 상대경로의 bytes를 이 환경에서 읽었다고 주장하지 않는다.

## 실제 완료
- 원격 소스를 복구하고 cloud 경로 회귀3개 실행 PASS. cloud 미연결 안내/로컬 API 미호출, storage 기존 경로 및 라벨 분리 확인.
- PC 원본/로그 수집기 collect_pc_r9_diagnostics.py 추가. 선택한 R9 보고서·버튼CSV·화면PNG와 bootstrap/server 로그를 별도 새 폴더로 복사, 원본 전후 및 복사본 SHA 비교, 크기/lock 메타데이터/누락/변경 중인 로그 표시, ZIP CRC와 SHA 산출. 제품 파일·lock·프로세스 변경 없음.
- 수집기 경계 테스트3개 PASS: 원본 보존+CRC/hash, 파일 누락 보고, 원본 하위경로/기존 증거 덮어쓰기 거부. 합성 테스트는 실제 PC 증거가 아니다.
- 읽기 전용 DOM 측정식 pc_r9_geometry.js 추가 및 Node 문법 검사 PASS. host/image 실제 크기·원본 크기·object-fit/position/overflow/grid/transform/zoom·viewport/DPR·CSS URL 및 영상 필수 진단값을 반환한다.

## 진단 판단
PHOTO 현재 source에는 object-fit:contain이 있으나 grid의 intrinsic 크기, max-height 및 부모 overflow 등이 실제 계산에 영향을 줄 수 있다. 실제 bounding box와 승인 비교 원본 없이 정확한 원인을 확정하지 않는다. CSS 수정 없음.

런처는 msvcrt 1byte 잠금과 준비 대기를 사용한다. 오류 전문이 없어 잠금 경합인지, 잠금 파일 open 실패인지, 준비 단계 예외인지 아직 구분되지 않는다. lock 삭제/강제 해제/대기시간 증가나 동작 변경 없음.

## PC Work에서 즉시 실행
기존 검수용 Python으로 아래 명령을 한 줄 실행한다. 실제 기존 R9 폴더, 실제 제품 data root, 기존 증거 밖의 새 출력 폴더를 지정한다. 제품 payload 안에서 설치/수정하지 않는다.

```text
python scripts/collect_pc_r9_diagnostics.py --r9-root "실제_R9_폴더" --data-root "실제_제품_DATA_폴더" --output "별도_새_진단_폴더"
```

일반 기본 data root는 %LOCALAPPDATA%/MINDLE/MEDIA_AI_DATA이며 --data-root가 지정된 실행이면 실제값을 사용한다. 실행 중 로그 변경으로 unstable이면 종료 후 새 폴더에서 추가 캡처하고 양쪽 모두 보존한다. 수집기 exit0은 선택 파일의 안정적 복사만 의미한다.

R9 전체 ZIP은 원본 그대로 보존하고 별도로 Get-FileHash -Algorithm SHA256 및 실제 bytes를 기록한다. 수집 ZIP에는 전체 R9 ZIP이 중복 포함되지 않는다. 원본 전체 ZIP과 수집 DELIVERY.json을 함께 인계한다. 외부 인계 전 로그의 credential 포함 여부를 점검하며 원본은 보존한다.

이미 직접 제어 중인 제품 page에서 pc_r9_geometry.js 전체 표현식을 evaluate하고 반환 객체를 PHOTO_GEOMETRY.json으로 저장한다. 임의 새 viewport를 적용하기 전에 현재 값을 먼저 캡처한다. 승인 원본과 동일 viewport 비교는 별도 캡처로 보존한다. 이 측정은 스타일·모델·프로젝트 상태를 변경하지 않는다.

수집과 병행해 기존 지시서의 Windows 플레이어 검수 및 서버 완전 종료→EXE 재실행→같은 프로젝트 복원→Export를 진행한다. 이 General Linux 환경에는 Windows 플레이어/제품 서버/사무실 PC 접근이 없으며 해당 실행을 대신 완료했다고 표시하지 않는다.

## 현 판정
General cloud source regression: PASS. 수집기 회귀: PASS. 실제 R9 원본 독립 검증: 원본 인계 대기. PHOTO/승인UI/잠금 원인: 진단 대기. Windows 플레이어 및 cold restart: 미완료. R9 보고된 기존 PASS: USER_REPORTED로 보존.

새 패키지 빌드/모델 재추론/승인UI 변경/클라우드 연결 없음. PR23 HOLD / DO NOT MERGE, main/force push 금지. Marketing/AVORA DEFERRED, OpenAI 미승인 유지. owner_pc_runtime_pass=false, final_product_pass=false 유지.
