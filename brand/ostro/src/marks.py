import sys; sys.path.insert(0,__file__.rsplit('/',1)[0])
from pen import *
from shapely.geometry import LineString
W=19; A=38
def final(W=W,A=A):
    # left: windward, one continuous curve. right: slip face, cut in flat facets.
    L = bez((48,5),(22,10),(12,30),(13,50),30)[:-1] + bez((13,50),(14,72),(24,90),(47,95),30)
    R = [(45,6),(62,13),(71,26),(71,70),(64,84),(44,95)]
    R = [p for a,b in zip(R,R[1:]) for p in [ (a[0]+(b[0]-a[0])*t/8, a[1]+(b[1]-a[1])*t/8) for t in range(8)]]+[R[-1]]
    g = unary_union([stroke(L,W,A), stroke(R,W,A)])
    return g.simplify(0.05)
def textura():
    L=[(46,6),(16,22),(16,78),(42,94)]; R=[(44,6),(70,22),(70,78),(44,94)]
    return unary_union([stroke(L,W,A),stroke(R,W,A)])
def roundO():
    L=bez((46,6),(10,8),(10,92),(44,94),50); R=bez((44,6),(78,8),(78,92),(46,94),50)
    return unary_union([stroke(L,W,A),stroke(R,W,A)])
def openO():
    L=bez((34,10),(10,22),(12,84),(44,94),50); R=bez((44,94),(74,88),(76,26),(56,10),50)
    return unary_union([stroke(L,W,A),stroke(R,W,A)])
def spur():
    g=textura(); s=stroke([(43,40),(43,60)],8,A)
    return unary_union([g,s])
def lozenge():
    L=[(44,4),(12,50),(44,96)]; R=[(44,4),(76,50),(44,96)]
    return unary_union([stroke(L,W,A),stroke(R,W,A)])
def wide():
    L=bez((60,14),(14,14),(8,86),(56,88),50); R=bez((58,14),(110,12),(104,86),(58,88),50)
    return unary_union([stroke(L,W,A),stroke(R,W,A)])
def heavy():
    L=[(46,8),(18,22),(18,78),(42,92)]; R=[(44,8),(68,22),(68,78),(44,92)]
    return unary_union([stroke(L,30,A),stroke(R,30,A)])

def close(g,r=2.2):
    return g.buffer(r,join_style=2,mitre_limit=4).buffer(-r,join_style=2,mitre_limit=4)
def clean(g,o=1.0,r=2.2,s=0.25):
    g=close(g,r)
    g=g.buffer(-o,join_style=2,mitre_limit=5).buffer(o,join_style=2,mitre_limit=5)
    return g.simplify(s)
