// Baca geometri kad kaca (window.__glass) dari motion/editorial untuk blur sebenar dalam compose.py
// Guna: node pipeline/probe_glass.js <dir-template> <gaya>   → cetak JSON
const { chromium } = require('playwright');
(async () => {
  const [, , dir, style] = process.argv;
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.addInitScript((s) => { window.__hyperframes = { getVariables: () => ({ style: s }) }; }, style);
  await p.goto('file://' + dir + '/index.html', { waitUntil: 'domcontentloaded' });
  await p.evaluate(() => document.fonts.ready.then(() => 1));
  await p.waitForTimeout(300);
  console.log(JSON.stringify(await p.evaluate(() => (window.__glassRefs || []).map((f) => f()))));
  await b.close();
})();
