# MINDLE MEDIA AI — R9 수정 후보 PC 인수 지시
기준일: 2026-10-16 KST
Epoch: MEDIA-AI-20261013-OWNER-RUNTIME-RECOVERY-R1
상태: R9_CORRECTED_CANDIDATE_READY_FOR_PC_ACCEPTANCE

## 정확한 후보
- Build source: fef692312ae8d8e3070c97e013dacdd31a043172
- Producer: https://github.com/ADAMBUILD-ai/mindle-media-ai/actions/runs/38822776656
- 독립 readback: https://github.com/ADAMBUILD-ai/mindle-media-ai/actions/runs/38824641294
- ZIP: MINDLE_MEDIA_AI_ONE_CLICK_WIN_X64_v1.0.zip
- 크기: 1913892012 bytes / part-00..04
- ZIP SHA256: 79b8fc38a5dade14a5974b132f265ba52476058f574b9d6c1795aa000aed7fe6
- Payload manifest SHA256: 3facd08b16aeae044af39755c2d0d9638af4fe3fa0fec317b2dbc0bd863f2c17
- Launcher SHA256: dd3f485a13a869acac87c3094381c9b97f872e461044af685e768afe9cadbe5a
- Runtime identity: fef692312ae8-1261762e58ca
- UI fingerprint: 1261762e58cacdc2fee1c7a01819b91551fe258c1abaffe6d0978b9e8490467e

이 후보는 개발 검수용이다. 기존 0e4e12a 후보와 파트를 혼합하지 않는다.
이전 후보와 R9 원본 증거를 덮어쓰지 않는다. 모델·가중치는 기존 검증 payload를 재사용했다.

## 완료 보존
백업/CRC·입력8·버튼60 준비, 사용자 보고 R9 재생/탐색/오디오 디코딩·사진7보정·브라우저 재열기·ZIP 결과를 반복하지 않는다.
PHOTO 분할/4× 알고리즘·가중치·완료 검수는 재작업하지 않는다.
이번 원격 Windows 검수는 116 pytest PASS/1 SKIP, Node5 PASS, 실제 EXE 첫/중복 실행, Chrome 재생/편집, 세로 PHOTO, 서버 완전 종료/새 PID/동일 프로젝트/Export PASS이다.
SKIP은 /usr/share/fonts 기반 한국어 폰트 테스트이며 Windows 플레이어/실제 청취 PASS를 뜻하지 않는다.
원격 runner와 실제 사용 PC의 판정은 분리한다.

## PC Work — 남은 항목만
1. 위 producer의 launcher-manifests 및 part00..04를 받아 순서대로 조립하고 ZIP SHA·CRC·source/manifest/runtime identity를 확인한다. 새 폴더에 압축을 푼다.
2. MINDLE_MEDIA_AI_RUN.exe를 더블클릭한다. 사용자 Python/pip/Git/모델 설치를 요구하지 않는다.
3. cloud 버튼이 외부 미연결 안내로 가고 로컬 storage와 분리됐는지 확인한다. 외부 cloud PASS로 처리하지 않는다.
4. 승인본을 확보한 경우 같은 viewport/zoom에서만 대조한다. 세로 PHOTO 원본/부모/image box·computed CSS·적용 파일 경로를 기록한다. 원본 비율·contain·center, 기존 색상/배치/VIDEO/7보정/광고 숏폼 버튼을 보존한다.
5. Save 응답/project_id, 대상 서버 PID/명령행/runtime identity를 기록한다. 정상 종료 경로가 있으면 우선 사용하고, 없으면 확인한 해당 제품 서버만 종료한다. PID 소멸과 endpoint 미응답을 둘 다 확인한다.
6. EXE 재실행 후 새 PID와 동일 프로젝트를 확인한다. 사진·영상·자막·오디오·참조의 실제 존재 항목별 복원을 확인하고 Export ZIP/MP4 해시·CRC를 기록한다. 원격의 사진/영상/보정3작업 복원을 전체 자료 복원으로 확대하지 않는다.
7. Export MP4를 설치된 Windows 플레이어에서 열어 플레이어 이름/버전·진행·탐색·영상·실제 청취를 각각 기록한다. 브라우저 디코딩으로 대체하지 않는다.
8. R9 원본 report/CSV/비교PNG/ZIP과 승인 화면, 잠금 예외 전문·bootstrap.log/server.log·launch.lock 상태를 확보할 수 있으면 실제 크기·SHA256·실행 시각과 함께 인계한다. 원본 확보 전 원인 일치를 단정하지 않는다.
9. 문제가 생기면 MediaError.code/readyState/videoWidth/currentSrc, HTTP/작업 상태를 먼저 기록한다. 300초 연장·lock 삭제·다른 Python/Chrome 일괄 종료로 우회하지 않는다.

## 고정 제한
package_build_allowed=false. 추가 자동 빌드와 직원 최종 패키지 재생성 금지.
PR23 HOLD / DO NOT MERGE, main 병합/force push 금지.
OpenAI 연결 미승인, Marketing/AVORA DEFERRED 유지.
owner_pc_runtime_pass=false, final_product_pass=false.
검수기 exit0은 증거 완전성만 의미한다. 전체 제품 최종 PASS를 발급하지 않는다.

## 제출
항목별 PASS/FAIL/BLOCKED/DEFERRED, 실제 파일 크기/해시/시각, 후보 identity와 R9 원본 출처를 연결한다.
Evidence Contract: docs/commander/MINDLE_MEDIA_AI_PC_R9_CORRECTED_CANDIDATE_EVIDENCE_CONTRACT_20261016.json

Active directive: docs/commander/MINDLE_MEDIA_AI_PC_R9_CORRECTED_CANDIDATE_ACCEPTANCE_20261016.md
