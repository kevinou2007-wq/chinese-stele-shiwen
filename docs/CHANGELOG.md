# Changelog

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
