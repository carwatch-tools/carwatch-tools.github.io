#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from pathlib import Path


SECTION_RE = re.compile(r"<section class=\"([^\"]+)\">.*?</section>", re.DOTALL)


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


def reorder_landing_sections(html: str) -> str:
    features = find_section(html, "features-section", "The CARWatch Framework Ecosystem")
    anchor = find_section(html, "text-section", "What is CARWatch")

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


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: postprocess_landing.py <index.html>", file=sys.stderr)
        return 1

    target = Path(sys.argv[1])
    html = target.read_text(encoding="utf-8")
    rewritten = reorder_landing_sections(html)
    target.write_text(rewritten, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
