# Builds the showcase website (index.html) from README.md: the content is the README's, rendered; the page around it is this file's, with style.css and site.js.
# Needs Python-Markdown 3.7: python -m pip install markdown==3.7, then python build.py
import sys, re, html as htmllib, markdown

site = sys.argv[1] if len(sys.argv) > 1 else "."
md = open(site + "/README.md", encoding="utf-8").read().replace("\r\n", "\n").replace("<details>\n", '<details markdown="1">\n')
body = markdown.markdown(md, extensions=["tables", "toc", "md_in_html"], output_format="xhtml")

REPO = "https://github.com/GamesAndBacon/able-generation-2-showcase"
SITE = "https://gamesandbacon.github.io/able-generation-2-showcase/"

# ---- Content touches -----------------------------------------------------------------------------------------------------------

# Image pairs (a table of images over captions) become galleries.
def gallery(m):
    images = re.findall(r'<td style="text-align: center;">(<img [^>]*/>)</td>', m.group(1))
    captions = re.findall(r'<td style="text-align: center;">(.*?)</td>', m.group(2))
    if not images or len(images) != len(captions):
        return m.group(0)
    return '<div class="gallery">' + "".join('<figure class="shot">%s<figcaption>%s</figcaption></figure>' % ic for ic in zip(images, captions)) + "</div>"
NOT_TABLE_END = r"(?:(?!</table>).)*?"
body = re.sub(r"<table>\n<thead>\n" + NOT_TABLE_END + r"</thead>\n<tbody>\n<tr>\n((?:<td style=\"text-align: center;\"><img [^>]*/></td>\n)+)</tr>\n<tr>\n((?:<td style=\"text-align: center;\">.*?</td>\n)+)</tr>\n</tbody>\n</table>",
              gallery, body, flags=re.S)

# A screenshot and its caption become a framed figure.
body = re.sub(r"<p>(<img [^>]*/>)</p>\n<p><em>(.*?)</em></p>", r'<figure class="shot">\1<figcaption>\2</figcaption></figure>', body)
body = re.sub(r"<p>(<img [^>]*/>)</p>", r'<figure class="shot">\1</figure>', body)

# Code directories.
body = re.sub(r"<p><strong>Code directory</strong>(.*?)</p>\n<table>", r'<p class="code-heading"><span>Code directory</span>\1</p>\n<table class="code-directory">', body)

# Look closer drawers.
body = body.replace("<details>\n<summary>", '<details class="drawer">\n<summary><span class="plus" aria-hidden="true"></span>')

# ---- Sections ------------------------------------------------------------------------------------------------------------------

parts = re.split(r'<p><a name="([^"]+)"></a></p>\n', body)
intro, sections = parts[0], list(zip(parts[1::2], parts[2::2]))

def strip(s):
    return htmllib.unescape(re.sub(r"<[^>]+>", "", s)).strip()

# The intro's own lines: the tagline, the description, the notes about Look closer.
intro_paras = re.findall(r"<p>(.*?)</p>", intro, flags=re.S)
tagline = next((strip(p) for p in intro_paras if p.startswith("<strong>") and p.endswith("</strong>") and "href" not in p), "")
lede = next((p for p in intro_paras if not p.startswith("<strong>") and not p.startswith("<a ") and not p.startswith("<img") and "Generation 2.0" not in p), "")
built_on = next((p for p in intro_paras if "Generation 2.0" in p and "names" in p), "")
notes = [p for p in intro_paras if "Look closer" in p]

# Accent hues, one per chapter, round the wheel from cyan.
HUES = [186, 200, 220, 245, 268, 290, 315, 340, 12, 36, 150, 168]
chapters, rendered = [], []
for name, content in sections:
    m = re.search(r'<h2 id="[^"]*">(\d+) · (.*?)</h2>\n', content)
    tag = re.search(r"<p><strong>(.*?)</strong></p>\n", content)
    if m:
        number, title = m.group(1), m.group(2)
        hue = HUES[(int(number) - 1) % len(HUES)]
        subtitle = tag.group(1) if tag and tag.start() < m.end() + 40 else ""
        content = content[:m.start()] + content[m.end():]
        if subtitle:
            content = content.replace(tag.group(0), "", 1)
        chapters.append((name, number, strip(title), strip(subtitle), hue))
        header = f'<header class="chapter-head"><span class="chapter-num" aria-hidden="true">{number}</span><div><p class="eyebrow">Chapter {number}</p><h2>{title}</h2>' + (f'<p class="subtitle">{subtitle}</p>' if subtitle else "") + "</div></header>"
        rendered.append(f'<section class="chapter" id="{name}" style="--hue:{hue}">{header}<div class="chapter-body">{content}</div></section>')
    elif name == "the-foundation-underneath":
        h = re.search(r'<h2 id="[^"]*">(.*?)</h2>\n', content)
        title = h.group(1) if h else "The foundation underneath"
        content = content[:h.start()] + content[h.end():] if h else content
        if tag:
            content = content.replace(tag.group(0), "", 1)
        chapters.append((name, "+", strip(title), strip(tag.group(1)) if tag else "", 205))
        header = f'<header class="chapter-head"><span class="chapter-num" aria-hidden="true">+</span><div><p class="eyebrow">Underneath</p><h2>{title}</h2>' + (f'<p class="subtitle">{tag.group(1)}</p>' if tag else "") + "</div></header>"
        rendered.append(f'<section class="chapter" id="{name}" style="--hue:205">{header}<div class="chapter-body">{content}</div></section>')
    else:
        rendered.append(f'<section class="notes" id="{name}">{content}</section>')

def esc(s):
    return htmllib.escape(s, quote=True)

cards = "".join(
    f'<a class="card" href="#{name}" style="--hue:{hue}"><span class="card-num">{number}</span><span class="card-title">{esc(title)}</span><span class="card-sub">{esc(sub)}</span></a>'
    for name, number, title, sub, hue in chapters)
rail = "".join(
    f'<a class="rail-node" href="#{name}" style="--hue:{hue}" data-target="{name}"><span class="rail-dot"></span><span class="rail-label"><b>{number}</b> {esc(title)}</span></a>'
    for name, number, title, sub, hue in chapters)
options = "".join(f'<option value="{name}">{number} · {esc(title)}</option>' for name, number, title, sub, hue in chapters)

# ---- The hero's hitbox: a ring of convex pieces, drawn in, with the editor's handles -----------------------------------------------
import math
def hero_art():
    cx, cy, rx, ry, depth = 360, 270, 310, 122, 58
    pieces = []
    n = 16
    for i in range(n):
        a0, a1 = 2 * math.pi * i / n + 0.03, 2 * math.pi * (i + 1) / n - 0.03
        def pt(a, r, dy=0):
            return (cx + math.cos(a) * rx * r, cy + math.sin(a) * ry * r + dy)
        outer = [pt(a0, 1), pt(a1, 1)]
        inner = [pt(a1, 0.78), pt(a0, 0.78)]
        top = outer + inner
        bottom = [(x, y + depth) for x, y in top]
        def path(ps):
            return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in ps) + " Z"
        walls = "".join(f'<path d="M{top[k][0]:.1f},{top[k][1]:.1f} L{bottom[k][0]:.1f},{bottom[k][1]:.1f}"/>' for k in range(4))
        pieces.append(f'<g class="piece" style="--i:{i}"><path class="face" d="{path(bottom)}"/>{walls}<path class="face top" d="{path(top)}"/></g>')
    spokes = "".join(f'<path class="spoke" style="--i:{k}" d="M{cx},{cy + depth / 2} L{cx + math.cos(a) * rx * 0.78:.1f},{cy + math.sin(a) * ry * 0.78 + depth / 2:.1f}"/>' for k, a in enumerate([0.4, 1.97, 3.54, 5.11]))
    grid = "".join(f'<path d="M{x},{cy - 150} L{x * 1.6 - 216},{cy + 230}"/>' for x in range(60, 700, 60)) + "".join(f'<path d="M-40,{y} L760,{y}"/>' for y in range(cy - 140, cy + 240, 38))
    return f'''<svg class="hero-art" viewBox="0 90 720 440" role="img" aria-label="A ring-shaped hitbox built from convex pieces, with editor handles for its outer radius, height and angle.">
<defs><linearGradient id="wire" x1="0" x2="1"><stop offset="0" stop-color="#5ff0ff"/><stop offset=".55" stop-color="#8f7bff"/><stop offset="1" stop-color="#ff5fd2"/></linearGradient>
<radialGradient id="floor" cx=".5" cy=".55" r=".6"><stop offset="0" stop-color="#5ff0ff" stop-opacity=".18"/><stop offset="1" stop-color="#5ff0ff" stop-opacity="0"/></radialGradient>
<filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="3.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<g class="grid">{grid}</g><ellipse cx="{cx}" cy="{cy + 40}" rx="330" ry="150" fill="url(#floor)"/>
<g class="ring" filter="url(#glow)">{"".join(pieces)}{spokes}</g>
<g class="dome" filter="url(#glow)"><path d="M{cx - 70},{cy + 20} A70,44 0 0 1 {cx + 70},{cy + 20}"/><path d="M{cx - 70},{cy + 20} A70,20 0 0 0 {cx + 70},{cy + 20}"/></g>
<g class="handle h-radius"><line x1="{cx}" y1="{cy}" x2="{cx + rx * .92:.0f}" y2="{cy - ry * .45:.0f}"/><circle cx="{cx + rx * .92:.0f}" cy="{cy - ry * .45:.0f}" r="9"/><text x="{cx + rx * .92 - 14:.0f}" y="{cy - ry * .45 - 16:.0f}" text-anchor="end">Outer Radius  450</text></g>
<g class="handle h-height"><line x1="{cx - rx * .55:.0f}" y1="{cy - ry * .85 + depth:.0f}" x2="{cx - rx * .55:.0f}" y2="{cy - ry * .85 - 26:.0f}"/><circle cx="{cx - rx * .55:.0f}" cy="{cy - ry * .85 - 26:.0f}" r="8"/><text x="{cx - rx * .55 - 132:.0f}" y="{cy - ry * .85 - 38:.0f}">Height  50</text></g>
<g class="handle h-angle"><circle cx="{cx + 30:.0f}" cy="{cy + ry + depth + 6:.0f}" r="8"/><text x="{cx + 48:.0f}" y="{cy + ry + depth + 34:.0f}">Angle  360</text></g>
<g class="handle h-location"><circle cx="{cx}" cy="{cy}" r="12"/><text x="{cx + 20}" y="{cy + 34}">Location</text></g>
</svg>'''

# ---- The page --------------------------------------------------------------------------------------------------------------------

page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Able · Generation 2.0</title>
<meta name="description" content="A visual tour of custom Able for Unreal Engine 5.8: collision shapes you can author visually, multiple phases, reactive gameplay, persistent state and weapon integration.">
<meta property="og:title" content="Able · Generation 2.0">
<meta property="og:description" content="{esc(tagline)}">
<meta name="theme-color" content="#07090f">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="progress" aria-hidden="true"><span></span></div>
<header class="topbar"><nav aria-label="Showcase navigation">
<a class="brand" href="#top"><span class="brand-mark">A</span>ABLE <em>2.0</em></a>
<select id="chapter-picker" aria-label="Jump to chapter"><option value="">Chapters</option>{options}</select>
<button id="details-toggle" type="button">Open every drawer</button>
<a class="gh" href="{REPO}">GitHub ↗</a>
</nav></header>
<nav class="rail" aria-label="Chapters"><span class="rail-track"><span class="rail-fill"></span></span>{rail}</nav>
<main id="top">
<section class="hero">
<div class="hero-copy">
<p class="kicker">Custom Able · Unreal Engine 5.8</p>
<h1><span class="h1-able">Able</span><span class="h1-gen">Generation 2.0</span></h1>
<p class="tagline">{esc(tagline)}</p>
<p class="lede">{lede}</p>
<p class="cta"><a class="button primary" href="#{chapters[0][0]}">Start the tour</a><a class="button" href="{REPO}">View on GitHub</a></p>
<p class="built">{built_on}</p>
</div>
{hero_art()}
</section>
<section class="cards" aria-label="Chapters">{cards}</section>
<aside class="howto">{"".join(f"<p>{n}</p>" for n in notes)}</aside>
{"".join(rendered)}
</main>
<footer class="foot"><div><b>Able · Generation 2.0</b> · captured in Unreal Engine 5.8, 11–12 October 2026</div><div>Click any screenshot to enlarge; arrow keys step through them. <a href="{REPO}">Showcase repository</a> · <a href="{SITE}">Website</a></div></footer>
<dialog id="viewer" aria-label="Enlarged screenshot"><button type="button" class="close" aria-label="Close">✕</button><figure><img alt=""><figcaption></figcaption></figure><button type="button" class="nav prev" aria-label="Previous image">‹</button><button type="button" class="nav next" aria-label="Next image">›</button></dialog>
<script src="site.js"></script>
</body>
</html>
'''
open(site + "/index.html", "w", encoding="utf-8", newline="\n").write(page)
print("chapters", len(chapters), "sections", len(rendered))
