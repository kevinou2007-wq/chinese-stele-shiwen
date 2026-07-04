"""chinese-stele-shiwen 数据校验脚本

遍历 data/stele/ 下所有 JSON 文件，按 schema 校验 + 检查命名约定。
退出码 0 = 全部通过，非 0 = 有错误。

    python scripts/validate.py            # 校验所有文件
    python scripts/validate.py --target data/stele/sui_tang  # 只校验指定目录
    python scripts/validate.py --verbose   # 显示详细信息
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    import jsonschema
except ImportError:
    sys.stderr.write("[!] 缺少 jsonschema 库。请运行：pip install jsonschema\n")
    sys.exit(2)

# 朝代枚举（与 schema.json 保持一致）
VALID_DYNASTIES = {"秦漢", "魏晉南北朝", "隋唐五代", "宋遼金", "元明清", "近現代"}

# 朝代目录 slug → 对应 dynasty 字段值映射
DIR_TO_DYNASTY = {
    "qin_han": "秦漢",
    "wei_jin_nanbei": "魏晉南北朝",
    "sui_tang": "隋唐五代",
    "song_liao_jin": "宋遼金",
    "yuan_ming_qing": "元明清",
    "modern": "近現代",
}

VALID_CALLIGRAPHY_TYPES = {"篆書", "隶書", "楷書", "行書", "草書", "其他"}

# 文件名允许中文（碑名）+ 数字前缀，如 stele_001_毛公鼎.json
SLUG_RE = re.compile(r"^stele_\d+_[\w\u4e00-\u9fff\-]+\.json$")


def load_schema(root: Path) -> dict:
    """加载 schema.json，schema 自身必须能被 jsonschema 解析。"""
    schema_path = root / "data" / "schema.json"
    if not schema_path.is_file():
        sys.stderr.write(f"[!] schema 文件不存在: {schema_path}\n")
        sys.exit(2)
    with schema_path.open(encoding="utf-8") as f:
        schema = json.load(f)
    # 验证 schema 自身合法
    try:
        jsonschema.Draft7Validator.check_schema(schema)
    except jsonschema.SchemaError as e:
        sys.stderr.write(f"[!] schema 自身不合法: {e}\n")
        sys.exit(2)
    return schema


def validate_date(text: str) -> bool:
    """校验 YYYY-MM-DD 格式。"""
    try:
        datetime.strptime(text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def check_file(path: Path, schema: dict, root: Path, verbose: bool) -> list[str]:
    """对单个文件做所有校验，返回错误列表（无错返回 []）。"""
    errors: list[str] = []
    display = path.relative_to(root).as_posix()

    # — 1. 文件名 slug 检查 —
    if not SLUG_RE.match(path.name):
        errors.append(f"{display}: 文件名不符合 slug 约定（全小写 ASCII/数字/_/- → .json）")

    # — 2. 读取 JSON —
    try:
        with path.open(encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(f"{display}: JSON 解析失败: {e}")
        return errors  # 无法继续后续检查
    except UnicodeDecodeError as e:
        errors.append(f"{display}: 文件编码必须是 UTF-8（无 BOM）: {e}")
        return errors

    # — 3. Schema 校验 —
    try:
        jsonschema.validate(data, schema)
    except jsonschema.ValidationError as e:
        errors.append(f"{display}: Schema 校验失败 — {e.message} @ {list(e.absolute_path)}")
        # schema 失败不立即返回，继续发现更多问题

    # — 4. dynasty 枚举 + 目录一致性 —
    if "dynasty" in data:
        if data["dynasty"] not in VALID_DYNASTIES:
            errors.append(f"{display}: dynasty 值 {data['dynasty']!r} 不在枚举中")
        dir_slug = path.parent.name
        expected = DIR_TO_DYNASTY.get(dir_slug)
        if expected is not None and data["dynasty"] != expected:
            errors.append(f"{display}: dynasty={data['dynasty']!r} 与目录 {dir_slug} 期望 {expected} 不符")

    # — 5. calligraphy_type 枚举 —
    if "calligraphy_type" in data:
        if data["calligraphy_type"] not in VALID_CALLIGRAPHY_TYPES:
            errors.append(f"{display}: calligraphy_type 值 {data['calligraphy_type']!r} 不在枚举中")

    # — 6. release_date 格式 —
    if "release_date" in data and data["release_date"] is not None:
        if not validate_date(data["release_date"]):
            errors.append(f"{display}: release_date 应为 YYYY-MM-DD 格式，得到 {data['release_date']!r}")

    # — 7. year 为整数 —
    if "year" in data and not isinstance(data["year"], int):
        errors.append(f"{display}: year 应为整数，得到 {type(data['year']).__name__}")

    # — 8. content 非空 —
    if "content" in data:
        if not isinstance(data["content"], str) or not data["content"].strip():
            errors.append(f"{display}: content 不能为空白字符串")

    return errors


def main():
    parser = argparse.ArgumentParser(description="校验碑帖释文 JSON 文件")
    parser.add_argument("--target", default="data/stele", help="要校验的根目录")
    parser.add_argument("--verbose", "-v", action="store_true", help="显示详细信息")
    args = parser.parse_args()

    data_dir = Path(args.target).resolve()
    # 脚本位于 scripts/，项目根目录是 scripts/ 的上级
    root = Path(__file__).resolve().parent.parent
    if not data_dir.is_dir():
        sys.stderr.write(f"[!] 数据目录不存在: {data_dir}\n")
        sys.exit(2)

    schema = load_schema(root)

    files = sorted(data_dir.rglob("*.json"))
    if not files:
        print(f"[!] {data_dir} 下未找到任何 JSON 文件")
        sys.exit(1)

    all_errors: list[str] = []
    seen_slugs: dict[str, Path] = {}
    ok_count = 0

    for f in files:
        file_errors = check_file(f, schema, root, args.verbose)
        if file_errors:
            all_errors.extend(file_errors)
        else:
            ok_count += 1
            if args.verbose:
                print(f"✓ {f.relative_to(root).as_posix()}")

        # — 9. 重复 slug 检查 —
        slug = f.name.lower()
        if slug in seen_slugs:
            all_errors.append(f"{f.relative_to(root).as_posix()}: 文件名 {slug} 与 {seen_slugs[slug].relative_to(root).as_posix()} 重复")
        else:
            seen_slugs[slug] = f

    # — 输出结果 —
    if all_errors:
        print(f"\n[✗] 共发现 {len(all_errors)} 个问题（{ok_count}/{len(files)} 文件通过校验）：")
        for e in all_errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print(f"[✓] 校验通过！{ok_count}/{len(files)} 文件全部符合 Schema 与命名约定。")
        sys.exit(0)


if __name__ == "__main__":
    main()
