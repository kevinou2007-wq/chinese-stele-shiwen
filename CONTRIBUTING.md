# 贡献指南

感谢您对 📜 chinese-stele-shiwen 的关注！本文件说明如何向仓库提交新碑帖或修改现有数据。

## 一、数据格式

新增碑帖时，请在对应朝代的目录下新建一个 JSON 文件。

### 文件名约定

- 使用 **ASCII slug**：全小写，数字/下划线/短横线，以 `.json` 结尾
- 建议：碑名拼音意译，或通用英文名
- 示例：
  - 《多宝塔碑》 → `duo_bao_ta_bei.json`
  - 《玄秘塔碑》 → `xuan_mi_ta_bei.json`
  - 《九成宫醴泉铭》 → `jiu_cheng_gong_quan_ming.json`

### 必填字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `name` | string | 碑帖中文全称，含书名号 |
| `dynasty` | string | 见朝代枚举 |
| `author` | string | 书丹者（无考可填"不详"） |
| `year` | integer | 公元纪年，无考填 `-1` |
| `calligraphy_type` | string | 书体枚举 |
| `source` | string | 释文依据的出版物名 |
| `content` | string | 通行释文纯文本 |

### 朝代枚举

```
秦漢 / 魏晉南北朝 / 隋唐五代 / 宋遼金 / 元明清 / 近現代
```

### 书体枚举

```
篆書 / 隶書 / 楷書 / 行書 / 草書 / 其他
```

## 二、新增碑帖步骤

```bash
# 1. Fork 仓库并克隆到本地
git clone https://github.com/YOUR/chinese-stele-shiwen.git
cd chinese-stele-shiwen

# 2. 在合适目录下新建碑帖 JSON 文件
#    例如：唐代碑帖 → data/stele/sui_tang/your_new_stele.json

# 3. 编辑文件，严格参照 schema.json 与现有示例

# 4. 运行校验脚本确认语法与 Schema 均通过
pip install jsonschema
python scripts/validate.py

# 5. 提交
git add data/stele/your_new_stele.json
git commit -m "feat: 新增《碑名》释文"
git push origin your-branch

# 6. 在 GitHub 上发起 Pull Request
```

## 三、现有数据修改

- 修改 `content` 时：请保留原文注释说明修改原因（参考"释文异同"）
- 修改 `source` 时：务必在 PR 描述里提供新出处的文献信息
- 修改文件内容后仍需通过 `python scripts/validate.py`

## 四、可接受内容

| 类型 | 示例 |
| --- | --- |
| 🆕 新碑帖 | 任何朝代的碑刻、墓志、摩崖、造像记、砖铭等释文 |
| ✏️ 释文校正 | 与原拓对照发现的误字，需附出处 |
| 📝 元数据补全 | 补充 ISBN、整理者、简介等 |
| 🐛 Schema 修正 | 字段遗漏、类型错误等 |
| 🔤 繁简说明 | 可在 `description` 字段注明异体字或避讳字 |

## 五、不接受内容

- ❌ 未经出处核实的释文
- ❌ 非 UTF-8 编码的文件
- ❌ 文件名带中文或特殊符号
- ❌ 一行式巨型 JSON（保持每文件一碑）
- ❌ 商用出版物原文全文（仅收通行"释文"段）

## 六、质量标准

- `content` 字段应为**简体、横排、按碑文本阅读顺序**的通行释文
- 残泐字用 `□` 标注
- 不可识读字用 `☐` 并在 `description` 中说明
- 避讳字建议在 `description` 字段注明"原碑避 X 讳作 Y"

## 七、行为准则

请互相尊重，专注于学术讨论。本仓库为公共数据集合，任何人都有权 Fork 并自行使用。
