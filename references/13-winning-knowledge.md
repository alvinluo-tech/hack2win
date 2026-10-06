# 黑客松夺奖知识库

> 用途: 供"参赛方法论 skill"引用的知识底座。
> 编制日期: 2026-10-04。方法: WebSearch + WebFetch 对真实来源逐条核验。
> 标注约定:
> - **[已核验]** = 本次通过抓取原文确认了内容,可放心引用
> - **[搜索快照]** = 仅通过搜索引擎结果片段确认了存在与部分表述,引用前建议再点开原文
> - **[经验推测]** = 无直接可靠来源,由多条来源综合推导或为行业常识

---

## 1. 官方评分标准汇编(按赛事)

### 1.1 Devpost(最主流的线上黑客松平台)

- **官方默认评分维度**(帮助中心原文概括): 典型 criteria 为 **idea 质量(creativity/uniqueness 创意与独特性)、implementation 质量(实现完成度)、potential impact(潜在影响)**;三项**通常等权重**——"Criteria are usually weighted equally and this is how the Devpost judging platform is set up",平台不支持差异化权重,权重不同的赛项需走线下评分。
  来源: [已核验] https://help.devpost.com/article/64-judging-public-voting
- **评委工作量与评分方式**: Devpost 通常**给每位评委最多 30 个项目、预期打分约 5 小时**,评审窗口 1-2 周;线上评审对每条 criterion 打 **1-5 星**("1 star is the lowest rating and 5 is the highest"),星标是唯一反馈手段;评委可对利益冲突项目选择 "I recuse myself"(回避)。
  来源: [已核验] https://help.devpost.com/article/103-how-to-judge-an-online-hackathon 、https://help.devpost.com/article/64-judging-public-voting
- **社区投票(Community Choice)的教训**: Devpost 官方承认公开投票存在 "fraudulent votes and attempts to game the system",建议把该奖额设小、且不要直播票数。→ 含义: 社区奖靠传播,主奖靠评委。
  来源: [已核验] https://help.devpost.com/article/64-judging-public-voting
- 评分流程类帮助文档入口: https://help.devpost.com/category/27-judging-announcing-winners [已核验]
- **Devpost 承办的大厂赛事实例**: Microsoft AI Agents Hackathon 2025(microsoft-ai-agents-hackathon-2025.devpost.com),其评分被第三方资料描述为**四维各 25%**(quality/innovation、implementation、design、impact 类) [搜索快照,权重表述未在官方页核验]。

### 1.2 MLH(Major League Hacking,最大的学生黑客松联盟)

- **官方标准规则里的评分条款**(MLH/mlh-hackathon-rules 仓库 Rules.md): 项目**在 Technology、Design、Completion、Learning 四项上被等权评分**;原文明确**不**按代码质量、pitch 演讲水平、idea 好坏、实用性打分("judged equally on Technology, Design, Completion, and Learning")。
  来源: [已核验] https://github.com/MLH/mlh-hackathon-rules/blob/master/Rules.md
- **参赛资格硬规则**(同上): "All work on a project should be done at the hackathon"(所有工作必须在赛内完成);可以用以前的 idea 但 "do not re-use code";可用开源库/框架;截止后只允许修 "a few lines of code" 的小 bug,不允许加新功能;Demo 被强烈鼓励而 pitch/演讲反被弱化("Demos are strongly encouraged... you aren't judged on pitch quality");"It's okay if you didn't finish your hack"。
  来源: [已核验] https://github.com/MLH/mlh-hackathon-rules/blob/master/Rules.md
- **AI 使用条款**(主办方指南的建议规则文本): "You may use LLM/ChatGPT/AI, but must state how you did so in your Devpost submission"(可以用 AI,但必须在提交里说明怎么用的);项目不能是 "a reskin of an existing AI tool";不披露 AI 使用会**被取消资格**并上报 cheating@mlh.io。
  来源: [已核验] https://guide.mlh.com/general-information/judging-and-submissions/rules-for-your-hackathon.md
- **MLH 评审组织方式**(官方主办方指南): 强烈推荐**科学展览式(Science Fair)**现场评审;每队被至少看 3 轮;时间公式 "4 mins per project. 2 minutes for presentation + demo, 1 minute for questions from judges and score compilations, and 1 minute for judge travel";要求团队同时提交 **2 分钟视频**,且视频 "be a demo of their hack, not a presentation";胜出机制用 **stack ranking**(每评委报 top3,第一得 3 分/第二 2 分/第三 1 分,归一化不同评委的宽严差);宣布前对所有 winners 做 **cheating check**;提醒评委 "Focus on learning over profit"。
  来源: [已核验] https://guide.mlh.com/general-information/judging-and-submissions/judging-plan.md

### 1.3 ETHGlobal(Web3 最大黑客松系列)

- 官方不发布统一评审规则手册,**criteria 挂在每个赛事页**: 如 Cannes 2026 页面 "⚖️ Judging Criteria. Judges will evaluate your project based on five categories: Technicality..."(五个类别,含技术难度/复杂度等) [搜索快照];第三方对 Cannes 2025 的复盘归纳为: **Technical complexity(技术复杂度)、Originality(原创性)、Real-world utility(现实实用性)、UI 质量、Overall(整体完成度与惊艳度)** [搜索快照];2026 New York 赞助赛道示例: "Projects will be judged on: Innovation, Product quality, Technical execution, Effective use of Composer(赞助技术)"——即**创新/产品质量/技术执行/是否用好赞助方技术**四条 [搜索快照]。
  来源: https://ethglobal.com/events/cannes (官方页,评分区为动态加载) ;币付 Media 对 Cannes 2025 的复盘;ethglobal.com New York 2026 finalist 页快照
- 提交走 ETHGlobal Showcase: 项目页 + demo 视频 + 仓库,要求赛期窗口内构建。[搜索快照]

### 1.4 Google

- **Solution Challenge(GDSC/GDG 全球赛)**: 官方 judging criteria 页(developers.google.com/community/gdsc/solution-challenge/judging-criteria)要点: **对 UN 17 项可持续发展目标(SDG)的针对性、Google 技术栈的使用、设计/可用性、完成度(有可运行 demo)、可扩展性** [搜索快照;developers.google.com 在本次环境无法直连核验]。
- **Gemini API Developer Competition(2024, Devpost 承办)**: 按四大奖项类别评(约 Social Impact / Most Commercially Viable / Most Useful / Most Entertaining),critieria 含 **对 Gemini API 的使用与展示、新颖性、设计/UX、实用性/影响力**,及"是否为 idea 阶段"等资格要求 [经验推测——官方页 ai.google.dev/competition 当前无法直连,此条请在使用前核验]。

### 1.5 跨赛事公约(综合观察)

综合以上,黑客松评分维度的高频并集:
1. **创新/原创性**(Devpost idea quality、ETHGlobal Originality)
2. **技术实现与难度**(MLH Technology、ETHGlobal Technicality)
3. **完成度/可运行**(MLH Completion、Devpost implementation、各赛 "working demo" 硬要求)
4. **设计/UX**(MLH Design、ETHGlobal UI)
5. **实用性/影响力**(Devpost impact、ETHGlobal utility、Solution Challenge SDG)
6. **演示与表达**(多数赛事计入或作为门槛;MLH 明确不单列)
7. **切题度/合规**(赛题契合、赞助技术使用、赛内完成、AI 披露)——常为隐藏一票否决项

---

## 2. 获奖者方法论(按主题归组)

### 2.1 选题策略

- **用销售方法论做选题调研**: freeCodeCamp 作者 Moshe Siegel 把获奖归功于赛前研究——用 SPIN Selling 四步(弄清现状→提问找问题→挖掘影响→量化解决价值)找到真痛点(价格维护每周耗 30 分钟/人);他的信条来自上级: "I focus on projects that make an impact"。评委评分四项: **originality, business impact, prototype completeness, pitch strength**。
  来源: [已核验] https://www.freecodecamp.org/news/how-i-won-the-hackathon/
- **选题要"一句话讲清 + 能点燃想象"**: HN 多次获奖者建议选 "something easy to explain that also captures peoples imagination"。
  来源: [已核验] https://hn.algolia.com/api/v1/items/27831250
- **避开拥挤赛道、错位竞争**: 连续获奖者 reidjs("2 for 2")专挑竞争少的类别——"everyone flocks to crypto/AI",他去做供应链类比赛;同时优先盯**赞助商 API 单项奖**(如 Best Use of Twilio),这是没拿总冠军也能带奖走的路径。
  来源: [已核验] https://hn.algolia.com/api/v1/items/27831250 ;单项奖策略另见 [已核验] http://alexstechthoughts.com/post/28836325740/how-to-win-a-hackathon
- **盯住赞助商/主办方动机**: 企业赛的本质是"评委=出题人",解决出题人自己的痛最容易赢(Moshe 案例中需求直接来自未来用户 planner 们)。
  来源: [已核验] https://www.freecodecamp.org/news/how-i-won-the-hackathon/
- **技术栈赛前定死**: "Pick the stack BEFORE the hackathon starts. Debating tech stack during the event wastes 2-4 hours that you can't afford."(Reskilll,2026)
  来源: [搜索快照] https://reskilll.com (Hackathon Tech Stack Guide 2026)

### 2.2 组队策略

- **互补技能优先**: 开发者应找设计师组队、反之亦然;设计师决定 "those final touches"。
  来源: [已核验] http://alexstechthoughts.com/post/28836325740/how-to-win-a-hackathon
- **"队里有个大牛"比什么都重要**: NickSingh 复盘多次获奖经历——每个夺冠队里都有一个 "10X" 程序员。
  来源: [已核验] https://hn.algolia.com/api/v1/items/27831250
- **工程师 1-2 个就够,加一个行业内部人**: reidjs——"you really only need 1, max 2 engineers",行业黑客松里懂行业的人价值极高。MLH 建议队伍 1-4 人(hackers 在 "teams of a maximum size of 4" 时表现最好)。
  来源: [已核验] https://hn.algolia.com/api/v1/items/27831250 ;https://guide.mlh.com/general-information/judging-and-submissions/rules-for-your-hackathon.md
- **分工前置、环境预置**: 赛前约定前后端数据契约、装好环境与版本控制,"hit the ground running";设计师提前一周用共享文档对齐技能与想法(freeCodeCamp 设计师文)。
  来源: [已核验] https://hn.algolia.com/api/v1/items/1366795 ;https://www.freecodecamp.org/news/what-every-designer-needs-to-know-before-their-first-hackathon/

### 2.3 时间分配

- **里程碑三段式**: 周五规划、周六全速开发、周日打磨+上线+写博客(Nervetattoo 的 100 小时三连赛经验);头脑风暴硬上限 30 分钟;"Don't obsess over a great user experience in the beginning"——先功能后视觉。
  来源: [已核验] https://hn.algolia.com/api/v1/items/1366795
- **范围 = 1/4 时间法则**: zachlatta(Hack Club 创始人): "Time is your biggest constraint... 选一个你能在 1/4 规定时间内做完的项目",剩下的时间给意外和打磨。
  来源: [已核验] https://hn.algolia.com/api/v1/items/6419839
- **可伸缩目标**: lsiebert——选 "a target that you can make worse/better depending on time constraints"(时间多就做厚、时间少就砍到能跑)。
  来源: [已核验] https://hn.algolia.com/api/v1/items/6419839
- **MVP 先行 + 缓冲**: 设计师经验——给 MVP、彩排、提交都设 deadline 并内置 buffer,延误是 "a near guarantee";只对真会被开发出来的界面做高保真。
  来源: [已核验] https://www.freecodecamp.org/news/what-every-designer-needs-to-know-before-their-first-hackathon/
- **睡觉也能赢**: 冠军复盘 jero.zone: 设计走 "vivid and bold" 路线、拿了 "a solid 8 hours of sleep" 照样横扫赛道奖。HN 亦有人直言 "you code better when well rested"。
  来源: [已核验] https://jero.zone/posts/meal-plan-wrapped ;https://hn.algolia.com/api/v1/items/27831250

### 2.4 实现与 Demo 策略

- **前端为王、后端可硬编码**: reidjs——"prioritize frontend/visual code and sponsor APIs; the backend can almost always be hardcoded";把精力花在评委看得见的东西上。
  来源: [已核验] https://hn.algolia.com/api/v1/items/27831250
- **只做一件事,做到能演示**: "Do one thing well——build something focused and center your demo on that single feature."
  来源: [已核验] http://alexstechthoughts.com/post/28836325740/how-to-win-a-hackathon
- **测试可跳过、版本控制不能省**: "Don't write tests, don't review code and just go for it";但 "use version control despite the temptation to skip"。
  来源: [已核验] https://hn.algolia.com/api/v1/items/1366795
- **真实用户=降维打击**: jero.zone 冠军项目(校园餐饮数据 Wrapped)赛前在校内发传单、在 Sidechat 上造势 "went (relatively) viral",几天内几百学生真实使用——评委面前"traction"直接碾压,连拿 general track + most complete 项目奖。
  来源: [已核验] https://jero.zone/posts/meal-plan-wrapped
- **评委只看得见主讲人**: "judges will only see what the speaker presents"——尽早定主讲、带队友排练(strdr4605,40+ 场黑客松经历);Moshe 因故不能上场时,用 SPIN 问题把要点"教会"队友,让真正的用户(planner)用业务语言讲出来,反而更可信。
  来源: [已核验] http://strdr4605.com/how-to-win-a-hackathon ;https://www.freecodecamp.org/news/how-i-won-the-hackathon/
- **讲故事**: "People like stories"——用问题→解法的叙事框住演示。
  来源: [已核验] http://alexstechthoughts.com/post/28836325740/how-to-win-a-hackathon

### 2.5 获奖的"账外收益"(为什么值得打)

- 30 小时做出的 credential 换来远超日常工作的曝光: 有队伍周六还是无名之辈、周一已在向 Dave McClure 和 Naval pitch;也有人靠一个月内的获奖经历进 YC 公司、过 Google 面试。
  来源: [已核验] https://hn.algolia.com/api/v1/items/3677056
- **"不拿第一也算赢"的九个位置**: 新人/程序员/设计师/主讲/经理/导师/主办方/志愿者/赞助方,每个角色都能刻意收获技能与人脉;"Treat winning first place as a bonus——the cherry on top"。
  来源: [已核验] http://strdr4605.com/how-to-win-a-hackathon

---

## 3. 常见失败模式 Top10(评审与复盘视角)

1. **只有 PPT/截图,没有能跑的东西**——组织者抱怨评委把 "a polished presentation with nothing behind it" 排在能跑的原型前面,引发公愤;反过来 "things work" 比截图 mockup 更让评委印象深刻(评委视角原话)。
   来源: [已核验] https://hn.algolia.com/api/v1/items/9554170 ;https://hn.algolia.com/api/v1/items/1366795
2. **Scope 过大做不完**——违反 "1/4 时间法则";没有 fallback 的目标一旦翻车全程皆输。
   来源: [已核验] https://hn.algolia.com/api/v1/items/6419839
3. **Demo 现场翻车**——三天不睡做出的东西毁在 3 分钟演示上: "to stay up for three days building something awesome only to bomb the demo presentation" 是创始人眼里最可惜的失败。
   来源: [已核验] https://techcrunch.com/2014/09/01/how-to-crush-your-hackathon-demo/
4. **不切题 / 评分标准错位**——评审目标与赛事目标不一致时(如目标是 "cool" 却评出商业奖),切题团队吃闷亏;选手必须先读清 rubric 再动工。
   来源: [已核验] https://hn.algolia.com/api/v1/items/9554170
5. **违规预写代码 / 抄袭旧项目**——Salesforce $1M 黑客松丑闻: 获奖应用赛前数月已公开 demo,被指 pre-existing work,舆论要求重审;组织者层面对策是 cheating check。恶性案例: 有队伍把**上一个黑客松的整个项目**搬来再战。
   来源: [已核验] https://hn.algolia.com/api/v1/items/6802895 ;https://hn.algolia.com/api/v1/items/9554170 ;https://github.com/MLH/mlh-hackathon-rules/blob/master/Rules.md
6. **AI 不披露 / 纯套壳**——MLH 规则: 用 AI 必须在提交中说明,不做 "a reskin of an existing AI tool",违者 DQ; peer-judge 环境下 "All the ChatGPT wrappers rank poorly"。
   来源: [已核验] https://guide.mlh.com/general-information/judging-and-submissions/rules-for-your-hackathon.md ;https://hn.algolia.com/api/v1/items/43889502
7. **演示讲不到点/超时/念稿**——"you only get a few minutes and you're exhausted, so plan your words";熬夜后即兴发挥是高危动作。
   来源: [已核验] https://techcrunch.com/2014/09/01/how-to-crush-your-hackathon-demo/
8. **在评委面前走平凡流程**——现场注册账号、打字输入等环节;正确做法是跳过或预填("pre-copy needed text to your clipboard")。
   来源: [已核验] https://techcrunch.com/2014/09/01/how-to-crush-your-hackathon-demo/
9. **纯段子项目**——整场 pitch 当笑话讲,评委会因 "lasting value beyond the weekend" 不敢给奖;段子做佐料,不做主菜。
   来源: [已核验] http://alexstechthoughts.com/post/28836325740/how-to-win-a-hackathon
10. **提交材料敷衍 / 忘交**——很多线上赛按提交页+视频评审,不在决赛名单里连 3 分钟都没有;"Start early as it will pay dividends"。视频要 "be a demo of their hack, not a presentation"(MLH)。
    来源: [已核验] https://techcrunch.com/2014/09/01/how-to-crush-your-hackathon-demo/ ;https://guide.mlh.com/general-information/judging-and-submissions/judging-plan.md

**补充黑名单**(未进前十但高频): 团队无分工导致集成地狱(HN 1366795);UI 粗糙劝退评委(设计师文: 设计是 "final touches");过度营销话术引起评委怀疑("anything impressive-looking raises suspicion"——赞助商视角,HN 43889502)。

---

## 4. Demo 与路演手册

### 4.1 时间结构(TechCrunch 四步法,适配 3 分钟)

来源: [已核验] https://techcrunch.com/2014/09/01/how-to-crush-your-hackathon-demo/

1. **开场 20-30 秒定场景**: "explain the problem you're solving, or the status quo you're greatly improving"——几句话讲清为什么做它,不贪长。
2. **中间 1.5-2 分钟演示真东西**(最重要的一段): 展示能塞进时间槽的功能,顺带点出关键技术与攻克的技术难点;评委必须看到 "resolution to the problem you initially identified"——首尾呼应。
3. **收尾 30 秒卖愿景**: "Spend a sentence or two on the project's potential and ambitions"。
4. **提交页是第二赛场**: 问题、功能、技术栈、学到了什么、队友署名 + 截图 + 视频,一样别少。

### 4.2 MLH 现场评审的物理约束(决定你有多少秒)

来源: [已核验] https://guide.mlh.com/general-information/judging-and-submissions/judging-plan.md

- 每队 **4 分钟**: 2 分钟演示 + 1 分钟问答 + 1 分钟评委走路。评委被明令 "only have 3 minutes per team"。
- 每个评委连看一排桌子,采用 stack ranking 报 top3 → 你的目标不是"让评委懂",是**进这位评委的 top3**。
- 提交的 2 分钟视频要 "be a demo of their hack, not a presentation"(录屏实拍优先,不是幻灯片朗读)。
- 评委被提醒 "Focus on learning over profit"——把商业神话讲到天上未必加分。

### 4.3 开场钩子与注意力

- 用"现状之痛"开场而非自我介绍/团队介绍(TechCrunch 步骤 1)。[已核验]
- 评委疲劳是常态: Devpost 线上评审的典型负荷是 30 项目/5 小时(≈10 分钟一个),线下是 3 分钟一队——**前 30 秒决定他给不打断你的机会**。[已核验: 数据来源 1.1/4.2;推论部分为经验推测]
- 把 URL/项目名放在每页幻灯片与口头反复出现(冠军复盘实操)。[已核验: https://jero.zone/posts/meal-plan-wrapped]
- 幽默可用: 加幽默可拿 people's choice,但 "just be wary of making your entire pitch a joke"。[已核验: alexstechthoughts]

### 4.4 Q&A 应对

- 评委问答通常 1 分钟,问的是澄清性问题(science fair 形式下边看边问)。[已核验: MLH judging plan]
- **主动交底硬编码/未完成部分**: 评委反感 "polished presentation with nothing behind it";把"这部分是 stub"说在前面比被戳穿强。 [经验推测,基于 3.1 与 MLH 诚信规则推导]
- 技术问题答不上时回到"问题-价值"叙事;让懂行的队友(领域 insider)接行业问题。 [经验推测,综合 2.2 reidjs 与 2.4 Moshe 案例]

### 4.5 演示的工程保障

- 演示路径做成一条"生路": 预填数据、预登录、避免现场注册;**每台设备本地缓存一份**;准备好录屏兜底(网络会挂)。[已核验: TechCrunch;兜底为经验推测]
- 设计师管视觉、主讲人管叙事、工程师蹲守现场 debug——"Presentation matters. Practice yours."。[已核验: HN 6419839]

---

## 5. 获奖项目共性画像(观察案例)

**案例库(全部已核验原文):**

| 项目/事件 | 结果 | 起作用的因素 |
|---|---|---|
| Meal Plan Wrapped (Tufts JumboHack) | 横扫 general + most complete | 真实用户数百人、Spotify Wrapped 式大胆视觉、校内病毒传播 |
| PriceSeeker (企业内部赛) | 冠军 | 真实痛点+可量化的业务影响、真用户来讲 pitch、简化的务实原型 |
| Anthropic Claude Code Hackathon 相关 (Matrix OS) | top 20 | agent SDK 深度用法、Show HN 公开构建 |
| Stagehand MCP | MCP hackathon 冠军 | 填补生态空白(浏览器自动化 MCP) |
|Yorkshire 口音 AI 电话 (Vilnius) | 现场惊艳 | 硬件+AI 的实体惊艳感,48h 零代码 |
| float4 所见反例 | 赢了 | 无意义 TSP 项目靠"名企评委"投票获胜——反面教材: 评委背景决定口味 |

- **共性 1: 完成度是入场券,traction 是区分项。** 能跑 + 有人真的用过 > 一切;Willison 在 AI 时代同样指出 polished repo 半小时可生成,"somebody to have used the thing" 才是信号。
  来源: [已核验] https://jero.zone/posts/meal-plan-wrapped ;https://simonwillison.net/2026/May/6/vibe-coding-and-agentic-engineering/
- **共性 2: 切题+满足"隐藏评分项"。** 读 rubric、盯赞助技术、合规赛内完成——MLH 四维(Technology/Design/Completion/Learning)里 Learning 常被选手忽略,答辩时讲清"我们学了什么新东西"反而加分。 [已核验: MLH Rules.md]
- **共性 3: 一句话能讲清的"演示型创新"。** "easy to explain that also captures imagination";实体交互(硬件/现场设备)在 2025-2026 软件同质化后惊艳度显著回升("hardware wins big at hackathons")。
  来源: [已核验] HN 27831250 ;HN 9205177 ;blog.oscars.dev(见 §6)
- **共性 4: 故事真实、主讲可信。** 用户自己讲用户的故事 > 撰稿人念稿(Moshe 案例)。
- **共性 5: 商业叙事的权重取决于评委构成。** 企业赛/赞助商赛(评委=市场与招聘)重 impact 与可行性;社区赛/学习赛重趣味与技术胆量——先判评委再定叙事。 [已核验: Moshe 案例评委四项 vs MLH "focus on learning over profit" vs HN 9205177 adrusi "judges are often recruiter-representatives"]
- **权重观察(综合推导)**: 完成度与 demo 惊艳度是"及格线权重",创新与故事是"拉开差距权重",商业叙事是"企业赛放大器",合规(赛内完成/AI 披露/切题)是"一票否决项"。 [经验推测,基于上述多来源归纳]
- **反面画像(容易陪跑)**: ChatGPT wrapper、克隆旧项目、demo 全靠脑补幻灯片、"为赞助商塞功能"的功能堆砌。 [已核验: HN 43889502 各评论]

---

## 6. AI 辅助参赛工作流(2025-2026 新玩法)

### 6.1 规则环境

- MLH: AI 可用但**必须披露用法**,禁止纯套壳,违规 DQ。[已核验: rules-for-your-hackathon.md]
- 舆论变化: 评委/组织者对"过度精致"的项目起疑,反而**赛中真实完成的朴素作品**更能建立信任("anything impressive-looking raises suspicion"——kanavs,赞助商视角)。[已核验: HN 43889502]
- 2026 年黑客松普遍进入 "AI-native" 状态: SeaHack 24 小时内多支队伍用现代 AI 工具做出可运行 AI 创业原型;Anthropic/Claude 系列黑客松成为常态(多个 Show HN 项目自述参赛/获奖)。[已核验: freeCodeCamp SeaHack;HN Algolia hackathon+claude 检索结果]

### 6.2 软件黑客松的"惊艳度通胀"与硬件转向

- Oscar(2026): 团队整周末 "didn't look at a single line of code"——AI 时代纯软件项目贬值,两年前惊艳的 web app "tumbled into mediocrity";瓶颈从敲代码转向系统设计,"free mental RAM" 应投向硬件/实体交互;预言硬件黑客松回潮。
  来源: [已核验] https://blog.oscars.dev/posts/rip-software-hackathons-long-live-the-hardware-hackathon/
- HN 呼应: "RIP software hackathons. Long live the hardware hackathon" 284 分。[已核验: HN Algolia 列表 https://hn.algolia.com/api/v1/search?query=hackathon&tags=story&numericFilters=points%3E100]

### 6.3 倍速开发工作流(以 Claude Code 官方最佳实践为骨架)

来源: [已核验] https://code.claude.com/docs/en/best-practices

1. **Explore → Plan → Code → Commit**: 先让 agent 读代码/文档再动手——"Letting Claude jump straight to coding can produce code that solves the wrong problem";但黑客松别过度规划: "If you could describe the diff in one sentence, skip the plan."
2. **精简项目记忆**: `/init` 生成 CLAUDE.md,只放命令/风格/工作流约定——"Bloated CLAUDE.md files cause Claude to ignore your actual instructions!"(赛前把 boilerplate 的 CLAUDE.md 写好,赛中零成本)
3. **先装"验证器"再放手机器**: "Give Claude a check it can run: tests, a build, a screenshot to compare";要求 agent 贴出证据("the test output, the command it ran and what it returned")而非口头成功——这是你敢并行多开的前提。
4. **上下文是最稀缺资源**: 无关任务之间 `/clear`;连续两次改不对就 `/clear` 换更好的初始 prompt;用子代理做调研"doesn't consume your main context"。
5. **并行/多代理**: worktree 开多会话、Writer/Reviewer 分工("A fresh context improves code review");`/batch` 把改动拆给 5-30 个子代理;"Test on a few files, then run on all of them."
6. **敢试错**: Esc 打断、`/rewind` 回滚 checkpoint,"so you can experiment aggressively without fear"。

### 6.4 AI 时代的参赛范式(综合推导,标注)

- **代码不再是瓶颈,demo/数据/故事才是**: 把 AI 省下的时间强制再分配给——真实用户种子(哪怕 10 个)、2 分钟视频、提交文案、彩排、睡眠。 [经验推测,由 §2/§4/§5 推导]
- **"用过"证据链**: 录屏、GitHub commit 时间线(自证赛内完成)、真实数据看板——同时回应"套壳质疑"与"作弊质疑"。 [经验推测,由 MLH 披露规则+cheating check+Willison 推导]
- **别做 wrapper,要做"只有 agent 时代才可能"的项目**: 多代理编排、MCP 工具、硬件+LLM 接口——评委会为此类"新物种"给出 wow。 [已核验: blog.oscars.dev 案例与 Stagehand/Matrix OS 案例;判断部分为推导]
- 工具镜像: Claude Code 已被多位从业者称为当下最强编程 agent(Cole Medin 等组织者言论) [搜索快照];Node/Python 生态的 boilerplate(如 277 分的 hackathon-starter)仍是起步加速器。 [已核验存在: https://github.com/sahat/hackathon-starter]

---

## 7. 十条最重要的"一句话军规"

1. **把评分表当题目做**——项目做完要能对着 rubric 逐条自证。[来源: Devpost/MLH 官方 criteria, §1]
2. **选题三问**: 一句话能讲清吗?评委能想象吗?这条赛道挤吗?[来源: HN 27831250 + reidjs 错位竞争, §2.1]
3. **范围=1/4 时间**,剩下 3/4 给意外、打磨和睡眠。[来源: zachlatta, §2.3]
4. **先通骨架再长肉**: 第一晚就要有端到端能跑的丑版本。[来源: Nervetattoo/avk 三段式 + MVP 先行, §2.3]
5. **评委看得见的才值得写**: 前端/演示路径优先,后端可以硬编码。[来源: reidjs, §2.4]
6. **拿到 10 个真实用户再上场**: traction 是最贵的加分项。[来源: jero.zone 案例 + Willison "somebody has used the thing", §5]
7. **Demo 是预告片不是纪录片**: 痛点→真机演示→愿景,砍掉注册登录等一切平凡流程。[来源: TechCrunch 四步法, §4.1/4.5]
8. **主讲人赛前隔离彩排**,材料(2 分钟 demo 视频+提交页)当第二个项目做。[来源: strdr4605 + TechCrunch + MLH 视频要求, §2.4/4.5]
9. **AI 大胆用、老实报、讲出独特性**: 披露用法、别当 wrapper、能解释每一行。[来源: MLH AI 条款 + Hack Club "wrappers rank poorly", §6.1]
10. **睡觉是战术**: 熬夜换不来评委的 top3,头脑清醒的 3 分钟换得来。[来源: jero.zone 8 小时睡眠夺冠 + seba_dos1, §2.3;表述为推导]

> 标注: 1-9 的内核均有直接来源(见括号章节);10 与部分措辞为由来源支持的推导。

---

## 附: 来源清单(按类型)

**官方标准(一手,已核验): 7 个**
1. https://help.devpost.com/article/64-judging-public-voting
2. https://help.devpost.com/article/103-how-to-judge-an-online-hackathon
3. https://help.devpost.com/article/191-judging-at-devpost-hackathons
4. https://github.com/MLH/mlh-hackathon-rules/blob/master/Rules.md
5. https://guide.mlh.com/general-information/judging-and-submissions/judging-plan.md
6. https://guide.mlh.com/general-information/judging-and-submissions/rules-for-your-hackathon.md
7. https://help.devpost.com/category/27-judging-announcing-winners

**获奖者复盘与方法论(已核验): 8 个**
8. https://www.freecodecamp.org/news/how-i-won-the-hackathon/
9. https://www.freecodecamp.org/news/what-every-designer-needs-to-know-before-their-first-hackathon/
10. http://alexstechthoughts.com/post/28836325740/how-to-win-a-hackathon
11. http://strdr4605.com/how-to-win-a-hackathon
12. https://jero.zone/posts/meal-plan-wrapped
13. https://hn.algolia.com/api/v1/items/27831250 (How to win a hackathon, 138 分讨论帖)
14. https://hn.algolia.com/api/v1/items/6419839 (Ask HN: Best Hackathon Practices)
15. https://hn.algolia.com/api/v1/items/3677056 (How to win a hackathon, 2012)

**评审/失败模式/文化批判(已核验): 5 个**
16. https://hn.algolia.com/api/v1/items/9554170 (Ask HN: What makes a good hackathon)
17. https://hn.algolia.com/api/v1/items/6802895 (Salesforce 黑客松评审丑闻, 108 分)
18. https://hn.algolia.com/api/v1/items/9205177 (Hackathon Hackers 文化, 251 分)
19. https://hn.algolia.com/api/v1/items/43889502 (Ask HN: Hackathons feel fake now, 213 分, 2026)
20. https://hn.algolia.com/api/v1/items/1366795 (Ask HN: Hackathon tips, 含评委发言)

**Demo/路演(已核验): 1 个**
21. https://techcrunch.com/2014/09/01/how-to-crush-your-hackathon-demo/

**AI 时代(已核验): 4 个**
22. https://blog.oscars.dev/posts/rip-software-hackathons-long-live-the-hardware-hackathon/
23. https://code.claude.com/docs/en/best-practices
24. https://simonwillison.net/2026/May/6/vibe-coding-and-agentic-engineering/
25. https://www.freecodecamp.org/news/inside-seahack-24-hours-to-build-an-ai-startup/

**其他(已核验存在): 1 个**
26. https://github.com/sahat/hackathon-starter

**搜索快照级(建议引用前复核): 4 个**
27. https://ethglobal.com/events/cannes (官方,评分区动态加载)
28. https://reskilll.com (Tech Stack Guide 2026 / 50+ 赛事获奖项目分析, 2026)
29. https://developers.google.com/community/gdsc/solution-challenge/judging-criteria
30. https://hn.algolia.com/api/v1/search?query=hackathon%20claude (Anthropic 系黑客松获奖项目检索)

**检索受限说明**: 本次调研期间搜索与部分站点(mlh.com 主站、medium.com、reddit、web.archive.org、developers.google.com)间歇性不可达;Devpost 赛事详情页为 JS 渲染无法直接抓取,相关表述以帮助中心(可核验)与搜索快照替代。OpenAI/Meta 官方黑客松评分原文未能核验到稳定一手 URL,文中未单独列出,相关模式可参照 §1.5 公约与 Microsoft/Google 条目。
