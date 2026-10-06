# 技术选型决策法 · 初始化规范 · 企业级架构设计质量门(09)

> **定位**: 本文件规定大型复杂生产系统的高阶工程规范：
> 1. 多端呈现形式决策树 (Web / Desktop / Mobile / Extension / Hybrid)；
> 2. 实时动态版本号探测法则 (Live Versioning — 彻底消灭写死陈旧版本)；
> 3. 项目初始化工程规范 (脚手架 vs 手写判定)；
> 4. Clean Architecture / DDD 架构质量门 (深模块 Deep Modules、Seams 设计、依赖单向流向、防屎山硬预算)。

---

## 一、多端呈现形式与技术选型决策引擎 (P3 选型 ADR)

总控层不预设答案，预设**严谨的第一性原理权衡推演过程**。

### 1. 多端呈现形式决策矩阵 (Form Factor Decision Matrix)
在确定技术栈前，首先推演业务的**最佳交互物理载体**，严禁不假思索默认做成网页：

| 呈现形态 | 适用业务场景与核心特征 | 官方推荐技术栈 | 对应编排技能 |
|---|---|---|---|
| **Web 云端工作台** | 绝大多数企业级 SaaS、B2B 控制台、跨平台免安装体验、低阻力评委快速验收 | **Next.js 15/16+ (App Router, React 19) + Tailwind CSS v4** | `design-taste-frontend` |
| **桌面端应用 (Desktop)** | 需底层系统权限(全局热键/屏幕录制/本地文件树)、极低延迟本地模型/GPU 推理、系统托盘常驻守护、无浏览器沙盒网络限制 | **Tauri 2+ (Rust 后端 + 现代 Web 前端，安装包 < 15MB，内存 < 60MB)** | `tauri`, `tauri-development` |
| **移动端应用 (Mobile)** | 强依赖手机随身性、高频摄像头扫码、GPS 定位、重度离线手持操作 | **React Native / Expo (TS) 或 Flutter** | 移动端专用脚手架 |
| **浏览器插件 (Extension)** | 寄生于用户现有工作流(如在 GitHub 页面自动加审核插件、在 Twitter/邮件页面做内嵌助手) | **WXT (Next-gen Web Extension Framework) / Plasmo (React)** | WebExtension 规范 |
| **跨端混合协同 (Hybrid)** | 系统分为“本地轻量执行器/数据采集守护者”与“云端协同管控中心”(如 Voodo 模式) | **Tauri/Python 本地守护进程 + Next.js 云端大盘 (WebSocket 通信)** | `tauri` + `hack2win` |

### 2. 实时动态版本号探测法则 (Live Versioning Law — 严禁写死陈旧版本)
AI 开发最致命的通病是**机械套用训练语料中的旧版本号**（如曾经反复出现的 Next 14、React 18、Tailwind 3、Pydantic 1）。
**在生成任何 `package.json`、`requirements.txt` 或 `Cargo.toml` 之前，必须执行动态注册表版本探测**：
```bash
# 1. Node/npm 生态探测 (实时获取当前正式最新稳定版本)
npm view <package-name> dist-tags.latest
# 示例: npm view next dist-tags.latest -> 16.x.x
# 示例: npm view tailwindcss dist-tags.latest -> 4.x.x

# 2. Python/PyPI 生态探测
powershell -Command "(Invoke-RestMethod 'https://pypi.org/pypi/<package-name>/json').info.version"
# 示例: pydantic -> 2.x.x, sqlalchemy -> 2.x.x

# 3. Rust/Crates 生态探测
cargo search <crate-name> --limit 1
```
- **禁止硬编码历史版本**：根据探测结果，生成当前年度最前沿、经过生态兼容验证的生产级版本配置。

### 3. 选型四步法与五维加权矩阵
1. **约束扫描**: 赛制时长、目标部署平台、云账号限制、赞助商强制技术项。
2. **多候选方案调研 (≥ 2-3 套)**: 提出至少 2 套切实可行的架构组合（如方案 A: Web 自建 vs 方案 B: 桌面 Tauri + 本地推理）。
3. **五维加权矩阵量化打分**:
   - 迭代速度 ($\times 3$)、部署运维 ($\times 2$)、运行成本 ($\times 2$)、生态成熟度 ($\times 2$)、技术熟悉度 ($\times 2$)。
4. **Spike 快速验证 (15-30分钟)**: 对得分最高方案的关键依赖跑通最小可用性探测。
5. **落盘 ADR 架构决策记录**: 单点维护于 `app/docs/adr/0001-stack-choice.md`，明确记录决策依据、备选与回头条件。

---

## 二、项目初始化规范: 脚手架 vs 手写

| 场景分类 | 初始化方式 | 决策依据与工程规范 |
|---|---|---|
| **Web 前端 (Next.js)** | **官方最新脚手架**:<br>`npx create-next-app@latest frontend --typescript --tailwind --eslint --app --no-src-dir --use-npm --yes` | 构建工具链、TS/ESLint 规则、SWC 编译器配置手动编写极易遗漏；安装后立即执行 `npm run build` 确立全绿基线，并**当场删除脚手架自带的无用样板页、图标与示例样式**。 |
| **桌面应用 (Tauri)** | **官方脚手架**:<br>`npm create tauri-app@latest` (引用 `tauri` 技能) | 自动配置 Rust `src-tauri` Cargo 依赖、权限能力配置 (Capabilities) 与 Web 前端模版。 |
| **工业级后端 (FastAPI)** | **手写分层架构目录**:<br>按 08 §3 标准层次创建 | 社区脚手架良莠不齐，手动创建 `core/`, `models/`, `repositories/`, `services/`, `workers/`, `api/` 保证结构完全受控并锁定依赖版本。 |
| **网络受限 / 脚手架失败** | **手写最小可编译骨架**:<br>手动组织 package.json + tsconfig | 重试超过 2 次坚决降级，先保证 `npm run build` 通过，再逐步迁入依赖。 |

---

## 三、Clean Architecture、深模块与防屎山架构设计质量门 (Anti-Spaghetti Protocol)

随着代码量迈入数千至数万行，必须通过**深模块 (Deep Modules) 隔离**与**严格依赖单向流向**抵御代码腐化：

```
                      ┌───────────────────────────────────────────┐
                      │    Presentation Layer (API Routers, DTOs) │
                      └─────────────────────┬─────────────────────┘
                                            │ 依赖向下调用
                                            ▼
                      ┌───────────────────────────────────────────┐
                      │  Application Layer (Use Cases, Workflows) │
                      └─────────────────────┬─────────────────────┘
                                            │ 依赖向下调用
                                            ▼
                      ┌───────────────────────────────────────────┐
                      │   Domain Layer (Entities, State Machines) │
                      └─────────────────────┬─────────────────────┘
                                            │ 依赖接口反转 (Inversion)
                                            ▼
                      ┌───────────────────────────────────────────┐
                      │ Infrastructure Layer (Repo, DB, Workers)  │
                      └───────────────────────────────────────────┘
```

### 1. 深度整合领域架构技能
- **深模块与接口接缝设计 ➔ 强制引用 `codebase-design`**:
  - **深模块原则 (Deep Module)**: 模块的公共表面积必须极小（Narrow Interface），而隐藏在其后的功能与复杂度必须极大（Deep Implementation）；
  - **接缝设计 (Seams)**: 寻找系统天然的解耦边界（如：存储接缝、网络通信接缝、模型推理接缝），严禁为了抽象而抽象伪造假接缝（必须通过 `Deletion Test`：如果删掉这个抽象接口，调用方是否变得更清晰？如果变清晰，则是假接缝，坚决删除！）；
- **TypeScript 依赖屏障硬隔离 ➔ 强制引用 `setup-ts-deep-modules`**:
  - 在大型 TS 工程中引入 `dependency-cruiser` 规则：
    1. 每个包只能通过根目录的 entry-point（如 `index.ts`, `client.ts`）对外暴露，子目录（`lib/`, `internal/`）一律对外私有化；
    2. 禁止深层跨包导入内部实现；
    3. 严禁循环依赖（Circular Dependencies，违者编译直接报错）；
    4. 禁止滥用大桶文件（Barrel files `index.ts` 重新到处整个目录树），保持依赖树扁平轻量。
- **领域建模与通用语言 ➔ 强制引用 `domain-modeling`**:
  - 维护 `app/CONTEXT.md`，定义业务无歧义的核心词汇表；
  - 每一个重大架构调整记录为一份标准 ADR。

### 2. 严格依赖单向流向
- **Presentation (API 控制器)**: 只负责参数校验、反序列化、调用 Service 并返回标准响应信封。路由层严禁书写业务运算或直接发起裸 SQL 查询。
- **Application (用例服务)**: 组织业务工作流、事务生命周期、调度后台异步 Worker、记录审计日志。
- **Domain (领域核心)**: 包含 ORM 实体、值对象、状态机校验器与纯业务算法。不依赖任何外部框架实现。
- **Infrastructure (基础设施)**: 数据库会话、仓储实现、Redis 缓存、外部 API 客户端。

### 3. 仓储模式与事务工作单元 (Repository & Unit of Work)
- 严禁在业务逻辑中散落 `db.query()` 或散碎提交；
- 建立泛型基类 `BaseRepository[ModelType]`，统一封装基础 CRUD、软删除与分页；
- 复合写操作通过事务工作单元确保原子性（要么全成功，要么全回滚）。

### 4. 异步任务与后台 Worker 解耦模式
- 耗时超过 500ms 的外部 API 调用、大文件处理或 AI 推理，一律进入异步队列 (Worker)；
- 接口立即返回 `task_id`，前端通过 SSE 或轮询追踪时间线；任务具备幂等键防止重复消费。

### 5. 状态机驱动核心业务流 (State Machine Pattern)
- 状态转移表驱动，禁止随意赋字符串状态；
- 转移前执行校验钩子，非法转移拦截并抛出领域异常，合法转移记录审计日志。

### 6. 硬性代码预算与架构自查六问
- **单文件预算**: 单文件 ≤ 300 行；单个业务函数 ≤ 50 行（含文档）；单个路由文件 ≤ 8 个 endpoint。
- **架构自查六问**:
  1. 新增一个业务模块，改动是否局限在该模块的独立目录下？
  2. 更换底层数据库或外部 API，Service 层的业务代码是否零修改？
  3. 新协作者只读目录树与 README，能否在 30 秒内精准找到编写业务用例的位置？
  4. 是否存在超过 300 行的“上帝类”或“胖控制器”？
  5. 核心业务函数的每个异常分支是否都有对应的测试覆盖与结构化错误响应？
  6. 耗时操作是否全部解耦至后台异步 Worker，HTTP 主线程是否存在阻塞风险？

### 7. 领域数学模型与单调性自检 (Domain Invariants & Mathematical Soundness)
- **单调性公理 (Monotonicity)**: 任何正向业务行为（如成功交付、获赞）必须在数学上单调递增或保持指标（$\Delta \text{Metric} \ge 0$），严禁“越做分越低”的逻辑倒挂；
- **有界性与平滑更新 (Boundedness & Bayesian Smoothing)**: 数值严格限定在定义域内，采用贝叶斯平滑公式更新；
- **守恒性公理 (Conservation Laws)**: 资金、点数转移必须满足借贷守恒（$\sum \text{Debits} + \sum \text{Credits} = 0$）。
- 配备专用单元测试断言核心不变量。

### 8. 单向真值源与事件驱动视图架构 (Single Source of Truth & Visual Projections)
- 3D 动画、体素世界、粒子、图表与 HUD，必须严格作为领域事件 (`DomainEvent`) 的纯函数投影；
- 严禁视图层生成独立的伪数值或假硬编码动画，真值源唯一。
