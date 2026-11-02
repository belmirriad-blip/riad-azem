import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from marks import *
from shapely.geometry import Polygon, LineString
from shapely import affinity
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_HTML = sys.argv[1]
OUT_SVG = sys.argv[2]
os.makedirs(OUT_SVG, exist_ok=True)

BONE, NIGHT, DUNE, SAND, ASH, EMBER = '#F1EBE0', '#15120F', '#4A3326', '#D6C3A1', '#8A8580', '#C4502A'

# ---------------------------------------------------------------- mark
raw = clean(final(), s=0.08)
minx, miny, maxx, maxy = raw.bounds
SC = 100 / (maxy - miny)
def same_norm(g):
    g = affinity.translate(g, -minx, -miny)
    return affinity.scale(g, SC, SC, origin=(0, 0))
MARK = same_norm(raw)
MW = MARK.bounds[2]                       # ~72.4 wide, 100 tall
COUNTER = Polygon(MARK.interiors[0])
X = COUNTER.bounds[3] - COUNTER.bounds[1] # clear-space unit = counter height
MARK_D = to_path(MARK)
# accent hairline: the counter's own contour, inset
hair = COUNTER.buffer(-5.5, join_style=2, mitre_limit=5).simplify(0.1).exterior
HAIR_D = 'M' + ' L'.join(f'{x:.2f},{y:.2f}' for x, y in list(hair.coords)[:-1]) + 'Z'

def mark(fill, tx=0, ty=0, s=1, accent=False):
    g = f'<path fill="{fill}" d="{MARK_D}"/>'
    if accent:
        g += f'<path fill="none" stroke="{EMBER}" stroke-width="1.1" stroke-linejoin="miter" d="{HAIR_D}"/>'
    return f'<g transform="translate({tx:.2f},{ty:.2f}) scale({s:.4f})">{g}</g>'

# construction strokes (same transform as the mark)
def strokes_parts():
    import marks as M
    W, A = M.W, M.A
    L = bez((48,5),(22,10),(12,30),(13,50),30)[:-1] + bez((13,50),(14,72),(24,90),(47,95),30)
    R = [(45,6),(62,13),(71,26),(71,70),(64,84),(44,95)]
    Rd = [p for a,b in zip(R,R[1:]) for p in [(a[0]+(b[0]-a[0])*t/8, a[1]+(b[1]-a[1])*t/8) for t in range(8)]]+[R[-1]]
    ls = same_norm(stroke(L, W, A).simplify(0.08)); rs = same_norm(stroke(Rd, W, A).simplify(0.08))
    tf = lambda pts: [((x-minx)*SC, (y-miny)*SC) for x, y in pts]
    return ls, rs, tf(L), tf(R)
LS, RS, LSK, RSK = strokes_parts()
def poly_d(pts): return 'M' + ' L'.join(f'{x:.2f},{y:.2f}' for x, y in pts)

# ---------------------------------------------------------------- wordmark (Archivo 800, outlined)
font = TTFont(os.path.join(HERE, '../fonts/archivo800.ttf'))
gs = font.getGlyphSet(); cmap = font.getBestCmap()
UPM = font['head'].unitsPerEm; CAP = font['OS/2'].sCapHeight
def wordmark_path(text='OSTRO', track=0.35):
    x = 0; ds = []; first_l = None; last_r = 0
    for i, ch in enumerate(text):
        gname = cmap[ord(ch)]; gl = gs[gname]
        bp = BoundsPen(gs); gl.draw(bp); bx0, by0, bx1, by1 = bp.bounds
        if first_l is None: first_l = bx0
        sp = SVGPathPen(gs)
        tp = TransformPen(sp, (1, 0, 0, -1, x - first_l, CAP))
        gl.draw(tp); ds.append(sp.getCommands())
        last_r = x - first_l + bx1
        x += gl.width + (track * UPM if i < len(text) - 1 else 0)
    return ''.join(ds), last_r      # units: font units, cap top at 0, baseline at CAP
WM_D, WM_W = wordmark_path()
def wordmark(fill, tx, ty, cap_h):
    s = cap_h / CAP
    return f'<path fill="{fill}" transform="translate({tx:.2f},{ty:.2f}) scale({s:.5f})" d="{WM_D}"/>', WM_W * s

# ---------------------------------------------------------------- lockup builders (return svg, w, h)
def guide_box(x0, y0, w, h, pad, col):
    return (f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{w:.1f}" height="{h:.1f}" fill="none" stroke="{col}" stroke-width="1" stroke-opacity=".7"/>'
            f'<rect x="{x0-pad:.1f}" y="{y0-pad:.1f}" width="{w+2*pad:.1f}" height="{h+2*pad:.1f}" fill="none" stroke="{col}" stroke-width="1" stroke-dasharray="4 4"/>'
            f'<g stroke="{col}" stroke-width="1"><line x1="{x0+w/2:.1f}" y1="{y0-pad:.1f}" x2="{x0+w/2:.1f}" y2="{y0:.1f}"/><line x1="{x0+w/2-4:.1f}" y1="{y0-pad:.1f}" x2="{x0+w/2+4:.1f}" y2="{y0-pad:.1f}"/><line x1="{x0+w/2-4:.1f}" y1="{y0:.1f}" x2="{x0+w/2+4:.1f}" y2="{y0:.1f}"/>'
            f'<line x1="{x0-pad:.1f}" y1="{y0+h/2:.1f}" x2="{x0:.1f}" y2="{y0+h/2:.1f}"/><line x1="{x0-pad:.1f}" y1="{y0+h/2-4:.1f}" x2="{x0-pad:.1f}" y2="{y0+h/2+4:.1f}"/><line x1="{x0:.1f}" y1="{y0+h/2-4:.1f}" x2="{x0:.1f}" y2="{y0+h/2+4:.1f}"/></g>'
            f'<g font-family="IBM Plex Mono,monospace" font-size="{max(9,pad*0.16):.1f}" fill="{col}"><text x="{x0+w/2+6:.1f}" y="{y0-pad/2+3:.1f}">x</text><text x="{x0-pad/2:.1f}" y="{y0+h/2-6:.1f}" text-anchor="middle">x</text></g>')

def primary(fg, guides=None, scale=1.0):
    mh = 100 * scale; cap = 27 * scale; gap = 30 * scale
    s = cap / CAP; ww = WM_W * s
    W = max(ww, MW * scale); pad = X * scale if guides else 0
    x0, y0 = pad, pad
    body = mark(fg, x0 + (W - MW*scale)/2, y0, scale)
    wm, _ = wordmark(fg, x0 + (W - ww)/2, y0 + mh + gap, cap)
    H = mh + gap + cap
    g = guide_box(x0, y0, W, H, pad, guides) if guides else ''
    return g + body + wm, W + 2*pad, H + 2*pad

def horizontal(fg, guides=None, scale=1.0):
    mh = 64 * scale; cap = 22 * scale; gap = 26 * scale
    s = cap / CAP; ww = WM_W * s; mw = MW * 0.64 * scale
    W = mw + gap + ww; H = mh; pad = X * 0.64 * scale if guides else 0
    x0, y0 = pad, pad
    body = mark(fg, x0, y0, 0.64*scale)
    wm, _ = wordmark(fg, x0 + mw + gap, y0 + (mh - cap)/2, cap)
    g = guide_box(x0, y0, W, H, pad, guides) if guides else ''
    return g + body + wm, W + 2*pad, H + 2*pad

def svg(inner, w, h, label, cls='', style=''):
    c = f' class="{cls}"' if cls else ''
    st = f' style="{style}"' if style else ''
    return f'<svg{c}{st} viewBox="0 0 {w:.1f} {h:.1f}" role="img" aria-label="{label}">{inner}</svg>'

def standalone(inner, w, h):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.1f} {h:.1f}" width="{w:.1f}" height="{h:.1f}">{inner}</svg>\n'

def app_icon(bg=NIGHT, fg=BONE, size=200, rx=44, accent=False):
    s = size * 0.62 / 100
    inner = f'<rect width="{size}" height="{size}" rx="{rx}" fill="{bg}"/>' + mark(fg, (size - MW*s)/2, (size - 100*s)/2, s, accent)
    return inner, size, size

# ---------------------------------------------------------------- hoodie (flat front)
def hoodie(body, panel, logo, uid, notes=False, rib_line=ASH):
    # body ~200 units wide = ~60 cm pit to pit -> 1 cm = 3.33 units ; 6 cm = 20 units
    dk = 'fill-opacity=".22"'
    p = []
    # hood (back) + sleeves
    p.append(f'<path fill="{body}" d="M146,104 C142,46 172,22 200,22 C228,22 258,46 254,104 Z"/>')
    p.append(f'<path fill="{NIGHT}" {dk} d="M160,104 C158,62 178,42 200,42 C222,42 242,62 240,104 Z"/>')
    for sx in (1, -1):
        t = (lambda x: x) if sx == 1 else (lambda x: 400 - x)
        p.append(f'<path fill="{body}" d="M{t(102)},100 L{t(70)},108 C{t(58)},112 {t(52)},122 {t(50)},134 L{t(30)},300 L{t(76)},305 L{t(102)},192 Z"/>')
        # curved contrast panel running down the underside of the sleeve into the side
        p.append(f'<path fill="{panel}" d="M{t(102)},150 C{t(86)},200 {t(72)},250 {t(64)},303 L{t(76)},305 L{t(102)},192 Z"/>')
        p.append(f'<path fill="{body}" d="M{t(30)},300 L{t(76)},305 L{t(73)},333 L{t(27)},328 Z"/>')
        for k in range(1, 8):
            xa = 30 + 46*k/8; xb = 27 + 46*k/8
            p.append(f'<line x1="{t(xa):.1f}" y1="{300+5*k/8:.1f}" x2="{t(xb):.1f}" y2="{328+5*k/8:.1f}" stroke="{rib_line}" stroke-opacity=".45" stroke-width=".8"/>')
    # body
    p.append(f'<path fill="{body}" d="M102,96 L150,86 C170,100 230,100 250,86 L298,96 L302,334 L98,334 Z"/>')
    # curved side panels on the body
    p.append(f'<path fill="{panel}" d="M101,128 C138,170 150,262 134,334 L98,334 Z"/>')
    p.append(f'<path fill="{panel}" d="M299,128 C262,170 250,262 266,334 L302,334 Z"/>')
    # hood front edges + neckline
    p.append(f'<path fill="none" stroke="{NIGHT}" stroke-opacity=".35" stroke-width="1.2" d="M150,86 C160,112 186,122 200,124 C214,122 240,112 250,86"/>')
    # pocket
    p.append(f'<path fill="none" stroke="{rib_line}" stroke-width="1" stroke-dasharray="3 3" d="M142,252 L258,252 L274,334 M142,252 L126,334"/>')
    # rib hem
    p.append(f'<rect x="98" y="334" width="204" height="30" fill="{body}"/>')
    p.append(f'<line x1="98" y1="334" x2="302" y2="334" stroke="{NIGHT}" stroke-opacity=".3" stroke-width="1.2"/>')
    for k in range(1, 34):
        x = 98 + 204*k/34
        p.append(f'<line x1="{x:.1f}" y1="336" x2="{x:.1f}" y2="362" stroke="{rib_line}" stroke-opacity=".45" stroke-width=".8"/>')
    # drop-shoulder seams
    p.append(f'<path fill="none" stroke="{NIGHT}" stroke-opacity=".3" stroke-width="1" d="M102,98 L102,192 M298,98 L298,192"/>')
    # chest monogram: 6 cm wide = 20 units, wearer's left chest
    cw = 20; s = cw / MW
    cx, cy = 236, 140
    p.append(mark(logo, cx, cy, s))
    if notes:
        a = ASH
        p.append(f'<g stroke="{a}" stroke-width=".8"><line x1="{cx}" y1="{cy-8}" x2="{cx+cw}" y2="{cy-8}"/><line x1="{cx}" y1="{cy-12}" x2="{cx}" y2="{cy-4}"/><line x1="{cx+cw}" y1="{cy-12}" x2="{cx+cw}" y2="{cy-4}"/></g>')
        p.append(f'<text x="{cx+cw/2}" y="{cy-15}" text-anchor="middle" font-family="IBM Plex Mono,monospace" font-size="9" letter-spacing="1" fill="{a}">6 CM</text>')
    return ''.join(p)

# ---------------------------------------------------------------- pencil sketches
SKETCH = [
    (textura,  'Textura',          'Reads as a typeface. Anyone could own it.'),
    (roundO,   'Round fraktur',    'Too soft. The pen disappears.'),
    (openO,    'Open head',        'Reads as a U at 32 px.'),
    (spur,     'Inner spur',       'A mark inside the counter. Ornament.'),
    (lozenge,  'Lozenge',          'A diamond, not an O.'),
    (wide,     'Wide dune',        'Turns into a zero on the chest.'),
    (heavy,    'Heavy nib',        'The counter fills in at 20 px.'),
    (final,    'Windward + slip face', 'Kept. Curved on one side, cut flat on the other.'),
]
def sketch_svg(i, fn, kept):
    g = norm(close(fn()) if fn is not openO else fn())
    if fn is final: g = MARK
    w = g.bounds[2]; s = 1.0
    if w > 80: s = 80 / w
    g = affinity.scale(g, s, s, origin=(0, 0))
    w = g.bounds[2]; h = g.bounds[3]
    ox, oy = (120 - w)/2, (130 - h)/2
    d = to_path(g)
    flt = f'pencil{i}'
    out = [f'<defs><filter id="{flt}" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="{i+3}" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="1.8"/></filter></defs>']
    out.append(f'<rect width="120" height="130" fill="{BONE}"/>')
    out.append(f'<g stroke="{ASH}" stroke-width=".4" stroke-dasharray="2 3" fill="none"><line x1="6" y1="{oy:.1f}" x2="114" y2="{oy:.1f}"/><line x1="6" y1="{oy+h:.1f}" x2="114" y2="{oy+h:.1f}"/></g>')
    passes = [(0.3, 0.6, 0.9, 1.0, 0.3), (-0.8, 0.4, 0.45, 0.55, -0.5), (0.9, -0.5, 0.35, 0.5, 0.6)]
    out.append(f'<g filter="url(#{flt})" transform="translate({ox:.2f},{oy:.2f})">')
    if kept:
        out.append(f'<path d="{d}" fill="{NIGHT}" fill-opacity=".1"/>')
    for dx, dy, op, sw, rot in passes:
        out.append(f'<path d="{d}" fill="none" stroke="{NIGHT}" stroke-opacity="{op}" stroke-width="{sw}" transform="translate({dx},{dy}) rotate({rot} {w/2:.1f} {h/2:.1f})"/>')
    out.append('</g>')
    if kept:
        out.append(f'<ellipse cx="60" cy="65" rx="52" ry="60" fill="none" stroke="{EMBER}" stroke-width="1.4" filter="url(#{flt})" transform="rotate(-6 60 65)"/>')
    else:
        out.append(f'<path d="M14,118 L106,14" stroke="{NIGHT}" stroke-opacity=".55" stroke-width="1.1" filter="url(#{flt})"/>')
    return f'<svg viewBox="0 0 120 130" role="img" aria-label="Pencil sketch: {SKETCH[i][1]}">' + ''.join(out) + '</svg>'

# ---------------------------------------------------------------- contrast
def lum(h):
    c = [int(h[i:i+2], 16)/255 for i in (1, 3, 5)]
    c = [x/12.92 if x <= 0.03928 else ((x+0.055)/1.055)**2.4 for x in c]
    return 0.2126*c[0] + 0.7152*c[1] + 0.0722*c[2]
def cr(a, b):
    la, lb = sorted([lum(a), lum(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)

# ================================================================ assemble
H = []
A = H.append

# ---------- cover
pl, pw, ph = primary(BONE, scale=1.0)
A(f'''<section class="panel cover" aria-label="OSTRO">
 {svg(pl, pw, ph, 'OSTRO primary lockup', 'cv')}
 <p class="tag">Menswear · Béchar, Algeria</p>
</section>''')

# ---------- story
A(f'''<section class="panel story">
 <p class="eyebrow">Story</p>
 <h2>Named after the wind that leaves the Sahara.</h2>
 <div class="storytext">
 <p>Ostro is the warm south wind that carries Sahara dust north over the sea. OSTRO starts where that wind starts: in Béchar, at the edge of the desert.</p>
 <p>We make heavyweight, boxy menswear. The first piece is one cut-and-sew hoodie with curved contrast side panels, sewn to order by the founder's mother and delivered across Algeria, cash on delivery.</p>
 </div>
 <dl class="facts">
  <div><dt>For</dt><dd>Young men, 17–28, into streetwear</dd></div>
  <div><dt>Mood</dt><dd>Desert at dusk. Calm, heavy, warm.</dd></div>
  <div><dt>Delivery</dt><dd>58 wilayas · paiement à la livraison</dd></div>
 </dl>
</section>''')

# ---------- mark: idea
ls_d, rs_d = to_path(LS), to_path(RS)
def part(d, fill, sk, label):
    pad = 14
    inner = (f'<g transform="translate({pad},{pad})"><path fill="{fill}" d="{d}"/>'
             f'<path d="{poly_d(sk)}" fill="none" stroke="{BONE}" stroke-width=".7" stroke-dasharray="2 2" stroke-opacity=".8"/></g>')
    return f'<figure>{svg(inner, MW + 2*pad, 100 + 2*pad, label)}<figcaption>{label}</figcaption></figure>'
fin = f'<figure>{svg(mark(BONE, 14, 14), MW + 28, 128, "OSTRO mark")}<figcaption>The OSTRO mark</figcaption></figure>'
A(f'''<section class="panel dark">
 <p class="eyebrow">Mark · The idea</p>
 <h2>Two pen strokes, shaped like a dune.</h2>
 <p class="lead">A dune has two sides: the windward side, long and curved, and the slip face, short and steep. The O is drawn the same way with a flat pen held at 38°. The left stroke is one continuous curve. The right stroke is cut into flat facets, the way blackletter is. Nothing runs through the counter and nothing sticks out.</p>
 <div class="eq">
  {part(ls_d, ASH, LSK, 'Windward stroke')}<span class="op">+</span>
  {part(rs_d, ASH, RSK, 'Slip-face stroke')}<span class="op">=</span>
  {fin}
 </div>
</section>''')

# ---------- mark: sketches
cells = ''.join(f'<figure class="sk{" kept" if fn is final else ""}">{sketch_svg(i, fn, fn is final)}<figcaption><b>{String}</b>{note}</figcaption></figure>'
                for i, (fn, String, note) in enumerate(SKETCH))
A(f'''<section class="panel paper">
 <p class="eyebrow">Mark · Sketches</p>
 <h2>Eight Os on the way to the dune</h2>
 <p class="lead">Every version was drawn with the same pen and the same angle, then tested at 32 and 20 pixels. A plain textura O looked like any gothic font. The round one lost the pen. The open head, the lozenge and the inner spur stopped reading as an O. The curved-and-cut version kept its counter open at small sizes and looks like nothing else.</p>
 <div class="sketches">{cells}</div>
</section>''')

# ---------- mark: geometry
gl = []
for x in range(-20, 101, 10): gl.append(f'<line x1="{x}" y1="-24" x2="{x}" y2="124"/>')
for y in range(-20, 121, 10): gl.append(f'<line x1="-24" y1="{y}" x2="96" y2="{y}"/>')
cy0, cy1 = COUNTER.bounds[1], COUNTER.bounds[3]
nib = 19 * SC
na = math.radians(38)
nx, ny = 84, -12
geo = (f'<g stroke="{ASH}" stroke-opacity=".35" stroke-width=".3">{"".join(gl)}</g>'
       f'<path fill="{BONE}" fill-opacity=".94" d="{MARK_D}"/>'
       f'<g stroke="{ASH}" stroke-width=".5" fill="none"><line x1="-24" y1="0" x2="96" y2="0"/><line x1="-24" y1="100" x2="96" y2="100"/>'
       f'<line x1="-24" y1="{cy0:.2f}" x2="96" y2="{cy0:.2f}" stroke-dasharray="1.5 1.5"/><line x1="-24" y1="{cy1:.2f}" x2="96" y2="{cy1:.2f}" stroke-dasharray="1.5 1.5"/></g>'
       f'<g stroke="{EMBER}" stroke-width=".7"><line x1="-12" y1="{cy0:.2f}" x2="-12" y2="{cy1:.2f}"/><line x1="-15" y1="{cy0:.2f}" x2="-9" y2="{cy0:.2f}"/><line x1="-15" y1="{cy1:.2f}" x2="-9" y2="{cy1:.2f}"/></g>'
       f'<text x="-17" y="{(cy0+cy1)/2+2:.1f}" font-family="IBM Plex Mono,monospace" font-size="5" fill="{EMBER}" text-anchor="end">x</text>'
       f'<line x1="{nx - nib/2*math.cos(na):.2f}" y1="{ny + nib/2*math.sin(na):.2f}" x2="{nx + nib/2*math.cos(na):.2f}" y2="{ny - nib/2*math.sin(na):.2f}" stroke="{BONE}" stroke-width="2.2"/>'
       f'<g font-family="IBM Plex Mono,monospace" font-size="3.6" letter-spacing=".5" fill="{BONE}" fill-opacity=".8">'
       f'<text x="-22" y="-2">CAP</text><text x="-22" y="105">BASELINE</text><text x="74" y="-1">NIB 38°</text>'
       f'<text x="-22" y="{cy0-1.5:.1f}">COUNTER</text></g>')
A(f'''<section class="panel dark geo">
 <div class="geotext"><p class="eyebrow">Mark · Geometry</p>
 <h2>One pen, one angle, one unit</h2>
 <p class="lead">The pen is {nib:.0f} units wide on a 100-unit cap height, held at 38°. That angle makes the strokes thin where they meet at the head and the foot and heavy down the sides. The height of the counter is the unit <b>x</b>: it sets the clear space around every lockup.</p>
 <ul class="specs"><li><span>Cap height</span>100</li><li><span>Width</span>{MW:.0f}</li><li><span>Pen</span>{nib:.0f} at 38°</li><li><span>Counter x</span>{X:.0f}</li></ul></div>
 {svg(geo, 0, 0, 'Mark construction grid').replace('viewBox="0 0 0.0 0.0"', 'viewBox="-26 -26 124 152"')}
</section>''')

# ---------- mark: versions + sizes
def tile_mark(bg, fg, cap, accent=False, cls='t-bone'):
    return f'<div class="tile {cls}">{svg(mark(fg, 8, 8, 1, accent), MW + 16, 116, "OSTRO mark " + cap, "mk")}<span class="cap">{cap}</span></div>'
sizes = ''.join(f'<div>{svg(mark(NIGHT, 2, 2), MW + 4, 104, "OSTRO mark at " + str(h) + " px", "", f"height:{h}px;width:auto")}<small>{h} px</small></div>' for h in (96, 48, 32, 20))
A(f'''<section class="panel">
 <p class="eyebrow">Mark · Versions</p>
 <h2>Three versions, nothing else</h2>
 <p class="lead">Night on Bone and Bone on Night cover almost everything. The accent version adds one Ember hairline that follows the inside of the counter. It is for the hang tag only.</p>
 <div class="suite three">
  {tile_mark(BONE, NIGHT, 'Night on Bone')}
  {tile_mark(NIGHT, BONE, 'Bone on Night', cls='t-night')}
  {tile_mark(BONE, NIGHT, 'Accent · hang tag only', True)}
 </div>
 <div class="sizes" aria-label="Small size test">{sizes}</div>
</section>''')

# ---------- lockups
def lock_tile(content, w, h, label, cls, cap, wide=False):
    return f'<div class="tile {cls}{" wide" if wide else ""}">{svg(content, w, h, label, "lk")}<span class="cap">{cap}</span></div>'
p1 = primary(NIGHT, guides=ASH); p2 = primary(BONE, guides=ASH)
h1 = horizontal(NIGHT, guides=ASH); h2 = horizontal(BONE, guides=ASH)
def icon_guides(bg, fg):
    inner, w, h = app_icon(bg, fg)
    pad = 30
    return (f'<rect x="{pad}" y="{pad}" width="{w}" height="{h}" rx="44" fill="{bg}"/>'
            f'<g transform="translate({pad},{pad})">{inner[inner.index("<g"):]}</g>'
            f'<rect x="4" y="4" width="{w+2*pad-8}" height="{h+2*pad-8}" fill="none" stroke="{ASH}" stroke-dasharray="4 4"/>'), w + 2*pad, h + 2*pad
i1 = icon_guides(NIGHT, BONE); i2 = icon_guides(NIGHT, BONE)
def chest_tile(body, panel):
    return hoodie(body, panel, BONE, 'c', notes=True)
A(f'''<section class="panel">
 <p class="eyebrow">Lockups</p>
 <h2>The mark leads, the name follows</h2>
 <p class="lead">The wordmark is OSTRO in Archivo ExtraBold, always in capitals, tracked at 0.35em. In the primary lockup the mark sits centred above it. The dashed line is the clear space: one counter height, <b>x</b>, on every side. Nothing else goes inside it.</p>
 <div class="suite">
  {lock_tile(p1[0], p1[1], p1[2], 'Primary lockup on Bone', 't-bone', 'Primary · on Bone')}
  {lock_tile(p2[0], p2[1], p2[2], 'Primary lockup on Night', 't-night', 'Primary · on Night')}
  {lock_tile(h1[0], h1[1], h1[2], 'Horizontal lockup on Bone', 't-bone', 'Horizontal · on Bone')}
  {lock_tile(h2[0], h2[1], h2[2], 'Horizontal lockup on Night', 't-night', 'Horizontal · on Night')}
  <div class="tile t-bone">{svg(i1[0], i1[1], i1[2], 'Profile picture and app icon', 'ico')}<span class="cap">Profile / app icon · on Bone</span></div>
  <div class="tile t-night">{svg(i2[0].replace(f'stroke="{ASH}"', f'stroke="{ASH}"'), i2[1], i2[2], 'Profile picture and app icon on Night', 'ico')}<span class="cap">Profile / app icon · on Night</span></div>
  <div class="tile t-bone tall">{svg(chest_tile(NIGHT, ASH).replace(f'fill="{NIGHT}" fill-opacity=".22"', f'fill="{ASH}" fill-opacity=".25"'), 400, 380, 'Chest monogram on Night hoodie', 'hd')}<span class="cap">Chest · 6 cm, on Bone</span></div>
  <div class="tile t-night tall">{svg(chest_tile(DUNE, SAND), 400, 380, 'Chest monogram on Dune hoodie', 'hd')}<span class="cap">Chest · 6 cm, on Night</span></div>
 </div>
</section>''')

# ---------- palette
PAL = [('Bone', BONE, 'Ground', 60, 'Backgrounds, labels, packaging'),
       ('Night', NIGHT, 'Ink', 25, 'Logo, text, headers'),
       ('Dune', DUNE, 'Hero product', 8, 'Hero colourway body (with Sand)'),
       ('Sand', SAND, 'Hero panel', None, 'Hero colourway side panels'),
       ('Ash', ASH, 'Support', 5, 'Borders, stitch lines, small text, second colourway panels'),
       ('Ember', EMBER, 'Accent', 2, 'One detail per surface, never body text')]
sw = ''.join(f'<div class="sw"><div class="chip" style="background:{h}"></div><div class="swt"><b>{n}</b><code>{h}</code><span>{r} · {str(p)+"%" if p else "with Dune"}</span><small>{u}</small></div></div>' for n, h, r, p, u in PAL)
checks = [('Night on Bone', NIGHT, BONE, 'Body text', True), ('Bone on Night', BONE, NIGHT, 'Body text', True),
          ('Ash on Bone', ASH, BONE, 'Small labels only', None), ('Ember on Bone', EMBER, BONE, 'Never body copy', False),
          ('Bone on Dune', BONE, DUNE, 'Chest mark, tags', True), ('Night on Sand', NIGHT, SAND, 'Panels, labels', True)]
ct = ''.join(f'<div class="ck"><div class="ckc" style="background:{bg};color:{fg}">Aa</div><div><b>{n}</b><code>{cr(fg,bg):.1f} : 1</code><small class="{"ok" if ok else ("no" if ok is False else "mid")}">{u}</small></div></div>' for n, fg, bg, u, ok in checks)
A(f'''<section class="panel">
 <p class="eyebrow">Palette</p>
 <h2>Six colours, mostly Bone and Night</h2>
 <p class="lead">Bone is the ground, Night is the ink. Dune and Sand belong to the product. Ash does the quiet work. Ember appears once per surface: a thread, a dot, a hairline.</p>
 <div class="sws">{sw}</div>
 <div class="ratio" aria-label="Usage ratio">
  <i style="flex:60;background:{BONE}"></i><i style="flex:25;background:{NIGHT}"></i><i style="flex:5;background:{DUNE}"></i><i style="flex:3;background:{SAND}"></i><i style="flex:5;background:{ASH}"></i><i style="flex:2;background:{EMBER}"></i>
 </div>
 <p class="mono-s">60 · 25 · 8 (Dune + Sand) · 5 · 2</p>
 <h3 class="sub">Contrast check</h3>
 <div class="checks">{ct}</div>
</section>''')

# ---------- colourways
def mini_hoodie(body, panel):
    return svg(hoodie(body, panel, BONE, 'm'), 400, 380, 'Hoodie', 'hd')
A(f'''<section class="panel">
 <p class="eyebrow">Colourways</p>
 <h2>One cut. Two colours.</h2>
 <div class="cws">
  <div class="cw"><div class="pair"><div style="background:{DUNE}"><span>Dune<br>{DUNE}</span></div><div style="background:{SAND}"><span>Sand<br>{SAND}</span></div></div><div class="cwfig t-bone">{mini_hoodie(DUNE, SAND)}</div><p class="mono">Colourway 01 — Dune / Sand</p></div>
  <div class="cw"><div class="pair"><div style="background:{NIGHT}"><span>Night<br>{NIGHT}</span></div><div style="background:{ASH}"><span>Ash<br>{ASH}</span></div></div><div class="cwfig t-bone">{mini_hoodie(NIGHT, ASH).replace(f'fill="{NIGHT}" fill-opacity=".22"', f'fill="{ASH}" fill-opacity=".25"')}</div><p class="mono">Colourway 02 — Night / Ash</p></div>
 </div>
</section>''')

# ---------- typography
A(f'''<section class="panel">
 <p class="eyebrow">Typography</p>
 <h2>One family and one mono</h2>
 <p class="lead">Archivo does the talking, IBM Plex Mono does the labelling. Both are on Google Fonts. No script, no serif.</p>
 <div class="types">
  <article class="ty"><p class="eyebrow">Display · Archivo 700–800 · uppercase · wide</p><p class="sp-d">Heavyweight hoodie</p><p class="sp-al">ABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789</p><p class="why">Wordmark, headlines, section titles. Track 0.2–0.35em.</p></article>
  <article class="ty"><p class="eyebrow">Body · Archivo 400 · sentence case</p><p class="sp-b">Each hoodie is cut in Béchar and sewn after you order. It goes out to all 58 wilayas and you pay when it reaches you.</p><p class="why">Captions, product pages, messages. 15–17 px on screens.</p></article>
  <article class="ty"><p class="eyebrow">Labels · IBM Plex Mono 400–500 · uppercase · 0.12em</p><p class="sp-m">Size · M &nbsp;/&nbsp; Colourway 01 — Dune / Sand &nbsp;/&nbsp; Made in Algeria</p><p class="why">Sizes, prices, tags, care labels, order numbers.</p></article>
 </div>
</section>''')

# ---------- voice
A(f'''<section class="panel dark">
 <p class="eyebrow">Voice</p>
 <h2>Say what it is, then stop.</h2>
 <p class="lead">Short sentences. Weight, cut, colour, size, where it was sewn. No hype words, no emojis, no exclamation marks.</p>
 <ul class="lines"><li>Heavy. Boxy. Made to order.</li><li>Sewn by hand in Béchar.</li><li>One cut. Two colours.</li><li>Made in your size.</li></ul>
 <p class="eyebrow" style="margin-top:28px">Words OSTRO never uses</p>
 <ul class="never"><li>cheap</li><li>best quality</li><li>limited offer</li></ul>
</section>''')

# ---------- applications
# hang tag
tag = (f'<rect x="0" y="0" width="200" height="340" fill="{ASH}" fill-opacity="0"/>'
       f'<path d="M14,44 L58,12 H142 L186,44 V330 H14 Z" fill="{BONE}"/>'
       f'<circle cx="100" cy="40" r="8" fill="{NIGHT}"/>'
       f'<path d="M100,40 C112,8 150,-2 196,6" stroke="{EMBER}" stroke-width="1.6" fill="none"/>'
       f'<path d="M100,40 C94,20 76,6 56,2" stroke="{EMBER}" stroke-width="1.6" fill="none"/>'
       + mark(NIGHT, 100 - MW*0.62/2, 70, 0.62, accent=True) +
       f'<g font-family="IBM Plex Mono,monospace" font-weight="500" font-size="9.5" letter-spacing="1.1" fill="{NIGHT}" text-anchor="middle">'
       f'<text x="100" y="170">HEAVYWEIGHT HOODIE</text>'
       f'<text x="100" y="196" font-weight="400" font-size="7.6" letter-spacing=".7">COLOURWAY 01 — DUNE / SAND</text>'
       f'<text x="100" y="222">SIZE · M</text></g>'
       f'<line x1="30" y1="250" x2="170" y2="250" stroke="{ASH}" stroke-width="1.4" stroke-dasharray="6 4" stroke-linecap="round"/>'
       f'<text x="100" y="282" text-anchor="middle" font-family="IBM Plex Mono,monospace" font-size="9" letter-spacing="1.2" fill="{NIGHT}">MADE IN ALGERIA</text>'
       + wordmark(NIGHT, 100 - WM_W*(8/CAP)/2, 302, 8)[0])
# neck label
lab = [f'<rect width="300" height="120" fill="{NIGHT}"/>']
for y in range(3, 120, 3): lab.append(f'<line x1="0" y1="{y}" x2="300" y2="{y}" stroke="{BONE}" stroke-opacity=".05" stroke-width="1"/>')
lab.append(f'<path d="M0,0 h300 M0,120 h300" stroke="{ASH}" stroke-width="3" stroke-opacity=".6"/>')
lab.append(mark(BONE, 40, 30, 0.6))
wmt, wmw = wordmark(BONE, 98, 50, 18)
lab.append(wmt)
lab.append(f'<line x1="{98+wmw+20:.1f}" y1="40" x2="{98+wmw+20:.1f}" y2="80" stroke="{BONE}" stroke-opacity=".4"/>')
lab.append(f'<text x="{98+wmw+44:.1f}" y="68" text-anchor="middle" font-family="IBM Plex Mono,monospace" font-weight="500" font-size="20" fill="{BONE}">M</text>')
label_svg = ''.join(lab)
# instagram profile
ig = [f'<rect width="320" height="440" rx="18" fill="{BONE}"/>',
      f'<rect x=".5" y=".5" width="319" height="439" rx="18" fill="none" stroke="{ASH}" stroke-opacity=".5"/>',
      f'<text x="20" y="34" font-family="Archivo,sans-serif" font-weight="700" font-size="14" fill="{NIGHT}">ostro.dz</text>',
      f'<circle cx="56" cy="92" r="36" fill="{NIGHT}"/>', mark(BONE, 56 - MW*0.42/2, 71, 0.42),
      f'<g font-family="Archivo,sans-serif" fill="{NIGHT}" text-anchor="middle">'
      f'<text x="150" y="90" font-weight="700" font-size="15">9</text><text x="150" y="106" font-size="10.5">posts</text>'
      f'<text x="210" y="90" font-weight="700" font-size="15">—</text><text x="210" y="106" font-size="10.5">followers</text>'
      f'<text x="270" y="90" font-weight="700" font-size="15">—</text><text x="270" y="106" font-size="10.5">following</text></g>',
      f'<text x="20" y="152" font-family="Archivo,sans-serif" font-weight="800" font-size="13" letter-spacing="3.5" fill="{NIGHT}">OSTRO</text>',
      f'<g font-family="Archivo,sans-serif" font-size="11.5" fill="{NIGHT}"><text x="20" y="172">Heavy boxy hoodies. Made to order.</text><text x="20" y="189">Sewn in Béchar · Delivery 58 wilayas</text><text x="20" y="206">Paiement à la livraison</text></g>',
      f'<rect x="20" y="220" width="136" height="28" rx="7" fill="{NIGHT}"/><text x="88" y="238" text-anchor="middle" font-family="Archivo,sans-serif" font-weight="700" font-size="11" fill="{BONE}">Follow</text>',
      f'<rect x="164" y="220" width="136" height="28" rx="7" fill="none" stroke="{ASH}"/><text x="232" y="238" text-anchor="middle" font-family="Archivo,sans-serif" font-weight="700" font-size="11" fill="{NIGHT}">Message</text>']
for k, (lbl, inner) in enumerate([('Pièce 01', 'hood'), ('Tailles', 'S M L'), ('Avis', '“ ”')]):
    cx = 48 + k*70
    ig.append(f'<circle cx="{cx}" cy="292" r="26" fill="none" stroke="{ASH}" stroke-width="1"/><circle cx="{cx}" cy="292" r="22" fill="{NIGHT}"/>')
    if inner == 'hood':
        ig.append(f'<g transform="translate({cx-17},{292-16}) scale(.085)">{hoodie(DUNE, SAND, BONE, "h")}</g>')
    else:
        ig.append(f'<text x="{cx}" y="{296 if inner!="“ ”" else 302}" text-anchor="middle" font-family="IBM Plex Mono,monospace" font-size="{9 if inner!="“ ”" else 20}" letter-spacing="1" fill="{BONE}">{inner}</text>')
    ig.append(f'<text x="{cx}" y="334" text-anchor="middle" font-family="Archivo,sans-serif" font-size="10" fill="{NIGHT}">{lbl}</text>')
ig.append(f'<line x1="0" y1="350" x2="320" y2="350" stroke="{ASH}" stroke-opacity=".5"/>')
for k in range(3):
    x = 1 + k*106.3
    bg = [BONE, NIGHT, SAND][k]
    ig.append(f'<rect x="{x:.1f}" y="352" width="105" height="86" fill="{bg}"/>')
    if k == 0: ig.append(f'<g transform="translate({x+30:.1f},358) scale(.19)">{hoodie(DUNE, SAND, BONE, "p")}</g>' + mark(NIGHT, x + 6, 357, 0.1))
    if k == 1: ig.append(mark(BONE, x + 52.5 - MW*0.4/2, 375, 0.4))
    if k == 2: ig.append(f'<g transform="translate({x+30:.1f},358) scale(.19)">{hoodie(NIGHT, ASH, BONE, "q")}</g>')
ig_svg = ''.join(ig)
# shipping bag + sticker
bag = [f'<path d="M20,30 H280 V350 H20 Z" fill="{NIGHT}"/>',
       f'<path d="M20,30 H280 V58 H20 Z" fill="{NIGHT}"/><line x1="20" y1="58" x2="280" y2="58" stroke="{ASH}" stroke-opacity=".5" stroke-dasharray="3 3"/>']
bw = WM_W * (22/CAP)
bag.append(wordmark(BONE, 150 - bw/2, 180, 22)[0])
bag.append(f'<circle cx="150" cy="232" r="4" fill="{EMBER}"/>')
bag.append(f'<text x="150" y="326" text-anchor="middle" font-family="IBM Plex Mono,monospace" font-size="8.5" letter-spacing="1.5" fill="{BONE}" fill-opacity=".75">BÉCHAR → 58 WILAYAS</text>')
bag.append(f'<circle cx="250" cy="330" r="44" fill="{BONE}"/><circle cx="250" cy="330" r="38" fill="none" stroke="{ASH}" stroke-width=".8" stroke-dasharray="2 2"/>')
bag.append(mark(NIGHT, 250 - MW*0.42/2, 309, 0.42))
bag_svg = ''.join(bag)
# post template
post = [f'<rect width="300" height="300" fill="{BONE}"/>',
        f'<rect x="40" y="52" width="220" height="186" fill="none" stroke="{ASH}" stroke-dasharray="4 4"/>',
        f'<g transform="translate(66,58) scale(.42)">{hoodie(DUNE, SAND, BONE, "t")}</g>',
        f'<text x="48" y="232" font-family="IBM Plex Mono,monospace" font-size="7" letter-spacing="1" fill="{ASH}">PRODUCT PHOTO</text>',
        mark(NIGHT, 18, 16, 0.24),
        f'<text x="18" y="276" font-family="Archivo,sans-serif" font-size="15" fill="{NIGHT}">Sewn by hand in Béchar.</text>',
        f'<text x="282" y="276" text-anchor="end" font-family="IBM Plex Mono,monospace" font-size="8" letter-spacing="1" fill="{ASH}">01 / 09</text>']
post_svg = ''.join(post)

A(f'''<section class="panel">
 <p class="eyebrow">Applications</p>
 <h2>On the hoodie, in the bag, on the feed</h2>
 <div class="apps">
  <div class="app wide2"><div class="hoodies"><div>{svg(hoodie(DUNE, SAND, BONE, 'a1'), 400, 380, 'Hoodie, Dune with Sand panels', 'hd')}<span class="lbl">Colourway 01 · Dune / Sand</span></div><div>{svg(hoodie(NIGHT, ASH, BONE, 'a2').replace(f'fill="{NIGHT}" fill-opacity=".22"', f'fill="{ASH}" fill-opacity=".25"'), 400, 380, 'Hoodie, Night with Ash panels', 'hd')}<span class="lbl">Colourway 02 · Night / Ash</span></div></div><span class="lbl">Heavyweight hoodie · front</span></div>
  <div class="app dk">{svg(tag, 200, 340, 'Hang tag', 'tagsvg')}<span class="lbl">Hang tag</span></div>
  <div class="app">{svg(label_svg, 300, 120, 'Woven neck label', 'labsvg')}<span class="lbl">Woven neck label</span></div>
  <div class="app ig">{svg(ig_svg, 320, 440, 'Instagram profile', 'igsvg')}<span class="lbl">Instagram profile</span></div>
  <div class="app">{svg(bag_svg, 300, 380, 'Shipping bag and sticker', 'bagsvg')}<span class="lbl">Shipping bag + sticker</span></div>
  <div class="app">{svg(post_svg, 300, 300, 'Instagram post template', 'postsvg')}<span class="lbl">Post template</span></div>
 </div>
</section>''')

# ---------- don'ts
def dont(inner, cap, bg=BONE):
    x = f'<g stroke="{NIGHT}" stroke-width="3" stroke-linecap="round"><line x1="14" y1="14" x2="186" y2="146"/><line x1="186" y1="14" x2="14" y2="146"/></g>'
    return f'<figure class="dont"><svg viewBox="0 0 200 160" role="img" aria-label="{cap}"><rect width="200" height="160" fill="{bg}"/>{inner}{x}</svg><figcaption>{cap}</figcaption></figure>'
stretched = f'<g transform="translate(40,30) scale(1.7,1)">{mark(NIGHT, 0, 0, 1.0)}</g>'.replace('scale(1.7,1)', 'scale(1.65,1)')
stretched = f'<g transform="translate(40,32) scale(1.65,0.96)"><path fill="{NIGHT}" d="{MARK_D}"/></g>'
ember_all = (f'<rect width="200" height="160" fill="{EMBER}"/>' + mark(BONE, 100 - MW*0.8/2, 16, 0.8)
             + f'<rect x="20" y="104" width="160" height="40" fill="{BONE}"/><text x="100" y="129" text-anchor="middle" font-family="Archivo,sans-serif" font-size="11" fill="{EMBER}">Sewn by hand in Béchar.</text>')
busy = [f'<defs><pattern id="busy" width="24" height="24" patternUnits="userSpaceOnUse" patternTransform="rotate(28)"><rect width="24" height="24" fill="{SAND}"/><rect width="12" height="24" fill="{DUNE}"/><circle cx="18" cy="6" r="5" fill="{ASH}"/><rect y="16" width="24" height="4" fill="{EMBER}" fill-opacity=".7"/></pattern></defs>',
        f'<rect width="200" height="160" fill="url(#busy)"/>', mark(BONE, 100 - MW*1.1/2, 25, 1.1)]
grad = (f'<defs><linearGradient id="gr" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{EMBER}"/><stop offset="1" stop-color="{DUNE}"/></linearGradient>'
        f'<filter id="sh" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="6" dy="8" stdDeviation="4" flood-color="{NIGHT}" flood-opacity=".6"/></filter></defs>'
        f'<g filter="url(#sh)"><g transform="translate({100 - MW*1.1/2:.1f},25) scale(1.1)"><path fill="url(#gr)" d="{MARK_D}"/></g></g>')
A(f'''<section class="panel">
 <p class="eyebrow">Don'ts</p>
 <h2>Four ways to break it</h2>
 <div class="donts">
  {dont(stretched, "Don't stretch or squash the mark.")}
  {dont(ember_all, "Don't use Ember everywhere. One detail per surface.")}
  {dont(''.join(busy), "Don't put the mark on a busy photo or pattern.")}
  {dont(grad, "Don't add gradients, shadows or effects.")}
 </div>
</section>''')

A(f'''<section class="panel">
 <p class="eyebrow">Files</p>
 <h2>Vector files in the repo</h2>
 <p class="lead">Every logo is outlined SVG, so it prints and embroiders without the fonts installed. They are in <code>brand/ostro/svg/</code>.</p>
 <ul class="files"><li><code>ostro-mark-night.svg</code>, <code>-bone.svg</code>, <code>-accent.svg</code></li><li><code>ostro-primary-night.svg</code>, <code>-bone.svg</code></li><li><code>ostro-horizontal-night.svg</code>, <code>-bone.svg</code></li><li><code>ostro-wordmark-night.svg</code>, <code>-bone.svg</code></li><li><code>ostro-app-icon.svg</code></li><li><code>ostro-chest-60mm-bone.svg</code> (6 cm embroidery)</li></ul>
</section>''')

# ================================================================ css + page
CSS = f'''
/* Layout: Bone board with rounded panels; Night panels for the dark studies, like a pinned-up presentation wall */
:root{{color-scheme:light;
 --bone:{BONE};--night:{NIGHT};--dune:{DUNE};--sand:{SAND};--ash:{ASH};--ember:{EMBER};
 --display:Archivo,"Helvetica Neue",Arial,sans-serif;--body:Archivo,"Helvetica Neue",Arial,sans-serif;--mono:"IBM Plex Mono",ui-monospace,Menlo,monospace}}
*{{box-sizing:border-box}}
body{{background:var(--bone);color:var(--night);font-family:var(--body);font-size:16px;line-height:1.6;margin:0}}
.wrap{{max-width:1180px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:20px 64px;display:grid;gap:18px}}
.panel{{background:var(--bone);border:1px solid color-mix(in srgb,var(--ash) 45%,transparent);border-radius:16px;padding:clamp(20px,4vw,44px);min-width:0;overflow:hidden}}
.panel.dark,.cover{{background:var(--night);color:var(--bone);border-color:var(--night)}}
h2{{font-family:var(--display);font-weight:800;text-transform:uppercase;letter-spacing:.06em;font-size:clamp(22px,3.2vw,34px);line-height:1.12;margin:0;text-wrap:balance;max-width:24ch}}
.eyebrow{{font-family:var(--mono);font-weight:500;font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--ash);margin:0 0 12px}}
.lead{{max-width:64ch;margin:14px 0 0}}
svg{{display:block;max-width:100%;height:auto}}
code{{font-family:var(--mono);font-size:.88em}}
/* cover */
.cover{{display:grid;place-items:center;gap:26px;padding-block:clamp(56px,10vw,120px)}}
.cover .cv{{width:min(72%,320px)}}
.cover .tag{{font-family:var(--mono);font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--ash);margin:0;text-align:center}}
@media (prefers-reduced-motion:no-preference){{.cover .cv{{animation:rise 1.1s cubic-bezier(.2,.7,.2,1) both}}@keyframes rise{{from{{transform:translateY(8px)}}to{{transform:none}}}}}}
/* story */
.storytext{{display:grid;gap:12px;margin-top:16px;max-width:64ch;font-size:clamp(16px,1.6vw,18px)}}
.storytext p{{margin:0}}
.facts{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr));gap:12px;margin:26px 0 0}}
.facts div{{border-top:1px solid var(--ash);padding-top:10px}}
.facts dt{{font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--ash)}}
.facts dd{{margin:2px 0 0}}
/* idea */
.eq{{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:clamp(8px,3vw,36px);margin-top:28px}}
.eq figure{{margin:0;display:grid;gap:8px;justify-items:center}}
.eq svg{{width:clamp(78px,15vw,150px)}}
.eq figcaption,.sk figcaption b,.cap,.lbl,.mono,.mono-s,.specs span,.dont figcaption{{font-family:var(--mono);text-transform:uppercase;letter-spacing:.12em}}
.eq figcaption{{font-size:10px;color:var(--ash)}}
.op{{font-size:clamp(26px,4vw,40px);font-weight:400;color:var(--ash)}}
/* sketches */
.sketches{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin-top:26px}}
.sk{{margin:0;display:grid;gap:8px;align-content:start}}
.sk svg{{width:100%;border-radius:10px}}
.sk figcaption{{font-size:13px;line-height:1.4}}
.sk figcaption b{{display:block;font-size:10.5px;font-weight:500;color:var(--night);margin-bottom:2px}}
.sk:not(.kept) figcaption b{{text-decoration:line-through;text-decoration-color:var(--ash)}}
/* geometry */
.geo{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,340px),1fr));gap:28px;align-items:center}}
.geo>*{{min-width:0}} .geo>svg{{width:min(100%,440px);margin:0 auto}}
.specs{{list-style:none;padding:0;margin:20px 0 0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px 18px}}
.specs li{{border-top:1px solid color-mix(in srgb,var(--ash) 60%,transparent);padding-top:8px;font-family:var(--mono);font-size:20px}}
.specs span{{display:block;font-size:10px;color:var(--ash)}}
/* tiles */
.suite{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin-top:26px}}
.suite.three{{grid-template-columns:repeat(3,minmax(0,1fr))}}
.tile{{border-radius:12px;display:grid;place-items:center;padding:32px 20px 44px;min-height:240px;position:relative}}
.t-bone{{background:var(--bone);border:1px solid color-mix(in srgb,var(--ash) 45%,transparent)}}
.t-night{{background:var(--night);color:var(--bone)}}
.tile .cap{{position:absolute;left:14px;bottom:12px;font-size:10px;color:var(--ash)}}
.tile .mk{{height:150px;width:auto}} .tile .lk{{width:min(100%,280px)}} .tile .ico{{width:min(70%,180px)}} .tile .hd{{width:min(100%,320px)}}
.sizes{{display:flex;align-items:flex-end;gap:28px;flex-wrap:wrap;margin-top:24px}}
.sizes small{{display:block;font-family:var(--mono);font-size:10px;letter-spacing:.12em;color:var(--ash);margin-top:6px}}
/* palette */
.sws{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-top:26px}}
.sw{{border-radius:12px;overflow:hidden;border:1px solid color-mix(in srgb,var(--ash) 45%,transparent)}}
.chip{{height:clamp(120px,16vw,180px)}}
.swt{{padding:14px 16px;display:grid;gap:2px}}
.swt b{{font-family:var(--display);font-weight:800;text-transform:uppercase;letter-spacing:.1em;font-size:18px}}
.swt code{{font-size:13px;letter-spacing:.08em}}
.swt span{{font-family:var(--mono);font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--night);margin-top:6px}}
.swt small{{font-size:13px;line-height:1.4}}
.ratio{{display:flex;height:16px;border-radius:8px;overflow:hidden;margin-top:22px;border:1px solid color-mix(in srgb,var(--ash) 45%,transparent)}}
.mono-s{{font-size:10.5px;color:var(--ash);margin:8px 0 0}}
.sub{{font-family:var(--mono);font-weight:500;font-size:11px;letter-spacing:.12em;text-transform:uppercase;margin:30px 0 0}}
.checks{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,250px),1fr));gap:10px;margin-top:12px}}
.ck{{display:flex;gap:12px;align-items:center;border-top:1px solid color-mix(in srgb,var(--ash) 45%,transparent);padding-top:10px}}
.ckc{{width:56px;height:56px;border-radius:10px;display:grid;place-items:center;font-weight:700;font-size:20px;flex:none;border:1px solid color-mix(in srgb,var(--ash) 35%,transparent)}}
.ck b{{display:block;font-weight:700;font-size:14px}} .ck code{{font-size:13px}}
.ck small{{display:block;font-family:var(--mono);font-size:10.5px;letter-spacing:.12em;text-transform:uppercase}}
.ck small.no{{text-decoration:underline;text-decoration-color:var(--ember);text-decoration-thickness:2px;text-underline-offset:3px}}
/* colourways */
.cws{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr));gap:18px;margin-top:26px}}
.cw{{display:grid;gap:12px}}
.pair{{display:grid;grid-template-columns:1fr 1fr;border-radius:12px;overflow:hidden;height:150px;border:1px solid color-mix(in srgb,var(--ash) 45%,transparent)}}
.pair div{{display:flex;align-items:flex-end;padding:12px}}
.pair span{{font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;line-height:1.5;background:var(--bone);color:var(--night);padding:4px 8px;border-radius:4px}}
.cwfig{{border-radius:12px;padding:18px;display:grid;place-items:center}} .cwfig svg{{width:min(100%,300px)}}
.mono{{font-size:12px;margin:0;font-weight:500}}
/* type */
.types{{display:grid;gap:14px;margin-top:26px}}
.ty{{border-top:1px solid var(--ash);padding-top:16px;display:grid;gap:8px;min-width:0}}
.ty p{{margin:0}}
.sp-d{{font-weight:800;text-transform:uppercase;letter-spacing:.2em;font-size:clamp(26px,5vw,52px);line-height:1.05;overflow-wrap:anywhere}}
.sp-al{{font-weight:700;letter-spacing:.2em;font-size:13px;overflow-wrap:anywhere}}
.sp-b{{font-weight:400;font-size:clamp(17px,2vw,21px);max-width:52ch;line-height:1.5}}
.sp-m{{font-family:var(--mono);font-weight:500;text-transform:uppercase;letter-spacing:.12em;font-size:clamp(12px,1.5vw,15px)}}
.why{{color:var(--night);font-size:14px;opacity:1}}
/* voice */
.lines{{list-style:none;padding:0;margin:26px 0 0;display:grid;gap:6px}}
.lines li{{font-weight:700;font-size:clamp(24px,4.4vw,46px);line-height:1.15;letter-spacing:-.005em}}
.never{{list-style:none;padding:0;margin:0;display:flex;gap:12px 28px;flex-wrap:wrap}}
.never li{{font-size:clamp(18px,2.4vw,24px);text-decoration:line-through;text-decoration-thickness:2px;text-decoration-color:var(--ember);color:var(--bone)}}
/* applications */
.apps{{display:grid;grid-auto-flow:dense;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin-top:26px}}
.app{{border-radius:12px;padding:24px;display:grid;gap:14px;place-items:center;align-content:center;min-height:300px;background:var(--sand)}}
.app.dk{{background:var(--night)}}
.app.wide2{{grid-column:1/-1;background:var(--bone);border:1px solid color-mix(in srgb,var(--ash) 45%,transparent)}}
.hoodies{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:18px;width:100%}}
.hoodies>div{{display:grid;gap:8px;justify-items:center}} .hoodies svg{{width:min(100%,380px)}}
.app .lbl{{font-size:10px;color:var(--night)}} .app.dk .lbl{{color:var(--bone)}}
.tagsvg{{width:min(60%,200px)}} .labsvg{{width:min(100%,300px)}} .igsvg{{width:min(100%,320px)}} .bagsvg{{width:min(90%,280px)}} .postsvg{{width:min(100%,300px)}}
/* donts */
.donts{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr));gap:14px;margin-top:26px}}
.dont{{margin:0;display:grid;gap:10px}} .dont svg{{width:100%;border-radius:10px;border:1px solid color-mix(in srgb,var(--ash) 45%,transparent)}}
.dont figcaption{{font-size:10.5px;line-height:1.5}}
.app.ig{{grid-row:span 2}}
@media (max-width:900px){{.apps{{grid-template-columns:repeat(2,minmax(0,1fr))}}}}
@media (max-width:720px){{.sketches{{grid-template-columns:repeat(2,minmax(0,1fr))}}.suite,.suite.three{{grid-template-columns:minmax(0,1fr)}}.sws{{grid-template-columns:repeat(2,minmax(0,1fr))}}}}
@media (max-width:600px){{.apps{{grid-template-columns:minmax(0,1fr)}}.app.ig{{grid-row:auto}}}}
.files{{columns:2 260px;font-size:14px;margin:16px 0 0;padding-left:18px}}
'''

page = ('<title>OSTRO — Brand Identity</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
        '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;700;800&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">\n'
        f'<style>{CSS}</style>\n<main class="wrap">\n' + '\n\n'.join(H) + '\n</main>\n')
open(OUT_HTML, 'w').write(page)

# ================================================================ svg files
def wsvg(name, inner, w, h): open(os.path.join(OUT_SVG, name), 'w').write(standalone(inner, w, h))
for nm, col in (('night', NIGHT), ('bone', BONE)):
    wsvg(f'ostro-mark-{nm}.svg', mark(col), MW, 100)
    c, w, h = primary(col); wsvg(f'ostro-primary-{nm}.svg', c, w, h)
    c, w, h = horizontal(col); wsvg(f'ostro-horizontal-{nm}.svg', c, w, h)
    c, w = wordmark(col, 0, 0, 100); wsvg(f'ostro-wordmark-{nm}.svg', c, w, 100)
wsvg('ostro-mark-accent.svg', mark(NIGHT, 2, 2, 1, True), MW + 4, 104)
c, w, h = app_icon(); wsvg('ostro-app-icon.svg', c, w, h)
# chest: 60 mm wide, in mm units
s = 60 / MW
open(os.path.join(OUT_SVG, 'ostro-chest-60mm-bone.svg'), 'w').write(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 {100*s:.2f}" width="60mm" height="{100*s:.2f}mm">{mark(BONE, 0, 0, s)}</svg>\n')
print('ok', len(page), 'X', round(X, 1), 'MW', round(MW, 1))
