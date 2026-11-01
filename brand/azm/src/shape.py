import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
import io
F='/tmp/claude-0/-home-user-riad-azem/3209b590-5b43-58af-b03b-1f50f3bef959/scratchpad/fonts/'
_c={}
def load(name,axes):
    k=(name,tuple(sorted((axes or {}).items())))
    if k in _c: return _c[k]
    tt=TTFont(F+name)
    if axes: tt=instantiateVariableFont(tt,axes)
    buf=io.BytesIO(); tt.save(buf); data=buf.getvalue()
    face=hb.Face(data); font=hb.Font(face)
    _c[k]=(tt,font); return _c[k]
def shaped_path(name,text,size,x=0,y=0,axes=None,tracking=0,rtl=True):
    tt,font=load(name,axes); upm=tt['head'].unitsPerEm; s=size/upm
    b=hb.Buffer(); b.add_str(text); b.guess_segment_properties(); hb.shape(font,b,{})
    gs=tt.getGlyphSet(); order=tt.getGlyphOrder(); pen=SVGPathPen(gs); bp=BoundsPen(gs); cx=0
    for info,pos in zip(b.glyph_infos,b.glyph_positions):
        g=order[info.codepoint]; T=(s,0,0,-s,x+cx+pos.x_offset*s,y-pos.y_offset*s)
        gs[g].draw(TransformPen(pen,T)); gs[g].draw(TransformPen(bp,T))
        cx+=pos.x_advance*s+tracking
    global LAST_BOUNDS; LAST_BOUNDS=bp.bounds
    return pen.getCommands(), cx-tracking
