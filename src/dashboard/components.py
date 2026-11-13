"""Reusable accessible UI components & inline SVG icon primitives for PRESSUREIQ v4 Editorial.

Warm Ivory (#F8F4EC) + Soft Cream (#F1E9DD) + Terracotta (#BD6548) + Deep Ink (#282321)
"""

from __future__ import annotations

import html
from typing import Dict, List, Optional, Sequence
import streamlit as st

from src.dashboard.design_tokens import (
    FONTS,
    PALETTE,
    PRODUCT_NAME,
    PRODUCT_TAGLINE,
    PRODUCT_VERSION,
    RETENTION_DEADLINE_DATE,
    SNAPSHOT_ANCHOR_DATE,
    STATUS_TONES,
)

_SVG_PATHS: Dict[str, str] = {
    "overview": '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/>',
    "trophy": '<path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/>',
    "user": '<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
    "compare": '<line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>',
    "activity": '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>',
    "sparkles": '<path d="M12 3l1.9 5.8L20 11l-6.1 2.2L12 19l-1.9-5.8L4 11l6.1-2.2z"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
    "briefcase": '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
    "book": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>',
    "database": '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14a9 3 0 0 0 18 0V5"/><path d="M3 12a9 3 0 0 0 18 0"/>',
    "check": '<polyline points="20 6 9 17 4 12"/>',
    "alert": '<circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>',
}


def svg_icon(name: str, size: int = 16, color: str = "currentColor") -> str:
    """Return accessible inline SVG icon markup (zero emojis)."""
    path = _SVG_PATHS.get(name, _SVG_PATHS["activity"])
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" '
        f'fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" '
        f'aria-hidden="true" style="flex-shrink:0;vertical-align:middle;">{path}</svg>'
    )


def render_brand_emblem() -> str:
    """Author inline vector cricket telemetry emblem in warm terracotta & cream."""
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="34" height="34" viewBox="0 0 34 34" fill="none" aria-hidden="true" style="flex-shrink:0;">'
        '<defs><linearGradient id="piqEmblemBg" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#FBF6EE"/><stop offset="1" stop-color="#F1E9DD"/></linearGradient></defs>'
        '<rect x="1.5" y="1.5" width="31" height="31" rx="8.5" fill="url(#piqEmblemBg)" stroke="#BD6548" stroke-width="1.5"/>'
        # Minimalist cricket ball curve & seam
        '<circle cx="17" cy="17" r="9.5" fill="#FFFFFF" stroke="#BD6548" stroke-width="1.4"/>'
        '<path d="M12 12C14 14.5 14 19.5 12 22" stroke="#BD6548" stroke-width="1.2" stroke-linecap="round"/>'
        '<path d="M22 12C20 14.5 20 19.5 22 22" stroke="#BD6548" stroke-width="1.2" stroke-linecap="round"/>'
        '<circle cx="21" cy="10" r="1.8" fill="#C5A46D"/>'
        '</svg>'
    )


def status_badge_html(status: str) -> str:
    """Build accessible editorial badge pill with distinct fill, border, text color."""
    label = str(status or "Pending Verification").strip()
    bg, border, txt = STATUS_TONES.get(label, STATUS_TONES["Pending Verification"])
    return (
        f'<span class="piq-badge" style="background:{bg};border:1px solid {border};color:{txt};">'
        f'{html.escape(label)}</span>'
    )


def render_top_bar(
    page_label: str,
    frozen_ok: bool,
    snapshot_date: str = SNAPSHOT_ANCHOR_DATE,
) -> None:
    """Render refined top navigation bar with breadcrumb, integrity indicator, and anchor date."""
    integrity_badge = (
        f'<span class="piq-badge" style="background:rgba(132,146,122,0.22);border:1px solid #84927A;color:#E8F0E4;">'
        f'<span style="width:7px;height:7px;border-radius:50%;background:#84927A;animation:piq-pulse 2.4s ease-out infinite;"></span>'
        f'{svg_icon("check", 12, "#E8F0E4")} Model A Verified (SHA-256)</span>'
        if frozen_ok
        else f'<span class="piq-badge" style="background:rgba(184,74,57,0.25);border:1px solid #B84A39;color:#FCEAE8;">'
        f'{svg_icon("alert", 12, "#FCEAE8")} Integrity Mismatch</span>'
    )
    snap_badge = (
        f'<span class="piq-badge" style="background:rgba(197,164,109,0.22);border:1px solid #C5A46D;color:#F9F4EB;">'
        f'Snapshot: {html.escape(snapshot_date)}</span>'
    )
    deadline_badge = (
        f'<span class="piq-badge" style="background:rgba(216,203,190,0.20);border:1px solid #D8CBBE;color:#F1E9DD;">'
        f'BCCI Retention Filing: {RETENTION_DEADLINE_DATE}</span>'
    )
    st.markdown(
        f'<div class="piq-topbar" role="banner">'
        f'<div class="piq-crumb"><span class="piq-crumb-muted">{PRODUCT_NAME}</span>'
        f'<span class="piq-crumb-muted">/</span><span style="color:#FFFFFF;font-weight:600;">{html.escape(page_label)}</span></div>'
        f'<div class="piq-meta-strip">{integrity_badge}{snap_badge}{deadline_badge}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def _feature_card_html(
    label: str,
    name: Optional[str],
    score: Optional[float],
    ci: Optional[str],
    role: Optional[str],
    accent: str,
    score_color: str,
    badge_style: str,
    empty_note: str,
) -> str:
    """Build one featured-player card (styled by .piq-feature* classes in styles.py)."""
    if name and score is not None:
        badge = (
            f'<span class="piq-badge" style="{badge_style}">{html.escape(role)}</span>'
            if role
            else ""
        )
        return (
            f'<div class="piq-feature" style="--feat-accent:{accent};--feat-score:{score_color};">'
            f'<div class="piq-feature-head"><span class="piq-feature-label">{label}</span>{badge}</div>'
            f'<div class="piq-feature-name">{html.escape(name)}</div>'
            f'<div class="piq-feature-meta">'
            f'<span class="piq-feature-score">{score:.2f}</span>'
            f'<span class="piq-feature-note">Reliability Score · 95% CI {html.escape(ci or "N/A")}</span>'
            f'</div>'
            f'</div>'
        )
    return (
        f'<div class="piq-feature" style="--feat-accent:#77675D;--feat-score:#77675D;">'
        f'<div class="piq-feature-head"><span class="piq-feature-label">{label}</span>'
        f'<span class="piq-badge" style="background:#FAF6F0;border:1px solid #D8CBBE;color:#77675D;font-weight:600;">Data Unavailable</span>'
        f'</div>'
        f'<div class="piq-feature-name is-empty">Ranking Data Unavailable</div>'
        f'<div class="piq-feature-note" style="margin-top:4px;">{empty_note}</div>'
        f'</div>'
    )


def render_editorial_hero(
    featured_bat_name: Optional[str] = None,
    featured_bat_score: Optional[float] = None,
    featured_bat_ci: Optional[str] = None,
    featured_bat_role: Optional[str] = None,
    featured_bowl_name: Optional[str] = None,
    featured_bowl_score: Optional[float] = None,
    featured_bowl_ci: Optional[str] = None,
    featured_bowl_role: Optional[str] = None,
) -> None:
    """Render the master Kinfolk-inspired editorial hero section (User Requirements Section 4)."""
    bat_card_html = _feature_card_html(
        "FEATURED #1 BATTER",
        featured_bat_name,
        featured_bat_score,
        featured_bat_ci,
        featured_bat_role,
        accent="#BD6548",
        score_color="#BD6548",
        badge_style="background:#FAF0EB;border:1px solid #BD6548;color:#BD6548;font-weight:700;",
        empty_note="No verified Model A batter rankings loaded",
    )
    bowl_card_html = _feature_card_html(
        "FEATURED #1 BOWLER",
        featured_bowl_name,
        featured_bowl_score,
        featured_bowl_ci,
        featured_bowl_role,
        accent="#C5A46D",
        score_color="#75460E",
        badge_style="background:#FAF6ED;border:1px solid #C5A46D;color:#75460E;font-weight:700;",
        empty_note="No verified Model A bowler rankings loaded",
    )

    hero_html = (
        f'<section class="piq-hero" aria-label="PRESSUREIQ Editorial Overview">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:32px;">'
        f'<div style="flex:1 1 540px;min-width:0;max-width:100%;">'
        f'<div class="piq-hero-eyebrow">{render_brand_emblem()}<span>{PRODUCT_NAME} · CRICKET INTELLIGENCE PUBLICATION</span></div>'
        f'<h1 class="piq-hero-title">Beyond Performance.</h1>'
        f'<div class="piq-hero-tagline">Measuring composure under pressure.</div>'
        f'<p class="piq-hero-desc">An advanced cricket intelligence platform identifying players who deliver when the game is on the line. Engineered for Rajasthan Royals SupeRR Selector Season 2, PRESSUREIQ isolates true high-leverage composure from low-stakes run accumulation across 200,999 ball-by-ball deliveries.</p>'
        f'<div class="piq-hero-stats">'
        f'<span class="piq-tape-tag">200,999 Balls</span>'
        f'<span class="piq-tape-tag">867 Played Matches</span>'
        f'<span class="piq-tape-tag">N=2,000 Bootstrap</span>'
        f'<span class="piq-tape-tag" style="background:#BD6548;color:#FFFFFF;">Frozen Model A</span>'
        f'</div>'
        f'</div>'
        f'<div class="piq-feature-col" style="flex:1 1 380px;min-width:0;max-width:100%;">'
        f'{bat_card_html}'
        f'{bowl_card_html}'
        f'</div>'
        f'</div>'
        f'</section>'
    )
    st.markdown(hero_html, unsafe_allow_html=True)


def render_kpi_grid(cards: List[Dict[str, str]]) -> None:
    """Render responsive CSS Grid of editorial KPI cards."""
    items = []
    for c in cards:
        accent = c.get("accent", PALETTE["accent_terracotta"])
        icon = svg_icon(c.get("icon", "activity"), 15, accent)
        items.append(
            f'<div class="piq-kpi" style="--kpi-accent:{accent};">'
            f'<div class="piq-kpi-head"><span>{html.escape(c["label"])}</span>{icon}</div>'
            f'<div class="piq-kpi-val">{html.escape(str(c["value"]))}</div>'
            f'<div class="piq-kpi-sub">{html.escape(str(c["sub"]))}</div>'
            f'</div>'
        )
    st.markdown(f'<div class="piq-kpi-grid">{"".join(items)}</div>', unsafe_allow_html=True)


def render_section_header(title: str, subtitle: str = "", icon: str = "activity") -> None:
    """Render editorial section header with Playfair Display serif styling."""
    sub_html = f'<p class="piq-sec-sub">{html.escape(subtitle)}</p>' if subtitle else ""
    st.markdown(
        f'<div class="piq-sec-head">'
        f'<h2 class="piq-sec-title">{svg_icon(icon, 18, PALETTE["accent_terracotta"])}<span>{html.escape(title)}</span></h2>'
        f'{sub_html}</div>',
        unsafe_allow_html=True,
    )


def render_callout(body_html: str, accent: str = PALETTE["accent_terracotta"]) -> None:
    """Render warm cream callout panel with terracotta accent."""
    st.markdown(
        f'<div class="piq-callout" style="--callout-accent:{accent};">{body_html}</div>',
        unsafe_allow_html=True,
    )


def render_chart_caption(caption_text: str) -> None:
    """Render refined editorial analytical interpretation below Plotly visualizations."""
    st.markdown(
        f'<div class="piq-chart-caption">'
        f'{svg_icon("activity", 13, PALETTE["accent_terracotta"])}'
        f'<span><b>Analytical Takeaway:</b> {caption_text}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_empty_state(heading: str, guidance: str) -> None:
    """Render elegant editorial empty state."""
    st.markdown(
        f'<div class="piq-empty">'
        f'<div style="font-family:\'Playfair Display\',serif;font-size:1.15rem;font-weight:600;color:#282321;margin-bottom:6px;">{html.escape(heading)}</div>'
        f'<div style="font-size:0.88rem;color:#77675D;">{html.escape(guidance)}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_footer(batter_sha: str, bowler_sha: str) -> None:
    """Render warm editorial footer with version and immutable Model A checksum provenance."""
    st.markdown(
        f'<footer class="piq-footer">'
        f'<span><b>{PRODUCT_NAME}</b> {PRODUCT_VERSION} — <i>{PRODUCT_TAGLINE}</i></span>'
        f'<span class="piq-mono" style="font-size:0.75rem;">Model A SHA-256: Bat {html.escape(batter_sha[:12])}… | Bowl {html.escape(bowler_sha[:12])}…</span>'
        f'</footer>',
        unsafe_allow_html=True,
    )


def render_sidebar_brand() -> None:
    """Render crisp sidebar masthead cleanly above navigation radio."""
    st.sidebar.markdown(
        f'<div class="piq-brand">'
        f'{render_brand_emblem()}'
        f'<div><div class="piq-brand-name">{PRODUCT_NAME}</div>'
        f'<div class="piq-brand-sub">Cricket Telemetry &amp; Scouting</div></div></div>',
        unsafe_allow_html=True,
    )
