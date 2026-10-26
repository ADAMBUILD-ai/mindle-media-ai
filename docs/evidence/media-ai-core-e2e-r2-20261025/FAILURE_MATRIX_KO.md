# 실패 보호 대조표

아래는 회귀/실패 주입 범위다. 실제 30초 건축 영상의 성공이나 신경망 음성 청취를 뜻하지 않는다.

| 항목 | 증거 | 범위/상태 |
|---|---|---|
| 영상·BGM 누락/해시/메타데이터 | test_e2e_intake.py, 실제 빈 입력 probe | PASS, 실제 영상 접수는 BLOCKED |
| 허용 구간·합산 길이 | test_usable_ranges_not_whole_file_duration_determine_coverage | PASS |
| 원본과 재인코딩 미리보기 분리 | test_original_input_and_transcoded_preview_have_separate_identities, 실제 lifecycle receipt | PASS |
| 가중치 분할 변조 | test_split_gguf_part_hash_is_verified_before_inference | PASS 계약. Windows 7B 새 실측 미실행 |
| Qwen 길이·비율·원고·음량 변경 | test_architecture_agent.py, test_local_planner_scope.py, test_audio_finish_cannot_change_exact_contract | PASS 계약 |
| 저장 계획과 실제 응답 불일치 | test_generated_plan_binding.py, ACTUAL_QWEN_BINDING_SMOKE | 계약 + 실제 7B 계획/변조 거부 PASS |
| 시간 초과·실행기 오류·JSON 오류 원문 | test_inference_fault_preserves_partial_reply_and_failure | PASS 실패 주입, 실제 지연 장애를 의도 발생시킨 것은 아님 |
| TTS 부재/기존 프로젝트 보존 | test_permanent_missing_tts_does_not_retry_or_change_saved_project | PASS. sherpa constructor identity 시험은 미설치 환경에서 SKIP |
| 음성 길이 초과 | FAILURE_PROTECTION_RECEIPT.long_voice | 실제 WAV 길이 검사 PASS; TTS 추론 없음 |
| 음성/BGM 해시 변경 | FAILURE_PROTECTION_RECEIPT | 실제 파일 변경 거부 PASS |
| 실제 FFmpeg 실패 | ACTUAL_FFMPEG_FAILURE.stderr.txt / FAILURE_PROTECTION_RECEIPT | 실제 비정상 종료·완료 게시 없음 PASS |
| 취소·중단 | test_cancel_own_real_process_and_no_publication, test_running_architecture_cancel_never_publishes_output | PASS |
| 출력 검수 실패 | test_quality_failure_never_publishes_project_or_jobs, test_normal_exposure_output_cannot_be_degraded_into_overexposure | PASS 계약/실제 합성 입력 |
| 30초·16:9 출력 조건 | test_fixed_30_second_quality_does_not_accept_short_video, test_candidate_probe_rejects_wrong_aspect_before_decode | PASS 거부 계약 |
| 정상 종료·콜드 재시작 | test_owned_real_product_process_cold_restart_reopen_and_export / LIFECYCLE_TOOLING_RECEIPT | 실제 Linux 자식 PID/instance 변경 PASS. Windows 후보는 미실행 |
| Export 실패 시 이전 프로젝트 | test_export_failure_preserves_previous_project_and_never_publishes_new_jobs | PASS 실제 worker + 실패 주입 |
| Export 내부 변조/작업 정보 변경 | test_export_internal_tamper_is_rejected_even_with_valid_zip_crc_and_outer_hash, test_export_cannot_hide_changed_job_metadata_behind_transport_url_normalization | PASS |
| 승인 없는 후보 호출 | test_candidate_approval_blocks_before_any_server_call | PASS, 실제 후보 호출 0 |

실제 Windows Supertonic 오류·메모리/성능·실무 작품의 화면/청취 품질은 이 표로 완료 처리하지 않는다.
