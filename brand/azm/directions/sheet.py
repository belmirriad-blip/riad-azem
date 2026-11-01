import sys; sys.path.insert(0,'.')
from m2 import A,B,B2,C,to_path
import shape
from shape import shaped_path
RP='ReadexPro%5BHEXP,wght%5D.ttf'
AR,_=shaped_path(RP,'عزم',100,0,0,{'wght':700,'HEXP':0},tracking=-2); ab=shape.LAST_BOUNDS
opts=[('A','Cut rings','Two ring segments with flat, cut ends. Geometric and calm, like an institution\'s seal.',A()),
      ('B','Square Kufic','The ع built on a grid, the way square Kufic is carved into tiles and walls. Rooted, serious, unmistakably Arabic.',B()),
      ('B2','Square Kufic, climbing','Same grid, but the end of the letter climbs in steps: the method, one step at a time.',B2()),
      ('C','Broad nib','A real calligrapher\'s ع: thick and thin strokes from a flat pen, sharp ends.',C())]
def mk(g,fill,h,tx=0,ty=0):
    x0,y0,x1,y1=g.bounds; s=h/(y1-y0)
    return f'<path fill="{fill}" fill-rule="evenodd" d="{to_path(g)}" transform="translate({tx:.1f},{ty:.1f}) scale({s:.4f}) translate({-x0:.1f},{-y0:.1f})"/>',(x1-x0)*s
def lockup(g,fill,bg):
    h=120; m,mw=mk(g,fill,h); x0,y0,x1,y1=ab; wh=h*0.9; ws=wh/(y1-y0); ww=(x1-x0)*ws; gap=36; pad=50
    W=ww+gap+mw+2*pad; H=h+2*pad
    word=f'<path fill="{fill}" d="{AR}" transform="translate({pad:.1f},{pad+(h-wh)/2+6:.1f}) scale({ws:.4f}) translate({-x0:.1f},{-y0:.1f})"/>'
    m,_=mk(g,fill,h,pad+ww+gap,pad)
    return f'<svg viewBox="0 0 {W:.0f} {H:.0f}" style="width:100%;display:block"><rect width="{W:.0f}" height="{H:.0f}" fill="{bg}"/>{word}{m}</svg>'
def icon(g,size):
    m,mw=mk(g,'#fff',size*0.56); x0,y0,x1,y1=g.bounds; s=size*0.56/(y1-y0)
    m,_=mk(g,'#fff',size*0.56,(size-mw)/2,size*0.22)
    return f'<svg viewBox="0 0 {size} {size}" width="{size}" height="{size}"><rect width="{size}" height="{size}" rx="{size*0.22:.0f}" fill="#2457D6"/>{m}</svg>'
cards=''
for k,n,d,g in opts:
    big,_=mk(g,'#2457D6',200)
    x0,y0,x1,y1=g.bounds; w=(x1-x0)*200/(y1-y0)
    cards+=f'''<div class="card"><div class="top"><span class="k">{k}</span><h2>{n}</h2></div>
<div class="row"><div class="big"><svg viewBox="-10 -10 {w+20:.0f} 220" style="height:150px">{big}</svg></div>
<div class="sm">{icon(g,72)}<div class="tiny"><svg viewBox="-10 -10 {w+20:.0f} 220" style="height:16px">{mk(g,'#2457D6',200)[0]}</svg><svg viewBox="-10 -10 {w+20:.0f} 220" style="height:32px">{mk(g,'#2457D6',200)[0]}</svg></div></div></div>
<div class="lk">{lockup(g,'#2457D6','#FFFFFF')}{lockup(g,'#FFFFFF','#121A2E')}</div><p>{d}</p></div>'''
html=f'''<html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Readex+Pro:wght@400;700&display=swap" rel="stylesheet"><style>
body{{margin:0;background:#F4F6FB;color:#121A2E;font-family:"Readex Pro",sans-serif;padding:44px;width:1400px;box-sizing:border-box}}
h1{{font-size:28px;margin:0 0 6px}} .sub{{color:#55607A;margin:0 0 28px;font-size:16px}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}
.card{{background:#fff;border:1px solid #DDE3EF;border-radius:14px;padding:24px}}
.top{{display:flex;gap:12px;align-items:center}} .k{{background:#2457D6;color:#fff;border-radius:8px;padding:2px 10px;font-weight:700}} h2{{margin:0;font-size:20px}}
.row{{display:flex;gap:24px;align-items:center;margin:18px 0}} .big{{flex:1;display:grid;place-items:center;background:#F4F6FB;border-radius:10px;padding:18px}}
.sm{{display:grid;gap:14px;justify-items:center}} .tiny{{display:flex;gap:10px;align-items:end}}
.lk{{display:grid;grid-template-columns:1fr 1fr;gap:10px}} .lk svg{{border-radius:8px;border:1px solid #DDE3EF}}
p{{color:#55607A;margin:14px 0 0;font-size:15px;line-height:1.6}}
</style></head><body><h1>Azm · new mark directions</h1><p class="sub">Four sharper, more serious takes on the ع. Each one shown large, as the app icon, at 16 and 32 px, and next to عزم.</p><div class="grid">{cards}</div></body></html>'''
open('sheet.html','w').write(html)
