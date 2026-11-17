const {chromium}=require('playwright'),path=require('path');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1080},deviceScaleFactor:2});
await p.goto('file://'+path.resolve(__dirname,'logo3d.html'));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(500);
await p.screenshot({path:path.resolve(__dirname,'logo_v2_3d@2x.png')});await b.close()})();
