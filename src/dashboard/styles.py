"""Global Editorial Luxury CSS system for PRESSUREIQ v5.

Warm Ivory (#F8F4EC) + Soft Cream (#F1E9DD) + Terracotta (#BD6548) + Deep Ink (#282321)
Kinfolk / Contemporary Luxury Editorial Magazine Aesthetics

Drop-in replacement: same public API (`inject_global_styles`) and every existing
`piq-*` class name is preserved. Only the look changes.
"""

from __future__ import annotations

import streamlit as st
from src.dashboard.design_tokens import FONTS, PALETTE

# Subtle paper-grain texture (percent-encoded SVG, ~5% opacity) for an editorial print feel.
_PAPER_GRAIN = (
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='180'%3E"
    "%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' "
    "stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 .16 0 0 0 0 .14 0 0 0 0 .13 0 0 0 .055 0'/%3E"
    "%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E"
)


def _root_vars() -> str:
    """CSS custom properties sourced from the shared design tokens (f-string kept tiny on purpose)."""
    return f"""
:root {{
    --bg-canvas: {PALETTE['bg_canvas']};
    --bg-sidebar: {PALETTE['bg_sidebar']};
    --bg-surface: {PALETTE['bg_surface']};
    --bg-surface-raised: {PALETTE['bg_surface_raised']};
    --bg-surface-subtle: {PALETTE['bg_surface_subtle']};
    --bg-deep: {PALETTE['bg_deep']};
    --border-subtle: {PALETTE['border_subtle']};
    --border-card: {PALETTE['border_card']};
    --border-strong: {PALETTE['border_strong']};
    --text-primary: {PALETTE['text_primary']};
    --text-secondary: {PALETTE['text_secondary']};
    --text-muted: {PALETTE['text_muted']};
    --text-inverse: {PALETTE['text_inverse']};
    --accent-terracotta: {PALETTE['accent_terracotta']};
    --accent-terracotta-hover: {PALETTE['accent_terracotta_hover']};
    --accent-gold: {PALETTE['accent_gold']};
    --accent-sage: {PALETTE['accent_sage']};
    --positive: {PALETTE['positive']};
    --warning: {PALETTE['warning']};
    --danger: {PALETTE['danger']};
    --font-serif: {FONTS['display']};
    --font-sans: {FONTS['body']};
    --font-mono: {FONTS['mono']};
}}
"""


_STATIC_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,500;1,600&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --ink-soft: #3A322E;
    --paper: #FFFFFF;
    --paper-warm: #FFFDF9;
    --shadow-sm: 0 1px 2px rgba(40, 35, 33, 0.04), 0 2px 8px rgba(40, 35, 33, 0.035);
    --shadow-md: 0 2px 4px rgba(40, 35, 33, 0.03), 0 10px 28px rgba(40, 35, 33, 0.06);
    --shadow-lg: 0 4px 8px rgba(40, 35, 33, 0.04), 0 18px 44px rgba(189, 101, 72, 0.12);
    --radius-md: 12px;
    --radius-lg: 16px;
    --radius-xl: 22px;
    --ease: cubic-bezier(0.22, 0.8, 0.28, 1);
}

/* ---------- Motion primitives ---------- */
@keyframes piq-rise {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes piq-pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(132, 146, 122, 0.55); }
    50%      { box-shadow: 0 0 0 5px rgba(132, 146, 122, 0); }
}

/* ---------- Canvas ---------- */
html, body, [class*="stAppViewContainer"], .stApp {
    font-family: var(--font-sans);
    background-color: var(--bg-canvas);
    color: var(--text-primary);
    scroll-padding-top: 72px;
    overflow-x: hidden;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-rendering: optimizeLegibility;
    font-feature-settings: "kern" 1, "liga" 1;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(1100px 520px at 96% -8%, rgba(189, 101, 72, 0.085), transparent 70%),
        radial-gradient(900px 460px at 4% 10%, rgba(197, 164, 109, 0.10), transparent 62%),
        radial-gradient(800px 500px at 60% 110%, rgba(132, 146, 122, 0.06), transparent 65%),
        var(--bg-canvas);
}
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    inset: 0;
    background-image: url("__GRAIN__");
    pointer-events: none;
    z-index: 0;
    opacity: 0.9;
}

[data-testid="stHeader"] {
    background: rgba(248, 244, 236, 0.80);
    -webkit-backdrop-filter: blur(14px) saturate(1.1);
    backdrop-filter: blur(14px) saturate(1.1);
    border-bottom: 1px solid var(--border-subtle);
}

/* Quiet the default Deploy chrome so the publication feels like a product, not a dev server */
[data-testid="stAppDeployButton"], .stDeployButton { display: none !important; }

.main .block-container,
[data-testid="stMainBlockContainer"] {
    padding-top: 4.4rem;
    padding-bottom: 3.6rem;
    padding-left: 2rem;
    padding-right: 2rem;
    max-width: 1440px;
}

/* ---------- Sidebar Dimensions & Shell (270–290px desktop) ---------- */
section[data-testid="stSidebar"] {
    background: #F1E9DD !important;
    border-right: 1px solid var(--border-card) !important;
    box-shadow: 1px 0 0 rgba(255, 255, 255, 0.7) inset, 4px 0 16px rgba(40, 35, 33, 0.03) !important;
}
section[data-testid="stSidebar"][aria-expanded="true"] {
    width: 280px !important;
    min-width: 270px !important;
    max-width: 290px !important;
}
section[data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
    padding-top: 1.2rem !important;
    padding-bottom: 1.5rem !important;
    padding-left: 0.95rem !important;
    padding-right: 0.95rem !important;
    width: 280px !important;
}

/* Hide default st.radio widgets in sidebar */
section[data-testid="stSidebar"] div[data-testid="stRadio"] {
    display: none !important;
}

/* ---------- Brand Header (Section 2) ---------- */
.piq-sb-brand {
    padding-bottom: 10px;
    margin-bottom: 12px;
    position: relative;
}
.piq-sb-brand-header {
    display: flex;
    align-items: center;
    gap: 10px;
}
.piq-sb-emblem {
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
}
.piq-sb-brand-text {
    display: flex;
    flex-direction: column;
}
.piq-sb-title {
    font-family: var(--font-serif);
    font-size: 1.25rem;
    font-weight: 700;
    color: #282321;
    letter-spacing: -0.015em;
    line-height: 1.1;
}
.piq-sb-sub {
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #77675D;
    margin-top: 3px;
}
.piq-sb-brand-divider {
    height: 1px;
    background: var(--border-card);
    margin-top: 12px;
    position: relative;
}
.piq-sb-brand-divider::after {
    content: "";
    position: absolute;
    left: 0;
    top: -1px;
    width: 44px;
    height: 2px;
    background: linear-gradient(90deg, var(--accent-terracotta), var(--accent-gold));
    border-radius: 2px;
}

/* ---------- Quick Player Lookup (Section 3) ---------- */
.piq-sb-section-head {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #77675D;
    margin-bottom: 6px;
    margin-left: 2px;
}
section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    min-height: 36px !important;
    height: 36px !important;
    font-size: 0.84rem !important;
    border-radius: 8px !important;
    background: #FFFFFF !important;
    border: 1px solid var(--border-card) !important;
    box-shadow: 0 1px 2px rgba(40, 35, 33, 0.04) !important;
}

/* ---------- Navigation Structure & Custom Items (Sections 4 & 5) ---------- */
.piq-sb-nav {
    display: flex;
    flex-direction: column;
    margin-top: 10px;
    margin-bottom: 14px;
}
.piq-sb-group-label {
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #8C7C72;
    padding: 10px 6px 4px 6px;
    user-select: none;
}

/* Sidebar navigation buttons (replaces default button look with editorial pills) */
section[data-testid="stSidebar"] div.stButton > button {
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
    text-align: left !important;
    gap: 10px !important;
    min-height: 36px !important;
    height: 36px !important;
    padding: 0 10px !important;
    border-radius: 8px !important;
    font-size: 0.84rem !important;
    font-weight: 500 !important;
    line-height: 1.3 !important;
    border: 1px solid transparent !important;
    border-left: 3px solid transparent !important;
    background: transparent !important;
    color: #282321 !important;
    box-shadow: none !important;
    transition: all 160ms var(--ease) !important;
    width: 100% !important;
    margin-bottom: 2px !important;
}
section[data-testid="stSidebar"] div.stButton > button p {
    font-size: 0.84rem !important;
    color: #282321 !important;
    margin: 0 !important;
}

/* Inactive button hover */
section[data-testid="stSidebar"] div.stButton > button:hover {
    background: rgba(234, 225, 213, 0.75) !important;
    border-color: rgba(216, 203, 190, 0.5) !important;
    border-left-color: var(--accent-terracotta) !important;
    color: #282321 !important;
    transform: translateX(2px) !important;
    box-shadow: none !important;
}

/* Active primary navigation button */
section[data-testid="stSidebar"] div.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #FFFFFF 0%, #FAF6F0 100%) !important;
    border: 1px solid #D8CBBE !important;
    border-left: 3px solid var(--accent-terracotta) !important;
    color: #282321 !important;
    font-weight: 600 !important;
    box-shadow: 0 1px 3px rgba(40, 35, 33, 0.05) !important;
    transform: none !important;
}
section[data-testid="stSidebar"] div.stButton > button[kind="primary"] p {
    font-weight: 600 !important;
    color: #282321 !important;
}

/* Material symbol icons inside sidebar buttons */
section[data-testid="stSidebar"] div.stButton > button span[data-testid="stIconMaterial"] {
    font-size: 17px !important;
    color: #77675D !important;
    transition: color 140ms var(--ease) !important;
}
section[data-testid="stSidebar"] div.stButton > button[kind="primary"] span[data-testid="stIconMaterial"] {
    color: var(--accent-terracotta) !important;
}

/* Distinct styling for Open Player Profile launcher button (CodeRabbit Pass 10) */
section[data-testid="stSidebar"] div.st-key-global_jump_btn button {
    background: #BD6548 !important;
    border: 1px solid #BD6548 !important;
    border-left: 1px solid #BD6548 !important;
    color: #FFFFFF !important;
    justify-content: center !important;
    text-align: center !important;
    font-weight: 600 !important;
    margin-top: 4px !important;
    box-shadow: 0 2px 6px rgba(189, 101, 72, 0.22) !important;
}
section[data-testid="stSidebar"] div.st-key-global_jump_btn button p {
    color: #FFFFFF !important;
    font-weight: 600 !important;
}
section[data-testid="stSidebar"] div.st-key-global_jump_btn button:hover {
    background: #A94F36 !important;
    border-color: #A94F36 !important;
    color: #FFFFFF !important;
    transform: translateY(-1px) !important;
}

/* ---------- Bottom Status Area (Section 7) ---------- */
.piq-sb-status {
    margin-top: auto;
    padding-top: 10px;
    border-top: 1px solid var(--border-card);
    font-size: 0.75rem;
    color: var(--text-secondary);
}
.piq-sb-status-divider {
    height: 1px;
    background: var(--border-subtle);
    margin-bottom: 8px;
}
.piq-sb-status-row {
    display: flex;
    align-items: center;
    gap: 7px;
    font-size: 0.75rem;
    margin-bottom: 8px;
}
.piq-sb-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    flex-shrink: 0;
}
.piq-sb-dot.is-valid {
    background: #5B7B5A;
    box-shadow: 0 0 0 3px rgba(91, 123, 90, 0.18);
}
.piq-sb-dot.is-invalid {
    background: #B84A39;
    box-shadow: 0 0 0 3px rgba(184, 74, 57, 0.18);
}
.piq-sb-status-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6px;
    background: rgba(255, 255, 255, 0.45);
    border: 1px solid var(--border-card);
    border-radius: 8px;
    padding: 7px 9px;
    margin-bottom: 8px;
}
.piq-sb-status-cell {
    display: flex;
    flex-direction: column;
}
.piq-sb-status-k {
    font-size: 0.58rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #8C7C72;
}
.piq-sb-status-v {
    font-family: var(--font-mono);
    font-size: 0.73rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-top: 1px;
}
.piq-sb-status-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.68rem;
    color: #8C7C72;
    padding: 2px 2px;
}

/* ---------- Collapsible Toggle & Responsive Media Queries (Sections 8 & 9) ---------- */
button[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarCollapseButton"] button {
    color: var(--text-secondary) !important;
    background: #FAF6F0 !important;
    border: 1px solid var(--border-card) !important;
    border-radius: 8px !important;
    transition: all 160ms var(--ease) !important;
}
button[data-testid="stSidebarCollapseButton"]:hover,
[data-testid="stSidebarCollapseButton"] button:hover {
    color: var(--accent-terracotta) !important;
    background: #FFFFFF !important;
    border-color: var(--accent-terracotta) !important;
}

@media (max-width: 1024px) and (min-width: 768px) {
    section[data-testid="stSidebar"][aria-expanded="true"] {
        width: 260px !important;
        min-width: 250px !important;
        max-width: 270px !important;
    }
    section[data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 260px !important;
        padding-left: 0.85rem !important;
        padding-right: 0.85rem !important;
    }
}

@media (max-width: 767px) {
    section[data-testid="stSidebar"][aria-expanded="true"] {
        width: 280px !important;
        max-width: 85vw !important;
        box-shadow: 0 0 24px rgba(40, 35, 33, 0.35) !important;
    }
    section[data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 100% !important;
    }
}

/* ---------- Selection, scrollbars, focus ---------- */
::selection {
    background: rgba(189, 101, 72, 0.22);
    color: var(--text-primary);
}
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: #F1E9DD; }
::-webkit-scrollbar-thumb {
    background: #D8CBBE;
    border-radius: 6px;
    border: 2px solid #F1E9DD;
}
::-webkit-scrollbar-thumb:hover { background: #BD6548; }

button:focus-visible, a:focus-visible, input:focus-visible, select:focus-visible,
[role="tab"]:focus-visible, [data-baseweb="select"]:focus-within {
    outline: 2px solid var(--accent-terracotta) !important;
    outline-offset: 2px !important;
}

/* ---------- Typography ---------- */
h1, h2, h3, h4 {
    font-family: var(--font-serif);
    color: var(--text-primary);
    letter-spacing: -0.015em;
    font-weight: 600;
}
.main .block-container h1:not(.piq-hero-title),
[data-testid="stMainBlockContainer"] h1:not(.piq-hero-title) {
    font-family: var(--font-serif) !important;
    font-size: 2.1rem !important;
    font-weight: 600 !important;
    line-height: 1.2 !important;
    color: var(--text-primary) !important;
    margin-bottom: 0.4rem !important;
}
.piq-serif { font-family: var(--font-serif) !important; }
.piq-mono, code {
    font-family: var(--font-mono) !important;
    font-variant-numeric: tabular-nums;
}
code {
    background: #F1E9DD;
    color: #8C3F27;
    border-radius: 5px;
    padding: 0.1em 0.4em;
}

/* ---------- Inputs ---------- */
div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border-color: var(--border-card) !important;
    color: var(--text-primary) !important;
    border-radius: 10px !important;
    min-height: 44px;
    box-shadow: var(--shadow-sm);
    transition: border-color 140ms var(--ease), box-shadow 140ms var(--ease);
}
div[data-baseweb="select"] > div:hover {
    border-color: var(--border-strong) !important;
}
div[data-baseweb="select"]:focus-within > div {
    border-color: var(--accent-terracotta) !important;
    box-shadow: 0 0 0 3px rgba(189, 101, 72, 0.14);
}
input[type="text"], input[type="number"], textarea {
    background-color: #FFFFFF !important;
    border-color: var(--border-card) !important;
    color: var(--text-primary) !important;
    border-radius: 10px !important;
}
span[data-baseweb="tag"] {
    background-color: #F6E7DF !important;
    color: #8C3F27 !important;
    border-radius: 6px !important;
    font-weight: 600;
}

/* ---------- Top navigation strip ---------- */
.piq-topbar {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 12px 18px;
    padding: 12px 20px;
    background: linear-gradient(135deg, #2E2825 0%, #282321 55%, #1F1A18 100%);
    border: 1px solid rgba(197, 164, 109, 0.20);
    border-radius: 14px;
    margin-bottom: 20px;
    box-shadow: 0 8px 24px rgba(40, 35, 33, 0.16), 0 1px 0 rgba(255, 255, 255, 0.05) inset;
    animation: piq-rise 0.5s var(--ease) both;
}
.piq-crumb {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    font-size: 0.88rem;
    font-weight: 500;
    color: #F8F4EC;
    letter-spacing: 0.04em;
}
.piq-crumb-muted {
    color: #BFB0A2;
    font-weight: 400;
}
.piq-meta-strip {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 8px;
}
.piq-topbar .piq-badge {
    font-size: 0.72rem;
    padding: 4px 11px;
    backdrop-filter: blur(4px);
}

/* ---------- Hero ---------- */
.piq-hero {
    background: linear-gradient(180deg, #FFFFFF 0%, #FFFDF9 100%);
    border: 1px solid var(--border-card);
    border-radius: var(--radius-xl);
    padding: 40px 44px 34px 44px;
    margin-bottom: 26px;
    box-shadow: var(--shadow-md);
    position: relative;
    overflow: hidden;
    animation: piq-rise 0.65s var(--ease) 0.05s both;
}
.piq-hero::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #BD6548 0%, #C5A46D 55%, rgba(197, 164, 109, 0) 100%);
    z-index: 2;
}
/* "Pressure ripple" motif: concentric rings radiating from the corner */
.piq-hero::after {
    content: "";
    position: absolute;
    top: -150px;
    right: -150px;
    width: 560px;
    height: 560px;
    border-radius: 50%;
    background:
        radial-gradient(circle, rgba(189, 101, 72, 0.10), transparent 62%),
        repeating-radial-gradient(circle, transparent 0 34px, rgba(189, 101, 72, 0.075) 34px 35px);
    -webkit-mask-image: radial-gradient(circle, #000 22%, transparent 70%);
    mask-image: radial-gradient(circle, #000 22%, transparent 70%);
    pointer-events: none;
}
.piq-hero > * { position: relative; z-index: 1; }

.piq-hero-eyebrow {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--accent-terracotta);
    margin-bottom: 18px;
    display: inline-flex;
    align-items: center;
    gap: 10px;
}
.stApp h1.piq-hero-title,
.piq-hero-title {
    font-family: 'Playfair Display', Georgia, serif !important;
    font-size: clamp(2.5rem, 4.2vw, 3.9rem) !important;
    font-weight: 700 !important;
    line-height: 1.04 !important;
    margin: 0 0 10px 0 !important;
    padding: 0 !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.035em !important;
}
.piq-hero-tagline {
    font-family: 'Playfair Display', Georgia, serif;
    font-style: italic;
    font-size: clamp(1.15rem, 1.6vw, 1.5rem);
    color: #8C3F27;
    margin: 0 0 18px 0;
    font-weight: 400;
}
.piq-hero-desc {
    font-size: 0.98rem;
    line-height: 1.72;
    color: var(--text-secondary);
    max-width: 68ch;
    margin: 0 0 22px 0;
}
.piq-hero-stats {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    padding-top: 18px;
    border-top: 1px solid var(--border-subtle);
}

/* Featured player cards (hero, right column) */
.piq-feature-col {
    display: flex;
    flex-direction: column;
    gap: 14px;
}
.piq-feature {
    --feat-accent: #BD6548;
    --feat-score: #BD6548;
    position: relative;
    background: linear-gradient(135deg, #FFFFFF 0%, #FAF6F0 100%);
    border: 1px solid var(--border-card);
    border-left: 4px solid var(--feat-accent);
    border-radius: 14px;
    padding: 16px 20px 16px 20px;
    box-shadow: var(--shadow-sm);
    transition: transform 200ms var(--ease), box-shadow 200ms var(--ease);
}
.piq-feature:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}
.piq-feature-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
    margin-bottom: 6px;
}
.piq-feature-label {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #77675D;
}
.piq-feature-name {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.5rem;
    font-weight: 600;
    color: #282321;
    letter-spacing: -0.01em;
    line-height: 1.2;
}
.piq-feature-name.is-empty {
    font-size: 1.15rem;
    color: #77675D;
}
.piq-feature-meta {
    display: flex;
    align-items: baseline;
    flex-wrap: wrap;
    gap: 4px 10px;
    margin-top: 6px;
}
.piq-feature-score {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.9rem;
    font-weight: 700;
    color: var(--feat-score);
    line-height: 1;
    font-variant-numeric: lining-nums tabular-nums;
}
.piq-feature-note {
    font-size: 0.78rem;
    color: #77675D;
}

/* ---------- KPI cards ---------- */
.piq-kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 16px;
    margin-bottom: 26px;
}
.piq-kpi {
    position: relative;
    background: linear-gradient(180deg, #FFFFFF 0%, #FFFDFA 100%);
    border: 1px solid var(--border-card);
    border-top: 3px solid var(--kpi-accent, #BD6548);
    border-radius: 14px;
    padding: 18px 20px 18px 20px;
    box-shadow: var(--shadow-sm);
    transition: transform 200ms var(--ease), box-shadow 200ms var(--ease), border-color 200ms var(--ease);
    animation: piq-rise 0.55s var(--ease) both;
    min-width: 0;
}
.piq-kpi:nth-child(1) { animation-delay: 0.08s; }
.piq-kpi:nth-child(2) { animation-delay: 0.14s; }
.piq-kpi:nth-child(3) { animation-delay: 0.20s; }
.piq-kpi:nth-child(4) { animation-delay: 0.26s; }
.piq-kpi:nth-child(5) { animation-delay: 0.32s; }
.piq-kpi:nth-child(6) { animation-delay: 0.38s; }
.piq-kpi:hover {
    border-color: var(--border-strong);
    box-shadow: var(--shadow-lg);
    transform: translateY(-3px);
}
.piq-kpi-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-muted);
    line-height: 1.5;
}
.piq-kpi-head svg {
    box-sizing: content-box;
    padding: 7px;
    border-radius: 10px;
    background: rgba(189, 101, 72, 0.10);
    background: color-mix(in srgb, var(--kpi-accent, #BD6548) 13%, transparent);
}
.piq-kpi-val {
    font-family: var(--font-serif);
    font-size: clamp(1.45rem, 1.2vw + 0.95rem, 1.95rem);
    font-weight: 600;
    color: var(--text-primary);
    margin-top: 10px;
    line-height: 1.15;
    letter-spacing: -0.01em;
    font-variant-numeric: lining-nums tabular-nums;
    text-wrap: balance;
    overflow-wrap: anywhere;
}
.piq-kpi-sub {
    font-size: 0.82rem;
    color: var(--text-secondary);
    margin-top: 8px;
    line-height: 1.5;
}

/* ---------- Section headers ---------- */
.piq-sec-head {
    margin-top: 32px;
    margin-bottom: 16px;
    padding-bottom: 12px;
    position: relative;
    border-bottom: 1px solid var(--border-card);
}
.piq-sec-head::after {
    content: "";
    position: absolute;
    left: 0;
    bottom: -1px;
    width: 64px;
    height: 2px;
    background: linear-gradient(90deg, var(--accent-terracotta), var(--accent-gold));
    border-radius: 2px;
}
.stApp h2.piq-sec-title,
.piq-sec-title {
    font-family: var(--font-serif) !important;
    font-size: 1.45rem !important;
    font-weight: 600 !important;
    line-height: 1.25 !important;
    letter-spacing: -0.015em !important;
    color: var(--text-primary) !important;
    margin: 0 !important;
    padding: 0 !important;
    display: flex;
    align-items: center;
    gap: 10px;
}
.piq-sec-title svg {
    box-sizing: content-box;
    padding: 7px;
    border-radius: 10px;
    background: rgba(189, 101, 72, 0.10);
}
.piq-sec-sub {
    font-size: 0.88rem;
    color: var(--text-secondary);
    margin: 8px 0 0 0;
    line-height: 1.55;
    max-width: 90ch;
}

/* ---------- Callouts, empty states, captions ---------- */
.piq-callout {
    background: linear-gradient(135deg, #FBF7F1 0%, #F8F1E7 100%);
    border: 1px solid var(--border-card);
    border-left: 4px solid var(--callout-accent, #BD6548);
    border-radius: 12px;
    padding: 16px 20px;
    font-size: 0.9rem;
    line-height: 1.65;
    color: var(--text-primary);
    margin-bottom: 18px;
    box-shadow: var(--shadow-sm);
}
.piq-empty {
    background:
        repeating-linear-gradient(135deg, rgba(216, 203, 190, 0.14) 0 8px, transparent 8px 16px),
        #FFFFFF;
    border: 1px dashed var(--border-strong);
    border-radius: var(--radius-lg);
    padding: 34px 24px;
    text-align: center;
    color: var(--text-secondary);
    margin: 14px 0;
}
.piq-chart-caption {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    font-size: 0.84rem;
    color: var(--text-secondary);
    line-height: 1.55;
    margin-top: -4px;
    margin-bottom: 20px;
    padding: 10px 14px;
    background: #FBF7F1;
    border: 1px solid var(--border-subtle);
    border-left: 3px solid var(--accent-terracotta);
    border-radius: 8px;
}
.piq-chart-caption b {
    color: var(--text-primary);
    font-weight: 700;
    letter-spacing: 0.01em;
}
.piq-chart-caption svg { margin-top: 3px; }

/* ---------- Badges & tape tags ---------- */
.piq-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 3px 11px;
    border-radius: 999px;
    font-size: 0.74rem;
    font-weight: 600;
    letter-spacing: 0.03em;
    line-height: 1.35;
    white-space: nowrap;
}
.piq-tape-tag {
    display: inline-block;
    padding: 5px 11px;
    background: #C5A46D;
    color: #282321;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    border-radius: 4px;
    box-shadow: 0 1px 0 rgba(40, 35, 33, 0.12), 0 4px 10px rgba(197, 164, 109, 0.25);
    transition: transform 160ms var(--ease);
}
.piq-tape-tag:hover { transform: translateY(-1px) rotate(-0.6deg); }

/* ---------- Tables ---------- */
.piq-table-wrap {
    width: 100%;
    overflow-x: auto;
    border: 1px solid var(--border-card);
    border-radius: var(--radius-md);
    background: #FFFFFF;
    margin-bottom: 18px;
    box-shadow: var(--shadow-sm);
}
.piq-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.86rem;
    color: var(--text-primary);
    font-variant-numeric: tabular-nums;
}
.piq-table th {
    background: #F1E9DD;
    color: #282321;
    font-family: var(--font-sans);
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    text-align: left;
    padding: 12px 14px;
    border-bottom: 1px solid var(--border-card);
    white-space: nowrap;
    position: sticky;
    top: 0;
}
.piq-table td {
    padding: 10px 14px;
    border-bottom: 1px solid var(--border-subtle);
    vertical-align: top;
}
.piq-table tbody tr:nth-child(even) td { background: #FDFAF5; }
.piq-table tr:hover td { background: #F8F0E6; }
.piq-table tr:last-child td { border-bottom: none; }

/* ---------- Native Streamlit widgets in the editorial palette ---------- */
button[data-baseweb="tab"] {
    min-height: 44px;
    font-weight: 600;
    color: var(--text-secondary);
    font-size: 0.92rem;
    transition: color 140ms var(--ease), background 140ms var(--ease);
}
button[data-baseweb="tab"]:hover {
    color: var(--text-primary);
    background: rgba(234, 225, 213, 0.45);
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--accent-terracotta) !important;
    border-bottom-color: var(--accent-terracotta) !important;
}
div[data-baseweb="tab-list"] { gap: 6px; }
div[data-baseweb="tab-highlight"] { background-color: var(--accent-terracotta) !important; height: 2px !important; }
div[data-baseweb="tab-border"] { background-color: var(--border-card) !important; }

div.stButton > button, div.stDownloadButton > button {
    min-height: 40px;
    border-radius: 10px;
    border: 1px solid var(--border-card);
    background: #FFFFFF;
    color: var(--text-primary);
    font-weight: 600;
    font-size: 0.86rem;
    box-shadow: var(--shadow-sm);
    transition: all 160ms var(--ease);
}
div.stButton > button:hover, div.stDownloadButton > button:hover {
    background: var(--accent-terracotta);
    border-color: var(--accent-terracotta);
    color: #FFFFFF !important;
    transform: translateY(-1px);
    box-shadow: 0 8px 20px rgba(189, 101, 72, 0.28);
}
div.stButton > button:active, div.stDownloadButton > button:active {
    transform: translateY(0);
}
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #C9704F 0%, #BD6548 55%, #A8553A 100%);
    border-color: #A8553A;
    color: #FFFFFF;
}

[data-testid="stExpander"] details {
    border: 1px solid var(--border-card) !important;
    border-radius: var(--radius-md) !important;
    background: #FFFFFF;
    box-shadow: var(--shadow-sm);
    overflow: hidden;
}
[data-testid="stExpander"] summary {
    font-weight: 600;
}
[data-testid="stExpander"] summary:hover {
    background: #FAF6F0;
}

[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid var(--border-card);
    border-radius: var(--radius-md);
    padding: 14px 18px;
    box-shadow: var(--shadow-sm);
}
[data-testid="stMetricValue"] {
    font-family: var(--font-serif);
    font-weight: 600;
    font-variant-numeric: lining-nums tabular-nums;
}
[data-testid="stMetricLabel"] p {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-muted);
}

[data-testid="stAlert"] {
    border-radius: var(--radius-md);
    border: 1px solid var(--border-card);
}

[data-testid="stPlotlyChart"] {
    background: #FFFFFF;
    border: 1px solid var(--border-card);
    border-radius: var(--radius-lg);
    padding: 12px 10px 4px 10px;
    box-shadow: var(--shadow-sm);
    transition: box-shadow 200ms var(--ease);
}
[data-testid="stPlotlyChart"]:hover {
    box-shadow: var(--shadow-md);
}

[data-testid="stDataFrame"] {
    border: 1px solid var(--border-card);
    border-radius: var(--radius-md);
    overflow: hidden;
    box-shadow: var(--shadow-sm);
}

[data-testid="stCaptionContainer"] {
    color: var(--text-muted);
}
hr {
    border-color: var(--border-subtle) !important;
}

/* ---------- Footer ---------- */
.piq-footer {
    margin-top: 44px;
    padding-top: 18px;
    border-top: 1px solid var(--border-card);
    position: relative;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    gap: 8px 16px;
    font-size: 0.8rem;
    color: var(--text-muted);
}
.piq-footer::before {
    content: "";
    position: absolute;
    left: 0;
    top: -1px;
    width: 64px;
    height: 2px;
    background: linear-gradient(90deg, var(--accent-terracotta), var(--accent-gold));
    border-radius: 2px;
}
.piq-footer b { color: var(--text-secondary); }

/* =====================================================================
   PRESSUREIQ v5.0 — PLAYER VISUAL INTELLIGENCE STYLES
   ===================================================================== */

/* ---------- Player Profile Hero ---------- */
.piq-player-hero {
    position: relative;
    background: linear-gradient(135deg, #FFFFFF 0%, #FAF6F0 60%, #F5EFE6 100%);
    border: 1px solid var(--border-card);
    border-bottom: 3px solid var(--accent-terracotta);
    border-radius: 20px;
    padding: 30px 34px;
    margin-bottom: 24px;
    box-shadow: 0 4px 20px rgba(40, 35, 33, 0.05);
    overflow: hidden;
}
.piq-player-hero-grid {
    display: flex;
    align-items: center;
    gap: 32px;
    position: relative;
    z-index: 2;
}
.piq-player-hero-portrait-col {
    flex: 0 0 260px;
    max-width: 290px;
    display: flex;
    justify-content: center;
}
.piq-player-hero-portrait-frame {
    position: relative;
    width: 240px;
    height: 240px;
    border-radius: 20px;
    background: radial-gradient(circle at center, #FFFFFF 0%, #F1E9DD 100%);
    border: 2px solid #D8CBBE;
    box-shadow: 0 8px 24px rgba(40, 35, 33, 0.10);
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
}
.piq-player-hero-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center top;
    display: block;
    transition: transform 300ms cubic-bezier(0.16, 1, 0.3, 1);
}
.piq-player-hero-portrait-frame:hover .piq-player-hero-img {
    transform: scale(1.04);
}
.piq-player-hero-rank-medallion {
    position: absolute;
    top: 10px;
    left: 10px;
    background: rgba(40, 35, 33, 0.88);
    backdrop-filter: blur(4px);
    border: 1px solid rgba(197, 164, 109, 0.6);
    color: #F8F4EC;
    padding: 3px 10px;
    border-radius: 999px;
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.18);
}
.piq-rank-num {
    color: #C5A46D;
    font-family: var(--font-mono);
}
.piq-player-hero-id-tag {
    position: absolute;
    bottom: 8px;
    right: 10px;
    background: rgba(248, 244, 236, 0.90);
    backdrop-filter: blur(4px);
    border: 1px solid #D8CBBE;
    color: #77675D;
    padding: 2px 7px;
    border-radius: 4px;
    font-size: 0.62rem;
    font-family: var(--font-mono);
    letter-spacing: 0.06em;
}
.piq-player-hero-dossier-col {
    flex: 1 1 500px;
    min-width: 0;
}
.piq-player-hero-eyebrow {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    color: var(--accent-terracotta);
    text-transform: uppercase;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.piq-player-hero-name {
    font-family: var(--font-serif);
    font-size: 2.25rem;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.15;
    margin: 0 0 8px 0;
    letter-spacing: -0.02em;
}
.piq-player-hero-badges {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 16px;
}
.piq-badge-role {
    background: #FAF0EB;
    border: 1px solid rgba(189, 101, 72, 0.4);
    color: #BD6548;
    font-weight: 600;
}
.piq-badge-team {
    background: #FAF6ED;
    border: 1px solid rgba(197, 164, 109, 0.5);
    color: #75460E;
    font-weight: 600;
}
.piq-badge-market {
    background: #EDF3EC;
    border: 1px solid rgba(91, 123, 90, 0.4);
    color: #385E38;
    font-weight: 600;
}
.piq-player-hero-kpi-banner {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    background: rgba(241, 233, 221, 0.65);
    border: 1px solid rgba(216, 203, 190, 0.8);
    border-radius: 12px;
    padding: 12px 16px;
    margin-bottom: 12px;
}
.piq-hero-kpi-item {
    display: flex;
    flex-direction: column;
}
.piq-hero-kpi-label {
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    color: var(--text-muted);
    text-transform: uppercase;
    margin-bottom: 2px;
}
.piq-hero-kpi-val {
    font-family: var(--font-mono);
    font-size: 1.30rem;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.2;
}
.piq-hero-kpi-sub {
    font-size: 0.70rem;
    color: var(--text-secondary);
    margin-top: 2px;
}
.piq-player-hero-meta-strip {
    display: flex;
    align-items: center;
    gap: 16px;
    font-size: 0.78rem;
    color: var(--text-secondary);
}
.piq-player-hero-meta-strip b {
    color: var(--text-primary);
}
.piq-player-hero-watermark {
    position: absolute;
    right: 20px;
    bottom: -15px;
    font-family: var(--font-serif);
    font-size: 7.5rem;
    font-weight: 800;
    color: rgba(216, 203, 190, 0.20);
    pointer-events: none;
    line-height: 1;
    z-index: 1;
    user-select: none;
}

/* ---------- Leaderboard Featured Podium Cards ---------- */
.piq-podium-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 18px;
    margin-bottom: 24px;
}
.piq-podium-card {
    background: linear-gradient(180deg, #FFFFFF 0%, #FAF6F0 100%);
    border: 1px solid var(--border-card);
    border-radius: 16px;
    padding: 22px 16px 18px 16px;
    text-align: center;
    position: relative;
    box-shadow: 0 4px 14px rgba(40, 35, 33, 0.05);
    transition: transform 200ms cubic-bezier(0.16, 1, 0.3, 1), box-shadow 200ms ease;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.piq-podium-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 22px rgba(40, 35, 33, 0.10);
}
.piq-podium-card.rank-1 {
    border-top: 4px solid var(--accent-gold);
    background: linear-gradient(180deg, #FFFDF9 0%, #FAF6EE 100%);
}
.piq-podium-card.rank-2 {
    border-top: 4px solid var(--accent-terracotta);
}
.piq-podium-card.rank-3 {
    border-top: 4px solid #77675D;
}
.piq-podium-portrait {
    width: 96px;
    height: 96px;
    border-radius: 50%;
    border: 3px solid #D8CBBE;
    object-fit: cover;
    background: #F1E9DD;
    margin-bottom: 10px;
    box-shadow: 0 3px 10px rgba(40, 35, 33, 0.12);
}
.piq-podium-card.rank-1 .piq-podium-portrait {
    border-color: var(--accent-gold);
    width: 108px;
    height: 108px;
}
.piq-podium-card.rank-2 .piq-podium-portrait {
    border-color: var(--accent-terracotta);
}
.piq-podium-badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 999px;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    margin-bottom: 6px;
}
.piq-podium-name {
    font-family: var(--font-serif);
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 4px 0 2px 0;
}
.piq-podium-team {
    font-size: 0.74rem;
    color: var(--text-muted);
    margin-bottom: 8px;
}
.piq-podium-score {
    font-family: var(--font-mono);
    font-size: 1.45rem;
    font-weight: 700;
    color: var(--accent-terracotta);
    line-height: 1;
}
.piq-podium-ci {
    font-size: 0.68rem;
    color: var(--text-secondary);
    margin-top: 4px;
}

/* ---------- Visual Directory & Emerging Gallery Cards ---------- */
.piq-dir-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 16px;
    margin-top: 16px;
}
.piq-dir-card {
    background: #FFFFFF;
    border: 1px solid var(--border-card);
    border-radius: 14px;
    padding: 16px;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    position: relative;
    box-shadow: 0 2px 8px rgba(40, 35, 33, 0.04);
    transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
}
.piq-dir-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(40, 35, 33, 0.08);
    border-color: var(--accent-terracotta);
}
.piq-dir-photo,
.piq-dir-portrait {
    width: 84px;
    height: 84px;
    border-radius: 12px;
    object-fit: cover;
    background: #F1E9DD;
    border: 1px solid #D8CBBE;
    margin-bottom: 10px;
}
.piq-dir-name {
    font-family: var(--font-serif);
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 2px 0;
}
.piq-dir-meta {
    font-size: 0.74rem;
    color: var(--text-muted);
    margin-bottom: 8px;
}
.piq-dir-score-box {
    display: flex;
    align-items: baseline;
    gap: 4px;
    margin-bottom: 6px;
}
.piq-dir-score-val {
    font-family: var(--font-mono);
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--accent-terracotta);
}
.piq-dir-score-label {
    font-size: 0.65rem;
    color: var(--text-muted);
    text-transform: uppercase;
}

/* ---------- Player Comparison Side-by-Side Gallery ---------- */
.piq-compare-gallery {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
    gap: 16px;
    margin-bottom: 24px;
}
.piq-compare-card {
    background: linear-gradient(180deg, #FFFFFF 0%, #FAF6F0 100%);
    border: 1px solid var(--border-card);
    border-top: 4px solid var(--accent-terracotta);
    border-radius: 14px;
    padding: 16px;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    box-shadow: 0 3px 12px rgba(40, 35, 33, 0.05);
}
.piq-compare-portrait {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    object-fit: cover;
    background: #F1E9DD;
    border: 2px solid #D8CBBE;
    margin-bottom: 10px;
    box-shadow: 0 4px 10px rgba(40, 35, 33, 0.10);
}

/* ---------- Emerging Talent Visual Scouting Gallery (v5.0 Section 7) ---------- */
.piq-emerging-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 16px;
    margin-bottom: 24px;
}
.piq-emerging-card {
    background: linear-gradient(180deg, #FFFFFF 0%, #FAF6F0 100%);
    border: 1px solid var(--border-card);
    border-radius: 12px;
    padding: 16px;
    display: flex;
    flex-direction: column;
    box-shadow: 0 2px 6px rgba(40, 35, 33, 0.04);
    transition: transform 160ms var(--ease), box-shadow 160ms var(--ease);
}
.piq-emerging-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(40, 35, 33, 0.08);
    border-color: var(--accent-terracotta);
}
.piq-emerging-portrait {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #D8CBBE;
    background: #F1E9DD;
    box-shadow: 0 3px 8px rgba(40, 35, 33, 0.08);
}
.piq-emerging-badge {
    display: inline-block;
    padding: 3px 8px;
    border-radius: 10px;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

/* ---------- Compact Leaderboard Item ---------- */
.piq-lb-compact-card {
    background: #FFFFFF;
    border: 1px solid var(--border-card);
    border-radius: 10px;
    padding: 10px 14px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 12px;
    transition: all 140ms var(--ease);
}
.piq-lb-compact-card:hover {
    border-color: var(--accent-terracotta);
    box-shadow: 0 2px 8px rgba(40, 35, 33, 0.05);
}
.piq-lb-thumb {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    object-fit: cover;
    border: 1.5px solid var(--border-card);
    background: #F1E9DD;
    flex-shrink: 0;
}

/* ---------- Responsive ---------- */
@media (max-width: 1024px) {
    .main .block-container,
    [data-testid="stMainBlockContainer"] {
        padding-left: 1.25rem;
        padding-right: 1.25rem;
    }
    .piq-hero { padding: 30px 28px 26px 28px; }
    .piq-podium-grid { gap: 12px; }
}
@media (max-width: 767px) {
    .main .block-container,
    [data-testid="stMainBlockContainer"] {
        padding-left: 0.85rem;
        padding-right: 0.85rem;
    }
    .piq-hero { padding: 22px 18px; border-radius: 16px; }
    .piq-hero-title { font-size: 2rem !important; }
    .piq-hero-tagline { font-size: 1.05rem !important; }
    .piq-kpi-grid { grid-template-columns: 1fr; }
    .piq-topbar { padding: 10px 14px; }

    /* Player Profile Hero Mobile Stacking */
    .piq-player-hero { padding: 20px 16px; border-radius: 16px; }
    .piq-player-hero-grid { flex-direction: column; text-align: center; gap: 18px; }
    .piq-player-hero-portrait-col { flex: 0 0 auto; max-width: 100%; }
    .piq-player-hero-portrait-frame { width: 180px; height: 180px; }
    .piq-player-hero-name { font-size: 1.70rem; }
    .piq-player-hero-badges { justify-content: center; }
    .piq-player-hero-kpi-banner { grid-template-columns: 1fr; text-align: center; gap: 10px; }
    .piq-player-hero-meta-strip { justify-content: center; flex-wrap: wrap; gap: 10px; }
    .piq-player-hero-watermark { display: none; }

    /* Podium and Grids Mobile Stacking */
    .piq-podium-grid { grid-template-columns: 1fr; }
    .piq-dir-grid { grid-template-columns: 1fr; }
    .piq-compare-gallery { grid-template-columns: 1fr; }
}

/* ---------- Reduced motion ---------- */
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.001ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.001ms !important;
        scroll-behavior: auto !important;
    }
}
""".replace("__GRAIN__", _PAPER_GRAIN)


def inject_global_styles() -> None:
    """Inject responsive, accessible warm editorial CSS matching Kinfolk luxury reference."""
    st.markdown(f"<style>{_root_vars()}{_STATIC_CSS}</style>", unsafe_allow_html=True)
