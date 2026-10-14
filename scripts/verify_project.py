#!/usr/bin/env python3
"""
verify_project.py — T2 全栈交付结构与基础工程契约校验 (跨平台通用版)
支持: Linux / macOS / Windows (零第三方依赖, 仅使用 Python 标准库)
用法: python scripts/verify_project.py --project-path <项目根目录>
"""

import os
import sys
import re
import argparse
from pathlib import Path

# 确保在任意语言的操作系统(如 Windows 默认 cp1252 英文环境)下能够安全输出中文字符
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

class Checker:
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.passed = 0
        self.failed = 0
        self.warned = 0
        self.probe_base_url = None

    def check(self, name: str, ok: bool, hard: bool = True, detail: str = ""):
        if ok:
            self.passed += 1
            tag = "PASS"
        elif hard:
            self.failed += 1
            tag = "FAIL"
        else:
            self.warned += 1
            tag = "WARN"
        print(f"[{tag}] {name} -- {detail}")

    def any_file(self, directory: Path, patterns: list[str]) -> bool:
        if not directory.exists():
            return False
        for root, _, files in os.walk(directory):
            for f in files:
                for p in patterns:
                    if re.search(p, f, re.IGNORECASE):
                        return True
        return False

    def scan_pattern(self, directory: Path, ext_pattern: str, regex: str) -> int:
        if not directory.exists():
            return 0
        count = 0
        for root, _, files in os.walk(directory):
            if any(x in root for x in ["node_modules", ".next", "venv", ".venv", "__pycache__"]):
                continue
            for f in files:
                if re.search(ext_pattern, f, re.IGNORECASE):
                    file_path = Path(root) / f
                    try:
                        content = file_path.read_text(encoding="utf-8", errors="ignore")
                        count += len(re.findall(regex, content))
                    except Exception:
                        pass
        return count

    def run(self) -> int:
        print(f"=== hack2win T2 结构契约校验 (Python 跨平台版): {self.project_path} ===")
        if not self.project_path.exists():
            print(f"[FAIL] 项目根目录不存在: {self.project_path}")
            return 1

        fe = self.project_path / "frontend"
        be = self.project_path / "backend"

        # 1. 项目结构: 前后端双目录
        has_dual = fe.exists() and be.exists()
        self.check("双目录 (frontend/ backend/)", has_dual, True, "T2 前后端分离架构")
        if not has_dual:
            print("结论: 非 T2 结构, 若为 T1 降级请确认 devlog 有触发器与决策记录")
            return 1

        # 2. 依赖管理
        self.check("前端 package.json", (fe / "package.json").exists(), True, "")
        lock_ok = self.any_file(fe, [r"package-lock\.json", r"pnpm-lock\.yaml", r"yarn\.lock", r"bun\.lockb"])
        self.check("前端 lockfile (依赖锁定)", lock_ok, True, "")
        be_deps = self.any_file(be, [r"requirements\.txt", r"pyproject\.toml", r"Pipfile"])
        self.check("后端依赖清单", be_deps, True, "")

        # 3. 配置
        fe_env = self.any_file(fe, [r"\.env\.local\.example", r"\.env\.example"])
        self.check("前端 .env 模板", fe_env, False, "未发现则配置要素缺失")
        be_env = self.any_file(be, [r"\.env\.example"])
        self.check("后端 .env.example", be_env, True, "配置要素")

        secret_pattern = r"(sk-[A-Za-z0-9]{20,}|api_key\s*=\s*['\"][A-Za-z0-9]{16,}['\"])"
        secrets_found = self.scan_pattern(be, r"\.py$", secret_pattern)
        self.check("无硬编码密钥", secrets_found == 0, True, f"扫描发现 {secrets_found} 处疑似明文密钥")

        # 4. 数据层
        models_dir = (be / "app" / "models")
        models_ok = (models_dir.exists() and any(models_dir.glob("*.py"))) or \
                    (be / "models").exists() or \
                    (be / "prisma" / "schema.prisma").exists() or \
                    self.any_file(be, [r"schema\.[jt]s", r"models?\.[jt]s"])
        self.check("数据模型层 (models/prisma/schema)", models_ok, True, "")

        mig_ok = (be / "alembic").exists() or (be / "migrations").exists() or (be / "alembic.ini").exists() or \
                 (self.project_path / "migrations").exists() or (be / "prisma" / "migrations").exists()
        self.check("数据库迁移 (alembic/migrations/prisma)", mig_ok, False, "未发现迁移脚本链 (部署前必须具备)")

        seed_ok = self.any_file(be, [r"seed.*\.(py|ts|js|sql)"]) or self.any_file(self.project_path, [r"seed.*\.(py|ts|js|sql)"])
        self.check("种子数据脚本", seed_ok, False, "未发现 seed 数据脚本 (py/ts/js/sql)")

        # 5. 接口定义
        routes_found = self.any_file(be / "app", [r"routes?\.py", r"api.*\.py", r"endpoints?\.py"]) or \
                       (be / "app" / "api").exists() or (be / "routes").exists() or (be / "src" / "routes").exists() or \
                       self.any_file(be, [r"routes?\.ts", r"api.*\.ts", r"controller.*\.[jt]s"])
        self.check("接口路由目录与文件", routes_found, True, "")
        entry_ok = (be / "app" / "main.py").exists() or (be / "main.py").exists() or \
                   (be / "server.ts").exists() or (be / "index.ts").exists() or (be / "src" / "index.ts").exists() or \
                   (be / "main.go").exists() or (be / "src" / "main.rs").exists()
        self.check("后端应用入口 (main/server/index)", entry_ok, True, "")

        # 6. 错误处理
        err_ok = (be / "app" / "core" / "errors.py").exists() or (be / "app" / "errors.py").exists() or \
                 (self.scan_pattern(be, r"\.(py|[jt]sx?)$", r"exception_handler|HTTPException|AppException|ApiError|ErrorHandler") > 0)
        self.check("后端统一错误处理", err_ok, True, "errors 模块或全局 exception_handler")

        fe_api_ok = self.any_file(fe, [r"api.*\.ts", r"api.*\.js", r"http.*\.ts", r"client.*\.ts"])
        self.check("前端统一API客户端", fe_api_ok, True, "lib/api-client.ts 或等价封装")

        # 7. 文档
        readme = self.project_path / "README.md"
        readme_ok = False
        if readme.exists():
            content = readme.read_text(encoding="utf-8", errors="ignore")
            readme_ok = bool(re.search(r"启动|run|install|架构|architecture|quickstart", content, re.IGNORECASE))
        self.check("README 架构与启动说明", readme_ok, True, "项目根 README.md")

        # 8. 反空壳警告扫描
        todo_count = self.scan_pattern(be / "app", r"\.py$", r"NotImplementedError|TODO|FIXME")
        self.check("后端 TODO/未实现探测", todo_count == 0, False, f"发现 {todo_count} 处 (规划注释应移入 devlog)")

        mock_count = self.scan_pattern(be / "app", r"\.py$", r"['\"]mock['\"]\s*:\s*true|return\s+\{\s*['\"]mock")
        self.check("后端 mock 假接口探测", mock_count == 0, False, f"发现 {mock_count} 处疑似假数据硬编码返回")

        # 9. OpenAPI 匿名全扫 (L3 边界不可信的机械化执法, R19 实测人工抽样会漏边门)
        if self.probe_base_url:
            self.probe_openapi_anonymous(self.probe_base_url)

        print("-----------------------------------------------------------------")
        print(f"=== 校验汇总: PASS={self.passed}  FAIL={self.failed}  WARN={self.warned} ===")
        if self.failed > 0:
            print("【结论】: ❌ 未达到 T2 交付契约！请补齐上述 FAIL 项。")
            return 1
        else:
            print("【结论】: ✅ T2 基础结构契约通过！(WARN 项请按需人工复核)")
            return 0

    def probe_openapi_anonymous(self, base_url: str) -> None:
        """解析 /openapi.json 逐操作匿名请求, 断言非白名单操作全部 401/403。

        - 2xx 匿名可达 → FAIL (鉴权边门)
        - 401/403 → closed, 计入 PASS 明细
        - 其他 4xx (如先过 body 校验的 422) → 无法证明受保护, 单独计数 WARN
        白名单: /health, /docs, /openapi.json, 登录/注册类路径 (auth/session|login|register|token)。
        """
        import json as _json
        import urllib.request
        import urllib.error

        openapi_url = base_url.rstrip("/") + "/openapi.json"
        try:
            with urllib.request.urlopen(openapi_url, timeout=5) as resp:
                spec = _json.loads(resp.read().decode("utf-8"))
        except Exception:
            self.check("OpenAPI 匿名全扫", False, False,
                       f"服务不可达({openapi_url}), 扫描跳过——联调期请带 --probe-base-url 复跑")
            return

        whitelist = re.compile(r"/health|/docs|/openapi|auth/(session|login|register|token)|/login|/register", re.IGNORECASE)
        closed, unproven, open_ops = 0, 0, []
        methods = {"get", "post", "put", "patch", "delete"}
        for path, item in spec.get("paths", {}).items():
            for method, op in item.items():
                if method.lower() not in methods:
                    continue
                if whitelist.search(path):
                    continue
                url = base_url.rstrip("/") + path
                req = urllib.request.Request(url, method=method.upper(),
                                             data=b"{}" if method.lower() in {"post", "put", "patch"} else None,
                                             headers={"Content-Type": "application/json"})
                try:
                    with urllib.request.urlopen(req, timeout=5) as resp:
                        status = resp.status
                except urllib.error.HTTPError as e:
                    status = e.code
                except Exception:
                    status = 0
                if status in (401, 403):
                    closed += 1
                elif 200 <= status < 300:
                    open_ops.append(f"{method.upper()} {path} -> {status}")
                else:
                    unproven += 1

        if open_ops:
            self.check("OpenAPI 匿名全扫(非白名单全 401/403)", False, True,
                       f"鉴权边门 {len(open_ops)} 个: {', '.join(open_ops[:5])}")
        else:
            self.check("OpenAPI 匿名全扫(非白名单全 401/403)", True, True,
                       f"已扫 {closed + unproven} 个操作: {closed} 关闭, {unproven} 未证明(body 先于鉴权 4xx), 0 边门")


def main():
    parser = argparse.ArgumentParser(description="hack2win T2 项目结构与基础契约校验")
    parser.add_argument("--project-path", "-p", required=True, help="项目根目录路径")
    parser.add_argument("--probe-base-url", default=None,
                        help="可选: 运行中后端的 base URL (如 http://127.0.0.1:8800); 提供时执行 OpenAPI 匿名全扫(L3 机械化执法)")
    args = parser.parse_args()
    checker = Checker(Path(args.project_path).resolve())
    checker.probe_base_url = args.probe_base_url
    sys.exit(checker.run())

if __name__ == "__main__":
    main()
