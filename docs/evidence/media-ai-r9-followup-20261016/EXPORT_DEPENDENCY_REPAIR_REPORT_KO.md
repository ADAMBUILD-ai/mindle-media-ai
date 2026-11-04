# 후속 마감: 프로젝트 Export 의존 파일 보존

기준일 2026-10-16 KST. 이전 PHOTO/런처 수정 및 증거는 보존했다. 해당 완료 검사를 반복하지 않고 Export의 입력·참조 의존 파일을 검사했다.

수정 source: 4f1d9e818811d5622722ceec4fd4404b32a9c2e1
검증 source: a4f093acf80c5e675d191fce7be9a8c95228547e
CI: https://github.com/ADAMBUILD-ai/mindle-media-ai/actions/runs/38791557820 — SUCCESS
실제 source HTTP Export ZIP/receipt: https://github.com/ADAMBUILD-ai/mindle-media-ai/actions/runs/38791557820/artifacts/12000626976

## 재현과 수정
기존 Export는 outputs 목록만 압축했다. 입력 원본은 누락됐고, reference_artifacts만으로 기록된 참조 역시 누락됐다. 실제 엔진은 일부 참조를 outputs에도 기록하므로 모든 참조가 항상 누락되는 것은 아니다. 그러나 명시적 역할 매핑이 없고 입력/별도 참조가 변조돼도 검출하지 못했다. 생성한 사진 보정 및 참조 fixture로 신규 회귀3개가 실패하는 것을 먼저 확인했다.

이제 결과 파일의 기존 jobs/... 경로를 보존하면서 기록된 입력은 inputs/..., 참조는 references/...에 포함한다. project.json 원본은 변경하지 않는다. BUNDLE_MANIFEST.json에 job_id/역할/압축 내부 경로/크기/SHA256을 기록한다. 중복 내부 경로는 거부하고, 포함 파일 전체의 사전 무결성과 ZIP 내부 실제 bytes를 검증한 후에만 이전 정상 Export를 원자적으로 교체한다. 쓰기 중 원본이 바뀐 경우도 실패 처리한다.

이는 기록된 작업 입력과 참조의 보존 개선이며, 새 ZIP import 기능이나 다른 PC에서 프로젝트 자동 복원을 구현했다는 뜻은 아니다. 기존 작업 receipt에 기록되지 않은 upstream 원본까지 복구한 것으로 확대하지 않는다. 모델 추론이나 가중치 변경 없음.

## 실제 검증
- 신규 의존 파일 검사4 PASS: 서비스 재시작 후 입력/참조 포함, 입력 변조 거부, 참조 변조 거부, ZIP 작성 중 참조 변경 거부.
- 기존 atomic Export·사진 저장/재열기·영상 편집 회귀를 포함해 총13 PASS. 로컬 및 원격에서 통과.
- 실제 Linux source HTTP 서버 PID3797 종료/기존 endpoint 미응답→PID3852 신규 기동→동일 project_id와 사진/영상 결과 복원→Export 다운로드 PASS. 입력2개/결과2개의 bundle 매핑 검증.
- 원격 artifact ZIP을 별도로 내려받아 내부 SOURCE_HTTP_EXPORT.zip을 독립 검증: 전체 CRC 및 매핑된4파일의 크기/SHA256 일치. Export SHA256 4462e5c64c27a02497c7b4b499d3dc93c759cd9bc4256f96b29271543fa4a35a.
- 엔진의 일부 참조가 outputs와 reference_artifacts 양쪽에 기록되는 경우도 생성 fixture로 추가 검증했다. 역할별 내부 경로가 충돌하지 않고4파일의 해시가 일치했다.

생성 fixture 및 source 경로 테스트이며 실제 AI 추론·사무실 PC 검수를 의미하지 않는다.

## R9 인계와 남은 항목
R9 원본 보고·승인비교PNG·전체 ZIP은 이번 보관 파일 검색에서도 확보하지 못했다. 이는 파일이 존재하지 않는다는 증거가 아니다. 원본 bytes 독립 검증은 아직 미완료다. 승인 UI 전체 비교, R9 잠금 예외의 인과 대조, 사무실 EXE cold restart 및 Windows 플레이어 검수도 남아 있다.

후속 Windows 개발 검수 후보에는 cloud 분리, PHOTO 크기 수정, 런처 정리, atomic Export 및 이번 의존 파일 보존 수정을 함께 포함해야 한다. 기존 후보는 수정하지 않았다. package_build_allowed=false, owner_pc_runtime_pass=false, final_product_pass=false 유지. PR23 HOLD / DO NOT MERGE, main/force push 금지. UI/PHOTO adapter/가중치 수정 및 고비용 모델 검수 반복 없음. OpenAI/Marketing/AVORA 기존 Gate 유지.
