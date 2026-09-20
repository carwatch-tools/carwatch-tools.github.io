"""Load structured news and render a compact, native HTML accordion."""

from __future__ import annotations

import json
import re
from datetime import date
from html import escape
from pathlib import Path
from urllib.parse import urlsplit


def validate_news(items: object) -> list[dict]:
    if not isinstance(items, list):
        raise ValueError("news: expected a JSON array of entries")
    ids: set[str] = set()
    for index, item in enumerate(items, start=1):
        context = f"news entry {index}"
        if not isinstance(item, dict):
            raise ValueError(f"{context}: expected an object")
        for field in ("id", "date", "title", "text"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                raise ValueError(f"{context}: '{field}' must be a non-empty string")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", item["id"]):
            raise ValueError(f"{context}: 'id' must use lowercase letters, numbers and hyphens")
        if item["id"] in ids:
            raise ValueError(f"{context}: duplicate id '{item['id']}'")
        ids.add(item["id"])
        try:
            if date.fromisoformat(item["date"]).isoformat() != item["date"]:
                raise ValueError
        except ValueError:
            raise ValueError(f"{context}: 'date' must be a valid YYYY-MM-DD date") from None
        for field, url_key, text_key in (("link", "url", "label"), ("image", "src", "alt")):
            if field not in item:
                continue
            value = item[field]
            if not isinstance(value, dict) or any(
                not isinstance(value.get(key), str) or not value[key].strip()
                for key in (url_key, text_key)
            ):
                raise ValueError(f"{context}: '{field}' requires '{url_key}' and '{text_key}' strings")
            url = value[url_key]
            if not ((url.startswith("/") and not url.startswith("//")) or
                    (urlsplit(url).scheme in {"https", "http"} and urlsplit(url).netloc)):
                raise ValueError(f"{context}: '{field}.{url_key}' must be an HTTP(S) URL or root-relative path")
    return sorted(items, key=lambda item: item["date"], reverse=True)


def load_news(path: Path) -> list[dict]:
    try:
        return validate_news(json.loads(path.read_text(encoding="utf-8")))
    except (OSError, ValueError) as error:
        raise ValueError(f"{path}: {error}") from error


def render_news_html(items: list[dict], title: str = "News", base_path: str = "") -> str:
    items = validate_news(items)
    if not items:
        return ""

    def url(value: str) -> str:
        return escape(base_path.rstrip("/") + value if value.startswith("/") else value)

    parts = [
        '<section class="text-section news-section" id="news" aria-labelledby="news-title">',
        '<div class="text-section-content align-left" style="max-width: 900px;">',
        f'<h2 class="text-section-title" id="news-title">{escape(title)}</h2>',
        '<div class="news-list">',
    ]
    for index, item in enumerate(items):
        opened = " open" if index == 0 else ""
        parts.extend([
            f'<details class="news-item" id="news-{item["id"]}" name="carwatch-news"{opened}>',
            f'<summary><span>{escape(item["title"])}</span></summary>',
            '<div class="news-body">',
            f'<time datetime="{item["date"]}">{item["date"]}</time>',
            f'<p>{escape(item["text"])}</p>',
        ])
        if image := item.get("image"):
            parts.append(f'<img class="news-image" src="{url(image["src"])}" alt="{escape(image["alt"])}" loading="lazy">')
        if link := item.get("link"):
            parts.append(f'<a class="news-link" href="{url(link["url"])}">{escape(link["label"])}</a>')
        parts.append('</div></details>')
    parts.append('</div></div></section>')
    return "\n".join(parts)
