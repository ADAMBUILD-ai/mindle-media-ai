# MINDLE MEDIA — AI 영상 제작 오케스트레이션 경계 R1

## 단일 책임

MEDIA는 사용자의 자연어 제작 지시와 승인된 실제 자료를 받아 장면 계획, 도구 실행, 결과 검수, 실패 보존·복구, 최종 인수 패키지를 지휘한다.

MEDIA는 다른 설계 팀의 토지 판정, 도면 변경, CAD·SketchUp 원본 입출력, 2D·3D 관계 검증을 재구현하지 않는다. 그런 자산이 영상 제작 자료로 전달될 경우에도 출처·해시·참조만 기록한다.

## 표준 반환

실제 소스 실행이 모든 기술 Gate를 통과했을 때만 `MEDIA_PRODUCTION_PACKAGE.json`을 쓴다. 패키지에는 다음을 포함한다.

- `projectId`, `revisionId`, `schema_version`, `createdAt`, `status`
- 실행 소스·입력 Manifest hash
- 실제 입력 자산의 역할·라벨·SHA-256·bytes·object reference
- 실제 Qwen 장면 계획과 음향 계획의 identity
- FFmpeg 조립·Supertonic·검수·저장·재시작·Reopen·Export 영수증
- 최종 MP4·Export 해시·실패/복구 이력

사람의 화면·음성 검수는 기술 통과와 분리하며, 그 전에는 `full_product_pass=false`를 유지한다.

## 경계와 정직한 상태

- 기존 자료 조립은 실제 실행 증거가 있을 때만 `existing_asset_assembly`로 기록한다.
- Wan/LTX/Blender를 통한 신규 장면 생성은 실행·검수 증거가 없으면 `NOT_IMPLEMENTED_NEW_SCENE_GENERATION`으로 기록한다.
- 자막은 요청·실행되지 않았다면 `NOT_REQUESTED_NOT_GENERATED`로 기록한다.
- 빈 입력, 권리 미확인 자료, 임의 원고, 테스트 영상, 과거 결과물은 패키지를 만들지 못한다.

## 다음 팀 또는 사람 검수에 필요한 증거

수신자는 패키지의 source asset hash, 실제 계획 원문, 도구 실행 기록, 최종 MP4, Export archive hash, 저장·재열기 evidence를 함께 확인한다. 화면 설명이나 파일명만으로 완료를 인정하지 않는다.
