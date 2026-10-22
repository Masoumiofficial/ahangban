/*
 * Ahangban cover-watermark builder  →  brand-kit/assets/watermark-*
 *
 * Source geometry: the stacked logo content bbox inside its 360-unit viewBox is
 *   x 63.36  y 51.96  w 239.64  h 223.08   (measured from the rendered alpha channel)
 * Chip size, inner padding, corner radius and edge margin are derived from one
 * base unit, so changing SIZES keeps every proportion identical.
 *
 * Run: node tools/build-watermarks.js
 * Requires sharp — a build-time tool only, not a runtime dependency.
 */
const fs = require('fs');
const path = require('path');

let sharp;
try {
  sharp = require('sharp');
} catch {
  // local fallback for this workspace
  sharp = require('/home/user/.tools/node_modules/sharp');
}

const KIT = path.resolve(__dirname, '..');
const ASSETS = path.join(KIT, 'assets');

const CANVAS = 1000;
const CONTENT = { x: 63.36, y: 51.96, w: 239.64, h: 223.08 };
// Bars inside ahangban-mark*.svg (viewBox 120): x 14  y 20  w 100  h 78
const MARK_CONTENT = { x: 14, y: 20, w: 100, h: 78 };

/* ---- one shared proportion system ---- */
const CHIP_RATIO = { inset: 0.13, radius: 0.13, margin: 0.05 }; // margin = 5 % of the canvas
const SIZES = {
  cover: 200, // 20 % of a 1000 px canvas — holds a 148 px logo
  mark: 118, // 11.8 % — for renders where the wordmark would be unreadable
  cover2k: 400, // identical geometry on a 2000 px canvas
};

const VARIANTS = {
  dark: {
    plate: '#111111',
    plateOpacity: 0.82, // blends into dark art, still ≥ 11:1 for a white logo on any photo
    logo: 'ahangban-logo-stacked.svg',
    mark: 'ahangban-mark.svg',
    recolor: [['fill="#111111"', 'fill="#FFFFFF"']],
    fa: 'تیره',
  },
  light: {
    plate: '#FFFFFF',
    plateOpacity: 0.92,
    logo: 'ahangban-logo-stacked-color.svg',
    mark: 'ahangban-mark-color.svg',
    recolor: [],
    fa: 'روشن',
  },
};

const inner = (svg) =>
  svg.slice(svg.lastIndexOf('</desc>') + '</desc>'.length, svg.lastIndexOf('</svg>')).trim();
const recolor = (body, map) => map.reduce((acc, [a, b]) => acc.split(a).join(b), body);

function geometry(panel, canvas = CANVAS) {
  const m = canvas * CHIP_RATIO.margin;
  const logoW = panel * (1 - CHIP_RATIO.inset * 2);
  return {
    panel,
    radius: +(panel * CHIP_RATIO.radius).toFixed(1),
    inset: +(panel * CHIP_RATIO.inset).toFixed(1),
    margin: +m.toFixed(1),
    x: +(canvas - m - panel).toFixed(1),
    y: +(canvas - m - panel).toFixed(1),
    logoW: +logoW.toFixed(1),
    logoH: +((logoW * CONTENT.h) / CONTENT.w).toFixed(1),
  };
}

function stacked(variant, sizeKey, canvas = CANVAS) {
  const v = VARIANTS[variant];
  const g = geometry(SIZES[sizeKey], canvas);
  const scale = g.logoW / CONTENT.w;
  const lx = g.x + (g.panel - g.logoW) / 2;
  const ly = g.y + (g.panel - g.logoH) / 2;
  const body = recolor(inner(fs.readFileSync(path.join(ASSETS, v.logo), 'utf8')), v.recolor);
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${canvas} ${canvas}" role="img" aria-labelledby="t d">
  <title id="t">واترمارک کاور آهنگ‌بان — نسخهٔ ${v.fa}</title>
  <desc id="d">تراشهٔ ${g.panel} پیکسلی در گوشهٔ پایین‌راستِ بوم ${canvas}×${canvas}، با حاشیهٔ ${g.margin} پیکسل از لبه؛ عرض نشان ${g.logoW} پیکسل.</desc>
  <rect x="${g.x}" y="${g.y}" width="${g.panel}" height="${g.panel}" rx="${g.radius}" fill="${v.plate}" fill-opacity="${v.plateOpacity}"/>
  <g transform="translate(${lx.toFixed(2)} ${ly.toFixed(2)}) scale(${scale.toFixed(6)}) translate(${-CONTENT.x} ${-CONTENT.y})">${body}</g>
</svg>
`;
}

function markOnly(variant, sizeKey, canvas = CANVAS) {
  const v = VARIANTS[variant];
  const g = geometry(SIZES[sizeKey], canvas);
  const scale = g.logoW / MARK_CONTENT.w;
  const logoH = (g.logoW * MARK_CONTENT.h) / MARK_CONTENT.w;
  const lx = g.x + (g.panel - g.logoW) / 2;
  const ly = g.y + (g.panel - logoH) / 2;
  const body = recolor(inner(fs.readFileSync(path.join(ASSETS, v.mark), 'utf8')), v.recolor);
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${canvas} ${canvas}" role="img" aria-labelledby="t d">
  <title id="t">واترمارک فشردهٔ کاور آهنگ‌بان — نسخهٔ ${v.fa}</title>
  <desc id="d">فقط نشان میله‌ای، بدون نوشتار؛ ${g.panel} پیکسل روی بوم ${canvas}×${canvas}. برای رندرهای کوچک‌تر از ۸۰۰ پیکسل.</desc>
  <rect x="${g.x}" y="${g.y}" width="${g.panel}" height="${g.panel}" rx="${g.radius}" fill="${v.plate}" fill-opacity="${v.plateOpacity}"/>
  <g transform="translate(${lx.toFixed(2)} ${ly.toFixed(2)}) scale(${scale.toFixed(6)}) translate(${-MARK_CONTENT.x} ${-MARK_CONTENT.y})">${body}</g>
</svg>
`;
}

const FILES = {
  'watermark-cover-dark.svg': stacked('dark', 'cover'),
  'watermark-cover-light.svg': stacked('light', 'cover'),
  'watermark-mark-dark.svg': markOnly('dark', 'mark'),
  'watermark-mark-light.svg': markOnly('light', 'mark'),
};

async function writeSvgPng() {
  for (const [name, svg] of Object.entries(FILES)) {
    fs.writeFileSync(path.join(ASSETS, name), svg);
    const png = await sharp(Buffer.from(svg), { density: 96 }).resize(1000, 1000).png({ compressionLevel: 9 }).toBuffer();
    fs.writeFileSync(path.join(ASSETS, name.replace(/\.svg$/, '.png')), png);
  }
  for (const [variant, name] of [
    ['dark', 'watermark-cover-2000-dark.svg'],
    ['light', 'watermark-cover-2000-light.svg'],
  ]) {
    const svg = stacked(variant, 'cover2k', 2000);
    fs.writeFileSync(path.join(ASSETS, name), svg);
    const png = await sharp(Buffer.from(svg), { density: 96 }).resize(2000, 2000).png({ compressionLevel: 9 }).toBuffer();
    fs.writeFileSync(path.join(ASSETS, name.replace(/\.svg$/, '.png')), png);
  }
}

module.exports = { CANVAS, CONTENT, SIZES, VARIANTS, CHIP_RATIO, geometry, FILES, stacked, markOnly, writeSvgPng };

if (require.main === module) {
  writeSvgPng().then(() => console.log('watermark assets written'));
}
