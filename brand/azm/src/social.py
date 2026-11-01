import os, sys, json, glob
sys.path.insert(0,'.')
OUT=sys.argv[1]; SO=os.path.join(OUT,'social'); os.makedirs(SO,exist_ok=True)
F='/tmp/claude-0/-home-user-riad-azem/3209b590-5b43-58af-b03b-1f50f3bef959/scratchpad/fonts/'
C=dict(blue='#2457D6',paper='#F4F6FB',amber='#F0A23B',slate='#A7B1C6',ink='#121A2E',white='#FFFFFF')
P=json.load(open('parts.json'))
from build_azm_marks import mark_svg  # small helper written below
GOOGLE='<link href="https://fonts.googleapis.com/css2?family=Readex+Pro:wght@600;700&family=IBM+Plex+Sans+Arabic:wght@400;500;600&display=swap" rel="stylesheet">'
LOCAL=f'''<style>@font-face{{font-family:"Readex Pro";src:url("file://{F}ReadexPro%255BHEXP,wght%255D.ttf");font-weight:100 900}}
@font-face{{font-family:"IBM Plex Sans Arabic";src:url("file://{F}IBMPlexSansArabic-Regular.ttf");font-weight:400}}
@font-face{{font-family:"IBM Plex Sans Arabic";src:url("file://{F}IBMPlexSansArabic-Medium.ttf");font-weight:500}}
@font-face{{font-family:"IBM Plex Sans Arabic";src:url("file://{F}IBMPlexSansArabic-SemiBold.ttf");font-weight:600}}</style>'''
BASE='''*{box-sizing:border-box;margin:0}html,body{margin:0}
.c{position:relative;overflow:hidden;font-family:"IBM Plex Sans Arabic",sans-serif;direction:rtl}
.h{font-family:"Readex Pro",sans-serif;font-weight:700;line-height:1.3}
.mk{position:absolute;width:64px;height:auto}
.n{font-variant-numeric:tabular-nums}'''
T={}
# 1. post, one line
def post(bg,fg,mk,name):
    return name,1080,1350,f'''<div class="c" style="width:1080px;height:1350px;background:{bg};color:{fg}">
<p class="h" style="position:absolute;inset:0 110px;display:flex;align-items:center;font-size:104px;letter-spacing:-.01em">الطريقة قبل الساعات.</p>
<div class="mk" style="left:96px;bottom:96px">{mark_svg(mk,64)}</div></div>'''
TPL=[post(C['ink'],C['paper'],C['white'],'post-1080x1350-ink'),post(C['white'],C['ink'],C['blue'],'post-1080x1350-white')]
# 2. story, number-led
TPL.append(('story-1080x1920-number',1080,1920,f'''<div class="c" style="width:1080px;height:1920px;background:{C['blue']};color:{C['white']}">
<div style="position:absolute;top:560px;right:110px;left:110px">
<p class="h n" style="font-size:420px;line-height:1">3</p>
<p class="h" style="font-size:112px;margin-top:10px">تمارين يومياً</p>
<p style="font-size:44px;margin-top:40px;opacity:.85;line-height:1.7">من امتحانات البكالوريا السابقة. ثم سجّلها.</p></div>
<div class="mk" style="left:110px;bottom:200px">{mark_svg(C['white'],64)}</div></div>'''))
# 3. reel cover: title inside the centre 1080x1440 crop zone
TPL.append(('reel-cover-1080x1920',1080,1920,f'''<div class="c" style="width:1080px;height:1920px;background:{C['ink']};color:{C['paper']}">
<div style="position:absolute;top:240px;bottom:240px;left:0;right:0;display:flex;flex-direction:column;justify-content:center;padding:0 120px">
<p style="font-size:40px;color:{C['amber']};font-weight:600">الحلقة 01</p>
<p class="h" style="font-size:118px;margin-top:24px">كيف أخطط<br>لأسبوع المراجعة</p></div>
<div class="mk" style="left:120px;bottom:300px">{mark_svg(C['white'],64)}</div></div>'''))
# 4. YouTube thumbnail: max 4 words, big number
TPL.append(('youtube-thumbnail-1280x720',1280,720,f'''<div class="c" style="width:1280px;height:720px;background:{C['paper']};color:{C['ink']}">
<div style="position:absolute;inset:0 90px;display:flex;align-items:center;gap:56px">
<p class="h n" style="font-size:330px;line-height:1;color:{C['blue']}">16</p>
<p class="h" style="font-size:96px;line-height:1.25">من 10<br>في 3 أشهر</p></div>
<div class="mk" style="left:70px;bottom:60px;width:56px">{mark_svg(C['blue'],56)}</div></div>'''))
# 5. testimonial card: placeholders, clearly marked
TPL.append(('testimonial-1080x1350',1080,1350,f'''<div class="c" style="width:1080px;height:1350px;background:{C['white']};color:{C['ink']}">
<div style="position:absolute;top:200px;right:110px;left:110px">
<div style="display:flex;gap:90px;align-items:flex-end">
<div><p style="font-size:38px;color:#55607A">قبل</p><p class="h n" style="font-size:190px;line-height:1.05;color:{C['slate']}">00</p></div>
<div><p style="font-size:38px;color:#55607A">بعد</p><p class="h n" style="font-size:190px;line-height:1.05;color:{C['blue']}">00</p></div></div>
<p style="font-size:58px;line-height:1.7;margin-top:90px;font-weight:500">«اقتباس قصير وصادق من الطالب، بكلماته.»</p>
<p style="font-size:40px;margin-top:50px;color:#55607A">الاسم الأول أو الحروف الأولى · 3AS علوم تجريبية</p></div>
<div class="mk" style="left:110px;bottom:110px">{mark_svg(C['blue'],64)}</div></div>'''))
for f in glob.glob(SO+'/*'): os.remove(f)
os.makedirs('socsrc',exist_ok=True)
for f in glob.glob('socsrc/*'): os.remove(f)
for name,w,h,body in TPL:
    page=lambda fonts: f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>Azm · {name}</title>{fonts}<style>{BASE}</style></head><body>{body}</body></html>'
    open(os.path.join(SO,name+'.html'),'w').write(page(GOOGLE))
    open(f'socsrc/{name}.html','w').write(page(LOCAL))
json.dump([(n,w,h) for n,w,h,_ in TPL],open('socsrc/list.json','w'))
print(len(TPL))
