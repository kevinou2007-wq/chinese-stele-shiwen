"""从 per_stele 目录（独立 JSON 文件）导入碑帖数据。

源目录：Marvis/output/per_stele/ 下的 *.json（每个文件一碑）
目标目录：data/stele/{dynasty_slug}/per_{原文件名}.json

与旧 batch 导入的区别：
- 源文件本身就是单碑 JSON，无 batch 包裹
- 文件名含完整朝代-作者-碑名，信息更丰富
- 直接复制字段，仅做朝代枚举映射

用法：
    python scripts/import_per_stele.py
    python scripts/import_per_stele.py --source "C:/path/to/per_stele"
    python scripts/import_per_stele.py --dry-run
    python scripts/import_per_stele.py --clean   # 清除旧的 stele_*.json 再导入
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

# ── 朝代映射（同 convert_marvis_data.py）──
DYNASTY_MAP = {
    # 秦汉
    "秦": "秦漢",
    "西汉": "秦漢",
    "西汉-东汉": "秦漢",
    "东汉": "秦漢",
    "新朝": "秦漢",
    "先秦": "秦漢",
    "东周": "秦漢",
    "西周": "秦漢",
    # 魏晋南北朝
    "三国魏": "魏晉南北朝",
    "三国吴": "魏晉南北朝",
    "西晋": "魏晉南北朝",
    "东晋": "魏晉南北朝",
    "北魏": "魏晉南北朝",
    "南朝宋": "魏晉南北朝",
    "南朝梁": "魏晉南北朝",
    "北周": "魏晉南北朝",
    "北齐": "魏晉南北朝",
    # 隋唐五代
    "隋": "隋唐五代",
    "唐": "隋唐五代",
    "唐/武周": "隋唐五代",
    "五代": "隋唐五代",
    # 宋辽金
    "北宋": "宋遼金",
    "南宋": "宋遼金",
    # 元明清
    "元": "元明清",
    "明": "元明清",
    "清": "元明清",
    "明清": "元明清",
    # 近现代
    "民国": "近現代",
}

DYNASTY_TO_DIR = {
    "秦漢": "qin_han",
    "魏晉南北朝": "wei_jin_nanbei",
    "隋唐五代": "sui_tang",
    "宋遼金": "song_liao_jin",
    "元明清": "yuan_ming_qing",
    "近現代": "modern",
}


def normalize_dynasty(raw: str) -> str:
    if not raw:
        return ""
    if raw in DYNASTY_MAP:
        return DYNASTY_MAP[raw]
    for key, val in DYNASTY_MAP.items():
        if key in raw:
            return val
    return ""


def year_from_text(text: str) -> int:
    """从文本中提取公元纪年（取第一个匹配）。"""
    if not text:
        return -1
    m = re.search(r"(\d{3,4})\s*年", text)
    if m:
        return int(m.group(1))
    m = re.search(r"前\s*(\d+)", text)
    if m:
        return -int(m.group(1))
    return -1


def convert_file(src: Path) -> tuple[str, str, dict] | None:
    try:
        data = json.load(src.open(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"  [跳过] {src.name}: {e}")
        return None

    name = data.get("name", "").strip()
    raw_dynasty = data.get("dynasty", "").strip()
    calligrapher = data.get("calligrapher", "").strip()
    stele_type = data.get("type", "").strip()
    note = data.get("note", "").strip()
    original = data.get("original", "").strip()
    translation = data.get("translation", "").strip()
    src_id = data.get("id", -1)

    if not name:
        print(f"  [跳过] {src.name}: 无 name 字段")
        return None

    dynasty = normalize_dynasty(raw_dynasty)
    dynasty_dir = DYNASTY_TO_DIR.get(dynasty, "unknown")

    # 年份：优先从 note 提取（最详细的来源文本）
    year = year_from_text(note)
    if year == -1:
        year = year_from_text(original)

    # 构建 source
    source = f"Marvis per_stele 数据集"
    if src_id and src_id != -1:
        source += f" (id={src_id})"

    # 构建 description
    parts = []
    if stele_type:
        parts.append(f"类型：{stele_type}")
    if raw_dynasty and raw_dynasty != dynasty:
        parts.append(f"原始朝代：{raw_dynasty}")
    if calligrapher:
        parts.append(f"作者：{calligrapher}")
    if note:
        parts.append(note)
    description = "。".join(parts)

    converted = {
        "name": name,
        "dynasty": dynasty,
        "author": calligrapher if calligrapher else "不详",
        "year": year,
        "calligraphy_type": "其他",  # per_stele 不直接提供书体枚举，由 type 字段描述
        "source": source,
        "editor": "marvis-import-v2",
        "release_date": "2024-12-01",
        "description": description,
        "content": translation if translation else original,
        "original_text": original,
        "translation": translation,
        "note": note,
        "raw_type": stele_type,
        "raw_dynasty": raw_dynasty,
        "marvis_id": src_id,
    }

    # 用源文件名做 slug（保留中文以便识别）
    slug = src.stem  # 如 "三国吴-传皇象（有争议）-天发神谶碑"
    out_filename = f"per_{slug}.json"

    return dynasty_dir, out_filename, converted


def main():
    parser = argparse.ArgumentParser(description="从 per_stele 目录导入独立 JSON 碑帖")
    parser.add_argument("--source",
        default=r"C:/Users/Administrator/AppData/Roaming/Tencent/Marvis/User/oAN1i2Z_UvqTUtGVkWMhJueKmvm0/workspace/conv_19f2b92b58e_f5f39f79e202/output/per_stele",
        help="源目录路径")
    parser.add_argument("--target", default="data/stele", help="目标根目录")
    parser.add_argument("--dry-run", action="store_true", help="只打印不写")
    parser.add_argument("--clean", action="store_true", help="清除旧 stele_*.json 再导入")
    args = parser.parse_args()

    source = Path(args.source).resolve()
    target = Path(args.target).resolve()

    if not source.is_dir():
        print(f"[!] 源目录不存在: {source}")
        return

    files = sorted(source.glob("*.json"))
    print(f"源目录: {source}")
    print(f"源文件数: {len(files)}")

    if args.clean:
        # 删除所有旧的 stele_*.json 文件
        old_files = list(target.rglob("stele_*.json"))
        for f in old_files:
            f.unlink()
        if old_files:
            print(f"已清除 {len(old_files)} 个旧 stele_*.json 文件")

    stats: dict[str, int] = {}
    written = 0
    skipped = 0

    for f in files:
        result = convert_file(f)
        if result is None:
            skipped += 1
            continue

        dynasty_slug, out_filename, converted = result

        if args.dry_run:
            stats[dynasty_slug] = stats.get(dynasty_slug, 0) + 1
            if written < 5:
                print(f"  [DRY] {dynasty_slug}/{out_filename} ← {f.name}")
            written += 1
            continue

        out_dir = target / dynasty_slug
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / out_filename

        try:
            with out_file.open("w", encoding="utf-8") as fp:
                json.dump(converted, fp, ensure_ascii=False, indent=2)
                fp.write("\n")
            written += 1
            stats[dynasty_slug] = stats.get(dynasty_slug, 0) + 1
        except Exception as e:
            print(f"  [错误] {f.name}: {e}")

    dir_names = {
        "qin_han": "秦汉", "wei_jin_nanbei": "魏晋南北朝",
        "sui_tang": "隋唐五代", "song_liao_jin": "宋辽金",
        "yuan_ming_qing": "元明清", "modern": "近现代", "unknown": "未知",
    }
    print(f"\n{'='*50}")
    action = "将写入" if args.dry_run else "已写入"
    print(f"[{action}] {written} 个文件（跳过 {skipped}）")
    for slug in ["qin_han", "wei_jin_nanbei", "sui_tang", "song_liao_jin", "yuan_ming_qing", "modern", "unknown"]:
        cnt = stats.get(slug, 0)
        if cnt:
            print(f"  {dir_names.get(slug, slug)}: {cnt}")


if __name__ == "__main__":
    main()
