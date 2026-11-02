import math
from shapely.geometry import Point, Polygon, box
from shapely import affinity
from shapely.ops import unary_union
RES=256
def C(x,y,r): return Point(x,y).buffer(r,RES)
DISC=C(50,50,50)
def lens(R=60,d=47,cx=50,cy=50): return C(cx+d,cy,R).intersection(C(cx-d,cy,R))
def ring(x,y,r,g): return C(x,y,r+g/2).difference(C(x,y,r-g/2))
def rot(g,a): return affinity.rotate(g,a,origin=(50,50))
def lensO(a=-22,R=60,d=47):
    return rot(DISC.difference(lens(R,d)),a)
def split(a=-22,R=60,d=47,g=4.5,both=True):
    L=lens(R,d); top=L.bounds[1]; bot=L.bounds[3]
    s=ring(50-d,50,R,g).intersection(box(-10,-10,110,top+1)).intersection(box(0,-10,50,110))
    o=DISC.difference(L).difference(s)
    if both:
        s2=ring(50+d,50,R,g).intersection(box(-10,bot-1,110,120)).intersection(box(50,0,110,120))
        o=o.difference(s2)
    return rot(o,a)
def crescent(a=-20):
    return rot(DISC.difference(C(54,50,30).difference(C(66,46,26))),a)
def egg(a=0):
    return rot(DISC.difference(C(42,44,27)),a)
def ovalO(a=-22):
    return rot(DISC.difference(affinity.scale(C(50,50,40),0.42,1)),a)
def cut(R,d,e): return C(50+d,50+e,R).intersection(C(50-d,50-e,R))
def dunes(a=-25,R=64,e=6,gap=5.5):
    # find d so the cut narrows to `gap` where it leaves the disc
    lo,hi=R-60,R-1
    for _ in range(60):
        d=(lo+hi)/2
        c=cut(R,d,e).intersection(DISC)
        o=DISC.difference(c)
        # opening width: thinnest part of the cut near the disc edge
        edge=c.intersection(DISC.difference(C(50,50,49)))
        w=edge.area/ max(1e-6, (2*1.0)) if not edge.is_empty else 0
        # width per opening ~ area/(2 openings * ring thickness 1)
        w=w/2
        if w>gap: lo=d
        else: hi=d
    return rot(DISC.difference(c),a), d
def dunesO(a=-25, hw=16, ew=3, e=6):
    R=(2304+(ew-hw)**2)/(2*(hw-ew)); d=R-hw
    return rot(DISC.difference(cut(R,d,e)),a), R, d
def dunes_counter(a=-25, hw=16, ew=3, e=6):
    R=(2304+(ew-hw)**2)/(2*(hw-ew)); d=R-hw
    return rot(cut(R,d,e).intersection(DISC),a)
