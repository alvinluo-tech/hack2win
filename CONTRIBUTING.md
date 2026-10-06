# Contributing to hack2win

Thank you for your interest in contributing to **hack2win**! We are building the open standard for autonomous, production-grade AI hackathon engineering and full-stack MVP orchestration.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## How Can I Contribute?

### 1. Reporting Bugs
- Check existing [Issues](https://github.com/alvinluo-tech/hack2win/issues) to ensure the bug hasn't already been reported.
- Open a new issue using the [Bug Report Template](.github/ISSUE_TEMPLATE/bug_report.md).
- Include minimal reproducible steps, agent runtime (Claude Code / OpenClaw / Cursor / Windsurf), and CLI script outputs.

### 2. Suggesting Reference Patterns
Have you reverse-engineered a winning UI metaphor or a bulletproof architectural invariant from a recent major hackathon?
- Open a Feature Request issue detailing:
  - Hackathon name & year
  - Winning project link / repo
  - The architectural or visual invariant that secured the win
  - Proposed additions to `references/12-winning-ui-patterns.md` or `references/13-winning-knowledge.md`

### 3. Submitting Pull Requests
1. Fork the repo and create your branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Keep documentation strictly modular:
   - Reference manuals must live under `references/` with strict two-digit numbering prefixes.
   - All internal links must be relative.
3. Test all CLI scripts locally:
   ```bash
   python scripts/list_skills.py
   python scripts/verify_project.py --help
   python scripts/verify_production_complexity.py --help
   ```
4. Commit with clear, conventional commit messages:
   ```bash
   git commit -m "feat(ui): add 3D voxel physics pattern to reference 12"
   ```
5. Push to your fork and submit a Pull Request.

## Coding Style & Standards
- **Python**: PEP 8 compliant, Python 3.10+ compatible, zero mandatory third-party dependencies for core scripts under `scripts/`.
- **Markdown**: Clear headings, Mermaid diagrams where architecture flows, and accurate cross-platform terminal snippets.
- **Language**: English in `README.md`, Chinese in `README_zh.md`. Keep headings and anchors strictly synchronized.
