import math
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union
from shapely import affinity

def bez(p0,p1,p2,p3,n=40):
    out=[]
    for i in range(n+1):
        t=i/n; u=1-t
        out.append((u**3*p0[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t**3*p3[0],
                    u**3*p0[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t**3*p3[1]))
    return out

def stroke(pts, w, ang):
    # flat nib: segment of length w at angle ang (deg, up-right, svg y-down)
    a=math.radians(ang); hx=w/2*math.cos(a); hy=-w/2*math.sin(a)
    polys=[]
    for (x0,y0),(x1,y1) in zip(pts,pts[1:]):
        polys.append(Polygon([(x0-hx,y0-hy),(x0+hx,y0+hy),(x1+hx,y1+hy),(x1-hx,y1-hy)]).convex_hull)
        polys.append(Polygon([(x0-hx,y0-hy),(x1-hx,y1-hy),(x1+hx,y1+hy),(x0+hx,y0+hy)]).convex_hull)
    return unary_union([p.buffer(0) for p in polys if p.area>0] )

def to_path(g, nd=2):
    if isinstance(g,Polygon): g=[g]
    elif isinstance(g,MultiPolygon): g=list(g.geoms)
    d=[]
    def ring(r):
        c=list(r.coords)[:-1]
        return 'M'+' L'.join(f'{x:.{nd}f},{y:.{nd}f}'.replace('.00','') for x,y in c)+'Z'
    for p in g:
        d.append(ring(p.exterior))
        for i in p.interiors: d.append(ring(i))
    return ''.join(d)

def norm(g, H=100):
    # scale so bbox height = H, origin at 0,0
    minx,miny,maxx,maxy=g.bounds
    s=H/(maxy-miny)
    g=affinity.translate(g,-minx,-miny)
    return affinity.scale(g,s,s,origin=(0,0))
