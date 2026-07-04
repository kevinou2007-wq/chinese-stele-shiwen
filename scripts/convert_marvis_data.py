"""将 Marvis 导出的 380 碑帖释文批量转换为本仓库的独立 JSON 文件。

源目录：Marvis/output/ 下的 38 批 JSON 文件
目标目录：data/stele/{dynasty_slug}/stele_{NNN}.json

用法：
    python scripts/convert_marvis_data.py
    python scripts/convert_marvis_data.py --source "C:/path/to/output"
    python scripts/convert_marvis_data.py --dry-run  # 只打印不写文件
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path

# ── 朝代映射：源数据 dynasty 字段 → 本仓库 dynasty 枚举 ──
DYNASTY_MAP = {
    # 秦汉
    "秦": "秦漢",
    "西汉": "秦漢",
    "西汉-东汉": "秦漢",
    "东汉": "秦漢",
    "新朝": "秦漢",
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
    # 近现代（源数据暂无，留作扩展）
    "民国": "近現代",
}

# 朝代枚举 → 目录 slug
DYNASTY_TO_DIR = {
    "秦漢": "qin_han",
    "魏晉南北朝": "wei_jin_nanbei",
    "隋唐五代": "sui_tang",
    "宋遼金": "song_liao_jin",
    "元明清": "yuan_ming_qing",
    "近現代": "modern",
}

# ── 书体映射：源数据 script 字段 → 本仓库 calligraphy_type 枚举 ──
SCRIPT_MAP = {
    # 楷书及其变体
    "楷书": "楷書",
    "小楷": "楷書",
    "大字楷书": "楷書",
    "擘窠大字楷书": "楷書",
    "楷书（大字）": "楷書",
    "楷书（阳文）": "楷書",
    # 行书及其变体
    "行书": "行書",
    "行楷": "行書",
    "行书（稿书）": "行書",
    "行书（大字）": "行書",
    "行书（杂糅体）": "行書",
    # 草书及其变体
    "草书": "草書",
    "狂草": "草書",
    "小草": "草書",
    "章草": "草書",
    "行草": "草書",
    "行草/飞白": "草書",
    # 隶书及其变体
    "隶书": "隶書",
    "隶楷": "隶書",
    "隶书（篆隶之间）": "隶書",
    "古隶/篆书": "隶書",
    "隶书/章草": "隶書",
    # 篆书及其变体（含金文、刻石大类）
    "篆书": "篆書",
    "小篆": "篆書",
    "小篆（错金）": "篆書",
    "篆书（篆隶之间）": "篆書",
    "金文": "篆書",
    "刻石": "篆書",  # 刻石多为篆书，如石鼓文、泰山刻石
    # 多体 / 其他
    "各体（丛帖）": "其他",
    "各体": "其他",
    "各体（六种书体）": "其他",
    "古文/小篆/隶书（三体）": "其他",
    "楷书/草书": "其他",
    "楷书与草书（二体）": "其他",
    # 特殊书体
    "瘦金体": "其他",
    "漆书": "其他",
}

# 类型字段保留但不进入 schema（写入 description 末尾）


def slugify(text: str) -> str:
    """极简 slug：移除非字母数字字符，用短横线连接。

    对于中文碑名，采用"汉字直接保留 + 数字"的方式，
    保证文件名可读且唯一。
    """
    # 去除书名号
    text = text.replace("《", "").replace("》", "")
    # 替换常见符号
    text = text.replace("（", "_").replace("）", "")
    text = text.replace("(", "_").replace(")", "")
    # 用短横线替换空格和特殊字符
    text = re.sub(r"[^\w\u4e00-\u9fff\-]", "_", text, flags=re.UNICODE)
    # 合并连续下划线
    text = re.sub(r"_+", "_", text).strip("_")
    return text


def normalize_dynasty(raw: str) -> str:
    """将源数据的 dynasty 字段映射到本仓库枚举。"""
    if not raw:
        return ""
    # 精确匹配
    if raw in DYNASTY_MAP:
        return DYNASTY_MAP[raw]
    # 包含匹配（如"唐代"→"唐"）
    for key, val in DYNASTY_MAP.items():
        if key in raw:
            return val
    return ""


def normalize_script(raw: str) -> str:
    """将源数据的 script 字段映射到本仓库枚举。"""
    if not raw:
        return ""
    if raw in SCRIPT_MAP:
        return SCRIPT_MAP[raw]
    # 包含匹配
    for key, val in SCRIPT_MAP.items():
        if key in raw:
            return val
    return "其他"


def extract_dynasty_from_note(note: str) -> str:
    """从 note 字段推断朝代（用于第1批 dict 格式数据）。"""
    # 按出现频率排列
    if "西周" in note:
        return "秦漢"  # 西周不在枚举中，归入秦汉（先秦到秦汉之间四百年差距）
    if "战国" in note or "春秋" in note or "秦" in note:
        return "秦漢"
    if "西汉" in note or "东汉" in note:
        return "秦漢"
    if "北魏" in note or "东晋" in note or "西晋" in note:
        return "魏晉南北朝"
    if "南朝" in note:
        return "魏晉南北朝"
    if "隋" in note:
        return "隋唐五代"
    if "唐" in note or "武周" in note or "五代" in note:
        return "隋唐五代"
    if "北宋" in note or "南宋" in note or "辽" in note or "金" in note:
        return "宋遼金"
    if "元" in note:
        return "元明清"
    if "明" in note:
        return "元明清"
    if "清" in note:
        return "元明清"
    return ""


def convert_item(item: dict, index: int) -> tuple[str, str, dict]:
    """将源数据 item 转换为本仓库格式。

    支持两种源格式：
    - dict 格式（第1批）：type 是金文/刻石，dynasty 从 note 推断
    - list 格式（第2-38批）：标准字段

    返回：(dynasty_slug, filename, converted_dict)
    """
    name = item.get("name", "").strip()
    raw_dynasty = item.get("dynasty", "").strip()
    raw_script = item.get("script", "").strip()
    calligrapher = item.get("calligrapher", "").strip()
    date_str = item.get("date", "").strip()
    baike_query = item.get("baike_query", "").strip()
    original = item.get("original", "").strip()
    translation = item.get("translation", "").strip()
    note = item.get("note", "").strip()
    stele_type = item.get("type", "").strip()

    # ★ 第1批 dict 格式兼容：无 dynasty/script 字段，需从 note 推断
    if not raw_dynasty and not raw_script:
        # 此时 stele_type 值域：金文 / 刻石 等（大类名）
        raw_dynasty = extract_dynasty_from_note(note)
        # stele_type 作为书体大类
        raw_script = stele_type  # 金文 → 会映射到 篆書；刻石 → 其他

    # 映射
    dynasty = normalize_dynasty(raw_dynasty)
    calligraphy_type = normalize_script(raw_script)

    # 年份：从 date 字段提取公元纪年
    year = -1
    year_match = re.search(r"(\d{3,4})\s*年", date_str or note)
    if year_match:
        year = int(year_match.group(1))
    elif "前" in (date_str or note):
        bc_match = re.search(r"前\s*(\d+)", date_str or note)
        if bc_match:
            year = -int(bc_match.group(1))

    # 构建 description
    parts = []
    if stele_type:
        parts.append(f"类型：{stele_type}")
    if date_str:
        parts.append(f"年代：{date_str}")
    if note:
        parts.append(note)
    description = "。".join(parts)

    # 构建 source
    source = f"Marvis 碑帖释文数据集（第 {index // 10 + 1} 批）"
    if baike_query:
        source += f"；参考：{baike_query}"

    # 构建 content：优先使用 translation（白话译文），否则用 original
    content = translation if translation else original

    # 文件名
    slug = slugify(name) if name else f"unnamed_{index:03d}"
    filename = f"stele_{index:03d}_{slug}.json"

    # 目录
    dynasty_dir = DYNASTY_TO_DIR.get(dynasty, "unknown")

    converted = {
        "name": name,
        "dynasty": dynasty,
        "author": calligrapher if calligrapher else "不详",
        "year": year,
        "calligraphy_type": calligraphy_type,
        "source": source,
        "editor": "marvis-import",
        "release_date": "2024-12-01",
        "description": description,
        "content": content,
        # ── 扩展字段（保留原始信息） ──
        "original_text": original,
        "translation": translation,
        "note": note,
        "baike_query": baike_query,
        "raw_type": stele_type,
        "raw_date": date_str,
    }

    return dynasty_dir, filename, converted


def main():
    parser = argparse.ArgumentParser(description="转换 Marvis 碑帖释文数据")
    parser.add_argument(
        "--source",
        default=r"C:/Users/Administrator/AppData/Roaming/Tencent/Marvis/User/oAN1i2Z_UvqTUtGVkWMhJueKmvm0/workspace/conv_19f2b92b58e_f5f39f79e202/output",
        help="源数据目录",
    )
    parser.add_argument("--target", default="data/stele", help="目标数据目录")
    parser.add_argument("--dry-run", action="store_true", help="只打印不写文件")
    parser.add_argument("--verbose", "-v", action="store_true", help="显示详细信息")
    args = parser.parse_args()

    source_dir = Path(args.source).resolve()
    target_dir = Path(args.target).resolve()

    if not source_dir.is_dir():
        print(f"[!] 源目录不存在: {source_dir}")
        return

    # 收集所有批次文件
    batches = sorted(
        [f for f in source_dir.glob("碑帖释文_第*.json")],
        key=lambda x: int(re.search(r"第(\d+)批", x.name).group(1)),
    )

    if not batches:
        print(f"[!] 源目录下未找到批次文件")
        return

    print(f"找到 {len(batches)} 个批次文件")

    # 解析所有条目
    all_items: list[tuple[Path, dict]] = []  # (source_file, item)
    for batch_file in batches:
        with batch_file.open(encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            for name, v in data.items():
                # dict 格式：补充 name 字段
                if "name" not in v:
                    v["name"] = name
                all_items.append((batch_file, v))
        elif isinstance(data, list):
            for v in data:
                all_items.append((batch_file, v))

    print(f"共解析 {len(all_items)} 条碑帖数据")

    # 转换并写入
    stats: dict[str, int] = {}
    written = 0
    errors: list[str] = []

    for idx, (src_file, item) in enumerate(all_items, start=1):
        dynasty_dir, filename, converted = convert_item(item, idx)

        # 统计
        stats[dynasty_dir] = stats.get(dynasty_dir, 0) + 1

        if args.dry_run:
            if args.verbose or idx <= 5:
                print(f"  [{idx:03d}] {dynasty_dir}/{filename} — {converted['name']}")
            continue

        # 写文件
        out_dir = target_dir / dynasty_dir
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / filename

        try:
            with out_file.open("w", encoding="utf-8") as f:
                json.dump(converted, f, ensure_ascii=False, indent=2)
                f.write("\n")
            written += 1
            if args.verbose:
                print(f"  ✓ {out_file.relative_to(target_dir.parent)}")
        except Exception as e:
            errors.append(f"{filename}: {e}")

    # ── 输出统计 ──
    print(f"\n{'='*50}")
    if args.dry_run:
        print(f"[DRY RUN] 将写入 {len(all_items)} 个文件：")
    else:
        print(f"[完成] 已写入 {written} 个文件：")

    for dynasty_slug in ["qin_han", "wei_jin_nanbei", "sui_tang", "song_liao_jin", "yuan_ming_qing", "modern", "unknown"]:
        cnt = stats.get(dynasty_slug, 0)
        if cnt:
            print(f"  {dynasty_dir_name(dynasty_slug)}: {cnt}")

    if errors:
        print(f"\n[✗] {len(errors)} 个错误：")
        for e in errors:
            print(f"  - {e}")


def dynasty_dir_name(slug: str) -> str:
    """目录 slug → 中文名。"""
    m = {
        "qin_han": "秦汉",
        "wei_jin_nanbei": "魏晋南北朝",
        "sui_tang": "隋唐五代",
        "song_liao_jin": "宋辽金",
        "yuan_ming_qing": "元明清",
        "modern": "近现代",
        "unknown": "未分类",
    }
    return m.get(slug, slug)


if __name__ == "__main__":
    main()
