---
title: 编码约定 — UTF-8 无 BOM
description: 所有 JSON 文件必须使用 UTF-8（无 BOM）编码
type: term
resource: docs/URD.md
tags: [编码,UTF8,BOM]
timestamp: 2024-12-01
source_ids: [URD-CON-001]
---

# 编码约定

所有 `data/stele/**/*.json` 文件必须满足：

- 字符编码：**UTF-8**
- **无 BOM**（字节顺序标记）
- 行尾：LF（Unix）或 CRLF（Windows）均可
- 每文件末尾保留一个换行符

## 校验方式

`python scripts/validate.py` 会尝试以 `encoding="utf-8"` 读取文件；读取失败则报错。
