const {chromium}=require('playwright'),path=require('path');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1080},deviceScaleFactor:2});
await p.goto('file://'+path.resolve(__dirname,'sticker.html')+'?p=brand');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(400);
await p.screenshot({path:path.resolve(__dirname,'adabclosing_profil_2160.png')});
await p.evaluate(()=>document.querySelector('svg rect').remove());
await p.addStyleTag({content:'html,body{background:transparent!important}'});
await p.screenshot({path:path.resolve(__dirname,'adabclosing_telus_2160.png'),omitBackground:true});await b.close()})();
