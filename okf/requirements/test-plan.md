---
title: Test Plan — 数据校验测试计划
description: 覆盖 schema 校验、枚举一致性、文件名约定等 11 项规则
type: requirement
resource: scripts/validate.py
tags: [test,校验,schema]
timestamp: 2024-12-01
source_ids: [TDD-TEST-001, TDD-TEST-011]
---

# 测试计划

## 测试清单

| 编号 | 内容 | 校验方式 |
| --- | --- | --- |
| 001 | Schema 文件自身合法 | `jsonschema.Draft7Validator.check_schema` |
| 002 | 单文件符合 Schema | `jsonschema.validate(instance, schema)` |
| 003 | 批量 100% 通过 | 遍历 `data/stele/**/*.json` |
| 004 | dynasty 字段枚举 | 值在白名单内 |
| 005 | calligraphy_type 字段枚举 | 值在白名单内 |
| 006 | 文件名 slug 正则 | `^[a-z][a-z0-9_\-]*\.json$` |
| 007 | release_date YYYY-MM-DD | `datetime.strptime` |
| 008 | year 为整数 | `isinstance(v, int)` |
| 009 | content 非空 | `len(content.strip()) > 0` |
| 010 | 无重复文件名 | 全小写比较 |
| 011 | dynasty 与目录一致 | 从 `DIR_TO_DYNASTY` 映射 |

## 运行命令

```bash
pip install jsonschema
python scripts/validate.py
```

## 通过标准

- exit code = 0
- 输出 `[✓] 校验通过！N/N 文件全部符合 Schema 与命名约定。`
