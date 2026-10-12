# Builds the showcase website (index.html) from README.md: the content is the README's, rendered; the page around it is this file's, with style.css and site.js.
# Needs Python-Markdown 3.7: python -m pip install markdown==3.7, then python build.py
import sys, re, math, html as htmllib, markdown

site = sys.argv[1] if len(sys.argv) > 1 else "."
md = open(site + "/README.md", encoding="utf-8").read().replace("\r\n", "\n").replace("<details>\n", '<details markdown="1">\n')
body = markdown.markdown(md, extensions=["tables", "toc", "md_in_html"], output_format="xhtml")

REPO = "https://github.com/GamesAndBacon/able-generation-2-showcase"
SITE = "https://gamesandbacon.github.io/able-generation-2-showcase/"
REVISION = (re.search(r"revision \*\*`([0-9a-f]+)`\*\*", md) or re.search(r"(x)", "x")).group(1)

def strip(s):
    return htmllib.unescape(re.sub(r"<[^>]+>", "", s)).strip()

def esc(s):
    return htmllib.escape(s, quote=True)

# ---- Content touches -----------------------------------------------------------------------------------------------------------

# Image pairs (a table of images over captions) become plates side by side.
def gallery(m):
    images = re.findall(r'<td style="text-align: center;">(<img [^>]*/>)</td>', m.group(1))
    captions = re.findall(r'<td style="text-align: center;">(.*?)</td>', m.group(2))
    if not images or len(images) != len(captions):
        return m.group(0)
    return '<div class="plates">' + "".join('<figure class="plate">%s<figcaption>%s</figcaption></figure>' % ic for ic in zip(images, captions)) + "</div>"
NOT_TABLE_END = r"(?:(?!</table>).)*?"
body = re.sub(r"<table>\n<thead>\n" + NOT_TABLE_END + r"</thead>\n<tbody>\n<tr>\n((?:<td style=\"text-align: center;\"><img [^>]*/></td>\n)+)</tr>\n<tr>\n((?:<td style=\"text-align: center;\">.*?</td>\n)+)</tr>\n</tbody>\n</table>",
              gallery, body, flags=re.S)

# A screenshot and its caption become a plate.
body = re.sub(r"<p>(<img [^>]*/>)</p>\n<p><em>(.*?)</em></p>", r'<figure class="plate">\1<figcaption>\2</figcaption></figure>', body)
body = re.sub(r"<p>(<img [^>]*/>)</p>", r'<figure class="plate">\1</figure>', body)

# Code directories read as parts lists.
body = re.sub(r"<p><strong>Code directory</strong>(.*?)</p>\n<table>", r'<p class="parts-heading"><span>Parts list</span>\1</p>\n<table class="parts">', body)

# Look closer: a specification you can open.
body = body.replace("<details>\n<summary>", '<details class="spec">\n<summary><span class="spec-toggle" aria-hidden="true"></span>')

# ---- Sections ------------------------------------------------------------------------------------------------------------------

parts = re.split(r'<p><a name="([^"]+)"></a></p>\n', body)
intro, sections = parts[0], list(zip(parts[1::2], parts[2::2]))

intro_paras = re.findall(r"<p>(.*?)</p>", intro, flags=re.S)
tagline = next((strip(p) for p in intro_paras if p.startswith("<strong>") and p.endswith("</strong>") and "href" not in p), "")
lede = next((p for p in intro_paras if not p.startswith("<strong>") and not p.startswith("<a ") and not p.startswith("<img") and "Generation 2.0" not in p), "")
built_on = next((p for p in intro_paras if "Generation 2.0" in p and "names" in p), "")
notes = [p for p in intro_paras if "Look closer" in p]

def number_plates(content, label):
    # FIG. 01.1, 01.2...: each plate in the chapter, in order.
    count = 0
    def repl(m):
        nonlocal count
        count += 1
        return f'<figure class="plate"><span class="fig-no">Fig. {label}.{count}</span>'
    return re.sub(r'<figure class="plate">', repl, content), count

chapters, rendered = [], []
for name, content in sections:
    m = re.search(r'<h2 id="[^"]*">(\d+) · (.*?)</h2>\n', content)
    h = m or re.search(r'<h2 id="[^"]*">(.*?)</h2>\n', content)
    tag = re.search(r"<p><strong>(.*?)</strong></p>\n", content)
    if not h:
        rendered.append(f'<section class="notes" id="{name}">{content}</section>')
        continue
    number = m.group(1) if m else "00"
    title = m.group(2) if m else h.group(1)
    subtitle = tag.group(1) if tag and tag.start() < h.end() + 40 else ""
    content = content[:h.start()] + content[h.end():]
    if subtitle:
        content = content.replace(tag.group(0), "", 1)
    content, figures = number_plates(content, number)
    files = sum(len(re.findall(r"<tr>\n<td", t)) for t in re.findall(r'<table class="parts">(.*?)</table>', content, re.S))
    chapters.append((name, number, strip(title), strip(subtitle), figures, files))
    margin = (f'<div class="margin"><span class="sec">§</span><span class="big">{number}</span>'
              f'<dl><dt>Figures</dt><dd>{figures}</dd><dt>Source files</dt><dd>{files}</dd></dl></div>')
    head = f'<header class="chapter-head"><p class="runner">Chapter {number}</p><h2>{title}</h2>' + (f'<p class="subtitle">{subtitle}</p>' if subtitle else "") + "</header>"
    rendered.append(f'<section class="chapter" id="{name}">{margin}<div class="chapter-main">{head}{content}</div></section>')

toc = "".join(
    f'<li><a href="#{name}"><span class="n">{number}</span><span class="t">{esc(title)}</span><span class="leader" aria-hidden="true"></span><span class="p">{figures} fig.</span></a><span class="s">{esc(sub)}</span></li>'
    for name, number, title, sub, figures, files in chapters)
total_figures = sum(c[4] for c in chapters)

# ---- The cover drawing: Ground Slam, plan and elevation, dimensioned ------------------------------------------------------------

def drawing():
    W, H = 760, 620
    cx, cy, R, r, dome = 300, 230, 170, 140, 46        # Plan: the ring (wave radius 450, width 60 at 1:2.65) and the dome.
    ey, eh = 520, 28                                   # Elevation: its baseline and the ring's height.
    L = []                                             # Lines, drawn in order.
    def line(x1, y1, x2, y2, cls="ink"):
        L.append(f'<line class="{cls}" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" pathLength="1"/>')
    def circle(x, y, rad, cls="ink"):
        L.append(f'<circle class="{cls}" cx="{x:.1f}" cy="{y:.1f}" r="{rad:.1f}" pathLength="1"/>')
    def text(x, y, s, cls="dim", anchor="middle"):
        L.append(f'<text class="{cls}" x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}">{s}</text>')

    # Plan view: ring, the convex pieces' joins, dome, the four fissures, centre marks.
    circle(cx, cy, R); circle(cx, cy, r); circle(cx, cy, dome)
    for i in range(24):
        a = 2 * math.pi * i / 24
        line(cx + math.cos(a) * r, cy + math.sin(a) * r, cx + math.cos(a) * R, cy + math.sin(a) * R, "thin")
    for a in (0.25, 1.82, 3.39, 4.96):
        ux, uy, px, py = math.cos(a), math.sin(a), -math.sin(a) * 7, math.cos(a) * 7
        for s in (1, -1):
            line(cx + ux * dome + px * s, cy + uy * dome + py * s, cx + ux * r + px * s, cy + uy * r + py * s, "thin")
    line(cx - R - 22, cy, cx + R + 22, cy, "centre"); line(cx, cy - R - 22, cx, cy + R + 22, "centre")
    # Diameter, below the ring.
    dy = cy + R + 34
    line(cx - R, cy + 6, cx - R, dy + 6, "ext"); line(cx + R, cy + 6, cx + R, dy + 6, "ext")
    line(cx - R, dy, cx + R, dy, "dimline")
    text(cx, dy - 7, "Ø 900")
    # Wave width, at the right.
    ay = cy - 62
    line(cx + r, ay, cx + R, ay, "dimline")
    text(cx + R + 10, ay + 4, "W 60", anchor="start")
    # Impact radius, a leader to the dome.
    lx, ly = cx + dome * math.cos(-2.3), cy + dome * math.sin(-2.3)
    line(lx, ly, lx - 70, ly - 52, "leader"); line(lx - 70, ly - 52, lx - 128, ly - 52, "leader")
    text(lx - 130, ly - 58, "R 120 · IMPACT", anchor="start")
    # The ring's full angle.
    L.append(f'<path class="dimline" d="M{cx + R + 26:.1f},{cy:.1f} A{R + 26},{R + 26} 0 0 0 {cx + (R + 26) * math.cos(-.9):.1f},{cy + (R + 26) * math.sin(-.9):.1f}" pathLength="1"/>')
    text(cx + (R + 40) * math.cos(-.45), cy + (R + 40) * math.sin(-.45), "360°", anchor="start")
    text(cx - R - 18, cy - R - 6, "PLAN", "label", "start")

    # Elevation: the ring's section (hatched), the dome, the height.
    text(cx - R - 18, ey - eh - 26, "ELEVATION", "label", "start")
    line(cx - R - 22, ey, cx + R + 22, ey, "centre")
    for x0 in (cx - R, cx + r):
        L.append(f'<rect class="section" x="{x0:.1f}" y="{ey - eh:.1f}" width="{R - r:.1f}" height="{eh:.1f}"/>')
    L.append(f'<path class="ink" d="M{cx - dome:.1f},{ey:.1f} A{dome},{dome * .9} 0 0 1 {cx + dome:.1f},{ey:.1f}" pathLength="1"/>')
    line(cx + R + 8, ey, cx + R + 30, ey, "ext"); line(cx + R + 8, ey - eh, cx + R + 30, ey - eh, "ext")
    line(cx + R + 24, ey, cx + R + 24, ey - eh, "dimline")
    text(cx + R + 32, ey - eh / 2 + 4, "H 50", anchor="start")

    # Title block.
    tx, ty, tw = 528, 22, 210
    rows = [("PART", "CS_GroundSlam"), ("BUILD", "28 hulls · 3 exact"), ("BOUNDS", "900 × 900 × 145"), ("UNITS", "cm"), ("REV", REVISION[:7])]
    L.append(f'<rect class="block" x="{tx}" y="{ty}" width="{tw}" height="{24 * (len(rows) + 1)}"/>')
    L.append(f'<text class="block-title" x="{tx + 10}" y="{ty + 17}">ABLE COLLISION ENGINE</text>')
    for i, (k, v) in enumerate(rows):
        y = ty + 24 * (i + 1)
        L.append(f'<line class="thin" x1="{tx}" y1="{y}" x2="{tx + tw}" y2="{y}"/>')
        L.append(f'<text class="block-key" x="{tx + 10}" y="{y + 16}">{k}</text><text class="block-val" x="{tx + 70}" y="{y + 16}">{esc(v)}</text>')
    L.append(f'<line class="thin" x1="{tx + 62}" y1="{ty + 24}" x2="{tx + 62}" y2="{ty + 24 * (len(rows) + 1)}"/>')

    lines = "".join(f'<g style="--i:{i}">{l}</g>' for i, l in enumerate(L))
    return (f'<svg class="drawing" viewBox="0 0 {W} {H}" role="img" aria-label="An engineering drawing of the Ground Slam Collision Shape: '
            f'a plan of its ring and dome dimensioned at 900 across, a 60 wide wave and a 120 impact radius, an elevation 50 high, and a title block.">'
            f'<rect class="sheet" x="1" y="1" width="{W - 2}" height="{H - 2}"/>{lines}</svg>')

# ---- The page --------------------------------------------------------------------------------------------------------------------

page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Able · Generation 2.0 — Field manual</title>
<meta name="description" content="A field manual for custom Able on Unreal Engine 5.8: collision shapes you author visually, multiple phases, reactive gameplay, persistent state and weapon integration.">
<meta property="og:title" content="Able · Generation 2.0">
<meta property="og:description" content="{esc(tagline)}">
<meta name="color-scheme" content="light dark">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&family=IBM+Plex+Mono:wght@400;500;600&family=Source+Serif+4:ital,opsz,wght@0,8..60,400..700;1,8..60,400..600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="bar"><nav aria-label="Showcase">
<a class="mark" href="#top">ABLE<span>/</span>2.0</a>
<a class="where" href="#contents"><span class="where-n">—</span><span class="where-t">Contents</span></a>
<button id="specs-toggle" type="button">Open all specs</button>
<a class="gh" href="{REPO}">Source ↗</a>
</nav></header>
<main id="top">
<section class="cover">
<div class="docline"><span>Doc. AB-2.0</span><span>Field manual · Unreal Engine 5.8</span><span>Rev. {REVISION[:7]}</span><span>12 · 10 · 2026</span></div>
<div class="cover-grid">
<div class="cover-copy">
<h1><span class="h1-a">Able</span><span class="h1-b">Generation 2.0</span></h1>
<p class="tagline">{esc(tagline)}</p>
<p class="lede">{lede}</p>
<p class="built">{built_on}</p>
<p class="cta"><a href="#contents">Read the contents</a><a href="{REPO}">View the source repository</a></p>
</div>
<figure class="drawing-wrap">{drawing()}<figcaption><span class="fig-no">Fig. 00</span> Ground Slam, one of the project's Collision Shapes, as the Shape Preview measures it.</figcaption></figure>
</div>
</section>
<section class="contents" id="contents">
<h2 class="contents-title">Contents</h2>
<ol class="toc">{toc}</ol>
<div class="howto">{"".join(f"<p>{n}</p>" for n in notes)}<p>{len(chapters)} chapters · {total_figures} figures.</p></div>
</section>
{"".join(rendered)}
</main>
<footer class="foot"><span>Able · Generation 2.0 — captured in Unreal Engine 5.8, 11–12 October 2026.</span><span>Click a figure to enlarge it; arrow keys step through them. <a href="{REPO}">Repository</a></span></footer>
<dialog id="viewer" aria-label="Enlarged figure"><button type="button" class="close" aria-label="Close">Close</button><figure><img alt=""><figcaption></figcaption></figure><button type="button" class="nav prev" aria-label="Previous figure">←</button><button type="button" class="nav next" aria-label="Next figure">→</button></dialog>
<script src="site.js"></script>
</body>
</html>
'''
open(site + "/index.html", "w", encoding="utf-8", newline="\n").write(page)
print("chapters", len(chapters), "figures", total_figures, "rev", REVISION[:7])
