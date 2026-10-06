# Contributing to hack2win

Thank you for your interest in contributing to **hack2win** — the open standard for autonomous, production-grade AI hackathon engineering and full-stack MVP orchestration.

## Community Principles

We keep this project lean and engineering-first. By participating, you agree to:

- **Be respectful and constructive.** Critique ideas and code, never people.
- **Stay on topic.** Issues and PRs should be about hack2win's manuals, CLI tools, or orchestration rules.
- **No spam, self-promotion, or harassment.** Such content will be removed and repeat offenders blocked.
- **Report security issues privately** (see [SECURITY.md](SECURITY.md)) instead of opening public issues.

## How to Contribute

### 1. Reporting Bugs
- Check existing [Issues](https://github.com/alvinluo-tech/hack2win/issues) first to avoid duplicates.
- Open a new issue using the [Bug Report Template](.github/ISSUE_TEMPLATE/bug_report.md).
- Include: minimal reproducible steps, your agent harness (Claude Code / OpenClaw / Cursor / Windsurf / ZCode), OS, and CLI script output.

### 2. Suggesting Winning Patterns
Reverse-engineered a winning UI metaphor or an architectural invariant from a recent major hackathon? Open a Feature Request with:
- Hackathon name & year
- Winning project link / repo
- The invariant that secured the win (visual, architectural, or process)
- Where it belongs: `references/12-winning-ui-patterns.md` or `references/13-winning-knowledge.md`

### 3. Submitting Pull Requests
1. Fork the repo and create your branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Keep documentation strictly modular:
   - Reference manuals live under `references/` with strict two-digit numbering prefixes.
   - All internal links must be relative.
3. Test the CLI suite locally before submitting:
   ```bash
   python scripts/list_skills.py
   python scripts/verify_project.py --help
   python scripts/verify_production_complexity.py --help
   ```
4. Commit with conventional messages:
   ```bash
   git commit -m "feat(ui): add 3D voxel physics pattern to reference 12"
   ```
5. Push to your fork and open a Pull Request against `main`.

## Style Guide

- **Python**: PEP 8, Python 3.10+, zero mandatory third-party dependencies for scripts under `scripts/`.
- **Markdown**: Clear headings, Mermaid diagrams for architecture flows, accurate cross-platform terminal snippets.
- **Bilingual docs**: English in `README.md`, Chinese in `README_zh.md` — keep section headings and anchors synchronized.
- **Encoding**: All scripts must keep the `sys.stdout.reconfigure(encoding="utf-8")` guard so they run on any locale (including Windows `cp1252` runners).

## Contact

- Ideas & discussions: [GitHub Discussions / Issues](https://github.com/alvinluo-tech/hack2win/issues)
- Security: [luoyaosheng123@gmail.com](mailto:luoyaosheng123@gmail.com) — see [SECURITY.md](SECURITY.md)
