# TEST R2 실제 사무실 PC 인수 — 2026-10-24

Epoch: MEDIA-AI-20261013-OWNER-RUNTIME-RECOVERY-R1.
기존 R9/c37은 과거 증거다. 이번 인수는 아래 고정 후보만 사용한다. 이후 전달용 metadata commit의 HEAD를 제품 source로 혼동하지 않는다.

- 제품 source: 2e5e9197d78c9b975686c1e419d2b68ce5f65226
- Producer: 39985471598 (실제 Windows EXE/Chrome/Qwen/TTS/정상 종료/새 PID/Reopen/UI Export PASS)
- Independent readback: 39987617196 (모든 19,333 payload 파일 SHA 및 최종 ZIP CRC PASS)
- Runtime: 2e5e9197d78c-473763a9ef2d-ai-r2
- 최종 ZIP SHA256: c3cfda25e2f36f97024a57b586a20914be3b21a2b481f25e1652c8931ece3606
- EXE SHA256: 701654240d8f2795957f78f7d1cc9d7fd23d3195f49a0d39ede1d8b8a3a915a5
- Payload manifest SHA256: 2c6c3345539473e77cab56b10105448d0c23b651875dca45e8d49217b781dc07
- 계약: docs/commander/MINDLE_MEDIA_AI_PC_TEST_R2_EVIDENCE_CONTRACT_20261024.json

설치기 MINDLE_MEDIA_AI_START_20261024_R1.zip과 동일 날짜의 part-00~06을 같은 폴더에 두고, 설치기만 압축 해제해 START_MINDLE_MEDIA_AI.cmd를 실행한다. 바탕화면의 새 MINDLE MEDIA AI TEST R2를 사용한다. 기존 TEST R1, 설치 폴더, 모델 및 사용자 자료는 삭제/덮어쓰기하지 않는다. 새 작업 데이터는 LOCALAPPDATA/MINDLE/MEDIA_AI_CANDIDATE_20261024_R1이다. 기존 프로젝트를 자동 이전하지 않는다.

PC Work가 접근 가능한 실제 PC에서 직접 수집·실행한다. 대표에게 과거 파일 위치나 로그 수집 책임을 넘기지 않는다. 물리 PC에 접근하지 못하면 해당 항목만 미실행으로 남기고 원격 증거로 바꾸지 않는다.

1. 후보 4종 해시를 대조한다. 기존 사용자 자료를 보존하고 새 후보 전용 프로젝트를 사용한다.
2. 새 EXE를 실행하고 identity·정확한 소유 PID·명령행·server.log를 기록한다. 무응답 때는 관련 후보 경로만 조사하며 다른 Python/Chrome 일괄 종료나 lock 삭제를 하지 않는다.
3. 실제 영상에서 `밝기를 3 높이고 "반갑습니다" 나레이션을 넣고 영상을 연장해 주세요.`를 입력한다. Qwen 모델 identity/원문 응답/계획과 Supertonic WAV/MP4 해시, 브라우저 MediaError.code·readyState·videoWidth·currentSrc를 기록한다. 실제 한국어 청취는 별도다.
4. 사진·영상·자막·나레이션·참고 이미지·입력 음성을 포함해 Save 응답/project_id를 확보한다. 고비용 PHOTO 분할/4×는 이유 없이 재추론하지 않는다. 이번 원격 실제 모델 검수는 Qwen/TTS이며 모든 PHOTO/STT 실증으로 확대하지 않는다.
5. `/api/runtime/control`의 소유 PID/instance/nonce를 대조한 정상 종료를 우선한다. 프로세스 종료와 endpoint 닫힘을 모두 확인한다. 새 EXE → 새 PID/instance → 같은 프로젝트/참고/자막/음성 복원 → UI Export를 원본 증거로 남긴다.
6. Export MP4를 설치 플레이어에서 직접 열고 이름/버전, 영상 표시·시간 진행·앞뒤 탐색·사람의 실제 소리 청취를 각각 기록한다.
7. 1536×1024·100%에서 승인 UI 원본과 대조한다. VIDEO 좌측/PHOTO 우측·헤더·타임라인·자연어 2곳·세로 PHOTO contain/중앙·7보정·숏폼 버튼·하단 비율을 확인한다. 설계를 바꾸거나 전체 일치로 추정하지 않는다.
8. 실패는 항목별 FAIL/BLOCKED로 기록하고 독립 항목을 계속한다. 출력 ZIP CRC뿐 아니라 MP4 stream/hash를 확인한다. 결과·원본 로그·해시·화면을 저장소 Evidence로 반환한다.

Build Gate=false 유지. 이번 후속 개발 후보 제작은 끝났으며 임의 직원 최종 패키지 재생성은 금지다. PR23 HOLD/DO NOT MERGE, main/force push 금지, 외부 키 미연결, Marketing/승인 AVORA DEFERRED_EXTERNAL. 사무실 PC·실제 청취·승인 UI·전체 제품 최종 PASS는 아직 발행하지 않는다.
