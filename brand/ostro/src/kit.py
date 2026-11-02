# Brand kit blocks for build.py: lockups, signature details, packaging & print, social media.
# exec()'d inside build.py so it shares its helpers (mark, wordmark, hoodie, svg, colours...).

MONO = 'IBM Plex Mono,monospace'
SANS = 'Archivo,sans-serif'
EXPORTS = {}          # path -> (inner, w, h), written as standalone SVG files at the end

def T(x, y, txt, size, fill, font=SANS, weight=400, anchor='start', ls=0, extra=''):
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-weight="{weight}" font-size="{size}" '
            f'letter-spacing="{ls}" text-anchor="{anchor}" fill="{fill}"{extra}>{txt}</text>')

def place_hoodie(x, y, w, body, panel, logo=BONE, uid='h'):
    s = w / 400
    inner = hoodie(body, panel, logo, uid)
    if body == NIGHT:
        inner = inner.replace(f'fill="{NIGHT}" fill-opacity=".22"', f'fill="{ASH}" fill-opacity=".25"')
    return f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.4f})">{inner}</g>'

def mark_at(fill, cx, cy, size, accent=False):
    return mark(fill, cx - size/2, cy - size/2, size/100, accent)

def wm_at(fill, cx, y, cap, anchor='middle'):
    w = WM_W * cap / CAP
    x = cx - w/2 if anchor == 'middle' else cx
    return wordmark(fill, x, y, cap)[0]

def stitch(x1, y1, x2, y2, col=ASH, sw=2, dash='14 9'):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{sw}" stroke-dasharray="{dash}" stroke-linecap="round"/>'

def dune_pattern(pid, fg, bg, op, cell=120, size=44):
    return (f'<defs><pattern id="{pid}" width="{cell}" height="{cell}" patternUnits="userSpaceOnUse" patternTransform="rotate(-8)">'
            f'<rect width="{cell}" height="{cell}" fill="{bg}"/>'
            f'<g opacity="{op}">{mark_at(fg, cell*0.25, cell*0.25, size)}{mark_at(fg, cell*0.75, cell*0.75, size)}</g></pattern></defs>')

# the counter on its own: "the cut"
CUT_D = to_path(COUNTER.simplify(0.08))
def cut_at(fill, cx, cy, h, rot_=0):
    s = h / (COUNTER.bounds[3] - COUNTER.bounds[1])
    mx, my = (COUNTER.bounds[0] + COUNTER.bounds[2]) / 2, (COUNTER.bounds[1] + COUNTER.bounds[3]) / 2
    return f'<g transform="translate({cx},{cy}) rotate({rot_}) scale({s:.4f}) translate({-mx:.2f},{-my:.2f})"><path fill="{fill}" d="{CUT_D}"/></g>'

# =================================================================== LOCKUPS
def primary_plain(fg, scale=1.0):
    return primary(fg, scale=scale)
def wordmark_box(fg, cap=60, pad=0):
    w = WM_W * cap / CAP
    return wordmark(fg, pad, pad, cap)[0], w + 2*pad, cap * 1.04 + 2*pad
def wm_guides(fg):
    cap = 40; w = WM_W * cap / CAP; pad = X * cap / 100 * 1.5
    inner = guide_box(pad, pad, w, cap, pad, ASH) + wordmark(fg, pad, pad, cap)[0]
    return inner, w + 2*pad, cap + 2*pad

p1 = primary(NIGHT, guides=ASH); p2 = primary(BONE, guides=ASH)
w1 = wm_guides(NIGHT); w2 = wm_guides(BONE)
def icon_guides(bg, fg):
    inner, w, h = app_icon(bg, fg)
    pad = 30
    return (f'<rect x="{pad}" y="{pad}" width="{w}" height="{h}" rx="44" fill="{bg}"/>'
            f'<g transform="translate({pad},{pad})">{inner[inner.index("<g"):]}</g>'
            f'<rect x="4" y="4" width="{w+2*pad-8}" height="{h+2*pad-8}" fill="none" stroke="{ASH}" stroke-dasharray="4 4"/>'), w + 2*pad, h + 2*pad
i1 = icon_guides(NIGHT, BONE)
def lock_tile(content, w, h, label, cls, cap, extra=''):
    return f'<div class="tile {cls} {extra}">{svg(content, w, h, label, "lk")}<span class="cap">{cap}</span></div>'
def chest(body, panel):
    inner = hoodie(body, panel, BONE, 'c', notes=True)
    if body == NIGHT: inner = inner.replace(f'fill="{NIGHT}" fill-opacity=".22"', f'fill="{ASH}" fill-opacity=".25"')
    return inner
wm_sizes = ''.join(f'<div>{svg(wordmark(NIGHT, 0, 1, h)[0], WM_W*h/CAP, h*1.06, "OSTRO wordmark at " + str(h) + " px cap height", "", f"height:{h*1.06:.0f}px;width:auto")}<small>Cap {h} px</small></div>' for h in (40, 20, 12))

A(f'''<section class="panel">
 <p class="eyebrow">Lockups</p>
 <h2>The mark lives inside the name</h2>
 <p class="lead">The first O of OSTRO is the mark itself, set at the size of Archivo ExtraBold's O so it sits level with the capitals next to it. The other four letters are Archivo ExtraBold, tracked at 0.35em. In the primary lockup the mark also sits centred above the name. Use the mark alone where space is tight: the profile picture, the chest, a sticker. The dashed line is the clear space: the width of the counter at its widest, <b>x</b>, on every side.</p>
 <div class="suite">
  {lock_tile(p1[0], p1[1], p1[2], 'Primary lockup on Bone', 't-bone', 'Primary · mark above the name')}
  {lock_tile(p2[0], p2[1], p2[2], 'Primary lockup on Night', 't-night', 'Primary · on Night')}
  {lock_tile(w1[0], w1[1], w1[2], 'Wordmark on Bone', 't-bone', 'Wordmark · the mark is the O', 'wmt')}
  {lock_tile(w2[0], w2[1], w2[2], 'Wordmark on Night', 't-night', 'Wordmark · on Night', 'wmt')}
  <div class="tile t-bone">{svg(i1[0], i1[1], i1[2], 'Profile picture and app icon', 'ico')}<span class="cap">Profile picture / app icon</span></div>
  <div class="tile t-night">{svg(app_icon(NIGHT, BONE)[0].replace('rx="44"', 'rx="100"'), 200, 200, 'Round avatar', 'ico')}<span class="cap">Cropped round by Instagram, Facebook, YouTube</span></div>
  <div class="tile t-bone tall">{svg(chest(NIGHT, ASH), 400, 380, 'Chest monogram on Night hoodie', 'hd')}<span class="cap">Chest · mark alone, 6 cm</span></div>
  <div class="tile t-night tall">{svg(chest(DUNE, SAND), 400, 380, 'Chest monogram on Dune hoodie', 'hd')}<span class="cap">Chest · on Night</span></div>
 </div>
 <div class="sizes" aria-label="Wordmark small size test">{wm_sizes}</div>
</section>''')

# =================================================================== SIGNATURE DETAILS
cut_art = (f'<rect width="300" height="160" fill="{BONE}"/>' + cut_at(NIGHT, 70, 80, 110, 0) +
           ''.join(f'{cut_at(NIGHT, 140, 46 + k*34, 16, 0)}<rect x="154" y="{42 + k*34}" width="{[110, 80, 96][k]}" height="8" rx="4" fill="{ASH}" fill-opacity=".5"/>' for k in range(3)))
pat_art = dune_pattern('sigpat', BONE, NIGHT, 0.12) + '<rect width="300" height="160" fill="url(#sigpat)"/>'
stitch_art = (f'<rect width="300" height="160" fill="{NIGHT}"/>' + stitch(30, 64, 270, 64, ASH, 3) +
              stitch(30, 96, 270, 96, BONE, 3) + f'<circle cx="270" cy="128" r="5" fill="{EMBER}"/>')
A(f'''<section class="panel">
 <p class="eyebrow">Signature details</p>
 <h2>Small things that repeat</h2>
 <p class="lead">Three details taken from the mark and the workshop. Use them one at a time, so each surface stays calm.</p>
 <div class="devices">
  <div class="dev"><div class="art">{svg(cut_art, 300, 160, 'The cut used as a bullet and a sticker')}</div><h3>The cut</h3><p>The counter on its own, the path of the wind. Use it as a bullet in lists, a cursor in stories, or a small sticker. Night or Bone, never Ember.</p></div>
  <div class="dev"><div class="art">{svg(stitch_art, 300, 160, 'Running stitch dividers and the Ember dot')}</div><h3>The stitch and the dot</h3><p>A dashed line of 14-unit stitches and 9-unit gaps replaces plain rules. The Ember dot is the one accent on a surface: on the bag, a card or a post.</p></div>
  <div class="dev"><div class="art">{svg(pat_art, 300, 160, 'Dune pattern')}</div><h3>The dune pattern</h3><p>The mark repeated on a slight tilt. For tissue paper, story backgrounds and the inside of the bag. Keep it at 10–15% so it reads as texture.</p></div>
 </div>
</section>''')

# =================================================================== PRODUCT & PACKAGING
# hang tag front
def tag_shape(fill): return f'<path d="M14,44 L58,12 H142 L186,44 V330 H14 Z" fill="{fill}"/>'
thread = (f'<circle cx="100" cy="40" r="8" fill="{NIGHT}"/>'
          f'<path d="M100,40 C112,8 150,-2 196,6" stroke="{EMBER}" stroke-width="1.6" fill="none"/>'
          f'<path d="M100,40 C94,20 76,6 56,2" stroke="{EMBER}" stroke-width="1.6" fill="none"/>')
tag_front = (tag_shape(BONE) + thread + mark(NIGHT, 100 - 31, 70, 0.62, accent=True) +
       f'<g font-family="{MONO}" font-weight="500" font-size="9.5" letter-spacing="1.1" fill="{NIGHT}" text-anchor="middle">'
       f'<text x="100" y="170">HEAVYWEIGHT HOODIE</text>'
       f'<text x="100" y="196" font-weight="400" font-size="7.6" letter-spacing=".7">COLOURWAY 01 — DUNE / SAND</text>'
       f'<text x="100" y="222">SIZE · M</text></g>'
       + stitch(30, 250, 170, 250, ASH, 1.4, '6 4') +
       T(100, 282, 'MADE IN ALGERIA', 9, NIGHT, MONO, 400, 'middle', 1.2) + wm_at(NIGHT, 100, 302, 8))
tag_back = (tag_shape(BONE) + thread +
       T(100, 96, 'Sewn by hand', 15, NIGHT, SANS, 700, 'middle') + T(100, 116, 'in Béchar.', 15, NIGHT, SANS, 700, 'middle') +
       T(100, 146, 'Cut and sewn after you', 10.5, NIGHT, SANS, 400, 'middle') + T(100, 161, 'ordered, in your size.', 10.5, NIGHT, SANS, 400, 'middle') +
       stitch(30, 186, 170, 186, ASH, 1.4, '6 4') +
       f'<g font-family="{MONO}" font-size="7.6" letter-spacing=".8" fill="{NIGHT}" text-anchor="middle">'
       f'<text x="100" y="212">WASH AT 30° · INSIDE OUT</text><text x="100" y="228">NO TUMBLE DRYER</text><text x="100" y="244">IRON INSIDE OUT</text></g>'
       f'<rect x="34" y="266" width="132" height="40" fill="none" stroke="{ASH}"/>'
       + T(42, 280, 'ORDER N°', 7, NIGHT, MONO, 500, 'start', 1) + T(42, 298, '________', 9, ASH, MONO))
# neck label
lab = [f'<rect width="300" height="120" fill="{NIGHT}"/>']
for y in range(3, 120, 3): lab.append(f'<line x1="0" y1="{y}" x2="300" y2="{y}" stroke="{BONE}" stroke-opacity=".05" stroke-width="1"/>')
lab.append(f'<path d="M0,0 h300 M0,120 h300" stroke="{ASH}" stroke-width="3" stroke-opacity=".6"/>')
wmt, wmw = wordmark(BONE, 36, 50, 20)
lab.append(wmt)
lab.append(f'<line x1="{36+wmw+20:.1f}" y1="38" x2="{36+wmw+20:.1f}" y2="82" stroke="{BONE}" stroke-opacity=".4"/>')
lab.append(T(f'{36+wmw+44:.1f}', 69, 'M', 22, BONE, MONO, 500, 'middle'))
label_svg = ''.join(lab)
# care label (side seam)
care = [f'<rect width="120" height="300" fill="{BONE}"/>']
for y in range(3, 300, 3): care.append(f'<line x1="0" y1="{y}" x2="120" y2="{y}" stroke="{NIGHT}" stroke-opacity=".035"/>')
care.append(f'<line x1="0" y1="24" x2="120" y2="24" stroke="{ASH}" stroke-dasharray="3 3"/>')
care.append(wm_at(NIGHT, 60, 42, 8.5))
care.append(f'<g font-family="{MONO}" font-size="7.4" letter-spacing=".7" fill="{NIGHT}" text-anchor="middle">'
            + ''.join(f'<text x="60" y="{y}">{t}</text>' for y, t in [(84, 'SIZE · M'), (112, 'WASH 30°'), (126, 'INSIDE OUT'), (148, 'NO TUMBLE'), (160, 'DRYER'), (182, 'IRON INSIDE'), (194, 'OUT'), (228, 'MADE IN'), (240, 'ALGERIA'), (262, 'BÉCHAR')]) + '</g>')
care_svg = ''.join(care)
# shipping bag + sticker
bag = [f'<path d="M20,30 H280 V350 H20 Z" fill="{NIGHT}"/>',
       f'<line x1="20" y1="58" x2="280" y2="58" stroke="{ASH}" stroke-opacity=".5" stroke-dasharray="3 3"/>',
       wm_at(BONE, 150, 180, 22), f'<circle cx="150" cy="232" r="4" fill="{EMBER}"/>',
       T(150, 326, 'BÉCHAR → 58 WILAYAS', 8.5, BONE, MONO, 400, 'middle', 1.5, ' fill-opacity=".75"'),
       f'<circle cx="250" cy="330" r="44" fill="{BONE}"/><circle cx="250" cy="330" r="38" fill="none" stroke="{ASH}" stroke-width=".8" stroke-dasharray="2 2"/>',
       mark_at(NIGHT, 250, 330, 42)]
bag_svg = ''.join(bag)
# cash-on-delivery shipping label
cod = [f'<rect width="320" height="210" fill="{BONE}"/>', f'<rect x=".5" y=".5" width="319" height="209" fill="none" stroke="{ASH}"/>',
       f'<rect width="320" height="40" fill="{NIGHT}"/>', wordmark(BONE, 16, 13, 13)[0],
       T(304, 25, 'PAIEMENT À LA LIVRAISON', 7.6, BONE, MONO, 500, 'end', .8)]
for k, (lbl, val) in enumerate([('NOM', ''), ('WILAYA / COMMUNE', ''), ('TÉLÉPHONE', ''), ('ARTICLE', 'PIÈCE 01 · M · DUNE / SAND')]):
    y = 62 + k*28
    cod.append(T(16, y, lbl, 6.6, NIGHT, MONO, 500, 'start', .8))
    cod.append(f'<line x1="16" y1="{y+12}" x2="200" y2="{y+12}" stroke="{ASH}" stroke-width=".8"/>')
    if val: cod.append(T(16, y + 9, val, 7.4, NIGHT, MONO, 400, 'start', .6))
cod += [f'<rect x="214" y="54" width="92" height="104" fill="none" stroke="{NIGHT}" stroke-width="1.4"/>',
        T(260, 72, 'MONTANT', 6.8, NIGHT, MONO, 500, 'middle', .8), T(260, 84, 'À PAYER', 6.8, NIGHT, MONO, 500, 'middle', .8),
        T(260, 128, '_____ DA', 11, NIGHT, MONO, 500, 'middle'),
        stitch(16, 184, 304, 184, ASH, 1, '5 4'), T(16, 200, 'EXPÉDITEUR · OSTRO · BÉCHAR', 6.6, NIGHT, MONO, 400, 'start', .8),
        mark_at(NIGHT, 296, 198, 14)]
cod_svg = ''.join(cod)
# thank-you card (A6 landscape)
ty_ = [f'<rect width="300" height="212" fill="{BONE}"/>', mark_at(NIGHT, 40, 44, 34),
       T(26, 104, 'MERCI.', 26, NIGHT, SANS, 800, 'start', 4),
       T(26, 130, 'Ta pièce a été coupée et cousue à Béchar,', 10.5, NIGHT), T(26, 145, 'après ta commande, à ta taille.', 10.5, NIGHT),
       stitch(26, 166, 274, 166, ASH, 1.2, '6 4'),
       T(26, 188, 'UN SOUCI DE TAILLE ? ÉCRIS-NOUS EN DM.', 7, NIGHT, MONO, 500, 'start', .8),
       T(26, 200, '@OSTRO.DZ', 7, NIGHT, MONO, 400, 'start', .8), f'<circle cx="270" cy="44" r="4" fill="{EMBER}"/>']
thanks_svg = ''.join(ty_)
# business card
bc_front = f'<rect width="350" height="200" fill="{NIGHT}"/>' + mark_at(BONE, 175, 100, 76)
bc_back = (f'<rect width="350" height="200" fill="{BONE}"/>' + wordmark(NIGHT, 28, 34, 16)[0] +
           T(28, 76, 'HEAVYWEIGHT MENSWEAR · BÉCHAR', 7.6, NIGHT, MONO, 500, 'start', 1.2) + stitch(28, 108, 322, 108, ASH, 1.2, '7 5') +
           f'<g font-family="{SANS}" font-size="10.5" fill="{NIGHT}"><text x="28" y="140">Commande en DM · Instagram @ostro.dz</text><text x="28" y="158">Livraison 58 wilayas</text><text x="28" y="176">Paiement à la livraison</text></g>')
# tissue paper with seal sticker
tissue = (dune_pattern('tis', NIGHT, BONE, 0.09, 90, 32) + '<rect width="300" height="220" fill="url(#tis)"/>' +
          f'<path d="M0,150 C80,120 200,180 300,140 V220 H0 Z" fill="{SAND}" fill-opacity=".55"/>' +
          f'<circle cx="150" cy="110" r="34" fill="{NIGHT}"/>' + mark_at(BONE, 150, 110, 38))
# stickers
stk = (f'<rect width="300" height="220" fill="{SAND}"/>' +
       f'<circle cx="74" cy="80" r="48" fill="{NIGHT}"/>' + mark_at(BONE, 74, 80, 54) +
       f'<circle cx="218" cy="80" r="48" fill="{BONE}"/>' + mark_at(NIGHT, 218, 80, 54) +
       f'<rect x="34" y="150" width="232" height="42" rx="21" fill="{BONE}"/>' +
       T(150, 176, 'MADE TO ORDER · BÉCHAR', 9, NIGHT, MONO, 500, 'middle', 1.4))

A(f'''<section class="panel">
 <p class="eyebrow">Product &amp; packaging</p>
 <h2>On the hoodie, in the bag, at the door</h2>
 <p class="lead">Everything the customer touches, from the label in the neck to the slip the delivery driver reads before they pay.</p>
 <div class="apps">
  <div class="app wide2"><div class="hoodies"><div>{svg(place_hoodie(0, 0, 400, DUNE, SAND, uid='a1'), 400, 380, 'Hoodie, Dune with Sand panels', 'hd')}<span class="lbl">Colourway 01 · Dune / Sand</span></div><div>{svg(place_hoodie(0, 0, 400, NIGHT, ASH, uid='a2'), 400, 380, 'Hoodie, Night with Ash panels', 'hd')}<span class="lbl">Colourway 02 · Night / Ash</span></div></div><span class="lbl">Heavyweight hoodie · front</span></div>
  <div class="app dk"><div class="pairsvg">{svg(tag_front, 200, 340, 'Hang tag front', 'tagsvg')}{svg(tag_back, 200, 340, 'Hang tag back', 'tagsvg')}</div><span class="lbl">Hang tag · front and back</span></div>
  <div class="app"><div class="stack">{svg(label_svg, 300, 120, 'Woven neck label', 'labsvg')}{svg(care_svg, 120, 300, 'Care label', 'caresvg')}</div><span class="lbl">Neck label + side-seam care label</span></div>
  <div class="app">{svg(bag_svg, 300, 380, 'Shipping bag and sticker', 'bagsvg')}<span class="lbl">Shipping bag + seal sticker</span></div>
  <div class="app">{svg(cod_svg, 320, 210, 'Cash-on-delivery shipping label', 'codsvg')}<span class="lbl">Shipping label · cash on delivery</span></div>
  <div class="app">{svg(thanks_svg, 300, 212, 'Thank-you card', 'cardsvg')}<span class="lbl">Thank-you card · A6, in every bag</span></div>
  <div class="app"><div class="cards">{svg(bc_front, 350, 200, 'Business card front')}{svg(bc_back, 350, 200, 'Business card back')}</div><span class="lbl">Business card · front and back</span></div>
  <div class="app">{svg(tissue, 300, 220, 'Tissue paper with seal', 'cardsvg')}<span class="lbl">Tissue paper + seal</span></div>
  <div class="app">{svg(stk, 300, 220, 'Sticker sheet', 'cardsvg')}<span class="lbl">Stickers</span></div>
 </div>
</section>''')
for nm, (inner, w, h) in {'hang-tag-front': (tag_front, 200, 340), 'hang-tag-back': (tag_back, 200, 340), 'neck-label': (label_svg, 300, 120),
                          'care-label': (care_svg, 120, 300), 'shipping-bag': (bag_svg, 300, 380), 'cod-shipping-label': (cod_svg, 320, 210),
                          'thank-you-card': (thanks_svg, 300, 212), 'business-card-front': (bc_front, 350, 200), 'business-card-back': (bc_back, 350, 200),
                          'stickers': (stk, 300, 220)}.items():
    EXPORTS[f'print/ostro-{nm}.svg'] = (inner, w, h)

# =================================================================== SOCIAL MEDIA
W_, H_ = 1080, 1350
def post_product():
    return (f'<rect width="{W_}" height="{H_}" fill="{BONE}"/>' + mark_at(NIGHT, 108, 108, 72) +
            T(1008, 120, '01 / 09', 24, ASH, MONO, 400, 'end', 3) +
            f'<rect x="72" y="190" width="936" height="900" fill="none" stroke="{ASH}" stroke-width="2" stroke-dasharray="10 10"/>' +
            place_hoodie(150, 250, 780, DUNE, SAND, uid='pp') + T(96, 1070, 'PRODUCT PHOTO', 20, ASH, MONO, 400, 'start', 3) +
            T(72, 1200, 'Heavy. Boxy. Made to order.', 54, NIGHT, SANS, 400) +
            T(72, 1262, 'PIÈCE 01 · DUNE / SAND', 24, NIGHT, MONO, 500, 'start', 3))
def post_voice():
    return (f'<rect width="{W_}" height="{H_}" fill="{NIGHT}"/>' +
            T(72, 520, 'Sewn by hand', 118, BONE, SANS, 700, 'start', -1) + T(72, 650, 'in Béchar.', 118, BONE, SANS, 700, 'start', -1) +
            stitch(72, 760, 420, 760, ASH, 4, '28 18') +
            T(72, 830, 'One hoodie at a time, after you order.', 38, BONE) +
            mark_at(BONE, 116, 1234, 88) + T(184, 1246, '@OSTRO.DZ', 24, ASH, MONO, 400, 'start', 3) +
            f'<circle cx="992" cy="1234" r="10" fill="{EMBER}"/>')
def post_launch():
    return (f'<rect width="{W_}" height="{H_}" fill="{DUNE}"/>' + T(72, 124, 'PIÈCE 01', 26, BONE, MONO, 500, 'start', 4) +
            T(72, 236, 'HEAVYWEIGHT', 92, BONE, SANS, 800, 'start', 9) + T(72, 340, 'HOODIE', 92, BONE, SANS, 800, 'start', 9) +
            place_hoodie(170, 400, 740, NIGHT, ASH, uid='pl') +
            f'<line x1="72" y1="1180" x2="1008" y2="1180" stroke="{SAND}" stroke-width="2"/>' +
            T(72, 1240, 'Two colours · S to XL · made to order', 34, BONE) +
            T(72, 1290, 'COMMANDE EN DM · PAIEMENT À LA LIVRAISON', 22, SAND, MONO, 500, 'start', 2.5))
def post_sizes():
    rows = ''.join(
        T(72, 560 + k*120, sz, 64, NIGHT, SANS, 800, 'start', 4) +
        ''.join(T(360 + j*230, 560 + k*120, '— cm', 36, NIGHT, MONO, 400) for j in range(3)) +
        f'<line x1="72" y1="{600 + k*120}" x2="1008" y2="{600 + k*120}" stroke="{ASH}" stroke-width="2" stroke-dasharray="14 9"/>'
        for k, sz in enumerate(['S', 'M', 'L', 'XL']))
    return (f'<rect width="{W_}" height="{H_}" fill="{BONE}"/>' + mark_at(NIGHT, 108, 108, 72) +
            T(72, 300, 'TAILLES', 110, NIGHT, SANS, 800, 'start', 14) +
            ''.join(T(360 + j*230, 440, t, 22, NIGHT, MONO, 500, 'start', 2.5) for j, t in enumerate(['POITRINE', 'LONGUEUR', 'MANCHE'])) + rows +
            T(72, 1150, 'Mesures prises à plat. Entre deux tailles ?', 36, NIGHT) +
            T(72, 1200, 'Envoie ta taille et ton poids en DM.', 36, NIGHT) +
            T(72, 1270, 'COUPE BOXY · TOMBE LARGE', 22, NIGHT, MONO, 500, 'start', 2.5))
POSTS = [('post-product', post_product(), 'Product · photo frame'), ('post-voice', post_voice(), 'Voice · one line'),
         ('post-launch', post_launch(), 'Launch · Pièce 01'), ('post-sizes', post_sizes(), 'Sizes · fill in the cm')]

SW, SH = 1080, 1920
def pill(cx, y, txt, bg, fg, w=520):
    return f'<rect x="{cx - w/2}" y="{y}" width="{w}" height="104" rx="52" fill="{bg}"/>' + T(cx, y + 64, txt, 34, fg, SANS, 700, 'middle')
def story_drop():
    return (f'<rect width="{SW}" height="{SH}" fill="{NIGHT}"/>' + mark_at(BONE, 540, 230, 110) +
            place_hoodie(110, 420, 860, DUNE, SAND, uid='sd') +
            T(540, 1360, 'PIÈCE 01', 120, BONE, SANS, 800, 'middle', 14) +
            T(540, 1440, 'Heavy. Boxy. Made to order.', 46, BONE, SANS, 400, 'middle') +
            pill(540, 1590, 'Commande en DM', BONE, NIGHT) + f'<circle cx="540" cy="1760" r="9" fill="{EMBER}"/>')
def story_order():
    steps = [('01', 'Choisis ta couleur :', 'Dune ou Night.'), ('02', 'Envoie ta taille', 'en DM.'), ('03', 'On coud ta pièce', 'à Béchar.'), ('04', 'Tu paies à la livraison,', '58 wilayas.')]
    out = f'<rect width="{SW}" height="{SH}" fill="{BONE}"/>' + mark_at(NIGHT, 140, 190, 96)
    out += T(80, 420, 'COMMENT', 96, NIGHT, SANS, 800, 'start', 10) + T(80, 520, 'COMMANDER', 96, NIGHT, SANS, 800, 'start', 10)
    for k, (n, a, b) in enumerate(steps):
        y = 700 + k*250
        out += T(80, y, n, 34, ASH, MONO, 500, 'start', 3) + T(200, y, a, 50, NIGHT) + T(200, y + 64, b, 50, NIGHT)
        out += stitch(80, y + 130, 1000, y + 130, ASH, 3, '28 18')
    return out + T(540, 1820, '@OSTRO.DZ', 28, NIGHT, MONO, 500, 'middle', 4)
def story_review():
    return (f'<rect width="{SW}" height="{SH}" fill="{SAND}"/>' + mark_at(NIGHT, 540, 200, 96) +
            T(80, 560, '«', 260, NIGHT, SANS, 700) +
            T(80, 720, 'Le texte de l’avis', 66, NIGHT, SANS, 700) + T(80, 800, 'du client ici,', 66, NIGHT, SANS, 700) + T(80, 880, 'mot pour mot.', 66, NIGHT, SANS, 700) +
            T(80, 990, '— PRÉNOM, WILAYA', 32, NIGHT, MONO, 500, 'start', 3) +
            f'<rect x="80" y="1100" width="920" height="560" rx="24" fill="none" stroke="{NIGHT}" stroke-opacity=".45" stroke-width="3" stroke-dasharray="16 12"/>' +
            T(540, 1390, 'CAPTURE DU MESSAGE', 28, NIGHT, MONO, 400, 'middle', 4, ' fill-opacity=".55"') +
            T(540, 1800, 'AVIS · PIÈCE 01', 28, NIGHT, MONO, 500, 'middle', 4))
STORIES = [('story-drop', story_drop(), 'New drop'), ('story-how-to-order', story_order(), 'How to order'), ('story-review', story_review(), 'Customer review')]

def highlight(kind):
    out = f'<rect width="1080" height="1080" fill="{NIGHT}"/>'
    if kind == 'piece':   out += place_hoodie(240, 260, 600, BONE, ASH, NIGHT, 'hl')
    if kind == 'sizes':   out += T(540, 600, 'S M L', 150, BONE, MONO, 500, 'middle', 10)
    if kind == 'reviews': out += T(540, 700, '« »', 330, BONE, SANS, 700, 'middle')
    if kind == 'delivery':out += T(540, 640, '58', 300, BONE, MONO, 500, 'middle') + T(540, 760, 'WILAYAS', 54, BONE, MONO, 500, 'middle', 8)
    if kind == 'order':   out += mark_at(BONE, 540, 540, 420)
    return out
HL = [('piece', 'Pièce 01'), ('sizes', 'Tailles'), ('reviews', 'Avis'), ('delivery', 'Livraison'), ('order', 'Commander')]

def avatar():
    return f'<rect width="1080" height="1080" fill="{NIGHT}"/>' + mark_at(BONE, 540, 540, 600)

FBW, FBH = 1640, 624
def fb_cover():
    return (dune_pattern('fbp', BONE, NIGHT, 0.06, 160, 54) + f'<rect width="{FBW}" height="{FBH}" fill="url(#fbp)"/>' +
            wordmark(BONE, 470, 210, 70)[0] +
            T(470, 370, 'Heavy boxy hoodies. Made to order.', 44, BONE) +
            T(470, 430, 'SEWN IN BÉCHAR · 58 WILAYAS · PAIEMENT À LA LIVRAISON', 22, ASH, MONO, 500, 'start', 2.6) +
            f'<circle cx="1490" cy="250" r="10" fill="{EMBER}"/>')

YW, YH = 2560, 1440
def yt_banner():
    sx, sy, sw_, sh_ = (YW - 1546)/2, (YH - 423)/2, 1546, 423
    return (f'<rect width="{YW}" height="{YH}" fill="{NIGHT}"/>' +
            f'<g opacity=".9">{cut_at(DUNE, 330, 720, 1500, 0)}{cut_at(DUNE, 2230, 720, 1500, 0)}</g>' +
            wordmark(BONE, sx + 120, sy + 110, 110)[0] +
            T(sx + 120, sy + 330, 'HEAVY BOXY HOODIES · MADE TO ORDER IN BÉCHAR', 34, BONE, MONO, 500, 'start', 4) +
            f'<circle cx="{sx + sw_ - 80}" cy="{sy + 320}" r="12" fill="{EMBER}"/>'), (sx, sy, sw_, sh_)
def yt_thumb():
    return (f'<rect width="1280" height="720" fill="{DUNE}"/>' + mark_at(BONE, 96, 96, 72) +
            T(64, 330, 'COMMENT ON', 82, BONE, SANS, 800, 'start', 6) + T(64, 430, 'COUD LA', 82, BONE, SANS, 800, 'start', 6) +
            T(64, 530, 'PIÈCE 01', 82, BONE, SANS, 800, 'start', 6) +
            T(64, 640, 'ÉPISODE 01 · L’ATELIER', 26, SAND, MONO, 500, 'start', 3) +
            place_hoodie(700, 120, 560, NIGHT, ASH, uid='yt'))

# instagram profile (phone view)
ig = [f'<rect width="320" height="460" rx="18" fill="{BONE}"/>',
      f'<rect x=".5" y=".5" width="319" height="459" rx="18" fill="none" stroke="{ASH}" stroke-opacity=".5"/>',
      T(20, 34, 'ostro.dz', 14, NIGHT, SANS, 700),
      f'<circle cx="56" cy="92" r="36" fill="{NIGHT}"/>', mark_at(BONE, 56, 92, 40),
      f'<g font-family="{SANS}" fill="{NIGHT}" text-anchor="middle">'
      f'<text x="150" y="90" font-weight="700" font-size="15">9</text><text x="150" y="106" font-size="10.5">posts</text>'
      f'<text x="210" y="90" font-weight="700" font-size="15">—</text><text x="210" y="106" font-size="10.5">followers</text>'
      f'<text x="270" y="90" font-weight="700" font-size="15">—</text><text x="270" y="106" font-size="10.5">following</text></g>',
      wordmark(NIGHT, 20, 142, 10)[0],
      f'<g font-family="{SANS}" font-size="11.5" fill="{NIGHT}"><text x="20" y="172">Heavy boxy hoodies. Made to order.</text><text x="20" y="189">Sewn in Béchar · Delivery 58 wilayas</text><text x="20" y="206">Paiement à la livraison</text></g>',
      f'<rect x="20" y="220" width="136" height="28" rx="7" fill="{NIGHT}"/>' + T(88, 238, 'Follow', 11, BONE, SANS, 700, 'middle'),
      f'<rect x="164" y="220" width="136" height="28" rx="7" fill="none" stroke="{ASH}"/>' + T(232, 238, 'Message', 11, NIGHT, SANS, 700, 'middle')]
for k, (kind, lbl) in enumerate(HL):
    cx = 40 + k*60
    ig.append(f'<circle cx="{cx}" cy="290" r="24" fill="none" stroke="{ASH}"/><clipPath id="hlc{k}"><circle cx="{cx}" cy="290" r="21"/></clipPath>'
              f'<g clip-path="url(#hlc{k})"><g transform="translate({cx-21},269) scale({42/1080:.5f})">{highlight(kind)}</g></g>')
    ig.append(T(cx, 330, lbl, 8.6, NIGHT, SANS, 400, 'middle'))
ig.append(f'<line x1="0" y1="348" x2="320" y2="348" stroke="{ASH}" stroke-opacity=".5"/>')
for k, (nm, inner, _) in enumerate(POSTS[:3]):
    x = k*107
    ig.append(f'<svg x="{x}" y="350" width="106" height="108" viewBox="0 0 1080 1350" preserveAspectRatio="xMidYMid slice">{inner}</svg>')
ig_svg = ''.join(ig)

def phone_frame(inner, w, h, label, cls):
    return svg(inner, w, h, label, cls)

posts_html = ''.join(f'<figure class="soc">{svg(inner, W_, H_, "Instagram post: " + cap)}<figcaption>{cap}<small>1080 × 1350</small></figcaption></figure>' for nm, inner, cap in POSTS)
stories_html = ''.join(f'<figure class="soc">{svg(inner, SW, SH, "Instagram story: " + cap)}<figcaption>{cap}<small>1080 × 1920</small></figcaption></figure>' for nm, inner, cap in STORIES)
hl_html = ''.join(f'<figure class="hl"><div class="hlc">{svg(highlight(k), 1080, 1080, "Highlight cover " + l)}</div><figcaption>{l}</figcaption></figure>' for k, l in HL)
ytb, (sx, sy, sw_, sh_) = yt_banner()
ytb_page = ytb + (f'<rect x="{sx}" y="{sy}" width="{sw_}" height="{sh_}" fill="none" stroke="{ASH}" stroke-width="4" stroke-dasharray="20 14"/>'
                  + T(sx + 12, sy - 18, 'SAFE AREA · VISIBLE ON EVERY DEVICE', 26, ASH, MONO, 500, 'start', 3))
fb_page = (f'<svg viewBox="0 0 {FBW} {FBH + 260}" role="img" aria-label="Facebook page with cover and profile picture">'
           f'<rect width="{FBW}" height="{FBH + 260}" fill="{BONE}"/>{fb_cover()}'
           f'<circle cx="190" cy="{FBH}" r="132" fill="{BONE}"/><circle cx="190" cy="{FBH}" r="122" fill="{NIGHT}"/>{mark_at(BONE, 190, FBH, 140)}'
           + T(350, FBH + 70, 'OSTRO', 52, NIGHT, SANS, 800, 'start', 14) + T(350, FBH + 124, 'Clothing brand · Béchar, Algeria', 30, NIGHT) +
           f'<rect x="350" y="{FBH + 160}" width="260" height="64" rx="12" fill="{NIGHT}"/>' + T(480, FBH + 202, 'Send message', 26, BONE, SANS, 700, 'middle') +
           f'<rect x="630" y="{FBH + 160}" width="200" height="64" rx="12" fill="none" stroke="{ASH}" stroke-width="2"/>' + T(730, FBH + 202, 'Follow', 26, NIGHT, SANS, 700, 'middle') +
           '</svg>')

A(f'''<section class="panel">
 <p class="eyebrow">Social media</p>
 <h2>One feed on every platform</h2>
 <p class="lead">Same avatar everywhere: the mark in Bone on a Night square, which each platform crops to a circle. Posts alternate between a product shot on Bone, one line of voice on Night, and the occasional Dune announcement, so the grid reads as a pattern. Text on templates is live type in Archivo and IBM Plex Mono, so it can be edited in Canva or Figma.</p>

 <h3 class="sub2">Instagram · profile and highlights</h3>
 <div class="igrow"><div class="igp">{svg(ig_svg, 320, 460, 'Instagram profile', 'igsvg')}</div>
  <div class="igside"><p class="note">Bio, word for word:</p><pre class="bio">Heavy boxy hoodies. Made to order.
Sewn in Béchar · Delivery 58 wilayas
Paiement à la livraison</pre>
  <div class="hls">{hl_html}</div><p class="note">Highlight covers: Night with one Bone sign each. Order them by what a new visitor asks first.</p></div></div>

 <h3 class="sub2">Instagram · posts</h3>
 <div class="posts">{posts_html}</div>

 <h3 class="sub2">Instagram · stories (also TikTok and WhatsApp status)</h3>
 <div class="stories">{stories_html}</div>

 <h3 class="sub2">Facebook · page</h3>
 <div class="wide-soc">{fb_page}<p class="note">Cover 1640 × 624. Keep the wordmark right of the profile picture, which covers the bottom-left corner on desktop.</p></div>

 <h3 class="sub2">YouTube · banner, thumbnail, avatar</h3>
 <div class="wide-soc">{svg(ytb_page, YW, YH, 'YouTube channel banner with safe area')}<p class="note">Banner 2560 × 1440. Phones show only the dashed safe area, so the name and line live inside it. The two Dune cuts fill the rest on TV.</p></div>
 <div class="ytrow"><figure class="soc">{svg(yt_thumb(), 1280, 720, 'YouTube thumbnail')}<figcaption>Thumbnail<small>1280 × 720</small></figcaption></figure>
  <figure class="soc av2">{svg(avatar(), 1080, 1080, 'Avatar').replace('<svg', '<svg style="border-radius:50%"', 1)}<figcaption>Avatar · all platforms<small>1080 × 1080</small></figcaption></figure></div>
</section>''')

for nm, inner, _ in POSTS: EXPORTS[f'social/ostro-ig-{nm}.svg'] = (inner, W_, H_)
for nm, inner, _ in STORIES: EXPORTS[f'social/ostro-ig-{nm}.svg'] = (inner, SW, SH)
for k, l in HL: EXPORTS[f'social/ostro-ig-highlight-{k}.svg'] = (highlight(k), 1080, 1080)
EXPORTS['social/ostro-avatar.svg'] = (avatar(), 1080, 1080)
EXPORTS['social/ostro-facebook-cover.svg'] = (fb_cover(), FBW, FBH)
EXPORTS['social/ostro-youtube-banner.svg'] = (ytb, YW, YH)
EXPORTS['social/ostro-youtube-thumbnail.svg'] = (yt_thumb(), 1280, 720)
