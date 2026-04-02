#!/usr/bin/env python3

from __future__ import annotations

import sys
from pathlib import Path

import yaml

from postprocess_homepage import process_homepage
from postprocess_shared import (
    cleanup_content_page_chrome,
    inject_brand_assets,
    remove_contact_sections,
)


def load_landing_config() -> dict:
    config_path = Path(__file__).resolve().parent.parent / "docs" / "config.yaml"
    with config_path.open("r", encoding="utf-8") as fh:
        config = yaml.safe_load(fh) or {}
    return config.get("landing", {})


def process_html(target: Path, site_root: Path, landing_config: dict) -> None:
    html = target.read_text(encoding="utf-8")
    nav_items = landing_config.get("nav", []) if isinstance(landing_config, dict) else []
    features_config = landing_config.get("features", {}) if isinstance(landing_config, dict) else {}
    workflow_config = landing_config.get("workflow", {}) if isinstance(landing_config, dict) else {}
    contact_config = landing_config.get("contact", {}) if isinstance(landing_config, dict) else {}

    rewritten = inject_brand_assets(html)
    rewritten = remove_contact_sections(rewritten)

    if target.resolve() == (site_root / "index.html").resolve():
        rewritten = process_homepage(
            rewritten,
            features_config=features_config,
            workflow_config=workflow_config,
            contact_config=contact_config,
        )
    else:
        rewritten = cleanup_content_page_chrome(rewritten, nav_items)

    target.write_text(rewritten, encoding="utf-8")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: postprocess_landing.py <site-dir-or-html-file>", file=sys.stderr)
        return 1

    landing_config = load_landing_config()
    target = Path(sys.argv[1])
    if target.is_dir():
        site_root = target.resolve()
        for html_file in sorted(target.rglob("*.html")):
            process_html(html_file, site_root, landing_config)
    else:
        process_html(target, target.resolve().parent, landing_config)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
