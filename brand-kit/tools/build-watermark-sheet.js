/*
 * Builds brand-kit/assets/watermark-comparison-fa.png — the Persian decision sheet
 * comparing the dark and light watermark variants on three covers.
 * Build-time helper only; requires sharp.  Run: node tools/build-watermark-sheet.js
 */
const fs = require('fs');
const path = require('path');
let sharp;
try { sharp = require('sharp'); } catch { sharp = require('/home/user/.tools/node_modules/sharp'); }

const K = path.resolve(__dirname, '..');
const A = path.join(K, 'assets');

// Optional: a real cover to test against. Without it the brand mood images are used.
//   COVER=/path/to/cover.png node tools/build-watermark-sheet.js
const COVER = process.env.COVER || '';

const lin = (c) => { c /= 255; return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
const L = ([r, g, b]) => 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);
const CR = (a, b) => { const x = Math.max(a, b), y = Math.min(a, b); return (x + 0.05) / (y + 0.05); };
const blend = (bg, plate, a) => bg.map((c, i) => plate[i] * a + c * (1 - a));
const faN = (n) => String(n).replace(/\d/g, (d) => '۰۱۲۳۴۵۶۷۸۹'[d]).replace('.', '٫');
const uri = (buf, mime = 'image/png') => `data:${mime};base64,${buf.toString('base64')}`;

async function composite(art, wm) {
  const ov = await sharp(`${A}/${wm}`, { density: 96 }).resize(1000, 1000).png().toBuffer();
  return sharp(art).composite([{ input: ov }]).png().toBuffer();
}
async function meanRGB(buf, rect) {
  const { data, info } = await sharp(buf).extract(rect).raw().toBuffer({ resolveWithObject: true });
  const n = info.width * info.height, ch = info.channels, s = [0, 0, 0];
  for (let i = 0; i < n; i++) { const o = i * ch; s[0] += data[o]; s[1] += data[o + 1]; s[2] += data[o + 2]; }
  return s.map((v) => Math.round(v / n));
}

(async () => {
  const C = {
    release: await sharp(COVER || `${K}/mood/hero.jpg`).resize(1000, 1000, { fit: 'cover' }).png().toBuffer(),
    dark: await sharp(`${K}/mood/hero.jpg`).resize(1000, 1000, { fit: 'cover' }).jpeg({ quality: 88 }).toBuffer(),
    light: await sharp(`${K}/mood/flatlay.jpg`).resize(1000, 1000, { fit: 'cover' }).jpeg({ quality: 88 }).toBuffer(),
    mid: await sharp(`${K}/mood/listening-room.jpg`).resize(1000, 1000, { fit: 'cover' }).jpeg({ quality: 88 }).toBuffer(),
  };

  const cases = [
    { key: 'a', art: C.release, wm: 'watermark-cover-dark.svg', pick: true, title: 'تیره روی همین کاور', note: 'تراشه با عکس یکی می‌شود؛ فقط نشان خوانده می‌شود' },
    { key: 'b', art: C.release, wm: 'watermark-cover-light.svg', title: 'روشن روی همین کاور', note: 'کارت سفید از عکس جدا می‌افتد و چشم را می‌دزدد' },
    { key: 'c', art: C.dark, wm: 'watermark-cover-light.svg', title: 'روشن روی کاور تیره', note: 'خوانا، اما شبیه کارت رابط می‌شود، نه مهر برند' },
    { key: 'd', art: C.light, wm: 'watermark-cover-dark.svg', pick: true, title: 'تیره روی کاور روشن', note: 'مهر تمیز روی هر پس‌زمینه‌ای' },
    { key: 'e', art: C.mid, wm: 'watermark-cover-dark.svg', pick: true, title: 'تیره روی کاور متوسط', note: 'حالت پیش‌فرضِ امن' },
    { key: 'f', art: C.light, wm: 'watermark-cover-light.svg', title: 'روشن روی کاور روشن', note: 'تراشه در پس‌زمینه حل می‌شود؛ استفاده نکنید' },
  ];

  for (const c of cases) {
    c.buf = await composite(c.art, c.wm);
    const dark = c.wm.includes('dark');
    c.bg = await meanRGB(c.buf, { left: 770, top: 706, width: 180, height: 30 });
    c.plate = blend(c.bg, dark ? [17, 17, 17] : [255, 255, 255], dark ? 0.82 : 0.92).map(Math.round);
    c.ratio = CR(L(c.plate), L(dark ? [255, 255, 255] : [17, 17, 17]));
    const t = await sharp(c.buf).resize(300, 300).png().toBuffer();
    c.thumb = await sharp(t).resize(190, 190, { kernel: 'nearest' }).png().toBuffer();
  }

  const mk = await composite(C.release, 'watermark-mark-dark.svg');
  const mkT = await sharp(await sharp(mk).resize(300, 300).png().toBuffer()).resize(190, 190, { kernel: 'nearest' }).png().toBuffer();

  const f600 = fs.readFileSync(`${A}/fonts/vazirmatn-arabic-600.woff2`).toString('base64');
  const f400 = fs.readFileSync(`${A}/fonts/vazirmatn-arabic-400.woff2`).toString('base64');
  const l400 = fs.readFileSync(`${A}/fonts/vazirmatn-latin-400.woff2`).toString('base64');
  const CSS = `<defs><style>
    @font-face{font-family:V;font-weight:600;src:url(data:font/woff2;base64,${f600}) format('woff2')}
    @font-face{font-family:V;font-weight:400;src:url(data:font/woff2;base64,${f400}) format('woff2')}
    @font-face{font-family:VL;font-weight:400;src:url(data:font/woff2;base64,${l400}) format('woff2')}
    .h1{font:600 44px V;fill:#111}
    .sub{font:400 20px V;fill:#666}
    .cap{font:600 24px V;fill:#111}
    .note{font:400 17px V;fill:#666}
    .small{font:400 16px V;fill:#8a8a8a}
    .mono{font:400 15px VL;fill:#a8a8a8}
    .pill{font:600 17px V;fill:#fff}
    .ruleN{font:600 16px V;fill:#fff}
    .rule{font:400 18px V;fill:#222}
    .ruleT{font:600 20px V;fill:#111}
  </style></defs>`;

  const W = 1560;
  const CELL = 430, GAP = 34, LEFT = 70;
  const xs = [LEFT, LEFT + CELL + GAP, LEFT + (CELL + GAP) * 2];
  const R1 = 320, R1H = 96, R2 = R1 + CELL + R1H, R2H = 96;
  const TH = 250; // thumbnail band
  const TY = R2 + CELL + R2H;
  const RULES_Y = TY + TH;
  const H = RULES_Y + 400;

  const cell = (c, x, y) => `<g transform="translate(${x} ${y})">
      <rect x="-1" y="-1" width="${CELL + 2}" height="${CELL + 2}" fill="none" stroke="#E5E5E5"/>
      <image x="0" y="0" width="${CELL}" height="${CELL}" href="${uri(c.buf)}"/>
      ${c.pick ? `<g transform="translate(14 14)"><rect width="100" height="31" rx="15.5" fill="#185ADB"/><text x="50" y="21.5" class="pill" text-anchor="middle">پیشنهاد</text></g>` : ''}
      <text x="${CELL}" y="-46" class="cap" text-anchor="end">${c.title}</text>
      <text x="${CELL}" y="-18" class="note" text-anchor="end">${c.note}</text>
      <text x="${CELL}" y="${CELL + 26}" class="small" text-anchor="end">نشان روی تراشه: ${faN(c.ratio.toFixed(1))} به ۱</text>
    </g>`;

  const STEP = 198;
  const thumbs = cases.map((c, i) => `<g transform="translate(${LEFT + i * STEP} ${TY})">
      <image x="0" y="0" width="190" height="190" href="${uri(c.thumb)}"/>
    </g>`).join('');

  const rules = [
    'پیش‌فرض کاورهای آهنگ‌بان نسخهٔ تیره است؛ میله‌های سفیدش روی هر عکسی خوانده می‌شوند.',
    'نسخهٔ روشن فقط برای گوشهٔ تیره و خلوت. روی عکس تیره، کارت سفید چشم را از چهره می‌دزدد.',
    'تراشه روی چهره، عنوان اثر یا لوگوی ناشر ننشیند؛ اگر جا اشغال است جای تراشه را عوض کنید، نه اندازه‌اش را.',
    'زیر ۸۰۰ پیکسل نوشتار خوانده نمی‌شود؛ نسخهٔ فشرده (فقط نشان) بگذارید یا واترمارک را بردارید.',
    'تراشه را نکشید، نچرخانید، رنگ عوض نکنید و روی‌اش سایه نگذارید.',
  ];

  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
  ${CSS}
  <rect width="${W}" height="${H}" fill="#fff"/>
  <rect x="0" y="0" width="7" height="${H}" fill="#185ADB"/>
  <text x="${W - LEFT}" y="84" class="h1" text-anchor="end">واترمارک کاور آهنگ‌بان — کدام نسخه؟</text>
  <text x="${W - LEFT}" y="124" class="sub" text-anchor="end">تراشهٔ ۲۰۰ پیکسلی، حاشیهٔ ۵۰ پیکسل از لبه، نشان ۱۴۸ پیکسل عرض، گوشهٔ گرد ۲۶ پیکسل — بوم ۱۰۰۰ در ۱۰۰۰</text>
  <text x="${W - LEFT}" y="158" class="sub" text-anchor="end">تیره: تراشهٔ ۱۱۱۱۱۱ با شفافیت ۸۲٪ · روشن: تراشهٔ FFFFFF با شفافیت ۹۲٪ · بدون گرادینت، سایه و چرخش</text>
  <line x1="${LEFT}" y1="196" x2="${W - LEFT}" y2="196" stroke="#E5E5E5" stroke-width="2"/>

  ${cases.slice(0, 3).map((c, i) => cell(c, xs[i], R1)).join('')}
  ${cases.slice(3, 6).map((c, i) => cell(c, xs[i], R2)).join('')}

  <text x="${W - LEFT}" y="${TY - 26}" class="cap" text-anchor="end">همان شش حالت در اندازهٔ واقعی ۳۰۰ پیکسل</text>
  ${thumbs}
  <g transform="translate(${LEFT + 6 * STEP} ${TY})">
    <image x="0" y="0" width="190" height="190" href="${uri(mkT)}"/>
    <rect x="0" y="190" width="190" height="3" fill="#185ADB"/>
  </g>
  <text x="${LEFT + 6 * STEP}" y="${TY + 214}" class="small" text-anchor="start">نسخهٔ فشرده · فقط نشان</text>

  <rect x="${LEFT}" y="${RULES_Y + 18}" width="${W - LEFT * 2}" height="${H - RULES_Y - 92}" rx="22" fill="#F4F4F4"/>
  <text x="${W - LEFT - 40}" y="${RULES_Y + 72}" class="ruleT" text-anchor="end">قاعدهٔ انتخاب</text>
  ${rules.map((r, i) => `<g transform="translate(${W - LEFT - 40} ${RULES_Y + 122 + i * 44})">
      <rect x="-30" y="-19" width="26" height="26" rx="13" fill="#185ADB"/>
      <text x="-17" y="0" class="ruleN" text-anchor="middle">${faN(i + 1)}</text>
      <text x="-46" y="0" class="rule" text-anchor="end">${r}</text>
    </g>`).join('')}
  <text x="${LEFT}" y="${H - 28}" class="mono">Ahangban brand kit · assets/watermark-cover-*.svg · assets/watermark-mark-*.svg</text>
</svg>`;

  if (process.env.SHEET_SVG) fs.writeFileSync(process.env.SHEET_SVG, svg);
  const rendered = await sharp(Buffer.from(svg), { density: 96 })
    .resize({ width: W, kernel: 'lanczos3' })
    // palette PNG keeps the sheet under ~0.5 MB without visible banding
    .png({ compressionLevel: 9, palette: true, quality: 92, effort: 10, colours: 255 })
    .toBuffer();
  fs.writeFileSync(path.join(A, 'watermark-comparison-fa.png'), rendered);
  console.log('sheet ok', cases.map((c) => `${c.key}:${c.ratio.toFixed(1)}`).join(' '));
})();
