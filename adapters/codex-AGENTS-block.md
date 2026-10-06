hack2win — Autonomous hackathon & production full-stack orchestration engine.
(Managed block appended by hack2win/install. Do not edit inside the markers.)

Activation: when the user mentions 黑客松/hackathon/编程马拉松/builder contest/demo day/
参赛/找点子/根据主题出产品/从 0 到 1 做个 MVP/prepare a demo — engage hack2win.

Protocol:
1. Read the full constitution at the skill home (default ~/.agents/skills/hack2win/SKILL.md;
   adjust if installed elsewhere) and obey its 7-phase pipeline and 24 red-lines.
   On-demand manuals live in references/00–13 relative to that SKILL.md.
2. Before declaring any deliverable done, run BOTH gates and paste their output:
   python <skill>/scripts/verify_project.py --project-path <app>
   python <skill>/scripts/verify_production_complexity.py --project-path <app> --min-loc 4000
3. Production floor: LOC >= 4000, >= 8 normalized tables, >= 16 typed endpoints,
   >= 15 frontend components, background async worker. No toy demos.
4. UI: user-specified style is supreme (pixel/3D/retro-OS/cyberpunk — obey and elevate).
   If unspecified, derive a physical metaphor per references/12. Never default to a
   generic admin dashboard.
5. UI-rendered numbers must be projections of real backend state — no hardcoded fakes.

(End of managed block)
