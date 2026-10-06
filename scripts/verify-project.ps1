# verify-project.ps1 — T2 全栈交付结构校验(反过简硬门槛)
# 用法: powershell -File verify-project.ps1 -ProjectPath <项目根目录>
# 输出: 逐项 PASS/FAIL/WARN + 汇总;全部硬项通过时退出码 0,否则 1
param([Parameter(Mandatory=$true)][string]$ProjectPath)

$ErrorActionPreference = "SilentlyContinue"
$script:pass = 0; $script:fail = 0; $script:warn = 0
function Check($name, $ok, $hard, $detail) {
    $tag = if ($ok) { $script:pass++; "PASS" } elseif ($hard) { $script:fail++; "FAIL" } else { $script:warn++; "WARN" }
    Write-Host ("[{0}] {1} -- {2}" -f $tag, $name, $detail)
}
function AnyFile($dir, $patterns) {
    foreach ($p in $patterns) { if (Get-ChildItem -Path $dir -Filter $p -Recurse -File -ErrorAction SilentlyContinue | Select-Object -First 1) { return $true } }
    return $false
}

Write-Host "=== hack2win T2 结构校验: $ProjectPath ==="
if (-not (Test-Path $ProjectPath)) { Write-Host "[FAIL] 项目根目录不存在"; exit 1 }

# 1. 项目结构: 前后端双目录
$fe = Join-Path $ProjectPath "frontend"; $be = Join-Path $ProjectPath "backend"
Check "双目录(frontend/ backend/)" ((Test-Path $fe) -and (Test-Path $be)) $true "T2 前后端分离"
if (-not ((Test-Path $fe) -and (Test-Path $be))) { Write-Host "结论: 非 T2 结构,若为 T1 降级请确认 devlog 有触发器记录"; exit 1 }

# 2. 依赖管理: lockfile + 依赖清单
Check "前端 package.json" (Test-Path (Join-Path $fe "package.json")) $true ""
Check "前端 lockfile" (AnyFile $fe @("package-lock.json","pnpm-lock.yaml","yarn.lock","bun.lockb")) $true "依赖锁定"
Check "后端依赖清单" ((AnyFile $be @("requirements.txt","pyproject.toml")) -or (Test-Path (Join-Path $be "Pipfile"))) $true ""

# 3. 配置: .env.example 双端
$feEnv = AnyFile $fe @(".env.local.example",".env.example")
$beEnv = AnyFile $be @(".env.example")
Check "前端 .env 模板" $feEnv $false "未发现则配置要素缺失"
Check "后端 .env.example" $beEnv $true "配置要素"
$secretHit = Get-ChildItem -Path $be -Recurse -Include *.py -File | Select-String -Pattern "(sk-[A-Za-z0-9]{20,}|api_key\s*=\s*['\`"][A-Za-z0-9]{16,})" -ErrorAction SilentlyContinue | Select-Object -First 1
Check "无硬编码密钥" (-not $secretHit) $true "backend 代码内疑似明文key"

# 4. 数据层: ORM + 迁移 + seed
$models = AnyFile (Join-Path $be "app") @("models") -ErrorAction SilentlyContinue
if (-not $models) { $models = Test-Path (Join-Path $be "app\models") }
Check "数据模型目录" $models $true "backend/app/models"
$mig = (Test-Path (Join-Path $be "alembic")) -or (Test-Path (Join-Path $be "migrations")) -or (AnyFile $be @("alembic.ini","migrations"))
Check "数据库迁移" $mig $false "alembic/migrations 未发现(赛期可SQLite+create_all,部署必须迁移)"
$seed = AnyFile $be @("seed*.py","*seed*.py")
Check "种子数据" $seed $false "seed 脚本未发现"

# 5. 接口定义: 路由非空 + 入口
$route = Get-ChildItem -Path (Join-Path $be "app") -Recurse -Include *.py -File | Where-Object { $_.FullName -match "routes|api|routers|endpoints" } | Select-Object -First 1
Check "接口路由文件" ($null -ne $route) $true "backend/app/api|routes"
Check "后端入口 main/app" ((AnyFile $be @("main.py")) -or (Test-Path (Join-Path $be "app\main.py"))) $true ""

# 6. 错误处理: 后端统一处理 + 前端调用封装
$errBe = (AnyFile (Join-Path $be "app") @("errors.py","exceptions.py","error_handler*")) -or ((Get-ChildItem -Path $be -Recurse -Include *.py -File | Select-String -Pattern "exception_handler|HTTPException" -ErrorAction SilentlyContinue | Select-Object -First 1) -ne $null)
Check "后端统一错误处理" $errBe $true "errors.py 或 exception_handler"
$feApi = AnyFile (Join-Path $fe "lib") @("api.ts","api.js","http.ts","request.ts") 
if (-not $feApi) { $feApi = AnyFile (Join-Path $fe "src") @("api.ts","api.js","http.ts") }
Check "前端统一API封装" $feApi $true "lib/api.ts(错误处理住这)"

# 7. 文档
$readme = Join-Path $ProjectPath "README.md"
$readmeOk = $false
if (Test-Path $readme) { $c = Get-Content $readme -Raw; $readmeOk = ($c -match "启动|run|install|架构|architecture") }
Check "README 含启动/架构说明" $readmeOk $true "项目根 README.md"

# 反空壳探测(警告级,人工复核)
$todo = (Get-ChildItem -Path (Join-Path $be "app") -Recurse -Include *.py -File | Select-String -Pattern "NotImplementedError|TODO|FIXME" -ErrorAction SilentlyContinue | Measure-Object).Count
Check "后端 TODO/未实现探测" ($todo -eq 0) $false "发现 $todo 处(规划注释请移入devlog)"
$mock = (Get-ChildItem -Path $be -Recurse -Include *.py -File | Select-String -Pattern "['\`"]mock['\`"]\s*:\s*true|return\s+\{\s*['\`"]mock" -ErrorAction SilentlyContinue | Measure-Object).Count
Check "后端 mock 返回探测" ($mock -eq 0) $false "发现 $mock 处疑似假接口"

# 冒烟提示(无法在此替你跑,列出命令)
Write-Host ""
Write-Host "=== 冒烟命令(须真实跑绿并把输出贴进 devlog) ==="
Write-Host "  frontend: cd frontend; npm install; npm run build"
Write-Host "  backend : cd backend; pip install -r requirements.txt; pytest; uvicorn app.main:app --port 8000  (curl /health)"
Write-Host ""
Write-Host ("=== 汇总: PASS={0} FAIL={1} WARN={2} ===" -f $script:pass, $script:fail, $script:warn)
if ($script:fail -gt 0) { Write-Host "结论: 未达 T2 交付契约"; exit 1 } else { Write-Host "结论: T2 结构契约通过(WARN 项人工复核)"; exit 0 }
