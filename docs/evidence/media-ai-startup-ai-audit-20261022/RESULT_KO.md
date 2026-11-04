# 2026-10-22 실행 장애 및 AI 제품 연결 전수 점검

판정: **REWORK_REQUIRED / 소스 수정·회귀 완료, 설치된 Windows 후보 인수 미완료**.
기준 HEAD: 196341fc4774846bf2987792551b848a4d79226b. 사용자가 받은 후보 소스는 e00e6e0b82994fca628d6ca3cf039f7dc43c15c6.

## 1. 사용자 사진으로 확인한 실행 실패

오류 창: `패키지 검증 실패: runtime/site-packages/PIL/__pycache__/ExifTags.cpython-311.pyc`.
바로가기는 후보의 MINDLE_MEDIA_AI_RUN을 가리킨다. 실패는 런처의 파일 크기/SHA 검사이며 모델 추론에 도달하기 전이다. 사용자 설치 파일의 바이트를 직접 회수한 것은 아니다.

코드에서 확정한 결함: 실행 시 갱신될 수 있는 .pyc를 manifest에 봉인한 후보를 발행했고, Python 실행에 -B가 없어 import가 이를 다시 쓸 수 있다. 기존 exporter는 숨김 복사 임시 파일만 제외하고 __pycache__는 포함했다. 최초 실행 무결성 검사·ZIP CRC는 다음 실행 안정성을 검증하지 못한다.

새 회귀는 실제 Python 모듈과 오래된 캐시를 만들고 import를 별도 프로세스에서 실행했다. 일반 import는 캐시 해시를 바꾸고 -B import는 원래 해시를 보존했다. **사용자 PC의 해당 파일을 쓴 정확한 PID·시각은 미확정**이지만, 실행과 검증이 충돌하는 패키지 설계 결함은 재현됐다. 다운로드 재시도·관리자 실행·잠금 삭제로 해결할 문제가 아니다.

수정: bootstrap→Python, launcher→server, durable queue→worker 모두 -B 사용. launcher 초기에 sys.dont_write_bytecode 설정. 다음 공식 builder의 최종 manifest와 archive에서 __pycache__/.pyc 제외. 기존 manifest 검증·모델 해시·잠금은 제거하지 않았다. 과거 증거 assembler는 기록으로 보존했다. 후속 후보는 이번 수정된 builder 정책을 사용해야 하며, 기존 c37 frozen EXE 재사용만으로 bootstrap 수정이 들어갔다고 할 수 없다.

**기존 캐시는 자동 복구되지 않는다. 현재 설치된 R1이 고쳐졌다고 주장하지 않는다.** 미검증 캐시를 무조건 삭제하거나 manifest 해시를 현장 값으로 바꾸는 복구 도구는 발행하지 않았다. 원본 후보와 프로젝트 데이터를 보존한다.

## 2. AI라는 체감이 부족했던 코드상 이유

| 기능/화면 | 실제 처리 | 이번 판정 |
|---|---|---|
| VIDEO 일반 자연어 | 종전에는 나레이션·순차 등 일부 단어만 Qwen 경로. 대비 등 다수 표현은 키워드 처리 또는 거절 | 연결 결함 수정. 지원 대화/미지원 요청은 plan API로 전달; 명시적 수동 도구 경로 보존 |
| 생성형 계획기 | Qwen2.5-1.5B-Instruct-GGUF + llama.cpp llama-completion. 모델 응답을 allowlist 단계로 검증 | 실제 생성형 코드 경로 있음. 이번 새 모델 추론은 미실행, 과거 한정 실추론 증거와 구분 |
| 단순 나레이션 지시 | 종전 정규식이 steps를 직접 만들어 모델 추론을 우회 | 자연어에서 주입 steps 제거. 실제 모델 계획 경로로 전달 |
| 누락된 복합 계획 | 요청하지 않은 작업은 차단했으나 요청 일부 누락은 통과 가능 | 요청 보정·받아쓰기·자막·나레이션 누락 거절 추가. 범용 의미 이해/모든 수치 정확성 PASS 아님 |
| VIDEO AI 자동 편집/하이라이트 | OpenCV 움직임·노출·선명도 표본 분석 + FFmpeg | 생성형 모델 아님. 기존 버튼·배치 보존, 설명 추가 |
| VIDEO AI 효과 | FFmpeg 필터 | 생성형 효과 아님. 설명 추가 |
| PHOTO AI 보정 | Canvas 픽셀 밝기 분위수·색온도 통계 | 모델 추론 아님. 완료 메시지·설명 명확화 |
| PHOTO 자연어 | 한정 키워드→고정 보정값 | 생성형 계획기 아님. 사용 범위 명시. 임의 이미지 생성으로 표시하지 않음 |
| PHOTO 스타일/인물/유사 이미지 | 흑백/따뜻한 필터, 전체 부드럽게 보정, 첨부 이미지 색상 히스토그램 | 신경망 스타일 전이·얼굴 전용 복원·의미 임베딩 검색 아님 |
| 사진 분할·배경 제거 | SAM 2.1 검증 어댑터·실제 분할 결과 | 기존 모델/가중치/알고리즘 보존. 새 추론 반복 안 함 |
| 4배 업스케일 | Intel single-image-super-resolution-1032 검증 경로 | 기존 PASS 보존. 새 추론 반복 안 함 |
| 영상 객체 추적 | SAM 기반 추적/메모리 어댑터 | 코드 경로 확인; 사무실 PC 전체 영상 새 실증 아님 |
| 한국어 STT | Whisper-small 로컬 어댑터 | 코드 경로 확인. 이번 새 Whisper 추론 아님 |
| 한국어 신경망 TTS | sherpa-onnx 1.13.8 / Supertonic 3 ONNX | 후보 설정/제품 호출 경로 존재. 과거 실제 WAV 증거 있음. 이번 PC 생성·사람 청취는 미확인 |
| eSpeak | 규칙 기반 formant 합성, 대체 설정 경로 | 신경망 TTS로 둔갑시키지 않음. 후보 기본 설정은 Supertonic |
| 영속 큐·취소·재시도 | SQLite 상태/소유 워커 프로세스/제한 재시도 | 실제 로컬 HTTP·프로세스 회귀 PASS. Windows 고유 프로세스 제어 인수 별도 |
| Save/Reopen/Export/MP4 | 저장 참조·봉인 파일·FFmpeg H.264/yuv420p/AAC·ZIP | 소스 회귀 PASS. Windows 설치 후보 완전 재시작·플레이어 청취로 확대 안 함 |
| 텍스트→새 이미지/영상 생성 | 해당 생성 모델·제품 실행 경로 없음 | **NOT_IMPLEMENTED**. 편집/계획/TTS를 이미지·영상 생성 완료로 대체 불가 |
| Marketing/승인 AVORA | 외부 계약·연동 검증 대기 | DEFERRED_EXTERNAL 유지. 광고 모드는 일반 workflow보다 먼저 처리해 혼선 방지 |

판단: 기존 제품은 실제 모델 기반 기능과 일반 편집 기능이 함께 있지만, **범용 생성형 미디어 제품 개발 완료는 아니다**. 모델 파일 포함, 단위 테스트, 과거 일부 실추론만으로 사용자가 받은 Windows 제품의 AI 전체 정상 작동을 보장할 수 없다. 처음 실행 후 다음 날 실행 실패가 발생했으므로 배포 준비 품질도 부족했다.

## 3. 수정 범위와 검증

CHANGES.diff: 시작/서버/워커 캐시 방지, builder 캐시 제외, VIDEO 모델 라우팅, 부분 계획 거절, 설명/placeholder/결과 메시지, 회귀 테스트. 색상·배치·제목·7보정·PHOTO 모델 가중치·숏폼 버튼은 변경하지 않았다. 승인 UI 전체 일치 판정은 여전히 미완료다.

- Python 전체: **167 passed / 6 skipped** (PYTEST.txt). 초기 선별 소스 추출 때문에 fixture 누락으로 수집/1개 검사 실패가 있었고, 저장소 원본 fixture를 복원한 뒤 최종 전체 통과했다. 테스트 기대값을 완화하지 않았다.
- Node 전체: **23 passed / 0 failed** (NODE.txt).
- 신규 캐시 테스트: 실제 별도 Python import로 캐시 변화/보존 확인. Windows EXE 아님.
- 신규 VIDEO 대화 테스트: production JS 실행 + API 경계 fixture. 대비·복합 보정/자막·나레이션·내레이션·미지원 요청이 steps 주입 없이 plan API 도달. 실제 Qwen 추론 아님.
- 기존 회귀에는 실제 FFmpeg 작업, HTTP 취소, 정상 결과 보존, 재시도, 작업 이력·저장/복원·ZIP 검사 포함.
- SKIP에는 네이티브 Windows 잠금/8.3 경로, 미설치 sherpa_onnx, 한국어 폰트 조건 등이 포함된다. SKIP을 엔진 정상 판정으로 처리하지 않는다.
- 과거 엔진 원본: docs/evidence/media-ai-local-engines-closeout-20261018/RESULT_KO.md 및 WAV/MP4/원문 응답. 이 자료는 당시 Linux 소스의 한정 실행이며 이번 변경/설치 PC PASS가 아니다.

## 4. 실제 남은 마감

1. 캐시 없는 payload·수정 bootstrap/launcher/server/worker를 담은 정확한 개발 후보가 필요하다. 원본 R1·자료를 보존하고 새 identity/manifest/ZIP 해시를 발행해야 한다. 이번 점검은 후보 재생성·직원 배포가 아니다.
2. 실제 Windows에서 첫 실행→실제 모델 사용→완전 종료→다음 실행→동일 프로젝트 Reopen/Export를 검수해야 한다. 특히 PIL import 후 재실행과 큐 worker 실행 후 재실행의 모든 봉인 해시가 유지돼야 한다.
3. 실제 PC Qwen·SAM·SISR·Whisper·Supertonic 각각 모델 identity/호출/결과 해시를 확보한다. 한국어 TTS는 사용자 실제 청취를 별도 기록한다.
4. 현재 Qwen 계획 범위를 넘어선 범용 생성·PHOTO 생성형 편집은 별도 개발 범위다. 지원하지 않는 기능을 버튼이나 홍보 표현만으로 완료 처리하지 않는다.
5. 승인 UI 최종 대조, 원시 중간 파일 writer, Windows 플레이어 인수는 기존 잔여다.

PR #23 HOLD / DO NOT MERGE. main/force push 금지. Build Gate=false 유지. 외부 키 연결·직원 최종 패키지 재생성·최종 전체 PASS 문자열 발급 없음.
