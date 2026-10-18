import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const browser = await chromium.launch(); const page = await browser.newPage();
await page.goto('file://' + process.argv[2] + '/index.html', { waitUntil: 'load' }); await page.waitForTimeout(500);
await page.pdf({ path: process.argv[2] + '/Track_unit_assembly_in_detail.pdf', format: 'A4', printBackground: true, preferCSSPageSize: true });
await browser.close(); console.log('pdf written');
