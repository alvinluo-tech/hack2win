# 评分标准汇编 — 逆向"考卷答案"(研究版,带来源)

> 用途:P0 命题解码时对照。目标比赛有官方 rubric 时以官方为准。
> 来源:全文论断核验自官方文档/获奖者复盘,完整来源清单见 [references/13-winning-knowledge.md](13-winning-knowledge.md)(30个来源,26个已核验原文)。

## 1. 官方标准(已核验原文)

### Devpost(线上赛主流平台)
- **默认三维度等权**:idea 质量(创意/独特性)、implementation(实现)、potential impact(潜在影响)——"Criteria are usually weighted equally",平台不支持差异化权重
- **评委负荷**:每位评委最多 30 个项目/约 5 小时,窗口 1-2 周,每维打 1-5 星——**≈10分钟/项目,前30秒决定他去留**
- 社区投票有刷票问题(官方承认),社区奖靠传播,主奖靠评委
- 来源: help.devpost.com/article/64 、/article/103

### MLH(最大学生赛联盟)
- **四维等权:Technology / Design / Completion / Learning**;官方原文明确**不**评:代码质量、pitch 水平、idea 好坏、实用性
- **合规一票否决**:全部工作赛内完成(可用旧idea不可复用代码)、截止后只许修小bug、**用AI必须在提交中说明用法**、禁止纯套壳("reskin")——违规 DQ 并上报 cheating@mlh.io
- **评审物理结构**:科学展览式,每队 4 分钟(2演示+1问答+1评委走路),每评委报 top3 stack ranking;必须提交**2分钟视频且"是demo不是presentation"**;宣布前有 cheating check;评委被提醒 "Focus on learning over profit"
- 来源: github.com/MLH/mlh-hackathon-rules Rules.md; guide.mlh.com judging-plan / rules-for-your-hackathon

### ETHGlobal(Web3)
- 无统一手册,criteria 挂各赛事页,通常五类(技术难度/原创性/实用性/UI/整体);赞助赛道常见四条:Innovation / Product quality / Technical execution / **Effective use of 赞助技术**——赞助赛道要逐条对照 prize 条件 [部分为搜索快照,用前核验赛事页]

### Google Solution Challenge
- SDG(联合国可持续发展目标)针对性、Google 技术栈使用、设计/可用性、完成度、可扩展性 [搜索快照]

### 跨赛事公约(高频并集)
创新原创 / 技术难度 / 完成度可运行 / 设计UX / 实用影响 / 演示表达(MLH不单列) / **切题+合规=隐藏一票否决**

## 2. 无官方 rubric 时的通用权重基线

| 维度 | 默认权重 | 评委心里的问题 |
|---|---|---|
| 切题性 | 15-25% | "这是为这个比赛做的吗?" |
| 创新/原创 | 20-30% | "今年第几次见到类似的?" |
| 技术实现 | 20-30% | "真功夫还是壳?" |
| 完成度/可运行 | 15-25% | "现场能跑吗?" |
| 实用/影响 | 15-25% | "有人需要吗?" |
| 演示表达 | 10-20% | "3分钟听懂了吗?" |

**修正规则**(来自官方标准研究):学生赛(MLH系)把 Learning 当正式维度准备("我们学了什么");大厂赞助赛把"用了赞助商技术"当独立得分项,漏用=白丢一栏。**美观度在赛道制比赛(尤其国内高校/大厂赛)常为显性评分维度**(天猫AI黑客松公开规则明写"美观度也计入")——P0 抄 rubric 时不要默认它不存在;UI 挣分方法见 05-polish.md。

## 3. 评审的物理约束 → 打法含义

1. **你的目标不是"让评委懂",是进这位评委的 top3**(stack ranking 制)
2. Devpost ≈10分钟/项目、MLH 3-4分钟/队 → **前30秒钩子决定一切**,把 URL/项目名反复露出
3. 提交页是第二赛场:很多评委只看提交页+视频就打分——视频是 demo 不是幻灯片朗读
4. 过度精致反而引起套壳怀疑("anything impressive-looking raises suspicion")→ **主动展示"赛内完成"的证据**:commit 时间线、devlog、诚实的 stub 交底

## 4. 获奖共性(核验案例归纳)

- 完成度是入场券,**traction(真实用户)是最贵区分项**——jero.zone 靠几百真实学生用户横扫;"somebody has used the thing" 才是信号(Willison)
- 一句话讲清+点燃想象;**错位竞争**:人人挤 AI/crypto 赛道时,冷门类别竞争小;盯赞助商 API 单项奖,没拿总冠军也能带奖走
- **AI时代惊艳度通胀**:纯软件项目贬值("整周末没看过一行代码"),wow 向硬件/实体交互/多代理/MCP"新物种"迁移;别做 wrapper("All the ChatGPT wrappers rank poorly")
- 评委=出题人:解决主办方自己的痛最容易赢;评委构成决定叙事(企业赛重 impact,社区赛重 learning)

## 5. 与本 skill 其他文件的接口

- P0 命题解码用 §1/§2 定权重 → 00-theme-decode.md
- P1 选题的错位竞争与单项奖策略 → 01-brainstorm.md
- P4 的"评委看得见的才值得写/后端可硬编码/commit证据链" → 04-build-playbook.md
- P6 的 4 分钟物理结构与 2 分钟 demo 视频 → 06-pitch-submit.md
