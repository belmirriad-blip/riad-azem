import json,sys
P=json.load(open('parts.json'))
C=dict(forest='#123F35',offwhite='#F4F0E6',spice='#E0663F',taupe='#B3A28E',charcoal='#232323')
sw=[('Forest','forest','#123F35','Primary · 25%','Mark, packaging, headers'),
    ('Off-white','offwhite','#F4F0E6','Ground · 60%','Paper, labels, backgrounds'),
    ('Charcoal','charcoal','#232323','Text · 8%','Body copy, fine print'),
    ('Taupe','taupe','#B3A28E','Support · 5%','Linen, borders, stitches'),
    ('Spice','spice','#E0663F','Accent · 2%','The fang colour, one detail per piece')]
swh=''.join(f'<div class="sw" style="--c:{h}"><div class="chip"></div><div class="swt"><b>{n}</b><code>{h}</code><span>{r}</span><small>{u}</small></div></div>' for n,k,h,r,u in sw)
combos=[('forest','offwhite'),('offwhite','forest'),('charcoal','spice'),('taupe','charcoal'),('spice','offwhite'),('offwhite','charcoal')]
mk={'offwhite':P['MARK_OFF'],'forest':P['MARK_FOR'],'spice':P['MARK_SPI'],'charcoal':P['MARK_CHA']}
comboh=''.join(f'<div class="combo" style="background:{C[b]}">{mk[f]}</div>' for b,f in combos)
pairs=[
 ('Recommended','Archivo ExtraBold','Josefin Sans','font-family:Archivo,sans-serif;font-weight:800;text-transform:uppercase;letter-spacing:.14em','font-family:"Josefin Sans",sans-serif','Couture sur mesure','Archivo ExtraBold is the face of the wordmark: wide-tracked capitals that sit well next to the sharp D. Josefin Sans, light and spaced, carries everything else.'),
 ('Alternative','Forum','Outfit','font-family:Forum,serif;text-transform:uppercase;letter-spacing:.12em','font-family:Outfit,sans-serif;font-weight:300','Couture sur mesure','Forum\'s capitals look carved and ceremonial. Use them for formal and evening collections.'),
 ('Alternative','Instrument Serif Italic','Outfit','font-family:"Instrument Serif",serif;font-style:italic','font-family:Outfit,sans-serif;font-weight:300','Une pièce, un client','Softer and more personal. Good for Instagram captions and stories.'),
]
pairh=''.join(f'''<article class="pair{' rec' if i==0 else ''}"><p class="eyebrow">{t}</p><p class="spec" style='{ds}'>{s}</p>
<p class="body" style='{bs}'>Each piece is drafted to one man's measurements, cut by hand and fitted in person at the atelier in Béchar.</p>
<p class="names"><span>{d}</span><span>+</span><span>{b}</span></p><p class="why">{w}</p></article>''' for i,(t,d,b,ds,bs,s,w) in enumerate(pairs))
html=f'''<title>DORIAN Brand Identity</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;800&family=Fraunces:opsz,wght@9..144,300;9..144,400&family=Josefin+Sans:wght@300;400;600&family=Forum&family=Outfit:wght@300;400&family=Instrument+Serif:ital@0;1&family=Pinyon+Script&display=swap" rel="stylesheet">
<style>
/* Layout: dark studio board of rounded panels, like a designer's presentation wall */
:root{{color-scheme:dark;
 --board:#161615;--panel:#1F1F1D;--line:#2E2D2A;--ink:#EDE8DC;--muted:#9C978B;
 --forest:#123F35;--offwhite:#F4F0E6;--spice:#E0663F;--taupe:#B3A28E;--charcoal:#232323;
 --display:Fraunces,"Times New Roman",serif;--sans:"Josefin Sans","Futura","Century Gothic",sans-serif;--script:"Pinyon Script",cursive;}}
*{{box-sizing:border-box}}
body{{background:var(--board);color:var(--ink);font-family:var(--sans);font-size:15px;line-height:1.6;margin:0}}
.wrap{{max-width:1180px;margin:0 auto;padding-inline:16px;padding-block:28px 64px;display:grid;gap:18px}}
.panel{{background:var(--panel);border-radius:18px;padding:clamp(20px,4vw,44px);min-width:0;overflow:hidden}}
.grid2{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,420px),1fr));gap:18px}}
h1,h2{{font-family:var(--display);font-weight:300;margin:0;text-wrap:balance;font-variation-settings:"opsz" 144}}
h2{{font-size:clamp(26px,3.4vw,38px);line-height:1.1}}
.eyebrow{{font-size:11px;letter-spacing:.28em;text-transform:uppercase;color:var(--muted);margin:0 0 10px}}
.lead{{color:var(--muted);max-width:62ch;margin:10px 0 0}}
svg{{display:block;max-width:100%;height:auto}}
/* hero */
.hero{{background:var(--offwhite);color:var(--charcoal);display:grid;place-items:center;gap:22px;padding-block:clamp(48px,9vw,110px)}}
.hero .hw{{width:min(78%,300px)}}.hero .hp{{width:min(70%,340px)}}
.hero .ic{{width:clamp(110px,16vw,150px);filter:drop-shadow(0 18px 30px rgba(18,63,53,.28))}}
.hero .tag{{font-size:12px;letter-spacing:.42em;text-transform:uppercase;color:#5b574f;text-align:center}}
.hero .tag b{{font-weight:600;color:var(--charcoal)}}
.hero .story{{font-family:var(--script);font-size:26px;color:var(--spice);margin:0}}
/* construction & sketches */
.constr{{background:#1A1A18}}
.constr svg{{width:100%;margin-top:24px}}
.sketch{{background:#FBF9F3;color:var(--charcoal)}}
.sketch .lead{{color:#6f6a60}}
.sketch svg{{margin-top:18px;width:100%;max-width:980px;margin-inline:auto}}
.geo{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,360px),1fr));gap:24px;align-items:center}}.geo>div{{min-width:0}}.gridp svg{{width:min(100%,400px);margin:0 auto}}
/* logo suite */
.suite{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,230px),1fr));gap:14px;margin-top:24px}}
.tile{{border-radius:14px;display:grid;place-items:center;padding:36px 24px;min-height:220px;position:relative}}
.tile .cap{{position:absolute;left:16px;bottom:10px;font-size:10px;letter-spacing:.25em;text-transform:uppercase;opacity:.6}}
.tile .mk{{height:150px;width:auto}} .tile .wm{{width:min(100%,280px)}} .tile .lk{{width:min(100%,300px)}} .tile.wide{{grid-column:1/-1;min-height:300px}} .tile.wide .wm{{width:min(100%,520px)}} .tile .st{{height:170px;width:auto}}
.t-off{{background:var(--offwhite);color:var(--charcoal)}} .t-for{{background:var(--forest);color:var(--offwhite)}} .t-cha{{background:var(--charcoal);color:var(--offwhite)}}
.sizes{{display:flex;align-items:flex-end;gap:26px;flex-wrap:wrap;margin-top:22px}}
.sizes svg{{width:auto}}
.sizes small{{display:block;font-size:10px;color:var(--muted);letter-spacing:.15em;margin-top:6px}}
/* details */
.devices{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,240px),1fr));gap:14px;margin-top:24px}}
.dev{{background:#262624;border-radius:14px;padding:22px;display:grid;gap:14px;align-content:start}}
.dev .art{{height:110px;display:grid;place-items:center;border-radius:10px;background:var(--offwhite)}}
.dev .art.dk{{background:var(--forest)}}
.dev h3{{margin:0;font-family:var(--display);font-weight:400;font-size:20px}}
.dev p{{margin:0;color:var(--muted);font-size:14px}}
.ac{{height:70px;width:auto}}
.stitch{{width:80%;height:4px;background:repeating-linear-gradient(90deg,var(--spice) 0 14px,transparent 14px 23px);border-radius:2px}}
.pattern svg{{width:100%;border-radius:10px}}
/* palette */
.sws{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,190px),1fr));gap:12px;margin-top:24px}}
.sw{{border-radius:14px;overflow:hidden;background:#262624}}
.chip{{height:120px;background:var(--c)}}
.swt{{padding:14px 16px;display:grid;gap:2px}}
.swt b{{font-family:var(--display);font-weight:400;font-size:19px}}
.swt code{{font-family:var(--sans);color:var(--muted);font-size:13px;letter-spacing:.08em}}
.swt span{{font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--taupe);margin-top:6px}}
.swt small{{color:var(--muted);font-size:13px;line-height:1.4}}
.ratio{{display:flex;height:14px;border-radius:7px;overflow:hidden;margin-top:20px}}
.combos{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,150px),1fr));gap:12px;margin-top:14px}}
.combo{{border-radius:14px;aspect-ratio:1;display:grid;place-items:center;max-width:100%}}
.combo .mk{{height:52%;width:auto}}
/* type */
.pairs{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr));gap:14px;margin-top:24px}}
.pair{{background:#262624;border-radius:14px;padding:26px;display:grid;gap:12px;align-content:start;border:1px solid transparent}}
.pair.rec{{border-color:var(--spice)}}
.pair.rec .eyebrow{{color:var(--spice)}}
.spec{{font-size:clamp(28px,3.2vw,36px);line-height:1.1;margin:0;color:var(--ink)}}
.pair .body{{margin:0;color:#c9c3b6;font-size:15px}}
.names{{display:flex;gap:10px;font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--taupe);margin:0}}
.why{{margin:0;color:var(--muted);font-size:14px}}
.script{{margin-top:18px;display:flex;gap:16px;align-items:baseline;flex-wrap:wrap;border-top:1px solid var(--line);padding-top:18px}}
.script span{{font-family:var(--script);font-size:38px;color:var(--spice)}}
.script small{{color:var(--muted)}}
/* applications */
.apps{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:14px;margin-top:24px;align-items:center}}
.app{{background:#2A2926;border-radius:14px;padding:28px;display:grid;gap:12px;place-items:center;min-height:300px}}
.app svg{{box-shadow:0 14px 34px rgba(0,0,0,.35)}}
.app .lbl{{font-size:10px;letter-spacing:.25em;text-transform:uppercase;color:var(--muted)}}
.cards{{display:grid;gap:12px;width:100%}}
.av svg{{width:150px;border-radius:50%}}
.icons{{display:flex;gap:14px;flex-wrap:wrap;justify-content:center}} .icons svg{{width:84px;box-shadow:none;filter:drop-shadow(0 10px 18px rgba(0,0,0,.4))}}
.files{{columns:2 260px;color:var(--muted);font-size:13px;margin:16px 0 0;padding-left:18px}}
.files code{{color:var(--ink)}}
@media (prefers-reduced-motion:no-preference){{.hero .hw{{width:min(78%,300px)}}.hero .hp{{width:min(70%,340px)}}
.hero .ic{{animation:rise .9s cubic-bezier(.2,.7,.2,1) both}}@keyframes rise{{from{{transform:translateY(10px)}}to{{transform:none}}}}}}
</style>
<main class="wrap">
<section class="panel hero" aria-label="DORIAN">
 {P['PRI_FOR'].replace('class="st"','class="hp"')}
 <div class="tag">COUTURE SUR MESURE</div>
 <p class="story">de mère en fils, cousu main</p>
</section>

<section class="panel constr">
 <p class="eyebrow">01 · The idea</p>
 <h2>The D is a blade with a fang.</h2>
 <p class="lead">There is no straight stem. One curved blade wraps the whole letter: thick on the right, sharpened to a gothic point at the belly, and thinning into two claws on the left. The stem is a fang hanging from the top bar. It stops short of the bottom, so nothing runs through the letter and nothing crosses.</p>
 {P['CONSTR']}
</section>

<section class="panel sketch">
 <p class="eyebrow" style="color:#8a8478">02 · Sketches</p>
 <h2>Eight Ds on the way to the fang</h2>
 <p class="lead">Two crescents, split blades, wings, a leaf, a leaf pushed through the bars, a pointed belly. The early ones read as “))” or as an eye, and the pierced leaf put a line through the letter. Hanging the blade from the top bar as a fang was the one that read as a D at 20 pixels.</p>
 {P['SKETCH']}
</section>
<section class="panel gridp geo">
 <div><p class="eyebrow">03 · Geometry</p>
 <h2>One blade, one fang</h2>
 <p class="lead">The bowl runs from the cap line to the baseline with no overshoot, so it sits level with the capitals next to it. The belly comes to a point on the right instead of a round curve. The fang's tip stops on its own line, well clear of the bottom bar.</p></div>
 {P['GRID']}
</section>

<section class="panel">
 <p class="eyebrow">04 · Logo suite</p>
 <h2>The mark lives inside the name</h2>
 <p class="lead">The logo sits above the name, and the first D of DORIAN is the logo itself, set at the height of the capitals in Archivo ExtraBold. Inside the name the D is cut slightly heavier so it matches the weight of the letters next to it. Use the D alone where space is tight: the profile picture, a woven label, a button.</p>
 <div class="suite">
  <div class="tile t-off wide">{P['PRI_FOR']}<span class="cap">Primary: logo above the name</span></div>
  <div class="tile t-for">{P['MARK_OFF']}<span class="cap">Mark</span></div>
  <div class="tile t-for">{P['WORD_OFF']}<span class="cap">Wordmark, reversed</span></div>
  <div class="tile t-off">{P['TAG_FOR']}<span class="cap">With tagline</span></div>
  <div class="tile t-cha">{P['WORD_SPI']}<span class="cap">Wordmark, spice</span></div>
 </div>
 <div class="sizes" aria-label="Small size test">
  <div>{P['SIZES'][0].replace('<svg ','<svg style="height:96px" ')}<small>96 px</small></div>
  <div>{P['SIZES'][1].replace('<svg ','<svg style="height:48px" ')}<small>48 px</small></div>
  <div>{P['SIZES'][2].replace('<svg ','<svg style="height:32px" ')}<small>32 px</small></div>
  <div>{P['SIZES'][3].replace('<svg ','<svg style="height:20px" ')}<small>20 px</small></div>
  <div>{P['WORD_SIZES'].replace('<svg ','<svg style="height:30px" ')}<small>Wordmark, 30 px</small></div>
 </div>
</section>

<section class="panel">
 <p class="eyebrow">05 · Signature details</p>
 <h2>Small things that repeat</h2>
 <p class="lead">Viral Toolkit reuses its play button everywhere. DORIAN does the same with three details taken from the mark, used one at a time.</p>
 <div class="devices">
  <div class="dev"><div class="art">{P['ACCENT']}</div><h3>The fang</h3><p>Lifted from the D. Use it as a bullet, a cursor, or a sticker on stories, tilted 12°.</p></div>
  <div class="dev"><div class="art dk"><div class="stitch"></div></div><h3>The running stitch</h3><p>A dashed line of 14-unit stitches and 9-unit gaps. It replaces plain rules and dividers.</p></div>
  <div class="dev pattern"><div class="art dk" style="padding:0;overflow:hidden">{P['PATTERN']}</div><h3>The fang pattern</h3><p>For tissue paper, garment bags and story backgrounds. Keep it at 10–15% opacity.</p></div>
 </div>
</section>

<section class="panel">
 <p class="eyebrow">06 · Colour</p>
 <h2>Five colours, mostly off-white and forest</h2>
 <p class="lead">Spice orange is the accent: one per piece, on the hang tag, the packaging or a single print, never a background for long text.</p>
 <div class="sws">{swh}</div>
 <div class="ratio" aria-label="Usage ratio"><i style="flex:60;background:var(--offwhite)"></i><i style="flex:25;background:var(--forest)"></i><i style="flex:8;background:var(--charcoal);outline:1px solid #444"></i><i style="flex:5;background:var(--taupe)"></i><i style="flex:2;background:var(--spice)"></i></div>
 <p class="eyebrow" style="margin-top:30px">Approved pairings</p>
 <div class="combos">{comboh}</div>
</section>

<section class="panel">
 <p class="eyebrow">07 · Typography</p>
 <h2>Three pairings from your Google Fonts list</h2>
 <p class="lead">Each pair is a strong face for headlines plus a quieter one for everything else. Pick one pair and stick to it.</p>
 <div class="pairs">{pairh}</div>
 <div class="script"><span>fait main, avec amour</span><small>Pinyon Script: a hand-written signature for tags and thank-you cards only. Never for headlines.</small></div>
</section>

<section class="panel">
 <p class="eyebrow">08 · In use</p>
 <h2>On the clothes and on the feed</h2>
 <div class="apps">
  <div class="app"><div class="cards">{P['CARD_F']}{P['CARD_B']}</div><span class="lbl">Business card</span></div>
  <div class="app">{P['LABEL']}<span class="lbl">Woven neck label</span></div>
  <div class="app">{P['TAG']}<span class="lbl">Hang tag</span></div>
  <div class="app"><div class="av">{P['AVATAR']}</div><div class="icons">{''.join(P['ICONS'])}</div><span class="lbl">Instagram &amp; app icons</span></div>
 </div>
</section>

<section class="panel">
 <p class="eyebrow">Files</p>
 <h2>Vector files in the repo</h2>
 <p class="lead">Every logo is outlined SVG, so it prints and embroiders without needing the fonts installed. They are in <code>brand/dorian/svg/</code> on the <code>claude/doria-logo-design-kyuigf</code> branch, with the social media pack in <code>brand/dorian/social/</code>.</p>
 <ul class="files"><li><code>dorian-primary-*.svg</code>: the logo above the name</li><li><code>dorian-wordmark-*.svg</code>: DORIAN with the fang D</li><li><code>dorian-mark-*.svg</code>: the D on its own</li><li><code>dorian-wordmark-tagline-*.svg</code></li><li><code>dorian-app-icon-*.svg</code></li><li><code>dorian-chest-print-80mm-*.svg</code></li></ul>
</section>
</main>'''
open(sys.argv[1],'w').write(html)
