import math, sys; sys.path.insert(0,'.')
from shapely.geometry import Point, Polygon, box
from shapely.ops import unary_union
from pen import to_path, stroke as penstroke, catmull
def wedge(cx,cy,a0,a1,R=400):
    pts=[(cx,cy)]+[(cx+R*math.cos(math.radians(a0+(a1-a0)*k/60)),cy+R*math.sin(math.radians(a0+(a1-a0)*k/60))) for k in range(61)]
    return Polygon(pts)
def ring(cx,cy,ro,ri,a0,a1): return Point(cx,cy).buffer(ro,resolution=96).difference(Point(cx,cy).buffer(ri,resolution=96)).intersection(wedge(cx,cy,a0,a1))
# A: cut rings — two ring segments with flat cut ends; the bowl's right end is sliced on a rising diagonal
def A():
    head=ring(56,28,22,9,90,322)          # C opening right, flat cut ends
    bowl=ring(56,72,42,24,12,236)         # big C opening right, joins under the head
    return unary_union([head,bowl])
# B: square Kufic ع on a grid, ending in a rising bar
def B(u=20):
    cells=[(1,0),(2,0),(3,0),(4,0),(1,1),(1,2),(2,2),(0,2),(0,3),(0,4),(0,5),(1,5),(2,5),(3,5),(4,5),(4,4)]
    return unary_union([box(x*u,y*u,(x+1)*u,(y+1)*u) for x,y in cells])
# B2: Kufic, the bowl's end climbs in steps
def B2(u=20):
    cells=[(1,0),(2,0),(3,0),(4,0),(1,1),(1,2),(2,2),(0,2),(0,3),(0,4),(0,5),(1,5),(2,5),(3,5),(3,4),(4,4),(5,4),(5,3),(5,2)]
    return unary_union([box(x*u,y*u,(x+1)*u,(y+1)*u) for x,y in cells])
# C: broad-nib calligraphic ع, sharp terminals
def C():
    head=catmull([(66,14),(54,6),(40,10),(34,22),(40,34),(52,38)],14)
    bowl=catmull([(52,38),(36,44),(24,58),(26,76),(42,86),(62,84),(78,72),(88,52)],14)
    return unary_union([penstroke(head,15,40),penstroke(bowl,19,40)])
# D: tile — A carved out of a solid square
def D():
    t=box(-6,-2,104,108); g=A()
    return t.difference(g.buffer(0))
MARKS={'A · Cut rings':A(),'B · Kufic grid':B(),'B2 · Kufic, stepped':B2(),'C · Calligraphic':C(),'D · Carved tile':D()}
