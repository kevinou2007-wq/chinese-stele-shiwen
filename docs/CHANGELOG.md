# Changelog

## 2026-07-19（per_stele 全量导入 · 482 件）

- ✅ **导入 482 个碑帖释文**（来源：Marvis `per_stele` 数据集，482 个独立 JSON）
  - 秦汉 66 / 魏晋南北朝 115 / 隋唐五代 90 / 宋辽金 111 / 元明清 100 / 近现代 0
  - 覆盖西周、先秦、秦、两汉、三国、两晋、南北朝、隋、唐、五代、北宋、南宋、元、明、清共 15 个细分朝代
- ✅ 使用 `scripts/import_per_stele.py` 转换脚本（每碑一文件，保留 `marvis_id` / `original_text` / `translation` / `note` / `raw_type` 等扩展字段）
- ✅ **482/482 文件全部通过 `scripts/validate.py` 校验**（Schema + 命名约定）
- ✅ 新增 `释文/` 目录：按 15 朝代整理的碑帖释文可读 Markdown（含原文、译文、考释）+ 总录索引
- ✅ 新增 `reports/` 目录：改进报告 / 全量核对报告 / 比对与重建报告
- ✅ 更新 README 数据量统计与目录结构说明

## 2024-12-01（数据批量导入）

- ✅ **导入 380 个真实碑帖释文**（来源：Marvis 数据集，38 批）
  - 秦汉 57 / 魏晋南北朝 113 / 隋唐五代 76 / 宋辽金 45 / 元明清 89
- ✅ 编写 `scripts/convert_marvis_data.py` 批量转换脚本
  - 兼容两种源格式（dict 第1批 / list 第2-38批）
  - 朝代自动映射 + 书体枚举归一化 + 年代提取
- ✅ 扩展 schema：新增 original_text / translation / note / baike_query / raw_type / raw_date
- ✅ 调整 validate.py：支持中文文件名 slug
- ✅ 清理旧占位样本（76 个），以真实数据取代
- ✅ **380/380 文件全部通过 validate.py 校验**

## 2024-12-01（初版骨架）

- ✅ 建立项目骨架与目录结构
- ✅ 产出全部 6 个设计文档（URD / ADD / MDD / TDD / RMD / TRACE）
- ✅ 定义 `data/schema.json` JSON Schema
- ✅ 按朝代分 6 个目录
- ✅ 编写 `scripts/validate.py` 数据校验脚本（覆盖 11 项规则）
- ✅ 写入 README.md 与 CONTRIBUTING.md
- ✅ 选择 MIT 许可证
