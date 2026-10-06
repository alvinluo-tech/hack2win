# 14 · 运行配置契约 (Run Config Contract)

> **本文件解决什么问题**: 前述 00–06 各阶段都有验收门, 但如果没有一份**机器可读的单一真值源**,
> agent 会在长会话中选择性遗忘或自由发挥——把"用户指定的像素风"做成通用后台、把 T2 悄悄降级成 T1、
> 把 `queue` 留空却宣称异步。本文件把 P0 之后**冻结一次、全程只读**的决策固化进 JSON, 让每个门都可被机械判定。

---

## 1. 为什么需要它

PaperSpine 的关键设计是: 开题阶段用向导生成 `paper_spine_config.json`, 之后的 12 个子技能**全部以该文件为输入**,
不允许各自解释需求; 所有审计脚本也读同一个文件判定 `scene`/`tier`。
这消灭了"多轮对话后需求漂移"这一长会话头号杀手。

hack2win 的对等物就是 **`hackathon-run/run-config.json`**。
它必须在 **P0 结束时生成, 在 P1 开始前向用户确认, 之后全程只读**。

**为什么必须有**: 本技能一次运行跨越数小时、数千次工具调用。没有冻结契约, 就会出现:

- P5 打磨时把"3D 像素世界"悄悄退回成"暗色管理后台"(最贵的失败, 直接丢掉视觉分);
- P4 装配时忘记 `queue`, 把 AI 调用写在 HTTP 请求线程里;
- 验收时无人记得赞助商赛道用了哪家, `SPONSOR_LIVE_CHECK` 变成走过场。

---

## 2. 结构与示例

Schema 位于 [`schemas/run-config.schema.json`](../schemas/run-config.schema.json)。
一份填好的实例:

```json
{
  "schema_version": "1.0",
  "hackathon": {
    "name": "NASA Space Apps Challenge 2026",
    "organizer": "NASA / Booz Allen",
    "url": "https://www.spaceappschallenge.org/",
    "mode": "online",
    "duration_hours": 36,
    "rubric_source": "published",
    "sponsor_tracks": ["Google Earth Engine", "AWS Open Data"]
  },
  "delivery": {
    "tier": "T2",
    "upgrade_triggers": ["需要多端(桌面/移动)同时交付时升级 T3"],
    "backend": "FastAPI + SQLAlchemy 2.0 (async)",
    "frontend": "Next.js 15 App Router + React 19",
    "database": "PostgreSQL 16 (容器) / SQLite WAL (本地演示兜底)",
    "queue": "Redis + ARQ"
  },
  "ui": {
    "user_pinned": true,
    "user_brief": "暗色像素风、带动画、3D 可交互, 不要平面工作台",
    "archetype": "3D voxel observatory: 地球数据以体素星球呈现, 观测站为可飞入场景",
    "metaphor": "卫星观测 = 在星球上点亮/调焦体素",
    "renderer": "React Three Fiber + drei + postprocessing",
    "viewports": ["1440x900", "768x1024", "390x844"]
  },
  "gates": {
    "complexity_floor": true,
    "click_level_acceptance": true,
    "screenshot_acceptance": true,
    "sponsor_live_check": "evidence/sponsor-live.log",
    "state_mutation_test": true,
    "runtime_evidence_dir": "evidence/"
  }
}
```

---

## 3. 字段语义与硬约束

| 字段 | 判定作用 | 违反后果 |
| :--- | :--- | :--- |
| `hackathon.rubric_source` | 决定 P0 是否必须逐项逆向官方评分表 | `published` 却未产出评分逆向表 → P0 门不过 |
| `hackathon.mode` | 决定 demo 时长预算(online 10min / onsite 3-4min) | 用 10 分钟脚本去打 3 分钟现场赛 |
| `delivery.tier` | 决定 P4 复杂度门的阈值档位 | 无 devlog 的静默降级 → 07 死法"T2 被无理由降级" |
| `delivery.queue` | T2 及以上禁止为空 | 空值即"耗时操作同步阻塞"预警 |
| `ui.user_pinned` | 为 `true` 时 **User-Intent Supremacy 强制生效** | 回落通用后台 → 视为最严重失败之一 |
| `ui.renderer` | P5 验收时校验依赖是否真实安装 | 声称 R3F 但 `package.json` 无 three |
| `ui.viewports` | 驱动 `ui_shot.py` 的截图矩阵 | 缺 390px → 窄屏溢出必漏检 |
| `gates.sponsor_live_check` | 指向真实运行日志路径 | 文件不存在 → 纸面适配器, 一票否决级风险 |

---

## 4. 冻结与变更纪律

1. **冻结时点**: P0 结束写入; P1 开始前把该文件**逐字读给用户确认**(这是全程唯一一次强制人工确认)。
2. **只读纪律**: P1–P6 期间任何 agent 不得修改本文件。
3. **唯一合法变更**: 若用户在 P3 之后追加 UI 风格指令, 允许**且必须**更新 `ui.user_brief` / `ui.archetype` / `ui.renderer`,
   同时在 `hackathon-run/devlog.md` 追加一条 `CONFIG-CHANGE` 记录(时间、旧值、新值、触发原话)。
4. **不得变更**: `delivery.tier` 只允许向上升级; 降级必须写明触发器命中证据, 否则验收直接判 FAIL。

---

## 5. 与机械门的关系

```
run-config.json ──┬─→ verify_project.py                 (读 tier 判定目录/契约完整度)
                  ├─→ verify_production_complexity.py   (读 tier 取复杂度阈值)
                  ├─→ ui_shot.py                        (读 ui.viewports 生成截图矩阵)
                  └─→ 人工/agent 审计                     (读 gates.* 判定证据是否留痕)
```

> **一句话总结**: 没有 `run-config.json`, 后面所有"验收门"都只是口头承诺;
> 有了它, 每个门都变成"读文件、比数值、给结论"的机械动作。
