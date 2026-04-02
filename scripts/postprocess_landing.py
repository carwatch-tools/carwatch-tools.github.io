#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml


SECTION_RE = re.compile(r"<section class=\"([^\"]+)\">.*?</section>", re.DOTALL)
BASE_PATH_RE = re.compile(r'<html[^>]*data-base-path="([^"]*)"')


def find_section(html: str, class_name: str, heading: str | None = None) -> tuple[int, int, str] | None:
    for match in SECTION_RE.finditer(html):
        classes = match.group(1).split()
        if class_name not in classes:
            continue
        block = match.group(0)
        if heading and heading not in block:
            continue
        return match.start(), match.end(), block
    return None


def get_base_path(html: str) -> str:
    match = BASE_PATH_RE.search(html)
    if not match:
        return ""
    return match.group(1)


def load_landing_config(index_path: Path) -> dict:
    config_path = Path(__file__).resolve().parent.parent / "docs" / "config.yaml"
    with config_path.open("r", encoding="utf-8") as fh:
        config = yaml.safe_load(fh) or {}
    return config.get("landing", {})


def reorder_landing_sections(html: str) -> str:
    features = find_section(html, "features-section", "The CARWatch Framework Ecosystem")
    anchor = find_section(html, "text-section", "Why CARWatch")

    if not features or not anchor:
        return html

    f_start, f_end, f_block = features
    a_start, a_end, _ = anchor

    if f_start > a_end:
        without_features = html[:f_start] + html[f_end:]
        insert_at = a_end
    else:
        without_features = html[:f_start] + html[f_end:]
        insert_at = a_end - len(f_block)

    return without_features[:insert_at] + "\n\n" + f_block + without_features[insert_at:]


def add_features_intro(html: str, intro_text: str) -> str:
    features = find_section(html, "features-section", "The CARWatch Framework Ecosystem")
    if not features or not intro_text:
        return html

    start, end, block = features
    if 'class="section-description"' in block:
        return html

    intro = f'<p class="section-description">{intro_text}</p>'

    updated = block.replace("</h2>", "</h2>\n" + intro, 1)
    return html[:start] + updated + html[end:]


def link_feature_tiles(html: str, items: list[dict]) -> str:
    features = find_section(html, "features-section", "The CARWatch Framework Ecosystem")
    if not features:
        return html

    base_path = get_base_path(html)
    link_map: dict[str, str] = {}
    for item in items:
        title = item.get("title")
        url = item.get("url")
        if not title or not url:
            continue
        href = f"{base_path}{url}" if isinstance(url, str) and url.startswith("/") else str(url)
        link_map[str(title).lower()] = href

    start, end, block = features
    card_pattern = re.compile(
        r'<div class="feature-card">(?P<body>.*?)<h3 class="feature-title">(?P<title>[^<]+)</h3>(?P<rest>.*?)</div>',
        re.DOTALL,
    )

    def replace_card(match: re.Match[str]) -> str:
        title = match.group("title")
        href = link_map.get(title.lower())
        if not href:
            return match.group(0)
        return (
            f'<a href="{href}" class="feature-card" style="text-decoration:none;color:inherit;">'
            f'{match.group("body")}<h3 class="feature-title">{title}</h3>{match.group("rest")}</a>'
        )

    updated = card_pattern.sub(replace_card, block)

    return html[:start] + updated + html[end:]


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: postprocess_landing.py <index.html>", file=sys.stderr)
        return 1

    target = Path(sys.argv[1])
    html = target.read_text(encoding="utf-8")
    landing_config = load_landing_config(target)
    features_config = landing_config.get("features", {}) if isinstance(landing_config, dict) else {}
    rewritten = reorder_landing_sections(html)
    rewritten = add_features_intro(rewritten, str(features_config.get("intro_text", "")))
    rewritten = link_feature_tiles(rewritten, features_config.get("items", []))
    target.write_text(rewritten, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
