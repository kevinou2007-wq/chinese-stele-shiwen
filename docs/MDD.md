# Building Blocks / MDD — chinese-stele-shiwen

> 本项目是纯数据仓库，没有"运行时代码模块"。MDD 只描述数据结构和文件契约。

## 模块列表

| MOD ID | 模块 | 类型 | 职责 |
| --- | --- | --- | --- |
| MDD-MOD-001 | 数据 schema | 文件定义 | `data/schema.json` 用 JSON Schema draft-07 声明所有合法字段 |
| MDD-MOD-002 | 朝代目录 | 目录命名规范 | `data/stele/{dynasty_slug}/` 按朝代存放 |
| MDD-MOD-003 | 单碑数据 | 数据文件 | 每个 `{name_slug}.json` 严格符合 schema |
| MDD-MOD-004 | 校验脚本 | Python 工具 | `scripts/validate.py` 遍历所有数据文件并校验 schema |
| MDD-MOD-005 | README | 文档 | 仓库首页使用说明、Schema 表、引用示例 |
| MDD-MOD-006 | CONTRIBUTING | 文档 | 贡献者指南：命名、metadata 填写、PR 流程 |

## 数据接口契约

### MDD-API-001: 单碑 JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SteleShiwen",
  "type": "object",
  "required": ["name", "dynasty", "author", "year", "source", "calligraphy_type", "content"],
  "properties": {
    "name": {
      "type": "string",
      "description": "碑帖名称，如《多宝塔碑》"
    },
    "dynasty": {
      "type": "string",
      "enum": ["秦漢", "魏晉南北朝", "隋唐五代", "宋遼金", "元明清", "近現代"],
      "description": "所属朝代"
    },
    "author": {
      "type": "string",
      "description": "书丹者或撰文者姓名"
    },
    "year": {
      "type": "integer",
      "description": "刊立年份（公元纪年），未知则填 -1"
    },
    "calligraphy_type": {
      "type": "string",
      "enum": ["篆書", "隶書", "楷書", "行書", "草書", "其他"],
      "description": "书体"
    },
    "source": {
      "type": "string",
      "description": "释文依据的出版物文献"
    },
    "source_isbn": {
      "type": "string",
      "description": "出版物 ISBN（可选）"
    },
    "editor": {
      "type": "string",
      "description": "数据整理者 ID，用于追溯贡献者"
    },
    "release_date": {
      "type": "string",
      "format": "date",
      "description": "YYYY-MM-DD"
    },
    "description": {
      "type": "string",
      "description": "碑帖简介（1-3 句）"
    },
    "content": {
      "type": "string",
      "description": "通行释文纯文本，横排简体，按碑文阅读顺序"
    }
  },
  "additionalProperties": false
}
```

### MDD-API-002: 文件名约定

- slug 全小写 ASCII
- 碑名中的汉字转拼音或意译
- 意译举例：`"多宝塔碑"` → `duo_bao_ta_bei.json`
- 年代不明或同碑多版本可在末尾加 `-v2`

### MDD-API-003: 目录枚举值

| 目录 slug | 中文名 | 公元范围 |
| --- | --- | --- |
| `qin_han` | 秦汉 | 前221 – 220 |
| `wei_jin_nanbei` | 魏晋南北朝 | 220 – 589 |
| `sui_tang` | 隋唐五代 | 581 – 960 |
| `song_liao_jin` | 宋辽金 | 960 – 1279 |
| `yuan_ming_qing` | 元明清 | 1271 – 1912 |
| `modern` | 近现代 | 1912 – 至今 |

## 脚本模块契约 (MDD-MOD-004)

### `scripts/validate.py`

**输入**：无参数或 `--target data/`
**输出**：stdout 打印每文件校验结果，exit code 0 = 全部通过，1 = 有错误
**行为**：
1. 遍历 `data/stele/**/*.json`
2. 用 `jsonschema` 库逐文件校验
3. 检查文件名 slug 是否与 `name` 字段一致（拼音近似匹配）
4. 检查 `release_date` 是否合法日期
