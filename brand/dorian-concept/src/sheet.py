import sys; sys.path.insert(0,'.')
from fang import fang_D
from pen import to_path
from glyphs import text_path, metrics
C=dict(forest='#123F35',offwhite='#F4F0E6',spice='#E0663F',charcoal='#232323')
def vb(g,p=6):
    x0,y0,x1,y1=g.bounds; return f"{x0-p:.1f} {y0-p:.1f} {x1-x0+2*p:.1f} {y1-y0+2*p:.1f}", (x0,y0,x1,y1)
M=fang_D(); D=to_path(M); V,(x0,y0,x1,y1)=vb(M)
AR='Archivo%5Bwdth,wght%5D.ttf'; AX={'wght':800,'wdth':100}
WD,WW=text_path(AR,'DORIAN',100,0,100,tracking=32,axes=AX); cap=100*metrics(AR,AX)['cap']; ww=WW-32
def lockup(fg,bg):
    mw=x1-x0; s=ww*0.40/mw; mh=(y1-y0)*s; pad=70; gap=cap
    W=ww+2*pad; H=mh+gap+cap+2*pad
    return f'<svg viewBox="0 0 {W:.0f} {H:.0f}"><rect width="{W:.0f}" height="{H:.0f}" fill="{bg}"/><path fill="{fg}" d="{D}" transform="translate({pad+(ww-mw*s)/2:.1f},{pad}) scale({s:.4f}) translate({-x0:.1f},{-y0:.1f})"/><path fill="{fg}" d="{WD}" transform="translate({pad},{pad+mh+gap-(100-cap):.1f})"/></svg>'
def tile(fg,bg,lbl): return f'<div class="t" style="background:{bg}"><svg viewBox="{V}"><path fill="{fg}" d="{D}"/></svg><span style="color:{fg}">{lbl}</span></div>'
alts=[('Belly: pointed (chosen)',fang_D()),('Belly: round',fang_D(point=False)),('Heavier',fang_D(belly=122,inner=90,fang_w=36))]
alth=''.join(f'<div class="a"><svg viewBox="{vb(g)[0]}"><path fill="#F4F0E6" d="{to_path(g)}"/></svg><span>{l}</span></div>' for l,g in alts)
sizes=''.join(f'<div class="s"><svg viewBox="{V}" style="height:{h}px"><path fill="#F4F0E6" d="{D}"/></svg><small>{h}px</small></div>' for h in (96,48,32,20))
ic=f'<svg viewBox="0 0 100 100" style="width:32px"><rect width="100" height="100" rx="22" fill="{C["forest"]}"/><svg x="16" y="18" width="68" height="64" viewBox="{V}"><path fill="#F4F0E6" d="{D}"/></svg></svg>'
ic96=ic.replace('width:32px','width:96px')
html=f'''<html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;800&display=swap" rel="stylesheet"><style>
body{{margin:0;background:#121413;color:#ECE8DE;font-family:Archivo,Arial,sans-serif;padding:40px;width:1400px;box-sizing:border-box}}
h1{{font-size:26px;letter-spacing:.08em;margin:0 0 4px}} p{{color:#959C97;margin:0 0 28px;font-size:15px}}
.row{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:14px}}
.t{{border-radius:14px;padding:40px 30px 16px;display:grid;justify-items:center;gap:14px}} .t svg{{height:220px}}
.t span,.a span,small{{font-size:11px;letter-spacing:.2em;text-transform:uppercase;font-weight:500}}
.l{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:14px}} .l svg{{width:100%;border-radius:14px;display:block}}
.b{{display:grid;grid-template-columns:1.2fr 1fr;gap:14px}}
.box{{background:#1B1E1C;border-radius:14px;padding:24px}} .box h2{{font-size:12px;letter-spacing:.25em;color:#959C97;margin:0 0 18px;font-weight:500}}
.alts{{display:flex;gap:26px}} .a{{display:grid;gap:10px;justify-items:center;color:#959C97}} .a svg{{height:120px}}
.sz{{display:flex;gap:26px;align-items:flex-end}} .s{{display:grid;gap:8px;justify-items:center;color:#959C97}}
</style></head><body>
<h1>DORIAN · FANG D · CONCEPT</h1>
<p>One blade wraps the letter and ends in two claws. The stem is a fang hanging from the top bar. It stops short of the bottom, so nothing runs through the letter and nothing crosses.</p>
<div class="row">{tile(C['offwhite'],C['forest'],'Main')}{tile(C['forest'],C['offwhite'],'Main')}{tile(C['spice'],C['charcoal'],'Accent')}{tile(C['spice'],C['offwhite'],'Accent')}</div>
<div class="l">{lockup(C['offwhite'],C['forest'])}{lockup(C['forest'],C['offwhite'])}</div>
<div class="b"><div class="box"><h2>VARIANTS</h2><div class="alts">{alth}</div></div>
<div class="box"><h2>SMALL SIZES</h2><div class="sz">{sizes}<div class="s">{ic96}<small>icon 96</small></div><div class="s">{ic}<small>icon 32</small></div></div></div></div>
</body></html>'''
open('sheet.html','w').write(html)
