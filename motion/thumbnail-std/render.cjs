// node render.cjs config.json out.png
const { chromium } = require("playwright");
const path = require("node:path"), fs = require("node:fs");
(async () => {
  const cfg = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.goto("file://" + path.resolve(__dirname, "index.html"));
  await p.evaluate((c) => window.render(c), cfg);
  await p.screenshot({ path: process.argv[3] });
  await b.close();
})();
