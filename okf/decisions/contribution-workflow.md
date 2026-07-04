---
title: Contribution Workflow — 贡献流程
description: 新增或修改碑帖数据时的操作步骤、可接受内容与质量标准
type: decision
resource: CONTRIBUTING.md
tags: [贡献,PR,流程]
timestamp: 2024-12-01
source_ids: [ADD-DP-005, MDD-MOD-006]
---

# 贡献者工作流

## 新增碑帖步骤

1. Fork 仓库并克隆到本地
2. 将新 JSON 文件放入对应朝代目录
3. 严格参照 `data/schema.json` 与现有示例
4. 运行 `python scripts/validate.py` 确认通过
5. `git commit` → `git push` → 发 PR

## 可接受内容

- 🆕 新碑帖
- ✏️ 释文校正（需附出处）
- 📝 元数据补全
- 🐛 Schema 修正
- 🔤 繁简说明

## 不接受内容

- ❌ 未出处核实的释文
- ❌ 非 UTF-8 编码
- ❌ 文件名含中文或特殊符号
- ❌ 一行式巨型 JSON
- ❌ 商用出版物原文全文

## 质量标准

- `content` 字段：简体、横排、按碑文本阅读顺序
- 残泐字用 `□`；不可识读字用 `☐` 并在 `description` 说明
- 避讳字在 `description` 字段注明
