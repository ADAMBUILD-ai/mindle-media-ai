# MEDIA 개발팀 — TEST R2 재사용 우선·재빌드 증거 Gate

기준일: 2026-10-24 KST  
대상: `ADAMBUILD-ai/mindle-media-ai`

이번 조사에서는 확정적인 중복 빌드를 확인하지 못했다. 근거 없이 CI를
변경하지 않고 기존 TEST R2 후보를 사무실 PC 인수에 우선 사용한다.

## 실행 원칙

1. 현재 후보의 source·EXE·payload manifest·ZIP·Runtime ID와 생산·readback·
   transport run을 한 세트로 유지한다.
2. 사무실 PC 인수는 TEST R2로 진행한다. 작업 창 또는 원격제어 연결 문제를
   제품 결함이나 재빌드 사유로 바꾸지 않는다.
3. 재빌드 요청은 새 승인 ID, 정확한 부모 SHA, 1회 attempt, 변경 파일 목록,
   파일별로 TEST R2가 해결할 수 없는 이유, 열린 Build Gate를 먼저 제출한다.
4. 기존 승인 ID와 producer run은 이미 소비됐다. 재사용하지 않는다.
5. 기존 모델·설치본·사용자 프로젝트·R9와 TEST R2 증빙은 삭제하거나
   덮어쓰지 않는다.

## 서로 다른 세 단계

| 단계 | Run | 역할 | 새 빌드 여부 |
|---|---:|---|---|
| Windows 후보 생산 | `39985471598` | 승인된 1회 후보 제작과 실제 원격 Windows 실행 | 예, 이미 소비됨 |
| 독립 readback | `39987617196` | 생산물을 다시 받아 전체 바이트와 CRC 확인 | 아니오 |
| 동일 바이트 transport | `39989419656` | 검증된 파일을 전송 크기로 재분할·복원 확인 | 아니오 |

세 실행은 목적과 증거가 다르다. 중복 빌드로 묶어 취소하거나 하나의 성공으로
나머지를 대체하지 않는다.

## 현재 결론

- `package_build_allowed=false`
- 기존 승인 attempt 소비 완료
- TEST R2 원격 Windows 후보·readback·transport 완료
- 사무실 PC 인수·사람 청취·승인 UI 최종 대조 미완료
- 연결 장애만으로 재빌드 금지
- PR #23 HOLD / DO NOT MERGE 및 main·force push 금지 유지
