# 📜 碑帖释文 chinese-stele-shiwen

<p align="center">
  <a href="https://github.com/chinese-poetry/chinese-poetry"><img src="https://img.shields.io/badge/model-chinese--poetry-blueviolet" alt="model"></a>
  <img src="https://img.shields.io/badge/format-JSON-orange" alt="format">
  <img src="https://img.shields.io/badge/language-python-brightgreen" alt="tool">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="license"></a>
</p>

> **一个开放的、结构化的中国书法碑帖释文数据集。**

每座碑帖独立一个 JSON 文件，按朝代分目录存放。与 [chinese-poetry](https://github.com/chinese-poetry/chinese-poetry) 项目思路一致——零依赖、可离线、能被任何语言直接引用。

## 目录结构

```
chinese-stele-shiwen/
├── README.md              ← 本页，项目介绍与使用说明
├── CONTRIBUTING.md        ← 贡献指南
├── LICENSE                ← 许可证
├── .gitignore
├── data/
│   ├── schema.json        ← JSON Schema 规范（字段定义）
│   └── stele/             ← 结构化数据（按朝代分目录，每碑一 JSON）
│       ├── qin_han/       ← 秦汉（66）
│       ├── wei_jin_nanbei/← 魏晋南北朝（115）
│       ├── sui_tang/      ← 隋唐五代（90）
│       ├── song_liao_jin/ ← 宋辽金（111）
│       ├── yuan_ming_qing/← 元明清（100）
│       └── modern/        ← 近现代（0）
├── 释文/                   ← 按朝代整理的碑帖释文可读文档（Markdown，15 个朝代 + 总录索引）
├── reports/               ← 数据质量报告（改进 / 全量核对 / 比对与重建）
├── scripts/               ← 转换与校验脚本（import_per_stele.py / validate.py 等）
└── docs/                  ← 内部设计文档
```

## 快速使用

### Shell：直接读取

```bash
cat data/stele/sui_tang/per_唐-颜真卿-多宝塔碑.json | jq .content
```

### JavaScript / Node

```sh
npm install chinese-stele-shiwen
# 或
git clone https://github.com/you/chinese-stele-shiwen.git
```

```js
import stele from "./data/stele/sui_tang/per_唐-颜真卿-多宝塔碑.json";
console.log(stele.content);
```

### Python

```python
import json, pathlib

f = pathlib.Path("data/stele/sui_tang/per_唐-颜真卿-多宝塔碑.json").read_text(encoding="utf-8")
stele = json.loads(f)
print(stele["content"])
```

## 数据格式

每个碑帖文件是一个独立 JSON 对象：

```json
{
  "name": "多宝塔碑",
  "dynasty": "隋唐五代",
  "author": "颜真卿",
  "year": 752,
  "calligraphy_type": "楷書",
  "source": "《北京图书馆藏中国历代石刻拓本汇编》第 27 册",
  "source_isbn": "978-7-5013-0853-3",
  "editor": "beixie-team",
  "release_date": "2024-12-01",
  "description": "全称《大唐西京千福寺多宝佛塔感应碑文》...",
  "content": "大唐西京千福寺多宝佛塔感应碑文。南阳岑勋撰..."
}
```

### Schema 字段表

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `name` | string | ✅ | 碑帖名称 |
| `dynasty` | string | ✅ | 朝代：秦漢 / 魏晉南北朝 / 隋唐五代 / 宋遼金 / 元明清 / 近現代 |
| `author` | string | ✅ | 书丹者或撰文者 |
| `year` | integer | ✅ | 公元纪年，未知填 `-1` |
| `calligraphy_type` | string | ✅ | 书体：篆書 / 隶書 / 楷書 / 行書 / 草書 / 其他 |
| `source` | string | ✅ | 释文来源说明 |
| `editor` | string | ❌ | 整理者 ID |
| `release_date` | string | ❌ | 数据录入日期（YYYY-MM-DD） |
| `description` | string | ❌ | 碑帖简介（类型、年代、备注） |
| `content` | string | ✅ | 通行释文 / 白话译文（横排简体） |
| `original_text` | string | ❌ | 碑文原文（含通假字、残泐标记） |
| `translation` | string | ❌ | 白话译文（如 content 非译文时） |
| `note` | string | ❌ | 备注（鉴藏、书体特征等） |
| `baike_query` | string | ❌ | 百科检索参考关键词 |
| `raw_type` | string | ❌ | 原始类型（碑刻/墓志/墨迹/金文等） |
| `raw_date` | string | ❌ | 原始年代描述字符串 |

详细规范见 [`data/schema.json`](data/schema.json)。

## 校验

仓库任何数据文件的变更都要经过校验脚本确认通过，详见 [`CONTRIBUTING.md`](CONTRIBUTING.md)。

```bash
pip install jsonschema
python scripts/validate.py
# 期望输出：[✓] 校验通过！N/N 文件全部符合 Schema 与命名约定。
```

## 数据量

| 朝代 | 文件数 |
| --- | --- |
| 秦汉 | 66 |
| 魏晋南北朝 | 115 |
| 隋唐五代 | 90 |
| 宋辽金 | 111 |
| 元明清 | 100 |
| 近现代 | 0 |
| **合计** | **482** |

数据来源于 Marvis 碑帖释文数据集（per_stele 直读模式），按本仓库 schema 整理。

## 释文文档与质量报告

除结构化 JSON 数据外，仓库另提供两类可读成果（与 `data/stele/` 同源，便于检索与阅读）：

- **`释文/`** — 按 15 个细分朝代整理的碑帖释文文档（西周 / 先秦 / 秦 / 两汉 / 三国 / 两晋 / 南北朝 / 隋 / 唐 / 五代 / 北宋 / 南宋 / 元 / 明 / 清），每件含原文、译文与考释备注；另含 `碑帖释文总录索引.md`（全 482 件目录）。
- **报告**见 [`reports/`](reports/)：`改进报告.md`、`全量核对报告.md`、`比对与重建报告.md`，记录数据订正、全量核对与比对重建过程。

> 释文均经权威来源（古诗文网、《金石萃编》、《全唐文》、故宫与各地碑林资料等）核对并修正；备注中带有「[核查修正·…]」标记的条目为已据权威本订正者。

## 数据来源与版权说明

- 本项目**仅收集整理**已有的碑帖释文文献，本身不主张对所收录释文的著作权。
- 每条 `source` 字段标注原始出处。如您对收录内容有任何异议，请提交 Issue。

## 贡献

欢迎提交：新碑帖数据、现有释文校正、元数据补充、翻译、质检等。详见 [`CONTRIBUTING.md`](CONTRIBUTING.md)。

---

## 类似的项目

- [chinese-poetry](https://github.com/chinese-poetry/chinese-poetry) — 最全的中华古典文集数据库
- [MOCDataset](https://github.com/cfhir/MOCDataset) — 古代字形的 OCR 数据集
	
