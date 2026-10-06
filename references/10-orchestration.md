# 技能编排机制 (10) — 总控层领域能力分发与深度生态协同

> **定位声明**: `hack2win` 是总控层开发引擎 (Orchestrator)。
> 它绝不试图在单一提示词中重新发明所有的软件工程领域轮子。它的核心职责是：**流程调度与决策 (P0-P6)、生产交付契约 (08/09/11)、机械化双重验收门、以及高阶领域技能的精准编排**。
> UI 设计、深模块解耦、领域建模、测试驱动、桌面开发、架构重构等专业能力，**一律优先检索并深度引用系统已安装的专门技能**。
> 引用不是形式主义的“念咒语”，而是**必须严格执行被引用技能所规范的专业工程步骤，并将关键中间产物与证据原样归档**！

---

## 一、引用外部专门技能的三种机制 (Orchestration Modalities)

按上下文与任务场景选择最合适的方式：

1. **模态 A: Skill 工具直接触发 (Tool Invocation)**:
   - 当技能在宿主可用工具清单中时，直接通过 Skill 工具调用（如调用 `Skill(skill="codebase-design")` 或 `Skill(skill="tdd")`）。
2. **模态 B: 直接研读目标技能的 `SKILL.md` 执行其标准流程 (Direct Spec Reading - 最通用可靠)**:
   - 在主流程到达对应阶段时，直接使用 `Read` 工具读取目标技能规范文件（跨平台通用路径）：
     `~/.agents/skills/<skill-name>/SKILL.md` (Linux / macOS: `$HOME/.agents/skills/...`; Windows: `%USERPROFILE%\.agents\skills\...`)
   - **严格按照该技能的指令、目录规范与步骤执行**（例如读取 `setup-ts-deep-modules` 后，立即安装 `dependency-cruiser` 并生成 `.dependency-cruiser.cjs` 依赖边界规则）。
3. **模态 C: 派发携带专业技能任务书的子代理 (Sub-agent Delegation)**:
   - 当任务属于解耦的并行模块（如独立编写 ORM 模型、编写独立前端组件、执行独立压力测试）时，派发专属子代理，任务书中明确包含目标技能的路径与验收标准。

**冲突裁决准则**: 若被引用技能与本技能的契约冲突（例如某外部 UI 技能建议做成单文件纯前端，而本技能在 P3 宣布了 T2 全栈），**无条件以本技能的生产级契约与架构质量门为最高准则**，并将冲突与裁决原因记录在 devlog 中。

---

## 二、本机专门技能注册表 (Orchestration Skill Registry)

已在环境实盘核验，绝对真实可用：

| 领域分类 | 专门技能名称 | 本地规范路径 | 触发时机与深度执行指引 |
|---|---|---|---|
| **架构解耦** | `codebase-design` | `~/.agents/skills/codebase-design/SKILL.md` | **P4 架构设计前必读**: 识别系统天然接缝 (Seams)，设计狭窄接口深层实现 (Deep Modules)，运用 `Deletion Test` 剔除多余的假抽象。 |
| **TS依赖屏障** | `setup-ts-deep-modules` | `~/.agents/skills/setup-ts-deep-modules/SKILL.md` | **大型 TS 前端/全栈必用**: 安装 `dependency-cruiser`，强制执行 4 条硬规则（仅允许根目录 entry-point 暴露、子目录内部私有化、禁止深层穿透导入、禁止循环依赖、禁止大桶文件 Barrel）。 |
| **领域建模** | `domain-modeling` | `~/.agents/skills/domain-modeling/SKILL.md` | **P3 产品定义必用**: 建立业务无歧义的通用语言，输出 `app/CONTEXT.md` 统一词汇表；架构决策按 ADR 标准格式归档。 |
| **架构重构** | `improve-codebase-architecture` | `~/.agents/skills/improve-codebase-architecture/SKILL.md` | **M3/M4 阶段体检**: 扫描代码库的深化重构机会，消除过度暴露与浅模块。 |
| **桌面端交付** | `tauri` / `tauri-development` | `~/.agents/skills/tauri/SKILL.md` | **选型为桌面应用时必用**: 遵循 Rust IPC 接口规范 (`#[tauri::command]`)，配置系统 Capabilities 与 Web 前端集成。 |
| **前沿 UI 美学** | `design-taste-frontend` | `~/.agents/skills/design-taste-frontend/SKILL.md` | **P5 视觉工程必用**: 注入反模板化设计语言、定制色阶系统、微动效与 typography，彻底消除业余感。 |
| **测试驱动开发** | `tdd` | `~/.agents/skills/tdd/SKILL.md` | **核心业务与状态机必用**: 测试先行，红-绿-重构循环；强制将第一轮失败输出（红）原样记录在 devlog。 |
| **端到端测试** | `typescript-e2e-testing` | `~/.agents/skills/typescript-e2e-testing/SKILL.md` | **P4 验收阶段**: 基于 Given-When-Then 模式，使用真实容器基础设施执行端到端全流程断言。 |
| **AI输出回归** | `ai-regression-testing` | `~/.agents/skills/ai-regression-testing/SKILL.md` | **含 AI 能力的项目必用**: 建立基准测试用例集，防止模型调优或 Prompt 变更导致输出质量雪崩。 |
| **工程质量闸** | `setup-pre-commit` | `~/.agents/skills/setup-pre-commit/SKILL.md` | **M4 生产加固**: 配置 Git 提交前自动执行代码格式化、类型检查与单测。 |
| **全仓代码审查** | `code-review` | `~/.agents/skills/code-review/SKILL.md` | **P6 提交前最后一道防线**: 逐模块扫描安全隐患、内存泄漏与规范违规。 |
| **紧急排障** | `diagnosing-bugs` / `triage` | `~/.agents/skills/diagnosing-bugs/SKILL.md` | **构建或演示翻车时**: 快速定位根因、最小化复现并实施修复。 |
| **技能发现扩充** | `find-skills` | `~/.agents/skills/find-skills/SKILL.md` | **能力缺失时**: 搜索并发现新的开源技能。 |

---

## 三、缺失技能的动态检索、安装与兜底机制

当项目遇到特定的前沿领域（如区块链智能合约、音视频底层处理、特定的云平台 SDK），且注册表中未包含时：

1. **第一步: 运行技能盘点脚本**:
   ```bash
   # 跨平台通用 Python
   python scripts/list_skills.py
   # 或 Windows PowerShell
   powershell -File scripts/list-skills.ps1
   ```
2. **第二步: 使用 `find-skills` 或语义检索网络**:
   - 检索 GitHub 官方或开源社区的相关专业技能。
3. **第三步: 安全代理安装**:
   - 国内网络走 `gh-proxy` 镜像克隆（跨平台安装至用户技能目录）：
     ```bash
     git clone --depth 1 https://gh-proxy.com/https://github.com/<owner>/<skill-repo> ~/.agents/skills/<skill-name>
     ```
   - 验证安装后目录存在 `SKILL.md` 且名称一致。
4. **第四步: 零依赖自建兜底 (使用 `skill-creator`)**:
   - 若外部技能无法下载，调用本地 `skill-creator` 插件，现场提炼该领域的 20-30 行微规范，保存于 `~/.agents/skills/<custom-skill>/SKILL.md`，并在 devlog 中注明“自建临时技能”。

---

## 四、七阶段流水线中的技能编排执行矩阵 (Execution Matrix)

总控层在推动七阶段流水线时，**必须在特定节点主动调用或研读对应技能，严禁闭门造车**：

```
P0 命题解码 & P2 市场调研
   ├── 引用 `research`: 展开三轮对抗性辩证调研 (全景扫描 -> 红队压力 -> 护城河)
   └── 引用 `domain-modeling`: 确立赛道业务领域词汇，开始起草 `app/CONTEXT.md`
         │
P3 产品定义 & 架构选型
   ├── 引用 `09-tech-architecture`: 运行动态版本号探测 (Live Versioning) 与多端形式决策 (Web/Tauri/Mobile)
   ├── 引用 `domain-modeling`: 记录架构决策并落地首份 `app/docs/adr/0001-stack-choice.md`
   └── 若选型为桌面端 ➔ 深入研读 `tauri` 与 `tauri-development`
         │
P4 快速构建 (万行级装配)
   ├── 初始化: 前端大型工程 ➔ 研读 `setup-ts-deep-modules` 安装 dependency-cruiser 锁死包隔离边界
   ├── 领域核心与状态机: 强制引用 `tdd` ➔ 测试先行 (先写 failing test 留证，再写实现，再重构)
   ├── 模块设计与接缝: 研读 `codebase-design` ➔ 设计 Narrow Interface 与 Deep Implementation，通过 Deletion Test
   ├── 质量加固: M3 末尾研读 `improve-codebase-architecture` 扫描深模块重构机会
   └── 自动化验收: 研读 `typescript-e2e-testing` 编写真实设施 E2E 增量断言脚本
         │
P5 企业级 UI 打磨
   ├── 深入研读 `design-taste-frontend`: 注入反模板化设计语言、色阶系统、微动效与 Typography
   └── 运行 `ui-shot.ps1` 与 `ui-audit-components.mjs`: 执行至少 2 轮视觉验收环与组件级无裁切审计
         │
P6 路演与交付
   └── 最终提交前 ➔ 触发 `code-review`: 执行全仓代码审查，清退 TODO 与潜在漏洞
```

---

## 五、技能编排记录留痕标准 (devlog 固定规范)

在 `04-devlog.md` 中，必须设立专属的 `## 技能编排与领域协同记录` 小节，真实记录调用过程：

```markdown
## 技能编排与领域协同记录

1. **domain-modeling**:
   - 研读路径: `~/.agents/skills/domain-modeling/SKILL.md`
   - 采纳观点: 建立通用语言体系，将核心实体与领域事件解耦定义在 `app/CONTEXT.md`；完成了 2 份标准 ADR。
2. **setup-ts-deep-modules**:
   - 研读路径: `~/.agents/skills/setup-ts-deep-modules/SKILL.md`
   - 执行操作: 配置了 `.dependency-cruiser.cjs`，强制执行 Entry-point 边界隔离，禁止内部子模块跨包随意深层 import。
3. **tdd**:
   - 研读路径: `~/.agents/skills/tdd/SKILL.md`
   - 执行过程: 针对结算状态机 `settle_payout` 先编写了 3 条失败测试，记录了红阶段输出；实现逻辑后重跑全绿；单调性测试通过。
4. **design-taste-frontend**:
   - 研读路径: `~/.agents/skills/design-taste-frontend/SKILL.md`
   - 采纳观点: 摒弃默认浅灰背景，引入深空黑与高对比度数据微芯片，重构了 KPI Sparklines 看板。
5. **冲突裁决**:
   - 外部技能 X 建议采用单文件简化演示，与本技能 T2 全栈生产标准契约冲突，依据总控优先级裁决坚决遵循 T2 规范。
```

**考核标准**: 评委与用户审查时，能够清晰看到总控层像交响乐指挥家一样，在正确的乐章调动了正确的专业乐手，将整个大型项目推向工业级顶峰。
