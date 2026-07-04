# Project Map / TRACE — chinese-stele-shiwen

> 追溯链：需求 → 设计参数 → 模块 → 测试 → 实施任务

## 主要追溯链

```
URD-REQ-001 Schema 统一，每碑可独立引用
  → ADD-FR-001 数据结构定义清晰
  → ADD-DP-001 JSON Schema 文档
  → MDD-MOD-001 Schema
  → TDD-TEST-001 / 002 / 003
  → RMD-TASK-002
  → okf/requirements/schema.md

URD-REQ-002 按朝代组织
  → ADD-FR-002 目录按朝代组织
  → ADD-DP-002 目录命名规范
  → ADD-DP-003 朝代枚举
  → MDD-MOD-002 朝代目录
  → TDD-TEST-004 / 006 / 011
  → RMD-TASK-002
  → okf/decisions/dynasty-classification.md

URD-REQ-003 来源出处可追溯
  → ADD-FR-004 来源可追溯
  → ADD-DP-004 字段约定
  → MDD-API-001 source/source_isbn/editor 字段
  → TDD-TEST-007 / 008 / 009
  → RMD-TASK-004
  → okf/contracts/source-attribution.md

URD-REQ-004 贡献者可独立新增
  → ADD-FR-005 贡献者独立新增
  → ADD-DP-005 贡献规范文档
  → MDD-MOD-006 CONTRIBUTING
  → TDD-TEST-003 贡献者自测
  → RMD-TASK-004
  → okf/decisions/contribution-workflow.md
```

## 设计决策追踪

| 决策 ID | 出处 | 说明 |
| --- | --- | --- |
| DEC-001 | ADD.md + MDD-API-001 | 碑帖 JSON 字段结构（单文件 schema） |
| DEC-002 | ADD.md | 按朝代分目录、文件名 ASCII slug |

## 文档与 OKF 的对应

| URD/ADD/MDD/TDD/RMD/TRACE | OKF 页 |
| --- | --- |
| MDD-API-001 | `okf/requirements/schema.md` |
| ADD-DP-003 | `okf/decisions/dynasty-classification.md` |
| ADD-DP-005 | `okf/decisions/contribution-workflow.md` |
| URD-CON-001 | `okf/terms/encoding-utf8.md` |
