#!/usr/bin/env python3
"""
list_skills.py — 本地已安装技能盘点与 hack2win 编排注册表核验 (跨平台通用版)
支持: Linux / macOS / Windows (零第三方依赖, 仅使用 Python 标准库)
用法: python scripts/list_skills.py
"""

import sys
from pathlib import Path

REGISTRY = [
    {"name": "find-skills",                  "use": "技能发现与安装"},
    {"name": "research",                     "use": "P0-P2 系统调研"},
    {"name": "domain-modeling",              "use": "P3 领域建模/ADR"},
    {"name": "codebase-design",              "use": "P4 架构边界设计与接缝"},
    {"name": "setup-ts-deep-modules",        "use": "P4 TS深模块依赖隔离 (dependency-cruiser)"},
    {"name": "improve-codebase-architecture","use": "P4 架构体检与重构"},
    {"name": "nextjs-supabase-auth",         "use": "P4 认证集成(可选)"},
    {"name": "tauri",                        "use": "P4 跨平台桌面交付"},
    {"name": "tauri-development",            "use": "P4 桌面端开发与调试"},
    {"name": "design-taste-frontend",        "use": "P5 UI 打磨(主引用)"},
    {"name": "tdd",                          "use": "P4 核心模块测试先行"},
    {"name": "typescript-e2e-testing",       "use": "P4 TS 集成/E2E(可选)"},
    {"name": "ai-regression-testing",        "use": "P4 AI 功能回归(可选)"},
    {"name": "setup-pre-commit",             "use": "P4 质量闸"},
    {"name": "code-review",                  "use": "P6 提交前评审"},
    {"name": "diagnosing-bugs",              "use": "紧急排障"},
    {"name": "skill-creator",                "use": "现场造最小技能(插件)"},
]

def scan_installed_skills() -> dict[str, Path]:
    home = Path.home()
    dirs_to_check = [
        home / ".agents" / "skills",
        home / ".zcode" / "skills",
    ]
    installed: dict[str, Path] = {}

    for base_dir in dirs_to_check:
        if base_dir.exists():
            for child in base_dir.iterdir():
                if child.is_dir() and (child / "SKILL.md").exists():
                    installed[child.name] = child

    return installed

def main():
    installed = scan_installed_skills()
    print(f"=== 本机已装技能 (跨平台检测): {len(installed)} 个 ===")
    for name in sorted(installed.keys()):
        print(f"  {name}")

    print("\n=== 编排注册表核对 ===")
    missing = []
    home = Path.home()

    for item in REGISTRY:
        name = item["name"]
        use = item["use"]
        is_ok = name in installed

        # 特例插件检测: skill-creator
        if not is_ok and name == "skill-creator":
            plugin_cache = home / ".zcode" / "cli" / "plugins" / "cache"
            if plugin_cache.exists():
                is_ok = any(plugin_cache.glob("**/skill-creator/**/SKILL.md"))

        status = "OK  " if is_ok else "MISS"
        if not is_ok:
            missing.append(name)
        print(f"  [{status}] {name:<32} {use}")

    print("")
    if missing:
        print(f"提示: 检测到 {len(missing)} 个未安装技能: {', '.join(missing)}")
        print("安装方法详见 references/10-orchestration.md §3 (例如 git clone 到 ~/.agents/skills/<name>)")
    else:
        print("✅ 注册表技能全部就绪，总控编排链完全可用！")

if __name__ == "__main__":
    main()
