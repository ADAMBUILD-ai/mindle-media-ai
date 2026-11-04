# Windows 실제 source Runtime 후속 검수 마감

2026-10-16 KST. 기준 source d227ada10072fe5629c88d4a5cc762f7bb065d2f.
최종 실행 https://github.com/ADAMBUILD-ai/mindle-media-ai/actions/runs/38801025886 — SUCCESS.
증거 https://github.com/ADAMBUILD-ai/mindle-media-ai/actions/runs/38801025886/artifacts/12004616213.

## 발견한 추가 결함과 수정

첫 원격 Windows 실행38800627258은 저장/의존 파일/Export 검사13개는 통과했으나, 서버 재시작 후 preview_url의 실제 파일 요청이404로 실패했다. 모델은 호출하지 않았고, 저장된 프로젝트 조회는 성공했다. 원인은 파일 전달에 사용하는 root와 resolved file 경로의 표현 불일치다.

Handler._file은 실제 파일의 resolved 부모 목록과 정규화되지 않은 data_dir를 비교했다. 상대 root는 Linux에서도 동일하게404를 재현했고 전체/Range 요청2개가 실패했다. Windows 실제 실행에서는 C:\Users\RUNNER~1\... 과 C:\Users\runneradmin\...의 차이도 관측했다.

ProductHttpServer 초기화 시 root/data_dir를 resolve해 서비스·URL·파일 containment가 같은 canonical root를 사용하도록 수정했다. 외부 파일을 허용하도록 검사를 제거하지 않았다. 루트 밖 파일은 계속404다. 수정 commit1fc6c9c851f8d71314158b4121a768379907fe76.

## 최종 실제 Windows 증거

- Windows source 회귀17 PASS: 기존 저장/입력·참조/atomic Export13개와 상대경로 전체/Range, 실제8.3 경로, root 밖 파일 차단4개.
- HTTP 서버 PID2124 종료, 기존 endpoint 미응답 확인, 새 PID6120으로 동일 프로젝트 재열기 PASS.
- 사진·영상 결과 파일의 실제 HTTP bytes 및 SHA256 일치.
- 설치된 공식 Chrome155.0.8059.40에서 source UI를 실제 열고 서버 재시작 후 프로젝트 복원.
- 영상 재생 버튼 실제 클릭. MediaError=null, readyState4, videoWidth160, currentTime0→0.065131.
- AAC 포함 MP4의 브라우저 오디오 디코딩:1channel/45026samples/44100Hz. 실제 소리 청취를 판정한 것은 아니다.
- 세로 사진90×160의 원본 비율과 contain 확인. Preview408×229.5 안에 이미지 요소406×227.5가 배치됐다.
- UI Export 버튼 실제 클릭, 다운로드 ZIP의 SHA를 UI 기록과 대조, CRC PASS.
- Windows source HTTP Export와 UI 다운로드 ZIP을 General 환경에 내려받아 별도 재검증. 두 ZIP 모두 SHA256 b66b0c495aa45abc4380441ae4d2bf528c88249b45b2740b5e4d0a87494ce5ee, 각4개 의존 파일의 크기/해시 및 CRC 일치.
- 최종 canonical 전체 source 회귀:113 PASS/4 Linux SKIP(run38801035307). Windows 잠금3개는 이전 실제 Windows source 실행에서 통과했고, 추가8.3 검사는 이번 Windows17개에 포함돼 통과했다.

## 범위와 남은 실제 인수

이 실행은 GitHub Windows runner의 source HTTP/Chrome 검수다. 사무실 PC, 패키지 EXE, Windows 기본 플레이어 검수로 확대하지 않는다. CI fixture용 FFmpeg는 기존 hash-pinned GPL 빌드를 RUNNER_TEMP에서만 사용했다. 제품의 LGPL FFmpeg·Media Foundation 배포 구성을 바꾸거나 새 패키지를 만들지 않았다. 모델 다운로드/추론 없음.

R9 원본 bytes와 승인 비교 원본을 확보하지 못했으므로, 이번 경로 결함을 R9 모든 오류의 원인으로 단정하지 않는다. 승인 UI 전체 일치, 사무실 EXE 종료/재실행, 실제 Windows 플레이어 재생/탐색/소리 청취는 남아 있다.

후속 검수 후보에 앞선 수정과 canonical root 수정을 함께 포함해야 한다. 현재 build gate=false를 유지했으며 기존 후보 payload 수정/재빌드/배포/직원 최종 패키지 생성 없음. PR23 HOLD / DO NOT MERGE, main/force push 금지. OpenAI/Marketing/AVORA 기존 Gate 유지. owner_pc_runtime_pass=false, final_product_pass=false.
