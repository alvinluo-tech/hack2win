---
name: hack2win
description: >
  黑客松总控层开发技能:从主题到万行级生产级全栈交付的编排者。MUST USE whenever the user mentions 黑客松/hackathon/编程马拉松/builder大赛/demo day,
  wants to 参赛/找点子/头脑风暴/调研比赛/根据主题出产品/写参赛作品/准备demo或路演, or asks to 从0到1交付一个具备商业落地条件、代码量在数千至万行级(4,000 - 25,000+ LOC)的复杂高保真产品 — even if they just say "帮我参加XX比赛".
  作为总控层,它负责 流程决策(命题解码/头脑风暴/选型/规模/架构)、交付契约(T2全栈七要素/复杂度硬性底线/反空壳/反玩具Demo)、验收门,以及**技能编排**——
  UI设计突破传统工作台定式(支持2D像素世界、Three.js 3D空间、复古OS终端、无限画布与高密驾驶舱多维隐喻;用户指定风格绝对优先并专业升维)/架构设计/测试/框架集成等领域能力通过引用其他技能完成(缺失则安装,见 references/10-orchestration.md),
  人类只需说"用某技能优化某方面"即可全程推进。
  NOT for: 简单的静态单文件实验(无工程化诉求时不套用本流程)。
---

# hack2win — 黑客松总控层开发引擎 (万行级复杂生产系统版)

**你现在的角色是总控层(orchestrator)**:把一个主题变成一个具备商业落地条件、复杂完备、高度精美、贴近生产的成熟产品(推荐 8,000 - 25,000+ LOC)。
**坚决彻底终结"几个 HTML+JS 文件"或"单表单接口"的玩具 Demo 思维**。
**同时坚决打破“一切界面都是传统枯燥管理后台”的局限**：黑客松大奖界面百花齐放——从斯坦福 2D 像素小镇、Three.js 3D 空间宇宙、复古 Win98 桌面到现代暗色驾驶舱；**若用户指定了特定风格，100% 遵照用户意志并专业升维做到极致**。

核心理念六条,全程贯穿:

1. **表面天马行空，底层坚如磐石(Playful Surface, Enterprise Foundation)**: 界面可以是一个有趣的 2D 像素小镇、3D 旋转星系或复古终端，但其下方**必须依然由 8 大子系统的生产级全栈工程支撑**(FastAPI + 8-15+ 实体表 + Alembic 迁移 + 异步 Worker 队列 + 状态机)。绝不做只有前端几行动画的空壳玩具！
2. **生产优先架构 + 演示切片提取(Production-First + Demo Extraction)**: 坚决不做只够跑演示的玩具薄壳。开局即以商业化落地标准设计多租户、ORM 数据层、后台异步任务队列与企业级组件库；路演时从这套完整扎实的万行级生产底座中，提取最惊艳的 3 分钟核心演示链路。
3. **用户指定风格绝对优先与专业升维 (User-Intent Supremacy & Elevation)**: 当用户提出明确的视觉风格（如“做成像素世界”、“用 3D 做成宇宙”、“复古 Win98”），严禁偷懒套用普通后台，必须调动对应专业前端库（Phaser/Three.js/98.css等）将该风格推向巅峰，补齐 8-bit 音效、光线追踪、CRT 扫描线等大奖细节。
4. **切题>炫技,进 top3>讲懂**: 评分标准是主办方公布的"考卷答案",先逆向再动手(见 07)。评审物理约束严酷——Devpost 线上评委约 10 分钟/项目、现场赛 3-4 分钟/队，采用 top3 排名制: 极具趣味与突破性的视觉隐喻瞬间击穿评委的第一眼心理锚定。
5. **真实>精致**: magic moment 至少有一条端到端"真实能力链路"支撑(真模型/真数据/真API任一),纯 mock 编排会被技术评委读代码三分钟看穿; 扎实的数据库迁移、真实感种子数据与测试套件是消除套壳怀疑的铁证。
6. **动效与真值源单向投影律 (State-Driven Visual Invariant)**: 界面里的所有 3D 动效、粒子爆发、金额浮字与状态指示，必须严格作为后端领域事件 (`DomainEvent`) 的纯函数投影；严禁在前端渲染层伪造脱节的硬编码数值，真值源唯一，动效即证明！

## 常驻规则(全程适用)

1. **工作区纪律**: 从 P0 起在当前项目下建 `hackathon-run/` 目录,每阶段产物落盘:
   ```
   hackathon-run/
   ├── 00-brief.md            命题解码卡
   ├── 01-ideas.md            头脑风暴+评分矩阵
   ├── 02-market.md           市场调研one-pager
   ├── 03-definition.md       产品定义+演示脚本+选型ADR
   ├── app/                   生产级全栈工程本体 (Next.js + FastAPI + Postgres/SQLite)
   │   ├── frontend/          企业级管理后台 (Layout Shell, Cmd+K, DataTable, Wizard)
   │   ├── backend/           DDD分层后端 (Models, Repos, Services, Workers, API v1)
   │   ├── docker-compose.yml 多容器集群编排
   │   └── start-all.ps1      一键冷启动管理脚本
   ├── 04-devlog.md           构建日志(里程碑/多代理装配/取舍记录)
   ├── 05-pitch/              slides、demo视频脚本、Q&A卡
   ├── iterations/            迭代引擎留痕 (多轮视觉环对比截图+四维质量评分)
   └── SUBMISSION.md          提交清单
   ```
2. **时间盒**: 开工先问/估总时间 T,按比例分配: P0 5% / P1 10% / P2 15% / P3 10% / P4 40% / P5 10% / P6 10%。每阶段到点必须收敛——采用多子代理并行推进各子系统(见 11 §3)，保障庞大工程在时间盒内完整闭环。
3. **双重机械化验收门**: 每阶段末尾对照验收门自查，P4 结束必须同时通过 `verify-project.ps1` 和 `verify-production-complexity.ps1` 双重脚本校验，不过关严禁进入下一阶段。
4. **并行借力与多代理分工**: 架构设计、数据表模型、API 路由、前端布局壳、异步任务队列由主总控派离子代理并行突进；主总控守住接口契约并在汇合点执行集成构建。
5. **数据诚实**: 市场数字、用户痛点证据必须有来源链接或明确标注[假设]；真实感种子数据覆盖 500+ 条真实记录。
6. **外部情报**: 本机装有 agent-reach 时,优先用其 Exa 通道(`mcporter call exa.web_search_exa query='关键词' numResults=6`)；来源全部记录进 02-market.md。
7. **平台合规与合规红线**: 全部工作赛内完成；AI 可以大胆用但必须在提交中如实披露用法；不做现有 AI 工具的纯套壳。
8. **编排优先**: 遇到领域能力需求(UI/架构/测试/框架集成),先查 10-orchestration.md 注册表引用对应技能(缺失则按流程安装)。验收权始终在本技能。

## 交付规模分级(先定规模,再动手)

P3 结束时必须宣布本次交付等级并写进 03-definition.md,选级依据与完整交付契约见 [references/08-production-standard.md](references/08-production-standard.md):

| 等级 | 定位与形态 | 硬性量化底线 (Floor) | 触发条件 |
|---|---|---|---|
| **T2 生产级全栈(默认)** | 工业级前后端分离体系(Next.js 15/16+ React 19 + FastAPI + SQLAlchemy 2.0 + Alembic + 异步任务队列) | **代码量 ≥ 4,000 行(排除依赖)**<br>数据表 **≥ 8 张规范表**<br>API 端点 **≥ 16 个规范路由**<br>前端组件 **≥ 18 个独立组件**<br>完整后台布局壳 + 高级表格 + 异步后台任务 | **默认强制执行**，无需理由 |
| T3 商业化复杂系统 | T2 + 完整多租户(RBAC) + Docker Compose 5集群 + Redis 缓存 + 指标监控(Prometheus) + 审计日志 | **代码量 ≥ 10,000 - 25,000+ 行**<br>数据表 **≥ 12-16 张表**<br>端点 **≥ 25-35+ 个**<br>组件 **≥ 30-50+ 个**<br>独立业务视图 **≥ 6-10 个** | 商业化竞赛、大厂主赛道、一周赛制或决赛冲刺 |
| T1 轻量交付 (严控降级) | 纯前端单页应用或轻量演示 | 核心源码 < 2,000 行 | **严控**: 仅限剩余<6h 且环境完全受限时经 devlog 详细说明方可降级，否则直接判定违背契约 |

## 迭代引擎(质量来自循环,不来自一次写对)

**默认假设:任何第一版产物都不合格。** 流水线给出方向,迭代给出质量。三种循环贯穿 P4-P6,每种都必须落证据:

| 循环 | 节奏 | 动作 | 证据落盘 |
|---|---|---|---|
| 构建环 | 每个装配里程碑 | build/pytest/verify-project/verify-production-complexity 红→修→绿 | devlog 命令输出 |
| **视觉环** | M4 起,P5 至少 2-3 轮 | **截图→三问评审→定向修→重截对比**(工具: scripts/ui-shot.ps1,桌面1440+窄屏390,必带 -ExpectText 内容断言防"错误页假阳性") | `iterations/round-N/` 前后截图 |
| 四维质量环 | M3 起,每个大里程碑后 | 四维各打 1-5 分(新颖度/UI美观/工程质量/代码质量)→**最低维获得下一轮优先投入** | `iterations/round-N/scores.md` |

**评分纪律**: 每一分变动必须附**证据物**——UI 提分附前后截图、工程提分附 verify 自动化输出、代码质量提分附 refactor diff; 无证据物的提分=无效评分。
**停止条件**: 时间盒尾预留 10% 缓冲; 或连续一轮四维均无提升=已收敛,转 P6。

## 七阶段流水线

每阶段 = 输入 → 核心动作 → 产物 → 验收门。**详细方法论按路由表读对应 reference,读完再动手。**

| 阶段 | 时间 | 一句话目标 | 详细文档 |
|---|---|---|---|
| P0 命题解码 | 5% | 把"考卷答案"找出来，评估主办方生态与赞助商技术可得性 | [references/00-theme-decode.md](references/00-theme-decode.md) |
| P1 头脑风暴 | 10% | 24+点子过8透镜(含视觉隐喻透镜)→评分矩阵收敛→1主1备(错位竞争+不讨巧切口, 见 12) | [references/01-brainstorm.md](references/01-brainstorm.md) |
| P2 市场调研 | 15% | **三轮对抗性辩证调研流水线**(全景扫描➔红队死亡审判对抗矩阵➔护城河锁定; link-check) | [references/02-market-research.md](references/02-market-research.md) |
| P3 产品定义 | 10% | 一句话+magic moment+演示脚本v1;**多端形式决策+实时版本号探测(09§1)+开放式物理隐喻推演(12)+编排计划** | [references/03-product-definition.md](references/03-product-definition.md) |
| P4 快速构建 | 40% | **万行级系统分阶段装配流水线(M0-M4.5)**;深模块解耦(codebase-design/setup-ts-deep-modules),TDD不变量测试,双重机械化硬门 | [references/04-build-playbook.md](references/04-build-playbook.md) |
| P5 打磨增色 | 10% | **企业级视觉打磨与视觉环(至少2轮截图对比)**;组件级无裁切审计+叙事-数据一致性;主引用 design-taste-frontend | [references/05-polish.md](references/05-polish.md) |
| P6 路演提交 | 10% | **顶级开源项目标杆交付(CI/CD, 完备DX, 双语README, ARCHITECTURE.md)**;路演合规提交 | [references/06-pitch-submit.md](references/06-pitch-submit.md) |

- 开始 P0 前必读: [references/07-judging-rubrics.md](references/07-judging-rubrics.md) (逆向评分)。
- P2 调研必读: [references/02-market-research.md](references/02-market-research.md) (三轮对抗性调研)。
- P3 选型/初始化/深模块架构必读: [references/09-tech-architecture.md](references/09-tech-architecture.md)。
- **P4 万行级复杂生产系统架构与装配必读: [references/11-enterprise-complexity-architecture.md](references/11-enterprise-complexity-architecture.md)**。
- **P5 开放式物理隐喻推演必读: [references/12-winning-ui-patterns.md](references/12-winning-ui-patterns.md)**。
- **全程编排: 领域能力先查 [references/10-orchestration.md](references/10-orchestration.md) 注册表,不要自己重新发明。**

## 各阶段验收门(速查)

- **P0**: 能不看资料回答——主办方是谁?他们想借比赛得到什么?评分维度哪条权重最高?往届冠军长什么样?赞助商技术预检结论与缓解方案是什么?
- **P1**: 评分矩阵≥10行,入选idea在五维各有明确打分与理由;选型三问通过;有1个备胎idea。
- **P2**: 竞品表≥3个真实竞品(全带链接并通过机器 link-check),差异化声明通过"遮名测试",痛点证据≥3条(含近24个月数据),"AI 在哪"三层预案写定。
- **P3**: 演示脚本≤10个场景、每个场景≤30秒、有明确"哇点"场景;选型四步法落盘 ADR(含2候选对比与回头条件);**开放式物理隐喻推演与视觉架构决策(12号文档: 资产物理原形、动词映射、视觉反差; 用户指定风格绝对优先并专业升维，严禁四选一狭隘模板化)**;宣布 T2 生产级全栈交付等级。
- **P4 (双重复杂度与契约硬门)**:
  - 源码体量达标: 核心源码 LOC ≥ 4,000 - 15,000+ 行(排除依赖)；
  - 数据模型深度: 数据库规范关系表 ≥ 8 张，Alembic 迁移链完整，seed 生成 500+ 真实记录；
  - 异步计算解耦: 耗时操作由独立后台 Worker / 任务队列处理，禁止同步阻塞；
  - 接口契约完备: API 端点 ≥ 16 个，统一异常响应信封与结构化日志；
  - 前端工作台: 完整企业级 Layout Shell、Cmd+K 指令面板、高级 DataTable 与 Wizard(或等价专业沉浸式世界观)；
  - 机器自动化双体验证: `verify-project.ps1` 与 `verify-production-complexity.ps1` **全部 PASS 退出码 0**；
  - 构建测试: `npm run build` 零错误 + `pytest` (≥ 12条) 100% 跑绿，单 Chunk 打包体积 ≤ 500KB；
  - 核心领域数学模型单调性与不变量单元测试通过；
  - 赞助商技术活体实测 (SPONSOR_LIVE_CHECK) 完成并有运行日志；
  - 冷启动与真实点击: `stop-all.ps1` 彻底停服后 `start-all.ps1` 冷启动，真实浏览器点击脚本跑绿，断言状态跃迁增量 $\Delta\text{State}$。
- **P5**: strangers-test——给没参与的人看截图,能说出"这是干嘛的、给谁用"; **视觉环 ≥2 轮且前后对比截图落 `iterations/`**(三问逐轮回答,最丑三处至少修掉两处); axe a11y 走查 0 严重违规; 窄屏 390px 适配无溢出; **叙事-数据一致性审计全通过(无硬编码伪高光)**。
- **P6**: 提交项对照比赛官方要求逐项打勾; Q&A卡≥10问; 备用demo(录屏)已上传; 部署地址真实可通。

## 常见死法 Top24(出现在任何一个,立即纠偏)

1. 开工12小时还没定idea(完美主义 brainstorm)→ 启动 P1 的硬规则:时间盒到点必须用矩阵强行选
2. scope 覆盖"产品该有的一生",demo 只能展示幻灯片 → 回到演示脚本,以核心主线贯穿整个生产架构
3. demo 当场翻车(网络/API/环境)→ P4 的三保险:本地种子数据、缓存兜底、录屏备胎
4. 技术很炫但评委没看懂解决什么问题 → P6 故事弧第一分钟永远讲"人的问题"
5. UI 惊悚拉低全部印象分 → P5 的 taste checklist,组件库起步不裸写CSS
6. 不切题:做了个通用产品硬蹭主题 → P0 命题解码卡贴在显眼处,每阶段末对照
7. 数据/演示内容明显假(Lorem ipsum、假名假数)→ P4 种子数据必须"真实感"(真实场景、真实比例、500+ 条记录)
8. 只有代码没有故事,路演念PPT → P6 故事弧+排练3遍
9. 提交缺项(video/README/表单/**公开部署链接**)错失资格 → SUBMISSION.md 开工第一天生成就建,逐项打勾;部署在 P5 就上线
10. 单点依赖某个成员/某个API到最后一晚 → P4 里程碑制,任何外部依赖在D-1天前必须有fallback
11. **全 mock 无真链路**:演示靠固定时长编排动画,评委读源码即穿帮 → P4"真实链路"规则:magic moment 单点接真,离线才走种子兜底
12. **合规翻车**:AI 使用未披露、复用旧代码、纯套壳 → 一票否决级风险,P3 起草披露文案,P6 提交前逐字核对
13. **赞助商技术零使用或只在PPT里**:大厂赛的隐性一栏分 → P0 做可得性预检,当天申请;用不上就诚实交底+迁移路径,或换赛
14. **被评委的红队输入击穿**:产品对刁钻输入给出荒谬结果(如核查工具为谣言背书) → M4.5 先自己红队3案例,修掉或标注
15. **公开链接即点即坏**:多资产应用上随机改名托管,页面200但资源404,评委首次点击就遇错 → 部署形态匹配+部署验收=从公开URL走完完整演示路径
16. **T2 被无理由降级成 T1**:时间明明够却只交几个静态 HTML,评委问"后端呢" → 交付规模分级是 P3 的显式决策;降级必须命中触发器并写 devlog
17. **全栈空壳**:目录齐全但 API 是 TODO、模型没迁移、前端没有真实调用后端 → 08 的反空壳清单+verify-project.ps1+冒烟跑绿,三者缺一不可
18. **AI 赛道的"AI 在哪"哑火**:核心能力是规则算法却投 AI 赛道,评委一句"AI 在哪"即打穿 → P6 前写好三层答案(算法真实在哪个函数/为何不需要 LLM/升级路径),答不出第一层回 P1 重收敛(02 证据卫生节)
19. **证据卫生欠账**:市场引用链接 404、strangers-test 未做且无书面记录 → 提交日 link-check 机器核验全部 URL(02);每个验收动作无论做没做都要有书面记录,结论是"未做"也要写
20. **玩具 Demo 综合征(致命)**: 仅凭几百行代码、单表单接口应付交付，无多租户、无异步队列、无后台布局壳 → 生产优先原则，P4 强制跑 `verify-production-complexity.ps1` 机械拦截，未达标严禁放行。
21. **重计算同步阻塞崩溃**: 外部 API、AI 调用、耗时计算在 HTTP 请求线程中阻塞导致接口超时或挂死 → 必须解耦至 Background Worker / 任务队列，前端通过异步状态轮询或 SSE 追踪。
22. **视觉动效与真实状态机脱节 (硬编码伪高光)**: 3D 浮字或粒子在假位置爆发、金额硬编码、顶栏余额不跳动 ➔ 动效与指示必须纯粹作为 DomainEvent 真实载荷的单向投影，真值源唯一。
23. **赞助商技术虚假合规 (纸面适配器)**: 仅在代码写了 Redis/云服务适配器但从未真实跑通一次 ➔ 必须运行 SPONSOR_LIVE_CHECK 留存真实运行日志，严禁将降级方案当作默认交付。
24. **领域数学模型反向单调性 (越做分越低)**: 核心评分/计费公式缺乏单调性与边界自检，随手写粗糙公式导致破绽 ➔ 必须配备领域数学不变量单调性单元测试。

## 详细文档索引

- [00-theme-decode.md](references/00-theme-decode.md) — 命题解码:主办方意图、评分逆向、往届分析
- [01-brainstorm.md](references/01-brainstorm.md) — 头脑风暴:发散透镜、评分矩阵、避坑
- [02-market-research.md](references/02-market-research.md) — 市场调研:竞品矩阵、差异化、快证据、link-check、"AI在哪"预演
- [03-product-definition.md](references/03-product-definition.md) — 产品定义:magic moment、MoSCoW、演示脚本
- [04-build-playbook.md](references/04-build-playbook.md) — 快速构建:万行级分阶段装配(M0-M4.5)、多代理分工、冷启动演练、真实链路
- [05-polish.md](references/05-polish.md) — 企业级 UI 打磨:Layout Shell、Cmd+K、高级 DataTable、Form Wizard、视觉验收环
- [06-pitch-submit.md](references/06-pitch-submit.md) — 路演:故事弧、demo脚本、Q&A、提交清单
- [07-judging-rubrics.md](references/07-judging-rubrics.md) — 评分标准汇编(Devpost/MLH/大厂赛/Web3赛)
- [08-production-standard.md](references/08-production-standard.md) — 交付规模分级、生产级复杂度硬性底线(Complexity Floor)、反玩具十诫
- [09-tech-architecture.md](references/09-tech-architecture.md) — 选型四步法、脚手架规范、Clean Architecture / DDD 架构质量门
- [10-orchestration.md](references/10-orchestration.md) — 技能编排:本机注册表、三种引用方式、缺失技能安装流程、编排路由
- [11-enterprise-complexity-architecture.md](references/11-enterprise-complexity-architecture.md) — 万行级复杂生产系统架构与装配工程蓝图(8大子系统、分阶段装配流水线、多子代理并行机制)
- [12-winning-ui-patterns.md](references/12-winning-ui-patterns.md) — 顶级黑客松获奖作品逆向工程: 四大界面范式与产品思维模型 (PolyAgents, AudiThor, Voodo, Storylayer 案例解构)
- [13-winning-knowledge.md](references/13-winning-knowledge.md) — 顶级黑客松夺奖知识库全集 (30个真实赛事与获奖团队核验来源)
