#!/usr/bin/env python3

from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover - exercised in environments without PyYAML
    yaml = None

from postprocess_homepage import process_homepage
from postprocess_shared import (
    cleanup_content_page_chrome,
    inject_brand_assets,
    remove_contact_sections,
)


def parse_scalar(value: str) -> object:
    value = value.strip()
    if value in {'""', "''"}:
        return ""
    if value == "true":
        return True
    if value == "false":
        return False
    if value.isdigit():
        return int(value)
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    return value


def split_key_value(text: str) -> tuple[str, str]:
    key, _, value = text.partition(":")
    return key.strip(), value.strip()


def parse_yaml_block(lines: list[tuple[int, str]], start: int, indent: int) -> tuple[object, int]:
    if lines[start][1].startswith("- "):
        items: list[object] = []
        index = start
        while index < len(lines):
            line_indent, text = lines[index]
            if line_indent != indent or not text.startswith("- "):
                break

            content = text[2:].strip()
            index += 1
            if not content:
                item: object = {}
                if index < len(lines) and lines[index][0] > line_indent:
                    item, index = parse_yaml_block(lines, index, lines[index][0])
                items.append(item)
                continue

            if ":" in content:
                key, value = split_key_value(content)
                item_dict: dict[str, object] = {}
                if value:
                    item_dict[key] = parse_scalar(value)
                elif index < len(lines) and lines[index][0] > line_indent:
                    nested, index = parse_yaml_block(lines, index, lines[index][0])
                    item_dict[key] = nested
                else:
                    item_dict[key] = {}

                if index < len(lines) and lines[index][0] > line_indent:
                    extra, index = parse_yaml_block(lines, index, lines[index][0])
                    if isinstance(extra, dict):
                        item_dict.update(extra)
                items.append(item_dict)
                continue

            items.append(parse_scalar(content))

        return items, index

    mapping: dict[str, object] = {}
    index = start
    while index < len(lines):
        line_indent, text = lines[index]
        if line_indent != indent or text.startswith("- "):
            break

        key, value = split_key_value(text)
        index += 1
        if value:
            mapping[key] = parse_scalar(value)
            continue

        if index < len(lines) and lines[index][0] > line_indent:
            nested, index = parse_yaml_block(lines, index, lines[index][0])
            mapping[key] = nested
        else:
            mapping[key] = {}

    return mapping, index


def parse_simple_yaml(text: str) -> dict:
    lines: list[tuple[int, str]] = []
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        lines.append((indent, stripped))

    if not lines:
        return {}

    parsed, _ = parse_yaml_block(lines, 0, lines[0][0])
    return parsed if isinstance(parsed, dict) else {}


def load_site_config() -> dict:
    config_path = Path(__file__).resolve().parent.parent / "docs" / "config.yaml"
    config_text = config_path.read_text(encoding="utf-8")
    if yaml is not None:
        return yaml.safe_load(config_text) or {}
    return parse_simple_yaml(config_text)


def process_html(target: Path, site_root: Path, site_config: dict) -> None:
    html = target.read_text(encoding="utf-8")
    landing_config = site_config.get("landing", {}) if isinstance(site_config, dict) else {}
    nav_items = landing_config.get("nav", []) if isinstance(landing_config, dict) else []
    features_config = landing_config.get("features", {}) if isinstance(landing_config, dict) else {}
    workflow_config = landing_config.get("workflow", {}) if isinstance(landing_config, dict) else {}
    contact_config = landing_config.get("contact", {}) if isinstance(landing_config, dict) else {}

    rewritten = inject_brand_assets(html, site_config)
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

    site_config = load_site_config()
    target = Path(sys.argv[1])
    if target.is_dir():
        site_root = target.resolve()
        for html_file in sorted(target.rglob("*.html")):
            process_html(html_file, site_root, site_config)
    else:
        process_html(target, target.resolve().parent, site_config)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
