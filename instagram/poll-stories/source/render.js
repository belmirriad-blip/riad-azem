const { chromium } = require('playwright');
const path = require('path');
const D = __dirname;
const MARK = "M95.18,28.59 L93.03,24.53 L90.50,20.68 L87.64,17.08 L84.67,13.98 L81.22,10.94 L77.49,8.24 L73.54,5.89 L69.39,3.91 L65.36,2.42 L60.92,1.21 L56.39,0.41 L51.81,0.03 L47.21,0.08 L42.63,0.55 L38.12,1.43 L33.85,2.68 L39.16,7.09 L43.79,11.53 L48.12,16.26 L52.12,21.29 L55.77,26.56 L59.06,32.08 L61.97,37.80 L64.69,44.25 L66.93,50.88 L68.55,57.09 L69.75,63.40 L70.52,69.77 L70.86,76.18 L70.74,83.18 L70.17,89.58 L69.12,96.20 L73.60,94.08 L78.06,91.38 L82.22,88.24 L85.81,84.89 L89.25,80.98 L92.10,76.98 L94.68,72.45 L96.66,67.96 L98.28,63.01 L99.32,58.21 L99.89,53.34 L99.96,48.13 L99.54,43.24 L98.57,38.12 L97.07,33.12ZM30.83,3.82 L26.40,5.92 L22.45,8.28 L18.73,10.98 L15.06,14.24 L11.92,17.60 L8.93,21.49 L6.33,25.65 L4.15,30.05 L2.42,34.64 L1.14,39.38 L0.34,44.22 L0.01,48.81 L0.12,53.41 L0.69,58.28 L1.74,63.07 L3.25,67.74 L5.22,72.24 L7.45,76.26 L10.23,80.30 L13.39,84.06 L16.68,87.28 L20.49,90.36 L24.59,93.06 L28.65,95.21 L32.90,96.98 L37.59,98.43 L42.39,99.42 L47.27,99.93 L52.18,99.95 L56.76,99.54 L61.59,98.64 L66.15,97.32 L60.84,92.91 L56.21,88.47 L51.88,83.74 L47.88,78.71 L44.23,73.44 L40.94,67.92 L38.03,62.20 L35.31,55.75 L33.24,49.67 L31.45,42.91 L30.25,36.60 L29.48,30.23 L29.14,23.82 L29.23,17.40 L29.76,11Z";
const C = { bone:'#F1EBE0', night:'#15120F', dune:'#4A3326' };
// hoodie PNGs = cut + 60px padding; cut sizes:
const H = { 1:{w:740,h:935}, 2:{w:870,h:984} }, PAD=60;
const T=170, k=T/90, sc=0.32*k;
const tile=(id,fill,op)=>`<pattern id="${id}" width="${T}" height="${T}" patternUnits="userSpaceOnUse" patternTransform="rotate(-8)">
 <g opacity="${op}"><g transform="translate(${6.5*k},${6.5*k}) scale(${sc})"><path fill="${fill}" d="${MARK}"/></g>
 <g transform="translate(${51.5*k},${51.5*k}) scale(${sc})"><path fill="${fill}" d="${MARK}"/></g></g></pattern>`;
const WAVE="M0,1452 C300,1392 640,1478 1080,1418 L1080,1920 L0,1920 Z";

function hoodies(ids, top, bottom){
  // same scale for all garments; fit into 1080-2*margin width and top..bottom height
  const gap=ids.length>1?8:0, maxW=ids.length>1?1050:900;
  const tw=ids.reduce((s,i)=>s+H[i].w,0), th=Math.max(...ids.map(i=>H[i].h));
  const s=Math.min((maxW-gap)/tw,(bottom-top)/th);
  let x=(1080-(tw*s+gap))/2, out='';
  for(const i of ids){
    const w=H[i].w*s, h=H[i].h*s, y=bottom-h- (th*s-h)/2 - ((bottom-top)-th*s)/2;
    out+=`<img src="file://${D}/work/hoodie${i}.png" style="position:absolute;left:${x-PAD*s}px;top:${y-PAD*s}px;width:${(H[i].w+2*PAD)*s}px">`;
    x+=w+gap;
  }
  return out;
}
function page({main,sub,ids,top,bottom,dark}){
  const bg=dark?C.night:C.bone, fg=dark?C.bone:C.night, pf=dark?C.bone:C.night, po=dark?0.12:0.09;
  return `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Plex;src:url(file://${D}/fontpkg/package/fonts/complete/woff2/IBMPlexSansArabic-SemiBold.woff2) format('woff2');font-weight:600}
html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:${bg}}
.t{position:absolute;top:290px;left:90px;right:90px;text-align:center;direction:rtl;font-family:Plex;font-weight:600;color:${fg}}
.m{font-size:76px;line-height:1.32}
.s{font-size:52px;line-height:1.3;opacity:.75;margin-top:26px}
</style></head><body>
<svg width="1080" height="1920" style="position:absolute;inset:0"><defs>${tile('p',pf,po)}${tile('q',C.bone,0.10)}</defs>
<rect width="1080" height="1920" fill="${bg}"/><rect width="1080" height="1920" fill="url(#p)"/>
<path d="${WAVE}" fill="${C.dune}"/><path d="${WAVE}" fill="url(#q)"/></svg>
${hoodies(ids,top,bottom)}
<div class="t"><div class="m">${main.join('<br>')}</div>${sub?`<div class="s">${sub}</div>`:''}</div>
</body></html>`;
}
const stories=[
  {n:1,main:['لقيت هاد الهودي','وعجبني بزاف.'],sub:'قطن تقيل · قصة واسعة',ids:[1],top:620,bottom:1385},
  {n:2,main:['كون صريح…','تلبسها؟'],ids:[1],top:560,bottom:1385},
  {n:3,main:['إذا عجبتك…','واش من لون؟'],ids:[1,2],top:560,bottom:1385},
];
(async()=>{
  const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
  for(const dark of [false,true]) for(const s of stories){
    const hf=path.join(D,'out','tmp.html'); require('fs').writeFileSync(hf,page({...s,dark})); await p.goto('file://'+hf,{waitUntil:'load'}); await p.evaluate(()=>document.fonts.ready); console.log(await p.evaluate(()=>[document.fonts.check('600 76px Plex'),[...document.images].map(i=>i.naturalWidth)]));
    const f=path.join(D,'out',`ostro-poll-${s.n}${dark?'-dark':''}.png`); await p.screenshot({path:f}); console.log(f);
    if(!dark&&s.n==1) console.log(await p.evaluate(()=>[...document.querySelectorAll('.t,.m,.s')].map(e=>e.getBoundingClientRect().bottom)));
  }
  await b.close();
})();
