import sys; sys.path.insert(0,'.')
from marks import MARKS, to_path
g=MARKS['1']; x0,y0,x1,y1=g.bounds; D=to_path(g)
def mark_svg(fill,w):
    return f'<svg viewBox="{x0:.1f} {y0:.1f} {x1-x0:.1f} {y1-y0:.1f}" width="{w}" style="display:block"><path fill="{fill}" d="{D}"/></svg>'
