// Local stand-in for Vercel: serves the repo as static files, applies vercel.json redirects,
// and runs the real /api/lead edge function, so tests go page -> relay -> (fake) GHL end to end.
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const TYPES = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.svg': 'image/svg+xml',
  '.json': 'application/json', '.xml': 'application/xml', '.txt': 'text/plain', '.ico': 'image/x-icon' };

let ipCounter = 0;

export async function startSite() {
  const vercel = JSON.parse(fs.readFileSync(path.join(ROOT, 'vercel.json'), 'utf8'));
  const { default: handler } = await import(path.join(ROOT, 'api/lead.js'));
  const srv = http.createServer(async (req, res) => {
    try {
      const url = new URL(req.url, 'http://local');
      for (const r of vercel.redirects || []) {
        const re = new RegExp('^' + r.source.replace(/\(\.\*\)/g, '.*') + '$');
        if (re.test(url.pathname)) { res.writeHead(r.permanent ? 308 : 307, { Location: r.destination }); return res.end(); }
      }
      if (url.pathname === '/api/lead') {
        const chunks = []; for await (const c of req) chunks.push(c);
        // each browser submission gets its own fake IP so the relay's rate limit does not trip between tests
        const ip = req.headers['x-forwarded-for'] || `10.0.${Math.floor(++ipCounter / 250)}.${ipCounter % 250}`;
        const request = new Request('http://localhost' + req.url, {
          method: req.method,
          headers: { 'content-type': req.headers['content-type'] || '', 'x-forwarded-for': ip, host: 'localhost' },
          body: ['GET', 'HEAD'].includes(req.method) ? undefined : Buffer.concat(chunks)
        });
        const out = await handler(request);
        res.writeHead(out.status, Object.fromEntries(out.headers));
        return res.end(Buffer.from(await out.arrayBuffer()));
      }
      let p = decodeURIComponent(url.pathname);
      if (p.endsWith('/')) p += 'index.html';
      const f = path.join(ROOT, p);
      if (!f.startsWith(ROOT + path.sep) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end('not found'); }
      res.writeHead(200, { 'content-type': TYPES[path.extname(f).toLowerCase()] || 'application/octet-stream' });
      fs.createReadStream(f).pipe(res);
    } catch (e) { res.writeHead(500); res.end(String(e)); }
  });
  await new Promise(r => srv.listen(0, '127.0.0.1', r));
  return { url: `http://127.0.0.1:${srv.address().port}`, close: () => new Promise(r => srv.close(r)) };
}

// A fake GHL inbound webhook. mode: "ok" | "down" (500) | "slow" (answers after `slowMs`).
export async function startFakeGHL() {
  const state = { mode: 'ok', slowMs: 9000, hits: 0, bodies: [] };
  const srv = http.createServer((req, res) => {
    let b = ''; req.on('data', d => b += d);
    req.on('end', () => {
      state.hits++;
      try { state.bodies.push(JSON.parse(b)); } catch { state.bodies.push(b); }
      if (state.mode === 'down') { res.statusCode = 500; return res.end(); }
      if (state.mode === 'slow') return setTimeout(() => res.end('{}'), state.slowMs);
      res.setHeader('content-type', 'application/json'); res.end('{"ok":true}');
    });
  });
  await new Promise(r => srv.listen(0, '127.0.0.1', r));
  const url = `http://127.0.0.1:${srv.address().port}/hook`;
  return {
    url, state,
    reset(mode = 'ok') { state.mode = mode; state.hits = 0; state.bodies = []; },
    close: () => new Promise(r => { srv.closeAllConnections?.(); srv.close(r); })
  };
}
