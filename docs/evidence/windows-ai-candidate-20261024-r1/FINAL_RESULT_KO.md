# TEST R2 후속 후보 제작·원격 Windows 실검증·전달 완료

**판정: 후속 개발 후보 제작/원격 검증 PASS. 실제 사무실 PC 최종 인수는 미완료.**
기준일: 2026-10-24 KST. PR #23 HOLD / DO NOT MERGE, main/force push 금지, 직원 최종 배포 금지 유지.

## 전달 후보

- 제품 source: `2e5e9197d78c9b975686c1e419d2b68ce5f65226`
- EXE: `701654240d8f2795957f78f7d1cc9d7fd23d3195f49a0d39ede1d8b8a3a915a5`
- Payload manifest: `2c6c3345539473e77cab56b10105448d0c23b651875dca45e8d49217b781dc07`
- Runtime ID: `2e5e9197d78c-473763a9ef2d-ai-r2`
- 최종 ZIP: `MINDLE_MEDIA_AI_PC_TEST_20261024_R1.zip`, **3,166,947,613 bytes**
- 최종 ZIP SHA256: `c3cfda25e2f36f97024a57b586a20914be3b21a2b481f25e1652c8931ece3606`
- 설치기 SHA256: `747ddd1eb7aa1cef93f235af2128d9aeef68399e15c362a30260d36b1a4e9b44`
- 설치기 1개·500MiB 이하 분할본 7개·원본 검수 ZIP 1개, 총 9개 파일 저장 완료. 모든 파일 저장/로컬 identity 반영 성공. 파일별 크기·해시는 FINAL_DELIVERY.json에 고정했다.

## 실제 수행 결과

| 항목 | 판정·증거 |
|---|---|
| 기존 입력 재사용 | c37 전체 ZIP SHA와 19,236 manifest 파일 크기/SHA/CRC 확인. PHOTO 분할/4× 가중치·알고리즘 재작업/고비용 재추론 없음 |
| 새 EXE | 캐시 쓰기 방지 -B를 포함한 최신 bootstrap으로 새 빌드. c37 frozen EXE 재사용 아님 |
| 실제 Chrome 자연어 | 제품 입력창에서 복합 명령 → 실제 Qwen 모델 추론 → 계획 → 순차 작업 PASS. ACTUAL_GENERATIVE_PLAN.json |
| 한국어 신경망 TTS | Supertonic3/sherpa-onnx 1.13.8의 실제 ONNX 생성. 44,100Hz mono, 1.494초 WAV. 파형/디코딩을 사람 청취로 처리하지 않음 |
| 저장·완전 재시작·복원 | 소유 서버 정상 종료, PID 4968 종료와 endpoint 닫힘, 새 EXE/PID 7412 → 같은 프로젝트·작업 이력·나레이션 복원 PASS |
| 재시작 후 UI Export | 실제 Chrome에서 내보내기 다운로드 PASS. 원본 ZIP SHA `f29db14aa2ea97ddd6faa2ca1855f106886a18b2e9f68753afe5a22814967d05` |
| Export/MP4 독립 확인 | API·UI ZIP 각각 11개 manifest 항목 SHA/크기·CRC PASS. 생성 MP4 H.264/yuv420p + AAC, 4.000/4.006초, faststart, FFmpeg 전체 디코딩 exit 0 |
| 실행 뒤 무결성 | 설치 runtime 및 배포 payload 19,333 파일 해시 PASS, 생성된 .pyc 0개. 검증을 끄거나 lock을 지우지 않았음 |
| 독립 전달 검증 | 별도 작업에서 전체 payload와 EXE/manifest SHA·ZIP CRC 재확인. 전달용 외부 체크섬 문서만 정정, 제품 payload 변경 없음 |
| 다운로드 회수 | 500MiB 아티팩트 도구 timeout을 64MiB 중간 전송으로 해결. 48개 중간 조각 모두 SHA 검증 후 원래 7개 분할본 복원, 전체 SHA c3cf… 일치. 모델 재추론·재빌드 없음 |
| 회귀/Control Plane | 이번 패키징 5 PASS, 기존 소스 회귀 167 PASS/6 SKIP·Node23 PASS 보존. 현재 Control Plane 정상 검증 및 변조 ZIP SHA 거절 PASS. 검수기 PASS는 사무실 PC 인수 PASS가 아님 |

원본 실행: https://github.com/ADAMBUILD-ai/mindle-media-ai/actions/runs/39985471598
독립 readback: https://github.com/ADAMBUILD-ai/mindle-media-ai/actions/runs/39987617196
동일 바이트 중간 전송: https://github.com/ADAMBUILD-ai/mindle-media-ai/actions/runs/39989419656

첫 원격 ZIP SHA b8f162…와 최종 c3cf…가 다른 이유는 payload 밖 DELIVERY_ARTIFACT_SHA256.txt가 과거 c37 값을 유지했기 때문이다. 해당 문서만 정정하고 수정 전 파일을 보존했다. EXE·payload manifest·제품/모델 모든 파일은 원격 Windows 인수본과 동일하다. 최종 ZIP의 전체 payload SHA와 CRC도 다시 통과했다.

## 사용 및 PC Work 인계

설치기와 part-00~06을 같은 폴더에 두고 설치기 ZIP만 풀어 START_MINDLE_MEDIA_AI.cmd를 실행한다. 새 바탕화면 바로가기 **MINDLE MEDIA AI TEST R2**를 사용한다. 기존 TEST R1·사용자 자료·모델은 보존된다. 새 데이터 폴더는 LOCALAPPDATA/MINDLE/MEDIA_AI_CANDIDATE_20261024_R1이며 기존 프로젝트를 자동 이전하지 않는다.

현재 SSOT는 TEST R2를 가리키도록 정합화했다. 과거 c37 identity는 historical_r9_20261016_candidate에 보존했다. 현재 지시서는 docs/commander/MINDLE_MEDIA_AI_PC_TEST_R2_ACCEPTANCE_20261024.md, 계약은 같은 날짜의 TEST_R2_EVIDENCE_CONTRACT다. 전역 Build Gate=false이며 이번 승인 건은 소비됐다.

## 남은 항목 — 완료로 확대하지 않음

1. 실제 사무실 PC에서 동일 후보 EXE·정상 종료·새 PID·사진/영상/자막/나레이션/참고/입력 음성 복원·Export. 이번 원격 새 시나리오는 영상·나레이션/작업 이력이며 사진/참고2/입력 음성 전체를 새로 실증한 것으로 주장하지 않는다.
2. 설치된 Windows 플레이어 재생·탐색과 사람의 실제 소리 청취·한국어 자연스러움.
3. 승인 원본과 1536×1024·100% 최종 UI 전체 대조. 배치·색상 재설계 없음. 현재 전체 픽셀 일치 승인 미발행.
4. R9 사무실 PC 원본 TXT/CSV/PNG/ZIP·lock 예외 전문과 당시 writer/PID 조사. 원격 후보 검증을 과거 물리 PC 원인 확정으로 바꾸지 않는다.
5. Marketing HTTP·승인 AVORA DEFERRED_EXTERNAL 유지. 텍스트로 새 이미지/영상을 생성하는 모델은 이번 후보 범위가 아니다.

**전체 제품 최종 PASS 문자열을 발급하지 않았다. 대표에게 과거 로그 위치를 찾아 제출하도록 요구하지 않는다. PC Work가 접근 가능한 실제 환경에서 위 고정 후보·계약으로 남은 인수를 수행한다.**
