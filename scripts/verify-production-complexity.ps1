# verify-production-complexity.ps1 — 生产级系统复杂度与规模硬性审计工具
# 用法: powershell -File verify-production-complexity.ps1 -ProjectPath <项目根目录> [-MinLOC 3000] [-MinTables 8] [-MinEndpoints 16] [-MinComponents 15]
# 目的: 机械化阻断"几百行代码/单表/单页面"的玩具 Demo, 强制系统达到工业级复杂度与工程完备度
param(
    [Parameter(Mandatory=$true)][string]$ProjectPath,
    [int]$MinLOC = 3000,
    [int]$MinTables = 8,
    [int]$MinEndpoints = 16,
    [int]$MinComponents = 15
)

$ErrorActionPreference = "SilentlyContinue"
$script:pass = 0; $script:fail = 0; $script:warn = 0

function Report($name, $ok, $hard, $detail) {
    $tag = if ($ok) { $script:pass++; "PASS" } elseif ($hard) { $script:fail++; "FAIL" } else { $script:warn++; "WARN" }
    Write-Host ("[{0}] {1} -- {2}" -f $tag, $name, $detail)
}

Write-Host "================================================================="
Write-Host "   hack2win 生产级系统复杂度与规模审计: $ProjectPath"
Write-Host "================================================================="

if (-not (Test-Path $ProjectPath)) {
    Write-Host "[FAIL] 项目根目录不存在: $ProjectPath"
    exit 1
}

$fe = Join-Path $ProjectPath "frontend"
$be = Join-Path $ProjectPath "backend"

# 1. 统计有效核心源码行数 (LOC, 排除 node_modules, .next, venv, cache)
$excludePattern = "node_modules|\.next|venv|\.venv|__pycache__|\.git|dist|build|coverage"
$srcFiles = Get-ChildItem -Path $ProjectPath -Recurse -File | Where-Object {
    $_.FullName -notmatch $excludePattern -and
    $_.Extension -match "\.(ts|tsx|js|jsx|py|sql|css|html)$" -and
    $_.Name -notmatch "package-lock\.json|yarn\.lock|pnpm-lock\.yaml"
}

$totalLOC = 0
$feLOC = 0
$beLOC = 0

foreach ($file in $srcFiles) {
    $lines = (Get-Content $file.FullName -ErrorAction SilentlyContinue | Measure-Object -Line).Lines
    $totalLOC += $lines
    if ($file.FullName.StartsWith($fe)) { $feLOC += $lines }
    elseif ($file.FullName.StartsWith($be)) { $beLOC += $lines }
}

$locOk = ($totalLOC -ge $MinLOC)
$locHard = ($totalLOC -lt 1500) # 低于 1500 行直接判定为低级玩具
Report "有效核心源码量 (LOC)" $locOk $locHard ("总行数: {0} (前端: {1}, 后端: {2}, 最低门槛: {3})" -f $totalLOC, $feLOC, $beLOC, $MinLOC)

# 2. 统计数据库实体模型类数量 (SQLAlchemy ORM)
$modelFiles = Get-ChildItem -Path (Join-Path $be "app\models") -Recurse -Filter "*.py" -File -ErrorAction SilentlyContinue
$tableCount = 0
if ($modelFiles) {
    foreach ($mf in $modelFiles) {
        $hits = (Select-String -Path $mf.FullName -Pattern "__tablename__\s*=|class\s+\w+\(.*Base.*\):" -ErrorAction SilentlyContinue | Measure-Object).Count
        $tableCount += $hits
    }
}
$tableOk = ($tableCount -ge $MinTables)
Report "数据库关系实体表数量" $tableOk $true ("检测到表/实体: {0} 个 (最低要求: {1} 张规范表)" -f $tableCount, $MinTables)

# 3. 统计 API 路由端点总数
# v9.1 修正: 匹配任意路由变量名(@router/@app/@api_v1/@runs_router...), 修复"命名 router 漏计导致端点数被低估"缺陷(R11 实测 28 vs 真实 38)
$apiFiles = Get-ChildItem -Path (Join-Path $be "app") -Recurse -Filter "*.py" -File -ErrorAction SilentlyContinue
$endpointCount = 0
if ($apiFiles) {
    foreach ($af in $apiFiles) {
        $hits = (Select-String -Path $af.FullName -Pattern "@\w+\.(get|post|put|delete|patch|options|head)\(" -ErrorAction SilentlyContinue | Measure-Object).Count
        $endpointCount += $hits
    }
}
$endpointOk = ($endpointCount -ge $MinEndpoints)
Report "API 业务路由端点数量" $endpointOk $true ("检测到端点: {0} 个 (最低要求: {1} 个端点)" -f $endpointCount, $MinEndpoints)

# 4. 统计前端独立组件数量
$compFiles = Get-ChildItem -Path (Join-Path $fe "components") -Recurse -File -ErrorAction SilentlyContinue | Where-Object {
    $_.Extension -match "\.(tsx|jsx)$"
}
$compCount = if ($compFiles) { ($compFiles | Measure-Object).Count } else { 0 }
$compOk = ($compCount -ge $MinComponents)
Report "前端独立业务组件数量" $compOk $true ("检测到组件: {0} 个 (最低要求: {1} 个)" -f $compCount, $MinComponents)

# 5. 检测异步后台任务队列 / Worker 支持
$workerFiles = Get-ChildItem -Path $be -Recurse -File -ErrorAction SilentlyContinue | Where-Object {
    $_.Name -match "worker|celery|arq|tasks\.py|background" -or $_.FullName -match "workers"
}
$hasWorker = ($null -ne $workerFiles -and ($workerFiles | Measure-Object).Count -gt 0)
Report "异步任务处理 / Worker 队列" $hasWorker $false ("后台队列模块: {0}" -f $(if ($hasWorker) { "已具备" } else { "缺失(耗时操作应解耦为异步)" }))

# 6. 检测 Docker Compose 多服务集群
# v9.1 修正: 旧正则会把 volumes/networks 等顶层键误计为服务(R11 实测 7 vs 真实 5);
# 新逻辑: 仅统计声明了 image: 或 build: 的服务条目
$composeFile = Join-Path $ProjectPath "docker-compose.yml"
$composeOk = $false
$serviceCount = 0
if (Test-Path $composeFile) {
    $composeRaw = Get-Content $composeFile -Raw -ErrorAction SilentlyContinue
    $serviceBlocks = [regex]::Matches($composeRaw, "(?ms)^\s{2}[a-zA-Z0-9_\-]+:\s*\r?\n(?:\s{4}.+\r?\n)*?\s{4}(image|build):")
    $serviceCount = ($serviceBlocks | Measure-Object).Count
    $composeOk = ($serviceCount -ge 2)
}
Report "Docker Compose 集群编排" $composeOk $false ("编排服务数(含 image/build): {0} (推荐包含 app, db, redis 等)" -f $serviceCount)

# 7. 检测数据库版本迁移脚本 (Alembic)
$alembicVersions = Get-ChildItem -Path (Join-Path $be "alembic\versions") -Filter "*.py" -File -ErrorAction SilentlyContinue
$hasMigrations = ($null -ne $alembicVersions -and ($alembicVersions | Measure-Object).Count -gt 0)
Report "Alembic 数据库迁移版本链" $hasMigrations $true ("版本脚本数: {0}" -f $(if ($alembicVersions) { ($alembicVersions | Measure-Object).Count } else { 0 }))

# 8. 检测企业级测试套件 (Tests)
$testFiles = Get-ChildItem -Path (Join-Path $be "tests") -Recurse -Filter "test_*.py" -File -ErrorAction SilentlyContinue
$testFuncCount = 0
if ($testFiles) {
    foreach ($tf in $testFiles) {
        $hits = (Select-String -Path $tf.FullName -Pattern "def test_\w+\(" -ErrorAction SilentlyContinue | Measure-Object).Count
        $testFuncCount += $hits
    }
}
$testOk = ($testFuncCount -ge 8)
Report "自动化测试用例数量" $testOk $true ("检测到测试函数: {0} 个 (最低要求: 8 个)" -f $testFuncCount)

# 9. 检测前端生产打包体积预算 (Bundle Chunk Budget <= 500KB)
$distAssets = @()
if (Test-Path (Join-Path $fe "dist\assets")) {
    $distAssets = Get-ChildItem -Path (Join-Path $fe "dist\assets") -Filter "*.js" -File -ErrorAction SilentlyContinue
} elseif (Test-Path (Join-Path $fe ".next\static\chunks")) {
    $distAssets = Get-ChildItem -Path (Join-Path $fe ".next\static\chunks") -Filter "*.js" -Recurse -File -ErrorAction SilentlyContinue
}
$oversizedChunks = @()
if ($distAssets) {
    foreach ($chunk in $distAssets) {
        if ($chunk.Length -gt 500KB) {
            $oversizedChunks += ("{0} ({1}KB)" -f $chunk.Name, [math]::Round($chunk.Length / 1KB))
        }
    }
}
$bundleOk = ($oversizedChunks.Count -eq 0)
$bundleDetail = if ($distAssets.Count -eq 0) { "未发现生产构建产物目录(建议提前 npm run build 验证体积)" } elseif ($bundleOk) { "所有 JS Chunk 均 <= 500KB" } else { "发现超大 Chunk: " + ($oversizedChunks -join ", ") }
Report "前端打包体积预算 (Chunk <= 500KB)" $bundleOk $false $bundleDetail

Write-Host "-----------------------------------------------------------------"
Write-Host ("复杂度审计汇总: PASS={0}  FAIL={1}  WARN={2}" -f $script:pass, $script:fail, $script:warn)
Write-Host "================================================================="

if ($script:fail -gt 0) {
    Write-Host "【结论】: ❌ 未达到生产级系统复杂度底线！存在 $script:fail 项致命缺陷。"
    Write-Host "         必须按照 references/11-enterprise-complexity-architecture.md 扩充数据模型、业务路由与前端组件，严禁提交简易玩具 Demo。"
    exit 1
} else {
    Write-Host "【结论】: ✅ 生产级系统复杂度与规模审计全面达标！具备商业级落地与大型系统基础。"
    exit 0
}
