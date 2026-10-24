#!/usr/bin/env python3
"""
بسته‌بندی افزونهٔ وردپرس آهنگ‌بان برای بارگذاری در پیشخوان.

    python3 brand-kit/wordpress/build-plugin.py

خروجی: brand-kit/wordpress/ahangban-banner.zip
ساختار داخل زیپ: ahangban-banner/{ahangban-banner.php, readme.txt, assets/*}

تصاویر بنر از brand-kit/assets کپی می‌شوند تا فقط یک نسخهٔ مرجع در مخزن بماند.
"""

from __future__ import annotations

import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
KIT = HERE.parent
SRC = HERE / "ahangban-banner"
IMAGES = {
    "banner-saret-biad-640x360.png": KIT / "assets" / "banner-saret-biad-640x360.png",
    "banner-saret-biad-1280x720.png": KIT / "assets" / "banner-saret-biad-1280x720.png",
}
OUT = HERE / "ahangban-banner.zip"
SLUG = "ahangban-banner"


def main() -> None:
    missing = [str(p) for p in IMAGES.values() if not p.exists()]
    if missing:
        raise SystemExit("missing assets: " + ", ".join(missing))

    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(SRC.rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts:
                zf.write(path, f"{SLUG}/{path.relative_to(SRC).as_posix()}")
        for name, path in IMAGES.items():
            zf.write(path, f"{SLUG}/assets/{name}")

    size = OUT.stat().st_size
    with zipfile.ZipFile(OUT) as zf:
        listing = zf.namelist()
    print(f"{OUT.relative_to(KIT)} · {size} bytes · {len(listing)} files")
    for name in listing:
        print("  " + name)


if __name__ == "__main__":
    main()
