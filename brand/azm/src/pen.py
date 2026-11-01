import math
from shapely.geometry import Polygon
from shapely.ops import unary_union
def catmull(pts, n=12):
    """smooth path through pts (Catmull-Rom)"""
    out=[]; P=[pts[0]]+pts+[pts[-1]]
    for i in range(1,len(P)-2):
        p0,p1,p2,p3=P[i-1],P[i],P[i+1],P[i+2]
        for k in range(n):
            t=k/n; t2=t*t; t3=t2*t
            out.append(tuple(0.5*((2*p1[j])+(-p0[j]+p2[j])*t+(2*p0[j]-5*p1[j]+4*p2[j]-p3[j])*t2+(-p0[j]+3*p1[j]-3*p2[j]+p3[j])*t3) for j in range(2)))
    out.append(pts[-1]); return out
def stroke(pts, W=17, ang=40, smooth=False):
    if smooth: pts=catmull(pts)
    a=math.radians(ang); nx,ny=W/2*math.cos(a), -W/2*math.sin(a)
    polys=[]
    for (x0,y0),(x1,y1) in zip(pts,pts[1:]):
        polys.append(Polygon([(x0-nx,y0-ny),(x0+nx,y0+ny),(x1+nx,y1+ny),(x1-nx,y1-ny)]).buffer(0))
    return unary_union(polys)
def to_path(geom, dec=2):
    gs=[geom] if geom.geom_type=='Polygon' else list(geom.geoms)
    d=''
    for g in gs:
        for ring in [g.exterior]+list(g.interiors):
            c=list(ring.coords)[:-1]
            d+='M'+' L'.join(f'{x:.{dec}f},{y:.{dec}f}' for x,y in c)+' Z '
    return d
