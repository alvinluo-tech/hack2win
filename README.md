# 🏆 hack2win

<div align="center">

**The Autonomous Production-Grade Hackathon & Full-Stack MVP Orchestration Skill for AI Coding Agents**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-green.svg)](https://www.python.org/)
[![Node.js 18+](https://img.shields.io/badge/Node.js-18%2B-brightgreen.svg)](https://nodejs.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey.svg)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

*From multi-round dialectic research to 10k+ LOC full-stack engineering, immersive UI metaphors, and automated production gates — in hours.*

</div>

---

## 🌟 Why hack2win?

Most hackathon demos built by AI agents suffer from **"Toy Demo Syndrome"**:
- **Fragile Architecture**: 1-2 flat database tables, monolithic controllers, and synchronous blocking calls.
- **Surface-Level Thinking**: Single-pass prompt brainstorms resulting in generic chatbots or trivial wrappers.
- **Templetized UIs**: Boring, cookie-cutter admin dashboards that fail to captivate judges within the critical first 30 seconds.
- **False Green Tests**: Shallow existence tests (`toBeVisible()`) that hide frozen, unreactive UI state and broken endpoints.

**hack2win** turns your AI agent into an **elite engineering team lead and product strategist**:
1. **Production-First + Demo Extraction**: Designs robust, multi-tenant, 8-subsystem architectures, and extracts a dazzling, flawless 3-minute golden path for judges.
2. **Three-Round Adversarial Research**: Dialectic pipeline (Landscape Sweep ➔ Red-Team Graveyard Analysis & Thesis vs. Antithesis ➔ Synthesis & Unfair Moat).
3. **Adaptive Form Factor & Live Versioning**: Scientific choice among Web, Desktop (Tauri 2+), Mobile, Extension, and Hybrid; dynamically queries package registries for current stable LTS releases instead of using outdated hardcoded versions.
4. **Deep Modules & Clean Architecture**: Hard limit of ≤300 lines per file, strictly enforced seams via specialized domain skills (`codebase-design`, `setup-ts-deep-modules`, `domain-modeling`, `tdd`).
5. **Unbounded 4D Generative Interface Space**: Breaks free from standard dashboard templates. Prompts creative physical metaphors (2D pixel towns, Three.js 3D spatial worlds, retro Win98 consoles, infinite canvas, audio DAWs) with **User-Intent Supremacy**.
6. **State-Driven Visual Invariant**: Visuals (particles, floating numbers, HUD chips) are pure functional projections of backend domain events—eliminating fake animations.
7. **Dual Mechanical Gates**: Automated CLI audit tools (`verify-project` & `verify-production-complexity`) that fail with exit code 1 if a project falls below production standards.

---

## 🚀 Quick Start / Installation

### 1. Install as an Agent Skill

Cloning into your agent skills directory (works with Claude Code, OpenClaw, Cursor, Windsurf, ZCode, or custom agent runners):

```bash
# Standard cross-platform path (Linux, macOS, Windows)
git clone https://github.com/alvinluo-tech/hack2win.git ~/.agents/skills/hack2win

# Or for ZCode specific directory
git clone https://github.com/alvinluo-tech/hack2win.git ~/.zcode/skills/hack2win
```

### 2. Verify Your Environment

Run the cross-platform skills diagnostic:

```bash
# Python (Linux / macOS / Windows)
python ~/.agents/skills/hack2win/scripts/list_skills.py

# Or Windows PowerShell
powershell -File ~/.agents/skills/hack2win/scripts/list-skills.ps1
```

### 3. Usage with Your AI Agent

Simply instruct your coding agent:

```text
"I am participating in [Contest Name / Theme]. 
Use the hack2win skill to lead the entire project lifecycle from research to full-stack delivery."
```

If you have a specific UI concept in mind:
```text
"I want the UI to be a 3D interactive voxel world with day/night cycles using React Three Fiber. 
Follow hack2win to build a production-grade backend and database underneath."
```

---

## 🏛️ Architecture & Knowledge Base

`hack2win` is organized into a modular, progressive-disclosure specification tree:

```
hack2win/
├── SKILL.md                                        # Master Orchestrator Specification & Core Philosophy
├── LICENSE                                         # MIT License
├── README.md                                       # Documentation & Quickstart
├── references/
│   ├── 00-theme-decode.md                          # P0 Theme decoding, sponsor technology feasibility analysis
│   ├── 01-brainstorm.md                            # P1 Brainstorming (8 lenses, asymmetric wedge strategy)
│   ├── 02-market-research.md                       # P2 3-Round adversarial research & automated link-check
│   ├── 03-product-definition.md                    # P3 Form factor matrix, live versioning & physical metaphors
│   ├── 04-build-playbook.md                        # P4 M0-M4.5 staged assembly, delta verification, cold start
│   ├── 05-polish.md                                # P5 Dual-track UI polish, full UX crawl & clipping audits
│   ├── 06-pitch-submit.md                          # P6 Pitch narrative, demo video scripts, Q&A defense
│   ├── 07-judging-rubrics.md                       # Reverse-engineering judge scorecards (Devpost, MLH, Web3)
│   ├── 08-production-standard.md                   # Complexity floor (LOC, tables, endpoints) & Anti-Toy rules
│   ├── 09-tech-architecture.md                     # Clean Architecture, DDD, deep modules & math invariants
│   ├── 10-orchestration.md                         # Skill orchestration registry (codebase-design, tauri, tdd...)
│   ├── 11-enterprise-complexity-architecture.md    # 8-subsystem breakdown & Top open-source caliber standards
│   ├── 12-winning-ui-patterns.md                   # 4D generative interface space & physical metaphor extraction
│   └── 13-winning-knowledge.md                     # 30 verified case studies & winner post-mortems (self-contained)
└── scripts/
    ├── verify_project.py / .ps1                    # 17-point T2 full-stack structure & contract verification
    ├── verify_production_complexity.py / .ps1      # Complexity auditor (LOC >= 4k, tables >= 8, bundle <= 500k)
    ├── ui_shot.py / .ps1                           # Cross-platform automated screenshot tool with DOM assertion
    ├── list_skills.py / .ps1                       # Cross-platform local skills inventory checker
    └── exa-search.ps1                              # External semantic search adapter script
```

---

## 🛠️ Automated Quality Verification CLI

`hack2win` includes automated, zero-dependency Python 3 verification scripts runnable on Linux, macOS, and Windows:

```bash
# 1. Verify project structure & clean architecture contracts
python scripts/verify_project.py --project-path ./app

# 2. Audit production complexity (LOC, normalized tables, endpoints, bundle size)
python scripts/verify_production_complexity.py --project-path ./app --min-loc 4000

# 3. Automated cross-platform visual screenshot with DOM verification
python scripts/ui_shot.py --url "http://localhost:3000" --out-dir "./iterations/round-1" --expect-text "ProductName"
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/alvinluo-tech/hack2win/issues).

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
