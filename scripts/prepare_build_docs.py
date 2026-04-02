#!/usr/bin/env python3

from __future__ import annotations

import shutil
import sys
from pathlib import Path


def encode_non_ascii(text: str) -> str:
    return "".join(f"&#{ord(ch)};" if ord(ch) > 127 else ch for ch in text)


def prepare_docs(source_dir: Path, target_dir: Path) -> None:
    if target_dir.exists():
        shutil.rmtree(target_dir)
    shutil.copytree(source_dir, target_dir)

    for markdown_file in target_dir.rglob("*.md"):
        text = markdown_file.read_text(encoding="utf-8")
        markdown_file.write_text(encode_non_ascii(text), encoding="utf-8")


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: prepare_build_docs.py <source-docs-dir> <target-docs-dir>", file=sys.stderr)
        return 1

    source_dir = Path(sys.argv[1]).resolve()
    target_dir = Path(sys.argv[2]).resolve()
    prepare_docs(source_dir, target_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
