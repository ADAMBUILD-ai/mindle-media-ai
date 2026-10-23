# 원격 Windows 실제 실행 통과 / 전달 최종화 진행

실행: https://github.com/ADAMBUILD-ai/mindle-media-ai/actions/runs/39985471598
소스: `2e5e9197d78c9b975686c1e419d2b68ce5f65226`.

새 EXE·실제 Chrome 자연어 → Qwen 추론 → Supertonic 한국어 신경망 음성 → MP4 재생 → 저장 → 정상 소유 서버 종료·endpoint 닫힘 → 새 PID → 동일 프로젝트/작업 이력/음성 복원 → 실제 UI Export가 통과했다. PID 4968 → 7412. 실행 후 19,333개 manifest 해시와 캐시 파일 0개를 확인했다. 사무실 PC·사람 청취·승인 UI 전체 일치·전체 제품 PASS는 아니다.

EXE SHA256 `701654240d8f2795957f78f7d1cc9d7fd23d3195f49a0d39ede1d8b8a3a915a5`.
Payload manifest SHA256 `2c6c3345539473e77cab56b10105448d0c23b651875dca45e8d49217b781dc07`.
Runtime `2e5e9197d78c-473763a9ef2d-ai-r2`.
한국어 음성: 131,846 bytes, mono 44,100Hz, 1.4943537415초, SHA256 `4134a7503b4c46878cbd0f090dbcd27042fce08f0fe56781bf81303d8baeeda3`.
재시작 후 API Export SHA256 `db053e2d59eb6ce7d62c20986133e4e496c4ef1a49f123e43e621e610ff76d15`. UI Export는 별도 BROWSER_REOPEN 원본에 기록됐다.

첫 전달 아티팩트는 여러 분할본을 하나로 묶어 512MiB 다운로드 도구 한도를 초과했다. 또 payload 밖 DELIVERY_ARTIFACT_SHA256.txt가 c37의 오래된 값을 유지했다. 새 EXE/manifest는 이미 검증됐으며 수정하지 않는다. 별도 독립 readback에서 원본 아카이브/모든 payload SHA/CRC를 재검증하고, 외부 체크섬 문서만 정확한 값으로 고친 뒤 ZIP SHA·분할본·설치기를 다시 고정한다. 새 제품 빌드나 모델 재추론이 아니다. 전달 ZIP SHA가 첫 원격 아카이브와 달라지는 이유와 수정 전 문서를 증거로 보존한다.

원격 원본 Evidence artifact: 12515578318, SHA256 433f119aabfc4a03dd0d8c95645620a5c9f09af416661ef4dce6a5e6091025d0. 이를 내려받아 CRC와 원본 SHA 일치를 확인했다. 전체 모델이 사무실 PC에서 검수됐다는 뜻이 아니다. PHOTO/SAM/업스케일의 고비용 재추론을 반복하지 않았다.
