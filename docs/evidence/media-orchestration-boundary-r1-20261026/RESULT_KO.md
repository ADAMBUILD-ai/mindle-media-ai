# MEDIA 역할 고정·표준 인계 패키지 R1

실행 소스: `94c2a0b102f2ad6c7dd2c4c6d82d1a5de3dafa31`  
판정: **MEDIA 오케스트레이션 역할 구현 / 실제 30초 제작 BLOCKED_ASSET_INTAKE**

MEDIA는 토지 판단, 도면 변경, CAD·SketchUp 원본 입출력, 2D·3D 관계 검증을 다시 만들지 않는다. 전달된 자료의 출처·해시·참조를 받아 실제 영상 제작을 지휘한다.

실제 실행이 Qwen 장면 계획, FFmpeg 조립, Supertonic 한국어 음성, 음량 합성, 기술 검사, 저장, 실제 재시작, Reopen, Export를 모두 통과하면 `MEDIA_PRODUCTION_PACKAGE.json`을 생성한다. 이 패키지는 `projectId`, `revisionId`, 실행 소스·입력 해시, source assets, storyboard, 도구 실행 기록, QA, final MP4, Export, 복구 이력, evidence receipt를 포함한다.

Wan/LTX/Blender 신규 장면 생성은 실제 실행 근거가 없으므로 `NOT_IMPLEMENTED_NEW_SCENE_GENERATION`으로 기록한다. 요청·실행하지 않은 자막도 생성됐다고 표시하지 않는다. 빈 입력, 시험 영상, 임의 원고, 과거 산출물로는 패키지를 생성하지 못한다.

검증: Python **465 PASS / 6 SKIP**, UI 계약 **2 PASS**, 구문·증거 동기화·소스 패키지 트리 검사 PASS.

실제 입력은 아직 모두 미접수이므로 Qwen·FFmpeg·Supertonic·최종 MP4·사람 시청·청취는 실행하지 않았다. Build Gate=false와 PR #23 Draft/HOLD를 유지한다.
