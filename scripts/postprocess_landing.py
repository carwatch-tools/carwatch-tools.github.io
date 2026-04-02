#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from html import escape
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


def render_workflow_html(workflow_config: dict) -> str:
    if not isinstance(workflow_config, dict):
        return ""

    parts: list[str] = []
    intro = workflow_config.get("intro_text")
    if intro:
        parts.append(f"<p>{intro}</p>")

    steps = workflow_config.get("steps", [])
    if isinstance(steps, list) and steps:
        parts.append('<div class="workflow-steps">')
        for i, step in enumerate(steps, start=1):
            if not isinstance(step, dict):
                continue
            title = escape(str(step.get("title", "")))
            text = escape(str(step.get("text", "")))
            parts.append(
                '<div class="workflow-step">'
                f'<span class="workflow-step-number">{i}</span>'
                f'<div class="workflow-step-body"><strong>{title}:</strong> {text}</div>'
                '</div>'
            )
        parts.append("</div>")

    image = workflow_config.get("image", {})
    if isinstance(image, dict) and image.get("src"):
        src = escape(str(image.get("src")))
        alt = escape(str(image.get("alt", "")))
        max_width = escape(str(image.get("max_width", "760px")))
        parts.append(
            f'<p><img src="{src}" alt="{alt}" '
            f'style="display:block;width:100%;max-width:{max_width};height:auto;margin:1.5rem auto 0;"></p>'
        )

    return "".join(parts)


def render_contact_html(contact_config: dict) -> str:
    if not isinstance(contact_config, dict):
        return ""
    title = escape(str(contact_config.get("title", "Contact")))
    text = escape(str(contact_config.get("text", "")))
    email = escape(str(contact_config.get("email", "")))
    if not email:
        return ""

    return (
        '<section class="text-section contact-section">'
        '<div class="text-section-content align-left" style="max-width: 900px;">'
        f'<h2 class="text-section-title">{title}</h2>'
        '<div class="text-section-body">'
        f'<p>{text} <a href="mailto:{email}"><strong>{email}</strong></a>.</p>'
        "</div>"
        "</div>"
        "</section>"
    )


def render_content_header(nav_items: list[dict], base_path: str) -> str:
    links: list[str] = []
    for item in nav_items:
        if not isinstance(item, dict):
            continue
        text = escape(str(item.get("text", "")))
        url = str(item.get("url", ""))
        href = f"{base_path}{url}" if url.startswith("/") else escape(url)
        links.append(f'<a href="{href}">{text}</a>')

    nav_html = "".join(links)
    return (
        '<header class="content-site-header">'
        '<div class="content-site-header-inner">'
        f'<a href="{base_path}/" class="full-width-logo brand-link"><img src="{base_path}/brand/logo.svg" alt="" class="brand-mark"><span>CARWatch</span></a>'
        f'<nav class="content-site-nav">{nav_html}</nav>'
        '<button id="theme-toggle" class="theme-toggle" aria-label="Toggle theme"><span class="theme-icon"></span></button>'
        '</div>'
        '</header>'
    )


def inject_brand_assets(html: str) -> str:
    base_path = get_base_path(html)

    favicon_markup = f"""
<link rel="icon" type="image/x-icon" href="{base_path}/brand/favicon.ico">
<link rel="icon" type="image/png" sizes="16x16" href="{base_path}/brand/favicon-16x16.png">
<link rel="icon" type="image/png" sizes="32x32" href="{base_path}/brand/favicon-32x32.png">
<link rel="apple-touch-icon" sizes="180x180" href="{base_path}/brand/apple-touch-icon.png">
<link rel="manifest" href="{base_path}/site.webmanifest">
<meta name="theme-color" content="#ffffff">
<style>
:root,
:root[data-theme="light"]{{
--link-color:#04316A;
--link-hover:#04316A;
--accent-primary:#04316A;
--accent-hover:#8C9FB1;
--accent-color:#04316A;
--accent-color-alpha:rgba(4,49,106,0.14);
--border-secondary:#8C9FB1;
--bg-hover:rgba(140,159,177,0.16);
}}
:root[data-theme="dark"]{{
--link-color:#8C9FB1;
--link-hover:#8C9FB1;
--accent-primary:#8C9FB1;
--accent-hover:#04316A;
--accent-color:#8C9FB1;
--accent-color-alpha:rgba(140,159,177,0.18);
--border-secondary:#8C9FB1;
--bg-hover:rgba(140,159,177,0.12);
}}
.brand-link{{display:inline-flex;align-items:center;gap:.55rem;color:inherit;text-decoration:none}}
.brand-mark{{width:1.5rem;height:1.5rem;display:block;flex:none}}
.landing-logo.brand-link{{font-size:var(--font-size-xl-2xl)}}
.full-width-logo.brand-link{{font-size:var(--font-size-xl)}}
.site-title .brand-link{{font-size:inherit;font-weight:inherit}}
.landing-logo.brand-link,
.full-width-logo.brand-link,
.site-title .brand-link{{color:var(--accent-primary)}}
.hero-title,
.text-section-title,
.section-title,
.links-grid-title,
.page-header h1,
.markdown-body h1,
.markdown-body h2,
.markdown-body h3{{color:var(--accent-primary)}}
.hero-title.brand-title{{display:inline-flex;align-items:center;gap:1rem}}
.hero-title .brand-mark{{width:5rem;height:5rem}}
.workflow-steps{{display:grid;gap:1rem;margin-top:1.25rem}}
.workflow-step{{display:grid;grid-template-columns:2.25rem 1fr;gap:1rem;align-items:start;padding:1rem 1.1rem;border:1px solid var(--border-primary);border-radius:.9rem;background:var(--bg-secondary)}}
.workflow-step-number{{display:inline-flex;align-items:center;justify-content:center;width:2.25rem;height:2.25rem;border-radius:999px;background:var(--accent-primary);color:var(--bg-primary);font-weight:700;line-height:1}}
.workflow-step-body{{color:var(--text-secondary);line-height:1.55}}
.workflow-step-body strong{{font-size:1.02em;color:var(--text-primary)}}
.contact-section{{padding-top:2.5rem}}
.contact-section .text-section-body p{{font-size:1.02rem}}
.content-site-header{{background:var(--bg-primary);border-bottom:1px solid var(--border-primary)}}
.content-site-header-inner{{max-width:1100px;margin:0 auto;padding:1rem 1.5rem;display:flex;align-items:center;justify-content:space-between;gap:1.5rem}}
.content-site-nav{{display:flex;align-items:center;gap:1.35rem;flex-wrap:wrap}}
.content-site-nav a{{color:var(--text-secondary);text-decoration:none;font-size:var(--font-size-md-lg)}}
.content-site-nav a:hover{{color:var(--link-color)}}
.full-width-layout .main-content{{max-width:1100px;margin:0 auto;padding:2.5rem 1.5rem 4rem}}
.page-content{{max-width:920px;margin:0 auto;background:var(--bg-primary);border:1px solid var(--border-primary);border-radius:1rem;padding:2rem 2.25rem;box-shadow:var(--shadow-sm)}}
.page-header{{margin-bottom:2rem;padding-bottom:1.25rem;border-bottom:1px solid var(--border-primary)}}
.page-header h1{{font-size:clamp(2rem,4vw,2.8rem);line-height:1.1;letter-spacing:-0.02em;margin:0}}
.page-description{{font-size:1.02rem;max-width:62ch;color:var(--text-secondary)}}
.page-updated{{font-size:.92rem;color:var(--text-secondary)}}
.markdown-body{{max-width:none}}
.markdown-body > h1:first-child{{display:none}}
.markdown-body p{{max-width:68ch;line-height:1.72}}
.markdown-body ul,
.markdown-body ol{{max-width:68ch}}
.markdown-body li{{margin-bottom:.45rem}}
.markdown-body blockquote{{max-width:68ch;background:var(--bg-secondary);border-left:4px solid var(--accent-primary);padding:1rem 1.1rem;border-radius:.5rem}}
.markdown-body table{{background:var(--bg-primary);border-radius:.75rem;overflow:hidden}}
.page-nav{{max-width:920px;margin:1.5rem auto 0}}
@media (max-width: 768px){{
.content-site-header-inner{{padding:.9rem 1rem;align-items:flex-start;flex-direction:column}}
.content-site-nav{{gap:.85rem 1rem}}
.page-content{{padding:1.35rem 1rem;border-radius:.85rem}}
.full-width-layout .main-content{{padding:1.25rem 1rem 3rem}}
}}
</style>""".strip()

    if 'rel="icon"' not in html:
        html = html.replace("</head>", favicon_markup + "\n</head>", 1)

    replacements = {
        'class="landing-logo"': 'class="landing-logo brand-link"',
        'class="full-width-logo"': 'class="full-width-logo brand-link"',
    }
    for old, new in replacements.items():
        html = html.replace(old, new)

    html = html.replace(
        '<p class="site-title"><a href="{{BASE}}/">',
        '<p class="site-title"><a href="{{BASE}}/" class="brand-link">',
    )

    logo_inner = '<img src="{{BASE}}/brand/logo.svg" alt="" class="brand-mark"><span>CARWatch</span>'
    html = html.replace('>CARWatch</a>', f'>{logo_inner}</a>')
    html = html.replace('{{BASE}}', base_path)
    return html


def add_hero_logo(html: str) -> str:
    if 'class="hero-title brand-title"' in html:
        return html

    return html.replace(
        '<h1 class="hero-title">CARWatch</h1>',
        '<h1 class="hero-title brand-title"><img src="/brand/logo.svg" alt="" class="brand-mark"><span>CARWatch</span></h1>',
        1,
    )


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


def replace_workflow_block(html: str, workflow_config: dict) -> str:
    section = find_section(html, "text-section", "Workflow")
    if not section:
        return html

    start, end, block = section
    rendered = render_workflow_html(workflow_config)
    if not rendered:
        return html

    if '<div class="text-section-body">' in block:
        updated = re.sub(
            r'<div class="text-section-body">.*?</div>\s*</div>\s*</section>',
            f'<div class="text-section-body">{rendered}</div>\n\n</div>\n</section>',
            block,
            count=1,
            flags=re.DOTALL,
        )
    else:
        updated = re.sub(
            r'\s*</div>\s*</section>\s*$',
            f'\n<div class="text-section-body">{rendered}</div>\n\n</div>\n</section>',
            block,
            count=1,
            flags=re.DOTALL,
        )
    return html[:start] + updated + html[end:]


def append_contact_section(html: str, contact_config: dict) -> str:
    rendered = render_contact_html(contact_config)
    if not rendered or 'class="contact-section"' in html:
        return html
    return html.replace("</main>", rendered + "\n\n</main>", 1)


def remove_contact_sections(html: str) -> str:
    return re.sub(
        r'\s*<section class="text-section contact-section">.*?</section>',
        "",
        html,
        flags=re.DOTALL,
    )


def cleanup_content_page_chrome(html: str, nav_items: list[dict]) -> str:
    base_path = get_base_path(html)
    html = re.sub(r"\s*<p class=\"page-updated\">.*?</p>", "", html, flags=re.DOTALL)
    html = re.sub(r"\s*<button class=\"copy-md-btn\".*?</button>", "", html, flags=re.DOTALL)
    header_pattern = re.compile(
        r'<div class="full-width-header">.*?</div>',
        re.DOTALL,
    )
    replacement = render_content_header(nav_items, base_path)
    html = header_pattern.sub(replacement, html, count=1)
    return html


def process_html(target: Path, site_root: Path) -> None:
    html = target.read_text(encoding="utf-8")
    landing_config = load_landing_config(target)
    nav_items = landing_config.get("nav", []) if isinstance(landing_config, dict) else []
    features_config = landing_config.get("features", {}) if isinstance(landing_config, dict) else {}
    workflow_config = landing_config.get("workflow", {}) if isinstance(landing_config, dict) else {}
    contact_config = landing_config.get("contact", {}) if isinstance(landing_config, dict) else {}
    rewritten = inject_brand_assets(html)
    rewritten = remove_contact_sections(rewritten)
    if target.resolve() == (site_root / "index.html").resolve():
        rewritten = add_hero_logo(rewritten)
        rewritten = reorder_landing_sections(rewritten)
        rewritten = add_features_intro(rewritten, str(features_config.get("intro_text", "")))
        rewritten = link_feature_tiles(rewritten, features_config.get("items", []))
        rewritten = replace_workflow_block(rewritten, workflow_config)
        rewritten = append_contact_section(rewritten, contact_config)
    else:
        rewritten = cleanup_content_page_chrome(rewritten, nav_items)
    target.write_text(rewritten, encoding="utf-8")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: postprocess_landing.py <site-dir-or-html-file>", file=sys.stderr)
        return 1

    target = Path(sys.argv[1])
    if target.is_dir():
        site_root = target.resolve()
        for html_file in sorted(target.rglob("*.html")):
            process_html(html_file, site_root)
    else:
        process_html(target, target.resolve().parent)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
