import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pen import *
from shapely.geometry import Point
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

# ---------------------------------------------------------------- mark: two barchan dunes
from o2 import C, DISC, lens, ring, rot, split, lensO, crescent, egg, ovalO, dunesO, dunes_counter
from shapely.geometry import box as _box
MA, MHW, MEW, ME = -25, 16, 3, 6          # tilt, counter half-width, half-opening at edge, stagger
_m, MR, MD = dunesO(MA, MHW, MEW, ME)
MARK = _m.simplify(0.08)
MG = 2*MEW
MW = 100.0
COUNTER = dunes_counter(MA, MHW, MEW, ME)
X = 2 * MHW                                # clear-space unit = widest part of the counter
MARK_D = to_path(MARK)
hair = COUNTER.buffer(-5, join_style=2, mitre_limit=5).simplify(0.05).exterior
HAIR_D = 'M' + ' L'.join(f'{x:.2f},{y:.2f}' for x, y in list(hair.coords)[:-1]) + 'Z'
def mark(fill, tx=0, ty=0, s=1, accent=False):
    g = f'<path fill="{fill}" d="{MARK_D}"/>'
    if accent:
        g += f'<path fill="none" stroke="{EMBER}" stroke-width="1.1" stroke-linejoin="round" d="{HAIR_D}"/>'
    return f'<g transform="translate({tx:.2f},{ty:.2f}) scale({s:.4f})">{g}</g>'
PIECES = sorted(list(MARK.geoms), key=lambda p: p.centroid.x)
def poly_d(pts): return 'M' + ' L'.join(f'{x:.2f},{y:.2f}' for x, y in pts)

# ---------------------------------------------------------------- wordmark (Archivo 800, outlined)
font = TTFont(os.environ.get('ARCHIVO_TTF', os.path.join(HERE, '../fonts/archivo800.ttf')))
gs = font.getGlyphSet(); cmap = font.getBestCmap()
UPM = font['head'].unitsPerEm; CAP = font['OS/2'].sCapHeight
def wordmark_path(text='STRO', track=0.35):
    # The first O of OSTRO is the mark itself: a disc the size of Archivo's O (with its overshoot).
    o = gs[cmap[ord('O')]]; bp = BoundsPen(gs); o.draw(bp); ox0, oy0, ox1, oy1 = bp.bounds
    D = oy1 - oy0                                   # disc diameter in font units
    disc = ((ox1 - ox0 - D) / 2, CAP - oy1, D)      # x, y (top), diameter; O ink starts at x=0
    x = o.width + track * UPM - ox0; ds = []; last_r = 0
    for i, ch in enumerate(text):
        gl = gs[cmap[ord(ch)]]
        bp = BoundsPen(gs); gl.draw(bp); bx0, by0, bx1, by1 = bp.bounds
        sp = SVGPathPen(gs)
        gl.draw(TransformPen(sp, (1, 0, 0, -1, x, CAP))); ds.append(sp.getCommands())
        last_r = x + bx1
        x += gl.width + (track * UPM if i < len(text) - 1 else 0)
    return ''.join(ds), last_r, disc
WM_D, WM_W, WM_DISC = wordmark_path()
def wordmark(fill, tx, ty, cap_h, accent=False):
    s = cap_h / CAP; dx, dy, D = WM_DISC
    g = mark(fill, tx + dx*s, ty + dy*s, D*s/100, accent)
    return g + f'<path fill="{fill}" transform="translate({tx:.2f},{ty:.2f}) scale({s:.5f})" d="{WM_D}"/>', WM_W * s

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
    (lensO(-22, 60, 47),          'Lens',            'Clean, but it looks like a hundred fashion logos.'),
    (crescent(),                  'Crescent counter','Reads as a moon, not an O.'),
    (egg(),                       'Off-centre counter','Reads as a button or an eye.'),
    (ovalO(),                     'Oval counter',    'Turns into a zero next to numbers.'),
    (split(-25, 64, 50, 5.5),      'Notched split',  'Steps where the gap meets the counter. Looks broken.'),
    (split(0, 60, 47, 4.5),       'Upright split',   'Upright, it reads as a coffee bean.'),
    (dunesO(-25, 11, 2.4, 6)[0],    'Thin dunes',      'The counter closes up at 20 px.'),
    (MARK,                        'Two dunes',       'Kept. Two crescents, the wind between them.'),
]
def sketch_svg(i, g, kept):
    s = 0.8
    g = affinity.scale(g.simplify(0.1), s, s, origin=(0, 0))
    w = g.bounds[2]; h = g.bounds[3]
    ox, oy = (120 - w)/2, (130 - h)/2
    d = to_path(g)
    flt = f'pencil{i}'
    out = [f'<defs><filter id="{flt}" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="{i+3}" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="1.8"/></filter></defs>']
    out.append(f'<rect width="120" height="130" fill="{BONE}"/>')
    out.append(f'<circle cx="{ox+40}" cy="{oy+40}" r="46" fill="none" stroke="{ASH}" stroke-width=".4" stroke-dasharray="2 3"/>')
    passes = [(0.3, 0.6, 0.9, 1.0, 0.3), (-0.8, 0.4, 0.45, 0.55, -0.5), (0.9, -0.5, 0.35, 0.5, 0.6)]
    out.append(f'<g filter="url(#{flt})" transform="translate({ox:.2f},{oy:.2f})">')
    out.append(f'<path d="{d}" fill="{NIGHT}" fill-opacity="{".16" if kept else ".07"}"/>')
    for dx, dy, op, sw, rot_ in passes:
        out.append(f'<path d="{d}" fill="none" stroke="{NIGHT}" stroke-opacity="{op}" stroke-width="{sw}" transform="translate({dx},{dy}) rotate({rot_} {w/2:.1f} {h/2:.1f})"/>')
    out.append('</g>')
    if kept:
        out.append(f'<ellipse cx="60" cy="65" rx="55" ry="58" fill="none" stroke="{EMBER}" stroke-width="1.4" filter="url(#{flt})" transform="rotate(-6 60 65)"/>')
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
def part(g, label):
    pad = 8
    inner = (f'<g transform="translate({pad},{pad})"><circle cx="50" cy="50" r="50" fill="none" stroke="{ASH}" stroke-width=".6" stroke-dasharray="2 2"/>'
             f'<path fill="{ASH}" d="{to_path(g.simplify(0.08))}"/></g>')
    return f'<figure>{svg(inner, 100 + 2*pad, 100 + 2*pad, label)}<figcaption>{label}</figcaption></figure>'
fin = f'<figure>{svg(mark(BONE, 8, 8), 116, 116, "OSTRO mark")}<figcaption>The OSTRO mark</figcaption></figure>'
A(f'''<section class="panel dark">
 <p class="eyebrow">Mark · The idea</p>
 <h2>Two dunes with the wind between them.</h2>
 <p class="lead">In the Sahara, a wind that always blows from one direction builds crescent-shaped dunes called barchans. The OSTRO mark is two of them, turned to face each other inside a heavy circle. The space between them is the path of the wind: thin where it enters and leaves the circle, open in the middle, where it becomes the counter of the O. Solid, calm, and readable as a letter at any size.</p>
 <div class="eq">
  {part(PIECES[0], 'First dune')}<span class="op">+</span>
  {part(PIECES[1], 'Second dune')}<span class="op">=</span>
  {fin}
 </div>
</section>''')

# ---------- mark: sketches
cells = ''.join(f'<figure class="sk{" kept" if g is MARK else ""}">{sketch_svg(i, g, g is MARK)}<figcaption><b>{nm}</b>{note}</figcaption></figure>'
                for i, (g, nm, note) in enumerate(SKETCH))
A(f'''<section class="panel paper">
 <p class="eyebrow">Mark · Sketches</p>
 <h2>Eight Os on the way to the dunes</h2>
 <p class="lead">Every version starts from the same heavy circle and only changes the counter. They were all tested at 32 and 20 pixels. The plain lens was clean but common. The crescent, the off-centre hole and the oval stopped reading as an O. The first split version had steps where the gap met the counter. Drawing the gap and the counter as one pair of curves fixed it, and kept a clear O.</p>
 <div class="sketches">{cells}</div>
</section>''')

# ---------- mark: geometry
gl = []
for x in range(-20, 121, 10): gl.append(f'<line x1="{x}" y1="-24" x2="{x}" y2="124"/>')
for y in range(-20, 121, 10): gl.append(f'<line x1="-24" y1="{y}" x2="124" y2="{y}"/>')
cy0, cy1 = COUNTER.bounds[1], COUNTER.bounds[3]
c1 = rot(Point(50 + MD, 50 + ME), MA); c2 = rot(Point(50 - MD, 50 - ME), MA)
def _xmeasure():
    a = math.radians(MA)
    def R_(x, y):
        dx, dy = x - 50, y - 50
        return 50 + dx*math.cos(a) - dy*math.sin(a), 50 + dx*math.sin(a) + dy*math.cos(a)
    (x1, y1), (x2, y2) = R_(50 - MHW, 50), R_(50 + MHW, 50)
    tx, ty = R_(50, 43)
    return (f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{EMBER}" stroke-width=".9"/>'
            f'<circle cx="{x1:.2f}" cy="{y1:.2f}" r="1" fill="{EMBER}"/><circle cx="{x2:.2f}" cy="{y2:.2f}" r="1" fill="{EMBER}"/>'
            f'<text x="{tx:.2f}" y="{ty:.2f}" font-family="IBM Plex Mono,monospace" font-size="5" fill="{EMBER}" text-anchor="middle">x</text>')
geo = (f'<defs><clipPath id="gclip"><rect x="-24" y="-24" width="148" height="148"/></clipPath></defs>'
       f'<g stroke="{ASH}" stroke-opacity=".35" stroke-width=".3">{"".join(gl)}</g>'
       f'<path fill="{BONE}" fill-opacity=".94" d="{MARK_D}"/>'
       f'<g clip-path="url(#gclip)" fill="none" stroke="{ASH}" stroke-width=".5" stroke-dasharray="1.5 1.5"><circle cx="{c1.x:.2f}" cy="{c1.y:.2f}" r="{MR}"/><circle cx="{c2.x:.2f}" cy="{c2.y:.2f}" r="{MR}"/></g>'
       f'<circle cx="50" cy="50" r="1.2" fill="{ASH}"/>'
       f'<g stroke="{ASH}" stroke-width=".5" fill="none"><line x1="-24" y1="0" x2="124" y2="0"/><line x1="-24" y1="100" x2="124" y2="100"/>'
       '</g>'
       + _xmeasure() +
       f'<g font-family="IBM Plex Mono,monospace" font-size="3.6" letter-spacing=".5" fill="{BONE}" fill-opacity=".8">'
       f'<text x="-22" y="-2">TOP</text><text x="-22" y="105">BASELINE</text></g>')
A(f'''<section class="panel dark geo">
 <div class="geotext"><p class="eyebrow">Mark · Geometry</p>
 <h2>One circle, two curves</h2>
 <p class="lead">The mark is a circle 100 units across. Two much larger circles, radius {MR:.0f}, overlap through its middle. Where they overlap, the circle is cut away: {2*MHW} units wide at the centre, narrowing to {MG:g} units where it leaves the edge. The two big circles are staggered by {ME} units, so the cut leans like a gust, and the whole cut is turned {abs(MA)}° to the left. The widest part of the counter is the unit <b>x</b>: it sets the clear space around every lockup.</p>
 <ul class="specs"><li><span>Circle</span>100</li><li><span>Cutting circles</span>R {MR:.0f}</li><li><span>Opening · tilt</span>{MG:g} · {abs(MA)}°</li><li><span>Counter x</span>{X:.0f}</li></ul></div>
 {svg(geo, 0, 0, 'Mark construction grid').replace('viewBox="0 0 0.0 0.0"', 'viewBox="-26 -26 152 152"')}
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

# ---------- lockups + signature details (kit.py, part 1)
_KIT = open(os.path.join(HERE, 'kit.py')).read().split('# =================================================================== PRODUCT & PACKAGING')
exec(_KIT[0])

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

# ---------- packaging + social (kit.py, part 2)
exec(_KIT[1])

# ---------- don'ts
def dont(inner, cap, bg=BONE):
    x = f'<g stroke="{NIGHT}" stroke-width="3" stroke-linecap="round"><line x1="14" y1="14" x2="186" y2="146"/><line x1="186" y1="14" x2="14" y2="146"/></g>'
    return f'<figure class="dont"><svg viewBox="0 0 200 160" role="img" aria-label="{cap}"><rect width="200" height="160" fill="{bg}"/>{inner}{x}</svg><figcaption>{cap}</figcaption></figure>'
stretched = f'<g transform="translate(40,30) scale(1.7,1)">{mark(NIGHT, 0, 0, 1.0)}</g>'.replace('scale(1.7,1)', 'scale(1.65,1)')
stretched = f'<g transform="translate(17,30) scale(1.66,1)"><path fill="{NIGHT}" d="{MARK_D}"/></g>'
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
 <p class="lead">Logos are outlined SVG, so they print and embroider without the fonts installed. Print pieces and social templates keep their text as live Archivo and IBM Plex Mono, so install both from Google Fonts before editing them.</p>
 <ul class="files"><li><code>svg/ostro-mark-night.svg</code>, <code>-bone.svg</code>, <code>-accent.svg</code></li><li><code>svg/ostro-primary-night.svg</code>, <code>-bone.svg</code></li><li><code>svg/ostro-wordmark-night.svg</code>, <code>-bone.svg</code></li><li><code>svg/ostro-app-icon.svg</code>, <code>svg/ostro-chest-60mm-bone.svg</code></li><li><code>social/</code>: 4 posts, 3 stories, 5 highlight covers, avatar, Facebook cover, YouTube banner and thumbnail</li><li><code>print/</code>: hang tag front and back, neck and care labels, bag, shipping label, thank-you card, business card, stickers</li></ul>
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
.app.dk{{grid-row:span 2}}
.tile.wmt{{grid-column:span 1}} .tile.wmt .lk{{width:min(100%,360px)}}
.devices{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin-top:26px}}
.dev{{display:grid;gap:10px;align-content:start}} .dev .art svg{{width:100%;border-radius:10px;border:1px solid color-mix(in srgb,var(--ash) 45%,transparent)}}
.dev h3{{margin:4px 0 0;font-weight:800;text-transform:uppercase;letter-spacing:.08em;font-size:16px}} .dev p{{margin:0;font-size:14.5px}}
.pairsvg{{display:flex;gap:12px;justify-content:center;width:100%}} .pairsvg .tagsvg{{width:min(46%,170px)}}
.stack{{display:flex;gap:14px;align-items:center;justify-content:center;flex-wrap:wrap;width:100%}} .caresvg{{width:90px}} .stack .labsvg{{width:min(100%,240px)}}
.codsvg{{width:min(100%,320px)}} .cardsvg{{width:min(100%,300px)}} .cards{{display:grid;gap:12px;width:min(100%,320px)}} .cards svg{{width:100%}}
.sub2{{font-family:var(--mono);font-weight:500;font-size:11px;letter-spacing:.12em;text-transform:uppercase;margin:36px 0 0;padding-top:14px;border-top:1px solid var(--ash)}}
.note{{font-size:14px;margin:10px 0 0;max-width:62ch}}
.bio{{font-family:var(--body);font-size:15px;line-height:1.5;background:color-mix(in srgb,var(--sand) 35%,var(--bone));padding:12px 14px;border-radius:8px;margin:6px 0 0;white-space:pre-wrap}}
.igrow{{display:grid;grid-template-columns:minmax(0,320px) minmax(0,1fr);gap:28px;margin-top:16px;align-items:start}}
.igp svg{{width:100%}} .igside{{min-width:0}}
.hls{{display:flex;flex-wrap:wrap;gap:16px;margin-top:22px}} .hl{{margin:0;display:grid;gap:6px;justify-items:center}}
.hlc{{width:72px;height:72px;border-radius:50%;overflow:hidden;outline:1.5px solid var(--ash);outline-offset:3px}} .hlc svg{{width:100%}}
.hl figcaption{{font-size:12px}}
.posts{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin-top:16px}}
.stories{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin-top:16px;max-width:820px}}
.soc{{margin:0;display:grid;gap:8px;align-content:start}} .soc svg{{width:100%;border-radius:8px;border:1px solid color-mix(in srgb,var(--ash) 45%,transparent)}}
.soc figcaption,.hl figcaption{{font-family:var(--mono);font-size:10.5px;letter-spacing:.12em;text-transform:uppercase}}
.soc small{{display:block;color:var(--ash);font-size:10px}}
.wide-soc{{margin-top:16px}} .wide-soc svg{{width:100%;border-radius:8px;border:1px solid color-mix(in srgb,var(--ash) 45%,transparent)}}
.ytrow{{display:grid;grid-template-columns:minmax(0,2fr) minmax(0,1fr);gap:14px;margin-top:14px;align-items:start}} .av2 svg{{border:none;max-width:220px}}
@media (max-width:820px){{.devices{{grid-template-columns:minmax(0,1fr)}}.posts{{grid-template-columns:repeat(2,minmax(0,1fr))}}.igrow{{grid-template-columns:minmax(0,1fr)}}.igp{{max-width:340px}}}}
@media (max-width:520px){{.stories{{grid-template-columns:repeat(2,minmax(0,1fr))}}.ytrow{{grid-template-columns:minmax(0,1fr)}}}}
@media (max-width:900px){{.apps{{grid-template-columns:repeat(2,minmax(0,1fr))}}}}
@media (max-width:720px){{.sketches{{grid-template-columns:repeat(2,minmax(0,1fr))}}.suite,.suite.three{{grid-template-columns:minmax(0,1fr)}}.sws{{grid-template-columns:repeat(2,minmax(0,1fr))}}}}
@media (max-width:600px){{.apps{{grid-template-columns:minmax(0,1fr)}}.app.dk{{grid-row:auto}}}}
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
    c, w = wordmark(col, 0, 2, 100); wsvg(f'ostro-wordmark-{nm}.svg', c, w, 106)
wsvg('ostro-mark-accent.svg', mark(NIGHT, 2, 2, 1, True), MW + 4, 104)
c, w, h = app_icon(); wsvg('ostro-app-icon.svg', c, w, h)
# chest: 60 mm wide, in mm units
s = 60 / MW
open(os.path.join(OUT_SVG, 'ostro-chest-60mm-bone.svg'), 'w').write(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 {100*s:.2f}" width="60mm" height="{100*s:.2f}mm">{mark(BONE, 0, 0, s)}</svg>\n')
ROOT = os.path.dirname(OUT_SVG.rstrip('/'))
for rel, (inner, w, h) in EXPORTS.items():
    p = os.path.join(ROOT, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w').write(standalone(inner, w, h))
print('ok', len(page), 'X', round(X, 1), 'MW', round(MW, 1))
