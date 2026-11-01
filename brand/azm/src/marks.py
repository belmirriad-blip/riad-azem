import math, sys; sys.path.insert(0,'.')
from shapely.geometry import LineString
from shapely.ops import unary_union
from pen import catmull, to_path
def arc(cx,cy,r,a0,a1,n=40):
    # degrees, y-down screen coords; a measured clockwise from +x
    return [(cx+r*math.cos(math.radians(a0+(a1-a0)*k/n)), cy+r*math.sin(math.radians(a0+(a1-a0)*k/n))) for k in range(n+1)]
def stroke(pts,W): return LineString(pts).buffer(W/2,cap_style=1,join_style=1,resolution=24)
W=15
HEAD=arc(50,31,16,-40,-270)   # from upper-right, over the top, round the left, to bottom-centre-left
def v1():   # rising curve
    j=HEAD[-1]
    tail=catmull([j,(34,52),(24,68),(30,84),(48,90),(68,86),(82,72),(88,56)],16)
    return unary_union([stroke(HEAD,W),stroke(tail,W)])
def v2():   # stepped tail: lands on the baseline, climbs two steps
    j=HEAD[-1]
    curve=catmull([j,(32,54),(23,70),(27,86),(36,90)],16)
    steps=[(36,90),(54,90),(54,70),(72,70),(72,50),(88,50)]
    return unary_union([stroke(HEAD,W),stroke(curve+steps[1:],W)])
def v3():   # geometric: quarter circles and straight runs, ending in a vertical climb
    j=HEAD[-1]
    p=[j]+[(26,58)]
    p+=arc(40,74,14,180,90)[1:]          # left side round into the baseline (180 -> 90 deg = left -> bottom)
    p+=[(68,88)]
    p+=arc(68,74,14,90,0)[1:]            # bottom -> right
    p+=[(82,52)]
    return unary_union([stroke(HEAD,W),stroke(p,W)])
def v_light():
    global W
    w0=W; W=10.5; g=v1(); W=w0; return g
MARKS={'1':v1(),'2':v3(),'3':v_light()}

# Final choice: C (broad nib). A and A+C kept as alternatives.
from m3 import C2, A2, AC
MARKS={'1':C2(),'2':A2(),'3':AC()}
