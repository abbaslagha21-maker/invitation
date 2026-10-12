# Builds hl-themes.html: the six highlight covers in the white and blue styles.
ICONS = [
  'LOGO',
  '<path d="M13 22h38l-3.2 32.5a2 2 0 0 1-2 1.8H18.2a2 2 0 0 1-2-1.8z"/><path d="M24 26v-7a8 8 0 0 1 16 0v7"/><path d="M27 40l4 4 7-8" stroke="{g}"/>',
  '<path d="M12 12h40a3 3 0 0 1 3 3v24a3 3 0 0 1-3 3H30l-11 9v-9h-7a3 3 0 0 1-3-3V15a3 3 0 0 1 3-3z"/><path d="M27 23.5a5 5 0 1 1 7.2 4.5c-1.4.7-2.2 1.8-2.2 3.3v1" stroke="{s}"/><circle cx="32" cy="36.6" r="0.6" fill="{s}" stroke="{s}" stroke-width="2.6"/>',
  '<path d="M8 44L44 8l12 12-36 36z"/><path d="M16.2 35.8l5 5M27.2 24.8l5 5M38.2 13.8l5 5" stroke="{g}"/><path d="M21.7 30.3l3 3M32.7 19.3l3 3" stroke="{s}"/>',
  '<path d="M6 17h31v26H6z"/><path d="M37 25h10.5L56 34v9H37"/><circle cx="17" cy="45" r="5" fill="{bg}"/><circle cx="46" cy="45" r="5" fill="{bg}"/><path d="M13 26h12M13 32h8" stroke="{s}"/>',
  '<path d="M32 57S15 41.5 15 27.5a17 17 0 0 1 34 0C49 41.5 32 57 32 57z"/><circle cx="32" cy="27" r="6.5" stroke="{g}"/>',
]
THEMES = {
  'white': dict(bg='#ffffff', page='background:#ffffff', ring='#E1ECF8', stroke='#0A2F72', g='#3f9a35', s='#2F9FE4', logo='assets/icon-dark.png'),
  'blue':  dict(bg='#2a72bd', page='background:linear-gradient(135deg,#1f4fa0 0%,#2f80c8 55%,#3aa0da 100%)', ring='rgba(255,255,255,0.35)', stroke='#ffffff', g='#C9F2B5', s='#D6EEFF', logo='assets/icon-white.png'),
}
frames = []
for name, t in THEMES.items():
    for icon in ICONS:
        if icon == 'LOGO':
            glyph = f'<img class="glyph" src="{t["logo"]}" alt="">'
        else:
            body = icon.format(g=t['g'], s=t['s'], bg=t['bg'])
            glyph = (f'<div class="glyph"><svg viewBox="0 0 64 64" fill="none" stroke="{t["stroke"]}" stroke-width="3.2" '
                     f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg></div>')
        frames.append(f'<div class="frame" style="{t["page"]}"><div class="disc" style="border-color:{t["ring"]}"></div>{glyph}</div>')
html = '''<!doctype html><html><head><meta charset="utf-8"><style>
*{box-sizing:border-box} html,body{margin:0;background:#000}
.frame{position:relative;width:1080px;height:1920px;overflow:hidden}
.disc{position:absolute;left:50%;top:50%;width:760px;height:760px;margin:-380px 0 0 -380px;border-radius:50%;border:6px solid}
.glyph{position:absolute;left:50%;top:50%;width:440px;height:440px;margin:-220px 0 0 -220px;object-fit:contain}
.glyph svg{width:100%;height:100%;display:block}
</style></head><body>''' + '\n'.join(frames) + '</body></html>'
open('hl-themes.html', 'w', encoding='utf-8').write(html)
