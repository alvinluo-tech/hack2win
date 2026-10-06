#!/usr/bin/env python3
"""
update_check.py — hack2win 安装状态记录与版本自检

对标 PaperSpine 的 paper-spine-update / nature-skills 的 update-codex-skills.sh:
技能包一旦被安装到 5 个不同宿主工具的 skills 目录, 用户很快会不知道
"我装的是哪一版、装到了哪些端、本地副本是否已落后于仓库"。

本脚本做三件事:
  1. --record  : 由 installer 调用, 把本次安装的版本/时间/落盘目标写入
                 <install root>/install_state.json (安装状态单一真值源);
  2. (默认)     : 读取仓库版本 (skill.json) 与安装状态, 报告各端副本是否与仓库同源
                 (通过对比 SKILL.md 的 SHA-256, 判断该端副本是否过期或已被篡改);
  3. --json     : 机器可读输出, 便于 CI 或上层编排消费。

零第三方依赖, 跨平台 (Linux / macOS / Windows)。退出码: 0 一致 / 1 存在漂移。
用法:
  python scripts/update_check.py
  python scripts/update_check.py --json
  python scripts/update_check.py --record --version 15.0 --targets claude,codex,zcode
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# 确保在任意语言的操作系统(如 Windows 默认 cp1252 英文环境)下能够安全输出中文字符
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "skill.json"

# 已知的宿主技能安装根目录 (与 install.sh / install.ps1 保持一致)
AGENT_ROOTS = {
    "agents": Path.home() / ".agents" / "skills" / "hack2win",
    "claude": Path.home() / ".claude" / "skills" / "hack2win",
    "codex": Path.home() / ".codex" / "skills" / "hack2win",
    "zcode": Path.home() / ".zcode" / "skills" / "hack2win",
    "opencode": Path.home() / ".config" / "opencode" / "skill" / "hack2win",
}


def sha256_of(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return ""


def load_manifest() -> dict:
    if not MANIFEST.is_file():
        return {"version": "unknown", "installed_state_file": "~/.hack2win/install_state.json"}
    try:
        return json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"version": "unreadable"}


def state_path() -> Path:
    return Path.home() / ".hack2win" / "install_state.json"


def do_record(version: str, targets: list[str]) -> int:
    """把本次安装事实写入安装状态文件, 供后续 --check 比对。"""
    manifest = load_manifest()
    payload = {
        "installed_version": version or manifest.get("version", "unknown"),
        "installed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "targets": targets,
        "source": {
            "repository": manifest.get("repository", ""),
            "skill_sha256": sha256_of(ROOT / "SKILL.md"),
            "reference_count": len(list((ROOT / "references").glob("*.md"))),
        },
    }
    path = state_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[record] 安装状态已写入 {path}")
    print(f"         版本 {payload['installed_version']} | 目标端 {', '.join(targets) or '(none)'}")
    return 0


def do_check(as_json: bool) -> int:
    manifest = load_manifest()
    repo_version = manifest.get("version", "unknown")
    repo_hash = sha256_of(ROOT / "SKILL.md")

    state = {}
    sp = state_path()
    if sp.is_file():
        try:
            state = json.loads(sp.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            state = {}

    rows = []
    drift = False
    for name, path in AGENT_ROOTS.items():
        installed = path.is_dir()
        local_hash = sha256_of(path / "SKILL.md") if installed else ""
        if not installed:
            status = "未安装"
        elif local_hash == repo_hash:
            status = "同源 (in-sync)"
        else:
            status = "已漂移 (drifted)"
            drift = True
        rows.append({
            "agent": name,
            "path": str(path),
            "installed": installed,
            "status": status,
            "sha256": local_hash[:12],
        })

    result = {
        "repo_version": repo_version,
        "repo_skill_sha256": repo_hash[:12],
        "installed_version": state.get("installed_version", "(未记录)"),
        "installed_at": state.get("installed_at", "(未记录)"),
        "agents": rows,
        "drift": drift,
    }

    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if drift else 0

    print("=" * 68)
    print("hack2win 版本与安装状态自检")
    print("=" * 68)
    print(f"  仓库版本      : {repo_version}")
    print(f"  SKILL.md 指纹 : {repo_hash[:12]}")
    print(f"  已记录安装版本: {result['installed_version']}  @ {result['installed_at']}")
    print("-" * 68)
    installed_any = False
    for r in rows:
        mark = {"同源 (in-sync)": "OK  ", "已漂移 (drifted)": "DRIFT", "未安装": "--  "}[r["status"]]
        print(f"  [{mark}] {r['agent']:<9} {r['status']:<16} {r['path']}")
        installed_any = installed_any or r["installed"]
    print("=" * 68)
    if not installed_any:
        print("结论: 本机尚未安装 hack2win 到任何宿主工具。运行 ./install.sh 或 ./install.ps1 安装。")
    elif drift:
        print("结论: 存在副本漂移 —— 某些宿主目录下的 SKILL.md 与仓库不一致。")
        print("      重新运行安装器即可刷新 (安装器为幂等覆盖)。")
    else:
        print("结论: 所有已安装副本与仓库同源, 版本一致。")
    return 1 if drift else 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="记录/检查 hack2win 的安装状态与各宿主工具副本是否与仓库同源"
    )
    parser.add_argument("--record", action="store_true", help="记录本次安装状态 (由安装器调用)")
    parser.add_argument("--version", default="", help="配合 --record: 本次安装的版本号")
    parser.add_argument("--targets", default="", help="配合 --record: 逗号分隔的目标端列表")
    parser.add_argument("--json", action="store_true", help="以 JSON 输出检查结果")
    args = parser.parse_args()

    if args.record:
        targets = [t.strip() for t in args.targets.split(",") if t.strip()]
        return do_record(args.version, targets)
    return do_check(args.json)


if __name__ == "__main__":
    sys.exit(main())
