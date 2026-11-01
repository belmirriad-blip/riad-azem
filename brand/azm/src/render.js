const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
const L=JSON.parse(fs.readFileSync('socsrc/list.json'));const out=process.argv[2];
for(const [n,w,h] of L){await p.setViewportSize({width:w,height:h});await p.goto('file://'+process.cwd()+'/socsrc/'+n+'.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);await p.screenshot({path:out+'/'+n+'.png'});}
const I=fs.readdirSync('iconsrc');
for(const f of I){const svg=fs.readFileSync('iconsrc/'+f,'utf8');const s=+svg.match(/viewBox="0 0 ([\d.]+)/)[1];await p.setViewportSize({width:s,height:s});await p.setContent(`<html><body style="margin:0;background:transparent">${svg.replace('<svg ',`<svg width="${s}" height="${s}" `)}</body></html>`);await p.screenshot({path:process.argv[3]+'/'+f.replace('.svg','.png'),omitBackground:true});}
await b.close();})();
