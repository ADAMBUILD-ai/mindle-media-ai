# Windows 더블클릭 개발 검증 후보 인계 — 2026-10-18

**조립·파일 무결성 PASS. 실제 새 Windows 후보 실행·승인 UI 일치·사람 청취는 미완료.**

사용자의 이번 대화에서 노트북/데스크톱용 더블클릭 실행 파일을 만들어 보내 달라는 명시 요청을 이 개발 후보 1회 제작·전달 승인으로 적용했다. 추가 빌드·직원 최종 배포·main/PR23 병합 승인은 아니다. 한 후보 제작 승인은 소진했고 Gate=false를 유지한다.

- 소스: `e00e6e0b82994fca628d6ca3cf039f7dc43c15c6`.
- 기존 c37 원본 ZIP SHA256 `5291760966d87089259de4d1030879fdf0a1a878d7b9f1fd12f7918f36656b30`, 원본 19,236개 파일·EXE 해시 독립 확인. 기존의 검증된 EXE bootstrap 바이트를 그대로 재사용했으며 새 EXE를 여기서 컴파일했다고 주장하지 않는다.
- 최신 canonical src/ui 72개 Git blob 대조·반영. 새 payload 20,440개 파일의 ZIP 내부 크기·SHA256·CRC와 엔진 트리 pin을 모두 검증.
- Windows용 llama.cpp b11716 공식 ZIP SHA256 `79b143075ab87fb5aff6f8f8ca80500a984f4120b5199fa9f9b70b284f17428e` 확인, Qwen 1.5B GGUF, Supertonic 3 ONNX, Windows CPython 3.11 ABI의 sherpa-onnx/core 1.13.8 wheel을 포함. Linux 바이너리를 Windows 엔진으로 포장하지 않았다.
- 한글 모델 stdout UTF-8 강제, 운영체제에 관계없이 같은 파일명 순서로 계산하는 엔진 해시, 별도 후보 데이터 프로필을 수정했다. 회귀 **127 PASS / native Windows 2 SKIP**. 과거 Linux 실제 생성형·신경망 TTS·브라우저·재시작 증거와 이 후보의 Windows 실행 증거를 구분한다.
- PHOTO 분할·4× 알고리즘 및 정식 가중치는 변경·재추론하지 않았다. 승인 UI 재설계 없음. UI 최종 일치 FAIL은 유지한다.

## 전달물

완성 ZIP: `MINDLE_MEDIA_AI_PC_TEST_20261018_R1.zip`, **3,177,192,286 bytes**, SHA256 `715c351a3733aea2ffd87fa0113cc6e554920faabe430c74f941b7b6e5feac8c`.

전달 서비스가 파일당 536,870,912 bytes를 제한해, 500MiB 이하 분할 7개와 작은 `MINDLE_MEDIA_AI_START_20261018_R1.zip`을 저장·전달했다. 분할을 재독립 읽기해 합친 SHA256이 위 완성 ZIP과 정확히 같음을 확인했다. `SPLIT_DELIVERY.json`, `INSTALLER.json` 참조.

분할 7개를 같은 폴더에 받는다. 작은 설치 ZIP을 그 폴더 또는 바로 아래 폴더에 풀고 `START_MINDLE_MEDIA_AI.cmd`를 더블클릭한다. 합치기→전체 ZIP SHA 검증→Windows tar 압축 해제→제품 EXE 실행→바탕화면 `MINDLE MEDIA AI TEST R1` 바로가기 생성 순서다. 별도 Python/pip/Git 명령 입력이 없다. 설치 명령은 보안 정책을 변경하거나 관리자 권한을 우회하지 않는다. 바로가기 실패가 제품 실행을 막지 않도록 분리했다.

이번 후보 설치 경로는 LOCALAPPDATA/MINDLE/PC_TEST_INSTALLS/20261018_R1, 작업 자료는 LOCALAPPDATA/MINDLE/MEDIA_AI_CANDIDATE_20261018_R1이다. 기존 c37 설치/자료를 덮어쓰거나 자동 이관하지 않는다. 저장 공간 35GB 이상 권장.

## 조립 중 확인·수정

대용량 파일의 host copy/rsync 임시 파일이 순회 목록에 혼입돼 첫 조립 검증을 중단했다. 부분 파일을 정식 모델로 게시하지 않았다. 최종 export에서 숨김 copy/rsync namespace를 제외하고 정식 모델·DLL·소스만 봉인했으며, ZIP 안의 정확한 파일 집합·개별 해시·CRC·엔진 트리를 다시 검증했다. 정상 numpy `.f2py_f2cmap`은 유지했다. 이 관찰을 과거 원시 중간 파일 writer 확정으로 확대하지 않는다.

완전한 원본 c37 ZIP과 최종 ZIP을 보존한 뒤, 공간 확보를 위해 이번 작업에서 생성한 재현 가능한 압축 해제 캐시만 정리했다. 사용자 PC의 파일이나 설치에는 접근·삭제하지 않았다.

## PC 인수 잔여

1. 위 정확한 후보 설치·더블클릭·실행 identity·모델 실제 실행 확인.
2. Save→소유 서버 정상 종료·endpoint 닫힘→EXE 재실행·새 PID→동일 프로젝트/작업 이력 복원→Export.
3. 나레이션 포함 MP4의 Windows 플레이어 표시·탐색·실제 소리 청취.
4. 승인 UI 원본과 헤더·Timeline·전체 비율 최종 대조·복원, 과거 잠금 예외/중간 파일 writer 로그 조사.

이 후보에서 실제 Windows EXE·모델 추론·설치 스크립트를 실행했다는 판정은 발급하지 않았다. PR #23 HOLD / DO NOT MERGE, main 병합·force push 금지, Marketing·AVORA DEFERRED_EXTERNAL, 직원 최종 패키지 금지, 전체 제품 PASS 금지를 유지한다.
