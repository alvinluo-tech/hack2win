# hack2win multi-agent installer (Windows PowerShell)
# Usage:
#   powershell -ExecutionPolicy Bypass -File install.ps1              # global install (auto-detect agents)
#   powershell -ExecutionPolicy Bypass -File install.ps1 -ProjectDir # wire rules into the CURRENT project
#   powershell -ExecutionPolicy Bypass -File install.ps1 -Uninstall   # remove everything this script created
param(
  [switch]$ProjectDir,
  [switch]$Uninstall
)

$ErrorActionPreference = "Stop"
if (-not ("stdout".Length -ge 0)) {} # noop guard for strict shells
try { if ($host.UI.RawUI) { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } } catch {}

$Src      = $PSScriptRoot
$Skill    = "hack2win"
$MarkB    = "# >>> hack2win >>>"
$MarkE    = "# <<< hack2win <<<"
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

function Copy-Skill([string]$SkillsRoot) {
  $dest = Join-Path $SkillsRoot $Skill
  New-Item -ItemType Directory -Force -Path $dest | Out-Null
  Get-ChildItem -LiteralPath $Src -Force |
    Where-Object { $_.Name -ne ".git" -and $_.Name -ne "install.ps1" -and $_.Name -ne "install.sh" } |
    ForEach-Object { Copy-Item -LiteralPath $_.FullName -Destination $dest -Recurse -Force }
  Write-Host "  [ok] $dest"
}

function Remove-ManagedDir([string]$SkillDir) {
  if (Test-Path (Join-Path $SkillDir "SKILL.md")) {
    Remove-Item -LiteralPath $SkillDir -Recurse -Force
    Write-Host "  [removed] $SkillDir"
  }
}

function Strip-Block([string]$File) {
  if (-not (Test-Path $File)) { return }
  $lines = [System.IO.File]::ReadAllLines($File)
  if ($lines -notcontains $MarkB) { return }
  $out = New-Object System.Collections.Generic.List[string]
  $inBlock = $false
  foreach ($l in $lines) {
    if ($l -eq $MarkB) { $inBlock = $true; continue }
    if ($l -eq $MarkE) { $inBlock = $false; continue }
    if (-not $inBlock) { $out.Add($l) }
  }
  [System.IO.File]::WriteAllLines($File, $out, $Utf8NoBom)
  Write-Host "  [cleaned] $File"
}

function Append-Block([string]$File) {
  if ((Test-Path $File) -and ((Get-Content $File -Raw -ErrorAction SilentlyContinue) -match [regex]::Escape($MarkB))) {
    Write-Host "  [skip] $File (already wired)"; return
  }
  $dir = Split-Path -Parent $File; New-Item -ItemType Directory -Force -Path $dir | Out-Null
  $block = [System.IO.File]::ReadAllText((Join-Path $Src "adapters\codex-AGENTS-block.md"))
  $newText = if (Test-Path $File) { (Get-Content $File -Raw) + "`r`n" + $MarkB + "`r`n" + $block + "`r`n" + $MarkE + "`r`n" }
             else { $MarkB + "`r`n" + $block + "`r`n" + $MarkE + "`r`n" }
  [System.IO.File]::WriteAllText($File, $newText, $Utf8NoBom)
  Write-Host "  [wired] $File"
}

Write-Host "hack2win installer — mode: $(if ($Uninstall) {'uninstall'} elseif ($ProjectDir) {'global + project'} else {'global'})"

$Targets = @(
  @{ Root = Join-Path $HOME ".agents\skills";          Always = $true  ; DetectParent = $false },
  @{ Root = Join-Path $HOME ".claude\skills";          Always = $false; DetectParent = $false },
  @{ Root = Join-Path $HOME ".codex\skills";           Always = $false; DetectParent = $false },
  @{ Root = Join-Path $HOME ".zcode\skills";           Always = $false; DetectParent = $false },
  @{ Root = Join-Path $HOME ".config\opencode\skill";  Always = $false; DetectParent = $true  }
)

function Test-AgentRoot($t) {
  if ($t.DetectParent) { return (Test-Path (Split-Path $t.Root -Parent)) }
  return (Test-Path $t.Root)
}

if ($Uninstall) {
  Write-Host "Uninstalling:"
  foreach ($t in $Targets) {
    if ($t.Always -or (Test-AgentRoot $t)) { Remove-ManagedDir (Join-Path $t.Root $Skill) }
  }
  Strip-Block (Join-Path $HOME ".codex\AGENTS.md")
  Remove-Item (Join-Path $HOME ".codex\prompts\$Skill.md") -Force -ErrorAction SilentlyContinue
  Write-Host "Done. (project rules, if any: remove .cursor/rules/hack2win.mdc, .windsurf/rules/hack2win.md, AGENTS.md, and the marked block in .github/copilot-instructions.md)"
  exit 0
}

Write-Host "Global install (canonical ~/.agents + detected agents):"
foreach ($t in $Targets) {
  if ($t.Always) {
    Write-Host "canonical skill home:"; Copy-Skill $t.Root
  } elseif (Test-AgentRoot $t) {
    # report the agent by walking one level up from its skills/skill root
    $label = Split-Path (Split-Path $t.Root -Parent) -Leaf
    Write-Host "$label detected:"; Copy-Skill $t.Root
  }
}

# Codex: managed block in AGENTS.md + /hack2win prompt
if (Test-Path (Join-Path $HOME ".codex")) {
  Append-Block (Join-Path $HOME ".codex\AGENTS.md")
  $prompts = Join-Path $HOME ".codex\prompts"; New-Item -ItemType Directory -Force -Path $prompts | Out-Null
  Copy-Item (Join-Path $Src "adapters\codex-AGENTS-block.md") (Join-Path $prompts "$Skill.md") -Force
  Write-Host "  [wired] $prompts\$Skill.md (use: /$Skill)"
}

if ($ProjectDir) {
  $P = (Get-Location).Path
  Write-Host "Project wiring in: $P"
  Copy-Item (Join-Path $Src "AGENTS.md") (Join-Path $P "AGENTS.md") -Force
  Write-Host "  [wired] AGENTS.md (Codex & agents.md tools)"
  New-Item -ItemType Directory -Force -Path (Join-Path $P ".cursor\rules") | Out-Null
  Copy-Item (Join-Path $Src "adapters\cursor.mdc") (Join-Path $P ".cursor\rules\$Skill.mdc") -Force
  Write-Host "  [wired] .cursor\rules\$Skill.mdc"
  New-Item -ItemType Directory -Force -Path (Join-Path $P ".windsurf\rules") | Out-Null
  Copy-Item (Join-Path $Src "adapters\windsurf.md") (Join-Path $P ".windsurf\rules\$Skill.md") -Force
  Write-Host "  [wired] .windsurf\rules\$Skill.md"
  New-Item -ItemType Directory -Force -Path (Join-Path $P ".github") | Out-Null
  $copilot = Join-Path $P ".github\copilot-instructions.md"
  if ((Test-Path $copilot) -and ((Get-Content $copilot -Raw -ErrorAction SilentlyContinue) -match [regex]::Escape($MarkB))) {
    Write-Host "  [skip] $copilot (already wired)"
  } else {
    $block = [System.IO.File]::ReadAllText((Join-Path $Src "adapters\copilot.md"))
    $newText = if (Test-Path $copilot) { (Get-Content $copilot -Raw) + "`r`n" + $MarkB + "`r`n" + $block + "`r`n" + $MarkE + "`r`n" }
               else { $MarkB + "`r`n" + $block + "`r`n" + $MarkE + "`r`n" }
    [System.IO.File]::WriteAllText($copilot, $newText, $Utf8NoBom)
    Write-Host "  [wired] $copilot"
  }
}

Write-Host "Verify: python `"$HOME\.agents\skills\$Skill\scripts\list_skills.py`""
Write-Host "Done."
