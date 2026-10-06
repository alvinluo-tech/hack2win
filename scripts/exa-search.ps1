# exa-search.ps1 — Exa 全网语义搜索封装(规避 PowerShell 引号/JSON 转义坑)
# 用法: .\exa-search.ps1 -Query "AI agent hackathon 2026" [-NumResults 6] [-OutFile out.txt]
# 依赖: mcporter + exa 配置 (mcporter config add exa https://mcp.exa.ai/mcp --scope home)
param(
    [Parameter(Mandatory=$true)][string]$Query,
    [int]$NumResults = 6,
    [string]$OutFile = ""
)
$raw = mcporter call exa.web_search_exa query="$Query" numResults=$NumResults 2>&1 | Out-String
if ($OutFile -ne "") {
    $raw | Out-File -FilePath $OutFile -Encoding UTF8
    Write-Host "saved $((Get-Item $OutFile).Length) bytes -> $OutFile"
} else {
    $raw
}
