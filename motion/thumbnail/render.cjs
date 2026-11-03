// Render thumbnail: node render.cjs out.png  (Playwright + Chromium yang dah ada dalam environment)
const { chromium } = require("playwright");
const path = require("node:path");
(async () => {
  const out = process.argv[2] || "thumbnail.png";
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.goto("file://" + path.resolve(__dirname, "index.html"));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(300);
  await p.screenshot({ path: out });
  await b.close();
})();
