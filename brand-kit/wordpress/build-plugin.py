#!/usr/bin/env python3
"""
ساخت خروجی‌های نصب وردپرس از یک منبع واحد.

    python3 brand-kit/wordpress/build-plugin.py

خروجی‌ها:
  brand-kit/wordpress/ahangban-banner.zip          افزونهٔ کامل (CSS و تصاویر جدا)
  brand-kit/wordpress/ahangban-banner-single.php   نسخهٔ تک‌فایل (CSS و تصاویر base64 داخل فایل)

تصاویر از brand-kit/assets کپی/خوانده می‌شوند تا فقط یک نسخهٔ مرجع در مخزن بماند.
"""

from __future__ import annotations

import base64
import re
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
KIT = HERE.parent
SRC = HERE / "ahangban-banner"
TMPL = HERE / "single" / "ahangban-banner-single.php.tmpl"
SINGLE_OUT = HERE / "ahangban-banner-single.php"
OUT = HERE / "ahangban-banner.zip"
SLUG = "ahangban-banner"
IMAGES = {
    "banner-saret-biad-640x360.png": KIT / "assets" / "banner-saret-biad-640x360.png",
    "banner-saret-biad-1280x720.png": KIT / "assets" / "banner-saret-biad-1280x720.png",
}


# زمان ثابت برای همهٔ مدخل‌ها تا خروجی ZIP بایت‌به‌بایت تکرارپذیر بماند.
FIXED_DATE = (2026, 10, 24, 0, 0, 0)


def _write(zf: zipfile.ZipFile, path: Path, arcname: str) -> None:
    info = zipfile.ZipInfo(arcname, date_time=FIXED_DATE)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    zf.writestr(info, path.read_bytes())


def b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


def build_zip() -> None:
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(SRC.rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts:
                _write(zf, path, f"{SLUG}/{path.relative_to(SRC).as_posix()}")
        for name, path in IMAGES.items():
            _write(zf, path, f"{SLUG}/assets/{name}")

    with zipfile.ZipFile(OUT) as zf:
        names = zf.namelist()
    print(f"{OUT.relative_to(KIT)} · {OUT.stat().st_size} bytes · {len(names)} files")
    for name in names:
        print("  " + name)


def build_single() -> None:
    css = (SRC / "assets" / "ahangban-banner.css").read_text(encoding="utf-8")
    php = TMPL.read_text(encoding="utf-8")
    php = php.replace("{{BANNER_CSS_B64}}", base64.b64encode(css.encode("utf-8")).decode("ascii"))
    php = php.replace("{{BANNER_PNG_1X_B64}}", b64(IMAGES["banner-saret-biad-640x360.png"]))
    php = php.replace("{{BANNER_PNG_2X_B64}}", b64(IMAGES["banner-saret-biad-1280x720.png"]))

    leftovers = re.findall(r"\{\{[A-Z0-9_]+\}\}", php)
    if leftovers:
        raise SystemExit(f"unresolved placeholders: {sorted(set(leftovers))}")

    SINGLE_OUT.write_text(php, encoding="utf-8")
    print(f"{SINGLE_OUT.relative_to(KIT)} · {SINGLE_OUT.stat().st_size} bytes")


def main() -> None:
    missing = [str(p) for p in IMAGES.values() if not p.exists()]
    if missing:
        raise SystemExit("missing assets: " + ", ".join(missing))

    build_zip()
    build_single()


if __name__ == "__main__":
    main()
