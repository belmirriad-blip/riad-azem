import sys, json
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
F='/tmp/claude-0/-home-user-riad-azem/3209b590-5b43-58af-b03b-1f50f3bef959/scratchpad/fonts/'
_cache={}
def font(name, axes=None):
    k=(name,json.dumps(axes,sort_keys=True))
    if k in _cache: return _cache[k]
    f=TTFont(F+name)
    if axes: f=instantiateVariableFont(f,axes)
    _cache[k]=f; return f
def text_path(name, text, size, x=0, y=0, tracking=0, axes=None):
    """returns (svg path d, advance width) baseline at y"""
    f=font(name,axes); gs=f.getGlyphSet(); cmap=f.getBestCmap(); upm=f['head'].unitsPerEm
    s=size/upm; pen=SVGPathPen(gs); cx=0
    for ch in text:
        g=cmap[ord(ch)]
        tp=TransformPen(pen,(s,0,0,-s,x+cx,y))
        gs[g].draw(tp)
        cx+=gs[g].width*s+tracking
    return pen.getCommands(), cx-tracking
def metrics(name, axes=None):
    f=font(name,axes); o=f['OS/2']; upm=f['head'].unitsPerEm
    return dict(cap=o.sCapHeight/upm, x=o.sxHeight/upm)
