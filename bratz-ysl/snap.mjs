// Render still frames of index.html with headless Chromium.
// Usage: node snap.mjs out_dir shot1 shot2 ...
import { createRequire } from 'node:module';
const { chromium } = createRequire(import.meta.url)(process.env.PW || 'playwright');
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';

const root = path.dirname(new URL(import.meta.url).pathname);
const types = { '.html': 'text/html', '.js': 'text/javascript', '.glb': 'model/gltf-binary', '.json': 'application/json' };
const server = http.createServer((req, res) => {
  const p = path.join(root, decodeURIComponent(req.url.split('?')[0]));
  fs.readFile(p, (e, d) => { if (e) { res.writeHead(404); res.end(); return; }
    res.writeHead(200, { 'Content-Type': types[path.extname(p)] || 'application/octet-stream' }); res.end(d); });
}).listen(0);
const port = server.address().port;
const [out = 'renders', ...shots] = process.argv.slice(2);
fs.mkdirSync(out, { recursive: true });
const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
page.on('console', m => console.log('[page]', m.text()));
page.on('pageerror', e => console.log('[err]', e.message));
await page.goto(`http://localhost:${port}/index.html?doll=${process.env.DOLL||'kylie'}`);
await page.waitForFunction('window.__ready === true', null, { timeout: 180000 });
console.log(await page.evaluate('JSON.stringify(window.__info)'));
for (const s of (shots.length ? shots : ['hero'])) {
  const [sn, r] = s.split(':'); await page.evaluate(([n, rr]) => window.setShot(n, +rr || 0), [sn, r]);
  await page.locator('canvas').screenshot({ path: `${out}/${process.env.DOLL||'kylie'}_${s.replace(':','_')}.png` });
  console.log('saved', s);
}
await browser.close(); server.close();
