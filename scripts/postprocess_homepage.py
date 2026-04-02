from __future__ import annotations

import re
from html import escape

from postprocess_shared import get_base_path, render_contact_html


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
    _, a_end, _ = anchor

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


def process_homepage(
    html: str,
    features_config: dict,
    workflow_config: dict,
    contact_config: dict,
) -> str:
    html = add_hero_logo(html)
    html = reorder_landing_sections(html)
    html = add_features_intro(html, str(features_config.get("intro_text", "")))
    html = link_feature_tiles(html, features_config.get("items", []))
    html = replace_workflow_block(html, workflow_config)
    html = append_contact_section(html, contact_config)
    return html
