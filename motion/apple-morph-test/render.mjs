// Render index.html frame demi frame (deterministik ikut masa) → JPEG → ffmpeg
// Guna: npm install && node render.mjs <output.mp4> [fps=30] [saat=4]
//       node render.mjs <prefix> 30 4 0.6,2.3   → still JPEG pada masa tertentu
import { createRequire } from "node:module";
import { execSync } from "node:child_process";
// Playwright: guna yang dipasang global (sudah ada dalam environment cloud)
const globalRoot = execSync("npm root -g").toString().trim() + "/";
const { chromium } = createRequire(globalRoot)("playwright");
import { spawn } from "node:child_process";
import http from "node:http";
import fs from "node:fs";
import path from "node:path";

const [, , outFile, fpsArg = "30", durArg = "4", onlyT] = process.argv;
const root = path.dirname(new URL(import.meta.url).pathname);
const types = { ".html": "text/html", ".js": "text/javascript", ".mjs": "text/javascript", ".woff2": "font/woff2" };
const server = http.createServer((req, res) => {
  const p = path.join(root, decodeURIComponent(req.url.split("?")[0]));
  if (!p.startsWith(root) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { "content-type": types[path.extname(p)] || "application/octet-stream" });
  fs.createReadStream(p).pipe(res);
}).listen(0);
const port = server.address().port;

const browser = await chromium.launch({ args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"] });
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
page.on("console", (m) => console.log("[page]", m.text()));
page.on("pageerror", (e) => console.log("[pageerror]", e.message));
await page.goto(`http://127.0.0.1:${port}/index.html${process.env.Q || ""}`);
await page.waitForFunction(() => window.ready === true, null, { timeout: 30000 });

const decode = (u) => Buffer.from(u.split(",")[1], "base64");
if (onlyT !== undefined) {
  for (const t of onlyT.split(",")) fs.writeFileSync(`${outFile}-${t}.jpg`, decode(await page.evaluate((t) => window.renderAt(t), Number(t))));
} else {
  const fps = Number(fpsArg), n = Math.round(fps * Number(durArg));
  const ff = spawn("ffmpeg", ["-v", "error", "-y", "-f", "image2pipe", "-framerate", String(fps), "-c:v", "mjpeg", "-i", "-",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-b:v", "16M", "-maxrate", "20M", "-bufsize", "32M", "-movflags", "+faststart", outFile], { stdio: ["pipe", "inherit", "inherit"] });
  for (let i = 0; i < n; i++) {
    ff.stdin.write(decode(await page.evaluate((t) => window.renderAt(t), i / fps)));
    if (i % 15 === 0) spawn("bash", [process.env.CLAUDE_PROGRESS_SH || "/bin/true", "-n", "render-3d", `${i}/${n}`], { stdio: "ignore" });
  }
  ff.stdin.end();
  await new Promise((r) => ff.on("close", r));
}
await browser.close();
server.close();
