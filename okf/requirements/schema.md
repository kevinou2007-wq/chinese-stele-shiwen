---
title: 碑帖释文 JSON Schema
description: 每碑 JSON 文件的字段结构与类型定义
type: requirement
resource: data/schema.json
tags: [schema,规范,数据格式]
timestamp: 2024-12-01
source_ids: [ADD-FR-001, MDD-API-001]
---

# 单碑 JSON Schema

每碑 JSON 文件必须含以下字段：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `name` | string | ✅ | 碑帖中文全称 |
| `dynasty` | string | ✅ | 朝代枚举 |
| `author` | string | ✅ | 书丹者 / 撰文者 |
| `year` | integer | ✅ | 公元纪年，未知填 -1 |
| `calligraphy_type` | string | ✅ | 书体枚举 |
| `source` | string | ✅ | 释文依据的出版物 |
| `source_isbn` | string | ❌ | ISBN |
| `editor` | string | ❌ | 整理者 ID |
| `release_date` | string | ❌ | YYYY-MM-DD |
| `description` | string | ❌ | 碑帖简介 |
| `content` | string | ✅ | 通行释文 |

## 朝代枚举

`秦漢` / `魏晉南北朝` / `隋唐五代` / `宋遼金` / `元明清` / `近現代`

## 书体枚举

`篆書` / `隶書` / `楷書` / `行書` / `草書` / `其他`

## 示例

```json
{
  "name": "多宝塔碑",
  "dynasty": "隋唐五代",
  "author": "颜真卿",
  "year": 752,
  "calligraphy_type": "楷書",
  "source": "《北京图书馆藏中国历代石刻拓本汇编》第 27 册",
  "content": "大唐西京千福寺多宝佛塔感应碑文。..."
}
```

详细 JSON Schema 见 [/modules/schema.json](/modules/schema.json)。
