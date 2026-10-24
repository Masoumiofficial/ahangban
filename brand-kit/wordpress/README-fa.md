# پیاده‌سازی بنر «سرت بیاد» در وردپرس

راهنمای کامل از نصب تا نمایش، همراه با مسیرهای جایگزین برای المنتور، بلوک HTML و اسلایدرهای آمادهٔ قالب.

**فایل‌های این پوشه**

| فایل | کاربرد |
|---|---|
| `ahangban-banner.zip` | افزونهٔ آمادهٔ نصب؛ همین را در پیشخوان بارگذاری کنید |
| `ahangban-banner/` | سورس افزونه: `ahangban-banner.php`، `assets/ahangban-banner.css`، `readme.txt` |
| `demo-fa.html` | پیش‌نمایش همان خروجی در یک صفحهٔ RTL و نمای ۳۶۰ پیکسلی |
| `demo-cover.svg` | جای‌گیر کاور برای نمایش؛ در سایت واقعی استفاده نمی‌شود |
| `build-plugin.py` | ساخت دوبارهٔ ZIP از سورس + تصاویر |

**تصاویر بنر** از `../assets/` می‌آیند (یک نسخهٔ مرجع در مخزن):
`banner-saret-biad-640x360.png` · `banner-saret-biad-1280x720.png` · `banner-saret-biad-640x360.webp`

---

## دانلود افزونه (به‌ازای شبکه)

نشانی `raw.githubusercontent.com` در بعضی شبکه‌ها (از جمله ایران) فیلتر است و خطای ۴۰۴ یا «صفحه باز نمی‌شود» می‌دهد؛ فایل سالم است و مشکل از مسیر دانلود است. هر یک از این چهار راه را امتحان کنید:

| راه | نشانی |
|---|---|
| jsDelivr (معمولاً بدون فیلتر) | `https://cdn.jsdelivr.net/gh/Masoumiofficial/ahangban@main/brand-kit/wordpress/ahangban-banner.zip` |
| Statically (آینهٔ دوم) | `https://cdn.statically.io/gh/Masoumiofficial/ahangban/main/brand-kit/wordpress/ahangban-banner.zip` |
| صفحهٔ فایل در گیت‌هاب | `https://github.com/Masoumiofficial/ahangban/blob/main/brand-kit/wordpress/ahangban-banner.zip?raw=true` |
| raw گیت‌هاب | `https://github.com/Masoumiofficial/ahangban/raw/main/brand-kit/wordpress/ahangban-banner.zip` |

اگر هیچ‌کدام باز نشد، با روشن‌بودن VPN یا از «دانلود کل مخزن» استفاده کنید:

```
https://codeload.github.com/Masoumiofficial/ahangban/zip/refs/heads/main
```

سپس از پوشهٔ استخراج‌شده، `brand-kit/wordpress/ahangban-banner.zip` را بردارید.

### بدون ZIP: نصب با FTP

اگر هاست آپلود ZIP را می‌بندد، پوشهٔ `ahangban-banner/` را از همین مخزن در مسیر `wp-content/plugins/` بگذارید و در پیشخوان فعالش کنید. لازم نیست ZIP بسازید.

---

## ۱. نصب افزونه (پیشنهادی)

1. در پیشخوان: **افزونه‌ها ← افزودن ← بارگذاری افزونه** → فایل `ahangban-banner.zip` را انتخاب کنید → **نصب** → **فعال‌سازی**.
   - اگر آپلود زیپ در هاست بسته است: پوشهٔ `ahangban-banner/` را با FTP در `wp-content/plugins/` بگذارید و سپس فعال کنید.
2. تصویر پس‌زمینه همراه افزونه می‌آید؛ نیازی به آپلود ندارد.

### درج در برگه یا نوشته

**راه سریع:** در ویرایشگر بلوک روی **＋** بزنید → دستهٔ **آهنگ‌بان** → الگوی **«بنر ویژهٔ آهنگ — سرت بیاد»**.

**راه دستی:** بلوک **Shortcode** بسازید و این خط را بگذارید:

```
[ahangban_banner href="/saret-biad" cover="/wp-content/uploads/2026/10/cover.webp"]
```

### پارامترهای شورت‌کد

| پارامتر | پیش‌فرض | توضیح |
|---|---|---|
| `title` | سرت بیاد | عنوان اثر؛ متن واقعی HTML |
| `artist` | مهدی جهانی | نام هنرمند |
| `meta` | تک‌آهنگ | نوع اثر / توضیح کوتاه |
| `cta` | گوش بده | برچسب دکمه |
| `href` | خالی | **اگر خالی باشد دکمه رندر نمی‌شود**؛ پیوند صفحهٔ اثر |
| `cover` | خالی | نشانی کاور ۱:۱ از کتابخانهٔ رسانه؛ خالی = جای‌گیر خط‌مویی |
| `cover_alt` | کاور «سرت بیاد» از مهدی جهانی | متن جانشین کاور (تصویر محتوایی است) |
| `bg` / `bg2x` | تصاویر افزونه | اگر خواستید پس‌زمینه را از کتابخانهٔ رسانه بدهید |
| `tag` | `h2` | سطح عنوان: `h1`، `h2`، `h3`، `p` |
| `loading` | `eager` | برای بنر بالای صفحه `eager`؛ برای پایین صفحه `lazy` |
| `class` | خالی | کلاس اضافه؛ برای سایت LTR: `hb-banner--ltr` |

نمونهٔ کامل:

```
[ahangban_banner
  title="سرت بیاد"
  artist="مهدی جهانی"
  meta="تک‌آهنگ · ۱۴۰۴"
  cta="گوش بده"
  href="/music/mehdi-jahani/saret-biad"
  cover="/wp-content/uploads/2026/10/saret-biad-cover.webp"
  loading="eager"]
```

---

## ۲. بدون افزونه: بلوک HTML سفارشی

اگر نمی‌خواهید افزونه نصب کنید:

1. تصویر بنر را در کتابخانهٔ رسانه آپلود کنید و نشانی آن را بردارید.
2. در برگه، بلوک **HTML سفارشی** بسازید و این مارک‌آپ را بگذارید:

```html
<div class="hb-banner" dir="rtl">
  <img class="hb-banner__media"
       src="/wp-content/uploads/2026/10/banner-saret-biad-1280x720.png"
       width="640" height="360" alt="" aria-hidden="true"
       fetchpriority="high" decoding="async">
  <div class="hb-banner__cover">
    <img src="/wp-content/uploads/2026/10/saret-biad-cover.webp"
         width="160" height="160"
         alt="کاور «سرت بیاد» از مهدی جهانی" loading="lazy" decoding="async">
  </div>
  <div class="hb-banner__body">
    <p class="hb-banner__artist">مهدی جهانی</p>
    <h2 class="hb-banner__title">سرت بیاد</h2>
    <p class="hb-banner__meta">تک‌آهنگ</p>
    <a class="hb-banner__cta" href="/music/mehdi-jahani/saret-biad">گوش بده</a>
  </div>
</div>
```

3. محتوای `ahangban-banner/assets/ahangban-banner.css` را در **نمایش ← سفارشی‌سازی ← CSS اضافه** (یا فایل `style.css` قالب فرزند) بگذارید.

> اگر چند برگه بنر دارند، بارگذاری CSS در همهٔ صفحات کمی اضافه‌بار است؛ افزونه این کار را فقط در صفحهٔ دارای شورت‌کد انجام می‌دهد.

---

## ۳. قالب فرزند (برای توسعه‌دهنده)

فایل `template-parts/ahangban-banner.php` در قالب فرزند بسازید و همان مارک‌آپ بخش ۲ را با `esc_url()` / `esc_html()` پر کنید، سپس در قالب صفحه:

```php
<?php get_template_part( 'template-parts/ahangban-banner' ); ?>
```

استایل را در `functions.php` قالب فرزند ثبت کنید:

```php
add_action( 'wp_enqueue_scripts', function () {
    wp_enqueue_style(
        'ahangban-banner',
        get_stylesheet_directory_uri() . '/assets/ahangban-banner.css',
        array(),
        '1.0.0'
    );
} );
```

فونت سازمانی: پوشهٔ `assets/fonts/` را در قالب فرزند کپی کنید و `brand-fonts.css` را با مسیر درست صدا بزنید (یا همان فونت قالب را نگه دارید و فقط `--hb-banner-font` را عوض کنید):

```css
.hb-banner { --hb-banner-font: "Vazirmatn", Tahoma, sans-serif; }
```

---

## ۴. المنتور

- **راه اول:** ویجت **Shortcode** را بکشید و `[ahangban_banner href="…" cover="…"]` را در آن بگذارید.
- **راه دوم:** ویجت **HTML** را بکشید و مارک‌آپ بخش ۲ را در آن بگذارید؛ CSS را در **Site Settings ← Custom CSS** اضافه کنید.
- برای بنر تک‌تصویری (بدون متن HTML) می‌توانید از ویجت Image استفاده کنید، اما عنوان دیگر متن واقعی نیست و در موبایل کوچک می‌شود؛ روش HTML/شورت‌کد خوانایی و سئوی بهتری دارد.

---

## ۵. اسلایدرهای آمادهٔ قالب

اگر اسلایدر صفحهٔ اصلی از قبل وجود دارد، دو انتخاب دارید:

**الف) کل اسلاید = بنر آماده، متن‌ها HTML خودتان (توصیه‌شده)**
اسلاید را ۱۶:۹ کنید و مارک‌آپ `.hb-banner` را داخل اسلاید بگذارید؛ پس‌زمینه و چیدمان همان است که در دمو می‌بینید.

**ب) لایه‌های جدا روی تصویر پس‌زمینه**
تصویر بنر را پس‌زمینهٔ اسلاید کنید (بدون برش، `cover` و `center`) و لایه‌ها را با این درصدها بچینید:

| لایه | افقی | عمودی | اندازه |
|---|---|---|---|
| کاور اثر | `left: 4.22%` | `top: 27.78%` | عرض `25%`، مربع |
| نام هنرمند | `right: 5%` | `top: 13.3%` | ~`2.03cqw` (۱۳px در ۶۴۰) |
| عنوان | `right: 5%` | وسط باند متن | ~`6.25cqw` (۴۰px در ۶۴۰) |
| نوع اثر | `right: 5%` | زیر عنوان | ~`1.88cqw` |
| دکمه | `right: 5%` | پایین متن | ارتفاع ≥ ۴۴px، آبی `#185ADB` |

**Smart Slider 3:** اسلاید را با نسبت ۱۶:۹ بسازید، تصویر بنر را در لایهٔ Background بگذارید، لایه‌های Heading/Text/Button را راست‌چین کنید و فاصلهٔ راست را ۵٪ بگذارید. در تنظیمات اسلایدر، «Fill» را روی `cover` و شیوهٔ نمایش موبایل را «حفظ نسبت» بگذارید.

**Slider Revolution:** Grid را ۱۶:۹ انتخاب کنید (یا لایه‌ها را با درصد بچینید)، `Right` را `5%` و اندازهٔ عنوان را نسبت به پهنای اسلاید تنظیم کنید. گزینهٔ «Layers aligned to Grid» را روشن بگذارید تا در موبایل متن کوچک شود نه اینکه برش بخورد.

> ⚠️ اگر قالب اسلایدر را در موبایل به ۴:۳ یا ارتفاع ثابت تغییر می‌دهد، بنر برش می‌خورد و جای کاور/متن جابه‌جا می‌شود. در این حالت یا نسبت ۱۶:۹ را نگه دارید، یا در موبایل از یک کارت سادهٔ «کاور + عنوان» استفاده کنید.

---

## ۶. فونت و راست‌به‌چپ

- بنر `dir="rtl"` و `text-align: start` دارد و از ویژگی‌های منطقی (`inset-inline-start/end`) استفاده می‌کند؛ روی قالب RTL خودکار درست می‌نشیند.
- **سایت LTR:** کلاس `hb-banner--ltr` را بدهید تا تصویر آینه شود و متن از چپ شروع شود:
  `[ahangban_banner class="hb-banner--ltr"]`
- برای فونت یکدست با برند، وزن‌های `400/500/700/800` از `assets/fonts/vazirmatn-arabic-*.woff2` را در رسانهٔ سایت آپلود کنید و با `@font-face` معرفی کنید. اگر نمی‌خواهید، بنر به Tahoma برمی‌گردد و چیدمان نمی‌شکند.

---

## ۷. کارایی

- تصویر ۲x فقط برای نمایشگرهای Retina بارگذاری می‌شود (`srcset` با توصیفگر `2x`).
- بنر بالای صفحه: `loading="eager"` و `fetchpriority="high"` (افزونه پیش‌فرض همین است). بنر پایین صفحه: `loading="lazy"`.
- نسخهٔ WebP بی‌اتلاف (۱۶۰ بایت) اگر خواستید سبک‌تر باشد در `assets/` موجود است.
- `width`/`height` تعیین شده‌اند؛ بنابراین CLS صفر است.
- بعد از تغییرات، کش صفحات (WP Rocket / LiteSpeed / Cloudflare) را پاک کنید.

**Preload اختیاری** در `functions.php` برای صفحهٔ اصلی:

```php
add_action( 'wp_head', function () {
    if ( is_front_page() ) {
        echo '<link rel="preload" as="image" href="' .
            esc_url( get_site_url() . '/wp-content/plugins/ahangban-banner/assets/banner-saret-biad-1280x720.png' ) .
            '" imagesrcset="' . esc_url( get_site_url() . '/wp-content/plugins/ahangban-banner/assets/banner-saret-biad-640x360.png' ) . ' 1x, ' .
            esc_url( get_site_url() . '/wp-content/plugins/ahangban-banner/assets/banner-saret-biad-1280x720.png' ) . ' 2x" imagesizes="100vw">' . "\n";
    }
} );
```

---

## ۸. چک‌لیست پیش از انتشار

- [ ] `href` دکمه به صفحهٔ واقعی همان اثر می‌رود (نه `#`).
- [ ] کاور واقعی از رسانهٔ مجاز بارگذاری شده و `cover_alt` درست است.
- [ ] بنر در ۳۲۰، ۷۶۸، ۱۰۲۴ و ۱۴۴۰ پیکسل بررسی شده؛ اسکرول افقی ندارد.
- [ ] در بزرگ‌نمایی ۲۰۰٪ عنوان بریده نمی‌شود.
- [ ] در موبایل دکمه ≥ ۴۴px است و با کیبورد focus می‌گیرد.
- [ ] در برگه‌های بدون بنر، استایل اضافه بارگذاری نمی‌شود (فقط حالت افزونه).
- [ ] متن جایگزین تصویر پس‌زمینه خالی و `aria-hidden` است؛ عنوان و هنرمند متن واقعی‌اند.
- [ ] کش و CDN پس از انتشار پاک شده‌اند.
- [ ] حقوق کاور و نام هنرمند برای همین استفاده بررسی شده است.

---

## ۹. عیب‌یابی

| نشانه | علت احتمالی | راه‌حل |
|---|---|---|
| بنر بدون استایل (متن روی تصویر بدون چیدمان) | CSS بارگذاری نشده | افزونه فعال است؟ کش را پاک کنید؛ در حالت دستی، CSS در «CSS اضافه» باشد |
| دکمه دیده نمی‌شود | `href` خالی است | پیوند صفحهٔ اثر را بدهید |
| جای کاور خالی و خط‌مویی است | `cover` تنظیم نشده | نشانی کاور ۱:۱ را بدهید |
| متن در موبایل بیرون می‌زند | قالب ارتفاع ثابت به اسلاید داده | نسبت را ۱۶:۹ کنید یا بنر را داخل `.hb-banner` بدون container با overflow بگذارید |
| فونت برند اعمال نمی‌شود | `@font-face` بارگذاری نشده | `--hb-banner-font` را بررسی کنید یا فونت را در رسانه آپلود کنید |
| بنر در سایت انگلیسی آینه نشده | کلاس LTR داده نشده | `class="hb-banner--ltr"` |

---

## ۱۰. ساخت دوبارهٔ ZIP

پس از هر ویرایش در سورس افزونه:

```bash
python3 brand-kit/wordpress/build-plugin.py
```

خروجی: `brand-kit/wordpress/ahangban-banner.zip` — شامل پوشهٔ `ahangban-banner/` و تصاویر بنر.
