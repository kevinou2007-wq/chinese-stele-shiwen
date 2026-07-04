---
title: Schema 模块 — 数据结构定义
description: JSON Schema draft-07 声明式定义，供脚本与贡献者共同遵守
type: module
resource: data/schema.json
tags: [schema,模块,数据结构]
timestamp: 2024-12-01
source_ids: [MDD-MOD-001]
---

# Schema 模块

## 文件位置

- `data/schema.json`：JSON Schema draft-07
- `scripts/validate.py`：使用此 schema 校验所有数据文件

## 字段详情

参见 [/requirements/schema.md](/requirements/schema.md)。

## 修改规则

- Schema 必须向后兼容——只在末尾**追加**新字段，不删、不改旧字段
- 修改 schema 前需同步修改 validate.py 和 okf/requirements/schema.json
- 需跑 `python scripts/validate.py` 确认现有数据全部兼容
