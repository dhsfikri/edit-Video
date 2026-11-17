const {chromium}=require('playwright'),path=require('path');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1080}});
for(const v of ['v1','v2','v3']){await p.goto('file://'+path.resolve(__dirname,'logo.html'));await p.evaluate(v=>{document.body.className=v},v);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);await p.screenshot({path:path.resolve(__dirname,`logo_${v}.png`)});}
await b.close()})();
