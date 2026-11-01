const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage();const [dir,out]=process.argv.slice(2);
for(const f of fs.readdirSync(dir).filter(f=>f.endsWith('.svg'))){const svg=fs.readFileSync(path.join(dir,f),'utf8');
 const vb=svg.match(/viewBox="([^"]+)"/)[1].split(' ').map(Number);
 for(const W of [512,1024]){const H=Math.round(W*vb[3]/vb[2]);await p.setViewportSize({width:W,height:H});
  await p.setContent(`<html><body style="margin:0;background:transparent">${svg.replace('<svg ',`<svg width="${W}" height="${H}" `)}</body></html>`);
  await p.screenshot({path:path.join(out,f.replace('.svg',`-${W}.png`)),omitBackground:true});}}
await b.close();})();
