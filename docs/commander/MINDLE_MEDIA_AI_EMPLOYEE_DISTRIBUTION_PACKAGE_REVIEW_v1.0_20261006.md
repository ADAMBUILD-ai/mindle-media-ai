# 직원용 Windows 배포 패키지 실행 검토 — 2026-10-06

최종 상태: **BLOCKED**. EMPLOYEE_PACKAGE_CLEAN_WINDOWS_E2E_PASS가 아니다.

지정된 다섯 파일을 순서대로 확인하고 validator를 실제 실행하여 CONTROL_PLANE_PASS를 얻었다. 로컬과 원격 canonical branch의 시작 HEAD는 b39ca305839f7d9f2fe1cb8ae25c8212159b91be였다. 새 저장소/브랜치/worktree, main merge, force-push는 수행하지 않았다.

## 실제 수행

- 토큰 없는 명시적 로컬 모드, 시작 시 세 모델 해시 검증, HF 클라이언트 생성 및 다운로드 경로 차단을 구현했다.
- Git 없는 패키지 identity와 제품 실행기, 설치/삭제, 분할/해시 재조립 스크립트를 추가했다.
- 빌드 전제조건을 실제 검사했고 실패했으므로 완성 ZIP을 생성하지 않았다.
- 복구된 SAM/Whisper/Intel 원본의 지정 SHA-256/SHA-384를 실제 재계산하여 일치를 확인했다. 패키지에 복사된 모델의 검증이나 모델 실행 성공을 의미하지 않는다.
- 새 오프라인/복원 회귀검사 4개를 포함한 전체 자동검사 56개가 통과했다. Clean Windows 설치된 제품의 기능 검증은 아니다.
- 1MiB 분할 단위의 무작위 2,500,000바이트 시험 ZIP을 3개로 나누고 재조립 SHA-256 일치 및 손상 part 거부를 실제 확인했다. 이 시험 ZIP은 직원 패키지가 아니다.

## 완료를 막는 조건

실제 설치 위치 MEDIA_AI, 사용자 데이터 위치 MEDIA_AI_DATA 및 시작 메뉴 바로가기 쓰기 권한은 두 번의 범위 지정 요청 결과에 포함되지 않았다. 허용되지 않은 설치/삭제는 수행하지 않았다.

현재 Python 3.11.9 환경의 PyTorch는 2.14.0+cu126이다. 동일 기본 버전 CPU wheel 2.14.0+cpu를 공식 SHA-256 8e2c47c6556c7d5a85848634372bb2252907d411e9cad669c99406856d536eb5와 대조하여 확보했다. 별도 경로에 CPU 런타임 후보를 구성하고 있으나 설치된 패키지의 검증 모델 실행은 아직 수행하지 않았다. OpenVINO 2025.1.0 Windows wheel은 보관본에 있다. 현재 NumPy 2.4.6은 이 wheel의 NumPy<2.3.0 조건과 충돌하며, 호환 버전 조정 여부에 대한 사용자 질문이 대기 중이다. ffmpeg 6.1.1/ffprobe 및 모델 라이선스는 staging에 확보했고 버전 명령 실행을 확인했다. 완성된 배포용 runtime lock 및 전체 redistribution notice 검증은 남아 있다.

Whisper-small 소스 모델 카드의 라이선스는 MIT이며 현재 모델 SSOT도 MIT로 기록한다. 지시서의 Apache-2.0 표기와 차이가 있으므로 Apache로 바꿔 표기하지 않았다.

## 남은 구현/검증

빌드/설치/실행 스크립트는 초기 구현이며 완성 패키지로 검증된 상태가 아니다. 전체 runtime closure 및 notice를 갖춘 staged runtime이 필요하다. Save→Close→Reopen UI 복원 코드를 추가했고 서비스 재생성 후 저장/Export 가능함을 회귀검사로 확인했다. 실제 설치된 UI 검증, 일반 사진 크기에 대한 Intel 모델 입력 처리, 설정 파일 기반 Marketing 연결은 추가 확인/구현이 필요하다. 설치/바탕화면 2/2/모델 4기능/Preview/Save-Reopen/Export/Shortform/삭제-재설치/데이터 보존 시험은 NOT_RUN이다. 해당 evidence 파일의 존재를 실행 성공으로 계산해서는 안 된다.

직원용 ZIP, 실제 분할본, 패키지 SHA-256, 완성 runtime lock, clean Windows self-containment proof는 없다. 다음 실행은 이 변경사항과 BLOCKED evidence에서 계속하여 실제 배포 산출물과 설치된 제품 검증을 완료해야 한다.

## 게시 방식과 로컬 제약

.git 쓰기 권한을 부여받은 뒤에도 .git/index.lock 생성이 Windows에서 거부되어 로컬 commit/push는 수행할 수 없었다. 연결된 GitHub API에서 기존 canonical parent의 후속 커밋을 만들고 동일 브랜치를 fast-forward하는 방식으로 게시를 시도한다. 새 저장소/브랜치/worktree를 만들지 않으며 force 옵션도 사용하지 않는다. 로컬 HEAD는 이 방식으로 갱신되지 않는다. 후보 런타임 복사는 완료됐고, NumPy/OpenVINO 요구 버전 충돌을 그대로 기록했다.

## 실제 원격 확인 및 후보 런타임 검사

원격 구현 커밋 ac0e6909f55aaf73ebcf8dcf736c37ebfda74824를 동일 브랜치에 fast-forward 게시했다. ls-remote로 HEAD를 확인했고 Evidence, product_server.py, 빌더, Review의 원격 내용이 게시 입력과 동일함을 검증했다. 로컬 HEAD는 기존 b39ca305 상태로 남는다.

후보 Python 3.11.9가 CPU PyTorch 2.14.0+cpu(CUDA 없음), Transformers, OpenVINO 2025.1.0, NumPy 2.4.6, OpenCV를 package-local 경로에서 import하는 것을 실제 확인했다. import site가 사용자 site-packages를 추가한 문제가 발견되어 ._pth에서 제거했고 재검사에서 모든 sys.path가 후보 런타임 내부임을 확인했다. 원래 NumPy/OpenVINO 메타데이터 요구조건 충돌은 여전히 남아 있으며 조정 질문은 대기 중이다.

검사 중 OpenVINO telemetry가 사용자 Intel 폴더에 쓰기를 시도한 경고도 기록했다. 제품 서버 자식의 LOCALAPPDATA/APPDATA를 제품 데이터 폴더로 지정하도록 실행기를 수정했으나 실제 설치된 서버 검증은 아직 없다. 전체 자동검사 56개는 다시 통과했다. 이 검사들은 완성 직원 ZIP의 Clean Windows E2E PASS를 뜻하지 않는다.
