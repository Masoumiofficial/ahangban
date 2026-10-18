#!/usr/bin/env python3
"""Create a portable, self-contained ZIP of the Brand Kit and a SHA-256 sidecar."""
from __future__ import annotations
import hashlib
import stat
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOWNLOADS = ROOT / "downloads"
ARCHIVE = DOWNLOADS / "ahangban-brand-kit.zip"
CHECKSUM = DOWNLOADS / "ahangban-brand-kit.zip.sha256"
ARCHIVE_ROOT = "ahangban-brand-kit"
FIXED_ZIP_TIME = (2026, 10, 18, 0, 0, 0)


def included_files():
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if any(part in {".git", "__pycache__", ".DS_Store"} for part in rel.parts):
            continue
        if path in {ARCHIVE, CHECKSUM} or path.suffix == ".pyc":
            continue
        yield path, rel.as_posix()


def main():
    DOWNLOADS.mkdir(parents=True, exist_ok=True)
    files = list(included_files())
    with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path, rel in files:
            info = zipfile.ZipInfo(f"{ARCHIVE_ROOT}/{rel}", FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            mode = stat.S_IMODE(path.stat().st_mode)
            info.external_attr = (stat.S_IFREG | mode) << 16
            info.flag_bits |= 0x800
            zf.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    digest = hashlib.sha256(ARCHIVE.read_bytes()).hexdigest()
    CHECKSUM.write_text(f"{digest}  {ARCHIVE.name}\n", encoding="ascii")
    print(f"Package: {ARCHIVE}")
    print(f"Files: {len(files)} | Size: {ARCHIVE.stat().st_size:,} bytes")
    print(f"SHA-256: {digest}")


if __name__ == "__main__":
    main()
