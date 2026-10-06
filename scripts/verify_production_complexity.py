#!/usr/bin/env python3
"""
verify_production_complexity.py — 生产级系统复杂度与规模硬性审计工具 (跨平台通用版)
支持: Linux / macOS / Windows (零第三方依赖, 仅使用 Python 标准库)
用法: python scripts/verify_production_complexity.py --project-path <项目根目录> [--min-loc 4000]
"""

import os
import sys
import re
import argparse
from pathlib import Path

class ComplexityAuditor:
    def __init__(self, project_path: Path, min_loc: int = 4000, min_tables: int = 8, min_endpoints: int = 16, min_components: int = 15):
        self.project_path = project_path
        self.min_loc = min_loc
        self.min_tables = min_tables
        self.min_endpoints = min_endpoints
        self.min_components = min_components
        self.passed = 0
        self.failed = 0
        self.warned = 0

    def report(self, name: str, ok: bool, hard: bool, detail: str):
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

    def run(self) -> int:
        print("=================================================================")
        print(f"   hack2win 生产级系统复杂度与规模审计 (Python 跨平台版): {self.project_path}")
        print("=================================================================")

        if not self.project_path.exists():
            print(f"[FAIL] 项目根目录不存在: {self.project_path}")
            return 1

        fe = self.project_path / "frontend"
        be = self.project_path / "backend"

        # 1. 统计有效核心源码行数 (LOC)
        exclude_dirs = {"node_modules", ".next", "venv", ".venv", "__pycache__", ".git", "dist", "build", "coverage"}
        code_exts = {".ts", ".tsx", ".js", ".jsx", ".py", ".sql", ".css", ".html"}
        exclude_files = {"package-lock.json", "yarn.lock", "pnpm-lock.yaml", "bun.lockb"}

        total_loc = 0
        fe_loc = 0
        be_loc = 0

        for root, dirs, files in os.walk(self.project_path):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            for f in files:
                if f in exclude_files:
                    continue
                p = Path(root) / f
                if p.suffix.lower() in code_exts:
                    try:
                        lines = len(p.read_text(encoding="utf-8", errors="ignore").splitlines())
                        total_loc += lines
                        if str(p).startswith(str(fe)):
                            fe_loc += lines
                        elif str(p).startswith(str(be)):
                            be_loc += lines
                    except Exception:
                        pass

        loc_ok = total_loc >= self.min_loc
        loc_hard = total_loc < 1500  # 低于 1500 行直接判定为低级玩具
        self.report("有效核心源码量 (LOC)", loc_ok, loc_hard,
                    f"总行数: {total_loc} (前端: {fe_loc}, 后端: {be_loc}, 门槛: {self.min_loc})")

        # 2. 统计数据库实体模型类数量
        model_files = list((be / "app" / "models").glob("**/*.py")) if (be / "app" / "models").exists() else []
        table_count = 0
        for mf in model_files:
            try:
                content = mf.read_text(encoding="utf-8", errors="ignore")
                hits = len(re.findall(r"__tablename__\s*=|class\s+\w+\(.*Base.*\):", content))
                table_count += hits
            except Exception:
                pass
        self.report("数据库关系实体表数量", table_count >= self.min_tables, True,
                    f"检测到表/实体: {table_count} 个 (最低要求: {self.min_tables} 张规范表)")

        # 3. 统计 API 路由端点总数
        api_files = list((be / "app").glob("**/*.py")) if (be / "app").exists() else []
        endpoint_count = 0
        for af in api_files:
            try:
                content = af.read_text(encoding="utf-8", errors="ignore")
                hits = len(re.findall(r"@\w+\.(get|post|put|delete|patch|options|head)\(", content))
                endpoint_count += hits
            except Exception:
                pass
        self.report("API 业务路由端点数量", endpoint_count >= self.min_endpoints, True,
                    f"检测到端点: {endpoint_count} 个 (最低要求: {self.min_endpoints} 个端点)")

        # 4. 统计前端独立组件数量
        comp_dir = fe / "components"
        comp_files = [f for f in comp_dir.glob("**/*") if f.suffix.lower() in {".tsx", ".jsx"}] if comp_dir.exists() else []
        comp_count = len(comp_files)
        self.report("前端独立业务组件数量", comp_count >= self.min_components, True,
                    f"检测到组件: {comp_count} 个 (最低要求: {self.min_components} 个)")

        # 5. 检测异步后台任务队列 / Worker 支持
        worker_files = []
        if be.exists():
            for root, dirs, files in os.walk(be):
                dirs[:] = [d for d in dirs if d not in exclude_dirs]
                for f in files:
                    if re.search(r"worker|celery|arq|taskiq|tasks\.py|background", f, re.IGNORECASE) or "workers" in root:
                        worker_files.append(f)
        has_worker = len(worker_files) > 0
        self.report("异步任务处理 / Worker 队列", has_worker, False,
                    "已具备" if has_worker else "缺失 (耗时操作应解耦为异步队列)")

        # 6. 检测 Docker Compose
        compose_file = self.project_path / "docker-compose.yml"
        service_count = 0
        if compose_file.exists():
            try:
                content = compose_file.read_text(encoding="utf-8", errors="ignore")
                matches = re.findall(r"(?ms)^\s{2}[a-zA-Z0-9_\-]+:\s*\r?\n(?:\s{4}.+\r?\n)*?\s{4}(image|build):", content)
                service_count = len(matches)
            except Exception:
                pass
        self.report("Docker Compose 集群编排", service_count >= 2, False,
                    f"编排服务数 (含 image/build): {service_count} (推荐包含 app, db, redis 等)")

        # 7. 检测 Alembic 版本迁移
        alembic_versions = list((be / "alembic" / "versions").glob("*.py")) if (be / "alembic" / "versions").exists() else []
        has_mig = len(alembic_versions) > 0
        self.report("Alembic 数据库迁移版本链", has_mig, True,
                    f"版本脚本数: {len(alembic_versions)}")

        # 8. 检测测试用例数量
        test_files = list((be / "tests").glob("**/test_*.py")) if (be / "tests").exists() else []
        test_count = 0
        for tf in test_files:
            try:
                content = tf.read_text(encoding="utf-8", errors="ignore")
                test_count += len(re.findall(r"def test_\w+\(", content))
            except Exception:
                pass
        self.report("自动化测试用例数量", test_count >= 8, True,
                    f"检测到测试函数: {test_count} 个 (最低要求: 8 个)")

        # 9. 检测前端生产打包体积预算 (Bundle Chunk Budget <= 500KB)
        dist_assets = []
        if (fe / "dist" / "assets").exists():
            dist_assets = list((fe / "dist" / "assets").glob("*.js"))
        elif (fe / ".next" / "static" / "chunks").exists():
            dist_assets = list((fe / ".next" / "static" / "chunks").glob("**/*.js"))

        oversized = []
        for chunk in dist_assets:
            sz = chunk.stat().st_size
            if sz > 500 * 1024:
                oversized.append(f"{chunk.name} ({round(sz / 1024)}KB)")

        bundle_ok = len(oversized) == 0
        bundle_detail = "未发现生产构建产物目录 (建议提前构建验证)" if not dist_assets else \
                        ("所有 JS Chunk 均 <= 500KB" if bundle_ok else f"发现超大 Chunk: {', '.join(oversized)}")
        self.report("前端打包体积预算 (Chunk <= 500KB)", bundle_ok, False, bundle_detail)

        print("-----------------------------------------------------------------")
        print(f"复杂度审计汇总: PASS={self.passed}  FAIL={self.failed}  WARN={self.warned}")
        print("=================================================================")

        if self.failed > 0:
            print(f"【结论】: ❌ 未达到生产级系统复杂度底线！存在 {self.failed} 项致命缺陷。")
            print("         必须按照 references/11-enterprise-complexity-architecture.md 扩充数据模型、业务路由与前端组件。")
            return 1
        else:
            print("【结论】: ✅ 生产级系统复杂度与规模审计全面达标！具备商业级落地与大型系统基础。")
            return 0

def main():
    parser = argparse.ArgumentParser(description="hack2win 生产级系统复杂度与规模审计")
    parser.add_argument("--project-path", "-p", required=True, help="项目根目录路径")
    parser.add_argument("--min-loc", "-m", type=int, default=4000, help="最低核心源码行数门槛 (默认 4000)")
    args = parser.parse_args()
    auditor = ComplexityAuditor(Path(args.project_path).resolve(), min_loc=args.min_loc)
    sys.exit(auditor.run())

if __name__ == "__main__":
    main()
