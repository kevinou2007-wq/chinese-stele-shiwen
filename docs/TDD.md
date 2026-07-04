# Check Plan / TDD — chinese-stele-shiwen

> 本项目无运行时应用代码，测试聚焦于：**所有数据文件能被 JSON Schema 校验通过** + **文件结构约定被遵守**。

## 测试用例

| TEST ID | 测试 | 输入 | 预期结果（oracle） | 关联需求 |
| --- | --- | --- | --- | --- |
| TDD-TEST-001 | Schema 文件自身合法 | `data/schema.json` | 能被 `jsonschema` 库成功加载 | FR-001 |
| TDD-TEST-002 | 随机抽一个数据文件符合 Schema | `data/stele/sui_tang/duo_bao_ta_bei.json` | `validate(schema, instance)` 不抛异常 | FR-001 / FR-003 |
| TDD-TEST-003 | 批量遍历所有数据文件 | `data/stele/**/*.json` | 100% 通过校验，无 warning | FR-003 |
| TDD-TEST-004 | `dynasty` 字段枚举检查 | 任一文件 | 字段值 in {秦漢, 魏晉南北朝, 隋唐五代, 宋遼金, 元明清, 近現代} | FR-002 |
| TDD-TEST-005 | `calligraphy_type` 字段枚举检查 | 任一文件 | 字段值 in {篆書, 隶書, 楷書, 行書, 草書, 其他} | FR-001 |
| TDD-TEST-006 | 文件名 slug 检查 | 任一文件 | slug 全小写 ASCII，文件名与 name 对应 | FR-002 |
| TDD-TEST-007 | `release_date` 格式检查 | 任一文件 | 字符串能 `datetime.strptime(s, "%Y-%m-%d")` 解析 | FR-004 |
| TDD-TEST-008 | `year` 为整数 | 任一文件 | `isinstance(v, int)` | FR-001 |
| TDD-TEST-009 | `content` 非空 | 任一文件 | `len(content.strip()) > 0` | FR-001 |
| TDD-TEST-010 | 重复 slug 检查 | 所有文件 | 无任何两个文件的 slug 相同 | FR-003 |
| TDD-TEST-011 | 朝代枚举值与目录一致 | 任一文件 | `dynasty` 字段值对应所在目录的 slug | FR-002 |

## 测试执行

```bash
# 安装校验依赖
pip install jsonschema

# 运行
python scripts/validate.py
```

**通过标准**：exit code 0 且每行输出 `✓ 档案名`。

## 新增数据时的自测

贡献者提交 PR 前应：

1. 把新增 JSON 文件放入对应朝代数目录
2. 执行 `python scripts/validate.py`
3. 确认新增文件出现在通过列表中
