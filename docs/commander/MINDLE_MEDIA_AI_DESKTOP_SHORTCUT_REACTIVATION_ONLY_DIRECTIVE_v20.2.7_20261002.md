# MINDLE MEDIA AI — DESKTOP SHORTCUT REACTIVATION ONLY DIRECTIVE v20.2.7

Date: 2026-10-02
Status: ACTIVE
Repository: ADAMBUILD-ai/mindle-media-ai
Branch: feature/ad-shortform-bridge-p0-20260926
Epoch: MEDIA-AI-20261002-V20.2.7

## 1. 절대 금지
현재 작업 폴더 UI는 정상이다.
다음 파일/영역은 수정하지 말 것:
- ui/approved_visual.css
- ui/index.html
- VIDEO / PHOTO 레이아웃
- 색상
- 브랜드 아이콘 디자인
- Shortform 기능

## 2. 이번 작업 목적
바탕화면의 "MINDLE MEDIA AI - 최종 UI" 아이콘이 현재 활성화되지 않는다.
기존 깨진 바로가기를 삭제하고 새 바로가기를 다시 만든다.

## 3. 바탕화면 바로가기 재생성
Windows 실제 사용자 Desktop 경로를 확인한 뒤:

Shortcut name:
MINDLE MEDIA AI - 최종 UI.lnk

TargetPath:
powershell.exe

Arguments:
-ExecutionPolicy Bypass -File "<CURRENT_REPO_ROOT>\scripts\launch_media_ai_windows.ps1"

WorkingDirectory:
<CURRENT_REPO_ROOT>

IconLocation:
<CURRENT_REPO_ROOT>\ui\assets\brand\MINDLE_MEDIA_AI_APP_ICON.ico,0

중요:
- Repository 경로를 실제 현재 작업 폴더에서 얻을 것
- 옛 worktree 경로 금지
- localhost URL 직접 지정 금지
- 별도 UI 복사본 금지

## 4. 활성화 확인
새 바로가기 생성 후 반드시 실제로 더블클릭한다.

PASS 조건:
1. 바로가기 아이콘이 정상 표시된다.
2. 더블클릭이 먹는다.
3. scripts/launch_media_ai_windows.ps1가 실행된다.
4. 현재 작업 폴더의 MEDIA AI가 열린다.
5. 브라우저가 최대화된다.
6. 작업 폴더에서 정상으로 확인한 동일 UI가 뜬다.
7. UI 파일은 전혀 수정되지 않는다.

## 5. 실패 시
아이콘이 클릭되지 않거나 아무 반응이 없으면:
- .lnk TargetPath
- Arguments
- WorkingDirectory
- PowerShell 실행 정책/경로
- launcher script 존재 여부
- Windows Shortcut COM 생성 결과
를 확인하고 바로가지만 재생성한다.

UI를 수정해서 해결하려 하지 말 것.

## 6. 검수자료
Review:
docs/commander/MINDLE_MEDIA_AI_DESKTOP_SHORTCUT_REACTIVATION_REVIEW_v20.2.7_20261002.md

Evidence:
evidence/pc_remote/MINDLE_MEDIA_AI_DESKTOP_SHORTCUT_REACTIVATION_EVIDENCE_v20_2_7_20261002.json

필수 기록:
- 기존 shortcut 상태
- 새 shortcut TargetPath / Arguments / WorkingDirectory / IconLocation
- 실제 더블클릭 실행 결과
- 실행된 repo root / branch / HEAD
- UI 수정 여부 = false

## 최종 기준
작업 폴더 UI는 건드리지 말고,
바탕화면 바로가기만 다시 살아나게 만들어
현재 작업 폴더를 그대로 열게 하라.
