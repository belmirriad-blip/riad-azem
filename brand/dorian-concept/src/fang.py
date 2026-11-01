from blade import *
from shapely.geometry import Polygon
def fang_D(belly=116, inner=88, fang_w=32, fang_tip=88, claw=1.0, point=True):
    tt=(-14,34+2*claw); tb=(-14,70-2*claw)
    br=(belly-4,18) if point else (belly,14)
    A=path(tt,((-18,28),(-19,20),(-16,13)),((-10,0),(6,-8),(30,-8)),
           ((68,-8),br,(belly,52)),(((belly-4,86) if point else (belly,90)),(70,110),(30,110)),
           ((4,110),(-12,104),(-18,92)),((-20,84),(-18,77),tb))
    B=path(tt,((-11,28),(-9,21),(-6,16)),((-2,8),(10,4),(28,4)),
           ((60,6),(inner-4,28),(inner,52)),((inner-4,76),(60,98),(30,98)),
           ((12,98),(0,96),(-6,90)),((-10,84),(-12,77),tb))
    bowl=blade(A,B)
    x0=8; tip=(x0+12,fang_tip)
    left=path((x0,0),((x0,30),(x0+1,62),tip))
    right=path((x0+fang_w,0),((x0+fang_w-2,40),(x0+fang_w-10,70),tip))
    fang=Polygon(left+right[::-1]).buffer(0)
    return unary_union([bowl,fang]).simplify(0.03)
