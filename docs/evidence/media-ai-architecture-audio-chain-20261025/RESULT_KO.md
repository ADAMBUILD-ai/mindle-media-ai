# MINDLE MEDIA AI 건축 영상·신경망 음성 연속 실행 보강

## 판정

`SOURCE_PASS / WINDOWS MODEL RUNTIME REVALIDATION REQUIRED / NEW CANDIDATE NOT BUILT`

## 확인한 결함

건축 AI는 Qwen으로 기존 영상의 장면 순서·길이·비율을 계획하고 FFmpeg로 MP4를 조립했지만, 같은 지시에 포함된 나레이션과 BGM을 후속 작업으로 자동 실행하지 않았다. 또한 일반 복합 계획에서 BGM 편집과 나레이션 믹스가 각각 배경음악을 받을 경우 중복 합성 가능성이 있었다.

## 수정

- 건축 Qwen 계획과 MP4 조립이 성공하면 같은 자연어 지시에서 나레이션·BGM 요청을 찾는다.
- 조립 결과 `job_id`를 입력으로 두 번째 Qwen 계획을 생성한다.
- Supertonic 한국어 신경망 음성 생성과 FFmpeg 오디오 합성을 영속 작업 큐에서 이어서 실행한다.
- 최종 프로젝트를 다시 열어 조립 영상·나레이션·BGM이 포함된 결과를 표시한다.
- 취소·실패 시 완료된 건축 MP4와 기존 프로젝트를 보존한다.
- 나레이션과 BGM을 함께 요청하면 BGM은 `mix_narration`에서 한 번만 합성한다.
- BGM 파일이 없으면 후속 작업 제출 전에 중단한다.
- 워커는 `background_volume`이 계획에 있는 경우에만 BGM을 믹스한다.

## 검증

- Python 자연어·오디오 믹싱 계약 포함 14개 시나리오 PASS
- UI 계약 3개 PASS
- Python 4개 모듈 구문 검사 PASS
- JavaScript 구문 검사 PASS
- 변경 파일 공백 검사 PASS

현재 환경에는 R3의 Qwen·Supertonic Windows runtime이 없어 이번 소스의 실제 모델 재추론과 사람 청취는 수행하지 않았다. 기존 R3에서 각 엔진이 실제 동작한 증거는 보존하지만 이번 연속 실행 변경의 Windows 증거로 확대하지 않는다.

텍스트→신규 영상 생성은 이 기능과 별개이며 여전히 미구현이다. Build Gate=false, PR #23 HOLD / DO NOT MERGE, 전체 제품 PASS 금지를 유지한다.
