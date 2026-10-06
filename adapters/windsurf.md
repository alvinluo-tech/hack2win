---
name: hack2win
description: Hackathon & production full-stack orchestration engine. Activate for hackathon/黑客松/编程马拉松/参赛/builder contest/demo day/build an MVP from scratch (从0到1做个产品/根据主题出产品/找点子/准备demo或路演).
trigger: model_decision
---

# hack2win engine (Windsurf rule adapter)

1. Locate the skill home (default `~/.agents/skills/hack2win`). If missing, install: https://github.com/alvinluo-tech/hack2win
2. **Read `SKILL.md` at the skill home in full** and obey its 7-phase pipeline and red-lines; load `references/00–13` on demand via its routing table.
3. Before declaring done, run both mechanical gates and paste output:
   - `python <skill>/scripts/verify_project.py --project-path <app>`
   - `python <skill>/scripts/verify_production_complexity.py --project-path <app> --min-loc 4000`
4. Production floor: LOC ≥ 4,000 / ≥ 8 tables / ≥ 16 endpoints / ≥ 15 components / async worker. No toy demos.
5. UI: user-specified style is supreme; otherwise derive a physical metaphor (references/12). UI numbers must come from real backend state.
