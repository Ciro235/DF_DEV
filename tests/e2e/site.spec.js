import { test, expect } from '@playwright/test';

for (const lang of ['es','en']) {
  const root = lang === 'es' ? '/' : '/en/';
  for (const width of [320,390,768,901,1440]) {
    test(lang+' layout '+width, async ({ page }) => {
      await page.setViewportSize({ width, height: 900 });
      await page.goto(root);
      await page.evaluate(() => document.fonts.ready);
      await expect(page.locator('html')).toHaveAttribute('lang',lang);
      await expect(page.locator('h1')).toBeVisible();
      await expect.poll(() => page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
      expect(await page.evaluate(() => {
        const a=document.querySelector('.hero-art').getBoundingClientRect();
        const b=document.querySelector('.hero').getBoundingClientRect();
        return a.left>=b.left && a.right<=b.right && a.top>=b.top && a.bottom<=b.bottom;
      })).toBe(true);
      await expect.poll(() => page.locator('#services').evaluate(section => section.getBoundingClientRect().top)).toBeLessThan(900);
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
  test(lang+' removed organizer and team contact cards', async ({ page, request }) => {
    expect((await request.get(root+'demo/')).status()).toBe(404);
    await page.goto(root+'team/');
    await expect(page.locator('.team-card')).toHaveCount(2);
    await expect(page.locator('.team-card').first()).toHaveAttribute('href','mailto:fsegui16@gmail.com');
    await expect(page.locator('.team-card').last()).toHaveAttribute('href','mailto:dariosc235@gmail.com');
    await expect(page.locator('a[href*="/demo/"]')).toHaveCount(0);
    await expect(page.locator('.hero-art')).toHaveCount(0);
    await page.goto(root+'contact/');
    await expect(page.locator('main img')).toHaveCount(0);
  });
  test(lang+' mock legal data cannot imply an inquiry was sent', async ({ page }) => {
    await page.goto(lang==='es'?'/contact/':'/en/contact/');
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
  await page.goto('/services/automation/');
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
