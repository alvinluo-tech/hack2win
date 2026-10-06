# ui-shot.ps1 — 视觉验收循环的截图工具(桌面+窄屏,多轮对比用)
# 用法: powershell -File ui-shot.ps1 -Url "http://localhost:3000" -OutDir ..\iterations\round-1 -Tag home [-ExpectText "产品名或必现文本"]
# 产物: <OutDir>\<Tag>-desktop.png / <Tag>-mobile.png
# 防假阳性: -ExpectText 指定页面必须包含的文本(产品名/标题),先 dump-dom 校验再截图;
#          无浏览器错误页特征检查(ERR_CONNECTION_CLOSED/无法访问此网站 命中即 FAIL)
# 依赖: 本机 Chrome 或 Edge(自动探测)
param(
    [Parameter(Mandatory=$true)][string]$Url,
    [Parameter(Mandatory=$true)][string]$OutDir,
    [string]$Tag = "shot",
    [string]$Sizes = "1440,900;390,844",
    [int]$WaitMs = 8000,
    [string]$ExpectText = ""
)
$ErrorActionPreference = "SilentlyContinue"
$candidates = @(
    "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
    "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
    "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe",
    "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe",
    "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe"
)
$browser = $candidates | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $browser) { Write-Host "[FAIL] 未找到 Chrome/Edge"; exit 1 }
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

# 步骤1: 内容预检(dump-dom)——防"成功截图了错误页"
$domFile = Join-Path $OutDir "_dom_check.html"
& $browser --headless=new --disable-gpu --virtual-time-budget=$WaitMs --dump-dom $Url 2>$null | Out-File -FilePath $domFile -Encoding UTF8
$dom = Get-Content $domFile -Raw -ErrorAction SilentlyContinue
$errPage = ($dom -match "ERR_(CONNECTION|NAME|INTERNET)|无法访问此网站|This site can")
if ($errPage) { Write-Host "[FAIL] 页面是浏览器错误页(网络/服务未起?)——不要用这张图做视觉验收"; exit 1 }
if ($ExpectText -ne "") {
    if (-not $dom -or -not $dom.Contains($ExpectText)) {
        Write-Host ("[FAIL] 页面 DOM 未包含预期文本 '{0}'——白屏/加载未完成/内容错误,截图无意义" -f $ExpectText); exit 1
    }
    Write-Host ("[PASS] 内容预检: 包含 '{0}'" -f $ExpectText)
} else {
    Write-Host "[WARN] 未指定 -ExpectText,跳过内容断言(建议永远带上产品名)"
}

# 步骤2: 截图
$ok = 0; $total = ($Sizes -split ';').Count
foreach ($size in $Sizes -split ';') {
    $dim = $size.Trim() -split ','
    $w = $dim[0]; $h = $dim[1]
    $label = if ([int]$w -le 500) { "mobile" } else { "desktop" }
    $out = Join-Path $OutDir ("{0}-{1}.png" -f $Tag, $label)
    $tmpProfile = Join-Path $env:TEMP ("uishot_" + [guid]::NewGuid().ToString("N"))
    & $browser --headless=new --disable-gpu --hide-scrollbars --user-data-dir="$tmpProfile" --window-size=$w,$h --virtual-time-budget=$WaitMs --screenshot="$out" $Url 2>$null | Out-Null
    if ((Test-Path $out) -and ((Get-Item $out).Length -gt 3KB)) {
        Write-Host ("[PASS] {0} ({1}x{2}) -> {3} [{4}KB]" -f $label, $w, $h, $out, [math]::Round((Get-Item $out).Length/1KB))
        $ok++
    } else {
        Start-Sleep -Milliseconds 1200
        & $browser --headless=new --disable-gpu --hide-scrollbars --user-data-dir="$tmpProfile-r" --window-size=$w,$h --virtual-time-budget=($WaitMs*2) --screenshot="$out" $Url 2>$null | Out-Null
        if ((Test-Path $out) -and ((Get-Item $out).Length -gt 3KB)) { Write-Host ("[PASS-RETRY] {0} -> {1}" -f $label, $out); $ok++ }
        else { Write-Host ("[FAIL] {0} 截图失败(含重试)" -f $label) }
    }
}
if ($ok -lt $total) { exit 1 }
Write-Host ("=== {0}/{1} 张完成。视觉环三问: 1)与竞品并排像获奖作品吗 2)第一眼最丑的三处 3)信息设计过关吗 ===" -f $ok, $total)

