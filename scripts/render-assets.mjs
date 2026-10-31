import { chromium } from '@playwright/test';
import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { resolve, sep, extname } from 'node:path';
const root=resolve('public');
const server=createServer(async(req,res)=>{
  try{
    let pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
    if(pathname.endsWith('/'))pathname+='index.html';
    const file=resolve(root,'.'+pathname);
    if(!file.startsWith(root+sep)){res.writeHead(403);res.end();return;}
    res.setHeader('Content-Type',({'.css':'text/css','.js':'text/javascript','.svg':'image/svg+xml','.png':'image/png'})[extname(file)]||'text/html');
    res.end(await readFile(file));
  }catch{res.writeHead(404);res.end();}
});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
const browser = await chromium.launch({ headless: true, ...(process.env.CHROME_PATH ? { executablePath: process.env.CHROME_PATH, args: ['--no-sandbox'] } : {}) });
try {
  for (const lang of ['es','en']) {
    const page = await browser.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
    await page.setContent('<!doctype html><html lang="'+lang+'"><meta charset="utf-8"><style>body{margin:0;width:1200px;height:630px;background:#09172d;color:white;font-family:Arial,sans-serif;box-sizing:border-box;padding:80px 88px}b{font-size:34px}h1{font-size:88px;line-height:1.12;letter-spacing:-3px;margin:82px 0 48px}em{font-style:normal;color:#13bf79}p{font-size:28px;color:#c7d3e3}</style><b>readytoprod</b><h1>'+(lang==='es'?'Menos tareas.<br><em>Más negocio.</em>':'Fewer tasks.<br><em>More business.</em>')+'</h1><p>'+(lang==='es'?'Automatización y desarrollo web a medida.':'Custom automation and web development.')+'</p></html>');
    await page.screenshot({ path: 'public/social'+(lang==='en'?'-en':'')+'.png' });
    await page.setViewportSize({width:1120,height:850});
    await page.goto('http://127.0.0.1:'+server.address().port+(lang==='es'?'/demo/':'/en/demo/'));
    await page.locator('#demo-volume').fill('42');
    await page.locator('#demo-urgency').selectOption('urgent');
    await page.locator('#demo-form button[type=submit]').click();
    await page.locator('.demo-layout').screenshot({path:'public/demo-preview-'+lang+'.png'});
    await page.close();
  }
} finally { await browser.close(); server.close(); }
