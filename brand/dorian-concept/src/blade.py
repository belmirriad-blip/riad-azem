import sys; sys.path.insert(0,'.')
from shapely.geometry import Polygon
from shapely.ops import unary_union
from pen import to_path
def cub(p0,p1,p2,p3,n=40):
    return [tuple((1-t)**3*p0[j]+3*(1-t)**2*t*p1[j]+3*(1-t)*t*t*p2[j]+t**3*p3[j] for j in range(2)) for t in [k/n for k in range(n+1)]]
def path(start,*segs):
    """segs: (c1,c2,end) cubic triples"""
    pts=[start]; cur=start
    for c1,c2,e in segs: pts+=cub(cur,c1,c2,e)[1:]; cur=e
    return pts
def blade(edgeA, edgeB):
    """two edges sharing first & last point -> filled blade"""
    return Polygon(edgeA+edgeB[::-1][1:-1]).buffer(0)
