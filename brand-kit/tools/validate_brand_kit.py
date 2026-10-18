#!/usr/bin/env python3
"""Dependency-free structural and local-reference checks for the brand-kit."""
from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
ERRORS: list[str] = []
WARNINGS: list[str] = []
STATUSES = {"COMPLETE", "INCOMPLETE", "NEEDS_REVIEW", "VERIFIED", "UNKNOWN"}
COMPLETION_FIELDS = {
    "name", "slug", "biography", "featured_image", "reliable_sources",
    "official_links", "track_album_relationships", "artist_page",
    "seo_title_description", "broken_links_and_duplicates", "final_quality_control",
}


def load(rel: str):
    p = ROOT / rel
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        ERRORS.append(f"JSON خوانده نشد {rel}: {exc}")
        return {}


def check_local_path(raw: str, base: Path, label: str):
    raw = unquote(raw.strip())
    if not raw or raw.startswith(("#", "mailto:", "tel:", "data:", "javascript:")):
        return
    parsed = urlparse(raw)
    if parsed.scheme or parsed.netloc:
        return
    path_part = parsed.path
    if not path_part:
        return
    target = (base / path_part).resolve()
    try:
        target.relative_to(REPO.resolve())
    except ValueError:
        ERRORS.append(f"لینک از ریشهٔ repo بیرون می‌رود: {label}: {raw}")
        return
    if not target.exists():
        ERRORS.append(f"مسیر داخلی پیدا نشد: {label}: {raw}")


class LocalHTMLRefs(HTMLParser):
    def __init__(self, file: Path):
        super().__init__()
        self.file = file

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key in ("href", "src", "poster"):
            val = attrs.get(key)
            if val:
                check_local_path(val, self.file.parent, str(self.file.relative_to(REPO)))


def main() -> int:
    for json_file in ROOT.rglob("*.json"):
        try:
            json.loads(json_file.read_text(encoding="utf-8"))
        except Exception as exc:
            ERRORS.append(f"JSON نامعتبر {json_file.relative_to(REPO)}: {exc}")

    artists = load("artists/artists.json")
    music = load("music-catalog/catalog.json")
    assets = load("visual-identity/assets.json")
    social = load("social-media/accounts.json")
    identity = load("brand/identity.json")
    tokens = load("assets/brand-tokens.json")
    prompt_templates = load("prompts/image-prompt-templates.fa.json")

    for key, placeholder in (("artist_portrait", "{{artist_name}}"), ("featured_slider", "{{artist_name}}")):
        template = prompt_templates.get(key, {}).get("template", "")
        if placeholder not in template:
            ERRORS.append(f"placeholder هنرمند در پرامپت وجود ندارد: {key}")
    if "{{track_title}}" not in prompt_templates.get("featured_slider", {}).get("template", ""):
        ERRORS.append("placeholder عنوان آهنگ در پرامپت اسلایدر وجود ندارد")

    if artists.get("registry_id") != "ahangban-artist-registry":
        ERRORS.append("شناسهٔ رجیستری هنرمند نادرست است")
    artist_rows = artists.get("records", [])
    ids = [r.get("artist_id") for r in artist_rows]
    if len(ids) != len(set(ids)):
        ERRORS.append("artist_id تکراری است")
    for row in artist_rows:
        aid = row.get("artist_id", "<بدون ID>")
        if not row.get("display_name_fa"):
            ERRORS.append(f"نام فارسی خالی است: {aid}")
        if set(row.get("completion", {})) != COMPLETION_FIELDS:
            ERRORS.append(f"فیلدهای completion ناقص/اضافی‌اند: {aid}")
        for field, status in row.get("completion", {}).items():
            if status not in STATUSES:
                ERRORS.append(f"وضعیت نامعتبر {aid}.{field}: {status}")
        if row.get("identity_status") not in STATUSES:
            ERRORS.append(f"identity_status نامعتبر است: {aid}")

    if music.get("registry_id") != "ahangban-music-catalog":
        ERRORS.append("شناسهٔ رجیستری موسیقی نادرست است")
    track_rows = music.get("records", [])
    track_ids = [r.get("record_id") for r in track_rows]
    if len(track_ids) != len(set(track_ids)):
        ERRORS.append("record_id تکراری در کاتالوگ موسیقی است")
    known_artist_ids = set(ids)
    for row in track_rows:
        for aid in row.get("artist_ids", []):
            if aid not in known_artist_ids:
                ERRORS.append(f"ارجاع هنرمند ناموجود در {row.get('record_id')}: {aid}")

    asset_rows = assets.get("records", [])
    asset_paths = [r.get("path") for r in asset_rows]
    if len(asset_paths) != len(set(asset_paths)):
        ERRORS.append("مسیر تکراری در assets.json است")
    for rel in asset_paths:
        target = ROOT / str(rel)
        if not target.is_file():
            ERRORS.append(f"فایل فهرست‌شده در manifest پیدا نشد: {rel}")
        else:
            row = next((item for item in asset_rows if item.get("path") == rel), {})
            if row.get("bytes") != target.stat().st_size:
                ERRORS.append(f"اندازهٔ فایل در manifest منسوخ است: {rel}")

    # Keep the documented JSON token source aligned with its CSS delivery layer.
    token_css = (ROOT / "assets/brand-tokens.css").read_text(encoding="utf-8", errors="replace")
    color_tokens = {
        "--hb-blue": tokens.get("corporateColor", {}).get("hex"),
        "--hb-blue-dark": tokens.get("corporateColor", {}).get("dark"),
        "--hb-blue-pale": tokens.get("corporateColor", {}).get("pale"),
        "--hb-ink": tokens.get("colors", {}).get("ink"),
        "--hb-white": tokens.get("colors", {}).get("white"),
        "--hb-dark": tokens.get("colors", {}).get("dark"),
        "--hb-text-muted": tokens.get("colors", {}).get("textMuted"),
        "--hb-surface": tokens.get("colors", {}).get("surface"),
        "--hb-line": tokens.get("colors", {}).get("line"),
        "--hb-gray": tokens.get("colors", {}).get("decorativeGray"),
    }
    for variable, value in color_tokens.items():
        if not value or not re.search(rf"{re.escape(variable)}\s*:\s*{re.escape(value)}\s*;", token_css, re.I):
            ERRORS.append(f"توکن JSON و CSS همگام نیستند: {variable}={value}")
    font_css = (ROOT / "assets/brand-fonts.css").read_text(encoding="utf-8", errors="replace")
    for font_path in re.findall(r"url\([\"']?([^\"')]+)", font_css):
        if not font_path.startswith(("http:", "https:", "data:")) and not (ROOT / "assets" / font_path).is_file():
            ERRORS.append(f"فایل فونت ارجاع‌شده پیدا نشد: {font_path}")

    asset_set = set(asset_paths)
    def check_asset_ref(value, label):
        if value and value not in asset_set and not (ROOT / value).is_file():
            ERRORS.append(f"ارجاع دارایی ناموجود در {label}: {value}")
    for row in social.get("records", []):
        check_asset_ref(row.get("avatar_asset"), f"social.{row.get('platform')}.avatar")
        for ref in row.get("content_assets", []):
            check_asset_ref(ref, f"social.{row.get('platform')}.content_assets")
        if row.get("is_official") and (not row.get("profile_url") or not row.get("last_verified_on")):
            ERRORS.append(f"حساب رسمی بدون URL یا تاریخ تأیید: {row.get('platform')}")
        if row.get("status") not in {"VERIFIED", "ACTIVE", "INACTIVE", "PLANNED", "UNKNOWN"}:
            ERRORS.append(f"وضعیت اجتماعی نامعتبر: {row.get('platform')}")

    # Scan relative links in Markdown and HTML; external links are deliberately not fetched.
    md_link = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
    for file in ROOT.rglob("*.md"):
        text = file.read_text(encoding="utf-8", errors="replace")
        for raw in md_link.findall(text):
            raw = raw.split()[0].strip("<>")
            check_local_path(raw, file.parent, str(file.relative_to(REPO)))
    for file in ROOT.rglob("*.html"):
        parser = LocalHTMLRefs(file)
        try:
            parser.feed(file.read_text(encoding="utf-8", errors="replace"))
        except Exception as exc:
            WARNINGS.append(f"HTML parse warning {file.relative_to(REPO)}: {exc}")

    # A null public_contact is intentional: no verified public contact is documented.
    if identity.get("public_contact") is not None:
        WARNINGS.append("اطلاعات تماس عمومی وجود دارد؛ منبع و رضایت انتشار را دستی بررسی کنید")

    print(f"Artists in registry: {len(artist_rows)} (candidate records; not site total)")
    print(f"Music records: {len(track_rows)}")
    print(f"Visual files indexed: {len(asset_rows)}")
    print(f"Social profiles with official=true: {sum(bool(r.get('is_official')) for r in social.get('records', []))}")
    for msg in WARNINGS:
        print(f"WARN: {msg}")
    for msg in ERRORS:
        print(f"ERROR: {msg}")
    if ERRORS:
        print(f"FAILED: {len(ERRORS)} error(s)")
        return 1
    print("PASS: JSON parsing, status fields, unique IDs, asset files/byte counts, token synchronization, and scanned internal links")
    return 0


if __name__ == "__main__":
    sys.exit(main())
