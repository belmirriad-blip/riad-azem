import json,sys
P=json.load(open('parts.json'))
def lum(h):
    h=h.lstrip('#'); c=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    c=[x/12.92 if x<=0.03928 else ((x+0.055)/1.055)**2.4 for x in c]; return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2]
def cr(a,b): la,lb=sorted([lum(a),lum(b)],reverse=True); return (la+0.05)/(lb+0.05)
C=dict(Blue='#2457D6',Paper='#F4F6FB',Amber='#F0A23B',Slate='#A7B1C6',Ink='#121A2E',White='#FFFFFF')
sw=[('Blue','#2457D6','Primary · 30%','Buttons, links, the mark, key numbers'),('Paper','#F4F6FB','Ground · 55%','Light backgrounds, cards'),
    ('Ink','#121A2E','Text & dark · 10%','Body text, dark theme background'),('Slate','#A7B1C6','Support · 4%','Borders, secondary data, muted marks'),
    ('Amber','#F0A23B','Accent · 1%','One highlight per screen: streak, the key call to action')]
swh=''.join(f'<div class="sw"><div class="chip" style="background:{h}"></div><b>{n}</b><code>{h}</code><span>{r}</span><small>{u}</small></div>' for n,h,r,u in sw)
pairs=[('White','Blue'),('Blue','Paper'),('Ink','Paper'),('Paper','Ink'),('Amber','Ink'),('Slate','Ink'),('Amber','Paper'),('Slate','Paper'),('Blue','Ink')]
rows=''
for a,b in pairs:
    r=cr(C[a],C[b]); ok='Pass' if r>=4.5 else ('Large text only' if r>=3 else 'Fail')
    note={'Amber/Paper':'Amber is a fill on light, never text','Slate/Paper':'Slate is for borders on light, never text','Blue/Ink':'On dark, the mark and links go white'}.get(f'{a}/{b}','')
    rows+=f'<tr><td><span class="pv" style="background:{C[b]};color:{C[a]}">عزم Aa</span></td><td>{a} on {b}</td><td class="num">{r:.2f}:1</td><td><span class="st {ok.split()[0].lower()}">{ok}</span></td><td class="muted">{note}</td></tr>'
vars_=''.join(f'<figure class="var{" pick" if k=="1" else ""}"><div class="vart">{big}</div><figcaption><b>{k} · {lbl}</b>{" · in use" if k=="1" else ""}<span class="tiny">{small}<em>16 px</em></span></figcaption></figure>' for k,lbl,big,small in P['VARS'])
socials=[('post-1080x1350-ink','Post · 1080×1350'),('post-1080x1350-white','Post · 1080×1350'),('story-1080x1920-number','Story · 1080×1920'),('reel-cover-1080x1920','Reel cover · 1080×1920'),('testimonial-1080x1350','Testimonial · 1080×1350')]
soch=''.join(f'<figure class="so"><img src="social/{n}.png" alt="{l}"><figcaption>{l}</figcaption></figure>' for n,l in socials)
fav=P['FAV']
html=f'''<title>Azm Brand Identity</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Readex+Pro:wght@400;600;700&family=IBM+Plex+Sans+Arabic:wght@400;500;600&display=swap" rel="stylesheet">
<style>
/* Layout: one calm column on paper; blue used as solid blocks, never as decoration */
:root{{--bg:#F4F6FB;--surface:#FFFFFF;--ink:#121A2E;--muted:#55607A;--line:#DDE3EF;--blue:#2457D6;--blue-ink:#2457D6;--amber:#F0A23B;--slate:#A7B1C6;--tint:#E6ECFB;
 --head:"Readex Pro","Segoe UI",Tahoma,sans-serif;--body:"IBM Plex Sans Arabic","Segoe UI",Tahoma,sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#0B1120;--surface:#121A2E;--ink:#EAF0FF;--muted:#93A0C4;--line:#243049;--blue-ink:#8FB0FF;--tint:#18233D;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#0B1120;--surface:#121A2E;--ink:#EAF0FF;--muted:#93A0C4;--line:#243049;--blue-ink:#8FB0FF;--tint:#18233D;color-scheme:dark}}
*{{box-sizing:border-box}}
body{{background:var(--bg);color:var(--ink);font-family:var(--body);font-size:16px;line-height:1.7;margin:0}}
.wrap{{max-width:1040px;margin:0 auto;padding-inline:16px;padding-block:0 80px}}
section{{padding-block:56px;border-top:1px solid var(--line)}}
h1,h2,h3{{font-family:var(--head);font-weight:700;line-height:1.3;margin:0;text-wrap:balance}}
h2{{font-size:clamp(26px,3.4vw,34px)}} h3{{font-size:18px;font-weight:600}}
.kicker{{font-family:var(--head);font-size:13px;font-weight:600;color:var(--blue-ink);margin:0 0 8px;letter-spacing:.04em}}
.lead{{color:var(--muted);max-width:62ch;margin:12px 0 0}}
svg,img{{display:block;max-width:100%;height:auto}}
[lang=ar]{{font-family:var(--head)}}
.hero{{background:#2457D6;color:#fff;border-radius:0 0 28px 28px;padding:72px 24px 56px;margin-inline:-16px;display:grid;gap:28px;justify-items:center;text-align:center}}
.hero .hero-lk{{width:min(80%,380px)}}
.hero p{{margin:0;max-width:46ch;color:#DCE6FD}} .hero p b{{color:#fff;font-weight:600}}
.facts{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,230px),1fr));gap:12px;margin-top:28px}}
.fact{{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:20px}}
.fact h3{{margin-bottom:6px}} .fact p{{margin:0;color:var(--muted);font-size:15px}}
.idea{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:32px;align-items:center;margin-top:28px}}
.idea .mkbox{{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:40px;display:grid;place-items:center}}
.idea .mkbox svg{{width:min(100%,220px)}}
.vars{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr));gap:12px;margin-top:28px}}
.var{{margin:0;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:18px}}
.var.pick{{border-color:var(--blue);box-shadow:0 0 0 1px var(--blue)}}
.vart svg{{width:min(100%,180px);margin:0 auto}}
.var figcaption{{display:flex;justify-content:space-between;align-items:center;gap:8px;margin-top:12px;font-size:14px}}
.tiny{{display:flex;gap:6px;align-items:center;color:var(--muted)}} .tiny em{{font-style:normal;font-size:12px}}
.lockups{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:12px;margin-top:28px}}
.lk-tile{{border-radius:12px;overflow:hidden;border:1px solid var(--line)}} .lk-tile svg{{width:100%}}
.lk-tile.alpha{{background:repeating-conic-gradient(#e9edf5 0 25%,#fff 0 50%) 0 0/20px 20px}}
.cap{{font-size:13px;color:var(--muted);margin-top:8px}}
.rules{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:24px;margin-top:28px;align-items:center}}
.rules .clear{{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:12px}}
.rules ul{{margin:0;padding-inline-start:20px;color:var(--muted)}} .rules li{{margin-bottom:6px}}
.favrow{{display:flex;gap:18px;align-items:flex-end;margin-top:14px;flex-wrap:wrap}}
.favrow div{{display:grid;gap:4px;justify-items:center;font-size:12px;color:var(--muted)}}
.donts{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,170px),1fr));gap:12px;margin-top:20px}}
.dont{{margin:0;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:14px;position:relative}}
.dont::after{{content:"";position:absolute;inset:14px 14px auto auto;width:14px;height:14px;border-radius:50%;background:#E5484D}}
.dont figcaption{{font-size:13px;color:var(--muted);margin-top:8px}}
.sws{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,180px),1fr));gap:12px;margin-top:28px}}
.sw{{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:12px;display:grid;gap:2px}}
.chip{{height:96px;border-radius:8px;margin-bottom:8px;border:1px solid rgba(0,0,0,.06)}}
.sw b{{font-family:var(--head);font-weight:600}} .sw code{{font-size:13px;color:var(--muted)}}
.sw span{{font-size:12px;font-weight:600;color:var(--blue-ink);margin-top:6px}} .sw small{{color:var(--muted);font-size:13px;line-height:1.5}}
.ratio{{display:flex;height:12px;border-radius:6px;overflow:hidden;margin-top:16px;border:1px solid var(--line)}}
.tw{{overflow-x:auto;margin-top:24px}}
table{{border-collapse:collapse;width:100%;font-size:14px;min-width:560px}}
th,td{{text-align:start;padding:10px 12px;border-bottom:1px solid var(--line);vertical-align:middle}} th{{font-weight:600;color:var(--muted);font-size:13px}}
.pv{{display:inline-block;padding:4px 10px;border-radius:6px;font-family:var(--head);font-weight:600}}
.num{{font-variant-numeric:tabular-nums}} .muted{{color:var(--muted)}}
.st{{font-size:12px;font-weight:600;padding:2px 10px;border-radius:999px}} .st.pass{{background:#19A97B22;color:#127a59}} .st.large{{background:#F0A23B33;color:#8a5a12}} .st.fail{{background:#E5484D22;color:#b3262b}}
:root[data-theme="dark"] .st.pass{{color:#5fd3a9}} :root[data-theme="dark"] .st.large{{color:#f5c27a}} :root[data-theme="dark"] .st.fail{{color:#ff8a8d}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]) .st.pass{{color:#5fd3a9}} :root:not([data-theme="light"]) .st.large{{color:#f5c27a}} :root:not([data-theme="light"]) .st.fail{{color:#ff8a8d}}}}
.type{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:12px;margin-top:28px}}
.tcard{{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:22px}}
.tcard .big{{font-size:44px;line-height:1.3;margin:6px 0 10px}} .tcard p{{margin:0;color:var(--muted);font-size:14px}}
.scale{{margin-top:16px;display:grid;gap:6px}} .scale div{{display:flex;justify-content:space-between;gap:12px;align-items:baseline;border-bottom:1px solid var(--line);padding-bottom:6px}}
.scale small{{color:var(--muted);font-variant-numeric:tabular-nums}}
.voice{{margin-top:24px}} .voice td[lang=ar]{{font-size:17px}} .voice td.no{{color:var(--muted);text-decoration:line-through;text-decoration-color:#E5484D88}}
.socials{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,180px),1fr));gap:12px;margin-top:28px;align-items:start}}
.so{{margin:0}} .so img{{border-radius:10px;border:1px solid var(--line)}} .so figcaption{{font-size:13px;color:var(--muted);margin-top:6px}}
.yt{{margin-top:12px;max-width:520px}}
.files{{columns:2 260px;color:var(--muted);font-size:14px;margin:16px 0 0;padding-inline-start:18px}} .files code{{color:var(--ink)}}
.note{{background:var(--tint);border-radius:12px;padding:18px 20px;margin-top:24px;font-size:15px}}
</style>
<main class="wrap">
<header class="hero">{P['HERO']}<p><b>عزم: resolve you act on.</b> Azm teaches Algerian Bac students how to study: a plan, past exam exercises, a daily log, and follow-up. It is not tutoring.</p></header>

<section>
 <p class="kicker">01 · The message</p>
 <h2>Students don't fail the Bac because it's hard. Nobody taught them how to study.</h2>
 <div class="facts">
  <div class="fact"><h3>Who it's for</h3><p>3AS students, mostly Sciences expérimentales, aged 16 to 19. Many average under 10/20. And the parents who pay and worry.</p></div>
  <div class="fact"><h3>What it teaches</h3><p>The method before the hours: a weekly plan, past exam exercises, logging every session, and follow-up.</p></div>
  <div class="fact"><h3>Who's behind it</h3><p>Riad, a medical student who went from 10 to 16 on the Bac in about three months by studying this way.</p></div>
  <div class="fact"><h3>How it sounds</h3><p>Calm, serious, honest, practical. A steady older brother who did it, not a motivational coach.</p></div>
 </div>
</section>

<section>
 <p class="kicker">02 · The mark</p>
 <h2>An ع whose curve keeps climbing</h2>
 <div class="idea">
  <div class="mkbox">{P['MARK']}</div>
  <p class="lead" style="margin:0">The mark is the first letter of عزم, drawn as one even stroke with rounded ends. The lower curve doesn't close. It drops, turns, and climbs back up past where it started, like steady progress. One step at a time, not a rocket. It's a single colour with no fine detail, so it still reads at 16 pixels.</p>
 </div>
 <h3 style="margin-top:40px">Three variations</h3>
 <p class="lead">Pick one and everything gets rebuilt from it. Variation 1 is in use until you choose.</p>
 <div class="vars">{vars_}</div>
</section>

<section>
 <p class="kicker">03 · Lockups</p>
 <h2>Mark and name</h2>
 <p class="lead">In Arabic, the mark sits on the right and عزم follows, reading right to left. For French or English, use the mark with “Azm”.</p>
 <div class="lockups">
  <div><div class="lk-tile">{P['AR_blue-on-white']}</div><p class="cap">Blue on white</p></div>
  <div><div class="lk-tile">{P['AR_white-on-blue']}</div><p class="cap">White on blue</p></div>
  <div><div class="lk-tile">{P['AR_white-on-ink']}</div><p class="cap">White on ink</p></div>
  <div><div class="lk-tile alpha">{P['AR_ink']}</div><p class="cap">Single colour, ink</p></div>
  <div><div class="lk-tile alpha">{P['LAT']}</div><p class="cap">Latin lockup, for French and English</p></div>
 </div>
 <div class="rules">
  <div class="clear">{P['CLEAR']}</div>
  <div><h3>Space and size</h3><ul><li>Keep clear space equal to the height of the ع's lower curve on every side (shaded).</li><li>Smallest mark: 20 px. Smallest lockup: 80 px wide.</li><li>Favicon at real size:</li></ul>
   <div class="favrow"><div><svg viewBox="0 0 64 64" width="16">{fav}</svg>16</div><div><svg viewBox="0 0 64 64" width="32">{fav}</svg>32</div><div><svg viewBox="0 0 64 64" width="48">{fav}</svg>48</div><div><svg viewBox="0 0 64 64" width="64" style="border-radius:50%;overflow:hidden">{fav}</svg>Android</div></div></div>
 </div>
 <h3 style="margin-top:40px">Don't</h3>
 <div class="donts">{P['DONTS']}</div>
</section>

<section>
 <p class="kicker">04 · Colour</p>
 <h2>Blue, and almost nothing else</h2>
 <p class="lead">Five colours. Blue carries the brand: calm for parents, focus for students. Amber is the only warm colour, used once per screen at most. No purple, no gradients.</p>
 <div class="sws">{swh}</div>
 <div class="ratio" aria-label="Usage ratio"><i style="flex:55;background:#F4F6FB"></i><i style="flex:30;background:#2457D6"></i><i style="flex:10;background:#121A2E"></i><i style="flex:4;background:#A7B1C6"></i><i style="flex:1;background:#F0A23B"></i></div>
 <div class="tw"><table><thead><tr><th>Sample</th><th>Pair</th><th>Contrast</th><th>WCAG AA</th><th>Rule</th></tr></thead><tbody>{rows}</tbody></table></div>
</section>

<section>
 <p class="kicker">05 · Type</p>
 <h2>Two Arabic faces</h2>
 <div class="type">
  <div class="tcard"><h3>Readex Pro · headings</h3><p class="big" lang="ar">حصتان اليوم.</p><p>Weights 600 and 700. Also used for the wordmark and for numbers that matter.</p></div>
  <div class="tcard"><h3 style="font-family:var(--head)">IBM Plex Sans Arabic · body</h3><p class="big" style="font-family:var(--body);font-weight:400;font-size:28px" lang="ar">ابدأ بالعلوم، ثم سجّل ما أنجزته.</p><p>Weights 400, 500 and 600. Line height 1.7, because Arabic needs room.</p></div>
 </div>
 <div class="scale" lang="ar" dir="rtl">
  <div><span style="font-size:3.5rem;font-family:var(--head);font-weight:700;line-height:1.1" class="num">124</span><small>Display 3.5 rem · countdown only</small></div>
  <div><span style="font-size:2.25rem;font-family:var(--head);font-weight:700">العنوان الرئيسي</span><small>H1 2.25 rem</small></div>
  <div><span style="font-size:1.75rem;font-family:var(--head);font-weight:600">عنوان القسم</span><small>H2 1.75 rem</small></div>
  <div><span style="font-size:1.375rem;font-family:var(--head);font-weight:600">عنوان فرعي</span><small>H3 1.375 rem</small></div>
  <div><span style="font-size:1rem">نص عادي للشرح والتعليمات.</span><small>Body 1 rem</small></div>
  <div><span style="font-size:.75rem;color:var(--muted)">ملاحظة صغيرة</span><small>Caption 0.75 rem</small></div>
 </div>
 <p class="lead">Western digits (0–9), as used in Algeria, with tabular figures for scores, timers and stats.</p>
</section>

<section>
 <p class="kicker">06 · Voice</p>
 <h2>Concrete actions, real numbers, no hype</h2>
 <p class="lead">Simple Modern Standard Arabic in the app, Darija is fine on social, French for the terms students already use. Never promise a grade. Address each student in the form that matches their gender.</p>
 <div class="tw voice"><table><thead><tr><th>Write like this</th><th>Not like this</th></tr></thead><tbody>
  <tr><td lang="ar" dir="rtl">حصتان اليوم. ابدأ بالعلوم.</td><td lang="ar" dir="rtl" class="no">انطلق نحو النجاح!!</td></tr>
  <tr><td lang="ar" dir="rtl">ضيّعت يوماً؟ زِد نصف ساعة غداً وواصل.</td><td lang="ar" dir="rtl" class="no">لا تستسلم أبداً، أنت بطل!</td></tr>
  <tr><td lang="ar" dir="rtl">الطريقة قبل الساعات.</td><td lang="ar" dir="rtl" class="no">احصل على 18 مضمونة!</td></tr>
 </tbody></table></div>
</section>

<section>
 <p class="kicker">07 · Social</p>
 <h2>Templates with a lot of empty space</h2>
 <p class="lead">At most two colours plus white, no photos, no emoji. One idea per post. The testimonial card is a blank template: fill it with a real student's grades and words, first name or initials only.</p>
 <div class="socials">{soch}</div>
 <figure class="so yt"><img src="social/youtube-thumbnail-1280x720.png" alt="YouTube thumbnail"><figcaption>YouTube thumbnail · 1280×720 · four words at most, one big number</figcaption></figure>
</section>

<section>
 <p class="kicker">Files</p>
 <h2>What's in the folder</h2>
 <ul class="files"><li><code>svg/</code>: mark, Arabic lockup and Latin lockup in four colour versions, plus variations 2 and 3</li><li><code>png/</code>: every logo at 512 and 1024 px</li><li><code>icons/</code>: favicon.svg and .ico, apple-touch-icon 180, PWA icons 192 and 512, maskable 192 and 512</li><li><code>social/</code>: each template as editable HTML plus a PNG</li><li><code>BRAND.md</code>: this page on one sheet</li></ul>
 <p class="note">Not done yet, because the app's code isn't in this session: redrawing the owl mascot, design tokens in the app, replacing the purple theme, and the /brand page. Those need the Azm app repo.</p>
</section>
</main>'''
open(sys.argv[1],'w').write(html)
