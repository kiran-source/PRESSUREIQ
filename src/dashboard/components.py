"""Reusable accessible UI components & inline SVG icon primitives for PRESSUREIQ v4 Editorial.

Warm Ivory (#F8F4EC) + Soft Cream (#F1E9DD) + Terracotta (#BD6548) + Deep Ink (#282321)
"""

from __future__ import annotations

import html
from typing import Any, Dict, List, Optional, Sequence
import urllib.parse
import streamlit as st

from src.dashboard.design_tokens import (
    FONTS,
    NAV_GROUPS,
    PALETTE,
    PRODUCT_NAME,
    PRODUCT_TAGLINE,
    PRODUCT_VERSION,
    RETENTION_DEADLINE_DATE,
    SNAPSHOT_ANCHOR_DATE,
    STATUS_TONES,
)

_SVG_PATHS: Dict[str, str] = {
    # Lucide icons mapped to v4.1 navigation specification
    "layout-dashboard": '<rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/>',
    "trophy": '<path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/>',
    "trending-up": '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>',
    "user-round-search": '<circle cx="10" cy="8" r="5"/><path d="M2 21a8 8 0 0 1 10.434-7.62"/><circle cx="18" cy="18" r="3"/><path d="m22 22-1.9-1.9"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "chart-no-axes-combined": '<path d="M12 16v5"/><path d="M16 14v7"/><path d="M20 10v11"/><path d="m22 3-8.646 8.646a.5.5 0 0 1-.708 0L9.354 8.354a.5.5 0 0 0-.707 0L2 15"/><path d="M4 18v3"/><path d="M8 14v7"/>',
    "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/>',
    "activity": '<path d="M22 12h-2.48a2 2 0 0 0-1.93 1.46l-2.35 8.36a.25.25 0 0 1-.48 0L9.24 2.18a.25.25 0 0 0-.48 0l-2.35 8.36A2 2 0 0 1 4.48 12H2"/>',
    "flask-conical": '<path d="M14 2v6a2 2 0 0 0 .245.96l5.51 10.08A2 2 0 0 1 18 22H6a2 2 0 0 1-1.755-2.96l5.51-10.08A2 2 0 0 0 10 8V2"/><path d="M6.453 15h11.094"/><path d="M8.5 2h7"/>',
    "database": '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/><path d="M3 12c0 1.66 4 3 9 3s9-1.34 9-3"/>',
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',

    # Preserved backward-compatible icon aliases
    "overview": '<rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/>',
    "user": '<circle cx="10" cy="8" r="5"/><path d="M2 21a8 8 0 0 1 10.434-7.62"/><circle cx="18" cy="18" r="3"/><path d="m22 22-1.9-1.9"/>',
    "compare": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "sparkles": '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>',
    "briefcase": '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
    "book": '<path d="M14 2v6a2 2 0 0 0 .245.96l5.51 10.08A2 2 0 0 1 18 22H6a2 2 0 0 1-1.755-2.96l5.51-10.08A2 2 0 0 0 10 8V2"/><path d="M6.453 15h11.094"/><path d="M8.5 2h7"/>',
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
    """Render refined compact editorial sidebar brand header (User Requirements Section 2)."""
    st.sidebar.markdown(
        f"""
        <div class="piq-sb-brand">
            <div class="piq-sb-brand-header">
                <div class="piq-sb-emblem">
                    <svg width="30" height="30" viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                        <circle cx="15" cy="15" r="13.5" fill="#FAF6F0" stroke="#BD6548" stroke-width="1.5"/>
                        <path d="M10.5 5.5C13.5 9 13.5 21 10.5 24.5" stroke="#BD6548" stroke-width="1.2" stroke-linecap="round"/>
                        <path d="M19.5 5.5C16.5 9 16.5 21 19.5 24.5" stroke="#BD6548" stroke-width="1.2" stroke-linecap="round"/>
                        <circle cx="15" cy="15" r="1.6" fill="#C5A46D"/>
                    </svg>
                </div>
                <div class="piq-sb-brand-text">
                    <div class="piq-sb-title">{PRODUCT_NAME}</div>
                    <div class="piq-sb-sub">CRICKET INTELLIGENCE</div>
                </div>
            </div>
            <div class="piq-sb-brand-divider"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_lookup(bundle: Any) -> None:
    """Render compact polished player search & profile launcher in sidebar (User Requirements Section 3)."""
    st.sidebar.markdown(
        f"""
        <div class="piq-sb-section-head">
            {svg_icon("search", 13, "#77675D")}
            <span>PLAYER LOOKUP</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    bat_names = [f"{n} (Bat)" for n in bundle.bat_df["player_name"].tolist()] if not bundle.bat_df.empty else []
    bowl_names = [f"{n} (Bowl)" for n in bundle.bowl_df["player_name"].tolist()] if not bundle.bowl_df.empty else []
    jump_opts = ["Select player to inspect…"] + bat_names + bowl_names

    quick_pick = st.sidebar.selectbox(
        "Select Player",
        jump_opts,
        index=0,
        key="global_quick_pick",
        label_visibility="collapsed",
    )
    if quick_pick != "Select player to inspect…":
        is_bat_pick = quick_pick.endswith(" (Bat)")
        disc_val = "Batting" if is_bat_pick else "Bowling"
        pname_val = quick_pick[:-6] if is_bat_pick else quick_pick[:-7]
        st.session_state["jump_disc"] = disc_val
        st.session_state["jump_player_name"] = pname_val
        if st.sidebar.button("Open Player Profile →", use_container_width=True, key="global_jump_btn"):
            st.session_state["active_page"] = "Player Intelligence"
            st.session_state["pi_disc"] = disc_val
            st.session_state[f"pi_sel_{disc_val}"] = pname_val
            try:
                st.query_params["page"] = "Player Intelligence"
            except Exception:
                pass
            st.rerun()


def _on_nav_item_click(target_page: str) -> None:
    """Callback to switch page within existing Streamlit session, preserving state (CodeRabbit Pass 9)."""
    st.session_state["active_page"] = target_page
    try:
        st.query_params["page"] = target_page
    except Exception:
        pass


def render_sidebar_navigation(active_page: str) -> None:
    """Render grouped luxury editorial navigation buttons preserving Streamlit session state (User Requirements Sections 4 & 5)."""
    st.sidebar.markdown('<div class="piq-sb-nav" role="navigation" aria-label="Sidebar Navigation">', unsafe_allow_html=True)
    for grp in NAV_GROUPS:
        st.sidebar.markdown(f'<div class="piq-sb-group-label">{html.escape(grp["group"])}</div>', unsafe_allow_html=True)
        for item in grp["items"]:
            is_active = (item["label"] == active_page)
            btn_type = "primary" if is_active else "secondary"
            btn_key = f"sb_nav_btn_{item['id']}"
            mat_icon = item.get("mat_icon")
            st.sidebar.button(
                item["label"],
                key=btn_key,
                icon=mat_icon,
                type=btn_type,
                use_container_width=True,
                help=item.get("subtitle", item["label"]),
                on_click=_on_nav_item_click,
                args=(item["label"],),
            )
    st.sidebar.markdown('</div>', unsafe_allow_html=True)


def render_sidebar_status(frozen_ok: bool) -> None:
    """Render restrained bottom status area in sidebar (User Requirements Section 7)."""
    integrity_dot = (
        '<span class="piq-sb-dot is-valid"></span><span style="color:#2B472A;font-weight:600;">Model A Verified (SHA-256)</span>'
        if frozen_ok
        else '<span class="piq-sb-dot is-invalid"></span><span style="color:#B84A39;font-weight:600;">Integrity Mismatch</span>'
    )
    st.sidebar.markdown(
        f"""
        <div class="piq-sb-status">
            <div class="piq-sb-status-divider"></div>
            <div class="piq-sb-status-row">{integrity_dot}</div>
            <div class="piq-sb-status-grid">
                <div class="piq-sb-status-cell">
                    <span class="piq-sb-status-k">SNAPSHOT</span>
                    <span class="piq-sb-status-v">{SNAPSHOT_ANCHOR_DATE}</span>
                </div>
                <div class="piq-sb-status-cell">
                    <span class="piq-sb-status-k">RETENTION FILING</span>
                    <span class="piq-sb-status-v">{RETENTION_DEADLINE_DATE}</span>
                </div>
            </div>
            <div class="piq-sb-status-footer">
                <span>{PRODUCT_NAME} {PRODUCT_VERSION}</span>
                <span>200,999 Balls · 867 Matches</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
