# General Work 전체 기능 인벤토리

Runtime source: `92897f4ff943d30d788416dbb10324f3df2b9427` · Run: 37752630381

| 기능 / UI 입력 | 상태 | Runtime / API | 실제 증거 |
|---|---|---|---|
| ▣ 프로젝트 | PASS | /api/projects | shell_projects |
| ⚙ 설정 | NOT_IMPLEMENTED | None | UI_CONTROLS.json |
| ● | NOT_IMPLEMENTED | None | UI_CONTROLS.json |
| — | NOT_IMPLEMENTED | None | UI_CONTROLS.json |
| × | NOT_IMPLEMENTED | None | UI_CONTROLS.json |
| ⌂ 홈 | PASS | browser navigation/dialog | shell_home_title_owner_ui_lock |
| ◔ 작업 내역 | PASS | /api/evidence | shell_history |
| ▣ 저장소 | PASS | /api/projects | shell_storage |
| ▦ 템플릿 | NOT_IMPLEMENTED | None | UI_CONTROLS.json |
| ? 도움말 | PASS | browser navigation/dialog | shell_help |
| ＋ 영상 불러오기 | PASS | /api/media/import | video_import_ratio, video_tool_rotate |
| ✦ AI 자동 편집 | PASS | /api/jobs tracking | model_ui_dispatch_tracking, frozen_tracking_h264_playback |
| ✦ 광고 숏폼 NEW | DEFERRED_EXTERNAL | /api/integrations/marketing/shortform | external_unavailable_base_continues |
| ▣ 프로젝트 저장 | PASS | /api/projects/save | corrected_edits_save_close_reopen, save_full_close_reopen_all_lanes |
| ⇧ 내보내기 | PASS | /api/projects/{id}/export then /files | corrected_edits_ui_export_integrity, ui_export_download_crc_all_hashes, save_failure_prevents_stale_export |
| 영상 AI 지시 | PASS | /api/photo-edits /api/video-edits /api/jobs | video_command, unsupported_video_command_rejected, failed_command_retained_for_retry |
| ＋ 참고 이미지 추가 | NOT_IMPLEMENTED | None | UI_CONTROLS.json |
| 참고 이미지 | NOT_IMPLEMENTED | None | UI_CONTROLS.json |
| 스타일 | PASS | browser command/control focus; connected edit APIs | video_command_chips_send_length_ratio |
| 길이 | PASS | browser command/control focus; connected edit APIs | video_command_chips_send_length_ratio |
| 비율 | PASS | browser command/control focus; connected edit APIs | video_command_chips_send_length_ratio |
| ➤ | PASS | /api/photo-edits /api/video-edits /api/jobs | video_command, unsupported_video_command_rejected, failed_command_retained_for_retry |
| ◀ | PASS | HTMLMediaElement/fullscreen | video_play_pause_seek_mute_start_end |
| ▶ | PASS | HTMLMediaElement/fullscreen | video_play_pause_seek_mute_start_end |
| ▶/ | PASS | HTMLMediaElement/fullscreen | video_play_pause_seek_mute_start_end |
| 영상 재생 위치 | PASS | /files/... single-byte-range 206 | video_seek_byte_range |
| 🔊 | PASS | HTMLMediaElement/fullscreen | video_play_pause_seek_mute_start_end |
| ⛶ | PASS | HTMLMediaElement/fullscreen | data-video-fullscreen |
| 자르기 | PASS | /api/video-edits | video_tool_trim |
| 분할 | PASS | /api/video-edits | video_tool_split |
| 회전 | PASS | /api/video-edits | video_tool_rotate |
| 속도 | PASS | /api/video-edits | video_tool_speed |
| brightness | PASS | /api/video-edits | video_corrections_stabilize_denoise |
| contrast | PASS | /api/video-edits | video_corrections_stabilize_denoise |
| saturation | PASS | /api/video-edits | video_corrections_stabilize_denoise |
| checkbox | PASS | /api/video-edits | video_corrections_stabilize_denoise |
| checkbox | PASS | /api/video-edits | video_corrections_stabilize_denoise |
| start | PASS | /api/video-edits | video_tool_trim |
| duration | PASS | /api/video-edits | video_tool_trim |
| speed | PASS | /api/video-edits | video_tool_speed |
| volume | PASS | /api/video-edits | video_background_music, video_tool_speed |
| 숏폼 변환 | PASS | /api/video-edits | video_tool_shortform |
| 장면 전환 | PASS | /api/video-edits | video_tool_fade |
| AI 효과 | PASS | /api/video-edits | video_tool_effect |
| 자막 | PASS | /api/video-edits | video_korean_subtitle_render |
| 자동 자막 생성 | PASS | /api/jobs then /api/video-edits | model_ui_dispatch_transcribe, frozen_korean_stt_visible |
| 하이라이트 추출 | PASS | /api/video-edits | video_tool_highlight |
| 배경음악 추가 | PASS | /api/video-edits | video_background_music, background_music_state_after_followup_edit |
| text | PASS | /api/video-edits | video_korean_subtitle_render |
| 영상 편집 적용 | PASS | /api/video-edits | video_corrections_stabilize_denoise, video_tool_trim, video_tool_split, video_korean_subtitle_render |
| ＋ 사진 불러오기 | PASS | /api/media/import | photo_landscape_ratio, photo_portrait_auto_fit, invalid_import_keeps_previous |
| ✦ AI 이미지 생성 | NOT_IMPLEMENTED | None | UI_CONTROLS.json |
| ✦ AI 보정 | PASS | /api/photo-edits | photo_auto_entry_header, photo_auto_entry_transport |
| ▣ 프로젝트 저장 | PASS | /api/projects/save | corrected_edits_save_close_reopen, save_full_close_reopen_all_lanes |
| ⇧ 내보내기 | PASS | /api/projects/{id}/export then /files | corrected_edits_ui_export_integrity, ui_export_download_crc_all_hashes, save_failure_prevents_stale_export |
| 사진 AI 지시 | PASS | /api/photo-edits /api/video-edits /api/jobs | photo_command, photo_command_chips_style_tone_ratio_send |
| ＋ 참고 이미지 추가 | PASS | browser reference input | photo_reference_similarity, reference_remove |
| 참고 이미지 | PASS | browser command/control focus; connected edit APIs | photo_reference_similarity |
| 스타일 | PASS | browser command/control focus; connected edit APIs | photo_command_chips_style_tone_ratio_send |
| 톤 조정 | PASS | browser command/control focus; connected edit APIs | photo_command_chips_style_tone_ratio_send |
| 비율 | PASS | browser command/control focus; connected edit APIs | photo_command_chips_style_tone_ratio_send |
| ➤ | PASS | /api/photo-edits /api/video-edits /api/jobs | photo_command, photo_command_chips_style_tone_ratio_send |
| ✋ | NOT_IMPLEMENTED | None | UI_CONTROLS.json |
| ⛶ | PASS | HTMLMediaElement/fullscreen | data-photo-fullscreen |
| ↶ | NOT_IMPLEMENTED | None | UI_CONTROLS.json |
| ↷ | NOT_IMPLEMENTED | None | UI_CONTROLS.json |
| ✦ AI 보정 | PASS | /api/photo-edits | photo_auto_entry_header, photo_auto_entry_transport |
| 기본 보정 | PASS | native HTML details | UI_CONTROLS.json |
| 사진 밝기 | PASS | /api/photo-edits | photo_brightness |
| 사진 대비 | PASS | /api/photo-edits | photo_contrast |
| 사진 하이라이트 | PASS | /api/photo-edits | photo_highlights |
| 사진 그림자 | PASS | /api/photo-edits | photo_shadows |
| 사진 채도 | PASS | /api/photo-edits | photo_saturation |
| 사진 색온도 | PASS | /api/photo-edits | photo_temperature |
| 사진 선명도 | PASS | /api/photo-edits | photo_sharpness |
| 크롭 | PASS | /api/photo-edits | photo_tool_crop |
| 크기 조절 | PASS | /api/photo-edits | photo_tool_resize |
| 회전 | PASS | /api/photo-edits | photo_tool_rotate |
| 좌우 반전 | PASS | /api/photo-edits | photo_tool_flip-h |
| 상하 반전 | PASS | /api/photo-edits | photo_tool_flip-v |
| AI 보정 | PASS | /api/photo-edits | photo_tool_auto |
| 배경 제거 | PASS | /api/jobs or /api/jobs/{id}/background | photo_background_removal_from_frozen_mask, frozen_photo_segment |
| 색감 보정 | PASS | /api/photo-edits | photo_tool_color |
| 스타일 변환 | PASS | /api/photo-edits | photo_tool_style |
| 인물 보정 | PASS | /api/photo-edits | photo_tool_portrait |
| 해상도 향상 | PASS | /api/jobs | frozen_photo_upscale, model_ui_dispatch_upscale |
| 유사 이미지 검색 | PASS | browser histogram comparison | photo_reference_similarity |
| number | PASS | /api/photo-edits | photo_tool_crop |
| number | PASS | /api/photo-edits | photo_tool_crop |
| number | PASS | /api/photo-edits | photo_tool_crop |
| number | PASS | /api/photo-edits | photo_tool_crop |
| number | PASS | /api/photo-edits | photo_tool_resize |
| ↻ 초기화 | PASS | /api/photo-edits | photo_reset |
| 적용하기 | PASS | /api/photo-edits | photo_brightness, corrected_edits_save_close_reopen |
| Project create/open saved project | PASS | /api/projects; /api/projects/{UUID} | new_project_and_open_existing |
| Reference validation/removal | PASS | browser CommandPanelState | photo_reference_similarity, reference_remove, REGRESSION.log |
| Actual HTTP replay/conflict/failed retry | PASS | ProductHttpServer.run_once | http_idempotency, REGRESSION.log |
| Pending edit save and duplicate-click guard | PASS | browser edit counters | pending_edit_save_guard_duplicate_click |
| Background mask derivative | PASS | /api/jobs/{id}/background | photo_background_removal_from_frozen_mask |
| Full process/browser close and reopen | PASS | server shutdown/new server + project latest | full_browser_server_close, save_full_close_reopen_all_lanes, single_server_after_relaunch |
| Legacy local FFmpeg concat | PASS | process_video | legacy_concat_original_ratio, REGRESSION.log |
| Legacy local Pillow/OpenCV computation | PASS | MediaRuntime/process_photo | REGRESSION.log |
| Runtime identity | PASS | /api/runtime-identity | REGRESSION.log |
| Malformed/unsupported input | PASS | HTTP422 / visible UI status | invalid_import_keeps_previous, unsupported_video_command_rejected, REGRESSION.log |
| before-after comparison | NOT_IMPLEMENTED | not exposed | unimplemented_capability_declarations_corrected |
| batch editor | NOT_IMPLEMENTED | not exposed | unimplemented_capability_declarations_corrected |
| keyframe editing | NOT_IMPLEMENTED | not exposed | unimplemented_capability_declarations_corrected |
| clip context/range deletion | NOT_IMPLEMENTED | not exposed | unimplemented_capability_declarations_corrected |
| editable multi-track timeline | NOT_IMPLEMENTED | not exposed | unimplemented_capability_declarations_corrected |
| real Marketing HTTP | DEFERRED_EXTERNAL | external Marketing bridge | external_unavailable_base_continues |
| approved AVORA assets | DEFERRED_EXTERNAL | external Marketing bridge | external_unavailable_base_continues |
| external ad 9:16 Preview | DEFERRED_EXTERNAL | external Marketing bridge | external_unavailable_base_continues |
| Representative Approval | DEFERRED_EXTERNAL | external Marketing bridge | external_unavailable_base_continues |
| approved ad MP4 Export | DEFERRED_EXTERNAL | external Marketing bridge | external_unavailable_base_continues |
| One-click Windows launch/update/native close/relaunch | PARTIAL | future ONE_CLICK_RUNTIME_PACKAGE | REGRESSION.log |
