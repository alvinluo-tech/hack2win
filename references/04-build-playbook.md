# P4 快速构建 — 万行级复杂生产系统装配指南

> **核心目标**: 产出具备工业级架构深度、真实可用、代码量在数千至万行级(4,000 - 25,000+ LOC)的完整产品，彻底摒弃仅靠几百行代码支撑的玩具 Demo。
> **工程思想**: 采用 **分阶段子系统解构与装配流水线 (Subsystem Staged Assembly Pipeline)**，通过领域拆解与多子代理协同，在时间盒内高效装配出涵盖多租户、ORM 数据层、后台异步 Worker、API 网关与企业级前端工作台的庞大生产体系。

---

## 一、企业级系统分阶段装配里程碑 (M0 - M4.5)

将整个构建过程划分为严密的 6 大装配里程碑，每步均有明确的交付物与自动化验证门槛：

```
M0: 蓝图与契约冻结  ───► M1: 底座与数据持久层 ───► M2: 领域引擎与后台 Worker
(Domain Blueprint)        (ORM, Migrations, Seed)    (State Machine, Queue)
                                                                 │
                                                                 ▼
M4.5: 生产加固与复杂度审计 ◄── M4: 复杂工作台与业务流 ◄── M3: 网关与企业级布局壳
(Tests, Docker, LOC Audit)     (DataTable, Wizard, BI)    (Layout, Cmd+K, API)
```

| 里程碑 | 核心建设内容 | 必须产出的实体与硬指标 | 验收标志 |
|---|---|---|---|
| **M0 蓝图与契约** | 领域实体关系图(E-R)、OpenAPI 端点清单、前端路由表 | 8-15+ 实体定义草案、20+ 路由契约、5+ 核心视图规划 | 蓝图文档落盘，前后端接口契约冻结 |
| **M1 底座与持久化** | 工业脚手架初始化、SQLAlchemy ORM 实体全量落地、Alembic 迁移、海量种子数据脚本 | 8-15+ 张规范表(含租户隔离、外键级联、软删除、审计字段)、`seed.py` 生成 500+ 条真实业务数据 | `alembic upgrade head` 执行成功，数据库表与初始数据真实可见 |
| **M2 领域引擎与Worker** | 业务核心状态机、Repository 仓储层、异步任务队列(Worker/Queue)、Redis 缓存 | 核心状态机驱动类、异步 Worker 处理器、至少 1 个高耗时业务后台化处理 | Worker 进程启动正常，任务派发后可轮询状态，状态转移非法拦截 |
| **M3 网关与布局壳** | FastAPI 路由全量挂载、Next.js 15/16+ (React 19, Tailwind v4) 企业级布局壳(Sidebar、Header、Cmd+K、Breadcrumbs) | API v1 全量路由组装(20+ 端点)、全局设计令牌、自适应侧边栏、全局指令面板 | 前后端通过网关打通，浏览器中布局壳完整渲染，Cmd+K 可唤起 |
| **M4 业务视图与工作台** | 高级 DataTable (多列排序/过滤/导出)、多步向导 (Form Wizard)、数据大盘 (KPI + Sparklines) | 核心资源列表全功能 DataTable、业务创建向导、多维分析统计页 | 真实用户全旅程在浏览器完整跑通(列表、创建、异步处理、报表) |
| **M4.5 加固与复杂度审计** | 自动化测试套件(pytest ≥ 15条)、红队对抗自测、Docker Compose 集群验证、复杂度量化审计 | `verify-production-complexity.ps1` 校验全绿、LOC 达到要求、Docker 一键拉起 | 退出码 0，测试 100% 跑绿，无未捕获异常 |

---

## 二、AI 如何协同写出万行级代码？(多子代理领域分工机制)

单个 Agent 一次性编写几万行代码必然会导致上下文衰减、截断或编写空洞代码。总控层必须采用 **多子代理分工装配 (Sub-agent Domain Partitioning)**：

1. **主总控 Agent (Orchestrator)**:
   - 守住全局架构图、数据库模式(Schema)与 API 契约；
   - 负责创建脚手架目录与环境变量基础文件；
   - 负责最终的模块集成、构建运行与全量自动化校验。
2. **派离子代理并行突进 (分派工作树)**:
   - **子代理 A (Data & Core Specialist)**:
     - 任务: 编写 `backend/app/models/` 下的 8-15 张 ORM 表，编写 Alembic 迁移脚本与生成 500+ 条真实数据的 `seed.py`。
   - **子代理 B (Services & Worker Specialist)**:
     - 任务: 编写 `backend/app/services/` (状态机、用例业务)与 `backend/app/workers/` (后台异步队列与定时任务)。
   - **子代理 C (API Gateway Specialist)**:
     - 任务: 编写 `backend/app/api/v1/` 下的全量路由端点、Pydantic DTO 校验、依赖注入与异常处理器。
   - **子代理 D (Frontend Shell & Design System Specialist)**:
     - 任务: 编写 `frontend/` 下的企业级布局壳(Sidebar, Header, Cmd+K, Breadcrumbs)与 Design System Tokens。
   - **子代理 E (Frontend Workbenches Specialist)**:
     - 任务: 编写高级 DataTable 组件、多步表单向导与 Analytics 动态图表页面。
   - **子代理 F (Quality & DevOps Specialist)**:
     - 任务: 编写 pytest 测试套件(单元+集成)、Playwright 端到端脚本、Docker Compose 编排与启动管理脚本。
3. **总控集成纪律**:
   - 每个子代理交付时必须附带语法检查与单元自测证据；
   - 主总控在汇合点统一执行 `npm run build` 和 `pytest`，严禁口头验收。

---

## 三、生产级核心工程规范 (防玩具十诫)

1. **拒绝单表玩具**: 数据库表数量必须 ≥ 8 张，必须包含外键级联、复合索引、软删除(`deleted_at`)与租户标识(`workspace_id`)。
2. **拒绝扁平代码堆砌**: 单文件控制在 300 行以内；业务逻辑必须下沉到 Service/Repository，路由层只负责参数绑定与响应封装。
3. **拒绝同步阻塞计算**: 凡涉及耗时超过 500ms 的操作(AI 调用、报告生成、批量计算、外部集成)，必须放入后台异步任务队列(Worker)，前端通过轮询或 SSE 追踪。
4. **拒绝无响应规范**: 全局统一响应结构体 Envelope：`{"code": 200, "data": ..., "message": "success", "trace_id": "..."}`。
5. **拒绝裸字符串魔法值**: 状态机的每一个状态、枚举字段全部定义为 `StrEnum`；错误码全系统集中定义。
6. **拒绝假数据与 Lorem Ipsum**: 种子数据必须贴近真实业务语义(真实姓名、规范行业术语、真实数值区间、真实时序分布)。
7. **拒绝简易粗糙 UI**: 前端必须具备企业级后台框架，数据呈现必须支持高级 DataTable(分页、排序、过滤、导出)，关键流程采用向导式交互。
8. **拒绝裸 print 与静默吃异常**: 日志全量结构化，携带 Correlation-ID；全局异常处理器兜底，禁止向前端泄漏原始未捕获错误堆栈。
9. **拒绝假阳性测试**: 测试套件必须包含真实业务边界断言(参数非法 422、权限越界 403、状态非法 409、并发幂等验证)，而非只断言 `/health`。
10. **拒绝无法一键拉起**: 必须提供标准的 `start-all.ps1` 和 `docker-compose.yml`，具备开箱即用的冷启动体验。

---

## 四、复杂度与质量双重自动化门槛 (Dual Verification Gates)

在进入打磨(P5)与路演(P6)之前，必须依次执行以下自动化检查，全部通过方可放行：

### 1. 结构与契约校验
```bash
# 跨平台通用 Python (Linux / macOS / Windows)
python scripts/verify_project.py --project-path app
# 或 Windows PowerShell
powershell -File scripts/verify-project.ps1 -ProjectPath app
```
- 检验前后端双目录、依赖锁定、.env.example、路由、错误处理等 17 项基础规范。

### 2. 生产级复杂度硬性审计 (Complexity Audit)
```bash
# 跨平台通用 Python (Linux / macOS / Windows)
python scripts/verify_production_complexity.py --project-path app
# 或 Windows PowerShell
powershell -File scripts/verify-production-complexity.ps1 -ProjectPath app
```
- 自动化扫描代码量(LOC)、数据表数量(≥8)、API 端点数(≥16)、前端组件数(≥18)、异步 Worker 存在性。
- 未达到生产复杂度底线者直接退出码 1，强制补齐业务深度。

### 3. 构建与冒烟测试
- 前端: `cd frontend && npm run build` (编译零错误，零严重 warning)
- 后端: `cd backend && pytest` (自动化测试用例 ≥ 12 条，全量通过)
- 集群: `curl http://localhost:8000/health` (探针返回 ok，且真实检测 DB/Redis 依赖健康)

### 4. 真实浏览器点击与冷启动演练
- 执行 `stop-all.ps1` 彻底停服；
- 执行 `start-all.ps1` 冷启动集群；
- 运行真实浏览器自动化脚本(如 `node frontend/scripts/e2e-click.mjs`)，走通一条从输入、到异步任务、到数据落库、到前端看板渲染的完整闭环。

---

## 五、生产红线与验证纪律(历轮实战沉淀,全部强制)

### 红线一:能力声明必须实证
- 每一条写进 QA 卡/slides 的能力声明("跑在GPU上"/"X秒出结果"/"支持XX语言")必须在**目标演示环境**实机验证;环境不允许时必须有等价验证路径(Node 同签名脚本/模拟器)+如实声明
- 禁止口径漂移:种子条数/数据源数量/响应时间全文档一致,提交前 grep 交叉核对
- **选型/叙事变更,当天回写**全部前置文档;竞品对比每格提交日复核
- **提交物物理核验**:`ls` 对照声明清单,不打空勾
- **结构声明必须有运行时证据**(R11 评委审法):verify 脚本只验结构不验运行——compose 服务数正则会误计 volumes、ARQ 文件存在但从未执行也 PASS、命名 router 会被正则漏计。凡声称"Worker 在跑/队列在消费/服务在编排",必须附一次真实运行日志(任务派发→状态流转→完成)与 `app.routes` 导出的真实端点数
- **赞助商与核心基建活体实测铁律 (SPONSOR_LIVE_CHECK, R12 实锤)**:
  - 凡赛道赞助技术(如 Redis、向量数据库、特定大模型供应商、Web3 链)：仅写出适配器类或在 compose 中声明不算数！
  - 必须在本地容器（`docker run` / 守护服务）或官方免费云实例（如 Redis Cloud Free Tier）中**真实建立网络连接，执行至少一条端到端读写任务**；
  - 必须将带有真实连接信息、握手日志与数据操作记录在 devlog 中；未完成实测者，严禁在路演材料中声称已集成该赞助商栈！
- **生产级打包体积与代码分割预算 (Bundle Splitting Budget)**:
  - 前端最终构建产物中，单个 JavaScript Chunk 严禁超过 **500KB**；
  - 针对 Three.js、React Three Fiber、Recharts、ECharts 等重型图形与可视化库，**强制采用动态导入 (`React.lazy` / `next/dynamic`) 实施组件级代码分割**；彻底消除 `vite build` 或 `next build` 报出的单体大 Chunk 性能警告。

### 红线二:端到端证据阶梯 + 点击级验收 + 冷启动演练
- **证据阶梯**:curl 不发 CORS 预检、SSR 不走跨域——"curl 通+SSR 含数据"≠浏览器用户能用。验收证据必须含**真实浏览器 fetch** 一级(playwright `page.evaluate`,范式 `frontend/scripts/e2e-cors.mjs`);换过端口/域名按最终形态重测
- **状态跃迁增量断言律 (State-Mutation Delta Verification, R12 实锤)**:
  - 彻底废除“仅断言元素存在或可见 (toBeVisible)”的弱检查！
  - 凡涉及资金扣减、收益入账、任务计数或状态变更的交互，E2E 测试必须执行**数学增量断言**：
    $$\text{State}_{after} == \text{State}_{before} + \Delta\text{Value}$$
  - 示例：下达任务前提取 `before_balance`，执行后断言 `after_balance == before_balance - cost`；结算后断言 `final_balance == after_balance + actual_payout`；严禁允许陈旧不变的数据标签蒙混过关！
- **点击级验收 + 冷启动演练(T2 交付最后一步,接口全绿≠可交付)**:
  1. 交付物必须含用户可自行执行的 `start-all.ps1`(起前后端+等健康+CORS 白名单显式注入前后端端口族)与 `stop-all.ps1`——服务生命周期不许挂在 agent 会话上
  2. **start-all 必须防重入**(端口已监听则 SKIP);健康轮询一律用 127.0.0.1(PS5.1 的 localhost 可能解析为 ::1)
  3. 冷启动演练:停全部服务 → 只跑 start-all → 浏览器真实点击演示场景(`e2e-click.mjs` 三态判定 PASS-STRONG/PASS-WEAK/FAIL)——专抓 BUILD_ID 缺失、CORS 白名单漏端口、SSR 掩盖后端宕机
  4. 两种经典假阳性:SSR 渲染数据掩盖后端不在;配置默认值与实际启动参数不符(CORS_ORIGINS 默认 3000 族,前端实际 3500)
- **红队探针标准化**(M4.5 配套):跨租户越权(换 workspace_id 读他人数据→空集/404)、越权写入(viewer 写→403)、畸形输入(空/超长/非法 JSON→422 信封)三类探针模板落 `tests/` 或 `scripts/`,M4.5 直接执行留原始输出——把"自查"变"可被第三方复跑的被查"
- **验收脚本自身是交付物且必须脏库可复跑**(R11 评委实锤):smoke/e2e 脚本非幂等、无空值守卫,在 e2e 污染后的脏库上复跑即崩=验收工具链失效。强制序列:**smoke → e2e → smoke** 全程 exit 0;magic moment 场景禁用宽容终态(必须 PASS-STRONG,见红线三)
- **外呼网络策略显式化**(R11 实锤:preview 代理 502 vs 直连 200,真实特征入库零实证):所有 httpx/requests/fetch 必须显式声明 `trust_env` 与代理策略(禁止静默继承系统代理);交付前做**断代理/断外网双态演练**并留痕
- **演示后门显式化**:特殊路径触发必须由显式开关控制(`?force_fail=1`/界面勾选),禁止输入内容嗅探(评委真实输入含敏感词会误触发),QA 与 UI 如实标注
- **交付目录一致性(运行目录与交付目录分离死法,R11 事故实证)**:冷启动演练与点击验收**必须在交付目录(hackathon-run/app)内执行**——严禁"服务跑在归档/临时目录、交付目录只是空壳"的组合(该形态下用户按交付目录自行启动=打开脚手架样板页)。每轮收尾自查:`交付目录/frontend` 是否含真实业务 page(非 create-next-app 样板)、`start-all.ps1` 是否位于交付目录且路径相对正确
- **UI 层全覆盖遍历验收(05 §三点五)**:后端接口全绿≠前端可用——全部页面截图(桌面+窄屏)+溢出检测+console/pageerror/HTTP≥400 零容错+点击遍历,修复后全量回归至清零
- **修复必须回归测试**:"已修掉"三个字说出口前先重跑原案例(核验案例:声称修掉空白音频崩溃,评委换个长度复现,诚信扣分)

### 红线三:真实链路(防评委读代码看穿)
1. magic moment 单点接真(真模型/真数据/真 API 任一,免费额度足够)
2. **magic moment 验收必须 PASS-STRONG**(R11 实证):真实点击 → 真实外呼 → **真实数据落库断言**(查 DB 新行/新文件,不是"没报错")三者缺一即 FAIL;PASS-WEAK(优雅错误/宽容终态)只允许非核心场景且书面标注——宽容终态会掩盖断链(实测:463 首"已分析"全为合成特征,e2e 13/13 全绿却无一次真实特征入库)
3. 混合模式:在线真链路+离线种子兜底,Q&A 标注边界
4. 编排推进由真实事件驱动,禁止固定 sleep 假装工作
5. **"任意输入"模式必须存在**:评委现场粘贴自己的内容也能出结果——不可复制的 wow
6. **单向真值源动效绑定 (State-Driven Visual Invariant, R12 实锤)**:
   - 3D 画布、粒子爆发、状态指示、飘字金额、HUD 标签严禁硬编码常量或本地伪数值！
   - 必须严格消费后端事件载荷中的真实字段（携带 `job_id`, `building_id`, `actual_payout`）。严禁出现实际结算 131 但动画硬编码 `+120 cr`、或者粒子在固定假楼宇爆发的“说谎瞬间”。
   - 顶栏或全局指标必须随状态流转即时动态响应，不得依赖手动刷新。
7. **领域数学模型与单调性自检 (Domain Invariants & Monotonicity)**:
   - 评分、定价、等级、抽成结算等核心公式必须具备数学自洽性；
   - 必须配备单元测试断言单调性（如任务成功交付必不降低员工综合评分）与数值边界，严禁随手编写粗糙公式导致逻辑破绽。

### 种子数据纪律
真实比例/真实命名/真实分布;来源真实公开数据集或 LLM 批量生成后人工校验,固定文件进 repo 断网可演;演示画像用常见真实姓名,拒绝 nickname123。T2 规模要求 seed 生成 **500+ 条**级连真实记录。

### 三保险(anti-翻车)
1. **本地兜底**:外部 API 调用带缓存层,失败读缓存标记 cached mode;核心路径可离线重放
2. **录屏备胎**:M3 后立即录全程,云端+U盘+本地三处;无头环境用 Playwright recordVideo/CDP 截屏帧序列+ffmpeg 合成,从"就绪态"起录,结尾必含证据镜头
3. **环境冻结**:D-1 锁依赖,演示机专用,关自动更新

### 速度证据链(回应套壳怀疑)
commit 时间线小步提交自证赛内完成;devlog 保留"砍了什么"取舍叙事;AI 披露模板:"本项目在 XX 环节使用了 XX 模型辅助(代码生成/文案/种子数据),核心逻辑与全部决策由团队完成"。

---

## 六、验收清单 (P4 离场检查)
- [ ] M0 - M4.5 里程碑全量达成并在 devlog 留存详细装配记录
- [ ] 源码体量跨越生产门槛 (LOC ≥ 4,000 - 15,000+ 行，排除依赖)
- [ ] 数据库实体表数量 ≥ 8 张，Alembic 迁移链完整，seed 脚本生成 500+ 真实记录
- [ ] 后台异步 Worker 与队列就绪，耗时任务完全解耦，且有真实运行日志证据
- [ ] API 路由数量 ≥ 16 个(以 app.routes 导出为准)，OpenAPI `/docs` 规范清晰，错误处理统一
- [ ] 前端具备完整的企业级 Layout Shell、Cmd+K、高级 DataTable、Wizard 与 Dashboard
- [ ] verify-project.ps1 与 verify-production-complexity.ps1 双双 PASS 退出码 0
- [ ] pytest (≥ 12 用例) 与 npm run build 100% 跑绿，单 Chunk 打包体积 ≤ 500KB
- [ ] 核心领域数学模型单调性与不变量单元测试通过
- [ ] 赞助商技术活体实测 (SPONSOR_LIVE_CHECK) 完成并有运行日志
- [ ] 冷启动演练与真实浏览器点击验收通过，包含状态跃迁增量断言
- [ ] 红队探针三类全部执行且原始输出留存

