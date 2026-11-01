import math, sys; sys.path.insert(0,'.')
from shapely.geometry import Point, Polygon
from shapely.ops import unary_union
from pen import to_path, stroke as penstroke, catmull
from m2 import wedge
def disc(cx,cy,r): return Point(cx,cy).buffer(r,resolution=128)
def A2():
    """A refined: concentric rings, even weight, flat radial cuts; bowl joins the head cleanly"""
    head=disc(56,28,22).difference(disc(56,28,9.5)).intersection(wedge(56,28,92,322))
    bowl=disc(56,72,42).difference(disc(56,72,24.5)).intersection(wedge(56,72,14,238))
    return unary_union([head,bowl])
def AC():
    """hybrid: same circles, but each inner circle is shifted so the stroke swells and thins like a pen"""
    head=disc(56,28,22).difference(disc(59.5,25.5,11)).intersection(wedge(56,28,92,322))
    bowl=disc(56,72,42).difference(disc(64,65,28)).intersection(wedge(56,72,14,238))
    return unary_union([head,bowl])
def C2():
    """broad nib refined: fuller head, longer climbing tail"""
    head=catmull([(68,15),(56,5),(41,8),(33,21),(38,34),(52,39)],16)
    bowl=catmull([(52,39),(35,45),(23,60),(25,78),(42,89),(64,87),(80,74),(90,50)],16)
    return unary_union([penstroke(head,15,40),penstroke(bowl,20,40)])
