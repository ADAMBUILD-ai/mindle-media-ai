# 후속 Windows 개발 후보 제작 — 2026-10-24

대표 지시 `추가 후보 재작까지 진행한다.`에 따라 기존 전역 Build Gate=false를 보존하고, 별도 parent 고정 승인 계약으로 후속 개발 후보 한 건을 제작한다. 직원 최종 배포·PR23/main 병합 승인이 아니다.

기준 소스: 8b694818c3bd401194695e427ae410dc7c04cb72 + 이번 패키징/원격 인수 도구. 패키지 source identity는 실제 빌드 commit SHA로 기록한다.

- c37 아티팩트 5개는 2026-10-24 원격 목록에서 미만료를 확인했다. ZIP 52917609…는 조립 후 전체 SHA와 19,236개 기존 manifest 파일의 크기·SHA·CRC를 독립 확인한다.
- 기존 모델 가중치·알고리즘 재작업 없음. 현재 src/ui/launcher 전체를 덮어 넣되 새 출력 디렉터리에서만 작업한다.
- bootstrap EXE는 최신 -B 수정으로 새로 빌드한다. 과거 frozen EXE를 새 수정본으로 표시하지 않는다.
- Python 캐시를 새 payload에서 제외한다. 실행 뒤 배포 원본과 설치 runtime의 모든 manifest hash 및 cache 부재를 재검증한다. 검증 실패를 제외 규칙 완화나 현장 해시 재발행으로 무시하지 않는다.
- Qwen 1.5B, llama.cpp Windows b11716, Supertonic3, sherpa-onnx 1.13.8을 기존 고정 모델 identity로 포함한다. 외부 API 키 없음.
- 실제 원격 Windows EXE → Chrome 지시 → 실제 Qwen 계획 → 실제 신경망 TTS/MP4 → Save → 정상 shutdown/PID 종료/endpoint 닫힘 → 새 EXE/PID → Chrome Reopen/UI Export를 검증한다. 원격 결과는 사무실 PC·사람 청취·최종 승인 UI PASS가 아니다.
- 가로/세로 SSOT 디자인은 수정하지 않는다. 근거 없는 전체 PASS 문자열을 발행하지 않는다.
- 후보가 통과할 때만 ZIP 및 500MiB 분할본과 TEST R2 바로가기 설치기를 출력한다. 기존 TEST R1과 자료는 변경하지 않는다. 신규 데이터 폴더를 사용하며 기존 프로젝트를 자동 이전하지 않는다.

패키징 자체 회귀 5 PASS와 Python 구문 검사를 완료했다. 원격 실행 결과와 최종 SHA는 Actions 원본에 기록하며 실행 전 성공을 선언하지 않는다. PR #23 HOLD, main/force push 금지, Marketing/AVORA DEFERRED_EXTERNAL 유지.
