import { test, expect } from '@playwright/test';
import { readFile } from 'node:fs/promises';

for (const lang of ['es','en']) {
  const root = lang === 'es' ? '/' : '/en/';
  for (const width of [320,390,768,901,1440]) {
    test(lang+' layout '+width, async ({ page }) => {
      await page.setViewportSize({ width, height: 900 });
      await page.goto(root);
      await expect(page.locator('html')).toHaveAttribute('lang',lang);
      await expect(page.locator('h1')).toBeVisible();
      expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
      expect(await page.evaluate(() => {
        const a=document.querySelector('.terminal').getBoundingClientRect();
        const b=document.querySelector('.hero-foot').getBoundingClientRect();
        return Math.min(a.right,b.right)<=Math.max(a.left,b.left)||Math.min(a.bottom,b.bottom)<=Math.max(a.top,b.top);
      })).toBe(true);
      if (width<=800) {
        await expect(page.locator('#main-nav')).toBeHidden();
        await page.locator('#menu-toggle').click();
        await expect(page.locator('#main-nav')).toBeVisible();
        await page.keyboard.press('Escape');
        await expect(page.locator('#main-nav')).toBeHidden();
        await expect(page.locator('#menu-toggle')).toBeFocused();
      }
      await page.locator('summary').first().focus();
      await page.keyboard.press('Enter');
      await expect(page.locator('details').first()).toHaveAttribute('open','');
    });
  }
  test(lang+' demo responds to choices and downloads actual data', async ({ page }) => {
    await page.goto(root+'demo/');
    await page.locator('#demo-form button[type=submit]').click();
    const first=await page.locator('#demo-result').textContent();
    await page.locator('#demo-urgency').selectOption('urgent');
    await page.locator('#demo-volume').fill('42');
    await page.locator('#demo-form button[type=submit]').click();
    expect(await page.locator('#demo-result').textContent()).not.toBe(first);
    await expect(page.locator('#demo-result')).toContainText('42');
    const pending=page.waitForEvent('download');
    await page.locator('#demo-download').click();
    const file=await (await pending).path();
    expect(await readFile(file,'utf8')).toContain('42');
    await page.locator('#demo-reset').click();
    await expect(page.locator('#demo-download')).toBeHidden();
    await expect(page.locator('#demo-result')).toBeEmpty();
  });
  test(lang+' mock legal data cannot imply an inquiry was sent', async ({ page }) => {
    await page.goto(lang==='es'?'/contacto/':'/en/contact/');
    let posts=0;
    page.on('request', req=>{if(req.method()==='POST')posts++;});
    await page.locator('#contact-service').selectOption('web');
    await page.locator('#contact-message').fill('Necesitamos organizar las solicitudes del formulario de nuestra web.');
    await page.locator('#contact-form button[type=submit]').click();
    await expect(page.locator('#contact-status a')).toHaveAttribute('href',/mailto:dariosc235@gmail.com/);
    await expect(page.locator('#contact-status a')).toHaveAttribute('href',/cc=fsegui16%40gmail.com/);
    await expect(page.locator('#contact-form')).toHaveAttribute('data-mode','email');
    expect(posts).toBe(0);
    expect(await page.locator('#contact-status').textContent()).not.toMatch(/aceptada para su envío|accepted for delivery/);
  });
}
test('language switch uses equivalent service URL', async ({ page }) => {
  await page.goto('/servicios/automatizacion/');
  await page.locator('[data-language=en]').click();
  await expect(page).toHaveURL(/\/en\/services\/automation\/$/);
  await expect(page.locator('html')).toHaveAttribute('lang','en');
});
test('all sections and languages are readable without JavaScript', async ({ browser }) => {
  const context=await browser.newContext({javaScriptEnabled:false});
  const page=await context.newPage();
  await page.goto('/en/');
  await expect(page.locator('#main-nav')).toBeVisible();
  await expect(page.locator('#menu-toggle')).toBeHidden();
  await page.locator('[data-language=es]').click();
  await expect(page.locator('html')).toHaveAttribute('lang','es');
  await context.close();
});
test('unknown page returns HTTP 404',async ({request})=>{
  const response=await request.get('/a-page-that-does-not-exist/');
  expect(response.status()).toBe(404);
});
