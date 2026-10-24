#!/usr/bin/env python3
"""
آهنگ‌بان — پس‌زمینهٔ بنر اسلایدر «سرت بیاد» · مهدی جهانی
Ahangban slider banner background · 640×360 (16:9) + 1280×720 (@2x)
هر خروجی مستقیماً در اندازهٔ خودش رندر می‌شود، نه با بزرگ‌نمایی از ۱x.

قواعد طراحی
-----------
- پالت: #111111، #222222، سفید کنترل‌شده و تنها یک تأکید آبی #185ADB — بدون گرادینت.
- بدون متن، حرف، عدد، لوگو، واترمارک، نماد کلیشه‌ای موسیقی یا چهرهٔ ساختگی.
- نسخهٔ WebP بی‌اتلاف (lossless) است تا خطوط مویی صفر و یک باقی بمانند.
- یک‌سوم چپ (۰ تا ۲۱۳px): فضای خالی و تمیز برای کاور اصلی ۱۶۰×۱۶۰.
- دو سوم راست: ستون تحریریه‌ای RTL با فضای منفی برای عنوان فارسی.

منطقهٔ امن (در مقیاس 640×360)
------------------------------
کاور        : x 27–187 ، y 100–260  (مربع ۱۶۰×۱۶۰، وسط‌چین عمودی)
عنوان/متن   : x 236–608 ، y 48–300
حاشیه‌ها    : ۳۲px راست · ۳۰px بالا · ۳۰px پایین
خط پایه     : y 330 (زیر آن چیزی نگذارید)

اجرا
----
    python3 generate-banner-saret-biad.py
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

INK = (17, 17, 17)        # #111111
CHARCOAL = (34, 34, 34)   # #222222
BLUE = (24, 90, 219)      # #185ADB
WHITE = (255, 255, 255)

W, H = 640, 360
HERE = Path(__file__).resolve().parent
ASSETS = HERE.parent / "assets"

SEAM_X = 213          # مرز یک‌سوم چپ
RULE_L = 236          # شروع خطوط (فضای تنفس بعد از مرز)
RULE_R = 608          # لبهٔ راست = تراز متن RTL (حاشیهٔ ۳۲px)
RULE_T = 30
RULE_B = 330
CORNER = 22           # اندازهٔ نشانهٔ آبی گوشهٔ بالا-راست


def render(scale: int = 1) -> Image.Image:
    s = scale
    size = (W * s, H * s)
    canvas = Image.new("RGB", size, INK)
    ImageDraw.Draw(canvas).rectangle([SEAM_X * s, 0, W * s, H * s], fill=CHARCOAL)

    overlay = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    def hline(x0, x1, y, alpha, color=WHITE):
        d.rectangle([x0 * s, y * s, x1 * s - 1, y * s + s - 1],
                    fill=color + (round(alpha * 255),))

    def vline(x, y0, y1, alpha, color=WHITE):
        d.rectangle([x * s, y0 * s, x * s + s - 1, y1 * s - 1],
                    fill=color + (round(alpha * 255),))

    # سرسطر: از شروع متن تا نشانهٔ آبی
    hline(RULE_L, RULE_R - CORNER, RULE_T, 0.15)
    # لبهٔ راست ستون متن، پایین‌تر از نشانهٔ آبی
    vline(RULE_R - 1, RULE_T + 18, RULE_B, 0.085)
    # خط پایه
    hline(RULE_L, RULE_R, RULE_B, 0.10)

    # تنها تأکید آبی: گوشهٔ شروع خواندن در چیدمان RTL
    hline(RULE_R - CORNER, RULE_R, RULE_T, 1.0, BLUE)
    vline(RULE_R - 1, RULE_T, RULE_T + 18, 1.0, BLUE)

    return Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    render(2).save(ASSETS / "banner-saret-biad-1280x720.png", optimize=True)
    render(1).save(ASSETS / "banner-saret-biad-640x360.png", optimize=True)
    render(1).save(ASSETS / "banner-saret-biad-640x360.webp", lossless=True, method=6)
    print("assets/banner-saret-biad-640x360.png")


if __name__ == "__main__":
    main()
