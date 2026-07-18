"""批量从维基文库抓取碑帖全文，补全截断条目。

用法：
    python scripts/fix_via_wikisource.py              # 修复所有截断条目
    python scripts/fix_via_wikisource.py --list "碑名" # 指定碑名
    python scripts/fix_via_wikisource.py --dry-run    # 预览
"""

from __future__ import annotations
import argparse, json, re, os, subprocess, shutil
from pathlib import Path

# 碑名 → 维基文库词条名映射（部分词条名与数据库不同）
WIKI_MAP = {
    "孔子庙堂碑": "孔子廟堂碑",
    "龙藏寺碑": "龍藏寺碑",
    "化度寺碑": "化度寺碑",
    "道因法师碑": "道因法師碑",
    "皇甫诞碑": "皇甫誕碑",
    "虞恭公碑": "虞恭公碑",
    "孟法师碑": "孟法師碑",
    "房玄龄碑": "房玄齡碑",
    "伊阙佛龛碑": "伊闕佛龕碑",
    "神策军碑": "神策軍碑",
    "颜氏家庙碑": "顏氏家廟碑",
    "元结碑": "元結碑",
    "宋璟碑": "宋璟碑",
    "臧怀恪碑": "臧懷恪碑",
    "郭氏家庙碑": "郭氏家廟碑",
    "殷君夫人碑": "殷君夫人碑",
    "等慈寺碑": "等慈寺碑",
    "昭仁寺碑": "昭仁寺碑",
    "信行禅师碑": "信行禪師碑",
    "颜勤礼碑": "顏勤禮碑",
}

def fetch_wikisource(name: str, wiki_name: str | None = None) -> str | None:
    """从维基文库抓取碑文全文"""
    page = wiki_name or WIKI_MAP.get(name, name)
    from urllib.parse import quote
    url = f"https://zh.wikisource.org/wiki/{quote(page)}"
    
    try:
        result = subprocess.run(
            ['curl', '-sL', '--connect-timeout', '8', '--max-time', '20',
             url],
            capture_output=True, text=True, timeout=25,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0,
        )
        html = result.stdout
        if not html or 'wgNamespaceNumber' not in html:
            return None
        
        # 提取正文（在 wikisource 中正文通常紧随导航）
        text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', '\n', text)
        lines = [l.strip() for l in text.split('\n') if l.strip() and len(l.strip()) > 2]
        
        # 找正文起始（跳过词条头/导航）
        start = -1
        header_markers = ['维基文库', '自由的图书馆', '语言', '下载', '打印', '此页面', '导航', '目录', '模板', 'Category']
        for i, l in enumerate(lines):
            if any(m in l for m in header_markers):
                continue
            if len(l) > 20 and any('\u4e00' <= c <= '\u9fff' for c in l[:5]):
                # 第一段真正的中文正文
                if not any(m in l for m in ['此', '本页', '根据']):
                    start = i
                    break
        
        if start < 0:
            return None
        
        # 收集正文直到遇到维基模板/版权声明
        result_lines = []
        for j in range(start, min(start+300, len(lines))):
            l = lines[j]
            if any(x in l for x in ['Public domain', 'PD-', 'Author-PD', '此', '作品在', '逝世已经', 'Template:', '分类:']):
                break
            if any(x in l for x in ['知识共享', '授权', '附加条款', '免责声明', '维基媒体', 'Copyright']):
                if result_lines:
                    break
                continue
            if l.startswith('==') or l.startswith('{{'):
                if result_lines:
                    break
                continue
            if len(l) > 3:
                result_lines.append(l)
        
        full = '\n'.join(result_lines)
        return full if len(full) > 100 else None
    
    except Exception as e:
        print(f"  [fetch error] {name}: {e}")
        return None


def find_truncated_files(root: Path) -> list[tuple[Path, dict, int]]:
    """查找疑似截断的文件"""
    results = []
    big_types = ['碑', '墓志', '颂', '铭', '记', '石经', '摩崖']
    for dp in sorted(root.rglob('per_*.json')):
        try:
            data = json.load(dp.open(encoding='utf-8'))
        except:
            continue
        name = data.get('name', '')
        rtype = data.get('raw_type', '')
        text = data.get('original_text', '')
        n = len(re.sub(r'\s+', '', text))
        is_big = any(t in name or t in rtype for t in big_types)
        if is_big and n < 200:
            results.append((dp, data, n))
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--list', type=str, nargs='*', help='指定碑名列表')
    parser.add_argument('--limit', type=int, default=0)
    args = parser.parse_args()
    
    root = Path(__file__).resolve().parent.parent
    os.chdir(root)
    
    if args.list:
        # 手动指定模式
        truncated = []
        for name in args.list:
            for dp in root.rglob('per_*.json'):
                try:
                    data = json.load(dp.open(encoding='utf-8'))
                    if data.get('name') == name:
                        n = len(re.sub(r'\s+', '', data.get('original_text', '')))
                        truncated.append((dp, data, n))
                        break
                except:
                    continue
    else:
        truncated = find_truncated_files(root)
    
    print(f'需要核对: {len(truncated)} 条')
    if args.limit:
        truncated = truncated[:args.limit]
    
    fixed = 0
    for i, (path, data, old_len) in enumerate(truncated):
        name = data['name']
        print(f'\n[{i+1}/{len(truncated)}] {name} ({old_len}字)', end=' ')
        
        if args.dry_run:
            print('[dry-run]')
            continue
        
        full_text = fetch_wikisource(name)
        if full_text and len(full_text) > old_len * 1.5:
            data['original_text'] = full_text
            data['content'] = full_text
            data['note'] = (data.get('note','') + f'【2024-12核对】据维基文库补全全文（{old_len}→{len(full_text)}字）。').strip()
            with path.open('w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                f.write('\n')
            print(f'✓ {old_len}→{len(full_text)}字')
            fixed += 1
        elif full_text:
            print(f'- 抓取内容不足({len(full_text)}字)')
        else:
            print('- 未抓取到')
    
    print(f'\n修复完成: {fixed}/{len(truncated)}')


if __name__ == '__main__':
    main()
