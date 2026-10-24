# MINDLE MEDIA AI — WINDOWS SANDBOX ACL STATE RECOVERY DIRECTIVE v1.1

Date: 2026-10-06
Status: ACTIVE — HOST RECOVERY ONLY
Repository: ADAMBUILD-ai/mindle-media-ai
Canonical branch: feature/ad-shortform-bridge-p0-20260926
CONTROL_PLANE_EPOCH: MEDIA-AI-20261006-WINDOWS-SANDBOX-ACL-RECOVERY-V1.1

## 0. Commander finding

The repeated error:

`helper_unknown_error: apply deny-read ACLs`

has been reproduced outside the repository and before command execution.

This exact failure is also reported in openai/codex Windows sandbox issues, including:
- #42958
- #28248
- #47950

A documented recurrent signature is a malformed persisted sandbox state file:
`%USERPROFILE%\.codex\.sandbox\deny_read_acl_state.json`

Known malformed signature:
- file size = 22 bytes
- every byte = 0x00
- sandbox log contains `parse deny-read ACL state`
- parser error such as `expected value at line 1 column 1`

This is a host sandbox-state recovery cycle, NOT product work.

## 1. Critical safety rule

Do NOT:
- reset repository ACLs
- run icacls against the product repo
- clone/copy the repo
- create another worktree
- modify product files
- build employee package
- disable Windows security
- broadly delete the .codex directory

Only inspect the persisted sandbox ACL state and related sandbox logs.

## 2. Why Work cannot self-repair

Normal PC Work / sandboxed exec cannot perform this diagnostic because process creation fails before the requested command runs.

Therefore the sandbox-state inspection must be performed from an ordinary Windows host PowerShell opened by the user, outside PC Work.

This is the only manual host action allowed in this recovery cycle.

## 3. Host diagnostic — read only first

Open ordinary Windows PowerShell (NOT inside PC Work).

Run the following exact block:

```powershell
$ErrorActionPreference = 'Stop'

$candidates = @(
  (Join-Path $env:USERPROFILE '.codex\.sandbox'),
  (Join-Path $env:USERPROFILE '.codex.sandbox')
) | Select-Object -Unique

$found = @()

foreach ($dir in $candidates) {
  if (-not (Test-Path -LiteralPath $dir)) { continue }

  $state = Join-Path $dir 'deny_read_acl_state.json'
  $setup = Join-Path $dir 'setup_error.json'

  Write-Host "=== SANDBOX DIR ==="
  Write-Host $dir

  if (Test-Path -LiteralPath $state) {
    $bytes = [System.IO.File]::ReadAllBytes($state)
    $allNull = ($bytes.Length -gt 0 -and (@($bytes | Where-Object { $_ -ne 0 }).Count -eq 0))
    $text = [System.Text.Encoding]::UTF8.GetString($bytes)
    $jsonValid = $false
    try {
      $null = $text | ConvertFrom-Json
      $jsonValid = $true
    } catch {}

    [pscustomobject]@{
      StatePath = $state
      Length = $bytes.Length
      AllNull = $allNull
      JsonValid = $jsonValid
      TextPreview = if ($allNull) { '<ALL_NUL_BYTES>' } else { $text }
    } | Format-List

    $found += [pscustomobject]@{
      Dir = $dir
      State = $state
      Length = $bytes.Length
      AllNull = $allNull
      JsonValid = $jsonValid
    }
  } else {
    Write-Host "deny_read_acl_state.json: NOT FOUND"
  }

  if (Test-Path -LiteralPath $setup) {
    Write-Host "=== setup_error.json ==="
    Get-Content -LiteralPath $setup -Raw
  }

  Write-Host "=== recent sandbox logs ==="
  Get-ChildItem -LiteralPath $dir -File -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -like '*sandbox*.log' -or $_.Name -like '*.log' } |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 5 FullName,Length,LastWriteTime
}

Write-Host "=== SUMMARY ==="
$found | Format-Table -AutoSize
```

## 4. Decision gate

### Case A — exact malformed signature

If ANY discovered `deny_read_acl_state.json` has:
- Length = 22
- AllNull = True
- JsonValid = False

then perform the controlled recovery in Section 5.

### Case B — malformed but not exact 22-byte signature

If:
- JsonValid = False
- but the exact 22-byte all-NUL signature is not present

STOP.

Do not delete or rename automatically.
Report:
`ACL_STATE_MALFORMED_NONCANONICAL`

### Case C — valid JSON

If:
- JsonValid = True

STOP.

Do not rename it.
Report:
`ACL_STATE_VALID_JSON_DIFFERENT_DEFECT`

The known NUL-state workaround does not apply.

### Case D — state file missing

STOP.
Report:
`ACL_STATE_FILE_NOT_FOUND`

## 5. Controlled recovery — ONLY Case A

Fully exit ChatGPT/Codex desktop applications first.

Then in ordinary host PowerShell run:

```powershell
$ErrorActionPreference = 'Stop'

$candidates = @(
  (Join-Path $env:USERPROFILE '.codex\.sandbox'),
  (Join-Path $env:USERPROFILE '.codex.sandbox')
) | Select-Object -Unique

$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'

foreach ($dir in $candidates) {
  $state = Join-Path $dir 'deny_read_acl_state.json'
  if (-not (Test-Path -LiteralPath $state)) { continue }

  $bytes = [System.IO.File]::ReadAllBytes($state)
  $allNull = ($bytes.Length -gt 0 -and (@($bytes | Where-Object { $_ -ne 0 }).Count -eq 0))
  $text = [System.Text.Encoding]::UTF8.GetString($bytes)
  $jsonValid = $false
  try {
    $null = $text | ConvertFrom-Json
    $jsonValid = $true
  } catch {}

  if ($bytes.Length -eq 22 -and $allNull -and -not $jsonValid) {
    $backup = Join-Path $dir ("deny_read_acl_state.corrupt-backup.$stamp.json")
    Move-Item -LiteralPath $state -Destination $backup
    Write-Host "BACKED_UP=$backup"
  } else {
    Write-Host "SKIP_NONMATCH=$state"
  }
}
```

Do NOT create a replacement file manually.

Restart ChatGPT/Codex normally and allow the sandbox to regenerate its own state.

## 6. Post-recovery verification

After restart, inspect the state file again from ordinary host PowerShell.

Expected regenerated content may be valid JSON such as:
`{"principals":{}}`

Then open a NEW PC Work session and run only the neutral probe:

- use `C:\MINDLE_WORK_TEST`
- create `acl_probe.txt`
- write `MINDLE_PC_WORK_ACL_PROBE_PASS`
- read it back

Required:
`HOST_SANDBOX_ACL_RECOVERY_PASS`

If the same `apply deny-read ACLs` error remains despite valid regenerated state:
`ACL_STATE_REGENERATED_BUT_SANDBOX_STILL_BLOCKED`

## 7. Repository gate

Only after `HOST_SANDBOX_ACL_RECOVERY_PASS`:

1. read canonical repo only
2. confirm branch `feature/ad-shortform-bridge-p0-20260926`
3. read CURRENT authority files
4. run control-plane validator
5. produce `RECOVERY_PASS`

Do not build the employee package in this cycle.

## 8. Required Evidence

Human Review:
`docs/commander/MINDLE_MEDIA_AI_WINDOWS_SANDBOX_ACL_RECOVERY_REVIEW_v1.1_20261006.md`

Machine Evidence:
`evidence/pc_remote/MINDLE_MEDIA_AI_WINDOWS_SANDBOX_ACL_RECOVERY_EVIDENCE_v1_1_20261006.json`

Detail:
`evidence/pc_remote/media-ai-windows-sandbox-acl-recovery-v1_1-20261006/`

Required:
- HOST_STATE_INSPECTION.txt
- HOST_STATE_CLASSIFICATION.json
- HOST_STATE_BACKUP.txt if Case A
- POST_RESTART_STATE_INSPECTION.txt
- ENV_NEUTRAL_EXEC_PROBE.txt
- CANONICAL_REPO_READONLY_PROBE.txt
- CONTROL_PLANE_VALIDATOR.txt
- EXACT_FAILURE.txt if blocked

## 9. Result vocabulary

PASS:
- HOST_SANDBOX_ACL_RECOVERY_PASS
- RECOVERY_PASS

BLOCKED/DIAGNOSTIC:
- ACL_STATE_MALFORMED_NONCANONICAL
- ACL_STATE_VALID_JSON_DIFFERENT_DEFECT
- ACL_STATE_FILE_NOT_FOUND
- ACL_STATE_REGENERATED_BUT_SANDBOX_STILL_BLOCKED
- WORK_ENVIRONMENT_ACL_HELPER_BLOCKED

## 10. Employee package status

Employee package work remains SUSPENDED / REFERENCE_ONLY.

It may be reactivated only by a new commander action after RECOVERY_PASS.

## Final command

DO NOT REPEAT BLIND WORK RESTARTS. CLASSIFY THE PERSISTED WINDOWS SANDBOX ACL STATE FIRST. APPLY THE BACKUP-AND-REGENERATE RECOVERY ONLY TO THE EXACT MALFORMED 22-BYTE ALL-NUL SIGNATURE. THEN VERIFY THE SANDBOX WITH A NEUTRAL EXEC PROBE BEFORE TOUCHING THE PRODUCT.
