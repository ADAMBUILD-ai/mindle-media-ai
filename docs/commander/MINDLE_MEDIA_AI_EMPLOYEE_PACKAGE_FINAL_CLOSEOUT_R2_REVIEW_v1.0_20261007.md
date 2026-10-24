# 직원용 Windows 패키지 Final Closeout R2 검증

판정: RUNTIME_DEPENDENCY_LEAK. EMPLOYEE_PACKAGE_CLEAN_WINDOWS_E2E_PASS 아님.

새 제어 파일과 지시서를 동기화하고 CONTROL_PLANE_PASS를 얻었다. 완료된 작업을 재사용했고 수정 후 소스 회귀 시험 56개가 통과했다.

실제 설치 복사본의 HTTP 서버에서 VIDEO SAM tracking, 한국어 Whisper STT, PHOTO SAM segmentation, Intel 4x가 통과했다. 실제 출력·미리보기 다운로드 해시, 패키지 FFmpeg 디코딩, 1920x1080 확대 크기를 확인했다. STT 정확도나 SAM 의미적 대상 선택 벤치마크를 주장하지 않는다.

서버를 완전히 종료하고 재시작한 뒤 프로젝트 1ef711bb-7fba-4f62-9365-d4acfc4dae73의 네 작업이 복원됐고, 내보낸 ZIP CRC·프로젝트 포함·다운로드 해시와 Shortform 503 이후 기본 기능 지속을 확인했다. 브라우저에서 동영상 readyState=4, 1920x1080 사진과 한국어 자막 공존을 확인했다.

설치/제거/재설치와 데이터 17/17 해시 보존은 R2가 지정한 이전 실제 임시 프로필 PASS를 재사용했다. 기본 Windows 프로필과 실제 바탕화면 cold launch 2/2는 아직 미실행이다. 일반 Windows에서 실행할 FINAL_EMPLOYEE_PACKAGE_HOST_GATE.cmd/.ps1과 결과 JSON/로그 생성 기능을 제작했다. 구문 검사는 통과했으나 이를 실제 기본 프로필 PASS로 간주하지 않는다.

소유자는 Visual Studio 재배포 권한이 아직 확인되지 않았다고 답했다. 새 Microsoft DLL/설치기를 패키지에 추가하지 않았다. 별도 온라인 보조 설치기는 공식 Microsoft URL·서명 검증·INSTALL 동의·해시/버전 기록을 적용했다. 실제 설치는 수행하지 않았고 검사 모드만 실행했다. 기존 Python/NumPy 포함 Microsoft DLL의 재배포 근거와 FFmpeg 정적 의존성 전체 소스 제공 조건도 미확인으로 기록했다.

실제 서버 DLL 122개를 조사했고 msvcp140.dll, vcruntime140_threads.dll, msvcp140_atomic_wait.dll이 Windows System32에서 로드되는 것을 확인했다. 따라서 완전 오프라인 자체 포함 판정은 실패다.

새 R2 후보 ZIP: 1,390,413,884 bytes. SHA-256: fe993be98a289a7d297466e312cba39b12477650c9dd73e39d0644b44d7c05d1. 실제 ZIP 항목 21,194개가 manifest와 일치하며 중복이 없다. 300MiB 분할본 5개를 재조립하고 새 ZIP 해시와 일치하는 것을 실제 확인했다. 이 해시는 검증 후보의 해시이며 런타임 의존성 마감 후 최종 해시로 재사용하지 않는다.

구현 커밋 0371cb72ee00802b5b9bd17bd05c809858cba813의 파일 10개를 원격에서 정확히 읽어 확인했다. 기존 브랜치만 사용했고 main 병합·강제 푸시·새 저장소/워크트리/브랜치를 만들지 않았다. 대기 중인 레이아웃 최적화 지시서는 실행하지 않았다.

Intel 4x 시험은 480x270 고정 입력에서 1920x1080 출력을 검증했다. 다른 입력 크기의 4x 확대를 검증한 것으로 간주하지 않는다.
