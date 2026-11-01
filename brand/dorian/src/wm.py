import sys; sys.path.insert(0,'.')
from fang import fang_D
from pen import to_path
from glyphs import text_path, metrics
AR='Archivo%5Bwdth,wght%5D.ttf'; AX={'wght':800,'wdth':100}
CAP=100*metrics(AR,AX)['cap']; TR=32
INWORD=dict(belly=124,inner=90,fang_w=38)
def wordmark(fill, tracking=TR, gapk=0.9):
    """DORIAN with the first D replaced by the Fang D. Cap top y=0, baseline y=CAP. returns (svg, width, height)"""
    g=fang_D(**INWORD); x0,y0,x1,y1=g.bounds; s=CAP/(y1-y0); dw=(x1-x0)*s
    d,w=text_path(AR,'ORIAN',100,dw+tracking*gapk,CAP,tracking=tracking,axes=AX)
    svg=(f'<path fill="{fill}" d="{to_path(g)}" transform="scale({s:.4f}) translate({-x0:.2f},{-y0:.2f})"/>'
         f'<path fill="{fill}" d="{d}"/>')
    return svg, dw+tracking*gapk+w, CAP
