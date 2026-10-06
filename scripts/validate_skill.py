#!/usr/bin/env python3
"""
validate_skill.py — hack2win 技能包自身的结构不变量自检 (本仓库 CI 专用)

背景: hack2win 与 PaperSpine / nature-skills 同类, 属于"多文件技能包"。
技能包一旦被拆成 SKILL.md + references/ + scripts/ + adapters/, 最大的腐化风险
不是逻辑错误, 而是**引用漂移**: SKILL.md 索引里指向的文档不存在、references 里新增了
文档却忘了登记、每种宿主工具的适配器清单漏了一个、双语文档失去同步。

这类问题人眼很难发现, 但会让 agent 在运行时读到不存在的文件而静默降级。
因此本脚本把"技能包结构"本身当作被测对象, 用机器校验的方式锁死。

零第三方依赖, 跨平台 (Linux / macOS / Windows), 退出码: 0 通过 / 1 失败。
用法: python scripts/validate_skill.py [--json]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# 确保在任意语言的操作系统(如 Windows 默认 cp1252 英文环境)下能够安全输出中文字符
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# 结构契约: 技能包必须长期持有的不变量
# ---------------------------------------------------------------------------

# 运行时被 agent 实际加载的核心文件, 缺失即技能不可用
REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "README_zh.md",
    "AGENTS.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "install.sh",
    "install.ps1",
    ".gitignore",
]

# 每种主流宿主工具的支持路径: 缺失即"兼容主流 agent 工具"的承诺落空
REQUIRED_ADAPTERS = [
    "adapters/codex-AGENTS-block.md",
    "adapters/cursor.mdc",
    "adapters/windsurf.md",
    "adapters/copilot.md",
]

# 跨平台 CLI 工具链 (.py 为唯一真值源, .ps1 为 Windows 便捷包装)
REQUIRED_SCRIPTS = [
    "scripts/verify_project.py",
    "scripts/verify_production_complexity.py",
    "scripts/ui_shot.py",
    "scripts/list_skills.py",
    "scripts/validate_skill.py",
    "scripts/update_check.py",
]

# 机器可读元数据与配置契约
REQUIRED_METADATA = [
    "skill.json",
    "schemas/run-config.schema.json",
]

# SKILL.md 正文必须包含的章节锚点: 少一个就意味着总控层的某类约束被悄悄削掉
REQUIRED_SKILL_SECTIONS = [
    "核心理念",
    "常驻规则",
    "验收",
    "详细文档索引",
]

# 严重度阈值
MIN_REFERENCE_COUNT = 14          # 知识库模块下限
MIN_SKILL_BYTES = 8_000           # 总控宪法不允许被削成一张便签
MIN_README_BYTES = 10_000         # 开源门面文档不允许空壳

# 运行配置契约必须声明的字段 (与 schemas/run-config.schema.json 的 required 对齐)
RUN_CONFIG_REQUIRED_KEYS = ["schema_version", "hackathon", "delivery", "ui"]


class Report:
    """收集 BLOCKER / WARNING / INFO 三级发现, 与 PaperSpine 审计模型对齐。"""

    def __init__(self) -> None:
        self.blockers: list[str] = []
        self.warnings: list[str] = []
        self.infos: list[str] = []

    @property
    def ok(self) -> bool:
        return not self.blockers

    def blocker(self, msg: str) -> None:
        self.blockers.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def info(self, msg: str) -> None:
        self.infos.append(msg)


def read_text(rel: str) -> str:
    path = ROOT / rel
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def check_required_files(rep: Report) -> None:
    for rel in REQUIRED_FILES + REQUIRED_ADAPTERS + REQUIRED_SCRIPTS + REQUIRED_METADATA:
        if not (ROOT / rel).is_file():
            rep.blocker(f"[缺失文件] {rel} 不存在 —— 技能包结构不完整")
    if rep.ok:
        rep.info(f"必需文件齐全: {len(REQUIRED_FILES)} 核心 + "
                 f"{len(REQUIRED_ADAPTERS)} 适配器 + {len(REQUIRED_SCRIPTS)} 脚本 + "
                 f"{len(REQUIRED_METADATA)} 元数据")


def check_config_contract(rep: Report) -> None:
    """配置契约与元数据必须自洽: schema 声明的 required 字段要真的在 properties 里。"""
    schema_path = ROOT / "schemas" / "run-config.schema.json"
    if not schema_path.is_file():
        return
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        rep.blocker(f"[配置契约] schemas/run-config.schema.json 不是合法 JSON: {exc}")
        return
    props = set(schema.get("properties", {}).keys())
    for key in schema.get("required", []):
        if key not in props:
            rep.blocker(f"[配置契约] schema.required 声明了 `{key}`, 但它不在 properties 中")
    for key in RUN_CONFIG_REQUIRED_KEYS:
        if key not in props:
            rep.blocker(f"[配置契约] schema 缺少 P0 冻结所必需的字段 `{key}`")

    manifest_path = ROOT / "skill.json"
    if manifest_path.is_file():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            rep.blocker(f"[元数据] skill.json 不是合法 JSON: {exc}")
            return
        for key in ("name", "version", "entrypoint", "repository"):
            if key not in manifest:
                rep.blocker(f"[元数据] skill.json 缺少 `{key}` 字段")
        version = manifest.get("version", "")
        body = read_text("SKILL.md")
        if version and f"version: {version}" not in body:
            rep.blocker(
                f"[版本漂移] skill.json 声明 version={version}, "
                f"但 SKILL.md frontmatter 未同步该版本号"
            )
        if rep.ok:
            rep.info(f"配置契约与元数据自洽 (version={version})")


def check_skill_sections(rep: Report) -> None:
    body = read_text("SKILL.md")
    if not body:
        rep.blocker("[SKILL.md] 无法读取或为空")
        return
    if len(body.encode("utf-8")) < MIN_SKILL_BYTES:
        rep.blocker(
            f"[SKILL.md] 体积仅 {len(body.encode('utf-8'))} 字节, "
            f"低于总控宪法下限 {MIN_SKILL_BYTES} —— 可能被误删章节"
        )
    if not body.lstrip().startswith("---"):
        rep.blocker("[SKILL.md] 缺少 YAML frontmatter (name/description)")
    else:
        front = body.split("---", 2)[1] if body.count("---") >= 2 else ""
        for key in ("name:", "description:"):
            if key not in front:
                rep.blocker(f"[SKILL.md] frontmatter 缺少 `{key}` 字段")
    for section in REQUIRED_SKILL_SECTIONS:
        if section not in body:
            rep.blocker(f"[SKILL.md] 缺少必需章节锚点: `{section}`")
    if rep.ok:
        rep.info(f"SKILL.md 宪法自检通过 ({len(body.encode('utf-8'))} 字节)")


def check_reference_index(rep: Report) -> dict[str, object]:
    """核心校验: SKILL.md 索引 <-> references/ 目录 双向一致。

    这是多文件技能包最常见的腐化点: 新增文档忘了登记(agent 永远找不到),
    或登记了不存在的文档(agent 读取时静默失败)。
    """
    ref_dir = ROOT / "references"
    on_disk = sorted(p.name for p in ref_dir.glob("*.md")) if ref_dir.is_dir() else []
    body = read_text("SKILL.md")

    indexed = sorted(set(re.findall(r"references/([0-9A-Za-z._-]+\.md)", body)))

    missing_in_index = [n for n in on_disk if n not in indexed]
    dangling = [n for n in indexed if n not in on_disk]

    for name in dangling:
        rep.blocker(f"[引用漂移] SKILL.md 索引指向 references/{name}, 但文件不存在")
    for name in missing_in_index:
        rep.blocker(f"[引用漂移] references/{name} 已存在, 但未登记进 SKILL.md 文档索引 "
                    f"(agent 将永远发现不了它)")

    if len(on_disk) < MIN_REFERENCE_COUNT:
        rep.warn(f"references/ 仅 {len(on_disk)} 篇, 低于知识库建议下限 {MIN_REFERENCE_COUNT}")

    if not dangling and not missing_in_index:
        rep.info(f"文档索引双向一致: {len(on_disk)} 篇 references 全部已登记且可达")

    return {"on_disk": on_disk, "indexed": indexed}


def check_encoding_guard(rep: Report) -> None:
    """每个 Python CLI 必须以 UTF-8 重配 stdout, 否则 Windows(cp1252) 下中文输出崩溃。

    这是本项目历史上真实踩过的 CI 失败, 固化为结构不变量。
    """
    for rel in REQUIRED_SCRIPTS:
        body = read_text(rel)
        if not body:
            continue
        if "reconfigure(encoding" not in body:
            rep.blocker(f"[编码守卫] {rel} 缺少 sys.stdout.reconfigure(encoding='utf-8') "
                        f"—— 将在 Windows cp1252 环境下抛 UnicodeEncodeError")
    rep.info("全部 Python CLI 均带 UTF-8 输出守卫")


def check_bilingual_sync(rep: Report) -> None:
    """中英双语文档必须同时更新, 且体积量级相当(防单边腐化)。"""
    en = (ROOT / "README.md")
    zh = (ROOT / "README_zh.md")
    if not en.is_file() or not zh.is_file():
        return
    en_len, zh_len = en.stat().st_size, zh.stat().st_size
    if min(en_len, zh_len) < MIN_README_BYTES:
        rep.blocker(f"[双语门面] README 体积过小 (EN={en_len}, ZH={zh_len}), "
                    f"开源门面不达下限 {MIN_README_BYTES}")
    ratio = min(en_len, zh_len) / max(en_len, zh_len)
    if ratio < 0.6:
        rep.warn(f"[双语漂移] README EN({en_len}B) 与 ZH({zh_len}B) 差异达 "
                 f"{int((1 - ratio) * 100)}%, 两侧可能失去同步")
    else:
        rep.info(f"双语 README 同步良好 (EN={en_len}B / ZH={zh_len}B)")


def check_feature_declaration(rep: Report) -> None:
    """README 声明的能力必须能在仓库里找到对应实体(防止文档吹牛)。"""
    en = read_text("README.md")
    declared_refs = set(re.findall(r"references/([0-9A-Za-z._-]+\.md)", en))
    on_disk = {p.name for p in (ROOT / "references").glob("*.md")}
    dangling = sorted(declared_refs - on_disk)
    for name in dangling:
        rep.blocker(f"[文档吹牛] README 链接 references/{name} 不存在")
    if not dangling and declared_refs:
        rep.info(f"README 引用的 {len(declared_refs)} 篇文档全部真实存在")


def check_installer_parity(rep: Report) -> None:
    """双平台安装器必须覆盖同一批宿主工具, 否则某个 OS 用户会静默少装。"""
    sh = read_text("install.sh")
    ps = read_text("install.ps1")
    if not sh or not ps:
        return
    hosts = {
        "Claude Code": (".claude", ".claude"),
        "Codex": (".codex", ".codex"),
        "ZCode": (".zcode", ".zcode"),
        "OpenCode": ("opencode", "opencode"),
        "agents.md 规范": (".agents", ".agents"),
    }
    for label, (token_sh, token_ps) in hosts.items():
        if token_sh not in sh or token_ps not in ps:
            rep.blocker(f"[安装器不对等] {label} 未被 install.sh 与 install.ps1 同时覆盖")
    project_tokens = ["cursor", "windsurf", "copilot"]
    for token in project_tokens:
        if token not in sh or token not in ps:
            rep.warn(f"[安装器不对等] 项目级 {token} 规则未被两个安装器同时支持")
    rep.info("install.sh / install.ps1 覆盖的宿主工具集合一致")


def summarise(rep: Report, refs: dict[str, object]) -> None:
    print("=" * 68)
    print("hack2win 技能包结构自检 (validate_skill.py)")
    print(f"根目录: {ROOT}")
    print("=" * 68)

    for msg in rep.blockers:
        print(f"  [BLOCKER] {msg}")
    for msg in rep.warnings:
        print(f"  [WARNING] {msg}")
    for msg in rep.infos:
        print(f"  [INFO   ] {msg}")

    print("-" * 68)
    print(f"知识库模块: {len(refs.get('on_disk', []))} 篇  |  "
          f"BLOCKER {len(rep.blockers)} / WARNING {len(rep.warnings)} / INFO {len(rep.infos)}")
    print("=" * 68)
    if rep.ok:
        print("结论: PASS —— 技能包结构不变量全部成立。")
    else:
        print("结论: FAIL —— 存在 BLOCKER, 技能包处于腐化状态, 禁止发布。")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="校验 hack2win 技能包的内部结构不变量(引用漂移/适配器覆盖/编码守卫/双语同步)"
    )
    parser.add_argument("--json", action="store_true", help="以 JSON 形式输出结果")
    args = parser.parse_args()

    rep = Report()
    refs = check_reference_index(rep)
    check_required_files(rep)
    check_skill_sections(rep)
    check_config_contract(rep)
    check_encoding_guard(rep)
    check_bilingual_sync(rep)
    check_feature_declaration(rep)
    check_installer_parity(rep)

    if args.json:
        print(json.dumps({
            "root": str(ROOT),
            "ok": rep.ok,
            "blockers": rep.blockers,
            "warnings": rep.warnings,
            "infos": rep.infos,
            "references": refs.get("on_disk", []),
        }, ensure_ascii=False, indent=2))
    else:
        summarise(rep, refs)

    return 0 if rep.ok else 1


if __name__ == "__main__":
    sys.exit(main())
