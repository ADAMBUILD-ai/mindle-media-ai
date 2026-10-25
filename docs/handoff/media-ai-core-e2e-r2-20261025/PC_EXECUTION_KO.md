# PC 후보 단일 실행 절차 (R2 통합 보강)

General 소스 실행/사전검사는 `EXECUTION_KO.md`, 단일 자료 접수표는 `INTAKE_AND_APPROVAL_KO.md`를 사용한다. `INPUT_MANIFEST.json`이 원본이고 상태 판정은 매번 재계산한다. 기존 BLOCKED_PROBE는 이전 HEAD의 이력이며 실행 입력/승인 자료가 아니다.

아래 PC 명령은 **실제 자산 인수 + Windows 7B 채택 승인 + 정확한 최신 후보 확보** 후에만 실행한다. 현재 Build Gate=false이며 새 EXE를 제작하지 않는다. 기존 R3, Linux 실행기 해시, 빈 승인 템플릿으로 통과시키지 않는다.

1. PC의 읽기 전용 사양/identity 기록을 재확인한다. 이미 전달된 PC snapshot은 보존하되 현재 가용 RAM이나 7B Windows 성능 PASS로 사용하지 않는다.
2. 실제 영상·구간·권리 근거·BGM·확정 원고·음량·장문 정책을 Manifest에 접수한다.
3. 별도 승인된 최신 후보 EXE와 `_payload/PACKAGE_MANIFEST.json`을 확인한다. 후보 EXE SHA·패키지 Manifest SHA·소스·입력 SHA·Windows 7B 채택 승인을 `WINDOWS_CANDIDATE_APPROVAL.template.json` 형식의 실제 승인본에 결속한다. 템플릿은 승인이 아니다.
4. 선언 의존성을 갖춘 검증 Python/동결 실행 환경에서 아래 명령을 한 번 실행한다. 새 증거 디렉터리만 허용하며 과거 출력은 덮어쓰지 않는다.

```powershell
$env:PYTHONPATH = "src"
python scripts/run_real_architecture_acceptance.py docs/handoff/media-ai-core-e2e-r2-20261025/INPUT_MANIFEST.json --expected-source "[승인 후보의 전체 source SHA]" --exe "[승인된 최신 후보의 MINDLE_MEDIA_AI_RUN.exe]" --approval-file "[실제 후보·모델 승인 JSON]" --evidence-root "[새 PC 실행 증거 디렉터리]"
```

실제 후보가 없어 EXE 경로·패키지 SHA를 확정하지 않았다. 후보 제작 승인 뒤 실제 값으로 동결하며 R3 경로를 대신 넣지 않는다. 환경 의존성이 누락되면 실행 환경 차단으로 분류한다. 검사를 빼거나 더 낮은 모델로 바꾸지 않는다.

실행기는 같은 제품 API와 General 공통 검사로 입력 재검사 → 제한 구간 적용 → 실제 pinned 7B 장면 계획 → 조립 → 실제 pinned 7B 음성 계획 → 실제 Supertonic·단일 믹스 → 30초/16:9/H264/AAC/전체 디코딩 → 공식 nonce 종료 → 기존 PID 종료 확인 → 승인 EXE 콜드 재실행 → 전체 job/artifact Reopen → Export ZIP 및 내부 파일 SHA 검사를 수행한다.

새 후보의 설치된 전체 Manifest 파일과 모델 2분할·Windows 실행기/runtime tree·Supertonic 데이터 identity를 확인한다. Linux identity는 대입하지 않는다. 영상/음성 계획·원고·세 음량·나레이션 job ID가 다르면 실패다. 시간 초과는 해당 작업 ID만 취소하고 중간 산출물/기존 프로젝트를 보존한다.

기술 통과 표시는 `TECHNICAL_E2E_PASS_HUMAN_ACCEPTANCE_REQUIRED`, full_product_pass=false다. 최종 MP4를 실제 UI에서 재생하고 건축 장면/구도/스토리/자막과 한국어 발음·자연스러움·BGM 균형을 사람이 확인한 기록을 추가한다. 기술 실행기가 UI/청취를 대신 완료했다고 표시하지 않는다.

반환: RESULT.json, 단계별 JSON, 실제 Qwen prompt/response가 있는 후보 데이터 경로, 최종 MP4 SHA, 콜드 재실행 로그/old-new PID, Export ZIP/내부 hash, 화면·청취 사람 검수표, 남은 Gate. main 병합·배포·기본 모델 교체·추가 예산 변경은 금지한다.
