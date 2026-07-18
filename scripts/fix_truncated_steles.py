"""使用 baike.baidu.com 抓取碑帖全文，补全被截断的条目。

已知可抓取的百度百科条目有完整的碑文（如前100字含"君讳"等标志性开头）。
本脚本：
1. 扫描 data/stele/ 下所有 JSON
2. 找出 original_text 疑似截断的（<200字的大作品）
3. 尝试从百度百科抓取完整碑文
4. 自动更新 JSON 文件

用法：
    python scripts/fix_truncated_steles.py           # 全量扫描
    python scripts/fix_truncated_steles.py --dry-run # 预览
    python scripts/fix_truncated_steles.py --limit 5 # 先试5条
"""

from __future__ import annotations

import argparse
import json
import re
import os
import subprocess
import time
from pathlib import Path

# 大作品类型（字数应 >200 的）
BIG_TYPES = ['碑', '墓志', '颂', '铭', '记', '石经']

# 百度百科词条名（从文件名或 name 字段提取）
def baike_url(name: str) -> str:
    """构建百度百科搜索 URL"""
    encoded = name.replace(' ', '%20')
    # 用百度百科 API 搜索
    return f"https://baike.baidu.com/item/{encoded}"


def is_truncated(data: dict) -> bool:
    """判断是否为截断的大作品"""
    text = data.get('original_text', '')
    rtype = data.get('raw_type', '')
    name = data.get('name', '')
    n = len(re.sub(r'\s+', '', text))
    is_big = any(t in name or t in rtype for t in BIG_TYPES)
    return is_big and n < 200


def extract_stele_text_from_html(html: str) -> str | None:
    """从百度百科 HTML 中提取碑文正文。

    启发式：找"原文"标记后的连续中文段落，或找以"君讳"/"永和"/"九成宫"等开头的段落。
    """
    # 清理 HTML
    text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', '\n', text)
    lines = [l.strip() for l in text.split('\n') if l.strip() and len(l.strip()) > 5]

    # 查找碑文标志
    markers = ['君讳', '永和九年', '九成宫', '皇帝立国', '维贞观',
               '上天帝言', '圣人因', '太岳之', '易称', '大唐',
               '维永平', '维天监', '若夫', '粤若', '盖闻', '维皇', '维大']

    for marker in markers:
        for i, line in enumerate(lines):
            if marker in line:
                # 收集从这个标志开始的连续段落
                result = []
                for j in range(i, min(i + 200, len(lines))):
                    l = lines[j]
                    if len(l) < 100 and not re.match(r'^[\u4e00-\u9fff\w]', l):
                        if result and len(result[-1]) > 50:
                            break
                        continue
                    result.append(l)
                full = '\n'.join(result)
                if len(full) > 100:
                    return full

    return None


def fetch_baike_text(name: str) -> str | None:
    """抓取百度百科词条的碑文内容"""
    url = baike_url(name)
    try:
        result = subprocess.run(
            ['curl', '-sL', '--connect-timeout', '10', '--max-time', '25',
             '-H', 'User-Agent: Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36',
             url],
            capture_output=True, text=True, timeout=30,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0,
        )
        html = result.stdout
        if not html or len(html) < 500:
            return None
        return extract_stele_text_from_html(html)
    except Exception as e:
        print(f"  [fetch error] {name}: {e}")
        return None


def scan_steles(target: str) -> list[Path]:
    """扫描所有疑似截断的条目"""
    dirs_to_scan = ['data/stele/qin_han', 'data/stele/wei_jin_nanbei',
                    'data/stele/sui_tang', 'data/stele/song_liao_jin',
                    'data/stele/yuan_ming_qing']
    truncated = []
    for d in dirs_to_scan:
        dp = Path(target) / d
        if not dp.is_dir():
            continue
        for f in sorted(dp.glob('per_*.json')):
            try:
                data = json.load(f.open(encoding='utf-8'))
            except Exception:
                continue
            if is_truncated(data):
                truncated.append(f)
    return truncated


def main():
    parser = argparse.ArgumentParser(description='补全截断的碑帖数据')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--limit', type=int, default=0)
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    os.chdir(project_root)

    truncated = scan_steles(str(project_root))
    print(f'发现 {len(truncated)} 条疑似截断条目')

    if args.limit > 0:
        truncated = truncated[:args.limit]
        print(f'限制处理前 {args.limit} 条')

    fixed = 0
    for i, path in enumerate(truncated):
        data = json.load(path.open(encoding='utf-8'))
        name = data['name']
        rtype = data.get('raw_type', '')
        n = len(re.sub(r'\s+','', data.get('original_text','')))
        print(f'\n[{i+1}/{len(truncated)}] {name} ({rtype}, {n}字)')

        if args.dry_run:
            continue

        # 抓取百度百科
        time.sleep(1)  # 礼貌等待
        full_text = fetch_baike_text(name)
        if full_text and len(full_text) > n * 1.2:
            data['original_text'] = full_text
            data['note'] = (data.get('note','') + f'【2024-12核对】据百度百科补充全文（原{n}字→{len(full_text)}字）。').strip()
            with path.open('w', encoding='utf-8') as fo:
                json.dump(data, fo, ensure_ascii=False, indent=2)
                fo.write('\n')
            print(f'  ✓ 已更新: {n} → {len(full_text)} 字')
            fixed += 1
        else:
            if full_text:
                print(f'  - 抓取内容相同({len(full_text)}字)，跳过')
            else:
                print(f'  - 未抓取到全文')

    print(f'\n处理完成: 修复 {fixed}/{len(truncated)} 条')


if __name__ == '__main__':
    main()
