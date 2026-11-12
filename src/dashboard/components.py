"""Reusable accessible UI components & inline SVG icon primitives for PRESSUREIQ v3."""

from __future__ import annotations

import html
from typing import Dict, List, Optional, Sequence
import streamlit as st

from src.dashboard.design_tokens import (
    PALETTE,
    PRODUCT_NAME,
    PRODUCT_TAGLINE,
    PRODUCT_VERSION,
    RETENTION_DEADLINE_DATE,
    SNAPSHOT_ANCHOR_DATE,
    STATUS_TONES,
)

_SVG_PATHS: Dict[str, str] = {
    "overview": '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/>',
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
        f'fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
        f'aria-hidden="true" style="flex-shrink:0;vertical-align:middle;">{path}</svg>'
    )


def render_brand_emblem() -> str:
    """Author inline vector telemetry emblem for sidebar & hero masthead."""
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32" fill="none" aria-hidden="true">'
        '<rect x="1.5" y="1.5" width="29" height="29" rx="8" fill="#17223B" stroke="#8B5CF6" stroke-opacity="0.65" stroke-width="1.5"/>'
        '<path d="M7 20L12.5 13L17 16.5L24.5 9" stroke="#3B82F6" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>'
        '<circle cx="24.5" cy="9" r="2.2" fill="#14B8A6"/>'
        '<path d="M7 24H25" stroke="#475569" stroke-width="1.3" stroke-linecap="round"/>'
        '</svg>'
    )


def status_badge_html(status: str) -> str:
    """Build accessible badge pill with distinct fill, border, text color, and label."""
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
    """Render sticky context bar with breadcrumb, integrity signal, and market snapshot date."""
    integrity_badge = (
        f'<span class="piq-badge" style="background:rgba(20,184,166,0.16);border:1px solid rgba(45,212,191,0.45);color:#5EEAD4;">'
        f'{svg_icon("check", 12, "#5EEAD4")} Model A Verified (SHA-256)</span>'
        if frozen_ok
        else f'<span class="piq-badge" style="background:rgba(244,63,94,0.18);border:1px solid rgba(251,113,133,0.5);color:#FDA4AF;">'
        f'{svg_icon("alert", 12, "#FDA4AF")} Integrity Mismatch</span>'
    )
    snap_badge = (
        f'<span class="piq-badge" style="background:rgba(59,130,246,0.14);border:1px solid rgba(96,165,250,0.35);color:#93C5FD;">'
        f'Snapshot: {html.escape(snapshot_date)}</span>'
    )
    deadline_badge = (
        f'<span class="piq-badge" style="background:rgba(245,158,11,0.14);border:1px solid rgba(251,191,36,0.38);color:#FDE68A;">'
        f'IPL Retention Filing: {RETENTION_DEADLINE_DATE}</span>'
    )
    st.markdown(
        f'<div class="piq-topbar" role="banner">'
        f'<div class="piq-crumb"><span class="piq-crumb-muted">{PRODUCT_NAME}</span>'
        f'<span class="piq-crumb-muted">/</span><span>{html.escape(page_label)}</span></div>'
        f'<div class="piq-meta-strip">{integrity_badge}{snap_badge}{deadline_badge}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_hero_banner(title: str, tagline: str, description: str, pills: Optional[Sequence[str]] = None) -> None:
    """Render clean hero surface matching DESIGN_SYSTEM.md."""
    pill_html = "".join(status_badge_html(p) for p in (pills or []))
    st.markdown(
        f'<section class="piq-hero" aria-label="Dashboard Overview">'
        f'<div class="piq-hero-top">'
        f'<div style="display:flex;align-items:flex-start;gap:14px;">'
        f'<div style="padding-top:3px;">{render_brand_emblem()}</div>'
        f'<div>'
        f'<h1 class="piq-hero-title">{html.escape(title)}</h1>'
        f'<p class="piq-hero-tagline">{html.escape(tagline)}</p>'
        f'<p class="piq-hero-desc">{html.escape(description)}</p>'
        f'</div></div>'
        f'<div style="display:flex;flex-wrap:wrap;gap:6px;">{pill_html}</div>'
        f'</div></section>',
        unsafe_allow_html=True,
    )


def render_kpi_grid(cards: List[Dict[str, str]]) -> None:
    """Render responsive CSS Grid of KPI cards (4-column desktop -> 2 tablet -> 1 mobile)."""
    items = []
    for c in cards:
        accent = c.get("accent", PALETTE["accent_violet"])
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
    """Render structured section header with clear vertical hierarchy."""
    sub_html = f'<p class="piq-sec-sub">{html.escape(subtitle)}</p>' if subtitle else ""
    st.markdown(
        f'<div class="piq-sec-head">'
        f'<h2 class="piq-sec-title">{svg_icon(icon, 17, PALETTE["accent_violet_soft"])}<span>{html.escape(title)}</span></h2>'
        f'{sub_html}</div>',
        unsafe_allow_html=True,
    )


def render_callout(body_html: str, accent: str = PALETTE["accent_blue"]) -> None:
    """Render informative callout notice panel."""
    st.markdown(
        f'<div class="piq-callout" style="--callout-accent:{accent};">{body_html}</div>',
        unsafe_allow_html=True,
    )


def render_empty_state(heading: str, guidance: str) -> None:
    """Render helpful empty state instead of blank containers."""
    st.markdown(
        f'<div class="piq-empty">'
        f'<div style="font-weight:600;font-size:1rem;color:#F8FAFC;margin-bottom:6px;">{html.escape(heading)}</div>'
        f'<div style="font-size:0.86rem;color:#94A3B8;">{html.escape(guidance)}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_footer(batter_sha: str, bowler_sha: str) -> None:
    """Render compact footer with version and immutable Model A checksum provenance."""
    st.markdown(
        f'<footer class="piq-footer">'
        f'<span>{PRODUCT_NAME} {PRODUCT_VERSION} — {PRODUCT_TAGLINE}</span>'
        f'<span class="piq-mono">Frozen Model A SHA-256: Bat {html.escape(batter_sha[:12])}… | Bowl {html.escape(bowler_sha[:12])}… | Zero Raw CSV Exposure</span>'
        f'</footer>',
        unsafe_allow_html=True,
    )


def render_sidebar_brand() -> None:
    """Render crisp sidebar masthead cleanly above navigation radio."""
    st.sidebar.markdown(
        f'<div style="display:flex;align-items:center;gap:10px;padding:4px 2px 12px 2px;border-bottom:1px solid rgba(148,163,184,0.16);margin-bottom:10px;">'
        f'{render_brand_emblem()}'
        f'<div><div style="font-weight:700;font-size:1.05rem;color:#F8FAFC;letter-spacing:-0.01em;">{PRODUCT_NAME}</div>'
        f'<div style="font-size:0.74rem;color:#94A3B8;">Cricket Telemetry &amp; Scouting</div></div></div>',
        unsafe_allow_html=True,
    )

