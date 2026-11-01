import os, sys, json, glob, math, random
sys.path.insert(0,'.')
from fang import fang_D, fang_parts
from pen import to_path
from glyphs import text_path, metrics
from wm import wordmark as _wm, AR, AX, CAP
from shapely.ops import unary_union
OUT=sys.argv[1]; SV=os.path.join(OUT,'svg'); os.makedirs(SV,exist_ok=True)
for f in glob.glob(SV+'/*.svg'): os.remove(f)
C=dict(forest='#123F35',offwhite='#F4F0E6',spice='#E0663F',taupe='#B3A28E',charcoal='#232323')
G=fang_D(); MD=to_path(G); mx0,my0,mx1,my1=G.bounds; MW,MH=mx1-mx0,my1-my0
def mark(fill,s=1,tx=0,ty=0): return f'<path fill="{fill}" d="{MD}" transform="translate({tx:.2f},{ty:.2f}) scale({s:.4f}) translate({-mx0:.2f},{-my0:.2f})"/>'
def word(fill,s=1,tx=0,ty=0):
    w,_,_=_wm(fill,gapk=0.75); return f'<g transform="translate({tx:.2f},{ty:.2f}) scale({s:.4f})">{w}</g>'
WW=_wm('#000',gapk=0.75)[1]; WH=CAP
TS=13*1.0  # tagline size relative to wordmark cap 68.6
TD,TW=text_path('JosefinSans%5Bwght%5D.ttf','COUTURE SUR MESURE',TS*1.55,0,0,tracking=TS*1.55*0.42,axes={'wght':400})
def tagline(fill,cx,y): return f'<path fill="{fill}" d="{TD}" transform="translate({cx-TW/2:.2f},{y:.2f})"/>'
def bg(w,h,c,r=0): return f'<rect width="{w:.1f}" height="{h:.1f}" rx="{r}" fill="{c}"/>'
def doc(w,h,inner,t): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.1f} {h:.1f}"><title>{t}</title>{inner}</svg>'
def save(n,inner,w,h,t): open(os.path.join(SV,n),'w').write(doc(w,h,inner,t))
# ---- layouts (all return inner,w,h)
def L_mark(fill,pad=4): return mark(fill,1,pad,pad), MW+2*pad, MH+2*pad
def L_word(fill,pad=6): return word(fill,1,pad,pad), WW+2*pad, WH+2*pad
def L_primary(fill,bgc=None,pad=40):
    """logo above, DORIAN (fang D inside) below"""
    s=WW*0.42/MW; mw,mh=MW*s,MH*s; gap=CAP*0.9
    W=WW+2*pad; H=mh+gap+WH+2*pad
    i=(bg(W,H,bgc) if bgc else '')+mark(fill,s,(W-mw)/2,pad)+word(fill,1,pad,pad+mh+gap)
    return i,W,H
def L_wordtag(fill,pad=6):
    ty=WH+46; i=word(fill,1,pad,pad)+tagline(fill,pad+WW/2,pad+ty)
    return i,WW+2*pad,ty+TS*1.55*0.75+2*pad+4
def L_icon(bgc,fg,size=200,r=None):
    r=size*0.22 if r is None else r; s=size*0.60/MW*1.0; s=min(s,size*0.56/MH)
    return bg(size,size,bgc,r)+mark(fg,s,(size-MW*s)/2,(size-MH*s)/2),size,size
# ---- logo files
for n in ['forest','charcoal','offwhite','spice']:
    save(f'dorian-mark-{n}.svg',*L_mark(C[n]),'DORIAN mark')
    save(f'dorian-wordmark-{n}.svg',*L_word(C[n]),'DORIAN wordmark')
    save(f'dorian-primary-{n}.svg',*L_primary(C[n]),'DORIAN primary lockup')
    save(f'dorian-wordmark-tagline-{n}.svg',*L_wordtag(C[n]),'DORIAN wordmark with tagline')
for nm,b,f in [('offwhite-on-forest','forest','offwhite'),('forest-on-offwhite','offwhite','forest'),('spice-on-charcoal','charcoal','spice'),('spice-on-offwhite','offwhite','spice')]:
    save(f'dorian-primary-{nm}.svg',*L_primary(C[f],C[b],70),'DORIAN primary lockup')
for b,f in [('forest','offwhite'),('offwhite','forest'),('charcoal','spice')]:
    save(f'dorian-app-icon-{b}.svg',*L_icon(C[b],C[f]),'DORIAN icon')
# chest print, real size 80 mm wide
open(os.path.join(SV,'dorian-chest-print-80mm-offwhite.svg'),'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" width="80mm" height="{80*MH/MW:.2f}mm" viewBox="{mx0:.2f} {my0:.2f} {MW:.2f} {MH:.2f}"><title>DORIAN chest print, 80 mm</title><path fill="{C["offwhite"]}" d="{MD}"/></svg>')
open(os.path.join(SV,'dorian-chest-print-80mm-forest.svg'),'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" width="80mm" height="{80*MH/MW:.2f}mm" viewBox="{mx0:.2f} {my0:.2f} {MW:.2f} {MH:.2f}"><title>DORIAN chest print, 80 mm</title><path fill="{C["forest"]}" d="{MD}"/></svg>')
# ---- social pack (svg sources rendered to png later)
SO=os.path.join(OUT,'social-src'); os.makedirs(SO,exist_ok=True)
for f in glob.glob(SO+'/*.svg'): os.remove(f)
def soc(name,w,h,inner): open(os.path.join(SO,name),'w').write(doc(w,h,inner,'DORIAN'))
for b,f in [('forest','offwhite'),('offwhite','forest'),('charcoal','spice')]:
    # profile picture: square, mark inside the circle-safe zone
    s=1080*0.50/MW; s=min(s,1080*0.50/MH)
    soc(f'profile-picture-1080-{b}.svg',1080,1080,bg(1080,1080,C[b])+mark(C[f],s,(1080-MW*s)/2+10,(1080-MH*s)/2))
def centered_primary(w,h,fill,bgc,width_frac,yoff=0,tag=False):
    i,pw,ph=L_primary(fill,None,0); s=w*width_frac/pw
    out=bg(w,h,bgc)+f'<g transform="translate({(w-pw*s)/2:.1f},{(h-ph*s)/2+yoff:.1f}) scale({s:.4f})">{i}</g>'
    if tag:
        ts=pw*s*0.62/TW; ty=(h+ph*s)/2+yoff+pw*s*0.11
        out+=f'<g transform="translate({w/2:.1f},{ty:.1f}) scale({ts:.4f})">{tagline(fill,0,0)}</g>'
    return out
soc('post-1080x1350-forest.svg',1080,1350,centered_primary(1080,1350,C['offwhite'],C['forest'],0.56,-40,True))
soc('post-1080x1350-offwhite.svg',1080,1350,centered_primary(1080,1350,C['forest'],C['offwhite'],0.56,-40,True))
soc('post-1080x1080-forest.svg',1080,1080,centered_primary(1080,1080,C['offwhite'],C['forest'],0.52,-30,True))
soc('story-1080x1920-forest.svg',1080,1920,centered_primary(1080,1920,C['offwhite'],C['forest'],0.62,-60,True))
soc('story-1080x1920-charcoal.svg',1080,1920,centered_primary(1080,1920,C['spice'],C['charcoal'],0.62,-60,False))
def banner(w,h,fill,bgc):
    s=h*0.34/WH; return bg(w,h,bgc)+word(fill,s,(w-WW*s)/2,(h-WH*s)/2)
soc('facebook-cover-1640x624-forest.svg',1640,624,banner(1640,624,C['offwhite'],C['forest']))
soc('x-header-1500x500-forest.svg',1500,500,banner(1500,500,C['offwhite'],C['forest']))
soc('youtube-banner-2560x1440-forest.svg',2560,1440,bg(2560,1440,C['forest'])+word(C['offwhite'],1440*0.11/WH,(2560-WW*1440*0.11/WH)/2,(1440-WH*1440*0.11/WH)/2))
soc('favicon-512.svg',512,512,L_icon(C['forest'],C['offwhite'],512)[0])
json.dump({},open('social.json','w'))
# ---- board parts
def inl(t,label,cls=''):
    i,w,h=t; return f'<svg class="{cls}" viewBox="0 0 {w:.1f} {h:.1f}" role="img" aria-label="{label}">{i}</svg>'
P={}
P['MARK_OFF']=inl(L_mark(C['offwhite']),'DORIAN mark','mk'); P['MARK_FOR']=inl(L_mark(C['forest']),'DORIAN mark','mk')
P['MARK_SPI']=inl(L_mark(C['spice']),'DORIAN mark','mk'); P['MARK_CHA']=inl(L_mark(C['charcoal']),'DORIAN mark','mk')
P['WORD_FOR']=inl(L_word(C['forest']),'DORIAN wordmark','wm'); P['WORD_OFF']=inl(L_word(C['offwhite']),'DORIAN wordmark','wm')
P['WORD_SPI']=inl(L_word(C['spice']),'DORIAN wordmark','wm')
P['PRI_FOR']=inl(L_primary(C['forest']),'DORIAN primary lockup','st'); P['PRI_OFF']=inl(L_primary(C['offwhite']),'DORIAN primary lockup','st')
P['TAG_FOR']=inl(L_wordtag(C['forest']),'DORIAN wordmark with tagline','lk')
P['HERO_WORD']=inl(L_word(C['forest']),'DORIAN','hw')
P['ICONS']=[inl(L_icon(C[b],C[f]),'DORIAN app icon','ic') for b,f in [('forest','offwhite'),('offwhite','forest'),('charcoal','spice')]]
P['SIZES']=[inl(L_mark(C['offwhite']),'DORIAN mark small','') for _ in range(4)]
P['WORD_SIZES']=inl(L_word(C['offwhite']),'DORIAN wordmark small','')
# small fang (signature detail)
bowl,fang=fang_parts(); fx0,fy0,fx1,fy1=fang.bounds
FD=to_path(fang)
P['ACCENT']=f'<svg class="ac" viewBox="{fx0-4:.1f} {fy0-4:.1f} {fx1-fx0+8:.1f} {fy1-fy0+8:.1f}" role="img" aria-label="The fang"><path fill="{C["spice"]}" d="{FD}" transform="rotate(-12 {(fx0+fx1)/2:.1f} {(fy0+fy1)/2:.1f})"/></svg>'
# construction: bowl blade + fang = mark
BD=to_path(bowl); bx0,by0,bx1,by1=bowl.bounds
grey='#5b5a55'
P['CONSTR']=f'''<svg viewBox="0 0 900 250" role="img" aria-label="Blade plus fang equals the DORIAN mark">
<g transform="translate(40,40) scale(1.3) translate({-bx0:.1f},{-by0:.1f})"><path d="{BD}" fill="{grey}"/></g>
<text x="250" y="135" text-anchor="middle" font-family="Josefin Sans, sans-serif" font-weight="200" font-size="46" fill="#8d8a82">+</text>
<g transform="translate(330,40) scale(1.3) translate({-fx0:.1f},{-by0:.1f})"><path d="{FD}" fill="{grey}"/></g>
<text x="460" y="135" text-anchor="middle" font-family="Josefin Sans, sans-serif" font-weight="200" font-size="46" fill="#8d8a82">=</text>
<g transform="translate(560,40) scale(1.3) translate({-mx0:.1f},{-my0:.1f})"><path d="{MD}" fill="{C['offwhite']}"/></g>
<g font-family="Josefin Sans, sans-serif" font-size="12" letter-spacing="3" fill="#8d8a82" text-anchor="middle"><text x="135" y="245">THE BLADE</text><text x="355" y="245">THE FANG</text><text x="660" y="245">DORIAN MARK</text></g></svg>'''
# grid
P['GRID']=f'''<svg viewBox="{mx0-14:.1f} {my0-14:.1f} {MW+28:.1f} {MH+28:.1f}" role="img" aria-label="Mark construction grid">
<g stroke="#4a4944" stroke-width=".5">{''.join(f'<line x1="{x}" y1="{my0-12:.0f}" x2="{x}" y2="{my1+12:.0f}"/>' for x in range(-30,131,10))}{''.join(f'<line x1="{mx0-12:.0f}" y1="{y}" x2="{mx1+12:.0f}" y2="{y}"/>' for y in range(-10,121,10))}</g>
<g opacity=".92"><path fill="{C['offwhite']}" d="{MD}"/></g>
<g fill="none" stroke="{C['spice']}" stroke-width=".8"><line x1="{mx0-12:.0f}" y1="-8" x2="{mx1+12:.0f}" y2="-8"/><line x1="{mx0-12:.0f}" y1="110" x2="{mx1+12:.0f}" y2="110"/>
<line x1="{mx0-12:.0f}" y1="88" x2="{mx1+12:.0f}" y2="88" stroke-dasharray="2 3"/><line x1="116" y1="{my0-12:.0f}" x2="116" y2="{my1+12:.0f}" stroke-dasharray="2 3"/></g>
<g font-family="Josefin Sans, sans-serif" font-size="5" letter-spacing=".8" fill="{C['spice']}"><text x="{mx1-26:.0f}" y="-10">CAP</text><text x="{mx1-36:.0f}" y="117">BASELINE</text><text x="{mx1-40:.0f}" y="86">FANG TIP</text><text x="118" y="56">POINT</text></g></svg>'''
# pattern of fangs
fs=0.42
P['PATTERN']=f'''<svg viewBox="0 0 480 240" role="img" aria-label="Fang pattern"><defs><pattern id="fp" width="56" height="56" patternUnits="userSpaceOnUse"><rect width="56" height="56" fill="{C['forest']}"/><path fill="{C['offwhite']}" fill-opacity=".13" d="{FD}" transform="translate(18,8) scale({fs}) translate({-fx0:.1f},{-fy0:.1f})"/></pattern></defs><rect width="480" height="240" fill="url(#fp)"/></svg>'''
# sketches: the real explorations, pencil look
sys.path.insert(0,'../dorian')
from blade import path, blade
from shapely.geometry import Polygon
def stem(hook=1.0):
    T1=(2-6*hook,2-4*hook); T2=(4-8*hook,106)
    return blade(path(T1,((12,4),(12,30),(12,52)),((12,76),(14,96),T2)),path(T1,((26,-2),(34,26),(34,52)),((34,80),(26,98),T2)))
def crescent(g=0):
    P1=(36+g,6); P2=(36+g,100)
    return blade(path(P1,((60,-4),(102,12),(102,54)),((102,90),(66,104),P2)),path(P1,((58,10),(80,26),(80,54)),((80,80),(60,92),P2)))
def leaf(x=24,top=8,bot=94):
    t=(x+4,top); b=(x+4,bot)
    return blade(path(t,((x-10,24),(x-12,40),(x-12,52)),((x-12,66),(x-10,80),b)),path(t,((x+10,26),(x+12,40),(x+12,52)),((x+12,66),(x+10,80),b)))
b0,_=fang_parts(point=False); b1,_=fang_parts()
SK=[('two crescents',unary_union([stem(),crescent()])),('split blades',unary_union([stem(),crescent(5)])),
    ('wrapped wings',unary_union([stem(0.3),b0])),('leaf eye',unary_union([b0,leaf()])),
    ('pierced leaf',unary_union([b0.difference(leaf(top=-6,bot=108).buffer(3)),leaf(top=-6,bot=108)])),
    ('pointed belly',unary_union([b1,leaf()])),('fang',G),('heavy fang',fang_D(belly=124,inner=90,fang_w=38))]
random.seed(5); cells=''
for i,(lbl,g) in enumerate(SK):
    col=i%4; row=i//4; x=col*235+70; y=row*270+50
    d=to_path(g); gx0,gy0,gx1,gy1=g.bounds; sc=150/max(gx1-gx0,gy1-gy0)
    pick=lbl=='fang'; body=''
    for k in range(4 if pick else 3):
        dx,dy,rot=random.uniform(-1.4,1.4),random.uniform(-1.4,1.4),random.uniform(-.8,.8)
        body+=f'<path d="{d}" fill="none" stroke="{"#1b1b1b" if pick else "#5a5a5a"}" stroke-width="{(1.7 if k==0 else .9)/sc:.2f}" stroke-opacity="{.9 if k==0 else .4}" transform="translate({dx:.1f},{dy:.1f}) rotate({rot:.2f} 50 50)"/>'
    cells+=f'<circle cx="{x+75}" cy="{y+75}" r="80" fill="none" stroke="#a9a49a" stroke-width=".6" stroke-dasharray="3 4"/><g transform="translate({x},{y}) scale({sc:.3f}) translate({-gx0:.1f},{-gy0:.1f})" filter="url(#pencil)">{body}</g>'
    cells+=f'<text x="{x+75}" y="{y+205}" text-anchor="middle" font-family="Pinyon Script, cursive" font-size="24" fill="#4d4a44">{lbl}</text>'
    if pick:
        for rx,ry,sw,op,rt in [(118,112,2.4,1,-8),(112,107,1.1,.55,-4)]:
            cells+=f'<ellipse cx="{x+75}" cy="{y+82}" rx="{rx}" ry="{ry}" fill="none" stroke="{C["spice"]}" stroke-width="{sw}" stroke-opacity="{op}" transform="rotate({rt} {x+75} {y+82})" filter="url(#pencil)"/>'
    elif lbl in ('two crescents','split blades','leaf eye','pierced leaf'):
        cells+=f'<path d="M{x-14},{y+166} L{x+164},{y+4}" stroke="#7d7a73" stroke-width="1.3" filter="url(#pencil)"/>'
P['SKETCH']=f'''<svg viewBox="0 0 1000 560" role="img" aria-label="Pencil sketches of eight D explorations; the fang circled"><defs><filter id="pencil" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="4" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="2.6"/></filter></defs><rect width="1000" height="560" fill="#FBF9F3"/>{cells}</svg>'''
# applications
lw=WW*0.5
P['LABEL']=f'''<svg viewBox="0 0 360 150" role="img" aria-label="Woven garment label"><rect width="360" height="150" fill="{C['forest']}"/><rect x="8" y="8" width="344" height="134" fill="none" stroke="{C['offwhite']}" stroke-opacity=".35" stroke-dasharray="5 4"/>
{word(C['offwhite'],0.5,180-lw/2,48)}
<text x="180" y="116" text-anchor="middle" font-family="Josefin Sans, sans-serif" font-size="10" letter-spacing="4" fill="{C['offwhite']}" fill-opacity=".8">COUTURE SUR MESURE · BÉCHAR</text></svg>'''
ts=0.5
P['TAG']=f'''<svg viewBox="0 0 200 330" role="img" aria-label="Hang tag"><path d="M20,40 L60,8 H140 L180,40 V318 H20 Z" fill="{C['offwhite']}"/><circle cx="100" cy="38" r="9" fill="{C['charcoal']}"/>
<path d="M100,38 C120,-10 170,10 200,-4" stroke="{C['spice']}" stroke-width="2" fill="none"/>
{mark(C['forest'],ts,100-MW*ts/2,88)}
<line x1="44" y1="222" x2="156" y2="222" stroke="{C['taupe']}" stroke-width="1.6" stroke-dasharray="7 5" stroke-linecap="round"/>
<text x="100" y="250" text-anchor="middle" font-family="Fraunces, serif" font-weight="300" font-size="16" fill="{C['charcoal']}">Costume sur mesure</text>
<text x="100" y="274" text-anchor="middle" font-family="Josefin Sans, sans-serif" font-size="9" letter-spacing="3" fill="#6f6a60">POUR HOMME</text>
<text x="100" y="300" text-anchor="middle" font-family="Pinyon Script, cursive" font-size="17" fill="{C['spice']}">fait main</text></svg>'''
s=118/MW
P['AVATAR']=f'''<svg viewBox="0 0 200 200" role="img" aria-label="Instagram avatar"><circle cx="100" cy="100" r="100" fill="{C['forest']}"/>{mark(C['offwhite'],s,100-MW*s/2+3,100-MH*s/2)}</svg>'''
s=0.62
P['CARD_F']=f'''<svg viewBox="0 0 350 200" role="img" aria-label="Business card front"><rect width="350" height="200" fill="{C['forest']}"/>{mark(C['offwhite'],s,175-MW*s/2,100-MH*s/2)}</svg>'''
P['CARD_B']=f'''<svg viewBox="0 0 350 200" role="img" aria-label="Business card back"><rect width="350" height="200" fill="{C['offwhite']}"/>
{word(C['forest'],0.36,28,34)}
<text x="28" y="92" font-family="Josefin Sans, sans-serif" font-size="8.5" letter-spacing="3" fill="#6f6a60">COUTURE SUR MESURE</text>
<line x1="28" y1="118" x2="322" y2="118" stroke="{C['spice']}" stroke-width="1.4" stroke-dasharray="7 5" stroke-linecap="round"/>
<g font-family="Josefin Sans, sans-serif" font-size="10" fill="{C['charcoal']}"><text x="28" y="146">Atelier DORIAN · Béchar, Algérie</text><text x="28" y="164">Sur rendez-vous</text><text x="28" y="182">@dorian.couture</text></g></svg>'''
json.dump(P,open('parts.json','w'))
print('ok', len(os.listdir(SV)), len(os.listdir(SO)))
