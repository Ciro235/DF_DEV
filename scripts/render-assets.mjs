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
    await page.goto('http://127.0.0.1:'+server.address().port+(lang==='es'?'/':'/en/'));
    await page.setContent('<!doctype html><html lang="'+lang+'"><meta charset="utf-8"><style>@font-face{font-family:Manrope;src:url(/fonts/manrope.ttf);font-weight:400 800}body{margin:0;width:1200px;height:630px;background:linear-gradient(120deg,#fff,#edf7ff 70%,#e9f9ef);color:#142144;font-family:Manrope,Arial,sans-serif;box-sizing:border-box;padding:65px 82px}b{font-size:32px;letter-spacing:-1px}h1{font-size:72px;line-height:1.2;letter-spacing:-2.5px;margin:65px 0 32px;font-weight:800}em{font-style:normal;color:#078149}.blue{color:#0860e9}p{font-size:25px;color:#53627c}</style><b>readytoprod</b><h1>'+(lang==='es'?'Soluciones digitales.<br><span class="blue">Menos tareas.</span> <em>Más negocio.</em>':'Digital solutions.<br><span class="blue">Fewer tasks.</span> <em>More business.</em>')+'</h1><p>'+(lang==='es'?'Desarrollo, IA y automatización a medida.':'Custom development, AI and automation.')+'</p></html>');
    await page.evaluate(()=>document.fonts.ready);
    await page.screenshot({ path: 'public/social'+(lang==='en'?'-en':'')+'.png' });
    await page.setViewportSize({width:1120,height:850});
    await page.goto('http://127.0.0.1:'+server.address().port+(lang==='es'?'/demo/':'/en/demo/'));
    await page.evaluate(()=>document.fonts.ready);
    await page.locator('#demo-volume').fill('42');
    await page.locator('#demo-urgency').selectOption('urgent');
    await page.locator('#demo-form button[type=submit]').click();
    await page.locator('.demo-layout').screenshot({path:'public/demo-preview-'+lang+'.png'});
    await page.close();
  }
} finally { await browser.close(); server.close(); }
