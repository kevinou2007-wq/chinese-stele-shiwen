# Design Split / ADD — chinese-stele-shiwen

> 这是一个数据仓库项目，架构设计重点是"schema 设计 + 目录命名约定"，而非软件模块。

## Functional Requirements (FR)

从 URD 提取出的用户需求对应的功能需求：

| FR ID | 说明 |
| --- | --- |
| ADD-FR-001 | 每个碑帖的释文数据结构定义清楚（Schema） |
| ADD-FR-002 | 目录按朝代组织，每朝一目录 |
| ADD-FR-003 | 每个释文文件可独立引用 |
| ADD-FR-004 | 元数据来源和出处可追溯 |
| ADD-FR-005 | 贡献者可按规范独立新增碑帖 |

## Design Parameters (DP)

| DP ID | 说明 |
| --- | --- |
| ADD-DP-001 | JSON Schema 文档 (`data/schema.json`) |
| ADD-DP-002 | 目录命名规范 (`data/stele/{dynasty}/{stele_name}.json`) |
| ADD-DP-003 | 朝代枚举值（秦、漢、魏晉南北朝、隋唐五代、宋遼金、元明清、近现代） |
| ADD-DP-004 | 每文件 metadata 字段约定 (`name`, `dynasty`, `author`, `year`, `source`, `calligraphy_type`) |
| ADD-DP-005 | 贡献规范文档 (CONTRIBUTING.md) |

## 设计矩阵

|  | DP-001 Schema | DP-002 目录约定 | DP-003 朝代枚举 | DP-004 字段约定 | DP-005 贡献规范 |
| --- | --- | --- | --- | --- | --- |
| FR-001 数据结构 | X | | | X | |
| FR-002 目录组织 | | X | X | | |
| FR-003 单文件引用 | | X | | | |
| FR-004 来源追溯 | | | | X | |
| FR-005 独立贡献 | | | | X | X |

> **结果：对角矩阵（uncoupled design）。** 每个 DP 仅服务于特定的 FR，模块之间无交叉依赖。

## 耦合状态

✅ **无耦合** — 各设计参数相互独立。修改 schema 不会影响目录结构，增加朝代枚举不会影响单个文件内容。

## Schema 设计（核心决策 / DEC-001）

每碑 JSON 文件结构：

```json
{
  "name": "多宝塔碑",
  "dynasty": "唐代",
  "author": "颜真卿",
  "year": 752,
  "calligraphy_type": "楷书",
  "source": "《北京图书馆藏中国历代石刻拓本汇编》第 27 册",
  "source_isbn": "978-7-5013-0853-3",
  "editor": "数据整理者 GitHub ID",
  "release_date": "2024-12-01",
  "description": "全称《大唐西京千福寺多宝佛塔感应碑文》，岑勋撰，颜真卿书。",
  "content": ""
}
```

`content` 字段为**纯文本**通行释文（简体、横排、按碑文阅读顺序、不含注码）。

## 目录命名决策（DEC-002）

```
data/stele/
├── qin_han/              # 秦汉
├── wei_jin_nanbei/       # 魏晋南北朝
├── sui_tang/             # 隋唐五代
├── song_liao_jin/        # 宋辽金
├── yuan_ming_qing/       # 元明清
└── modern/               # 近现代
```

每朝目录内用 `碑名_slug.json` 命名（ASCII slug，便于 URL 兼容引用）。
