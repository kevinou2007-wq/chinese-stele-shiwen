---
title: Build Path — 实施顺序描述
description: 按任务依赖关系排列的实施步骤与 🛑 STOP 条件
type: decision
resource: docs/RMD.md
tags: [实施,排序,风险]
timestamp: 2024-12-01
source_ids: [RMD-TASK-001, RMD-TASK-006]
---

# Build Path 决策

## 任务顺序

1. **RMD-TASK-001** — 项目骨架（已完成）
2. **RMD-TASK-002** — Schema + 目录结构（已完成）
3. **RMD-TASK-003** — 校验脚本（已完成）
4. **RMD-TASK-004** — README / CONTRIBUTING（已完成）
5. **RMD-TASK-005** — 首批样本 ≥50 碑（已完成，实际 76 碑）
6. **RMD-TASK-006** — GitHub 仓库 🔴 CHECKPOINT（待用户确认远程地址后执行）

## 🛑 STOP 条件

- **RMD-TASK-003** 完成前不允许录入正式样本（无校验手段）
- **RMD-TASK-005** 每批必须通过 `python scripts/validate.py`
- **RMD-TASK-006** 首次 push 前必须用户明确确认远程仓库地址

## 回滚点

- RP-1: RMD-TASK-003 完成后
- RP-2: RMD-TASK-005 首批完成后
- RP-3: RMD-TASK-006 push 后
