# 交付规模分级与生产级交付契约(08)

> **核心原则**: 坚决终结"几个 HTML+JS 文件"或"单表单接口"的玩具 Demo 思维。在黑客松及高标准工业化开发中，真正具有夺奖与商业落地价值的产物必须具备**生产级复杂度、完整系统分层、丰富业务交互与扎实的代码量级**(推荐 8,000 - 25,000+ LOC)。
> P3 结束时必须宣布交付等级;**T2 生产级全栈是默认且强制的基线**，深入场景直接向 **T3 商业化复杂系统** 对齐。

---

## 1. 三级定义与复杂度量化底线(Complexity Floor)

| 等级 | 定位与形态 | 硬性量化底线 (Floor) | 触发条件 |
|---|---|---|---|
| **T2 生产级全栈(默认)** | 工业级前后端分离体系(Next.js 15/16+ App Router, React 19 + FastAPI + PostgreSQL/SQLAlchemy + Alembic + 异步任务队列) | **代码量 ≥ 4,000 行(排除依赖)**<br>数据表 **≥ 8 张规范表**<br>API 端点 **≥ 16 个规范路由**<br>前端组件 **≥ 18 个独立组件**<br>完整后台布局壳 + 高级表格 + 异步后台任务 | **默认强制执行**，无需理由 |
| T3 商业化复杂系统 | T2 + 完整多租户(RBAC) + Docker Compose 5集群 + Redis 缓存 + 指标监控(Prometheus) + 审计日志 | **代码量 ≥ 10,000 - 25,000+ 行**<br>数据表 **≥ 12-16 张表**<br>端点 **≥ 25-35+ 个**<br>组件 **≥ 30-50+ 个**<br>独立业务视图 **≥ 6-10 个** | 商业化竞赛、大厂主赛道、一周赛制或决赛冲刺 |
| T1 轻量交付 (严控降级) | 纯前端单页应用或轻量演示 | 核心源码 < 2,000 行 | **严控**: 仅限剩余<6h 且环境完全受限时经 devlog 详细说明方可降级，否则直接判定违背契约 |

### T2 设为默认基线的四大不可辩驳依据
1. **真实落地性**: 商业投资人和黑客松顶级评委看重的是团队能否在赛后 2 周内将项目上线运营。没有多租户、没有状态流转历史、没有后台任务队列的单表项目，本质上只是幻灯片的动态翻页器，不具备任何技术护城河。
2. **AI 倍速时代的必然**: 随着 AI 编码能力飞跃，写 500 行代码的项目在评委眼里已形同零门槛。利用分阶段子代理编排，AI 能够在数小时内构建出数万行高质量分层代码，**生产级架构深度是拉开分数的关键胜负手**。
3. **消除评委审查穿帮**: 技术评委审查代码时，若发现后端无 Repository 分层、无异步队列、数据库无审计字段、前端全写在一个 `page.tsx` 里，会直接归类为"学生玩具"扣除全部技术实现分。
4. **架构可扩展性**: 规范的 Clean Architecture / DDD 分层结构，使得后续增设支付、短信、AI 批量流水线等业务时无需重构核心底座。

---

## 2. 生产级技术栈标准选型 (The Enterprise Production Stack)

| 层次 | 生产标准选型 | 深度选型依据与工业级特性 |
|---|---|---|
| **前端交互层** | **Next.js 15/16+ (App Router, React 19) + TypeScript (Strict) + Tailwind CSS v4 (@theme CSS-first) + Radix UI / shadcn/ui** | 企业级选型共识，服务端组件(RSC)+客户端交互解耦；React 19 异步特性与 Turbopack 秒级构建；Tailwind v4 零配置原生 CSS Tokens。 |
| **前端状态与请求** | **TanStack Query v5 + nuqs (类型化 URL 状态同步) + Zustand v5** | 统一服务端状态缓存、乐观更新、自动重试与窗口失焦刷新；nuqs 实现筛选、分页、排序与 URL 双向绑定；Zustand 管理轻量客户端会话与抽屉。 |
| **API 网关与服务** | **FastAPI + Pydantic v2 (Strict)** | 原生异步高性能，自动生成强类型 OpenAPI 规范；Pydantic v2 编译级校验性能；依赖注入(Depends)天然支持多租户与事务管理。 |
| **数据与持久化** | **PostgreSQL + SQLAlchemy 2.0 (Async) + Alembic** | 工业级 RDBMS；SQLAlchemy 2.0 强类型 `Mapped[T]` 语法；Alembic 严密版本迁移链；赛期本地若用 SQLite，强制 `aiosqlite` 并开启 WAL 模式 (`PRAGMA journal_mode=WAL; PRAGMA busy_timeout=5000;`)，防止并发锁库；部署切 Postgres。 |
| **异步队列与缓存** | **Redis + ARQ / Taskiq (原生异步队列) / SAQ (Celery 视为重型遗留选型)** | 原生集成 Python asyncio 与 Redis，解耦高耗时 AI 推理、数据大批处理与外部通知；支持分布式锁、任务进度持久化追踪与死信处理。 |
| **可观测与安全性** | **Structlog / Loguru + Prometheus (/metrics) + PyJWT[crypto] / authlib (替换废弃的 python-jose) + pwdlib[argon2,bcrypt] (替换废弃的 passlib)** | 请求 Correlation-ID 贯穿日志；Prometheus 性能监控指标；JWT 双 Token 轮换；CORS 严格白名单与速率限制(slowapi)。 |

---

## 3. 标准企业级项目结构 (The Enterprise Directory Hierarchy)

大型复杂项目禁止单层扁平堆砌，必须遵循 Clean Architecture 分层：

```
project-root/
├── frontend/                                # Next.js 15/16+ Enterprise Application (React 19, Tailwind v4)
│   ├── app/                                 # App Router 路由体系
│   │   ├── (auth)/                          # 认证路由组 (login, register, reset-password)
│   │   ├── (dashboard)/                     # 核心工作台路由组 (带统一后台布局壳)
│   │   │   ├── layout.tsx                   # 全局企业布局 (Sidebar + Header + Breadcrumbs)
│   │   │   ├── overview/                    # 业务大盘与 KPI 视图
│   │   │   ├── [resource]/                  # 核心资源 CRUD 列表与详情 (DataTable)
│   │   │   ├── workflows/                   # 多步业务向导与编排视图
│   │   │   ├── analytics/                   # 深度统计图表与报表
│   │   │   └── settings/                    # 租户、团队成员与审计日志视图
│   │   ├── api/                             # BFF 代理与客户端 Webhook
│   │   ├── globals.css                      # 全局 Design Tokens 与色阶变量
│   │   └── layout.tsx                       # 顶层 Providers (QueryClient, Theme, Toast)
│   ├── components/                          # 企业级组件系统
│   │   ├── ui/                              # Radix/shadcn 底层原子组件 (Button, Dialog, Dropdown...)
│   │   ├── layout/                          # 布局壳 (Sidebar, TopNav, CommandPalette, UserMenu)
│   │   ├── data-table/                      # 高级数据表格 (多列排序, 过滤芯片, 列配置, 导出)
│   │   ├── forms/                           # 复合表单与向导组件 (Zod Schema 校验)
│   │   └── charts/                          # Recharts/ECharts 交互式图表
│   ├── lib/                                 # 前端基础设施
│   │   ├── api-client.ts                    # Axios/Fetch 统一拦截封装 (自动注入 Token, 统一错误 Toast)
│   │   ├── auth.ts                          # 会话管理与权限守卫
│   │   └── utils.ts                         # 通用格式化与样式合并
│   ├── types/                               # 前端共享 TypeScript 类型契约
│   ├── .env.example                         # 完整环境变量清单
│   └── package.json + lockfile              # 锁定依赖
│
├── backend/                                 # FastAPI Enterprise Architecture (Clean Architecture / DDD)
│   ├── app/
│   │   ├── core/                            # 系统核心基建
│   │   │   ├── config.py                    # pydantic-settings 强类型环境配置
│   │   │   ├── security.py                  # JWT、密码加盐哈希、权限判定
│   │   │   ├── database.py                  # Async SQLAlchemy Engine 与 Session 会话工厂
│   │   │   ├── redis.py                     # Redis 连接池与缓存工具
│   │   │   ├── logging.py                   # Structlog / Loguru JSON 结构化日志配置
│   │   │   └── errors.py                    # 统一业务异常基类与全系统 Exception Handler
|   │   ├── models/                          # 8-15+ SQLAlchemy 关系实体 (ORM)
│   │   │   ├── base.py                      # UUID、时间戳、租户 ID、软删除基类
│   │   │   ├── tenant.py                    # Organization, Workspace 租户表
│   │   │   ├── user.py                      # User, Role, Permission 权限体系表
│   │   │   ├── [domain_entities].py         # 核心业务领域实体 (包含状态转移字段)
│   │   │   ├── audit.py                     # AuditLog 业务操作审计日志表
│   │   │   └── task.py                      # AsyncTask 异步任务追踪表
│   │   │   # ⚠️ 赞助商技术(如 Redis/向量库/云服务)的 Port 适配器必须实装且**至少真实运行一轮留日志**——
# │   │   │   │   "适配器写了但从未运行"在赞助商赛道=该栏零分(R12 评委实锤), SPONSOR_LIVE_CHECK 探测见 04 红线
│   │   ├── schemas/                         # Pydantic v2 DTO 传输对象 (严格分层)
│   │   │   ├── common.py                    # 分页响应 `PageResult[T]`、通用 Envelope
│   │   │   └── [domain_schemas].py          # Request / Response / Filter DTOs
│   │   ├── repositories/                    # 仓储与数据访问层 (Repository Pattern)
│   │   │   ├── base.py                      # 通用泛型仓储 (CRUD, 分页, 软删除过滤)
│   │   │   └── [domain_repo].py             # 领域专用复杂聚合查询与锁机制
│   │   ├── services/                        # 核心业务领域服务 (Use Cases & Business Rules)
│   │   │   ├── state_machine.py             # 业务状态机驱动引擎 (状态转移与校验)
│   │   │   ├── [domain_service].py          # 核心业务用例实现 (事务管理)
│   │   │   └── external_integrations.py     # 外部第三方 API 适配器
│   │   ├── workers/                         # 异步后台任务与队列 (Async Worker)
│   │   │   ├── celery_app.py / arq_worker.py# Worker 配置与进程入口
│   │   │   └── tasks.py                     # 异步计算、报告导出、批量处理任务
│   │   ├── api/                             # API 控制器与路由层
│   │   │   ├── deps.py                      # 依赖注入 (get_db, get_current_user, require_perm)
│   │   │   ├── v1/                          # API v1 路由模块
│   │   │   │   ├── auth.py                  # 登录、注册、刷新 Token
│   │   │   │   ├── users.py                 # 成员与权限管理
│   │   │   │   ├── [resources].py           # 核心业务 REST 端点 (CRUD, 批量, 状态转移)
│   │   │   │   ├── analytics.py             # 聚合统计与报表端点
│   │   │   │   └── tasks.py                 # 异步任务进度查询
│   │   │   └── router.py                    # 统一路由装配总入口
│   │   └── main.py                          # FastAPI 主应用入口 (中间件, 异常拦截, OpenAPI 配置)
│   ├── alembic/                             # 数据库版本迁移
│   │   ├── versions/                        # 迁移脚本列表
│   │   └── env.py
│   ├── tests/                               # 工业级自动化测试套件
│   │   ├── conftest.py                      # 测试夹具 (TestClient, In-Memory DB, Seed Fixtures)
│   │   ├── unit/                            # 领域单元测试 (状态机、算法逻辑)
│   │   └── integration/                     # 接口集成测试 (认证、CRUD 闭环、异常拦截)
│   ├── Dockerfile
│   ├── requirements.txt                     # 严密锁定版本号
│   └── .env.example
│
├── docker-compose.yml                       # 全栈一键编排 (Frontend, Backend, Worker, DB, Redis)
├── Makefile / start-all.ps1                 # 一键本地工程管理脚本
└── README.md                                # 生产级工程说明文档 (架构图, 部署步骤, 接口清单)
```

---

## 4. 生产级八大要素交付契约与反玩具底线 (Anti-Toy-Demo Criteria)

任何声称"已完成"的项目，必须对照以下八大要素硬性指标核查：

### 要素 1: 复杂关系型数据层 (≥ 8-15+ 张表)
- **合格标准**: 数据库表数量必须 ≥ 8 张，包含租户隔离、用户权限、多张业务核心实体、关联关系表、审计日志表与任务追踪表。
- **反玩具底线**: 严禁只有 1-2 张单表！严禁无外键级联约束！实体必须具备统一的时间戳、UUID/主键与软删除字段。必须附带生成 500-1000+ 条真实业务场景数据的 `seed.py`。

### 要素 2: 完整分层后端架构 (Clean Architecture / DDD)
- **合格标准**: 严格遵守 `Router -> DTO -> Service -> Repository -> Model` 依赖方向。路由层禁止编写业务算法或直接执行 SQL；核心状态转移必须有独立的状态机校验；数据库访问统一收拢至 Repository。
- **反玩具底线**: 严禁在 main.py 或路由函数中裸写几十行数据库操作！严禁无 DTO 强类型校验直接操作原始 dict！

### 要素 3: 异步任务处理与后台 Worker 引擎
- **合格标准**: 耗时操作(超过 500ms 的外部 API 交互、批量计算、报表生成)必须由后台 Worker 异步处理。接口立即返回 `job_id`，前端通过状态轮询或 SSE 追踪多步处理状态。
- **反玩具底线**: 严禁将重计算或外部阻塞式请求直接写在 HTTP Handler 中！

### 要素 4: API 网关、规范化响应与全局异常契约
- **合格标准**: 接口数量必须 ≥ 18 个。所有接口遵循统一的响应 Envelope：`{"code": 200, "data": ..., "message": "success", "trace_id": "..."}`。全局定义业务异常基类(`AppException`)，抛出统一错误码与用户可读错误信息。
- **反玩具底线**: 严禁发生未捕获的 500 堆栈泄漏！严禁部分接口返回字符串、部分接口返回对象的不一致格式！

### 要素 5: 真实可落地的多租户与 RBAC 权限设计
- **合格标准**: 系统原生支持 Organization / Workspace 隔离，所有业务数据带有 `workspace_id`；支持至少 3 种角色(Owner/Admin, Member, Viewer)与粒度权限拦截。
- **反玩具底线**: 严禁无权限区分、任何访问者随意修改全站数据的单机玩具设计！

### 要素 6: 企业级前端设计系统与完整布局壳 (Enterprise Layout Shell)
- **合格标准**: 前端具备现代 SaaS 级别的统一框架：左侧可折叠响应式导航栏、顶部工作区切换、全局搜索与指令面板(`Cmd+K`)、面包屑导航、用户状态栏；核心列表页面必须采用高级 DataTable(多列排序、条件过滤、分页器、列显隐、批量操作)；核心业务采用多步向导(Wizard)驱动。
- **反玩具底线**: 严禁简单用 `flex-col` 堆砌一个大卡片就算完整前端！严禁缺少加载态(Skeleton)与空状态(EmptyState)！

### 要素 7: 深度可观测性与缓存策略
- **合格标准**: 每次 HTTP 请求在中间件自动注入 UUID `X-Correlation-ID`，日志输出结构化 JSON 并携带此 ID；只读高频业务接口集成 Redis 缓存或本地 LRU 缓存；后端挂载 `/health` 探针检查 DB/Redis 连接状态，挂载 `/metrics` 供性能分析。
- **反玩具底线**: 严禁全站使用裸 `print()` 打印调试信息！严禁健康检查无条件写死 `{"status": "ok"}`！

### 要素 8: 自动化测试套件与容器化集群
- **合格标准**: 单元与集成测试用例必须 ≥ 15 个，真实覆盖业务核心分支与边界异常；根目录提供一键拉起完整集群的 `docker-compose.yml`(涵盖 frontend, backend, worker, postgres, redis)以及一键跨端自启的脚本。
- **反玩具底线**: 严禁只有 1 个简单的 test_health 测试！严禁无法通过标准 Docker 编译构建！

### 要素 8: 自动化测试套件与容器化集群
- **合格标准**: 单元与集成测试用例必须 ≥ 15 个，真实覆盖业务核心分支与边界异常；根目录提供一键拉起完整集群的 `docker-compose.yml`(涵盖 frontend, backend, worker, postgres, redis)以及一键跨端自启的脚本。
- **反玩具底线**: 严禁只有 1 个简单的 test_health 测试！严禁无法通过标准 Docker 编译构建！

---

## 5. 跨越玩具缺陷的四大第一性原理工程铁律 (The 4 First-Principle Engineering Laws)

通过数十轮真实验证与终审对抗性审计，提炼出阻止系统发生“高光时刻脱节、虚假合规、逻辑崩溃”的四大底层第一性原理铁律：

### 铁律 1: 单向真值源投影律 (State-Driven Visual Invariant)
- **底层病灶**: 开发者往往将 3D/动画/微交互视作“前端皮囊”，而将后端视作“数据逻辑”，导致动画中的浮字、粒子爆发、状态指示使用硬编码常量或本地伪状态（如 R12 中实际结算 +131，但 3D 浮字硬编码 `+120 cr` 且爆点固定在第一栋楼；顶栏余额仅在挂载时取数导致账面不跳动）。
- **第一性法则**: **任何视觉反馈必须是领域事件 (`DomainEvent`) 的纯函数投影**！
  1. 3D 世界或界面的所有动效触发（小人行走、金币喷涌、状态牌变色），必须订阅来自 API 轮询或 SSE 的真实事件载荷（携带 `job_id`, `building_id`, `actual_payout`）；
  2. 严禁在 JSX/动画渲染函数中硬编码任何金额、统计数字或固定实体引用；
  3. 全局数据芯片（如顶栏余额、活跃任务数）必须与全站状态同步总线（Zustand Store / React Query Cache）绑定，在操作完成后立即响应，严禁要求用户手动 F5 刷新才能见真实账面。

### 铁律 2: 领域数学模型与单调性自检律 (Mathematical Invariants & Monotonicity Testing)
- **底层病灶**: 编写核心算法（定价公式、员工评分、声誉、质量衰减、对账结算）时凭直觉写随意公式，缺乏数学不变量约束（如 R12 中 `quality = 0.55 + jobs_done * 0.01` 整体覆写，导致初始 0.78 的高分员工接单越多评分反而降到 0.61）。
- **第一性法则**: **所有核心数值算法必须在领域层明确声明数学不变量并在单元测试中严密断言**！
  1. **单调性约束 (Monotonicity)**: 例如“高质量成功交付必定增加或维持 Agent 评分，绝不可产生反向惩罚”；
  2. **数值边界约束 (Bounded Range)**: 明确数值的定义域（如 `0.0 <= score <= 1.0`，溢出截断与平滑贝叶斯更新 `new = 0.9 * old + 0.1 * delta`）；
  3. **资金守恒约束 (Conservation of Value)**: 账本与托管扣款必须满足 `sum(debits) + sum(credits) == 0`，每一笔扣款必须回填对应的业务实体句柄 (`job_id`)。

### 铁律 3: 赞助商与外部基建活体实测铁律 (Sponsor Live-Proof Gate / SPONSOR_LIVE_CHECK)
- **底层病灶**: “仅在代码里写了适配器”就自认为完成了赞助商技术要求（如 R12 中实现了 `RedisQueue` 适配器并写了 compose，但在本地实跑时因无 Redis 静默降级到 SQLite，评委直接扣除赞助商分数）。
- **第一性法则**: **契约存在 ≠ 运行时实证！**
  1. 凡赛道要求或鼓励使用赞助商技术（如 Redis、特定的向量数据库、大模型厂商、Web3 链）：
     - 必须在本地容器（`docker run`）、免费云服务（如 Redis Cloud 免费实例）中真实跑通至少 1 条端到端任务链路；
     - 必须将**带有真实连接信息、握手输出与操作执行的日志**记录在 devlog 中；
  2. 严禁将“降级回退方案”当作默认运行形态——降级只能作为极端网络异常下的备选，不能作为唯一交付证据。

### 铁律 4: 状态跃迁增量断言律 (State-Mutation Delta Verification)
- **底层病灶**: E2E 自动化测试停留在“弱存在性检查”（例如仅断言某个余额标签在页面上“存在且包含数字”，即便数值根本没变也判定通过，掩盖了状态未响应的严重 Bug）。
- **第一性法则**: **凡涉及写操作或状态转移的交互，测试必须断言具体增量 `ΔState = Action(State)`**！
  1. 提交订单前获取 `before_balance`，执行后断言 `after_balance == before_balance - cost`；
  2. 任务完成后断言 `final_balance == before_balance - cost + payout`；
  3. 严禁单纯使用 `toBeVisible()` 冒充端到端闭环测试。

---

## 6. 复杂度核验工具: `verify-production-complexity.ps1`

在构建完成与提交通道前，必须在项目根目录运行 `verify-production-complexity.ps1`：
- 该脚本会自动化物理扫描：
  1. 统计有效核心源码行数 (LOC)，确保项目代码体量跨入数千至万行级门槛。
  2. 统计数据库实体模型类数量 (≥ 8 张表)。
  3. 统计 API 路由端点总数 (≥ 16 个)。
  4. 统计前端独立组件数量 (≥ 18 个)。
  5. 检测是否存在异步 Worker / 任务队列结构。
  6. 检测是否包含统一异常信封、Alembic 迁移脚本、Docker Compose。
- **未达标者直接退出码 1，严禁以"已完成"自居汇报**。
