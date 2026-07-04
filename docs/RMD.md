# Build Path / RMD — chinese-stele-shiwen

> 以下任务是按**依赖关系**排序的实施步骤。每个任务结束都配一个 Git 保存点。

## 实施顺序

### RMD-TASK-001: 建立项目骨架 ✅（本次产出）

- 创建 `docs/` / `data/` / `okf/` / `scripts/` 等目录
- 产出 URD / ADD / MDD / TDD / RMD / TRACE 六个设计文档
- 初始 commit: `init: 项目骨架与设计文档`

### RMD-TASK-002: 产出 JSON Schema 文档

- 新增 `data/schema.json`（来自 MDD-API-001）
- 新增 `data/stele/` 朝代子目录（空目录加 `.gitkeep`）
- commit: `feat: 添加数据 schema 与目录结构`

### RMD-TASK-003: 编写 validate.py 脚本

- `scripts/validate.py` 实现 TDD-TEST-001 ~ TDD-TEST-011 所有校验
- 依赖：`jsonschema`（`requirements.txt` 或 `pyproject.toml` 记录）
- 先用 `TDD-TEST-001 ~ TDD-TEST-003` 作为冒烟测试
- commit: `feat: 添加数据校验脚本`

### RMD-TASK-004: 编写 README 和 CONTRIBUTING

- `README.md`：项目介绍、Schema 表、引用示例、贡献入口
- `CONTRIBUTING.md`：命名规范、metadata 填写、PR 流程
- 参照 chinese-poetry 项目的风格写
- commit: `docs: 仓库 README 和贡献指南`

### RMD-TASK-005: 录入跨朝代代表性样本 ≥ 50 碑

- 按 MDD-API-003 目录结构，每朝至少 5-8 种代表性碑帖
- 经典优先：多宝塔碑、玄秘塔碑、九成宫醴泉铭、皇甫诞碑、雁塔圣教序、祭侄文稿、石门颂、曹全碑、张猛龙碑、龙藏寺碑……
- 全程 `python scripts/validate.py` 校验通过后 commit
- commit: `data: 录入首批 50 种代表性碑帖释文`（或多个分批 commit）

### RMD-TASK-006: 初始化 GitHub 仓库 & 公开

- `git remote add origin git@github.com:you/chinese-stele-shiwen.git`
- 第一次 push 给用户确认后执行（🔴 CHECKPOINT）
- 设置 license（推荐 MIT）
- commit: `chore: 初始化 LICENSE 与远程仓库配置`

## 🛑 STOP 条件

- RMD-TASK-003 产出前，不允许录入正式样本数据（因为没有校验手段）
- RMD-TASK-005 的每批数据必须通过 `validate.py` 才算切片完成
- RMD-TASK-006 首次 push 前必须用户明确确认远程仓库地址

## 回滚点

| 回滚点 | 位置 | 回滚方法 |
| --- | --- | --- |
| RP-1 | RMD-TASK-003 完成后 | `git checkout <commit>` |
| RP-2 | RMD-TASK-005 首批完成后 | 数据文件可单文件删除，无需整体回滚 |
| RP-3 | RMD-TASK-006 push 后 | `git revert` 特定 commit |
