# list-skills.ps1 — 本机技能盘点 + hack2win 编排注册表核对
# 用法: powershell -File list-skills.ps1
# 输出: 已装技能清单 / 注册表技能的存在状态 / 缺失清单(含安装提示)

$agentsDir = Join-Path $env:USERPROFILE ".agents\skills"
$zcodeDir  = Join-Path $env:USERPROFILE ".zcode\skills"

$installed = @()
foreach ($dir in @($agentsDir, $zcodeDir)) {
    if (Test-Path $dir) {
        Get-ChildItem $dir -Directory | ForEach-Object {
            $skillMd = Join-Path $_.FullName "SKILL.md"
            $installed += [pscustomobject]@{ Name = $_.Name; Dir = $dir; HasSkillMd = (Test-Path $skillMd) }
        }
    }
}
$installed = $installed | Sort-Object Name -Unique
Write-Host ("=== 本机已装技能: " + $installed.Count + " 个 ===")
$installed | ForEach-Object { $m = if ($_.HasSkillMd) { "" } else { "  [警告] 缺 SKILL.md" }; Write-Host ("  " + $_.Name + $m) }

# hack2win 编排注册表(与 references/10-orchestration.md 保持同步)
$registry = @(
    @{ name = "find-skills";                  use = "技能发现与安装" },
    @{ name = "research";                     use = "P0-P2 系统调研" },
    @{ name = "domain-modeling";              use = "P3 领域建模/ADR" },
    @{ name = "codebase-design";              use = "P4 架构边界设计与接缝" },
    @{ name = "setup-ts-deep-modules";        use = "P4 TS深模块依赖隔离 (dependency-cruiser)" },
    @{ name = "improve-codebase-architecture";use = "P4 架构体检与重构" },
    @{ name = "nextjs-supabase-auth";         use = "P4 认证集成(可选)" },
    @{ name = "tauri";                        use = "P4 跨平台桌面交付" },
    @{ name = "tauri-development";            use = "P4 桌面端开发与调试" },
    @{ name = "design-taste-frontend";        use = "P5 UI 打磨(主引用)" },
    @{ name = "tdd";                          use = "P4 核心模块测试先行" },
    @{ name = "typescript-e2e-testing";       use = "P4 TS 集成/E2E(可选)" },
    @{ name = "ai-regression-testing";        use = "P4 AI 功能回归(可选)" },
    @{ name = "setup-pre-commit";             use = "P4 质量闸" },
    @{ name = "code-review";                  use = "P6 提交前评审" },
    @{ name = "diagnosing-bugs";              use = "紧急排障" },
    @{ name = "skill-creator";                use = "现场造最小技能(插件)" }
)
Write-Host ""
Write-Host "=== 编排注册表核对 ==="
$missing = @()
foreach ($r in $registry) {
    $hit = $installed | Where-Object { $_.Name -eq $r.name -and $_.HasSkillMd }
    $inPlugin = Test-Path (Join-Path $env:USERPROFILE ".zcode\cli\plugins\cache\zcode-plugins-official\skill-creator\0.1.0\skills\skill-creator\SKILL.md")
    $ok = ($null -ne $hit) -or ($r.name -eq "skill-creator" -and $inPlugin)
    if (-not $ok) { $missing += $r.name }
    $tag = if ($ok) { "OK  " } else { "MISS" }
    Write-Host ("  [$tag] " + $r.name.PadRight(32) + $r.use)
}
Write-Host ""
if ($missing.Count -gt 0) {
    Write-Host ("缺失 " + $missing.Count + " 个: " + ($missing -join ", "))
    Write-Host "安装方式见 references/10-orchestration.md §3(GitHub 走 gh-proxy 镜像;不可达时用 skill-creator 现场造最小技能)"
} else {
    Write-Host "注册表技能全部就绪,编排链可用。"
}
