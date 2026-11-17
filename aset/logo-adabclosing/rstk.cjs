const {chromium}=require('playwright'),path=require('path');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1080},deviceScaleFactor:1});
for(const v of ['ref','brand','dark']){await p.goto('file://'+path.resolve(__dirname,'sticker.html')+'?p='+v);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(400);await p.screenshot({path:path.resolve(__dirname,`logo_sticker_${v}.png`)});}
await b.close()})();
