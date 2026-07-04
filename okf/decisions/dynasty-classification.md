---
title: 按朝代分目录
description: 碑帖数据按朝代维度划分为 6 个目录，ASCII slug 命名
type: decision
resource: data/stele/
tags: [组织结构,朝代,目录]
timestamp: 2024-12-01
source_ids: [ADD-DP-002, ADD-DP-003, DEC-002]
---

# DEC-002：按朝代分目录

## 决策

碑帖数据按**朝代**维度划分为 6 个一级目录，文件名使用 ASCII slug。

## 目录表

| slug | 中文名 | 公元范围 |
| --- | --- | --- |
| `qin_han` | 秦汉 | 前221 – 220 |
| `wei_jin_nanbei` | 魏晋南北朝 | 220 – 589 |
| `sui_tang` | 隋唐五代 | 581 – 960 |
| `song_liao_jin` | 宋辽金 | 960 – 1279 |
| `yuan_ming_qing` | 元明清 | 1271 – 1912 |
| `modern` | 近现代 | 1912 – 至今 |

## 理由

- 与 chinese-poetry 项目风格一致，用户迁移成本低
- 朝代是碑帖研究最主流的视角
- 便于贡献者确定归类；避免后人反复争论

## 文件名规范

- 全小写 ASCII
- 允许数字、下划线、短横线
- 必须以 `.json` 结尾
- 示例：`duo_bao_ta_bei.json`
