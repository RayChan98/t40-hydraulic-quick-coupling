# -*- coding: utf-8 -*-
"""把 04-范本自审 的 3 篇英文文章转成博客 md 页（BlogLayout 驱动）"""
import re, os

SRC_DIR = r'D:\kravzik-work\t40-hydraulic-quick-coupling\04-范本自审'
DST_DIR = r'D:\kravzik-work\t40-hydraulic-quick-coupling\site\src\pages\blog'

ARTICLES = [
    dict(src='范本01-ISO快接互换与选型指南.md', slug='iso-7241-vs-iso-16028-vs-iso-5675',
         title='ISO 7241 vs ISO 16028 vs ISO 5675: Interchange & Selection Guide',
         category='Selection Guide', date='2026-08-24', readTime='10',
         desc='The full standard map: what ISO 7241 Series A/B, ISO 16028 flat-face and ISO 5675 agricultural couplings cover, which profiles interchange, how to size and select - plus the 8-step replacement qualification process.'),
    dict(src='批量B1-如何识别液压快接.md', slug='how-to-identify-hydraulic-quick-couplings',
         title='How to Identify Hydraulic Quick Couplings: A Field Guide',
         category='Maintenance', date='2026-08-24', readTime='6',
         desc='Identify any hydraulic quick coupling in 5 steps: record the application, inspect both mating halves, measure critical features, check operating condition, confirm with a drawing.'),
    dict(src='批量B2-液压快接泄漏修复.md', slug='hydraulic-quick-disconnect-leaking-fixes',
         title='Hydraulic Quick Disconnect Leaking? Top 5 Causes & Fixes',
         category='Maintenance', date='2026-08-24', readTime='7',
         desc='The top 5 causes of hydraulic quick disconnect leaks - contamination, seal wear, sleeve damage, wrong valve arrangement, trapped pressure - and the fixes that actually work.'),
]

def slugify(s):
    s = s.lower()
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'[\s]+', '-', s.strip())
    return s

def strip_meta(lines):
    out = []
    for ln in lines:
        if re.match(r'^>\s*(范本|目标主词|做优对照|批量|词源)', ln):
            continue
        out.append(ln)
    return out

def esc(s):
    return s.replace('"', "'")

for a in ARTICLES:
    src = os.path.join(SRC_DIR, a['src'])
    text = open(src, encoding='utf-8').read()
    lines = text.split('\n')
    lines = [l for l in lines if not l.startswith('# ')]
    lines = strip_meta(lines)
    body = '\n'.join(lines).strip()
    toc = []
    def renum(m):
        label = re.sub(r'^\d+\.\s*', '', m.group(1)).strip()
        toc.append({'id': slugify(label), 'label': label})
        return '## ' + label
    body = re.sub(r'^##\s+(.+)$', lambda m: renum(m), body, flags=re.M)
    toc_lines = []
    for t in toc:
        toc_lines.append('      - id: "' + t['id'] + '"')
        toc_lines.append('        label: "' + esc(t['label']) + '"')
    yaml_toc = '\n'.join(toc_lines)
    fm_lines = []
    fm_lines.append('---')
    fm_lines.append('layout: ../../layouts/BlogLayout.astro')
    fm_lines.append('title: "' + esc(a['title']) + '"')
    fm_lines.append('category: "' + a['category'] + '"')
    fm_lines.append('date: "' + a['date'] + '"')
    fm_lines.append('readTime: "' + a['readTime'] + '"')
    fm_lines.append('author: "Ray Chan"')
    fm_lines.append('description: "' + esc(a['desc']) + '"')
    fm_lines.append('toc:')
    fm_lines.append(yaml_toc)
    fm_lines.append('---')
    fm_lines.append('')
    dst = os.path.join(DST_DIR, a['slug'] + '.md')
    open(dst, 'w', encoding='utf-8').write('\n'.join(fm_lines) + '\n\n' + body + '\n')
    print('OK', a['slug'], '| toc', len(toc), '| words', len(body.split()))
print('TOTAL', len(ARTICLES))
