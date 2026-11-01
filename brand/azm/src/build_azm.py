import os, sys, json, glob
sys.path.insert(0,'.')
from marks import MARKS, to_path
from shape import shaped_path
OUT=sys.argv[1]
for sub in ('svg','png','icons','social'):
    os.makedirs(os.path.join(OUT,sub),exist_ok=True)
    for f in glob.glob(os.path.join(OUT,sub,'*')): os.remove(f)
C=dict(blue='#2457D6',paper='#F4F6FB',amber='#F0A23B',slate='#A7B1C6',ink='#121A2E',white='#FFFFFF')
RP='ReadexPro%5BHEXP,wght%5D.ttf'; RX={'wght':700,'HEXP':0}
def norm(g):
    x0,y0,x1,y1=g.bounds; return to_path(g),x0,y0,x1-x0,y1-y0
M={k:norm(g) for k,g in MARKS.items()}
MD,mx,my,MW,MH=M['1']
def mark(fill,h,tx,ty,key='1'):
    d,x0,y0,w,hh=M[key]; s=h/hh
    return f'<path fill="{fill}" d="{d}" transform="translate({tx:.2f},{ty:.2f}) scale({s:.4f}) translate({-x0:.2f},{-y0:.2f})"/>', w*s
# wordmarks (outlined, shaped)
import shape
AR,ARW=shaped_path(RP,'عزم',100,0,0,RX,tracking=-2); ab=shape.LAST_BOUNDS
LA,LAW=shaped_path(RP,'Azm',100,0,0,RX,tracking=-1); lb=shape.LAST_BOUNDS
from fontTools.pens.boundsPen import BoundsPen
def bbox(d):
    import re
    nums=[float(v) for v in re.findall(r'-?\d+\.?\d*',d)]
    xs,ys=nums[0::2],nums[1::2]; return min(xs),min(ys),max(xs),max(ys)
def word(d,b,fill,h,tx,ty):  # scale glyph bbox to height h
    x0,y0,x1,y1=b; s=h/(y1-y0)
    return f'<path fill="{fill}" d="{d}" transform="translate({tx:.2f},{ty:.2f}) scale({s:.4f}) translate({-x0:.2f},{-y0:.2f})"/>',(x1-x0)*s
def bg(w,h,c,r=0): return f'<rect width="{w:.1f}" height="{h:.1f}" rx="{r}" fill="{c}"/>' if c else ''
def doc(w,h,inner,t): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.1f} {h:.1f}"><title>{t}</title>{inner}</svg>'
def save(n,inner,w,h,t='Azm'): open(os.path.join(OUT,'svg',n),'w').write(doc(w,h,inner,t))
# layouts; clear space = height of the ع bowl ≈ 0.45*MH
CS=lambda h: h*0.45
def L_mark(fill,bgc=None,h=200,pad=None):
    pad=CS(h) if pad is None else pad; m,w=mark(fill,h,pad,pad); W,H=w+2*pad,h+2*pad
    return bg(W,H,bgc)+m,W,H
def L_ar(fill,bgc=None,h=200,pad=None):
    """RTL: mark on the right, عزم on the left"""
    pad=CS(h) if pad is None else pad
    wh=h*0.92; wd,ww=word(AR,ab,fill,wh,0,0); gap=h*0.22; mw=MW*h/MH
    W=ww+gap+mw+2*pad; H=h+2*pad
    wd,_=word(AR,ab,fill,wh,pad,pad+(h-wh)/2+h*0.06)
    m,_=mark(fill,h,pad+ww+gap,pad)
    return bg(W,H,bgc)+wd+m,W,H
def L_lat(fill,bgc=None,h=200,pad=None):
    pad=CS(h) if pad is None else pad
    lh=h*0.56; mw=MW*h/MH; gap=h*0.22
    m,_=mark(fill,h,pad,pad); wd,lw=word(LA,lb,fill,lh,pad+mw+gap,pad+(h-lh)/2+h*0.05)
    W=mw+gap+lw+2*pad; H=h+2*pad
    return bg(W,H,bgc)+m+wd,W,H
VERS=[('blue-on-white','blue','white'),('white-on-blue','white','blue'),('white-on-ink','white','ink'),('ink','ink',None)]
for nm,f,b in VERS:
    for ln,L in (('mark',L_mark),('lockup-arabic',L_ar),('lockup-latin',L_lat)):
        i,w,h=L(C[f],C[b] if b else None); save(f'azm-{ln}-{nm}.svg',i,w,h)
for k in ('2','3'):
    i,w,h=(lambda: (lambda m: (m[0],m[1]+2*CS(200),200+2*CS(200)))(mark(C['blue'],200,CS(200),CS(200),k)))()
    save(f'azm-mark-variation-{k}-blue.svg',i,w,h)
# app icons
def icon(size,bgc,fg,frac=0.56,r=None):
    r=size*0.22 if r is None else r; h=size*frac; mw=MW*h/MH
    m,_=mark(fg,h,(size-mw)/2,(size-h)/2)
    return bg(size,size,bgc,r)+m
open(os.path.join(OUT,'icons','favicon.svg'),'w').write(doc(64,64,icon(64,C['blue'],C['white'],0.62,14),'Azm'))
ICONS={'icon-512':(512,icon(512,C['blue'],C['white'])),'icon-192':(192,icon(192,C['blue'],C['white'])),
       'apple-touch-icon':(180,icon(180,C['blue'],C['white'],0.56,0)),
       'maskable-512':(512,icon(512,C['blue'],C['white'],0.42,0)),'maskable-192':(192,icon(192,C['blue'],C['white'],0.42,0)),
       'favicon-32':(32,icon(32,C['blue'],C['white'],0.66,7)),'favicon-16':(16,icon(16,C['blue'],C['white'],0.70,3.5)),
       'azm-1024':(1024,icon(1024,C['blue'],C['white'])),'icon-512-ink':(512,icon(512,C['ink'],C['white']))}
os.makedirs('iconsrc',exist_ok=True)
for f in glob.glob('iconsrc/*'): os.remove(f)
for n,(s,i) in ICONS.items(): open(f'iconsrc/{n}.svg','w').write(doc(s,s,i,'Azm'))
# parts for the board
def inl(t,label,cls=''):
    i,w,h=t; return f'<svg class="{cls}" viewBox="0 0 {w:.1f} {h:.1f}" role="img" aria-label="{label}">{i}</svg>'
P={}
P['VARS']=[]
for k,lbl in (('1','Rising curve'),('2','Geometric'),('3','Light')):
    m,w=mark(C['blue'],200,0,0,k); P['VARS'].append((k,lbl,f'<svg viewBox="-20 -20 {w+40:.1f} 240" role="img" aria-label="Variation {k}">{m}</svg>',
        f'<svg viewBox="-20 -20 {w+40:.1f} 240" style="height:16px" aria-hidden="true">{mark(C["blue"],200,0,0,k)[0]}</svg>'))
for nm,f,b in VERS:
    P['AR_'+nm]=inl(L_ar(C[f],C[b] if b else None),'Azm Arabic lockup','lk')
P['LAT']=inl(L_lat(C['blue']),'Azm Latin lockup','lk'); P['MARK']=inl(L_mark(C['blue']),'Azm mark','mk')
P['MARK_W']=inl(L_mark(C['white']),'Azm mark','mk')
P['HERO']=inl(L_ar(C['white'],None,200,20),'عزم','hero-lk')
# clear-space diagram
h=200; i,w,hh=L_ar(C['blue'],None,h); pad=CS(h)
P['CLEAR']=f'''<svg viewBox="0 0 {w:.1f} {hh:.1f}" role="img" aria-label="Clear space">{i}
<rect x="{pad:.1f}" y="{pad:.1f}" width="{w-2*pad:.1f}" height="{hh-2*pad:.1f}" fill="none" stroke="{C['amber']}" stroke-dasharray="6 5" stroke-width="2"/>
<rect x="1" y="1" width="{w-2:.1f}" height="{hh-2:.1f}" fill="none" stroke="{C['slate']}" stroke-width="2"/>
<g fill="{C['amber']}" fill-opacity=".25"><rect x="0" y="0" width="{pad:.1f}" height="{hh:.1f}"/><rect x="{w-pad:.1f}" y="0" width="{pad:.1f}" height="{hh:.1f}"/></g></svg>'''
# don'ts
m,mw=mark(C['blue'],120,0,0)
def cell(inner,lbl): return f'<figure class="dont"><svg viewBox="-30 -20 {mw+60:.1f} 160">{inner}</svg><figcaption>{lbl}</figcaption></figure>'
P['DONTS']=''.join([
 cell(f'<g transform="scale(1.6,0.8) translate(-12,30)">{m}</g>','Don’t stretch it'),
 cell(f'<defs><filter id="sh"><feDropShadow dx="6" dy="8" stdDeviation="5" flood-opacity=".45"/></filter></defs><g filter="url(#sh)">{m}</g>','Don’t add shadows'),
 cell(f'<defs><linearGradient id="gr" x1="0" x2="1"><stop offset="0" stop-color="#2457D6"/><stop offset="1" stop-color="#F0A23B"/></linearGradient></defs>{m.replace(C["blue"],"url(#gr)")}','Don’t add gradients'),
 cell(m.replace(C['blue'],'#8E44AD'),'Don’t recolour it outside the palette'),
 cell(f'<defs><pattern id="busy" width="16" height="16" patternUnits="userSpaceOnUse"><rect width="16" height="16" fill="#c8a27a"/><circle cx="8" cy="8" r="6" fill="#7a9e6e"/><rect width="8" height="8" fill="#d06b4f"/></pattern></defs><rect x="-30" y="-20" width="{mw+60:.1f}" height="160" fill="url(#busy)"/>{m}','Don’t put it on busy images'),
])
P['FAV']=icon(64,C['blue'],C['white'],0.62,14)
json.dump(P,open('parts.json','w'),ensure_ascii=False)
print('ok',len(os.listdir(os.path.join(OUT,'svg'))))
