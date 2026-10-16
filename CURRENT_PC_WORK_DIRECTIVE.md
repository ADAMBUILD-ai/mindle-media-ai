# MINDLE MEDIA AI — 저장 수정 후속 후보 인수
기준일: 2026-10-16
Epoch: MEDIA-AI-20261013-OWNER-RUNTIME-RECOVERY-R1
Phase: R9_CORRECTED_CANDIDATE_READY_FOR_PC_ACCEPTANCE

## 현재 후보 identity
- Source: c37c7819b1454996f3510f92184b1ef62faf3c78
- Producer: https://github.com/ADAMBUILD-ai/mindle-media-ai/actions/runs/38845082039
- 독립 readback: https://github.com/ADAMBUILD-ai/mindle-media-ai/actions/runs/38846038527
- ZIP: MINDLE_MEDIA_AI_ONE_CLICK_WIN_X64_v1.0.zip (1913893429 bytes, 5 parts)
- ZIP SHA256: 5291760966d87089259de4d1030879fdf0a1a878d7b9f1fd12f7918f36656b30
- Manifest SHA256: 7a31da30969b9e7901da8f109c467f281e2550171c15e9ddf3a8ddf215ab3377
- EXE SHA256: 24fe0ad565a5568b392b32040d7789cbd8abce7b60e8dade97666bbd1ec2888c
- Runtime: c37c7819b145-cfb26b181119
- UI fingerprint: cfb26b1811196c1abd19d5e59d33c420647ca122c060c753a7391ff43a8f8c2f

## 검증 범위
추가 저장 수정 4e20d02e601302cdebf56a131c1eb60cde0f19cb가 포함된 후보이다. 이전 fef692312ae8 후보는 역사 자료로 보존하며 parts/manifest를 섞지 않는다.
독립 ZIP CRC·19,236 manifest 파일 검증 PASS. Producer Windows 125 PASS/1 SKIP 및 기존 실제 EXE 검증은 사무실 PC 검증으로 확대하지 않는다.
추가 pending 참고 이미지/음성의 실제 EXE 저장·서버 종료·재실행·복원·UI Export 검증은 별도 실행 receipt로 판정한다.

## PC 잔여 순서
1. 실제 사무실 PC의 기존 도움 도구/접속으로 위 identity를 확인한 뒤 EXE 실행, Save 응답·project_id·PID·명령행을 기록한다.
2. 정상 종료 경로 우선. 확인한 제품 서버만 종료하고 PID 소멸과 endpoint 미응답을 모두 확인한다. EXE 재실행 후 새 PID·동일 프로젝트·사진/영상/자막/오디오/참조 복원·Export를 검수한다.
3. 설치된 Windows 플레이어의 이름·버전·재생 진행·탐색·영상·실제 소리 청취를 각각 기록한다. 브라우저 디코딩이나 생성 무음 WAV로 청취 PASS를 내지 않는다.
4. SHA f27eeb5031d83d7015494bc1683a981488ac4806627dc91c21f1c8c523df2541 승인 원본(1536×1024)과 같은 viewport/100% 배율에서 비교한다. R9 원본 TXT/CSV/PNG/ZIP의 크기·SHA·시각, 예외 전문·bootstrap/server log·lock 상태를 확보한다.

## 보존 및 제한
백업/입력8/버튼60 준비와 완료 PHOTO 분할·4× 모델 검수를 반복하지 않는다.
확정 UI 제목·배치·색상·VIDEO 구조·7보정·광고 숏폼을 임의 변경하지 않는다.
package_build_allowed=false. 승인된 1회 제작은 소진됐다. 추가 제작·직원 최종 패키지 재생성 금지.
PR23 HOLD / DO NOT MERGE. main 병합/force push 금지. OpenAI 연결 미승인. Marketing/AVORA DEFERRED_EXTERNAL.
사무실 PC/최종 전체 PASS=false. 미접속·미확보 자료는 BLOCKED이며 기능 FAIL로 추정하지 않는다.

Evidence Contract: docs/commander/MINDLE_MEDIA_AI_PC_R9_CORRECTED_CANDIDATE_EVIDENCE_CONTRACT_20261016.json

## 이번 원격 마감 결과
실제 후보 EXE pending 첨부 저장→서버 완전 종료→새 PID 재실행→복원→UI Export: PASS (38851276116 / artifact12025910982). 참고2+입력음성 해시일치, ZIP CRC·6개 파일 SHA 확인. 사무실 PC PASS는 아니다.
승인 F27E 원본과 1536×1024/DPR1/zoom1 실제 후보 비교: 상하/좌우 배치 및 전역 탐색 구조 불일치 FAIL. 임의 UI 수정 없음.
사무실 PC 실제 실행·플레이어 청취, R9 원본·예외 로그: 미확보 BLOCKED.
상세 결과: docs/evidence/media-ai-r9-followup-20261016/FOUR_ITEM_CLOSEOUT_KO.md
