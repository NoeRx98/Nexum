// Renders every html/*.html into ../out/<name>.jpg at its native ad size.
import { chromium } from 'playwright';
import fs from 'fs'; import path from 'path'; import { fileURLToPath } from 'url';
const here = process.env.ADS_SRC || path.dirname(fileURLToPath(import.meta.url));
const out = path.join(here, '..', 'out'); fs.mkdirSync(out, { recursive: true });
const only = process.argv[2] || '';
const b = await chromium.launch();
for (const f of fs.readdirSync(path.join(here, 'html')).filter(f => f.endsWith('.html') && f.includes(only)).sort()) {
  const [w, h] = { '1x1': [1080, 1080], '4x5': [1080, 1350], '9x16': [1080, 1920] }[f.match(/_(\dx\d+)\.html$/)[1]];
  const p = await (await b.newContext({ viewport: { width: w, height: h } })).newPage();
  await p.goto((process.env.ADS_URL ? process.env.ADS_URL + '/html/' + f : 'file://' + path.join(here, 'html', f)), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: path.join(out, f.replace('.html', '.jpg')), type: 'jpeg', quality: 90 });
  await p.close();
}
await b.close();
console.log('rendered');
