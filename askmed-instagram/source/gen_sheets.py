# Builds compare.html (all pinned versions) and hl-styles.html (highlight cover styles).
import json, sys
O = '/home/user/invitation/askmed-instagram'
versions = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'versions.json', encoding='utf-8'))
out = sys.argv[2] if len(sys.argv) > 2 else 'compare.html'
head = '''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Alexandria:wght@400;600;800;900&display=swap" rel="stylesheet">
<style>*{box-sizing:border-box}html,body{margin:0;background:#fff}
.sheet{width:1080px;background:#fff;font-family:'Alexandria',sans-serif;color:#0A2F72;padding:36px 0 30px}
.v{padding:26px 0 18px}.v+.v{border-top:1px solid #e3e8ef}
.h{display:flex;align-items:center;gap:18px;padding:0 36px 16px}
.k{flex:0 0 auto;width:64px;height:64px;border-radius:50%;background:#0A2F72;color:#fff;display:flex;align-items:center;justify-content:center;font-size:34px;font-weight:900;font-family:Arial,sans-serif}
.t{font-size:34px;font-weight:800;line-height:1.3}.d{font-size:23px;font-weight:400;color:#5b6b85;line-height:1.5;margin-top:2px}
.grid{display:flex;direction:ltr;gap:3px}.grid img{width:358px;display:block}
.row{display:flex;gap:20px;padding:0 36px}.c{width:150px;display:flex;flex-direction:column;align-items:center;gap:10px}
.ring{width:148px;height:148px;border-radius:50%;padding:6px;border:3px solid #d6dbe3}
.ring div{width:100%;height:100%;border-radius:50%;background-size:145% auto;background-position:center}
.c b{font-size:21px;font-weight:600;color:#13213a;white-space:nowrap}
</style></head><body>'''
parts = [head, '<div class="sheet" id="compare">']
for v in versions:
    imgs = ''.join(f'<img src="{O}/{v["dir"]}/{n}.jpg" alt="">' for n in ['post-3_left', 'post-2_middle', 'post-1_right'])
    parts.append(f'<div class="v"><div class="h"><div class="k">{v["key"]}</div><div><div class="t">{v["title"]}</div>'
                 f'<div class="d">{v["desc"]}</div></div></div><div class="grid">{imgs}</div></div>')
parts.append('</div>')
labels = ['من نحن', 'المنتجات', 'اسألنا', 'المقاسات', 'التوصيل', 'موقعنا']
slugs = ['1-min-nehna', '2-el-montajet', '3-is2alna', '4-el-2iyesat', '5-el-tawsil', '6-wen-nehna']
styles = [('1', 'كحلي', 'covers'), ('2', 'أبيض', 'covers-white'), ('3', 'أزرق', 'covers-blue')]
parts.append('<div class="sheet" id="hlstyles">')
for k, name, d in styles:
    cells = ''.join(f'<div class="c"><div class="ring"><div style="background-image:url({O}/highlights/{d}/{s}.jpg)"></div></div><b>{l}</b></div>'
                    for s, l in zip(slugs, labels))
    parts.append(f'<div class="v"><div class="h"><div class="k">{k}</div><div><div class="t">highlights · {name}</div></div></div><div class="row">{cells}</div></div>')
parts.append('</div></body></html>')
open(out, 'w', encoding='utf-8').write('\n'.join(parts))
