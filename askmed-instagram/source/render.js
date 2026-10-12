// usage: node render.js <html> <selector> <outPrefix>
// screenshots every element matching selector to <outPrefix>-<i>.png
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const [html, selector, outPrefix] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 3400, height: 2000 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.resolve(html));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(500);
  const els = await page.$$(selector);
  for (let i = 0; i < els.length; i++) {
    // show one element at a time so each screenshot starts at the page origin
    await page.evaluate(([sel, keep]) => {
      document.querySelectorAll(sel).forEach((el, j) => { el.style.display = j === keep ? '' : 'none'; });
      window.scrollTo(0, 0);
    }, [selector, i]);
    const file = `${outPrefix}-${i + 1}.png`;
    await els[i].screenshot({ path: file });
    console.log(file);
  }
  const report = await page.evaluate(() => {
    const out = {};
    document.querySelectorAll('[data-measure]').forEach(el => {
      const r = el.getBoundingClientRect();
      out[el.dataset.measure] = [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)];
    });
    return out;
  });
  if (Object.keys(report).length) console.log(JSON.stringify(report));
  await browser.close();
})();
