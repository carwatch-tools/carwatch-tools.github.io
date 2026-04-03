from __future__ import annotations

import re
from html import escape


BASE_PATH_RE = re.compile(r'<html[^>]*data-base-path="([^"]*)"')


def get_base_path(html: str) -> str:
    match = BASE_PATH_RE.search(html)
    if not match:
        return ""
    return match.group(1)


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


def resolve_theme_colors(site_config: dict) -> dict[str, dict[str, str]]:
    branding = site_config.get("branding", {}) if isinstance(site_config, dict) else {}
    colors = branding.get("colors", {}) if isinstance(branding, dict) else {}
    required_modes = ("light", "dark")
    required_keys = ("primary", "secondary", "primary_alpha", "secondary_alpha")

    if not isinstance(colors, dict):
        raise ValueError("Missing required 'branding.colors' configuration in docs/config.yaml")

    resolved: dict[str, dict[str, str]] = {}
    for mode in required_modes:
        mode_values = colors.get(mode, {})
        if not isinstance(mode_values, dict):
            raise ValueError(f"Missing required 'branding.colors.{mode}' configuration in docs/config.yaml")

        missing = [key for key in required_keys if key not in mode_values]
        if missing:
            missing_str = ", ".join(f"branding.colors.{mode}.{key}" for key in missing)
            raise ValueError(f"Missing required theme color settings in docs/config.yaml: {missing_str}")

        resolved[mode] = {key: str(mode_values[key]) for key in required_keys}

    return resolved


def inject_brand_assets(html: str, site_config: dict | None = None) -> str:
    base_path = get_base_path(html)
    theme_colors = resolve_theme_colors(site_config or {})
    light = theme_colors["light"]
    dark = theme_colors["dark"]

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
--link-color:{light["primary"]};
--link-hover:{light["primary"]};
--accent-primary:{light["primary"]};
--accent-hover:{light["secondary"]};
--accent-color:{light["primary"]};
--accent-color-alpha:{light["primary_alpha"]};
--border-secondary:{light["secondary"]};
--bg-hover:{light["secondary_alpha"]};
}}
:root[data-theme="dark"]{{
--link-color:{dark["primary"]};
--link-hover:{dark["primary"]};
--accent-primary:{dark["primary"]};
--accent-hover:{dark["secondary"]};
--accent-color:{dark["primary"]};
--accent-color-alpha:{dark["primary_alpha"]};
--border-secondary:{dark["primary"]};
--bg-hover:{dark["secondary_alpha"]};
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
.features-section .feature-emoji{{display:flex;align-items:center;justify-content:flex-start;color:var(--accent-primary);margin-bottom:1rem;line-height:1}}
.feature-icon-wrap{{display:flex;align-items:center;justify-content:flex-start}}
.feature-icon-img{{width:2rem;height:2rem;display:block}}
.feature-icon-wrap svg{{width:2rem;height:2rem;display:block}}
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
    html = re.sub(r"\s*<nav class=\"page-nav\">.*?</nav>", "", html, flags=re.DOTALL)
    header_pattern = re.compile(
        r'<div class="full-width-header">.*?</div>',
        re.DOTALL,
    )
    replacement = render_content_header(nav_items, base_path)
    html = header_pattern.sub(replacement, html, count=1)
    return html
