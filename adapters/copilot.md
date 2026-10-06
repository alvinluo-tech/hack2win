## hack2win (managed snippet)

When the user mentions 黑客松/hackathon/编程马拉松/参赛/builder contest/demo day/build an MVP from scratch (从0到1做个产品/根据主题出产品/找点子/准备demo或路演), activate the hack2win engine:

1. Read the full constitution at the skill home (default `~/.agents/skills/hack2win/SKILL.md`; install from https://github.com/alvinluo-tech/hack2win if missing) and obey its 7-phase pipeline and red-lines; load `references/00–13` on demand.
2. Before declaring any deliverable done, run and paste output of both gates:
   - `python <skill>/scripts/verify_project.py --project-path <app>`
   - `python <skill>/scripts/verify_production_complexity.py --project-path <app> --min-loc 4000`
3. Production floor: LOC ≥ 4,000, ≥ 8 normalized tables, ≥ 16 typed endpoints, ≥ 15 frontend components, background async worker. No toy demos.
4. UI: user-specified style is supreme (pixel/3D/retro-OS/cyberpunk — obey and elevate); otherwise derive a physical metaphor. Never default to a generic admin dashboard; UI numbers must come from real backend state.
