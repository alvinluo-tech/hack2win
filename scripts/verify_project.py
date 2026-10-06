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
        models_ok = models_dir.exists() and any(models_dir.glob("*.py"))
        self.check("数据模型目录 (backend/app/models)", models_ok, True, "")

        mig_ok = (be / "alembic").exists() or (be / "migrations").exists() or (be / "alembic.ini").exists()
        self.check("数据库迁移 (alembic/migrations)", mig_ok, False, "未发现迁移脚本链 (部署前必须具备)")

        seed_ok = self.any_file(be, [r"seed.*\.py"])
        self.check("种子数据脚本", seed_ok, False, "未发现 seed.py 数据脚本")

        # 5. 接口定义
        routes_found = self.any_file(be / "app", [r"routes?\.py", r"api.*\.py", r"endpoints?\.py"]) or (be / "app" / "api").exists()
        self.check("接口路由目录与文件", routes_found, True, "")
        entry_ok = (be / "app" / "main.py").exists() or (be / "main.py").exists()
        self.check("后端应用入口 (main.py)", entry_ok, True, "")

        # 6. 错误处理
        err_ok = (be / "app" / "core" / "errors.py").exists() or (be / "app" / "errors.py").exists() or \
                 (self.scan_pattern(be / "app", r"\.py$", r"exception_handler|HTTPException|AppException") > 0)
        self.check("后端统一错误处理", err_ok, True, "errors.py 或 exception_handler")

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

        print("-----------------------------------------------------------------")
        print(f"=== 校验汇总: PASS={self.passed}  FAIL={self.failed}  WARN={self.warned} ===")
        if self.failed > 0:
            print("【结论】: ❌ 未达到 T2 交付契约！请补齐上述 FAIL 项。")
            return 1
        else:
            print("【结论】: ✅ T2 基础结构契约通过！(WARN 项请按需人工复核)")
            return 0

def main():
    parser = argparse.ArgumentParser(description="hack2win T2 项目结构与基础契约校验")
    parser.add_argument("--project-path", "-p", required=True, help="项目根目录路径")
    args = parser.parse_args()
    checker = Checker(Path(args.project_path).resolve())
    sys.exit(checker.run())

if __name__ == "__main__":
    main()
