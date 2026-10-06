#!/usr/bin/env python3
"""
ui_shot.py — 视觉验收循环的跨平台自动化截图工具 (桌面+窄屏)
支持: Linux (Ubuntu/Debian) / macOS / Windows
自动探测浏览器: Chrome / Chromium / Edge / Brave
防假阳性: 内建 DOM 内容预检与浏览器错误页识别 (ERR_CONNECTION_CLOSED 等中断告警)
用法: python scripts/ui_shot.py --url "http://localhost:3000" --out-dir "iterations/round-1" --tag "home" [--expect-text "产品名"]
"""

import os
import sys
import re
import shutil
import tempfile
import argparse
import subprocess
from pathlib import Path

# 确保在任意语言的操作系统(如 Windows 默认 cp1252 英文环境)下能够安全输出中文字符
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

def find_browser() -> str | None:
    # 环境变量指定优先
    custom = os.environ.get("CHROME_BIN") or os.environ.get("BROWSER_PATH")
    if custom and Path(custom).exists():
        return custom

    # 按系统查找候选路径
    if sys.platform == "darwin":  # macOS
        candidates = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
            "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
            "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        ]
    elif sys.platform.startswith("linux"):  # Linux
        candidates = [
            shutil.which("google-chrome"),
            shutil.which("google-chrome-stable"),
            shutil.which("chromium"),
            shutil.which("chromium-browser"),
            shutil.which("microsoft-edge"),
            "/usr/bin/google-chrome",
            "/usr/bin/chromium",
            "/usr/bin/chromium-browser",
            "/snap/bin/chromium",
        ]
    else:  # Windows
        candidates = [
            os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"),
            os.path.expandvars(r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"),
        ]

    for c in candidates:
        if c and Path(c).exists():
            return str(Path(c).resolve())
    return None

def main():
    parser = argparse.ArgumentParser(description="hack2win 视觉验收循环跨平台截图工具")
    parser.add_argument("--url", "-u", required=True, help="目标页面 URL")
    parser.add_argument("--out-dir", "-o", required=True, help="截图输出目录")
    parser.add_argument("--tag", "-t", default="shot", help="截图名称前缀 (默认: shot)")
    parser.add_argument("--sizes", "-s", default="1440,900;390,844", help="截图分辨率列表 (默认: 1440,900;390,844)")
    parser.add_argument("--wait-ms", "-w", type=int, default=8000, help="虚拟时间等待毫秒数 (默认: 8000)")
    parser.add_argument("--expect-text", "-e", default="", help="页面必须包含的关键文本 (防白屏与假阳性)")
    args = parser.parse_args()

    browser = find_browser()
    if not browser:
        print("[FAIL] 未找到 Chrome / Chromium / Edge 浏览器！请安装或设置 CHROME_BIN 环境变量。")
        sys.exit(1)

    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    # 步骤 1: 内容预检 (dump-dom)
    dom_file = out_dir / "_dom_check.html"
    cmd_dump = [
        browser,
        "--headless=new",
        "--disable-gpu",
        f"--virtual-time-budget={args.wait_ms}",
        "--dump-dom",
        args.url
    ]
    try:
        res = subprocess.run(cmd_dump, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="ignore", timeout=25)
        dom = res.stdout or ""
        dom_file.write_text(dom, encoding="utf-8", errors="ignore")
    except Exception as e:
        print(f"[FAIL] 预检执行失败: {e}")
        sys.exit(1)

    # 检测错误页特征
    if re.search(r"ERR_(CONNECTION|NAME|INTERNET)|无法访问此网站|This site can", dom, re.IGNORECASE):
        print(f"[FAIL] 页面是浏览器错误页 (网络受阻或本地服务未启动) -- 拒绝产出误导性截图！")
        sys.exit(1)

    if args.expect_text:
        if args.expect_text not in dom:
            print(f"[FAIL] 页面 DOM 未包含预期文本 '{args.expect_text}' -- 白屏/加载未完成/渲染异常！")
            sys.exit(1)
        print(f"[PASS] 内容预检通过: 成功检测到关键文本 '{args.expect_text}'")
    else:
        print("[WARN] 未指定 --expect-text 参数，跳过内容断言 (建议在正式验收时始终指定产品名)")

    # 步骤 2: 逐分辨率截图
    ok_count = 0
    size_list = [s.strip() for s in args.sizes.split(";") if s.strip()]
    
    for size in size_list:
        w_s, h_s = size.split(",")
        w, h = int(w_s), int(h_s)
        label = "mobile" if w <= 500 else "desktop"
        out_file = out_dir / f"{args.tag}-{label}.png"

        with tempfile.TemporaryDirectory(prefix="uishot_") as tmp_profile:
            cmd_shot = [
                browser,
                "--headless=new",
                "--disable-gpu",
                "--hide-scrollbars",
                f"--user-data-dir={tmp_profile}",
                f"--window-size={w},{h}",
                f"--virtual-time-budget={args.wait_ms}",
                f"--screenshot={str(out_file)}",
                args.url
            ]
            try:
                subprocess.run(cmd_shot, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
                if out_file.exists() and out_file.stat().st_size > 3 * 1024:
                    print(f"[PASS] {label} ({w}x{h}) -> {out_file.name} [{round(out_file.stat().st_size / 1024)}KB]")
                    ok_count += 1
                else:
                    print(f"[FAIL] {label} 截图失败或体积异常")
            except Exception as e:
                print(f"[FAIL] {label} 截图执行异常: {e}")

    if ok_count < len(size_list):
        sys.exit(1)

    print(f"=== {ok_count}/{len(size_list)} 张截图完成！视觉环三问: 1)与竞品并排像获奖作品吗 2)第一眼最丑的三处 3)信息设计过关吗 ===")
    sys.exit(0)

if __name__ == "__main__":
    main()
