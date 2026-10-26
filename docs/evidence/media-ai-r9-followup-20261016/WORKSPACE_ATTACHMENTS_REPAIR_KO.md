# 실행 전 참고 이미지·음성 저장 누락 수정
기준일: 2026-10-16 KST

## 결과 및 범위
실제 Windows Chrome에서 저장 누락을 재현하고 소스 수정을 검증했다.
원인은 모델 처리 실패나 Preview 표시가 아니라 프로젝트 저장 데이터 누락이다.
현재 배포 후보 fef692312ae8은 변경하지 않았으며 이 추가 수정은 아직 포함하지 않는다.

- 수정 commit: 4e20d02e601302cdebf56a131c1eb60cde0f19cb
- 검증 source HEAD: c443d0388e84a3fdc637299d19b1b3cc8260140d
- Windows 실행: https://github.com/ADAMBUILD-ai/mindle-media-ai/actions/runs/38838462732
- 원본 artifact: 12020147459 (1743808 bytes)
- 전체 소스 검증: run38838236618 /122 PASS·4 native-Windows-only SKIP.
- 해당 Windows 회귀22 PASS /Node5 PASS.

## 재현과 원인
기존 소스55003e0에서 사진을 불러오고 PHOTO/VIDEO 참고 이미지 각1개 및 STT용 WAV를 첨부한 뒤 실제 프로젝트 저장 버튼을 눌렀다.
브라우저를 닫고 서버 PID8512를 종료하여 endpoint 미응답을 확인했다.
새 PID6912로 재시작·재열기하자 참고 이미지2개와 음성이 모두 사라졌다.
Save 요청은 완료 job_ids만 전송했고, 서버의 project.json/Export는 완료 Job에 연결된 파일만 저장했다.
아직 모델에 전달하지 않은 CommandPanelState.references와 state.audio는 어디에도 영속화되지 않았다.

## 수정
- UI의 기존 참고 이미지 상태와 음성 File을 Save 요청의 workspace에 직렬화한다.
- 서버는 이미지 유효성과 첨부 형식을 검증하고 프로젝트별 content hash 파일로 보존한다. 같은 첨부의 반복 저장은 중복 파일을 만들지 않는다.
- project.json의 workspace에 원본 이름/MIME/크기/SHA를 저장하고 재열기 URL을 제공한다.
- UI는 새 workspace를 우선 복원한다. 구 프로젝트의 완료 Job 기반 참고 이미지/음성 복원은 유지한다.
- 비어 있는 workspace는 명시적 삭제로 취급해 예전 참고 이미지가 되살아나지 않는다.
- 구 API가 workspace 없이 저장하면 기존 workspace를 보존한다.
- Export의 BUNDLE_MANIFEST에 workspace_reference/workspace_audio를 추가하고 기존 원자 ZIP/CRC/해시 검사에 포함한다.
- 새 프로젝트는 기존 첨부 상태를 비운다.

저장 조건인 완료된 미디어 작업1개 이상은 유지한다. 모델을 실행하지 않은 빈 프로젝트만의 저장 기능을 새로 만들지 않았다.
첨부는 영역별 참고 이미지 최대5개, 파일별32MB 이하로 검증한다. 원본 미디어 편집·모델 입력 제한을 변경하지 않았다.
새 UI 요소나 배치/색상 변경은 없다. HTML·승인 CSS·PHOTO CSS·아이콘·사진/영상 workspace·shell의7파일 해시가 전후 동일하다.
{
  "unchanged": [
    "ui/index.html",
    "ui/approved_visual.css",
    "ui/interaction.css",
    "ui/assets/brand/MINDLE_MEDIA_AI_APP_ICON.ico",
    "ui/photo_workspace.js",
    "ui/video_workspace.js",
    "ui/workspace_shell.js"
  ],
  "changed": [
    "ui/interaction.js",
    "ui/product_integration.js"
  ]
}

## 실제 검증
수정 소스의 PID9900 종료/endpoint 미응답→PID5692 생성→동일 프로젝트 재열기를 실제 Chrome155.0.8059.40에서 수행했다.
참고 이미지2개와 WAV의 이름·크기·SHA가 저장 전후 일치했다. 새 프로젝트 전환 시 모두 비워졌다.
WAV는 생성한 무음 저장 fixture다. 한국어 STT 추론·음성 인식 품질·실제 청취 PASS로 취급하지 않는다.
PHOTO 분할/4×·기존 모델·패키지 빌드를 반복하지 않았다.

UI 내보내기 버튼으로 내려받은 ZIP:
- SHA256: 1639628c610a8e6d00d9de28e49021aaf36ef37f70331e727689096d717ef6a5
- bytes: 3735
- CRC PASS, manifest6파일 모두 독립 크기/SHA 검증.
- input/output/workspace_reference/workspace_audio 포함.
- 미실행 참고 이미지2개와 WAV가 실제 ZIP 바이트에 존재한다.

회귀검증에는 서비스 재시작, 중복 저장 dedup, 구 API의 workspace 보존, 명시적 비우기, 잘못된 첨부로 인한 기존 저장본 보존, 첨부 변조 시 기존 Export 보존을 포함했다.
첫 전용 CI38838231820은 기존 영상 회귀 fixture용 FFmpeg 누락으로21 PASS/1 FAIL이었다.
해시 고정 CI 전용 FFmpeg를 추가한 38838462732에서22 PASS와 브라우저 전후 비교를 완료했다. 제품 배포 FFmpeg는 변경하지 않았다.

## 판정
| 항목 | 결과 |
|---|---|
| 기존 소스의 미실행 참고 이미지/음성 저장 누락 | FAIL 재현 |
| 수정 소스의 Save→서버 완전 재시작→Reopen | PASS |
| 수정 소스의 실제 UI Export 및 독립 ZIP 검증 | PASS |
| 완료 Job의 기존 입력/참조/원자 Export 경로 | 회귀 PASS |
| 현재 Windows 후보에 이번 추가 수정 포함 | 미포함 |
| 후속 Windows 후보 | 필요, build gate=false 유지 |
| 실제 사무실 PC/Windows 플레이어/승인 원본/R9 예외 로그 | 기존 잔여 항목 유지 |
| Marketing/AVORA | DEFERRED |
| OpenAI 연결 | 미승인·미연결 |

기존 R9 후보6수정과 원격 실기동·전달 ZIP 증거는 보존한다. 이번 소스 PASS를 해당 후보/실제 사용 PC의 PASS로 확대하지 않는다.
PR23 HOLD / DO NOT MERGE, main/force 금지, owner_pc_runtime_pass=false, final_product_pass=false.
