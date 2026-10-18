# راه‌اندازی سریع آهنگ‌بان

## دریافت بسته

`ahangban-brand-kit.zip` را دانلود و از حالت فشرده خارج کنید. پوشهٔ خروجی `ahangban-brand-kit/` شامل کل Brand Kit، داشبورد، سازندهٔ پرامپت، گزارش Excel، فونت‌ها، دارایی‌ها و فایل‌های راهنماست. هیچ backend، دیتابیس، API key یا وابستگی اینترنتی برای اجرای داشبورد لازم نیست.

## ویندوز

1. ZIP را Extract کنید.
2. وارد پوشهٔ `ahangban-brand-kit` شوید.
3. روی `start-localhost.bat` دوبار کلیک کنید.
4. در مرورگر `http://localhost:8000/hub.html` باز می‌شود. لینک `prompts.html` برای ساخت پرامپت‌ها و `reports/ahangban-brand-intelligence-hub.xlsx` برای گزارش اکسل است.
5. پنجرهٔ سرور را تا پایان کار باز نگه دارید؛ برای توقف `Ctrl+C` را بزنید.

برای اجرای BAT، Python 3 لازم است. بازکردن `index.html` بدون Python پیش‌نمایش ثابت را نشان می‌دهد، اما داشبورد و ابزار پرامپت که JSON می‌خوانند باید با HTTP باز شوند.

## Linux / macOS

در پوشهٔ استخراج‌شده اجرا کنید:

```sh
./start-localhost.sh
```

یا به‌صورت دستی:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

سپس `http://127.0.0.1:8000/hub.html` را باز کنید. سرور محلی روی loopback محدود است و به اینترنت عمومی گوش نمی‌دهد.

## استقرار روی وب‌سرور خودتان (Nginx)

این بسته یک سایت ایستای HTML/CSS/JS/JSON است؛ چیزی برای build یا اجرای backend ندارد.

1. ZIP را روی سرور در مسیر موقتی استخراج کنید.
2. محتوای پوشهٔ `ahangban-brand-kit/` را به مسیر ثابت و اختصاصی مثل `/var/www/ahangban-brand-kit/` کپی کنید؛ محتوای پوشه را در document root درست قرار دهید.
3. برای یک hostname که خودتان کنترل می‌کنید، نمونهٔ Nginx:

```nginx
server {
    listen 80;
    server_name brand.example.com;
    root /var/www/ahangban-brand-kit;
    index hub.html index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

4. پیکربندی را بررسی و Nginx را reload کنید؛ DNS و HTTPS/TLS باید جداگانه برای دامنهٔ خودتان تنظیم شوند.
5. مسیر `https://brand.example.com/hub.html` و `https://brand.example.com/prompts.html` را آزمایش کنید.

**امنیت و دامنهٔ کاربرد:** `python -m http.server` برای میزبانی عمومی یا production نیست. برای دسترسی اینترنتی از وب‌سرور واقعی، TLS، firewall و دامنهٔ خودتان استفاده کنید. این بسته داده‌ها را ذخیره یا ویرایش آنلاین نمی‌کند و احراز هویت ندارد. همهٔ JSONها و فایل‌های پوشه برای بازدیدکنندهٔ سایت قابل دریافت‌اند؛ هیچ دادهٔ محرمانه‌ای در آن قرار ندهید. محتوای قابل انتشار و مجوز تصاویر/موسیقی را پیش از میزبانی عمومی جداگانه بررسی کنید.

## بررسی صحت دانلود

فایل `ahangban-brand-kit.zip.sha256` کنار ZIP قرار دارد. در Linux/macOS، پس از دانلود هر دو فایل در یک پوشه:

```sh
sha256sum -c ahangban-brand-kit.zip.sha256
```

در PowerShell ویندوز:

```powershell
Get-FileHash .\ahangban-brand-kit.zip -Algorithm SHA256
```

مقدار چاپ‌شده را با خط داخل فایل `.sha256` مقایسه کنید.

## محتوای اصلی

- `hub.html` — داشبورد دادهٔ برند.
- `prompts.html` — پرامپت پرترهٔ ۵۰۰×۵۰۰ و اسلایدر ۶۴۰×۳۶۰.
- `reports/ahangban-brand-intelligence-hub.xlsx` — گزارش بصری قابل بازکردن در Excel/LibreOffice.
- `README.md` — نقشهٔ کامل منبع حقیقت و محدودیت‌های داده.
