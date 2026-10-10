# 직원용 Windows 패키지 검증 현황

최종 배포 판정: RUNTIME_DEPENDENCY_LEAK. EMPLOYEE_PACKAGE_CLEAN_WINDOWS_E2E_PASS 아님.

Python 3.11.9, CPU PyTorch 2.14.0, Torchvision 0.29.0, NumPy 2.2.6, OpenVINO 2025.1.0으로 배포 런타임을 조정했다. 실제 모델 구성요소 시험에서 한국어 STT, PHOTO SAM, VIDEO SAM tracking, Intel 4x가 통과했다.

복사 설치본 UI에서 VIDEO tracking/재생, PHOTO 1920x1080 확대/미리보기, 저장 후 탭을 닫고 새 탭에서 프로젝트 복원, ZIP 내보내기, Shortform 미지원 안내와 기본 작업 지속을 확인했다. 구성요소 시험을 모든 UI E2E 통과로 간주하지 않는다.

허용된 임시 프로필에서 제거·재설치가 완료되었고 보존 데이터 17개 파일의 해시가 모두 일치했다. 실제 기본 Windows 프로필 설치와 바탕화면 시작 2/2는 아직 검증하지 못했다. 기본 설치 경로 쓰기 권한 요청은 허용 값이 반환되지 않았으며 사유도 제공되지 않았다.

현재 후보 ZIP: 1,388,859,811 bytes. SHA-256: d9afe1d284f5d8fb295955442f70b6c96f5a20a138575b21dfb13af92c5cafc8. 5개 분할본의 재조립 해시 검증은 통과했다. 이 후보는 직원 배포 승인본이 아니다.

패키지에 msvcp140.dll, msvcp140_atomic_wait.dll, vcruntime140_threads.dll이 빠져 현재 PC의 외부 Visual C++ 런타임에 의존한다. 공식 Microsoft 배포본의 DLL 서명·해시를 기록했으나 재배포 권한 확인 전 최종 패키지에 포함하지 않았다. 라이선스 및 FFmpeg 재배포 고지 감사도 미완료다.

기존 브랜치 최신 구현 커밋 a70e7cfd88555f6a8ef11f49fbd25f511431598c. 분할 설치 압축 해제 경로 수정은 원격 파일과 정확히 일치한다. main 병합, 강제 푸시, 신규 저장소·워크트리·브랜치를 만들지 않았다.
