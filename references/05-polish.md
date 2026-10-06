# P5 企业级 UI 打磨与视觉验收工程(05)

> **目标**: 杜绝业余感与玩具感，交付具备 **现代高阶 SaaS 质感、完整设计系统、深层交互细节与工业级完备性** 的用户界面。
> 评委的第一眼视觉决定了对整体工程质量的心理锚定。不仅要好看，更要有严谨的信息层级、无障碍可达性与跨端自适应。

---

## 一、界面布局体系：双轨并立（传统高阶控制台 vs 非传统沉浸隐喻）

在 P5 视觉工程中，首先明确作品所绑定的主交互形态（依据 03-definition.md 与 12 号文档）：
- **若用户指定了特定风格**（如像素风、3D、复古操作系统、赛博终端），**绝对遵从用户意志**，跳过传统后台壳，按形态 B 打造专属世界观；
- **若项目属于严肃 B2B / DevTool / 金融运维**，采用形态 A 标准现代化管理控制台。

### 形态 A: 现代化企业级应用壳 (Enterprise Application Shell)
```
┌──────────────────────────────────────────────────────────────────────────────────┐
│ [Logo] Workspace: [Acme Corp ▾] | Breadcrumbs: Project > Analytics  [Cmd+K] [🔔] [Avatar ▾]│
├──────────────┬───────────────────────────────────────────────────────────────────┤
│ 📁 Overview  │  [KPI Metric: Revenue] [KPI: Active Tasks] [KPI: System Health]   │
│ 📊 Analytics │  ───────────────────────────────────────────────────────────────  │
│ ⚡ Pipelines │  [Filter: Status ▾] [Filter: Range ▾] [Search...]   [+ New Task]  │
│ 👥 Team      │  ┌─────────────────────────────────────────────────────────────┐  │
│ 🛡️ Audit Log │  │ Advanced DataTable (Multi-sort, Facets, Columns, Bulk-ops)  │  │
│ ⚙️ Settings  │  └─────────────────────────────────────────────────────────────┘  │
│ ──────────── │  ┌───────────────────────────────┐ ┌───────────────────────────┐  │
│ [Collapse ◀] │  │ Real-time Event Stream / Log  │ │ Metrics Chart (Recharts)  │  │
│ [v2.4.0 Live]│  └───────────────────────────────┘ └───────────────────────────┘  │
└──────────────┴───────────────────────────────────────────────────────────────────┘
```
- **响应式折叠侧边栏 (Collapsible Sidebar)**: 分组导航，动态状态角标动画，底部收折按键；
- **全局顶部导航 (Enterprise TopNav)**: 多工作区选择、动态面包屑、Cmd+K 快捷面板、通知抽屉、主题切换。

### 形态 B: 沉浸隐喻与非传统舞台 (Spatial & Immersive Metaphors, 见 12)
- **2D 像素小镇 / 虚拟沙盒 (Pixel World / Canvas)**: 全屏 HTML5 Canvas / Phaser.js 瓦片地图视口，角色走动与头顶状态气泡，8-bit 等宽像素字体 (`Press Start 2P`)、NES.css 像素对话框、Web Audio 合成音效；
- **3D 空间宇宙 / 数字孪生 (Three.js / React Three Fiber)**: 全屏 3D WebGL 视口，轨道控制器 (OrbitControls)，星系/微缩物理模型，柔和泛光 (Bloom)、半透明玻璃态 HUD 悬浮抬头数据窗；
- **复古 OS / 赛博黑客终端 (Retro OS 95/98 / Terminal)**: 桌面图标、任务栏、WinBox 多层自由拖拽移动窗口，98.css / XP.css 像素灰底双层边框、CRT 扫描线微特效、等宽 ASCII 日志流；
- **无限探索白板 (Infinite Canvas)**: React Flow / tldraw 力导向节点平移缩放空间，连线流动微动效，右侧属性检查抽屉；
- **多轨音频/音波剪辑工作台 (DAW / Waveform Stage)**: Wavesurfer.js / Web Audio 实时声波频谱流，拖动播放磁头，拟物阻尼感音量旋钮；
- **物态模拟器 (Physical Simulators / Receipt Roll)**: 模拟复古热敏纸收据吐出、便携式对讲机外壳、交互式日漫分镜翻页。

**不论采取何种非传统形式，组件级无裁切检测(`ui-audit-components.mjs`)依然强制执行**：像素对话框文字不能溢出、3D HUD 按钮热区必须 ≥ 20px、复古窗口标题必须完整。

---

## 二、四大企业级交互核心组件规范 (The 4 Core UI Engines)

大型复杂系统必须通过工业级组件库承载多维度业务操作：

### 1. 高级数据表格引擎 (Advanced DataTable)
- 基于 TanStack Table，禁止写死简易 `<table>`：
  - **多列复合排序**: 点击表头支持升序、降序与取消排序；
  - **分面筛选芯片 (Faceted Filter Chips)**: 状态、类型、时间区间的独立下拉多选标签；
  - **列显隐控制器 (Column Visibility Toggle)**: 用户可自主勾选隐藏或展示特定列；
  - **行选择与批量操作工具栏 (Bulk Actions)**: 勾选多行时顶部浮现批量删除、批量导出、批量状态变更栏；
  - **服务器端分页与条数切换**: 支持 10/20/50/100 条每页切换；
  - **数据导出功能**: 支持导出当前过滤结果为 CSV 或 JSON 文件。

### 2. 多步向导与高级表单引擎 (Form Wizard Engine)
- 核心业务流程(创建任务、配置流水线、系统初始化)严禁一坨大表单滚到底：
  - **分阶段向导 (3-4 步骤指示器)**: 步骤完成态打勾、进行态高亮、未激活态置灰；
  - **Zod 强类型逐步校验**: 下一步时仅校验当前步骤字段，报错精准锚定到输入框；
  - **草稿自动持久化**: 刷新页面或回退上一步保留已填内容；
  - **确认概览页 (Review Step)**: 最终提交前渲染配置汇总卡片与变更差异。

### 3. 指标看板与可视化大盘 (Analytics Dashboard)
- **KPI 核心指标卡 (Metric Cards)**:
  - 包含主数值、趋势环比徽章(`+12.5% vs last week` 绿色带箭头)；
  - 内嵌 7 天走势迷你折线图 (Sparkline)；
  - 配套鼠标悬停 Tooltip 详情。
- **专业图表体系**: 采用 Recharts 或 ECharts，保证图表自适应容器宽度、暗色模式配色适配、图例交互与十字线指示器。

### 4. 健壮的状态反馈体系 (State Feedback Stack)
- **骨架屏全量覆盖 (Skeleton Screens)**: 表格、卡片、图表在数据加载期间严禁出现白屏或生硬的大转圈，必须按照最终布局渲染骨架流动高亮。
- **富有行动力的空状态 (Actionable Empty States)**: 表格筛选无结果或初始无数据时，展示规范矢量插画、一句话解释原因、明确的主操作按钮(如"立即创建第一个工作流")。
- **破坏性操作二次确认抽屉/弹窗 (Confirmation Modals)**: 涉及删除、回滚、停用等高危操作，必须弹出明确警示对话框，关键操作要求输入确认词。
- **层叠 Toast 消息栈**: 统一管理 success/error/info 通知，支持点击查看详情或重试动作。

---

## 三、视觉验收循环 (Visual Acceptance Loop — §0.5)

界面不是凭想象写出来的，必须**以真实渲染的屏幕像素为依据，持续迭代至少 2-3 轮**：

```
第 1 轮: 启动服务 ──► ui-shot.ps1 (桌面+移动端截图) ──► 三问视觉评审 ──► 发现排版/对比度/组件缺陷
                                                                          │
第 2 轮: 定向重构代码 ──► 重新截图 ──► 像素级对比 ◄─────────────────────────┘
                                  │
                                  ▼
第 3 轮: axe a11y 走查 ──► 终局收敛 (留存 iterations/round-N/ 对比图集)
```

### 1. 自动化截图命令
```bash
# 跨平台通用 Python (Linux / macOS / Windows)
python scripts/ui_shot.py --url "http://localhost:3000/dashboard" --out-dir "hackathon-run/iterations/round-1" --tag "dashboard" --expect-text "产品名称"

# 或 Windows PowerShell
powershell -File scripts/ui-shot.ps1 `
  -Url "http://localhost:3000/dashboard" `
  -OutDir "hackathon-run/iterations/round-1" `
  -Tag "dashboard" `
  -ExpectText "产品名称"
```
- 严禁假阳性：`-ExpectText` 自动检验关键标题，若捕获到浏览器错误页(`ERR_CONNECTION_CLOSED` 等)立即告警中断。

### 2. 视觉评审三问 (必须如实记录在 iterations/round-N/visual-reviews.md)
1. **与国际一线 SaaS 竞品(如 Linear, Stripe Dashboard, Vercel)并排，这份作品像商业级成熟软件吗？差距在哪个层级(间距、对比度、字体层级、组件质感)？**
2. **第一眼最丑、最粗糙的三处是什么？(必须列出 Top 3 具象缺陷，并作为下一轮必改项)**
3. **信息架构是否清晰？用户在 5 秒内能否辨别核心指标并找到主要操作入口？**

### 3. 定向优化与对比收敛
- 针对 Top 3 缺陷实施重构，并使用相同参数重截放入 `round-2`；
- 前后截图差异必须肉眼可辨(如：粗糙白底表格变为带分面过滤的高级 Data Grid；文字墙变为 KPI 脉搏看板)；
- 至少一轮执行 `axe-core` 或 `Lighthouse` 走查，确保无严重可达性违规。

---

## 三点五、UI 层全覆盖遍历审计 (UX Crawl & Click-Through Audit — 用户实报事故催生的强制红线)

**核心认知:后端接口全绿 + 单测全绿 ≠ 前端 UI 层可用。** 真实用户会遇到的三类问题只有"在 UI 层面真实操作"才能暴露:
- **显示缺陷**:水平溢出、内容被截断、窄屏错位、白屏加载卡死;
- **点击报错**:点某按钮/入口直接弹"无法连接"或未捕获异常(后端全绿也拦不住——SSR 数据掩盖后端状态、前端调用参数与接口契约不符、组件运行时崩溃);
- **入口遗漏**:某页面/组件根本没被接线(交付目录空壳、运行目录与交付目录分离)。

### 遍历审计脚本范式(每项目落两份)
**① 整页遍历 `frontend/scripts/shot-all-pages.mjs`**
```js
// Playwright: 登录 → 遍历全部可达路由 → 每页:
//  1. 桌面(1440)与窄屏(390)双截图, fullPage
//  2. 溢出检测: document.documentElement.scrollWidth > clientWidth + 2 → 记 OVERFLOW-X
//  3. 零容错采集: pageerror / console.error / HTTP>=400 响应(含 API)
//  4. (点击遍历版)页内全部 button/link 逐个真实点击一次, 断言无未捕获错误与连接错误横幅
// 产出: 每页截图 + ux-audit 报告(console/page/http errors 清单)
```
**② 组件级裁切审计 `frontend/scripts/ui-audit-components.mjs`(精确到组件)**
```js
// 对每页全部 button/select/input/[role=button] 元素逐个检测:
//  1. 垂直裁切: el.scrollHeight > el.clientHeight + 2 → V-CLIP(如分页器"20 条/页"文字裁半)
//  2. 热区过小: 可交互元素 rect.height < 20px → TINY(如表头排序按钮 h=17)
//  3. 文档横向溢出 + pageerror/console.error/HTTP>=400 一并采集
// 产出: 逐元素 CLIP/TINY 清单(带元素标签与文本), 有 FAIL 退出码 1
```
参考实现规范: `frontend/scripts/`(shot-all-pages.mjs / ui-audit-components.mjs——实测可机械化抓出表头按钮过小、组件运行时崩溃与截断缺陷)。

### 验收硬标准(P5 离场 + 提交前各跑一遍,修复后必须回归重跑至清零)
- [ ] 全部可达页面截图归档(桌面+窄屏),逐张过目——**不许只看首页**
- [ ] 溢出检测:所有页面 OVERFLOW-X = 无
- [ ] console.error / pageerror / HTTP≥400 采集清单 = **空**(或每条有书面豁免说明)
- [ ] **组件级裁切检测(ui-audit-components)**:V-CLIP / TINY = 0——精确到每一个 button/select/input,任何文字垂直裁切(如分页器"20 条/页"只露半截)都不合格
- [ ] **叙事-数据一致性审计(R12 评委新增维度, 真值源投影律)**:
  1. 凡 UI 展示的金额、状态、计数、收益浮字(如 "+N cr"、余额卡片、进度百分比、粒子爆发位置)，**必须严格是领域事件 (`DomainEvent`) 的单向响应投影**；
  2. 静态代码扫描：禁止在 JSX 或动效组件中硬编码任何非零演示数字常量；
  3. E2E 增量断言：提交订单前后必须断言余额差值精准等于结算额 ($\Delta \text{Balance} == \text{Payout}$)，严禁仅断言元素可见；
  4. 动态数据必须接入 1-2s 轮询或 SSE 保持实时响应，严禁挂载时拉取一次后永不更新；
  5. 严禁“说谎瞬间”：例如庆祝动画放烟花但金额与真实账本脱节、或者任务在楼宇 A 完成却在楼宇 B 爆破，任何脱节直接判定为诚信硬伤扣分！
- [ ] **生产打包体积与代码分割预算 (Bundle Budget)**:
  - 执行生产构建 (`vite build` 或 `next build`) 时，单 JavaScript Chunk 体积必须 **≤ 500KB**；
  - 针对 Three.js、React Three Fiber、Recharts、ECharts 等重型可视化与 3D 模块，强制采用动态引入 (`React.lazy` / `next/dynamic`) 实施路由与组件级按需加载，彻底消灭大型单体 Bundle 警告！
- [ ] **点击遍历**:每一个按钮/入口/表单提交都被真实点击过一次且行为符合预期;破坏性操作按钮(删除/退款/停用)单独验证确认弹窗
- [ ] 修复后全量回归(不是只回归修复页)——一个组件的修复常牵连其他页

### 复合控件强制使用成熟组件库(优先第三方,禁止手搓易裁切控件)
分页条数选择、日期范围、级联筛选、多人选择等**复合控件,一律使用组件库标准组件**(shadcn/Radix Select、Combobox、DatePicker),严禁手写原生 `<select>`/`<input>` 凑合:
- 原因:原生控件高度与字体度量在各平台不一致,**固定矮容器(h-7/h-8)下中文文字必然垂直裁切**(实战实锤:分页器"20 条/页"只露上半截),且浮层无法定制、会被父容器 overflow 裁切;
- 项目标准:`components/ui/select.tsx`(基于 `@radix-ui/react-select` 的 shadcn Select,浮层走 Portal 不受父容器裁切);
- 手写控件的唯一豁免:通过组件级裁切检测(V-CLIP=0)+ 三平台(Chrome/Edge/窄屏)截图验证。

### 已知高频病灶(实战抓到的)
| 病灶 | 典型形态 | 修法 |
|---|---|---|
| 组件 props 引用不稳定 | columns/数据数组每渲染重建 → TanStack memo 断链抛 undefined | 调用方 useMemo 包裹;组件侧给 props 默认值(data=[]) |
| button 嵌套 button | DropdownMenu 外层 button 包 trigger Button → hydration 错误 | 外层改 div[role=button]+键盘处理 |
| 原生 select 文字垂直裁切 | h-7/h-8 容器 + Windows/Chrome 默认度量 → "20 条/页"只露半截 | 换 Radix/shadcn Select(组件库);或高度 ≥36px+leading 校验 |
| SSR 掩盖后端状态 | 首页 SSR 数据正常,按钮点击才暴露后端挂了 | 点击级验收(04 红线)+错误横幅断言 |
| 演示环境与交付目录分离 | start-all 指向归档目录,交付目录是脚手架空壳 | 交付目录一致性死法(08 §4-9)+冷启动演练以交付目录为准 |

---

## 四、生产级 UI 验收清单 (P5 离场硬门槛)
- [ ] 完整企业级 Layout Shell 落地 (可折叠 Sidebar + 带有 Cmd+K/面包屑的 Header)
- [ ] 核心列表页全部升级为高级 DataTable (支持多字段排序、分页、筛选与列显隐)
- [ ] 核心业务具备向导式 (Wizard) 表单流与 Zod 类型校验
- [ ] 仪表盘具备指标卡 (含 Sparkline 趋势微图) 与自适应图表
- [ ] 四态完整：所有异步区域骨架屏加载、空状态引导、错误人话重试、成功 Toast
- [ ] 视觉环至少执行 2 轮，前后对比截图与评审记录完整留存在 `iterations/`
- [ ] 移动端断点 (390px) 适配自查通过，无水平溢出或变形
- [ ] 严格遵守 Design System Tokens，代码中无随意散落的魔法样式值
