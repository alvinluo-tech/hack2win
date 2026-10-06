# AGENTS.md — hack2win multi-agent entry point

This file follows the [agents.md](https://agents.md) convention, read natively by **OpenAI Codex**, **OpenCode**, **Jules**, **Factory**, **Amp**, **Zed**, and other compatible agents.
Claude Code / ZCode / OpenClaw users: the canonical skill lives at [`SKILL.md`](SKILL.md) — same engine, discovered via the skills mechanism.

## When to activate

Activate this engine whenever the user mentions: 黑客松 / hackathon / 编程马拉松 / builder contest / demo day / 参赛 / 找点子 / 头脑风暴 / 根据主题出产品 / 从 0 到 1 做个 MVP / prepare a demo or pitch — even casually ("帮我参加 XX 比赛").

Do NOT activate for: long-cycle enterprise R&D without a timebox, or pure fundraising documents.

## Mandatory protocol (non-negotiable)

1. **Read [`SKILL.md`](SKILL.md) in full before doing anything.** It is the orchestrator constitution (7-phase pipeline, iteration engine, 24 failure red-lines). Follow its routing table into `references/00`–`13` on demand.
2. **Dual mechanical gates before delivery**: run
   `python scripts/verify_project.py --project-path <app>` then
   `python scripts/verify_production_complexity.py --project-path <app> --min-loc 4000`.
   Exit code must be `0` for both. Self-reported completion without gate output is forbidden.
3. **Complexity floor**: production deliverables require LOC ≥ 4,000, ≥ 8 normalized tables, ≥ 16 typed endpoints, ≥ 15 frontend components, and a background async worker. Toy demos are rejected.
4. **User-Intent Supremacy on UI**: if the user names a visual style (pixel town, 3D voxel world, retro Win98, cyberpunk terminal), obey it 100% and elevate it with authentic details. When unspecified, derive a physical metaphor via `references/12-winning-ui-patterns.md`. Never default to a generic admin dashboard.
5. **Truth discipline**: every metric rendered in the UI must be a projection of real backend state (no hardcoded fake numbers); every claim in reports needs command output or screenshot evidence in the devlog.

## Fast command map

| Need | Read |
|---|---|
| Decode theme & rubric | `references/00-theme-decode.md` |
| Ideate (8 lenses) | `references/01-brainstorm.md` |
| 3-round adversarial research | `references/02-market-research.md` |
| Product spec & metaphor | `references/03-product-definition.md` |
| Build pipeline M0–M4.5 | `references/04-build-playbook.md` |
| UI polish & clipping audits | `references/05-polish.md` |
| Pitch & submission | `references/06-pitch-submit.md` |
| Complexity floor / anti-toy | `references/08-production-standard.md` |
| Clean Architecture gates | `references/09-tech-architecture.md` |
| Skill orchestration registry | `references/10-orchestration.md` |
| 8-subsystem assembly | `references/11-enterprise-complexity-architecture.md` |

## Install for your agent

```bash
git clone https://github.com/alvinluo-tech/hack2win.git
cd hack2win && ./install.sh        # macOS / Linux / Git Bash
# or on Windows:
powershell -ExecutionPolicy Bypass -File install.ps1
```

The installer auto-detects installed agents (Claude Code, Codex, Cursor, Windsurf, ZCode, OpenCode, Copilot) and wires hack2win into each. See `adapters/` for per-tool formats.
