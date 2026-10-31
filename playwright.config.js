import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  use: { baseURL: 'http://127.0.0.1:3000', headless: true, launchOptions: process.env.CHROME_PATH ? { executablePath: process.env.CHROME_PATH, args: ['--no-sandbox'] } : {} },
  webServer: { command: 'python3 -m http.server 3000 --directory public --bind 127.0.0.1', port: 3000, reuseExistingServer: !process.env.CI },
  reporter: [['list'], ['html', { open: 'never' }]],
  outputDir: 'test-results'
});
